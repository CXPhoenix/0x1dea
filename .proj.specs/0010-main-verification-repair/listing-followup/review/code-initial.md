# Combined implementation review: initial findings

Snapshot: /private/tmp/0x1dea-listing-repair/code-review, 83 files, base=HEAD=merge-base 88b9c53852f527ee636bcc4b4ca5e166f6ec10fd. No committed or staged diff; three tracked WIP changes and 80 untracked files.

Standards reviewer main_code_standards: P0/P1/P2=0/0/0. Spec reviewer main_code_spec: P0/P1/P2=0/1/0.

Spec P1: mobile screenshots have intrinsic dimensions 375x812, while browser.json reports window 390x844; the existing table did not distinguish screenshot dimensions from measured viewport. This is an evidence gap, not a demonstrated layout defect. Remedy: directly measure live window/document/visualViewport dimensions for both modes and record screenshot dimensions separately. Source behavior and guard controls had no other findings.

Disposition: retained as historical finding; closed by independent recheck documented in code-final.md. No implementation change was needed.
