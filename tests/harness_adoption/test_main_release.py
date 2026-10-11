"""Public CLI regressions for the owner-merged, selected article release."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
MERGE = '88b9c53852f527ee636bcc4b4ca5e166f6ec10fd'
LISTING_INDEX = 'blog/post/course/security-awareness/index.md'
REPAIR = ('scripts/verify-harness-adoption.py', 'scripts/main_publication_verification.py',
          'tests/harness_adoption/test_tracker.py', 'tests/harness_adoption/test_main_release.py')


class MainReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='main-release-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'candidate'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', str(SOURCE), str(self.root)],
                       check=True, capture_output=True)
        self.git('checkout', '--detach', MERGE)
        for name in (*REPAIR, LISTING_INDEX):
            shutil.copyfile(SOURCE / name, self.root / name)

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, stderr=subprocess.STDOUT)

    def cli(self):
        return subprocess.run(['python3', str(SOURCE / 'scripts/verify-harness-adoption.py'),
                               '--root', str(self.root)], cwd=self.root,
                              capture_output=True, text=True)

    def accepted(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'pass')

    def rejected(self, fragment):
        result = self.cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(fragment, result.stdout + result.stderr)

    def adoption_closeout(self):
        name = '.proj.tickets/0001-harness-adoption/T-0001-harness-adoption.md'
        original = self.git('show', MERGE + ':' + name)
        done = original.replace(b'status: review\n', b'status: done\n'
                                b'landing_evidence: .proj.specs/0001-harness-adoption/landing.json\n', 1)
        (self.root / name).write_bytes(done)
        for evidence in ('.proj.specs/0001-harness-adoption/landing.json',
                         '.proj.specs/0001-harness-adoption/landing-approval.md'):
            target = self.root / evidence; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / evidence, target)
        self.git('branch', '-f', 'staging', 'c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7')
        return name

    def test_exact_adoption_closeout_with_real_landing_is_accepted(self):
        self.accepted()
        self.adoption_closeout()
        self.accepted()

    def test_adoption_receipt_cannot_use_another_valid_ancestor(self):
        self.adoption_closeout()
        self.accepted()
        path = self.root / '.proj.specs/0001-harness-adoption/landing.json'
        receipt = json.loads(path.read_text())
        receipt['commit'] = 'e457143e8be2f7d54f69bc3e9b80230375be49de'
        path.write_text(json.dumps(receipt))
        self.rejected('changed adoption landing evidence: ')

    def test_adoption_done_identity_remains_exact(self):
        name = self.adoption_closeout()
        path = self.root / name; original = path.read_bytes(); mode = path.stat().st_mode
        for mutation in ('prose', 'status', 'receipt-path', 'mode', 'missing', 'link'):
            with self.subTest(mutation=mutation):
                try:
                    if mutation == 'prose':
                        path.write_bytes(original + b'\nUNAPPROVED')
                    elif mutation == 'status':
                        path.write_bytes(original.replace(b'status: done', b'status: review'))
                    elif mutation == 'receipt-path':
                        alternate = self.root / '.proj.specs/0001-harness-adoption/alternate.json'
                        shutil.copyfile(self.root / '.proj.specs/0001-harness-adoption/landing.json', alternate)
                        path.write_bytes(original.replace(b'adoption/landing.json', b'adoption/alternate.json'))
                    elif mutation == 'mode':
                        path.chmod(mode | 0o100)
                    elif mutation == 'missing':
                        path.unlink()
                    else:
                        foreign = Path(self.temp.name) / 'same-ticket.md'; foreign.write_bytes(original)
                        path.unlink(); path.symlink_to(foreign)
                    prefix = {'missing': 'missing evidence/source path: ',
                              'link': 'linked evidence/source path: '}.get(
                                  mutation, 'changed publication source: ')
                    self.rejected(prefix + name)
                finally:
                    if path.is_symlink(): path.unlink()
                    path.write_bytes(original); path.chmod(mode)
        # A T1 exception never permits a different existing ticket to change.
        other = '.proj.tickets/0002-article-publication/T-0002-article-publication-preparation.md'
        other_path = self.root / other
        other_path.write_bytes(other_path.read_bytes() + b'\nUNAPPROVED')
        self.rejected('changed publication source: ' + other)

    def test_adoption_receipt_and_approval_remain_exact_regular_files(self):
        self.adoption_closeout()
        receipt_name = '.proj.specs/0001-harness-adoption/landing.json'
        receipt = self.root / receipt_name; original = receipt.read_bytes()
        self.git('config', 'user.name', 'Disposable fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        unrelated = self.git('commit-tree', MERGE + '^{tree}').decode().strip()
        for field, value in (('authorized', False), ('landed', False), ('ticket', 'T-0002'),
                             ('target', 'main'), ('commit', '0' * 40), ('commit', unrelated),
                             ('approval_receipt', '.proj.specs/0001-harness-adoption/spec.en.md')):
            with self.subTest(field=field, value=value):
                data = json.loads(original); data[field] = value
                receipt.write_text(json.dumps(data))
                self.rejected('changed adoption landing evidence: ' + receipt_name)
                receipt.write_bytes(original)
        for name in (receipt_name, '.proj.specs/0001-harness-adoption/landing-approval.md'):
            path = self.root / name; saved = path.read_bytes(); mode = path.stat().st_mode
            for mutation in ('bytes', 'mode', 'missing', 'link'):
                with self.subTest(path=name, mutation=mutation):
                    try:
                        if mutation == 'bytes': path.write_bytes(saved + b'\nUNAPPROVED')
                        elif mutation == 'mode': path.chmod(mode | 0o100)
                        elif mutation == 'missing': path.unlink()
                        else:
                            foreign = Path(self.temp.name) / 'same-evidence'; foreign.write_bytes(saved)
                            path.unlink(); path.symlink_to(foreign)
                        prefix = {'missing': 'missing evidence/source path: ',
                                  'link': 'linked evidence/source path: '}.get(
                                      mutation, 'changed adoption landing evidence: ')
                        self.rejected(prefix + name)
                    finally:
                        if path.is_symlink(): path.unlink()
                        path.write_bytes(saved); path.chmod(mode)

    def test_reviewed_main_with_listing_repair_is_accepted(self):
        self.accepted()

    def test_listing_successor_is_exact_and_required(self):
        path = self.root / LISTING_INDEX
        original = path.read_bytes(); mode = path.stat().st_mode
        for mutation in ('stale', 'bytes', 'mode', 'missing', 'symlink'):
            with self.subTest(mutation=mutation):
                self.accepted()
                try:
                    if mutation == 'stale':
                        path.write_bytes(self.git('show', MERGE + ':' + LISTING_INDEX))
                    elif mutation == 'bytes':
                        path.write_bytes(original + b'\nUNAPPROVED')
                    elif mutation == 'mode':
                        path.chmod(mode | 0o100)
                    elif mutation == 'missing':
                        path.unlink()
                    else:
                        path.unlink()
                        foreign = Path(self.temp.name) / 'same-index.md'
                        foreign.write_bytes(original); path.symlink_to(foreign)
                    prefix = {'missing': 'missing evidence/source path: ',
                              'symlink': 'linked evidence/source path: '}.get(
                                  mutation, 'changed publication source: ')
                    self.rejected(prefix + LISTING_INDEX)
                finally:
                    if path.is_symlink():
                        path.unlink()
                    path.write_bytes(original); path.chmod(mode)

    def test_ignored_compilable_source_is_rejected(self):
        self.accepted()
        name = 'blog/post/hidden-main.md'
        exclude = Path(self.git('rev-parse', '--git-path', 'info/exclude').decode().strip())
        if not exclude.is_absolute():
            exclude = self.root / exclude
        with exclude.open('a') as stream:
            stream.write('/' + name + '\n')
        (self.root / name).write_text('# Unapproved ignored article\n')
        self.rejected('unknown publication source: ' + name)

    def test_git_history_overlays_are_rejected(self):
        self.accepted()
        release = '604f8733ca47d67fc277ec127a9da743cefbc22e'
        base = 'e457143e8be2f7d54f69bc3e9b80230375be49de'
        ref = 'refs/replace/' + release
        self.git('update-ref', ref, base)
        with self.subTest(overlay='replace'):
            self.rejected('publication history overlays are not allowed')
        self.git('update-ref', '-d', ref)
        graft = Path(self.git('rev-parse', '--git-path', 'info/grafts').decode().strip())
        if not graft.is_absolute():
            graft = self.root / graft
        graft.write_text(MERGE + ' ' + base + '\n')
        with self.subTest(overlay='graft'):
            self.rejected('publication history overlays are not allowed')

    def test_product_and_historical_bytes_cannot_drift(self):
        self.accepted()
        names = ('blog/post/course/security-awareness/electricity-privacy.md',
                 'blog/.vitepress/config.mts', 'package.json', 'pnpm-lock.yaml',
                 'blog/public/assets/post_course_security-awareness_electricity-privacy/p-cat-event.png',
                 'tests/fixtures/article-caption-entry.md',
                 'maintenance/lint-cleanup/source-boundary.json',
                 'maintenance/harness-adoption/candidate-delta.json',
                 '.proj.specs/0002-article-publication/electricity-release/validation.md')
        for name in names:
            with self.subTest(path=name):
                path = self.root / name; original = path.read_bytes()
                try:
                    path.write_bytes(original + b'\nUNAPPROVED')
                    self.rejected('changed publication source: ' + name)
                finally:
                    path.write_bytes(original)

    def test_release_scope_cannot_be_refreshed_or_deleted(self):
        self.accepted()
        name = '.proj.specs/0002-article-publication/electricity-release/scope.json'
        path = self.root / name; original = path.read_bytes()
        scope = json.loads(original); scope['base'] = '0' * 40
        path.write_text(json.dumps(scope))
        self.rejected('changed publication scope: ' + name)
        path.unlink()
        self.rejected('missing evidence/source path: ' + name)

    def test_source_existence_type_mode_and_parent_are_enforced(self):
        self.accepted()
        name = 'blog/post/course/security-awareness/electricity-privacy.md'
        path = self.root / name; original = path.read_bytes(); mode = path.stat().st_mode
        path.unlink()
        self.rejected('missing evidence/source path: ' + name)
        foreign = Path(self.temp.name) / 'same-bytes.md'; foreign.write_bytes(original)
        path.symlink_to(foreign)
        self.rejected('linked evidence/source path: ' + name)
        path.unlink(); path.write_bytes(original); path.chmod(mode | 0o100)
        self.rejected('changed publication source: ' + name)
        path.chmod(mode)
        parent = path.parent; saved = parent.with_name('saved-category'); parent.rename(saved)
        parent.symlink_to(saved, target_is_directory=True)
        self.rejected('linked evidence/source path: ' + name)

    def test_required_repair_sources_cannot_be_removed_or_linked(self):
        self.accepted()
        for name in REPAIR:
            with self.subTest(path=name):
                path = self.root / name; original = path.read_bytes()
                path.unlink()
                self.rejected('missing evidence/source path: ' + name)
                path.write_bytes(original)
        name = 'tests/harness_adoption/test_main_release.py'
        path = self.root / name; original = path.read_bytes(); path.unlink()
        foreign = Path(self.temp.name) / 'same-test.py'; foreign.write_bytes(original)
        path.symlink_to(foreign)
        self.rejected('linked evidence/source path: ' + name)

    def test_unknown_tracked_and_untracked_product_is_rejected(self):
        self.accepted()
        name = 'blog/post/unselected-article.md'
        (self.root / name).write_text('# Must stay outside main\n')
        self.rejected('unknown publication source: ' + name)
        self.git('add', '--', name)
        self.rejected('unknown publication source: ' + name)

    def test_nonancestor_head_is_rejected(self):
        self.accepted()
        self.git('update-ref', 'HEAD', 'e457143e8be2f7d54f69bc3e9b80230375be49de')
        self.rejected('merge-base --is-ancestor ' + MERGE + ' HEAD')

    def test_missing_pinned_objects_are_rejected(self):
        self.accepted()
        (self.root / '.git').rename(Path(self.temp.name) / 'saved-git')
        self.git('init', '-q')
        self.rejected('unavailable publication Git object/history')

    def test_generated_output_symlink_is_rejected(self):
        self.accepted()
        foreign = Path(self.temp.name) / 'outside-output'; foreign.mkdir()
        name = 'blog/.vitepress/dist'; (self.root / name).symlink_to(foreign, target_is_directory=True)
        self.rejected('linked publication source: ' + name)

    def test_existing_allowed_sources_are_still_immutable(self):
        self.accepted()
        for name in ('scripts/article-publication.py', 'scripts/materialize-writing-skills.py',
                     'tests/article_publication/test_cli.py', 'docs/agents/issue-tracker.md'):
            with self.subTest(path=name):
                path = self.root / name; original = path.read_bytes()
                try:
                    path.write_bytes(original + b'\n# UNREVIEWED CHANGE\n')
                    self.rejected('changed publication source: ' + name)
                finally:
                    path.write_bytes(original)
        name = 'scripts/article-publication.py'; (self.root / name).unlink()
        self.rejected('missing evidence/source path: ' + name)
