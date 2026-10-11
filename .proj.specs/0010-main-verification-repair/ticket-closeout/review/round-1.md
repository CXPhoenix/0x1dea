# Spec adversarial review, round 1

Base=HEAD=eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a. Pure spec snapshot; five untracked files, no code implementation. Four independent harness-reviewer contexts; frozen prompt unchanged.

| Axis | P0 | P1 | P2 | Result |
|---|---|---|---|---|
| Completeness | 0 | 0 | 0 | Every matrix row reaches C1-C4 |
| Verifiability | 0 | 0 | 0 | Exact two-identity relation and public CLI outcomes are observable; implementation must supply independent oracle |
| Contract conflict | 0 | 0 | 0 | Exact T1 exception is explicit; landing and original historical assertions remain required |
| Red team | 0 | 1 | 0 | Existing tracker only validates receipt shape/ancestor; a different valid ancestor or unrelated regular approval may otherwise pass |

Carried P1: pin the exact original adoption commit, approval and observed staging receipt bytes in the T1 successor. Add public CLI counterexamples for a wrong but valid staging ancestor and unrelated existing approval. This resolves C2 within the existing seam; no new authority or broad exception. No P0 remains; no second spec round is required. These are spec reviews, not acceptance or code-review results.
