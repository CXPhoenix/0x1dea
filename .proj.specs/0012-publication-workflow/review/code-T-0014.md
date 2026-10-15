# T-0014 獨立程式審查

範圍：main-based `tickets/T-0014/v2-selected-candidate`，base/HEAD `001b26f`；
五個 v2 controller/build helper/tests/schema/使用者文件。精確 hashes 見
`../implementation/T-0014/review-capture.json`。共同 current guard、runner 與有限
工程 map 另由 T-0015 共同邊界審查，不能由本報告宣稱通過。

## Standards

原 P2 語言與 Duplicated Code 各一項：文件使用「子行程」，pin checking 改為同一
check_pins 入口；覆核未解 P0/P1/P2=0/0/0。v2 offline 行為限於匯入的 module
instance，原 v1 bytes/assertions 不變。canonical branch、已核准 public Git/CLI seams、
合成核准與實際 build／發布的區別均符合規範。extra regressions 未冒稱 red cycles。

## Spec

原 P1 兩項已解決：完整 base→candidate delta 拒絕 canonical alias 新增／刪除／變更；
其他 article 的非 main commit identity 與 source ancestry 相交即拒絕，包含 empty
commit。兩項均有 public CLI 真實 red→green；alias 刪除另有 green regression。
覆核 P0/P1/P2=0/0/0。完整 registry、來源歷史、shared patch、依賴、legacy binding、
固定 build 與 separate ready evidence 均符合本票範圍。

三位 reviewers 分別完成 Standards、Spec、Security 固定快照複查，父 agent 另完成
30 項 public tests 與真實隔離 build；reviewers 沒有執行候選程式。合成 Git/approval
不能證明真實 legacy 搬移、shared preview HTTP 或作者驗收。T-0014 尚未實際落地。
