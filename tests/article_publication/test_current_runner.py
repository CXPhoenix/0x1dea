"""The explicit historical runner must not hide changes to its live historical test file."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]


class CurrentRunnerTests(unittest.TestCase):
    def test_changed_historical_fixture_file_is_rejected_before_loading_tests(self):
        with tempfile.TemporaryDirectory(prefix='runner-contract-') as tmp:
            root = Path(tmp) / 'tests'
            folder = root / 'article_publication'
            folder.mkdir(parents=True)
            (folder / '__init__.py').write_bytes(b'')
            historical = 'test_current_baseline.py'
            (folder / historical).write_bytes((SOURCE/'tests/article_publication'/historical).read_bytes() + b'\n# unreviewed assertion contract change\n')
            result = subprocess.run([sys.executable, str(SOURCE/'scripts/run-current-python-tests.py'),
                                     '--tests-root', str(root)], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('changed historical T13 test contract', result.stderr)
            self.assertNotIn('T13 #22 frozen fixture: commit=', result.stdout)


if __name__ == '__main__':
    unittest.main()
