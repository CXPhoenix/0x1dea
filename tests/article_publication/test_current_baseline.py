"""Approved P02/P03/P23 tests at the real Git/native CLI boundary."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
CLI = SOURCE / 'scripts/publication-baseline.py'
MAIN = 'eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a'
STAGING = 'c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7'
ARTICLE = 'blog/post/course/security-awareness/electricity-privacy.md'


class CurrentBaselineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='current-baseline-')
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / 'projection'

    def run_cli(self, *args):
        return subprocess.run(['python3', str(CLI), *args], capture_output=True, text=True)

    def prepare(self):
        result = self.run_cli('prepare', '--output', str(self.out))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_engineering_projection_preserves_published_main_and_all_staging_candidates(self):
        result = self.prepare()
        self.assertFalse(result['publishable'])
        self.assertEqual((self.out / 'main' / ARTICLE).read_bytes(), subprocess.check_output(['git', 'show', MAIN + ':' + ARTICLE], cwd=SOURCE))
        inventory = json.loads((SOURCE / '.proj.specs/0012-publication-workflow/implementation/T-0013/M0-inventory.proposed.json').read_text())
        for candidate in inventory['candidates']:
            for name in candidate['paths']:
                self.assertEqual((self.out / 'staging' / name).read_bytes(), subprocess.check_output(['git', 'show', STAGING + ':' + name], cwd=SOURCE), name)
        self.assertFalse((self.out / 'main/blog/post/local-preview').exists())
        self.assertEqual((self.out / 'main/scripts/publication_current.py').read_bytes(), (self.out / 'staging/scripts/publication_current.py').read_bytes())
        self.assertEqual(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.out / 'main').decode().strip(), MAIN)
        self.assertEqual(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.out / 'staging').decode().strip(), STAGING)

    def test_same_engine_validates_both_trusted_targets_and_refuses_cross_role_candidates(self):
        self.prepare()
        for role in ('main', 'staging'):
            controller = self.out / role
            result = subprocess.run(['python3', str(controller / 'scripts/publication-baseline.py'),
                                     'verify', '--repo', str(controller)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report['target_role'], role)
            self.assertFalse(report['publishable'])
        result = subprocess.run(['python3', str(self.out / 'main/scripts/publication-baseline.py'), 'verify', '--repo', str(self.out / 'staging')], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        result = self.run_cli('verify', '--repo', str(self.out / 'main'), '--role', 'staging')
        self.assertNotEqual(result.returncode, 0)

    def test_native_adoption_command_uses_exact_current_successor_on_both_projections(self):
        self.prepare()
        for role in ('main', 'staging'):
            controller = self.out / role
            result = subprocess.run(['python3', str(controller / 'scripts/verify-harness-adoption.py')], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)['target_role'], role)

    def test_candidate_policy_management_and_protected_bytes_cannot_weaken_target_checks(self):
        self.prepare()
        controller = self.out / 'main'
        root = self.out / 'candidate'
        shutil.copytree(controller, root, symlinks=True)
        mutations = [
            ('maintenance/publication-workflow/engineering-v1.json', b'{}'),
            ('blog/post/course/security-awareness/electricity-privacy.md', b'candidate revision'),
            ('maintenance/harness-adoption/baseline-files.json', b'{}'),
            ('.proj.specs/unreviewed/waiver.json', b'{"allow_management":true}'),
        ]
        for name, raw in mutations:
            with self.subTest(path=name):
                path = root / name
                original = path.read_bytes() if path.exists() else None
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                result = subprocess.run(['python3', str(controller / 'scripts/publication-baseline.py'), 'verify', '--repo', str(root)], text=True, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, '')
                if original is None:
                    path.unlink()
                else:
                    path.write_bytes(original)

    def test_exact_tracker_update_cannot_close_t13_without_actual_authorized_landing(self):
        self.prepare()
        controller = self.out / 'main'
        ticket = '.proj.tickets/0012-publication-workflow/T-0013-common-engineering-baseline.md'
        path = controller / ticket
        path.write_text(path.read_text().replace('status: processing', 'status: done', 1).replace('status: review', 'status: done', 1))
        import hashlib
        policy_path = controller / 'maintenance/publication-workflow/engineering-v1.json'
        record = json.loads(policy_path.read_text())
        record['common'][ticket]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        policy_path.write_text(json.dumps(record, indent=2) + '\n')
        result = subprocess.run(['python3', str(controller / 'scripts/publication-baseline.py'),
                                 'verify', '--repo', str(controller)], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn('landing', result.stderr)

    def test_m0_ancestor_with_generic_receipt_is_not_t13_implementation_landing(self):
        self.prepare()
        controller = self.out / 'main'
        ticket = '.proj.tickets/0012-publication-workflow/T-0013-common-engineering-baseline.md'
        receipt = '.proj.specs/0012-publication-workflow/fake-landing.json'
        path = controller / ticket
        path.write_text(path.read_text().replace('status: processing', 'status: done', 1).replace('status: review', 'status: done', 1).replace('status: done', 'status: done\nlanding_evidence: ' + receipt, 1))
        (controller / receipt).write_text(json.dumps({'ticket': 'T-0013', 'authorized': True,
                         'landed': True, 'commit': MAIN, 'main_commit': MAIN, 'target': 'staging',
                         'approval_receipt': 'maintenance/publication-workflow/M0-approval.json'}))
        subprocess.run(['git', 'update-ref', 'refs/heads/staging', STAGING], cwd=controller, check=True)
        import hashlib
        policy_path = controller / 'maintenance/publication-workflow/engineering-v1.json'
        record = json.loads(policy_path.read_text())
        for name in (ticket, receipt):
            record['common'][name] = {'mode': '100644', 'sha256': hashlib.sha256((controller / name).read_bytes()).hexdigest()}
        policy_path.write_text(json.dumps(record, indent=2) + '\n')
        result = subprocess.run(['python3', str(controller / 'scripts/publication-baseline.py'),
                                 'verify', '--repo', str(controller)], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn('T-0013', result.stderr)

    def test_reviewed_main_based_control_topic_keeps_main_role_after_commit(self):
        self.prepare()
        controller = self.out / 'main'
        tree = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], cwd=controller).decode().strip()
        commit = subprocess.check_output(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                                          'commit-tree', tree, '-p', MAIN, '-m', 'fixture control commit'], cwd=controller).decode().strip()
        subprocess.run(['git', 'update-ref', 'HEAD', commit], cwd=controller, check=True)
        result = subprocess.run(['python3', str(controller / 'scripts/publication-baseline.py'),
                                 'verify', '--repo', str(controller)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['target_role'], 'main')

    def test_common_record_cannot_waive_candidate_or_historical_ownership(self):
        self.prepare()
        controller = self.out / 'main'
        policy_path = controller / 'maintenance/publication-workflow/engineering-v1.json'
        original = policy_path.read_bytes()
        import hashlib
        for mutation in ('candidate-overlay', 'historical-overlay', 'broad-waiver'):
            with self.subTest(mutation=mutation):
                record = json.loads(original)
                if mutation == 'broad-waiver':
                    record['allow_management_prefixes'] = ['.proj.specs/']
                else:
                    name = ARTICLE if mutation == 'candidate-overlay' else 'maintenance/harness-adoption/baseline-files.json'
                    record['common'][name] = {'mode': '100644', 'sha256': hashlib.sha256((controller / name).read_bytes()).hexdigest()}
                policy_path.write_text(json.dumps(record, indent=2) + '\n')
                result = subprocess.run(['python3', str(controller / 'scripts/publication-baseline.py'),
                                         'verify', '--repo', str(controller)], text=True, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, '')
        policy_path.write_bytes(original)

    def test_literal_alias_bytes_are_protected_even_when_target_is_equivalent(self):
        self.prepare()
        controller = self.out / 'main'
        root = self.out / 'candidate'
        shutil.copytree(controller, root, symlinks=True)
        inventory = json.loads((SOURCE / '.proj.specs/0012-publication-workflow/implementation/T-0013/M0-inventory.proposed.json').read_text())
        name = next(p for p, entry in inventory['trees']['main'].items() if entry['mode'] == '120000')
        import os
        path = root / name
        target = os.readlink(path)
        path.unlink()
        path.symlink_to('./' + target)
        result = subprocess.run(['python3', str(controller / 'scripts/publication-baseline.py'),
                                 'verify', '--repo', str(root)], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertIn(name, result.stderr)

    def test_projection_preserves_target_refs_needed_by_unchanged_landing_fixtures(self):
        self.prepare()
        for role in ('main', 'staging'):
            for ref, expected in [('main', MAIN), ('staging', STAGING)]:
                result = subprocess.run(['git', 'rev-parse', '--verify', 'refs/heads/' + ref],
                                         cwd=self.out / role, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), expected)


if __name__ == '__main__':
    unittest.main()
