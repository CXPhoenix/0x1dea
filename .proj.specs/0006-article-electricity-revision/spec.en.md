# Exact article revision successor and staging preview

## Problem Statement
The owner-approved revised article and two new meme images are rejected by the immutable component epoch. The existing guard must accept this exact successor without weakening historical or current source checks.

## Solution
Retain all earlier records. Add one immutable exact three-path revision record and enforce it through the real required verifier before the authorized non-force staging publication.

## User Stories
1. As the owner, I want the revised article rendered with existing staging components so I can inspect the current preview.
2. As a reviewer, I want all other source changes and tampering rejected so this revision cannot become a general exemption.

## Implementation Decisions
Pin predecessor 69ff85f5fe1baddb54102070a436dff9ac1c5b73; require its Git object and ancestry. Enumerate exactly the approved article and two PNG assets, their predecessor mode/hash and approved final mode/hash. Pin record bytes and the exact path set in reviewed guard code. Verify predecessor identities against Git and prior component expectations for overlapping entries. Apply the revision after the unchanged component epoch. Require the component record when the revision exists. Reject a missing revision if its source overlay is present. Preserve every old record/digest and existing guard rules. Source inventory still rejects ignored/untracked unknown paths. Guard code and tests remain independently reviewed, not circularly authenticated.

The approved article SHA-256 is f36261ac4208d55d73c5c1250c3c96bf419cbadbfa053fd33b45f40af4969e34; cat PNG is 8a841ead65839eb117ce054edf84402c2f76baaab77acb0e8e22946cc671f3a7; midnight PNG is 99aead19c23b41ab372d1080e51fdc32ba5bf8f463e42d035794b29a4631441e. All final modes are 100644. Existing article predecessor is 7d7df900fe0bb3da0dc8beb8e8e146dab9326cccdf57d12d0c25fcf2a708bcc0; new image predecessors are absent.

## Acceptance Criteria
- A1: exact revised article/asset overlay passes the public CLI and preserves owner source bytes; no theme/config/other article changes.
- A2: article/image byte, mode, missing or linked input changes and fourth paths including ignored files fail.
- A3: predecessor/hash/record tampering, absent/missing/nonancestor pin and historical changes fail; old records stay byte-identical.
- A4: existing harness/publication/unit/lint/build/materializer/structure checks pass and independent standards/spec/security review resolves findings.
- A5: authorized non-force staging push is followed by exact-SHA automatic deployment and real preview validation; main and owner's uncommitted branch remain untouched. Failure is reported, not labeled success.

## Testing Decisions
Reuse the approved Python unittest + public verifier CLI seam in disposable real-Git clones. One failing acceptance test first, minimal enforcement, then rejection tests for each trust boundary. Historical test fixtures use immutable Git epoch bytes rather than the mutable revised article. Reuse installed toolchain; no installs or new testing runtime.

## Out of Scope
Generic successor engine, arbitrary allowlists, automatic hash refresh, old record rewrites, main publication, owner branch synchronization, Cloudflare settings/manual deployment, Notion and Library uploads.

## Further Notes
Owner explicitly approved modifying this precise guard and pushing staging after disclosure. The single tracer bullet and existing test seam are approved by the supplied bounded proposal; no original conversation identifiers or private paths are public evidence. Rollback removes this record/guard extension together, restoring the preceding exact guard, while product rollback needs fresh authorization. This extends T-0005's exact-successor pattern for this new authorized revision; its original no-publication scope remains historical.
