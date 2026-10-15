# 共同工程基底與 current successor

T-0013 在已核准 M0 上建立一份工程變更，供 main 與 staging 共用。main 只保留已發布文章；
staging 保留候選文章、既有網址上的未發布修訂、圖片與原始 frontmatter。這個工具不發布
文章，也不執行 merge 或修改部署設定。

## 可信執行位置

從**已審查的控制 checkout** 執行工具，將受驗 checkout 傳給 `--repo`／`--root`。
控制 checkout 的 M0 ancestry 決定 main／staging 角色；受驗目錄、候選政策及 CLI role
旗標不能改變角色。若控制 checkout 含 staging 的固定 ancestor，結果明載為 staging；
消費驗證結果的流程必須比對自己的目標角色及 base。不能把 staging 結果當成 main 驗證。

不要執行未審查候選內的 validator 來證明候選安全。執行中的程式碼、M0 原始盤點與精確
engineering-v1.json 是控制平面的可信輸入；受驗 checkout 只提供 Git metadata 與檔案。
工具不宣稱能抵抗控制平面本身遭竄改。後續 CI 必須從可信目標取出工具，不能從 PR head
執行政策或程式碼。現階段沒有啟用 CI、自動同步或部署設定。

## 本機指令

```sh
python3 scripts/publication-baseline.py --help
python3 scripts/publication-baseline.py prepare --output /absolute/new/output
python3 scripts/publication-baseline.py verify --repo /absolute/candidate
python3 scripts/verify-harness-adoption.py --root /absolute/candidate
python3 scripts/run-python-tests.py
```

`prepare` 只接受新的外部輸出位置，建立兩個獨立 clone，固定 HEAD 與供歷史 landing
fixtures 使用的 main／staging refs，再套用逐檔列出的共同工程變更。既有輸出與原始
checkout 不覆寫。不使用 Git merge；兩個目標分支也不前進。

`verify` 比對完整來源清單、mode 與 SHA-256，包含被 Git ignore 的文章與管理檔案。
只有明列的 dependency／build／bytecode 產物資料夾略過，且不能是 symlink。沒有管理
資料夾的整體豁免。精確政策不得加入候選、blog、部署、三套既有寫作技能或歷史契約的
overlay；既有工程檔案只有新版 entrypoint 可以更換，其原版本另行封存。

輸出固定 `publishable: false`，包含角色、M0 base、受驗 HEAD、路徑數與 tracker 狀態。
本機 pass 不是 main／staging 落地、文章發布、遠端 CI 或實際網站驗證。

## 歷史契約與新契約

main／staging 的原始 verifier 完整保留於 `maintenance/publication-workflow/history/`，
轉接層只載入 M0 固定 Git commit 中、SHA-256 符合的歷史程式碼；不載入候選程式碼。
舊 fixture 仍用原契約判定，既有 assertions 不改。current 路徑則執行共用的精確 successor，
不把歷史 snapshot 當成可變 tracker 的 oracle。

工程邊界的 authoring 是維護者審查工作，不是 validator 的自動修復功能。工具不會從
目前檔案自動重設預期 hash，也不提供自行核准、role override 或整體豁免指令。新增或
變更共同工程路徑必須先建立明確邊界，再完成同等審查。

## 結案

T-0013 的 done 除既有核准收據與 staging ancestry 外，還要求 main／staging 的實際
landing commit 包含本次工程程式碼。拿 M0 ancestor 或 PR-ready 收據不能結案。歷史
ADR-0006 保留；main-first 設計見 ADR-0008。未 merge 的本機驗證樹不提供落地證據。
