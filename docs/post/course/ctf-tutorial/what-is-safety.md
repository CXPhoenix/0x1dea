---
title: 安全？能吃嗎？
description:
createdTime: 2026-02-27T00:47:45+08:00
thumbnail: /assets/post_course_ctf-tutorial_what-is-safety/20260227005508.png
---

![post banner](/assets/post_course_ctf-tutorial_what-is-safety/20260227005508.png)

# 安全？能吃嗎？

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

![圖 1：吐槽（AI 製作）](/assets/post_course_ctf-tutorial_what-is-safety/20260227014249.png)

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

![圖 2：死掉就是最佳安全？](/assets/post_course_ctf-tutorial_what-is-safety/20260228013411.png)

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

![圖 3：安全是不要發生危險，但危險千千萬萬種](/assets/post_course_ctf-tutorial_what-is-safety/20260228022122.png)

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

但就會有下一個問題：什麼是「危險」？

### 危險還有分？當然有！

