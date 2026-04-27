## Context

0x1DEA 是 VitePress 部落格，使用 `pnpm` 為套件管理器、`tsx` 執行 TypeScript 腳本。`scripts/vpHelper.ts` 透過 `package.json` 的 `new:post` 暴露給使用者，把「建立新文章」這件事的格式契約集中在腳本裡：

- **Frontmatter 契約**：`title`（title-case 自動套用）、`description`、`createdTime`（UTC+8 ISO-8601）、`thumbnail`
- **時區規則**：`getFormattedDate()` 在 `scripts/vpHelper.ts:85` 強制 UTC+8 並把 `Z` 替換為 `+08:00`
- **Assets 命名規則**：`getAssetFolderName()` 在 `scripts/vpHelper.ts:99` 把 `docs/post/<segments>/<file>` 轉換成 `docs/public/assets/<segments_joined_with_underscore>_<safe_filename>`，特例為 `root_<safe_filename>`
- **互斥旗標**：`-c <category>` 與 `-d <path>` 在 `parseArgs` 階段（`scripts/vpHelper.ts:28`）若同時提供會丟出 `參數 -c 與 -d 不能同時使用。`
- **衝突檢測**：目標檔已存在時 `main()` 在 `scripts/vpHelper.ts:182` 黃字警告並 `exit(1)`，避免覆蓋

專案同時支援三家 LLM agent — Claude Code、Codex、Gemini CLI — 各自的專案層 skill 掃描路徑分別為 `.claude/skills/`、`.agents/skills/`、`.gemini/skills/`。三個目錄此刻都已存在（`.claude/skills/` 與 `.gemini/skills/` 已含 9 個 `spectra-*` skill 重複實體；`.agents/skills/` 為空）。

利害關係人：CXPh03n1x（單人作者）希望在自動化工作流（包括 Spectra apply、各種 agent 自動產文）中，三家 agent 都能正確走 `pnpm new:post` 而非手動 `Write` markdown。

## Goals / Non-Goals

**Goals:**

- 撰寫一支符合 [Anthropic Agent Skills 規範](https://agentskills.io/specification) 的 skill `creating-vitepress-post`
- Frontmatter 嚴格符合：`name`（letters/numbers/hyphens）、`description`（第三人稱「Use when…」、不總結內部流程）、總長度 ≤ 1024 chars
- 內容覆蓋觸發條件、CLI 用法、產出結構、frontmatter 契約、assets 命名、5 條常見錯誤、reference implementation
- 同一份 skill 內容能被 Claude Code、Codex、Gemini CLI 三家 agent 讀取
- 為日後新增 `scripts/<other>.ts` 建立可複製的 skill 撰寫與部署模式

**Non-Goals:**

- 不修改 `scripts/vpHelper.ts` 行為
- 不為其他不在 `scripts/` 的功能撰寫 skill
- 不部署到使用者層級的 skill 目錄
- 不採 RED/GREEN 子代理測試

## Decisions

### Decision 1：採 Canonical + Symlink，不採重複實體

**選擇：** 在專案根新增 `skills/creating-vitepress-post/SKILL.md` 為唯一事實來源，於 `.claude/skills/`、`.gemini/skills/`、`.agents/skills/` 各建一條相對 symlink 指回 canonical。

**理由：**

- 現有 `spectra-*` skills 在 `.claude/skills/` 與 `.gemini/skills/` 各有一份實體 — 那是 Spectra CLI 自動產生的，CLI 會主動同步，不會漂移
- 此次 skill 是手寫且需保持三家 agent 一致；若用重複實體，未來修改一處忘了同步另外兩處就會漂移
- 使用者層級的 `~/.claude/skills/` 中已有 77 條 symlink 證明 Claude Code skill loader 能跟隨 symlink
- Git 預設 `core.symlinks=true` 保留 symlink，clone 後仍可用
- 命名 `skills/`（與 `scripts/` 對稱）讓「為腳本而生的 skill」語意清楚

**Alternatives considered:**

- *跟現有 spectra 風格一樣放三份實體檔* — 拒絕：手寫 skill 易漂移
- *只放在 `.claude/skills/` 一處* — 拒絕：不符合使用者「Codex / Gemini CLI 也要讀得到」的要求
- *放在 `~/.claude/skills/` 等使用者層級* — 拒絕：skill 與專案 npm script 緊耦合，跨專案無意義

### Decision 2：單一 SKILL.md，不切分子 skill

**選擇：** 一份 self-contained `SKILL.md`，無附屬檔案。

**理由：**

- `scripts/` 目前只有 **一支腳本、一個指令、兩個互斥旗標**
- `superpowers:writing-skills` 建議：內容 < 50 行的 code、< 250 行的整體可全部 inline
- 切多支 skill 會過度切割且觸發詞重疊，反而降低 Claude search optimization (CSO) 命中

**Alternatives considered:**

- *拆成 `creating-post`、`managing-post-assets`、`writing-post-frontmatter` 三支* — 拒絕：契約都源自同一支腳本，拆開反而稀釋觸發訊號

### Decision 3：Description 採中英雙語觸發詞、不寫流程摘要

**選擇：** description 明列「新增文章 / 新文章 / 寫一篇 / create post / add blog post / write article / scaffold article」等中英觸發詞，並提及 `docs/post`、`pnpm new:post`，但 **不** 描述 skill 內部流程。

**理由：**

- 專案 README、`package.json` keywords 是中英雙語
- `superpowers:writing-skills` 的 CSO 章節指出：description 若摘要流程，agent 會跟著 description 跑而不讀 skill 主體；只列觸發條件能逼 agent 載入完整內容
- 字數預估約 480 chars，對齊 frontmatter 1024 chars 上限有充裕緩衝

**Alternatives considered:**

- *純英文 description* — 拒絕：使用者主要用繁中提問，會錯失 trigger
- *列舉 step-by-step 流程到 description* — 拒絕：違反 CSO 反模式

### Decision 4：Spec 使用 normative SHALL，禁中文

**選擇：** `openspec/specs/vitepress-post-scaffolding/spec.md` 全英文撰寫，採 SHALL/MUST/WHEN-THEN-AND 格式。

**理由：**

- `superpowers:writing-skills` + Spectra 慣例：spec.md 即使 locale 為其他語言，仍需英文 normative voice
- 英文 SHALL/MUST 在 Spectra analyzer 與既有 OpenSpec 工具鏈中可被結構化解析

### Decision 5：以 Inline Self-Review 取代 RED/GREEN 子代理測試

**選擇：** Apply 階段執行 `superpowers:writing-skills` 的 Inline Self-Review 四項檢核（No Placeholders / Internal Consistency / Scope / Ambiguity），加上 live skill load 驗證取代壓力測試。

**理由：**

- 此 skill 屬 reference + technique 混合型，非 discipline-enforcing skill（如 TDD）
- `superpowers:writing-skills` 的「Testing All Skill Types」章節對 reference 類僅要求「retrieval scenarios」，可由 live load 達成
- 縮短反饋迴路、避免在工具產出階段牽動子代理成本

## Risks / Trade-offs

- **[風險] Symlink 在 Windows 或部分 CI 環境失效** → Mitigation：本專案目標環境為 macOS（`Darwin 25.2.0`），Git 預設保留 symlink；若日後跨平台再評估改重複實體並由 lint 工具同步
- **[風險] LLM 仍偏好 `Write`（rationalize 為「快」）** → Mitigation：在 SKILL.md 的 Common Mistakes 第一條與 Step-by-Step 開頭強調「frontmatter 契約只有腳本能保證」，並在 spec 中以 SHALL 條文鎖死
- **[風險] Description 描述太長壓過 skill body** → Mitigation：嚴守「Use when…」+ 觸發詞、不寫流程摘要；apply 階段用 `head -n 20 SKILL.md | wc -c` 驗證 frontmatter ≤ 1024 chars
- **[風險] 未來 `scripts/` 增加新工具時 skill 散亂** → Mitigation：本次決策建立可複製模式 — 每支腳本對應 `skills/<verb-noun>/SKILL.md` + 三個 agent 路徑下 symlink
- **[風險] Spectra CLI 在後續流程覆蓋 symlink** → Mitigation：此 skill 非 Spectra 自動產生，CLI 不會碰它；apply 流程中 symlink 步驟須在 `pnpm new:post` 驗證之前完成、之後不再動三個 skills 目錄

## Migration Plan

不適用（純新增，無既有資料）。Rollback：刪除 `skills/creating-vitepress-post/` 與三條 symlink、`openspec/specs/vitepress-post-scaffolding/`，回滾即完成。

## Open Questions

無。
