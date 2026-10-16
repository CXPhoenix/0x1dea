"""Checked local job inputs; never provisions runners or proves remote capabilities."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import stat
import subprocess
import sys
import tempfile

import publication_current as current
import publication_remote as remote
from publication_remote_git import load

CONTROL = Path(__file__).resolve().parents[1]
CREDENTIALS = ('PUBLICATION_WRITER_TOKEN', 'PUBLICATION_REPORTER_TOKEN', 'GH_TOKEN', 'GITHUB_TOKEN')


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate job input key')
        result[key] = value
    return result


def exact(value, fields):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError('job input schema: unknown or missing fields')


def location(value, *, outside=()):
    if not isinstance(value, (str, Path)):
        raise ValueError('canonical absolute job path required')
    path = Path(value)
    if not path.is_absolute() or path != path.resolve():
        raise ValueError('canonical absolute job path required; no symlinks')
    for p in (path, *path.parents):
        if p.is_symlink():
            raise ValueError('linked job input path')
    if any(path.is_relative_to(Path(root).resolve()) for root in outside):
        raise ValueError('job input overlaps source, state or snapshot')
    return path


def read_exact(path, expected, *, sealed_root=None):
    path = location(path)
    if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
        raise ValueError('independently supplied job input digest required')
    before = path.lstat()
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise ValueError('job input opened identity/type changed')
        if sealed_root is not None and (
                not path.is_relative_to(sealed_root) or path == sealed_root
                or opened.st_uid != os.geteuid() or stat.S_IMODE(opened.st_mode) != 0o400
                or opened.st_nlink != 1):
            raise ValueError('job snapshot file ownership/mode/link/containment mismatch')
        with os.fdopen(fd, 'rb', closefd=False) as handle:
            raw = handle.read()
        after = os.fstat(fd)
        keys = ('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns')
        if (any(getattr(opened, key) != getattr(after, key) for key in keys)
                or hashlib.sha256(raw).hexdigest() != expected):
            raise ValueError('job input digest or read identity changed')
    finally:
        os.close(fd)
    return raw


def probe_isolation(node, dependencies):
    """Observe the host boundary without executing candidate code or writing Git."""
    if sys.platform != 'darwin' or not Path('/usr/bin/sandbox-exec').is_file():
        raise ValueError('enforced macOS isolation unavailable; no fallback')
    with tempfile.TemporaryDirectory(prefix='job-isolation-') as tmp:
        root = Path(tmp).resolve()
        workspace = root/'workspace'; workspace.mkdir()
        inside = workspace/'inside'; inside.write_text('INSIDE')
        outside = root/'outside'; outside.write_text('OUTSIDE')
        target = root/'outside-write'
        quote = json.dumps
        reads = [workspace, dependencies, node.parent.parent, Path('/System'), Path('/usr/lib'),
                 Path('/usr/share'), Path('/usr/bin'), Path('/bin')]
        profile = root/'probe.sb'
        profile.write_text('(version 1)\n(deny default)\n'
            '(allow process* sysctl-read file-read-metadata)\n(allow file-read-data (literal "/"))\n'
            +'\n'.join('(allow file-read-data (subpath '+quote(str(p))+'))' for p in reads)
            +'\n(allow file-read-data file-write-data (literal "/dev/null") (literal "/dev/tty"))\n')
        listener = socket.socket()
        try:
            listener.bind(('127.0.0.1',0)); listener.listen()
            port = listener.getsockname()[1]
            script = ("const fs=require('node:fs'),net=require('node:net');"
                +"const r={inside:fs.readFileSync("+quote(str(inside))+",'utf8')==='INSIDE'};"
                +"for(const [k,f] of [['outside_read',()=>fs.readFileSync("+quote(str(outside))+")],"
                +"['outside_write',()=>fs.writeFileSync("+quote(str(target))+",'bad')]])"
                +"{try{f();r[k]='allowed'}catch(e){r[k]=['EPERM','EACCES'].includes(e.code)?'denied':e.code}}"
                +f"const c=net.connect({port},'127.0.0.1');c.setTimeout(1500);"
                +"c.on('connect',()=>{r.network='allowed';c.destroy();console.log(JSON.stringify(r))});"
                +"c.on('error',e=>{r.network=['EPERM','EACCES'].includes(e.code)?'denied':e.code;console.log(JSON.stringify(r))});"
                +"c.on('timeout',()=>{r.network='unverified';c.destroy();console.log(JSON.stringify(r))});")
            result = subprocess.run(['/usr/bin/sandbox-exec','-f',str(profile),str(node),'-e',script],
                cwd=workspace,capture_output=True,text=True,timeout=20,
                env={'PATH':str(node.parent)+':/usr/bin:/bin','LANG':'en_US.UTF-8'})
        finally:
            listener.close()
        if result.returncode:
            raise ValueError('enforced isolation host probe failed')
        observed = json.loads(result.stdout.strip())
        if (observed != {'inside':True,'outside_read':'denied','outside_write':'denied','network':'denied'}
                or outside.read_text() != 'OUTSIDE' or target.exists()):
            raise ValueError('enforced isolation sentinels failed')
        return observed


def runtime_ready(runtime, pnpm):
    exact(runtime, ('version','node','node_version','dependencies'))
    exact(pnpm, ('path','version'))
    if (sys.version_info[:2] < (3,11) or type(runtime['version']) is not int
            or runtime['version'] != 1 or runtime['node_version'] != 'v24.13.0'
            or pnpm['version'] != '10.28.0'):
        raise ValueError('Python 3.11+, Node 24.13.0 and pnpm 10.28.0 required; no install')
    node = location(runtime['node']); dependencies = location(runtime['dependencies'])
    package_manager = location(pnpm['path'])
    if not node.is_file() or not package_manager.is_file() or not dependencies.is_dir():
        raise ValueError('installed Node/pnpm/dependencies missing; no install')
    vitepress = (dependencies/'vitepress/bin/vitepress.js').resolve()
    if not vitepress.is_file() or not vitepress.is_relative_to(dependencies):
        raise ValueError('installed dependency containment unavailable')
    env = {'PATH':str(node.parent)+':/usr/bin:/bin','LANG':'en_US.UTF-8'}
    for executable, expected in ((node,'v24.13.0'),(package_manager,'10.28.0')):
        result = subprocess.run([str(executable),'--version'],capture_output=True,text=True,env=env,timeout=20)
        if result.returncode or result.stdout.strip() != expected:
            raise ValueError('installed Node/pnpm version mismatch')
    return probe_isolation(node, dependencies)


def check_state(directory, expected, repository, source, pins):
    directory = location(directory, outside=(CONTROL, source))
    info = directory.stat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
        raise ValueError('durable state directory must be job-owned and private')
    identity = json.loads(read_exact(directory/'identity.json',expected),object_pairs_hook=unique_object)
    exact(identity, ('version','repository','store_id'))
    if (type(identity['version']) is not int or identity['version'] != 1 or identity['repository'] != repository
            or not isinstance(identity['store_id'],str) or not re.fullmatch('[0-9a-f]{64}',identity['store_id'])):
        raise ValueError('durable state repository/identity mismatch')
    journal = directory/(hashlib.sha256(repository.encode()).hexdigest()+'.json')
    if journal.exists() or journal.is_symlink():
        path = location(journal)
        value = json.loads(path.read_bytes(),object_pairs_hook=unique_object)
        operation = value.get('operation') or value.get('last_preparation',{}).get('operation')
        if (not isinstance(operation,dict) or operation.get('repository') != repository
                or operation != remote.operation_for(repository,operation.get('policy'),operation,
                                                       operation.get('tree'))):
            raise ValueError('durable journal operation identity unknown')
        if (type(operation.get('version')) is not int or operation['version'] != 1
                or any(not isinstance(operation.get(key),str)
                       or not re.fullmatch('[0-9a-f]{'+str(64 if key == 'policy' else 40)+'}',operation[key])
                       for key in ('main','staging','tree','policy'))):
            raise ValueError('durable journal source identity malformed')
        try:
            for side in ('main','staging'):
                current.git(source,'merge-base','--is-ancestor',operation[side],pins[side])
            prior_policy = current.git(source,'show',operation['main']+':'+current.POLICY)
        except subprocess.CalledProcessError as error:
            raise ValueError('durable journal source ancestry unknown') from error
        if hashlib.sha256(prior_policy).hexdigest() != operation['policy']:
            raise ValueError('durable journal source policy identity mismatch')
    return directory


def materialize_job(path, expected_digest, *, repository, role):
    if any(os.environ.get(key) for key in CREDENTIALS):
        raise ValueError('job preflight must not receive API credentials')
    if role not in ('writer','validator') or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',repository):
        raise ValueError('trusted job role/repository required')
    raw_manifest = read_exact(path, expected_digest)
    config = json.loads(raw_manifest,object_pairs_hook=unique_object)
    exact(config, ('version','repository','role','main','staging','policy_sha256','source',
                   'registry','runtime','pnpm','snapshot_root','state_directory','state_identity_sha256'))
    if type(config['version']) is not int or config['version'] != 1 or config['repository'] != repository or config['role'] != role:
        raise ValueError('trusted job repository/role mismatch')
    for name in ('main','staging','policy_sha256'):
        length = 64 if name == 'policy_sha256' else 40
        if not isinstance(config[name],str) or not re.fullmatch('[0-9a-f]{'+str(length)+'}',config[name]):
            raise ValueError('full job source/policy pins required')
    source = location(config['source'])
    output = location(config['snapshot_root'],outside=(CONTROL,source,config['state_directory']))
    location(path,outside=(CONTROL,source,output,config['state_directory']))
    if output.exists():
        raise ValueError('fresh job snapshot root required')
    current.check_history(source)
    sync = load('staging-sync.py')
    raw_inputs = {}
    for name in ('registry','runtime'):
        item = config[name]; exact(item, ('path','sha256'))
        location(item['path'],outside=(CONTROL,source,output,config['state_directory']))
        raw_inputs[name] = read_exact(item['path'],item['sha256'])
    registry = sync.load_registry(raw_inputs['registry'])
    if (registry['repository'] != str(source)
            or any(registry[side]['sha'] != config[side] for side in ('main','staging'))):
        raise ValueError('job registry/source pins mismatch')
    sync.check_refs(registry)
    for side in ('main','staging'):
        if sync.identities(source,config[side]) != registry['trees'][side]:
            raise ValueError('job full tree identity mismatch')
    policy_raw = current.git(source,'show',config['main']+':'+current.POLICY)
    if hashlib.sha256(policy_raw).hexdigest() != config['policy_sha256']:
        raise ValueError('job trusted policy identity mismatch')
    state = check_state(config['state_directory'],config['state_identity_sha256'],repository,source,config)
    runtime = json.loads(raw_inputs['runtime'],object_pairs_hook=unique_object)
    isolation = runtime_ready(runtime,config['pnpm'])
    with tempfile.TemporaryDirectory(prefix='job-independent-tree-') as temporary:
        result = sync.compute(registry,Path(temporary)/'result.git')
    sync.check_refs(registry)
    operation = remote.operation_for(repository,config['policy_sha256'],config,result['result_tree'])
    binding = {'version':1,'repository':repository,'role':role,'snapshot_root':str(output),
        'operation':operation,'manifest_sha256':expected_digest,
        'registry_sha256':config['registry']['sha256'],'runtime_sha256':config['runtime']['sha256'],
        'state_directory':str(state),'state_identity_sha256':config['state_identity_sha256'],
        'writer_group':'publication-writers-'+repository.lower(),
        'validation_group':'publication-validation-'+repository.lower(),'cancel_in_progress':False,
        'isolation':isolation,'publishable':False,
        'surface':'local job input preparation; no remote capability proof'}
    output.mkdir(mode=0o700)
    try:
        for name,raw in {'manifest':raw_manifest,**raw_inputs,'binding':canonical(binding)}.items():
            target = output/(name+'.json'); target.write_bytes(raw); target.chmod(0o400)
        sync.check_refs(registry)
        output.chmod(0o500)
    except Exception:
        output.chmod(0o700); shutil.rmtree(output); raise
    return dict(binding,binding_sha256=hashlib.sha256(canonical(binding)).hexdigest())


def verify_job(snapshot_root, expected_binding, *, repository, role, include_inputs=False):
    if any(os.environ.get(key) for key in CREDENTIALS):
        raise ValueError('job input verification must not receive API credentials')
    root = location(snapshot_root,outside=(CONTROL,))
    info = root.stat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.geteuid()
            or stat.S_IMODE(info.st_mode) != 0o500):
        raise ValueError('job snapshot directory ownership/mode mismatch')
    if {p.name for p in root.iterdir()} != {'binding.json','manifest.json','registry.json','runtime.json'}:
        raise ValueError('job snapshot file inventory mismatch')
    binding = json.loads(read_exact(root/'binding.json',expected_binding,sealed_root=root),
                         object_pairs_hook=unique_object)
    exact(binding, ('version','repository','role','snapshot_root','operation','manifest_sha256',
                    'registry_sha256','runtime_sha256','state_directory','state_identity_sha256',
                    'writer_group','validation_group','cancel_in_progress','isolation','publishable','surface'))
    if (type(binding['version']) is not int or binding['version'] != 1
            or role not in ('writer','validator') or binding['role'] != role
            or binding['repository'] != repository or binding['snapshot_root'] != str(root)
            or binding['writer_group'] != 'publication-writers-'+repository.lower()
            or binding['validation_group'] != 'publication-validation-'+repository.lower()
            or binding['cancel_in_progress'] is not False or binding['publishable'] is not False):
        raise ValueError('job snapshot role/repository/source binding mismatch')
    config = json.loads(read_exact(root/'manifest.json',binding['manifest_sha256'],sealed_root=root),
                        object_pairs_hook=unique_object)
    if (config['repository'] != repository or config['role'] != role
            or config['snapshot_root'] != str(root) or config['state_directory'] != binding['state_directory']
            or config['state_identity_sha256'] != binding['state_identity_sha256']
            or config['registry']['sha256'] != binding['registry_sha256']
            or config['runtime']['sha256'] != binding['runtime_sha256']):
        raise ValueError('job snapshot manifest/input binding mismatch')
    source = location(config['source'])
    location(root,outside=(source,config['state_directory']))
    current.check_history(source)
    sync = load('staging-sync.py')
    registry = sync.load_registry(read_exact(root/'registry.json',binding['registry_sha256'],sealed_root=root))
    runtime = json.loads(read_exact(root/'runtime.json',binding['runtime_sha256'],sealed_root=root),
                         object_pairs_hook=unique_object)
    if (registry['repository'] != str(source)
            or any(registry[side]['sha'] != config[side] for side in ('main','staging'))):
        raise ValueError('job snapshot registry/source identity mismatch')
    sync.check_refs(registry)
    if hashlib.sha256(current.git(source,'show',config['main']+':'+current.POLICY)).hexdigest() != config['policy_sha256']:
        raise ValueError('job snapshot trusted policy changed')
    check_state(config['state_directory'],config['state_identity_sha256'],repository,source,config)
    observed = runtime_ready(runtime,config['pnpm'])
    if binding['isolation'] != observed:
        raise ValueError('job snapshot isolation observation mismatch')
    with tempfile.TemporaryDirectory(prefix='job-verify-tree-') as temporary:
        result = sync.compute(registry,Path(temporary)/'result.git')
    sync.check_refs(registry)
    if binding['operation'] != remote.operation_for(repository,config['policy_sha256'],config,result['result_tree']):
        raise ValueError('job snapshot operation recomputation mismatch')
    result = dict(binding,binding_sha256=expected_binding,status='pass')
    if include_inputs:
        result['checked_inputs'] = {'registry':registry,'runtime':runtime}
    return result
