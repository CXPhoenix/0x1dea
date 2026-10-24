# Future publication, rollback and re-publication

This reference specifies later work. Phase 1 has no implementation for these actions.

## Publish

Require explicit authorization for the selected article branch, exact current main SHA,
article head SHA and declared dependency heads. Re-run preparation, source/diff checks,
isolated build, output/index checks and independent review if any pin or candidate changed.
Create the eventual PR to main from the selected article branch and required explicit
shared dependency changes only. Combined staging is a public preview integration branch;
it is never merged back into articles or published as a whole. Keep unselected source,
routes, indexes and assets out of the candidate. A preparation receipt or skill invocation
is not permission to commit, push, create a PR, merge or deploy.

Verify the actual official site and intended article/index/assets after an authorized
publication; a staging preview does not establish official publication. Preserve the
before/after main and deployed revision evidence and report any mismatch.

## Rollback

Require fresh authorization for the precise published revision and intended revert.
From current main create a new reviewed revert, accounting for later hotfixes, shared
assets/configuration, indexes and other articles. Prepare/build/review it and verify the
site after the authorized rollback. Use no reset, force push or whole-staging replacement.
Keep unrelated published changes intact. Specify follow-up evidence if shared dependencies
must remain because another article uses them.

## Re-publication after revert

An old already-merged article branch alone may introduce no new content. Build a new
candidate from current main that explicitly reapplies the intended article changes,
with reviewed dependencies and conflict resolution. Pin the new main and new head;
run prepare/build/source-output checks/review again. Obtain new exact-candidate publication
authorization and verify the official site afterward. Previous authorization and previous
build receipts do not automatically cover the new candidate.
