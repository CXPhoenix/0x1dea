# Reused approved test seams

The owner approved one ticket, no dependencies and the original six-row table in the prior repair request, and now explicitly requests preserving history and passing tests/review after PR #17. This follow-up reuses rows 1, 3 and 6 without a new seam. Rows 2, 4 and 5 receive compatibility verification only; renderer, command topology and tracker behavior are unchanged.

| Seam | Test intent | Scope | AC | Boundary conditions |
|---|---|---|---|---|
| Existing Python verifier CLI in disposable Git clones | historical accepted inputs remain valid with current code | lint fixture and existing negative cases | M1 | epoch bytes; missing object; no skips |
| Existing current preservation CLI | accept exact merged main; reject unauthorized source/history changes | pinned release and reviewed repair | M2,M3,M4 | hashes, modes, type, ancestry, record changes, missing input, extra/ignored paths |
| Existing complete project commands | execute full current checks and review | Vitest, both Python suites, lint/build/structure/materializer/verifier | M5 | real exits and counts; no external deployment claim |
