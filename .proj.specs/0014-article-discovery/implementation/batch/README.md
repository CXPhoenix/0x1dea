# 0014 A～D 批次驗證與 PR 準備

使用者已追加授權 B～D 一次完成，A～D 共同開一張 main PR。四票維持永久相依與 review；尚未 landing，不提前稱整個 epic 結案。產品原則是「先自由聊、按需整理」。

## 結果與範圍

| Seam | Tests | Measured coverage | Acceptance criterion | Uncovered, and why |
|---|---|---|---|---|
| X01 原生跨階段 | B 15 組／20 輪；C 33 組來源階段觀測／46 輪；D＋X01 17 組／22 輪 | Codex 實際呼叫、多輪與 fresh session、實際保存／讀回及獨立行為判讀；各票表逐列對照，不以百分比代替 | AC-01–13/17 | C 包含修正前後重跑，非 33 個相異 final-source 案例；Claude OAuth 過期，未驗證 |
| X02 完整 Python | current Harness 66＋current article-publication 193＋原 #22 10＋原 #32 14＋原 Phoenix 4 | 287 項，零失敗／錯誤／略過；固定重跑 exit0 | AC-14–17 | 本機合成 Git／REST／隔離 build，非 live GitHub／P13 |
| X02 既有網站程式回歸 | pnpm test:unit；pnpm lint | Vitest 54 項成功；lint 成功，無新 Warning | AC-16 | 未改網站介面；不聲稱 browser 渲染／裝置／完整無障礙驗收 |
| X02 套件／來源 | portable、materializer --check、quick_validate、native current＋雙角色同時筆記 | 37 技能結構；185 產生檔／59 來源；原始型態與命名、雙 runtime、有限 source 身分及保存前／後相容；最後 metadata 另跑精確 gate | AC-14–17 | 靜態套件存在不代表 Claude 執行成功 |
| X02 保存稽核 | preservation.json | 凍結規格／trace／提示、36 核准列、388 個既有文章／聲音／framework／E1～E8 檔及 56 個 A 保護 pin 保留；唯一既有測試修改是具名 live fixture 兩項清冊 owner | AC-16 | maintaining-writing-skills 的 live writing-process 為核准替換，非凍結聲音修改 |
| X03 獨立判讀 | Standards／Spec／Security＋native 行為 | 正式來源 Standards 0 違反／重要 smell、Spec 0 P0／P1／P2、Security 0 HIGH／MEDIUM 候選；C 先行 P1 已修正並 fresh 重跑 | AC-15/16 | 原始 local trace 只以 SHA-256 綁定；來源 reviewer 不冒稱執行所有 host；最終 metadata 補審另記 |

完整命令、耗時、來源快照及初次失敗在 [command-results.json](command-results.json)、[完整 Python](full-python.txt)、[初次完整失敗](initial-full-python.txt)、[原失敗案例修正後](focused-regression.txt)。Vitest／lint 分別見 [unit.txt](unit.txt)及[lint.txt](lint.txt)。[來源保留稽核](preservation.json)、[雙角色筆記](notes-coexistence.json)與[固定回歸來源](regression-source-snapshot.json)分開保存。

## 真實回歸與修正

第一次完整執行兩項失敗，不宣稱成功：兩份新 .log 雖已追蹤，在測試的重新產生候選樹中仍會被 git add 忽略，導致精確來源集合缺檔；已以完全相同 bytes 改名 .txt，沒有改 ignore 或放寬來源檢查。另一個 live head-reporting fixture 固定要求 staging 舊四套件清冊，與已審查 main 五套件 successor 衝突；只將兩個精確清冊的預期身分綁定獨立 pinned main，保留其他 protected checks 和所有 assertions。修正來源後，第一次 focused 呼叫尚未同步該測試的精確 common pin 而拒絕，保留於 [中間失敗](intermediate-source-pin-failure.txt)；同步該具名身分後，兩個原失敗案例均成功，最後完整 287 項再次執行成功。

原 current runner 與預定歷史模組完整保留。新 runner 在執行前即選定 #22、#32、Phoenix 四套件的固定歷史脈絡並比對原測試 bytes，從未將本次失敗案例移到較舊版本；current 五套件 counterpart 繼承原三個負向方法，另驗證原聲音與五套件契約。D 的 expressive／rich 前測原本就成功，明列為回歸，沒有捏造 red。

## 可核對的限制

原生行為證據分別見 [B](../T-0027/native-results.json)、[C](../T-0028/native-results.json)、[D／X01](../T-0029/native-results.json)。C 的 write-only 0200 實際寫入成功但讀回失敗，明列未驗證；父程序測後查驗再還原權限。自訂筆記保留原位及 policy，guard 具名拒絕，不阻止獨立正文。C legacy 有 Python cache 執行產物，不能概括為全檔案未變。D01 pnpm 啟動器受本機 socket 限制，改以 node --import tsx 執行同一原 CLI 成功；沒有手刻文章或安裝。X01 最終共用 fixture 快照與保存當輪讀回分列；實際 web_search 事件未附完整來源回傳，不能據此宣稱完整來源查證。

這是非瀏覽器的 native CLI／對話／檔案表面，沿用 ADR-0006 的 owned subprocess 與獨立 writer／judge 驗證分工。未動原工作目錄已追蹤來源、真實作者文章、帳號、trust、credential、全域技能或外部索引。PR、merge、部署與發布各有自己的結果；本批次只準備一張已授權的工程 PR。

[正式 Standards／Spec 審查](../../review/code-review-batch.md)與[安全審查](../../review/security-batch.md)保留各自結論及限制。landing 後的 chain analysis／evidence-report／retrospective 仍依原 workflow，沒有提前偽造完成紀錄。
