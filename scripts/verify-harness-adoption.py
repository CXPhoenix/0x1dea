#!/usr/bin/env python3
"""Validate local Harness tracker, provenance and approved product boundaries."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import os
import stat
import subprocess


def git_blob(content):
    return hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()


def frontmatter(path):
    text = path.read_text()
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        raise ValueError(f'missing frontmatter: {path}')
    data = {}
    for line in text.split('\n---\n', 1)[0][4:].splitlines():
        match = re.fullmatch(r'([a-z_]+):\s*(.*)', line)
        if not match or match[1] in data:
            raise ValueError(f'unsupported or duplicate frontmatter: {path}: {line}')
        data[match[1]] = match[2].strip().strip('"').strip("'")
    return data


def regular_path(root, name):
    path = Path(name)
    if path.is_absolute() or '..' in path.parts or not name:
        raise ValueError(f'unsafe evidence/source path: {name}')
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'linked evidence/source path: {name}')
    if not current.is_file():
        raise ValueError(f'missing evidence/source path: {name}')
    return current


def check_tickets(root):
    tickets = {}
    for path in sorted((root / '.proj.tickets').glob('**/T-*.md')):
        data = frontmatter(path)
        ticket_id = data.get('id', '')
        if not re.fullmatch(r'T-\d{4}', ticket_id) or not path.name.startswith(ticket_id + '-'):
            raise ValueError(f'invalid ticket id/path: {path}')
        if ticket_id in tickets:
            raise ValueError(f'duplicate ticket id: {ticket_id}')
        if data.get('epic') != path.parent.name or not data.get('title'):
            raise ValueError(f'invalid epic/title: {path}')
        if data.get('status') not in {'todo', 'processing', 'review', 'done', 'pending'}:
            raise ValueError(f'invalid stored status: {path}')
        raw = data.get('blocked_by', '')
        if not re.fullmatch(r'\[(?:\s*T-\d{4}\s*(?:,\s*T-\d{4}\s*)*)?\]', raw):
            raise ValueError(f'invalid blocked_by list: {path}')
        data['blocked_by'] = re.findall(r'T-\d{4}', raw)
        if len(set(data['blocked_by'])) != len(data['blocked_by']):
            raise ValueError(f'duplicate dependency: {path}')
        if data['status'] == 'pending':
            for key in ('pending_reason', 'pending_evidence', 'pending_on', 'revisit_when'):
                if not data.get(key): raise ValueError(f'pending missing {key}: {path}')
            try: date.fromisoformat(data['pending_on'])
            except ValueError: raise ValueError(f'invalid pending date: {path}') from None
            regular_path(root, data['pending_evidence'].split('#', 1)[0])
        if data['status'] == 'done':
            try:
                landing = json.loads(regular_path(root, data.get('landing_evidence', '')).read_text())
                if landing.get('ticket') != ticket_id or landing.get('authorized') is not True or landing.get('landed') is not True or not re.fullmatch(r'[a-f0-9]{40}', landing.get('commit', '')) or not landing.get('approval_receipt') or landing.get('target') != 'staging':
                    raise ValueError('incomplete landing record')
                regular_path(root, landing['approval_receipt'])
                subprocess.run(['git', 'cat-file', '-e', landing['commit'] + '^{commit}'], cwd=root, check=True, capture_output=True)
                subprocess.run(['git', 'merge-base', '--is-ancestor', landing['commit'], 'staging'], cwd=root, check=True, capture_output=True)
            except (ValueError, KeyError, subprocess.CalledProcessError):
                raise ValueError(f'missing/invalid landing evidence: {path}') from None
        tickets[ticket_id] = data
    visiting, visited = set(), set()
    def visit(ticket_id):
        if ticket_id in visiting: raise ValueError(f'dependency cycle: {ticket_id}')
        if ticket_id in visited: return
        visiting.add(ticket_id)
        for dependency in tickets[ticket_id]['blocked_by']:
            if dependency == ticket_id: raise ValueError(f'self dependency: {ticket_id}')
            if dependency not in tickets: raise ValueError(f'missing dependency: {dependency}')
            visit(dependency)
        visiting.remove(ticket_id)
        visited.add(ticket_id)
    for ticket_id in tickets: visit(ticket_id)
    blocked = {i: [d for d in t['blocked_by'] if tickets[d]['status'] != 'done'] for i, t in tickets.items()}
    return {'tickets': tickets, 'next_id': f"T-{max((int(i[2:]) for i in tickets), default=0) + 1:04d}", 'frontier': [i for i, t in tickets.items() if t['status'] == 'todo' and not blocked[i]], 'blocked': {i: d for i, d in blocked.items() if d}, 'paused': [i for i, t in tickets.items() if t['status'] == 'pending']}


def check_translation(path, root):
    data = frontmatter(path)
    name = data.get('synced_from', '')
    source_name = str((path.parent / name).relative_to(root)) if name else ''
    source = regular_path(root, source_name)
    if git_blob(source.read_bytes()) != data.get('synced_from_sha'):
        raise ValueError(f'stale translation: {path}')
    return source_name


def entry_sha(path):
    data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def check_preserved(root, baseline, exceptions):
    moves = []
    for entry in baseline:
        name = entry['path']
        if name in exceptions:
            expected = exceptions[name]
            if expected.get('retired'):
                if (root / name).exists() or (root / name).is_symlink():
                    raise ValueError(f'retired active entry remains: {name}')
                path = regular_path(root, expected['archive'])
            elif expected.get('generated'):
                if (root / name).is_symlink() or not (root / name).is_dir():
                    raise ValueError(f'generated package absent/linked: {name}')
                continue
            else:
                path = regular_path(root, name)
            wanted = expected.get('sha256', entry['sha256'])
        else:
            mapped = 'blog/' + name[5:] if name.startswith('docs/') else name
            path = root / mapped
            if name.startswith('docs/'):
                if (root / name).exists() or (root / name).is_symlink():
                    raise ValueError(f'old website path remains: {name}')
                moves.append({'source': name, 'candidate': mapped, 'sha256': entry['sha256']})
            wanted = entry['sha256']
            expected_link = entry['type'] == 'symlink'
            if path.is_symlink() != expected_link or (not path.is_symlink() and not path.is_file()):
                raise ValueError(f'changed entry type/missing file: {mapped}')
        if entry_sha(path) != wanted:
            raise ValueError(f'changed preserved source: {name}')
    return moves


def allowed_new(name):
    prefixes = ('.proj.specs/', '.proj.tickets/', 'docs/agents/', 'docs/adr/', 'docs/security/', 'maintenance/harness-adoption/', '.agents/skills/', '.claude/skills/', '.claude/agents/', '.codex/')
    exact = {'docs/README.md', 'docs/guide.md', 'scripts/verify-project.py', 'scripts/verify-harness-adoption.py', 'scripts/materialize-writing-skills.py', 'skills-lock.json', 'THIRD_PARTY_NOTICES.md', 'CONTEXT.md', 'tests/harness_adoption/test_tracker.py', 'tests/harness_adoption/test_materializer.py', 'tests/harness_adoption/test_publication.py'}
    return name in exact or name.startswith(prefixes)


def check_added_paths(root, baseline_names, moved):
    names = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=root).decode().split('\0')
    for name in names:
        if name and name not in baseline_names and name not in moved and not allowed_new(name):
            raise ValueError(f'unknown added product file: {name}')


def check_readme_scripts(root):
    scripts = json.loads(regular_path(root, 'package.json').read_text())['scripts']
    readme = regular_path(root, 'README.md').read_text()
    commands = set(re.findall(r'\bpnpm\s+(?:run\s+)?([A-Za-z0-9_.-]+:[A-Za-z0-9_.:-]+)\b', readme))
    for command in sorted(commands):
        if command not in scripts:
            raise ValueError(f'README names an unknown package script: {command}')
    return sorted(commands)


EVIDENCE_STATUSES = {'pass', 'existing-failure', 'new-regression', 'blocked', 'not-run', 'expected-red'}


def check_evidence(root, record):
    if record.get('status') not in EVIDENCE_STATUSES:
        raise ValueError('invalid evidence status')
    if record['status'] == 'pass':
        if record.get('exit_code') != 0 or not record.get('log_sha256'):
            raise ValueError('passed evidence lacks successful execution')
        log = regular_path(root, record.get('log', ''))
        if entry_sha(log) != record['log_sha256']:
            raise ValueError('evidence log hash mismatch')


def check_trace(root, tickets):
    path = root / '.proj.specs/0001-harness-adoption/candidate-traceability.json'
    rows = json.loads(path.read_text())
    baseline = json.loads((path.parent / 'baseline-traceability.json').read_text())
    if len(rows) != 113 or len({r['row_id'] for r in rows}) != 113:
        raise ValueError('historical trace row count/id mismatch')
    by_id = {r['row_id']: r for r in baseline}
    for row in rows:
        original = by_id[row['row_id']]
        for key in ('source_path', 'source_sha256', 'source_git_blob', 'expected_behavior', 'heading'):
            if row[key] != original[key]: raise ValueError(f'changed baseline trace {key}: {row["row_id"]}')
        source = regular_path(root, row['source_path'])
        if entry_sha(source) != row['source_sha256'] or git_blob(source.read_bytes()) != row['source_git_blob']:
            raise ValueError(f'dangling/changed trace source: {row["row_id"]}')
        if row.get('ticket') not in tickets: raise ValueError(f'dangling trace ticket: {row["row_id"]}')
        criterion = row.get('AC', '')
        values = criterion if isinstance(criterion, list) else [criterion]
        if not values or any(not re.fullmatch(r'HA-0[1-9]|HA-10', v) for v in values): raise ValueError('dangling AC')
        status = row.get('evidence_status', 'not-run')
        if status not in EVIDENCE_STATUSES: raise ValueError('invalid trace evidence status')
        if status == 'pass' and not row.get('actual_evidence'): raise ValueError('false passed trace')
        for name in row.get('actual_evidence', []):
            record = json.loads(regular_path(root, name).read_text())
            check_evidence(root, record)
            if status == 'pass' and record['status'] != 'pass':
                raise ValueError(f'passed trace references nonpass evidence: {row["row_id"]}: {name}')
    return len(rows)


def check_baseline_manifest(root, baseline):
    expected_commit = 'ee7fecfff72f47abc735d26ac7e9a943de04ebbf'
    if baseline.get('baseline') != expected_commit: raise ValueError('unapproved baseline')
    actual = []
    for raw in subprocess.check_output(['git', 'ls-tree', '-r', '-z', expected_commit], cwd=root).split(b'\0'):
        if not raw: continue
        metadata, name = raw.split(b'\t', 1)
        mode, kind, blob = metadata.decode().split()
        content = subprocess.check_output(['git', 'cat-file', 'blob', blob], cwd=root)
        actual.append({'path': name.decode(), 'type': 'symlink' if mode == '120000' else 'regular', 'sha256': hashlib.sha256(content).hexdigest()})
    if actual != baseline.get('files'): raise ValueError('baseline manifest differs from actual pinned Git tree')


def check_framework(root):
    """Verify the immutable initialized framework import, including its provenance."""
    manifest = regular_path(root, 'maintenance/harness-adoption/framework-import-manifest.json')
    raw = manifest.read_bytes()
    data = json.loads(raw)
    if data.get('source_commit') != '917e6025da0901a79dda016e1ce5bd89b6e6e19f':
        raise ValueError('unapproved framework template commit')
    if data.get('source_digest') != 'b7782890459cf3c546395ac5546f22dc074f13d4166688751a9c1e08d4216bf5':
        raise ValueError('unapproved framework template digest')
    # Pin the approved manifest itself: deleting or repinning one of its entries
    # must not turn a modified framework into an apparently verified import.
    if hashlib.sha256(raw).hexdigest() != 'b0fb7cf39924c3371be420bce8f3c8c6f1356fcd0f2dc5a24f538e9192718d7e':
        raise ValueError('framework import manifest differs from approved pins')
    files = data['initialized_snapshot_files']
    if len(files) != 641 or data.get('new_tuning_executed') is not False:
        raise ValueError('framework import count/tuning provenance mismatch')
    for name, expected in files.items():
        path = regular_path(root, name)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'framework source SHA mismatch: {name}')
    product = {'phoenix-writing', 'maintaining-writing-skills', 'creating-vitepress-post'}
    catalogs = {}
    for runtime in ('.agents', '.claude'):
        prefix = runtime + '/skills/'
        framework = {name[len(prefix):].split('/', 1)[0] for name in files if name.startswith(prefix)}
        if len(framework) != 32 or framework & product:
            raise ValueError('framework runtime catalog provenance mismatch')
        base = root / runtime / 'skills'
        actual = set()
        for entry in os.scandir(base):
            if entry.is_symlink() or not entry.is_dir(follow_symlinks=False):
                raise ValueError(f'nonphysical runtime skill root: {entry.path}')
            actual.add(entry.name)
        if actual != framework | product:
            raise ValueError(f'unknown/missing runtime skill roots: {runtime}')
        for name in actual:
            regular_path(root, prefix + name + '/SKILL.md')
        # scandir errors propagate: a partially unreadable tree must not be
        # reported as fully verified. Never follow a directory symlink.
        pending = [base]
        while pending:
            with os.scandir(pending.pop()) as entries:
                for entry in entries:
                    path = Path(entry.path)
                    mode = entry.stat(follow_symlinks=False).st_mode
                    if stat.S_ISLNK(mode):
                        raise ValueError(f'runtime symlink rejected: {path.relative_to(root)}')
                    if stat.S_ISDIR(mode):
                        pending.append(path)
                    elif stat.S_ISREG(mode):
                        name = path.relative_to(root).as_posix()
                        skill = name[len(prefix):].split('/', 1)[0]
                        if skill in framework and name not in files:
                            raise ValueError(f'unpinned framework file: {name}')
                    else:
                        raise ValueError(f'nonregular runtime entry: {path.relative_to(root)}')
        catalogs[runtime] = len(actual)
    return {'pinned_files': len(files), 'source_commit': data['source_commit'],
            'source_digest': data['source_digest'], 'runtime_skill_counts': catalogs}


EXCEPTION_NAMES = {
    'AGENTS.md', 'CLAUDE.md', 'GEMINI.md', '.gitignore', 'README.md', 'package.json',
    'scripts/vpHelper.ts', 'tests/vpHelper.vitest.ts', 'tsconfig.json',
    'skills/creating-vitepress-post/SKILL.md', 'skills/phoenix-writing/AGENTS.md',
    'skills/maintaining-writing-skills/SKILL.md',
    'skills/maintaining-writing-skills/references/spectra-codex.md',
    'skills/maintaining-writing-skills/references/skill-maintenance.md',
}


def approved_exception_names(entries):
    names = set(EXCEPTION_NAMES)
    for entry in entries:
        name = entry['path']
        if (name.startswith(('.claude/', '.gemini/', '.github/')) and 'spectra-' in name) or name.startswith('.gemini/commands/spectra/'):
            names.add(name)
        if name.startswith(('.agents/skills/', '.claude/skills/')) and entry['type'] == 'symlink':
            names.add(name)
    return names


def check_adoption_ancestry(root, baseline_commit):
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode().strip()
    result = subprocess.run(['git', 'merge-base', '--is-ancestor', baseline_commit, head], cwd=root, capture_output=True)
    if result.returncode != 0:
        raise ValueError('pinned baseline is not an ancestor of HEAD')
    return head


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    baseline = json.loads((root / 'maintenance/harness-adoption/baseline-files.json').read_text())
    delta = json.loads((root / 'maintenance/harness-adoption/candidate-delta.json').read_text())
    check_baseline_manifest(root, baseline)
    framework = check_framework(root)
    check_readme_scripts(root)
    if set(delta['exceptions']) != approved_exception_names(baseline['files']):
        raise ValueError('unapproved/missing exception entry')
    check_adoption_ancestry(root, baseline['baseline'])
    moves = check_preserved(root, baseline['files'], delta['exceptions'])
    if len(moves) != 55: raise ValueError('site move count mismatch')
    baseline_names = {f['path'] for f in baseline['files']}
    moved = {m['candidate'] for m in moves}
    check_added_paths(root, baseline_names, moved)
    for name, expected in delta['literal_adapters'].items():
        content = subprocess.check_output(['git', 'show', baseline['baseline'] + ':' + name], cwd=root).decode()
        if name == 'package.json':
            for verb in ('dev', 'build', 'preview'): content = content.replace(f'vitepress {verb} docs', f'vitepress {verb} blog')
        elif name == 'tsconfig.json': content = content.replace('"docs/', '"blog/')
        else:
            content = content.replace('docs', 'blog')
            if name == 'tests/vpHelper.vitest.ts': content = content.replace('expect(config.options.dir).toBe(DEFAULT_DIR);', "expect(config.options.dir).toBe('blog/post');")
        if (root / name).read_text() != content: raise ValueError(f'nonliteral adapter change: {name}')
    state = check_tickets(root)
    translations = list((root / '.proj.specs').glob('**/spec.zh-TW.md'))
    if len(translations) != 7: raise ValueError('six baseline + one adoption translations required')
    for path in translations: check_translation(path, root)
    trace_count = check_trace(root, state['tickets'])
    print(json.dumps({'status': 'pass', 'framework': framework, 'site_moves': len(moves), 'baseline_entries': len(baseline['files']), 'translations': len(translations), 'trace_rows': trace_count, 'tracker': state}, indent=2))


if __name__ == '__main__':
    try: main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        raise SystemExit(f'FAIL: {error}')
