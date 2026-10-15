# Reconciliation matrix

| Type × field × boundary | Expected observable behavior | AC |
|---|---|---|
| History × epoch × original source/manifest | pinned historical checks pass; old manifests unchanged | R1,R4 |
| Current × clean staging × known evolution | CLI reaches full history/tracker checks | R2 |
| Current × approved component delta × exact bytes | integrated candidate passes required CLI | R2 |
| Current × product/new path × unknown/untracked | nonzero CLI, offending path diagnosed | R3 |
| Current × source × changed/missing/symlink | nonzero CLI; no file/ref mutation | R3,R5 |
| Provenance × pin × missing/wrong/non-ancestor | reject before projection | R4 |
| Provenance × manifest × changed scope/path/hash | reject; no automatic rebaseline | R4 |
| Current × approved source × subsequent stale edit | reject and require fresh review | R3,R4 |
| History × missing approval × present-day reconciliation | label reconciliation date, retain historic gap | R1,R5 |
| Recovery × rollback × successor removed | old fail-closed verifier restored, product unchanged | R5 |
| Management × tracker/translation/trace/runtime × invalid | retained current management checks reject | R2,R6 |
