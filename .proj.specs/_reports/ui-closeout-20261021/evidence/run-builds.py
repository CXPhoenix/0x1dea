from pathlib import Path
import subprocess,os,json,time
root=Path('/private/tmp/0x1dea-ui-closeout-stage-20261021');out=Path('/private/tmp/0x1dea-ui-closeout-evidence-20261021')
base={k:v for k,v in os.environ.items() if k not in ('VITE_SITE_NOTICE_ENABLED','CF_PAGES_BRANCH')}
cases=[('true-staging','true','staging'),('absent-staging',None,'staging'),('false-main','false','main'),('absent-main',None,'main'),('absent-absent',None,None),('true-main','true','main')]
records=[]
for label,flag,branch in cases:
 env=base.copy()
 if flag is not None:env['VITE_SITE_NOTICE_ENABLED']=flag
 if branch is not None:env['CF_PAGES_BRANCH']=branch
 cmd=['pnpm','exec','vitepress','build','blog','--outDir',str(out/'builds'/label)]
 start=time.time()
 with (out/(label+'-build.log')).open('w') as log:r=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
 record={'case':label,'command':cmd,'exit_code':r.returncode,'seconds':round(time.time()-start,2),'env':{k:env.get(k) for k in ('VITE_SITE_NOTICE_ENABLED','CF_PAGES_BRANCH')}}
 records.append(record);(out/'build-matrix.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps(record),flush=True)
 if r.returncode:break
