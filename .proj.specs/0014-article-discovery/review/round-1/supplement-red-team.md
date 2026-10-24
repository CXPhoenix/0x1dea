# Round 1 補充證據：紅隊

Reviewer：`/root/ad_redteam`。同一輪、同一提示、同一 spec，唯讀補充。

補充證據影響原結論：**新增 1 項 P1；P0、P2 仍為 0**。這是同一 round 1 的證據補充。

原 40 份與補充 23 份快照的 SHA-256／位元組數全部符合 manifest。

## RT-01｜P1｜正常保存文章脈絡會新增現行工程驗證器不接受的來源

- 規格位置：`.proj.specs/0014-article-discovery/spec.en.md:65`、`:96`、`:143`。
- 對應要求：AC-08、AC-16；traceability R18、R20、R38。正常保存應可與既有工程驗證並存，且不能藉此放寬整個管理目錄的來源界線。
- 新增證據：`scripts/publication_current.py:227–248` 的 source_names() 明確掃描包含 ignored files 的來源；排除清單只有 .git、依賴／建置產物及指定 Python cache，沒有 `.proj.writing/`。
- 同檔 :288–302 將實際來源集合與固定 expected 集合比較，不相等即拋出 current reconciliation source inventory mismatch。
- `scripts/verify-harness-adoption.py:62–63` 的 current 路徑確實呼叫這個驗證器。
- 補充的 engineering-v1.json 有 1,568 個 exact common entries，沒有 `.proj.writing/` 項目或動態本機資料排除欄位。
- 具體反例：在其他條件皆可通過的 checkout，作者說「把這篇設定保存，明天接著寫」。新 skill 按規格建立 `.proj.writing/rain/PROJECT.md`，且 Git 正確忽略它。之後執行既有 current verifier，該檔仍會進入來源集合並造成 mismatch。每次新增工作區或更新筆記內容，也無法靠一次性的固定檔案 identity 接納解決。
- 影響：成功的文章保存成為後續工程驗證的意外障礙；可能迫使操作者搬走筆記，或錯誤採用規格禁止的 blanket waiver。
- 最小修正方向：明定動態本機寫作資料與 current source guard 的相容契約，例如經審查的窄範圍排除規則，或採用來源掃描範圍之外的預設位置；並驗證保存及更新筆記後的 guard 行為。保留其他來源與歷史界線。
- 分級／不確定性：列 P1，因可在實作票內處理，尚不足以判定規格無法正確實作。上述是凍結程式碼支持的行為推論，未建立工作區或實際執行驗證器。

其餘原 Red team 結論保留。補充發布契約、Claude 原始三技能與既有案例，未產生其他可確認 finding。

證據範圍更正：補充 manifest 實際包含 E1～E8 的 input／rubric，沒有 E9；未宣稱已審查 E9。這不改變上述 finding，亦不構成 runtime 通過證據。
