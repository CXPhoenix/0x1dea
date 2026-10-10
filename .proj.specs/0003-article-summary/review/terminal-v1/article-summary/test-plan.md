# Proposed test plan — approval required before tests

| Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|
| Existing component mount | fallback, literal title, preserved slot semantics | all three variants | S1, S2, S6, S8 | omitted/empty/invalid variant; blank/hostile title; richer content |
| Existing VitePress build → SSR artifact (primary) | compiled Markdown produces real registered component with intact following text | one temporary fixture + approved article consumer | S1–S4, S8 | all required inline/block forms, three list items, close tags, two instances, adjacent/nested four container types and their lists, nested takeaway list, malformed/unclosed pinned compiler comparison |
| Served built page → browser | hydration/navigation, appearance, accessibility | 1280px desktop + 360px mobile, light/dark | S4–S6 | no unresolved component/hydration warning; long URL/code; keyboard link focus and decorative icon silence; terminal window title, one $ per direct takeaway, none on wraps/nested lists, prompt excluded from copied/announced author text and no input/active window buttons |
| Built page print | retained, readable content | each variant | S7 | A4 portrait/100%, headers off/backgrounds on; all text and no clipping; white background and ≥4.5:1 text contrast; page reflow allowed |
| Existing project check/build/lint | compatibility and bounded diff | approved isolated worktree | S8 | no new package, parser modification or unrelated article changes |

No tests are written by this task. Reuse installed VitePress/Vitest/Vue tooling; do not install. Renderer-only HTML assertions supplement rather than replace the actual compiled page. Browser screenshots verify appearance, not keyboard accessibility; tree and keyboard evidence are also required. Final coverage report records measured evidence and unverified boundaries rather than invented percentages.
