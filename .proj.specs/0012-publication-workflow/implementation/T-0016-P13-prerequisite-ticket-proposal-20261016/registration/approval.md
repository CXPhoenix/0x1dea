# Approved P13 prerequisite ticket registration

## Owner decision and authority

On 2026-10-16 (Asia/Taipei) the owner replied **「同意」** to the immediately preceding four-ticket proposal, C→A/B and T16→C/D dependency update (retaining T15), and A6/B6/C7/D4=23 local test allocation. The preceding confirmation explicitly said tracker publication only; implementation requires separate authorization. The owner did not authorize implementation, lab creation, provisioning, active workflow/automation, deployment settings, merge, commit or push.

This record supersedes only the pending-owner-confirmation wording in the historical proposal/drafts/test-plan/review records. Those reviewed documents remain byte-identical; the 23-row table is now approved but remains NOT WRITTEN / NOT RUN. Original frozen epic spec, traceability, 24-row allocation and P13 a–l outcomes are not changed. This is not a new spec-review round.

## Permanent allocation

| Former draft | Ticket | Direct blockers | Approved rows | Initial status |
|---|---|---|---|---|
| A | T-0019 | None | PA-01–06 (6) | todo |
| B | T-0020 | None | PB-01–06 (6) | todo |
| C | T-0021 | T-0019, T-0020 | PC-01–07 (7) | todo; blocked derived |
| D | T-0022 | None | PD-01–04 (4) | todo |

T-0016 stays review, preserving T-0015 and adding T-0021/T-0022 as direct blockers. T-0019/T-0020 are transitive through T-0021. T-0017/T-0018 are unchanged; no repair depends on T-0016 done. The derived frontier is T-0019/T-0020/T-0022; frontier availability is not permission to start implementation in this request.

## Evidence and scope

A fresh read-only origin fetch verified main8b31956f47075a831cfd0339339f616af96b3dae and staging05fc16c30f978bbafab4b8cc89f24f8657ab3045. Every epic in these actual refs, the planning clone, prior staging clone and original checkout was scanned; the previous maximum was T-0018. IDs T-0019–T-0022 were allocated globally once, in topological order. Registration mapping is tickets.json.

The four independent review axes completed two rounds, final unresolved P0/P1/P2=0/0/0. V-01 explicit snapshot predicates and C-01 parent-compatible exact owned recovery remain in the published ticket requirements. Review files manifest SHA-256: 4d6679da51298d028c983c14b74fb23860bb4b0d4f54fa71692365b1ca6ad6b6; unchanged frozen prompt SHA-256: 8159428349fc05f1841e42db54967d3b7cd710ea7d470e80d1c65c3a505586da. Parent-record modification is the owner's explicit approved edge update, overriding the generic to-tickets prohibition against changing a parent only to that extent.

Work remains in the existing isolated planning clone. Prior preparation/proposal WIP and its exact map entries are preserved. New authorized scope is four tracker files, T-0016's exact dependency/comment successor, this registration folder and their exact finite management-map identities. No other candidate/history/code/spec changes. verification.json records local documentary/native checks; they do not prove P13 or actual remote tracker delivery.
