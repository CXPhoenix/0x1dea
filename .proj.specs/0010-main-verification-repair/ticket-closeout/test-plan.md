# Reused approved test plan

The owner already approved T-0010's existing public verifier, tracker/Git and complete-command seams and now authorizes evidence closeout and both unmerged PRs. No new interface is introduced.

| Seam | Intent | Scope | AC | Boundaries |
|---|---|---|---|---|
| Existing verifier CLI in disposable real Git clones | Original and exact done successor accepted | Existing main release fixture with actual adoption commit and local staging ref | C2 | Exact bytes/mode/regular path; arbitrary prose/status/receipt path rejected |
| Existing tracker/landing CLI | Hash approval is insufficient without landing evidence | Real JSON receipt and approval file | C2 | Missing/false/wrong-ticket/wrong-target/missing-object/nonancestor, wrong valid ancestor and unrelated existing approval rejected |
| Existing Python suites and native validators | Both target-specific sources pass | Main and staging clones, fixed remote target pins | C3 | Zero skips, immutable manifests and all blog paths unchanged |
| Existing GitHub delivery readback | Correct two open PRs | T-0012 canonical branch → main; T-0011 projection branch → staging | C4 | No merge, no auto-merge, no force push, exact diff scope |
