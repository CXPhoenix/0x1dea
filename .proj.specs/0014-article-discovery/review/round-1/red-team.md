# Round 1：紅隊

Reviewer：`/root/ad_redteam`；獨立上下文、唯讀。父執行緒保存以下回傳結果，未更動其分級。

Red team round 1 結果：**未確認 P0／P1／P2 finding**。本結論僅涵蓋凍結規格容許的未預期行為，不代表實作、宿主互動或使用體驗已通過。

證據範圍：base＝HEAD＝`6fcb277a9841dfad21d91f79005d39924acd92d2`，branch 為 staging；staged／unstaged patch 均為空。40 份凍結副本的 SHA-256／位元組數全部符合 capture.json；四份 addition patch 均與對應副本一致。審查全程唯讀，未執行攻擊、修改檔案或讀取其他 reviewer 結果。

以下 S 指原始路徑 `.proj.specs/0014-article-discovery/spec.en.md`，行號均來自 frozen 副本。

| 覆蓋範圍 | 具體反例與規格判讀 | 證據／AC／row |
|---|---|---|
| 自由聊、抒發、未知目的／受眾、listen-only | 「只聽我說，不要改」若被改稿、評價或要求先完成設定，直接違反條件；未知受眾也不能成為起稿門檻。 | S:35、S:37、S:39、S:44；AC-02～04；R03～08 |
| 直接起稿、反覆摘要、完整訪談 | 「先開始寫，其他未定」不能被下一輪設定問卷攔住；例行摘要也不能重設確認關卡。未找到規格授權助手以完整訪談作預設的路徑。 | S:30、S:39、S:45、S:107；AC-01、05；R02、R10～12 |
| 返回舊稿、改方向 | 「沿用舊設定，但後半改教學」只能更新受影響部分；重問既有設定或要求互斥文類會違反規格。 | S:36、S:38、S:105；AC-03；R07、R10 |
| 工程／文章分工 | 「先寫正文，再補互動元件」可繼續正文，元件另走工程流程；不能藉文章例外修改 renderer、配置或發布。這份 skill 規格本身仍明列為工程工作。 | S:52～S:60、S:90；AC-06～07、13；R13～16 |
| GLOSSARY 按需建立 | 無術語不建空表；第一個已解決且需重用的術語才觸發建立。作者自訂用法須與事實定義分開；普通比喻、多義情緒詞不能被強制定義。未決詞義只留 pending，不阻擋其他 prose。 | S:73～S:76；AC-09～11；R21～27 |
| persistence 關閉／明示 scaffold | 談話或只要文章檔案不額外建立 context。明示要 glossary／空 scaffold 是刻意允許的作者選擇，不能因此編造條目或推導發布授權。 | S:64、S:73、S:90；AC-08～09、13；R17、R23 |
| legacy CONTEXT／GLOSSARY 相容 | 單一 legacy article CONTEXT 沿用；只有 GLOSSARY 也沿用。兩者未指定權威、指定無效或目標缺失時，只暫停 glossary 寫入。工程根 CONTEXT 明確排除為 fallback。 | S:81～S:84；AC-12、14；R29～30、R33 |
| 保存授權、來源內嵌指令、路徑 | 僅有資料夾存在不等於「已建立且已授權的工作區」。文章或來源內的「改工程 CONTEXT／寫到別處」不產生權限。預設 key 限單一路徑元件，碰撞不能覆寫其他專案，linked components 須拒絕。 | S:64～S:68、S:77、S:143；AC-08、11；R18～20、R28 |
| 公開位置、readback 失敗 | 明示另存到指定且實際公開的位置，是規格保留的作者自由；Git ignore 也未被宣稱為保密保證。寫入或 readback 失敗不得回報已保存，亦不阻擋其他寫作。 | S:67～S:68；AC-08；R19～20 |
| 第五套件、驗證與歷史 | 第五個 canonical 套件與有限 current-source 調整已有界定；未容許 blanket waiver、改寫 frozen history，或用靜態產物冒充 native-host discovery。scenario families 明確未取代核准測試計畫。 | S:94～S:97、S:117～S:126；AC-15～16；R34～39 |

幾個可疑情境因既有明文限制而未列 finding：以已存在的資料夾自行推定保存權限、glossary 衝突後停止全部起稿、以文章寫作例外繞過工程票、以本次 discovery 延伸 commit／push／發布權限。這些都屬違反規格的實作，沒有找到規格同時容許它們的具體路徑。

不確定性：尚無新 skill 的實作、對話 action trace、檔案行為結果或 fresh-host 執行證據，因此無法確認實際模型是否會遵守停問、授權與相容規則。現有宿主另行載入其他 skill 的可能性，也不能僅憑此規格斷言已消除。上述限制應於核准後的測試計畫與實際執行中驗證；本輪沒有缺少阻礙靜態 Red team 審查的必要凍結證據。
