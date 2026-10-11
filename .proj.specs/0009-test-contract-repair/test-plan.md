# Owner-approved test plan

Approved on 2026-10-11 in approval.md; copied from the six-row discovery proposal.
AC identifiers name the same approved intent, not new testing seams.

| Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|
| Existing Python verifier CLI in disposable Git clones | historical accepted inputs stay valid after later source changes; negative cases reach the intended offending path | component/revision fixtures and public CLI | V1,V3 | changed live article/theme, missing object, wrong pin, byte/mode/link/missing source, unknown and ignored paths |
| Existing VitePress renderer and article source checks | current article preserves semantic figures/references/citations; historical conversion uses frozen input | existing article-caption suite | V2 | three figures, six references, eight alt/src pairs, source links, independent historical hash; current prose remains byte-identical |
| Existing current public preservation CLI | accept only the exact reviewed successor without altering old manifests | captured product and repair delta | V3,V7 | before/after hash, record digest, ancestry, extra/ignored source, linked source and changed historical manifest; preserved Finder metadata receipt; coupled disposable rollback and no-clobber restore |
| Local test command subprocess | run both Python suites and aggregate with Vitest; propagate failure and reject zero discovery | existing runtimes, no dependency installation | V4 | success, failing suite, import failure, zero tests; no test logic copied into the runner |
| Existing tracker/public CLI JSON | documented views agree with status and dependency rules | todo/processing/review/done/pending and unresolved edges | V5,V6 | unresolved dependencies remain visible, true blocked todo, invalid landing receipt, missing id and cycle |
| Existing complete project commands | final integrated state is verified and reports reference the executed state | full Vitest and both Python suites, lint, build, structure, materializer and current verifier | V8 | run on the repair checkout; no silent skips, historical passes reused as current, or external deployment claim |
