# Ticket allocation and TDD approval

Recorded on 2026-10-24 (Asia/Taipei), from the direct owner message in this chat:

> 我同意這四張的拆分、相依關係與測試計畫，幫我建立正式 tickets，先從 A 開始依核准的測試表進行 TDD，保留「先自由聊、按需整理」原則。

The approval covers the four proposed deliverables and A→C, B→C, B→D dependency edges, their 36 per-ticket plan rows and shared X01–X03. It authorizes formal local tracker allocation and beginning A's local TDD. B–D are allocated only. It grants no new commit, push, PR, merge, deployment, external-index, installation, credential or trust authority. Existing applicable authority retains its original scope.

The reviewed spec blob remains `aa08308eb23756514ebc770e6a4719c60388d83d`; this receipt changes no frozen spec/review artifact. Approval is not an implementation or runtime pass. Original proposal wording remains an immutable record of the pre-approval state; this receipt supersedes its waiting status.

## Allocation

| Proposal | Ticket | Blocked by |
|---|---|---|
| A | T-0026 | None |
| B | T-0027 | None |
| C | T-0028 | T-0026, T-0027 |
| D | T-0029 | T-0027 |

## Approved artifact identities

- `.proj.specs/0014-article-discovery/planning/ticket-proposal/README.md` — SHA-256 `bcbf1a4aa7ea99ef56dafab870c79cf9e9848e9b14fa53b7b100ef1ec9c6e451`.
- `.proj.specs/0014-article-discovery/planning/ticket-proposal/A-local-notes-current-guard.md` — SHA-256 `49a27355a11526a6cb7a288875aaf8b37e052dbedf5cab2b70cd3ba8f29aea02`.
- `.proj.specs/0014-article-discovery/planning/ticket-proposal/B-free-conversation-entry.md` — SHA-256 `636a88074f26e4914c4f4d9495c46a09f147cde3688146c9254e24f1ad1d3985`.
- `.proj.specs/0014-article-discovery/planning/ticket-proposal/C-optional-context-glossary.md` — SHA-256 `44476db73632e8a428d03da6092139da35289c3c57a35ec3a4abad19369041e4`.
- `.proj.specs/0014-article-discovery/planning/ticket-proposal/D-public-preparation-routing.md` — SHA-256 `d8f74ae4850b463c6e448fa05a4e97c2b6bd20e39ef1e1877fdda6da03e5095b`.
