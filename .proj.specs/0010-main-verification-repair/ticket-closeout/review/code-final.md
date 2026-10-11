# T-0012 independent implementation review

## Scope

Two native independent read-only reviewers received the same frozen final WIP packet: main base/HEAD/merge-base eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a on tickets/T-0012/ticket-evidence-closeout; staging c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7 on tickets/T-0011/main-to-staging-sync. Committed/staged layers empty; tracked WIP plus all untracked entries captured (300 main, 115 staging). Manifest copies capture-main.json/capture-staging.json identify all input hashes. Five historical binary copies on main match staging blobs; no new visual behavior asserted. New HTML only statically inspected due browser file-navigation policy.

## Standards

Documented-standard breaches P0/P1/P2=0/0/0; actionable smells=0. Exact T1 successor plus receipt/approval identities preserve the historical inventory (scripts/main_publication_verification.py:139-147). Public CLI tests preserve every old assertion. Coverage distinguishes fresh native checks from historical product/browser runs and missing acceptance evidence; T12 stays review.

Reviewer identified a fixture risk for Spec adjudication: test_main_release.py:55 unconditionally created staging after clone, so SOURCE currently on staging already had that branch. This was not classified as a documented-standard breach.

## Spec

Initial captured review found no omissions in conditional closure, exact identity boundaries, target-specific article preservation or corrected test-plan/traceability mappings. Independent comparison found all 185 imported historical management files byte-identical to staging base; original constants and assertions retained. C4 remote delivery requires actual readback after push, not this review.

Supplemental review confirmed the fixture risk as P1 under C3: parent reproduced the original test error with SOURCE on staging (branch-reproduction-red.txt), then changed only helper line55 to git branch -f staging <same pinned SHA>. Unchanged setUp detaches the disposable clone before this command; only fixture-local ref changes. Same source-branch scenario now passes (branch-reproduction-green.txt: 1 test, 24.858s). Both reviewers independently compared this exact one-line delta and confirmed original assertions/runtime guard unchanged. P1 resolved; residual Spec P0/P1/P2=0/0/0.

## Drift and verification limits

Parent checked every captured file hash, HEAD, status and diff before the fixture correction: no drift. Supplemental reviews cover only that declared one-line correction and reproduction logs. Later additions are these reports, capture/verification summaries and ticket links; the user research also corrects current GitHub GITHUB_TOKEN PR-event exceptions against freshly read official docs; no unreviewed runtime change. Complete final harness results after correction are separately bound in harness-final-main/staging.json and coverage-report.md; prior full runs are retained as history, not substituted for final runs. Reviewers read evidence but did not rerun tests. No fresh product/browser/CI/deployment claim. Missing historical acceptance artifacts remain missing. Final branch/base/open/auto-merge state is read back during authorized delivery.
