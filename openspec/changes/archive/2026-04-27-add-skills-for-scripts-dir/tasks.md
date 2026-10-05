## 1. Skill canonical 內容

- [x] 1.1 建立 canonical 目錄 `skills/creating-vitepress-post/`，遵循「Decision 2：單一 SKILL.md，不切分子 skill」的決策
- [x] 1.2 撰寫 SKILL.md frontmatter，滿足「The skill frontmatter SHALL satisfy the Anthropic Agent Skill specification」：`name: creating-vitepress-post`、第三人稱「Use when…」description、letters/numbers/hyphens 命名、總長度 ≤ 1024 chars
- [x] 1.3 撰寫 Overview 與 When to Use 區段，呼應「Decision 3：Description 採中英雙語觸發詞、不寫流程摘要」決策，描述觸發條件與不適用情境
- [x] 1.4 撰寫 Quick Reference Table 列出三種呼叫方式（預設 / `-c` / `-d`），明文呈現「The skill SHALL document the -c / -d exclusivity」並引用錯誤訊息 `參數 -c 與 -d 不能同時使用。`
- [x] 1.5 撰寫 Step-by-Step 與 Generated File Layout 區段，落實「The skill SHALL describe the assets folder naming rule」，含 `root_<safe_filename>` 特例
- [x] 1.6 撰寫 Common Mistakes Table（5 條），第一條明列「手寫 markdown 繞過 helper」是違反「Agents SHALL invoke the helper script for new posts」的常見錯誤
- [x] 1.7 撰寫 Reference Implementation 區段，對照 `scripts/vpHelper.ts` 中 `parseArgs` / `getFormattedDate` / `getAssetFolderName` / `main` 的對外契約

## 2. 跨 agent 部署（Canonical + Symlink）

- [x] 2.1 在 `.claude/skills/creating-vitepress-post` 建立指向 canonical 的相對 symlink，落實「Decision 1：採 Canonical + Symlink，不採重複實體」決策
- [x] 2.2 [P] 在 `.gemini/skills/creating-vitepress-post` 建立同名相對 symlink，使 Gemini CLI 讀取相同內容
- [x] 2.3 [P] 在 `.agents/skills/creating-vitepress-post` 建立同名相對 symlink，作為 Codex 讀取入口
- [x] 2.4 驗證「The skill SHALL be reachable from Claude Code, Codex, and Gemini CLI」：執行 `ls -laL` 與 `diff` 確認三個入口路徑解析到同一份 `SKILL.md`，內容完全一致

## 3. 規範與驗證

- [x] 3.1 [P] 複檢 spec.md 全英文且使用 normative SHALL/MUST，落實「Decision 4：Spec 使用 normative SHALL，禁中文」決策
- [x] 3.2 [P] 執行 `head -n 20 skills/creating-vitepress-post/SKILL.md | wc -c`，確認 frontmatter 字數 ≤ 1024 chars
- [x] 3.3 用沙盒驗證腳本：`pnpm new:post "Skill Verification" -d /tmp/0x1dea-skill-test`，確認三行輸出（`📄`/`🖼️`/`📅`）並比對檔案結構符合「Agents SHALL invoke the helper script for new posts」契約；事後執行 `rm -rf /tmp/0x1dea-skill-test/`
- [x] 3.4 載入 `creating-vitepress-post` skill，按「Decision 5：以 Inline Self-Review 取代 RED/GREEN 子代理測試」決策進行 retrieval 驗證：問「我要寫一篇新文章該怎麼做」並確認 skill 被觸發、能引導出正確指令
- [x] 3.5 對 spec.md 全部 Scenario 逐一手動模擬：能在 SKILL.md 找到 `-c` / `-d` 互斥規則的答案，並能找到 assets 命名表（含 `root_` 特例）

## 4. 完工流程

- [x] 4.1 執行 `spectra analyze add-skills-for-scripts-dir --json` 並修復所有 Critical / Warning
- [x] 4.2 執行 `spectra validate add-skills-for-scripts-dir` 通過，準備進入 archive 流程
