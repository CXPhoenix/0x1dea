# 已接受的整合範圍

32cd6a9 基準至凍結來源的差異：無字 banner、pageClass 限定圖片置中、PreviewNotice 文章替換與樣式、摘要三句原型、四處已接受小修（聚合量測用語、以功率線名稱替代顏色、五戶共449天、圖2來源locator）。本次保留原檔hash/evidence，不重寫其他文章、圖檔與時間。pageClass 為已接受置中需求的明示 frontmatter 例外，不變更 created/updated times、draft/previewOnly 或 URL。

T-0003 實作擁有摘要component/registration/docs/tests及三句wrapper；T-0004 擁有 notice 文章替換與既有功能追溯／驗證。兩個 ticket checkout 分開，無互相依賴；最終整合候選共用同一文章檔，由單一 writer 依已接受scope合併。暫時 QA Markdown 僅供build驗收，最終產品檔移除，fixture與本機build證據保留。
