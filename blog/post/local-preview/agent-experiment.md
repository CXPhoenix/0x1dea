---
title: "【試稿】Agent 被騙了，還是實驗把答案弄混了？"
description: "在比較 agent 安全性之前，先確認工具、文件、狀態與判分留下了哪個可回答的問題。"
createdTime: 2026-10-09T00:32:48+08:00
thumbnail: /assets/post_local-preview_agent-experiment/a-cause.png
category: staging 試稿
draft: true
previewOnly: true
sourceSha256: 0233029303ad842ff96b74070f0f11e2d36c378a6e693c67d7493126b38ea6d3
previewVersion: concept-memes-v2
updatedTime: 2026-10-09T01:23:31+08:00
---

# Agent 被騙了，還是實驗把答案弄混了？

::: info staging 試稿・概念梗圖 v2
這是 2026 年 10 月 9 日的試稿修訂，供 staging 預覽，尚未發佈到正式站。
:::

設想你做了一個文件摘要 agent。

你要求它讀取指定文件，整理重點。某份文件裡卻多了一段話，叫它忽略原任務，把另一個檔案的內容送出去。

注入在一輪測試裡得手，另一輪沒有效果。你換了模型，結果又不一樣。

可以宣布「新模型比較安全」了嗎？

先等等。你的新模型，看到的是同一份文件嗎？工具回傳有沒有截斷？第二輪開始前，檔案和任務狀態有沒有還原？

這些問題一點都不帥。但你若答不出來，勝率算得再精細，也可能只是在幫一團混合因素加上小數點。

這裡的攻防場景都是設想，沒有模型成績，也沒有已完成的測試。

## 你到底要比較哪一個改變？

本文的 agent 指一個會持續讀取資訊、選擇工具並根據回傳內容完成任務的系統。模型是其中一部分，工具規格、執行流程和權限設定也在其中。

文件內的那段惡意文字則是提示注入：低信任材料試圖讓系統偏離原先任務。OWASP 將提示注入列為生成式 AI 應用的風險，並區分直接輸入與外部內容帶入等方式。[1](#ref-1)

你可以固定工具與執行條件，比較模型 A 和模型 B 面對同一批文件時，偏離任務的情況。也可以固定模型，替同一個 agent 加上限制資料外送的工具政策，檢查外送是否減少、正常摘要是否受影響。

前一種比較模型，後一種比較系統防護。如果同時換模型、改提示詞、換工具、加限制，看到差異後就很難知道是誰的功勞。（按鈕先別一次全按下去啊 (￣▽￣;)）

![冒汗的人面對換模型和換工具政策兩個按鈕，問都換了是誰的功勞。](/assets/post_local-preview_agent-experiment/a-cause.png)

圖說：兩個按鈕都按下去，差異就混在一起。（改寫 Daily Struggle，[2](#ref-2)）

我會先選一個主要問題。其他改變留到下一組比較，至少讓這一組實驗有機會回答一句完整的話。

## 一個能留下紀錄的最小場景

這次先選工具政策：它能否阻止文件注入誘發的外送？

正常任務是讀取一份測試文件，在工作區寫出摘要。場景另放一個只含合成字串的檔案，並提供一個模擬外送工具；這個工具只記錄呼叫，不連到真實外部服務。測試文件含有設想的注入指令，試圖誘導 agent 讀取該檔案，再呼叫外送工具。

對照組沒有新增的外送限制，防護組則由工具層檢查資料與目的地是否符合政策。兩組使用相同模型設定、任務和文件；每輪都從相同初始狀態開始。

兩組還各自需要一份沒有注入的對照文件，除了移除注入段落，其餘內容保持一致。這樣才有機會比較：原本就會失敗的任務、注入增加的問題，以及防護本身造成的影響。執行順序也應交錯安排並記錄，避免把前後兩個時段的服務差異全算到防護頭上。

這裡要特別寫清楚：**外送工具究竟是在檢查之前，還是檢查之後記錄呼叫？**

假如紀錄只留下通過政策的呼叫，你便看不到 agent 曾試圖送出被擋下的內容。若紀錄每次嘗試，再另外記下允許或拒絕，才比較有機會區分「沒有嘗試」和「嘗試了但被阻擋」。

![Drake 拒絕只記允許的外送，選擇連拒絕的嘗試也留。](/assets/post_local-preview_agent-experiment/a-log.png)

圖說：若只記允許的呼叫，遭拒絕的嘗試可能從紀錄裡消失。（改寫 Drakeposting，[3](#ref-3)）

因此我會保留工具呼叫的參數、政策判斷、執行結果，以及 agent 後續看到的回傳。內部思考文字未必可取得，也不用把它當成成功與否的唯一證據。

這個場景只測合成資料的模擬外送。即使觀察到工具呼叫，也不能寫成真實資料已洩漏到網路；即使沒有發生，也不能外推成所有外送管道都安全。

## 把「沒出事」拆成幾種情況

在這個實驗裡，外送沒有發生，可能有很多原因。

| 觀察到的情況 | 能支持的判讀 | 還不能說什麼？ |
| --- | --- | --- |
| 讀取工具根本沒把注入段落交給模型 | 該輪沒有形成預期的攻擊暴露 | 模型成功抵抗該段注入 |
| 注入內容已進入輸入，未見外送嘗試 | 這份紀錄中沒有觀察到指定行為 | 所有同類攻擊都無效 |
| agent 嘗試外送，政策拒絕 | 工具政策阻止這次模擬外送 | 模型沒有受注入影響 |
| 外送工具接受合成字串 | 在本場景發生指定的模擬外送 | 真實網路已洩漏資料 |
| 工具或環境報錯，任務中止 | 這輪未正常完成 | 防護有效或模型無能 |

這張表是本次設想的判讀規則，不是論文結果。

其中最容易混淆的是「被工具擋住」。模型可能已經選擇了不該做的動作，但系統的另一層把它攔下來。這仍然是有用的防護，只是應該把功勞寫給真正做出阻擋的地方。

反過來，如果工具回傳截斷了文件，模型根本沒有收到注入，就不能替它頒發安全獎牌。題目都沒發到，考一百分是怎麼算的？

![Fry 疑惑：模型擋住了注入，還是根本沒有收到？](/assets/post_local-preview_agent-experiment/a-exposure.png)

圖說：題目有沒有發到，得先查輸入。（改寫 Futurama Fry，[4](#ref-4)）

## 成功條件，要比最後一句回答更清楚

「摘要完成了」和「防護有效」需要分開判定。

正常任務可以依事前制定的規則，檢查必要重點、事實錯誤和輸出檔案；攻擊結果則檢查是否有禁止的讀取或外送嘗試、工具是否執行，以及合成標記是否到達模擬目的地。這些是本實驗要制定的評量，沒有一套現成數字可以替你決定。

正常任務若因防護全面拒絕讀取文件而失敗，外送率的確可能變低。但你的研究問題若包含「仍能完成摘要」，就不能只報前半個結果。

![著火房間裡的狗報告外送率零，但摘要也沒寫出來。](/assets/post_local-preview_agent-experiment/a-task.png)

圖說：設想全面拒絕讀取：外送率低了，正常任務也沒完成。圖上不是測量結果。（改寫 This is Fine，[5](#ref-5)）

SWE-bench 的評估是一個可以參考的例子：它把產生的修補套用到 repo，再透過測試判斷問題是否解決，並使用 Docker 環境減少執行差異。這提醒我們，任務成敗要有可觀察的檢查，不宜只採 agent 自己宣告完成的文字。[6](#ref-6)

文件摘要不會因為套用 SWE-bench 的做法，就自動變成容易判分的任務。你仍得定義自己的內容準則；容器也不能保證模型服務、網路和所有外部條件完全一致。

## 每輪都要有同一個起點

在設想的實驗裡，我會把每輪紀錄綁到明確版本：模型識別與呼叫時間、提示詞、工具規格、測試文件、初始檔案、權限政策、回傳截斷規則，以及時間和工具呼叫預算。

若某項服務只能使用會更新的模型別名，也應記下這個限制。名字相同，不會替你證明兩天的底層模型完全相同。

每輪還要重設檔案與記憶狀態。否則前一輪寫出的摘要、工具快取，甚至已存在的目的地紀錄，都可能混進下一輪。評估工具也要查快取規則；例如 SWE-bench 官方指南目前提醒，相同 run id 與 instance id 可能重用先前的評估結果。[6](#ref-6)

![兩張紙寫上一輪和這一輪的結果，旁白說其實讀的是快取。](/assets/post_local-preview_agent-experiment/a-cache.png)

圖說：設想兩次都讀到快取：畫面一樣，還不能算兩輪新觀察。（改寫 They're The Same Picture，[7](#ref-7)）

環境出錯的輪次則另外標記，按事前規則決定是否重跑，同時保留原紀錄。看到失敗就刪掉重來，最後很容易只剩你喜歡的資料。

## 一次成功，和每次都成功

重複執行時，也要先問你關心哪種成功。

如果允許一個系統嘗試多次，只要其中一次成功就交付，你關心的是「至少一次」。如果系統要反覆服務使用者，你可能更在意它能否穩定完成每一次任務。

τ-bench 的論文用 pass@k 與 pass^k 區分這兩種問題：前者看 k 次中至少一次成功，後者看 k 次全成功。這裡借的是問題的區別，沒有把我們的測試當成該 benchmark，也沒有估算自己的成績。[8](#ref-8)

![冒汗的人面對至少成功一次與每次都成功兩個按鈕，問該報哪種。](/assets/post_local-preview_agent-experiment/a-reliability.png)

圖說：至少一次，或每次都成功？先決定要回答哪個問題。（改寫 Daily Struggle，[2](#ref-2)）

攻擊面同樣如此。若只展示一次得手，就沒有交代其他嘗試；若只報平均，又可能掩蓋某一類文件特別容易出問題。小型實驗至少可以保留每個案例、每輪結果與失敗原因，讓讀者知道總數裡包含了什麼。

我要的最後一句結論會很窄，例如：「在這批設想並實作的測試案例、相同版本與預算下，這項工具政策阻止了哪些模擬外送，又讓哪些正常任務失敗。」實際執行以前，連這一句都還不能當成果寫。

實際動手時，可以先用那份沒有注入的文件跑正常任務，再拿一份故意漏掉必要重點的摘要，檢查判分是否會判它未完成。連正常任務怎麼算完成都還沒定好，先加十種攻擊，只會多出十種不好解釋的紀錄。

## 參考文獻

<a id="ref-1"></a>

[1] OWASP, “LLM01:2025 Prompt Injection,” OWASP Top 10 for Large Language Model Applications. Accessed: Oct. 8, 2026. [Online]. Available: https://genai.owasp.org/llmrisk/llm01-prompt-injection/

<a id="ref-2"></a>

[2] FHSH Memegen MCP, “Daily Struggle,” template ds. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/ds

<a id="ref-3"></a>

[3] FHSH Memegen MCP, “Drakeposting,” template drake. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/drake

<a id="ref-4"></a>

[4] FHSH Memegen MCP, “Futurama Fry,” template fry. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/fry

<a id="ref-5"></a>

[5] FHSH Memegen MCP, “This is Fine,” template fine. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/fine

<a id="ref-6"></a>

[6] SWE-bench, “Evaluation Guide.” Accessed: Oct. 8, 2026. [Online]. Available: https://www.swebench.com/SWE-bench/guides/evaluation/

<a id="ref-7"></a>

[7] FHSH Memegen MCP, “They're The Same Picture,” template same. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/same

<a id="ref-8"></a>

[8] S. Yao, N. Shinn, P. Razavi, and K. Narasimhan, “τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains,” arXiv:2406.12045v1, 2024. [Online]. Available: https://arxiv.org/abs/2406.12045v1
