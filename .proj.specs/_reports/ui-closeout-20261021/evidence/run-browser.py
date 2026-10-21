from pathlib import Path
import subprocess,json,time
out=Path('/private/tmp/0x1dea-ui-closeout-evidence-20261021')
js=(out/'metrics.js').read_text();actions=[];metrics=[]
def run(*args,session='ticket-local',input=None):
 r=subprocess.run(['agent-browser','--session',session,*args],input=input,text=True,capture_output=True,timeout=40)
 actions.append({'args':list(args),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 (out/'local-browser-actions.json').write_text(json.dumps(actions,ensure_ascii=False,indent=2)+'\n')
 if r.returncode:raise RuntimeError(str(args)+r.stderr)
 return r.stdout
def measure(label):
 data=json.loads(json.loads(run('eval','--stdin',input=js)))
 data['label']=label;metrics.append(data)
 (out/'browser-metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
 assert data['pageWidth']<=data['viewport']+1,(label,'overflow')
 assert not data['duplicates'],(label,'duplicate ids')
 assert all(c['font']>=14 and c['contrast']>=4.5 and not c['clipped'] for c in data['captions']),(label,'caption metrics')
 assert all(n['contrast']>=4.5 and n['executable']==0 for n in data['notices']),(label,'notice safety')
 print(label,'passed',flush=True)
 return data
for width in [1280,360,390]:
 run('set','viewport',str(width),'900')
 for theme in ['light','dark']:
  run('set','media',theme)
  for page in ['__closeout_acceptance.html','post/course/security-awareness/electricity-privacy.html']:
   run('open','http://127.0.0.1:4380/'+page)
   # Theme preference is native media emulation, then observed DOM class.
   data=measure(f'{width}-{theme}-'+('fixture' if page.startswith('_') else 'article'))
   assert ('dark' in data['theme'])==(theme=='dark'),data['theme']
   run('screenshot',str(out/(data['label']+'.png')))
# Complete the compiled environment matrix against BOTH consumers after hydration.
for i,case in enumerate(['true-staging','absent-staging','false-main','absent-main','absent-absent','true-main']):
 for page in ['index.html','post/course/security-awareness/electricity-privacy.html']:
  run('open',f'http://127.0.0.1:{4380+i}/'+page)
  data=measure(case+'-'+('home' if page=='index.html' else 'article'))
  assert len(data['notices'])==(1 if case in ['true-staging','absent-staging','true-main'] else 0)
run('console');run('errors')
