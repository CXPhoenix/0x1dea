import hashlib,json,pathlib,re,datetime,sys
P=pathlib.Path(__file__).parent
han=lambda s: len(re.findall(r'[\u4e00-\u9fff]',s))
results=[]
def check(case,name,ok,actual):
 results.append(dict(case=case,check=name,passed=bool(ok),actual=actual))
freeze=json.loads((P/'freeze.json').read_text())
for f in freeze['files']:
 source=P/'frozen-v2'/f['path']
 b=source.read_bytes() if source.exists() else json.loads((P/'instruction-snapshot.json').read_text())[f['path']]['utf8'].encode('utf-8')
 check('freeze',f['path'],hashlib.sha256(b).hexdigest()==f['sha256'],hashlib.sha256(b).hexdigest())
for n in range(1,9):
 c=f'E{n}';d=P/'cases'/c
 if not (d/'output-v2.json').exists():continue
 i=json.loads((d/'input.json').read_text());o=json.loads((d/'output-v2.json').read_text());a=o['artifact']
 check(c,'json identity',o['case_id']==c,o['case_id'])
 if c=='E1':
  check(c,'180–320 Han characters',180<=han(a)<=320,han(a));check(c,'no heading',not re.search(r'^\s*#',a,re.M),a.count('\n'))
 elif c=='E2':
  original=i['materials']['article'];target='同一份資料也可能已經改變。失效策略要讓它失效，所以我們必須設計失效策略。';pre,post=original.split(target)
  check(c,'protected prefix/suffix exact',a.startswith(pre) and a.endswith(post),dict(prefix=a.startswith(pre),suffix=a.endswith(post)))
  check(c,'paragraph separators unchanged',a.count('\n\n')==original.count('\n\n'),a.count('\n\n'))
 elif c=='E3':
  words=len(a.split());check(c,'<=80 English whitespace words',words<=80,words);check(c,'one paragraph/no heading/question',not '\n' in a and not '?' in a and not a.startswith('#'),a)
 elif c=='E4':
  lines=a.splitlines();check(c,'three required labeled lines',len(lines)==3 and all(l.startswith(x) for l,x in zip(lines,['主旨','說明','擬辦'])),lines)
  check(c,'required facts literal',all(x in a for x in ['2026-10-03','20項','18項','2項','小林']),a)
 elif c=='E5':
  check(c,'only syntax repair/code block',a=='```python\ndef add(a, b):\n    return a + b\n```',a)
  check(c,'writer reports no style invocation',o['invoked_skill'] is False,o['invoked_skill'])
 elif c=='E6':
  body=a.split('\n\n')[0];check(c,'body120–220 Han characters',120<=han(body)<=220,han(body))
  check(c,'evidence/stance tokens',all(x in body for x in ['先不採用','單機','十次','200','120','尖峰','一致性']),body)
 elif c=='E7':
  body,caption=a.rsplit('\n\n',1);check(c,'body150–260 Han characters',150<=han(body)<=260,han(body));check(c,'one caption line',caption.startswith('圖說：') and '\n' not in caption,caption)
 elif c=='E8':
  m=re.fullmatch(r'A\n(.*?)\n\nB\n(.*)',a,re.S);check(c,'only A/B labels',bool(m),bool(m))
  if m:
   ca,cb=map(han,m.groups());check(c,'A50–90/B180–300 Han characters',50<=ca<=90 and 180<=cb<=300,dict(A=ca,B=cb))
report={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'mechanical format/length/protected-byte checks; not a style or semantic judge','count':len(results),'failures':sum(not x['passed'] for x in results),'checks':results}
if '--write-report' in sys.argv:
 (P/'mechanical-checks-v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':len(results),'failures':report['failures'],'case_counts':{c:sum(x['case']==c for x in results) for c in sorted(set(x['case'] for x in results))}},ensure_ascii=False))

raise SystemExit(1 if report['failures'] else 0)
