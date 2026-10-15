Scope note: this T13 delivery reuses ONLY the four identical shared current/runner files from the captured T15 review; no T15 sync implementation is included. Original full review follows.

# T-0015 與共同 guard／runner 安全審查

固定範圍同 code-T-0015：54檔／13context，加 Git 分層 capture；hashes均相符，
base/HEAD/merge-base001b26f。未發現 HIGH/MEDIUM、confidence≥0.8 的候選；
未解HIGH/MEDIUM=0/0，因此無需新增偽陽性派工。

所有來源 Git 讀取強制禁止 lazy fetch／remote protocol；含 include 的 partial／
promisor 設定、缺失與內容 hash 不符的 blobs 均拒絕。空 template 的新 bare Git
與唯讀 alternates，不繼承來源 shell merge driver／候選 checker。完整來源、候選、
protected history、immutable aliases 及重新計算的 receipt/tree 均綁定可信控制資料。

共同 current metadata 採 offline 邊界；T13 已落地 policy 取自其 main commit，
由可信 controller objects／target ancestry 核對兩端，受驗 checkout不能自行選
程式或政策。新 runner 明確拒絕原歷史 test bytes 變更，不在失敗後切換契約。

reviewer 為唯讀靜態審查，未執行 PoC／候選程式；父 agent 另執行最新版完整127
Python與來源保留檢查，並保留23sync／3closed／1preflight等 public CLI 證據。
控制端／核准政策本身遭入侵、依賴掃描、可用性、遠端 adapter/CI/deployment 與
epic chain analysis不在此結論內；不宣稱全專案安全。
