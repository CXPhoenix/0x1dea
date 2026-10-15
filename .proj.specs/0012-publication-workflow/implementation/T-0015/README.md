# T-0015 本機同步驗證

本輪新增 `scripts/staging-sync.py` 的 prepare、verify、schema 介面。23 項 public CLI／Git 測試通過，涵蓋獨立 tree、no-op、衝突、完整候選身分、metadata／mode、來源 pin、漂移、歷史 alias、protected checks 與輸出路徑安全。

實際 main `001b26f8e931e0cf1e62373c5aa088a1b5ed09eb` 已在 staging `035783590895a426ee395045829ebc9d50e2b9cf` 的歷史中，因此 prepare／verify 都回傳 no-op，不需要 PR。6 個候選、50 個持有路徑仍與核准的 M0 身分一致。逐檔 registry、SHA 與 tree 綁定於 `actual-*.json`，不會自行替未經審查的 registry 賦予核准。

[coverage.md](coverage.md) 列出核准 P09／P10 本機範圍、真實 red→green 與未涵蓋的遠端範圍。產品 unit 54 項、build、lint、structure、materializer 通過；native 全套與歷史／現行 successor 修正分開記錄，沒有修改原歷史 assertions。

這份證據只涵蓋本機，不宣稱遠端 CI、瀏覽器或正式部署。T-0015 維持 review，等待獨立審查與真正落地。本輪沒有 commit、push、PR、merge 或部署設定修改。

安全審查補強後，23 項本機同步測試、3 項目前結案 guard 測試與 1 項歷史 runner 保護測試通過。完整 native checkpoint 為 66 + 43 + 10 項，完成於最後安全補強之前；最終整合驗證由父 agent 另行記錄，不能用該舊總數宣稱新版全套結果。`actual-final-*.json` 記錄新版完整歷史檢查後的實際 no-op。
