"""Publication must preserve the pinned baseline while accepting its descendants."""
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[2] / 'scripts/verify-harness-adoption.py'
spec = importlib.util.spec_from_file_location('publication_verifier', MODULE)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class PublicationAncestryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = dict(os.environ, GIT_AUTHOR_NAME='Graph fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid', GIT_COMMITTER_NAME='Graph fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        self.git('init', '-q')
        self.tree = self.git('mktree', input=b'').strip().decode()
        self.baseline = self.commit()
        self.git('update-ref', 'HEAD', self.baseline)

    def git(self, *args, input=None):
        return subprocess.check_output(['git', *args], cwd=self.root, env=self.env, input=input, stderr=subprocess.STDOUT)

    def commit(self, parent=None):
        # Plumbing creates synthetic graph objects; no user-facing git commit or hooks.
        args = ['commit-tree', self.tree]
        if parent: args += ['-p', parent]
        return self.git(*args, input=b'Graph fixture\n').strip().decode()

    def guard(self):
        fn = getattr(verifier, 'check_adoption_ancestry', None)
        self.assertTrue(callable(fn), 'published descendants need a real Git ancestry guard')
        return fn(self.root, self.baseline)

    def test_baseline_and_authorized_descendant_history_are_accepted(self):
        self.assertEqual(self.guard(), self.baseline)
        child = self.commit(self.baseline)
        grandchild = self.commit(child)
        self.git('update-ref', 'HEAD', grandchild)
        self.assertEqual(self.guard(), grandchild)

    def test_unrelated_history_is_rejected(self):
        unrelated_tree = self.git('mktree', input=b'').strip().decode()
        unrelated = self.git('commit-tree', unrelated_tree, input=b'Unrelated fixture\n').strip().decode()
        self.git('update-ref', 'HEAD', unrelated)
        with self.assertRaisesRegex(ValueError, 'baseline.*ancestor'):
            self.guard()

    def test_missing_baseline_object_is_rejected(self):
        fn = getattr(verifier, 'check_adoption_ancestry', None)
        self.assertTrue(callable(fn), 'published descendants need a real Git ancestry guard')
        with self.assertRaisesRegex(ValueError, 'baseline.*ancestor'):
            fn(self.root, 'f' * 40)


if __name__ == '__main__':
    unittest.main()
