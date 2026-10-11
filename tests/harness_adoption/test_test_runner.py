"""Exercise the complete Python entrypoint through disposable test packages."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNNER = Path(__file__).resolve().parents[2] / 'scripts/run-python-tests.py'


class TestRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for suite in ('harness_adoption', 'article_publication'):
            package = self.root / suite
            package.mkdir()
            (package / '__init__.py').write_text('')
            (package / 'test_sample.py').write_text(
                'import unittest\nclass Sample(unittest.TestCase):\n'
                '    def test_sample(self): self.assertTrue(True)\n')

    def run_cli(self):
        return subprocess.run([sys.executable, '-B', str(RUNNER), '--tests-root', str(self.root)],
                              capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))

    def test_both_named_suites_run_with_positive_counts(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('harness_adoption: testsRun=1 failures=0 errors=0', result.stdout)
        self.assertIn('article_publication: testsRun=1 failures=0 errors=0', result.stdout)
        self.assertFalse(list(self.root.rglob('__pycache__')))

    def test_zero_tests_in_either_suite_is_failure_but_other_suite_runs(self):
        for name, other in (('harness_adoption', 'article_publication'), ('article_publication', 'harness_adoption')):
            path = self.root / name / 'test_sample.py'
            original = path.read_bytes()
            try:
                path.write_text('')
                result = self.run_cli()
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(f'{name}: testsRun=0', result.stdout)
                self.assertIn(f'{other}: testsRun=1', result.stdout)
            finally:
                path.write_bytes(original)

    def test_failure_and_import_error_in_either_suite_propagate(self):
        for name, other in (('harness_adoption', 'article_publication'), ('article_publication', 'harness_adoption')):
            path = self.root / name / 'test_sample.py'
            original = path.read_bytes()
            for content, diagnostic in ((original.replace(b'assertTrue(True)', b'assertTrue(False)'), 'failures=1'),
                                        (b'raise ImportError("broken suite")\n', 'errors=1')):
                with self.subTest(suite=name, diagnostic=diagnostic):
                    try:
                        path.write_bytes(content)
                        result = self.run_cli()
                        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                        self.assertIn(diagnostic, result.stdout)
                        self.assertIn(f'{other}: testsRun=1 failures=0 errors=0', result.stdout)
                    finally:
                        path.write_bytes(original)

    def test_unimportable_suite_does_not_prevent_other_suite_running(self):
        (self.root / 'harness_adoption/__init__.py').unlink()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('article_publication: testsRun=1 failures=0 errors=0', result.stdout)
