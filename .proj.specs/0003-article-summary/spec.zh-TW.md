---
synced_from: spec.en.md
synced_from_sha: 95641c8b0456f607cba3e4af2a0b1ebabe7fd82d
---

# 文章摘要元件

## 問題

作者需要三種可重用的文章摘要外觀，避免重複維護包裝標記或與 VitePress 內建容器衝突。三種外觀都呈現相同、由作者提供的三項重點。

## 解法

ArticleSummary 使用 PascalCase Vue 元件與原生 Markdown default slot。note 為淡色細邊便條，cards 為三個裝飾 icon 卡片（手機直排），terminal 為深色終端視窗、標題列與三行 prompt。元件不產生摘要。

## 使用者故事

1. 作者希望直接在 Markdown 使用元件，保持摘要一致。
2. 作者希望選擇 note/cards/terminal，使用三種已同意外觀。
3. 作者希望保留原生 Markdown，讓連結、強調與程式碼意義不變。
4. 讀者希望各外觀重點內容／順序相同，不因樣式改變主張。
5. 手機與鍵盤讀者希望能閱讀摘要與操作連結。
6. 列印讀者希望保留完整摘要。
7. 維護者希望內建容器與後文解析不受影響。

## 實作決策

- variant 為選用字串 note/cards/terminal；省略、空值或無效值回 note。title 為純文字，預設 TL;DR；空白回 TL;DR。
- Terminal 的純文字 title 是靜態視窗標題列。頂層三項清單每項開頭恰一個裝飾 $；換行、巢狀項目及容器後代不再加 prompt。無命令輸入、執行、可操作視窗按鈕或假互動控制。裝飾 prompt 不進入複製與可及性文字。
- 原生 slot 由作者提供內容；標準三項形式為一個頂層 unordered list。各外觀保留相同文字、連結、順序。裝飾 icon／prefix 不帶額外意義。
- 段落、list、link、emphasis、inline code、fence 及其他非標準內容不能被丟棄、裁切、重新解析或改寫。cards 裝飾頂層 takeaway list，其他區塊保持可讀流程。
- 元件 opening／closing tag 前後以空白行界定區塊；提供已驗證用法。錯誤／未閉合標籤保留 pinned compiler 原行為，不另加 recovery。
- 使用既有 theme 註冊，不新增 custom container、markdown-it 規則、v-html、任意字串 parser、ClientOnly 或依賴升級。作者 Markdown 延用本站信任邊界，沒有新增「不受信任輸入已安全化」保證。
- 保留 SSR/hydration 一致；局部樣式不改無關內容或內建容器。已接受 banner／置中／四處文字修訂另由凍結 scope 紀錄追蹤。

## 驗收

- S1：Markdown 可用三種外觀呈現相同三項重點；Terminal 有視窗框、標題列、TL;DR 或作者 title，每個直接頂層 takeaway 恰一個裝飾 $，換行／巢狀不重複、不污染複製／朗讀、不新增 active 控制；無效 variant 回 note。
- S2：每種外觀保留段落、清單、連結、粗體／斜體、inline code、fence 的內容與語意。
- S3：closing tag 不吞後文；相鄰／巢狀 info/tip/warning/details 正常，兩摘要不互吞。錯誤標籤的 output／diagnostics 與未修改 pinned compiler 一致。裝飾只到頂層清單直接項目，巢狀／容器清單保持普通結構與排版。
- S4：靜態 HTML 在 hydration 前包含摘要；初載／client navigation 沒有 hydration mismatch 或元件未解析 warning。
- S5：360px 手機全部重點可見、cards 直排，長 URL／inline code 換行，不造成頁面 overflow；fence 可在自己的區域捲動。1280px desktop 三卡一列。
- S6：淺／深色一般文字對比至少 4.5:1，link／focus 可見，裝飾不影響 accessible name／順序。摘要是以 title 命名的 note，除了作者連結不加其他 active 控制。
- S7：A4 直式、100% 縮放、關閉頁首頁尾、開啟 background graphics，列印保留全部文字、白摘要底、一般文字 ≥4.5:1 對比，不裁切；允許跨頁流動。
- S8：不新增 arbitrary string-to-HTML、parser override 或文章產生；只整合已批准文章，其他文字／資產／URL／frontmatter 維持。已接受來源 scope 明示追蹤。

## 測試決策

主要 seam 為實際 VitePress build→SSR HTML→served browser，含初載／navigation／keyboard／layout。fixture 用已安裝 alpha.16，不以其他 renderer 代替；補既有 Vue Test Utils/Vitest seam 測 fallback、title escaping、slot。使用者已核准 seam/test plan；原候選測試不等於批准證據或歷史 TDD。

## 範圍外

自動摘要、新容器／parser、全站遷移、套件升級、文章事實重寫、banner 設計、Production 發布、公開 issue／Notion 更新。

## 補充

摘要是獨立 epic，一張完整票含共享 slot 與三種 CSS 外觀；不按 registration/CSS/tests 水平拆票。若實際 scope 超出單一 context，重審拆票，不先製造依賴。官方 Vue in Markdown／Markdown 文件支持方向；線上文件 alpha.20，實際 pinned alpha.16 編譯仍須實測。
