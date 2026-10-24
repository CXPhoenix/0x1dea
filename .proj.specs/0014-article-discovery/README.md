# Article discovery

更新日期：2026-10-24。規格已完成第二輪、也是最後一輪四面向獨立對抗式審查。使用者已核准四張票的拆分、相依與測試計畫，正式 tickets 已建立。A／T-0026 已完成本機 TDD，狀態為 review；B～D 尚未開始。本頁不宣稱整個 epic 完成或 article-discovery skill 已可使用。

- [英文規格](spec.en.md)：凍結的實作依據。
- [繁體中文稽核版](spec.zh-TW.md)：綁定已審查英文規格的 Git blob。
- [追溯矩陣](traceability.md)：48 列需求組合，對應 17 項驗收條件。
- [審查狀態](review/STATUS.md)及[第二輪結果](review/round-2.md)：保留凍結提示與來源證據。
- [核准提案](planning/ticket-proposal/README.md)：保留核准前原文；其中「等待確認」已由[使用者核准紀錄](planning/approval.md)取代。
- [前期研究](../_discovery/article-writing-entry/research.md)：來源與設計理由；最終名詞與規則以已審查規格為準。

## 正式 tickets

| 提案 | 永久票號 | 相依 | 目前範圍 |
|---|---|---|---|
| A | [T-0026：本機筆記與 current guard](../../.proj.tickets/0014-article-discovery/T-0026-local-notes-current-guard.md) | 無 | 本機 TDD 完成，位於從 main 建立的隔離分支，狀態 review；[覆蓋報告](implementation/T-0026/coverage-report.md) |
| B | [T-0027：自由聊入口](../../.proj.tickets/0014-article-discovery/T-0027-free-conversation-entry.md) | 無 | 已建票，尚未開始 |
| C | [T-0028：按需保存與詞彙檔](../../.proj.tickets/0014-article-discovery/T-0028-optional-context-glossary.md) | T-0026、T-0027 | 已建票，尚未開始 |
| D | [T-0029：公開準備與交付路由](../../.proj.tickets/0014-article-discovery/T-0029-public-preparation-routing.md) | T-0027 | 已建票，尚未開始 |

狀態以各票 frontmatter 為準。須完成經授權的 landing，才能標為 done；建票或本機測試不等於完成此關卡。正式票中的核准測試表維持原文。

## 寫作原則

**先自由聊、按需整理。** 目的、受眾、論點與文類可以未知，也可以刻意不設定。試寫與心情抒發不必先填問卷、建立工程 spec／ticket／測試表。技能、CLI、renderer、設定或網站行為修改仍走工程流程。

PROJECT.md 的持久筆記須有保存要求或既有有效授權。GLOSSARY.md 預設需要啟用保存、至少一個已解決且需重用的術語，而且沒有現行相容詞彙檔；明確要求空白骨架仍可照辦。單一有效文章 GLOSSARY.md 或舊 CONTEXT.md 直接沿用。兩份詞彙檔權威未定時，只暫停詞彙寫入；工程 CONTEXT.md 維持工程用途。

預設本機範圍有限：`.proj.writing/<article-key>/` 只接受直接位於工作區內、未追蹤、非連結、不可執行的 PROJECT.md、GLOSSARY.md 與相容用 CONTEXT.md。先檢查整個範圍，再將合法筆記檔名自實際工程來源集合排除。非法形狀或 HEAD／index／受信任來源碰撞仍拒絕，不整個資料夾放行。一般陪聊不建立工作區。

公開準備在有要求時才啟動，記錄實際結果或待解缺口，不變成起稿問卷，也不表示發布就緒。建立文章、Phoenix 聲音與發布流程保留各自分工。
