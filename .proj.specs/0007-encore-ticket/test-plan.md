# Proposed single ticket and test plan

Status: owner-approved single-ticket breakdown and test seams on 2026-10-11; see approval.md. Spec clarifications in review round 2 keep these same seams.

## Approved breakdown

One tracer-bullet ticket, T-0007: reusable EncoreTicket plus the electricity-article consumer, usage guide and validation. No blocking edges; existing Vue/VitePress seams are present in the current checkout. No separate tickets for CSS, registration, or tests.

## Test plan table

| Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|
| Existing Vue component mount | Authored title/destination/description, plain-text escaping, independent reuse | Two instances through public props | E1 | Different destinations; description present/omitted; title/action/href retained; text containing HTML-like characters; guide examples match public props |
| Existing VitePress build → actual article SSR | Global registration and exact recommendation replacement | One article consumer | E2 | Following heading stays outside component; no unresolved component |
| Served article → real browser | Approved D appearance, responsive layout, native accessible navigation | 1280px and 390px, light/dark | E3–E4 | Wraps without overflow; Tab focus visible; one accessible link; decorative text silent; activation reaches original article in same tab |
| Task-entry bytes → final source | Preserve the owner's current article edit and all unrelated content | Exact paragraph substitution plus bounded file inventory | E5 | Existing caption retained; assets and frontmatter unchanged |
| Existing unit/lint/build/structure/materializer commands | Compatibility | Current installed toolchain, no install | E6 | Execute preservation verifier; separately report baseline caption rejection and new authorized-delta hash/inventory rejection; no historical guard changes |

The owner approved the combined one-ticket breakdown and this table. No tests were written before approval. Coverage will be reported as executed cases/observed surfaces; no invented percentage.
