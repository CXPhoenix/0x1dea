# 指定文章 v2 本機驗證

`article-publication.py` 的 v1 契約與歷史測試維持原樣。明確 v2 入口為
`python3 scripts/article-publication-v2.py --help`；`schema` 印出完整結構文件。
此工具只處理本機候選與驗證，不會 commit、push、開 PR、merge 或修改部署設定。

## 控制資料與信任邊界

plan 宣告 repository 的絕對路徑、main/staging 的 ref 與完整 SHA、恰好一個
selected article，以及其精確 dependencies。registry 是經作者與工程審查的控制資料，
不是文章 frontmatter；呼叫端必須另行提供經審查的原始 registry SHA-256。
自行計算一份候選所選政策的 digest，不會使該政策獲得授權。

registry 包含完整 staging mode/blob 清單、每個候選（含既有文章修訂與獨占資產）的
精確 paths、獨立來源 pin、必要依賴、明確 integration commit、anchor 與 retained
工程差異。exclusive paths 不得重疊；shared_patches 逐 commit/path 綁定 before/after
mode/blob，不是整個資料夾豁免。retained 必須是精確 staging identity，不能豁免
`blog/post/` 或 `blog/public/`。完整結構見 `article-publication-v2.schema.json`。

clean source 必須源於目前 pinned main。已整合進 staging 的 source 本身仍可使用；
所有 v2 Git 讀取明確禁止 lazy fetch 與 remote transport，拒絕 partial/promisor 設定。
讀取 baseline、staging 與來源 blob 時，也會重新計算 Git blob OID，拒絕內容與已核准
OID 不符的 object；`cat-file` 成功本身不代表內容雜湊已驗證。這項檢查限於 v2，
原 v1 helper 與歷史 assertions 保持原樣。
source 不能包含 staging integration、另一篇候選或未申報的歷史 commit，包含加入後
還原的內容。main refresh merge 以獨立 bare repository 重算；衝突須在 registry 的
resolutions 明確綁定完整 commit/tree，無衝突的結果不能被該欄位覆寫。
legacy 須有原始／重建 SHA、精確抽取 mode/blob 與作者核准 binding；這項入口不會
搬移或改寫目前的六個 legacy 候選。

## 執行順序

以下 digest 與路徑由經審查的呼叫端帶入，不是工具自動重新信任的值：

```sh
python3 scripts/article-publication-v2.py prepare --plan PLAN --registry REGISTRY --registry-sha256 REVIEWED_DIGEST --output NEW_BUNDLE
python3 scripts/article-publication-v2.py verify --plan PLAN --registry REGISTRY --registry-sha256 REVIEWED_DIGEST --output BUNDLE
python3 scripts/article-publication-v2.py build --plan PLAN --registry REGISTRY --registry-sha256 REVIEWED_DIGEST --output BUNDLE --runtime RUNTIME --runtime-sha256 REVIEWED_RUNTIME_DIGEST --build-output NEW_BUILD_BUNDLE
python3 scripts/article-publication-v2.py ready --plan PLAN --registry REGISTRY --registry-sha256 REVIEWED_DIGEST --output BUNDLE --build-receipt BUILD_RECEIPT --build-sha256 REVIEWED_BUILD_DIGEST --approval APPROVAL --approval-sha256 REVIEWED_APPROVAL_DIGEST
```

prepare 重建 main 加指定文章與核准依賴，保留原三個 literal aliases，並拒絕其新增、刪除或任何變更；輸出須為 repository
外的新路徑。verify 重新核對 refs、准入、receipt 與完整實體檔案 bytes/modes；任何新 link、
submodule、escaping include、active import 或篡改均拒絕。Git objects 寫入暫存區，來源
refs/index、dirty files 與 object database 不會被修改。

runtime JSON 的欄位恰為 version:1、node、node_version:"v24.13.0"、dependencies；
兩個路徑指向既有、經審查的 Node 與 node_modules。固定執行 Node 的 VitePress build，
不執行候選選擇的 shell/package scripts、不安裝套件。現有實作使用 macOS sandbox-exec；
缺少受強制約束的隔離／runtime 時直接拒絕，沒有 unrestricted fallback。

build 使用另一份暫存 source，限制讀取與寫入範圍並禁止網路。inside read、outside
read/write 與有效 localhost listener 四項探針必須符合預期，才執行實際 build。產出獨立
build receipt、stdout/stderr 與所有 output 的 inventory；來源檔案在 build 子行程中唯讀。
單次 build 成功仍是 pr_ready:false。

approval 欄位恰為 version:2、record_id、binding、preview。binding 綁定完整 verify
report 的 canonical SHA-256；preview 必須有 staging_sha、served_sha、evidence_sha256，
兩個 SHA 均須等於 plan 的 staging。這是呼叫端已審查的實際預覽／作者核准證據，
工具不能自行產生授權；合成測試的 record_id 不代表實際網站已驗收。

ready 重新核對來源、完整 build output、分開提供的 build 與 approval digests，並掃描
全部檔案（包含 route、listing、search、RSS、資產）。B 已發布 baseline 可保留；未核准
新增內容與修訂拒絕。signature scan 是補充檢查，不能取代 source/tree/binding；缺少
可辨識 signature 時標示 exclusion-unverified 並拒絕 ready，沒有手動略過選項。
ready 只回傳本機 PR 準備狀態，publishable 永遠為 false；PR、落地與 HTTP/browser
驗收仍須各自取得授權與證據。任一 pin、policy、依賴或候選變更都使原核准失效。

## 測試範圍

`python3 -m unittest discover -s tests -p test_v2.py -v` 使用 remote-free Git fixtures。
實際 build 測試需要 macOS、現有 Node 24.13.0 與 toolchain；可透過
`PUBLICATION_TEST_DEPENDENCIES` 指定已審查的既有 node_modules。缺少平台/runtime 會
明確 skip，不能當成隔離或 readiness 成功。主機 sandbox 也可能阻擋父程序的 localhost
listener；應保留失敗、於授權環境重驗，不能改成未受約束的 build。

加入 article-discovery 第五套件後，目前完整驗證入口是
`python3 -B scripts/run-writing-python-tests.py`，並沿用上述既有相依套件前置條件。
current suites 與預先固定的 #22、#32、Phoenix 四套件歷史契約分開列出；current
五套件 counterpart 保留原負向方法，另核對原聲音與五套件。原
`run-current-python-tests.py`、`test_current_baseline.py` 與固定歷史模組的
bytes/assertions 保留，不在失敗後更換契約。當時 review→done 的反事實測試使用
當時 code/tracker，新的 closed-tracker cases 仍核對目前已落地的 T-0013。
歷史成功不代表現行 v2 程式成功，實際結果以當次完整命令與範圍為準。
