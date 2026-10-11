# Main to staging synchronization

## Problem Statement
Owner-merged PR #18 leaves staging divergent from main. A direct merge has six conflicts across navigation, theme, the electricity article, article tests and preservation verification. Both publication contracts must survive synchronization.

## Solution
Merge pinned main eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a into a new ticket branch based on staging 4005ee45f2f3267a8b53ce24fa97af7b49cfb144. Keep staging content and candidates exact, carry main repair code and evidence, pass both historical contract suites, and deliver an unmerged PR targeting staging.

## User Stories
1. As the owner, I want staging to contain merged main history while retaining every candidate and preview behavior.
2. As a maintainer, I want both exact preservation contracts and their tamper tests to continue running without refreshing historical expectations.

## Implementation Decisions
- One no-dependency synchronization ticket; the owner approved this bounded maintenance operation and its commit, non-force push and PR to staging. Original checkouts, main and remote staging are not modified by delivery.
- Retain every pre-existing staging tracked entry byte-for-byte and mode-for-mode except the shared preservation CLI, its reconciliation helper and tracker harness. Resolve product/navigation/theme/article-caption conflicts using staging intent. This includes the electricity review draft and all five local-preview articles/assets. The listing is already identical in both pins and remains unchanged.
- Import main's new repair helper, release regression suite and management evidence through the actual merge. Preserve all old manifests, records, hashes, package/lockfile and test expectations.
- The public CLI selects the existing reconciliation contract whenever any of its four exact provenance records is present (including links). Otherwise, the existing main release scope selects the main contract; without either, preserve the historical adoption path. No failed validation falls back to another contract. Selection does not authorize data: each selected guard enforces its own immutable pins, identities, existence/type/mode, ancestry and source inventory.
- Load guard modules only on their selected path so historical fixtures do not require unrelated new modules. Extend reconciliation reviewed-code roots only by the exact two main repair sources; no prefix exemption. Retain main helper bytes and its four mandatory regular repair sources. Keep tracker status/dependency behavior from staging and main's pinned lint input and no-replace Git read; no skips are added.
- Main fixture tests continue to execute the current shared CLI against their pinned main tree; staging fixtures continue to execute their historical/current trees. Neither suite is removed or converted to frozen verifier execution.

## Acceptance Criteria
- S1: A real merge records both pinned parents. Relative to staging, all pre-existing tracked paths except the three named integration sources retain their exact identities; all five candidates, their assets, preview flags, article and listing remain unchanged. Main-only repair/evidence additions are retained.
- S2: Current staging CLI and existing historical/current staging and main release positive controls pass. Each selected contract rejects its existing byte/mode/link/missing, record/pin/history and unknown/ignored-source counterexamples. No fallback or generic bypass is introduced.
- S3: Original manifests, historical fixtures and record bytes remain exact; every existing test and negative assertion is retained, with no new skip. Main release helper and release tests remain byte-identical to main. Tracker keeps staging's blocked/unresolved-dependency semantics and pinned lint epoch input.
- S4: Fresh full Vitest, both Python suites, lint, build, structure, materializer and public CLI checks pass with actual counts/exits/skips. Independent Standards, Spec and security reviews have no unresolved blocking findings. On the local build, /post/course/security-awareness/ renders heading 資安認知推廣備課系列 and exactly one article card titled 用電紀錄裡的正常與異常：家裡哪台設備在偷偷忙？ with its staging frontmatter description/date and destination /post/course/security-awareness/electricity-privacy. Keyboard Enter on that card reaches the article, whose heading matches and whose staging 修訂審閱稿 preview notice is visible. Listing light/dark at desktop 1440×900 and mobile 390×844 has no document horizontal overflow (scrollWidth equals clientWidth). No deployment claim is made.
- S5: Only the ticket branch is pushed, without force. PR base is staging, it is attached to this task and left unmerged with no automatic merge. Remote main/staging remain pinned at delivery; if either moves, re-evaluate before push/PR. Ticket remains review until actual authorized staging landing.

## Testing Decisions
Reuse the owner's approved verifier/disposable Git, renderer, runner, tracker and complete-command seams from T-0009/T-0010. Existing failing merge/fixture executions supply red evidence; preserve every counterexample. No new public interface or seam is introduced. Exact source comparison covers candidate preservation independently of build output. Use installed runtimes without installation. Existing browser surface and isolated local build provide compatibility evidence.

## Out of Scope
Article editing or publication, staging-to-main merge, dependency/lockfile changes, expectation refresh, remote merge, deploy, global settings, credentials and external indexes.

## Further Notes
This maintenance spec explicitly combines the existing main and staging contracts on a staging synchronization branch; it does not relax either contract or change the main publication preparation rules. Rollback is a reviewed revert of this synchronization on staging, never a reset/force push. Do not delete historical evidence or claim the PR has landed.
