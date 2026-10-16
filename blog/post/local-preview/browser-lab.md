---
title: "【試稿】拿到 flag 之後，你能解釋瀏覽器做了什麼嗎？"
description: "拿到 flag 之後，從瀏覽器、請求與伺服器拆開信任邊界。"
createdTime: 2026-10-09T00:32:47+08:00
thumbnail: /assets/post_local-preview_browser-lab/b-flag.png
category: staging 試稿
draft: true
previewOnly: true
sourceSha256: 1d6679c428fca6d28bbf04c62c8fa3f7eab32f31d6516ffd093755038dd3b3a8
previewVersion: concept-memes-v2
updatedTime: 2026-10-09T01:23:31+08:00
---

# 拿到 flag 之後，你能解釋瀏覽器做了什麼嗎？

::: info staging 試稿・概念梗圖 v2
這是 2026 年 10 月 9 日的試稿修訂，供 staging 預覽，尚未發佈到正式站。
:::

假設你剛解完一道網頁靶場題目。

你打開開發者工具，改了某個值，送出請求，畫面顯示成功。flag 到手，心情很好。

但如果這時有人問：「為什麼改這裡就有效？是瀏覽器相信你，還是伺服器相信你？」你答得出來嗎？

這個問題有點掃興。都過關了，還要口試喔？（先讓我開個 Network 面板……(￣▽￣;)）

![握拳慶祝拿到 flag 的小孩，接著被問還要解釋為什麼。](/assets/post_local-preview_browser-lab/b-flag.png)

圖說：拿到 flag，還要口試？這次成功尚未回答機制。（改寫 Success Kid，[1](#ref-1)）

我會想保留這場口試。因為靶場把成功做成了一個很清楚的訊號，卻沒有替我們保證：拿到訊號的人，已經理解訊號背後的機制。

## 瀏覽器裡的畫面，只是其中一層

先設想一個簡化的購物靶場：頁面上有商品價格、數量與總額。你把畫面上的總額改成一元。

這時至少有兩種可能。

一種是伺服器收到商品編號與數量後，自行查價、重新計算。畫面雖然變成一元，訂單仍按正確金額建立。

另一種是伺服器直接採用瀏覽器送來的總額。畫面修改若同時影響送出的資料，便可能改變訂單。

兩種系統在修改畫面的那一刻，看起來可以一模一樣。差別要到請求和伺服器處理才會出現。這是設想的比較，不是某個網站的漏洞紀錄。

![桌前的牌子問：前端改成一元，訂單就算一元？](/assets/post_local-preview_browser-lab/b-trust.png)

圖說：前端改成一元之後，訂單怎麼算？答案要從請求與伺服器處理找。（改寫 Change My Mind，[2](#ref-2)）

所以我比較在意的，是解題後能不能指出：**哪一份資料跨過了哪一道信任邊界？**

瀏覽器送出的資訊需要由伺服器檢查。就授權而言，OWASP 的建議是每個請求都要檢查權限，不能靠前端的限制代替。把按鈕藏起來，只能改變畫面；它沒有讓伺服器自動學會拒絕不該成立的操作。[3](#ref-3)

同一道靶場題目，可以再追問：伺服器在哪裡接受了使用者提供的資料？哪些檢查缺席，才讓這次修改生效？

## 「跨來源」也需要先說清楚

接著換一個常見疑問：瀏覽器會限制跨來源讀取，那是不是不同網站之間什麼都不能做？

先不要把「不同網站」當成精確術語。在一般 HTTP(S) 情境中，瀏覽器判斷來源（origin）會比較協定、主機與通訊埠；路徑不同不會單獨形成另一個來源。[4](#ref-4)

假設靶場的頁面位於 `https://lab.example`：

| 要比較的網址 | 與頁面同源嗎？ | 差在哪裡？ |
| --- | --- | --- |
| `https://lab.example/api/profile` | 是 | 只有路徑不同 |
| `https://lab.example:8443/api/profile` | 否 | 通訊埠不同 |
| `https://api.lab.example/profile` | 否 | 主機不同 |
| `http://lab.example/api/profile` | 否 | 協定不同 |

這些網址只用來比較規則，不是要你連線的靶場。

![Fry 疑惑：看起來同一個網站，來源真的相同嗎？](/assets/post_local-preview_browser-lab/b-origin.png)

圖說：長得像同一站，也得比較協定、主機與通訊埠。（改寫 Futurama Fry，[5](#ref-5)）

光是「同一個網域」這句話，就可能混進主機、子網域、通訊埠等不同意思。若你把表裡四種情況記成同一條規則，下一次換了網址，預測就可能出錯。

## 紅色錯誤訊息，不等於伺服器沒收到

現在設想一組教學對照：頁面向另一個來源送出一個普通、沒有額外自訂標頭的 GET 請求。目標伺服器可以記錄收到的請求，並回傳固定的測試文字。

第一輪，伺服器不提供允許該頁面來源讀取的 CORS 標頭。第二輪，只改回應中的 CORS 設定，允許這個頁面來源。其餘條件保持一致。

在第一輪，可能出現這樣的組合：伺服器日誌記錄了 GET，頁面的 JavaScript 卻拿不到回應內容；第二輪則可以讀取。符合條件、無須預檢的跨來源請求，本來就可能先送達，再由瀏覽器依 CORS 規則決定能否把回應交給程式。需要預檢的請求，流程又不同。[6](#ref-6)

這裡刻意說「設想」。實作這組對照時，還得固定瀏覽器版本、頁面來源、請求模式與伺服器設定，記錄實際結果。若連伺服器都沒啟動，看到紅字也不能直接宣布「同源政策生效了」。

有用的觀察，是把錯誤拆成不同位置：請求有沒有送出？伺服器有沒有收到？回應是否抵達？頁面的程式能不能讀？

瀏覽器主控台把錯誤畫成同一種紅色，並不表示它們都是同一種錯誤。紅色只是瀏覽器的配色，不是因果分析。

![Drake 拒絕只看主控台紅字，選擇查請求、回應與權限。](/assets/post_local-preview_browser-lab/b-response.png)

圖說：紅字沒有交代請求是否送達、回應是否可讀。（改寫 Drakeposting，[7](#ref-7)）

## 那不能讀，為什麼還可能出事？

如果一個操作會改變帳戶狀態，攻擊者有時只需要讓動作發生，不必讀到回應。CSRF 就讓我們看到這種差別：在符合漏洞條件的系統裡，使用者的瀏覽器可能被誘導送出並非使用者真正想執行的請求。[8](#ref-8)

這不代表隨便放一個表單，就能控制所有帳戶。請求如何帶入登入憑證、Cookie 的限制、伺服器是否驗證防護 token，都會影響結果。這一篇的重點，是不要把「對方讀不到回應」誤認成「對方不可能觸發動作」。

![著火房間裡的狗淡定宣稱：JavaScript 讀不到回應，帳戶操作還是發生了。](/assets/post_local-preview_browser-lab/b-action.png)

圖說：「讀不到就沒事」的反串：符合 CSRF 漏洞條件時，動作仍可能發生。（改寫 This is Fine，[9](#ref-9)）

CORS 處理跨來源資源分享的規則；帳戶能不能操作某筆資料，還需要伺服器自己的授權判斷。兩者都在談限制，限制的對象卻不一樣。

若靶場只要求你把錯誤消掉，讀者很可能帶走「加一個標頭就安全了」。若要求你說明請求、回應與權限各在哪裡被判定，才有機會看見這些差異。

## 過關之後，再改一個條件

我會替這類靶場安排一個小小的收尾：交出解法後，換一個條件，再請解題者預測結果。

原本只是換路徑，現在換通訊埠；原本伺服器接受前端總額，現在改成伺服器計價；原本用頁面程式讀回應，現在只觀察伺服器是否收到請求。

![冒汗的人面對背解法與預測結果的按鈕，問換個條件還會嗎。](/assets/post_local-preview_browser-lab/b-transfer.png)

圖說：原本的解法背熟了，換條件後能否預測？這是理解題的提案，還沒有學習成效資料。（改寫 Daily Struggle，[10](#ref-10)）

不需要每次都把題目做得更難。真正想知道的是：你能否用剛才的解釋，處理一個沒有背過答案的變化？

這是教學設計的提議，還不是經過課堂實驗證明有效的方法。若要評估它，得另外設計理解題、對照方式與評量紀錄。完成幾題本身，回答不了理解是否能轉移。

交解題紀錄時，可以補上這句：「這次成功，是因為＿＿把＿＿當成了可信的＿＿。」

如果還填不出來，就回到那筆請求：它帶了什麼，伺服器又採用了什麼。讓截圖旁邊多留一段你查得到的理由。

## 參考文獻

<a id="ref-1"></a>

[1] FHSH Memegen MCP, “Success Kid,” template success. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/success

<a id="ref-2"></a>

[2] FHSH Memegen MCP, “Change My Mind,” template cmm. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/cmm

<a id="ref-3"></a>

[3] OWASP, “Authorization Cheat Sheet,” OWASP Cheat Sheet Series. Accessed: Oct. 8, 2026. [Online]. Available: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

<a id="ref-4"></a>

[4] MDN Web Docs, “Same-origin policy.” Accessed: Oct. 8, 2026. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy

<a id="ref-5"></a>

[5] FHSH Memegen MCP, “Futurama Fry,” template fry. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/fry

<a id="ref-6"></a>

[6] MDN Web Docs, “Cross-Origin Resource Sharing (CORS).” Accessed: Oct. 8, 2026. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS

<a id="ref-7"></a>

[7] FHSH Memegen MCP, “Drakeposting,” template drake. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/drake

<a id="ref-8"></a>

[8] PortSwigger, “Cross-site request forgery (CSRF),” Web Security Academy. Accessed: Oct. 8, 2026. [Online]. Available: https://portswigger.net/web-security/csrf

<a id="ref-9"></a>

[9] FHSH Memegen MCP, “This is Fine,” template fine. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/fine

<a id="ref-10"></a>

[10] FHSH Memegen MCP, “Daily Struggle,” template ds. Accessed: Oct. 8, 2026. [Online]. Available: https://memegen.fhsh.taipei/templates/ds
