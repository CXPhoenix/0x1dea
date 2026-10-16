"""Trusted main writer orchestration; transport/source callbacks are trusted code."""
import hashlib
import json
from contextlib import contextmanager
import fcntl
import os
from pathlib import Path
import re
import tempfile

BRANCH = 'tickets/T-0016/main-to-staging-sync'
OWNER = '0x1DEA:T-0016:main-to-staging-sync:v1'


class RemoteError(ValueError):
    def __init__(self, message, *, uncertain=False, status=None):
        super().__init__(message)
        self.uncertain = uncertain
        self.status = status


def observe_write(action, readback, matches):
    """Always read an ambiguous outcome before allowing another mutation."""
    try:
        action()
    except RemoteError as error:
        if not error.uncertain:
            raise
    observed = readback()
    if not matches(observed):
        raise RemoteError('remote outcome not established; inspect before retry', uncertain=True)
    return observed


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def operation_for(repository, policy, refs, tree):
    operation = {'version':1, 'repository':repository, 'target':'staging',
                 'branch':BRANCH, 'owner':OWNER, 'main':refs['main'],
                 'staging':refs['staging'], 'policy':policy, 'tree':tree}
    operation['id'] = hashlib.sha256(canonical(operation)).hexdigest()
    return operation


@contextmanager
def writer_lock(state_dir, repository):
    """Shared by sync, preview integration and future publication writers on one host.

    Deployed jobs additionally require the shared Actions concurrency group. This
    lock does not claim to serialize manual GitHub writers; pin rereads guard them.
    """
    path = Path(state_dir)
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    if any(p.is_symlink() for p in (path, *path.parents) if str(p) not in ('/tmp', '/var')):
        raise ValueError('linked writer state directory')
    name = hashlib.sha256(repository.encode()).hexdigest()
    fd = os.open(path/(name+'.lock'), os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def run_sync(api, prepare, *, repository, policy, state_dir, activation, authorized=False, manual_history=None):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository) or not re.fullmatch('[0-9a-f]{64}', policy):
        raise ValueError('invalid trusted repository/policy identity')
    with writer_lock(state_dir, repository):
        record = Path(state_dir)/(hashlib.sha256(repository.encode()).hexdigest()+'.json')
        last = {}
        def journal(value):
            last.clear()
            last.update(value)
            _write_record(record, value)
        for retry in range(4):
            try:
                result = _run_once(api, prepare, repository, policy, activation, authorized, journal, manual_history)
            except (RemoteError, KeyError, TypeError, ValueError):
                result = {'status':'blocked', 'reason':'remote outcome/permission/response not established; readback required', 'publishable':False}
            result['retries'] = retry
            if result['status'] != 'stale':
                break
        if last:
            result['last_preparation'] = last
        _write_record(record, result)
        return result


def _write_record(path, value):
    fd, temporary = tempfile.mkstemp(prefix='.operation-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(canonical(value))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _owned_pulls(api, repository, activation, main, manual_history=None, refs=None):
    prs = [p for p in api.pulls() if p['branch'] == BRANCH]
    bootstrap = [p for p in prs if type(activation.get('bootstrap_pr')) is int
                 and p['number'] == activation['bootstrap_pr'] and p['state'] == 'closed'
                 and p.get('merged') is True and p['base'] == 'main' and p['repository'] == repository
                 and p['head'] == activation.get('branch_seed')
                 and api.is_ancestor(p['head'], main)]
    # Excluding the record is not enough: its observed identity is also required
    # before an initial implementation commit may bootstrap branch ownership.
    proven = len(bootstrap) == 1
    history = [manual_history.observe(api, refs, prs)] if manual_history else []
    filtered = [p for p in prs if (not proven or p != bootstrap[0])
                and not any(p['number'] == item['number'] for item in history)]
    return filtered, proven, history


def _pull_snapshot(prs):
    fields = ('number', 'state', 'base', 'branch', 'repository', 'owner', 'operation', 'merged')
    return canonical([{key:p.get(key) for key in fields} for p in sorted(prs, key=lambda p:p['number'])])


def _matches_pull(p, repository, operation, head):
    return (p.get('state') == 'open' and p.get('owner') == OWNER and p.get('operation') == operation['id']
            and p.get('head') == head and p.get('base') == 'staging'
            and p.get('repository') == repository and p.get('branch') == BRANCH)


def _run_once(api, prepare, repository, policy, activation, authorized, journal, manual_history=None):
    required = ('permissions_verified', 'latest_base_verified', 'dispatch_verified',
                'candidate_isolation_verified')
    if (not authorized or activation.get('repository') != repository
            or not all(activation.get(key) is True for key in required)
            or type(activation.get('exercise_run_id')) is not int or activation['exercise_run_id'] <= 0):
        return {'version': 1, 'status': 'blocked', 'reason': 'activation/authority prerequisites missing',
                'publishable': False}
    refs = api.refs()
    prepared = prepare(refs)
    if prepared['status'] != 'ready':
        return dict(prepared, version=1, publishable=False)
    operation = operation_for(repository, policy, refs, prepared['tree'])
    prs, bootstrap_pr_proven, history = _owned_pulls(api, repository, activation, refs['main'], manual_history, refs)
    if (any(p['repository'] != repository or p['base'] != 'staging' or p['owner'] != OWNER for p in prs)
            or sum(p['state'] == 'open' for p in prs) > 1
            or any(p['state'] != 'open' and p['operation'] == operation['id'] for p in prs)):
        return {'status': 'blocked', 'reason': 'pull ownership/closed-operation mismatch', 'publishable': False}
    if refs['branch'] is not None:
        commit = api.commit(refs['branch'])
        bootstrap = (bootstrap_pr_proven and refs['branch'] == activation.get('branch_seed')
                     and api.is_ancestor(refs['branch'], refs['main']))
        if commit.get('owner') != OWNER and not bootstrap:
            return {'status': 'blocked', 'reason': 'branch ownership mismatch', 'publishable': False}
    head = prepared['head']
    if refs['branch'] and api.commit(refs['branch']).get('operation') == operation['id']:
        if api.commit(refs['branch'])['tree'] != prepared['tree']:
            return {'status': 'blocked', 'reason': 'owned result tree mismatch', 'publishable': False}
        head = refs['branch']
    journal({'status':'prepared', 'operation':operation, 'head':head, 'manual_history':history, 'publishable':False})
    workflow = api.workflow(refs['main'])
    if (workflow != {'sha256': activation.get('workflow_sha256'), 'main': refs['main']}
            or not re.fullmatch('[0-9a-f]{64}', str(activation.get('workflow_sha256', '')))
            or activation.get('workflow') != 'staging-sync-validate.yml'):
        return {'status': 'blocked', 'reason': 'trusted main workflow identity missing', 'publishable': False}
    if api.refs() != refs:
        return {'status': 'stale', 'reason': 'pins drifted before write', 'publishable': False}
    if refs['branch'] != head:
        observe_write(lambda: api.upload(prepared, operation), lambda: api.commit(head),
                      lambda commit: commit.get('tree') == operation['tree']
                          and commit.get('operation') == operation['id'] and commit.get('owner') == OWNER
                          and commit.get('parents') == prepared['parents'])
        if api.refs() != refs:
            return {'status': 'stale', 'reason': 'pins drifted before branch write', 'publishable': False}
        observe_write(lambda: api.advance(head, refs['branch']), api.refs,
                      lambda actual: actual == dict(refs, branch=head))
    commit = api.commit(head)
    if (commit.get('operation') != operation['id'] or commit.get('tree') != operation['tree']
            or commit.get('owner') != OWNER or not {refs['main'], refs['staging']} <= set(commit.get('parents', []))):
        return {'status':'blocked', 'reason':'candidate commit identity mismatch', 'publishable':False}
    expected = dict(refs, branch=head)
    if api.refs() != expected:
        return {'status': 'stale', 'reason': 'pins drifted before dispatch', 'publishable': False}
    runs = api.validation_runs(operation, head)
    if not runs:
        runs = observe_write(lambda: api.dispatch(operation, head),
                             lambda: api.validation_runs(operation, head), lambda observed: bool(observed))
    exact_runs = [r for r in runs if r.get('event') == 'workflow_dispatch'
                  and r.get('main') == refs['main'] and r.get('head') == head
                  and r.get('workflow') == activation['workflow'] and r.get('operation') == operation['id']
                  and type(r.get('id')) is int and r['id'] > 0]
    if len(exact_runs) != 1 or exact_runs[0].get('status') != 'completed' or exact_runs[0].get('conclusion') != 'success':
        return {'status': 'blocked', 'reason': 'exact trusted successful validation run not observed',
                'operation': operation, 'head': head, 'publishable': False}
    run = exact_runs[0]
    if api.refs() != expected:
        return {'status': 'stale', 'reason': 'pins drifted during validation', 'publishable': False}
    latest_prs, _, latest_history = _owned_pulls(api, repository, activation, refs['main'], manual_history, refs)
    if _pull_snapshot(latest_prs) != _pull_snapshot(prs) or latest_history != history:
        return {'status':'stale', 'reason':'PR identity changed during validation', 'publishable':False}
    prs = [p for p in prs if p['state'] == 'open']
    if not prs:
        observe_write(lambda: api.create_pull(operation, head), api.pulls,
                      lambda observed: sum(_matches_pull(p, repository, operation, head) for p in observed) == 1)
    else:
        observe_write(lambda: api.update_pull(prs[0]['number'], operation, head), api.pulls,
                      lambda observed: sum(_matches_pull(p, repository, operation, head) and p.get('number') == prs[0]['number'] for p in observed) == 1)
    if api.refs() != expected:
        return {'status':'stale', 'reason':'pins drifted after PR mutation', 'publishable':False}
    if manual_history and _owned_pulls(api, repository, activation, refs['main'], manual_history, expected)[2] != history:
        return {'status':'stale', 'reason':'manual history changed after PR mutation', 'publishable':False}
    return {'version': 1, 'status': 'ready', 'operation': operation,
            'head': head, 'run_id': run['id'], 'manual_history':history, 'publishable': False}


class GitHubAdapter:
    """Fixed GitHub REST mapping; request is a trusted JSON transport, never shell."""
    WORKFLOW = 'staging-sync-validate.yml'

    def __init__(self, repository, request, *, poll_attempts=60, poll_seconds=5):
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
            raise ValueError('invalid repository')
        self.repository, self.request = repository, request
        self.prefix = 'repos/'+repository+'/'
        self.poll_attempts, self.poll_seconds = poll_attempts, poll_seconds
        self.waiting = False

    def dispatch(self, operation, head):
        self.waiting = True
        self.request('POST', self.prefix+'actions/workflows/'+self.WORKFLOW+'/dispatches',
                     {'ref': 'main', 'inputs': {key: operation[key]
                      for key in ('main', 'staging', 'tree', 'policy')} |
                      {'operation': operation['id'], 'head': head}})

    def pages(self, endpoint, field=None):
        from urllib.parse import urlencode
        rows = []
        for page in range(1, 51):
            separator = '&' if '?' in endpoint else '?'
            result = self.request('GET', self.prefix+endpoint+separator+urlencode({'per_page':100, 'page':page}))
            items = result[field] if field else result
            if not isinstance(items, list):
                raise RemoteError('invalid list response')
            rows.extend(items)
            if len(items) < 100:
                return rows
        raise RemoteError('complete remote inventory unavailable')

    def is_ancestor(self, ancestor, descendant):
        value = self.request('GET', self.prefix+'compare/'+ancestor+'...'+descendant)
        return value.get('status') in ('ahead', 'identical') and value.get('merge_base_commit', {}).get('sha') == ancestor

    def refs(self):
        from urllib.parse import quote
        result = {}
        for key, branch in [('main', 'main'), ('staging', 'staging'), ('branch', BRANCH)]:
            try:
                value = self.request('GET', self.prefix+'git/ref/heads/'+quote(branch, safe=''))
                result[key] = value['object']['sha']
                if not re.fullmatch('[0-9a-f]{40}', result[key]):
                    raise RemoteError('invalid remote ref')
            except RemoteError as error:
                if key == 'branch' and getattr(error, 'status', None) == 404:
                    result[key] = None
                else:
                    raise
        return result

    def commit(self, head):
        value = self.request('GET', self.prefix+'git/commits/'+head)
        marker = '\n\n0x1DEA-operation: '
        try:
            operation = json.loads(value['message'].split(marker, 1)[1])
        except (IndexError, ValueError):
            operation = {}
        return {'tree':value['tree']['sha'], 'parents':[p['sha'] for p in value['parents']],
                'owner':operation.get('owner') if operation.get('repository') == self.repository
                        and operation.get('branch') == BRANCH and operation.get('target') == 'staging' else None,
                'operation':operation.get('id')}

    def pull_identity(self, p):
        try:
            operation = json.loads((p.get('body') or '').split('\n\n0x1DEA-operation: ', 1)[1])
        except (ValueError, IndexError):
            operation = {}
        if not isinstance(operation, dict):
            operation = {}
        return {'number':p['number'], 'state':p['state'], 'base':p['base']['ref'],
                'head':p['head']['sha'], 'branch':p['head']['ref'],
                'repository':(p['head'].get('repo') or {}).get('full_name'),
                'owner':operation.get('owner'), 'operation':operation.get('id'),
                'merged':p.get('merged_at') is not None, 'base_sha':p['base'].get('sha'),
                'merge':p.get('merge_commit_sha'), 'tree':None,
                'actor':{key:(p.get('user') or {}).get(key) for key in ('id','login','type')}}

    def pulls(self):
        from urllib.parse import urlencode
        rows = self.pages('pulls?'+urlencode({'state':'all', 'head':self.repository.split('/')[0]+':'+BRANCH}))
        return [self.pull_identity(p) for p in rows]

    def pull_details(self, number):
        result = self.pull_identity(self.request('GET', self.prefix+'pulls/'+str(number)))
        if result['merged'] and result['merge']:
            result['tree'] = self.commit(result['merge'])['tree']
        return result

    def workflow(self, main):
        import base64
        value = self.request('GET', self.prefix+'contents/.github/workflows/'+self.WORKFLOW+'?ref='+main)
        if value.get('encoding') != 'base64':
            raise RemoteError('workflow content unavailable')
        raw = base64.b64decode(''.join(value['content'].split()), validate=True)
        return {'sha256':hashlib.sha256(raw).hexdigest(), 'main':main}

    def validation_runs(self, operation, head):
        import time
        title = 'staging-sync:'+operation['id']+':'+head
        for attempt in range(self.poll_attempts):
            rows = self.pages('actions/workflows/'+self.WORKFLOW+'/runs?event=workflow_dispatch', 'workflow_runs')
            found = [{'id':r['id'], 'event':r['event'], 'main':r['head_sha'],
                      'workflow':r['path'].split('@', 1)[0].removeprefix('.github/workflows/'),
                      'operation':operation['id'], 'head':head,
                      'status':r['status'], 'conclusion':r.get('conclusion')}
                     for r in rows if r.get('display_title') == title]
            if found and all(r['status'] == 'completed' for r in found):
                return found
            if not found and not self.waiting:
                return []
            if attempt+1 < self.poll_attempts:
                time.sleep(self.poll_seconds)
        return found

    def create_pull(self, operation, head):
        self.request('POST', self.prefix+'pulls', {'title':'🔧 chore: 同步 main 核准工程至 staging',
            'head':BRANCH, 'base':'staging', 'body':self.pull_body(operation, head)})

    def update_pull(self, number, operation, head):
        if type(number) is not int or number <= 0:
            raise RemoteError('invalid pull number')
        self.request('PATCH', self.prefix+'pulls/'+str(number), {'body':self.pull_body(operation, head)})

    @staticmethod
    def pull_body(operation, head):
        template = (Path(__file__).resolve().parents[1]/
                    'maintenance/publication-workflow/automation/sync-pr-template.md').read_text().rstrip()
        return template+'\n\nhead: '+head+'\n\n0x1DEA-operation: '+canonical(operation).decode().strip()

    def advance(self, head, previous):
        if not re.fullmatch('[0-9a-f]{40}', head):
            raise RemoteError('invalid branch head')
        if previous is None:
            self.request('POST', self.prefix+'git/refs', {'ref':'refs/heads/'+BRANCH, 'sha':head})
        else:
            self.request('PATCH', self.prefix+'git/refs/heads/'+BRANCH, {'sha':head, 'force':False})

    def upload(self, prepared, operation):
        import base64
        from publication_remote_git import load
        sync = load('staging-sync.py')
        store = Path(prepared['store'])
        entries = sync.identities(store, prepared['tree'])
        sync.check_source_blobs(store, {'trees':{'result':entries}})
        known = set(prepared['known_blobs'])
        for blob in sorted({e['blob'] for e in entries.values()} - known):
            raw = sync.git(store, 'cat-file', 'blob', blob).stdout
            value = self.request('POST', self.prefix+'git/blobs',
                                 {'encoding':'base64', 'content':base64.b64encode(raw).decode()})
            if value['sha'] != blob:
                raise RemoteError('uploaded blob identity mismatch')
        value = self.request('POST', self.prefix+'git/trees', {'tree':[
            {'path':path, 'mode':entry['mode'], 'type':'blob', 'sha':entry['blob']}
            for path,entry in sorted(entries.items())]})
        if value['sha'] != prepared['tree'] or operation['tree'] != prepared['tree']:
            raise RemoteError('uploaded tree differs from independent merge')
        identity = {'name':'0x1DEA Sync', 'email':'sync@example.invalid', 'date':'2000-01-01T00:00:00Z'}
        value = self.request('POST', self.prefix+'git/commits', {'tree':prepared['tree'],
            'parents':prepared['parents'], 'message':prepared['message'],
            'author':identity, 'committer':identity})
        if value['sha'] != prepared['head']:
            raise RemoteError('uploaded commit identity mismatch')


class GhTransport:
    """Fixed-host gh JSON transport with an explicit, filtered child environment."""
    def __init__(self, token, *, state_dir, executable=None, process=None):
        import shutil
        import subprocess
        self.executable = executable or shutil.which('gh')
        if not token or not self.executable:
            raise RemoteError('explicit writer credential and installed gh required')
        home = Path(state_dir)/'gh-auth'
        if any(p.is_symlink() for p in (home, *home.parents) if str(p) not in ('/var', '/tmp')):
            raise RemoteError('linked authentication directory')
        home.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.env = {'PATH':str(Path(self.executable).parent)+':/usr/bin:/bin',
                    'HOME':str(home), 'GH_CONFIG_DIR':str(home), 'GH_TOKEN':token,
                    'GH_HOST':'github.com', 'GH_PROMPT_DISABLED':'1', 'LANG':'en_US.UTF-8'}
        self.process = process or subprocess.run

    def __call__(self, method, endpoint, data=None):
        import subprocess
        if method not in ('GET', 'POST', 'PATCH') or not endpoint.startswith('repos/') or any(c in endpoint for c in ('\r', '\n', '\0', '\\')):
            raise RemoteError('unsupported API request')
        command = [self.executable, 'api', '--hostname', 'github.com', '--include', '--method', method,
                   '-H', 'Accept: application/vnd.github+json', '-H', 'X-GitHub-Api-Version: 2022-11-28', endpoint]
        if data is not None:
            command += ['--input', '-']
        try:
            result = self.process(command, input=json.dumps(data) if data is not None else None,
                                  env=self.env, capture_output=True, text=True, timeout=45)
        except (subprocess.TimeoutExpired, OSError) as error:
            raise RemoteError('GitHub transport unavailable', uncertain=method != 'GET') from error
        raw = result.stdout.replace('\r\n', '\n')
        header, separator, body = raw.partition('\n\n')
        match = re.match(r'HTTP/\S+ (\d{3})', header)
        if not match or not separator:
            raise RemoteError('GitHub response not established', uncertain=method != 'GET')
        status = int(match[1])
        if result.returncode or not 200 <= status < 300:
            raise RemoteError('GitHub request refused or failed', status=status,
                              uncertain=status >= 500 and method != 'GET')
        return json.loads(body) if body.strip() else {}
