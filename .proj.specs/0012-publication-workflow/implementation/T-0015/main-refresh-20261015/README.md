# T-0015／PR #26：目前 main 的整合與驗證

日期：2026-10-15（Asia/Taipei）。#25 已合併，實際 main 為
`b84321dfeb23e155de923e6fdf799f261e3cd1c9`；staging 仍為
`035783590895a426ee395045829ebc9d50e2b9cf`。本輪起始 #26 HEAD 為
`1f13b030eaf322a5ace4c469dfeda453844819f7`；merge-base 為
`b4e87c2453c47010cd82e6789dbb4be3cea0b28f`。使用者授權以目前 main 整理原 #26、
測試與審查後 commit、非強制 push，不授權目標 main／staging merge 或部署設定變更。

## 共同 manifest 與範圍

僅在 T-0015 topic 整合目前 main；唯一衝突為 engineering-v1.json。三方逐 key 比對，
main 282、原 topic 237，整合為 336 個精確 identities；其後新證據與報告另列逐檔 hash。
沒有整份 ours／theirs、沒有刪除 main identity 或資料夾豁免；唯一既有 main identity
更新是 T-0015 ticket 的已審 review 版本。T-0014 程式、blob 修正、測試、文件、證據
均保留。manifest-resolution.json 保存初始三方選擇；後續修正的三個 T15 hashes 另審。

原 v1、歷史 helper／assertions、M0、候選與部署檔案均未改動。#20、#21 未納入。
實際 PR 相對目前 main 只含 T-0015 工程與管理增量；T14 staged 檔案是既有 main 內容。

## 安全問題與修正

Security 與另一位獨立偽陽性審查者確認 MEDIUM 輸出 artifact 完整性問題：原 verify
只比對輸出 result.git 的 mode／blob OID；來源的 hash 檢查不能保證輸出 bytes。
攻擊者若可寫入外部 bundle，可用同 OID 檔名的 loose object 遮蔽正確 alternates；
來源、registry、receipt 不變，原 verify 仍回 ready。只有文章 commit 權限並不足。
未證明 registry digest 變更、RCE、sandbox 逃逸或實際發布。

修正沿用既有 blob checker，依獨立重算的可信完整 result 清單，驗證受驗輸出每個
blob 的 type／長度／內容 OID，再回報成功。來源檢查維持；沒有改 v1 或新增政策入口。
一項公開 CLI 回歸包含工程檔與候選兩個子案例；raw red 兩次錯誤准入，green 全部
拒絕，來源與 receipt 保留。保障限於當次驗證，後續寫入前仍須重驗。

## 最新驗證與覆蓋

| 核准列／範圍 | 證據 | 結果 | 表面與限制 |
|---|---|---|---|
| P09／AC05 | python-current.txt | 24 個 sync cases 通過 | 公開 CLI／真實暫存 Git；含 clean、no-op、conflict、候選不同段落變動、歷史及輸出竄改 |
| P10 local／AC06 | python-current.txt | pin drift 拒絕 | 不代替 T-0016 concurrency／remote writer 驗收 |
| 輸出完整性 | output-reproduction、output-red/green | 一項 genuine red→green、兩個子案例 | 來源、registry、receipt 保留；不宣稱直接發布 |
| main T14 與歷史回歸 | python-current.txt | 66 live harness＋83 live publication＋10 固定 #22＝159；failures/errors 皆 0 | 含31個v2與24個sync；原歷史 module bytes checked，使用當時code/tracker，無失敗後fallback |
| 實際隔離 build | actual-build-receipt.json、build stdout/stderr | outside read／write／network 全 denied | 繼承main的T14固定Node24.13.0實際VitePress CLI；非HTTP或作者核准 |
| 網站回歸 | unit.txt、website-build.txt、lint.txt | 54 unit、build／lint 均 exit0 | main網站來源，不是部署證據 |
| Native／structure／materializer | native-preflight.json、structure.txt、materializer.txt | 通過 | 新證據加入前preflight；最終metadata與commit後另驗證 |
| 實際 pins 的本機同步 | actual-registry、actual-prepare/verify、preservation | ready；六候選50路徑、382protectedchecks保留 | local_ready只代表CLI來源檢查，未同步遠端 |

完整命令：`PUBLICATION_TEST_DEPENDENCIES=... PUBLICATION_TEST_EVIDENCE=... python3 scripts/run-current-python-tests.py`，
使用既有、已審查的 Node24.13.0／pnpm10.28.0與node_modules，沒有安裝。父行程的
暫時localhost listener僅供探針；候選build仍受原deny-default OS sandbox約束。

## 實際同步證據的邊界

registry列出目前main／staging完整2113／2317路徑；498個差異由六候選完整ownership
及460個逐檔工程路徑涵蓋，382個固定historychecks保留。候選source pin使用staging
保留快照，不表示legacy來源已取得clean-publication provenance。registry由維護者
依核准M0與使用者實際合併的main構建，提供獨立審查；digest不會自行授權遠端操作。

修正後prepare／verify一致，result tree為
`5bf030793ba2eea97fe09457df0793c48f6bcd67`，local_ready=true／publishable=false。
actual-source-snapshots.json附來源refs／index／status／object database的前後hash摘要
及object清單，確認CLI未改寫來源。這些pins僅涵蓋已落地#25，尚未含本票#26工程；
任何main／stage／候選pin變動都必須重算，不代表nativeCI／HTTP／實際stage已同步。

舊001b26f時期的no-op／127項與本輪修正前158項紀錄分開保留，未改標為159。
探查時controller曾預期衝突，但CLI實際成功；actual-observation如實保留修正後判讀。
local-ready.json為T14合成作者／served-preview fixture，不能冒稱真實HTTP／作者核准。
原始log／source.patch空白保留。程式與新說明的diff另檢查，新增metadata另獨立審查。
T-0015維持review；尚無本票main／staging落地，不可標記done。
