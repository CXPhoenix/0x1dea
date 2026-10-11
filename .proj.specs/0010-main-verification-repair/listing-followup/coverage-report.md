# Listing follow-up coverage report

| Seam | Tests / observations | Measured coverage | AC | Uncovered, and why |
|---|---|---|---|---|
| Existing rendered listing / browser | before 0 rows; after 1 exact electricity row, original metadata/date/URL/intro; excludes other categories | desktop 1440x900 and mobile 390x844, both light/dark; no horizontal overflow; actual Tab/Enter navigation; captured console logs [] (not an HTTP-error assertion) | L1,L2 | no remote deployment claim; local sandbox-built website only |
| Existing public verifier CLI / disposable Git fixture | 1 new method, 5 positive-first negative controls: stale, bytes, mode, deletion, symlink | targeted red exit 1, green exit 0; complete harness 66 methods, no failures/errors/skips | L3 | no line coverage instrumentation; behavioral controls instead |
| Complete commands | 54 Vitest; 66 harness; 16 publication; lint/structure/materializer/verifier exit 0 | all current suites; original negative controls retained | L4 | no CI/remote acceptance claim |
| Sandboxed build | VitePress build exit 0 in 5.66s with existing Node 24.13.0 / pnpm 10.28.0 | final OS sandbox probes: inside read succeeds, outside read/write and network denied | L4 | personal package-manager config reads denied, recorded as warnings; no install |
| Preservation | all 1719 merged-release entries compared | 1716 unchanged; only index and two original T-0010 tracked code repairs differ; build projection matches all blog/config inputs | L3,L4 | new reviewed repair code and management artifacts are additions |

Evidence: evidence/{browser.json,listing-*.png,red.json,targeted-green.json,unit.txt,harness.txt,publication.txt,lint.txt,structure.txt,materializer.txt,verifier.txt,preservation.json,sandbox-build.txt,isolation-sentinel.json}. Independent implementation review follows this table. Earlier T-0010 coverage and reviews describe the pre-listing snapshot and remain unchanged.

## Mobile evidence clarification after independent review

The initial screenshot-versus-viewport P1 is retained and closed. See evidence/mobile-viewport-supplement.json: actual window.innerWidth/innerHeight=390/844 in light and dark modes; document.clientWidth=scrollWidth=375, clientHeight844; visualViewport375x844, scale1. The article rect fits the visible content area. Screenshot artifacts are JPEG375x812 despite their original .png suffix; intrinsic image size is not the viewport measurement, and screenshot height difference remains unexplained. New supplement screenshots use .jpg. Existing Font Awesome stylesheet404s occur both before and after; unchanged and outside this repair.
