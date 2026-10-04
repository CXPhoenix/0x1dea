# 寫作技能來源與設計選擇

讀取日期：2026-10-04。這是本 repo 的維護證據，不是一般寫作必讀教材。

## 使用者指定的實際來源

| 來源 | 位置與已讀範圍 | 使用方式 |
|---|---|---|
| OpenAI／Eric Provencher，2026-09-11，Rethinking skills and prompts for GPT-6 Astra | [官方正文](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)，Better skills、Up-to-date AGENTS.md、Decision boundaries、Persistence；已讀正文，不以導航代替 | 精準 description、漸進揭露、情境式文件指標與完成邊界 |
| @skills-mcp quill-n-grill | load_skill 的 version：f977506ca51914552cec6bc715a3d027700a97c2091cb8cd58dc07574b675f45；主文及 plan、draft、revise、project-context、context-handling、explain、glossary、genres/teaching、genres/technical、genres/administrative 已讀 | 讀者／目的／文類、作者立場、證據、自然轉折、專案脈絡與本文／對話分離；選用相關原則，不整包移植 |
| @skills-mcp writing-for-agents | load_skill 的 version：be3d06401968682923a83ccfd6040797e6d37473e1f7a33e7d1ba5add7ac09ad；主文和 SKILL-MECHANICS.md 已讀 | 精準 context pointer、參考層次、單一來源、可驗收完成條件與 invocation 邊界 |
| skill-creator，Codex 本地技能 | ~/.codex/skills/.system/skill-creator/SKILL.md，已讀 | portable frontmatter、保留使用者意圖、按任務驗證與 Codex 宿主支援的設定 |

父執行緒提供的 search revision 為 67406af76bfe2b00170ae2b5724cd155cb8d5f5248876c2c2146789769380187；執行端以 load_skill 返回的 immutable version 固定 resource 讀取，完整 inventory 已取得。read_skill_resource 的原 bytes 由 base64 還原，逐檔檢查 EOF 和 SHA-256；[已讀 manifest](skills-mcp-manifest.json) 保存實際讀取版本、路徑、大小與 hash。

## 版本差異與先前失敗

先前 skills.read catalog 主文不是以上 @skills-mcp 版本：新版 quill 的分支檔是 plan/draft/revise 和 genres 子目錄，不是舊 catalog 的 writing.md／genres.md。兩份 catalog 快照保留在本機證據，供追溯；以本次直接 skills-mcp 版本複核有效設計。

先前 skills.read 附屬檔讀取失敗、Notion 下載 404 未分享，未視為權限拒絕或來源內容證明。改用父核實的已授權同一 skills-mcp 直接工具後讀取成功；第一批平行 resource 讀取部分 Internal error，依 exact version 逐項重試成功，沒有改權限／憑證或安裝工具。

## 官方原則與 repo 選擇

Astra 文章建議精準簡短的技能描述、按需讀文件、減少過度配方，以及明確的完成邊界；它提醒不同模型需要的約束可能不同，不保證其他模型的效果。

本 repo 選擇 Phoenix 只定義作者聲音，新文、維護與寫作專案流程分開。CONTEXT.md 只作術語表，需求／作者決策與待解問題另用 PROJECT.md 或既有任務文件。本地 Codex 寫入實際授權檔案並核對保存結果；沒有複製 ChatGPT 模組的「未保存、下次上傳」限制。技能維護沿用 openspec，不為此任務新建文章專案。

來源的 invocation 討論包含宿主差異；本 repo 保留可由模型發現的 description，沒有新增 disable-model-invocation 等 invocation 控制欄位，採本次 Codex skill-creator 的宿主規範並保留原本可發現的設定。是否命中依描述中的任務條件，而非一般繁中或所有 docs/post 字樣。

context-handling 的研究數字與跨文類遷移有其限制；本 repo 只採讀者需要與脈絡尺度作設計判斷，不匯入研究數字、作者身份判定、AI 偵測規避或「研究證明最佳模板」主張。正式摘要和有用回顧保留，沒有禁用結論的通則。

本次指定 GPT-6.1-sol high + fast，原因是多技能重整、風格／工作流程邊界與 Mac 搬移相容需要整體判斷。Astra 文沒有指定 sol effort 或 fast；技能不綁模型，不修改全域模型設定，也不宣稱已透過工具切換執行模型。

## 原內容追溯

Mac 原實體為 ~/.agents/custom_skills/phoenix-writing；原 Codex/Gemini 入口是 symlink。原始指引和 reference 位於 [歷史資料](legacy/phoenix-writing/SKILL.md)，validator 由維護技能保管。歷史 AGENTS／CLAUDE 保存為 .md.txt，避免成為有效指令；[公開原始 hash 子集](original-manifest.json) 記錄 43 個指引／reference／validator 的搬移前內容；完整 50 檔清單只保留於本機。

原章節的例句歸因沿用舊技能所載資料，未重新核實私有書稿；新 style-examples 明示為此次示例，不冒充作者原話。完整原檔、實際來源 bytes 與測試 log 留在本機執行 workspace migration-evidence，不作其他 contributor 的必要依賴。

## 圖文父 QA 後的最小修正（2026-10-04）

quill 當前 frozen draft 要求按段落功能及文類組織，revise 要求對照 brief／來源且保留有效段落，explain 要求機制、成立條件與限制依讀者脈絡呈現。這些原則支持圖的證據參與論述，但來源沒有直接禁止「先看圖」或規定問句開頭。

「一般圖表說明自然融入正文，不用移動視線導語；明示操作讀圖教學才逐步導引」是本專案依使用者明示偏好採用的具體選擇。風格對照加入自然融合正例及操作教學邊界，未擴成禁止讀者對話或固定問句開場。原 E7 的父 QA 否決與針對性 v2.1 重測分開保存。

v2.1 的 E7 首次重測被新 judge 判為 fail：第二人稱開頭把可能事件寫成已發生，未標示假設。依 quill revise／explain 的 uncertainty 與 source 支持原則，v2.2 在風格對照補正反例，並把圖文列入該參考的按需觸發；不改已通過的操作教學規則，只再重跑 E7。
