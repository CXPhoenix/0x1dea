---
proposal_key: D
title: Perform requested public checks and retain article delivery ownership
epic: 0014-article-discovery
blocked_by_proposals: [B]
primary_rows: [15, 16, 32, 41, 42, 43, 44]
primary_scenarios: [14, 15, 30]
approval: awaiting-owner
---

# D — Requested public checks and existing delivery routes

## Context

This is a proposed ticket. The [reviewed specification](../../spec.en.md), D4/D8, separates useful discovery from article artifact creation and publication. Public checks have concrete triggers/results and run for requested public preparation; they are not the price of starting a personal article.

## Deliverable

An author who requests a new article file, revision, preview or public preparation reaches its existing owner. Requested public preparation identifies the concrete passage/asset and known result or named gap for each triggered D8 category. Untriggered categories do not create questions or a checklist. A missing source/author choice stays unverified; completion of gap identification is never reported as publication readiness. The branch is available in both runtime packages with the necessary live route/current-identity integration.

## Blocked by

- B: this branch extends the working conversational entry and its project packages.

A and C do not gate this feature: public preparation can operate on supplied article text/assets without saved notes or a glossary. The all-slices resume/public-preparation integration check runs only after C and D exist; it is a shared epic check, not a false implementation dependency.

## Acceptance criteria

- Use the existing creation CLI/skill for new site artifacts, maintenance for existing revisions, and publication contracts for preview/selected preparation. Preserve creation time, article/assets/URL bytes, topic provenance, delivery allocation and action authority.
- For a triggered external factual claim, record location plus source/result, or the specific unverified claim/evidence gap. Personal feeling alone does not trigger evidence collection or universalize the experience.
- For borrowed material, identify the asset and known source/attribution/use-condition evidence or exact missing evidence. A citation is not permission or a legal conclusion.
- For an identifiable person's private/unclear-scope information, reuse supplied public-scope decisions or ask only the exact unresolved choice. Do not infer consent or request unrelated biography.
- For information-bearing media, identify existing alternative explanation/text/transcript or concrete missing information. This is editorial inspection, not a rendered-site/accessibility pass.
- A generic reminder fails the observable result requirement. Untriggered categories add no prerequisite checklist, audience/purpose/SEO question or persistent artifact. Reuse applicable authority; no discovery result grants commit, push, PR, deploy or external-index actions.
- Update only affected canonical/live routing, generated packages and finite current identities; preserve earlier conversation/no-notes/voice behavior.

Primary traceability: R15–R16, R32, R41–R44; AC-07/13. Recheck R33–R39 for affected integration and B's no-questionnaire/no-authority invariants.

## Proposed test plan — awaiting approval

| ID | Seam | Test intent | Scope | Acceptance criterion | Boundary conditions |
|---|---|---|---|---|---|
| D01 | Actual creation/revision routes + existing new-post CLI | Create a requested artifact through the existing contract and revise an existing one without resetting metadata | Disposable article/source tree and affected existing CLI regressions; AD14 | AC-07/16; R15/R37 | Preserve existing article time/URL/assets; an article-file-only request adds no PROJECT/glossary; no real author article mutation |
| D02 | Native preview/publication routing + action trace | Retain delivery ownership, provenance and action-specific authority | Preview, selected preparation and remote-action request variants; AD15 | AC-07/13; R16 | Reuse existing valid scope rather than re-asking; absent remote authority does not grant it; route evidence is not a live publication/rollback result |
| D03 | Requested public-preparation interaction + source/result record | Produce passage-linked factual evidence or a specific unverified gap | Number, quote, version/date, causal/general claim; supplied verified-source record versus inaccessible/unsupported source; AD30 | AC-13; R32/R41 | Personal-feeling variant alone has no factual trigger; distinguish fixture source evidence from any actual live lookup; no generic reminder or false verified claim |
| D04 | Borrowed-material public check + provenance record | Identify each triggered external asset and its known use-condition evidence or specific gap | Quotation, image and code with complete versus missing provenance/conditions; AD30 | AC-13; R42 | Attribution alone is not permission; no legal conclusion, rights acquisition or speculative unrelated questionnaire |
| D05 | Multi-turn public-scope interaction | Ask only a material unresolved third-party scope choice and reuse an already supplied decision | Identifiable private communication; same case with earlier explicit scope decision; AD30 | AC-13; R43 | No inferred consent, repeated settled question, unrelated biography or stoppage of independent prose |
| D06 | Supplied article/media editorial inspection | Identify available reading support or exact missing information per triggered asset | Information-bearing image/diagram/table/audio/video; sufficient surrounding explanation versus missing alternative/text/transcript; AD30 | AC-13; R44 | Decorative or fully explained media does not force extra questions; no rendered-site, device or full accessibility claim |
| D07 | Paired draft/public-preparation interaction + judgment record | Keep checks out of initial discovery, suppress absent-category checklists and distinguish named gaps from readiness | Expressive start; public request with no D8 triggers; public request with unresolved triggered items; AD30 | AC-13; R32/R41–R44 | No mandatory purpose/audience/SEO; generic warning-only output fails; named gap completes identification only, not verification or publication readiness |
| D08 | Materializer/current CLIs + preservation audit | Keep the new conditional branch complete across both packages and finite live sources | Affected live instructions, native metadata/links, deterministic generation and current identities; AD31–AD34 | AC-14–16; R33–R39 | B's direct drafting/listen-only/no-notes behavior still holds; previous packages/aliases/history remain intact; per-host results and unavailable surfaces are explicit |

## Implementation and evidence

Use stable supplied passages/assets and independent source records for repeatable cases. A real external factual lookup records its actual evidence; fixture or route checks are never presented as remote publication or browser validation. Preserve historical writing evaluation inputs/rubrics/results. Exercise changed interactions in each available actual host and keep their evidence separate.

Apply the [shared checks](README.md#共用驗證與收尾) with scope D. All rows await approval; neither tests nor implementation have started.

## 給使用者（zh-TW）

這張票讓「準備公開」有可查的結果：指出哪一段事實、哪個引用素材、哪段第三人資訊或哪個媒體需要處理，交付已知結果或具體缺口。單純心情抒發不會先被問目的、受眾、SEO；已回答的公開範圍不再重問。

建立文章檔、改稿、預覽與發布仍各走既有流程。列出缺口不等於驗證通過，更不等於已發布。這條路不要求先建詞彙表或保存脈絡，因此只依賴 B。尚未開始實作。
