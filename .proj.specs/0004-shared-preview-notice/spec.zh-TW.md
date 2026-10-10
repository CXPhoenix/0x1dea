---
synced_from: spec.en.md
synced_from_sha: 781ac5ead08c97a543c38f866d2dec5055482dad
---

# 共用預覽提示

## 問題

首頁已有 env 控制的提示，基準文章的手寫 staging block 不受開關控制。各頁需管理自己的文案，正式站在支持的 Production 設定下不得出現 staging 提示。此次未找到首頁功能對應的既有本地 spec/ticket，需誠實補記錄。

## 解法

首頁行為以真實 commit/evidence 追溯；選定文章改用同一 PreviewNotice，透過 Preview／Production 建置驗證兩個 consumer。不可聲稱原實作之前已寫本次 spec。

## 使用者故事

1. 作者希望 title/text 由 Markdown 頁面管理，不必為文案改環境。
2. 維護者希望首頁／文章共用一個明確 env 開關。
3. Production 讀者希望在驗證過的正式設定下不看到 staging 文案。
4. Preview 讀者希望看到有可及性名稱的審閱提示。
5. 維護者希望 tracker 保存真實歷史、不回補虛構 gate。

## 實作決策

- 保留純文字 title/text，trim 頭尾空白、保留內部換行；空欄位省略，兩欄空則整個 note 隱藏。title 是 accessible name，只有 text 則用「預覽說明」。不解析 HTML／Markdown props。
- VITE_SITE_NOTICE_ENABLED 是唯一明確 visibility switch：精確 true 顯示；false、空字串、空白、TRUE、1、padded true 或其他提供值隱藏。缺值時 exact CF_PAGES_BRANCH=staging 顯示，其餘／缺分支隱藏；分支只是原 metadata fallback，不新增第二 switch。
- 保留 root envDir 與受追蹤的公開 example；本機 macOS .env／變體被忽略，不讀／複製秘密，不新增載入來源。
- 只把選定文章的 manual staging block 換成 shared props，保留原文／metadata／URL（已接受 banner／置中 scope 另追蹤）。不自動清除其他文章容器。
- true 對 main 也有優先權，符合原契約。Production 明確 false 並驗證實際產物；Preview 可用 true 或缺值＋staging。不新增 branch guard。
- env 是 build-time 字串，變更須重啟／重建。Preview 與 Production 都可能使用 production mode，不能用 mode 判斷部署環境。這次不改部署設定。

## 驗收

- N1：首頁與文章各自提供 title/text，enabled 時保留跳脫文字／換行、空欄位省略，兩欄空不產生 note。
- N2：flag/branch truth table 在 SSR 與 hydration 一致，true/main 是預期 override。
- N3：Preview true 或缺值/staging 兩處顯示；Production false/main、乾淨缺值/main、缺值/缺分支兩處的 HTML/DOM 都不顯示，文章後文保留。
- N4：Production release 證據記錄 resolved false 與 served artifact；缺或受汙染證據不得算通過。true/main 是有效診斷，不是支持的 Production 驗收設定。
- N5：惡意樣貌文字不產生 executable element；role=note、title／fallback accessible name。360px 全部文字可見、無 notice 造成的 horizontal overflow；淺／深色一般文字 ≥4.5:1；其他連結可 keyboard focus。SSR/DOM 的文案與 visibility 一致，初載／navigation 零 hydration mismatch warning。
- N6：公開 example 可追蹤，local .env／變體被忽略，沒有秘密、新 env 或 parser。
- N7：紀錄區分首頁 f981af2、基準文章 manual block、未落地 candidate；future gate/landing 有實際日期才記錄，追溯文件不是原本合規證明。

## 測試決策

重用既有 Vue Test Utils/Vitest 22 case flag/props seam；擴展為實際 VitePress build→SSR HTML→browser，同時測首頁／文章及乾淨 env matrix。隔離 build outputs，使用已知公開字串、不裝套件／改其他 worker output。local build 不代表 deployment 成功；既有功能不補造 retrospective red/green。

## 範圍外

全文章遷移、文章事實／publication state 修改、新 parser/API、Notion／public issue、歷史 approval 重寫、Cloudflare account/settings 與任何 push。

## 補充

一份首頁 retrospective 加一張 prospective article-sharing／matrix 驗證票；不虛構已 done 的歷史票。Notion #16 是外部索引，不是 T-0016。notice 與 summary 無技術 blocking edge。Vite 官方 env 文件供參考，root env loading 與 branch define 必須以 pinned toolchain 實測。
