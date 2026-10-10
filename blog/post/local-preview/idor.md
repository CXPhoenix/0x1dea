---
title: "【試稿】IDOR：知道報修單編號，為什麼不代表你能打開它？"
description: "知道物件編號與獲得存取權限之間，還差一個伺服器授權決定。"
createdTime: 2026-10-09T00:35:53+08:00
thumbnail: /assets/post_local-preview_idor/idor-knowing-id.png
category: staging 試稿
draft: true
previewOnly: true
sourceSha256: 0f8348c4ba53a2fa387f8c9b3e3839d7b711fd9513564a94105850858aaf0e6a
previewVersion: v3
updatedTime: 2026-10-09T01:23:05+08:00
---

# IDOR：知道報修單編號，為什麼不代表你能打開它？

::: info staging 試稿・高密度修訂 v3
這是 2026 年 10 月 9 日的試稿修訂，供 staging 預覽，尚未發佈到正式站。

文中 `verification/` 檔名指作者的離線試稿 bundle。本 staging 預覽提供文中程式碼與圖片，未附完整測試 bundle。
:::

假設有一個虛構的報修系統。你登入後，點開自己的工單，網址長這樣：

```http
GET /tickets/101
```

把 `101` 改成 `102`，畫面居然出現另一位使用者的報修內容。你可能會想：問題就是編號太好猜，那改成一長串 UUID，不就好了？

先別急著換編號。我們還少問了一件事：**系統原本允不允許你看這張工單？** 如果它本來就分享給你，讀得到是正常功能；如果它是別人的私人資料，讀得到才是越權。單憑「換了 ID，回傳 200」還不能完成判斷。

IDOR（Insecure Direct Object Reference）發生在程式根據請求裡的物件參照取得資料，卻缺少適當的物件授權檢查時。參照可能是數字、UUID、檔名或其他字串；重點在伺服器有沒有確認這個使用者能否存取這個物件。[1](#ref-1)

下面用自建的報修資料，說明共享與租戶規則如何落成授權檢查，再驗證允許和拒絕的結果。所有名稱與資料都是虛構的；實驗只在本地記憶體執行。

## 登入檢查通過，還剩什麼沒檢查？

我們先把報修系統寫得很單純：使用者登入後，可以讀工單。

```python
def read_ticket_unsafe(ticket_id):
    return tickets[ticket_id]
```

假設呼叫這段程式之前，登入中介層已經確認請求來自 Alice。這能回答「是誰來的」，卻沒有回答「Alice 能不能讀 102」。`tickets[ticket_id]` 只負責找出物件，沒有判斷它與 Alice 的關係。

![比爾博先說「我知道工單編號」，接著問「為什麼不能看？」；知道參照不代表取得存取權限。](/assets/post_local-preview_idor/idor-knowing-id.png)

*知道編號，只是找得到工單。能不能看，還得問這張工單的授權規則。梗圖以 [FHSH Memegen 的 bilbo 範本](https://memegen.fhsh.taipei/templates/bilbo) 製作。*

這裡有三個不同的資訊：請求主體是 Alice、目標物件是工單 102、動作是讀取。少了其中一個，授權問題就容易問錯。例如「Alice 是客服，所以她可以用工單 API」，仍然沒有說明她能看哪個客戶、哪家公司的工單。

OWASP 在 API Security Top 10 2023 裡把這類問題列為 Broken Object Level Authorization（BOLA）：使用者可能本來就能使用這個 API，錯誤發生在特定物件的權限上。若使用者連那個管理功能都不該使用，則還涉及功能層級的授權問題。依據這個區分，可以找出應補上的檢查。[2](#ref-2)

所以，`ticket_id == current_user.id` 通常也不是答案。工單編號與使用者編號是兩種不同的東西。正確問題是工單的擁有者、租戶與共享設定，是否符合這次請求的規則。

![梗圖文字「登入成功／也不能看遍所有工單」，提醒登入只確認身分，還要檢查 Alice 是否能讀指定工單。](/assets/post_local-preview_idor/idor-login-is-not-access.png)

*登入檢查認得 Alice，工單檢查還得判斷她能不能讀 102。 [範本：波羅莫](https://memegen.fhsh.taipei/templates/mordor)*

## 先把「應該允許誰」寫出來

現在讓虛構系統稍微接近真的產品。它服務兩家公司，每家公司是一個租戶（tenant）；同一家公司內，工單可以分享給同事閱讀。

這次實驗採用以下政策：

- 使用者只能存取自己租戶的工單。
- 工單擁有者可以閱讀，也可以修改狀態。
- 被加入閱讀名單的人可以看，不能修改。
- 沒有符合上述規則，就拒絕。

這是本文為了教學選定的規則，不是所有報修系統都必須照抄的規格。若產品允許跨公司協作，就得明確設計另一套規則，不能看到不同租戶就直接認定有漏洞。

OWASP 的授權指引建議在設計時列出使用者、資源與操作，再建立權限測試；未明確授權時預設拒絕，並在每次請求檢查權限。[3](#ref-3) 這些建議在這裡可以落成一個很小的表：

| 使用者 Alice，租戶 A | 工單關係 | 讀取 | 修改狀態 |
|---|---|---|---|
| 工單 101，租戶 A | Alice 擁有 | 允許 | 允許 |
| 工單 102，租戶 A | Bob 擁有，未共享 | 拒絕 | 拒絕 |
| 工單 103，租戶 A | Bob 擁有，分享給 Alice | 允許 | 拒絕 |
| 工單 104，租戶 B | Charlie 擁有 | 拒絕 | 拒絕 |

工單 103 的共享閱讀要留下。修補越權時，如果一律只准擁有者讀取，Alice 會被擋在 Bob 的私人單外，原本合法的共享功能卻也一起壞掉了。（共享功能別一起修掉啊。(・_・<span>;</span>)）

![梗圖一方說「Bob 分享工單給我了」，另一方問「只是讓你看，對吧？」；工單 103 的分享只授予閱讀，沒有修改權限。](/assets/post_local-preview_idor/idor-shared-read-only.png)

*工單 103 讓 Alice 讀取；修改狀態仍要另外授權。 [範本：女人與貓](https://memegen.fhsh.taipei/templates/woman-cat)*

同租戶也不是通行證。它只表示 Alice 和 Bob 屬於同一家公司，沒有自動授予 Alice 閱讀 Bob 私人工單的權利。租戶邊界與物件關係需要一起成立。

## 把政策放在資料交出去之前

下面的本地範例刻意不用 Web 框架，讓授權條件露出來。`user` 代表伺服器已完成認證後取得的主體；測試直接建立它，是為了模擬可信任的認證脈絡。正式系統不能讓請求自行填入 `user.id` 或 `user.tenant`，再把它們當成已驗證的身分。

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    id: str
    tenant: str

@dataclass
class Ticket:
    tenant: str
    owner: str
    viewers: set[str]
    summary: str
    status: str = "open"

tickets = {
    "101": Ticket("A", "alice", set(), "Alice 的螢幕故障"),
    "102": Ticket("A", "bob", set(), "Bob 的私人報修"),
    "103": Ticket("A", "bob", {"alice"}, "共享的會議室報修"),
    "104": Ticket("B", "charlie", set(), "另一家公司的報修"),
}

class NotFound(Exception):
    pass

def allowed(user, ticket, action):
    if user.tenant != ticket.tenant:
        return False
    if action == "read":
        return user.id == ticket.owner or user.id in ticket.viewers
    if action == "update_status":
        return user.id == ticket.owner
    return False

def find_authorized(user, ticket_id, action):
    ticket = tickets.get(ticket_id)
    if ticket is None or not allowed(user, ticket, action):
        raise NotFound()
    return ticket

def read_ticket(user, ticket_id):
    ticket = find_authorized(user, ticket_id, "read")
    return {"summary": ticket.summary, "status": ticket.status}

def update_status(user, ticket_id, status):
    ticket = find_authorized(user, ticket_id, "update_status")
    if status not in {"open", "closed"}:
        raise ValueError("invalid status")
    ticket.status = status
```

先看 `find_authorized`：取得工單後，程式在回傳內容或修改狀態之前，確認主體、物件與動作是否符合政策。`read` 和 `update_status` 分別檢查，所以看得到共享工單，不會順便取得修改權限。

這個例子把「不存在」與「存在但無權限」都轉成 `NotFound`。接到 HTTP 時，可以把它們映射成相同的 404 回應，以減少透露私人資源存在與否。這是本文選定的回應策略；如果產品需要讓使用者清楚辨認無權限，也可能選擇 403。無論回哪個狀態碼，資料和副作用都必須真正被擋住。[1](#ref-1)

另一種常見做法，是在查詢時就縮小可查到的集合。例如只允許擁有者讀取的系統，可以用下列查詢概念：

```sql
SELECT summary, status
FROM tickets
WHERE id = ? AND tenant_id = ? AND owner_id = ?;
```

`id` 來自請求；租戶與擁有者條件則來自可信任的主體脈絡，或伺服器已驗證的租戶成員資格。這裡假設使用資料庫介面的參數綁定。它與前面的記憶體範例一樣，讓「符合權限」成為取得資料的必要條件；如果要支援共享，查詢也得涵蓋共享關係，不能只加 `owner_id` 就宣布完成。[1](#ref-1) 這段 SQL 是概念示範，沒有接上資料庫執行。

兩種實作都能成立。該選哪種，取決於資料層、權限複雜度與團隊如何避免漏掉檢查。我會優先讓業務程式透過統一的授權介面取用資料，並用測試確認每個入口都有走到它。只有函式名稱叫 `authorized`，還不足以當證據。

## 測試時，不必靠運氣猜中 ID

在自己管理或已獲授權的測試環境裡，準備 Alice 和 Bob 兩個帳號，各自建立資料，再拿 Bob 已知的工單編號測 Alice。這樣測的是授權，不是編號猜測能力。OWASP WSTG 的 IDOR 測試章節也建議以不同使用者及其物件，確認不應允許的存取是否被擋住。[4](#ref-4)

![兩個按鈕分別標成「兩個帳號，權限先寫好」與「亂猜千個 ID，撞運氣」，按按鈕者標成「在測授權的我」；比較已知測試物件的權限驗證與沒有政策的猜測。](/assets/post_local-preview_idor/idor-test-known-objects.png)

*用 Bob 已知的私人單測 Alice，預期拒絕；用共享單測她，預期允許閱讀。 [範本：兩個按鈕](https://memegen.fhsh.taipei/templates/ds)*

本文的本地腳本刻意包含兩個版本：沒做物件檢查的函式會讓 Alice 讀到 102；修補版則拒絕。其他測試還會確認：

- Alice 仍能讀取與修改自己的 101。
- Alice 可以讀共享的 103，但不能改它的狀態。
- Charlie 可以讀租戶 B 的 104，Alice 不行。
- 撤銷 Alice 對 103 的閱讀分享後，她下一次讀取會被拒絕。
- 修改被拒絕時，工單狀態確實維持原值。

別忘了檢查工單狀態。若程式先改資料，再發現無權限而回傳錯誤，使用者看到失敗，資料卻已經變了。

![梗圖並列「畫面：修改失敗」與「資料：已經改好了」，反串先更新資料才拒絕請求的錯誤實作；拒絕測試也要檢查資料狀態。](/assets/post_local-preview_idor/idor-denied-side-effect.png)

*拒絕修改的測試，還要確認工單狀態沒有變。 [範本：災難女孩](https://memegen.fhsh.taipei/templates/disastergirl)*

範例檔 `verification/idor_demo.py` 使用 Python 標準函式庫，可在專案根目錄執行：

```sh
python3 verification/idor_demo.py
```

預期會看到未修補版的越權讀取被重現，接著每一項修補版測試顯示 `PASS`。這驗證的是小型政策函式的行為，沒有測 HTTP 路由、登入中介層或資料庫；不能把這份紀錄當成正式服務已完成安全驗收。

當系統變大，還要沿著同一份資料的不同出口找：詳情 API 有檢查，匯出 CSV 的 API 呢？工單附件是不是直接由儲存服務回傳？批次修改能不能混進另一個人的工單？若路由長成 `/projects/{project_id}/tickets/{ticket_id}`，也要驗證兩者的從屬關係，不能只檢查網址裡那個專案。

這些是從本文政策延伸的檢查方向；每個系統應依實際資料流補齊，而不是以這幾項當成固定、完整清單。

## 為什麼掃描器不能替你決定共享政策？

用兩個帳號交換物件參照，適合重現一部分錯誤，但工具仍然需要知道什麼結果應該被允許。工單 102 和 103 都是 Bob 建立的；前者不該給 Alice，後者刻意分享給她。只比對擁有者不同，就會把正常共享當成漏洞。

![梗圖文字「102 不能看，103 可以看／共享規則先給我啊」，呈現工具需要共享政策，才能判定 Alice 讀到 Bob 的工單是否越權。](/assets/post_local-preview_idor/idor-scanner-needs-policy.png)

*102 與 103 都是 Bob 的工單，是否分享給 Alice 會改變預期結果。 [範本：甘道夫](https://memegen.fhsh.taipei/templates/gandalf)*

學術研究也遇過「正確授權政策沒有完整寫下來」的困難。MACE 在 2014 年提出分析 PHP 程式的授權脈絡一致性：比較不同程式路徑對資源的檢查，找出可能漏掉的條件。論文也說明，若原本作為比較基準的檢查就錯了，其他路徑跟著錯，方法可能無法發現；為避免公開閱讀內容帶來誤報，其評估沒有納入 SELECT 查詢。[5](#ref-5)

這項研究示範如何從程式找出授權落差，仍受方法與評估範圍限制，不能當成今天所有框架都能直接套用的偵測保證。產品還是得定義誰能看哪張工單，把政策寫成可驗證的預期結果，工具與人工審查才有共同的判斷基準。

## UUID 能幫忙，但不能替你回答權限

隨機、難預測的 ID 能提高枚舉的成本。它仍可能透過合法共享、紀錄或其他流程被知道；對私人資源，即使別人拿到 ID，伺服器還是要拒絕無權限的存取。[1](#ref-1)

![梗圖以「只要 ID 猜不到／就不用查權限了吧」反串錯誤推論；UUID 降低猜測機會，取得 ID 的使用者仍要接受授權檢查。](/assets/post_local-preview_idor/idor-uuid-is-not-policy.png)

*私人資源的 ID 即使被知道，無權限的請求仍要拒絕。 [範本：動動腦](https://memegen.fhsh.taipei/templates/rollsafe)*

如果產品刻意採用「持有分享連結就能看」的設計，連結本身是授權憑證，就需要另行設計範圍、撤銷與有效期限。那與本文要求登入、再檢查共享名單的政策不同，不能拿同一套測試結果判定對錯。

本文的小模型還省略了管理員委派、資料庫並行更新與權限快取。正式系統若可能在檢查後、更新前撤銷權限，要依資料庫與一致性需求考慮交易或帶條件的更新；若快取了授權結果，也要處理權限變更如何生效。這些是部署時需要補上的工程問題，本地示範沒有證明它們已被解決。

驗收修補時，讓 Alice 再跑一次：自己的 101 能讀也能改，Bob 私人的 102 被擋住，共享的 103 能讀卻不能改。拒絕之後，資料也必須維持原值。這些預期結果要來自明確的權限政策，並由各個資料與副作用的出口落實；編號長什麼樣子，都不能省掉這個判斷。

## 參考文獻

<a id="ref-1"></a>

[1] OWASP Foundation, “Insecure Direct Object Reference Prevention Cheat Sheet,” *OWASP Cheat Sheet Series*. Accessed: Oct. 8, 2026. [Online]. Available: [https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)

<a id="ref-2"></a>

[2] OWASP Foundation, “API1:2023 Broken Object Level Authorization,” *OWASP API Security Top 10*, 2023. Accessed: Oct. 8, 2026. [Online]. Available: [https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/)

<a id="ref-3"></a>

[3] OWASP Foundation, “Authorization Cheat Sheet,” *OWASP Cheat Sheet Series*. Accessed: Oct. 8, 2026. [Online]. Available: [https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

<a id="ref-4"></a>

[4] OWASP Foundation, “Testing for Insecure Direct Object References,” *OWASP Web Security Testing Guide*, ver. 4.2, sec. 4.5.4, WSTG-ATHZ-04. Accessed: Oct. 8, 2026. [Online]. Available: [https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References/](https://wstg.owasp.org/v4.2/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References/)

<a id="ref-5"></a>

[5] M. Monshizadeh, P. Naldurg, and V. N. Venkatakrishnan, “MACE: Detecting privilege escalation vulnerabilities in web applications,” in *Proc. 2014 ACM SIGSAC Conf. Computer and Communications Security (CCS ’14)*, 2014, doi: 10.1145/2660267.2660337. [Online]. Available: [https://doi.org/10.1145/2660267.2660337](https://doi.org/10.1145/2660267.2660337). Author manuscript: [https://www.cs.uic.edu/~venkat/research/papers/monshizadeh-ccs14.pdf](https://www.cs.uic.edu/~venkat/research/papers/monshizadeh-ccs14.pdf)
