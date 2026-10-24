# Article discovery traceability

Revised for stage-3 round 2, 2026-10-24. Each row maps a type, field and boundary to an observable behavior and acceptance criterion in [spec.en.md](spec.en.md). Scenario labels are coverage proposals, not an approved implementation test plan. No tests have been written or run for the new skill.

## Behavioral and integration matrix

| Row | Type | Field | Boundary / public seam | Expected behavior | AC | Proposed scenario |
|---|---|---|---|---|---|---|
| R01 | Entry | explicit invocation; article idea/direction | actual runtime discovery/invocation | route to article-discovery | AC-01 | AD01 |
| R02 | Non-entry | code-only; non-writing emotion; proofreading; specified drafting | actual runtime request routing | use existing owner without a discovery questionnaire | AC-01 | AD02 |
| R03 | Expression | fragment; venting | captured conversation | respond/explore as requested before demanding settings | AC-02 | AD03 |
| R04 | Assistance | listen-only | captured conversation and file actions | response without unsolicited rewrite, evaluation or file scaffolding | AC-02, AC-08 | AD04 |
| R05 | Intent | unknown; emerging; self-expression | captured conversation | drafting can begin without an imposed purpose/thesis | AC-03 | AD03, AD05 |
| R06 | Audience | self-only; unspecified | captured conversation | retain choice; no mandatory persona or reader outcome | AC-03 | AD05 |
| R07 | Genre | mixed; changed midway | multi-turn conversation | update only affected choices without restarting interview | AC-03 | AD06 |
| R08 | Author agency | protected phrase; stance; ambiguous ending; assistance | captured draft/revision | preserve requested expression; no invented experience/cause/moral | AC-04 | AD07 |
| R09 | Voice | explicit Phoenix; continuing Phoenix; other style | runtime routing and produced text | apply existing Phoenix trigger without imposing it on all articles | AC-04 | AD08 |
| R10 | Question | next-action/meaning/fact dependency | transcript with input variants | ask only materially relevant unresolved choices; inspect facts separately | AC-05 | AD09 |
| R11 | Completion | start-writing request; usable next action | multi-turn transcript | perform requested action with relevant uncertainty retained | AC-05 | AD10 |
| R12 | Depth | explicitly requested full interview | captured conversation | deeper questioning available; ordinary requests stay conversational | AC-05 | AD11 |
| R13 | Editorial work | conversation; drafting; revision | runtime action trace / disposable filesystem | no engineering spec/ticket/ADR/test table created merely for prose | AC-06 | AD12 |
| R14 | Mixed work | prose plus renderer/skill/tooling change | runtime routing and delivered artifact | separate engineering need, preserve its gates, continue unaffected prose | AC-06 | AD13 |
| R15 | Article delivery | new artifact; existing revision | existing creation route/CLI; temp article | use existing artifact contract and retain existing creation time | AC-07 | AD14 |
| R16 | Publication | preview; prepare; remote request | existing publication route and action trace | keep provenance/authority requirements; no discovery-as-publication claim | AC-07, AC-13 | AD15 |
| R17 | Persistence absent | conversation; article file alone | temporary filesystem before/after | no forced context/workspace creation | AC-08 | AD04, AD16 |
| R18 | Persistence enabled | save/resume request; established workspace | file write/readback | save/reuse relevant brief/context at authorized location without promoting tentative suggestions to confirmed author choices | AC-08 | AD17 |
| R19 | Persistence failure | unavailable write/readback | filesystem error plus conversation | report unsaved content and continue unaffected writing | AC-08 | AD18 |
| R20 | Workspace | local default; stable key; title change; collision | temporary filesystem, Git ignore and native current guard | ignored/outside website, stable identity, no overwrite; D5a constrains source-set exclusion | AC-08, AC-17 | AD19, AD35–AD37 |
| R21 | Glossary absent | no qualifying term | authorized empty writing workspace | create no empty glossary, table or placeholder definitions | AC-09 | AD20 |
| R22 | Glossary present | first resolved reusable technical/custom term | write/readback in disposable workspace | create GLOSSARY.md with actual resolved entry | AC-09 | AD21 |
| R23 | Author override | requested glossary/scaffold | captured request and resulting artifact | honor explicit scope; label empty scaffold without invented terms | AC-09 | AD22 |
| R24 | Glossary entry | term; meaning; scope; alias/source applicability | actual glossary readback | include applicable semantic fields; distinguish local/source-supported usage | AC-10 | AD21, AD23 |
| R25 | Artifact separation | audience; genre; progress versus vocabulary | brief and glossary readback | settings/progress stay in brief; engineering context unchanged | AC-10 | AD23 |
| R26 | Literary language | deliberate polysemy; emotional word; metaphor | expressive conversation and filesystem | preserve ambiguity; no glossary solely to force a canonical meaning | AC-10 | AD24 |
| R27 | Definition conflict | technical inconsistency; unresolved author choice | conversation plus glossary/brief readback | unresolved alternatives stay pending; continue independent prose | AC-11 | AD25 |
| R28 | Authority | supplied-source write instruction; escaping/linked destination | action trace and temporary external sentinels | no unauthorized writes outside workspace, no source-granted action authority | AC-11 | AD26 |
| R29 | Existing vocabulary | only unassigned article GLOSSARY.md; only legacy article CONTEXT.md | existing temp workspace read/write | reuse the single active glossary without another designation question, rename, deletion or duplicate | AC-12 | AD27 |
| R30 | Glossary authority | designated owner; competing filenames; invalid/missing designation | temp workspace plus conversation | respect valid designation; resolve ambiguous ownership before vocabulary writes only | AC-12 | AD28 |
| R31 | Evidence | feeling versus external fact; personal versus general claim | captured draft and source check | preserve experience scope; factual support/uncertainty remains identifiable | AC-13 | AD29 |
| R32 | Public stage | triggered versus absent D8 categories; unresolved evidence; search | draft versus public-preparation request variants | concrete passage/asset result or named gap per triggered category; generic reminder fails; no checklist/SEO prerequisite for absent categories | AC-13 | AD30 |
| R33 | Live guidance | editorial exception; optional persistence; GLOSSARY name | review of active routing and references | one consistent contract; no mandatory new article CONTEXT or empty glossary | AC-14 | AD31 |
| R34 | Package | canonical source; two runtime trees; metadata; links; policy | existing materializer CLI and portable verifier | complete physical packages, native metadata and equivalent invocation | AC-15 | AD32 |
| R35 | Generation | repeated output; generated edit | disposable materializer --write/--check | stable output; changed generated bytes detected | AC-15 | AD32 |
| R36 | Host evidence | fresh Codex/Claude discovery and interaction | actual host, per-runtime transcript | separate actual host results from static checks; missing runtime unverified | AC-15 | AD01–AD15, AD33 |
| R37 | Preservation | original engineering skills; Phoenix voice; article bytes/time/URL/assets; aliases | exact Git/file identity audit | only approved scoped integration changes; original contracts retained | AC-16 | AD34 |
| R38 | Current guards | finite new identities; frozen baselines/fixtures | existing current verification CLI | exact reviewed successor if needed, no blanket directory waiver or history rewrite | AC-16 | AD34 |
| R39 | Verification reporting | unavailable surface; failed check | recorded commands, exits, output and report | no success inferred from a missing/failed check or from another surface | AC-16 | AD33, AD34 |
| R40 | Decision state | unanswered suggestion; confirmed choice; unknown/intentionally unset | conversation→save→resume transcript and file readback | preserve state/provenance without invented author acceptance or repetitive confirmation | AC-08 | AD17 |
| R41 | Public factual claim | checkable external claim versus personal feeling | D8 claim/location and source-result record | source/result or named unverified claim; personal feeling alone does not trigger | AC-13 | AD30 |
| R42 | Borrowed material | external quotation/image/code; known or absent use-condition evidence | supplied asset/provenance record | identify asset and known source/condition or specific missing evidence; no citation-as-permission claim | AC-13 | AD30 |
| R43 | Third-party scope | private/unclear public communication; previously answered scope | requested public-version transcript | identify passage and reuse author decision, or ask only the exact unresolved scope; no invented consent | AC-13 | AD30 |
| R44 | Media reading support | information-bearing media; existing text/alternative explanation; missing support | supplied draft/asset inspection | identify available support or concrete missing information, without claiming rendered-site/accessibility pass | AC-13 | AD30 |
| R45 | Notes/guard normal path | absent root; empty directory; authorized brief/glossary/legacy note creation and text update | native current verifier on otherwise valid disposable main/staging | pass before/after with unchanged role and non-note source identities | AC-17 | AD35 |
| R46 | Notes/guard invalid shape | linked/non-directory root or workspace; invalid key; nested/extra name; linked/nonregular/executable note | native verifier with disposable namespace mutations | refuse before exclusion; unrelated source outside namespace still refuses | AC-17 | AD36 |
| R47 | Notes/guard source ownership | HEAD/index tracking; trusted expected-inventory collision | native current verifier with independent Git/policy fixtures | reject collision rather than silently excluding trusted/tracked source; retain historical behavior | AC-16, AC-17 | AD37 |
| R48 | Alternate note location | explicitly requested path inside scanned sources outside D5a | write/readback plus native-verifier result and transcript | preserve requested notes, name guard blocker, continue prose; no silent move/delete/admission expansion or renewed interview | AC-08, AC-17 | AD38 |

## Proposed public-seam groups

| Group | Existing public seam / prior art | Scope | Coverage intent | Approval state |
|---|---|---|---|---|
| Conversation | Native project skill discovery and actual multi-turn requests; fixed input/output/judgment practice in existing writing evaluations | AD01–AD13, AD17, AD24–AD25, AD29–AD30, AD38 | default, bypasses, transitions, depth, author agency, saved choice states and routing | Proposed; ticket test plan not yet approved |
| Filesystem | Existing agent file tools with write/readback and independent temporary fixture expectations | AD04, AD16–AD28 | optional persistence, glossary lifecycle, compatibility and ownership boundaries | Proposed; ticket test plan not yet approved |
| Existing article interfaces | New-post CLI, existing revision and publication routes | AD14–AD15 | retain artifact and delivery responsibilities | Reuse existing contracts; affected test allocation awaits ticket approval |
| Packaging | Materializer CLI, portable verifier, existing materializer regressions | AD31–AD32 | effective guidance, deterministic generation, metadata and drift detection | Reuse existing public seams; new case allocation awaits ticket approval |
| Runtime/preservation | Actual fresh hosts, exact Git identities and existing current verification CLI | AD33–AD38 | honest surface reporting, finite reviewed integration, notes/guard intersection and refusal boundaries | Proposed evaluation allocation; no implementation or host pass asserted |

AD identifiers describe scenario families; the ticket plan must enumerate their concrete inputs, expected outputs, boundaries and runtime coverage before tests are written. They are not ticket ids and do not reserve a global ticket allocation. No additional implementation tool, private helper seam or workflow exemption is introduced by this matrix.
