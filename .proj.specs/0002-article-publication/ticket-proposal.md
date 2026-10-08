# Proposed single tracer-bullet ticket

Proposed next permanent id: T-0002 (current highest id is T-0001). Allocation and actual ticket creation remain after zero P0 spec review and user approval.

1. **Local article preview and selected candidate preparation**
   - Blocked by: none; local phase 1 does not depend on landing T-0001.
   - Delivery: canonical English skill, formal fourth-product materialization and CLI preview/prepare/verify with source/output exclusion, pinned SHA verification, test evidence and independent review.
   - Branch after approval: tickets/T-0002/article-publication-preparation.
   - Acceptance: AP-01 through AP-09 and the spec test table.
   - State at handoff: proposed only. Actual publication/rollback are later work.

## 給使用者（zh-TW）

建議第一階段採一張可完整驗收的 ticket：集中預覽 A/B、只準備 A、檢查污染與固定 SHA、核對來源與建置輸出，並正式擴充第四個雙 runtime 技能。請核准這個切分與 spec 的測試表；另請明確允許僅在可丟棄、無遠端的測試 repo 建立 fixture commits，以測到 merge、revert、main/head 漂移與 hotfix。產品 repo 維持不 commit、不 push、不發布。
