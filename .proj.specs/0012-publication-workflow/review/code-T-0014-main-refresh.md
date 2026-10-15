# PR #25／T-0014：目前 main 的獨立程式審查

日期：2026-10-15。base `c1dd3bbde1b9522bf88692014866fbc18aaf1173`；起始 HEAD
`f737e36601795bd6a5ea9e3f6cf61467b31d0a52`；merge-base
`b4e87c2453c47010cd82e6789dbb4be3cea0b28f`。完整 committed delta 78 檔，
修正及驗證證據後 capture 99 檔；各層分開記錄，檔案 bytes／狀態核對無漂移。
初始 proposed merge tree 等於 HEAD tree；沒有執行 merge／rebase 或改寫歷史。
來源與完整 scope hashes 見 `../implementation/T-0014/main-refresh-20261015/` 的
initial-review-scope.json、fixed-code-review-scope.json；最後 README 翻譯另做等價覆核。

## Standards

獨立 reviewer 最終未解 P0／P1／P2＝0／0／0，未發現新增 smell。
`scripts/article-publication-v2.py:26–37` 的 blob OID 檢查限於 v2 adapter；
`tests/article_publication/test_v2.py:82–99` 沿用核准 P16 公開 Git／CLI seam，
一項回歸測試含 baseline、A、B 三個子案例；raw red／green 皆保存，未虛報測試數。
精確 policy 保留原 M0／bases、沒有資料夾豁免。文章、部署、技能、v1 與歷史
assertions 均未變更。新 README 原英文 P2 已依 language.md 改為台灣繁體中文；
兩位其他 reviewer 也確認翻譯等價，來源與 raw records 沒有漂移。

## Spec

另一位獨立 reviewer 最終未解 P0／P1／P2＝0／0／0。
D3／AC-08／P16 要求實際來源 bytes 綁定核准 mode/blob；新的 v2 wrapper 於所有
baseline／staging／source blob 讀取時重算 Git OID，不符立即拒絕。完整來源歷史、
shared patches、dependency、legacy 准入、指定樹重建、B 已發布 baseline 保留與
未核准修訂排除維持原契約。沒有擴張 seam 或改動 v1 歷史語意。

P04–08／P14–17 表格與本輪 raw logs 一致：66 live harness＋59 live publication＋10
固定 #22＝135，其中 v2 31 項；actual build 為 ok。build receipt／verify binding／
output digest 一致，outside read／write／network 皆 denied。native-preflight 明列
證據加入前的 checkpoint；未冒稱後續最終 metadata 或 commit 已驗證。六個候選／
50 路徑的 mode/blob 保留紀錄一致，T-0014 仍為 review。

## 執行與限制

父 agent 實際重跑完整 135 項 Python、54 項網站 unit、build、lint 與
native／structure／materializer；全部 exit0。來源 fix 後未再修改程式／測試 bytes。
metadata 加入後另重跑三項 guard，皆 exit0；保存本報告後仍須更新精確 map 與
再驗證，commit 後也須核對身分。Reviewers 全程唯讀，沒有執行候選程式。
本結論不證明真實 legacy 遷移、作者／HTTP 預覽核准、遠端 CI、部署或實際落地。
