# Reused approved test plan

The owner's current instruction authorizes the proposed synchronization, tests and review. This reuses the already approved T-0009 six-row and T-0010 verifier plans; no new seam or public interface is added.

| Seam | Test intent | Scope | AC | Boundary conditions |
|---|---|---|---|---|
| Existing Git/disposable CLI harness | preserve both historical/current contracts and source identity | existing staging/main positive and tamper cases | S1,S2,S3 | bytes/mode/link/missing/pins/history/extra/ignored, no fallback |
| Existing renderer, runner and tracker suites | preserve preview, historical article conversion, discovery and views | full unchanged assertions and tracker fixture reconciliation | S3,S4 | no skips, epoch input, both suites positive counts |
| Existing complete commands and browser | verify synchronized staging compatibility | Vitest/Python/lint/build/structure/materializer/verifier and listing/preview | S4 | existing installed runtime, actual results; exact S4 listing/card/destination/preview and keyboard/light-dark desktop-mobile browser assertions; local surface only |
| Existing Git/GitHub delivery | verify scope, parents and PR target | pinned refs and non-force ticket branch | S1,S5 | no merge/main update or other candidate publication |
