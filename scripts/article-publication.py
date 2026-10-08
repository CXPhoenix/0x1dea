#!/usr/bin/env python3
"""Reconstruct local article candidates; this command grants no publication authority."""
import argparse
import hashlib
import html
import json
import os
import posixpath
from pathlib import Path, PurePosixPath
import re
import subprocess
import stat
import sys
import tempfile


BASELINE_ALIASES = {
    'skills/phoenix-writing/reference': b'../../maintenance/writing-skills/legacy/phoenix-writing/reference',
    'skills/phoenix-writing/scripts': b'../maintaining-writing-skills/legacy-validator',
    '.gemini/skills/creating-vitepress-post': b'../../skills/creating-vitepress-post',
}


class Invalid(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2)+'\n').encode()


def git(repo, *args, data=None, env=None):
    # Disable inherited Git redirection, replacement objects and external helpers.
    clean = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
    clean.update({'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':os.devnull,
                  'GIT_NO_REPLACE_OBJECTS':'1','GIT_TERMINAL_PROMPT':'0'})
    if env:
        clean.update(env)
    result = subprocess.run(['git','--no-optional-locks','-C',str(repo),*args],
                            input=data, capture_output=True, env=clean)
    if result.returncode:
        raise Invalid('Git check failed: '+result.stderr.decode('utf-8','replace').strip())
    return result.stdout


def exact(value, keys):
    if not isinstance(value,dict) or set(value)!=set(keys):
        raise Invalid('schema: unknown or missing fields')


def safe_path(value):
    if (not isinstance(value,str) or not value or any(c in value for c in ('\\','\x00','\n','\r','\t','*','?','[',']',':'))
            or PurePosixPath(value).is_absolute() or any(c in ('','.','..','.git') for c in value.split('/'))):
        raise Invalid('schema: unsafe exact path')
    return value


def validate_plan(plan):
    exact(plan,('version','repository','main','staging','articles','dependencies','selected'))
    if type(plan['version']) is not int or plan['version']!=1 or not isinstance(plan['repository'],str) or not Path(plan['repository']).is_absolute():
        raise Invalid('schema: version or absolute repository path')
    for name in ('articles','dependencies','selected'):
        if not isinstance(plan[name],list):
            raise Invalid('schema: list required')
    ids=[]
    for source in plan['articles']+plan['dependencies']:
        exact(source,('id','ref','sha','paths'))
        if not isinstance(source['id'],str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}',source['id']):
            raise Invalid('schema: source id')
        ids.append(source['id'])
        if not isinstance(source['paths'],list) or not source['paths']:
            raise Invalid('schema: nonempty exact paths required')
        for path in source['paths']:
            safe_path(path)
        if len(set(source['paths']))!=len(source['paths']):
            raise Invalid('schema: duplicate paths')
    if len(set(ids))!=len(ids):
        raise Invalid('schema: duplicate source identities')
    for pin in [plan['main'],plan['staging']]+plan['articles']+plan['dependencies']:
        if pin in (plan['main'],plan['staging']):
            exact(pin,('ref','sha'))
        if not isinstance(pin['sha'],str) or not re.fullmatch(r'[0-9a-f]{40}',pin['sha']):
            raise Invalid('schema: full SHA required')
        if (not isinstance(pin['ref'],str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]*',pin['ref'])
                or any(x in pin['ref'] for x in ('..','//','@{')) or pin['ref'].endswith('/')):
            raise Invalid('schema: unsafe ref')
    selected=plan['selected']
    article_ids={a['id'] for a in plan['articles']}
    if (not selected or any(not isinstance(x,str) for x in selected) or len(set(selected))!=len(selected)
            or not set(selected)<=article_ids):
        raise Invalid('schema: selected article identities')
    return plan


def load_plan(path):
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:
                raise Invalid('schema: duplicate JSON key')
            result[key]=value
        return result
    return validate_plan(json.loads(path.read_text(),object_pairs_hook=unique))


def tree(repo, revision):
    result={}
    for row in git(repo,'ls-tree','-rz','--full-tree',revision).split(b'\0'):
        if not row:
            continue
        meta, name=row.split(b'\t',1)
        mode, kind, oid=meta.decode().split()
        path=safe_path(name.decode('utf-8'))
        if mode not in ('100644','100755','120000') or kind!='blob':
            raise Invalid('unsafe tree entry: '+path)
        data=git(repo,'cat-file','blob',oid)
        if mode=='120000' and BASELINE_ALIASES.get(path)!=data:
            raise Invalid('unsafe symlink: '+path)
        result[path]={'mode':mode,'data':data}
    return result


def inventory(files):
    return {p:{'mode':f['mode'],'sha256':digest(f['data'])} for p,f in sorted(files.items())}


def check_refs(repo, plan):
    sources=plan['articles']+plan['dependencies']
    pins=[plan['main'],plan['staging']]+sources
    for pin in pins:
        actual=git(repo,'rev-parse','--verify','--end-of-options',pin['ref']+'^{commit}').decode().strip()
        if actual!=pin['sha']:
            raise Invalid('ref/head drift: '+pin['ref'])
    main=plan['main']['sha']
    staging=plan['staging']['sha']
    staging_only=set(git(repo,'rev-list',staging,'^'+main).decode().splitlines())
    for source in sources:
        ancestors=set(git(repo,'rev-list',source['sha']).decode().splitlines())
        if main not in ancestors:
            raise Invalid('article must descend from pinned main: '+source['id'])
        if source['sha']==staging or staging_only & ancestors:
            raise Invalid('staging ancestry rejected: '+source['id'])
        for other in plan['articles']:
            if other['id']!=source['id'] and other['sha'] in ancestors:
                raise Invalid('article ancestry rejected: '+source['id']+' contains '+other['id'])


def active_markdown(text):
    lines=[]; fence=None
    for line in text.splitlines():
        marker=re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$',line)
        if fence:
            if marker and marker[1][0]==fence[0] and len(marker[1])>=len(fence) and not marker[2].strip():
                fence=None
            continue
        if marker:
            fence=marker[1]
        else:
            lines.append(line)
    return '\n'.join(lines)


def check_build_inputs(files, changed):
    for path,entry in files.items():
        if not path.startswith('blog/') or not path.endswith('.md'):
            continue
        text=entry['data'].decode('utf-8','replace')
        references=re.findall(r'<!--\s*@include:\s*(.*?)\s*-->',text)
        references+=re.findall(r'^\s*<<<\s*(.+)$',text,re.M)
        for reference in references:
            # Ambiguous aliases, line-selection and query syntax are refused.
            reference=reference.strip()
            if (not reference or any(c in reference for c in ('{','#','?','\\','\x00'))
                    or reference.startswith(('/','@','~'))):
                raise Invalid('unsafe build input: '+path)
            target=posixpath.normpath(posixpath.join(posixpath.dirname(path),reference))
            if target.startswith('../') or target not in files or files[target]['mode']=='120000':
                raise Invalid('escaping/missing build input: '+path)
        if path in changed and re.search(r'<script\b|^\s*import\s|\b(?:from|import)\s*[(]?\s*[\"\']',active_markdown(text),re.M):
            raise Invalid('executable build input requires separate review: '+path)


def reconstruct(plan, mode):
    repo=Path(plan['repository']).resolve()
    check_refs(repo,plan)
    base=tree(repo,plan['main']['sha'])
    files=dict(base)
    selected=[a for a in plan['articles'] if a['id'] in plan['selected']]
    if mode=='prepare' and len(selected)!=1:
        raise Invalid('prepare requires exactly one selected article')
    unselected_article_paths={path for article in plan['articles'] if article['id'] not in plan['selected']
                              for path in article['paths'] if path.startswith('blog/post/') and path.endswith('.md')}
    for source in plan['dependencies']+selected:
        if set(source['paths']) & unselected_article_paths:
            raise Invalid('unselected article path in selected source/dependency: '+source['id'])
        head=tree(repo,source['sha'])
        changed={p for p in set(base)|set(head) if base.get(p)!=head.get(p)}
        if changed!=set(source['paths']):
            raise Invalid('ownership mismatch: '+source['id'])
        for path in changed:
            if (base.get(path,{}).get('mode')=='120000' or head.get(path,{}).get('mode')=='120000'):
                raise Invalid('changed symlink rejected: '+path)
            incoming=head.get(path)
            previous=files.get(path)
            original=base.get(path)
            if previous!=original and previous!=incoming:
                if (original is None or incoming is None or previous is None
                        or len({original['mode'],incoming['mode'],previous['mode']})!=1):
                    raise Invalid('merge conflict: '+path)
                with tempfile.TemporaryDirectory(prefix='article-merge-') as temporary:
                    paths=[Path(temporary)/name for name in ('ours','base','theirs')]
                    for file,entry in zip(paths,(previous,original,incoming)):
                        file.write_bytes(entry['data'])
                    try:
                        merged=git(repo,'merge-file','-p',*(str(x) for x in paths))
                    except Invalid:
                        raise Invalid('merge conflict: '+path) from None
                files[path]={'mode':incoming['mode'],'data':merged}
                continue
            if path in head:
                files[path]=head[path]
            else:
                files.pop(path,None)
    changed={p for p in set(base)|set(files) if base.get(p)!=files.get(p)}
    check_build_inputs(files,changed)
    return repo,base,files


def candidate_tree(repo, files):
    # All object writes are temporary; source object database stays untouched.
    with tempfile.TemporaryDirectory(prefix='article-tree-') as temporary:
        objects=Path(temporary)/'objects'; objects.mkdir()
        env={'GIT_OBJECT_DIRECTORY':str(objects)}
        entries={}
        for path,entry in files.items():
            oid=git(repo,'hash-object','-w','--stdin',data=entry['data'],env=env).decode().strip()
            node=entries
            parts=path.split('/')
            for component in parts[:-1]:
                node=node.setdefault(component,{})
            node[parts[-1]]=(entry['mode'],oid)
        def emit(node):
            rows=[]
            for name,value in sorted(node.items()):
                if isinstance(value,dict):
                    rows.append(f'040000 tree {emit(value)}\t{name}\0'.encode())
                else:
                    rows.append(f'{value[0]} blob {value[1]}\t{name}\0'.encode())
            return git(repo,'mktree','-z',data=b''.join(rows),env=env).decode().strip()
        return emit(entries)


def export(files, destination):
    destination.mkdir()
    for name,entry in files.items():
        if entry['mode']=='120000':
            continue
        path=destination/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(entry['data'])
        path.chmod(0o755 if entry['mode']=='100755' else 0o644)


def regular_files(root):
    if root.is_symlink() or not root.is_dir():
        raise Invalid('unsafe candidate directory or symlink')
    files={}
    for path in root.rglob('*'):
        mode=path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise Invalid('symlink rejected: '+path.relative_to(root).as_posix())
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise Invalid('nonregular file rejected')
        files[safe_path(path.relative_to(root).as_posix())]={'mode':'100755' if mode & 0o111 else '100644','data':path.read_bytes()}
    return files


def normalized(data):
    text=data.decode('utf-8','replace')
    text=html.unescape(re.sub(r'<[^>]*>',' ',text))
    return ' '.join(text.split())


def scan_output(repo, plan, base, candidate, build):
    allowed_text='\n'.join(normalized(v['data']) for v in candidate.values())
    allowed_assets={digest(v['data']) for v in candidate.values()}
    routes=set(); prose=set(); assets={}; unverified=[]
    for article in plan['articles']:
        if article['id'] in plan['selected']:
            continue
        head=tree(repo,article['sha'])
        found=False
        for path in article['paths']:
            if path not in head or head.get(path)==base.get(path):
                continue
            data=head[path]['data']
            if path.startswith('blog/post/') and path.endswith('.md'):
                if path not in base:
                    route='/'+path[len('blog/'):-3]+'.html'
                    routes.add(route); found=True
                for paragraph in re.split(rb'\n\s*\n',data):
                    text=normalized(paragraph)
                    if len(text)>=80 and text not in allowed_text:
                        prose.add(text); found=True
            elif digest(data) not in allowed_assets:
                assets[digest(data)]=data; found=True
        if not found:
            unverified.append(article['id'])
    actual=regular_files(build)
    if not actual:
        raise Invalid('empty build output')
    matches=[]
    for path,entry in actual.items():
        data=entry['data']; text=normalized(data)
        if (any(route in text or route[1:] in text for route in routes)
                or any(fragment in text for fragment in prose)
                or any(blob in data for blob in assets.values())):
            matches.append(path)
        for route in routes:
            if path==route[1:]:
                matches.append(path)
    if matches:
        raise Invalid('unselected output detected: '+', '.join(sorted(set(matches))))
    return {'status':'exclusion-unverified' if unverified else 'supplementary-pass',
            'unverified_articles':unverified,'forbidden_routes':sorted(routes),
            'prose_signature_count':len(prose),'asset_signatures':sorted(assets),
            'files':inventory(actual),'output_manifest_sha256':digest(canonical(inventory(actual))),
            'limits':'Supplementary detection only: rewrites, transformations and short fragments may evade signatures. Exact candidate tree/diff is the primary guarantee. This is not build provenance, confidentiality or publication authorization.'}


def receipt(repo,plan,mode,base,files):
    return {'version':1,'mode':mode,'plan_sha256':digest(canonical(plan)),
            'candidate_tree':candidate_tree(repo,files),'files':inventory(files),
            'omitted_baseline_aliases':sorted(p for p,f in files.items() if f['mode']=='120000'),
            'changed_paths':sorted(p for p in set(base)|set(files) if base.get(p)!=files.get(p)),
            'articles':sorted(p for p in files if p.startswith('blog/post/') and p.endswith('.md')),
            'publishable':False,'source_pins':{'main':plan['main'],'staging':plan['staging'],'articles':plan['articles'],'dependencies':plan['dependencies'],'selected':plan['selected']},
            'authority':'local preparation only; separate publication authorization required'}


def clean_location(path):
    path=path.absolute()
    for current in [path]+list(path.parents):
        if current.is_symlink():
            raise Invalid('symlink output location rejected')
    return path


def run(mode,plan,output,build_output=None):
    output=clean_location(output)
    repo_path=Path(plan['repository']).resolve()
    if output.resolve().is_relative_to(repo_path):
        raise Invalid('output cannot be inside source repository')
    repo,base,files=reconstruct(plan,mode)
    report=receipt(repo,plan,mode,base,files)
    if mode=='verify':
        clean_location(output/'receipt.json')
        saved=json.loads((output/'receipt.json').read_text())
        if saved.get('mode') not in ('prepare','preview'):
            raise Invalid('receipt mode drift')
        # Regenerate the original mode rather than trust an edited output manifest.
        _,_,expected=reconstruct(plan,saved['mode'])
        if saved!=receipt(repo,plan,saved['mode'],base,expected):
            raise Invalid('receipt or plan drift')
        actual=regular_files(output/'candidate')
        if inventory(actual)!=inventory({p:f for p,f in expected.items() if f['mode']!='120000'}):
            raise Invalid('candidate output drift')
        result={'verified':True,'publishable':False,'candidate_tree':candidate_tree(repo,expected)}
        if build_output is not None:
            result['output_scan']=scan_output(repo,plan,base,expected,build_output)
        return result
    if output.exists():
        raise Invalid('output must be a new directory')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='article-export-',dir=output.parent) as temporary:
        staged=Path(temporary)/'output'; staged.mkdir()
        export(files,staged/'candidate')
        (staged/'receipt.json').write_bytes(canonical(report))
        check_refs(repo,plan)
        staged.rename(output)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('preview','prepare','verify'))
    parser.add_argument('--plan',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--build-output',type=Path,help='Supplementary output scan in verify mode; never publication authority')
    args=parser.parse_args()
    try:
        if args.build_output is not None and args.mode!='verify':
            raise Invalid('--build-output requires verify')
        result=run(args.mode,load_plan(args.plan),args.output,args.build_output)
    except (Invalid,OSError,ValueError,KeyError,TypeError) as exc:
        print('ARTICLE-PUBLICATION: '+str(exc),file=sys.stderr)
        return 1
    print(json.dumps(result,sort_keys=True,ensure_ascii=False))
    return 0


if __name__=='__main__':
    sys.exit(main())
