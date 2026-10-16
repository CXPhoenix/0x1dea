---
synced_from: spec.en.md
synced_from_sha: 6cb6473aba50a4d02115020c50cdb30d648266e5
---

# 精確文章後繼版本與 staging 預覽

## 問題
使用者已批准的修訂文章與兩張新梗圖被不可變元件 epoch 拒絕。既有 guard 必須接受這個精確後繼版本，同時維持歷史與目前來源檢查。

## 解法
保留全部舊紀錄。新增一份不可變的精確三路徑修訂紀錄，先通過真實 required verifier，再執行已授權的非 force staging 發布。

## 使用者需求
1. 作為站主，我希望新版文章使用 staging 既有元件呈現，方便檢視最新預覽。
2. 作為審查者，我希望其他來源修改與竄改繼續被拒絕，避免這次修訂成為一般豁免。

## 實作決策
固定 predecessor 為 69ff85f5fe1baddb54102070a436dff9ac1c5b73，要求 Git object 存在且為 ancestor。精確列出已批准文章與兩張 PNG 的 predecessor mode／hash 與最後 mode／hash；由受審查 guard 固定紀錄位元組與精確路徑集合。前版身分須與 Git 一致，重疊路徑亦須符合先前元件期待值；修訂紀錄在未變動的元件 epoch 之後套用。修訂存在時要求元件紀錄存在；新版 overlay 存在卻缺修訂紀錄時拒絕。所有舊紀錄、digest 與 guard 規則保留；來源盤點繼續拒絕 ignored／untracked 未知路徑。guard 與測試接受獨立審查，不以循環雜湊自證。

已批准文章 SHA-256：f36261ac4208d55d73c5c1250c3c96bf419cbadbfa053fd33b45f40af4969e34；貓梗圖：8a841ead65839eb117ce054edf84402c2f76baaab77acb0e8e22946cc671f3a7；半夜電鍋梗圖：99aead19c23b41ab372d1080e51fdc32ba5bf8f463e42d035794b29a4631441e。最終 mode 均為 100644；文章 predecessor 為 7d7df900fe0bb3da0dc8beb8e8e146dab9326cccdf57d12d0c25fcf2a708bcc0；新圖 predecessor 不存在。

## 驗收條件
- A1：精確文章／圖片 overlay 通過公開 CLI，保留使用者來源位元組；不修改 theme、config 或其他文章。
- A2：文章／圖片 byte、mode、missing／linked 輸入，以及含 ignored 檔的第四路徑皆失敗。
- A3：predecessor／hash／record 竄改、absent／missing／nonancestor pin、歷史改動皆失敗；舊紀錄逐位元組不變。
- A4：既有 harness／publication／unit／lint／build／materializer／structure 檢查通過，獨立 Standards／Spec／Security 審查 findings 已處理。
- A5：已授權非 force push staging 後，追蹤 exact SHA 自動部署並驗證真實 preview；main 與使用者未提交分支不動。失敗如實回報，不宣稱成功。

## 測試決策
沿用已批准的 Python unittest 與公開 verifier CLI seam，在 disposable 真實 Git clone 執行。先寫一個失敗的接受測試，最小實作通過後逐個驗證信任邊界的拒絕案例。歷史 fixture 使用不可變 Git epoch 位元組，不複製可變新版文章。沿用已安裝 toolchain，不安裝或新增測試 runtime。

## 不在範圍內
一般 successor engine、任意 allowlist、自動更新 hash、改寫舊紀錄、main 發布、同步使用者分支、CF 設定／手動部署、Notion 與 Library 上傳。

## 補充
使用者在揭露原因後明確批准這個 guard 與 staging push；單一完整票與既有 seam 已由有界提案確認。公開證據不包含原對話識別碼或私人路徑。回復 guard 時一併移除本次紀錄及 guard extension，恢復先前精確檢查；產品 rollback 仍需新的授權。本次延伸 T-0005 精確 successor 模式；原規格不發布的範圍仍保留為歷史。
