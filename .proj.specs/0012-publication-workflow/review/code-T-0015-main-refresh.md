# PR #26／T-0015：目前 main 的獨立程式審查

日期：2026-10-15。base `b84321dfeb23e155de923e6fdf799f261e3cd1c9`；
起始 HEAD `1f13b030eaf322a5ace4c469dfeda453844819f7`；merge-base
`b4e87c2453c47010cd82e6789dbb4be3cea0b28f`。只在 T15 topic 整合 main，
MERGE_HEAD 為 base；目標 main／staging 未 merge。各次 committed／staged／
unstaged／untracked 分開捕捉；來源56檔、最終含證據82檔，hash／patch／狀態均無漂移。
來源 capture 與初始三方選擇見 implementation/T-0015/main-refresh-20261015。

## Standards

獨立 reviewer 最終未解 P0／P1／P2＝0／0／0，未發現新增 smell。
engineering manifest 使用三方逐 key 整合：main282＋topic237→336，保留 main
的T14程式／測試／證據身分，唯一既有main identity更新為T15ticket；新證據另以
逐檔mode/hash列入，沒有資料夾豁免、候選、歷史或部署路徑覆蓋。

輸出完整性修正重用既有blob checker，沒有重複實作。公開CLI回歸沿用核准P09
seam，一項測試含工程／候選兩個子案例，來源與receipt保留；raw red兩次失敗、
green通過。README為台灣繁體中文，raw logs／舊127／no-op／158 checkpoint保留。

## Spec

另一位獨立 reviewer 最終未解 P0／P1／P2＝0／0／0。
AC05／P09完整tree、獨立bare merge、候選完整mode/blob及protectedchecks與
local AC06／P10重讀pins維持原契約。`staging-sync.py:368–371`以獨立重算的
可信完整expected清單核對受驗output blobs；`:186–209`檢查type／長度／OID，
補上原verify只比mode/OID的缺口。文件明載當次驗證及後續寫入前重驗，不擴大權限。

最終raw為66liveharness＋83livepublication＋10固定#22＝159，含24sync／31v2；
failures/errors皆0；54unit及build/lint/各guard證據一致，實際隔離build binding／
outputdigest相符，外部read/write/net皆denied。歷史modulebytes先檢查，再執行
原code/tracker；沒有失敗後換契約。T14與v1／原assertions／M0未改動。

實際mainb843／stage035完整registry與Git trees相符：498差異由候選及460工程項
完整分類；六候選50路徑、382checks保留。Reviewer唯讀重算result確認1758個
不同blobs的type／長度／OID正確；prepare/verify一致ready/publishablefalse。
來源前後refs/index/status/objecthashes相同。Stage source pin是保留快照，不是
clean-publication provenance；尚未包含未落地#26，也不證明stage已同步。

## 驗證責任與限制

Reviewers全程唯讀、未執行候選程式；父agent執行新159、54unit、build/lint/
native/structure/materializer。加入metadata後三項guard另exit0；來源等於已審
fixedpacket。保存報告後須再更新有限map、驗證及commit後核對，不能提前當完成。
T15維持review；遠端writer／CI、HTTP、作者核准、部署及實際雙目標落地另行驗收。
