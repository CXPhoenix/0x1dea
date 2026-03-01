---
title: 安全？能吃嗎？
description: 我好像都懂「資訊安全」，深入後有一些新發現...
createdTime: 2026-02-27T00:47:45+08:00
thumbnail: /assets/post_course_cybersec_what-is-safety/20260227005508.png
---

![post banner](/assets/post_course_cybersec_what-is-safety/20260227005508.png)

# 什麼是安全？能吃嗎？

<div class="vp-post">
    <Badge type="tip">Cybersecurity 課程</Badge>
    ｜
    <Badge type="tip">高中課程備課</Badge>
</div>

每次開始新學期課程時，我都會煩惱：我到底要怎麼介紹「資訊安全」這個概念？

應該說，資安的「概念」大家都知道，但是要怎麼應用到「CTF」的培訓，那就開始犯難...

不過我開始在想：說不定從「安全」的原始定義來開始講會比較好🤔？

## 安全的定義

### 國語辭典中的「安全」

根據[教育部的國語辭典簡編本的說明](https://dict.concised.moe.edu.tw/dictView.jsp?ID=39720&q=1)，針對安全的定義如下：

::: tip 安全 `ㄢ ㄑㄩㄢˊ`

平安而沒有危險。 <span style="background-color: #fd3221; color: #fff; font-weight: 900; border-radius: 0.1rem; padding: 0.15rem;">例</span> 時時注意居家安全，才能保障生命財產不受損失。

:::

真的是廢話...我們當然知道「安全」就是不要危險、沒有危險嘛！

但會不會是我搞錯了？畢竟國語辭典簡編本只是「簡編」，會不會有更具體的解釋？

所以我去查了[教育部重編國語辭典修訂本](https://dict.revised.moe.edu.tw/search.jsp?md=1)對於「安全」的定義：

::: tip 重編國語辭典修訂本的「[安全](https://dict.revised.moe.edu.tw/dictView.jsp?ID=147841&q=1&word=%E5%AE%89%E5%85%A8)」

1. 平安，沒有危險。如：「安全可靠」。《舊唐書．卷六九．列傳．薛萬徹》：「賊兵多少，極於此矣。宜善自固，以圖安全。」《三遂平妖傳》第二一回：「若顧了他時，我須有分吃官司。寧可把他來壞了，我夫妻兩口兒，倒得安全。」
2. 保全。《南史．卷一〇．陳本紀．後主》：「隋文帝以陳氏子弟既多，恐京下為過，皆分置諸州縣，每歲賜以衣服以安全之。」

:::

...好吧，沒有好多少...

但我就想，會不會「安全」這個詞彙的定義其實是衍伸自「危險」呢？畢竟我們有許多詞彙的解釋都有可能參考其他詞語的解釋。

既然這樣，我們來了解一下「[危險](https://dict.revised.moe.edu.tw/dictView.jsp?ID=160729&q=1&word=%E5%8D%B1%E9%9A%AA)」的定義好了：

::: tip 危險 `ㄨㄟˊ ㄒㄧㄢˇ`

不安全。 <span style="background-color: #fd3221; color: #fff; font-weight: 900; border-radius: 0.1rem; padding: 0.15rem;">例</span> 三更半夜一個人在外面遊蕩是很危險的事。

:::

![圖 1：吐槽（AI 製作）](/assets/post_course_cybersec_what-is-safety/20260227014249.png)

好吧，我們對於「危險」的定義也是來源於「安全」...

> 順帶一提，這種「互相引用」的方法，在程式設計時會造成 error...

> [!NOTE] 「平安」的定義？
> 我猜你會問：那[平安](https://dict.concised.moe.edu.tw/dictView.jsp?ID=3357)的定義呢？我這邊列給你：
> 
> > 平穩而沒有危險。 <span style="background-color: #fd3221; color: #fff; font-weight: 900; border-radius: 0.1rem; padding: 0.15rem;">例</span> 這艘貨輪已經平安抵達高雄港。{style="font-size: calc(var(--vp-custom-root-font-size) * 0.9);"}
> 
> ...依舊是一句廢話呢...

### 英文語系中對「安全」的解釋

好吧，看起來在中文的語系中，對於「安全」的相關定義比較像是一個概念，而沒有更為精確的定義。

於是我就想：「既然『資訊安全』這個概念是從西方國家來的，那不如查查英文的定義？」說到就行動，我們來參考一下英文「Safety」的定義：

::: tip Safety

the condition of being safe from undergoing or causing hurt, injury, or loss

> 一種免於遭受或造成任何人痛苦、傷害與損失的安全無虞的境地。

&lt;from [Merriam-Webster Dictionary](https://www.merriam-webster.com/dictionary/safety)&gt;{style="text-align: right;"}

---

a state in which or a place where you are safe and not in danger or at risk

> 一個不會遭受危害，且沒有任何風險隱憂的安全狀態或場所。

&lt;from [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/safety)&gt;{style="text-align: right;"}

:::

我使用了兩個不同來源的解釋：一個是美國最權威的「韋氏辭典」、一個是劍橋辭典。

雖然解釋起來看起來還是有一種「又是一句廢話」的感覺，但是這兩個辭典把我們平常所講的那種「安全的概念」有做比較具體的說明。

例如韋氏辭典中有提到「...causing hurt, injury, or loss」，他指的就是針對面對危險時的三種不同「狀態」：主觀性的傷害、客觀性的破壞，以及存在的消失（失去）。

若是以人生安全來說，一個人的安全就是他不會遭受、也不會造成他人的「主觀感受到傷害」、「客觀、物理性、可被測量的破壞」，或是不會讓所持有的「存在（小至持有的物體，大至生命）」消失。

我知道可能有點難懂，但比起國語辭典的「平安，沒有危險」來的好多了吧...

至少你從解釋中知道，所謂「安全」就是要避免受到或是對他人造成從小到大的狀態傷害。

![圖 2：死掉就是最佳安全？（AI 製作）](/assets/post_course_cybersec_what-is-safety/20260228013411.png)

不過，劍橋辭典的解釋我覺得也非常讚！

尤其是他使用到兩個詞彙：Danger 與 Risk。

我們來看看這兩個詞彙的意思：

::: tip [Danger](https://www.merriam-webster.com/dictionary/danger)

exposure or liability to injury, pain, harm, or loss

> 曝露在傷害、痛苦、危害或損失的威脅之中，或處於極易受其波及的處境。

:::

::: tip [Risk](https://www.merriam-webster.com/dictionary/risk)

the chance of loss or the perils to the subject matter of an insurance contract
_also_ : the degree of probability of such loss

> 損失發生的機會，或特定對象所面臨的危害；同時也指該損失發生的機率程度。

:::

所以安全不只「不要危險」，還有盡可能避免「發生危險的可能性」。

所以從上面兩個詞彙你可以發現：「Safety」一詞不只是「不要危險」，還包含概念：「減少發生危險的可能性」。

![圖 3：安全是不要發生危險，但危險千千萬萬種很難預測（AI 製作）](/assets/post_course_cybersec_what-is-safety/20260228022122.png)

### 誤會了！國語辭典的「安全」其實已經告訴你了

看完英文的「具體」解釋後，先別急著吐槽教育部的修編本。

因為他其實已經把這幾個定義告訴你了！

還記得辭典中的定義嗎？

「**平穩**，沒有危險」{style="text-align: center;font-size: 1.5em;"}

沒錯，就在「平穩」這個詞上。

正如我前面說的，在中文裡面提供的是一個「大方向」的概念，你仔細拆解這個概念後就會發險：誒？好像就跟英文解釋的一樣了噎？

* 平穩 --> 不太會發生預期外的事
* 危險 --> 傷害、破壞、讓我們會失去什麼的原因

其實我們換句話說：如果把發生危險的可能性降到最低，是不是就是「安全」了呢？

![圖 4：教育部的解釋可不是廢話（AI 製作）](/assets/post_course_cybersec_what-is-safety/20260228114351.png)

在了解什麼是「安全」後，就可以開始了解「資訊安全」了嗎？

No No No！我們剛剛說到了：「把發生危險的可能性降到最低」，但是「危險」又是什麼呢？我們怎麼定義「危險」的？

## 我們如何判斷「危險」

我知道又來講「定義」很煩，但先別著急！具體定義我們前面已經講完了，接下來我們來整理一下概念，這樣就能了解什麼是「危險」。

### 從「Danger」的定義出發

回顧剛剛，你會不會覺得在 Merriam-Webster Dictionary 解釋的「Danger」是不是很「不具體」？

也許你會覺得：「很具體啦！就受傷害啊、被破壞啊、損失什麼的，別雞蛋裡挑骨頭。」那麼就大錯特錯了！

我所說的具體是指：所以怎麼樣「受傷害」？什麼東西「被破壞」？「損失」了什麼？

在 Merriam-Webster Dictionary 中都沒有定義，只告訴你：恩，不要發生這三件壞壞的事情喔！

這時候你可能會反駁：對啊！他只是解釋這個「詞」，但用在什麼情境是由我們決定的。

你說到重點了！{.text-center style="font-size:1.5em; color: var(--vp-c-red-2); padding: 2rem 0;"}

因為我們所謂的「危險」的確是「人訂的」！

### 危險＝發生壞事

在日常生活中，父母在你外出時，可能不免擔心你就說：「注意安全／Stay safe」；當你在過馬路時，會看到「通過人行穿越道注意安全」的標誌；當你在家逛網站時，你也會發現越來越多宣導「網路交友要小心，注意安全」。

如果我們把剛剛的「安全」定義拆解放到這個脈絡中，這些「注意安全」其實就是要你「遠離危險」對吧？

![圖 5：注意安全，遠離危險，所以危險是啥？](/assets/post_course_cybersec_what-is-safety/20260228130720.png)

那為什麼要遠離危險呢？那當然是因為我們不希望「壞事」發生！

壞事發生會怎樣？其實就是你無法「達成目標」對吧？

### 保持安全＝達成我們的目標

所以其實我們「保持安全」的本質，是不希望「壞事」發生；而所謂「壞事」則是會阻礙我們達成目標的事情。

所以我們想要的「注意安全」，在某種程度上也代表我們「達成目標」的驅力。

::: tip 舉個例子

父母要我們出門「注意安全」，目標是什麼？
不要被車撞？不要去不好的場所？
其實就是希望你能夠「完整的、沒有損傷的、出去回來是同一個人的回到家」而已。

所以只要所有會阻礙這個目標的事情，對於父母來說都屬於「危險」的事情。

:::

![圖 6：搞錯重點的注意安全](/assets/post_course_cybersec_what-is-safety/20260301114806.png)

我們瞭解了這點，終於可以回頭來看「資訊安全」這件事情了！

## 達成某種需要「資訊」力量的目標

所以：資訊安全（Information Security／Cybersecurity）在做什麼呢？

::: tip [Security](https://www.merriam-webster.com/dictionary/security)

the quality or state of being secure: such as
1. freedom from danger : safety
2. freedom from fear or anxiety
3. freedom from the prospect of being laid off

> 一種安全的品質或狀態，例如遠離危險（保持安全）、遠離恐懼或焦慮、遠離被解僱的未來。

:::

簡單來說：我們在「資訊」這個領域有一些目標、或是有些目標包含了「資訊」這個領域，而在這個領域中的所有事情都可以持續保持「<span style="font-size: 1.1em; color: var(--vp-c-red-2)">不會阻礙我們達成目標</span>」的狀態或品質。

但是「所有事情」這個範圍太大了，包山包海實在可怕...

所以就開始設定「資訊的安全」要「被管理」的範圍。

這邊就不得不提到鼎鼎大名的 ISO 27000 系列「資訊安全管理系統（Information Security Management System，ISMS）」。

### 資安的範圍？

認真說，資安管理中，要管的說大不大，說小完全不小。

但根據 ISO 27000 系列的定義，[資安](https://www.iso.org/obp/ui/#iso:std:iso-iec:27000:ed-5:v1:en:term:3.28)要注意的就三件事：機密性（Credentialaity）、完整性（Integriry）、可用性（Availabiltiy）。

![圖 7：Cybersecurity CIA](/assets/post_course_cybersec_what-is-safety/20260301122300.png)

但關於這三個，我就先放一旁，下次再說...總之，在這之後所有關於 CTF 的相關內容，其實我們就是在跟這三個目標鬥智鬥力（但最主要還是前兩個，可用性的挑戰在 CTF 沒有看過）。

## 不夠清楚？舉個例子

這邊我用一個 CTF 的題目來舉例：[https://buckeye-bazaar.osucyber.club/](https://buckeye-bazaar.osucyber.club/)

> [!NOTE]
>
> 這已經是我在教資安第一堂課程必用的題目了 ╮(￣▽￣"")╭

![圖 8：Buckeye Bazaar](/assets/post_course_cybersec_what-is-safety/20260301120037.png)

> 你如果用電腦板打開這個網站，會發現他的滿版讓人非常不舒服...的確，因為這是手機版的 Challenge 哈 ¯\\\_(ツ)_/¯

### 確認目標與目的

看到這個網站，你應該就知道這是一個電商的網頁。

主要就是線上購物，讓賣家可以不用以實體的方式進行與顧客進行交易。

你會說：「廢話，不然是做慈善嗎？」但這就是我們要釐清的「<span style="font-size: 2em; color: var(--vp-c-red-2); font-weight: 900">目標</span>」

::: tip 電商網站的「目標」

1. 與顧客互動
2. 增加更多的知名度
3. 賺錢

電商網站的目的是以上哪一個呢？

:::

如果你不清楚以上問題的答案，那...恩...加油 (;^_^A

當然是 <span style="font-size: 2em; font-weight: 900;">賺錢</span> 啊！～ ↖($ω$)↗

那作為我輩駭客、攻擊手、漏洞研究員...我們關注的會是什麼呢？

不讓他賺錢！！{style="font-size: 2.5em; font-weight: 900; color: var(--vp-c-red-2); text-align: center; padding: 1em 0;"}

因此，在針對這個網站進行滲透、找漏洞時，著重點就會放在如何不讓他賺錢，也就是「賠錢」上。

::: info 現實上...

當然啦，現實中我們攻擊的理由不會只是這樣..

這邊只是提供一個可以考量的角度。

現實中別真的這樣做啊！

:::

### 規劃破壞「安全目標」的方法

那在這個購物網站上，我們要讓他賠錢有哪些方法呢？

以這個挑戰來說：我們要在資源不足的情況下，購買高價的 flag 才行。

那麼要怎麼達成這個目標呢？除了「儲值餘額」外，我們怎麼樣協助這個購物網站找到破壞其「賺錢」目標的方法？

這時候就來分析：網站會如何賠錢？

::: tip 賠錢的可能

基於這個挑戰的脈絡，會賠錢的可能有這些：

1. 原本網站標價 1000，但使用者用 100 買到 --> 賠 900。
2. 使用者的餘額是 100，但是再不儲值的情況下，使用者的餘額變成 1000 --> 賠 900。
3. 使用者免費拿到物品 --> 賠標價的價格。

:::

我們了解網站如何賠錢後，當然就可以開始嘗試相對應的「方法」。

例如以第一個賠錢的可能「使用者以低於網站標價的金額買到商品」來說，我們就會開始思考：怎麼樣會讓購買商品時低於網站標價呢？

我們就會來針對網站的購物流程進行分析。（萬字分析，在此不寫，手酸了（；＿；））

分析完流程後，我們確認：在購物時，購物金額是以以下公式判斷：

$$\text{Unit Price}\times\text{Quantity}=\text{Total Amount}$$

所以我們要以「低價」買到商品的話，要怎麼辦？

用<span style="text-decoration: underline; text-underline-offset: 0.2em;">小數點</span>作為數量！{style="font-size: 2em; color: var(--vp-c-red-2); font-weight: 900; text-align: center;"}

### 嘗試執行攻擊方法

所以我們在把 flag 加入購物車後，數量變成： $0.0001$ 。

![圖 9：flag](/assets/post_course_cybersec_what-is-safety/20260301125241.png)

![圖 10：購物車](/assets/post_course_cybersec_what-is-safety/20260301125313.png)

![圖 11：改變數量為 0.0001](/assets/post_course_cybersec_what-is-safety/20260301125401.png)

![圖 12：購買成功](/assets/post_course_cybersec_what-is-safety/20260301125743.png)

購買成功！這樣就成功地抓到這個購物網站的漏洞。

## 結論？

所以：「資訊安全」是什麼？

就跟一般的「安全」一樣：保護我們能夠順利、無受傷、無破壞、無損失的達成我們的目標。

所以生活中的資訊安全包含但不限於：

1. 我在逛一個網站，但是我不希望我的身分資訊在網路上一起裸奔；
2. 我在社交媒體上貼文，但是我不希望奇怪的網友循線而來；
3. 我當酸民，但不想被抓到（這個道德問題我們到後台好好說說
4. ...

因此，學習資安的目標，不是破壞網站、不是盜取資訊，只是想「安全的活著」罷了。

![圖 13：像個瘋子一樣活著](/assets/post_course_cybersec_what-is-safety/1772342178110.gif)

---

好啦，太悲傷了 ╮(￣▽￣"")╭

總之，學習資安，保護別人，也保護自己才是王道啦！

> [!IMPORTANT] 總而言之
> 
> 當我們有能力突破系統限制時，真正關鍵的，是我們的選擇。
> 
> 所謂素養、道德，就是我們可以，但我們選擇不做！
>
> > 我們是做好駭客！{style="font-size: 1.75em; text-align: center;"}
> >
> > &lt;&lt;From Vicent55&gt;&gt;{style="text-align: right; padding-right: 4em;"}
> >
> > ![圖 13：感謝 Vincent55 支援圖片哈](/assets/post_course_cybersec_what-is-safety/20260301132349.png)