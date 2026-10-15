#!/usr/bin/env python3
"""Explicit local version-2 article preparation; no publication or merge authority."""
import argparse
import hashlib
import html
from importlib.util import module_from_spec, spec_from_file_location
import json
import os
import subprocess
import stat
import shutil
import re
from pathlib import Path
import sys
import tempfile

# Load only the reviewed executing controller's preserved v1 helpers.
_spec = spec_from_file_location('preserved_publication_v1', Path(__file__).with_name('article-publication.py'))
old = module_from_spec(_spec)
_spec.loader.exec_module(old)

# Preserve v1 bytes/semantics in its own CLI. Only this explicit v2 controller
# replaces the imported module's Git dependency with a strict offline boundary.
_preserved_git = old.git

def offline_git(repo, *args, data=None, env=None):
    protected = {**(env or {}), 'GIT_NO_LAZY_FETCH': '1', 'GIT_ALLOW_PROTOCOL': ''}
    result = _preserved_git(repo, *args, data=data, env=protected)
    # cat-file can read a corrupt loose object without checking its content hash.
    # Bind every v2 tree read (baseline, staging and sources) back to its Git OID.
    if len(args) == 3 and args[:2] == ('cat-file', 'blob'):
        actual = hashlib.sha1(b'blob ' + str(len(result)).encode() + b'\0' + result).hexdigest()
        if actual != args[2]:
            raise old.Invalid('source blob object identity mismatch')
    return result

old.git = offline_git


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise old.Invalid('schema: duplicate JSON key')
        result[key] = value
    return result


def validate_schema(plan, registry):
    old.exact(plan, ('version', 'repository', 'main', 'staging', 'selected', 'dependencies'))
    old.exact(registry, ('version', 'main', 'staging', 'anchor', 'sources', 'integrations', 'retained', 'staging_inventory') + (('resolutions',) if 'resolutions' in registry else ()))
    if not isinstance(registry.get('resolutions', {}), dict) or any(not isinstance(k, str) or not isinstance(v, str) or not re.fullmatch(r'[0-9a-f]{40}', k) or not re.fullmatch(r'[0-9a-f]{40}', v) for k, v in registry.get('resolutions', {}).items()):
        raise old.Invalid('schema: exact reviewed resolution commit/tree pins required')
    if type(plan['version']) is not int or plan['version'] != 2 or type(registry['version']) is not int or registry['version'] != 2:
        raise old.Invalid('schema: unsupported explicit v2 version')
    if not isinstance(registry['anchor'], str) or not re.fullmatch(r'[0-9a-f]{40}', registry['anchor']) or not isinstance(registry['integrations'], list) or len(set(registry['integrations'])) != len(registry['integrations']) or any(not isinstance(x, str) or not re.fullmatch(r'[0-9a-f]{40}', x) for x in registry['integrations']):
        raise old.Invalid('schema: complete anchor/integration pins required')
    if not isinstance(registry['retained'], dict) or not isinstance(registry['staging_inventory'], dict):
        raise old.Invalid('schema: exact retained/inventory maps required')
    if registry['main'] != plan['main'] or registry['staging'] != plan['staging']:
        raise old.Invalid('schema: registry/plan pins differ')
    if not isinstance(registry['sources'], list) or not isinstance(plan['dependencies'], list):
        raise old.Invalid('schema: source/dependency lists required')
    articles = []
    dependencies = []
    for source in registry['sources']:
        old.exact(source, ('id', 'ref', 'sha', 'paths', 'kind', 'shared_patches', 'requires', 'provenance'))
        if source['kind'] not in ('article', 'dependency') or not isinstance(source['shared_patches'], dict) or not isinstance(source['requires'], list) or any(not isinstance(x, str) for x in source['requires']) or len(set(source['requires'])) != len(source['requires']) or not isinstance(source['provenance'], dict):
            raise old.Invalid('schema: source classification')
        flat = {k: source[k] for k in ('id', 'ref', 'sha', 'paths')}
        (articles if source['kind'] == 'article' else dependencies).append(flat)
    old.validate_plan({'version': 1, 'repository': plan['repository'], 'main': plan['main'], 'staging': plan['staging'], 'articles': articles, 'dependencies': dependencies, 'selected': plan['selected']})


def identities(repo, revision):
    result = {}
    for row in old.git(repo, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0'):
        if row:
            header, name = row.split(b'\t', 1)
            mode, kind, blob = header.decode().split()
            result[old.safe_path(name.decode())] = {'mode': mode, 'blob': blob}
    return result


def independent_merge(repo, left, right, resolution=None):
    # Use a fresh bare repository: source Git config/attributes cannot supply shell drivers.
    objects = Path(old.git(repo, 'rev-parse', '--path-format=absolute', '--git-path', 'objects').decode().strip())
    with tempfile.TemporaryDirectory(prefix='v2-independent-merge-') as directory:
        scratch = Path(directory)
        old.git(scratch, 'init', '--bare', '-q')
        clean = {'PATH': os.defpath, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_TERMINAL_PROMPT': '0', 'GIT_NO_LAZY_FETCH': '1', 'GIT_ALLOW_PROTOCOL': '',
                 'GIT_ALTERNATE_OBJECT_DIRECTORIES': str(objects)}
        result = subprocess.run(['git', '--no-optional-locks', '-C', str(scratch), '-c', 'merge.default=text',
                                 'merge-tree', '--write-tree', left, right], capture_output=True, env=clean)
        first = result.stdout.splitlines()[0].decode() if result.stdout else ''
        if result.returncode not in (0, 1) or not re.fullmatch(r'[0-9a-f]{40}', first):
            raise old.Invalid('independent merge check failed')
        if result.returncode == 1:
            if resolution is None:
                raise old.Invalid('unknown or unreviewed conflict resolution')
            return resolution
        if resolution is not None:
            raise old.Invalid('resolution cannot override a conflict-free independent merge')
        return first



def migration(repo, source):
    provenance = source['provenance']
    if provenance == {'kind': 'clean'}:
        return
    if set(provenance) != {'kind', 'migration'} or provenance['kind'] != 'legacy':
        raise old.Invalid('legacy migration requires explicit owner-reviewed original/new extraction record')
    record = provenance['migration']
    old.exact(record, ('original', 'reconstructed', 'extracted', 'owner_approval'))
    approval = record['owner_approval']
    old.exact(approval, ('record_id', 'binding_sha256'))
    binding = {k: record[k] for k in ('original', 'reconstructed', 'extracted')}
    if not isinstance(approval['record_id'], str) or not approval['record_id'] or approval['binding_sha256'] != old.digest(old.canonical(binding)) or record['reconstructed'] != source['sha']:
        raise old.Invalid('migration approval binding mismatch')
    if not isinstance(record['original'], str) or not re.fullmatch(r'[0-9a-f]{40}', record['original']):
        raise old.Invalid('migration requires original full commit')
    original = identities(repo, record['original'])
    current = identities(repo, source['sha'])
    expected = {p: current.get(p) for p in source['paths']}
    if record['extracted'] != expected or any(original.get(p) != expected[p] for p in source['paths']):
        raise old.Invalid('migration extraction bytes/modes mismatch')


def signatures(repo, plan, registry, base):
    routes = set(); prose = set(); assets = []; unverified = []
    baseline_text = '\n'.join(old.normalized(entry['data']) for entry in base.values())
    baseline_assets = {old.digest(entry['data']) for entry in base.values()}
    selected = set(plan['selected']) | set(plan['dependencies'])
    for source in registry['sources']:
        if source['id'] in selected:
            continue
        found = False
        head = old.tree(repo, source['sha'])
        for name in source['paths']:
            entry = head.get(name)
            if entry is None or entry == base.get(name):
                continue
            data = entry['data']
            if name.startswith('blog/') and name.endswith('.md'):
                if name not in base:
                    route = '/' + name[5:-3]
                    routes.update((route, route + '.html', route + '.md')); found = True
                for paragraph in re.split(rb'\n\s*\n', data):
                    text = old.normalized(paragraph)
                    if len(text) >= 80 and text not in baseline_text:
                        prose.add(text); found = True
                # Supplement custom route declarations without trusting article metadata as policy.
                for route in re.findall(r'^\s*(?:permalink|url|route):\s*[\"\']?(/[^\s\"\']+)', data.decode('utf-8', 'replace'), re.M):
                    if route not in baseline_text:
                        routes.add(route); found = True
            elif data and old.digest(data) not in baseline_assets:
                assets.append(data); found = True
        if not found:
            unverified.append(source['id'])
    return routes, prose, assets, unverified


def scan(files, signatures_value):
    routes, prose, assets, unverified = signatures_value
    matches = []
    for name, entry in files.items():
        if entry['mode'] == '120000':
            continue
        data = entry['data']; text = old.normalized(data)
        raw_text = html.unescape(data.decode('utf-8', 'replace')).replace('\\/', '/')
        if (any(re.search(re.escape(route.lstrip('/')) + r'(?:[\s\"\'?#<)]|$)', raw_text) for route in routes)
                or any(fragment in text for fragment in prose) or any(blob in data for blob in assets)
                or '/' + name.removeprefix('blog/') in routes):
            matches.append(name)
    if matches:
        raise old.Invalid('unselected content detected: ' + ', '.join(sorted(matches)))
    return {'status': 'exclusion-unverified' if unverified else 'supplementary-pass',
            'unverified_sources': unverified, 'forbidden_routes': sorted(routes),
            'prose_signature_count': len(prose), 'asset_signature_count': len(assets),
            'limits': 'Supplementary signatures; exact source admission and candidate tree remain primary.'}


def reconstruct(plan, registry, registry_hash):
    validate_schema(plan, registry)
    repo = Path(plan['repository']).resolve()
    config = old.git(repo, 'config', '--local', '--includes', '--list').decode().lower().splitlines()
    if any(row.split('=', 1)[0] == 'extensions.partialclone' or re.fullmatch(r'remote\..*\.promisor', row.split('=', 1)[0]) for row in config):
        raise old.Invalid('complete history without partial/promisor configuration required')
    if old.git(repo, 'rev-parse', '--is-shallow-repository').strip() != b'false' or old.git(repo, 'for-each-ref', '--format=%(refname)', 'refs/replace').strip():
        raise old.Invalid('complete history without overlays is required')
    graft = Path(old.git(repo, 'rev-parse', '--path-format=absolute', '--git-path', 'info/grafts').decode().strip())
    if graft.exists() or graft.is_symlink():
        raise old.Invalid('complete history without grafts is required')
    check_pins(repo, plan, registry)
    base = old.tree(repo, plan['main']['sha'])
    staging = old.tree(repo, plan['staging']['sha'])
    actual_inventory = identities(repo, plan['staging']['sha'])
    if registry['staging_inventory'] != actual_inventory:
        raise old.Invalid('registry inventory differs from complete pinned staging')
    owners = {}
    for source in registry['sources']:
        for name in source['paths']:
            old.safe_path(name)
            if name in owners:
                raise old.Invalid('registry ownership overlap')
            owners[name] = source['id']
    shared = {p for source in registry['sources'] for patch in source['shared_patches'].values() for p in patch}
    if shared & set(owners):
        raise old.Invalid('registry shared/exclusive overlap')
    for name in shared:
        old.safe_path(name)
        if name.startswith(('blog/post/', 'blog/public/')):
            raise old.Invalid('shared patches cannot waive article or asset ownership')
    retained = registry['retained']
    if any(actual_inventory.get(p) != entry for p, entry in retained.items()):
        raise old.Invalid('retained identity differs from pinned staging')
    if set(retained) & set(owners) or any(p.startswith(('blog/post/', 'blog/public/')) for p in retained):
        raise old.Invalid('registry ownership cannot waive article or asset paths')
    changed = {p for p in set(base) | set(staging) if base.get(p) != staging.get(p)}
    if not changed <= set(owners) | set(retained) | shared:
        raise old.Invalid('registry ownership omits unapproved staging content')
    if len(plan['selected']) != 1:
        raise old.Invalid('exactly one selected article required')
    for source in registry['sources']:
        migration(repo, source)
        ancestors = set(old.git(repo, 'rev-list', source['sha']).decode().splitlines())
        if plan['main']['sha'] not in ancestors or plan['staging']['sha'] in ancestors or set(registry['integrations']) & ancestors:
            raise old.Invalid('source ancestry includes staging integration or lacks current main')
        for other in registry['sources']:
            if other['kind'] == 'article' and other['id'] != source['id']:
                other_commits = set(old.git(repo, 'rev-list', other['sha'], '^' + plan['main']['sha']).decode().splitlines())
                if other_commits & ancestors:
                    raise old.Invalid('other candidate ancestry rejected')
        source_tree = old.tree(repo, source['sha'])
        for name in source['paths']:
            if source_tree.get(name) != staging.get(name):
                raise old.Invalid('registry provenance: source bytes differ from pinned preview')
        owned = set(source['paths'])
        for commit in old.git(repo, 'rev-list', '--reverse', source['sha'], '^' + plan['main']['sha']).decode().splitlines():
            parents = old.git(repo, 'rev-list', '--parents', '-n', '1', commit).decode().split()[1:]
            if len(parents) == 2:
                try:
                    old.git(repo, 'merge-base', '--is-ancestor', parents[1], plan['main']['sha'])
                    expected_tree = independent_merge(repo, parents[0], parents[1], registry.get('resolutions', {}).get(commit))
                except old.Invalid:
                    raise old.Invalid('source history contains unknown or unreviewed merge') from None
                if old.git(repo, 'rev-parse', commit + '^{tree}').decode().strip() != expected_tree:
                    raise old.Invalid('source history has unreviewed conflict resolution')
                continue
            if len(parents) != 1:
                raise old.Invalid('source history contains unreviewed merge')
            changed = set(old.git(repo, 'diff-tree', '--no-ext-diff', '--no-textconv', '--no-renames', '--no-commit-id', '--name-only', '-r', '-z', parents[0], commit).decode().split('\0')) - {''}
            patch = source['shared_patches'].get(commit, {})
            before_tree = identities(repo, parents[0]); after_tree = identities(repo, commit)
            for name, binding in patch.items():
                old.exact(binding, ('before', 'after'))
                if name not in changed or binding != {'before': before_tree.get(name), 'after': after_tree.get(name)}:
                    raise old.Invalid('shared patch binding mismatch')
            if not changed <= owned | set(patch):
                raise old.Invalid('source history changes another candidate or unknown path')
        ordinary = {c for c in old.git(repo, 'rev-list', source['sha'], '^' + plan['main']['sha']).decode().splitlines() if len(old.git(repo, 'rev-list', '--parents', '-n', '1', c).decode().split()) == 2}
        if set(source['shared_patches']) - ordinary:
            raise old.Invalid('shared patch references unknown commit')
        permitted = owned | {p for patch in source['shared_patches'].values() for p in patch}
        if any(source_tree.get(p) != base.get(p) for p in (set(base) | set(source_tree)) - permitted):
            raise old.Invalid('source final tree changes an undeclared path')
    all_source_commits = {c for source in registry['sources'] for c in old.git(repo, 'rev-list', source['sha'], '^' + plan['main']['sha']).decode().splitlines()}
    reviewed_merges = {c for c in all_source_commits | set(registry['integrations']) if len(old.git(repo, 'rev-list', '--parents', '-n', '1', c).decode().split()) == 3}
    if set(registry.get('resolutions', {})) - reviewed_merges:
        raise old.Invalid('resolution policy references unknown commit')
    # Every post-anchor staging commit must be a registered source or explicit integration.
    old.git(repo, 'merge-base', '--is-ancestor', registry['anchor'], plan['staging']['sha'])
    known = set(old.git(repo, 'rev-list', plan['main']['sha'], registry['anchor']).decode().splitlines())
    for source in registry['sources']:
        known.update(old.git(repo, 'rev-list', source['sha']).decode().splitlines())
    unknown = set(old.git(repo, 'rev-list', plan['staging']['sha']).decode().splitlines()) - known
    if unknown != set(registry['integrations']):
        raise old.Invalid('staging history has unknown or missing integration commits')
    cursor = plan['staging']['sha']
    while cursor != registry['anchor']:
        if cursor not in unknown:
            raise old.Invalid('staging history does not follow explicit integration first parents')
        parents = old.git(repo, 'rev-list', '--parents', '-n', '1', cursor).decode().split()[1:]
        if len(parents) != 2 or parents[1] in unknown or parents[1] not in known:
            raise old.Invalid('staging history has unknown merge topology')
        if independent_merge(repo, *parents, registry.get('resolutions', {}).get(cursor)) != old.git(repo, 'rev-parse', cursor + '^{tree}').decode().strip():
            raise old.Invalid('staging history has unreviewed integration resolution')
        cursor = parents[0]
    selected = next(s for s in registry['sources'] if s['id'] == plan['selected'][0])
    by_id = {s['id']: s for s in registry['sources']}
    required = set()
    def visit(source, trail):
        for dependency in source['requires']:
            if not isinstance(dependency, str) or dependency not in by_id or by_id[dependency]['kind'] != 'dependency' or dependency in trail:
                raise old.Invalid('dependency registry has unknown/article/cyclic requirement')
            required.add(dependency)
            visit(by_id[dependency], trail | {dependency})
    for source in registry['sources']:
        visit(source, {source['id']})
    required.clear(); visit(selected, {selected['id']})
    if len(set(plan['dependencies'])) != len(plan['dependencies']) or set(plan['dependencies']) != required:
        raise old.Invalid('dependency selection differs from exact reviewed requirements')
    base = old.tree(repo, plan['main']['sha'])
    files = dict(base)
    applied = {}
    for source in [selected] + [by_id[x] for x in sorted(required)]:
        head = old.tree(repo, source['sha'])
        for name in set(source['paths']) | {p for patch in source['shared_patches'].values() for p in patch}:
            old.safe_path(name)
            if name in applied and applied[name] != head.get(name):
                raise old.Invalid('dependency/shared patches conflict; explicit reviewed composition required')
            applied[name] = head.get(name)
            if name in head:
                files[name] = head[name]
            else:
                files.pop(name, None)
    delta = {p for p in set(base) | set(files) if base.get(p) != files.get(p)}
    if any(base.get(p, {}).get('mode') == '120000' or files.get(p, {}).get('mode') == '120000' for p in delta):
        raise old.Invalid('immutable alias change rejected')
    old.check_build_inputs(files, delta)
    source_scan = scan(files, signatures(repo, plan, registry, base))
    report = {'version': 2, 'mode': 'prepare', 'plan_sha256': old.digest(old.canonical(plan)), 'registry_sha256': registry_hash, 'candidate_tree': old.candidate_tree(repo, files), 'files': old.inventory(files), 'source_scan': source_scan, 'publishable': False, 'pr_ready': False, 'authority': 'local preparation; separate approval, isolated build and output checks required'}
    check_pins(repo, plan, registry)
    return report, files


def check_pins(repo, plan, registry):
    for pin in [plan['main'], plan['staging']] + registry['sources']:
        if old.git(repo, 'rev-parse', '--verify', '--end-of-options', pin['ref'] + '^{commit}').decode().strip() != pin['sha']:
            raise old.Invalid('ref/head drift')


def export(files, destination):
    old.export(files, destination)
    for name, entry in files.items():
        if entry['mode'] == '120000':
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(entry['data'].decode())


def physical(root, excluded=()):
    if root.is_symlink() or not root.is_dir():
        raise old.Invalid('unsafe candidate root')
    result = {}
    for directory, subdirs, names in os.walk(root, followlinks=False):
        for name in list(subdirs) + names:
            path = Path(directory) / name
            relative = old.safe_path(path.relative_to(root).as_posix())
            mode = path.lstat().st_mode
            if relative in excluded:
                if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
                    raise old.Invalid('unsafe excluded build directory')
                if name in subdirs:
                    subdirs.remove(name)
                continue
            if stat.S_ISLNK(mode):
                data = os.readlink(path).encode()
                if old.BASELINE_ALIASES.get(relative) != data:
                    raise old.Invalid('unsafe candidate alias: ' + relative)
                result[relative] = {'mode': '120000', 'data': data}
                if name in subdirs:
                    subdirs.remove(name)
            elif stat.S_ISDIR(mode):
                continue
            elif stat.S_ISREG(mode):
                result[relative] = {'mode': '100755' if mode & 0o111 else '100644', 'data': path.read_bytes()}
            else:
                raise old.Invalid('unsafe candidate special file')
    return result


def prepare(plan, registry, registry_hash, output):
    report, files = reconstruct(plan, registry, registry_hash)
    output = old.clean_location(output)
    if output.exists() or output.resolve().is_relative_to(Path(plan['repository']).resolve()):
        raise old.Invalid('output must be new and outside repository')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.v2-prepared-', dir=output.parent) as temporary:
        staging = Path(temporary)
        export(files, staging / 'candidate')
        if physical(staging / 'candidate') != files:
            raise old.Invalid('candidate export filesystem identity mismatch')
        (staging / 'receipt.json').write_bytes(old.canonical(report))
        check_pins(Path(plan['repository']), plan, registry)
        output.mkdir()  # exclusive ownership; never replace another caller's output
        try:
            os.rename(staging / 'candidate', output / 'candidate')
            os.rename(staging / 'receipt.json', output / 'receipt.json')
        except BaseException:
            shutil.rmtree(output)
            raise
    return report


def verify(plan, registry, registry_hash, bundle):
    bundle = old.clean_location(bundle)
    expected, files = reconstruct(plan, registry, registry_hash)
    if bundle.is_symlink() or not bundle.is_dir() or {p.name for p in bundle.iterdir()} != {'candidate', 'receipt.json'}:
        raise old.Invalid('candidate bundle inventory mismatch')
    receipt = bundle / 'receipt.json'
    if receipt.is_symlink() or not receipt.is_file() or receipt.read_bytes() != old.canonical(expected):
        raise old.Invalid('candidate receipt mismatch')
    if physical(bundle / 'candidate') != files:
        raise old.Invalid('candidate full bytes/modes inventory mismatch')
    return {**expected, 'mode': 'verify', 'primary_source_verification': 'pass'}

def checked_json(path, expected_digest, label):
    if path is None or expected_digest is None:
        raise old.Invalid(label + ' required')
    raw = path.read_bytes()
    if old.digest(raw) != expected_digest:
        raise old.Invalid(label + ' trusted digest mismatch')
    return json.loads(raw, object_pairs_hook=unique)


def build(plan, registry, registry_hash, args):
    verified = verify(plan, registry, registry_hash, args.output)
    runtime = checked_json(args.runtime, args.runtime_sha256, 'reviewed runtime')
    if args.build_output is None:
        raise old.Invalid('new build output required')
    repo = Path(plan['repository']).resolve()
    if args.build_output.resolve().is_relative_to(repo) or args.build_output.resolve().is_relative_to(args.output.resolve()):
        raise old.Invalid('build must use a separate disposable output')
    helper_spec = spec_from_file_location('reviewed_build_v2', Path(__file__).with_name('publication_build_v2.py'))
    helper = module_from_spec(helper_spec); helper_spec.loader.exec_module(helper)
    report, files = reconstruct(plan, registry, registry_hash)
    result = helper.execute(old, verified, files, runtime, args.runtime_sha256, args.build_output, export, physical, scan,
                            signatures(repo, plan, registry, old.tree(repo, plan['main']['sha'])))
    check_pins(repo, plan, registry)
    return result


def ready(plan, registry, registry_hash, args):
    verified = verify(plan, registry, registry_hash, args.output)
    built = checked_json(args.build_receipt, args.build_sha256, 'actual build receipt')
    approval = checked_json(args.approval, args.approval_sha256, 'owner approval')
    old.exact(approval, ('version', 'record_id', 'binding', 'preview'))
    old.exact(approval['preview'], ('staging_sha', 'served_sha', 'evidence_sha256'))
    binding = old.digest(old.canonical(verified))
    if approval['version'] != 2 or not isinstance(approval['record_id'], str) or not approval['record_id'] or approval['binding'] != binding or approval['preview']['staging_sha'] != plan['staging']['sha'] or approval['preview']['served_sha'] != plan['staging']['sha'] or not re.fullmatch(r'[0-9a-f]{64}', approval['preview']['evidence_sha256']):
        raise old.Invalid('owner approval/served preview binding mismatch')
    if built.get('version') != 2 or built.get('binding') != binding or built.get('status') != 'pass' or built.get('isolation') != {'inside': True, 'outside_read': 'denied', 'outside_write': 'denied', 'network': 'denied'}:
        raise old.Invalid('actual isolated build binding/check mismatch')
    output = old.regular_files(args.build_receipt.parent / 'output')
    if old.inventory(output) != built.get('files') or old.digest(old.canonical(old.inventory(output))) != built.get('output_manifest_sha256'):
        raise old.Invalid('actual output full inventory mismatch')
    output_scan = scan(output, signatures(Path(plan['repository']), plan, registry, old.tree(Path(plan['repository']), plan['main']['sha'])))
    if output_scan != built.get('scan') or output_scan['status'] != 'supplementary-pass' or verified['source_scan']['status'] != 'supplementary-pass':
        raise old.Invalid('required output exclusion is unverified or mismatched')
    check_pins(Path(plan['repository']), plan, registry)
    return {**verified, 'mode': 'ready', 'pr_ready': True, 'publishable': False,
            'approval_sha256': args.approval_sha256, 'build_sha256': args.build_sha256,
            'authority': 'local exact candidate ready for separately authorized PR; no merge/publication authority'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('schema', 'prepare', 'verify', 'build', 'ready'))
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--registry', type=Path, help='Owner-reviewed control policy, never article-selected metadata')
    parser.add_argument('--registry-sha256', help='Expected digest supplied by the reviewed caller')
    parser.add_argument('--output', type=Path)
    for name in ('runtime', 'build-output', 'build-receipt', 'approval'):
        parser.add_argument('--' + name, type=Path)
    for name in ('runtime-sha256', 'build-sha256', 'approval-sha256'):
        parser.add_argument('--' + name)
    args = parser.parse_args()
    if args.mode == 'schema':
        print((Path(__file__).resolve().parents[1] / 'docs/article-publication-v2.schema.json').read_text(), end='')
        return 0
    try:
        if any(x is None for x in (args.plan, args.registry, args.registry_sha256, args.output)):
            raise old.Invalid('plan, reviewed registry/digest and output required')
        raw = args.registry.read_bytes()
        if hashlib.sha256(raw).hexdigest() != args.registry_sha256:
            raise old.Invalid('trusted registry digest mismatch')
        plan = json.loads(args.plan.read_text(), object_pairs_hook=unique)
        registry = json.loads(raw, object_pairs_hook=unique)
        if type(plan.get('version')) is not int or plan['version'] != 2 or registry.get('version') != 2:
            raise old.Invalid('unsupported explicit v2 schema')
        if args.mode in ('prepare', 'verify'):
            result = (prepare if args.mode == 'prepare' else verify)(plan, registry, args.registry_sha256, args.output)
        else:
            result = (build if args.mode == 'build' else ready)(plan, registry, args.registry_sha256, args)
    except (old.Invalid, OSError, ValueError, KeyError, TypeError, StopIteration, subprocess.TimeoutExpired) as exc:
        print('ARTICLE-PUBLICATION-V2: ' + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
