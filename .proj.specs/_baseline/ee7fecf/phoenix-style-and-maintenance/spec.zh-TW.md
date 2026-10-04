---
language: zh-TW
authority: spec.en.md
synced_from: spec.en.md
synced_from_sha: bf6b088ca2d1f08294336af11100902a7d9810e9
source_path: openspec/specs/phoenix-style-and-maintenance/spec.md
source_commit: ee7fecfff72f47abc735d26ac7e9a943de04ebbf
historical_harness_review: not-recorded-under-harness
---
# phoenix-style-and-maintenance 規格稽核翻譯

> 英文原文是歷史權威；本頁是全文稽核翻譯。歷史 Harness review、TDD 與 landing 未記錄，不在此次重建。 Harness 歷史狀態為 `not recorded under harness`；`historical review not recreated`。下文保留歷史 agent symlink、Mac 全域入口與原 @trace 的既有證據；此次採用不授權重做或修改全域入口，局部取代另見 adoption 規格。

## 目的

待補：由封存變更 `migrate-writing-skills-to-codex` 建立。原規格要求封存後更新 Purpose；本次唯讀歷史匯入保留這項未完成狀態。

## 需求

### Requirement: Phoenix 風格邊界

Phoenix 技能必須在明確要求 Phoenix 聲音，或延續已採 Phoenix 風格的作品時啟用。必須將作者聲音與作品工作流程分開，保留證據與作者立場，並優先遵守明確的語言、篇幅、幽默及格式要求，而非預設值。

#### Scenario: 適合的風格要求

- **WHEN** 使用者要求以 Phoenix 風格向初學者解釋快取
- **THEN** agent 從具體讀者疑問及有界限的類比解釋機制，不強制章節或圖片配額

#### Scenario: 不適合及衝突的要求

- **WHEN** 使用者只要求程式碼修復或正式會議紀錄，未要求 Phoenix 聲音
- **THEN** 技能不強加此聲音
- **AND** 明確要求英文、無幽默、80 words 的 Phoenix 內容時，仍保留這些限制

<!-- @trace
source: migrate-writing-skills-to-codex
updated: 2026-10-04
code:
  - maintenance/writing-skills/skills-mcp-manifest.json
  - maintenance/writing-skills/SOURCES.md
  - skills/phoenix-writing/reference
  - maintenance/writing-skills/legacy/phoenix-writing/reference/templates.md
  - maintenance/writing-skills/VALIDATION.md
  - skills/maintaining-writing-skills/legacy-validator/validate_article.py
  - skills/phoenix-writing/references/tw-vocabulary.md
  - skills/maintaining-writing-skills/references/skill-maintenance.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/concept-escalation-example.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/tw-vocabulary.md
  - skills/phoenix-writing/AGENTS.md
  - skills/phoenix-writing/references/style-examples.md
  - maintenance/writing-skills/legacy/phoenix-writing/AGENTS.md.txt
  - maintenance/writing-skills/MIGRATION.md
  - skills/maintaining-writing-skills/legacy-validator/rules/__init__.py
  - maintenance/writing-skills/residual-inventory.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/kaomoji-catalog.md
  - skills/maintaining-writing-skills/legacy-validator/rules/tier1_format.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/humor-patterns.md
  - skills/phoenix-writing/scripts
  - skills/maintaining-writing-skills/legacy-validator/rules/tier3_llm_hints.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/visual-guide.md
  - skills/maintaining-writing-skills/references/article-maintenance.md
  - skills/maintaining-writing-skills/legacy-validator/config.json
  - skills/maintaining-writing-skills/legacy-validator/rules/tier2_heuristic.py
  - maintenance/writing-skills/legacy/phoenix-writing/CLAUDE.md.txt
  - AGENTS.md
  - skills/creating-vitepress-post/SKILL.md
  - skills/maintaining-writing-skills/SKILL.md
  - maintenance/writing-skills/original-manifest.json
  - .agents/skills/phoenix-writing
  - maintenance/writing-skills/legacy/phoenix-writing/SKILL.md
  - CLAUDE.md
  - skills/maintaining-writing-skills/references/writing-process.md
  - skills/phoenix-writing/SKILL.md
  - skills/maintaining-writing-skills/references/spectra-codex.md
  - .agents/skills/maintaining-writing-skills
  - skills/maintaining-writing-skills/legacy-validator/rules/_common.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/dialogue-voices.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/domain-infosec.md
  - README.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/editorial-rules.md
  - skills/maintaining-writing-skills/references/legacy-validator.md
  - maintenance/writing-skills/INVENTORY.md
  - skills/phoenix-writing/CLAUDE.md
tests:
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/k1_sparse.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier2_tier3.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_with_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_no_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e2e_full.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/w1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/o1_hint.md
  - maintenance/writing-skills/tests/samples.json
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s2_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/m1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier1.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/c1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t1_hint.md
  - maintenance/writing-skills/tests/cases.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_clean.md
-->

---
### Requirement: Canonical 來源與可復原搬移

有效技能必須位於 repo skills，且 agent 入口 symlink 能解析。Mac 原始資料在被相容 symlink 取代前，必須有可復原備份。舊 reference 與 validator 呼叫者必須保留可解析的路徑，並記載其歷史語意。

#### Scenario: Mac 與 repo 入口

- **WHEN** 搬移後 agent 開啟 repo 或既有全域 Phoenix 入口
- **THEN** 所有有效 SKILL.md 路徑都解析到 canonical repo 檔案
- **AND** 原始檔案可從通過雜湊驗證的備份復原

<!-- @trace
source: migrate-writing-skills-to-codex
updated: 2026-10-04
code:
  - maintenance/writing-skills/skills-mcp-manifest.json
  - maintenance/writing-skills/SOURCES.md
  - skills/phoenix-writing/reference
  - maintenance/writing-skills/legacy/phoenix-writing/reference/templates.md
  - maintenance/writing-skills/VALIDATION.md
  - skills/maintaining-writing-skills/legacy-validator/validate_article.py
  - skills/phoenix-writing/references/tw-vocabulary.md
  - skills/maintaining-writing-skills/references/skill-maintenance.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/concept-escalation-example.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/tw-vocabulary.md
  - skills/phoenix-writing/AGENTS.md
  - skills/phoenix-writing/references/style-examples.md
  - maintenance/writing-skills/legacy/phoenix-writing/AGENTS.md.txt
  - maintenance/writing-skills/MIGRATION.md
  - skills/maintaining-writing-skills/legacy-validator/rules/__init__.py
  - maintenance/writing-skills/residual-inventory.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/kaomoji-catalog.md
  - skills/maintaining-writing-skills/legacy-validator/rules/tier1_format.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/humor-patterns.md
  - skills/phoenix-writing/scripts
  - skills/maintaining-writing-skills/legacy-validator/rules/tier3_llm_hints.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/visual-guide.md
  - skills/maintaining-writing-skills/references/article-maintenance.md
  - skills/maintaining-writing-skills/legacy-validator/config.json
  - skills/maintaining-writing-skills/legacy-validator/rules/tier2_heuristic.py
  - maintenance/writing-skills/legacy/phoenix-writing/CLAUDE.md.txt
  - AGENTS.md
  - skills/creating-vitepress-post/SKILL.md
  - skills/maintaining-writing-skills/SKILL.md
  - maintenance/writing-skills/original-manifest.json
  - .agents/skills/phoenix-writing
  - maintenance/writing-skills/legacy/phoenix-writing/SKILL.md
  - CLAUDE.md
  - skills/maintaining-writing-skills/references/writing-process.md
  - skills/phoenix-writing/SKILL.md
  - skills/maintaining-writing-skills/references/spectra-codex.md
  - .agents/skills/maintaining-writing-skills
  - skills/maintaining-writing-skills/legacy-validator/rules/_common.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/dialogue-voices.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/domain-infosec.md
  - README.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/editorial-rules.md
  - skills/maintaining-writing-skills/references/legacy-validator.md
  - maintenance/writing-skills/INVENTORY.md
  - skills/phoenix-writing/CLAUDE.md
tests:
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/k1_sparse.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier2_tier3.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_with_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_no_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e2e_full.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/w1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/o1_hint.md
  - maintenance/writing-skills/tests/samples.json
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s2_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/m1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier1.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/c1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t1_hint.md
  - maintenance/writing-skills/tests/cases.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_clean.md
-->

---
### Requirement: 有來源依據的 Codex 維護

寫作維護指引必須使用 host 可用工具及實際 CLI 契約，保留來源脈絡，區分 OpenAI 原則與 repo 選擇，並分開記錄已執行驗證與尚未執行的模型評估。

#### Scenario: 審查搬移證據

- **WHEN** 維護者審查此次搬移
- **THEN** 證據指出 Astra 文章、quill-n-grill 與 writing-for-agents，提供必要引用並保留其限制
- **AND** GPT-6.1-sol high 加 fast 被描述為任務選擇，而不是 Astra 推薦

<!-- @trace
source: migrate-writing-skills-to-codex
updated: 2026-10-04
code:
  - maintenance/writing-skills/skills-mcp-manifest.json
  - maintenance/writing-skills/SOURCES.md
  - skills/phoenix-writing/reference
  - maintenance/writing-skills/legacy/phoenix-writing/reference/templates.md
  - maintenance/writing-skills/VALIDATION.md
  - skills/maintaining-writing-skills/legacy-validator/validate_article.py
  - skills/phoenix-writing/references/tw-vocabulary.md
  - skills/maintaining-writing-skills/references/skill-maintenance.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/concept-escalation-example.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/tw-vocabulary.md
  - skills/phoenix-writing/AGENTS.md
  - skills/phoenix-writing/references/style-examples.md
  - maintenance/writing-skills/legacy/phoenix-writing/AGENTS.md.txt
  - maintenance/writing-skills/MIGRATION.md
  - skills/maintaining-writing-skills/legacy-validator/rules/__init__.py
  - maintenance/writing-skills/residual-inventory.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/kaomoji-catalog.md
  - skills/maintaining-writing-skills/legacy-validator/rules/tier1_format.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/humor-patterns.md
  - skills/phoenix-writing/scripts
  - skills/maintaining-writing-skills/legacy-validator/rules/tier3_llm_hints.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/visual-guide.md
  - skills/maintaining-writing-skills/references/article-maintenance.md
  - skills/maintaining-writing-skills/legacy-validator/config.json
  - skills/maintaining-writing-skills/legacy-validator/rules/tier2_heuristic.py
  - maintenance/writing-skills/legacy/phoenix-writing/CLAUDE.md.txt
  - AGENTS.md
  - skills/creating-vitepress-post/SKILL.md
  - skills/maintaining-writing-skills/SKILL.md
  - maintenance/writing-skills/original-manifest.json
  - .agents/skills/phoenix-writing
  - maintenance/writing-skills/legacy/phoenix-writing/SKILL.md
  - CLAUDE.md
  - skills/maintaining-writing-skills/references/writing-process.md
  - skills/phoenix-writing/SKILL.md
  - skills/maintaining-writing-skills/references/spectra-codex.md
  - .agents/skills/maintaining-writing-skills
  - skills/maintaining-writing-skills/legacy-validator/rules/_common.py
  - maintenance/writing-skills/legacy/phoenix-writing/reference/dialogue-voices.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/domain-infosec.md
  - README.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/editorial-rules.md
  - skills/maintaining-writing-skills/references/legacy-validator.md
  - maintenance/writing-skills/INVENTORY.md
  - skills/phoenix-writing/CLAUDE.md
tests:
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/k1_sparse.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier2_tier3.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_with_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_no_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e2e_full.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/w1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/o1_hint.md
  - maintenance/writing-skills/tests/samples.json
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s2_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/m1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier1.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/c1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t1_hint.md
  - maintenance/writing-skills/tests/cases.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_clean.md
-->

---
### Requirement: 圖表正文與操作式讀圖教學邊界

Phoenix 正文必須在論述中解釋圖表的機制、證據與限制，不得以指揮讀者移動目光的命令取代論述。明確要求操作式讀圖教學時，必須允許準確的逐步引導。兩種形式都不得強制用疑問開場，也不得禁止讀者對話。

#### Scenario: 圖表融入正文

- **WHEN** 使用者要求正文解釋單一快取時間線，資料於 10:00 更新、10:05 失效
- **THEN** 正文解釋可能讀到舊資料的區間及單一快取範圍，不指揮目光移動
- **AND** 保留不確定性，不聲稱多服務協調

#### Scenario: 明確要求操作式讀圖教學

- **WHEN** 使用者明確要求用兩個步驟教如何閱讀該時間線
- **THEN** 輸出兩個準確讀圖步驟及指定圖說
- **AND** 引導服務於指定教學，不虛構圖表資料

#### Scenario: 保留失敗評估歷史

- **WHEN** 父任務 QA 因目光指揮正文及不相符的開場 rubric，拒絕較早輸出
- **THEN** 原始輸入、輸出、judgments 保持不變，另存父任務 QA 修正
- **AND** 凍結後的修訂技能只對受影響的正向及邊界案例評估，使用新的 writer 與獨立 judge

<!-- @trace
source: integrate-figures-in-prose
updated: 2026-10-04
code:
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/results.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E1/rubric.json
  - README.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/input.json
  - skills/maintaining-writing-skills/legacy-validator/rules/tier3_llm_hints.py
  - skills/maintaining-writing-skills/legacy-validator/rules/tier1_format.py
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/execution-provenance.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E6/output-v2.json
  - skills/maintaining-writing-skills/references/spectra-codex.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E4/rubric.json
  - skills/maintaining-writing-skills/legacy-validator/config.json
  - skills/maintaining-writing-skills/references/skill-maintenance.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/mechanical-checks-final.json
  - maintenance/writing-skills/legacy/phoenix-writing/AGENTS.md.txt
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/REPORT.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E8/input.json
  - skills/phoenix-writing/reference
  - maintenance/writing-skills/behavior-eval-20261004/cases/E5/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E5/input.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E7/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/check_figures.py
  - maintenance/writing-skills/behavior-eval-20261004/cases/E4/input.json
  - maintenance/writing-skills/legacy/phoenix-writing/CLAUDE.md.txt
  - maintenance/writing-skills/legacy/phoenix-writing/reference/templates.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/instruction-snapshot.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/visual-guide.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E5/rubric.json
  - skills/phoenix-writing/CLAUDE.md
  - maintenance/writing-skills/behavior-eval-20261004/REPORT.md
  - skills/phoenix-writing/scripts
  - skills/maintaining-writing-skills/legacy-validator/rules/tier2_heuristic.py
  - maintenance/writing-skills/behavior-eval-20261004/cases/E2/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E9/judgment-v21.json
  - maintenance/writing-skills/behavior-eval-20261004/instruction-snapshot.json
  - skills/phoenix-writing/AGENTS.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E6/rubric.json
  - skills/maintaining-writing-skills/SKILL.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/freeze-v22.json
  - AGENTS.md
  - maintenance/writing-skills/behavior-eval-20261004/results-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E2/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E6/input.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/output-v22.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/tw-vocabulary.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E3/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/check_mechanical.py
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/freeze.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E3/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/execution-provenance.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E8/rubric.json
  - maintenance/writing-skills/SOURCES.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E5/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/design.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/design.json
  - maintenance/writing-skills/original-manifest.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E3/input.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E8/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E9/output-v21.json
  - skills/maintaining-writing-skills/legacy-validator/rules/__init__.py
  - maintenance/writing-skills/behavior-eval-20261004/freeze.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E6/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E9/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E1/judgment-v2.json
  - skills/maintaining-writing-skills/legacy-validator/rules/_common.py
  - .agents/skills/phoenix-writing
  - skills/phoenix-writing/SKILL.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E4/output-v2.json
  - maintenance/writing-skills/skills-mcp-manifest.json
  - skills/creating-vitepress-post/SKILL.md
  - .agents/skills/maintaining-writing-skills
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E9/input.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/editorial-rules.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E2/input.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E1/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E3/judgment-v2.json
  - maintenance/writing-skills/INVENTORY.md
  - CLAUDE.md
  - skills/maintaining-writing-skills/references/legacy-validator.md
  - skills/maintaining-writing-skills/references/writing-process.md
  - skills/phoenix-writing/references/style-examples.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/output-v21.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/concept-escalation-example.md
  - maintenance/writing-skills/MIGRATION.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E2/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E7/rubric.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E7/judgment-v2.json
  - skills/maintaining-writing-skills/references/article-maintenance.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/humor-patterns.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/instruction-snapshot-v22.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E8/output-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/parent-qa-correction.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E1/input.json
  - maintenance/writing-skills/behavior-eval-20261004/REPORT.original-v2.md
  - maintenance/writing-skills/behavior-eval-20261004/mechanical-checks-v2.json
  - maintenance/writing-skills/legacy/phoenix-writing/reference/dialogue-voices.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/domain-infosec.md
  - maintenance/writing-skills/legacy/phoenix-writing/SKILL.md
  - maintenance/writing-skills/legacy/phoenix-writing/reference/kaomoji-catalog.md
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/mechanical-checks-v21.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/judgment-v21.json
  - maintenance/writing-skills/behavior-eval-20261004/figure-followup/cases/E7/judgment-v22.json
  - maintenance/writing-skills/residual-inventory.json
  - skills/phoenix-writing/references/tw-vocabulary.md
  - maintenance/writing-skills/behavior-eval-20261004/cases/E4/judgment-v2.json
  - maintenance/writing-skills/behavior-eval-20261004/cases/E7/input.json
  - maintenance/writing-skills/VALIDATION.md
  - skills/maintaining-writing-skills/legacy-validator/validate_article.py
tests:
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/c1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/k1_sparse.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier1.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_violation.md
  - maintenance/writing-skills/tests/samples.json
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/m1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e2e_full.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_with_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_violation.md
  - maintenance/writing-skills/tests/cases.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/o1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/v1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t1_hint.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t2_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/e1_no_warning.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/w1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/t3_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/p1_clean.md
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/f1_violation.md
  - skills/maintaining-writing-skills/legacy-validator/tests/test_tier2_tier3.py
  - skills/maintaining-writing-skills/legacy-validator/tests/fixtures/s2_hint.md
-->
