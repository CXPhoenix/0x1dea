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
REVISION_BASE = '69ff85f5fe1baddb54102070a436dff9ac1c5b73'
REVISION_RECORD = 'maintenance/harness-reconciliation/article-electricity-revision.json'
REVISION_DIGEST = 'a59ff8d81971f9ee85b92fa2eb940f6c7018d182454ded89169bbf27e8c125f9'
REVISION_PATHS = {
    'blog/post/course/security-awareness/electricity-privacy.md',
    'blog/public/assets/post_course_security-awareness_electricity-privacy/p-cat-event.png',
    'blog/public/assets/post_course_security-awareness_electricity-privacy/p-midnight-event.png',
}
COMPONENT_PATHS = set(['blog/.vitepress/theme/components/ArticleSummary.vue', 'blog/.vitepress/theme/components/PreviewNotice.vue', 'blog/.vitepress/theme/index.ts', 'blog/.vitepress/theme/style.css', 'blog/post/course/security-awareness/electricity-privacy.md', 'blog/public/assets/post_course_security-awareness_electricity-privacy/article-banner.png', 'docs/article-summary.md', 'tests/articleSummary.vitest.ts', 'tests/fixtures/article-summary.md', 'tests/fixtures/component-acceptance.md', 'tests/previewNotice.vitest.ts', 'tests/previewNoticeArticle.vitest.ts'])
REPAIR_BASE = 'f93237b1ed538484f24ed103ef00c7e5ee2e1828'
REPAIR_CAPTURE = '6e4eb804bcbda8504935be49fd6537d6327d5303'
REPAIR_RECORD = 'maintenance/harness-reconciliation/test-contract-repair.json'
REPAIR_DIGEST = 'd5d286235aaf60ac04389a1fc76ab396a3dde087270856be36d804c9e3937aeb'
PRODUCT_PATHS = {'blog/.vitepress/theme/index.ts', 'docs/authoring/article-captions.md', 'tests/encoreTicket.vitest.ts', 'blog/.vitepress/markdown/articleCaptions.ts', 'tests/fixtures/article-caption-baseline.json', 'docs/components/encore-ticket.md', 'tests/articleCaptions.vitest.ts', 'skills/phoenix-writing/references/context-form.md', 'maintenance/writing-skills/VALIDATION.md', 'blog/.vitepress/config.mts', 'maintenance/writing-skills/SOURCES.md', 'blog/.vitepress/theme/components/EncoreTicket.vue', 'skills/phoenix-writing/SKILL.md', 'blog/post/course/security-awareness/electricity-privacy.md', 'blog/.vitepress/theme/style.css'}
REPAIR_PATHS = {'tests/fixtures/article-caption-entry.md', 'tests/articleCaptions.vitest.ts', 'tests/fixtures/article-caption-provenance.json', 'tests/article_publication/__init__.py', 'README.md', 'tests/harness_adoption/__init__.py', 'tests/fixtures/article-caption-migrated.md', 'package.json'}
RECORDS = {'maintenance/harness-reconciliation/staging.json', 'maintenance/harness-reconciliation/components.json', REVISION_RECORD, REPAIR_RECORD}
CODE = {'tests/harness_adoption/test_test_runner.py', 'scripts/verify-harness-adoption.py', 'tests/harness_adoption/test_successor.py', 'tests/harness_adoption/test_reconciliation.py', 'scripts/harness_reconciliation.py', 'scripts/run-python-tests.py'}
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


def apply_repair(root, current, allowed_new, regular_path, ancestry):
    """Validate a reviewed, exact successor; never derive approval from live bytes."""
    raw = regular_path(root, REPAIR_RECORD).read_bytes()
    if sha(raw) != REPAIR_DIGEST:
        raise ValueError('changed test repair provenance')
    record = json.loads(raw)
    if (set(record) != {'version', 'predecessor', 'captured', 'product_delta', 'repair_delta'}
            or record['version'] != 1 or record['predecessor'] != REPAIR_BASE
            or record['captured'] != REPAIR_CAPTURE):
        raise ValueError('unapproved test repair pins or fields')
    ancestry(root, REPAIR_BASE); ancestry(root, REPAIR_CAPTURE)
    if subprocess.run(['git', 'merge-base', '--is-ancestor', REPAIR_BASE, REPAIR_CAPTURE], cwd=root).returncode:
        raise ValueError('invalid test repair predecessor ancestry')
    before = git_tree(root, REPAIR_BASE); captured = git_tree(root, REPAIR_CAPTURE)
    delta = {name for name in set(before) | set(captured)
             if not allowed_new(name) and identity(before.get(name)) != identity(captured.get(name))}
    if delta != PRODUCT_PATHS:
        raise ValueError('incomplete protected test repair product scope')
    for key, names in (('product_delta', PRODUCT_PATHS), ('repair_delta', REPAIR_PATHS)):
        rows = record[key]
        if len(rows) != len(names) or {row['path'] for row in rows} != names:
            raise ValueError('unapproved test repair scope: ' + key)
        for row in rows:
            if set(row) != {'path', 'before', 'after'}:
                raise ValueError('invalid test repair identity fields')
            name = row['path']
            predecessor = before if key == 'product_delta' else captured
            if row['before'] != identity(predecessor.get(name)) or row['before'] != current.get(name):
                raise ValueError('invalid test repair predecessor: ' + name)
            after = row['after']
            if (not isinstance(after, dict) or set(after) != {'mode', 'sha256'}
                    or after['mode'] not in {'100644', '100755'}
                    or not isinstance(after['sha256'], str) or len(after['sha256']) != 64
                    or any(c not in '0123456789abcdef' for c in after['sha256'])):
                raise ValueError('unsupported test repair source identity: ' + name)
            if key == 'product_delta' and after != identity(captured.get(name)):
                raise ValueError('invalid test repair captured source: ' + name)
            current[name] = after


def check(root, allowed_new, regular_path, ancestry):
    stage_path = root / 'maintenance/harness-reconciliation/staging.json'
    repair_path = root / REPAIR_RECORD
    has_repair = repair_path.exists() or repair_path.is_symlink()
    if has_repair:
        for name in ('maintenance/harness-reconciliation/staging.json', 'maintenance/harness-reconciliation/components.json', REVISION_RECORD):
            regular_path(root, name)
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
    revision_path = root / REVISION_RECORD
    if revision_path.exists() or revision_path.is_symlink():
        if not component_path.exists():
            raise ValueError('article revision requires component provenance')
        raw = regular_path(root, REVISION_RECORD).read_bytes()
        if sha(raw) != REVISION_DIGEST:
            raise ValueError('changed article revision provenance')
        revision = json.loads(raw)
        if revision['base'] != REVISION_BASE or {row['path'] for row in revision['delta']} != REVISION_PATHS or len(revision['delta']) != len(REVISION_PATHS):
            raise ValueError('unapproved article revision scope or pin')
        ancestry(root, REVISION_BASE)
        predecessor = git_tree(root, REVISION_BASE)
        for row in revision['delta']:
            name = row['path']
            if row['before'] != identity(predecessor.get(name)) or row['before'] != current.get(name):
                raise ValueError('invalid article revision predecessor: ' + name)
            current[name] = row['after']
    if has_repair:
        # Reviewed code is a trust root, but must still be present and regular.
        for name in sorted(CODE):
            regular_path(root, name)
        apply_repair(root, current, allowed_new, regular_path, ancestry)
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
