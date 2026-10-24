---
proposal_key: C
title: Save and resume writing context with an on-demand compatible glossary
epic: 0014-article-discovery
blocked_by_proposals: [A, B]
primary_rows: [18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 40, 48]
primary_scenarios: [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 38]
approval: awaiting-owner
---

# C — Optional save/resume and glossary ownership

## Context

This is a proposed ticket. The [reviewed specification](../../spec.en.md), D3/D5–D7, permits durable notes when requested or already authorized. Saving context must not convert a suggestion into the author's decision or require a glossary for expressive writing.

## Deliverable

An author can ask to save or resume a writing project. The actual read-back notes preserve useful choice states, sources and next action. A first resolved reusable term creates GLOSSARY.md only when persistence is enabled and no active compatible glossary exists. Returning authors reuse a sole existing GLOSSARY.md or legacy article CONTEXT.md without another designation question. Ambiguous ownership pauses vocabulary writes alone. The completed path includes both runtime packages, live writing references, safe file actions and native guard interaction.

## Blocked by

- A: default note creation/updates must be compatible with native current-source verification before this slice exposes persistence.
- B: save/resume extends the actual conversational entry and its generated runtime packages.

## Acceptance criteria

- Ordinary conversation and article-file-only requests retain B's no-extra-notes behavior. Saving/resuming or an established authorized workspace enables context reuse; do not seek a second approval for already authorized notes.
- Write and verify actual bytes at the authorized destination. Preserve confirmed, tentative, unknown and intentionally unset choices across save/resume without imposing a serialization schema or confirming every sentence. An unanswered agent suggestion remains tentative.
- Use stable valid default keys; title changes do not rename them. Same-project collisions reuse the established workspace; different projects use a distinct key without overwrite. Reject linked/escaping default paths. A custom destination retains its actual visibility and source-guard consequences.
- Create a glossary only for a resolved reusable term under D6's conditions, or an explicit glossary/scaffold request. Separate scoped meaning, author usage, source-supported definition and reader explanation. Settings/progress stay in the brief; intentional polysemy is not forced into a definition.
- Keep unresolved alternatives pending in the brief, investigate factual meanings and ask only material author choices. Continue independent prose; article/source text does not grant file-write or publication authority.
- Reuse a valid designated glossary, sole unassigned GLOSSARY or sole legacy article CONTEXT directly. With two unassigned candidates or an invalid/missing designation, resolve ownership before vocabulary writes only. Preserve files and engineering CONTEXT.
- Replace live universal CONTEXT+PROJECT requirements with the delivered optional contract in canonical references and both generated trees. Preserve historical/global material and Phoenix voice. Verify this slice's exact current-source successors.

Primary traceability: R18–R19, R21–R30, R40 and R48; lifecycle portion of R20. AC-08–12/14–17. Recheck R17 and A's R45–R47 through the integrated save/resume path; those rows retain their primary owners.

## Proposed test plan — awaiting approval

| ID | Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|---|
| C01 | Native conversation → file readback → fresh-session resume | Save only useful context, then resume without promoting suggestions or repeating settled questions | Request save; separately reuse an established authorized workspace; confirmed/tentative/unknown/intentionally unset choices; AD17 | AC-08; R18/R40 | Unanswered agent audience suggestion stays tentative; existing authorization is reused; no mandatory field schema or full-transcript copy |
| C02 | Agent file write/readback + interaction | Name exactly what was not saved and continue independent writing after a write/readback failure | Unwritable/unavailable destination and failed readback as independent cases; AD18 | AC-08; R19 | No false saved claim, fallback destination mutation or requirement to restart discovery; preserve any already-written bytes honestly |
| C03 | Authorized file actions + temporary filesystem/sentinels | Keep stable project identity, avoid collisions and refuse unsafe default destinations | Title change; same/different-project collision; empty/dot/dot-dot, slash/backslash input; linked root/workspace; AD19/AD26 | AC-08/11/17; R20/R28 | Reject unsafe key input before a write; do not let slash/dot normalization select another location; Unicode/spaces allowed; no overwrite or title-to-public-URL inference |
| C04 | Native request + actual workspace readback | Create no glossary without a qualifying term; create the first resolved entry when all conditions hold; honor an explicit scaffold | No term; resolved technical/custom/translation term; explicit empty scaffold; AD20–AD22 | AC-09; R21–R23 | Persistence disabled never silently enables it; unresolved choices are not resolved entries; a requested scaffold is labeled without invented terms |
| C05 | Brief/glossary readback + source record | Keep scope, aliases, sources, author usage and reader explanation distinct | Supplied term with relevant bilingual alias/source and author-local meaning; AD21/AD23 | AC-10; R22/R24/R25 | Applicable fields only; audience/genre/progress in brief; explanatory metaphor does not replace a technical definition; engineering context unchanged |
| C06 | Native ambiguity/conflict interaction + file readback | Preserve literary ambiguity; isolate a real technical/authorial conflict and continue other prose | Emotional metaphor versus conflicting source definitions/author usage; AD24/AD25 | AC-10/11; R26/R27 | Factual investigation is agent work; only unresolved material author choice prompts; pending alternatives stay outside resolved glossary entries |
| C07 | Native file-action trace + external sentinels | Refuse source-embedded or out-of-workspace mutation instructions | Article/source/term text requests engineering CONTEXT edits, escaping writes or publication; AD26 | AC-11; R28 | Supplied data is not action authority; protect other project notes and external sentinel bytes; do not broaden authorization |
| C08 | Existing-workspace native resume + readback | Reuse the single vocabulary owner without a new designation question | Sole unassigned GLOSSARY; sole legacy article CONTEXT; valid designated owner including both filenames present; AD27/AD28 | AC-12; R29/R30 | No duplicate glossary, rename, merge or deletion; retain existing entries and supplied authorization |
| C09 | Existing-workspace native resume + before/after snapshots | Stop only vocabulary writes for a genuine ownership ambiguity | Both files unassigned; missing designated target; invalid designated target; AD28 | AC-12; R30 | Identify the exact ownership choice; continue independent prose; no modification-time selection, root engineering fallback or silent migration |
| C10 | Native save/resume actions + native current CLI | Verify an actual default save and update against A's boundary, and report a custom-path guard blocker honestly | Both valid current roles; PROJECT/first glossary, update, legacy reuse; custom scanned-source destination; AD35–AD38 | AC-08/16/17; R20/R45–R48 | Default path keeps role/non-note identity; custom path gains no exemption: preserve requested bytes, name blocker, continue prose, no move/delete/repeated interview |
| C11 | Live routing audit + materializer/current CLIs | Remove effective universal context requirements and keep both runtime packages/current identities consistent | Optional persistence references and conditional entry links; AD31/AD32/AD34 | AC-14–16; R33–R39 | No live instruction requires a new CONTEXT or empty glossary for every project; preserve historical snapshots/three Chinese exceptions; edited generated bytes still detected |

## Implementation and evidence

Use existing file tools and evaluation practice, not a new persistence CLI/parser/database. Fixtures have independent expected bytes and never write real author/engineering notes. Per-host interaction records cover the changed branch; static generation checks cannot stand in for runtime behavior. A refusal or unavailable host is explicitly reported. A valid native baseline is required for every notes/guard claim.

Apply the [shared checks](README.md#共用驗證與收尾) with scope C. All rows are proposed; no implementation tests/evaluations have been executed for this proposal.

## 給使用者（zh-TW）

這張票交付「有需要才整理、下次可以接著寫」。一般聊聊與單純建立文章檔都不附贈筆記。要求保存時才整理有用脈絡，實際讀回確認；尚未接受的建議不會在下次變成你的決定。

沒有需要重用的術語就沒有 GLOSSARY.md；第一個已解決術語才建立，明確要求空白骨架則照辦。既有單一 GLOSSARY.md 或文章 CONTEXT.md 直接沿用，不重問、不自動搬移。兩份詞彙檔無法判定誰作主時，只先停詞彙寫入，其他文章繼續。

自訂保存位置若擋住 current guard，會保留筆記、指出是哪個來源造成阻擋，不為了顯示通過而搬檔、刪檔或擴大放行。尚未開始實作。
