# ADR-0008: Main-first engineering with shared staging preview

Status: accepted design; operational activation pending epic 0012 acceptance.
Date: 2026-10-11
Authority: owner-approved epic 0012 spec and six-ticket allocation; see that epic's
approval.md. This ADR grants no merge, deployment or remote-write authority.

## Decision

Engineering ticket branches start from main. An authorized main PR lands the engineering
change first. The same commits reach staging through a separately validated sync PR;
there is no second implementation of the engineering fix. Main contains only approved,
published articles. Staging adds all retained public candidate articles and revisions at
one shared preview alias. An existing published path can contain a candidate revision.

Staging remains the configured tracker landing target under ADR-0006. Done requires all
acceptance criteria, actual authorized staging ancestry and approval receipts, plus main
landing where required. A main-only landing, open sync PR or successful checks cannot
close the ticket. ADR-0006 and its historical receipts remain unchanged.

Routine sync uses the permanent ticket-owned branch
`tickets/T-0016/main-to-staging-sync`. Its repeated operational PRs do not allocate or reuse
that ticket id for new development. Retain the branch after merge; deletion or ownership
drift blocks activation until identity is checked. New development and conflict repairs
use separate tickets, branches and approved test plans.

## Consequences and gates

The owner retains separate authority for publication and merges. There is no automatic
merge. M0 must account for every pinned main/staging difference and receive concrete
owner approval before policy use. Unknown or overlapping ownership, incomplete ancestry,
changed candidates and unreviewed successor boundaries block affected preparation.

Historical validator assertions, immutable receipts, published URLs and candidate bytes
remain protected. A shared current validator selects its role from trusted target/base
context, never from candidate input. Deployment settings remain unchanged under this epic's
present authorization; real automation activation requires the separately specified gates.
