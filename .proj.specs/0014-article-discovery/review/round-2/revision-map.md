# Round-2 revision map

Date: 2026-10-24 (Asia/Taipei). These are proposed repairs, not reviewer closure decisions or implementation results. The owner requested this revision and a second four-axis review. Original round-1 reports, captures and prompt remain unchanged.

| Round-1 finding | Revised contract | Acceptance / traceability | Scope retained |
|---|---|---|---|
| V-01 (P0) | D8 specifies four existing categories' material triggers and minimum passage/asset-bound results; named unknowns complete identification only, not verification/readiness | AC-13; R32, R41–R44; AD30 variants | Public preparation only; absent triggers create no question/checklist; no discovery/SEO prerequisites |
| C-R1-01 (P1) | Explicitly include a single existing unassigned GLOSSARY.md in normal reuse | AC-12; R29; AD27 | Existing CONTEXT compatibility, conflict handling and no automatic migration retained |
| C-R1-02 (P1) | Preserve tentative, confirmed, unknown and intentionally unset author choices across conversation/save/resume; unanswered suggestions cannot become acceptance | D3; AC-08; R18, R40; AD17 | No required metadata schema or repeated sentence-by-sentence approval |
| C-R1-03 / RT-01 (one P1 issue) | D5a defines one bounded mutable local-output shape in the live current source guard, with regular-file/name/ownership checks before exclusion | AC-17; R20, R45–R48; AD35–AD38 | No whole-directory waiver, historical verifier rewrite, configurable exclusion, tracked source hiding or publication authority |

The historical evaluation inventory is identified as E1–E8 to match the supplied design/case evidence; this does not change those cases or results. The fifth canonical skill and both runtime packages remain a future implementation, not files created by this revision.

## Pre-review consistency check

This author self-check is not a fifth independent reviewer:

- D2 permits unresolved intent and a start-writing request; D8 runs only on requested public preparation and carries unresolved evidence explicitly. The public check cannot restart the settings interview.
- D5 still requires persistence authorization. D5a classifies filesystem objects for validation; it grants neither permission to create notes nor permission to execute/read them as trusted policy.
- D6 creates no empty glossary by default; D5a permits the absence of any note and recognizes legacy CONTEXT without requiring its creation.
- D7's active glossary precedence and dual-file ambiguity remain unchanged; the AC now includes the existing single-file GLOSSARY case.
- D9's finite current successors cover actual engineering changes. D5a's only dynamic exemption has named filenames and shape/ownership checks; other source identities and frozen validators remain protected.
- An explicitly requested alternate note path is preserved. It does not silently acquire the default namespace's exclusion, and a validation failure does not stop unrelated prose.

## Frozen inputs

- Prompt SHA-256 remains `3f5d674830cff8f9154503ee589378ebeb7a3ba1175953e350e70b8bebe7526d`.
- Round-2 spec SHA-256: `1dd95c9e0883a7f29d2512ad53449463fb56edd1d92310364c9a2fe73d21e7c4`.
- 3 reviewed package sources changed; the 60 captured surrounding sources remain identical to final round-1 context.
- [Capture](../versions/round-2/capture.json), [revision diff](../versions/round-2/round-1-to-round-2.patch), [document validation](../versions/round-2/document-validation.json).
- Only one second round will be performed. Surviving P0 findings require the project's split/restart procedure; there is no third round.
