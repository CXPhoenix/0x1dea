# Frozen P13 prerequisite proposal review prompt

Review the immutable packet named by CURRENT.json supplied with this prompt. This prompt is identical across rounds; only the packet version changes. The caller assigns exactly one axis below and keeps that assignment for a second round. Read-only: do not edit files, execute candidate code, change Git refs, access credentials, perform remote writes, create tickets or create a lab.

Scope: the new P13 prerequisite requirements supplement, traceability, 23-row proposed test table, four draft slices, dependency/authority/completion boundaries and owner summary. Compare against captured source context (pinned main/staging identities, prior P13 preparation, parent frozen spec/24-row table, project instructions, tracker/runtime/review/language rules, CONTEXT/ADRs and current code/templates). Parent implementation is context, not a request to reopen unrelated historical scope. Existing prior preparation/engineering-map WIP is inventoried separately; do not claim it was authored by this proposal.

User request: prepare and review a four-prerequisite repair ticket proposal listing scope, blockers and test allocation, then ask owner confirmation. Keep T-0016 review; no implementation, lab, automation or deployment changes. Owner has not approved this new allocation or authorized new engineering work.

Axes (use only your assigned one):
1. Completeness: each type × field × boundary reaches an acceptance criterion and test allocation; identify missing combinations and undeclared dependencies.
2. Verifiability: each criterion has an observable pass/fail at its declared local surface; vague terms requiring interpretation are P0. Distinguish documentary/local/live and readiness/landing/completion.
3. Contract conflict: name any conflict with project rules, parent requirements, actual established seams, CONTEXT vocabulary or ADRs. Check frozen history, tracker approval gates, exact successor and candidate preservation.
4. Red team: identify unintended behavior or trust crossing enabled by the proposed repairs, including fabricated authority/evidence, credential mixing, workflow admission, manual-history laundering and stale readiness.

Grades: P0 cannot be implemented correctly as written and blocks ticket creation; P1 real problem resolvable inside a ticket; P2 record-only. Report concrete findings with packet-relative file:line, failing scenario, consequence and smallest correction. No majority vote; unresolved disagreement goes to owner. At most two rounds. Do not demand live implementation/exercise evidence for a proposal, but flag wording that claims such proof. Do not add speculative unrelated work or silently expand authority.

Return: assigned axis, packet version/hash checked, findings by grade (explicit zero when none), acceptance/AC coverage notes, unresolved or unverified facts, and a verdict restricted to proposal readiness. No implementation or security-audit completion claim.
