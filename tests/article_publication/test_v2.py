"""Explicit v2 public CLI seams; legacy behavior remains a separate contract."""
import hashlib
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import unittest
import zlib
from article_publication import test_cli as fixtures

SCRIPT = Path(__file__).resolve().parents[2] / 'scripts/article-publication-v2.py'

class V2Tests(unittest.TestCase):
    git = fixtures.PublicationTests.git
    put = fixtures.PublicationTests.put
    commit = fixtures.PublicationTests.commit
    ok = fixtures.PublicationTests.ok
    reject = fixtures.PublicationTests.reject

    def setUp(self):
        fixtures.PublicationTests.setUp(self)
        self.integrations = []
        self.git('switch', '-q', 'staging')
        for source in self.articles:
            before = self.git('rev-parse', 'HEAD').strip()
            self.git('merge', '--no-ff', '--no-commit', source['ref'])
            tree = self.git('write-tree').strip()
            sha = self.git('commit-tree', tree, '-p', before, '-p', source['sha'], '-m', 'synthetic preview integration').strip()
            self.git('update-ref', 'HEAD', sha)
            self.git('reset', '--hard', sha)
            self.integrations.append(sha)
        self.stage = self.git('rev-parse', 'HEAD').strip()
        self.git('switch', '-q', 'main')
        self.plan['staging']['sha'] = self.stage
        self.v2plan = {'version': 2, 'repository': str(self.repo), 'main': self.plan['main'], 'staging': self.plan['staging'], 'selected': ['A'], 'dependencies': []}
        self.registry = {'version': 2, 'main': self.plan['main'], 'staging': self.plan['staging'], 'anchor': self.main, 'sources': [{**a, 'kind': 'article', 'shared_patches': {}, 'requires': [], 'provenance': {'kind': 'clean'}} for a in self.articles], 'integrations': self.integrations, 'retained': {}, 'staging_inventory': self.identities(self.stage)}
        self.registry_path = self.root / 'trusted-registry.json'

    def identities(self, revision):
        result = {}
        for line in self.git('ls-tree', '-r', '--full-tree', revision).splitlines():
            meta, name = line.split('\t', 1)
            mode, kind, blob = meta.split()
            result[name] = {'mode': mode, 'blob': blob}
        return result

    def v2(self, mode, output, *extra):
        self.plan_path.write_text(json.dumps(self.v2plan))
        raw = json.dumps(self.registry).encode()
        self.registry_path.write_bytes(raw)
        return subprocess.run([sys.executable, str(SCRIPT), mode, '--plan', str(self.plan_path), '--registry', str(self.registry_path), '--registry-sha256', hashlib.sha256(raw).hexdigest(), '--output', str(output), *extra], capture_output=True, text=True)

    def test_explicit_v2_accepts_registered_clean_A_already_previewed_and_v1_still_rejects(self):
        self.reject(fixtures.PublicationTests.run_cli(self, 'prepare', self.root / 'v1'), 'staging ancestry')
        refs = self.git('show-ref')
        self.put('dirty-note.txt', 'PRESERVE_DIRTY_WORK\n')
        prepared = self.root / 'v2'
        report = self.ok(self.v2('prepare', prepared))
        self.assertEqual(report['version'], 2)
        self.assertEqual(report['candidate_tree'], self.git('rev-parse', 'post/A^{tree}').strip())
        self.assertTrue((prepared / 'candidate/blog/post/A.md').is_file())
        self.assertFalse((prepared / 'candidate/blog/post/B.md').exists())
        self.assertFalse(report['publishable'])
        self.assertFalse(report['pr_ready'])
        self.assertEqual(self.git('show-ref'), refs)
        self.assertEqual((self.repo / 'dirty-note.txt').read_text(), 'PRESERVE_DIRTY_WORK\n')

    def test_source_with_staging_integration_ancestry_is_rejected_before_export(self):
        self.git('switch', '-q', 'post/A')
        before = self.git('rev-parse', 'HEAD').strip()
        self.git('merge', '--no-commit', '--no-ff', 'staging')
        merged = self.git('commit-tree', self.git('write-tree').strip(), '-p', before, '-p', self.stage, '-m', 'contaminated source').strip()
        self.git('update-ref', 'HEAD', merged)
        self.git('reset', '--hard', merged)
        self.registry['sources'][0]['sha'] = merged
        out = self.root / 'rejected'
        self.reject(self.v2('prepare', out), 'source ancestry')
        self.assertFalse(out.exists())

    def test_corrupt_blob_bytes_cannot_reuse_reviewed_object_ids(self):
        refs = self.git('show-ref')
        for name in ('blog/index.md', 'blog/post/A.md', 'blog/post/B.md'):
            with self.subTest(path=name):
                oid = self.registry['staging_inventory'][name]['blob']
                blob = self.repo / '.git/objects' / oid[:2] / oid[2:]
                original = blob.read_bytes()
                payload = b'# Unapproved bytes under an unchanged reviewed object id\n'
                blob.chmod(0o600)
                blob.write_bytes(zlib.compress(b'blob ' + str(len(payload)).encode() + b'\0' + payload))
                output = self.root / ('corrupt-' + Path(name).stem)
                try:
                    self.assertEqual(self.git('cat-file', 'blob', oid).encode(), payload)
                    self.reject(self.v2('prepare', output), 'blob object identity')
                    self.assertFalse(output.exists())
                    self.assertEqual(self.git('show-ref'), refs)
                finally:
                    blob.write_bytes(original)

    def test_B_add_then_revert_in_A_is_rejected_even_when_final_tree_is_only_A(self):
        self.git('switch', '-q', 'post/A')
        self.put('blog/post/B.md', 'UNAPPROVED B TRANSIENT SOURCE\n')
        self.commit('add B in source history')
        self.git('rm', 'blog/post/B.md')
        self.commit('revert B but preserve contaminated history')
        self.registry['sources'][0]['sha'] = self.git('rev-parse', 'HEAD').strip()
        out = self.root / 'rejected-history'
        self.reject(self.v2('prepare', out), 'source history')
        self.assertFalse(out.exists())

    def test_omitting_B_from_trusted_registry_blocks_full_staging_inventory(self):
        self.registry['sources'] = self.registry['sources'][:1]
        out = self.root / 'missing-B'
        self.reject(self.v2('prepare', out), 'registry ownership')
        self.assertFalse(out.exists())

    def test_plan_cannot_select_a_role_or_smuggle_unknown_schema_fields(self):
        self.v2plan['role'] = 'staging'
        out = self.root / 'role-spoof'
        self.reject(self.v2('prepare', out), 'schema')
        self.assertFalse(out.exists())

    def test_advancing_source_ref_invalidates_the_old_registry_pin(self):
        self.git('switch', '-q', 'post/A')
        self.put('blog/post/A.md', '# A\n\nADVANCED ARTICLE BYTES MUST NEED NEW POLICY\n')
        self.commit('advance source without renewed registry')
        out = self.root / 'stale-source'
        self.reject(self.v2('prepare', out), 'ref/head drift')
        self.assertFalse(out.exists())

    def test_owned_staging_path_cannot_hide_an_unregistered_revision(self):
        self.git('switch', '-q', 'staging')
        self.put('blog/post/A.md', '# A\n\nUNREGISTERED STAGING REVISION\n')
        self.commit('unregistered direct staging edit')
        latest = self.git('rev-parse', 'HEAD').strip()
        self.plan['staging']['sha'] = latest
        self.v2plan['staging']['sha'] = latest
        self.registry['staging']['sha'] = latest
        self.registry['staging_inventory'] = self.identities(latest)
        out = self.root / 'unregistered-revision'
        self.reject(self.v2('prepare', out), 'registry provenance')
        self.assertFalse(out.exists())

    def test_legacy_classification_requires_explicit_owner_migration_record(self):
        self.registry['sources'][0]['provenance'] = {'kind': 'legacy'}
        self.reject(self.v2('prepare', self.root / 'legacy-without-approval'), 'migration')

    def test_reviewed_legacy_extraction_admits_only_bound_original_and_new_bytes(self):
        source = self.registry['sources'][0]
        extracted = {p: self.identities(source['sha'])[p] for p in source['paths']}
        binding = {'original': self.stage, 'reconstructed': source['sha'], 'extracted': extracted}
        encoded = (json.dumps(binding, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
        source['provenance'] = {'kind': 'legacy', 'migration': {**binding, 'owner_approval': {'record_id': 'synthetic-reviewed-migration', 'binding_sha256': hashlib.sha256(encoded).hexdigest()}}}
        report = self.ok(self.v2('prepare', self.root / 'approved-extraction'))
        self.assertEqual(report['candidate_tree'], self.git('rev-parse', 'post/A^{tree}').strip())

    def test_shallow_repository_is_rejected_even_when_needed_objects_still_exist(self):
        (self.repo / '.git/shallow').write_text(self.main + '\n')
        self.reject(self.v2('prepare', self.root / 'shallow'), 'complete history')

    def merge_fixture(self, other):
        before = self.git('rev-parse', 'HEAD').strip()
        incoming = self.git('rev-parse', other).strip()
        self.git('merge', '--no-ff', '--no-commit', other)
        sha = self.git('commit-tree', self.git('write-tree').strip(), '-p', before, '-p', incoming, '-m', 'synthetic refreshed merge').strip()
        self.git('update-ref', 'HEAD', sha)
        self.git('reset', '--hard', sha)
        return sha

    def refresh_main(self):
        self.git('switch', '-q', 'main')
        self.put('blog/.vitepress/config.mts', "import { defineConfig } from 'vitepress';\nexport default defineConfig({ title: 'ISOLATED SYNTHETIC SITE' });\n")
        self.commit('reviewed main configuration refresh')
        self.main = self.git('rev-parse', 'HEAD').strip()
        self.plan['main']['sha'] = self.main
        for source in self.registry['sources']:
            self.git('switch', '-q', source['ref'])
            source['sha'] = self.merge_fixture('main')
        self.git('switch', '-q', 'staging')
        self.stage = self.merge_fixture('main')
        self.integrations.append(self.stage)
        self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)

    def test_reviewed_conflict_free_main_refresh_uses_fresh_pins(self):
        self.refresh_main()
        report = self.ok(self.v2('prepare', self.root / 'refreshed'))
        self.assertEqual(report['candidate_tree'], self.git('rev-parse', 'post/A^{tree}').strip())
        self.assertEqual((self.root / 'refreshed/candidate/blog/.vitepress/config.mts').read_text(), "import { defineConfig } from 'vitepress';\nexport default defineConfig({ title: 'ISOLATED SYNTHETIC SITE' });\n")

    def shared_patch(self, text):
        source = self.registry['sources'][0]
        self.git('switch', '-q', source['ref'])
        before = self.identities(source['sha'])['blog/index.md']
        self.put('blog/index.md', text)
        self.commit('synthetic reviewed listing patch')
        source['sha'] = self.git('rev-parse', 'HEAD').strip()
        source['shared_patches'][source['sha']] = {'blog/index.md': {'before': before, 'after': self.identities(source['sha'])['blog/index.md']}}
        self.git('switch', '-q', 'staging')
        self.stage = self.merge_fixture(source['ref'])
        self.integrations.append(self.stage)
        self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)

    def test_exact_reviewed_shared_listing_patch_is_included(self):
        self.shared_patch('# Published index\n\n[Selected A](/post/A)\n')
        report = self.ok(self.v2('prepare', self.root / 'shared'))
        self.assertEqual((self.root / 'shared/candidate/blog/index.md').read_text(), '# Published index\n\n[Selected A](/post/A)\n')
        self.assertNotIn('blog/post/B.md', report['files'])

    def test_shared_listing_permission_does_not_admit_unselected_route_or_prose(self):
        self.shared_patch('# Published index\n\n[Unapproved B](/post/B)\n')
        self.reject(self.v2('prepare', self.root / 'shared-B'), 'unselected')

    def test_exact_declared_dependency_is_included_and_undeclared_dependency_refused(self):
        self.git('switch', '-q', 'main')
        self.git('switch', '-q', '-c', 'shared/dependency')
        self.put('blog/public/shared/chart.svg', '<svg>APPROVED EXACT SHARED DEPENDENCY</svg>\n')
        self.commit('synthetic reviewed dependency')
        dependency = {'id': 'chart', 'ref': 'shared/dependency', 'sha': self.git('rev-parse', 'HEAD').strip(), 'paths': ['blog/public/shared/chart.svg'], 'kind': 'dependency', 'shared_patches': {}, 'requires': [], 'provenance': {'kind': 'clean'}}
        self.registry['sources'].append(dependency)
        self.registry['sources'][0]['requires'] = ['chart']
        self.v2plan['dependencies'] = ['chart']
        self.git('switch', '-q', 'staging')
        self.stage = self.merge_fixture(dependency['ref'])
        self.integrations.append(self.stage)
        self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)
        report = self.ok(self.v2('prepare', self.root / 'with-dependency'))
        self.assertIn('blog/public/shared/chart.svg', report['files'])
        self.assertNotIn('blog/post/B.md', report['files'])
        self.v2plan['dependencies'] = []
        self.reject(self.v2('prepare', self.root / 'missing-dependency'), 'dependency')

    def test_unknown_staging_add_revert_history_cannot_hide_behind_equal_final_inventory(self):
        self.git('switch', '-q', 'staging')
        original = (self.repo / 'blog/post/A.md').read_text()
        self.put('blog/post/A.md', original + '\nUNREGISTERED STAGING TRANSIENT CHANGE\n')
        self.commit('unknown direct staging commit')
        self.put('blog/post/A.md', original)
        self.commit('unknown direct staging revert')
        self.stage = self.git('rev-parse', 'HEAD').strip()
        self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)
        self.reject(self.v2('prepare', self.root / 'unknown-stage-history'), 'staging history')

    def test_conflicting_main_refresh_requires_exact_reviewed_resolution_tree(self):
        self.shared_patch('# A listing changed from base\n')
        self.git('switch', '-q', 'main')
        self.put('blog/index.md', '# Main independently changed from base\n')
        self.commit('synthetic main conflict')
        self.main = self.git('rev-parse', 'HEAD').strip()
        self.plan['main']['sha'] = self.main
        for branch in ('post/A', 'staging'):
            self.git('switch', '-q', branch)
            left = self.git('rev-parse', 'HEAD').strip()
            proc = subprocess.run(['git', '-C', str(self.repo), 'merge', '--no-ff', '--no-commit', 'main'], capture_output=True)
            self.assertEqual(proc.returncode, 1)
            self.put('blog/index.md', '# A listing changed from base\n')
            self.git('add', 'blog/index.md')
            tree = self.git('write-tree').strip()
            merged = self.git('commit-tree', tree, '-p', left, '-p', self.main, '-m', 'synthetic explicit conflict resolution').strip()
            self.git('update-ref', 'HEAD', merged); self.git('reset', '--hard', merged)
            self.registry.setdefault('resolutions', {})[merged] = tree
            if branch == 'post/A':
                self.registry['sources'][0]['sha'] = merged
            else:
                self.stage = merged; self.integrations.append(merged)
                self.plan['staging']['sha'] = merged
        self.git('switch', '-q', 'post/B')
        self.registry['sources'][1]['sha'] = self.merge_fixture('main')
        self.registry['staging_inventory'] = self.identities(self.stage)
        saved = self.registry.pop('resolutions')
        self.reject(self.v2('prepare', self.root / 'unreviewed-resolution'), 'unreviewed')
        self.registry['resolutions'] = saved
        self.ok(self.v2('prepare', self.root / 'reviewed-resolution'))
        self.registry['resolutions'][self.stage] = '0' * 40
        self.reject(self.v2('prepare', self.root / 'wrong-resolution'), 'resolution')

    def test_verify_checks_full_receipt_blob_mode_and_literal_aliases(self):
        self.git('switch', '-q', 'main')
        self.git('switch', '-q', '-c', 'main-alias-refresh')
        alias = self.repo / 'skills/phoenix-writing/reference'
        alias.parent.mkdir(parents=True)
        alias.symlink_to('../../maintenance/writing-skills/legacy/phoenix-writing/reference')
        self.commit('immutable baseline alias fixture')
        self.git('switch', '-q', 'main')
        self.git('merge', '--ff-only', 'main-alias-refresh')
        self.refresh_main()
        bundle = self.root / 'literal-alias'
        self.ok(self.v2('prepare', bundle))
        self.assertTrue((bundle / 'candidate/skills/phoenix-writing/reference').is_symlink())
        self.ok(self.v2('verify', bundle))
        article = bundle / 'candidate/blog/post/A.md'
        article.chmod(0o755)
        self.reject(self.v2('verify', bundle), 'candidate')
        article.chmod(0o644)
        article.write_text('TAMPERED SOURCE\n')
        self.reject(self.v2('verify', bundle), 'candidate')

    def test_unselected_existing_article_revision_keeps_published_baseline(self):
        self.git('switch', '-q', 'main')
        published = '# Published C\n\nPUBLISHED BASELINE THAT MUST REMAIN\n'
        self.put('blog/post/C.md', published)
        self.commit('publish independent baseline C')
        self.refresh_main()
        self.git('switch', '-q', '-c', 'post/C', 'main')
        self.put('blog/post/C.md', published + '\n' + ('UNAPPROVED LONG C REVISION ' * 8) + '\n')
        self.put('blog/public/C-secret.bin', 'UNAPPROVED C ASSET')
        self.commit('candidate revision C')
        source = {'id': 'C', 'ref': 'post/C', 'sha': self.git('rev-parse', 'HEAD').strip(), 'paths': ['blog/post/C.md', 'blog/public/C-secret.bin'], 'kind': 'article', 'shared_patches': {}, 'requires': [], 'provenance': {'kind': 'clean'}}
        self.registry['sources'].append(source)
        self.git('switch', '-q', 'staging')
        self.stage = self.merge_fixture(source['ref']); self.integrations.append(self.stage)
        self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)
        bundle = self.root / 'retain-published-C'
        self.ok(self.v2('prepare', bundle))
        self.assertEqual((bundle / 'candidate/blog/post/C.md').read_text(), published)
        self.assertFalse((bundle / 'candidate/blog/public/C-secret.bin').exists())

    @unittest.skipUnless(sys.platform == 'darwin' and (os.environ.get('PUBLICATION_TEST_DEPENDENCIES') or (SCRIPT.parents[1] / 'node_modules').is_dir()), 'real macOS boundary/runtime unavailable; never a readiness pass')
    def test_isolated_real_build_and_separate_evidence_required_for_readiness(self):
        self.refresh_main()
        bundle = self.root / 'build-candidate'
        self.ok(self.v2('prepare', bundle))
        self.ok(self.v2('verify', bundle))
        self.reject(self.v2('ready', bundle), 'required')
        runtime = {'version': 1, 'node': str(Path(shutil.which('node')).resolve()), 'node_version': 'v24.13.0', 'dependencies': str(Path(os.environ.get('PUBLICATION_TEST_DEPENDENCIES', SCRIPT.parents[1] / 'node_modules')).resolve())}
        runtime_path = self.root / 'reviewed-runtime.json'
        raw = json.dumps(runtime).encode(); runtime_path.write_bytes(raw)
        build = self.root / 'actual-build'
        built = self.ok(self.v2('build', bundle, '--runtime', str(runtime_path), '--runtime-sha256', hashlib.sha256(raw).hexdigest(), '--build-output', str(build)))
        self.assertEqual(built['status'], 'pass')
        self.assertEqual(built['isolation']['outside_read'], 'denied')
        self.assertEqual(built['isolation']['outside_write'], 'denied')
        self.assertEqual(built['isolation']['network'], 'denied')
        self.assertFalse(built['pr_ready'])
        verified = self.ok(self.v2('verify', bundle))
        approval = {'version': 2, 'record_id': 'SYNTHETIC OWNER REVIEW ONLY', 'binding': built['binding'], 'preview': {'staging_sha': self.stage, 'served_sha': self.stage, 'evidence_sha256': 'f' * 64}}
        approval_path = self.root / 'reviewed-approval.json'
        approval_raw = json.dumps(approval).encode(); approval_path.write_bytes(approval_raw)
        build_receipt = build / 'build-receipt.json'
        extra = ('--build-receipt', str(build_receipt), '--build-sha256', hashlib.sha256(build_receipt.read_bytes()).hexdigest(), '--approval', str(approval_path), '--approval-sha256', hashlib.sha256(approval_raw).hexdigest())
        ready = self.ok(self.v2('ready', bundle, *extra))
        self.assertTrue(ready['pr_ready']); self.assertFalse(ready['publishable'])
        if os.environ.get('PUBLICATION_TEST_EVIDENCE'):
            evidence = Path(os.environ['PUBLICATION_TEST_EVIDENCE']); evidence.mkdir(parents=True, exist_ok=True)
            (evidence / 'actual-build-receipt.json').write_bytes(build_receipt.read_bytes())
            (evidence / 'local-ready.json').write_text(json.dumps(ready, indent=2) + '\n')
            (evidence / 'build-stdout.txt').write_bytes((build / 'build-stdout.txt').read_bytes())
            (evidence / 'build-stderr.txt').write_bytes((build / 'build-stderr.txt').read_bytes())
        (build / 'output/search-data.json').write_text('/post/B.html')
        self.reject(self.v2('ready', bundle, *extra), 'output')

    def test_escaping_include_and_active_import_are_rejected_before_build(self):
        for text in ('# A\n\n<!-- @include: ../../../../outside -->\n', '# A\n\n<script setup>import x from "outside"</script>\n'):
            self.git('switch', '-q', 'post/A')
            self.put('blog/post/A.md', text); self.commit('synthetic unsafe source input')
            self.registry['sources'][0]['sha'] = self.git('rev-parse', 'HEAD').strip()
            self.git('switch', '-q', 'staging'); self.stage = self.merge_fixture('post/A')
            self.integrations.append(self.stage); self.plan['staging']['sha'] = self.stage
            self.registry['staging_inventory'] = self.identities(self.stage)
            self.reject(self.v2('prepare', self.root / ('unsafe-' + self.stage)), 'build input')

    def test_new_source_symlink_and_submodule_are_rejected(self):
        self.git('switch', '-q', 'post/A')
        path = self.repo / 'blog/post/escape.md'; path.symlink_to('/outside')
        self.commit('unsafe candidate link')
        self.registry['sources'][0]['sha'] = self.git('rev-parse', 'HEAD').strip()
        self.registry['sources'][0]['paths'].append('blog/post/escape.md')
        self.git('switch', '-q', 'staging'); self.stage = self.merge_fixture('post/A')
        self.integrations.append(self.stage); self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)
        self.reject(self.v2('prepare', self.root / 'unsafe-link'), 'symlink')
        self.git('switch', '-q', 'post/A'); self.git('rm', 'blog/post/escape.md')
        self.git('update-index', '--add', '--cacheinfo', '160000,' + self.main + ',blog/post/escape.md')
        # Plumbing commit without reading any external submodule.
        sha = self.git('commit-tree', self.git('write-tree').strip(), '-p', self.registry['sources'][0]['sha'], '-m', 'synthetic unsafe submodule').strip()
        self.git('update-ref', 'HEAD', sha); self.git('reset', '--hard', sha)
        self.registry['sources'][0]['sha'] = sha
        self.plan['staging'] = {'ref': 'post/A', 'sha': sha}
        self.v2plan['staging'] = self.plan['staging']; self.registry['staging'] = self.plan['staging']
        self.registry['staging_inventory'] = self.identities(sha)
        self.reject(self.v2('prepare', self.root / 'unsafe-submodule'), 'tree entry')

    def test_exact_retained_identities_and_asset_ownership_are_mandatory(self):
        source = self.registry['sources'][1]
        self.git('switch', '-q', source['ref'])
        self.put('blog/public/B-secret.bin', 'UNAPPROVED SECRET B ASSET'); self.commit('B exclusive asset')
        source['sha'] = self.git('rev-parse', 'HEAD').strip()
        self.git('switch', '-q', 'staging'); self.stage = self.merge_fixture(source['ref'])
        self.integrations.append(self.stage); self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)
        self.registry['retained']['blog/public/B-secret.bin'] = self.identities(self.stage)['blog/public/B-secret.bin']
        self.reject(self.v2('prepare', self.root / 'asset-waiver'), 'ownership')
        self.registry['retained'] = {}; source['paths'].append('blog/public/B-secret.bin')
        self.ok(self.v2('prepare', self.root / 'asset-owned'))
        self.registry['sources'][0]['paths'].append('blog/public/B-secret.bin')
        self.reject(self.v2('prepare', self.root / 'overlap'), 'overlap')

    def test_hash_duplicate_schema_and_host_git_configuration_cannot_select_authority(self):
        sentinel = self.root / 'shell-driver-ran'
        self.git('config', 'merge.text.driver', 'touch ' + str(sentinel))
        self.ok(self.v2('prepare', self.root / 'no-source-driver'))
        self.assertFalse(sentinel.exists())
        self.registry['staging_inventory']['blog/post/B.md']['mode'] = '100755'
        self.reject(self.v2('prepare', self.root / 'forged-full-inventory'), 'inventory')

    def test_permitted_HTML_listing_cannot_hide_unselected_route_in_href(self):
        self.shared_patch('# Index\n\n<a href="/post/B.html">Read the next article</a>\n')
        self.reject(self.v2('prepare', self.root / 'hidden-href'), 'unselected')

    def test_canonical_alias_cannot_be_newly_added_by_article_source(self):
        self.git('switch', '-q', 'post/A')
        name = 'skills/phoenix-writing/reference'
        path = self.repo / name; path.parent.mkdir(parents=True)
        path.symlink_to('../../maintenance/writing-skills/legacy/phoenix-writing/reference')
        self.commit('unapproved new canonical alias')
        source = self.registry['sources'][0]; source['sha'] = self.git('rev-parse', 'HEAD').strip(); source['paths'].append(name)
        self.git('switch', '-q', 'staging'); self.stage = self.merge_fixture('post/A')
        self.integrations.append(self.stage); self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)
        self.reject(self.v2('prepare', self.root / 'new-canonical-alias'), 'immutable alias')

    def test_promisor_local_config_is_refused_before_any_object_fetch(self):
        # No remote URL or missing object: safe public CLI red for configuration admission.
        self.git('config', 'remote.untrusted.promisor', 'true')
        self.reject(self.v2('prepare', self.root / 'partial-source'), 'partial/promisor')

    def test_empty_other_article_commit_is_rejected_by_identity(self):
        # Build a valid complete preview graph where B already exists on main,
        # but its pending topic has only an empty commit. A forks that topic.
        a_text = (self.repo / 'blog/index.md').read_text()
        self.git('switch', '-q', 'main'); self.put('blog/post/B.md', '# Published B\n')
        self.commit('published B baseline'); self.main = self.git('rev-parse', 'HEAD').strip()
        self.plan['main']['sha'] = self.main; self.registry['anchor'] = self.main
        self.git('switch', '-q', 'post/B'); self.git('reset', '--hard', self.main)
        self.commit('empty candidate B commit'); b_sha = self.git('rev-parse', 'HEAD').strip()
        self.registry['sources'][1]['sha'] = b_sha
        self.git('switch', '-q', 'post/A'); self.git('reset', '--hard', b_sha)
        self.put('blog/post/A.md', '# A\n\nSelected A independent content\n'); self.commit('A from empty B topic')
        self.registry['sources'][0]['sha'] = self.git('rev-parse', 'HEAD').strip()
        self.git('switch', '-q', 'staging'); self.git('reset', '--hard', self.main)
        self.integrations.clear()
        for source in self.registry['sources']:
            merged = self.merge_fixture(source['ref']); self.integrations.append(merged)
        self.stage = merged; self.plan['staging']['sha'] = merged
        self.registry['staging_inventory'] = self.identities(merged)
        self.reject(self.v2('prepare', self.root / 'empty-B-ancestor'), 'other candidate ancestry')

    def test_missing_blob_promisor_never_runs_external_helper(self):
        sentinel = self.root / 'external-helper-ran'
        blob = self.git('rev-parse', 'post/B:blog/post/B.md').strip()
        (self.repo / '.git/objects' / blob[:2] / blob[2:]).unlink()
        self.git('config', 'remote.untrusted.promisor', 'true')
        self.git('config', 'remote.untrusted.url', 'ext::/usr/bin/touch ' + str(sentinel))
        self.git('config', 'protocol.ext.allow', 'always')
        self.reject(self.v2('prepare', self.root / 'no-lazy-fetch'), 'partial/promisor')
        self.assertFalse(sentinel.exists())

    def test_existing_canonical_alias_cannot_be_deleted_by_article_source(self):
        self.git('switch', '-q', 'main')
        name = 'skills/phoenix-writing/reference'
        path = self.repo / name; path.parent.mkdir(parents=True)
        path.symlink_to('../../maintenance/writing-skills/legacy/phoenix-writing/reference')
        self.commit('baseline canonical alias'); self.refresh_main()
        source = self.registry['sources'][0]
        self.git('switch', '-q', source['ref']); self.git('rm', name); self.commit('delete canonical alias in article')
        source['sha'] = self.git('rev-parse', 'HEAD').strip(); source['paths'].append(name)
        self.git('switch', '-q', 'staging'); self.stage = self.merge_fixture(source['ref'])
        self.integrations.append(self.stage); self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)
        self.reject(self.v2('prepare', self.root / 'deleted-canonical-alias'), 'immutable alias')

    def test_short_unselected_revision_has_no_exclusion_override(self):
        self.git('switch', '-q', 'main'); self.put('blog/post/C.md', '# Published C\n'); self.commit('published C')
        self.refresh_main()
        self.git('switch', '-q', '-c', 'post/C', 'main')
        self.put('blog/post/C.md', '# Published C\n\nShort revision.\n'); self.commit('short C revision')
        source = {'id': 'C', 'ref': 'post/C', 'sha': self.git('rev-parse', 'HEAD').strip(), 'paths': ['blog/post/C.md'], 'kind': 'article', 'shared_patches': {}, 'requires': [], 'provenance': {'kind': 'clean'}}
        self.registry['sources'].append(source)
        self.git('switch', '-q', 'staging'); self.stage = self.merge_fixture(source['ref'])
        self.integrations.append(self.stage); self.plan['staging']['sha'] = self.stage
        self.registry['staging_inventory'] = self.identities(self.stage)
        bundle = self.root / 'no-signature'
        result = self.ok(self.v2('prepare', bundle))
        self.assertEqual(result['source_scan']['status'], 'exclusion-unverified')
        self.assertIn('C', result['source_scan']['unverified_sources'])
        self.assertFalse(result['pr_ready'])
        self.reject(self.v2('ready', bundle), 'required')
