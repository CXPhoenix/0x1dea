#!/usr/bin/env python3
"""Compute a local fixed-staging sync; never grants remote/publication authority."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
BASELINE_ALIASES = {
    'skills/phoenix-writing/reference': b'../../maintenance/writing-skills/legacy/phoenix-writing/reference',
    'skills/phoenix-writing/scripts': b'../maintaining-writing-skills/legacy-validator',
    '.gemini/skills/creating-vitepress-post': b'../../skills/creating-vitepress-post',
}

PROTECTED_HISTORY = {
    'maintenance/article-publication/source-boundary.json',
    'maintenance/lint-cleanup/source-boundary.json',
    'maintenance/writing-skills/original-manifest.json',
    'maintenance/writing-skills/publication-manifest.json',
    'maintenance/writing-skills/skills-mcp-manifest.json',
    'maintenance/harness-reconciliation/staging.json',
    'maintenance/harness-reconciliation/components.json',
    'maintenance/harness-reconciliation/article-electricity-revision.json',
    'maintenance/harness-reconciliation/test-contract-repair.json',
    'maintenance/publication-workflow/history/main-verifier.py',
    'maintenance/publication-workflow/history/staging-verifier.py',
    '.proj.specs/0002-article-publication/electricity-release/scope.json',
}


class Invalid(ValueError):
    def __init__(self, message, *, status='failure', paths=()):
        super().__init__(message)
        self.status = status
        self.paths = list(paths)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def git(repo, *args, check=True, data=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_NO_REPLACE_OBJECTS='1', GIT_TERMINAL_PROMPT='0',
               GIT_NO_LAZY_FETCH='1', GIT_ALLOW_PROTOCOL='')
    result = subprocess.run(['git', '--no-optional-locks', '-C', str(repo), *args],
                            capture_output=True, env=env, input=data)
    if check and result.returncode:
        raise Invalid('Git check failed: ' + result.stderr.decode('utf-8', 'replace').strip())
    return result


def exact(value, fields):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise Invalid('schema: unknown or missing fields')


def safe_path(value):
    if (not isinstance(value, str) or not value or value.startswith('/')
            or any(c in value for c in ('\\', '\0', '\n', '\r', '\t'))
            or any(c in ('', '.', '..', '.git') for c in value.split('/'))):
        raise Invalid('schema: unsafe path')
    return value


def pin_schema(value):
    exact(value, ('ref', 'sha'))
    if (not isinstance(value['sha'], str) or not re.fullmatch('[0-9a-f]{40}', value['sha'])
            or not isinstance(value['ref'], str) or not re.fullmatch('[A-Za-z0-9][A-Za-z0-9._/-]*', value['ref'])
            or any(c in value['ref'] for c in ('..', '//')) or value['ref'].endswith('/')):
        raise Invalid('schema: unsafe pin')


def identity_map(value):
    if not isinstance(value, dict):
        raise Invalid('schema: path identity map required')
    for path, identity in value.items():
        safe_path(path)
        exact(identity, ('mode', 'blob'))
        if (identity['mode'] not in ('100644', '100755', '120000')
                or not isinstance(identity['blob'], str) or not re.fullmatch('[0-9a-f]{40}', identity['blob'])):
            raise Invalid('schema: invalid path identity: ' + path, paths=[path])


def validate(registry):
    exact(registry, ('version', 'target', 'repository', 'main', 'staging', 'trees', 'candidates', 'engineering', 'checks'))
    if type(registry['version']) is not int or registry['version'] != 1 or registry['target'] != 'staging':
        raise Invalid('schema: version 1 fixed staging target required')
    if (not isinstance(registry['repository'], str) or not Path(registry['repository']).is_absolute()
            or any(c in registry['repository'] for c in ('\0', '\n', '\r'))):
        raise Invalid('schema: absolute source repository required')
    pin_schema(registry['main'])
    pin_schema(registry['staging'])
    for role in ('main', 'staging'):
        if registry[role]['ref'] not in (role, 'refs/heads/' + role, 'refs/remotes/origin/' + role):
            raise Invalid('schema: fixed target ref required: ' + role)
    exact(registry['trees'], ('main', 'staging'))
    for role in ('main', 'staging'):
        identity_map(registry['trees'][role])
    identity_map(registry['checks'])
    if not isinstance(registry['candidates'], list) or not isinstance(registry['engineering'], list):
        raise Invalid('schema: lists required')
    owned, ids = set(), set()
    for candidate in registry['candidates']:
        exact(candidate, ('id', 'source', 'paths'))
        if (not isinstance(candidate['id'], str) or not re.fullmatch('[A-Za-z0-9][A-Za-z0-9._-]{0,63}', candidate['id'])
                or candidate['id'] in ids):
            raise Invalid('schema: duplicate or invalid candidate id')
        ids.add(candidate['id'])
        pin_schema(candidate['source'])
        identity_map(candidate['paths'])
        if not candidate['paths'] or not any(p.startswith('blog/') and p.endswith('.md') for p in candidate['paths']):
            raise Invalid('schema: candidate article paths required')
        for name, expected in candidate['paths'].items():
            if name in owned or not name.startswith('blog/') or registry['trees']['staging'].get(name) != expected:
                raise Invalid('schema: candidate overlap or staging identity mismatch: ' + name, paths=[name])
            owned.add(name)
    main, stage = registry['trees']['main'], registry['trees']['staging']
    historical = {p for p in stage if p.startswith('maintenance/harness-adoption/') or p in PROTECTED_HISTORY}
    omitted = historical - set(registry['checks'])
    if omitted:
        raise Invalid('schema: protected history checks missing', paths=sorted(omitted))
    delta = {p for p in set(main) | set(stage) if main.get(p) != stage.get(p)}
    engineering = set()
    for name in registry['engineering']:
        safe_path(name)
        blog_engineering = name == 'blog/index.md' or name.startswith(('blog/.vitepress/', 'blog/shared/'))
        if name in engineering or name in owned or (name.startswith('blog/') and not blog_engineering):
            raise Invalid('schema: engineering ownership overlap or article path: ' + name, paths=[name])
        engineering.add(name)
    missing = delta - owned - engineering
    extra = engineering - delta
    if missing or extra:
        raise Invalid('schema: incomplete or extra delta classification', paths=sorted(missing | extra))
    return registry


def load_registry(raw):
    def unique(pairs):
        found = {}
        for key, value in pairs:
            if key in found:
                raise Invalid('schema: duplicate JSON key')
            found[key] = value
        return found
    return validate(json.loads(raw, object_pairs_hook=unique))


def pins(registry):
    return [registry['main'], registry['staging']] + [c['source'] for c in registry['candidates']]


def check_refs(registry):
    for pin in pins(registry):
        actual = git(registry['repository'], 'rev-parse', '--verify', '--end-of-options',
                     pin['ref'] + '^{commit}').stdout.decode().strip()
        if actual != pin['sha']:
            raise Invalid('ref drift: ' + pin['ref'], status='stale')


def identities(repo, ref):
    found = {}
    for row in git(repo, 'ls-tree', '-rz', '--full-tree', ref).stdout.split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, blob = meta.decode().split()
        path = safe_path(name.decode())
        if kind != 'blob' or mode not in ('100644', '100755', '120000'):
            raise Invalid('unsafe tree entry: ' + path, paths=[path])
        if mode == '120000' and (path not in BASELINE_ALIASES or git(repo, 'cat-file', 'blob', blob).stdout != BASELINE_ALIASES[path]):
            raise Invalid('unsafe symlink: ' + path, paths=[path])
        if path in found:
            raise Invalid('duplicate source tree path: ' + path, paths=[path])
        found[path] = {'mode': mode, 'blob': blob}
    return found


def check_source_blobs(source, registry):
    names = {}
    for entries in registry['trees'].values():
        for path, identity in entries.items():
            names.setdefault(identity['blob'], set()).add(path)
    order = sorted(names)
    if not order:
        return
    raw = git(source, 'cat-file', '--batch', data=('\n'.join(order) + '\n').encode()).stdout
    cursor = 0
    for blob in order:
        end = raw.find(b'\n', cursor)
        header = raw[cursor:end].split()
        paths = sorted(names[blob])
        if end < cursor or len(header) != 3 or header[:2] != [blob.encode(), b'blob'] or not header[2].isdigit():
            raise Invalid('missing or invalid source blob', paths=paths)
        size = int(header[2])
        content = raw[end+1:end+1+size]
        if (len(content) != size or raw[end+1+size:end+2+size] != b'\n'
                or hashlib.sha1(b'blob ' + str(size).encode() + b'\0' + content).hexdigest() != blob):
            raise Invalid('source blob identity mismatch', paths=paths)
        cursor = end + size + 2
    if cursor != len(raw):
        raise Invalid('unexpected source blob batch output')


def compute(registry, store):
    source = Path(registry['repository'])
    partial = git(source, 'config', '--local', '--includes', '--get-regexp',
                  r'^(extensions\.partialclone|remote\..*\.(promisor|partialclonefilter))$', check=False)
    if partial.returncode not in (0, 1):
        raise Invalid('source configuration check failed')
    if partial.stdout.strip():
        raise Invalid('complete source required: partial/promisor configuration is not allowed')
    if git(source, 'rev-parse', '--is-shallow-repository').stdout.strip() != b'false':
        raise Invalid('complete source required: shallow history is not allowed')
    if git(source, 'for-each-ref', '--format=%(refname)', 'refs/replace').stdout.strip():
        raise Invalid('unmodified source history required: replacement refs are not allowed')
    grafts = Path(git(source, 'rev-parse', '--path-format=absolute', '--git-path', 'info/grafts').stdout.decode().strip())
    if grafts.exists() or grafts.is_symlink():
        raise Invalid('unmodified source history required: grafts are not allowed')
    check_refs(registry)
    for role in ('main', 'staging'):
        actual = identities(source, registry[role]['sha'])
        expected = registry['trees'][role]
        if actual != expected:
            raise Invalid('trusted source tree mismatch: ' + role,
                          paths=sorted(p for p in set(actual) | set(expected) if actual.get(p) != expected.get(p)))
    main_aliases = {p: identity for p, identity in registry['trees']['main'].items() if identity['mode'] == '120000'}
    stage_aliases = {p: identity for p, identity in registry['trees']['staging'].items() if identity['mode'] == '120000'}
    alias_delta = sorted(p for p in set(main_aliases) | set(stage_aliases) if main_aliases.get(p) != stage_aliases.get(p))
    if alias_delta:
        raise Invalid('immutable alias delta is not allowed', paths=alias_delta)
    check_source_blobs(source, registry)
    for candidate in registry['candidates']:
        source_tree = identities(source, candidate['source']['sha'])
        bad = [p for p, expected in candidate['paths'].items() if source_tree.get(p) != expected]
        if bad:
            raise Invalid('candidate source identity mismatch', paths=sorted(bad))
    git(source, 'init', '--bare', '--template=', '-q', str(store))
    object_path = Path(git(source, 'rev-parse', '--git-path', 'objects').stdout.decode().strip())
    if not object_path.is_absolute():
        object_path = source / object_path
    (store/'objects/info/alternates').write_text(str(object_path.resolve()) + '\n')
    contained = git(store, 'merge-base', '--is-ancestor', registry['main']['sha'], registry['staging']['sha'], check=False).returncode == 0
    merged = git(store, 'merge-tree', '--write-tree', '--name-only', '-z',
                 registry['staging']['sha'], registry['main']['sha'], check=False)
    if merged.returncode:
        if merged.returncode == 1:
            names = merged.stdout.split(b'\0')[1:]
            paths = []
            for name in names:
                if not name:
                    break
                paths.append(name.decode())
            raise Invalid('Git merge conflict', status='conflict', paths=sorted(set(paths)))
        raise Invalid('Git merge failed: ' + merged.stderr.decode('utf-8', 'replace').strip())
    tree = merged.stdout.split(b'\0', 1)[0].decode()
    result = identities(store, tree)
    result_aliases = {p: identity for p, identity in result.items() if identity['mode'] == '120000'}
    if result_aliases != stage_aliases:
        raise Invalid('immutable alias result changed',
                      paths=sorted(p for p in set(result_aliases) | set(stage_aliases) if result_aliases.get(p) != stage_aliases.get(p)))
    for candidate in registry['candidates']:
        for name, expected in candidate['paths'].items():
            if result.get(name) != expected:
                raise Invalid('candidate identity changed: ' + name, paths=[name])
    for name, expected in registry['checks'].items():
        if result.get(name) != expected:
            raise Invalid('protected identity check failed: ' + name, paths=[name])
    check_refs(registry)
    return {'version': 1, 'status': 'no-op' if contained else 'ready', 'target': 'staging', 'local_ready': not contained,
            'publishable': False, 'repository': str(source), 'main': registry['main'],
            'staging': registry['staging'], 'sources': [c['source'] for c in registry['candidates']],
            'result_tree': tree, 'checks': ['pinned-source-trees', 'independent-git-tree',
                                         'full-candidate-identities', 'protected-identities', 'local-ref-pins']}


def safe_output(path, repository):
    if not path.is_absolute():
        raise Invalid('output must be absolute')
    for parent in (path, *path.parents):
        if parent.is_symlink() and str(parent) not in ('/tmp', '/var'):
            raise Invalid('output symlink or symlinked parent')
    output = path.resolve()
    if output.is_relative_to(Path(repository).resolve()):
        raise Invalid('output must be external to source repository')
    common = Path(git(repository, 'rev-parse', '--git-common-dir').stdout.decode().strip())
    if not common.is_absolute():
        common = Path(repository) / common
    if output.is_relative_to(common.resolve()):
        raise Invalid('output must be external to source Git storage')
    return output


def public_schema():
    pin = {'type': 'object', 'additionalProperties': False, 'required': ['ref', 'sha'],
           'properties': {'ref': {'type': 'string'}, 'sha': {'type': 'string', 'pattern': '^[0-9a-f]{40}$'}}}
    identity = {'type': 'object', 'additionalProperties': False, 'required': ['mode', 'blob'],
                'properties': {'mode': {'enum': ['100644', '100755', '120000']},
                               'blob': {'type': 'string', 'pattern': '^[0-9a-f]{40}$'}}}
    paths = {'type': 'object', 'additionalProperties': identity}
    properties = {'version': {'const': 1}, 'target': {'const': 'staging'},
                  'repository': {'type': 'string', 'description': 'Absolute trusted source repository'},
                  'main': pin, 'staging': pin,
                  'trees': {'type': 'object', 'additionalProperties': False, 'required': ['main', 'staging'],
                            'properties': {'main': paths, 'staging': paths}},
                  'candidates': {'type': 'array', 'items': {'type': 'object', 'additionalProperties': False,
                                 'required': ['id', 'source', 'paths'], 'properties': {
                                     'id': {'type': 'string'}, 'source': pin, 'paths': paths}}},
                  'engineering': {'type': 'array', 'uniqueItems': True, 'items': {'type': 'string'}},
                  'checks': paths}
    return {'version': 1, 'target': 'staging', 'operations': ['prepare', 'verify', 'schema'],
            'registry': {'type': 'object', 'additionalProperties': False,
                         'required': list(properties), 'properties': properties},
            'receipt': {'version': 1, 'statuses': ['ready', 'no-op', 'conflict', 'failure', 'stale'],
                        'authority': 'local CLI source checks only; no remote/native/browser/CI authority',
                        'success_fields': ['version', 'status', 'target', 'local_ready', 'publishable',
                                           'repository', 'main', 'staging', 'sources', 'result_tree',
                                           'checks', 'registry_sha256'],
                        'failure_fields': ['version', 'status', 'target', 'local_ready', 'publishable', 'paths', 'error']},
            'constraints': ['Full source tree inventory and exact delta ownership required',
                            'Candidate full bytes include all metadata; sources and staging must match',
                            'Only fixed historical literal aliases are allowed; never followed',
                            'Reviewed caller supplies external registry digest; no automatic registry approval']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('prepare', 'verify', 'schema'))
    parser.add_argument('--registry', type=Path)
    parser.add_argument('--registry-sha256', help='Reviewed external digest, not derived from candidate input')
    parser.add_argument('--output', type=Path, help='New external directory for prepare; existing result for verify')
    args = parser.parse_args()
    if args.operation == 'schema':
        print(canonical(public_schema()).decode(), end='')
        return 0
    if args.registry is None or args.registry_sha256 is None or args.output is None:
        parser.error('prepare/verify require --registry, --registry-sha256 and --output')
    created = None
    try:
        raw = args.registry.read_bytes()
        if hashlib.sha256(raw).hexdigest() != args.registry_sha256:
            raise Invalid('trusted registry digest mismatch')
        registry = load_registry(raw)
        output = safe_output(args.output, registry['repository'])
        if args.operation == 'prepare':
            if output.exists() or output.is_relative_to(Path(registry['repository']).resolve()):
                raise Invalid('output must be a new external directory')
            with tempfile.TemporaryDirectory(prefix='staging-sync-compute-') as tmp:
                store = Path(tmp) / 'result.git'
                report = compute(registry, store)
                report['registry_sha256'] = args.registry_sha256
                output.mkdir()
                created = output
                shutil.copytree(store, output/'result.git')
                (output/'receipt.json').write_bytes(canonical(report))
        else:
            receipt = json.loads((output/'receipt.json').read_bytes())
            with tempfile.TemporaryDirectory(prefix='staging-sync-verify-') as tmp:
                report = compute(registry, Path(tmp)/'result.git')
                report['registry_sha256'] = args.registry_sha256
                if report != receipt or identities(output/'result.git', report['result_tree']) != identities(Path(tmp)/'result.git', report['result_tree']):
                    raise Invalid('receipt or result tree mismatch')
        check_refs(registry)
        print(canonical(report).decode(), end='')
        return 0
    except (Invalid, OSError, ValueError, KeyError, TypeError) as error:
        if created is not None:
            shutil.rmtree(created)
        print(canonical({'version': 1, 'status': getattr(error, 'status', 'failure'),
                         'target': 'staging', 'local_ready': False, 'publishable': False,
                         'paths': getattr(error, 'paths', []), 'error': str(error)}).decode(), end='')
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
