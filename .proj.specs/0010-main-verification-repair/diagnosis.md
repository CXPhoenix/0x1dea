# Root cause and verification boundary

PR #17 was owner-merged at 88b9c53852f527ee636bcc4b4ca5e166f6ec10fd. Its 45-path delta from e457143 contains exactly the selected electricity article, required dependencies/tests and 11 release evidence files. It does not import staging's other five candidates.

## Independent reproduction

The pre-release predecessor's public verifier exits 0 and its 29 tracker tests pass. The merged main's verifier exits 1 with `lint cleanup preserved source hash mismatch: blog/.vitepress/config.mts`. The full unchanged main harness executes 53 methods, with 52 passes and one error at the lint successor positive control. A focused baseline re-run and the predecessor CLI output are retained with this repair's evidence.

## Two causes

1. `test_lint_successor_rejects_source_scope_and_history_tampering` copied source files from the mutable checkout. Its immutable lint boundary describes commit 724ddad, but PR #17 legitimately adds the caption markdown configuration. The positive control consequently fails before its tampering cases execute. Using that same current verifier with input from the pinned lint epoch passes, falsifying a broken historical hash contract.
2. The public verifier understood adoption and lint epochs only. It had no separately reviewed successor for the selected main release. Its rejection is fail-closed behavior, not a corrupt article or an invalid historical manifest. Staging's T-0009 successor has different ancestors and includes other source evolution, so importing it wholesale would violate selected publication isolation.

## Repair

The historical fixture now reads original epoch Git bytes with current verifier code. A separate bounded guard validates the existing release scope against fixed predecessor/release/merge Git objects, the complete 34-product/11-evidence delta, real ancestry, and the current source inventory. Only then does the existing verifier evaluate historical predecessor bytes. Old hash expectations and historical release failure logs are unchanged. The guard rejects unknown ignored inputs and Git replace/graft overlays, and requires regular repair sources.

## Evidence limits and workflow cause

Main's package retains `test:unit`, which runs Vitest only; both Python suites and the adoption verifier are explicit independent checks. There is no tracked `.github` workflow in this main tree. Green Vitest results therefore never established a passing Python or preservation gate. The original PR release records explicitly retained these failures and a draft gate; they are not rewritten after the owner's manual merge. Current repair results are recorded separately in coverage-report.md.

All verification here concerns local CLI/Git behavior and website build compatibility. No hosted CI, deployed-site acceptance, new publication, remote change, or external-index update is claimed.
