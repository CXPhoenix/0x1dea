"""Validate PR #17 as an exact successor without changing historical contracts."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

BASE = 'e457143e8be2f7d54f69bc3e9b80230375be49de'
RELEASE = '604f8733ca47d67fc277ec127a9da743cefbc22e'
MERGE = '88b9c53852f527ee636bcc4b4ca5e166f6ec10fd'
LISTING_INDEX = 'blog/post/course/security-awareness/index.md'
LISTING_BEFORE = '7da24230dca20c0a475caef2d616b15a7f56f47443f97eb7e0f8de6963c1f174'
LISTING_AFTER = '5c578e76cdbd84e0d316008e341d56daaa34a0f150237a53a9111bcd58c73d3a'
EVIDENCE = '.proj.specs/0002-article-publication/electricity-release/'
SCOPE = EVIDENCE + 'scope.json'
SCOPE_SHA256 = '07a8241a373314efc31a08d1587fc984c56fe186bd96fc4578d7c233d9619e2d'
EVIDENCE_NAMES = {'harness-tests.txt', 'isolation-sentinel.json', 'lint.txt', 'plan.md',
                  'publication-tests.txt', 'review.md', 'sandbox-build.txt', 'scope.json',
                  'source-provenance.json', 'unit-green.txt', 'validation.md'}
CODE = {'scripts/verify-harness-adoption.py', 'scripts/main_publication_verification.py',
        'tests/harness_adoption/test_tracker.py', 'tests/harness_adoption/test_main_release.py'}


def git(root, *args, input=None):
    try:
        return subprocess.check_output(['git', '--no-replace-objects', *args], cwd=root,
                                       input=input, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as error:
        raise ValueError('unavailable publication Git object/history: ' + ' '.join(args)) from error


def sha(data):
    return hashlib.sha256(data).hexdigest()


def tree(root, ref):
    entries = []
    for row in git(root, 'ls-tree', '-r', '-z', ref).split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, kind, blob = meta.decode().split()
            if kind != 'blob':
                raise ValueError('unsupported publication Git entry: ' + name.decode())
            entries.append((name.decode(), mode, blob))
    blobs = list(dict.fromkeys(row[2] for row in entries))
    raw = git(root, 'cat-file', '--batch', input=('\n'.join(blobs) + '\n').encode())
    contents = {}; offset = 0
    for blob in blobs:
        end = raw.index(b'\n', offset); header = raw[offset:end].decode().split()
        if header[:2] != [blob, 'blob']:
            raise ValueError('unavailable publication Git blob: ' + blob)
        size = int(header[2]); offset = end + 1
        contents[blob] = raw[offset:offset + size]; offset += size + 1
    return {name: {'mode': mode, 'sha256': sha(contents[blob]), 'bytes': contents[blob]}
            for name, mode, blob in entries}


def identity(entry):
    return None if entry is None else {key: entry[key] for key in ('mode', 'sha256')}


def source_inventory(root):
    names = set(filter(None, git(root, 'ls-files', '--cached', '--others', '--exclude-standard', '-z').decode().split('\0')))
    generated = {'blog/.vitepress/dist', 'blog/.vitepress/cache', 'blog/.vitepress/.temp'}
    pending = [root / name for name in ('blog', 'docs', 'tests')]
    while pending:
        directory = pending.pop()
        if directory.is_symlink():
            raise ValueError('linked publication directory: ' + directory.relative_to(root).as_posix())
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path); name = path.relative_to(root).as_posix()
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISLNK(mode):
                    raise ValueError('linked publication source: ' + name)
                if name in generated or (name.startswith('tests/') and entry.name == '__pycache__'):
                    if not stat.S_ISDIR(mode):
                        raise ValueError('non-directory publication output: ' + name)
                    continue
                if stat.S_ISDIR(mode):
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    names.add(name)
                else:
                    raise ValueError('nonregular publication source: ' + name)
    return names


def check(root, allowed_new, regular_path):
    grafts = Path(git(root, 'rev-parse', '--git-path', 'info/grafts').decode().strip())
    if not grafts.is_absolute():
        grafts = root / grafts
    if git(root, 'for-each-ref', '--format=%(refname)', 'refs/replace').strip() or grafts.exists() or grafts.is_symlink():
        raise ValueError('publication history overlays are not allowed')
    for name in sorted(CODE):
        regular_path(root, name)
    for older, newer in ((BASE, RELEASE), (RELEASE, MERGE), (MERGE, 'HEAD')):
        git(root, 'merge-base', '--is-ancestor', older, newer)
    if git(root, 'rev-parse', RELEASE + '^{tree}') != git(root, 'rev-parse', MERGE + '^{tree}'):
        raise ValueError('changed merged publication tree')
    before = tree(root, BASE); released = tree(root, MERGE)
    raw = regular_path(root, SCOPE).read_bytes()
    if sha(raw) != SCOPE_SHA256 or raw != released[SCOPE]['bytes']:
        raise ValueError('changed publication scope: ' + SCOPE)
    scope = json.loads(raw)
    product = scope['content_and_dependency_files']
    evidence = {EVIDENCE + name for name in EVIDENCE_NAMES}
    delta = {name for name in set(before) | set(released)
             if identity(before.get(name)) != identity(released.get(name))}
    if (scope['base'] != BASE or len(product) != 34 or delta != set(product) | evidence
            or any(identity(released.get(name)) != expected for name, expected in product.items())):
        raise ValueError('incomplete publication source boundary')
    if identity(released.get(LISTING_INDEX)) != {'mode': '100644', 'sha256': LISTING_BEFORE}:
        raise ValueError('changed original category index identity')
    # Keep the release oracle intact; only this exact current index successor differs.
    protected = {name: entry for name, entry in released.items() if name not in CODE}
    protected[LISTING_INDEX] = {'mode': '100644', 'sha256': LISTING_AFTER}
    for name, expected in sorted(protected.items()):
        path = root / name
        if expected['mode'] == '120000':
            current = root
            for part in path.relative_to(root).parts[:-1]:
                current = current / part
                if current.is_symlink():
                    raise ValueError('linked publication source parent: ' + name)
            if not path.is_symlink() or sha(os.readlink(path).encode()) != expected['sha256']:
                raise ValueError('changed publication source link: ' + name)
        else:
            path = regular_path(root, name)
            mode = '100755' if path.stat().st_mode & stat.S_IXUSR else '100644'
            if identity(expected) != {'mode': mode, 'sha256': sha(path.read_bytes())}:
                raise ValueError('changed publication source: ' + name)
    for name in source_inventory(root):
        if name and name not in released and name not in CODE and not allowed_new(name):
            raise ValueError('unknown publication source: ' + name)
    historical = {name: entry['bytes'] for name, entry in before.items() if entry['mode'] != '120000'}
    return historical, set(product) | CODE
