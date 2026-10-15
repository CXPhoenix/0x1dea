# T-0011 retrospective

## Delivered

Owner-merged PR #19 imports main ancestry into staging while retaining every website/candidate entry. The merged tree is identical to the locally tested and independently reviewed ticket tree. Historical oracle bytes remain unchanged, both contract families execute, and the owner explicitly requested done.

## What the evidence changed

Full-suite disposable clones exposed a local-only staging-ref assumption that the initial conflict resolution did not reveal. A minimal real-Git regression reproduced it. A second observed counterexample rejected the broader any-error fallback; final routing permits only genuine ref absence and retains fail-closed ancestry/receipt checks. The final full Python run passed with unchanged source hashes.

## Next iteration

- Keep a remote-only branch clone in the existing tracker seam; retain corrupt-local-ref and wrong-ancestry negatives.
- Synchronize main back into staging on a dedicated branch after selected publication, while keeping whole-staging publication outside the article contract.
- Record actual PR delivery and owner landing separately. Reconcile old review metadata against landing and per-ticket acceptance evidence rather than mass-changing statuses.
- Before continuing development, choose a current clean work copy deliberately; original local main/staging refs are stale and were intentionally not moved.

No new architecture decision is needed: these actions follow existing contracts. No frozen spec, historical record, unrelated ticket, dependency, remote ref or external setting is changed by this closeout.
