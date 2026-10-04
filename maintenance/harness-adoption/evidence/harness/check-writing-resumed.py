#!/usr/bin/env python3
"""Read-only mechanical verification of nine completed isolated writing cases.

Only this script's --freeze option writes evidence/resumed/writing-runtime-freeze.json.
No writer, judge, runtime, canonical source, or historical evaluation is mutated.
Semantic scoring remains the responsibility of the saved independent judges.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT / 'implementation-resumed'
EVIDENCE = ROOT / 'evidence/resumed'
HISTORICAL = CANDIDATE / 'maintenance/writing-skills/behavior-eval-20261004/full-regression-v22/cases'
POLICY = CANDIDATE / 'maintenance/harness-adoption/runtime-source-policy.json'
MANIFEST = CANDIDATE / 'maintenance/harness-adoption/generated-writing-manifest.json'
checks = []
observations = {}
cases = []


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return path.read_bytes()


def load(path):
    return json.loads(read(path))


def utc(timestamp):
    return dt.datetime.fromtimestamp(timestamp, dt.timezone.utc).isoformat()


def record(path):
    data = read(path)
    s = path.stat()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(data),
            'bytes': len(data), 'filesystem_mtime_utc': utc(s.st_mtime),
            'filesystem_birthtime_utc': utc(s.st_birthtime) if hasattr(s, 'st_birthtime') else None}


def check(name, passed, **details):
    checks.append({'check': name, 'passed': bool(passed), **details})


def han(text):
    # Unicode ideographs, excluding punctuation, digits, Latin letters, whitespace.
    return sum(unicodedata.name(c, '').startswith('CJK UNIFIED IDEOGRAPH-')
               or unicodedata.name(c, '').startswith('CJK COMPATIBILITY IDEOGRAPH-') for c in text)


def paragraphs(text):
    return [p for p in re.split(r'\n\s*\n', text.strip()) if p]


def no_markdown_scaffold(text):
    return not re.search(r'(?m)^\s*(?:#{1,6}\s|```|[-*+]\s|\d+[.)]\s|>)', text)


def count_check(case, label, text, lower, upper):
    n = han(text)
    check(f'{case}.{label}.Han_count', lower <= n <= upper, actual=n, minimum=lower, maximum=upper)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze', action='store_true')
    args = parser.parse_args()
    observed_at = dt.datetime.now(dt.timezone.utc).isoformat()
    policy, manifest = load(POLICY), load(MANIFEST)
    check('manifest.policy_hash', manifest['source_policy_sha256'] == sha(read(POLICY)))
    source_records = []
    for entry in policy['inputs']:
        path = CANDIDATE / entry['path']
        check('source_policy.input.' + entry['path'], sha(read(path)) == entry['sha256'])
        source_records.append(record(path))
    canonical_files = {p.relative_to(CANDIDATE).as_posix()
                       for name in policy['skills']
                       for p in (CANDIDATE / 'skills' / name).rglob('*') if p.is_file()}
    policy_skill_files = {e['path'] for e in policy['inputs'] if e['path'].startswith('skills/')}
    check('source_policy.exact_canonical_three_tree_file_set', canonical_files == policy_skill_files,
          actual_files=len(canonical_files), missing=sorted(policy_skill_files-canonical_files),
          extra=sorted(canonical_files-policy_skill_files))
    alias_records = []
    for entry in policy['aliases']:
        path = CANDIDATE / entry['path']
        literal = path.readlink().as_posix() if path.is_symlink() else None
        check('source_policy.alias.' + entry['path'], literal == entry['literal_target']
              and sha(literal.encode()) == entry['literal_sha256'] if literal else False)
        alias_records.append({'path': path.relative_to(ROOT).as_posix(),
                              'literal_target': literal, 'literal_sha256': sha(literal.encode()) if literal else None,
                              'backing_root': entry['backing_root']})
    generated = {x['path']: x['sha256'] for x in manifest['files']}
    generated_records = []
    for entry in manifest['files']:
        path = CANDIDATE / entry['path']
        check('generated.current.' + entry['path'], sha(read(path)) == entry['sha256'])
        if 'source_sha256' in entry:
            check('generated.source.' + entry['path'], sha(read(CANDIDATE / entry['source'])) == entry['source_sha256'])
        generated_records.append(record(path))

    for i in range(1, 10):
        case = f'E{i}'
        writer = ROOT / 'writing-resumed' / case
        judge = ROOT / f'judges-resumed/group-{(i-1)//3+1}' / case
        context_path = EVIDENCE / f'writer-{case}-context.json'
        context = load(context_path)
        inp, out = load(writer / 'input.json'), read(writer / 'output.md').decode('utf-8')
        item = {'id': case, 'writer_context': record(context_path),
                'writer_input': record(writer / 'input.json'), 'writer_output': record(writer / 'output.md'),
                'writer_minimal_agents': record(writer / 'AGENTS.md'),
                'canonical_input': record(HISTORICAL / case / 'input.json'),
                'canonical_rubric': record(HISTORICAL / case / 'rubric.json'),
                'judge_input': record(judge / 'input.json'), 'judge_output': record(judge / 'output.md'),
                'judge_rubric': record(judge / 'rubric.json'), 'isolated_runtime_records': []}
        check(f'{case}.writer_input.canonical_bytes', read(writer / 'input.json') == read(HISTORICAL / case / 'input.json'))
        check(f'{case}.judge_input.canonical_bytes', read(judge / 'input.json') == read(HISTORICAL / case / 'input.json'))
        check(f'{case}.judge_rubric.canonical_bytes', read(judge / 'rubric.json') == read(HISTORICAL / case / 'rubric.json'))
        check(f'{case}.judge_output.writer_bytes', read(judge / 'output.md') == read(writer / 'output.md'))
        listed = {x['path']: x['sha256'] for x in context['files']}
        current = {p.relative_to(writer).as_posix() for p in writer.rglob('*') if p.is_file() and p.name != 'output.md'}
        check(f'{case}.context.exact_file_set', current == set(listed), missing=sorted(set(listed)-current), extra=sorted(current-set(listed)))
        check(f'{case}.context.generated_manifest_set', set(listed) == set(generated) | {'AGENTS.md', 'input.json'})
        check(f'{case}.context.no_supplied_rubric_or_old_answers_attestation', context.get('rubric_provided') is False and context.get('old_answers_provided') is False,
              limitation='Saved manifest attestations and directory inventory; not a proof of all agent reads.')
        for rel, expected in listed.items():
            path = writer / rel
            check(f'{case}.context.unchanged.{rel}', sha(read(path)) == expected)
            if rel in generated:
                check(f'{case}.runtime.generated_bytes.{rel}', read(path) == read(CANDIDATE / rel))
            item['isolated_runtime_records'].append(record(path))
        cs, os = context_path.stat(), (writer / 'output.md').stat()
        check(f'{case}.filesystem_context_mtime_before_output_birthtime', cs.st_mtime < getattr(os, 'st_birthtime', os.st_mtime),
              context_mtime_utc=utc(cs.st_mtime), output_birthtime_utc=utc(os.st_birthtime) if hasattr(os, 'st_birthtime') else None,
              limitation='Mutable filesystem metadata observed now; output timestamps date parent serialization, not native response completion.')
        item['context_embedded_timestamp_fields'] = {k:v for k,v in context.items() if ('time' in k or '_at' in k) and k != 'files'}
        if i == 1:
            count_check(case, 'body', out, 180, 320)
            check(f'{case}.paragraph_only', len(paragraphs(out)) == 1 and no_markdown_scaffold(out))
        elif i == 2:
            original = inp['materials']['article'].encode()
            allowed = '同一份資料也可能已經改變。失效策略要讓它失效，所以我們必須設計失效策略。'.encode()
            pre, post = original.split(allowed)
            output = read(writer / 'output.md')
            replacement = output[len(pre):len(output)-len(post)] if output.startswith(pre) and output.endswith(post) else b''
            check(f'{case}.protected_prefix_byte_exact', output.startswith(pre), protected_sha256=sha(pre), bytes=len(pre))
            check(f'{case}.protected_suffix_byte_exact', output.endswith(post), protected_sha256=sha(post), bytes=len(post))
            check(f'{case}.only_two_authorized_sentences', bool(replacement) and replacement.count('。'.encode()) == 2 and b'\n' not in replacement,
                  authorized_original_sha256=sha(allowed), replacement_sha256=sha(replacement), replacement=replacement.decode(errors='replace'))
            check(f'{case}.paragraph_layout_unchanged', len(paragraphs(out)) == len(paragraphs(original.decode())))
        elif i == 3:
            check(f'{case}.English_word_count', len(out.split()) <= 80, whitespace_word_count=len(out.split()))
            check(f'{case}.paragraph_only_no_questions_Han_or_emoticons', len(paragraphs(out)) == 1 and no_markdown_scaffold(out)
                  and not re.search(r'[?？]|[:;=8][-^]?[)D(Pp/\\]|[\U0001f300-\U0001faff]', out) and han(out) == 0)
        elif i == 4:
            lines = out.strip().splitlines()
            check(f'{case}.three_formal_lines', len(lines) == 3 and all(line.startswith(prefix) for line,prefix in zip(lines, ['主旨：','說明：','擬辦：'])))
        elif i == 5:
            m = re.fullmatch(r'```python\n(.*?)```\n?', out, re.S)
            check(f'{case}.only_python_fence', m is not None)
            code = m.group(1) if m else ''
            expected = inp['materials']['code'].replace('def add(a, b)\n', 'def add(a, b):\n', 1)
            check(f'{case}.only_colon_added_byte_exact', code.encode() == expected.encode())
            try:
                compile(code, '<E5 fresh output>', 'exec')
                compiled = True
            except SyntaxError:
                compiled = False
            check(f'{case}.Python_compile', compiled)
        elif i == 6:
            ps = paragraphs(out)
            count_check(case, 'body', ps[0], 120, 220)
            count_check(case, 'body_plus_gap', out, 120, 220)
            check(f'{case}.body_and_separate_one_line_gap', len(ps) == 2 and '\n' not in ps[1] and ps[1].startswith('結論缺口：') and no_markdown_scaffold(ps[0]))
        elif i == 7:
            ps = paragraphs(out)
            count_check(case, 'body', ps[0], 150, 260)
            count_check(case, 'body_plus_caption', out, 150, 260)
            check(f'{case}.body_and_one_line_caption', len(ps) == 2 and no_markdown_scaffold(ps[0]) and ps[1].startswith('圖說：') and '\n' not in ps[1])
        elif i == 8:
            m = re.fullmatch(r'A\n\n(.*?)\n\nB\n\n(.*?)\n?', out, re.S)
            check(f'{case}.only_A_B_labels', m is not None and re.findall(r'(?m)^[A-Z]$', out) == ['A', 'B'] and no_markdown_scaffold(out))
            if m:
                count_check(case, 'A', m.group(1), 50, 90)
                count_check(case, 'B', m.group(2), 180, 300)
        elif i == 9:
            ps = paragraphs(out)
            count_check(case, 'whole_artifact', out, 80, 160)
            check(f'{case}.two_numbered_steps_one_line_caption', len(ps) == 3 and all('\n' not in x for x in ps)
                  and ps[0].startswith('1. ') and ps[1].startswith('2. ') and ps[2].startswith('圖說：')
                  and '先找出' in ps[0] and '再對照' in ps[1])
        cases.append(item)

    judge_records = []
    judged_cases = []
    for group in range(1, 4):
        report_path = EVIDENCE / f'writing-judge-group-{group}.json'
        provenance_path = EVIDENCE / f'writing-judge-group-{group}-provenance.json'
        report, provenance = load(report_path), load(provenance_path)
        results = report.get('results', report.get('cases', []))
        for result in results:
            scores = [d['score'] for d in result['dimensions']]
            check(result['id'] + '.saved_independent_judge.strict_threshold', len(scores) == 5 and scores == [2]*5
                  and result['total'] == sum(scores) == 10 and result['hard_failures'] == []
                  and result.get('verdict', 'pass') == 'pass',
                  scores=scores, total=result['total'], hard_failures=result['hard_failures'])
            judged_cases.append(result['id'])
        events = provenance.get('read_files', provenance.get('files', [])) + provenance.get('verification_read_events', [])
        for event in events:
            path = Path(event['path'])
            check(f'judge{group}.provenance_current_bytes.' + path.relative_to(ROOT).as_posix(), sha(read(path)) == event['sha256'])
        judge_records.append({'group': group, 'report': record(report_path), 'provenance': record(provenance_path),
                              'canonical_task_name': provenance.get('canonical_task', provenance.get('canonical_task_name')),
                              'judged_at_utc': report.get('judged_at_utc'),
                              'recorded_at_utc': provenance.get('recorded_at_utc', provenance.get('recorded_at')),
                              'timestamp_meaning': 'fresh judge run' if group == 1 else 'preservation time of completed report; original judging timestamp unavailable'})
    check('judge.coverage_exactly_E1_E9', sorted(judged_cases) == [f'E{i}' for i in range(1,10)])
    gaps = [
        'Writer context JSON has no embedded creation timestamp. Saved current filesystem birthtime/mtime precedes output file birthtime; these are mutable metadata, not an immutable historical freeze.',
        'Output.md files are parent serialization of completed native responses with a final newline. File birthtime is not native response completion time; original response API JSON is not persisted here.',
        'Native dispatch fork_turns=none and inherited model/no overrides is a parent-supplied attestation; conversation tool receipts are not copied as raw API JSON.',
        'Judge groups 2 and 3 preservation timestamps are not original judging timestamps. Group 1 is a fresh rejudge because the old report was not available in the live agent; writers were not rerun according to parent attestation.',
        'One group-1 self-provenance read has null read_at_utc as disclosed in its record; its reconstructed historical hash is not treated as a directly observed current-file hash.',
        'File contents, directory inventories and hashes cannot prove that an agent never called a tool or read an unlisted file. No such claim is made.',
        'The saved manifest generator_sha256 is recorded metadata only; the generator script is outside this verification read scope. API 400 attempts are not claimed successful and native catalog verification belongs to separate evidence.'
    ]
    result = {'name': 'fresh-writing-mechanical-final', 'observed_at_utc': observed_at,
              'scope': 'Mechanical checks only; no semantic rescoring; no source/writer/judge mutation or network/install.',
              'check_count': len(checks), 'passed': sum(c['passed'] for c in checks),
              'failed': sum(not c['passed'] for c in checks), 'checks': checks, 'evidence_gaps': gaps}
    if args.freeze:
        destination = EVIDENCE / 'writing-runtime-freeze.json'
        if destination.exists():
            raise SystemExit('Refusing to replace an existing freeze; choose a separate new snapshot intentionally.')
        freeze = {'schema_version': 1, 'recorded_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                  'record_type': 'current post-run portable hash snapshot; not a backdated pre-run freeze',
                  'path_base': 'workspace root; all file paths relative for portability',
                  'mechanical_result': result, 'source_policy': record(POLICY), 'generated_manifest': record(MANIFEST),
                  'canonical_source_records': source_records, 'canonical_alias_records': alias_records,
                  'current_generated_runtime_records': generated_records, 'writer_cases': cases, 'judges': judge_records,
                  'native_collaboration': {
                      'writer_canonical_task_names': [f'/root/writing_e{i}' for i in range(1,10)],
                      'judge_canonical_task_names': [j['canonical_task_name'] for j in judge_records],
                      'writer_fork_turns': 'none', 'model': 'inherited from parent',
                      'model_override': None, 'reasoning_effort_override': None,
                      'evidence_type': 'parent-supplied dispatch attestation; host collaboration task names; tool receipts reside conversation',
                      'writer_first_outputs_completed': True, 'writer_rewrite_or_rerun': False,
                      'group_1_rejudge': True, 'raw_dispatch_api_json_persisted': False},
                  'checker': record(Path(__file__)), 'runner': record(ROOT / 'run-check-resumed.py')}
        destination.write_text(json.dumps(freeze, ensure_ascii=False, indent=2) + '\n')
        result['freeze_path'] = destination.relative_to(ROOT).as_posix()
        result['freeze_sha256'] = sha(read(destination))
    # Full failures plus the useful measured constraints, avoiding thousands of repetitive lines.
    print(json.dumps({k:v for k,v in result.items() if k != 'checks'}, ensure_ascii=False, indent=2))
    for item in checks:
        if not item['passed'] or '.Han_count' in item['check'] or item['check'].endswith('English_word_count'):
            print(json.dumps(item, ensure_ascii=False))
    return 1 if result['failed'] else 0


if __name__ == '__main__':
    sys.exit(main())
