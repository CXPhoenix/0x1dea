# Owner approval

On 2026-10-11 the owner selected prototype D, the encore ticket, and asked for a reusable component applied to the electricity/privacy article.

The owner then approved the single tracer-bullet T-0007 and the proposed public seams/test table with: 「同意這張票與測試表，繼續實作」.

Approved delivery: EncoreTicket, the exact article recommendation replacement, author examples, component-mount behavior, compiled article placement, desktop/mobile light/dark browser checks, keyboard focus and navigation, source preservation and existing local checks. No commit, push, deployment, external-index update, install, or historical guard change is included.

Review round 2 clarifies objective assertions and distinguishes the baseline preservation rejection from additional authorized-delta rejection. It does not introduce a new test seam or enlarge product scope.

## Staging publication authorization

After reviewing the local result and the disclosed validation limits, the owner requested: 「目前可以，做 commit 並 push 到 staging」 on 2026-10-11. This authorizes a scoped commit and non-force push to origin/staging, superseding the earlier local-only boundary for these actions. It does not authorize installing dependencies, changing historical preservation rules, main publication, or manual deployment. Existing caption WIP remains uncommitted; the published article delta is only the EncoreTicket paragraph replacement. Known lint/metadata/preservation limitations remain recorded rather than relabeled as passes.

## Tool restoration exception

After the normal pre-commit hook failed on the missing UnoCSS ESLint plugin, the owner explicitly chose: 「允許補齊缺少的工具，跑正常 hook」 on 2026-10-11. This supersedes the no-install boundary only for restoring missing tools needed for normal validation and commit. It does not authorize skipping hooks, changing dependency versions or historical guards, main publication, or manual deployment. Dependencies were restored with the existing frozen lockfile; the package manifest and lockfile remain unchanged.
