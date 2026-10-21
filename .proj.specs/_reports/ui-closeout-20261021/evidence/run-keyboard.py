from pathlib import Path
import subprocess,json
out=Path('/private/tmp/0x1dea-ui-closeout-evidence-20261021');actions=[]
def run(*args,input=None):
 r=subprocess.run(['agent-browser','--session','ticket-local',*args],input=input,text=True,capture_output=True,timeout=35)
 actions.append({'args':list(args),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});(out/'keyboard-spa-actions.json').write_text(json.dumps(actions,ensure_ascii=False,indent=2)+'\n')
 if r.returncode:raise RuntimeError(str(args)+r.stderr)
 return r.stdout
def ev(js):return json.loads(json.loads(run('eval',js)))
run('set','viewport','1280','900');run('set','media','light');run('open','http://127.0.0.1:4380/__closeout_acceptance.html')
run('snapshot','-i','-u')
for href in ['#fig-first-proof','#tbl-first-table']:
 selector='a[href="'+href+'"]'
 run('focus',selector);run('press','Shift+Tab');run('press','Tab')
 focused=ev('JSON.stringify({href:document.activeElement.getAttribute("href"),outline:getComputedStyle(document.activeElement).outline,rect:document.activeElement.getBoundingClientRect().toJSON()})')
 assert focused['href']==href,focused
 run('screenshot',str(out/('focus-'+href[1:]+'.png')))
 run('press','Enter');result=ev('JSON.stringify({hash:location.hash,target:!!document.getElementById(location.hash.slice(1))})');assert result['hash']==href and result['target']
run('eval','window.__closeoutSpaProbe="ticket-closeout-20261021"')
run('click','a[href="/post/course/security-awareness/electricity-privacy.html"]');run('wait','--fn',"location.pathname.endsWith('/electricity-privacy.html')")
spa=ev('JSON.stringify({probe:window.__closeoutSpaProbe,url:location.href,figures:document.querySelectorAll("figure").length,references:document.querySelectorAll("a[href^=\\"#fig-\\"]").length,ids:[...document.querySelectorAll("[id]")].map(x=>x.id).filter((id,i,a)=>a.indexOf(id)!==i)})')
assert spa['probe']=='ticket-closeout-20261021' and spa['figures']==3 and spa['references']==6 and not spa['ids'],spa
selector='a[href="/post/course/cybersec/what-is-safety"]'
run('focus',selector);run('press','Shift+Tab');run('press','Tab')
f=ev('JSON.stringify({href:document.activeElement.getAttribute("href"),outline:getComputedStyle(document.activeElement).outline,descendants:document.activeElement.querySelectorAll("a,button,input").length})');assert f['href']=='/post/course/cybersec/what-is-safety' and '3px' in f['outline'] and f['descendants']==0,f
run('screenshot',str(out/'focus-encore.png'));run('press','Enter');run('wait','--fn',"location.pathname.includes('/what-is-safety')")
run('snapshot','-i','-u');run('console');run('errors')
run('open','http://127.0.0.1:4380/__closeout_acceptance.html')
run('snapshot');print('Native Tab/Enter figure, table, Encore navigation and SPA probe passed',flush=True)
