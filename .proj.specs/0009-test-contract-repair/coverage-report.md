# T-0009 coverage report

Worktree: /Users/phoenix/dev/online-notes/0x1DEA. Branch:
`tickets/T-0009/test-contract-repair`. Base/HEAD/merge-base:
`6e4eb804bcbda8504935be49fd6537d6327d5303`; implementation is uncommitted WIP.
Final `pnpm test` after the independent-review correction exited 0:
**87 Vitest cases, 81 harness Python methods, 16 publication Python methods**.
Python failures=0, errors=0; no skips. Root discovery independently finds all
97 Python methods. Counts are testsRun, not numbers of subtest failure records.

| Seam | Tests / measured result | Covered behavior | AC | Limits |
|---|---|---|---|---|
| historical verifier CLI | 16 methods passed in final aggregate | fixed epochs; exact success; intended diagnostics; bytes/mode/missing/link/unknown/ignored/provenance/ancestry | V1,V3 | real disposable Git clones; no remote execution |
| renderer/article | 26 article-caption cases; complete Vitest 87/87 | historical inverse SHA/source links; current 3 figures/6 refs/8 alt-src/frontmatter/citations and article SHA | V2 | public Markdown renderer; no new browser claim |
| current preservation CLI | 7 methods passed | exact 15 product + 8 repair paths, frozen record, history, missing/nonancestor Git, required records, data byte/type/presence, ignored extra source; missing runner/test and linked runner reject | V3 | reviewed code content is trust root, not self-hash authenticated; presence/type required |
| runner/process | 4 methods passed | either suite fails/imports/zero/unimportable, both execute, positive counts, bytecode-free | V4 | testsRun and failure/error records reported separately |
| tracker | 30 methods passed | todo-only blocked, all-status unresolved edges, existing frontier/pending/cycle/missing id/landing validators | V5,V6 | authentic human authorization needs manual source check; no existing ticket closed |
| Finder and rollback | disposable clone checks passed, evidence/rollback.txt | exact backup, coupled reversion, prior rejection returns, no-clobber restore | V7 | actual backup remains ignored/local; no real checkout rollback |
| integrated commands | final pnpm test, lint, build, structure, materializer, verifier passed | complete installed runtimes and actual current CLI | V8 | final independent Standards/Spec/security review closed with no remaining findings |

The complete first aggregate passed before review, then the CODE presence/type
regression reproduced three failure records in one method and passed after the
minimal correction. The final full aggregate above includes that new method.
Build/lint inputs remained identical through this Python-only review correction;
the successful build/lint executions apply to those same final inputs. Structure,
materializer and public verifier were rerun after the correction.

No line/branch coverage percentage was measured. No test was removed or skipped.
No installs, external index changes, commit, push, landing or deploy were performed.
The source article, nine original history/oracle records and pnpm lock match the
pre-implementation identities in evidence/preservation.json. `environment.json`
records installed versions and successor digest; full results are in
`evidence/full-test-final.txt`, build.txt, lint.txt, structure-final.txt,
materializer-final.txt and guard-final.txt.

Initial independent Standards review found the late coverage table; it now exists
before final stage-6 review. Initial Spec review found CODE presence/type; all
three public regression scenarios pass and the final aggregate includes them.
Initial security review found no new HIGH/MEDIUM candidate; dependency scanning,
DoS/rate limiting, low-severity hardening, deployment and external services are
excluded. Final reports record the refreshed packet and dispositions.

## Final review closure

Standards and Spec each have P0=0/P1=0/P2=0; both initial P1 findings are closed.
The separate security supplement has no new HIGH/MEDIUM candidate. See
review/code-T-0009.md and review/security-T-0009.md. Reviewers confirmed all 73
captured files and HEAD had no drift. These disposition outputs and ticket
checkboxes were appended after review, without changing implementation.
The actual local public CLI is the tooling end-to-end surface; no fresh browser,
native skill discovery, CI or deployment claim is made.

## Authorized landing update

The owner subsequently authorized done and staging push. Actual remote landing
and current permission are recorded in landing.json and landing-approval.md.
Earlier local-only observations remain historical; reports/staging-closeout.html
and review/chain-analysis.md complete the epic close-out. No main or separate
deployment operation was performed.
