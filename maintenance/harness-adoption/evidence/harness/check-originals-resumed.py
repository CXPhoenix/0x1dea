from pathlib import Path
import hashlib,importlib.util,json,os,platform,subprocess
root=Path(__file__).resolve().parent
sources={
 'product':(Path('{SOURCE_REPO}'),'ee7fecfff72f47abc735d26ac7e9a943de04ebbf'),
 'template':(Path('{TEMPLATE_REPO}'),'917e6025da0901a79dda016e1ce5bd89b6e6e19f')}
result={}
for name,(repo,wanted) in sources.items():
 def git(*args):return subprocess.check_output(['git',*args],cwd=repo,timeout=20)
 head=git('rev-parse','HEAD').decode().strip();assert head==wanted
 status=git('status','--porcelain=v1','-uall').decode();assert not status
 branch=git('branch','--show-current').decode().strip()
 regular,linked=0,0; manifest=[]
 for entry in git('ls-tree','-r','-z',head).split(b'\0'):
  if not entry:continue
  meta,rawname=entry.split(b'\t',1);mode,kind,blob=meta.decode().split();name_=rawname.decode();p=repo/name_
  raw=os.readlink(p).encode() if mode=='120000' else p.read_bytes()
  assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==blob
  if mode=='120000':linked+=1
  else:
   regular+=1
   if name=='template':assert (root/'vendor-resumed'/name_).read_bytes()==raw
  manifest.append({'path':name_,'type':'symlink' if mode=='120000' else 'regular','sha256':hashlib.sha256(raw).hexdigest(),'git_blob':blob})
 result[name]={'head':head,'branch':branch,'git_clean':True,'tracked_regular':regular,'tracked_symlink':linked,'files':manifest}
 if name=='product':assert git('rev-parse','staging','origin/staging').decode().split()==[wanted,wanted]
assert result['template']['tracked_regular']==737
spec=importlib.util.spec_from_file_location('pinned_bundle',root/'vendor-resumed/harness_agile/bundle.py')
bundle=importlib.util.module_from_spec(spec);spec.loader.exec_module(bundle)
snapshot=bundle.snapshot(sources['template'][0])
assert len(snapshot['files'])==718
assert snapshot['source']['content_sha256']=='b7782890459cf3c546395ac5546f22dc074f13d4166688751a9c1e08d4216bf5'
assert snapshot['source']['commit']==sources['template'][1] and snapshot['source']['dirty'] is False
candidate=root/'implementation-resumed'; baseline=root/'rollback-resumed'; source=sources['product'][0]
deps={}
for file in ['pnpm-lock.yaml','node_modules/.modules.yaml','node_modules/.pnpm/lock.yaml']:
 shas=[hashlib.sha256((p/file).read_bytes()).hexdigest() for p in [source,candidate,baseline]]
 assert len(set(shas))==1
 deps[file]=shas[0]
assert not (candidate/'node_modules').is_symlink() and not (baseline/'node_modules').is_symlink()
versions={label:subprocess.check_output(argv,cwd=candidate,env={**os.environ,'COREPACK_ENABLE_NETWORK':'0'},timeout=20).decode().strip() for label,argv in [('node',['{EXISTING_NODE_BIN}/node','-v']),('pnpm',['{EXISTING_NODE_BIN}/pnpm','-v'])]}
assert versions=={'node':'v24.13.0','pnpm':'10.28.0'}
print(json.dumps({'status':'pass','original_sources':result,'dependency_snapshot_sha256':deps,'runtime_versions':versions,'python':platform.python_version(),'template_regular_worktree_matches_owned_vendor':True,'original_snapshot_recomputed':snapshot['source'],'original_snapshot_file_count':len(snapshot['files']),'original_snapshot_digest_received':'b7782890459cf3c546395ac5546f22dc074f13d4166688751a9c1e08d4216bf5','digest_note':'Fresh pinned bundle.snapshot PATHS selects 718 files and reproduces the approved digest; separate Git check verifies all 737 tracked regular template files against pinned blobs and owned vendor bytes.','original_repos_written':False},indent=2))
