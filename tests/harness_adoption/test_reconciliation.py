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
                shutil.copyfile(SOURCE / name, target)
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
