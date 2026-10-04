## Why

原 E7 以移動視線的導語代替自然正文，未符合使用者的圖表融入偏好；原評分反而要求提問開場，與技能不固定配方的原則衝突。需校正圖文規則與驗收，保留可追溯歷史。

## What Changes

- 正文直接說明圖表的機制、證據與界限；明示讀圖操作教學才使用逐步導引。
- 修正 E7 rubric，保存原輸出、原 judge 與父 QA 否決理由。
- 以新凍結版本重跑 E7 正例及新增操作教學邊界例，另起獨立 judge。
- 明確分開主 work 的 fast 啟動回報與子 worker API 的 fast 限制。

## Non-Goals

不禁止讀者對話，不要求問句開頭，不重跑其他七例，不改文章或程式，不做跨模型效果比較。

## Capabilities

### New Capabilities

無。

### Modified Capabilities

- phoenix-style-and-maintenance: 圖表自然融入正文與明示操作教學的條件。

## Impact

- Modified: skills/phoenix-writing/SKILL.md
- Modified: skills/phoenix-writing/references/style-examples.md
- Modified: skills/maintaining-writing-skills/references/writing-process.md
- Modified: maintenance/writing-skills/SOURCES.md
- Modified: maintenance/writing-skills/VALIDATION.md
- Modified: maintenance/writing-skills/behavior-eval-20261004/REPORT.md
- New: maintenance/writing-skills/behavior-eval-20261004/figure-followup/
