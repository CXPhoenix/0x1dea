# 公開提交與可攜證據

2026-10-04，使用者另行授權 commit／push。原始測試與搬移資料已先保留於本機證據副本，沒有覆寫 Mac 完整 50 檔備份。

公開內容只包含技能、相容指引／validator、規格、測試輸入及產出與維護證據。original-manifest.json 是 43 個功能／歷史檔案的 hash 子集；7 個私有草稿的內容、名稱與 hash 都不提交。歷史指引中的 `/home/user` 是原檔的通用示例，保留原 bytes，並非本機使用者位置。

輸出 JSON 的本機讀檔路徑、freeze root 與案例來源路徑改為可攜格式；artifact 本文、input、rubric、評分、模型指定、指令快照不變。[publication-manifest.json](publication-manifest.json) 列出受影響檔案的原始及公開 SHA-256，輸出另核對 artifact hash。文件另補歷史時間範圍與這項說明。

圖文檢查器保留父 QA 記錄的原 32 檔 hash：原 bytes 相符，或符合明列的 metadata 投影且 artifact hash 相符才通過。這代表可查核的公開投影，不宣稱含私有路徑的原 JSON bytes 被逐字公開。其他機械檢查仍核對原 input／rubric／指令 hash。原始 bytes 可在 Mac 追溯，不是新 checkout 的相依。

Codex 專案入口 `.agents/skills/phoenix-writing` 使用 repo 內相對 symlink 指向 `skills/phoenix-writing`；新 checkout 無需全域 Phoenix 安裝。這次保持既有連結慣例，沒有採用另一套 harness 的無 symlink 政策。
