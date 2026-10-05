from pathlib import Path
import hashlib,json,os,shutil,subprocess
root=Path(__file__).resolve().parent
candidate=root/'implementation-resumed'; disposable=root/'rollback-resumed'
fixed='ee7fecfff72f47abc735d26ac7e9a943de04ebbf'
assert disposable.parent==root and disposable.name=='rollback-resumed' and disposable.resolve()!=Path('{SOURCE_REPO}').resolve()
def git(*args, **kw): return subprocess.check_output(['git',*args],cwd=disposable,**kw)
assert git('rev-parse','HEAD').decode().strip()==fixed
assert not git('status','--porcelain=v1','-uall')
patch=subprocess.check_output(['git','diff','--binary','HEAD','--'],cwd=candidate)
(root/'evidence/resumed/rollback-applied.patch').write_bytes(patch)
subprocess.run(['git','apply','--binary','-'],input=patch,cwd=disposable,check=True)
new=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=candidate).split(b'\0')
count=0
for raw in new:
    if not raw: continue
    name=os.fsdecode(raw); src=candidate/name; target=disposable/name
    assert not src.is_symlink() and src.is_file(),name
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.is_symlink(): target.unlink()
    shutil.copyfile(src,target); count+=1
assert (disposable/'blog/.vitepress/config.mts').is_file()
assert not (disposable/'docs/.vitepress/config.mts').exists()
for runtime in ['.agents/skills','.claude/skills']:
    assert len([p for p in (disposable/runtime).iterdir() if p.is_dir()])==35
    assert not [p for p in (disposable/runtime).rglob('*') if p.is_symlink()]
status_before=git('status','--porcelain=v1','-uall').decode()
assert status_before
# These operations are confined to this explicitly disposable independent checkout.
reset=subprocess.run(['git','reset','--hard',fixed],cwd=disposable,check=True,capture_output=True,text=True)
clean=subprocess.run(['git','clean','-fd'],cwd=disposable,check=True,capture_output=True,text=True)
files=json.loads((candidate/'maintenance/harness-adoption/baseline-files.json').read_text())['files']
restored=[]
for f in files:
    path=disposable/f['path']; linked=path.is_symlink()
    assert linked==(f['type']=='symlink'),f
    data=os.readlink(path).encode() if linked else path.read_bytes()
    sha=hashlib.sha256(data).hexdigest(); assert sha==f['sha256'],f
    restored.append({'path':f['path'],'type':f['type'],'sha256':sha})
assert not git('status','--porcelain=v1','-uall')
assert not (disposable/'blog').exists()
assert (disposable/'docs/.vitepress/config.mts').is_file()
result={'status':'pass','surface':'real independent disposable Git checkout restore','disposable':'rollback-resumed','baseline':fixed,'applied_tracked_patch_sha256':hashlib.sha256(patch).hexdigest(),'copied_new_regular_files':count,'adopted_runtime_skills':35,'pre_reset_status':status_before,'actual_reset_argv':['git','reset','--hard',fixed],'reset_stdout':reset.stdout,'actual_clean_argv':['git','clean','-fd'],'clean_stdout':clean.stdout,'restored_entries':restored,'git_clean':True,'unit_cli_build':'subsequent distinct real runs required'}
print(json.dumps(result,ensure_ascii=False,indent=2))
