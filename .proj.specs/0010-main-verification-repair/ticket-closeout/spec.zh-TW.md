---
synced_from: spec.en.md
synced_from_sha: 74d89732b01ea9433d940288ad7c2a56eb9be957
---

# 依證據結案追補

逐項稽核六張票的驗收與實際 staging 落地，只將符合條件的 T-0001、T-0010 標記 done，連同已由使用者確認的 T-0011 結案紀錄交付。T-0002、T-0003、T-0004、T-0008 保留 review，列出尚缺的必要證據。

T-0001 只允許原始 ticket，或僅修改 status 與固定 landing_evidence 的精確後繼版本；固定真實 adoption commit、授權與目前 staging 查核收據。原始版本仍供歷史 fixtures 使用，其他位元組、mode、link、路徑或收據替換一律拒絕，既有 tracker／Git 檢查仍獨立執行。

C1：六票逐項紀錄結果、可查證來源、落地 commit 與限制，不補造遺失產物。C2：公開 verifier 接受兩個核准身分並拒絕任意變更、缺失或錯誤收據及祖先。C3：兩個目標的完整 Python suites 與管理檢查成功、零 skip，blog 與歷史 manifests 完全不變；不宣稱重新執行產品瀏覽器、Vitest、lint 或 build。C4：獨立 Standards／Spec／security 審查與兩份 PR 範圍驗證，僅 non-force push，PR 保持未合併、未啟用 auto-merge。

新增單一無相依 T-0012 追蹤尚未落地的 guard 修正，沿用已核准 CLI／tracker／Git seams；main 使用其正式分支，staging 沿用 T-0011 的同步交付分支。T-0012 維持 review；T-0010 done 只代表已由 PR18／PR19 落地的原 M／L 範圍。保留歷史報告原文。main 只匯入必要管理證據與 T-0005 相依收據，不匯入候選文章或 staging verifier dispatcher。未驗票的瀏覽器／正式環境補證、文章修改、部署與後續 workflow 實作均不在本次範圍。
