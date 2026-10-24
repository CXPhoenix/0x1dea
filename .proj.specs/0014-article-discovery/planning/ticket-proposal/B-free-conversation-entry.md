---
proposal_key: B
title: Start article discovery through free conversation in both project runtimes
epic: 0014-article-discovery
blocked_by_proposals: []
primary_rows: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 31, 33, 34, 35, 36, 37, 39]
primary_scenarios: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 29, 31, 32, 33, 34]
approval: awaiting-owner
---

# B — Free conversation to a useful writing action

## Context

This is a proposed ticket. The [reviewed specification](../../spec.en.md), D1–D4, defines discovery as assistance with the supplied material. An unset audience or purpose is valid; the skill must not inherit a relentless engineering interview as its default.

## Deliverable

An author can invoke or naturally reach article-discovery, talk about a fragment, request listening, change genre or begin drafting without completing settings. The English canonical entry is deterministically packaged for Codex and Claude with actual per-host discovery/interaction evidence. Live routing separates editorial assistance from engineering work. This slice delivers the complete conversation-only path; C adds durable notes and glossary operations, and D adds the requested public-preparation branch.

## Blocked by

None within 0014. This path writes no writing notes and therefore does not depend on A. Shared canonical/live files still have one writer; absence of a dependency is not permission for competing edits.

## Acceptance criteria

- Matching start/direction requests and explicit invocation reach the skill. Code-only work, generic non-writing emotion, proofreading and sufficiently specified drafting retain their appropriate routes without a discovery interview.
- Respond to the requested assistance first. Listening alone produces neither unsolicited rewriting nor evaluation. Draft when asked; retain relevant uncertainty without requiring purpose, persona, audience, thesis, outline or a fixed question count.
- Ask only a question whose alternatives change the next action, meaning or material factual claim. Investigate discoverable facts; reuse answers; reserve deeper interviewing for an explicit request.
- Preserve protected expressions, stance, intentional ambiguity and author experience. Apply Phoenix only under its existing trigger. Keep personal experience distinct from an unsupported universal claim.
- Pure prose creates no engineering spec/ticket/ADR/test table. In a mixed request, identify the engineering need for its existing pipeline while continuing unaffected prose. This engineering ticket itself retains all project gates.
- Add the fifth canonical package and required native metadata, materializer/provenance/finite source identities, live routes and references for the delivered path. Keep the original three Chinese exceptions, existing engineering skills, aliases and historical material intact.
- Do not expose nonexistent reference targets or claim completion of C/D, the full epic, website verification or publication. Add conditional persistence/public-preparation instructions when their implementing slices are complete. The conversation path itself needs no temporary stub or newly invented fallback workflow.

Primary traceability: R01–R14, R17, R31, R33–R37 and R39; AC-01–06/08/13–16. R33–R39 are integration obligations rechecked by every affected later slice, not a claim that B alone completes them for the epic.

## Proposed test plan — awaiting approval

| ID | Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|---|
| B01 | Actual native discovery/invocation | Reach the new skill through explicit invocation and a matching article idea/direction request | Fresh Codex and Claude sessions; AD01/AD33 | AC-01/15; R01/R36/R39 | Record the selected skill and actual response per host; inspecting YAML/frontmatter is not a host pass |
| B02 | Native request routing + file-action trace | Keep bypass requests on their appropriate paths without a settings interview or extra context files | Code-only, ordinary emotional conversation unrelated to an article, proofreading and fully specified drafting; AD02/AD16 | AC-01/08; R02/R17 | Mentioning an article/repository/emotion alone does not force discovery; no scaffold/save request is inferred |
| B03 | Multi-turn article interaction | Respond to an expressive fragment and begin on request while purpose/audience remain unknown, self-only or intentionally unset | Inputs include「只是想寫爽的，不知道要說什麼」and「先寫一段」; AD03/AD05/AD10 | AC-02/03/05; R03/R05/R06/R11 | No mandatory persona/thesis/outline; remaining uncertainty stays distinguishable; do not count questions as a quality metric |
| B04 | Listen-only interaction + before/after file snapshot | Deliver listening without unsolicited rewrite/evaluation or context creation |「先聽我說，不要改寫或分析」with supplied text; AD04 | AC-02/08; R04/R17 | No new writing root, PROJECT, glossary or article; requested response alone completes this assistance |
| B05 | Multi-turn direction change | Change only affected decisions when genre/audience/assistance changes | Mixed essay/tutorial, then change direction after answering earlier choices; AD06 | AC-03; R07 | Do not restart the interview or force a single genre; reuse still-applicable answers |
| B06 | Draft/revision interaction | Preserve protected phrase, stance and an unresolved ending; keep Phoenix's existing trigger | Explicit Phoenix, continuing Phoenix and another requested voice; AD07/AD08 | AC-04; R08/R09 | No invented autobiography, psychological certainty, reconciliation or universal Phoenix style |
| B07 | Paired interaction + factual investigation record | Ask only the unresolved choice that changes the next action; distinguish author choice, feeling and external fact | Known versus unknown material choice; supplied verifiable technical fact versus inaccessible evidence; AD09/AD29 | AC-05/13; R10/R31 | Fact lookup is agent work; unavailable evidence stays unverified; independent prose continues; already answered choices are not asked again |
| B08 | Native explicitly requested interview | Provide deeper questioning when requested while ordinary discovery stays conversational | Same starting material with/without explicit deep-interview request; AD11 | AC-05; R12 | No required question quota or form for the ordinary variant; a later start-writing instruction ends unnecessary questioning |
| B09 | Native editorial/mixed routing + action trace | Separate prose from a renderer/tooling requirement and deliver unaffected prose | Pure draft versus draft plus requested new renderer behavior; AD12/AD13 | AC-06; R13/R14 | No engineering artifact merely for prose; do not silently implement tooling or bypass its gates; preserve existing article-delivery allocation requirements |
| B10 | Materializer CLI + portable verifier | Generate both physical packages with native metadata, complete links and equivalent invocation policy; demonstrate idempotence and drift detection | Canonical → two runtimes, second generation, then deliberate generated-byte edit in a disposable copy; AD31/AD32 | AC-14/15; R33–R35 | Edit canonical sources once; --check refuses drift; two canonical alias exceptions and original three language exceptions remain intact |
| B11 | Existing current verification CLI + exact identity audit | Admit only B's finite live integration and preserve existing contracts | Original engineering skills, Phoenix content/voice references, article/assets/times/URLs, aliases, historical runners/evaluations; AD34 | AC-16; R37–R39 | New package/routing identities require exact reviewed admission; no blanket management-tree allowance; failed/unavailable checks stay visible |

## Implementation and evidence

One writer owns canonical and live routing changes; generated files come only from the existing materializer. Link C/D references only once their targets and behavior exist. Each later ticket updates and verifies its own affected packages/current identities, so there is no final horizontal packaging ticket.

Use fixed scenario inputs with actual responses, tool/file traces and explicit rubric judgments; wording need not match a golden paragraph. Preserve historical E1–E8 unchanged. Run host cases on each actual available host and label a missing host unverified rather than borrowing the other host's result. A simulated response or self-check does not prove native execution.

Apply the [shared checks](README.md#共用驗證與收尾) with scope B. These are proposed tests/evaluations, not executed results.

## 給使用者（zh-TW）

這張票做出可直接使用的「先自由聊」入口：可以不知道目的、只寫給自己、先抒發、要求只聽，或直接試寫。文類改變不用重做訪談，已回答的問題不重問；只有影響下一步、文意或重要事實的缺口才處理。單純文章討論不要求工程 spec、ticket 或測試表。

會同步交付 Codex／Claude 套件與必要指引，但實際執行結果分開記錄。按需保存由 C 交付；公開前檢查由 D 交付，兩者都不會變成此入口的前置問卷。尚未開始實作。
