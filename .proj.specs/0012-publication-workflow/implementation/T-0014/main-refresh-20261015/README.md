# T-0014／PR #25：以目前 main 重新驗證

日期：2026-10-15（Asia/Taipei）。實際 main 為 `c1dd3bbde1b9522bf88692014866fbc18aaf1173`
（#24 已合併）；staging 為 `035783590895a426ee395045829ebc9d50e2b9cf`。
本輪起始 #25 HEAD：`f737e36601795bd6a5ea9e3f6cf61467b31d0a52`；merge-base：
`b4e87c2453c47010cd82e6789dbb4be3cea0b28f`。#24 的檔案樹與共用 parent 相同；
起始版本的獨立 merge-tree 結果等於 HEAD tree，因此不需要 merge、rebase 或改寫歷史。

使用者已授權重新驗證、必要修正、commit、非強制 push，並更新原 #25；不授權目標
分支 merge 或部署設定變更。#20、#21、#26 未納入或更新；T-0014 維持 review，
須待核准的雙目標實際落地與完整驗收，才能標記 done。

## 原因與修正範圍

Security 與另一位獨立偽陽性審查者確認一項 MEDIUM 來源完整性缺陷：Git cat-file
可以讀出遭竄改的 loose blob，而未重新計算其 OID。因此，即使可信 registry、refs、
OID 不變，未核准內容仍可能進入 v2 候選。攻擊前提是能寫入本機來源 object database；
只有文章 commit 權限並不足。未證明 owner approval binding 可被繞過、sandbox 逃逸
或實際發布。

修正限於 v2 Git wrapper：每次讀取 baseline、staging 與所有來源 blob，依 Git 的
header／長度／內容重算 SHA-1，比對 OID，不符即於輸出前拒絕。v1、歷史 helper／
assertions、receipt 與 M0 均保留。新增一項公開 CLI 回歸測試，含 baseline/index、
指定 A、未指定 B 三個子案例，並非新增三項測試。raw red 記錄三次錯誤准入；green
確認拒絕、未產出候選及 refs 保留。另以公開 verify 確認準備後的 object 竄改也被拒絕。

## 本輪驗證與覆蓋

| 核准測試列／範圍 | 證據 | 結果 | 實際表面／限制 |
|---|---|---|---|
| P04–P08／AC03,04 | python-current.txt | 通過 | 不連遠端的 Git／CLI fixtures；未搬移真實 legacy 來源 |
| P14–P15／AC08 | python-current.txt | 通過 | 精確指定樹、其他修訂／資產排除；來源與產物 fixtures |
| P16／AC07,08 | blob-red/green、blob-verify.json、python-current.txt | 通過 | blob 不符遭拒；一項真實 red→green，三個子案例 |
| P17／AC08 | actual-build-receipt.json、build stdout/stderr | 通過 | 固定 Node24.13.0 實際 VitePress CLI 與 macOS 強制隔離；非 HTTP 驗收 |
| 共用現行／歷史契約 | python-current.txt | 66 live harness＋59 live publication＋10 固定 #22＝135；failures/errors 皆 0 | 原歷史測試先核對 bytes，再以當時 code/tracker 執行；沒有失敗後切換契約 |
| 網站回歸 | unit.txt、website-build.txt、lint.txt | 54 unit、實際 build／lint 均 exit0 | main 網站來源；非部署證據 |
| Native／structure／materializer | native-preflight.json、structure.txt、materializer.txt | 通過 | 加入本輪證據前的 preflight；最終 metadata／commit 另驗證 |
| 候選與歷史保留 | preservation.json | 六候選、50 個持有路徑 mode/blob 零差異 | 實際 pinned staging；blog／部署／技能／歷史 helper 未修改 |

完整命令為帶入既有、已審查 node_modules 與暫存證據路徑的
`PUBLICATION_TEST_DEPENDENCIES=... PUBLICATION_TEST_EVIDENCE=... python3 scripts/run-current-python-tests.py`。
使用既有 Node24.13.0／pnpm10.28.0，沒有安裝。主機層暫時啟動 localhost listener
供探針驗證；候選 build 仍在原 deny-default OS sandbox 內執行，外部讀取、寫入、
網路均 denied，未改成不受約束的 build。

修正前 134 項紀錄獨立保留為 checkpoint；135 是修正後完整重跑結果，舊 134／30
紀錄沒有改標。local-ready.json 使用合成作者／served-preview 證據，只驗證本機
binding 邏輯，不代表真實作者核准、HTTP 預覽、GitHub checks 或 production 驗收。
原始 log 與 source.patch 的空白保留；程式碼與新說明的 diff 分開檢查。精確 source
captures 記錄各審查快照。加入證據後另做 metadata／報告審查與最終 manifest 驗證；
不據此宣稱目標分支已 merge、遠端自動化或部署已啟用。
