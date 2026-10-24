# T-0027 先行來源與行為檢查

這是批次實作中的先行檢查，不是正式 stage-6／全套驗收結束。使用者已授權 B～D 全部實作及一個 A～D PR；全組合 coverage、完整回歸與正式 source／security 關卡仍須完成。

## Standards

獨立 reviewer：documented violations 0；重要 smell 0。擷取範圍為 /private/tmp/0x1dea-article-evidence/review-B 的 20 個檔案，base＝HEAD＝merge-base `f1f753a7ee9e4c30043156379351a870a02f4fb8`，分支 tickets/T-0027/free-conversation-entry；確認無漂移。已知第五套件保留原四套件 fixture 與三樹中文例外，來源逐名 pin，工程／文章分工未繞過工具流程。

## Spec

獨立 reviewer：0 P0／P1／P2。先回應、直接起稿、只聽、作者保護與 Phoenix 觸發符合來源要求；沒有暴露不存在的 C／D 參照。舊 Phoenix 測試與 runner 未改，新歷史脈絡在執行前指定並綁定 bytes；current counterpart 保留原三個負向方法，未發現失敗後切換舊版洗白的來源證據。

## 行為稽核

另一個獨立 reviewer 依實際 Codex 輸入／回應／讀取動作及檔案差異判讀。先確認 12 組未見已證實缺陷，指出受眾變更及可取得來源尚缺觀測；補跑 B05 同 session 與 B07 提供標頭／實際讀 fixture 後，確認補足、無新增 P0／P1／P2。未把 fixture 當 live lookup。Claude OAuth 過期仍為未驗證。

## 限制

來源 reviewer 未執行 code，行為 reviewer 不代表完整程式審查。正式報告及本機檢查證據的 metadata 納入屬擷取後有限差異；最終批次審查仍需包含它們。沒有全套通過或 landing 宣告。
