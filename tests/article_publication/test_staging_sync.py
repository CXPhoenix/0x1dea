"""P09/P10 at public CLI + disposable real Git boundary; no remote mutations."""
import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zlib

CLI = Path(__file__).resolve().parents[2] / 'scripts/staging-sync.py'
ARTICLE = 'blog/post/B.md'


class StagingSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='staging-sync-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.repo = self.root / 'source'
        self.repo.mkdir()
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.put('engineering.txt', b'base\n')
        self.put('maintenance/harness-adoption/history.json', b'{"contract": "unchanged"}\n')
        self.put(ARTICLE, b'---\ntitle: B\n---\n\nfirst published paragraph\n\nseparator\n\nlast published paragraph\n')
        alias = self.repo / 'skills/phoenix-writing/reference'
        alias.parent.mkdir(parents=True, exist_ok=True)
        alias.symlink_to('../../maintenance/writing-skills/legacy/phoenix-writing/reference')
        self.base = self.commit()
        self.git('switch', '-q', '-c', 'staging')
        self.put(ARTICLE, b'---\ntitle: B\n---\n\nfirst published paragraph\n\nseparator\n\nlast candidate paragraph\n')
        self.put('blog/post/B/assets/photo.bin', b'original asset')
        self.stage = self.commit()
        self.git('branch', 'candidate/B')
        self.git('switch', '-q', 'main')
        self.put('engineering.txt', b'main improved\n')
        self.main = self.commit()
        self.registry = self.make_registry()
        self.policy = self.root / 'trusted-registry.json'
        self.output = self.root / 'result'

    def git(self, *args):
        result = subprocess.run(['git', *args], cwd=self.repo, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def put(self, name, data):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def commit(self):
        self.git('add', '--all')
        tree = self.git('write-tree').strip()
        parents = self.git('for-each-ref', '--format=%(objectname)', self.git('symbolic-ref', 'HEAD').strip()).strip()
        oid = self.git('commit-tree', tree, '-m', 'Synthetic fixture', *(['-p', parents] if parents else [])).strip()
        self.git('update-ref', 'HEAD', oid)
        return oid

    def identities(self, ref):
        result = {}
        for row in self.git('ls-tree', '-r', ref).splitlines():
            meta, path = row.split('\t')
            mode, kind, blob = meta.split()
            self.assertEqual(kind, 'blob')
            result[path] = {'mode': mode, 'blob': blob}
        return result

    def make_registry(self):
        main = self.identities('main')
        stage = self.identities('staging')
        candidate_paths = [ARTICLE, 'blog/post/B/assets/photo.bin']
        return {'version': 1, 'target': 'staging', 'repository': str(self.repo),
                'main': {'ref': 'main', 'sha': self.git('rev-parse', 'main').strip()},
                'staging': {'ref': 'staging', 'sha': self.git('rev-parse', 'staging').strip()},
                'trees': {'main': main, 'staging': stage},
                'candidates': [{'id': 'B', 'source': {'ref': 'candidate/B', 'sha': self.stage},
                                'paths': {p: stage[p] for p in candidate_paths}}],
                'engineering': ['engineering.txt'],
                'checks': {'maintenance/harness-adoption/history.json': stage['maintenance/harness-adoption/history.json']}}

    def run_cli(self, operation='prepare', *extra):
        raw = (json.dumps(self.registry, indent=2) + '\n').encode()
        self.policy.write_bytes(raw)
        return subprocess.run([sys.executable, str(CLI), operation, '--registry', str(self.policy),
                               '--registry-sha256', hashlib.sha256(raw).hexdigest(),
                               '--output', str(self.output), *extra], capture_output=True, text=True, env=getattr(self, 'child_env', None))

    def ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def source_snapshot(self):
        git_root = self.repo / '.git'
        return {str(p.relative_to(self.repo)): p.read_bytes() for p in self.repo.rglob('*')
                if p.is_file() and (git_root / 'objects') not in p.parents}

    def test_clean_sync_has_independent_expected_tree_and_preserves_dirty_source(self):
        self.put('engineering.txt', b'uncommitted local edit\n')
        self.put('untracked.txt', b'keep untracked\n')
        before = self.source_snapshot()
        objects = sorted(str(p.relative_to(self.repo)) for p in (self.repo / '.git/objects').rglob('*'))
        report = self.ok(self.run_cli())
        self.assertEqual(report['status'], 'ready')
        self.assertEqual(report['target'], 'staging')
        self.assertTrue(report['local_ready'])
        self.assertFalse(report['publishable'])
        merged = self.identities_from_output(report['result_tree'])
        expected = dict(self.registry['trees']['staging'])
        expected['engineering.txt'] = self.registry['trees']['main']['engineering.txt']
        self.assertEqual(merged, expected)
        self.assertEqual(before, self.source_snapshot())
        self.assertEqual(objects, sorted(str(p.relative_to(self.repo)) for p in (self.repo / '.git/objects').rglob('*')))
        verified = self.ok(self.run_cli('verify'))
        self.assertEqual(verified['result_tree'], report['result_tree'])

    def test_already_contained_main_returns_noop_without_pr_readiness(self):
        self.git('update-ref', 'refs/heads/main', self.base)
        self.registry = self.make_registry()
        self.registry['engineering'] = []
        before = self.source_snapshot()
        report = self.ok(self.run_cli())
        self.assertEqual(report['status'], 'no-op')
        self.assertFalse(report['local_ready'])
        self.assertEqual(report['result_tree'], self.git('rev-parse', 'staging^{tree}').strip())
        self.assertEqual(before, self.source_snapshot())
        self.assertEqual(self.ok(self.run_cli('verify'))['status'], 'no-op')

    def test_conflict_reports_exact_paths_and_never_materializes_readiness(self):
        self.put(ARTICLE, b'---\ntitle: B\n---\n\nfirst published paragraph\n\nseparator\n\nlast incompatible main paragraph\n')
        self.commit()
        self.registry = self.make_registry()
        before = self.source_snapshot()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report['status'], 'conflict')
        self.assertEqual(report['paths'], [ARTICLE])
        self.assertFalse(report['local_ready'])
        self.assertFalse(self.output.exists())
        self.assertEqual(before, self.source_snapshot())

    def test_conflict_free_different_paragraph_edit_blocks_full_candidate_blob(self):
        self.put(ARTICLE, b'---\ntitle: B\n---\n\nfirst changed main paragraph\n\nseparator\n\nlast published paragraph\n')
        self.commit()
        self.registry = self.make_registry()
        before = self.source_snapshot()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report['status'], 'failure')
        self.assertEqual(report['paths'], [ARTICLE])
        self.assertIn('candidate identity changed', report['error'])
        self.assertFalse(self.output.exists())
        self.assertEqual(before, self.source_snapshot())

    def test_registry_requires_complete_unique_candidates_fixed_role_and_strict_schema(self):
        original = json.loads(json.dumps(self.registry))
        cases = [
            ('missing candidate', lambda p: p['candidates'][0]['paths'].pop(ARTICLE)),
            ('overlap', lambda p: p['candidates'].append(dict(p['candidates'][0], id='B-copy'))),
            ('role', lambda p: p.update(target='main')),
            ('unknown', lambda p: p.update(waive_folders=['blog/'])),
            ('engineering article', lambda p: p['engineering'].append(ARTICLE)),
            ('incomplete source', lambda p: p['trees']['main'].pop('engineering.txt')),
        ]
        before = self.source_snapshot()
        for label, change in cases:
            with self.subTest(case=label):
                self.output = self.root / ('case-' + label.replace(' ', '-'))
                self.registry = json.loads(json.dumps(original))
                change(self.registry)
                result = self.run_cli()
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertFalse(json.loads(result.stdout)['local_ready'])
                self.assertFalse(self.output.exists())
                self.assertEqual(before, self.source_snapshot())
        self.registry = original

    def test_candidate_source_pin_must_own_the_registered_full_identity(self):
        self.git('update-ref', 'refs/heads/candidate/B', self.base)
        self.registry['candidates'][0]['source']['sha'] = self.base
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        report = json.loads(result.stdout)
        self.assertIn('candidate source identity', report['error'])
        self.assertIn(ARTICLE, report['paths'])
        self.assertFalse(self.output.exists())

    def test_literal_historical_alias_is_preserved_and_new_symlinks_are_rejected(self):
        alias = 'skills/phoenix-writing/reference'
        report = self.ok(self.run_cli())
        self.assertEqual(self.identities_from_output(report['result_tree'])[alias], self.registry['trees']['staging'][alias])
        self.output = self.root / 'unsafe-output'
        self.git('switch', '-q', 'staging')
        path = self.repo / alias
        path.unlink()
        path.symlink_to('/etc/passwd')
        self.stage = self.commit()
        self.git('update-ref', 'refs/heads/candidate/B', self.stage)
        self.registry = self.make_registry()
        self.registry['engineering'].append(alias)
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unsafe symlink', json.loads(result.stdout)['error'])
        self.assertFalse(self.output.exists())

    def test_local_pin_advance_expires_receipt_for_main_staging_and_candidate_source(self):
        for ref in ('main', 'staging', 'candidate/B'):
            with self.subTest(ref=ref):
                self.output = self.root / ('prepared-' + ref.replace('/', '-'))
                self.ok(self.run_cli())
                old = self.git('rev-parse', ref).strip()
                self.git('update-ref', 'refs/heads/' + ref, self.base)
                before = self.source_snapshot()
                result = self.run_cli('verify')
                self.assertNotEqual(result.returncode, 0)
                report = json.loads(result.stdout)
                self.assertEqual(before, self.source_snapshot())
                self.git('update-ref', 'refs/heads/' + ref, old)
                self.assertEqual(report['status'], 'stale')
                self.assertFalse(report['local_ready'])
                self.assertIn(ref, report['error'])

    def test_schema_and_help_expose_supported_local_operations_without_role_selector(self):
        result = subprocess.run([sys.executable, str(CLI), 'schema'], capture_output=True, text=True)
        report = self.ok(result)
        self.assertEqual(report['target'], 'staging')
        self.assertEqual(report['operations'], ['prepare', 'verify', 'schema'])
        self.assertEqual(set(report['registry']['required']), set(self.registry))
        self.assertFalse(report['registry']['additionalProperties'])
        help_result = subprocess.run([sys.executable, str(CLI), '--help'], capture_output=True, text=True)
        self.assertEqual(help_result.returncode, 0)
        self.assertIn('--registry-sha256', help_result.stdout)
        self.assertNotIn('--role', help_result.stdout)

    def test_protected_history_check_cannot_be_omitted_or_use_wrong_expected_identity(self):
        self.registry['checks'] = {}
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('protected history', json.loads(result.stdout)['error'])
        self.registry = self.make_registry()
        name = 'maintenance/harness-adoption/history.json'
        self.registry['checks'][name] = self.registry['trees']['main']['engineering.txt']
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertIn('protected identity check failed', report['error'])
        self.assertEqual(report['paths'], [name])
        self.assertFalse(self.output.exists())

    def test_symlinked_output_parent_cannot_redirect_writes(self):
        destination = self.root / 'outside'
        destination.mkdir()
        alias = self.root / 'output-alias'
        alias.symlink_to(destination, target_is_directory=True)
        self.output = alias / 'redirected'
        before = self.source_snapshot()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('output', json.loads(result.stdout)['error'])
        self.assertFalse((destination / 'redirected').exists())
        self.assertEqual(before, self.source_snapshot())

    def test_final_pin_reread_blocks_a_native_merge_race(self):
        wrapper = self.root / 'bin'
        wrapper.mkdir()
        real_git = shutil.which('git')
        script = wrapper / 'git'
        script.write_text('#!' + sys.executable + '\n' +
                          'import subprocess, sys\n' +
                          'result = subprocess.run([' + repr(real_git) + ', *sys.argv[1:]])\n' +
                          'if "merge-tree" in sys.argv:\n' +
                          '    subprocess.run([' + repr(real_git) + ', "-C", ' + repr(str(self.repo)) +
                          ', "update-ref", "refs/heads/main", ' + repr(self.base) + '], check=True)\n' +
                          'sys.exit(result.returncode)\n')
        script.chmod(0o755)
        self.child_env = {**os.environ, 'PATH': str(wrapper) + os.pathsep + os.environ['PATH']}
        index = (self.repo / '.git/index').read_bytes()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['status'], 'stale')
        self.assertFalse(self.output.exists())
        self.assertEqual(index, (self.repo / '.git/index').read_bytes())
        self.assertEqual(self.git('rev-parse', 'main').strip(), self.base)

    def test_source_custom_shell_merge_driver_is_not_executed(self):
        marker = self.root / 'executed'
        self.git('config', 'merge.candidate.driver', 'touch ' + str(marker))
        self.put('.gitattributes', b'engineering.txt merge=candidate\n')
        self.commit()
        self.git('switch', '-q', 'staging')
        self.put('.gitattributes', b'engineering.txt merge=candidate\n')
        self.put('engineering.txt', b'staging incompatible\n')
        self.stage = self.commit()
        self.git('update-ref', 'refs/heads/candidate/B', self.stage)
        self.registry = self.make_registry()
        before = self.source_snapshot()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['paths'], ['engineering.txt'])
        self.assertFalse(marker.exists())
        self.assertEqual(before, self.source_snapshot())

    def test_candidate_metadata_mode_and_receipt_tampering_block_readiness(self):
        self.put(ARTICLE, b'---\ntitle: changed main metadata\n---\n\nfirst published paragraph\n\nseparator\n\nlast published paragraph\n')
        self.commit()
        self.registry = self.make_registry()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['paths'], [ARTICLE])
        self.git('update-ref', 'refs/heads/main', self.main)
        (self.repo / ARTICLE).write_bytes(subprocess.check_output(['git', 'show', self.main + ':' + ARTICLE], cwd=self.repo))
        (self.repo / ARTICLE).chmod(0o755)
        self.commit()
        self.registry = self.make_registry()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['paths'], [ARTICLE])
        self.git('update-ref', 'refs/heads/main', self.main)
        self.registry = self.make_registry()
        self.ok(self.run_cli())
        receipt_path = self.output / 'receipt.json'
        receipt = json.loads(receipt_path.read_bytes())
        receipt['result_tree'] = self.git('rev-parse', 'main^{tree}').strip()
        receipt_path.write_text(json.dumps(receipt))
        before = self.source_snapshot()
        result = self.run_cli('verify')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('receipt or result tree', json.loads(result.stdout)['error'])
        self.assertFalse(json.loads(result.stdout)['local_ready'])
        self.assertEqual(before, self.source_snapshot())

    def test_verify_rejects_corrupt_output_blobs_with_unchanged_source_and_receipt(self):
        self.ok(self.run_cli())
        source = self.source_snapshot()
        receipt = (self.output / 'receipt.json').read_bytes()
        for name, expected in (
            ('engineering.txt', self.registry['trees']['main']['engineering.txt']),
            (ARTICLE, self.registry['trees']['staging'][ARTICLE]),
        ):
            with self.subTest(path=name):
                oid = expected['blob']
                blob = self.output / 'result.git/objects' / oid[:2] / oid[2:]
                blob.parent.mkdir(exist_ok=True)
                original = blob.read_bytes() if blob.exists() else None
                if original is not None:
                    blob.chmod(0o600)
                payload = b'harmless unapproved output artifact bytes\n'
                blob.write_bytes(zlib.compress(b'blob ' + str(len(payload)).encode() + b'\0' + payload))
                try:
                    result = self.run_cli('verify')
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    report = json.loads(result.stdout)
                    self.assertEqual(report['status'], 'failure')
                    self.assertFalse(report['local_ready'])
                    self.assertIn('blob identity mismatch', report['error'])
                    self.assertEqual(report['paths'], [name])
                    self.assertEqual((self.output / 'receipt.json').read_bytes(), receipt)
                    self.assertEqual(self.source_snapshot(), source)
                finally:
                    if original is None:
                        blob.unlink()
                    else:
                        blob.write_bytes(original)

    def test_source_git_template_cannot_install_an_external_merge_driver(self):
        marker = self.root / 'template-driver-executed'
        template = self.root / 'git-template'
        template.mkdir()
        (template / 'config').write_text('[merge "candidate"]\n\tdriver = touch ' + str(marker) + '\n')
        self.git('config', 'init.templateDir', str(template))
        self.put('.gitattributes', b'engineering.txt merge=candidate\n')
        self.commit()
        self.git('switch', '-q', 'staging')
        self.put('.gitattributes', b'engineering.txt merge=candidate\n')
        self.put('engineering.txt', b'staging incompatible\n')
        self.stage = self.commit()
        self.git('update-ref', 'refs/heads/candidate/B', self.stage)
        self.registry = self.make_registry()
        result = self.run_cli()
        self.assertFalse(marker.exists())
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['status'], 'conflict')

    def test_explicit_preview_ui_engineering_is_allowed_without_article_waiver(self):
        self.git('switch', '-q', 'staging')
        self.put('blog/.vitepress/config.mts', b'export default { title: "preview" }\n')
        self.put('blog/index.md', b'# Shared preview\n')
        self.stage = self.commit()
        self.git('update-ref', 'refs/heads/candidate/B', self.stage)
        self.registry = self.make_registry()
        self.registry['engineering'].extend(['blog/.vitepress/config.mts', 'blog/index.md'])
        report = self.ok(self.run_cli())
        result = self.identities_from_output(report['result_tree'])
        self.assertEqual(result['blog/.vitepress/config.mts'], self.registry['trees']['staging']['blog/.vitepress/config.mts'])
        self.assertEqual(result[ARTICLE], self.registry['trees']['staging'][ARTICLE])

    def test_main_ref_cannot_be_labeled_as_staging_even_with_self_consistent_registry(self):
        main = self.registry['trees']['main']
        self.registry['staging'] = dict(self.registry['main'])
        self.registry['trees']['staging'] = dict(main)
        self.registry['candidates'] = []
        self.registry['engineering'] = []
        self.registry['checks'] = {'maintenance/harness-adoption/history.json': main['maintenance/harness-adoption/history.json']}
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('target ref', json.loads(result.stdout)['error'])
        self.assertFalse(self.output.exists())

    def test_partial_promisor_source_configuration_is_rejected_without_fetch(self):
        self.git('config', 'remote.fixture.promisor', 'true')
        self.git('config', 'remote.fixture.partialclonefilter', 'blob:none')
        before = self.source_snapshot()
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('partial/promisor', json.loads(result.stdout)['error'])
        self.assertFalse(self.output.exists())
        self.assertEqual(before, self.source_snapshot())

    def test_included_promisor_configuration_cannot_hide_partial_history(self):
        included = self.root / 'included-git-config'
        included.write_text('[remote "fixture"]\n\tpromisor = true\n')
        self.git('config', 'include.path', str(included))
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('partial/promisor', json.loads(result.stdout)['error'])
        self.assertFalse(self.output.exists())

    def test_missing_candidate_asset_blob_blocks_noop_without_source_object_writes(self):
        self.git('update-ref', 'refs/heads/main', self.base)
        self.registry = self.make_registry()
        self.registry['engineering'] = []
        name = 'blog/post/B/assets/photo.bin'
        blob = self.registry['trees']['staging'][name]['blob']
        (self.repo / '.git/objects' / blob[:2] / blob[2:]).unlink()
        objects = sorted(str(p.relative_to(self.repo)) for p in (self.repo / '.git/objects').rglob('*'))
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        report = json.loads(result.stdout)
        self.assertIn('source blob', report['error'])
        self.assertIn(name, report['paths'])
        self.assertFalse(self.output.exists())
        self.assertEqual(objects, sorted(str(p.relative_to(self.repo)) for p in (self.repo / '.git/objects').rglob('*')))

    def test_corrupted_blob_bytes_cannot_keep_the_registered_git_identity(self):
        name = 'blog/post/B/assets/photo.bin'
        blob = self.registry['trees']['staging'][name]['blob']
        content = b'tampered asset with valid Git object header'
        object_file = self.repo / '.git/objects' / blob[:2] / blob[2:]
        object_file.chmod(0o644)
        object_file.write_bytes(zlib.compress(b'blob ' + str(len(content)).encode() + b'\0' + content))
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertIn('source blob identity mismatch', report['error'])
        self.assertIn(name, report['paths'])
        self.assertFalse(self.output.exists())

    def test_main_deleting_a_staging_canonical_alias_blocks_the_sync(self):
        alias = 'skills/phoenix-writing/reference'
        (self.repo / alias).unlink()
        self.commit()
        self.registry = self.make_registry()
        self.registry['engineering'].append(alias)
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('immutable alias', json.loads(result.stdout)['error'])
        self.assertEqual(json.loads(result.stdout)['paths'], [alias])
        self.assertFalse(self.output.exists())

    def test_fixed_legacy_source_boundary_requires_protected_history_check(self):
        self.git('switch', '-q', 'staging')
        name = 'maintenance/article-publication/source-boundary.json'
        self.put(name, b'{"immutable": true}\n')
        self.stage = self.commit()
        self.git('update-ref', 'refs/heads/candidate/B', self.stage)
        self.registry = self.make_registry()
        self.registry['engineering'].append(name)
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('protected history', json.loads(result.stdout)['error'])
        self.assertIn(name, json.loads(result.stdout)['paths'])
        self.assertFalse(self.output.exists())

    def identities_from_output(self, tree):
        rows = subprocess.check_output(['git', '--git-dir', str(self.output/'result.git'), 'ls-tree', '-r', tree], text=True)
        return {row.split('\t')[1]: {'mode': row.split()[0], 'blob': row.split()[2]} for row in rows.splitlines()}


if __name__ == '__main__':
    unittest.main()
