from pathlib import Path
import hashlib,json,os,subprocess
root=Path(__file__).resolve().parent;repo=root/'implementation-resumed';packet=root/'review-resumed/code-round-2';meta=json.loads((packet/'manifest.json').read_text());allowed=meta['post_review_closeout_paths']
def permitted(name):return any(name==p or (p.endswith('/') and name.startswith(p)) for p in allowed)
def current(name):
 p=repo/name
 if p.is_symlink():return {'type':'symlink','sha256':hashlib.sha256(os.readlink(p).encode()).hexdigest()}
 if p.is_dir():return {'type':'directory-replacing-baseline-link'}
 if not p.exists():return {'type':'absent'}
 return {'type':'regular','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
addendum=root/'review-resumed/code-round-2-guide-addendum'; amended=json.loads((addendum/'manifest.json').read_text())
assert hashlib.sha256((addendum/'manifest.json').read_bytes()).hexdigest()=='8c2db57b874beceecac71436c8b419f659434e67892de5038043456cd54568b4'
for f in amended['files']:
 assert current(f['path'])=={'type':'regular','sha256':f['sha256']}, f'guide addendum drift: {f["path"]}'
changes=[]
for entry in meta['files']:
 observed=current(entry['path']);old={k:entry[k] for k in observed}
 if observed!=old:changes.append(entry['path']);assert permitted(entry['path']) or entry['path']=='docs/guide.md',f'unreviewed drift: {entry["path"]}'
paths=set(filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=repo).decode().split('\0')))|set(filter(None,subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=repo).decode().split('\0')))
paths.update(str(p.relative_to(repo)) for p in (repo/'maintenance/harness-adoption/evidence').rglob('*') if p.is_file() or p.is_symlink())
new=sorted(paths-{f['path'] for f in meta['files']});assert all(permitted(p) for p in new),f'unreviewed additions: {new}'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()==meta['base']
assert subprocess.check_output(['git','branch','--show-current'],cwd=repo).decode().strip()==meta['branch']
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=repo)
assert hashlib.sha256((packet/'manifest.json').read_bytes()).hexdigest()=='e84119fb6d4478e51c7ef1bbed54987cfc93299b44165dcb5a66a38dc7b7ca34'
print(json.dumps({'status':'pass','review_packet_sha256':'e84119fb6d4478e51c7ef1bbed54987cfc93299b44165dcb5a66a38dc7b7ca34','frozen_entries':len(meta['files']),'allowed_closeout_changes':changes,'allowed_closeout_additions':new,'code_spec_source_changes_since_review':[],'documentation_change_reviewed_in_addendum':['docs/guide.md'],'guide_addendum_sha256':'8c2db57b874beceecac71436c8b419f659434e67892de5038043456cd54568b4','head':meta['head'],'branch':meta['branch'],'staged_changes':[]},indent=2))
