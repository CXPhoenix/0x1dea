"""Pinned historical epochs plus a separately enforced current source boundary."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

EPOCH = '724ddad73f8411a33c77c68d75f95b41d3af2988'
STAGING = '32cd6a9d4ead636ddc4e5020fceb35ad9645cc7f'
STAGE_DIGEST = '96011a4f53031ffffa4ab029c0eaaf3c01d34f50145a3e6da77c9deb42c59195'
COMPONENT_DIGEST = '5c72ce5d7a3b3dd370ddfe59bf595411adab5f618e738149034e1ea7505db377'
COMPONENT_PATHS = set(['blog/.vitepress/theme/components/ArticleSummary.vue', 'blog/.vitepress/theme/components/PreviewNotice.vue', 'blog/.vitepress/theme/index.ts', 'blog/.vitepress/theme/style.css', 'blog/post/course/security-awareness/electricity-privacy.md', 'blog/public/assets/post_course_security-awareness_electricity-privacy/article-banner.png', 'docs/article-summary.md', 'tests/articleSummary.vitest.ts', 'tests/fixtures/article-summary.md', 'tests/fixtures/component-acceptance.md', 'tests/previewNotice.vitest.ts', 'tests/previewNoticeArticle.vitest.ts'])
RECORDS = {'maintenance/harness-reconciliation/staging.json', 'maintenance/harness-reconciliation/components.json'}
CODE = {'scripts/harness_reconciliation.py', 'tests/harness_adoption/test_reconciliation.py'}
SUPPORT = {'maintenance/component-delivery/source-freeze.json', 'maintenance/component-delivery/TDD.md', 'maintenance/component-delivery/scope.md'}
GENERATED = {'blog/.vitepress/dist', 'blog/.vitepress/cache', 'blog/.vitepress/.temp'}
HISTORY = ('maintenance/harness-adoption/baseline-files.json', 'maintenance/harness-adoption/candidate-delta.json', 'maintenance/harness-adoption/framework-import-manifest.json', 'maintenance/article-publication/source-boundary.json', 'maintenance/lint-cleanup/source-boundary.json')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_tree(root, ref):
    rows = subprocess.check_output(['git', 'ls-tree', '-r', '-z', ref], cwd=root).split(b'\0')
    entries = []
    for row in rows:
        if row:
            meta, name = row.split(b'\t', 1)
            mode, kind, blob = meta.decode().split()
            if kind != 'blob':
                raise ValueError('unsupported pinned Git entry: ' + name.decode())
            entries.append((name.decode(), mode, blob))
    blobs = list(dict.fromkeys(v[2] for v in entries))
    raw = subprocess.check_output(['git', 'cat-file', '--batch'], input=('\n'.join(blobs) + '\n').encode(), cwd=root)
    contents = {}
    offset = 0
    for blob in blobs:
        end = raw.index(b'\n', offset)
        header = raw[offset:end].decode().split()
        if header[:2] != [blob, 'blob']:
            raise ValueError('invalid pinned Git blob')
        size = int(header[2]); offset = end + 1
        contents[blob] = raw[offset:offset + size]; offset += size + 1
    return {name: {'mode': mode, 'sha256': sha(contents[blob]), 'bytes': contents[blob]} for name, mode, blob in entries}


def identity(record):
    return None if record is None else {key: record[key] for key in ('mode', 'sha256')}


def source_inventory(root):
    names = set(filter(None, subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=root).decode().split('\0')))
    # Ignore rules must not hide compilable input. Runtime outputs are explicitly outside source scope.
    pending = [root / name for name in ('blog', 'tests', 'docs')]
    while pending:
        directory = pending.pop()
        if directory.is_symlink():
            raise ValueError('linked current source: ' + directory.relative_to(root).as_posix())
        with os.scandir(directory) as items:
            for entry in items:
                path = Path(entry.path); name = path.relative_to(root).as_posix()
                mode = entry.stat(follow_symlinks=False).st_mode
                if name in GENERATED or (name.startswith('tests/') and entry.name == '__pycache__'):
                    if stat.S_ISLNK(mode):
                        raise ValueError('linked generated directory: ' + name)
                    continue
                if stat.S_ISLNK(mode):
                    raise ValueError('linked current source: ' + name)
                if stat.S_ISDIR(mode):
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    names.add(name)
                else:
                    raise ValueError('nonregular current source: ' + name)
    return names


def check(root, allowed_new, regular_path, ancestry):
    stage_path = root / 'maintenance/harness-reconciliation/staging.json'
    if not stage_path.exists():
        return {}, set()
    stage_raw = regular_path(root, stage_path.relative_to(root).as_posix()).read_bytes()
    if sha(stage_raw) != STAGE_DIGEST:
        raise ValueError('changed reconciliation staging provenance')
    stage = json.loads(stage_raw)
    if stage['epoch'] != EPOCH or stage['staging'] != STAGING:
        raise ValueError('unapproved reconciliation pins')
    ancestry(root, EPOCH); ancestry(root, STAGING)
    old = git_tree(root, EPOCH); known = git_tree(root, STAGING)
    expected_delta = {name: (identity(old.get(name)), identity(known.get(name))) for name in set(old) | set(known) if identity(old.get(name)) != identity(known.get(name))}
    received = {row['path']: (row['before'], row['after']) for row in stage['historical_delta']}
    if received != expected_delta or len(received) != len(stage['historical_delta']):
        raise ValueError('invalid historical reconciliation delta')
    for name in HISTORY:
        if regular_path(root, name).read_bytes() != old[name]['bytes']:
            raise ValueError('changed historical reconciliation source: ' + name)
    current = {name: identity(value) for name, value in known.items() if not allowed_new(name)}
    component_path = root / 'maintenance/harness-reconciliation/components.json'
    if component_path.exists():
        raw = regular_path(root, component_path.relative_to(root).as_posix()).read_bytes()
        if sha(raw) != COMPONENT_DIGEST:
            raise ValueError('changed reconciliation component provenance')
        component = json.loads(raw)
        if component['base'] != STAGING or {row['path'] for row in component['delta']} != COMPONENT_PATHS or len(component['delta']) != len(COMPONENT_PATHS):
            raise ValueError('unapproved reconciliation component scope')
        for row in component['delta']:
            name = row['path']
            if row['before'] != identity(known.get(name)):
                raise ValueError('invalid component predecessor: ' + name)
            current[name] = row['after']
    for name, expected in current.items():
        if expected['mode'] == '120000':
            path = root / name
            for parent in path.parents:
                if parent == root:
                    break
                if parent.is_symlink():
                    raise ValueError('linked current source parent: ' + name)
            if not path.is_symlink() or sha(os.readlink(path).encode()) != expected['sha256']:
                raise ValueError('changed current reconciliation symlink: ' + name)
            continue
        path = regular_path(root, name)
        mode = '100755' if path.stat().st_mode & stat.S_IXUSR else '100644'
        if {'mode': mode, 'sha256': sha(path.read_bytes())} != expected:
            raise ValueError('changed current reconciliation source: ' + name)
    for name in SUPPORT:
        if (root / name).exists() or (root / name).is_symlink():
            regular_path(root, name)
    for name in source_inventory(root):
        if name not in current and not allowed_new(name) and name not in RECORDS | CODE | SUPPORT:
            raise ValueError('unknown current reconciliation source: ' + name)
    return {name: entry['bytes'] for name, entry in old.items() if entry['mode'] != '120000'}, set(current) | RECORDS | CODE | SUPPORT
