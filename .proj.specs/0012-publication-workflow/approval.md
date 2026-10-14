# Owner approval and current gate

Date: 2026-10-11 (Asia/Taipei).

The owner directly replied `spec OK` and explicitly invoked the project's `to-tickets`
skill after receiving the reviewed spec, test-plan and skill-draft links. This records
approval of the detailed specification, English Git blob
`a3f0c03754c389d40ca9fb97d8bb7c1ae992651b`, with its matching Traditional Chinese audit copy.
The frozen reviewed source and snapshots are unchanged; their planning-time status lines
remain historical. This sidecar records the later decision instead of rewriting the spec.

Current authorized action: prepare the ticket breakdown under the configured local tracker
workflow. The proposed six-ticket breakdown and allocation of the existing 24 planned tests
are presented for explicit owner confirmation before ticket publication/test writing.
No permanent new ticket id is allocated by the proposal.

The planning-round restrictions in the spec describe the completed planning round; they do
not prohibit the owner-authorized ticket-planning stage now. P24's no-ticket snapshot is
retained as historical authoring evidence, not replayed as a ban on later approved tickets.

Approval does not grant commit/push/PR/merge, deployment changes, repository-rule changes,
credential installation, external test-repository creation or live automation activation.
Existing specific authorizations retain their scope; none is silently expanded here.

Next gate: owner approval of granularity, blocking edges and test allocation in
ticket-breakdown.md. Publish one English-primary ticket per approved slice with the embedded
Traditional Chinese user section, status todo and explicit blocked_by. Recheck global ids
before allocation. Do not close, reopen, renumber or modify previous tickets.

## Subsequent owner approval: tickets and T-0013 implementation

On 2026-10-11 (Asia/Taipei), the owner explicitly approved all six tickets, blocking edges
and the 24-row test allocation, requested publication to the local tracker, and authorized
implementation starting at T-0013 under the project workflow. This supersedes the earlier
waiting-for-breakdown/test-plan gate. Main contains approved publication content only;
candidates/history remain preserved. Deployment settings and merges remain prohibited.
Future T-0014–T-0018 execution is not claimed started. M0 itself still requires review of
the concrete inventory before it is trusted as policy.

## Concrete M0 owner approval and T-0013 continuation

On 2026-10-14 (Asia/Taipei), the owner approved the concrete M0 inventory and candidate
preservation boundary, and authorized completion of T-0013's common engineering baseline
and exact successor, with project testing/review. Main retains published articles only;
candidates and historical contracts remain preserved. Deployment settings and merges remain
prohibited. This does not close T-0013 or grant a new external publication authority.

Approved classification SHA-256:
`71e88f0f2187505145701fd13145f9e156692d0e40d1bba7852b7c5290e03b49`.
Approved full inventory SHA-256:
`6d95e0c7036fef827ce3c4c7b97beae811597e908d755837cce4431b526ea89a`.
Remote main/staging pins and OPEN PR20/21 were refreshed and remained identical.

## Owner authorization: T-0013 main PR delivery

2026-10-14 Asia/Taipei: owner explicitly authorized remote refresh and verification of
PR20/21, necessary revalidation, commit and non-force topic push, and a main PR containing
only approved engineering/management changes. Candidate articles and historical contracts
remain protected. No merge or deployment-setting changes authorized. This does not mark
T-0013 done, land PR20/21, or authorize staging integration or article publication.
See implementation/T-0013-current/delivery-preflight.json for fresh unchanged pins/states.
