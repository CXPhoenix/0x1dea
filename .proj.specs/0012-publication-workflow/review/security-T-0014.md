# T-0014 安全審查與修正

固定範圍同 code-T-0014；原候選 HIGH 由另一位 reviewer 獨立確認（confidence0.85），
修正後覆核：未解 HIGH/MEDIUM=0/0。未宣稱全專案安全。

## 已解 HIGH：來源 Git lazy fetch 啟動外部 helper

攻擊者須能控制受驗 repository 的 local Git config 與 object database；只有文章
commit 權限並不足。原新 v2 call sites 在 build sandbox 前沿用 old.git/tree，
Git 的 missing blob＋promisor remote 可觸發 fetch／ext transport；v1 helper 清除
GIT_* 防護且只禁用 global/system config，因而重新暴露既有 helper 問題。
原因見 [Git partial clone](https://git-scm.com/docs/partial-clone)、
[remote-ext](https://git-scm.com/docs/git-remote-ext)、
[promisor remote 原始碼](https://kernel.googlesource.com/pub/scm/git/git.git/+/18df122d3da765f104d451f95d9195d333f60671/promisor-remote.c)。

修正只在 v2 匯入實例強制 GIT_NO_LAZY_FETCH=1/GIT_ALLOW_PROTOCOL 空值，所有來源
Git 呼叫與獨立 bare merge 都涵蓋；含 local include 的 partial/promisor 設定於讀取
objects 前拒絕。原 v1 CLI/helpers/history assertions 不修改。
public CLI 的 harmless promisor admission 有真實 red→green；缺失 blob＋ext::touch
合成 fixture regression 確認 marker 未產生，Git2.54.0。沒有在舊實作執行惡意命令。

## 覆蓋與限制

獨立 reviewer 靜態資料流複查確認原路徑已封閉，其他逐路徑／binding／固定 build
／產物比對未找到 confidence≥0.8 的新增漏洞。父 agent 執行30focusedcases與真實
OS sentinel，read/write/network均 denied；raw records 相鄰保存。共同 current
guard／runner 尚依另一份固定快照審查；控制端本身遭入侵、依賴掃描、可用性、
遠端部署與 epic chain analysis 不在本票安全結論內。
