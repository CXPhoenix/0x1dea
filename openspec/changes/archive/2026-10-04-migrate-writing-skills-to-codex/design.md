## Context

repo 初始 Git 狀態乾淨，實體名稱為 0x1DEA。新文技能已採 skills 作內容來源、.agents/skills 與 .claude/skills 作 symlink。Mac 原技能位於 custom_skills，Codex 全域入口為 symlink。原始 50 個程式與指引檔先保存於執行 workspace，私有 temp-reference 也保留可恢復備份。

## Goals / Non-Goals

目標是可辨識且可調整的作者風格、精準工作路由、完整來源與可恢復搬移。不改文章、網站程式或 CSS，不安裝工具，不 commit、push、deploy，不變更憑證或安全設定。

## Decisions

### 風格與工作流程分離

Phoenix 核心承載聲音、讀者理解與適用邊界。網站新文操作留在既有 creating-vitepress-post，維護與舊版檢查另設 maintaining-writing-skills。篇章結構依讀者與文類選擇，取消顏文字／對話／圖表數量配額。寫作專案的 CONTEXT.md 只存術語，PROJECT.md 或既有任務文件存需求與決策；相關流程放在按需參考。維護指引以實際 CLI 和可用宿主工具操作，不假設 Claude 工具名稱存在。

### 單一來源與可恢復搬移

repo skills 為有效內容來源，.agents 和 .claude 為入口。Mac 原資料夾改名保存，再將原位設為 repo symlink；原 Codex symlink 保留。舊 reference 和 scripts 子路徑提供相容入口，舊固定配方標為歷史資料，不載入一般寫作。

### 來源與模型決策

讀取使用者指定 Astra 官方正文及 @skills-mcp 兩份技能的當前 immutable version 與相關 references，保留位置與讀取日期。官方原則和本 repo 選擇分列。本次指定 GPT-6.1-sol high + fast，原因是多技能重整、風格與工作流程邊界及搬移相容；不宣稱 Astra 指南指定 sol effort，也不宣稱更改了執行模型設定。

## Implementation Contract

- 明示 Phoenix 風格才採其聲音；純程式修改、正式文件、資料格式化與一般繁中內容不因語言觸發。
- 網站新文才呼叫既有 CLI；改稿與對話草稿不建立檔案。現有文章保留 createdTime。
- 所有有效技能有 name/description，引用與 symlink 可解析，Mac 舊新入口同實體。
- 用戶明示語言、字數、幽默與格式需求覆寫風格預設。研究主張與作者立場分開，不虛構本人經驗。
- 權限拒絕即停止對該位置寫入並報告；來源不可讀即標未驗證，不捏造。
- 以結構／引用檢查、代表性適用與不適用案例、明示衝突案例及 diff 範圍驗收；不宣稱跨模型 eval。

## Risks / Trade-offs

- 全域相容 symlink 依賴 repo 不搬家；搬家時需更新 Mac 入口，備份可恢復。
- 舊 validator 保留舊格式與密度規則；其結果只用於明示舊規格工作，不能證明新風格品質。
- Spectra 供應商生成的 Claude/Gemini/GitHub 指引保留歷史，Codex 維護參考以宿主可用工具與 CLI 為準。

## Migration Plan

備份並建立清單，寫入 repo 核心與維護檔，核對來源，驗證入口，最後保留原資料夾備份並切換原位 symlink。恢復時先把新 symlink 改名保存，再將備份資料夾改回原名，Codex 入口不需重建。
