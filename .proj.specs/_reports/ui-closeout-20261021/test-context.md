# Local candidate test context

The first full invocation omitted PUBLICATION_TEST_DEPENDENCIES; its diagnostic is preserved, not counted as green. Supplying the existing dependency path exposed an actual add/add merge conflict for T-0006/T-0007: actual main 8baa has neither ticket, the future-main positive fixture imports their current done bytes, and pre-closeout staging f503 has review versions. The real Git refusal is retained in pre-closeout-ref-merge-conflict.json. No code or assertion was changed to convert it to success.

The intended delivery lands this metadata on staging first. A disposable candidate checkpoint 04d078d883d3b3bd0610b9b59f507558c6769007 (parent f503) contains exactly the reviewed 119-file core. Only that clone's local staging ref points to this candidate; real main remains 8baa and remote staging remains f503. All website, tests, runner and verifier bytes are unchanged. This is a local candidate input, not a claim of remote landing or deployment.

The same original PC01 test passes with the existing dependencies and required loopback permission. A default-sandbox attempt correctly failed at listener.bind before the actual data path; it is retained separately. The complete unchanged runner is now executed on the candidate context, with actual source digests, timestamps and environment recorded in python-receipt.json. The full result must be read before any aggregate pass claim.

The full regression checkpoint predates the additive result archive/HTML/review files. Program functions, the five exact closeout identities and all test bytes remain identical. Final native validation covers the completed archive; final delivery-context PC01 has not yet run and is scheduled after the five delivery commits. The QA checkpoint itself is never published.
