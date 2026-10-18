# Initial implementation review findings

Spec P1: external authority initially excluded only CONTROL, not the separate source/candidate checkout. PD-03 publicly reproduced acceptance of candidate-contained grant and receipt. ManualHistory now requires the independently trusted source root; both external authority files exclude it and CONTROL. CLI passes the full registry source root. Four methods and existing22 pass after correction; raw red/green retained. The initial full run was interrupted before completion to keep the revised source's final full run coherent.

Standards heuristic P2 (duplicated PR projection): list and detail share one pure pull_identity projection; detail alone obtains the independently observed merge tree. No old receipt, PR body, branch or article is changed.

Source v2 supplement and full regressions pending. No actual target landing or P13 proof.
