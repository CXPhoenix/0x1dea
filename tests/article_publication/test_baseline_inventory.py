"""Public, read-only Git inventory seam for the proposed M0 boundary."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

CLI = Path(__file__).resolve().parents[2] / 'scripts/publication-baseline.py'


class BaselineInventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Fixture')
        self.git('remote', 'add', 'origin', 'https://example.invalid/site.git')
        (self.root / 'published.md').write_text('published\n')
        self.commit()
        self.main = self.git('rev-parse', 'HEAD').strip()
        (self.root / 'published.md').write_text('unapproved revision\n')
        (self.root / 'A.md').write_text('candidate A\n')
        (self.root / 'engine.py').write_text('print("engineering")\n')
        self.commit()
        self.stage = self.git('rev-parse', 'HEAD').strip()
        self.plan = {
            'schema_version': 1, 'main': self.main, 'staging': self.stage,
            'classifications': {
                'published.md': {'category': 'candidate', 'owner': 'revision'},
                'A.md': {'category': 'candidate', 'owner': 'A'},
                'engine.py': {'category': 'engineering', 'owner': 'common'},
            },
            'candidates': [
                {'id': 'A', 'paths': ['A.md'], 'provenance': 'legacy-requires-migration'},
                {'id': 'revision', 'paths': ['published.md'], 'provenance': 'legacy-requires-migration'},
            ],
            'prerequisites': [],
        }

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True)

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')

    def invoke(self):
        policy = self.root.parent / (self.root.name + '-classification.json')
        policy.write_text(json.dumps(self.plan))
        self.addCleanup(policy.unlink, missing_ok=True)
        return subprocess.run(
            ['python3', str(CLI), 'inventory', '--repo', str(self.root),
             '--classification', str(policy)], text=True, capture_output=True,
        )

    def test_complete_proposal_preserves_revision_and_records_both_trees(self):
        before = self.git('status', '--porcelain=v1', '--untracked-files=all')
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['status'], 'proposal-only')
        self.assertFalse(report['trusted_policy'])
        self.assertEqual(len(report['trees']['main']), 1)
        self.assertEqual(len(report['trees']['staging']), 3)
        revision = next(r for r in report['delta'] if r['path'] == 'published.md')
        self.assertEqual(revision['category'], 'candidate')
        self.assertEqual(revision['main']['blob'], self.git('rev-parse', self.main + ':published.md').strip())
        self.assertEqual(revision['staging']['blob'], self.git('rev-parse', self.stage + ':published.md').strip())
        self.assertEqual(revision['main']['mode'], '100644')
        self.assertEqual(revision['main_action'], 'retain-published')
        self.assertEqual(revision['staging_action'], 'preserve-exact')
        self.assertEqual(before, self.git('status', '--porcelain=v1', '--untracked-files=all'))

    def test_unknown_delta_or_stale_classification_blocks_without_partial_output(self):
        original = json.loads(json.dumps(self.plan))
        for mutation in ('unknown', 'stale'):
            with self.subTest(mutation=mutation):
                self.plan = json.loads(json.dumps(original))
                if mutation == 'unknown':
                    (self.root / 'unknown.txt').write_text('unclassified\n')
                    self.commit()
                    self.plan['staging'] = self.git('rev-parse', 'HEAD').strip()
                else:
                    self.plan['classifications']['absent.md'] = {'category': 'engineering', 'owner': 'common'}
                result = self.invoke()
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, '')
                self.assertIn('classification', result.stderr.lower())
                self.plan = original

    def test_overlapping_or_incomplete_candidate_ownership_blocks(self):
        original = json.loads(json.dumps(self.plan))
        for mutation in ('overlap', 'missing', 'masquerade'):
            with self.subTest(mutation=mutation):
                self.plan = json.loads(json.dumps(original))
                if mutation == 'overlap':
                    self.plan['candidates'][1]['paths'].append('A.md')
                elif mutation == 'missing':
                    self.plan['candidates'][0]['paths'] = []
                else:
                    self.plan['classifications']['A.md'] = {'category': 'engineering', 'owner': 'common'}
                result = self.invoke()
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, '')
                self.assertIn('ownership', result.stderr.lower())

    def test_open_pr_is_not_landed_and_shared_patch_is_exact(self):
        self.plan['classifications']['engine.py']['shared'] = True
        self.plan['prerequisites'] = [
            {'pr': 20, 'state': 'OPEN', 'target': 'main', 'merge_commit': None,
             'head': self.stage},
            {'pr': 21, 'state': 'MERGED', 'target': 'staging', 'merge_commit': self.stage,
             'head': self.stage},
        ]
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual([p['landed_by_observation_and_ancestry'] for p in report['prerequisites']], [False, True])
        engine = next(r for r in report['delta'] if r['path'] == 'engine.py')
        self.assertIn('+print("engineering")', engine['patch'])
        self.assertIn('new file mode 100644', engine['patch'])

    def test_unpinned_or_self_asserted_trust_input_is_rejected(self):
        original = json.loads(json.dumps(self.plan))
        for mutation in ('short-pin', 'branch-pin', 'trusted', 'role', 'category', 'duplicate-json'):
            with self.subTest(mutation=mutation):
                self.plan = json.loads(json.dumps(original))
                if mutation == 'short-pin':
                    self.plan['main'] = self.main[:8]
                elif mutation == 'branch-pin':
                    self.plan['main'] = 'HEAD'
                elif mutation == 'trusted':
                    self.plan['trusted_policy'] = True
                elif mutation == 'role':
                    self.plan['target_role'] = 'permissive'
                elif mutation == 'category':
                    self.plan['classifications']['engine.py']['category'] = 'anything'
                else:
                    policy = self.root.parent / (self.root.name + '-duplicate.json')
                    self.addCleanup(policy.unlink, missing_ok=True)
                    policy.write_text(json.dumps(self.plan)[:-1] + ', "main": "HEAD"}')
                    result = subprocess.run(['python3', str(CLI), 'inventory', '--repo', str(self.root),
                                             '--classification', str(policy)], text=True, capture_output=True)
                if mutation != 'duplicate-json':
                    result = self.invoke()
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, '')

    def test_history_overlays_and_incomplete_history_are_rejected(self):
        self.git('replace', self.main, self.stage)
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.git('replace', '-d', self.main)
        (self.root / '.git/info/grafts').write_text(self.stage + '\n')
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        (self.root / '.git/info/grafts').unlink()
        (self.root / '.git/shallow').write_text(self.stage + '\n')
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')

    def test_candidate_deletion_retains_published_main_and_records_absence(self):
        (self.root / 'published.md').unlink()
        self.commit()
        self.plan['staging'] = self.git('rev-parse', 'HEAD').strip()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        revision = next(r for r in json.loads(result.stdout)['delta'] if r['path'] == 'published.md')
        self.assertIsNone(revision['staging'])
        self.assertEqual(revision['main_action'], 'retain-published')
        self.assertEqual(revision['main']['blob'], self.git('rev-parse', self.main + ':published.md').strip())

    def test_shared_patch_treats_git_metacharacters_as_literal_paths(self):
        for path, content in [('engine*.py', 'literal-only'), ('engineZ.py', 'other-path')]:
            (self.root / path).write_text(content + '\n')
            self.plan['classifications'][path] = {'category': 'engineering', 'owner': 'common', 'shared': True}
        self.commit()
        self.plan['staging'] = self.git('rev-parse', 'HEAD').strip()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        patch = next(r['patch'] for r in json.loads(result.stdout)['delta'] if r['path'] == 'engine*.py')
        self.assertIn('+literal-only', patch)
        self.assertNotIn('+other-path', patch)


if __name__ == '__main__':
    unittest.main()
