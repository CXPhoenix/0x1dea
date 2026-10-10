---
title: "【試稿】JWT 漏洞：簽章沒壞，為什麼還是信錯人？"
description: "簽章正確之後，issuer、audience、時間與用途仍決定這個 API 有沒有理由採信 token。"
createdTime: 2026-10-09T00:35:54+08:00
thumbnail: /assets/post_local-preview_jwt/jwt-wrong-audience.png
category: staging 試稿
draft: true
previewOnly: true
sourceSha256: 11db0c137517e38d2f459358418ffb723fb1bf802a629ea43d6c96c7a54c0972
previewVersion: v3
updatedTime: 2026-10-09T01:23:05+08:00
---

# JWT 漏洞：簽章沒壞，為什麼還是信錯人？

::: info staging 試稿・高密度修訂 v3
這是 2026 年 10 月 9 日的試稿修訂，供 staging 預覽，尚未發佈到正式站。

文中 `verification/` 檔名指作者的離線試稿 bundle。本 staging 預覽提供文中程式碼與圖片，未附完整測試 bundle。
:::

假設你正在做一個文件預覽服務。使用者登入後，瀏覽器帶著 JWT 呼叫 API，後端驗過簽章，便拿 `sub` 找使用者資料。一切看起來很合理。

現在，多加一個條件：同一個登入系統也替付款服務發 token。某張 token 的簽章完全正確，`sub` 也真的是這個人，但 `aud` 寫的是 `payment-api`。文件預覽服務收到它，應該接受嗎？

如果你的理由只有「它是我們登入系統簽的」，判斷就少了一步：**簽發者確實說過這些話，不代表它是在對這個服務說。** RFC 7519 把 `aud` 定義為 JWT 的預定接收者；當 token 帶有這個宣告，而處理者不在其中，就必須拒絕 [1](#ref-1)。

這個例子全是虛構的。接下來只用本地 Python 產生與驗證 token，不連線到任何網站。讀到 JSON 後，先別急著拿它授權：資料能解析、密碼驗證通過、API 可以採信，是三個不同的判斷。

## 那三段字串，到底保證了什麼？

常見的 JWT 長得像這樣：

```text
base64url(header).base64url(payload).base64url(signature)
```

這是使用 JWS compact serialization 的情況：header 描述演算法等資訊，payload 放宣告，最後一段承載數位簽章或訊息鑑別碼（MAC）[2](#ref-2)。本文只處理這種情況。JWT 也可以用 JWE 加密表示，不能把「三段」當成所有 JWT 的定義 [1](#ref-1)。

把 payload 做 Base64url 解碼，可能就看得到下面的內容：

```json
{"sub":"user-17","aud":"document-preview"}
```

這個動作不需要密鑰。你也可以改 JSON，再編碼回去；只有解析的程式仍然能讀到新內容。編碼讓資料方便傳輸。只改內容、保留原 MAC，解析仍會成功，驗證 MAC 才會發現不一致。一般未加密的 JWS payload 也沒有保密效果 [2](#ref-2)。

![反串錯誤推論的梗圖：上行「JSON 我看得懂」，下行「那就放行吧」。能解析 payload 並不代表 MAC 或簽章已通過驗證。](/assets/post_local-preview_jwt/jwt-parse-is-not-verify.png)

*看得懂內容，離放行還有幾關。只改 payload 時，解析能成功，原 MAC 的驗證卻會失敗。[範本：挑眉哥](https://memegen.fhsh.taipei/templates/rollsafe)。*

以本文的 `HS256` 為例，HMAC 使用共享密鑰，對指定的 signing input 計算 MAC。持有同一把密鑰的人可以產生 MAC，也可以驗證它；這和只用公開金鑰驗證的非對稱簽章不同。RFC 7518 要求 HS256 使用至少 256 位元的密鑰 [3](#ref-3)。範例因此產生 32 個隨機位元組，沒有拿一個好記的密碼來湊數。

讀到 `sub` 只是收到一個宣告。驗證 MAC 後，才有依據判斷內容是否由持有預期密鑰的一方產生。接著仍要回答：這把密鑰屬於誰？這張 token 的對象、用途和時間，合不合這個 API 的規則？

## 先訂收件規則，再收 token

我們替虛構的文件預覽服務訂一份驗證規則：

| 條件 | 本地範例接受什麼 | 少了這個條件會混淆什麼 |
|---|---|---|
| 演算法與密鑰 | 固定 `HS256`，使用程式自己產生的密鑰 | 讓輸入替驗證者選安全規則 |
| `iss` | `https://issuer.example.invalid` | 誰發出的宣告 |
| `aud` | 單一字串 `document-preview` | token 是簽給哪個服務 |
| `sub` | 已知的本地使用者 | 宣告能否對應應用中的主體 |
| `exp`、`nbf`、`iat` | 全部存在；整數時間；時間順序合理；有效期最多 300 秒 | 何時可用、何時過期，以及本地允許的存活時間 |
| `typ` | 自訂 `preview+jwt` | 是否拿別種用途的 token 來用 |

這是教學用的本地 profile，**不是通用 JWT 規格，也不是 OAuth access token 標準。** `preview+jwt` 是本例自訂值，300 秒是本例政策。RFC 7519 的 registered claims 並非每一項都對所有用途強制要求，應用必須說清楚自己需要哪些 [1](#ref-1)。

下面以 PyJWT 2.10.1 實作。它的 API 有一個容易漏看的差別：`require` 檢查「宣告是否存在」，各項驗證選項才檢查其有效性。只開過期驗證，不能順便假設每張 token 都一定帶 `exp` [4](#ref-4)。

（欄位根本沒來，檢查什麼到期日啦。￣▽￣;）

若想在乾淨的本地環境重跑：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install PyJWT==2.10.1
.venv/bin/python jwt_example.py
```

將下面存成 `jwt_example.py`：

```python
import secrets
import time
import jwt

KEY = secrets.token_bytes(32)  # 每次執行重新產生，只供本地實驗
ISSUER = "https://issuer.example.invalid"
AUDIENCE = "document-preview"
SUBJECTS = {"user-17", "user-23"}

def verify_preview(token):
    result = jwt.decode_complete(
        token, KEY,
        algorithms=["HS256"],
        issuer=ISSUER,
        audience=AUDIENCE,
        options={
            "require": ["iss", "sub", "aud", "exp", "nbf", "iat"],
            "strict_aud": True,
        },
        leeway=0,
    )
    claims = result["payload"]
    if result["header"].get("typ") != "preview+jwt":
        raise jwt.InvalidTokenError("wrong token type")
    if claims["sub"] not in SUBJECTS:
        raise jwt.InvalidTokenError("unknown local subject")
    if any(type(claims[k]) is not int for k in ("iat", "nbf", "exp")):
        raise jwt.InvalidTokenError("integer time required")
    if not (claims["iat"] <= claims["nbf"] < claims["exp"]):
        raise jwt.InvalidTokenError("invalid time order")
    if claims["exp"] - claims["iat"] > 300:
        raise jwt.InvalidTokenError("lifetime exceeds local policy")
    return claims

now = int(time.time())
base = {
    "iss": ISSUER, "sub": "user-17", "aud": AUDIENCE,
    "iat": now, "nbf": now, "exp": now + 300,
}
for label, audience in [("preview", AUDIENCE), ("payment", "payment-api")]:
    token = jwt.encode(
        {**base, "aud": audience}, KEY,
        algorithm="HS256", headers={"typ": "preview+jwt"},
    )
    try:
        claims = verify_preview(token)
        print(label, "accepted:", claims["sub"])
    except jwt.InvalidTokenError as error:
        print(label, "rejected:", type(error).__name__)
```

預期輸出是：

```text
preview accepted: user-17
payment rejected: InvalidAudienceError
```

兩張 token 都是同一把密鑰產生的，第二張沒有偽造簽章。它被拒絕，是因為這個 API 不接受付款服務的收件對象。這也說明為什麼測 JWT 時，只準備一張合法 token 和一張亂碼還不夠：你需要一張**密碼驗證會通過、但應用必須拒絕**的 token。

![期待與現實梗圖：上格開心地寫著「簽章驗過了」，下格失望地發現「aud 是另一個 API」。](/assets/post_local-preview_jwt/jwt-wrong-audience.png)

*簽章可以是真的，收件對象也可以真的不對。這張圖只提醒 audience 這一關，其餘驗證條件仍要逐項成立。梗圖以 [FHSH Memegen 的 dbg 範本](https://memegen.fhsh.taipei/templates/dbg) 製作。*

程式用 `decode_complete` 取得已通過 library 驗證的 header 與 payload，接著才檢查本地的 `typ` 和使用者規則。名稱裡有 `decode` 不代表一定只有解析；應看 API 文件與實際選項。反過來說，PyJWT 可以透過 `verify_signature=False` 讀內容，此時不能把回傳的宣告拿來授權 [4](#ref-4)。方便除錯的開關，放進驗證路徑就會改變信任前提。

## 驗證規則不能交給 token 自己選

你可能會想，header 已經寫了 `alg`，照著做不就好了？問題是 header 也在收到的 token 裡。驗證前，它和其他輸入一樣可能被改動。PyJWT 官方明確提醒：允許的演算法不能從 token 的 `alg` 推導，也不要混用會以不同方式解讀密鑰的對稱與非對稱演算法 [4](#ref-4)。

RFC 8725 整理了歷史上某些實作接受 `alg=none`、或把 RSA 公開金鑰誤當 HMAC 共享密鑰的問題。這些攻擊需要相應的實作缺陷或錯誤設定；不能看到 JWT 就推論它一定能被這樣繞過。該 RFC 要求驗證者限制演算法，並把密鑰綁定到指定演算法 [5](#ref-5)。本地測試中，固定只接受 HS256 的規則便拒絕了 HS384 與未簽署的 `none` token。

再看選密鑰的 `kid`。RFC 7515 把它定義成協助選擇密鑰的提示，不是可信密鑰的證明 [2](#ref-2)。正式服務若需要輪替密鑰，可以用 `kid` 在事先信任的密鑰集合中查找；不能因 token 說「請用這把」，就接受輸入附上的任意密鑰。RFC 8725 也提醒，盲目追蹤 `jku`、`x5u` 中的網址可能引入 SSRF，密鑰查找則可能形成注入入口 [5](#ref-5)。

本文先把密鑰固定在本地程式，讓範例不必處理遠端密鑰查找。真正接上身分提供者時，還得建立 issuer 與密鑰來源的綁定，處理輪替、快取與未知 `kid`；只比較 `iss` 字串，不能證明驗證用的密鑰真的屬於那個 issuer [5](#ref-5)。

![吐槽驗證規則交給輸入決定的梗圖：上行「演算法跟金鑰都你選」，下行「那我還驗什麼」。指的是未限定演算法或不查核金鑰來源的錯誤做法。](/assets/post_local-preview_jwt/jwt-token-picks-rules.png)

*可以讀 header 來選擇候選金鑰，但候選必須來自可信集合；演算法也得符合事先設定的規則。[範本：威利旺卡](https://memegen.fhsh.taipei/templates/wonka)。*

## 時間與用途，也要由應用說清楚

`exp` 是不能再接受 token 的時間，`nbf` 是尚不能接受的時間；`iat` 表達簽發時間，本身不是有效期限。RFC 7519 允許為時鐘偏差保留少量容忍值 [1](#ref-1)。本例設為零，方便觀察測試邊界；正式部署要依時鐘同步狀況決定，不能用很大的容忍值把驗證失敗一筆抹掉。

程式額外限制整數時間、時間順序與最多 300 秒的有效期。這些是本文的本地政策：例如 RFC 的 NumericDate 允許非整數表示，本文為了簡化處理選擇更窄的輸入。若 API 還要求「簽發超過多久就不能用」，也要另行定義；有 `iat` 欄位不會自動替你完成這個政策。

另一張 token 即使也採 JWT 格式，用途規則仍可能不同。以 RFC 9068 的 OAuth 2.0 JWT access token profile 為例，接收者需檢查 `typ`、issuer、audience、簽章與到期時間，並拒絕 `none`；其中的 `typ` 使用 `at+jwt` 或 `application/at+jwt` [6](#ref-6)。本文的 `preview+jwt` 不遵循那份 profile，不能拿這段程式直接替換 OAuth resource server。接真實協定時，應實作協定的完整規則，而不是搬幾個欄位過來就算接好了。

![檢查宣告有效性的疑問梗圖：上行「欄位都有了」，下行「值也一定有效嗎」。提醒存在檢查還需搭配時間、對象與用途規則。](/assets/post_local-preview_jwt/jwt-claims-have-rules.png)

*`require` 管存在，驗證規則管值與用途。本文的整數時間、五分鐘有效期和自訂類型都是本地政策，不能拿來代替別種 profile。[範本：瞇眼弗萊](https://memegen.fhsh.taipei/templates/fry)。*

## `user-17` 通過驗證，能讀 `user-23` 的檔案嗎？

本地範例回傳 `sub=user-17`，只代表這張 token 符合我們的規則。它沒有回答 `user-17` 能不能預覽 `doc-b`。假設那份文件屬於 `user-23`，API 仍然要檢查物件授權。RFC 9068 也把 token 驗證與結合其他情境資訊的授權判斷分開 [6](#ref-6)。

這裡有兩種不同的錯誤：一種是採信不該採信的 token；另一種是已確認使用者，卻讓他讀到不該讀的文件。後者即使 JWT 驗證全對，也可能照樣發生。在本例的擁有者政策下，`verify_preview()` 回傳後，還得把 `sub` 與文件的擁有者對起來。

![反串過度授權的梗圖：上行「我的 token 驗證過了」，下行「全站檔案都是我的」。錯誤推論在於把身分驗證成功當成所有文件的存取授權。](/assets/post_local-preview_jwt/jwt-verified-not-owner.png)

*`sub=user-17` 通過驗證後，讀 `user-23` 的文件仍須依物件政策拒絕。[範本：巴斯光年](https://memegen.fhsh.taipei/templates/buzz)。*

驗證也沒有消除 token 被偷走的風險。若以 bearer token 方式使用，持有者不需要另外證明自己握有密碼金鑰，便可呈送它 [7](#ref-7)。從這個性質可推知：簽章檢查無法單獨區分原使用者與拿到同一張 token 的人。傳輸與儲存、登出或撤銷需求，仍要在系統設計中處理；本文的五分鐘有效期只是縮短範例的可用期間。

## 把「拒絕的理由」放進測試

Gonzalez 等人在 MSR 2020 的研究分析了 53 個 Java 開源專案中的 481 個 JUnit 測試，整理出 token authentication 的測試情境 [8](#ref-8)。這份研究的 token 範圍比 JWT 廣，也以 Spring Security 為主要脈絡，不能當成所有 JWT library 的弱點統計。它提供的實用提醒是：測試要分辨輸入條件與預期結果，而不是只確認「登入成功過」。

本文的本地驗證另外跑了 22 個 token 案例，包括錯誤 issuer、audience、密鑰、演算法、用途、未知使用者、過期、尚未生效，以及缺少六項必要宣告。所有案例都符合預期；另確認改過的 payload 仍可在不驗簽模式下讀出。測試還在驗證 token 之後呼叫一個獨立的本地物件授權函式：`user-17` 讀取自己的文件成功，讀取 `user-23` 的文件則拋出 `PermissionError`。這是本例的擁有者政策，不是 JWT library 自動替 API 做的判斷。

![反諷不完整測試的梗圖：上行「合法 token 過關」，下行「壞的也過關 好耶」。把不該接受的 token 也放行是測試失敗，不是成功。](/assets/post_local-preview_jwt/jwt-test-rejects-too.png)

*測試也要確認不該接受的 token 被拒絕，尤其是簽章正確、用途或對象錯誤的案例；合法案例通過並不能補上這一關。[範本：成功小孩](https://memegen.fhsh.taipei/templates/success)。*

這些結果只覆蓋 Python 3.14.3、PyJWT 2.10.1 與本文的本地 profile。沒有測 HTTP middleware、非對稱金鑰、遠端 JWKS、輪替、token 撤銷或其他 library，也沒有拿它測第三方服務。範例完整測試程式為隨稿的 `verification/jwt_demo.py`。

檢查這段驗證程式時，可以拿開場的付款 token 試一次：**簽章正確，`aud` 卻是 `payment-api`，文件預覽 API 會拒絕嗎？** 再沿著程式查演算法由哪裡設定、密鑰由誰管理、哪些宣告必填、時間怎麼判斷，以及誰在驗證後檢查文件的擁有者。

## 參考文獻

<a id="ref-1"></a>

[1] M. Jones, J. Bradley, and N. Sakimura, “JSON Web Token (JWT),” RFC 7519, May 2015, doi: [10.17487/RFC7519](https://doi.org/10.17487/RFC7519). [Online]. Available: [https://www.rfc-editor.org/rfc/rfc7519.html](https://www.rfc-editor.org/rfc/rfc7519.html)

<a id="ref-2"></a>

[2] M. Jones, J. Bradley, and N. Sakimura, “JSON Web Signature (JWS),” RFC 7515, May 2015, doi: [10.17487/RFC7515](https://doi.org/10.17487/RFC7515). [Online]. Available: [https://www.rfc-editor.org/rfc/rfc7515.html](https://www.rfc-editor.org/rfc/rfc7515.html)

<a id="ref-3"></a>

[3] M. Jones, “JSON Web Algorithms (JWA),” RFC 7518, May 2015, doi: [10.17487/RFC7518](https://doi.org/10.17487/RFC7518). [Online]. Available: [https://www.rfc-editor.org/rfc/rfc7518.html](https://www.rfc-editor.org/rfc/rfc7518.html)

<a id="ref-4"></a>

[4] PyJWT contributors, “API Reference,” *PyJWT 2.10.1 documentation*. Accessed: Oct. 8, 2026. [Online]. Available: [https://pyjwt.readthedocs.io/en/2.10.1/api.html](https://pyjwt.readthedocs.io/en/2.10.1/api.html)

<a id="ref-5"></a>

[5] Y. Sheffer, D. Hardt, and M. Jones, “JSON Web Token Best Current Practices,” BCP 225, RFC 8725, Feb. 2020, doi: [10.17487/RFC8725](https://doi.org/10.17487/RFC8725). [Online]. Available: [https://www.rfc-editor.org/rfc/rfc8725.html](https://www.rfc-editor.org/rfc/rfc8725.html)

<a id="ref-6"></a>

[6] V. Bertocci, “JSON Web Token (JWT) Profile for OAuth 2.0 Access Tokens,” RFC 9068, Oct. 2021, doi: [10.17487/RFC9068](https://doi.org/10.17487/RFC9068). [Online]. Available: [https://www.rfc-editor.org/rfc/rfc9068.html](https://www.rfc-editor.org/rfc/rfc9068.html)

<a id="ref-7"></a>

[7] M. Jones and D. Hardt, “The OAuth 2.0 Authorization Framework: Bearer Token Usage,” RFC 6750, Oct. 2012, doi: [10.17487/RFC6750](https://doi.org/10.17487/RFC6750). [Online]. Available: [https://www.rfc-editor.org/rfc/rfc6750.html](https://www.rfc-editor.org/rfc/rfc6750.html)

<a id="ref-8"></a>

[8] D. Gonzalez, M. Rath, and M. Mirakhorli, “Did You Remember to Test Your Tokens?,” in *Proc. 17th Int. Conf. Mining Software Repositories (MSR)*, 2020, doi: [10.1145/3379597.3387471](https://doi.org/10.1145/3379597.3387471). Author manuscript: [https://arxiv.org/abs/2006.14553](https://arxiv.org/abs/2006.14553)
