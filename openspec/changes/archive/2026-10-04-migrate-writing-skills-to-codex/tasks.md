## 1. 來源與備份

- [x] 1.1 落實來源與模型決策及 Source-backed Codex maintenance：讀取三份指定來源與必要 references、保留官方與 repo 決策區別；以來源清單與讀取結果驗證。
- [x] 1.2 落實單一來源與可恢復搬移及 Canonical source and recoverable migration：備份 Mac 原檔、建立 repo 來源與相容入口；以 hash 清單與舊新 symlink 解析驗證。

## 2. 風格與工作流程

- [x] 2.1 落實風格與工作流程分離及 Phoenix style boundaries：改寫風格核心、分離維護與舊規格檢查；以適用、不適用與明示衝突小樣本驗證。
- [x] 2.2 落實 Agents SHALL invoke the helper script for new posts 及 The skill frontmatter SHALL satisfy the Anthropic Agent Skill specification：收斂新文觸發、保留 CLI 契約並更新入口；以 frontmatter、引用與腳本來源比對驗證。

## 3. 驗收

- [x] 3.1 分類 Claude 限定殘留、驗證所有本次修改引用／symlink 與 diff 範圍；保存實際執行結果及限制，通過 Spectra validate/analyze 並確認可歸檔；完成驗收後按歸檔分支關閉變更。
