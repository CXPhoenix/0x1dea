---
title: "【試稿】電表沒拍到你，為什麼還可能透露你的生活？"
description: "用電總量相同，時間分布仍可能留下生活線索；先釐清資料與推論的界限。"
createdTime: 2026-10-09T00:32:47+08:00
thumbnail: /assets/post_local-preview_electricity-privacy/p-total.png
category: staging 試稿
draft: true
previewOnly: true
sourceSha256: eca98bc13c817b2a286f56052641b090bb1facbb6ec12737dbdd419c8ca25132
previewVersion: concept-memes-v2
updatedTime: 2026-10-09T01:23:31+08:00
---

# 電表沒拍到你，為什麼還可能透露你的生活？

::: info staging 試稿・概念梗圖 v2
這是 2026 年 10 月 9 日的試稿修訂，供 staging 預覽，尚未發佈到正式站。
:::

設想兩個家庭，一天都用了十二度電。一家把較多用電集中在白天，另一家集中在晚上。只看一天的總量，你會得到兩個相同的數字；保留時間，就能區分這兩種分布。

這裡的十二度是教學用的設定，沒有對應住戶，也不代表家庭平均用電。

![兩張圖分別寫白天與晚上用電十二度；只看總量時兩者一樣。](/assets/post_local-preview_electricity-privacy/p-total.png)

圖說：只比十二度，兩張圖一樣；保留時間，分布就不同。十二度是教學設想。（改寫 They're The Same Picture，[1](#ref-1)）

## 十二度，藏掉了什麼？

只有一天的總量，你無法讀出這一天的所有變化。若保留每一小段時間的數值，再連續記錄幾個星期，資料就會留下變化何時發生、持續多久，以及哪些變化反覆一起出現。

電表沒有長出攝影機。它只是多留了時間。

「度」通常指千瓦小時（kWh），是累積的電能。功率則是使用電能的速率，單位可以是瓦（W）。若設想一個設備維持一千瓦、一小時，累積電能就是一度。畫曲線前要先確認手上的欄位是哪一種：瞬間功率、區間平均功率，或區間累積電能。三者不能看到一串數字就當成同一回事。

![握拳的小孩以一千瓦維持一小時，算出累積一度電。](/assets/post_local-preview_electricity-privacy/p-units.png)

圖說：設想維持一千瓦、一小時，累積電能是一度；瓦與度各有自己的單位。（改寫 Success Kid，[2](#ref-2)）

功率曲線可以讓你看見變化，但它沒有自帶「現在正在煮飯」的字幕。（字幕先別急著配……(・_・;)）

## 從總用電，估計個別設備

有一類研究叫做非侵入式負載監測（Non-intrusive Load Monitoring，NILM），也常稱為能源分解。它嘗試由整戶的聚合量測，估計個別電器的用電，而不必在分析時逐台讀取專用電表。[3](#ref-3)

可以把它想成聽一段合奏，嘗試辨認有哪些樂器。這個類比只說明「混合訊號裡可能保留各部分的特徵」；電器用電不是聲音，辨識方法和可靠程度也不能從樂器類比直接搬過來。

設想總功率突然上升一段時間，之後又降回去。這可以成為某個設備啟動的候選線索。但要判斷是哪個設備，你還需要設備模型、過去的變化模式，或其他有根據的資訊。

如果同時有幾台設備運作，總和可能相近；同一台設備也可能切換模式。NILMTK 的論文便把資料缺口、前處理與評估指標當成實驗需要處理的部分。這些條件會影響你是否能比較不同方法。[3](#ref-3)

看到一個高峰，指著它說「微波爐」，你就替曲線配了旁白。那個名字可能猜對，還得拿設備模型與量測資料查證。

![Fry 看著功率上升，疑惑是否就能喊出微波爐。](/assets/post_local-preview_electricity-privacy/p-device.png)

圖說：喊出「微波爐」之後，還得查證。這個名字只是候選猜測。（改寫 Futurama Fry，[4](#ref-4)）

## 設備猜測，怎麼走到生活猜測？

即使某段訊號能支持設備使用的估計，生活行為仍多了一層推論。

例如，設想你認為某個加熱設備在晚間運作。這不會直接證明是哪個人操作，也不會證明全家當時都在家；設備可能有定時功能，家中可能有不同成員，操作原因也可能不同。

![四格銀河腦依序寫看到高峰、估計設備、推測有人在家、宣布全家都在家。](/assets/post_local-preview_electricity-privacy/p-inference.png)

圖說：最後一格故意越界：估計設備啟動，不能直接證明全家都在家。（改寫 Galaxy Brain，[5](#ref-5)）

在家狀態可以另外被建成預測問題。Liang 與 Wang 的一篇原始研究使用 ECO 資料集，把電流、電壓與相位差等量測彙整成每小時資料，並結合在家狀態標記訓練、評估模型。它提供了一個具體例子：電表資料有機會被拿來做住戶在家狀態的推論。[6](#ref-6)

這個例子支持的是「在該研究設定中可以研究這種推論」，不等於你隨手取得任一家庭的資料就能準確判斷；它也不是只靠帳單上的度數。資料包含哪些欄位、標記如何取得、訓練與測試怎麼分開，都會限制結果能說到哪裡。

而且，粗一點也不會自動變成「沒有隱私風險」。上述研究本身就使用每小時的資料做預測。彙整可能減少某些細節，是否足以阻止你在意的推論，仍要針對那個目標檢查。

我會把這裡的問題寫得比較小：**這份資料，能讓取得它的人，比原本更有根據地猜到什麼？**

不必等到能百分之百還原生活，才開始討論資料用途。猜測會出錯，也仍可能被拿去做你不希望的分類或決策。

## 把名字刪掉，還留下什麼？

再設想一份資料：姓名和地址都已刪除，每個家庭換成代碼，但保留長時間的曲線。

這個動作確實拿掉了直接識別欄位。然而代碼仍把同一戶不同時段的紀錄連在一起。若取得資料的人還能拿到其他資訊，是否可能對上某個家庭，就成了另一個需要檢查的問題。

![著火房間裡的狗說姓名地址刪掉了，同一戶的曲線還連在一起。](/assets/post_local-preview_electricity-privacy/p-link.png)

圖說：欄位刪掉了，紀錄還連在一起。這張反串圖沒有完成重新識別。（改寫 This is Fine，[7](#ref-7)）

這段是在提出風險問題，不是在宣稱我們已經完成重新識別，也不是在判定某份資料違法。把「刪除欄位」「難以連結身分」「不洩漏生活資訊」分開問，才知道自己到底驗證了哪一件事。

假如資料只是要用來估計一個社區的尖峰負載，為什麼一定要讓每位分析者取得每戶的完整長期曲線？如果只是要讓住戶找出耗電設備，是否可以讓較細的分析留在住戶端，另外提供所需的彙整結果？

這些是可討論的設計方向。保留多少細節，會影響分析功能；彙整到什麼程度，也不會有一個對所有目的都安全的答案。

## 如果只想知道社區尖峰？

前面那個社區負載問題，可以拿來逐項檢查資料需求。

要估計帳單？要找出設備耗電？要判斷是否有人在家？這幾個任務聽起來都能用電表資料，對細節的需求和對住戶的影響卻差很多。

![分析者回頭看每戶完整曲線，忽略原本只需社區尖峰的任務。](/assets/post_local-preview_electricity-privacy/p-purpose.png)

圖說：設想的任務只需社區尖峰，收集慾望卻轉向每戶完整曲線。（改寫 Distracted Boyfriend，[8](#ref-8)）

用途清楚了，才有辦法逐項討論：誰需要看到原始資料、是否要保留每戶代碼、紀錄存多久、哪些推論允許做，以及如何檢查多收的細節是否真的有幫助。

你不用因此把所有用電分析都想成監控。能源分解也能協助理解設備用電；同一種推論能力，放在住戶自己手上和放在另一個目的的系統裡，會帶來不同問題。

若提案寫「只收用電數字」，我會請它補上多久一筆、連續多久，以及誰能取得哪一層資料。

社區尖峰的問題仍在那裡：拿掉每戶代碼、改用彙整資料後，究竟哪一個必要分析會做不出來？這個答案，才有辦法說明為什麼還要多收。

## 參考文獻

<a id="ref-1"></a>

[1] FHSH Memegen MCP, “They're The Same Picture,” template same. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/same

<a id="ref-2"></a>

[2] FHSH Memegen MCP, “Success Kid,” template success. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/success

<a id="ref-3"></a>

[3] N. Batra et al., “NILMTK: An Open Source Toolkit for Non-intrusive Load Monitoring,” arXiv:1404.3878v1, 2014. [Online]. Available: https://arxiv.org/abs/1404.3878v1

<a id="ref-4"></a>

[4] FHSH Memegen MCP, “Futurama Fry,” template fry. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/fry

<a id="ref-5"></a>

[5] FHSH Memegen MCP, “Galaxy Brain,” template gb. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/gb

<a id="ref-6"></a>

[6] X. Liang and H. Wang, “Hybrid Transformer-RNN Architecture for Household Occupancy Detection Using Low-Resolution Smart Meter Data,” arXiv:2308.14114v1, 2023. [Online]. Available: https://arxiv.org/abs/2308.14114v1

<a id="ref-7"></a>

[7] FHSH Memegen MCP, “This is Fine,” template fine. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/fine

<a id="ref-8"></a>

[8] FHSH Memegen MCP, “Distracted Boyfriend,” template db. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/db
