"""Shared, exact M0 successor; callers execute this from the trusted control checkout."""
import hashlib
from importlib.util import module_from_spec, spec_from_file_location
import json
import os
from pathlib import Path
import shutil
import subprocess

MAIN = 'eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a'
STAGING = 'c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7'
BASES = {'main': MAIN, 'staging': STAGING}
POLICY = 'maintenance/publication-workflow/engineering-v1.json'
M0 = '.proj.specs/0012-publication-workflow/implementation/T-0013/M0-inventory.proposed.json'
M0_SHA = '6d95e0c7036fef827ce3c4c7b97beae811597e908d755837cce4431b526ea89a'


# Finite, reviewed metadata successors; historical M0 blobs remain immutable.
CLOSEOUT_SUCCESSORS = {'.proj.specs/0011-main-to-staging-sync/coverage-report.md': 'd610282c67b42bad42d78e4e3d6857c0311fc364c69f41239309c03e06997121',
 '.proj.tickets/0001-harness-adoption/T-0001-harness-adoption.md': '5465e347c083e87ac5146c65c7fef4a1d6a25c55ffde1acbd4130490493d3799',
 '.proj.tickets/0002-article-publication/T-0002-article-publication-preparation.md': '9edef29e54074191f930cd4619b4becdc843ae345dc3d68780615a89cea71b3f',
 '.proj.tickets/0010-main-verification-repair/T-0010-main-verification-repair.md': '9e7d02cdea898061f5e1e91dd66392e81813623eab4531c7069306942e4eeaf4',
 '.proj.tickets/0011-main-to-staging-sync/T-0011-main-to-staging-sync.md': '21ceaea9edad9a52874d8d1b3112dd8afc37d2d1a1fce0c55c5d6419cc3a7125'}
CLOSEOUT_RECEIPTS = {'.proj.specs/0001-harness-adoption/landing-approval.md': 'b7e332f00d749f628ddfdcaf22c544c97944418c5f43a6e21177f675deef5b28',
 '.proj.specs/0001-harness-adoption/landing.json': 'b08e7e97a9ac61a81bd762018237ada0e9e821603720f668c6d980b032f0395b',
 '.proj.specs/0010-main-verification-repair/landing-approval.md': '8245a7aa22aa30c12f2dd1f6a55e1a18323bee98573b385e93f11cef8a2b05a8',
 '.proj.specs/0010-main-verification-repair/landing.json': '192e4976b96fc496767eaa7f43ce4b271211b89b0155a5eef5aded7273ce956a',
 '.proj.specs/0010-main-verification-repair/ticket-closeout/current-main/T-0002-landing-approval.md': '8150d99bf9c9b320ea4511c66176725eed6ff351a374e1ba7e8f5167ce24b444',
 '.proj.specs/0010-main-verification-repair/ticket-closeout/current-main/T-0002-landing.json': '26733b306005a09a713b7a0a6865fb4bf57400605ee34273512f936392b002a9',
 '.proj.specs/0011-main-to-staging-sync/landing-approval.md': 'e4c721dcbb228a18bab5728276ebe2b5f2fac660381944ee9725d8b14d754ac0',
 '.proj.specs/0011-main-to-staging-sync/landing.json': '57d798306754b5b6ec250274f87455d983e176e442defbd75ec3b32192a598ac'}

def git_environment(*, local_clone=False):
    env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull,
                'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_NO_LAZY_FETCH': '1',
                'GIT_ALLOW_PROTOCOL': 'file' if local_clone else '', 'GIT_TERMINAL_PROMPT': '0'})
    return env


def git(root, *args):
    return subprocess.check_output(['git', '--no-replace-objects', '--literal-pathspecs', '-C', str(root), *args],
                                   stderr=subprocess.PIPE, env=git_environment())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def regular(root, name):
    path = Path(name)
    if path.is_absolute() or '..' in path.parts or not name or path.as_posix() != name:
        raise ValueError('unsafe successor path: ' + name)
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ValueError('linked successor path: ' + name)
    if not current.is_file():
        raise ValueError('missing successor path: ' + name)
    return current


def policy(control):
    data = json.loads(regular(control, POLICY).read_text())
    if set(data) != {'version', 'bases', 'm0_sha256', 'scope', 'common'} or type(data['version']) is not int or data['version'] != 1 or data['bases'] != BASES or data['m0_sha256'] != M0_SHA:
        raise ValueError('unapproved M0 successor pins')
    raw = regular(control, M0).read_bytes()
    if digest(raw) != M0_SHA:
        raise ValueError('changed approved M0 inventory')
    inventory = json.loads(raw)
    protected_history = {'maintenance/harness-adoption/baseline-files.json',
                         'maintenance/harness-adoption/candidate-delta.json',
                         'maintenance/harness-adoption/framework-import-manifest.json',
                         'maintenance/article-publication/source-boundary.json',
                         'maintenance/lint-cleanup/source-boundary.json'}
    owned = {p for c in inventory['candidates'] for p in c['paths']}
    if not isinstance(data['common'], dict):
        raise ValueError('exact common successor must be a path map')
    for name, sha256 in (CLOSEOUT_SUCCESSORS | CLOSEOUT_RECEIPTS).items():
        if data['common'].get(name) != {'mode': '100644', 'sha256': sha256}:
            raise ValueError('unapproved exact closeout identity: ' + name)
        path = regular(control, name)
        if path.stat().st_mode & 0o111 or digest(path.read_bytes()) != sha256:
            raise ValueError('changed exact closeout identity: ' + name)
    writing = ('phoenix-writing', 'maintaining-writing-skills', 'creating-vitepress-post')
    for name, expected in data['common'].items():
        regular(control, name)
        if name in owned or name in protected_history or name.startswith(('blog/', '.github/')) or any(name.startswith(prefix + package + '/') for prefix in ('skills/', '.agents/skills/', '.claude/skills/') for package in writing):
            raise ValueError('protected content/history in common successor: ' + name)
        if set(expected) != {'mode', 'sha256'} or expected['mode'] not in {'100644', '100755'} or not isinstance(expected['sha256'], str) or len(expected['sha256']) != 64 or any(c not in '0123456789abcdef' for c in expected['sha256']):
            raise ValueError('invalid exact common identity: ' + name)
        if name != 'scripts/verify-harness-adoption.py' and name not in CLOSEOUT_SUCCESSORS:
            for entries in inventory['trees'].values():
                previous = entries.get(name)
                if previous and expected != {'mode': previous['mode'], 'sha256': digest(git(control, 'cat-file', 'blob', previous['blob']))}:
                    raise ValueError('unapproved existing engineering replacement: ' + name)
    return data, inventory


def prepare(control, output):
    check_history(control)
    data, inventory = policy(control)
    output = output.absolute()
    if output.exists() or output.is_symlink() or output.resolve().is_relative_to(control.resolve()):
        raise ValueError('output must be new and outside the control checkout')
    for parent in output.parents:
        if parent.is_symlink() and (parent.as_posix(), parent.readlink().as_posix()) not in {('/var', 'private/var'), ('/tmp', 'private/tmp')}:
            raise ValueError('linked projection output parent')
    output = output.resolve()
    owned = {p for c in inventory['candidates'] for p in c['paths']}
    for name, expected in data['common'].items():
        if name in owned or name.startswith(('blog/', '.github/')):
            raise ValueError('candidate/deployment path in engineering projection: ' + name)
        path = regular(control, name)
        mode = '100755' if path.stat().st_mode & 0o100 else '100644'
        if {'mode': mode, 'sha256': digest(path.read_bytes())} != expected:
            raise ValueError('changed exact engineering successor: ' + name)
    output.mkdir(parents=True)
    try:
        for role, base in BASES.items():
            target = output / role
            subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--template=', str(control), str(target)],
                           check=True, capture_output=True, env=git_environment(local_clone=True))
            git(target, 'checkout', '--detach', base)
            for target_role_name, target_pin in BASES.items():
                git(target, 'update-ref', 'refs/heads/' + target_role_name, target_pin)
            for name in data['common']:
                target_path = target / name
                target_path.parent.mkdir(parents=True, exist_ok=True)
                regular(control, name)  # Input has been checked against the exact record.
                if target_path.is_symlink():
                    raise ValueError('linked projection replacement: ' + name)
                shutil.copyfile(control / name, target_path)
                target_path.chmod(0o755 if data['common'][name]['mode'] == '100755' else 0o644)
            target_path = target / POLICY
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_bytes(regular(control, POLICY).read_bytes())
        return {'status': 'prepared-local', 'publishable': False, 'bases': BASES,
                'output': str(output), 'common_paths': sorted(data['common'])}
    except Exception:
        shutil.rmtree(output)
        raise


def target_role(control):
    # The executing reviewed control checkout supplies the context, never root/candidate.
    for role in ('staging', 'main'):
        result = subprocess.run(['git', '--no-replace-objects', '-C', str(control),
                                 'merge-base', '--is-ancestor', BASES[role], 'HEAD'], capture_output=True, env=git_environment())
        if result.returncode == 0:
            return role
    raise ValueError('trusted target ancestor context is unavailable')


def check_history(root):
    partial = subprocess.run(['git', '-C', str(root), 'config', '--local', '--includes', '--get-regexp',
                              r'^(extensions\.partialclone|remote\..*\.(promisor|partialclonefilter))$'],
                             capture_output=True, env=git_environment())
    if partial.returncode not in (0, 1):
        raise ValueError('source configuration check failed')
    if partial.stdout.strip():
        raise ValueError('complete history required: partial/promisor configuration is not allowed')
    if git(root, 'for-each-ref', '--format=%(refname)', 'refs/replace').strip():
        raise ValueError('replacement history is not allowed')
    grafts = Path(git(root, 'rev-parse', '--path-format=absolute', '--git-path', 'info/grafts').decode().strip())
    if grafts.exists() or grafts.is_symlink() or git(root, 'rev-parse', '--is-shallow-repository').strip() != b'false':
        raise ValueError('complete, unmodified history is required')


def source_names(root):
    """Include ignored sources, except named local dependency/build/cache outputs."""
    names = set()
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            name = path.relative_to(root).as_posix()
            excluded = name in {'.git', 'node_modules', 'blog/.vitepress/dist',
                                'blog/.vitepress/cache', 'blog/.vitepress/.temp'}
            excluded |= path.name == '__pycache__' and name.startswith(('scripts/', 'tests/'))
            if excluded:
                if not path.is_dir() or path.is_symlink():
                    raise ValueError('linked/non-directory local output: ' + name)
                continue
            if path.is_symlink() or path.is_file():
                names.add(name)
            elif path.is_dir():
                pending.append(path)
            else:
                raise ValueError('nonregular source: ' + name)
    return names


def current_identity(root, name, expected):
    path = root / name
    for parent in path.parents:
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError('linked current source parent: ' + name)
    if expected['mode'] == '120000':
        if not path.is_symlink():
            raise ValueError('changed current alias: ' + name)
        raw = os.readlink(path).encode()
        mode = '120000'
    else:
        path = regular(root, name)
        raw = path.read_bytes()
        mode = '100755' if path.stat().st_mode & 0o100 else '100644'
    return {'mode': mode, 'sha256': digest(raw)}


def verify(control, root):
    from main_publication_verification import tree, identity
    check_history(control)
    check_history(root)
    role = target_role(control)
    data, inventory = policy(control)
    git(root, 'merge-base', '--is-ancestor', BASES[role], 'HEAD')
    expected = {p: identity(e) for p, e in tree(control, BASES[role]).items()}
    expected.update(data['common'])
    expected[POLICY] = {'mode': '100644', 'sha256': digest(regular(control, POLICY).read_bytes())}
    actual = source_names(root)
    if actual != set(expected):
        raise ValueError('current reconciliation source inventory mismatch: ' + ', '.join(sorted(actual ^ set(expected))[:8]))
    for name, entry in expected.items():
        if current_identity(root, name, entry) != entry:
            raise ValueError(('changed test repair provenance: ' if name == 'maintenance/harness-reconciliation/test-contract-repair.json' else 'changed current reconciliation source: ') + name)
    spec = spec_from_file_location('trusted_current_tracker', control / 'scripts/verify-harness-adoption.py')
    tracker = module_from_spec(spec)
    spec.loader.exec_module(tracker)
    state = tracker.check_tickets(root)
    check_t13_landing(control, root, state, data)
    return {'status': 'pass', 'tracker': state, 'target_role': role, 'target_base': BASES[role],
            'candidate_head': git(root, 'rev-parse', 'HEAD').decode().strip(),
            'source_paths': len(expected), 'publishable': False,
            'candidate_paths_preserved': sum(len(c['paths']) for c in inventory['candidates']) if role == 'staging' else 0}


def check_t13_landing(control, root, state, data):
    ticket = state['tickets'].get('T-0013')
    if not ticket or ticket['status'] != 'done':
        return
    receipt = json.loads(regular(root, ticket.get('landing_evidence', '')).read_text())
    from main_publication_verification import tree, identity
    # A completed ticket is bound to its actual main landing policy, not future
    # T-0014/T-0015 additions in the live engineering control map.
    main_commit = receipt.get('main_commit', '')
    if not isinstance(main_commit, str) or len(main_commit) != 40 or any(c not in '0123456789abcdef' for c in main_commit):
        raise ValueError('T-0013 requires actual main and staging landing commits')
    try:
        frozen = json.loads(git(control, 'show', main_commit + ':' + POLICY))
    except (subprocess.CalledProcessError, ValueError) as error:
        raise ValueError('T-0013 landing policy is unavailable') from error
    if (set(frozen) != {'version', 'bases', 'm0_sha256', 'scope', 'common'}
            or frozen['version'] != 1 or frozen['bases'] != BASES or frozen['m0_sha256'] != M0_SHA
            or not isinstance(frozen['common'], dict)):
        raise ValueError('T-0013 landing policy has an invalid contract')
    engineering = {p: entry for p, entry in frozen['common'].items()
                   if p.startswith('scripts/') or p == 'docs/adr/0008-main-first-engineering-and-shared-staging.md'}
    required = {'scripts/publication_current.py', 'scripts/publication-baseline.py',
                'scripts/verify-harness-adoption.py', 'docs/adr/0008-main-first-engineering-and-shared-staging.md'}
    if not required <= set(engineering):
        raise ValueError('T-0013 landing policy is missing the engineering successor')
    for key, role in [('main_commit', 'main'), ('commit', 'staging')]:
        commit = receipt.get(key, '')
        if not isinstance(commit, str) or len(commit) != 40 or any(c not in '0123456789abcdef' for c in commit):
            raise ValueError('T-0013 requires actual main and staging landing commits')
        target = 'refs/heads/' + role
        if subprocess.run(['git', '-C', str(control), 'show-ref', '--verify', '--quiet', target], capture_output=True, env=git_environment()).returncode:
            target = 'refs/remotes/origin/' + role
        try:
            git(control, 'merge-base', '--is-ancestor', commit, target)
            landed = tree(control, commit)
        except subprocess.CalledProcessError as error:
            raise ValueError('T-0013 landing is not in the trusted target history') from error
        if any(identity(landed.get(p)) != expected for p, expected in engineering.items()):
            raise ValueError('T-0013 engineering successor is not actually landed')
