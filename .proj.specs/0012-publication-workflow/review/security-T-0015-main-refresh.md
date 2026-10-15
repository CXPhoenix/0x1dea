# PR #26／T-0015：目前 main 的安全審查

範圍與Git身分同code-T-0015-main-refresh.md。完整56檔來源與最終82檔證據分層
capture，hash均吻合；T14已落地內容僅作context，不是本PR的新增行為。
最終未解HIGH／MEDIUM＝0／0；不宣稱全專案安全。

## 已確認並修復 MEDIUM：輸出 object bytes 未驗證

類別data_integrity。Security reviewer提出confidence0.85；另一位獨立偽陽性
reviewer保留MEDIUM、confidence0.90。前提是攻擊者可在prepare與verify之間
寫入外部bundle的result.git/objects；僅文章commit權限不足，不需修改controller、
source repo、registry、receipt或refs。這是明確兩次公開操作間的竄改，不依賴理論race。

原verify重新compute來源後，只對輸出identities比較mode／OID；既有
check_source_blobs只驗來源。因此可在輸出store加入同OID檔名的loose blob，遮蔽
alternates中的正確內容，原receipt/tree仍相符，verify卻回ready/local_readytrue。
父agent安全公開fixture重現：來源與receipt不變、輸出實際為替換文字，verify exit0。
證據output-reproduction.json與output-red.txt保留。

影響限於輸出artifact再驗證／候選保留的完整性判定錯誤，不是泛泛硬化；未證明
registrydigest變更、RCE、sandbox逃逸或實際發布。若輸出儲存完全可信且不再使用
原bundle，暴露可降低，但目前verify契約沒有以此取代實際內容驗證。

修正於`staging-sync.py:368–371`使用獨立重新計算的完整expected結果清單，先確認
receipt/mode/OID，再重用`:186–209`checker檢查受驗store全部blob的type、長度、
完整batch輸出與Git內容hash。來源檢查及offline Git限制不變，沒有輸出可控命令。
新公開回歸一項、工程與候選兩個子案例，真實red兩次錯誤准入→green拒絕，
回報具體path且來源與receipt保留。獨立Security覆核原路徑封閉，無新增符合門檻漏洞。

## 整合、證據與限制

三方精確map保留main所有T14來源與證據，只有T15ticket採本票review版本；
後續改動限T15controller/test/docs與逐檔證據。最終metadata362個mode/hash一致，
無blog／部署overlay或自動政策入口；保存本報告後仍需最終有限map與native核對。

新159＝66＋83＋10的raw結果無failures/errors；原158不當作修正後pass。
54unit/build/lint及guard有實際紀錄，actualT14隔離build外部read/write/net denied，
合成local-ready binding相符。實際registry2113/2317完整trees、498差異分類、
六候選50mode/blob、460工程項與382checks一致；actualprepare/verify皆ready，
publishablefalse。來源前後snapshothashes相同，未把尚未落地#26納入actualmain。

當次輸出驗證不能保證驗證後儲存不再變更，正式寫入前仍須重驗。local_ready只代表
本機CLI，不當作nativeCI／HTTP／作者核准／stage已同步／部署就緒。
Reviewer唯讀未執行PoC；父agent執行tests／實際CLI。排除可信controller遭入侵、
依賴掃描、可用性、遠端writer／CI／部署及epic chain analysis；commit後readback另做。
