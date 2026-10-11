# Round 1 — four independent spec axes

Frozen prompt: prompt.md. Captured v1 inputs: the local frozen review-v1 packet (local evidence). Base/HEAD: f93237b1ed538484f24ed103ef00c7e5ee2e1828. No production implementation/tests at review time.

| Axis | P0 | P1 | P2 | Finding | Resolution for v2 |
|---|---|---|---|---|---|
| Completeness | 0 | 1 | 0 | Author guide's two examples lack an acceptance/traceability row | E1 and traceability/test-plan explicitly cover both examples |
| Verifiability | 1 | 0 | 0 | E3's omitted-description “usable” clause has no objective mount assertion | E1 explicitly requires title/action/href and no description paragraph; E3 refers to E1 |
| Contract conflict | 1 | 0 | 0 | New component/registration will cause additional preservation rejection, beyond baseline caption WIP | E6/test-plan distinguish baseline rejection from authorized-delta rejection; independent exact preservation comparison required |
| Red team | 0 | 0 | 0 | No unintended attack boundary found in trusted-author plain-text/native-anchor contract | No change |

Four read-only harness-reviewer contexts were used. Completeness and contract reviewers received the full packet before their final report. Verifiability and red-team initial reports were limited to the spec/prompt; round 2 supplies the full packet to all four. No disagreement requiring owner adjudication occurred. All findings were accepted and corrected in v2. Two-round ceiling remains in force.
