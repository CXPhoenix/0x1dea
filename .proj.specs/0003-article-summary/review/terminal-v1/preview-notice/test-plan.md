# Proposed test plan — approval required before new tests

| Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|
| Existing Vue Test Utils/Vitest | retain exact flag and props contract | existing 22-case suite; meaningful missing cases only | N1, N2, N5 | precise strings, absent flag/branch, hostile props, omitted fields |
| VitePress build → SSR HTML (primary expansion) | both consumers follow actual resolved environment | clean isolated build outputs | N1–N4 | true/staging; absent/staging; false/main; absent/main; absent/absent; diagnostic true/main proves the valid override; Production acceptance is false/main |
| Served artifact browser | no hydration mismatch; correct copy/absence and layout | homepage + article, first load/navigation, 360px light/dark | N3, N5 | SSR/DOM notice text and visibility equal, zero hydration mismatch warning; 360px no notice-induced overflow; ordinary text contrast ≥4.5:1; title/fallback note name; text outside replacement preserved, links focusable |
| Git ignore/public file metadata | secret-safe filename policy | no environment contents read | N6 | .env and variants; .env.example |
| Historical record and diff review | honest scope and minimal consumer change | commit baseline vs candidate | N7 | retrospective label; no fake approval chronology or done state |
| Actual authorized Production artifact | release safety | parent-owned release step after gates | N4 | explicit false resolved; actual served homepage/article absence; not inferred from local build |

Retain existing unit evidence as historical evidence; do not manufacture retrospective TDD. New article behavior and safety gaps follow approved red→green cycles. Test environments must not inherit an unknown .env and must not share another worker's output directory. Cloudflare settings are not changed in this task.
