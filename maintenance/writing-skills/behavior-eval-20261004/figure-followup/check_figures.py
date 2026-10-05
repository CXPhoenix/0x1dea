import json,pathlib,hashlib,re,argparse
P=pathlib.Path(__file__).parent
parser=argparse.ArgumentParser();parser.add_argument('--history-root',type=pathlib.Path,default=P.parent);parser.add_argument('--write-report',action='store_true');args=parser.parse_args();checks=[]
def add(name,ok,actual=None):checks.append(dict(check=name,passed=bool(ok),actual=actual))
for name in ['instruction-snapshot.json','instruction-snapshot-v22.json']:
 for path,x in json.loads((P/name).read_text()).items():add(name+':'+path,hashlib.sha256(x['utf8'].encode()).hexdigest()==x['sha256'])
for c,version in [('E7','v21'),('E9','v21'),('E7','v22')]:
 d=P/'cases'/c;p=d/f'output-{version}.json'
 if not p.exists():continue
 o=json.loads(p.read_text());a=o['artifact'];han=lambda s:len(re.findall(r'[\u4e00-\u9fff]',s));add(c+version+' identity',o['case_id']==c)
 if c=='E7':
  body,cap=a.rsplit('\n\n',1);add(c+version+' 150–260 Han',150<=han(body)<=260,han(body));add(c+version+' caption',cap.startswith('圖說：') and '\n' not in cap);add(c+version+' old gaze literals absent',not any(x in a for x in ['先盯著','往右看','視線拉回']))
 else:
  lines=[x for x in a.splitlines() if x.strip()];add(c+version+' 80–160 Han',80<=han(a)<=160,han(a));add(c+version+' steps+caption',len(lines)==3 and lines[0].startswith('1.') and lines[1].startswith('2.') and lines[2].startswith('圖說：'));add(c+version+' requested guide',all(x in a for x in ['先找出','再對照']))
 j=d/f'judgment-{version}.json'
 if j.exists():
  j=json.loads(j.read_text());rubric=json.loads((d/'rubric.json').read_text());expected='pass' if not j['hard_failures'] and all(x['score']>=1 for x in j['criteria']) and j['total']>=8 else 'fail';add(c+version+' judgment data integrity',len(j['criteria'])==5 and [x['criterion'] for x in j['criteria']]==rubric['criteria'] and sum(x['score'] for x in j['criteria'])==j['total'] and expected==j['verdict'])
qa=json.loads((P/'parent-qa-correction.json').read_text())
ledger_path=P.parents[1]/'publication-manifest.json'
ledger=json.loads(ledger_path.read_text())['files'] if ledger_path.exists() else {}
def preserved(path, raw_hash):
 p=args.history_root/path
 if not p.exists():return False
 b=p.read_bytes();actual=hashlib.sha256(b).hexdigest()
 if actual==raw_hash:return True
 row=ledger.get('behavior-eval-20261004/'+path,{})
 return (row.get('raw_sha256')==raw_hash and row.get('published_sha256')==actual
         and row.get('transformation')=='local path metadata normalization'
         and hashlib.sha256(json.loads(b)['artifact'].encode()).hexdigest()==row.get('artifact_sha256'))
add('original32 identity or declared metadata-only publication projection',all(preserved(path,h) for path,h in qa['unchanged_original_json_hashes'].items()))
report=dict(method='mechanical only; judgment integrity is checked, semantic/style verdict is not recomputed',checks=checks,total=len(checks),failures=sum(not x['passed'] for x in checks))
if args.write_report:(P/'mechanical-checks-final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False));raise SystemExit(1 if report['failures'] else 0)
