#!/usr/bin/env python3
"""M0 inventory, local engineering projections and exact verification; no publication authority."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


def git(root, *args):
    return subprocess.check_output(
        ['git', '--no-replace-objects', '--literal-pathspecs', '-C', str(root), *args], stderr=subprocess.PIPE,
    )


def tree(root, commit):
    result = {}
    for entry in git(root, 'ls-tree', '-rz', '--full-tree', commit).split(b'\0'):
        if entry:
            header, path = entry.split(b'\t', 1)
            mode, kind, blob = header.decode().split()
            result[path.decode()] = {'mode': mode, 'type': kind, 'blob': blob}
    return result


CATEGORIES = {'published', 'candidate', 'engineering', 'historical-management',
              'current-management', 'target-role'}


def full_commit(root, value):
    if not isinstance(value, str) or not re.fullmatch(r'[0-9a-f]{40}', value):
        raise ValueError('pins must be full commit ids')
    if git(root, 'cat-file', '-t', value).strip() != b'commit':
        raise ValueError('pin is not a commit')


def validate(root, plan):
    if git(root, 'for-each-ref', '--format=%(refname)', 'refs/replace').strip():
        raise ValueError('replacement refs are not allowed')
    grafts = Path(git(root, 'rev-parse', '--path-format=absolute', '--git-path', 'info/grafts').decode().strip())
    if grafts.exists() and grafts.read_bytes().strip():
        raise ValueError('history grafts are not allowed')
    if git(root, 'rev-parse', '--is-shallow-repository').strip() != b'false':
        raise ValueError('complete Git history is required')
    if not isinstance(plan, dict) or set(plan) != {
        'schema_version', 'main', 'staging', 'classifications', 'candidates', 'prerequisites',
    } or type(plan['schema_version']) is not int or plan['schema_version'] != 1:
        raise ValueError('unsupported classification schema; trust/role input is not accepted')
    full_commit(root, plan['main'])
    full_commit(root, plan['staging'])
    if not isinstance(plan['classifications'], dict):
        raise ValueError('classification must be an exact path map')
    for path, item in plan['classifications'].items():
        if not isinstance(item, dict) or not {'category', 'owner'} <= item.keys() <= {
            'category', 'owner', 'shared',
        } or item['category'] not in CATEGORIES or not isinstance(item['owner'], str) or not item['owner']:
            raise ValueError(f'invalid classification: {path}')
        if 'shared' in item and type(item['shared']) is not bool:
            raise ValueError(f'invalid shared classification: {path}')
    if not isinstance(plan['candidates'], list) or not isinstance(plan['prerequisites'], list):
        raise ValueError('candidate and prerequisite registries must be lists')
    for item in plan['candidates']:
        if not isinstance(item, dict) or set(item) != {'id', 'paths', 'provenance'} or not isinstance(item['id'], str) or not item['id']:
            raise ValueError('invalid candidate ownership record')
        if not isinstance(item['paths'], list) or not all(isinstance(p, str) for p in item['paths']):
            raise ValueError('invalid candidate ownership paths')
        if item['provenance'] != 'legacy-requires-migration':
            raise ValueError('this proposal does not admit clean candidate provenance')
    for item in plan['prerequisites']:
        if not isinstance(item, dict) or set(item) != {'pr', 'state', 'target', 'merge_commit', 'head'}:
            raise ValueError('invalid prerequisite observation')
        if type(item['pr']) is not int or item['pr'] <= 0 or item['state'] not in {'OPEN', 'CLOSED', 'MERGED'} or item['target'] not in {'main', 'staging'}:
            raise ValueError('invalid prerequisite observation values')
        full_commit(root, item['head'])
        if item['merge_commit'] is not None:
            full_commit(root, item['merge_commit'])


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def inventory(root, plan):
    validate(root, plan)
    main, stage = plan['main'], plan['staging']
    trees = {'main': tree(root, main), 'staging': tree(root, stage)}
    changed = {p for p in trees['main'].keys() | trees['staging'].keys()
               if trees['main'].get(p) != trees['staging'].get(p)}
    if set(plan['classifications']) != changed:
        raise ValueError('classification must account for exactly every changed path')
    owners = {}
    ids = set()
    for candidate in plan['candidates']:
        if candidate['id'] in ids or not candidate['paths']:
            raise ValueError('candidate ownership needs unique ids and nonempty paths')
        ids.add(candidate['id'])
        for path in candidate['paths']:
            if path in owners or path not in trees['main'].keys() | trees['staging'].keys():
                raise ValueError(f'ambiguous or missing candidate ownership: {path}')
            owners[path] = candidate['id']
    for path in changed:
        item = plan['classifications'][path]
        if item['category'] == 'candidate':
            if owners.get(path) != item['owner']:
                raise ValueError(f'incomplete candidate ownership: {path}')
        elif path in owners:
            raise ValueError(f'candidate ownership contradicts classification: {path}')
    delta = []
    for path in sorted(trees['main'].keys() | trees['staging'].keys()):
        before, after = trees['main'].get(path), trees['staging'].get(path)
        if before == after:
            continue
        classification = plan['classifications'][path]
        candidate = classification['category'] == 'candidate'
        patch = None
        if classification.get('shared'):
            patch = git(root, 'diff', '--no-ext-diff', '--no-textconv', '--no-renames',
                        '--binary', '--full-index', main, stage, '--', path).decode()
        delta.append({
            'path': path, **classification, 'main': before, 'staging': after, 'patch': patch,
            'main_action': 'retain-published' if candidate else 'pending-exact-review',
            'staging_action': 'preserve-exact',
        })
    prerequisites = []
    for item in plan['prerequisites']:
        merge = item['merge_commit']
        landed = False
        if item['state'] == 'MERGED' and merge:
            target = {'main': main, 'staging': stage}[item['target']]
            status = subprocess.run(
                ['git', '--no-replace-objects', '-C', str(root),
                 'merge-base', '--is-ancestor', merge, target], capture_output=True,
            ).returncode
            if status not in (0, 1):
                raise ValueError('unavailable prerequisite ancestry')
            landed = status == 0
        prerequisites.append({**item, 'landed_by_observation_and_ancestry': landed})
    return {
        'schema_version': 1, 'status': 'proposal-only', 'trusted_policy': False,
        'repository': git(root, 'config', '--get', 'remote.origin.url').decode().strip(),
        'pins': {'main': main, 'staging': stage}, 'trees': trees, 'delta': delta,
        'candidates': plan['candidates'], 'prerequisites': prerequisites,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    command = commands.add_parser('inventory', help='Print a complete proposed M0 as JSON')
    command.add_argument('--repo', type=Path, required=True)
    command.add_argument('--classification', type=Path, required=True)
    prepare_parser = commands.add_parser('prepare', help='Prepare local engineering-only main/staging projections')
    prepare_parser.add_argument('--output', type=Path, required=True)
    verify_parser = commands.add_parser('verify', help='Verify candidate using the executing trusted target checkout')
    verify_parser.add_argument('--repo', type=Path, required=True)
    from publication_workflows import add_arguments, from_args
    for command_parser in (prepare_parser, verify_parser):
        add_arguments(command_parser)
    args = parser.parse_args()
    try:
        if args.command == 'verify':
            from publication_current import verify
            control = Path(__file__).resolve().parents[1]
            print(json.dumps(verify(control, args.repo.resolve(),
                                   workflow_admission=from_args(args, control, args.repo)), indent=2))
            return 0
        if args.command == 'prepare':
            from publication_current import prepare
            control = Path(__file__).resolve().parents[1]
            print(json.dumps(prepare(control, args.output,
                                    workflow_admission=from_args(args, control)), indent=2))
            return 0
        plan = json.loads(args.classification.read_text(), object_pairs_hook=unique_object)
        print(json.dumps(inventory(args.repo, plan), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        print(f'Blocked inventory: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
