# Round 1 補充證據：完整性

Reviewer：`/root/ad_completeness`。同一輪、同一提示、同一 spec，唯讀補充。

補充證據影響完整性結論：新增 **C-R1-03（P1）**。修正後合計 **P0：0、P1：3、P2：0**；原 C-R1-01、C-R1-02 保留。

原 40 份及補充 23 份 frozen source 的大小與 SHA-256 均符合各自 manifest。

## C-R1-03｜P1｜本機寫作筆記與 current source guard 的交集缺少驗收要求

- 需求組合：已啟用保存 × Git 忽略的 `.proj.writing/<key>/PROJECT.md`／GLOSSARY.md × current source inventory 驗證。
- 原始位置：`.proj.specs/0014-article-discovery/spec.en.md:68`、`:96`、`:118`、`:143`；`scripts/publication_current.py:227`、`:235`、`:300`；`scripts/verify-harness-adoption.py:59`。
- 相關 AC／row：AC-08、AC-16；R20、R38、R39。目前分別覆蓋筆記保存及 current guards，沒有覆蓋兩者同時存在的情境。
- 證據：source_names() 明確納入 ignored sources，排除項目沒有 `.proj.writing/`；_verify_current() 要求實際檔案集合與固定 inventory 完全相同。補充的 engineering-v1.json 也沒有寫作筆記身分。
- 具體反例：作者完成一次已授權保存，產生 ignored `.proj.writing/cache/PROJECT.md`。即使新套件及工程來源已正確納入 successor，這份正常生成的筆記仍會被來源盤點視為額外檔案。只驗證「筆記已忽略」及「無筆記的乾淨環境通過 guard」，會漏掉這個交集。
- 影響：新功能正常使用後，可能使必要的 current-source 檢查失敗，誘發移走筆記或擴大來源放行等臨時處理。
- 最小修正方向：明定本機生成筆記在 current-source 驗證中的分類及邊界，並補上「保存後再執行 current guard」的驗收組合；保留精確工程來源盤點及歷史保護，不採 blanket management-directory allowance。
- 不確定性：這是 frozen 程式碼的靜態推論，未執行 guard。若預定只驗證排除筆記的投影，應明列該 surface、排除規則及驗收方式；目前規格沒有交代。

其餘補充的 publication local contract、Claude 原始三技能與既有行為評估資料，未改變原兩項發現。

補充範圍另有限制：manifest 實際提供 E1–E8 的 input／rubric，沒有 E9；原 design.json:2 也記載八例。因此尚不能聲稱已核對規格 spec.en.md:124 所稱的完整 E1–E9。此處僅記錄證據缺口，不據此推定 E9 不存在或另行加級。
