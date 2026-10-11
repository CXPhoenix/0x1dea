---
title: "用電紀錄裡的正常與異常：家裡哪台設備在偷偷忙？"
description: "從半夜電鍋到未經同意的挖礦，認識用電的正常與異常，排除一般原因，再把設備、程序與網路紀錄一起帶進攻擊調查。"
createdTime: 2026-10-09T00:32:47+08:00
updatedTime: 2026-10-11T00:54:35+08:00
thumbnail: /assets/post_course_security-awareness_electricity-privacy/p-total.png
category: 資安認知推廣備課系列
draft: true
previewOnly: true
pageClass: electricity-privacy-article
---

<img src="/assets/post_course_security-awareness_electricity-privacy/article-banner.png" alt="深藍夜色中的住宅與暖色窗光，柔和波形橫越屋頂上方。" style="display: block; margin: 1.5rem auto; max-width: 100%; height: auto;" />

# 用電紀錄裡的正常與異常：家裡哪台設備在偷偷忙？

<PreviewNotice
  title="staging 修訂審閱稿"
  text="這篇供 staging 預覽與審稿，尚未發佈到正式站。"
/>

<ArticleSummary variant="note">

- 先認識平常的用電，再留意時段、持續時間與設備是否出現異常。
- 用電增加可能來自宵夜、排程或故障；挖礦等未經同意的工作也是要查的方向。
- 對照設備量測、程序、連線與帳號紀錄，才能進一步查明原因；總電表不會直接判定被駭。

</ArticleSummary>

電，是我們生活中的每一天都在用的東西。而電表，則紀錄了用電的量。

通常我們對於這種紀錄沒有什麼感覺，甚至只有「啊啊，台電又來收錢了」的想法。

但是，電的使用相關紀錄資訊，其實可以幫我們看見生活中發生了什麼事！

打個比方：有兩個家庭都用了十二度電。

但一家把較多用電集中在白天，而另一家集中在晚上。

如果我們只關心「十二度」這個總量，得到只是兩個相同的數字；但如果多一個「時間」的變項呢？那就會有很多故事可以講了！

<img src="/assets/post_course_security-awareness_electricity-privacy/p-total.png" alt="兩張圖分別寫白天與晚上用電十二度；只看總量時兩者一樣。" style="display: block; margin: 1.5rem auto; max-width: 100%; height: auto;" />

## 用電的時間變化可以透露生活細節？

看到標題先不要急著說：啊！台電偷我們的隱私資料！

想太多了孩子......(´ー`)

紀錄可能留下生活的線索，但要知道是誰、做了什麼，還得多查一點。

畢竟在這物聯網時代：這時候開始攀升用電，不一定代表你正在家中啊！也有可能只是你家的貓在反覆刷飼料...╮(╯_╰)╭

> 啊？你家沒養貓？
> 那還不趕快去養一隻！！！ヽ(#`Д´)ﾉ

不過從另一面來思考，我們也可以用這些細節，發現家裡哪裡跟平常不同，再去查：有沒有設備出了問題，甚至被安排了你沒同意的工作？

<img src="/assets/post_course_security-awareness_electricity-privacy/p-cat-event.png" alt="女人懷疑突然增加的用電代表有人在家，貓回答只是來吃宵夜。" style="display: block; margin: 1.5rem auto; max-width: 100%; height: auto;" />

## 半夜的電鍋，是壞了還是有人用？

這是我上次聽到的一個故事：

一位爸爸裝了能源管理系統（Energy Management System，EMS），某天發現半夜的電鍋用電和平常不同，先懷疑電鍋是不是壞了。

為了讓大家更了解這段變化，我讓 LLM 協助畫出@fig:simulated-ems。這裡假設電鍋接上能單獨量測功率的智慧插座，每五分鐘記錄一次；家中其他設備合計維持 150 W，電鍋以 600 W 加熱，再以 50 W 保溫後關閉。這些都是教學設定，不是故事裡那戶人家的實測資料。

::: figure simulated-ems
![模擬凌晨00:00至02:00用電，01:10至01:25電鍋加熱600瓦，接著保溫50瓦至01:35；家戶總功率是固定150瓦基載加上電鍋功率。](/assets/post_course_security-awareness_electricity-privacy/simulated-ems.svg "模擬總功率")
:::

從@fig:simulated-ems 中你會發現，這段加熱用電的狀況十分醒目，卻沒有告訴你原因：是有人煮東西？設備故障？還是定時功能啟動？

這個爸爸只能東修修、西修修，差點以為是自家的 EMS 壞掉了 இдஇ

直到有一天，爸爸在晚餐時提起這件匪夷所思的事，才知道原來是小孩半夜肚子餓，起來蒸饅頭，吃完又回去睡覺...... (´-ι_-｀) 。

<img src="/assets/post_course_security-awareness_electricity-privacy/p-midnight-event.png" alt="Fry 看著半夜電鍋加熱，分不清是設備壞了還是有人餓了。" style="display: block; margin: 1.5rem auto; max-width: 100%; height: auto;" />

這故事是有點有趣沒錯，但重點是：這樣的紀錄，你可以觀察到「異常」！

<EncoreTicket
  title="什麼是安全？能吃嗎？"
  href="/post/course/cybersec/what-is-safety"
  description="如果平常怎麼運作都還不清楚，要怎麼發現哪裡出了問題呢？"
/>

## 先知道平常，才知道哪裡怪怪的

爸爸會注意到半夜的電鍋，是因為那段用電跟平常不同。如果家裡每天都有人半夜蒸饅頭，那條曲線可能早就變成日常了......（宵夜班固定報到？）

所以要找「異常」，你得先認識自己家的「正常」。平日和假日、夏天和冬天、有人在家和出門上班，用電原本就可能不同。把它們全部混成一個平均數，再說超過平均就是可疑，冷氣大概第一個喊冤。

假設你家平常半夜只剩冰箱、路由器和幾個待機設備。有一晚，用電持續比相近條件的其他夜晚高，你可以先記下：什麼時候開始？維持多久？是不是連續好幾晚都這樣？這裡是假設的排查情境，不是我家實測的紀錄。

再回頭問家人、看看設備排程。有人煮宵夜、熱水器預約加熱、電腦正在更新，都可能補上曲線沒寫的那一段故事。

如果這些都對不上，才有理由繼續找。這時你大概會想：總電表只給我一條線，到底是哪一台在忙啊？

## 從總用電，估計個別設備

最直接的方法，是針對設備另外量測。前面的@fig:simulated-ems 就假設電鍋接上可量測功率的智慧插座，所以我們才有一條能叫做「電鍋」的線。只有家戶總功率時，不能直接把那段增加全算到電鍋頭上。

那如果沒有逐台量測呢？

有一類研究叫做非侵入式負載監測（Non-intrusive Load Monitoring，NILM），也常稱為能源分解：試著從整戶合在一起的量測，估計個別電器的用電 [[1]](#ref-1)。

::: figure nilm-process
![整戶用電經能源分解模型，得到個別設備用電估計，再與各設備單獨量測的用電比較。](/assets/post_course_security-awareness_electricity-privacy/nilm-process.svg "由整戶用電估計設備用電，再以單獨量測評估差異；依 NILMTK 的定義與評估流程重繪 [[1]](#ref-1)。")
:::

有點像聽一場合奏：所有樂器一起出聲，你還是可能認出鼓或小提琴。不過認得聲音，跟每一個音都能分對，是兩回事。電器也會同時運作、切換模式，幾種組合甚至可能產生相近的總功率。

看到一段高峰，NILM 可以幫你提出設備候選；要看它猜得如何，仍得和單獨量測的資料比較。NILMTK 把資料缺口、前處理與評估一起納入工具流程，正是因為這些條件會影響結果 [[1]](#ref-1)。

<img src="/assets/post_course_security-awareness_electricity-privacy/p-device.png" alt="Fry 看著功率上升，疑惑是否就能喊出微波爐。" style="display: block; margin: 1.5rem auto; max-width: 100%; height: auto;" />

用在剛才的排查，你可以先縮小範圍：是廚房那幾台，還是一直開著的電腦？有量測就拿量測對照；只有模型估計，就把它當作接著要查的方向。

## 如果設備真的在忙，它忙的是什麼？

先別急著把耗電的設備當成壞人。

電腦可能正在備份、跑你自己安排的工作，或處理系統更新。冷氣與冰箱則可能因為天氣、設定或故障而改變用電。找到哪台比較耗電之後，還要看它做的事，能不能跟這段變化對上。

不過，也有另一種你沒安排的「工作」：有人讓你的設備替他挖礦。

這不是只會發生在大公司的事。Radware 在 2018 年的 ADB.miner 警報裡，就記錄了手機、媒體播放器與智慧電視等 Android 裝置受影響，設備上執行的是挖 Monero 的程式。報告也提到，這些感染影響了處理器（CPU）資源與耗電 [[2]](#ref-2)。原本拿來追劇的設備，竟然被安排了一份你沒同意的兼職......(눈_눈)

挖礦讓設備持續做運算，可能增加負載與耗能。但這份事件報告沒有提供家庭電表的實測，也沒有固定的耗電增幅，不能直接換算成「你家電費會多幾成」。設備本來就在忙、受到功率限制，或額外工作只用了一點資源時，變化也可能不明顯。

真有研究試著從功率觀察攻擊嗎？有。Zhou 等人量測 33 台商用 IoT 設備的每秒功率，研究阻斷服務與偵察攻擊；量測是各台設備接智慧插座，不是拿整戶總電表找挖礦程式。研究也指出，正常影音或家電的功率波動，可能遮住較小的攻擊增量 [[3]](#ref-3)。

換到家裡，冷氣、冰箱等設備的變化還會疊在一起。一台小型 IoT 裝置多用的電，未必會在總表裡跳出一個你認得的高峰。反過來，沒有明顯增加，也不能就宣布設備安全。

## 一條電力曲線，怎麼接到攻擊調查？

假設一台平常不太忙的電腦，這幾天半夜卻持續高負載；你沒有安排備份或運算工作，單獨量測也顯示它用電增加。這時可以一起查：哪些程序在使用 CPU？什麼時候開始執行？是不是你認得、也確實安裝過的程式？

如果設備有提供紀錄，再對照網路連線、帳號登入、排程工作與設定變更。時間是否接近？連到哪裡？有沒有不認得的登入或工作？無法直接查看程序的 IoT 裝置，則要靠它提供的管理介面與路由器等設備的連線紀錄協助縮小範圍。

用電曲線指出的是「這段時間值得看看」。程序、連線與帳號紀錄，才有機會說明它到底在做什麼，以及是不是未經你同意。

若只是看見電費變高，連耗電的是哪台都還沒確認，那就先從用電與一般設備排查開始。先確認是設備正常運作還是額外的工作，才不會讓冷氣白白背鍋......(；´∀｀)

即使最後找到的是設定錯誤或硬體故障，這次觀察也沒有白做。你更知道家裡平常怎麼運作；下次出現不一樣的事件，就有紀錄可以比較。

## 這些生活紀錄，也會帶出隱私問題

你自己拿紀錄找異常，很有幫助。但如果同一份資料交到別人手上，他能猜到什麼？

前面爸爸是問了家人，才知道半夜蒸的是饅頭。設備使用和生活行為之間，還隔著確認的過程：定時功能、不同家人與寵物，都可能讓「用電增加」和「有人在家」對不上。

研究也有人直接用電表資料估計在家狀態。Liang 與 Wang 使用 ECO 資料集，將電流、電壓與相位差整理成每小時平均，再送入模型 [[4]](#ref-4)。

::: figure occupancy-process
![每小時電表資料送入模型估計在家狀態；另外取得的在家紀錄用於訓練與評估。](/assets/post_course_security-awareness_electricity-privacy/occupancy-process.svg "每小時電表資料用於估計在家狀態，另以在家紀錄訓練與核對；依 Liang 與 Wang 的方法重繪 [[4, Sec. IV]](#ref-4)。")
:::

用來核對的在家紀錄，來自住戶回報或紅外線感測器。研究前處理後使用五戶、共 449 天的資料，描述十折交叉驗證；原文未交代測試家庭是否完全不參與訓練，不能直接把結果當成對任意新家庭都適用的保證 [[4, Sec. IV]](#ref-4)。

這裡也看得出來：每小時一筆，仍可能有資訊可供模型推測。資料少一點，不等於所有生活線索都消失了。

所以我會分開問兩件事：我需要留下哪些紀錄，才能觀察家中的異常？如果要分享給能源管理服務或其他分析者，他又需要看到哪些細節？

刪掉姓名與地址，卻保留同一戶長期相連的曲線，仍可能留下時段與事件的線索。拿去分析社區尖峰，和協助某一戶排查設備，也不需要完全相同的資料。

## 先把家裡的「怪怪的」記下來

下次看到用電和平常不同，你可以先保留時段、持續時間與家裡正在運作的設備，再問問家人、檢查排程。能確認是哪台，就看它的狀態；如果出現不認得的程序、連線或登入，再把那些紀錄一起帶進調查。

爸爸問出了半夜的饅頭，我們也可能查到忘了關的設備、故障，或未經同意的運算工作。電表不會替你寫完整的答案，但多留一點你看得懂的紀錄，就多了一個發現「今天哪裡不一樣」的機會。

<small>圖源與製圖：@fig:simulated-ems 是本文教學模擬，並非住戶實測或挖礦實驗；@fig:nilm-process 是依 NILMTK 重新繪製的流程示意 [[1]](#ref-1)；@fig:occupancy-process 依 Liang 與 Wang 的方法重繪 [[4]](#ref-4)，原作採 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權。</small>

## 參考文獻

<a id="ref-1"></a>

[1] N. Batra et al., “NILMTK: An open source toolkit for non-intrusive load monitoring,” 2014, arXiv:1404.3878v1. [Online]. Available: https://arxiv.org/abs/1404.3878v1

<a id="ref-2"></a>

[2] Radware Emergency Response Team, “ADB Miner: A new botnet surfaces,” ERT Threat Alert, Feb. 6, 2018. [Online]. Available: https://www.radware.com/getattachment/Security/Threat-Advisories-and-Attack-Reports/1850/ERT-Alert-ADB-Miner_3.pdf.aspx/?lang=en-US

<a id="ref-3"></a>

[3] Y. Zhou, H. Zia, J. Qin, S. Siby, and A. M. Mandalari, “Catching hackers by watching watts: A measurement study of power-only attack detection on consumer IoT devices,” IEEE Internet of Things Journal, in press, 2026, doi: 10.1109/JIOT.2026.3702795. [Online]. Available: https://discovery.ucl.ac.uk/id/eprint/10226943/

<a id="ref-4"></a>

[4] X. Liang and H. Wang, “Hybrid transformer-RNN architecture for household occupancy detection using low-resolution smart meter data,” 2023, arXiv:2308.14114v1. [Online]. Available: https://arxiv.org/abs/2308.14114v1
