# Coupled rollback validation

A disposable Git clone received all non-planning repair changes, then restored
all existing changed paths to captured HEAD and removed all newly added repair
paths. `git diff` was empty afterward; the runner and successor record were
absent. Article, nine original history/oracle records and pnpm lock remained
unchanged. The original current-config rejection returned, as expected.

The same copy restored Finder backup bytes using exclusive creation (`xb`), then
attempted a restore to a pre-existing destination. FileExistsError prevented the
overwrite and the pre-existing bytes remained unchanged. No real checkout rollback
was performed. Exact path inventory and outcomes: evidence/rollback.txt.
