# Owner-approved live fixture history alignment supplement

Date: 2026-10-21 (Asia/Taipei). Direct owner answer: 「同意追加此 fixture 修正並重跑完整測試」 to the explicit question allowing the current workflow admission fixture staging ref to follow actual staging. This expands original AC5 only for the setup ref; the original reviewed spec remains preserved.

Approved change: in tests/article_publication/test_workflow_admission.py setUp, replace the old fixed staging ref with SOURCE refs/heads/staging resolved through real Git to a full commit ID. The fixture copies current common and must retain actual done-ticket landing ancestry. No product verifier, tracker, old receipt, five frozen modules, runner, assertion, expected result or workflow execution changes.

D05 reuses the existing public native/prepare CLI and real Git seams. The prior source-v3 full failures are the red checkpoint: each live publication suite reports4 failures/1error from the shared stale setup. A pre-Discord baseline directly reproduces one shared-fixture case; remaining common-cause attribution follows full-run stack traces. Apply only the captured proposed patch, rerun affected existing cases, then the complete original runner separately on current main/staging. Keep all previous failures and independent historical results.

Existing local implementation/review authority continues. This supplement grants no commit, push, PR, merge, installation, workflow activation or deployment-setting change.
