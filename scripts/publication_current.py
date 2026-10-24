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
DISCORD_PUBLICATION = '0e690064985d9d734849e1ec44a8c0f8d84fb2a3'
DISCORD_RECORD = 'blog/public/.well-known/discord'
DISCORD_IDENTITY = {'mode': '100644',
                    'sha256': 'd28142c7a5a13b28d22abaa933cedc2027ce9abbabb2f09c55b989084caa5019'}
LOCAL_NOTES_IGNORE = {'mode': '100644',
                      'sha256': '9f7ac2c358f5b1af070bf44703e40dfe4786e8dfd02772f66c944e09ea58bb98'}
PRE_NOTES_CURRENT = {'ae535a8040f01620a77d3fab4d3f433cb578f883b1e24c162769ff05f0cb27cd',
                     '759826ee582cf0fd8b8d72cf5a6911b09b89dd53c1abe5f17cf48167697bcd58'}

# Exact owner-approved Phoenix v2.3 source from staging bf6f872; no prefix waiver.
PHOENIX_V23_SUCCESSORS = {'skills/phoenix-writing/SKILL.md': {'mode': '100644',
                                     'sha256': '056a6c0afa6996049378b8aa2cefae908aa208efb43a7ebe0805d75ae5db80ea'},
 'skills/phoenix-writing/references/context-form.md': {'mode': '100644',
                                                       'sha256': 'ec4a9205411a835a28f4ba3a72b8f155a0d7378c48de99f354d57c2e575bd04e'},
 '.agents/skills/phoenix-writing/SKILL.md': {'mode': '100644',
                                             'sha256': '056a6c0afa6996049378b8aa2cefae908aa208efb43a7ebe0805d75ae5db80ea'},
 '.agents/skills/phoenix-writing/references/context-form.md': {'mode': '100644',
                                                               'sha256': '99425a0fa284146eec55e5625406ad6c6b50ea4249bd7587c80925d2311c67d9'},
 '.claude/skills/phoenix-writing/SKILL.md': {'mode': '100644',
                                             'sha256': '056a6c0afa6996049378b8aa2cefae908aa208efb43a7ebe0805d75ae5db80ea'},
 '.claude/skills/phoenix-writing/references/context-form.md': {'mode': '100644',
                                                               'sha256': '99425a0fa284146eec55e5625406ad6c6b50ea4249bd7587c80925d2311c67d9'},
 'maintenance/harness-adoption/runtime-source-policy.json': {'mode': '100644',
                                                             'sha256': 'a4b2b842bd1e1079e67bf20e2b21a01fb400305f60f70f82b207099a90e508cb'},
 'maintenance/harness-adoption/generated-writing-manifest.json': {'mode': '100644',
                                                                  'sha256': '606b123e3cdb43ad4449c45eb1c58e572a794c73b066696ae746b216451d01f0'},
 'maintenance/writing-skills/SOURCES.md': {'mode': '100644',
                                           'sha256': 'fc29bbefb00580a0bf07978bf94533e766b370c7a188f8852fa18097727d7c15'},
 'maintenance/writing-skills/VALIDATION.md': {'mode': '100644',
                                              'sha256': '2292d41418aaad231f1efbcda34dad4b0fa1f2f8ffb05f21e86144c10b0152b5'}}

ARTICLE_DISCOVERY_SUCCESSORS = {'.agents/skills/article-discovery/SKILL.md': {'mode': '100644',
                                               'sha256': '74cbe852edb17cf1194e9e5ac760c377fa50ffba995fe8b3b06989a3e7e3eea5'},
 '.agents/skills/article-discovery/agents/openai.yaml': {'mode': '100644',
                                                         'sha256': '641ef492c9b319271ee9289d3aee8409a036e24141c1aefaf3eb695f783292ad'},
 '.agents/skills/article-discovery/references/persistence.md': {'mode': '100644',
                                                                'sha256': '427426fb7376b33c982e844bdd13a33e6e61301f7dd12eec1acfb08f710024d1'},
 '.agents/skills/article-discovery/references/public-preparation.md': {'mode': '100644',
                                                                       'sha256': 'c69d3b041c9219a02eaaf239271a8bf55a02e7ac3ac327359cdf53deb20b821c'},
 '.agents/skills/maintaining-writing-skills/references/writing-process.md': {'mode': '100644',
                                                                             'sha256': '3b191bef447d141cd2fd923f8ff37569b93fb8f82d5d155498d4e7913bfeea02'},
 '.claude/skills/article-discovery/SKILL.md': {'mode': '100644',
                                               'sha256': '74cbe852edb17cf1194e9e5ac760c377fa50ffba995fe8b3b06989a3e7e3eea5'},
 '.claude/skills/article-discovery/references/persistence.md': {'mode': '100644',
                                                                'sha256': '427426fb7376b33c982e844bdd13a33e6e61301f7dd12eec1acfb08f710024d1'},
 '.claude/skills/article-discovery/references/public-preparation.md': {'mode': '100644',
                                                                       'sha256': 'c69d3b041c9219a02eaaf239271a8bf55a02e7ac3ac327359cdf53deb20b821c'},
 '.claude/skills/maintaining-writing-skills/references/writing-process.md': {'mode': '100644',
                                                                             'sha256': '3b191bef447d141cd2fd923f8ff37569b93fb8f82d5d155498d4e7913bfeea02'},
 'AGENTS.md': {'mode': '100644',
               'sha256': 'c68401f65bb1ba9d264abaeff3921bf0df71cbba60e0fa093ed5cac360733aea'},
 'docs/agents/domain.md': {'mode': '100644',
                           'sha256': 'd14b5f02d004f3a82da35aa8b8fa5f0837d5ce24f1388faa63b9d1059261dfd6'},
 'docs/agents/language.md': {'mode': '100644',
                             'sha256': 'd44b4af6c0c2fed01ad883567e7a31b0699a06919b1c07b2572409a26a2f9c00'},
 'docs/agents/runtime.md': {'mode': '100644',
                            'sha256': '5ef5e21fe7a96745fd3de64080df318131a82bd34f365d6d5a0a6015c1372438'},
 'docs/agents/skill-sources.json': {'mode': '100644',
                                    'sha256': '15138ad2917774c7e2378853610470a7c202662de5982a5d69976bac4e2ae521'},
 'docs/agents/workflow.md': {'mode': '100644',
                             'sha256': 'eb6ede2cc9249bd88224ba484ab05459f0aef048a9d4e7ade7d600add5865b3b'},
 'maintenance/harness-adoption/generated-writing-manifest.json': {'mode': '100644',
                                                                  'sha256': '07d2bd25cb1263542c341a42b4b4f1c30705f26502b24f161dc38aba624052d2'},
 'maintenance/harness-adoption/runtime-source-policy.json': {'mode': '100644',
                                                             'sha256': '1438ca382e0b6e68d412cc97b563936c22cebfa708c621d60749a6e7554782cc'},
 'scripts/materialize-writing-skills.py': {'mode': '100644',
                                           'sha256': '493c657224ef88f5340afc1c73f6be1209b566e35eba9bf4a0d9042a935287c1'},
 'skills/article-discovery/SKILL.md': {'mode': '100644',
                                       'sha256': '74cbe852edb17cf1194e9e5ac760c377fa50ffba995fe8b3b06989a3e7e3eea5'},
 'skills/article-discovery/references/persistence.md': {'mode': '100644',
                                                        'sha256': '427426fb7376b33c982e844bdd13a33e6e61301f7dd12eec1acfb08f710024d1'},
 'skills/article-discovery/references/public-preparation.md': {'mode': '100644',
                                                               'sha256': 'c69d3b041c9219a02eaaf239271a8bf55a02e7ac3ac327359cdf53deb20b821c'},
 'skills/maintaining-writing-skills/references/writing-process.md': {'mode': '100644',
                                                                     'sha256': 'be8d12b3bedcc5852068a3a76182b3a2f9dfc9762d70417cf929b6b935c334a4'}}
REVIEWED_SUCCESSORS = PHOENIX_V23_SUCCESSORS | ARTICLE_DISCOVERY_SUCCESSORS

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

# Owner-authorized, actual PR20/25/26 + PR21 dual-target closeout.
CLOSEOUT_SUCCESSORS.update({'.proj.tickets/0010-main-verification-repair/T-0012-ticket-evidence-closeout.md': '6570950636c67b59a0d0f8fb41dfe7ca6983346f44e4a0741702f3968f86bb77', '.proj.tickets/0012-publication-workflow/T-0014-v2-selected-candidate.md': '2af9335a48b95e2857eb367d5d8601ff473b5715683db66dddad1de3fa731983', '.proj.tickets/0012-publication-workflow/T-0015-local-staging-sync.md': 'd2a8496fdec3958ab6cc19a835ff64f8b7901c3ca43173b1f52aac5aafcc0e3e'})
CLOSEOUT_RECEIPTS.update({'.proj.specs/0012-publication-workflow/implementation/dual-landing-20261016/approval.md': '2eccaf3a6ee4284d6e7289929e0165ca8e9a976315c91bc0012004f1c3cb76d4', '.proj.specs/0012-publication-workflow/implementation/dual-landing-20261016/T-0012-landing.json': 'aa43e02ca8224e4322cc12d9d456cf4feaaa047e9c00f6c73bd8a5ce23d82965', '.proj.specs/0012-publication-workflow/implementation/dual-landing-20261016/T-0014-landing.json': '50093c6da06cea477dfc1931896f8cc835f89ecd8d0b182e497dc64ef8257130', '.proj.specs/0012-publication-workflow/implementation/dual-landing-20261016/T-0015-landing.json': 'f7087e76d6a67f15d6c4e7da3469f1cf1347fb4e8879d89b77dd7af778333cee'})

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


def policy(control, workflow_admission=None):
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
    for name, expected in REVIEWED_SUCCESSORS.items():
        if data['common'].get(name) != expected:
            raise ValueError('unapproved exact Phoenix v2.3 identity: ' + name)
        path = regular(control, name)
        if path.stat().st_mode & 0o111 or digest(path.read_bytes()) != expected['sha256']:
            raise ValueError('changed exact Phoenix v2.3 identity: ' + name)
    ignore = regular(control, '.gitignore')
    if data['common'].get('.gitignore') != LOCAL_NOTES_IGNORE:
        raise ValueError('unapproved exact local notes ignore identity: .gitignore')
    if ignore.stat().st_mode & 0o111 or digest(ignore.read_bytes()) != LOCAL_NOTES_IGNORE['sha256']:
        raise ValueError('changed exact local notes ignore identity: .gitignore')
    admitted = workflow_admission.allowed(control) if workflow_admission else {}
    if not workflow_admission:
        from publication_workflows import github_git_paths
        if github_git_paths(control, 'HEAD'):
            raise ValueError('protected Git deployment sources require finite workflow admission')
    github_sources = {name for name in source_names(control)
                      if name == '.github' or name.startswith('.github/')}
    if github_sources != set(admitted):
        raise ValueError('protected deployment sources outside finite workflow admission: '
                         + ', '.join(sorted(github_sources ^ set(admitted))))
    writing = ('phoenix-writing', 'maintaining-writing-skills', 'creating-vitepress-post', 'article-discovery')
    for name, expected in data['common'].items():
        # Retain each target's pre-notes pin so an additive shared successor
        # does not conflict with staging's existing identity during Git merge.
        if name == 'scripts/publication_current.py' and 'successor_sha256' in expected:
            if (set(expected) != {'mode', 'sha256', 'successor_sha256'}
                    or expected['mode'] != '100644' or expected['sha256'] not in PRE_NOTES_CURRENT):
                raise ValueError('invalid finite current guard successor: ' + name)
            expected = {'mode': expected['mode'], 'sha256': expected['successor_sha256']}
            data['common'][name] = expected
        regular(control, name)
        if name in owned or name in protected_history or name.startswith('blog/') or (name.startswith('.github/') and name not in admitted) or (name not in REVIEWED_SUCCESSORS and any(name.startswith(prefix + package + '/') for prefix in ('skills/', '.agents/skills/', '.claude/skills/') for package in writing)):
            raise ValueError('protected content/history in common successor: ' + name)
        if set(expected) != {'mode', 'sha256'} or expected['mode'] not in {'100644', '100755'} or not isinstance(expected['sha256'], str) or len(expected['sha256']) != 64 or any(c not in '0123456789abcdef' for c in expected['sha256']):
            raise ValueError('invalid exact common identity: ' + name)
        if name not in {'scripts/verify-harness-adoption.py', '.gitignore'} and name not in CLOSEOUT_SUCCESSORS and name not in REVIEWED_SUCCESSORS:
            for entries in inventory['trees'].values():
                previous = entries.get(name)
                if previous and expected != {'mode': previous['mode'], 'sha256': digest(git(control, 'cat-file', 'blob', previous['blob']))}:
                    raise ValueError('unapproved existing engineering replacement: ' + name)
    return data, inventory


def prepare(control, output, *, workflow_admission=None):
    check_history(control)
    data, inventory = policy(control, workflow_admission)
    output = output.absolute()
    if output.exists() or output.is_symlink() or output.resolve().is_relative_to(control.resolve()):
        raise ValueError('output must be new and outside the control checkout')
    for parent in output.parents:
        if parent.is_symlink() and (parent.as_posix(), parent.readlink().as_posix()) not in {('/var', 'private/var'), ('/tmp', 'private/tmp')}:
            raise ValueError('linked projection output parent')
    output = output.resolve()
    owned = {p for c in inventory['candidates'] for p in c['paths']}
    for name, expected in data['common'].items():
        if name in owned or name.startswith('blog/') or (name.startswith('.github/') and not workflow_admission):
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
            # HEAD/tree stay at the immutable M0 projection bases. Named target
            # refs retain actual trusted histories needed by completed-ticket checks.
            for target_role_name in BASES:
                target_pin = git(control, 'rev-parse', 'refs/heads/' + target_role_name).decode().strip()
                if workflow_admission and target_role_name == 'main':
                    target_pin = workflow_admission.main
                git(target, 'update-ref', 'refs/heads/' + target_role_name, target_pin)
            if workflow_admission:
                git(target, 'update-ref', 'refs/publication/workflow-main', workflow_admission.main)
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


def local_note_names(root, expected):
    """Validate the finite local writing-output shape before excluding names."""
    owned = set(expected)
    for args in (('ls-tree', '-rz', '--name-only', 'HEAD', '--', '.proj.writing'),
                 ('ls-files', '-z', '--cached', '--', '.proj.writing')):
        owned.update(name.decode() for name in git(root, *args).split(b'\0') if name)
    collisions = {name for name in owned
                  if name == '.proj.writing' or name.startswith('.proj.writing/')}
    if collisions:
        raise ValueError('local writing source ownership collision: ' + ', '.join(sorted(collisions)))
    namespace = root / '.proj.writing'
    if namespace.is_symlink():
        raise ValueError('linked local writing namespace: .proj.writing')
    if not namespace.exists():
        return set()
    if not namespace.is_dir():
        raise ValueError('non-directory local writing namespace: .proj.writing')
    notes = set()
    for workspace in namespace.iterdir():
        if (workspace.name in {'.', '..'} or '\\' in workspace.name
                or workspace.is_symlink() or not workspace.is_dir()):
            raise ValueError('invalid local writing workspace: ' + str(workspace.relative_to(root)))
        for note in workspace.iterdir():
            name = note.relative_to(root).as_posix()
            if (note.name not in {'PROJECT.md', 'GLOSSARY.md', 'CONTEXT.md'}
                    or note.is_symlink() or not note.is_file()
                    or note.stat().st_mode & 0o111):
                raise ValueError('invalid local writing note: ' + name)
            notes.add(name)
    return notes


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


def verify(control, root, *, workflow_admission=None):
    return _verify_current(control, root, target_role(control), workflow_admission)


def verify_staging_sync(control, root, *, workflow_admission=None):
    """Trusted main sync operation fixes the staging role; candidate data cannot select it."""
    return _verify_current(control, root, 'staging', workflow_admission)


def _verify_current(control, root, role, workflow_admission=None):
    from main_publication_verification import tree, identity
    check_history(control)
    check_history(root)
    data, inventory = policy(control, workflow_admission)
    from publication_workflows import check_git_sources
    check_git_sources(root, {name:entry for name,entry in data['common'].items()
                             if name.startswith('.github/')})
    git(root, 'merge-base', '--is-ancestor', BASES[role], 'HEAD')
    expected = {p: identity(e) for p, e in tree(control, BASES[role]).items()}
    expected.update(data['common'])
    expected[POLICY] = {'mode': '100644', 'sha256': digest(regular(control, POLICY).read_bytes())}
    # Only targets containing the actual approved publication require this record.
    # Historical M0 projections retain their original source set.
    try:
        git(root, 'merge-base', '--is-ancestor', DISCORD_PUBLICATION, 'HEAD')
    except subprocess.CalledProcessError as error:
        if error.returncode != 1:
            raise ValueError('published Discord source ancestry is unavailable') from error
    else:
        expected[DISCORD_RECORD] = DISCORD_IDENTITY
    notes = local_note_names(root, expected)
    actual = source_names(root) - notes
    if actual != set(expected):
        raise ValueError('current reconciliation source inventory mismatch: ' + ', '.join(sorted(actual ^ set(expected))[:8]))
    for name, entry in expected.items():
        if name == '.gitignore' and regular(root, name).stat().st_mode & 0o111:
            raise ValueError('executable local notes ignore source: .gitignore')
        if name == DISCORD_RECORD and regular(root, name).stat().st_mode & 0o111:
            raise ValueError('executable published Discord source: ' + name)
        if name in REVIEWED_SUCCESSORS and regular(root, name).stat().st_mode & 0o111:
            raise ValueError('executable approved Phoenix v2.3 source: ' + name)
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
