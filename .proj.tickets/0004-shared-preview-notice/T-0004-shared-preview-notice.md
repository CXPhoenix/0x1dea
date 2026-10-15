---
id: T-0004
title: Shared preview notice on homepage and article
epic: 0004-shared-preview-notice
status: review
blocked_by: [T-0005]
---


## Context

The homepage feature is existing behavior at f981af27b4992a938ac9f0065b57b857083e8737. The baseline article manual staging block is not controlled by that flag. The dirty local conversion is not landed. This prospective ticket does not pretend the homepage originally passed the new spec pipeline.

## Deliverable

Homepage and selected article use the same environment-controlled note with independent author-owned plain text. Verified preview builds show both; supported production builds show neither. The existing homepage implementation gets an explicitly retrospective evidence record.

## Acceptance criteria

- [ ] N1–N2: title/text and exact flag behavior preserved on both consumers.
- [ ] N3–N4: clean preview and Production matrix evidenced with actual SSR HTML and browser; true/main documented as the valid explicit override; supported Production configuration is false; separately authorized release verification remains required.
- [ ] N5–N6: escaping/accessibility/layout preserved; public example tracked and local .env variants ignored without secret access or new env loader.
- [ ] N7: existing commit and unlanded consumer work distinguished; retrospective record does not backdate gates or create fake completion.
- [ ] New work follows approved test plan and review/security/surface gates; selected article change is limited to the staging notice replacement.

## 給使用者（zh-TW）

把文章手寫的 staging 說明改成首頁已用的 PreviewNotice，各頁文案由 props 管理。補上首頁功能的真實追溯紀錄，驗證 Preview 顯示與正式建置隱藏；不把「index 切換」擴成新的 UI 切換器。

## Comments

External index: 0X1DEA #18 (external index maintained privately). Parent verified creation and readback; external status is processing. Repository status and blocking edges remain authoritative.

Blocked by: T-0005 (owner-approved required preservation gate reconciliation); prior no-edge statement predates the correction; summary is independent. Deployment account/settings changes and landing require separate authorization. No historical homepage ticket is fabricated as done. Production verification preserves the current API; no branch guard is proposed.

Approval: ../../.proj.specs/0004-shared-preview-notice/approval.md. No landing authorized; status cannot become done.

## Local verification evidence

See coverage-report.md under the epic, maintenance/component-delivery/TDD.md and scope.md. Local behavior verified; existing harness verifier config hash mismatch reproduced on pristine baseline. Actual deployment/landing not performed.
