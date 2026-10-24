# T-0028 先行來源與行為檢查

範圍：/private/tmp/0x1dea-article-evidence/review-C 及 review-C-fixed 的 16 檔；base＝HEAD＝merge-base `383e670589b929a9df25119760aefef2b89251f3`，分支 tickets/T-0028/optional-context-glossary。兩個唯讀來源 reviewer 核對擷取與 checkout，無漂移。本檢查點不是正式批次驗收。

## Standards

0 documented violations、0 重要 smells。保存授權、原始 key、實體目的地、讀回失敗如實揭露，以及 canonical-only／三樹中文例外符合專案規範。未改原 voice 或歷史。

## Spec

初次 0 P0／1 P1／0 P2：persistence.md 把「沒有 designation」與「已指定 target 不存在」混用，可能讓唯一 legacy 再被追問。已改為 `a designated target is missing/invalid`，canonical 與雙 runtime 同步；獨立補審確認 resolved，剩餘 0 P0／P1／P2。其他差異只為精確來源身分。

## 獨立行為判讀

初版案例未見已證實行為缺陷，卻缺單獨 . key；修正版補齊。全新 fixture 的保存／標題、選擇狀態／fresh resume、首詞、三種唯一 owner 與三類衝突均 confirmed。真正 current main／staging 的 before／create／update／legacy exit0，3405／3554 個工程來源身分不變；custom exit1 正確具名、保留筆記且續寫。沒有把列出阻擋改報成功；Python cache 執行產物另列，不概括成全檔案無變化。

## 限制

來源 reviewer 未執行 code；行為稽核不代表完整程式／安全審查。Claude OAuth 過期未驗證。最終全套回歸、正式 Standards／Spec／Security、跨票整合與實際 PR gate 尚待批次收尾，票沒有 falsely done。
