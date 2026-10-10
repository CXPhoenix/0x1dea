# Coverage report: T-0004

| Seam | Tests / evidence | Measured coverage | Acceptance criterion | Uncovered, and why |
|---|---|---|---|---|
| Vue Test Utils / pinned renderer / Vue compiler | Summary 12, PreviewNotice 32, article consumer 1; final full suite 59 | Behavior cases counted; statement/branch instrumentation not configured | S1–S3/S8 or N1–N2/N5 | No invented source coverage percentage |
| VitePress build → SSR HTML | 5 env builds × homepage/article; three actual rendered summary variants in build-only fixture | 10 env artifacts and all compiled slot content verified | S1–S4 or N1–N4 | Local artifact only; no production deployment authorized |
| Served browser light/dark 1280px/360px | 4 component metric sets, 12 variant screenshots, 20 notice consumer/theme checks | All checks passed; ordinary text ≥4.5:1; no observed hydration/unresolved-component warnings | S4–S6 or N3/N5 | No real screen-reader audio session; accessibility tree/keyboard checked |
| Browser keyboard / accessibility / text selection | Visible focus, Enter navigation/back, static terminal aria tree, copy selection without $ | Actual focused link and tree/copy logs | S1/S3/S6 | No OS clipboard permission needed; selected copied text tested |
| Browser print / generated PDF | A4 portrait/100%, white backgrounds, text extracted from PDF | All three authored takeaway strings present; screenshot/PDF saved | S7 | Cross-browser print engines not checked |
| Git/content regression | 101 unaffected tracked blog files byte-identical; source 8-file freeze intact | 0 unexpected changed files; original times/category/draft/previewOnly intact | S8/N7 | Accepted banner/pageClass/centering/four prose changes documented separately |
| Repo tooling | lint, verify-project, generated skill check pass | Existing harness verifier fails identically on pristine 32cd6a9 baseline | S8/N7 | Historical preserved hash in config.mts blocks that inherited check; no unrelated history rewrite |

Evidence root: ../../evidence/; screenshots/PDF: ../../output/playwright/. No commit/push/deploy occurred, so ticket cannot be done. Separately authorized deployment and landing remain outside this task.
