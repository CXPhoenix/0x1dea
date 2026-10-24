# Round 2：契約衝突

Reviewer：`/root/ad2_contracts`；獨立上下文、唯讀。父執行緒保存回傳結果，未更動其分級。

本輪 Contract conflict 審查未發現可成立的 P0／P1／P2 finding。此結論僅涵蓋供應的 round 2 規格與 frozen 契約，不代表新 skill、current guard 或實際互動已通過驗收。

## 輸入核對

- ROUND_INPUT：`.proj.specs/0014-article-discovery/review/versions/round-2`。
- branch＝staging；base＝HEAD＝`6fcb277a9841dfad21d91f79005d39924acd92d2`。
- 已核對 capture.json 所列 63 份副本的 SHA-256 與長度，皆相符。
- prompt SHA-256＝`3f5d674830cff8f9154503ee589378ebeb7a3ba1175953e350e70b8bebe7526d`，符合 capture。
- staged／unstaged patch 皆為空；完整 addition patch 涵蓋三份規格套件與研究文件，另有 round-1-to-round-2.patch。未因 Git diff 為空而排除未追蹤提案。
- 未讀其他 reviewer 結果；未修改檔案、執行實作測試或呼叫子 agent。

以下引用均為 frozen 副本對應的原始路徑與行號。

| 覆蓋範圍 | 對照契約與證據 | 本軸判斷 |
|---|---|---|
| 自由聊、抒發、listen-only、未知目的／受眾、直接起稿、返回與改方向 | spec.en.md:29–39,43–46；`.agents/skills/grilling/SKILL.md:6–28`；`.claude/skills/grilling/SKILL.md:6–28`；R01–R12／AC-01–05 | 新入口明示只借用原則、不載入完整工程訪談契約；原工程用途保留。因此「尚未確定驗收條件卻先寫文章」不構成互斥。 |
| 純文章、工程混合需求與新技術需求 | spec.en.md:48–60；AGENTS.md:48–69,79–89；docs/agents/workflow.md:29–101；R13–R16／AC-06–07 | 第 57 行明示新增 editorial routing exception；第 55、59 行仍將 skill／renderer／automation 交回工程流程。本 epic 自身仍屬工程工作。 |
| 新文 artifact 與既有改稿 | spec.en.md:53–54,109,128；skills/creating-vitepress-post/SKILL.md:14–23；skills/maintaining-writing-skills/references/article-maintenance.md:3–11 | 建檔使用既有 CLI，改稿保留 createdTime；對話起稿不自動建立文章檔案或取得發布權限。 |
| optional glossary、首個術語、未決定義、作者用法與比喻 | spec.en.md:79–86；.agents/skills/domain-modeling/SKILL.md:40–64；docs/agents/domain.md:3–13,43–47；R21–R28／AC-09–11 | 工程 glossary 保持原用途。文章定義依 scoped 新契約處理，未決選項留 brief；沒有將文學多義性強行交給工程 canonical-term 規則。 |
| 舊 CONTEXT／單一 GLOSSARY／兩檔／指定失效 | spec.en.md:88–93,133；skills/maintaining-writing-skills/references/writing-process.md:9–11；R29–R30／AC-12、14 | 第 93 行明示取代普遍建立 CONTEXT＋PROJECT 的舊規則；單一既有檔直接沿用，兩檔或失效指定只暫停詞彙寫入。這是明示變更，不能把舊規則本身再列為衝突。 |
| 不保存、已授權 workspace、artifact-only、scaffold override、保存失敗 | spec.en.md:45,62–68,82,129–130,164；writing-process.md:9–11；R17–R23、R40／AC-08–09 | 保存以明示請求或「已建立且已授權」workspace 為條件；不能只從一般對話推導。artifact-only 不強制建立筆記；readback 不把 tentative 升成作者確認。 |
| 預設 key／碰撞／linked path／其他位置／公開性 | spec.en.md:68,73–77,86,164–165；.gitignore:58–63；R20、R28、R45–R48／AC-08、11、17 | 固定預設 namespace、禁止連結與覆寫異專案；Git ignore 明示不等於保密或來源排除。自訂位置遇 guard 阻擋時保留筆記並報告，不重開文章訪談或擴張權限。 |
| 筆記與 current-source guard | spec.en.md:70–77,138,165；scripts/publication_current.py:227–247,279–309；docs/adr/0008-main-first-engineering-and-shared-staging.md:29–36；R38、R45–R48／AC-16–17 | 舊 guard 納入 ignored source 並比對 exact inventory；本版已明示對 live guard 新增有限 local-output 分類，先驗證形狀與 HEAD/index/trusted-inventory 碰撞，再排除允許的筆記。沒有要求「完全維持舊來源集合」與「新增筆記仍通過」同時成立。 |
| 第五 canonical 套件、語言、生成與歷史保存 | spec.en.md:111–116,135–137,163–168；docs/agents/runtime.md:32–43,140–148；docs/adr/0005-physical-product-writing-packages.md:8–26；scripts/materialize-writing-skills.py:20,99–141,255–277；R33–R38／AC-14–16 | 第五套件明示擴充四套件清單，並要求更新 policy/provenance/inventory；仍只允許三樹繁中例外，保留 aliases、framework 與歷史證據。 |
| 公開檢查、發布與 branch／ticket 權限 | spec.en.md:58,95–109,151；skills/managing-article-publication/references/local.md:42–65,91–92；references/future-actions.md:7–18；ADR-0006、0008；R16、R31–R32、R41–R44／AC-07、13 | D8 的未解項目只能完成辨識／報告，不能冒充 verified 或 publication-ready；既有 provenance、分支與 action-specific authority 明確保留。 |
| scenario proposal 與實際驗證／核准測試表 | spec.en.md:140–147；traceability.md:3,55–68；AGENTS.md:81–89；docs/agents/runtime.md:129–138；R34–R39／AC-15–17 | AD 情境家族沒有被當成已核准測試表或執行結果；兩個實際 runtime、靜態生成與 native guard 證據分開報告。歷史 design 的八案例 E1–E8 與其 inputs／rubrics 保留。 |

## 範圍限制與不確定性

- 這是未實作提案的契約審查；尚不能證明未來所有有效引用均已更新，或 fresh-host discovery、保存、兩種 current role 的 native verification 真正可行。
- capture 未含 maintenance/writing-skills/SOURCES.md、完整 Phoenix 風格參考、publication_workflows.py、main_publication_verification.py 與兩種 runtime 的全部生成檔。本輪未以目前檔案替代，結論不延伸為這些檔案的逐行稽核。
- 實作仍須把上述明示替代落入 live 指引、有限 successor 與 materializer 設定；這些是本版已有的交付義務，不另列為契約衝突。
