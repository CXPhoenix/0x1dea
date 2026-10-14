# 規格來源與目前證據

查核日期：2026-10-11。這份文件分開記錄專案觀察、官方能力與本規格的設計選擇；不是部署完成證明。

## 已確認的使用者要求

採 GitHub Flow 加共用 staging 預覽；main 只含已發布文章；保留候選文章與歷史驗證契約。
本輪先完成 spec、測試計畫、審查與 workflow skill 草案，交作者確認；不修改部署設定。
既有 PR 不因本輪規劃取得 merge 授權。

## 分支與既有工作

| 項目 | 觀察 |
|---|---|
| 原始 checkout | staging，HEAD `4005ee45f2f3267a8b53ce24fa97af7b49cfb144`；規劃前沒有工作目錄變更 |
| 遠端 main | `eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a` |
| 遠端 staging | `c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7` |
| PR #20 → main | OPEN，head `e6e7a04da7a1e4d9819fa6f8aaadb72a0611e20c`；尚未落地 |
| PR #21 → staging | OPEN，head `a67b8de69f70f794a9e062e3ac50a957688ffa9a`；尚未落地 |
| 編號 | 前輪已使用 epic 0010、0011 與 ticket T-0012；本輪使用 epic 0012，不配置新 ticket |

這些是規劃時的快照。實作前必須重新查核，不能把 PR head 說成 main/staging 已包含。
前輪研究保存於 [PR #20 的研究文件](https://github.com/CXPhoenix/0x1dea/blob/e6e7a04da7a1e4d9819fa6f8aaadb72a0611e20c/.proj.specs/_discovery/publication-workflow/research.md)。

## 本機程式與契約觀察

- `scripts/article-publication.py:131–149` 的 v1 檢查拒絕 source 的任何 staging-only ancestor。
  A 尚未進 main、但 A topic 已合入 staging 時，A 自身就屬於 staging-only，因而遭拒絕。
  這是程式語意推論；本輪沒有改寫或執行新版實作測試。規格要求以 v2 的正例與污染反例驗證。
- 現有 CLI 只有 preview／prepare／verify；local receipt 的 `publishable:false` 不是發布授權。
  `skills/managing-article-publication/references/local.md` 要求精確 paths、獨立來源、build isolation
  與來源／輸出證據分離；`references/future-actions.md` 保留遠端操作與回復授權邊界。
- main/staging 仍有候選正文、專屬圖片與共用工程差異；其中 staging 的
  `blog/post/electricity-privacy.md` 是既有正式路徑上的不同版本，也必須視為未核准 revision，不能漏列。
- `docs/adr/0006-local-tracker-and-authorized-landing.md` 的 done 契約仍要求實際授權 staging 祖先與 receipt。
  新規格沒有把 main PR-ready 改成 done。
- 四個 canonical product packages 由 materializer 產生兩個 runtime；新 workflow 草案延伸既有
  `managing-article-publication`，不增加第五個 active package，也不直接修改生成檔。

## 官方能力與設計選擇

GitHub Flow 支援小型分支、PR 與審查；Git topic/integration 模型支援候選先進整合分支，再個別進穩定分支。
本專案選擇 main 為工程基底、staging 為共用預覽，而非整批 staging 發版。
[GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)、[Git workflows](https://git-scm.com/docs/gitworkflows)。

官方文件說明 `GITHUB_TOKEN` push 不會觸發一般 push workflow；明確 dispatch 是例外。
bot 產生的部分 PR 事件可能產生需要批准的 run，因此設計不可把「bot 開 PR」當作 checks 已執行。
本規格提議明確 dispatch 並核對實際 run；尚未啟用。
[Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)。

Merge API 的 `sha` 保護 head，不能當成鎖定 base 的原子操作；規格因此要求 activation 前驗證最新 base 檢查，
並區分 PR-ready 與後續實際 landing tree。
[Merge API](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request)、[Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)。

VitePress 依檔案路徑產生頁面，public assets 也會進入 build；「首頁沒列出 B」不足以證明 B 沒被帶入。
[Routing](https://vitepress.dev/guide/routing#file-based-routing)、[Asset handling](https://vitepress.dev/guide/asset-handling#the-public-directory)。

Cloudflare 可提供分支 alias 與 preview branch controls，但本輪未讀取帳號設定，也不改設定。
實際 alias、served SHA、GitHub branch rules、權限與 Actions dispatch 能力仍是 activation 前查核項目。
[Preview aliases](https://developers.cloudflare.com/pages/configuration/preview-deployments/#preview-aliases)、[Branch controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)。
