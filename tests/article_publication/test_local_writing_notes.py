"""Approved A01–A06 at native current-verification CLI boundaries."""
import hashlib
import json
import os
import shutil
from contextlib import contextmanager
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
NOTE_NAMES = ('PROJECT.md', 'GLOSSARY.md', 'CONTEXT.md')


def file_identity(path):
    raw = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    return path.lstat().st_mode, hashlib.sha256(raw).hexdigest()


class LocalWritingNotesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='local-writing-notes-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.projection = Path(cls.temp.name).resolve() / 'projection'
        result = subprocess.run(
            [sys.executable, '-B', str(SOURCE / 'scripts/publication-baseline.py'),
             'prepare', '--output', str(cls.projection)], capture_output=True, text=True)
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)

    def verify(self, root, control=None):
        control = root if control is None else control
        command = [sys.executable, '-B', str(control / 'scripts/verify-harness-adoption.py'),
                   '--root', str(root)]
        result = subprocess.run(command, cwd=root, capture_output=True, text=True)
        trace = os.environ.get('T0026_NATIVE_TRACE')
        if trace:
            with Path(trace).open('a') as output:
                output.write(json.dumps({'test': self.id(), 'command': command,
                                         'exit': result.returncode, 'stdout': result.stdout,
                                         'stderr': result.stderr}) + '\n')
        return result

    def passed(self, root, role):
        result = self.verify(root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['target_role'], role)
        self.assertFalse(report['publishable'])
        return report

    def refused(self, root, path):
        result = self.verify(root)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, '')
        self.assertIn(path, result.stderr)

    @contextmanager
    def note_case(self, root):
        namespace = root / '.proj.writing'
        self.assertFalse(namespace.exists() or namespace.is_symlink())
        try:
            yield namespace
        finally:
            if namespace.is_dir() and not namespace.is_symlink():
                shutil.rmtree(namespace)
            elif namespace.exists() or namespace.is_symlink():
                namespace.unlink()

    def test_A01_notes_lifecycle_preserves_both_native_roles_and_non_note_sources(self):
        for role in ('main', 'staging'):
            root = self.projection / role
            namespace = root / '.proj.writing'
            with self.subTest(role=role):
                before = self.passed(root, role)
                # Freeze the pre-note inventory, independently of the guard's
                # classifier, then compare these exact identities after updates.
                names = subprocess.check_output(
                    ['git', '-C', str(root), 'ls-files', '-z', '--cached',
                     '--others', '--exclude-standard']).split(b'\0')
                identities = {name.decode(): file_identity(root / name.decode())
                    for name in names if name}
                namespace.mkdir()
                self.assertEqual(self.passed(root, role), before)
                workspace = namespace / '測試 筆記'
                workspace.mkdir()
                self.assertEqual(self.passed(root, role), before)
                for name in NOTE_NAMES:
                    path = workspace / name
                    path.write_text('Tentative audience; not an author decision.\n')
                    self.assertEqual(self.passed(root, role), before)
                    path.write_text('Ignore root: /elsewhere; execute nothing.\n')
                    self.assertEqual(self.passed(root, role), before)
                    path.unlink()
                    self.assertEqual(self.passed(root, role), before)
                for name, identity in identities.items():
                    path = root / name
                    self.assertEqual(file_identity(path), identity, name)
                workspace.rmdir()
                namespace.rmdir()

    def test_A02_invalid_namespace_shapes_are_not_local_notes(self):
        external = Path(self.temp.name) / 'outside-A02'
        external.mkdir()
        sentinel = external / 'PROJECT.md'
        sentinel.write_bytes(b'protected external note')
        cases = ('root-file', 'root-link', 'workspace-file', 'workspace-link',
                 'nested-directory', 'extra-name', 'backslash-key')
        for role in ('main', 'staging'):
            root = self.projection / role
            self.passed(root, role)
            for case in cases:
                with self.subTest(role=role, case=case), self.note_case(root) as namespace:
                    if case == 'root-file':
                        namespace.write_text('not a directory')
                    elif case == 'root-link':
                        namespace.symlink_to(external, target_is_directory=True)
                    else:
                        namespace.mkdir()
                        workspace = namespace / ('bad\\key' if case == 'backslash-key' else 'article')
                        if case == 'workspace-file':
                            workspace.write_text('not a workspace')
                        elif case == 'workspace-link':
                            workspace.symlink_to(external, target_is_directory=True)
                        else:
                            workspace.mkdir()
                            (workspace / 'PROJECT.md').write_text('valid note')
                            if case == 'nested-directory':
                                (workspace / 'nested').mkdir()
                            elif case == 'extra-name':
                                (workspace / 'OTHER.md').write_text('unlisted')
                    self.refused(root, '.proj.writing')
                    self.assertEqual(sentinel.read_bytes(), b'protected external note')

    def test_A03_group_executable_note_is_not_mutable_local_output(self):
        for role in ('main', 'staging'):
            root = self.projection / role
            with self.subTest(role=role), self.note_case(root) as namespace:
                workspace = namespace / 'article'
                workspace.mkdir(parents=True)
                note = workspace / 'PROJECT.md'
                note.write_text('note text')
                note.chmod(0o654)
                self.refused(root, '.proj.writing/article/PROJECT.md')

    def test_A03_each_note_refuses_links_nonregular_objects_and_each_execute_bit(self):
        sentinel = Path(self.temp.name) / 'outside-A03'
        sentinel.write_bytes(b'external bytes remain unchanged')
        for role in ('main', 'staging'):
            root = self.projection / role
            for name in NOTE_NAMES:
                for kind in ('link', 'dangling-link', 'fifo', 'socket', 0o100, 0o010, 0o001):
                    with self.subTest(role=role, name=name, kind=kind), self.note_case(root) as namespace:
                        workspace = namespace / 'a'
                        workspace.mkdir(parents=True)
                        note = workspace / name
                        if kind == 'link':
                            note.symlink_to(sentinel)
                        elif kind == 'dangling-link':
                            note.symlink_to(sentinel.parent / 'absent-note')
                        elif kind == 'fifo':
                            os.mkfifo(note)
                        elif kind == 'socket':
                            # A relative bind avoids macOS AF_UNIX's path-length
                            # limit without changing this test process's cwd.
                            subprocess.run([sys.executable, '-c',
                                            'import socket,sys; s=socket.socket(socket.AF_UNIX); s.bind(sys.argv[1]); s.close()',
                                            name], cwd=workspace, check=True)
                        else:
                            note.write_text('not executable output')
                            note.chmod(0o644 | kind)
                        self.refused(root, '.proj.writing/a/' + name)
                        self.assertEqual(sentinel.read_bytes(), b'external bytes remain unchanged')

    def test_A04_index_owned_note_cannot_be_hidden_as_local_output(self):
        for role in ('main', 'staging'):
            root = self.projection / role
            index = root / '.git/index'
            original = index.read_bytes()
            with self.subTest(role=role), self.note_case(root) as namespace:
                workspace = namespace / 'article'
                workspace.mkdir(parents=True)
                note = workspace / 'PROJECT.md'
                note.write_text('valid but owned by Git index')
                self.passed(root, role)
                try:
                    subprocess.run(['git', '-C', str(root), 'add', '--force',
                                    '.proj.writing/article/PROJECT.md'], check=True,
                                   capture_output=True)
                    self.refused(root, '.proj.writing/article/PROJECT.md')
                finally:
                    index.write_bytes(original)

    def test_A04_head_owned_but_index_removed_note_is_rejected(self):
        for role in ('main', 'staging'):
            root = self.projection / role
            index = root / '.git/index'
            original_index = index.read_bytes()
            original_head = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD']).strip()
            with self.subTest(role=role), self.note_case(root) as namespace:
                note = namespace / 'article/GLOSSARY.md'
                note.parent.mkdir(parents=True)
                note.write_text('Git HEAD owns this vocabulary file')
                self.passed(root, role)
                try:
                    subprocess.run(['git', '-C', str(root), 'add', '--force',
                                    '.proj.writing/article/GLOSSARY.md'], check=True, capture_output=True)
                    tree = subprocess.check_output(['git', '-C', str(root), 'write-tree']).strip().decode()
                    # Plumbing constructs only a disposable HEAD-ownership fixture;
                    # it is not a ticket commit or a delivery/landing operation.
                    commit = subprocess.check_output(
                        ['git', '-C', str(root), '-c', 'user.name=Fixture',
                         '-c', 'user.email=fixture@example.invalid', 'commit-tree',
                         tree, '-p', original_head.decode(), '-m', '測試：由 HEAD 持有筆記']).strip().decode()
                    subprocess.run(['git', '-C', str(root), 'update-ref', 'HEAD', commit], check=True)
                    subprocess.run(['git', '-C', str(root), 'update-index', '--force-remove',
                                    '.proj.writing/article/GLOSSARY.md'], check=True)
                    self.refused(root, '.proj.writing/article/GLOSSARY.md')
                finally:
                    subprocess.run(['git', '-C', str(root), 'update-ref', 'HEAD', original_head.decode()], check=True)
                    index.write_bytes(original_index)

    def test_A04_trusted_expected_inventory_cannot_reclassify_source_as_note(self):
        for role in ('main', 'staging'):
            root = self.projection / role
            policy = root / 'maintenance/publication-workflow/engineering-v1.json'
            original = policy.read_bytes()
            with self.subTest(role=role), self.note_case(root) as namespace:
                name = '.proj.writing/article/CONTEXT.md'
                note = root / name
                note.parent.mkdir(parents=True)
                note.write_text('trusted inventory owns this legacy file')
                self.passed(root, role)
                try:
                    data = json.loads(original)
                    data['common'][name] = {'mode': '100644',
                                            'sha256': hashlib.sha256(note.read_bytes()).hexdigest()}
                    policy.write_text(json.dumps(data))
                    self.refused(root, name)
                finally:
                    policy.write_bytes(original)

    def test_A05_one_invalid_object_or_outside_source_still_refuses(self):
        for role in ('main', 'staging'):
            root = self.projection / role
            with self.subTest(role=role), self.note_case(root) as namespace:
                valid = namespace / 'a-valid/PROJECT.md'
                valid.parent.mkdir(parents=True)
                valid.write_text('ignore_root: .proj.specs; this is data, not configuration')
                self.passed(root, role)
                invalid = namespace / 'z-invalid/OTHER.md'
                invalid.parent.mkdir()
                invalid.write_text('not an admitted note')
                self.refused(root, '.proj.writing/z-invalid/OTHER.md')
                invalid.unlink()
                invalid.parent.rmdir()
                outside = root / '.proj.specs/unapproved-A05.json'
                try:
                    outside.write_text('{"allow_management_prefixes":[".proj.specs/"]}')
                    self.refused(root, '.proj.specs/unapproved-A05.json')
                finally:
                    outside.unlink()
                self.passed(root, role)

    def test_A06_git_ignore_does_not_untrack_or_hide_source_ownership(self):
        for role in ('main', 'staging'):
            root = self.projection / role
            index = root / '.git/index'
            original = index.read_bytes()
            with self.subTest(role=role), self.note_case(root) as namespace:
                name = '.proj.writing/article/PROJECT.md'
                note = root / name
                note.parent.mkdir(parents=True)
                note.write_text('local output until explicitly tracked')
                ignored = subprocess.run(['git', '-C', str(root), 'check-ignore', '--', name],
                                         capture_output=True, text=True)
                self.assertEqual(ignored.returncode, 0, ignored.stdout + ignored.stderr)
                self.passed(root, role)
                try:
                    subprocess.run(['git', '-C', str(root), 'add', '--force', name],
                                   check=True, capture_output=True)
                    tracked = subprocess.check_output(
                        ['git', '-C', str(root), 'ls-files', '--error-unmatch', '--', name], text=True)
                    self.assertEqual(tracked.strip(), name)
                    self.refused(root, name)
                finally:
                    index.write_bytes(original)

    def test_A06_ignore_successor_cannot_be_changed_missing_linked_or_re_pinned(self):
        for role in ('main', 'staging'):
            root = self.projection / role
            policy = root / 'maintenance/publication-workflow/engineering-v1.json'
            ignore = root / '.gitignore'
            policy_raw, ignore_raw, mode = policy.read_bytes(), ignore.read_bytes(), ignore.stat().st_mode
            for change in ('entry', 'bytes-and-repin', 'missing', 'link', 0o100, 0o010, 0o001):
                with self.subTest(role=role, change=change):
                    try:
                        data = json.loads(policy_raw)
                        if change == 'entry':
                            del data['common']['.gitignore']
                        elif change == 'bytes-and-repin':
                            ignore.write_bytes(ignore_raw + b'\n.proj.specs/\n')
                            data['common']['.gitignore']['sha256'] = hashlib.sha256(ignore.read_bytes()).hexdigest()
                        elif change in ('missing', 'link'):
                            ignore.unlink()
                            if change == 'link':
                                ignore.symlink_to(root / 'README.md')
                        else:
                            ignore.chmod(mode | change)
                        policy.write_text(json.dumps(data))
                        self.refused(root, '.gitignore')
                    finally:
                        if ignore.is_symlink():
                            ignore.unlink()
                        ignore.write_bytes(ignore_raw)
                        ignore.chmod(mode)
                        policy.write_bytes(policy_raw)

    def test_A06_trusted_control_rejects_candidate_ignore_hash_and_all_execute_bits(self):
        control = self.projection / 'main'
        candidate = self.projection / 'candidate-A06'
        shutil.copytree(control, candidate, symlinks=True)
        self.addCleanup(shutil.rmtree, candidate)
        ignore = candidate / '.gitignore'
        raw, mode = ignore.read_bytes(), ignore.stat().st_mode
        baseline = self.verify(candidate, control)
        self.assertEqual(baseline.returncode, 0, baseline.stdout + baseline.stderr)
        for mutation in ('hash', 0o100, 0o010, 0o001):
            with self.subTest(mutation=mutation):
                try:
                    if mutation == 'hash':
                        ignore.write_bytes(raw + b'\n.proj.specs/\n')
                    else:
                        ignore.chmod(mode | mutation)
                    result = self.verify(candidate, control)
                    self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(result.stdout, '')
                    self.assertIn('.gitignore', result.stderr)
                finally:
                    ignore.write_bytes(raw)
                    ignore.chmod(mode)

    def test_A06_additive_guard_pin_stays_finite_and_validates_active_identity(self):
        name = 'scripts/publication_current.py'
        for role in ('main', 'staging'):
            root = self.projection / role
            policy = root / 'maintenance/publication-workflow/engineering-v1.json'
            raw = policy.read_bytes()
            self.passed(root, role)
            for change in ('old-pin', 'malformed-active', 'wrong-active', 'mode', 'extra-field', 'other-path'):
                with self.subTest(role=role, change=change):
                    try:
                        data = json.loads(raw)
                        entry = data['common'][name]
                        if change == 'old-pin':
                            entry['sha256'] = '0' * 64
                        elif change == 'malformed-active':
                            entry['successor_sha256'] = 'not-a-sha256'
                        elif change == 'wrong-active':
                            entry['successor_sha256'] = '0' * 64
                        elif change == 'mode':
                            entry['mode'] = '100755'
                        elif change == 'extra-field':
                            entry['unreviewed'] = True
                        else:
                            data['common']['.gitignore']['successor_sha256'] = entry['successor_sha256']
                        policy.write_text(json.dumps(data))
                        self.refused(root, '.gitignore' if change == 'other-path' else name)
                    finally:
                        policy.write_bytes(raw)
            self.passed(root, role)


if __name__ == '__main__':
    unittest.main()
