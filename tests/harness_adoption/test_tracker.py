import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[2] / 'scripts/verify-harness-adoption.py'
spec = importlib.util.spec_from_file_location('adoption_verifier', MODULE)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_authorized_lint_dependency_is_exact_and_fail_closed(self):
        before = '{"devDependencies":{"@types/js-yaml":"^4.0.9"}}'
        after = '{"devDependencies":{"@types/js-yaml":"^4.0.9","@unocss/eslint-plugin":"66.6.0"}}'
        verifier.check_lint_dependency_delta(before, after)
        for unsafe in (after.replace('66.6.0', '66.10.5'), after.replace('^4.0.9', '^4.1.0'), after.replace('"66.6.0"', '"66.6.0","other-package":"1.0.0"'), before):
            with self.assertRaises(ValueError):
                verifier.check_lint_dependency_delta(before, unsafe)

    def test_lint_cleanup_manifest_is_exact_and_fail_closed(self):
        import json
        guard = getattr(verifier, 'check_lint_cleanup_delta', None)
        self.assertTrue(callable(guard), 'cleanup needs a separate successor contract')
        before = {'devDependencies': {'eslint': '^10.0.0', '@unocss/eslint-plugin': '66.6.0'}, 'scripts': {'test:unit': 'vitest run'}}
        after = json.loads(json.dumps(before))
        after['devDependencies']['eslint'] = '9.39.2'
        after['scripts']['lint'] = verifier.LINT_COMMAND
        guard(json.dumps(before), json.dumps(after))
        for section, key, value in (
            ('devDependencies', 'eslint', '^9.39.2'),
            ('devDependencies', '@unocss/eslint-plugin', '66.10.5'),
            ('devDependencies', 'unrelated', '1.0.0'),
            ('scripts', 'lint', 'eslint scripts --quiet'),
            ('scripts', 'test:unit', 'echo pass'),
        ):
            unsafe = json.loads(json.dumps(after))
            unsafe[section][key] = value
            with self.assertRaises(ValueError):
                guard(json.dumps(before), json.dumps(unsafe))

    def test_lint_successor_rejects_source_scope_and_history_tampering(self):
        import json
        import shutil
        import subprocess
        source = MODULE.parents[1]
        if not (source / 'maintenance/lint-cleanup/source-boundary.json').exists():
            self.skipTest('lint successor is absent in this historical tree')
        fixture = self.root / 'successor'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', str(source), str(fixture)], check=True, capture_output=True)
        names = set(verifier.LINT_UPDATE_NAMES) | {
            'uno.config.ts', 'tests/lintCleanup.vitest.ts', 'maintenance/lint-cleanup/source-boundary.json',
            'maintenance/article-publication/source-boundary.json',
        }
        for name in names:
            target = fixture / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, target)
        verifier.check_lint_successor(fixture)
        boundary_path = fixture / 'maintenance/lint-cleanup/source-boundary.json'
        original = boundary_path.read_bytes()
        for change in ('scope', 'base', 'path', 'before_hash', 'after_hash', 'new_hash'):
            data = json.loads(original)
            if change == 'scope': data['scope'] = 'unapproved'
            elif change == 'base': data['base'] = '0' * 40
            elif change == 'path': data['preserved_updates']['blog/about.md'] = data['preserved_updates']['package.json']
            elif change == 'before_hash': data['preserved_updates']['package.json']['before_sha256'] = '0' * 64
            elif change == 'after_hash': data['preserved_updates']['package.json']['after_sha256'] = '0' * 64
            else: data['new_sources']['uno.config.ts'] = '0' * 64
            boundary_path.write_text(json.dumps(data))
            with self.subTest(change=change), self.assertRaises(ValueError):
                verifier.check_lint_successor(fixture)
        boundary_path.write_bytes(original)
        for name in ('scripts/vpHelper.ts', 'uno.config.ts', 'maintenance/article-publication/source-boundary.json'):
            target = fixture / name
            content = target.read_bytes()
            target.write_bytes(content + b'\nchanged')
            with self.subTest(path=name), self.assertRaises(ValueError):
                verifier.check_lint_successor(fixture)
            target.write_bytes(content)

    def ticket(self, number=1, status='todo', blockers='[]', extra=''):
        p = self.root / f'.proj.tickets/0001-demo/T-{number:04d}-demo.md'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f'---\nid: T-{number:04d}\ntitle: Demo\nepic: 0001-demo\nstatus: {status}\nblocked_by: {blockers}\n{extra}---\n\n## 給使用者（zh-TW）\n測試\n')
        return p

    def test_frontier_and_global_next_id(self):
        self.ticket(7)
        self.assertEqual(verifier.check_tickets(self.root)['next_id'], 'T-0008')
        self.assertEqual(verifier.check_tickets(self.root)['frontier'], ['T-0007'])

    def test_blocking_is_derived(self):
        self.ticket(1, 'processing')
        self.ticket(2, blockers='[T-0001]')
        self.assertEqual(verifier.check_tickets(self.root)['blocked'], {'T-0002': ['T-0001']})

    def test_duplicate_id_across_epics_rejected(self):
        p = self.ticket()
        other = self.root / '.proj.tickets/0002-other/T-0001-other.md'
        other.parent.mkdir(parents=True)
        other.write_text(p.read_text().replace('0001-demo', '0002-other'))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            verifier.check_tickets(self.root)

    def test_missing_self_and_cycles_rejected(self):
        for blockers in ['[T-9999]', '[T-0001]']:
            with self.subTest(blockers=blockers):
                self.ticket(blockers=blockers)
                with self.assertRaises(ValueError): verifier.check_tickets(self.root)
        self.ticket(1, blockers='[T-0002]')
        self.ticket(2, blockers='[T-0001]')
        with self.assertRaisesRegex(ValueError, 'cycle'): verifier.check_tickets(self.root)

    def test_stored_blocked_and_unknown_status_rejected(self):
        for status in ['blocked', 'finished']:
            self.ticket(status=status)
            with self.assertRaises(ValueError): verifier.check_tickets(self.root)

    def test_pending_requires_reason_evidence_date_and_revisit(self):
        self.ticket(status='pending')
        with self.assertRaisesRegex(ValueError, 'pending'): verifier.check_tickets(self.root)
        (self.root / 'pause.md').write_text('Owner chose to pause.')
        self.ticket(status='pending', extra='pending_reason: waiting\npending_evidence: pause.md\npending_on: 2026-10-04\nrevisit_when: owner resumes\n')
        self.assertEqual(verifier.check_tickets(self.root)['paused'], ['T-0001'])

    def test_done_requires_real_landing_record(self):
        self.ticket(status='done', extra='landing_evidence: nonexistent.json\n')
        with self.assertRaisesRegex(ValueError, 'landing'): verifier.check_tickets(self.root)

    def test_stale_translation_and_missing_source_rejected(self):
        en = self.root / 'spec.en.md'
        zh = self.root / 'spec.zh-TW.md'
        en.write_text('Original')
        sha = verifier.git_blob(en.read_bytes())
        zh.write_text(f'---\nsynced_from: spec.en.md\nsynced_from_sha: {sha}\n---\n原文\n')
        verifier.check_translation(zh, self.root)
        en.write_text('Changed')
        with self.assertRaisesRegex(ValueError, 'stale'): verifier.check_translation(zh, self.root)
        en.unlink()
        with self.assertRaises(ValueError): verifier.check_translation(zh, self.root)

    def test_site_projection_rejects_tamper_missing_and_extra_product(self):
        import hashlib
        baseline = [{'path': 'docs/post/test.md', 'type': 'regular', 'sha256': hashlib.sha256(b'article').hexdigest()}]
        site = self.root / 'blog/post/test.md'
        site.parent.mkdir(parents=True)
        site.write_bytes(b'article')
        verifier.check_preserved(self.root, baseline, {})
        site.write_bytes(b'tamper')
        with self.assertRaises(ValueError): verifier.check_preserved(self.root, baseline, {})
        site.unlink()
        with self.assertRaises(ValueError): verifier.check_preserved(self.root, baseline, {})

    def test_unknown_product_addition_is_rejected(self):
        self.assertFalse(verifier.allowed_new('blog/extra.md'))
        self.assertFalse(verifier.allowed_new('scripts/surprise.ts'))
        self.assertFalse(verifier.allowed_new('package-lock.json'))

    def test_readme_pnpm_commands_must_exist_in_package_scripts(self):
        import json
        guard = getattr(verifier, 'check_readme_scripts', None)
        self.assertTrue(callable(guard), 'README commands need a package-script guard')
        (self.root / 'package.json').write_text(json.dumps({'scripts': {'docs:dev': 'vitepress dev blog', 'custom:check': 'echo checked'}}))
        readme = self.root / 'README.md'
        readme.write_text('```sh\npnpm install\npnpm docs:dev\n```\n| Check | `pnpm run custom:check` |\n')
        self.assertEqual(guard(self.root), ['custom:check', 'docs:dev'])
        for command in ['pnpm blog:dev', 'pnpm run typo:check']:
            with self.subTest(command=command):
                readme.write_text(f'```sh\n{command}\n```\n')
                with self.assertRaisesRegex(ValueError, 'README.*script'):
                    guard(self.root)

    def test_pass_evidence_requires_real_log_hash_and_exit(self):
        import hashlib
        log = self.root / 'check.log'
        log.write_bytes(b'actual execution')
        record = {'status': 'pass', 'exit_code': 0, 'log': 'check.log', 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest()}
        verifier.check_evidence(self.root, record)
        log.write_bytes(b'changed')
        with self.assertRaises(ValueError): verifier.check_evidence(self.root, record)
        record['exit_code'] = 1
        with self.assertRaises(ValueError): verifier.check_evidence(self.root, record)

    def test_trace_rejects_dangling_ac_ticket_source_and_false_pass(self):
        import hashlib, json
        source = self.root / 'openspec/specs/demo/spec.md'
        source.parent.mkdir(parents=True)
        source.write_text('Original requirement')
        specdir = self.root / '.proj.specs/0001-harness-adoption'
        specdir.mkdir(parents=True)
        rows = [{'row_id': f'row-{i:03}', 'source_path': 'openspec/specs/demo/spec.md', 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'source_git_blob': verifier.git_blob(source.read_bytes()), 'expected_behavior': 'Original requirement', 'heading': 'Requirement', 'AC': ['HA-01'], 'ticket': 'T-0001', 'evidence_status': 'not-run', 'actual_evidence': []} for i in range(113)]
        (specdir / 'baseline-traceability.json').write_text(json.dumps(rows))
        candidate = specdir / 'candidate-traceability.json'
        candidate.write_text(json.dumps(rows))
        verifier.check_trace(self.root, {'T-0001': {}})
        for key, value in [('AC', ['HA-99']), ('ticket', 'T-9999'), ('source_path', 'missing.md'), ('evidence_status', 'pass')]:
            with self.subTest(key=key):
                changed = json.loads(json.dumps(rows)); changed[0][key] = value
                candidate.write_text(json.dumps(changed))
                with self.assertRaises(ValueError): verifier.check_trace(self.root, {'T-0001': {}})


class AddedPathTests(unittest.TestCase):
    """Exercise the Git index as well as untracked files in a disposable repository."""
    def setUp(self):
        import json, subprocess
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        delta = json.loads((MODULE.parent.parent / 'maintenance/harness-adoption/candidate-delta.json').read_text())
        self.moved = {entry['candidate'] for entry in delta['site_moves']}
        self.assertEqual(len(self.moved), 55)
        self.baseline = {'README.md'}

    def file(self, name, staged=False):
        import subprocess
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('fixture bytes')
        if staged:
            subprocess.run(['git', 'add', '--', name], cwd=self.root, check=True, capture_output=True)

    def guard(self):
        guard = getattr(verifier, 'check_added_paths', None)
        self.assertTrue(callable(guard), 'new-file guard must inspect both index and untracked files')
        return guard(self.root, self.baseline, self.moved)

    def test_staged_unknown_product_is_rejected(self):
        self.file('blog/extra.md', staged=True)
        with self.assertRaisesRegex(ValueError, 'unknown added product file: blog/extra.md'):
            self.guard()

    def test_untracked_unknown_product_is_rejected(self):
        self.file('scripts/surprise.ts')
        with self.assertRaisesRegex(ValueError, 'unknown added product file: scripts/surprise.ts'):
            self.guard()

    def test_staged_approved_moves_baseline_and_management_are_accepted(self):
        for name in sorted(self.moved | self.baseline | {'docs/guide.md', '.proj.tickets/0001-demo/T-0001-demo.md', 'tests/harness_adoption/test_publication.py'}):
            self.file(name, staged=True)
        self.file('docs/agents/next-step.md')
        self.guard()


class TraceEvidenceTests(unittest.TestCase):
    """Use all 113 real historical rows with isolated source and execution records."""
    def setUp(self):
        import hashlib, json, shutil
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source_root = MODULE.parent.parent
        spec_name = '.proj.specs/0001-harness-adoption'
        specdir = self.root / spec_name
        specdir.mkdir(parents=True)
        shutil.copyfile(source_root / spec_name / 'baseline-traceability.json', specdir / 'baseline-traceability.json')
        self.rows = json.loads((source_root / spec_name / 'candidate-traceability.json').read_text())
        self.assertEqual(len(self.rows), 113)
        for name in {row['source_path'] for row in self.rows}:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_root / name, target)
        for row in self.rows:
            row['evidence_status'] = 'not-run'
            row['actual_evidence'] = []
        self.tickets = {row['ticket']: {} for row in self.rows}
        self.candidate = specdir / 'candidate-traceability.json'
        log = self.root / 'actual.log'
        log.write_bytes(b'actual successful execution\n')
        self.passed = {'status': 'pass', 'exit_code': 0, 'log': 'actual.log', 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest()}
        self.record('passed.json', self.passed)

    def record(self, name, data):
        import json
        (self.root / name).write_text(json.dumps(data))

    def guard(self):
        import json
        self.candidate.write_text(json.dumps(self.rows))
        return verifier.check_trace(self.root, self.tickets)

    def test_pass_trace_rejects_each_nonpass_record_and_mixed_evidence(self):
        self.assertEqual(self.guard(), 113)
        self.rows[0].update(evidence_status='pass', actual_evidence=['passed.json'])
        self.assertEqual(self.guard(), 113)
        for status in ('blocked', 'not-run', 'expected-red', 'existing-failure', 'new-regression'):
            for mixed in (False, True):
                with self.subTest(status=status, mixed=mixed):
                    self.record('nonpass.json', {'status': status})
                    self.rows[0]['actual_evidence'] = (['passed.json'] if mixed else []) + ['nonpass.json']
                    with self.assertRaisesRegex(ValueError, 'passed trace.*nonpass'):
                        self.guard()

    def test_trace_rejects_unknown_row_status(self):
        self.rows[0]['evidence_status'] = 'finished'
        with self.assertRaisesRegex(ValueError, 'trace.*status'):
            self.guard()

    def test_pass_trace_rejects_invalid_execution_receipt(self):
        self.rows[0].update(evidence_status='pass', actual_evidence=['passed.json'])
        for key, value in [('exit_code', 1), ('log_sha256', '0' * 64), ('log', 'missing.log')]:
            with self.subTest(key=key):
                self.record('passed.json', dict(self.passed, **{key: value}))
                with self.assertRaises(ValueError):
                    self.guard()


class FrameworkImportTests(unittest.TestCase):
    """Validate pinned framework bytes and native skill roots in real temp trees."""
    def setUp(self):
        import json, shutil
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source_root = MODULE.parent.parent
        self.manifest_name = 'maintenance/harness-adoption/framework-import-manifest.json'
        self.manifest = json.loads((self.source_root / self.manifest_name).read_text())
        for name in [self.manifest_name, *self.manifest['initialized_snapshot_files']]:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.source_root / name, target)
        for runtime in ('.agents', '.claude'):
            for product in ('phoenix-writing', 'maintaining-writing-skills', 'creating-vitepress-post', 'managing-article-publication'):
                name = f'{runtime}/skills/{product}/SKILL.md'
                target = self.root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(self.source_root / name, target)

    def guard(self):
        self.assertTrue(callable(getattr(verifier, 'check_framework', None)), 'framework manifest must have a real verification entrypoint')
        return verifier.check_framework(self.root)

    def test_pinned_framework_asset_tamper_is_rejected(self):
        result = self.guard()
        self.assertEqual(result['pinned_files'], 641)
        path = self.root / '.agents/skills/archify/assets/template.html'
        original = path.read_bytes()
        path.write_bytes(original + b'\n<!-- injected -->\n')
        with self.assertRaisesRegex(ValueError, 'framework.*SHA'):
            self.guard()

    def test_runtime_catalog_rejects_an_unknown_root_skill_in_each_runtime(self):
        for runtime in ('.agents', '.claude'):
            with self.subTest(runtime=runtime):
                path = self.root / runtime / 'skills/unapproved/SKILL.md'
                path.parent.mkdir()
                path.write_text('---\nname: unapproved\ndescription: must not be discovered\n---\n')
                try:
                    with self.assertRaisesRegex(ValueError, 'runtime skill roots'):
                        self.guard()
                finally:
                    path.unlink();path.parent.rmdir()

    def test_runtime_tree_rejects_unpinned_framework_files_and_nested_links(self):
        for runtime, product, kind in [('.agents', 'tdd', 'file'), ('.claude', 'tdd', 'link'), ('.agents', 'phoenix-writing', 'link'), ('.claude', 'tdd', 'directory-link')]:
            with self.subTest(runtime=runtime, product=product, kind=kind):
                path = self.root / runtime / 'skills' / product / 'unapproved'
                if kind == 'file':
                    path.write_text('unreviewed framework instruction')
                elif kind == 'directory-link':
                    path.symlink_to(self.root / '.agents/skills/tdd', target_is_directory=True)
                else:
                    path.symlink_to(self.root / '.agents/skills/tdd/SKILL.md')
                try:
                    with self.assertRaisesRegex(ValueError, 'unpinned framework file|runtime symlink'):
                        self.guard()
                finally:
                    path.unlink()

    def test_framework_provenance_and_manifest_repins_are_rejected(self):
        import hashlib, json
        path = self.root / self.manifest_name
        original = path.read_bytes()
        for field, value, message in [('source_commit', '0' * 40, 'template commit'), ('source_digest', '0' * 64, 'template digest'), ('new_tuning_executed', True, 'approved pins')]:
            with self.subTest(field=field):
                changed = json.loads(original);changed[field] = value
                path.write_text(json.dumps(changed))
                with self.assertRaisesRegex(ValueError, message):self.guard()
        modified = self.root / '.claude/skills/tdd/SKILL.md'
        modified.write_bytes(modified.read_bytes()+b'\nUnapproved change\n')
        changed = json.loads(original)
        changed['initialized_snapshot_files']['.claude/skills/tdd/SKILL.md'] = hashlib.sha256(modified.read_bytes()).hexdigest()
        path.write_text(json.dumps(changed))
        with self.assertRaisesRegex(ValueError, 'approved pins'):self.guard()
        changed = json.loads(original);del changed['initialized_snapshot_files']['.claude/skills/tdd/SKILL.md']
        path.write_text(json.dumps(changed))
        with self.assertRaisesRegex(ValueError, 'approved pins'):self.guard()

    def test_pinned_file_and_parent_symlinks_and_missing_file_are_rejected(self):
        import shutil
        path = self.root / '.agents/skills/tdd/SKILL.md'
        original = path.read_bytes();path.unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):self.guard()
        foreign = self.root / 'same-bytes.md';foreign.write_bytes(original);path.symlink_to(foreign)
        with self.assertRaisesRegex(ValueError, 'linked'):self.guard()
        path.unlink();path.write_bytes(original)
        parent = self.root / '.claude/skills/archify/assets';external = self.root / 'same-assets';parent.rename(external)
        parent.symlink_to(external,target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'linked'):self.guard()

    def test_catalog_rejects_missing_product_skill_and_same_count_replacement(self):
        import shutil
        path = self.root / '.agents/skills/phoenix-writing';path.rename(self.root / 'saved-product')
        with self.assertRaisesRegex(ValueError, 'runtime skill roots'):self.guard()
        replacement = self.root / '.agents/skills/unapproved';replacement.mkdir()
        (replacement / 'SKILL.md').write_text('Unknown despite still having 36 roots')
        with self.assertRaisesRegex(ValueError, 'runtime skill roots'):self.guard()
        shutil.rmtree(replacement);(self.root / 'saved-product').rename(path)
        (path / 'SKILL.md').unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):self.guard()

    def test_verified_catalog_reports_36_physical_skills_per_runtime(self):
        result = self.guard()
        self.assertEqual(result['runtime_skill_counts'], {'.agents':36, '.claude':36})
        self.assertEqual(result['source_commit'],'917e6025da0901a79dda016e1ce5bd89b6e6e19f')
        self.assertEqual(result['source_digest'],'b7782890459cf3c546395ac5546f22dc074f13d4166688751a9c1e08d4216bf5')


if __name__ == '__main__': unittest.main()
