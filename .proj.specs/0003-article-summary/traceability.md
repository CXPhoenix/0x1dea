# Traceability

| Type | Field | Boundary | Expected behavior | AC |
|---|---|---|---|---|
| Markdown component | name/registration/default slot | pinned VitePress compile/build | PascalCase block resolves; authored three-item list becomes semantic slot content | S1, S4 |
| Variant | note/cards/terminal | identical source except variant | same three claims/order; pale thin-border note, three icon cards, dark terminal rows | S1 |
| Variant | omitted/invalid/empty/case/hostile string | component + built page | note fallback, no injected markup | S1, S8 |
| Terminal | window frame/title bar/$ prompts | built DOM, accessibility, copy selection | author/default title in window bar; one decorative $ per direct takeaway, none for wrap/nesting; no input/execution/fake controls | S1, S6, S8 |
| Prop | title/default/blank/hostile text | component + accessibility tree | escaped plain text; TL;DR fallback and note name | S6, S8 |
| Slot | paragraph/list/link/strong/em/inline code/fence | renderer → built page | all text, semantics, href and code retained for each variant | S2 |
| Slot | noncanonical/rich content | component/build | no discarded content; extra blocks readable, list receives appearance | S2, S8 |
| Markdown boundary | blank lines/closing tag/sentinel/two instances | renderer + build | following text and next component remain outside | S3 |
| Markdown boundary | adjacent/nested info/tip/warning/details | renderer + built page | built-in containers retain content and details interaction | S3 |
| Markdown boundary | malformed/unclosed tags | unmodified pinned compiler comparison | same diagnostics/output; no new recovery | S3 |
| Slot isolation | nested takeaway lists/container-contained lists | built page | only direct items of canonical list decorated; inner structure/layout ordinary | S3 |
| Runtime | SSR/first load/navigation | static artifact → browser | text exists without JS; hydration and navigation resolve cleanly | S4 |
| Viewport | 1280px desktop/360px mobile/long URL/code | real browser | three desktop cards; mobile stack; no page overflow, fence self-scroll allowed | S5 |
| Theme | light/dark | computed colors + browser | ordinary text ≥4.5:1; links and focus visible | S6 |
| Accessibility | name/order/decorations/keyboard | tree + keyboard | meaningful content/order preserved, decorations silent, links operable | S6 |
| Print | all variants | print rendering | A4 portrait/100%, headers off/backgrounds on; all text, white background, ≥4.5:1 text contrast, no clipping; reflow allowed | S7 |
| Change boundary | prose/assets/parser/env | reviewed diff | no generated article copy, parser override, new string-to-HTML path or unrelated edits | S8 |
