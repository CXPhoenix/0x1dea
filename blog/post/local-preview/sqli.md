---
title: "【試稿】SQL Injection：當商品名稱開始改寫查詢"
description: "從一個商品名稱觀察 SQL 的資料與指令邊界，以及參數化查詢能保證的範圍。"
createdTime: 2026-10-09T00:35:53+08:00
thumbnail: /assets/post_local-preview_sqli/sqli-data-captain.png
category: staging 試稿
draft: true
previewOnly: true
sourceSha256: 8dbb6d534ad16ce85b0116d23a63c10183247b238fa9f4cc42cc3d8db21084b0
previewVersion: v3
updatedTime: 2026-10-09T01:23:05+08:00
---

# SQL Injection：當商品名稱開始改寫查詢

::: info staging 試稿・高密度修訂 v3
這是 2026 年 10 月 9 日的試稿修訂，供 staging 預覽，尚未發佈到正式站。
:::

假設你正在做一個小型商品目錄。搜尋欄輸入 `Pocket Pen`，畫面正常顯示商品；換成 `Maker's Notebook`，後端卻拋出 SQL 語法錯誤。

商品名字有個單引號，怎麼會變成資料庫的問題？

因為這個假想程式把名稱直接接進 SQL 文字。名稱裡的字元於是有機會結束字串，甚至改變查詢條件。SQL Injection（SQLi）發生的關鍵，就是不可信的輸入取得了改寫 SQL 語法的能力。OWASP 將參數化查詢列為主要防禦方式：讓查詢結構和輸入值分開處理。[1](#ref-1)

接下來只用 Python 內建的 `sqlite3` 和記憶體資料庫觀察這條邊界。[2](#ref-2) 所有商品與情境都是虛構的，沒有連到網站，也不需要找別人的搜尋欄試手氣。

## 先看那個單引號做了什麼

建立一個有兩筆已上架商品、一筆未上架商品的目錄：

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute(
    "CREATE TABLE products("
    "id INTEGER PRIMARY KEY, title TEXT, price INTEGER, published INTEGER)"
)
db.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", [
    (1, "Maker's Notebook", 900, 1),
    (2, "Pocket Pen", 300, 1),
    (3, "Unreleased Kit", 0, 0),
])

def unsafe_search(title):
    sql = (
        "SELECT id, title FROM products "
        f"WHERE published = 1 AND title = '{title}' ORDER BY id"
    )
    return db.execute(sql).fetchall()
```

這裡的 `published = 1` 表示只搜尋已上架商品。輸入 `Pocket Pen` 時，最後一段 SQL 是：

```sql
WHERE published = 1 AND title = 'Pocket Pen' ORDER BY id
```

輸入 `Maker's Notebook`，則會變成：

```sql
WHERE published = 1 AND title = 'Maker's Notebook' ORDER BY id
```

SQL 解析器看到 `'Maker'` 就認為字串結束了，後面的 `s Notebook` 不再是完整字串的一部分。本地範例實際得到 `OperationalError`。`Maker's Notebook` 是合法商品名，照樣撞到這個缺陷。（商品沒有取錯名字啊 (´･ω･｀)）

再把輸入換成這段只用於本地練習的文字：

```python
unsafe_search("' OR 1=1 --")
```

拼出來的查詢變成：

```sql
SELECT id, title FROM products
WHERE published = 1 AND title = '' OR 1=1 --' ORDER BY id
```

在 SQLite 中，`AND` 的優先序高於 `OR`。[3](#ref-3) 而 `--` 會讓後面的內容直到換行或輸入結束都成為註解。[4](#ref-4) 因此條件相當於 `(published = 1 AND title = '') OR 1=1`；右半邊恆真，三筆商品都被選出，包括原本不應公開的 `Unreleased Kit`。

這裡沒有刪除資料，也沒有執行第二句 SQL。光是改變同一句查詢的條件，就已經越過「只顯示已上架商品」的限制。

![船長梗圖寫著「我只是商品名稱／現在查詢聽我的」，反串輸入值被拼進 SQL 後，能改變 WHERE 查詢條件。](/assets/post_local-preview_sqli/sqli-data-captain.png)

*被接進查詢的輸入讓 WHERE 多出恆真的 OR 條件，連未上架商品都被選出。梗圖以 [FHSH Memegen 的 captain 範本](https://memegen.fhsh.taipei/templates/captain) 製作。*

## 修補的重點，是保住資料的位置

先把剛才的查詢改成這樣：

```python
def safe_search(title):
    return db.execute(
        "SELECT id, title FROM products "
        "WHERE published = 1 AND title = ? ORDER BY id",
        (title,),
    ).fetchall()
```

`?` 是值的 placeholder。Python 的 `sqlite3` 介面把 SQL 和參數序列分別交給 `execute()`；`(title,)` 中的逗號表示這是只有一個元素的 tuple。[2](#ref-2) 輸入再像 SQL，仍留在 `title` 的值位置，無法把這個比較改寫成另一個條件。

本地測試裡，`safe_search("Maker's Notebook")` 找到第一筆商品；`safe_search("' OR 1=1 --")` 則得到空清單，因為沒有商品的完整名稱等於那串文字。兩個結果一起看，才能確認修補沒有把合法資料順便趕走。

![得意小孩梗圖寫著「你想讓 OR 改寫條件／我只拿它比商品名稱」，以資料庫的口吻表達 safe_search 將整串輸入當作 title 的值比較。](/assets/post_local-preview_sqli/sqli-bound-value.png)

*同一串輸入在 safe_search 裡只拿來比對 title，不會增添 OR 條件。[範本：得意小孩](https://memegen.fhsh.taipei/templates/success)。*

你可能會想，把單引號拿掉是否更省事？先別急著替商品改名。名稱既然會直接進入 SQL 文字，就得改用值 binding，讓它留在商品名稱的位置。只針對一組字元做刪除或轉義，還得正確處理資料庫、語法位置與編碼差異；OWASP 明確不建議把全面轉義當成首選防禦。[1](#ref-1)

還有一種外觀看起來「用了參數」的寫法：

```python
sql = f"SELECT id FROM products WHERE title = '{title}'"
db.execute(sql, ())
```

傳入第二個參數不會讓已經拼好的 SQL 變安全。到 `execute()` 接手時，輸入早已進入查詢文字。檢查這段程式時，要追到 `title` 被拼接的那一行：空 tuple 沒有把它重新分離成綁定值。

## 欄位名稱也能塞進問號嗎？

搜尋修好了，接著加上「依名稱或價格排序」。這時可能會寫出：

```python
db.execute(
    "SELECT id, title FROM products WHERE published = ? ORDER BY " + sort_key,
    (1,),
)
```

`published` 使用 binding，`sort_key` 卻直接進入 SQL 文字。如果預期只允許升冪排序的欄位名稱，而本地輸入是 `-price`，SQLite 會把它讀成價格的負值運算，讓結果順序反轉。這個範例沒有引號、沒有分號，也沒有第二句查詢；它指出的缺陷是呼叫者仍可提供排序運算式。

那麼，把排序也寫成 `ORDER BY ?` 呢？

```python
db.execute(
    "SELECT id, title FROM products WHERE published = 1 ORDER BY ?",
    ("price",),
)
```

這不會把 `price` 變成價格欄位。SQLite 的參數代表運算式中的值；此處每一列的排序值都是同一個字串 `"price"`，無法得到想要的價格排序。[3](#ref-3) 沒有其他排序條件時，也不該依賴相同排序值之間的回傳順序。

欄位名稱、資料表名稱叫作識別字（identifier）；它們參與 SQL 的結構。一般的值 binding 不能取代這些位置。例如，隨附範例中的 `SELECT id FROM ?` 搭配 `("products",)`，實際產生語法錯誤。

![頓悟臉梗圖寫著「我把 price 綁好了／怎麼沒照價格排」，提醒 ORDER BY 的值 placeholder 收到字串 price，沒有把它變成價格欄位。](/assets/post_local-preview_sqli/sqli-identifier-value.png)

*ORDER BY ? 收到的是同一個字串值；要選價格欄位，得處理識別字。[範本：頓悟臉](https://memegen.fhsh.taipei/templates/scc)。*

這個界線也有學術研究直接討論。Cetin、Goldgof 與 Ligatti 的 *SQL-Identifier Injection Attacks* 研究指出：程式即使用 prepared statements 保護值，仍可能因為另外拼接欄位或資料表名稱而暴露識別字注入。他們還提出擴充 prepared-statement API 的研究原型；那是論文中的設計與實驗，不能當成你現在的 `sqlite3` 已經具有的功能。[5](#ref-5)

這篇論文分析的是特定 Java 原始碼資料集，並以規則辨認查詢建構方式；它的實驗範圍不能代表所有網站。[5](#ref-5)

對這個小目錄而言，介面只需要兩種排序，不必讓使用者交出任何 SQL 片段。我會把外部選項映射到程式碼裡的固定欄位：

```python
def list_products(sort_key, descending=False):
    sort_columns = {"title": "title", "price": "price"}
    if sort_key not in sort_columns:
        raise ValueError("Unsupported sort field")

    column = sort_columns[sort_key]
    direction = "DESC" if descending else "ASC"
    sql = (
        "SELECT id, title FROM products WHERE published = ? "
        f"ORDER BY {column} {direction}, id ASC"
    )
    return db.execute(sql, (1,)).fetchall()
```

這裡仍使用 f-string，但拼進去的 `column` 和 `direction` 都由程式碼控制。`sort_key` 只用來選擇既定選項，未知選項直接拒絕；外部輸入沒有被原樣放進 SQL。這就是這個功能的允許清單（allowlist），符合 OWASP 對無法用值 binding 的查詢部分所建議的處理方向。[1](#ref-1)

![黑豹梗圖寫著「名稱排序還是價格排序／沒有『幫我接這段 SQL』」，表達介面只提供固定排序選項，不讓呼叫者提供任意 SQL 運算式。](/assets/post_local-preview_sqli/sqli-sort-allowlist.png)

*清單只讓 sort_key 選既定欄位，未知選項會被拒絕；值仍另外綁定。[範本：黑豹](https://memegen.fhsh.taipei/templates/wddth)。*

如果 HTTP 參數是 `descending=false`，應先用明確規則解析成布林值，再呼叫函式。Python 中非空字串 `"false"` 本身仍是真值，直接把字串丟進這個 `if`，會選到 `DESC`。防住注入之外，功能也得照介面契約運作。

允許清單的範圍應隨功能決定。列出「資料庫裡所有存在的欄位」可能避免任意運算式，卻未必適合這個頁面；某個內部欄位合法存在，不代表公開搜尋介面應讓人使用它。本文的清單只放目錄確實提供的排序選項，資料存取權限仍要另外設計。

如果需求真的需要動態識別字，就要查所用資料庫與驅動程式的正式介面。例如 PostgreSQL 的 PL/pgSQL 動態查詢，官方文件區分用 `USING` 傳入的資料值，與透過 `format()` 的 `%I` 處理的識別字。[6](#ref-6) `%I` 是這個 PostgreSQL 介面的用法；SQLite 的識別字仍要依它自己的介面處理。識別字被正確引用後，仍須判斷該資源是否在功能允許的範圍。

## 幾個看似安心，卻還沒回答完的判斷

「這個驅動不能執行多句 SQL。」在 Python `sqlite3` 中，`execute()` 確實只接受單句，超過會拋出 `ProgrammingError`。[2](#ref-2) 但剛才的 `OR 1=1` 和排序運算都在單句內完成。即使 `execute()` 拒絕第二句，剛才那兩種單句改寫仍然可以成功。

「資料已經存進資料庫，應該可信了吧？」假設先用 binding 儲存商品名稱，後來某個報表又把查出的名稱接回 SQL，第二次使用仍會重現語法邊界問題。來源換成資料庫，不會自動把文字升格成安全的 SQL 片段。這個假設沒有在本文腳本中重現；它用來提醒審查者追蹤每一次查詢建構，而不只看第一次寫入。

「專案用了 ORM 或預存程序。」名稱本身也沒有交代輸入怎麼走到查詢裡。ORM 的 raw SQL、動態排序介面，或預存程序內部再次建構的 SQL，都應沿著實際介面檢查。OWASP 的建議同樣附有前提：預存程序必須安全實作，不能在裡面重新引入不安全的動態 SQL。[1](#ref-1)

![火場狗梗圖寫著「有 ORM 我就放心了／raw SQL：我還在拼字串」，反串假想開發者只看框架名稱，漏看 raw SQL 的不可信輸入拼接。](/assets/post_local-preview_sqli/sqli-orm-raw-sql.png)

*假想專案即使用了 ORM，raw SQL 的值傳遞方式仍要查；預存程序也有同樣的實作前提。[範本：火場狗](https://memegen.fhsh.taipei/templates/fine)。*

因此，若要替這個目錄寫回歸測試，我會保留三種不同目的的案例：普通名稱要能找到商品；含單引號的合法名稱也要能找到；試圖改寫條件的文字不能讓未上架商品出現。排序則另外測試每個允許選項、相同價格時的次排序，以及未知選項會被拒絕。這樣測，普通名稱壞掉、未上架商品意外出現，或排序偷偷接受額外運算式，都會各自留下失敗結果。

## 查詢安全了，還有哪些事沒被保證？

這個練習使用精確比對 `title = ?`。如果功能改成 `LIKE ?`，綁定值中的 `%` 和 `_` 仍有萬用字元語意。[3](#ref-3) 它們留在值的位置，不代表查詢語法被注入，但可能讓搜尋範圍比使用者預期更廣。介面要提供「樣式搜尋」還是「字面文字搜尋」，需要另訂規則。

![不滿貓梗圖寫著「參數是綁好了／% 還是萬用字元」，提醒 LIKE 的綁定值仍依樣式規則解讀百分號，搜尋範圍可能擴大。](/assets/post_local-preview_sqli/sqli-like-wildcard.png)

*綁定值沒有改寫 SQL，LIKE 仍會解讀 % 與 _；介面得決定要樣式搜尋還是字面搜尋。[範本：不滿貓](https://memegen.fhsh.taipei/templates/grumpycat)。*

參數化也不會替你決定誰能看資料、限制每次回傳幾筆，或修正昂貴查詢。它保護的是輸入值與 SQL 結構的邊界。資料庫帳號另應只拿到功能所需的權限，降低其他缺陷造成的損害；這也是 OWASP 建議的額外防禦。[1](#ref-1)

![扶額艦長梗圖寫著「SQLi 已經補好了／授權檢查？還沒寫」，以假想開發者的疏漏說明防止查詢被改寫，不會自動完成資料授權。](/assets/post_local-preview_sqli/sqli-query-authorization.png)

*梗圖中的假想開發者漏了授權；參數化不能替他判斷誰能看資料，資料庫帳號權限也得另設。[範本：扶額艦長](https://memegen.fhsh.taipei/templates/facepalm)。*

本篇隨附的腳本已在 Python 3.14.3、SQLite 3.52.0 執行，驗證單引號、條件注入、值 placeholder、排序允許清單與單句限制。它沒有實作 HTTP 伺服器，也沒有測試 PostgreSQL、MySQL、ORM 或預存程序；換環境時，必須依實際介面核對語法與行為。

若你取得了包含本文與驗證檔的本地草稿資料夾，可以在資料夾根目錄執行：

```sh
python3 verification/sqli-demo.py
```

成功時最後一行會顯示 `PASS: 14 checks`。資料庫只存在記憶體中，程式結束後就消失。

審查時，可以從收到 `title` 或 `sort_key` 的地方往下追，找到它進入 SQL 的那一行。商品名稱應透過 placeholder 傳值；排序選項則應映射到功能允許的固定欄位與方向。若還能把外部文字原樣接進查詢，就在那一行停下來，確認呼叫者究竟拿到了多少改寫 SQL 的空間。

## 參考文獻

<a id="ref-1"></a>

[1] OWASP Foundation, “SQL Injection Prevention Cheat Sheet,” *OWASP Cheat Sheet Series*. Accessed: Oct. 8, 2026. [Online]. Available: [https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html).

<a id="ref-2"></a>

[2] Python Software Foundation, “sqlite3 — DB-API 2.0 interface for SQLite databases,” *Python 3 Documentation*, secs. “How to use placeholders to bind values in SQL queries” and “Cursor objects.” Accessed: Oct. 8, 2026. [Online]. Available: [https://docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html).

<a id="ref-3"></a>

[3] SQLite, “SQL Language Expressions,” secs. “Operators, and Parse-Affecting Attributes,” “Parameters,” and “The LIKE, GLOB, REGEXP, MATCH, and extract operators”. Accessed: Oct. 8, 2026. [Online]. Available: [https://www.sqlite.org/lang_expr.html](https://www.sqlite.org/lang_expr.html).

<a id="ref-4"></a>

[4] SQLite, “SQL Comment Syntax.” Accessed: Oct. 8, 2026. [Online]. Available: [https://www.sqlite.org/lang_comment.html](https://www.sqlite.org/lang_comment.html).

<a id="ref-5"></a>

[5] C. Cetin, D. Goldgof, and J. Ligatti, “SQL-Identifier Injection Attacks,” in *2019 IEEE Conference on Communications and Network Security (CNS)*, 2019, doi: [10.1109/CNS.2019.8802743](https://doi.org/10.1109/CNS.2019.8802743). Author manuscript: [https://cse.usf.edu/~ligatti/papers/SQL-IDIA.pdf](https://cse.usf.edu/~ligatti/papers/SQL-IDIA.pdf).

<a id="ref-6"></a>

[6] PostgreSQL Global Development Group, “41.5.4. Executing Dynamic Commands,” *PostgreSQL 18 Documentation*. Accessed: Oct. 8, 2026. [Online]. Available: [https://www.postgresql.org/docs/18/plpgsql-statements.html#PLPGSQL-STATEMENTS-EXECUTING-DYN](https://www.postgresql.org/docs/18/plpgsql-statements.html#PLPGSQL-STATEMENTS-EXECUTING-DYN).
