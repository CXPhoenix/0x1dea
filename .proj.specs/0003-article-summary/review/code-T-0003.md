# 獨立 Code review：Standards／Spec

基準／HEAD／merge-base：32cd6a9；tracked WIP + relevant untracked files，immutable review-packet，共39檔；committed/staged皆空。兩軸由不同 native reviewer 只讀，未由主 writer 代審。

## Standards

P1：coverage-report.md:13 的 ../../../evidence、../../../output 多退一層，證據鏈失效。修為 ../../evidence、../../output。
P2：ticket frontmatter 在 code review 仍 processing；已進入stage6–8，改為 review，沒有宣稱 done 或 landing。
未提出 code smell；略過已由 tooling 覆蓋項。

## Spec

P1：ArticleSummary.vue:56–69、80–86、212–214 的所有後代 p/ul/ol/li 樣式及terminal marker會改內嵌原生容器 layout，違反S3隔離。移除泛用terminal marker規則，相關後代 selector排除 .custom-block 後代，直接頂層裝飾仍保留；另補內外容器 list 的 computed-style對比與重驗。
其餘未見需求遺漏或未授權擴張。

本記錄保留初始發現；修正與affected recheck見後續補記。Runtime/binary被排除；review不能自行推論browser/deployment完成。

## 修正確認

Standards reviewer只讀核對corrected packet：兩項resolved、remaining0；四檔hash與manifest一致，只有證據路徑與review狀態變更。Spec reviewer確認CSS排除容器後代／移除nested marker，direct-child裝飾保留，原P1在code層resolved，無新需求錯誤。Security reviewer核對delta，保持零可利用HIGH/MEDIUM候選與原限制。

Writer重驗：affected13tests、lint通過；實際browser四組viewport/theme比較內外info容器ul/li的font/line-height/margins/display/list-style/color，完全相同；桌手機截圖重取。Corrected packet納入產品檔hash核對無drift。最終Production-mode本機build false/main通過，temporary QA頁已移除。
