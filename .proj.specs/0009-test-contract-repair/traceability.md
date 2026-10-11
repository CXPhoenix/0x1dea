# Repair traceability

| Type | Field | Boundary | Expected behavior | AC |
|---|---|---|---|---|
| Historical fixture | product input bytes | immutable Git → current verifier CLI | later live edits cannot corrupt accepted fixture; missing object fails | V1 |
| Historical rejection | bytes/mode/path/provenance | disposable clone → CLI diagnostic | intended offending input is identified after positive control | V1,V3 |
| Article history | entry hash, migrated source | frozen data → Markdown/inverse conversion | original independent SHA and source links retained | V2 |
| Live article | figures/references/alt/src/frontmatter/citations | current source → public renderer | 3 figures, 6 refs, 8 alt/src, original frontmatter and source-note links | V2 |
| Live article | full bytes | captured Git → repair checkout | editorial content remains identical | V2 |
| Product successor | commits and complete delta | pinned Git → successor → guard | exact before/after identity and ancestor chain required | V3 |
| Repair successor | exact path set and identities | reviewed record → current inputs | no duplicate/unknown/missing entry or runtime auto-refresh | V3 |
| Original history | manifests and package semantics | old Git projection → old checks | original bytes/rules unchanged; current acceptance checked separately | V3 |
| Current inventory | byte/type/presence/unknown/ignored/link | filesystem → public verifier | changed and hidden unapproved input rejects | V3 |
| Test discovery | both packages and counts | unittest root / Python runner | both suites discovered; zero in either rejects | V4 |
| Test outcomes | fail/import/success | disposable test modules → runner/process | real results propagate nonzero/zero; aggregate executes both runtimes | V4 |
| Ticket views | status and dependency edges | tracker → CLI JSON | blocked todo only; unresolved in-flight edges still visible | V5 |
| Tracker validation | frontier/pending/cycle/missing/landing | local records → existing validator | established validation retained | V5,V6 |
| Existing ticket | authorization and containment | evidence → status | missing evidence remains review; no historical authorization inferred | V6 |
| Finder metadata | content identity and location | scanned tree → ignored local backup | exact single file preserved with matching hash and receipt | V7 |
| Delivery evidence | version, results and review scope | actual local commands → coverage/reports | fresh complete results; old observations not relabeled | V8 |
| Delivery authority | external actions | local task → publication boundary | no commit/push/deploy/install or external writes | V6,V8 |
| Rollback | coupled repair set, backup destination | disposable repaired copy → prior state | restore guard/data/tests/commands together; article/history unchanged; occupied destination never overwritten | V7 |
