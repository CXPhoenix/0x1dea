# T-0024 本機修補驗收

現行來源檢查只在目標包含已發布的 Discord commit 時，要求指定路徑、43-byte 內容、SHA-256 與一般檔案模式。所有額外來源、變造、連結與執行位元仍拒絕；舊 M0 projection 保留原清單。

main 244 項、staging 273 項完整 Python／Git／CLI／歷史測試通過，兩次執行皆確認來源 SHA 不漂移。完整數量、各測試範圍與限制見 coverage.md；原始失敗與中斷紀錄同時保留。

五份 frozen modules、原 assertions、歷史 runner／verifier、M0、舊收據、已發布內容與候選均保留。staging 的 33 筆專屬 policy 紀錄維持原身分，50 個候選路徑保留。

本票維持 review，尚未 commit／push／PR／merge 或變更部署設定；原工作目錄與備份未更動。這是本機修補驗收，不宣稱遠端已套用、P13 成功或自動化啟用。
