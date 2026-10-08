# Authorization clarification — 2026-10-07

The parent clarified: the no-commit boundary concerns delivery/publication history in the product repository. Commits in disposable test repositories with no remote are within the authorized automated test scope. Use synthetic data only and never push. The original checkout remains untouched. Ticket breakdown and the new test seam table still await parent review before implementation.

This clarification supersedes the fixture-commit approval concern in the reviewed spec and ticket proposal. It changes authorization evidence, not acceptance behavior. No fixture commits have yet been created.

The parent subsequently approved T-0002, the seam table and AP-01–AP-09. Signatures are supplementary detection only; primary assurance is the exact reconstructed source tree/diff. Missing isolation/native runtime capability is reported, never installed or enabled by changing host settings. Implementation may now proceed.
