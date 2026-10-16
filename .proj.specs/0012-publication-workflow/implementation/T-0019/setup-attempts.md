# Verification setup attempts

Two earlier full-suite attempts did not complete successfully: the first lacked the canonical dependency environment (the clone dependency links resolve outside its copied root); the second supplied canonical installed dependencies but the parent process could not bind the loopback listener under the outer sandbox. Original raw logs remain in the local session evidence. These failures are not passes. Subsequent full runs explicitly supply the existing canonical dependency root and permit only the parent host loopback probe; deny-default sandbox-exec remains enforced for the child build/probes.

The synthetic-article-readiness.json artifact is an existing local synthetic article ready report, not an isolation probe receipt. Real build/isolation behavior is covered by the named successful public test cases in python-full.txt. No artifact here proves Actions, P13 or deployment.

A subsequent v3 run was interrupted after reproducing a missing-successor failure: renaming the synthetic readiness evidence left its obsolete exact-map entry. The renamed document map was repaired without changing the historical fixtures or policy behavior; the final clean full run is authoritative.
