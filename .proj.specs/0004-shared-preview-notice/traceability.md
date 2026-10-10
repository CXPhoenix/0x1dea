# Traceability

Run flag rows with nonblank page-owned title/text on both homepage and selected article. “Absent” means genuinely unset, with no local env file supplying it.

| Type | Field | Boundary | Expected behavior | AC |
|---|---|---|---|---|
| Flag | true | any branch including main/absent | show under preserved current contract; true/main proves the explicit override contract; Production acceptance uses false | N2, N4 |
| Flag | false/empty/space/TRUE/1/padded true | any branch including staging | hide | N2 |
| Flag | absent | exact staging | show | N2, N3 |
| Flag | absent | main/feature/Staging/empty/absent | hide | N2, N3 |
| Props | title + text | enabled, SSR + hydration | supplied page copy, trimmed edges, internal newlines preserved | N1 |
| Props | title only/text only | enabled | only populated elements; accessible title or 預覽說明 | N1, N5 |
| Props | omitted/empty/whitespace both | enabled | no whole note, no empty placeholder | N1 |
| Props | hostile HTML-like strings | enabled | literal escaped text; no executable nodes | N5 |
| Consumer | homepage + selected article | preview true or absent/staging | both correct notices; article prose unaffected | N1, N3 |
| Consumer | homepage + selected article | Production false/main | neither notice in SSR HTML or hydrated browser DOM | N3, N4 |
| Consumer | homepage + selected article | clean absent/main and absent/absent | neither notice; no local env leakage | N3 |
| Environment | root envDir/build-time precedence/rebuild | actual pinned build | same effective flag in SSR/client; changed config requires rebuild | N2, N3 |
| Git boundary | .env/example | ignore check without reading secrets | public example tracked, local .env variants ignored; no extra automatic env loader | N6 |
| Surface | mobile/dark/light/keyboard/hydration | browser | 360px complete text/no notice-induced horizontal overflow; ≥4.5:1 contrast; role=note/title or fallback name; surrounding links focusable; SSR/DOM text and visibility equal, zero hydration mismatch warnings | N5 |
| History | homepage commit/dirty article/#16 | retrospective record | true dates/scope, no fabricated original spec or done status | N7 |
| Release | resolved public flag/served artifact | separately authorized Production verification | explicit false plus actual served absence; otherwise release gate stays open | N4 |
