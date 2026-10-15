# PR #25／T-0014：目前 main 的安全審查

範圍與 Git 身分同 code-T-0014-main-refresh.md；先審完整 78 檔 committed delta，
再審最小四檔修正與包含證據的 99 檔 capture，最後覆核 README 翻譯。
所有 captured bytes／精確 mode/hash 核對一致；不沿用舊 pass 充作本輪證據。
最終未解 HIGH／MEDIUM＝0／0；未宣稱整個專案安全。

## 已確認並修復 MEDIUM：來源 blob 內容未重新綁定核准 OID

類別 data_integrity。Security reviewer 提出 confidence0.8；另一位 reviewer
獨立排除偽陽性後保留 MEDIUM、confidence0.90。新 v2 以 registry／ls-tree OID
核對來源，卻透過原 helper 的 cat-file 讀取實際 bytes，未重算 object hash。
Git 讀取成功不等於 OID 驗證；攻擊者可覆寫 loose blob，維持合法壓縮 header 與
OID 檔名，使 source／staging 同讀到未核准內容，再由 v2 納入候選。
前提是能寫入來源本機 object database，僅文章 commit 權限不足。

父 agent 的安全公開 CLI fixture 實證 registry／refs／OID 均不變、prepare exit0，
候選實際含替換文字。證據 blob-reproduction.json 與 blob-red.txt 保留。影響限於
v2 來源准入與 provenance 完整性；沒有證明 owner approval binding 繞過、sandbox
逃逸、主機 RCE 或實際發布。低層 v1 helper 缺口既存，不另算 v1 新引入漏洞。

修正位置 `scripts/article-publication-v2.py:26–37`：v2-only wrapper 在每次
cat-file blob OID 讀取後重算 `SHA-1("blob "+length+NUL+bytes)`，不符即拒絕；
baseline、staging 與所有 source 的 old.tree 皆經此 wrapper。原 v1 helper 與
assertions 未修改；offline lazy-fetch／remote transport 限制維持原樣。
`test_v2.py:82–99` 的一項回歸測試涵蓋三種角色；raw red 三個子案例均失敗，
green 全部拒絕且不產出 output。另公開 verify 的三次竄改也拒絕，refs 保留。

## 最終複查與證據限制

安全 reviewer 獨立覆核修正已封閉原路徑，未發現新增 confidence≥0.8 的
HIGH／MEDIUM。新增紀錄沒有成為候選可控政策／程式入口，逐檔 exact map 沒有
新增 blog／部署路徑或整體豁免。繁中 README 保留相同前提、影響與授權限制。

父 agent 完成135項 Python與實際隔離 build，receipt 顯示外部 read／write／network
均 denied，build digest 與 local-ready binding 相符，publishable 仍 false；
54 項網站 unit／build／lint 與各 guard 結果另列 raw evidence。合成核准／served
preview 不證明真實 HTTP 或作者驗收。舊134 checkpoint與所有歷史 bytes 保留。
Reviewer 未執行程式；本審查不涵蓋 controller 遭入侵、依賴掃描、可用性、遠端
adapter／CI／部署或 epic chain analysis。最終報告加入後的 map／native 與
commit／遠端 readback 由父 agent 另行執行；不把待完成動作寫成已落地。
