# #20 合併後的 #21 同步

本輪把已核准的共同工程與結案紀錄同步到 staging，更新原 PR #21；不發布候選文章，不 merge PR，也不修改部署設定。固定來源：main `5e6c889c808e7ef4cb83493bf06f8a70dd055b41`、staging `035783590895a426ee395045829ebc9d50e2b9cf`、原 #21 `a67b8de69f70f794a9e062e3ac50a957688ffa9a`。

保留原分支歷史，以目前 main 的已審核共用 controller、helper、原 assertions 與工程 manifest 為同步來源。四個衝突檔案的來源與理由列於 conflict-decisions.json；原 #21 的 helper／fixture 修正不再帶回，原版本仍在 Git 歷史中。

T-0001、T-0002、T-0010 的結案事實與 T-0005、T-0011 既有 done 一起同步；T-0003、T-0004、T-0008、T-0012、T-0014、T-0015 不提前結案。T-0011 的 done 指原 PR #19 已落地工作，不表示這次 #21 已合併。

沿用原核准 native CLI、Python、Vitest、lint、隔離 build 與實際瀏覽器測試介面。新測試結果與原歷史紀錄分開保存，詳 authority-and-tests.md 與後續 coverage／review 紀錄。
