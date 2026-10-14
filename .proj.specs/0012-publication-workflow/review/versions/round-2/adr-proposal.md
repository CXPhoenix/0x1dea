# Proposed clarification: main-first engineering with staging landing evidence

Status: proposed; this file is not an accepted ADR or a change to AGENTS.md.

Engineering topics start from main and first land through an authorized main PR. The same
commits reach staging through a separately validated synchronization PR; no second
implementation of the fix is maintained. Staging remains the configured tracker landing
target under ADR-0006. A ticket cannot become done until its acceptance criteria, actual
authorized staging ancestry and approval receipt exist, including main landing where required.
An open sync PR and successful checks alone are insufficient.

The approved breakdown designates one ticket-owned routine sync branch. Repeated automated
sync PRs are operational uses of that one branch and retain its permanent ticket identity;
they do not allocate or reuse the id for new development. New features and conflict repairs
use their own ticket branches and approved test plans. The sync branch is retained after
merge; deletion/ownership drift stops until identity is checked. If the repository cannot
support this lifecycle without violating its actual rules, activation stays blocked until
the owner approves a different operational branch policy.

The owner retains independent authority for main/staging merges and publication. No automatic
merge is introduced. The historical meaning of done, original receipts, published URLs and
candidate preservation remain effective. If approved, the implementation ticket may adopt
this clarification as a new ADR and update the workflow documentation; it must not rewrite
the accepted historical ADR or backdate evidence.
