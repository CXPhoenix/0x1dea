"""Current public verifier acceptance and rejection in disposable Git clones."""
from contextlib import contextmanager
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
RECORD = 'maintenance/harness-reconciliation/test-contract-repair.json'


class SuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name) / 'candidate'
        subprocess.run(['git', 'clone', '--no-hardlinks', str(SOURCE), str(cls.root)], check=True, capture_output=True)
        changed = subprocess.check_output(['git', 'diff', 'HEAD', '--name-only', '-z'], cwd=SOURCE)
        added = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=SOURCE)
        for name in set(filter(None, (changed + added).decode().split('\0'))):
            source = SOURCE / name
            target = cls.root / name
            if not source.exists():
                target.unlink(missing_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target, follow_symlinks=False)
        result = subprocess.run(['python3', '-B', str(cls.root / 'scripts/verify-harness-adoption.py')],
                                cwd=cls.root, capture_output=True, text=True)
        if result.returncode:
            cls.temp.cleanup()
            raise AssertionError('positive control failed: ' + result.stdout + result.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def cli(self):
        return subprocess.run(['python3', '-B', str(self.root / 'scripts/verify-harness-adoption.py')],
                              cwd=self.root, capture_output=True, text=True)

    def test_00_exact_current_successor_passes_readonly_public_cli(self):
        before = subprocess.check_output(['git', 'status', '--porcelain', '-z'], cwd=self.root)
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"status": "pass"', result.stdout)
        self.assertEqual(subprocess.check_output(['git', 'status', '--porcelain', '-z'], cwd=self.root), before)

    @contextmanager
    def changed(self, name):
        path = self.root / name
        original = path.read_bytes()
        mode = path.stat().st_mode
        try:
            yield path
        finally:
            if path.is_symlink():
                path.unlink()
            path.write_bytes(original)
            path.chmod(mode)

    def rejected(self, diagnostic):
        result = self.cli()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(diagnostic, result.stdout + result.stderr)

    def test_product_and_repair_bytes_modes_missing_and_linked_sources_reject(self):
        for name, change in (
            ('blog/.vitepress/config.mts', 'bytes'),
            ('tests/fixtures/article-caption-entry.md', 'bytes'),
            ('package.json', 'bytes'),
            ('tests/harness_adoption/__init__.py', 'mode'),
            ('tests/fixtures/article-caption-migrated.md', 'missing'),
            ('tests/fixtures/article-caption-provenance.json', 'link'),
        ):
            with self.subTest(path=name, change=change), self.changed(name) as path:
                if change == 'bytes':
                    path.write_bytes(path.read_bytes() + b' ')
                elif change == 'mode':
                    path.chmod(path.stat().st_mode | 0o100)
                else:
                    path.unlink()
                    if change == 'link':
                        path.symlink_to(self.root / 'README.md')
                self.rejected(name)

    def test_record_changes_including_duplicate_missing_extra_and_wrong_pins_reject(self):
        import json
        for change in ('bytes', 'duplicate', 'missing', 'extra', 'before', 'after', 'pin', 'mode'):
            with self.subTest(change=change), self.changed(RECORD) as path:
                original = path.read_bytes()
                record = json.loads(original)
                rows = record['repair_delta']
                if change == 'duplicate':
                    rows.append(rows[0])
                elif change == 'missing':
                    rows.pop()
                elif change == 'extra':
                    rows.append(dict(rows[0], path='blog/unapproved.md'))
                elif change in ('before', 'after'):
                    record['product_delta'][0][change]['sha256'] = '0' * 64
                elif change == 'pin':
                    record['captured'] = '0' * 40
                elif change == 'mode':
                    rows[0]['after']['mode'] = '120000'
                path.write_bytes(original + b' ' if change == 'bytes' else json.dumps(record).encode())
                self.rejected('changed test repair provenance')

    def test_original_history_and_required_provenance_remain_enforced(self):
        for name in (
            'maintenance/harness-adoption/candidate-delta.json',
            'tests/fixtures/article-caption-baseline.json',
        ):
            with self.subTest(path=name), self.changed(name) as path:
                path.write_bytes(path.read_bytes() + b' ')
                self.rejected(name)
        for name in (
            'maintenance/harness-reconciliation/staging.json',
            'maintenance/harness-reconciliation/components.json',
            'maintenance/harness-reconciliation/article-electricity-revision.json',
        ):
            with self.subTest(path=name), self.changed(name) as path:
                path.unlink()
                self.rejected(name)
        with self.changed(RECORD) as path:
            path.unlink()
            self.rejected('current reconciliation source')

    def test_unknown_ignored_source_is_not_hidden_by_git(self):
        path = self.root / 'tests/unapproved_test.py'
        exclude = self.root / '.git/info/exclude'
        original = exclude.read_bytes()
        try:
            path.write_text('unapproved source')
            self.rejected('tests/unapproved_test.py')
            exclude.write_bytes(original + b'\ntests/unapproved_test.py\n')
            self.rejected('tests/unapproved_test.py')
        finally:
            path.unlink()
            exclude.write_bytes(original)

    def test_reviewed_code_requires_regular_existing_runner_and_guard_test(self):
        for name, change in (
            ('scripts/run-python-tests.py', 'missing'),
            ('tests/harness_adoption/test_successor.py', 'missing'),
            ('scripts/run-python-tests.py', 'link'),
        ):
            with self.subTest(path=name, change=change), self.changed(name) as path:
                path.unlink()
                if change == 'link':
                    path.symlink_to(self.root / 'scripts/verify-project.py')
                self.rejected(name)

    def test_captured_commit_must_be_present_and_ancestor_of_actual_head(self):
        head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root).decode().strip()
        try:
            subprocess.run(['git', 'update-ref', 'HEAD', 'f93237b1ed538484f24ed103ef00c7e5ee2e1828'], cwd=self.root, check=True)
            self.rejected('ancestor')
        finally:
            subprocess.run(['git', 'update-ref', 'HEAD', head], cwd=self.root, check=True)
        with tempfile.TemporaryDirectory() as temp:
            older = Path(temp) / 'older'
            subprocess.run(['git', 'init', str(older)], check=True, capture_output=True)
            subprocess.run(['git', 'fetch', '--no-tags', str(SOURCE), 'f93237b1ed538484f24ed103ef00c7e5ee2e1828'], cwd=older, check=True, capture_output=True)
            subprocess.run(['git', 'checkout', '--detach', 'FETCH_HEAD'], cwd=older, check=True, capture_output=True)
            absent = subprocess.run(['git', 'cat-file', '-e', '6e4eb804bcbda8504935be49fd6537d6327d5303^{commit}'], cwd=older, capture_output=True)
            self.assertNotEqual(absent.returncode, 0, 'fixture unexpectedly contains captured commit')
            saved = Path(temp) / 'original-git'
            (self.root / '.git').rename(saved)
            (older / '.git').rename(self.root / '.git')
            try:
                self.rejected('ancestor')
            finally:
                (self.root / '.git').rename(older / '.git')
                saved.rename(self.root / '.git')
