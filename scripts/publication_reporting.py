"""Trusted reporting contract. Replayed API observations never prove live enforcement."""
import base64
import hashlib
import re
import os
import json
from pathlib import Path
import stat
import tempfile
import subprocess

from publication_remote import canonical, operation_for, RemoteError, GitHubAdapter, writer_lock


class GitHubReportingAdapter:
    """Read-only REST seam; controller-owned transport, never a dispatch artifact."""
    def __init__(self, repository, request, *, verify_inputs=None):
        self.verify_inputs = verify_inputs
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
            raise ValueError('invalid reporting repository')
        self.repository, self.request = repository, request
        self.prefix = 'repos/'+repository+'/'
        self.inventory = GitHubAdapter(repository, request)

    def get(self, path):
        return self.request('GET', self.prefix+path)

    def content(self, path, main):
        value = self.get('contents/'+path+'?ref='+main)
        if value.get('encoding') != 'base64':
            raise ValueError('report source content unavailable')
        return hashlib.sha256(base64.b64decode(''.join(value['content'].split()),validate=True)).hexdigest()

    def rulesets(self):
        # Include inherited rules. Missing/hidden bypass information is not proof
        # of non-bypass; deliberately refuse rather than infer team/custom roles.
        rows = self.inventory.pages('rulesets?includes_parents=true')
        seen, details = set(), []
        for row in rows:
            identity = row.get('id') if isinstance(row,dict) else None
            if type(identity) is not int or identity <= 0 or identity in seen:
                raise ValueError('complete unique ruleset identity unavailable')
            seen.add(identity)
            item = self.get('rulesets/'+str(identity)+'?includes_parents=true')
            if (not isinstance(item,dict) or type(item.get('id')) is not int or item['id'] != identity
                    or item.get('enforcement') not in ('active','disabled','evaluate')
                    or item.get('source_type') not in ('Repository','Organization','Enterprise')
                    or not isinstance(item.get('source'),str) or not item['source']
                    or item.get('target') not in ('branch','tag','push')):
                raise ValueError('ruleset source/bypass observation unavailable')
            details.append(item)
        return sorted(details,key=lambda item:item['id'])

    def observe(self, expected):
        if self.verify_inputs is not None:self.verify_inputs()
        operation = expected['operation']
        observed = {'pull':self.get('pulls/'+str(expected['pull'])),
            'main':self.get('git/ref/heads/main')['object']['sha'],
            'staging':self.get('git/ref/heads/staging')['object']['sha'],
            'commit':self.get('git/commits/'+expected['head']),
            'policy':self.content('maintenance/publication-workflow/engineering-v1.json',operation['main']),
            'workflow':self.content(expected['workflow'],operation['main']),
            'run':self.get('actions/runs/'+str(expected['run_id'])),
            'protection':self.get('branches/staging/protection'),
            'rulesets':self.rulesets(),
            'actor':self.get('collaborators/'+expected['landing_actor']+'/permission')}
        # Bracket the multi-request observation; this is still not a lock/CAS.
        observed['pull'] = self.get('pulls/'+str(expected['pull']))
        observed['main'] = self.get('git/ref/heads/main')['object']['sha']
        observed['staging'] = self.get('git/ref/heads/staging')['object']['sha']
        if self.verify_inputs is not None:self.verify_inputs()
        return observed

    def runs(self, expected):
        rows = self.inventory.pages('actions/workflows/'+expected['workflow'].removeprefix('.github/workflows/')+'/runs?event=workflow_dispatch','workflow_runs')
        title = 'staging-sync:'+expected['operation']['id']+':'+expected['head']
        return [r for r in rows if isinstance(r,dict) and r.get('display_title') == title]

    def checks(self, expected):
        return self.inventory.pages('commits/'+expected['head']+'/check-runs?filter=all','check_runs')


class CheckReporter:
    """A separate reporting transport; only one configured check request is exposed."""
    def __init__(self, repository, request, *, app_id, role):
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repository):
            raise ValueError('invalid reporting repository')
        self.repository, self.request = repository, request
        self.app_id, self.role = app_id, role

    def publish(self, payload):
        if self.role != 'reporter':raise ValueError('separate reporter role required')
        return self.request('POST','repos/'+self.repository+'/check-runs',payload)


def _expected(value):
    fields = {'repository','pull','operation','head','workflow','workflow_sha256','run_id',
              'run_attempt','check','reporter_app_id','landing_actor','landing_actor_id'}
    if not isinstance(value,dict) or set(value) != fields:
        return False
    if any(type(value[k]) is not int or value[k] <= 0 for k in
           ('pull','run_id','run_attempt','reporter_app_id','landing_actor_id')):
        return False
    if (not isinstance(value['head'],str) or not re.fullmatch('[0-9a-f]{40}',value['head'])
            or not isinstance(value['workflow_sha256'],str)
            or not re.fullmatch('[0-9a-f]{64}',value['workflow_sha256'])
            or not isinstance(value['workflow'],str)
            or not re.fullmatch(r'\.github/workflows/[A-Za-z0-9][A-Za-z0-9_.-]*\.(?:yml|yaml)',value['workflow'])
            or not isinstance(value['check'],str) or not 1 <= len(value['check']) <= 255
            or any(c in value['check'] for c in ('\r','\n','\0'))
            or not isinstance(value['landing_actor'],str)
            or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_\[\]-]{0,99}',value['landing_actor'])):
        return False
    op = value['operation']
    return (isinstance(op,dict) and type(op.get('version')) is int and op['version'] == 1
        and all(isinstance(op.get(k),str) and re.fullmatch('[0-9a-f]{'+str(n)+'}',op[k])
                for k,n in [('main',40),('staging',40),('tree',40),('policy',64),('id',64)]))


def _binding(observed, expected):
    operation = expected['operation']
    pull, run, commit = (observed[key] for key in ('pull','run','commit'))
    return (operation == operation_for(expected['repository'],operation['policy'],operation,operation['tree'])
        and pull['number'] == expected['pull'] and pull['state'] == 'open'
        and pull['base']['ref'] == 'staging' and pull['base']['sha'] == operation['staging']
        and pull['head']['repo']['full_name'] == expected['repository']
        and pull['head']['ref'] == operation['branch']
        and pull['head']['sha'] == expected['head']
        and observed['main'] == operation['main'] and observed['staging'] == operation['staging']
        and commit['tree']['sha'] == operation['tree']
        and {operation['main'],operation['staging']} <= {p['sha'] for p in commit['parents']}
        and observed['policy'] == operation['policy'] and observed['workflow'] == expected['workflow_sha256']
        and type(run['id']) is int and type(run['run_attempt']) is int
        and run['id'] == expected['run_id'] and run['run_attempt'] == expected['run_attempt']
        and run['status'] == 'completed' and run['conclusion'] == 'success'
        and run['event'] == 'workflow_dispatch' and run['head_sha'] == operation['main']
        and run['head_branch'] == 'main' and run['path'] == expected['workflow']
        and run['repository']['full_name'] == expected['repository']
        and run['head_repository']['full_name'] == expected['repository']
        and run['display_title'] == 'staging-sync:'+operation['id']+':'+expected['head'])


def _exact_check(row, payload, app_id, check_id=None):
    return (isinstance(row,dict) and type(row.get('id')) is int and row['id'] > 0
        and (check_id is None or row['id'] == check_id)
        and type(row.get('app',{}).get('id')) is int and row['app']['id'] == app_id
        and all(row.get(key) == payload[key] for key in ('name','head_sha','external_id','status','conclusion')))


def _capable(observed, expected):
    protection, actor = observed['protection'], observed['actor']
    checks = protection.get('required_status_checks',{})
    return (checks.get('strict') is True
        and protection.get('enforce_admins',{}).get('enabled') is True
        and [c for c in checks.get('checks',[]) if c.get('context') == expected['check']]
            == [{'context':expected['check'],'app_id':expected['reporter_app_id']}]
        and actor.get('permission') == 'write' and actor.get('role_name') == 'write'
        and all(isinstance(item.get('bypass_actors'),list)
                and (item['enforcement'] != 'active' or item['bypass_actors'] == [])
                for item in observed['rulesets'])
        and actor.get('user',{}).get('login') == expected['landing_actor']
        and actor.get('user',{}).get('id') == expected['landing_actor_id']
        and actor.get('user',{}).get('site_admin') is False)


def _capability_key(observed):
    actor = observed['actor']
    identity = {'permission':actor.get('permission'),'role_name':actor.get('role_name'),
                'user':{key:actor.get('user',{}).get(key) for key in ('id','login','site_admin')}}
    return hashlib.sha256(canonical({'protection':observed['protection'],
        'rulesets':observed['rulesets'],'actor':identity})).hexdigest()


def _drift(observed, expected):
    operation = expected['operation']
    if observed['pull']['head']['sha'] != expected['head']:
        return 'head'
    if observed['staging'] != operation['staging'] or observed['pull']['base']['sha'] != operation['staging']:
        return 'staging'
    if observed['main'] != operation['main']:
        return 'main'
    if observed['policy'] != operation['policy']:
        return 'policy'
    if observed['workflow'] != expected['workflow_sha256']:
        return 'workflow'
    return None


def _report_validation(api, reporter, expected, *, state_dir, live=False):
    """Only explicit trusted expected bindings are accepted; no merge is ever attempted."""
    blocked = {'status':'blocked','local_ready':False,'live_ready':False,'publishable':False,
               'reason':'report binding/permission/outcome not established',
               'surface':'local API contract; live enforcement unverified','fresh_validation_required':True}
    try:
        if live:
            return dict(blocked,reason='live capability is not established by local API fixtures; independent P13 observation required')
        if not _expected(expected):return blocked
        if (api.repository != expected['repository'] or reporter.repository != api.repository
                or reporter.role != 'reporter' or type(reporter.app_id) is not int
                or reporter.app_id != expected['reporter_app_id']
                or any(os.environ.get(k) for k in ('PUBLICATION_WRITER_TOKEN','PUBLICATION_REPORTER_TOKEN','GH_TOKEN','GITHUB_TOKEN'))):
            return blocked
        before = api.observe(expected)
        drift = _drift(before,expected)
        if drift:
            return dict(blocked,reason=drift+' drift; fresh independent validation required')
        if not _binding(before,expected) or not _capable(before,expected) or api.runs(expected) != [before['run']]:
            return blocked
        payload = {'name':expected['check'],'head_sha':expected['head'],
            'status':'completed','conclusion':'success',
            'external_id':hashlib.sha256(canonical(expected)).hexdigest()}
        journal = state_dir/(payload['external_id']+'.json')
        prior = None
        check_id = None
        capability = _capability_key(before)
        if journal.exists() or journal.is_symlink():
            metadata = journal.lstat()
            if (not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1
                    or metadata.st_uid != os.geteuid() or stat.S_IMODE(metadata.st_mode) != 0o600):
                return blocked
            with os.fdopen(os.open(journal,os.O_RDONLY|os.O_NOFOLLOW),'r') as handle:
                prior = json.load(handle)
            if (not isinstance(prior,dict) or set(prior) != {'binding','status','check_id','capability'}
                    or prior['binding'] != payload['external_id']
                    or prior['status'] not in ('pending','confirmed')
                    or prior['capability'] != capability
                    or (prior['status'] == 'pending' and prior['check_id'] is not None
                        and (type(prior['check_id']) is not int or prior['check_id'] <= 0))
                    or (prior['status'] == 'confirmed' and (type(prior['check_id']) is not int or prior['check_id'] <= 0))):
                return blocked
            check_id = prior['check_id']
        rows = [r for r in api.checks(expected) if r.get('name') == expected['check']]
        if rows and (len(rows) != 1 or not _exact_check(rows[0],payload,expected['reporter_app_id'],check_id)):
            return blocked
        if rows:
            check_id = rows[0]['id']
            _save(journal,{'binding':payload['external_id'],'status':'pending','check_id':check_id,'capability':capability})
        before_write = api.observe(expected)
        drift = _drift(before_write,expected)
        if drift:
            return dict(blocked,reason=drift+' drift; fresh independent validation required')
        if before_write != before or not _binding(before_write,expected) or not _capable(before_write,expected):
            return blocked
        if not rows:
            if prior is not None:
                return dict(blocked,reason='previous report outcome unconfirmed; exact readback required before retry')
            _save(journal,{'binding':payload['external_id'],'status':'pending','check_id':None,'capability':capability})
            try:
                acknowledged = reporter.publish(payload)
                if not _exact_check(acknowledged,payload,expected['reporter_app_id']):
                    return blocked
                check_id = acknowledged['id']
                _save(journal,{'binding':payload['external_id'],'status':'pending','check_id':check_id,'capability':capability})
            except RemoteError as error:
                if not error.uncertain:
                    return blocked
        rows = [r for r in api.checks(expected) if r.get('name') == expected['check']]
        if len(rows) != 1 or not _exact_check(rows[0],payload,expected['reporter_app_id'],check_id):
            return blocked
        check_id = rows[0]['id']
        _save(journal,{'binding':payload['external_id'],'status':'pending','check_id':check_id,'capability':capability})
        direct = api.get('check-runs/'+str(rows[0]['id']))
        if not _exact_check(direct,payload,expected['reporter_app_id'],check_id) or direct['id'] != rows[0]['id']:
            return blocked
        after = api.observe(expected)
        drift = _drift(after,expected)
        if drift:
            return dict(blocked,reason=drift+' drift; fresh independent validation required')
        if (after != before or not _binding(after,expected) or not _capable(after,expected)
                or api.runs(expected) != [after['run']]):
            return blocked
        _save(journal,{'binding':payload['external_id'],'status':'confirmed','check_id':rows[0]['id'],'capability':capability})
        return dict(blocked,status='ready',local_ready=True,check_id=rows[0]['id'],
                    reason='exact successful candidate check observed; local observation only',fresh_validation_required=False,
                    binding=payload['external_id'],guarantee='point-in-time observation; no lock, base CAS, merge authority or later-main guarantee')
    except (ValueError,KeyError,TypeError,RemoteError):
        return blocked


def _save(path, value):
    fd, temporary = tempfile.mkstemp(prefix='.report-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as handle:
            handle.write(canonical(value));handle.flush();os.fsync(handle.fileno())
        os.replace(temporary,path)
        directory = os.open(path.parent,os.O_RDONLY)
        try:os.fsync(directory)
        finally:os.close(directory)
    finally:
        if os.path.exists(temporary):os.unlink(temporary)


def report_validation(api, reporter, expected, *, state_dir=None, live=False):
    """Separate trusted reporter + explicit durable state; no candidate input selects authority.

    This adapter implements the approved local request/refusal contract only.
    Even real-looking replayed rule/capability envelopes cannot satisfy live=True.
    Actual effective bypass/ruleset/token behavior needs independent P13 evidence.
    """
    blocked = {'status':'blocked','local_ready':False,'live_ready':False,'publishable':False,
        'fresh_validation_required':True,'reason':'report input/state binding not established',
        'surface':'local API contract; live enforcement unverified'}
    try:
        if live:
            return dict(blocked,reason='live capability is not established by local API fixtures; independent P13 observation required')
        from publication_jobs import location
        if not _expected(expected):return blocked
        expected = json.loads(canonical(expected))
        if state_dir is None:return blocked
        path = location(state_dir,outside=(Path(__file__).resolve().parents[1],))
        with writer_lock(path,api.repository):
            info = path.stat()
            if info.st_uid != os.geteuid() or stat.S_IMODE(info.st_mode) != 0o700:return blocked
            return _report_validation(api,reporter,expected,state_dir=path)
    except (ValueError,KeyError,TypeError,AttributeError,OSError,subprocess.CalledProcessError,RemoteError):
        return blocked


def report_from_job(api, reporter, *, control, snapshot_root, binding_sha256, admission, config, live=False):
    """Consume real A/B public interfaces before the reporter's independent API reads.

    The controller supplies config and independent digests outside candidate data.
    No dispatch artifact or candidate executable chooses source roles or authority.
    """
    blocked = {'status':'blocked','local_ready':False,'live_ready':False,'publishable':False,
        'fresh_validation_required':True,'reason':'sealed reporter source binding not established',
        'surface':'local API contract; live enforcement unverified'}
    try:
        if live:
            return dict(blocked,reason='live capability requires independent P13 observation')
        from publication_jobs import verify_job, exact, location
        from publication_workflows import WorkflowAdmission
        if not isinstance(admission,WorkflowAdmission):return blocked
        import publication_current as current
        exact(config,('repository','pull','head','workflow','run_id','run_attempt','check',
                      'reporter_app_id','landing_actor','landing_actor_id'))
        checked = verify_job(snapshot_root,binding_sha256,repository=config['repository'],
                             role='validator',include_inputs=True)
        operation = checked['operation']
        control = location(control)
        if (str(control) != checked['checked_inputs']['registry']['repository']
                or current.git(control,'rev-parse','HEAD').decode().strip() != operation['main']
                or admission.repository != operation['repository'] or admission.main != operation['main']):
            return blocked
        allowed = admission.allowed(control)
        workflow = allowed.get(config['workflow'])
        if not workflow or workflow['mode'] != '100644':
            return blocked
        tree = current.git(control,'show','-s','--format=%T',config['head']).decode().strip()
        parents = current.git(control,'show','-s','--format=%P',config['head']).decode().strip().split()
        if tree != operation['tree'] or not {operation['main'],operation['staging']} <= set(parents):
            return blocked
        expected = dict(config,operation=operation,workflow_sha256=workflow['sha256'])
        def verify_inputs():
            again = verify_job(snapshot_root,binding_sha256,repository=config['repository'],role='validator')
            if (again['operation'] != operation or admission.allowed(control) != allowed
                    or current.git(control,'rev-parse','HEAD').decode().strip() != operation['main']):
                raise ValueError('reporter source inputs drifted')
        bound_api = GitHubReportingAdapter(api.repository,api.request,verify_inputs=verify_inputs)
        return report_validation(bound_api,reporter,expected,state_dir=Path(checked['state_directory'])/'reporting')
    except (ValueError,KeyError,TypeError,AttributeError,OSError,subprocess.CalledProcessError,RemoteError):
        return blocked


def check_reporter_from_environment(repository, app_id, state_dir, *, process=None):
    """Consume only the explicit reporter secret; never enlarge a writer/build token."""
    token = os.environ.pop('PUBLICATION_REPORTER_TOKEN',None)
    if (not token or type(app_id) is not int or app_id <= 0
            or any(os.environ.get(key) for key in ('PUBLICATION_WRITER_TOKEN','GH_TOKEN','GITHUB_TOKEN'))):
        raise ValueError('separate explicit reporter credential required')
    from publication_jobs import location
    from publication_remote import GhTransport
    root = location(state_dir,outside=(Path(__file__).resolve().parents[1],))
    transport = GhTransport(token,state_dir=root,process=process)
    return CheckReporter(repository,transport,app_id=app_id,role='reporter')
