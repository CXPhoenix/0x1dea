"""Finite workflow grants supplied independently by the trusted caller, never a candidate."""
import json
from pathlib import Path
import re


def add_arguments(parser):
    parser.add_argument('--workflow-admission', type=Path)
    parser.add_argument('--workflow-admission-sha256')
    parser.add_argument('--trusted-repository')
    parser.add_argument('--trusted-main')


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate workflow admission key')
        result[key] = value
    return result


def from_args(args, *roots):
    values = (args.workflow_admission, args.workflow_admission_sha256,
              args.trusted_repository, args.trusted_main)
    if not any(value is not None for value in values):
        return None
    if not all(values):
        raise ValueError('all independent workflow admission inputs are required')
    path = args.workflow_admission.absolute()
    for p in (path, *path.parents):
        if p.is_symlink() and (p.as_posix(), p.readlink().as_posix()) not in {
                ('/tmp', 'private/tmp'), ('/var', 'private/var')}:
            raise ValueError('linked workflow admission input')
    if any(path.resolve().is_relative_to(Path(root).resolve()) for root in roots):
        raise ValueError('workflow admission must be outside control and candidate')
    return WorkflowAdmission(path.resolve(), *values[1:])


def github_git_paths(control, ref):
    import publication_current as current
    # Include trees: Git can contain an empty tree or an uninitialized gitlink
    # that the physical file inventory cannot observe.
    paths = set()
    for record in current.git(control, 'ls-tree', '-rzt', ref, '--', '.github').split(b'\0'):
        if record:
            header, name = record.split(b'\t', 1)
            paths.add(name.decode())
    return paths


def admitted_git_paths(names):
    paths = set(names)
    for name in names:
        paths.update(str(parent) for parent in Path(name).parents if str(parent) != '.')
    return paths


def check_git_sources(root, workflows):
    import publication_current as current
    head = current.git(root, 'rev-parse', 'HEAD').decode().strip()
    # M0 projections intentionally overlay reviewed files onto immutable bases.
    # Any other real commit must contain exactly the admitted Git source set.
    expected = set() if head in current.BASES.values() else admitted_git_paths(workflows)
    if github_git_paths(root, head) != expected:
        raise ValueError('protected control/readback Git sources outside finite workflow admission')
    if head in current.BASES.values():
        return
    for name, entry in workflows.items():
        rows = current.git(root, 'ls-tree', '-z', head, '--', name).split(b'\0')
        if len(rows) != 2 or not rows[0]:
            raise ValueError('admitted workflow missing from control/readback Git tree')
        header, observed = rows[0].split(b'\t', 1)
        mode, kind, blob = header.decode().split()
        if (observed.decode() != name or kind != 'blob' or mode != entry['mode']
                or current.digest(current.git(root, 'cat-file', 'blob', blob)) != entry['sha256']):
            raise ValueError('admitted workflow control/readback Git identity mismatch')


class WorkflowAdmission:
    def __init__(self, path, expected_digest, repository, main):
        if (not re.fullmatch('[0-9a-f]{64}', expected_digest)
                or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository)
                or not re.fullmatch('[0-9a-f]{40}', main)):
            raise ValueError('invalid independently supplied workflow identity')
        self.path, self.expected_digest = path, expected_digest
        self.repository, self.main = repository, main

    def allowed(self, control):
        import publication_current as current
        if self.path.is_symlink() or not self.path.is_file():
            raise ValueError('workflow admission must remain a regular external file')
        raw = self.path.read_bytes()
        if current.digest(raw) != self.expected_digest:
            raise ValueError('workflow admission digest changed')
        grant = json.loads(raw, object_pairs_hook=unique_object)
        if (not isinstance(grant, dict) or set(grant) != {
                'version', 'repository', 'main', 'policies', 'roles', 'approval', 'workflows'}
                or type(grant['version']) is not int or grant['version'] != 1
                or grant['repository'] != self.repository or grant['main'] != self.main
                or grant['roles'] != ['main', 'staging']
                or not isinstance(grant['approval'], str) or not grant['approval'].strip()
                or not isinstance(grant['policies'], dict)
                or set(grant['policies']) != {'main', 'staging'}
                or not all(isinstance(v, str) and re.fullmatch('[0-9a-f]{64}', v)
                           for v in grant['policies'].values())
                or not isinstance(grant['workflows'], dict) or not grant['workflows']):
            raise ValueError('workflow admission authority/shape mismatch')
        role = current.target_role(control)
        if current.git(control, 'cat-file', '-t', self.main).strip() != b'commit':
            raise ValueError('workflow main pin is not a commit')
        head = current.git(control, 'rev-parse', 'HEAD').decode().strip()
        if current.git(control, 'rev-parse', 'refs/heads/main').decode().strip() != self.main:
            raise ValueError('trusted workflow main ref drifted')
        if head in current.BASES.values():
            observed = current.git(control, 'rev-parse', 'refs/publication/workflow-main').decode().strip()
            if observed != self.main:
                raise ValueError('projected workflow main changed')
        elif role == 'main':
            if head != self.main:
                raise ValueError('trusted workflow main drifted')
        else:
            current.git(control, 'merge-base', '--is-ancestor', self.main, 'HEAD')
        policy = current.regular(control, current.POLICY).read_bytes()
        if (current.digest(policy) != grant['policies'][role]
                or current.digest(current.git(control, 'show', self.main+':'+current.POLICY))
                != grant['policies']['main']):
            raise ValueError('workflow control policy drifted')
        common = json.loads(policy)['common']
        if github_git_paths(control, self.main) != admitted_git_paths(grant['workflows']):
            raise ValueError('protected trusted-main Git sources outside finite workflow admission')
        for name, entry in grant['workflows'].items():
            if (not re.fullmatch(r'\.github/workflows/[A-Za-z0-9][A-Za-z0-9_.-]*\.(?:yml|yaml)', name)
                    or not isinstance(entry, dict) or set(entry) != {'mode', 'sha256'}
                    or entry['mode'] not in {'100644', '100755'}
                    or not isinstance(entry['sha256'], str)
                    or not re.fullmatch('[0-9a-f]{64}', entry['sha256'])
                    or common.get(name) != entry):
                raise ValueError('invalid exact workflow admission entry')
            listing = current.git(control, 'ls-tree', '-z', self.main, '--', name).split(b'\0')
            if len(listing) != 2 or not listing[0]:
                raise ValueError('workflow absent from admitted trusted main')
            header, observed_name = listing[0].split(b'\t', 1)
            mode, kind, blob = header.decode().split()
            if (observed_name.decode() != name or kind != 'blob' or mode != entry['mode']
                    or current.digest(current.git(control, 'cat-file', 'blob', blob)) != entry['sha256']
                    or current.current_identity(control, name, entry) != entry):
                raise ValueError('workflow trusted-main identity mismatch')
        check_git_sources(control, grant['workflows'])
        return grant['workflows']
