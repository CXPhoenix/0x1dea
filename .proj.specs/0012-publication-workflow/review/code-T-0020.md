# T-0020 獨立程式碼審查

來源：`T20-review-source-v2`；SHA-256 `39f200dc836be53c2205fa925d30cafb903fac3a8c5164c0ef9dd3aca995c30a`。base／merge-base `8b31956f47075a831cfd0339339f616af96b3dae`，HEAD 為共用登記 commit `1a82f59c4c949f5e6b25b69d96a281ec3c229d2e`，含已列明 pending／untracked。

## Standards

獨立 reviewer `t13_sync_standards`：P0／P1／P2＝0／0／0。變更限核准工程、管理、inactive 範本與精確 successor；候選、歷史與正式設定未改。T-0022 曾有 PR 投影重複的 P2 建議，已改用共用純資料投影。

## Spec

獨立 reviewer `t13_sync_spec`：P0／P1／P2＝0／0／0。B2 消費端原先會於驗證後另開檔；現在同一流程直接使用已驗證的記憶體值。公開反例與修正後結果保留於本票 evidence。

兩軸為唯讀 source review，沒有自行執行候選或遠端操作。來源完整測試由 parent 執行，見 execution.json；最終證據補審另列。審查成功不等於實際落地、P13 或 done。
