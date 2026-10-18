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


    def test_changed_pr32_contracts_are_rejected_before_any_test_import(self):
        """K1: frozen selection never hides changed/missing/linked current test bytes."""
        names=('test_closed_baseline.py','test_closeout_successor.py',
               'test_landed_closeout.py','test_remote_validation.py')
        for changed in names:
            for mutation in ('bytes','missing','symlink'):
                with self.subTest(module=changed,mutation=mutation),tempfile.TemporaryDirectory(prefix='runner-pr32-contract-') as tmp:
                    root=Path(tmp)/'tests';folder=root/'article_publication';folder.mkdir(parents=True)
                    (folder/'__init__.py').write_bytes(b'')
                    for name in ('test_current_baseline.py',)+names:
                        (folder/name).write_bytes((SOURCE/'tests/article_publication'/name).read_bytes())
                    target=folder/changed
                    if mutation=='bytes':target.write_bytes(target.read_bytes()+b'\n# changed contract\n')
                    elif mutation=='missing':target.unlink()
                    else:
                        target.unlink();target.symlink_to(SOURCE/'tests/article_publication'/changed)
                    sentinel=Path(tmp)/'import-executed'
                    harness=root/'harness_adoption';harness.mkdir()
                    (harness/'__init__.py').write_text(
                        'import os\nfrom pathlib import Path\nPath('+repr(str(sentinel))+').touch()\nos._exit(77)\n')
                    result=subprocess.run([sys.executable,str(SOURCE/'scripts/run-current-python-tests.py'),
                                           '--tests-root',str(root)],capture_output=True,text=True)
                    self.assertNotEqual(result.returncode,0)
                    self.assertIn('changed PR32 frozen test contract',result.stderr)
                    self.assertFalse(sentinel.exists(),'test discovery preceded contract verification')
                    self.assertNotIn('frozen fixture: commit=',result.stdout)


if __name__ == '__main__':
    unittest.main()
