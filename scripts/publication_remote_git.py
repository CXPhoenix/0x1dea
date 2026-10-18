"""Read-only trusted Git preparation and validation for the remote sync adapter."""
import hashlib
import copy
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import tempfile

import publication_remote as remote

CONTROL = Path(__file__).resolve().parents[1]


def load(name):
    spec = spec_from_file_location('trusted_'+name.replace('-', '_'), CONTROL/'scripts'/name)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


operation_for = remote.operation_for

class LocalPreparation:
    def __init__(self, registry, *, repository, policy, directory):
        self.sync = load('staging-sync.py')
        self.registry = self.sync.validate(registry)
        self.repository, self.policy = repository, policy
        self.directory = self.sync.safe_output(Path(directory), registry['repository'])
        self.directory.mkdir(parents=True, exist_ok=True)

    def refreshed_registry(self, refs):
        registry = copy.deepcopy(self.registry)
        source = registry['repository']
        for role in ('main', 'staging'):
            if self.sync.git(source, 'merge-base', '--is-ancestor', registry[role]['sha'], refs[role], check=False).returncode:
                raise ValueError('source pins unavailable or history changed')
            registry[role]['sha'] = refs[role]
            registry['trees'][role] = self.sync.identities(source, refs[role])
        owned = {p for c in registry['candidates'] for p in c['paths']}
        for candidate in registry['candidates']:
            if any(registry['trees']['staging'].get(p) != e for p,e in candidate['paths'].items()):
                raise ValueError('candidate changed; explicit registry/source approval required')
            original = candidate['source']
            for role in ('main', 'staging'):
                if original == self.registry[role]:
                    candidate['source'] = dict(registry[role])
        allowed = set(self.registry['engineering'])
        policy_path = 'maintenance/publication-workflow/engineering-v1.json'
        policy_entry = registry['trees']['main'].get(policy_path)
        if policy_entry:
            raw = self.sync.git(source, 'cat-file', 'blob', policy_entry['blob']).stdout
            if hashlib.sha256(raw).hexdigest() != self.policy:
                raise ValueError('latest main policy requires a fresh trusted controller run')
            allowed.update(json.loads(raw)['common'])
            allowed.add(policy_path)
        mt,st = registry['trees']['main'],registry['trees']['staging']
        engineering = {p for p in set(mt)|set(st) if mt.get(p) != st.get(p)} - owned
        if engineering - allowed:
            raise ValueError('new unclassified engineering paths require reviewed policy')
        registry['engineering'] = sorted(engineering)
        return self.sync.validate(registry)

    def __call__(self, refs):
        try:
            registry = self.refreshed_registry(refs)
        except self.sync.Invalid as error:
            return {'status':error.status, 'paths':error.paths, 'reason':str(error)}
        except ValueError as error:
            return {'status':'stale', 'reason':str(error)}
        store = Path(tempfile.mkdtemp(prefix='sync-', dir=self.directory))/'result.git'
        try:
            result = self.sync.compute(registry, store)
        except self.sync.Invalid as error:
            return {'status':error.status, 'paths':error.paths, 'reason':str(error)}
        if result['status'] == 'no-op':
            return result
        parents = list(dict.fromkeys([refs['staging'], refs['main']] +
                                     ([refs['branch']] if refs['branch'] else [])))
        for parent in parents:
            self.sync.git(store, 'cat-file', '-e', parent+'^{commit}')
        operation = operation_for(self.repository, self.policy, refs, result['result_tree'])
        template = (CONTROL/'maintenance/publication-workflow/automation/sync-commit-template.txt').read_text().rstrip()
        message = template+'\n\n0x1DEA-operation: '+remote.canonical(operation).decode().strip()+'\n'
        identity = '0x1DEA Sync <sync@example.invalid> 946684800 +0000'
        raw = ('tree '+result['result_tree']+'\n'+''.join('parent '+p+'\n' for p in parents)
               +'author '+identity+'\ncommitter '+identity+'\n\n'+message).encode()
        head = self.sync.git(store, 'hash-object', '-t', 'commit', '-w', '--stdin', data=raw).stdout.decode().strip()
        if hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest() != head:
            raise ValueError('result commit identity mismatch')
        return {'status':'ready', 'tree':result['result_tree'], 'head':head, 'store':str(store),
                'parents':parents, 'message':message,
                'known_blobs':sorted({e['blob'] for tree in registry['trees'].values() for e in tree.values()})}


def validate_operation(operation, head, registry, runtime, runtime_digest, output):
    """Read-only trusted main validation. Candidate checkout code is never imported."""
    import os
    import subprocess
    import publication_current as current
    if any(os.environ.get(key) for key in ('PUBLICATION_WRITER_TOKEN', 'PUBLICATION_REPORTER_TOKEN', 'GH_TOKEN', 'GITHUB_TOKEN')):
        raise ValueError('validation must not receive writer or API credentials')
    expected = operation_for(operation['repository'], operation['policy'], operation, operation['tree'])
    if operation != expected:
        raise ValueError('operation identity or fields mismatch')
    if current.git(CONTROL, 'rev-parse', 'HEAD').decode().strip() != operation['main']:
        raise ValueError('trusted validation must execute from exact main commit')
    raw_policy = current.regular(CONTROL, current.POLICY).read_bytes()
    if hashlib.sha256(raw_policy).hexdigest() != operation['policy']:
        raise ValueError('trusted main policy changed')
    current.verify(CONTROL, CONTROL)
    sync = load('staging-sync.py')
    with tempfile.TemporaryDirectory(prefix='trusted-sync-validation-') as tmp:
        preparer = LocalPreparation(registry, repository=operation['repository'], policy=operation['policy'],
                                    directory=Path(tmp)/'preparation')
        registry = preparer.refreshed_registry(operation)
        store = Path(tmp)/'result.git'
        computed = sync.compute(registry, store)
        if computed['result_tree'] != operation['tree']:
            raise ValueError('independent validation tree mismatch')
        raw = sync.git(store, 'cat-file', 'commit', head).stdout
        if hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest() != head:
            raise ValueError('candidate commit identity mismatch')
        meta, message = raw.split(b'\n\n', 1)
        tree = [line[5:].decode() for line in meta.splitlines() if line.startswith(b'tree ')]
        parents = [line[7:].decode() for line in meta.splitlines() if line.startswith(b'parent ')]
        marker = json.loads(message.decode().split('\n\n0x1DEA-operation: ', 1)[1])
        if tree != [operation['tree']] or marker != operation or not {operation['main'], operation['staging']} <= set(parents) or len(parents) > 3:
            raise ValueError('candidate provenance mismatch')
        target = Path(tmp)/'candidate'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--template=', registry['repository'], str(target)],
                       check=True, capture_output=True, env=current.git_environment(local_clone=True))
        current.git(target, '-c', 'core.hooksPath=/dev/null', 'checkout', '--detach', head)
        for role in ('main', 'staging'):
            current.git(target, 'update-ref', 'refs/heads/'+role, operation[role])
        native = current.verify_staging_sync(CONTROL, target)
        v2 = load('article-publication-v2.py')
        files = v2.old.tree(store, operation['tree'])
        boundary = load('publication_build_v2.py')
        receipt = boundary.execute(v2.old, operation, files, runtime, runtime_digest, Path(output),
            v2.export, v2.physical,
            lambda files, signatures: {'status':'staging-build', 'scope':'All registered preview candidates allowed; no publication exclusion claim'},
            None, staging=True)
    return {'version':1, 'status':'pass', 'operation':operation, 'head':head,
            'native':native, 'build':receipt, 'surface':'local trusted CLI, native data validation and isolated VitePress build',
            'publishable':False}
