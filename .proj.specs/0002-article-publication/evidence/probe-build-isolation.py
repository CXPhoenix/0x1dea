"""Synthetic read/write/network sentinel verification only."""
import errno
import json
from pathlib import Path
import socket
import sys
working=Path(sys.argv[1]);outside=Path(sys.argv[2])
report={'inside_read':False,'outside_read_denied':False,'outside_write_denied':False,'network_denied':False}
report['inside_read']=(working/'inside-sentinel.txt').read_text()=='SYNTHETIC_ALLOWED_SENTINEL\n'
for action,key in [(lambda:outside.read_text(),'outside_read_denied'),(lambda:outside.write_text('overwrite'),'outside_write_denied')]:
 try:action()
 except PermissionError:report[key]=True
try:
 with socket.socket() as probe:probe.connect(('127.0.0.1',9))
except OSError as exc:
 report['network_denied']=exc.errno in (errno.EACCES,errno.EPERM)
report['status']='pass' if all(report.values()) else 'blocked'
(working/'isolation-sentinel-result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
raise SystemExit(0 if report['status']=='pass' else 1)
