# Traceability

| Type | Field | Boundary | Expected behavior | AC |
|---|---|---|---|---|
| Historical fixture | accepted epoch and negative cases | Python harness/current verifier | frozen lint input accepted; tampering and missing input reject | M1 |
| Release | pins, scope and complete diff | public CLI/Git objects | exact 34 product plus 11 evidence paths; real ancestry required | M2,M3,M4 |
| Current input | bytes, type, mode and inventory | public CLI/filesystem | exact successor; missing/link/mode/unknown/ignored reject | M2,M3 |
| Historical evidence | old boundaries, oracles and release evidence | public CLI/Git bytes | immutable; deleting or altering data cannot bypass checks | M3,M4 |
| Repair code | required sources | public CLI/filesystem | reviewed trust roots must be regular and present | M3 |
| Integrated result | commands, counts and independent review | actual repair checkout | full executed checks pass, no unresolved blockers | M5 |
