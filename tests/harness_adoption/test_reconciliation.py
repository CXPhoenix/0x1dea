"""Public verifier accepts exact epochs while rejecting current drift."""
import shutil
import json
from contextlib import contextmanager
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2]


class ReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name) / 'candidate'
        subprocess.run(['git', 'clone', '--no-hardlinks', str(SOURCE), str(cls.root)], check=True, capture_output=True)
        subprocess.run(['git', 'checkout', '--detach', '69ff85f5fe1baddb54102070a436dff9ac1c5b73'], cwd=cls.root, check=True, capture_output=True)
        for name in ('scripts/verify-harness-adoption.py', 'scripts/harness_reconciliation.py', 'maintenance/harness-reconciliation/staging.json'):
            path = SOURCE / name
            if path.exists():
                target = cls.root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def cli(self):
        return subprocess.run(['python3', str(self.root / 'scripts/verify-harness-adoption.py')], cwd=self.root, capture_output=True, text=True)

    def test_00_clean_pinned_staging_reaches_successful_readonly_full_cli(self):
        before = {str(path.relative_to(self.root)) for path in self.root.rglob('*') if '.git' not in path.relative_to(self.root).parts}
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"status": "pass"', result.stdout)
        after = {str(path.relative_to(self.root)) for path in self.root.rglob('*') if '.git' not in path.relative_to(self.root).parts}
        self.assertEqual(after, before, 'read-only CLI created source-tree artifacts')

    @contextmanager
    def overlay(self):
        record = json.loads((SOURCE / 'maintenance/harness-reconciliation/components.json').read_text())
        names = [row['path'] for row in record['delta']] + ['maintenance/harness-reconciliation/components.json']
        backups = {name: (self.root / name).read_bytes() if (self.root / name).exists() else None for name in names}
        try:
            for name in names:
                target = self.root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(subprocess.check_output(['git', 'show', '69ff85f5fe1baddb54102070a436dff9ac1c5b73:' + name], cwd=SOURCE))
            yield
        finally:
            for name, data in backups.items():
                path = self.root / name
                if path.is_symlink():
                    path.unlink()
                if data is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(data)

    @contextmanager
    def revision(self):
        record_name = 'maintenance/harness-reconciliation/article-electricity-revision.json'
        record = json.loads((SOURCE / record_name).read_text())
        names = [row['path'] for row in record['delta']] + [record_name]
        backups = {name: (self.root / name).read_bytes() if (self.root / name).exists() else None for name in names}
        try:
            for name in names:
                target = self.root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(subprocess.check_output(['git', 'show', 'f93237b1ed538484f24ed103ef00c7e5ee2e1828:' + name], cwd=SOURCE))
            yield
        finally:
            for name, data in backups.items():
                path = self.root / name
                if path.is_symlink():
                    path.unlink()
                if data is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(data)

    def test_exact_authorized_article_revision_passes_public_cli(self):
        with self.revision():
            result = self.cli()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('"status": "pass"', result.stdout)

    def test_revision_rejects_source_bytes_mode_missing_and_links(self):
        with self.revision():
            record = json.loads((SOURCE / 'maintenance/harness-reconciliation/article-electricity-revision.json').read_text())
            for row in record['delta']:
                name = row['path']; path = self.root / name
                original = path.read_bytes(); mode = path.stat().st_mode
                for change in ('bytes', 'mode', 'missing', 'link'):
                    with self.subTest(path=name, change=change):
                        try:
                            if change == 'bytes':
                                path.write_bytes(original + b'tamper')
                            elif change == 'mode':
                                path.chmod(mode | 0o100)
                            else:
                                path.unlink()
                                if change == 'link':
                                    path.symlink_to(self.root / 'blog/.vitepress/config.mts')
                            self.rejected(name)
                        finally:
                            if path.is_symlink():
                                path.unlink()
                            path.write_bytes(original); path.chmod(mode)

    def test_revision_rejects_record_before_hash_and_pin_tampering(self):
        with self.revision():
            path = self.root / 'maintenance/harness-reconciliation/article-electricity-revision.json'
            original = path.read_bytes()
            for change in ('record', 'before', 'base', 'path'):
                with self.subTest(change=change):
                    try:
                        record = json.loads(original)
                        if change == 'before':
                            record['delta'][0]['before']['sha256'] = '0' * 64
                        elif change == 'base':
                            record['base'] = '0' * 40
                        elif change == 'path':
                            record['delta'][0]['path'] = 'blog/post/not-approved.md'
                        path.write_bytes(original + b' ' if change == 'record' else json.dumps(record).encode())
                        self.rejected('article revision provenance')
                    finally:
                        path.write_bytes(original)

    def test_revision_requires_both_records_and_preserves_history(self):
        with self.revision():
            for name, diagnostic in (
                ('maintenance/harness-reconciliation/article-electricity-revision.json', 'current reconciliation source'),
                ('maintenance/harness-reconciliation/components.json', 'requires component provenance'),
                ('maintenance/harness-reconciliation/staging.json', 'preserved source'),
            ):
                with self.subTest(path=name):
                    path = self.root / name; original = path.read_bytes()
                    try:
                        path.unlink(); self.rejected(diagnostic)
                    finally:
                        path.write_bytes(original)
            path = self.root / 'maintenance/harness-adoption/candidate-delta.json'; original = path.read_bytes()
            try:
                path.write_bytes(original + b' '); self.rejected('changed historical reconciliation source')
            finally:
                path.write_bytes(original)

    def test_revision_rejects_fourth_path_even_when_ignored(self):
        with self.revision():
            path = self.root / 'blog/public/assets/post_course_security-awareness_electricity-privacy/fourth.png'
            exclude = self.root / '.git/info/exclude'; original = exclude.read_bytes()
            try:
                path.write_bytes(b'not approved')
                self.rejected('fourth.png')
                exclude.write_bytes(original + b'\nblog/public/assets/post_course_security-awareness_electricity-privacy/fourth.png\n')
                self.rejected('fourth.png')
            finally:
                path.unlink(); exclude.write_bytes(original)

    def test_revision_rejects_nonancestor_pin(self):
        with self.revision():
            original = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root).decode().strip()
            try:
                subprocess.run(['git', 'update-ref', 'HEAD', '32cd6a9d4ead636ddc4e5020fceb35ad9645cc7f'], cwd=self.root, check=True)
                self.rejected('ancestor')
            finally:
                subprocess.run(['git', 'update-ref', 'HEAD', original], cwd=self.root, check=True)

    def test_revision_rejects_missing_predecessor_object(self):
        with self.revision(), tempfile.TemporaryDirectory() as temp:
            other = Path(temp) / 'old-history'; other.mkdir()
            subprocess.run(['git', 'init', str(other)], check=True, capture_output=True)
            subprocess.run(['git', 'fetch', '--no-tags', str(SOURCE), '32cd6a9d4ead636ddc4e5020fceb35ad9645cc7f'], cwd=other, check=True, capture_output=True)
            subprocess.run(['git', 'checkout', '--detach', 'FETCH_HEAD'], cwd=other, check=True, capture_output=True)
            original_git = Path(temp) / 'original-git'
            (self.root / '.git').rename(original_git)
            (other / '.git').rename(self.root / '.git')
            try:
                absent = subprocess.run(['git', 'cat-file', '-e', '69ff85f5fe1baddb54102070a436dff9ac1c5b73^{commit}'], cwd=self.root, capture_output=True)
                self.assertNotEqual(absent.returncode, 0, 'fixture unexpectedly contains revision predecessor')
                self.rejected('ancestor')
            finally:
                (self.root / '.git').rename(other / '.git')
                original_git.rename(self.root / '.git')

    def rejected(self, diagnostic):
        before = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root)
        result = self.cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(diagnostic, result.stdout + result.stderr)
        self.assertEqual(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root), before)

    def test_exact_reviewed_components_pass_full_cli(self):
        with self.overlay():
            result = self.cli()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_byte_drift_of_config_theme_summary_banner_is_rejected(self):
        with self.overlay():
            for name in ('blog/.vitepress/config.mts', 'blog/.vitepress/theme/index.ts', 'blog/.vitepress/theme/components/ArticleSummary.vue', 'blog/public/assets/post_course_security-awareness_electricity-privacy/article-banner.png'):
                with self.subTest(path=name):
                    path = self.root / name; original = path.read_bytes()
                    try:
                        path.write_bytes(original + b'\ntamper')
                        self.rejected(name)
                        self.assertEqual(path.read_bytes(), original + b'\ntamper')
                    finally:
                        path.write_bytes(original)

    def test_unknown_and_ignored_blog_markdown_are_rejected(self):
        path = self.root / 'blog/post/unknown-review.md'
        exclude = self.root / '.git/info/exclude'; original = exclude.read_bytes()
        try:
            path.write_text('# Not approved')
            self.rejected('blog/post/unknown-review.md')
            exclude.write_bytes(original + b'\nblog/post/unknown-review.md\n')
            self.rejected('blog/post/unknown-review.md')
        finally:
            path.unlink(missing_ok=True); exclude.write_bytes(original)

    def test_ignored_unapproved_test_source_is_rejected(self):
        path = self.root / 'tests/unknown_review.py'
        exclude = self.root / '.git/info/exclude'; original = exclude.read_bytes()
        try:
            path.write_text('# Unapproved executable test source')
            exclude.write_bytes(original + b'\ntests/unknown_review.py\n')
            self.rejected('tests/unknown_review.py')
        finally:
            path.unlink(missing_ok=True); exclude.write_bytes(original)

    def test_missing_linked_and_executable_drift_are_rejected(self):
        with self.overlay():
            name = 'blog/.vitepress/theme/components/ArticleSummary.vue'; path = self.root / name
            original = path.read_bytes(); mode = path.stat().st_mode
            try:
                path.unlink(); self.rejected(name)
                path.symlink_to(self.root / 'blog/.vitepress/config.mts'); self.rejected(name)
                path.unlink(); path.write_bytes(original); path.chmod(mode | 0o100); self.rejected(name)
            finally:
                if path.is_symlink(): path.unlink()
                path.write_bytes(original); path.chmod(mode)

    def test_pins_and_provenance_tampering_are_rejected(self):
        with self.overlay():
            for name in ('maintenance/harness-reconciliation/staging.json', 'maintenance/harness-reconciliation/components.json', 'maintenance/lint-cleanup/source-boundary.json', 'maintenance/harness-adoption/candidate-delta.json'):
                path = self.root / name; original = path.read_bytes()
                try:
                    path.write_bytes(original + b' '); self.rejected('provenance' if '/harness-reconciliation/' in name else name)
                finally: path.write_bytes(original)

    def test_nonancestor_or_missing_pin_history_is_rejected(self):
        original = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root).decode().strip()
        try:
            subprocess.run(['git', 'update-ref', 'HEAD', '8890d5250e22ec4ee0e0493c1e72bab89d16489b'], cwd=self.root, check=True)
            self.rejected('ancestor')
        finally:
            subprocess.run(['git', 'update-ref', 'HEAD', original], cwd=self.root, check=True)

    def test_manifest_absence_is_fail_closed_rollback(self):
        with self.overlay():
            component = self.root / 'maintenance/harness-reconciliation/components.json'
            original_component = component.read_bytes()
            try:
                component.unlink(); self.rejected('current reconciliation source')
            finally:
                component.write_bytes(original_component)
        path = self.root / 'maintenance/harness-reconciliation/staging.json'; original = path.read_bytes()
        try:
            path.unlink(); self.rejected('lint cleanup preserved source hash mismatch')
        finally: path.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
