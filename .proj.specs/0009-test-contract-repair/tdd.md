# Implementation loop

The six-row owner-approved table in test-plan.md was used without a new seam.
No old test was removed or skipped. Tests use real Git, subprocesses and the
public Markdown renderer; no mocked guard success or expected-value refresh.

| Behavior | Red evidence | Minimum change / green evidence |
|---|---|---|
| historical component CLI | fixture-red.txt: config/theme fixture rejection | pin all overlay product bytes to the recorded Git epoch; same test passed |
| historical article revision CLI | original diagnostic run: acceptance plus 12 subtest failures | pin revision inputs to f93237b; all 16 reconciliation methods passed |
| article migration | article-red.txt: mutable article no longer contains old captions | retain independent baseline, reconstruct/freeze source and migrated data; separate live article case, all 87 Vitest tests passed |
| runner success | runner-red.txt: entrypoint absent | standard-library real discovery, results and two explicit suites |
| runner zero suite | runner-zero-red.txt: exit 0 despite zero tests | require positive testsRun in each suite |
| runner unimportable package | runner-discovery-red.txt: second suite not run | catch discovery ImportError/OSError, report failure and continue |
| runner fail/import cases | already correctly handled by real unittest result | 4 runner methods passed, including either suite failing and the other still running |
| tracker views | tracker-red.txt: review/processing incorrectly listed blocked | todo-only blocked plus all-status unresolved_dependencies; 30 tracker methods passed |
| current source CLI | successor-red.txt: preserved current config rejected | exact 15-path captured delta plus 8 repair data paths, immutable digest, original provenance and Git ancestry |
| source tamper | existing guard rejected earlier invalid sources | current successor counterexamples added after successful positive control; final aggregate results are in coverage-report.md |

Frozen fixture provenance explicitly labels present-day reconstruction, not a
recovered historical execution artifact. The original oracle and article bytes
remain unchanged. Record freezing was a one-time implementation operation outside
the shipped verifier; no runtime update or bypass command was added.

Review correction: missing runner, missing successor test and linked runner each
incorrectly returned pass (one method, three failure records) in
evidence/code-presence-red.txt. Requiring regular CODE files only when the repair
record exists fixes all three; evidence/code-presence-green.txt passes. Historical
epochs do not require code added later. Final full aggregate is rerun after this
correction. No data record identity or product source was changed by this fix.
