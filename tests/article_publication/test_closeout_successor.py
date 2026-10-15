"""T-0012 C2: finite closeout identities at the existing native CLI seam."""
from pathlib import Path
import json
import hashlib
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
MAIN = '87740186f2a1b57f8c1df89f36647cbe3663f428'
STAGING = '035783590895a426ee395045829ebc9d50e2b9cf'


class CloseoutSuccessorTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='closeout-successor-')
        self.addCleanup(temp.cleanup)
        self.output = Path(temp.name)/'projection'
        result = subprocess.run([sys.executable, str(SOURCE/'scripts/publication-baseline.py'),
                                 'prepare', '--output', str(self.output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for role in ('main', 'staging'):
            controller = self.output/role
            for name, pin in (('main', '5e6c889c808e7ef4cb83493bf06f8a70dd055b41'), ('staging', '612924848ca13663bb2af64e32638fbabedb1685')):
                subprocess.run(['git', '-C', str(controller), 'update-ref', 'refs/heads/'+name, pin], check=True)
            subprocess.run(['git', '-C', str(controller), 'update-ref', 'HEAD', MAIN if role == 'main' else STAGING], check=True)

    def verify(self, controller):
        return subprocess.run([sys.executable, str(controller/'scripts/verify-harness-adoption.py')], capture_output=True, text=True)

    def repin(self, controller, name):
        path = controller/'maintenance/publication-workflow/engineering-v1.json'
        policy = json.loads(path.read_bytes())
        policy['common'][name]['sha256'] = hashlib.sha256((controller/name).read_bytes()).hexdigest()
        path.write_text(json.dumps(policy))

    def test_exact_closeout_is_accepted_on_both_target_projections(self):
        for role in ('main', 'staging'):
            result = self.verify(self.output/role)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            for ticket in ('T-0001', 'T-0002', 'T-0010', 'T-0011', 'T-0013'):
                self.assertEqual(report['tracker']['tickets'][ticket]['status'], 'done')
            self.assertEqual(report['target_role'], role)
            self.assertFalse(report['publishable'])

    def test_repinning_arbitrary_ticket_text_does_not_authorize_a_successor(self):
        controller = self.output/'main'
        name = '.proj.tickets/0001-harness-adoption/T-0001-harness-adoption.md'
        path = controller/name
        original = path.read_bytes()
        for raw in (original+b'\nUnapproved prose.\n', original.replace(b'status: done', b'status: review'),
                    original.replace(b'landing.json', b'other.json')):
            with self.subTest(raw=raw[-60:]):
                path.write_bytes(raw)
                self.repin(controller, name)
                result = self.verify(controller)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('unapproved exact closeout identity', result.stderr)
                self.assertEqual(result.stdout, '')

    def test_closeout_requires_regular_exact_mode_and_path(self):
        controller = self.output/'main'
        name = '.proj.tickets/0010-main-verification-repair/T-0010-main-verification-repair.md'
        path = controller/name
        original = path.read_bytes()
        for mutation in ('executable', 'symlink', 'missing'):
            with self.subTest(mutation=mutation):
                path.write_bytes(original)
                path.chmod(0o644)
                if mutation == 'executable':
                    path.chmod(0o755)
                else:
                    path.unlink()
                    if mutation == 'symlink':
                        path.symlink_to('T-0012-ticket-evidence-closeout.md')
                result = self.verify(controller)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, '')
                if path.is_symlink():
                    path.unlink()
        path.write_bytes(original)
        policy_path = controller/'maintenance/publication-workflow/engineering-v1.json'
        policy = json.loads(policy_path.read_bytes())
        del policy['common'][name]
        policy_path.write_text(json.dumps(policy))
        result = self.verify(controller)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unapproved exact closeout identity', result.stderr)

    def test_receipt_mutation_cannot_be_authorized_by_repinning_the_map(self):
        controller = self.output/'main'
        name = '.proj.specs/0001-harness-adoption/landing.json'
        path = controller/name
        original = json.loads(path.read_bytes())
        mutations = [('ticket', 'T-0010'), ('authorized', False), ('landed', False),
                     ('target', 'main'), ('commit', MAIN),
                     ('commit', '0'*40), ('approval_receipt', '.proj.specs/0010-main-verification-repair/landing-approval.md')]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                receipt = dict(original)
                receipt[key] = value
                path.write_text(json.dumps(receipt))
                self.repin(controller, name)
                result = self.verify(controller)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('unapproved exact closeout identity', result.stderr)
                self.assertEqual(result.stdout, '')

    def test_existing_unrelated_approval_is_not_the_pinned_closeout_authority(self):
        controller = self.output/'main'
        name = '.proj.specs/0010-main-verification-repair/landing-approval.md'
        (controller/name).write_bytes((controller/'.proj.specs/0011-main-to-staging-sync/landing-approval.md').read_bytes())
        self.repin(controller, name)
        result = self.verify(controller)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unapproved exact closeout identity', result.stderr)


if __name__ == '__main__':
    unittest.main()
