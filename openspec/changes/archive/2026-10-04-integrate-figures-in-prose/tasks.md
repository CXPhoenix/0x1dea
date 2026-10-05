## 1. 規則與來源

- [x] 1.1 實現 Figure prose and guided-reading boundary：正文說明機制與圖的證據，明示操作教學才導引；核對核心、風格對照、寫作參考及 quill 來源映射。
- [x] 1.2 保留原 E7 輸出與判讀，另記父 QA 否決及修正 rubric；以原檔 hash 與新案例輸入核對歷史未覆寫。

## 2. 針對性驗收

- [x] 2.1 以凍結 v2.1 實際執行 E7 正例及操作教學邊界例，保留 E7 不確定性失敗後以 v2.2 僅重跑 E7；新 writer 不讀 rubric，另起 judge 評判，驗證兩案明示要求與機制及引用。
- [x] 2.2 保存完整輸入／輸出／判讀／配置限制，分開主 work fast 與 worker API；以 hash、symlink、連結、git diff --check 及 spectra validate/analyze 驗證後歸檔。
