# 0x1DEA Harness Agile 本機驗收

本文件先記錄完成的本機驗收。使用者於 2026-10-04T11:53:10Z 另行授權 commit 並非強制推送到 staging 供檢查；目前 publication preflight 已完成，實際 landing 尚待 commit/push 後 remote SHA 核對。沒有 main merge、另行部署或外部設定修改。工作區為獨立 clone，分支 `tickets/T-0001/harness-adoption`；HEAD 固定 `ee7fecfff72f47abc735d26ac7e9a943de04ebbf`。

網站 55 個檔案完整搬到 `blog/`，內容與網址保留；工程文件留在 `docs/`。六個 capability、四份歷史 archive 與原證據逐檔保留，沒有補造過去的 review。Codex／Claude 各有 32 個 framework 與 3 個實體產品 skill；三個產品從 canonical source 決定性產生。繁中 v2.2 三份核心原文未改。

| 驗收 | 實際結果 |
| --- | --- |
| 母範本 | 原始 22 tests；固定 snapshot 718 檔 digest 重算吻合，737 個 Git tracked 檔另行核對 |
| 實體套件 | 21 tests；52 pinned input、169 output；35＋35 skills，runtime 無 symlink |
| Tracker／provenance | 26 tests；370 baseline entries、55 精準搬移、641 framework pins、113 原始 trace rows |
| 雙語 | 7 pairs；32 requirement、81 scenario、230 條件句、9 trace blocks；英文基準逐 byte 保留 |
| 產品 | 11 unit tests、實際 build、8 個隔離 CLI cases；77 個 build 檔與 baseline 全部 byte identical |
| 新寫作 | E1–E9 九位隔離 writer 的首次回答；三位獨立 judge，各例 10／10、零 hard fail；3,587 項機械核對 |
| 歷史寫作 | 實跑 31／30／62 checks；不改舊答案或原證據 |
| 原生探索 | 新 Codex app-server `skills/list forceReload`，35 enabled repo skills、errors 空 |
| UI | baseline／candidate localhost 實際操作：清單／卡片、搜尋／排序／分類、鍵盤、圖片、sidebar、深淺色、390×844 手機及粒子 smoke |
| 回復 | disposable clone 真正套用轉換再 reset／clean，370 entries 還原；重跑 11 unit／8 CLI／build，Git 乾淨 |
| 獨立審查 | Standards／Spec 各 P0／P1／P2＝0；security 無 HIGH／MEDIUM 候選；原問題與修正回執完整保留 |

公開回執保留實際命令語意、起迄時間、exit code、原始 SHA 與明示的本機路徑投影。完整私有 raw logs 留在 Mac；失敗與 red→green 過程請見 [coverage-report](../../.proj.specs/0001-harness-adoption/coverage-report.md)、[可攜 evidence](evidence/README.md) 與 [evidence SHA index](evidence/final-manifest.json)。[工作票](../../.proj.tickets/0001-harness-adoption/T-0001-harness-adoption.md) 停在 review；done 需依既有授權完成實際 landing 並核對 remote SHA。

已知限制：原生 CLI 曾因帳號不支援指定 model 回傳 HTTP400，保留為 blocked；沒有改 model 或全域設定，寫作以另行授權的原生 collaboration 完成。Claude／Gemini 的 fresh native host discovery 未執行。113 個歷史列中，28 列有完整 fresh 驗證，85 列保留 not-run，另附 inherited integrity 證據；沒有以 source hash 或 build 成功冒充完整行為驗證。

寫作時間與 dispatch 來源、judge 報告補存／E1–E3 重新獨立評分的 provenance 均已標明；不以 output 宣稱沒有工具行為。雙語檢查覆蓋結構與識別字，沒有宣稱人工翻譯認證。UI 為實際 smoke，沒有做粒子效能／reduced-motion benchmark。

baseline 本來就有空搜尋結果隱藏控制項與四個 FontAwesome CSS404；candidate 相同，未引入新回歸。既有 README 圖片參照與小寫 vphelper import 也保持原樣。靜態手機文章截圖 byte identical；粒子背景使清單截圖像素不同。

Cloudflare 僅根據使用者提供、parent 檢視的畫面留下 [handoff](deployment-handoff.md)，沒有登入修改或驗證正式部署。Production main 需先實際包含 blog；root dependency watch paths 的建議需另行處理。母範本 release CI 沒有套入本案。

來源 repo 與母範本最後核對乾淨且固定 SHA／digest 吻合。無安裝軟體、憑證／安全設定修改、Notion 更新或原始 checkout 寫入。175 MiB 完整 source／pending diff／raw evidence 私有封包留在 Mac，SHA 為 `edf74f9816a6d39b714ec34283ba450ceabf6ca31c38fafc68a8d4036885c176`；沒有上傳。公開 repo 的三份大 diff 僅保留原大小／SHA與省略理由，見 [publication-projection.json](evidence/publication-projection.json)。公開複本不是 byte-identical raw logs／reports；本機路徑以占位符取代，receipt 綁定公開 log SHA 並保留私有原 SHA。

![手機文章驗證](evidence/candidate-mobile.png)

Publication preflight 新增真實 Git graph ancestry 邊界（baseline／descendant 接受、unrelated／missing 拒絕），以及該 test file 的精準新增檔 allowlist 反例；50 個 Python tests、11 unit、build、main／runtime／project checks 實跑通過。未重跑無變更的 writers／UI／rollback；原結果及限制保留。ESLint 檢查涵蓋此輪 13 個 JS／TS／Vue，但既有設定缺 `@unocss/eslint-plugin`，CI mode exit2；先前 exit0 只停在安裝提示，不是 lint 通過。未安裝、關閉規則或刪 assertion。原 checkout 有 `npx lint-staged` hook 但依賴缺失；isolated clone 只有 Git sample hooks，正常 commit 不使用 skip／no-verify flags。
