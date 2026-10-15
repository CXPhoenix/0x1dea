# 共用 staging 預覽與指定文章發布：workflow 研究

查閱日期：2026-10-11。這份文件是供作者討論的研究與建議，沒有更改專案契約、部署設定或分支保護規則。官方能力、本機觀察、專案推論分別標示。

## 結論

可以做到。建議以 **GitHub Flow 的小型 PR，加上共用 staging 整合預覽** 實現：main 的目前 Git tree 只含正式文章，所有候選在同一個 staging 網站審稿，核准後只把指定文章及明確依賴帶進 main。工程修正只做一次，合併 main 後由工具同步 staging。

這不是把 staging 當作必須整批發版的 develop。Git 官方 topic/integration 模型更直接對應需求：各 topic 可以先整合測試，成熟後分別進穩定分支；不穩定分支整支合併至穩定分支會帶入全部變更。[Git 官方 gitworkflows](https://git-scm.com/docs/gitworkflows)

## 你的需求可以保留

| 需求 | 建議行為 |
|---|---|
| main 只含已發布文章 | 進 main 的 PR 必須只有已核准文章、必要資源與明示共用依賴 |
| 全部候選集中審稿 | staging 整合每個候選的目前來源；作者固定開 staging 預覽網址 |
| 不想一篇一個網址 | 只部署 staging 作預覽，來源分支不需各自部署 |
| 指定文章才發布 | 從乾淨來源建立選文 PR，永不整支 staging→main |
| 不想修正推兩次 | 工程／管理 PR 以 main 為主，main→staging 同步自動產生並驗證 |
| 保留歷史驗證契約 | 既有來源凍結不改寫；新版規則使用明確、經審查的後繼邊界 |

這張表是對使用者契約的設計建議，不是已部署能力聲明。

## Git Flow、GitHub Flow 與整合預覽的差異

Git Flow 的 develop 整合下一版變更，release 從 develop 切出；原作者還要求不屬於該版的功能不得先進 release 來源。將已混有多篇未核准稿件的 staging 當 develop，再直接切 release，無法自然取得「任選一篇」的隔離。原作者在 2020 年補充，持續交付的網站可考慮較簡單的 GitHub Flow。[Git Flow 原作者模型與補充](https://nvie.com/posts/a-successful-git-branching-model/)

GitHub Flow 的核心是獨立分支、commit、PR、審查與合併，官方也用於文件協作。它沒有原生替本專案定義共用 staging 或 main→staging 自動同步；必須補上專案規則。[GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)

**專案推論：**不需要搬進完整 Git Flow。用 topic 保存可獨立發布的來源，staging 保存共同審稿的整合結果，比同時維護兩份工程基底更合適。分支名稱仍遵守 `tickets/<ticket-id>/<ticket-slug>`；一個 topic 可以先進 staging，核准後再進 main。Git 官方允許同一 topic 在不同整合分支逐步成熟。[gitworkflows](https://git-scm.com/docs/gitworkflows)

## 來源分支與預覽網址是兩件事

Cloudflare Pages 支援指定 Production branch，Preview branch controls 可用 Custom branches 僅 Include `staging`。文章來源分支存在，不代表必須觸發它們各自的預覽部署。[Branch deployment controls](https://developers.cloudflare.com/pages/configuration/branch-build-controls/)

成功的預覽部署具有固定分支 alias，例如 `staging.<project>.pages.dev`，隨該分支的新部署更新。每次部署的 hash URL 仍可能保留，作者日常可以只開 alias，不必管理各稿件的網址。[Preview aliases](https://developers.cloudflare.com/pages/configuration/preview-deployments/#preview-aliases)

**未查證：**本專案 Cloudflare 帳號目前是否只部署 staging、實際 alias、production branch、build command、watch paths 與遠端保護規則。官方文件只證明平台可做，不能替代帳號設定查核。未成功的新部署也不能當成 alias 已顯示最新 source；審稿需辨識 deployed SHA。[Build environment variables](https://developers.cloudflare.com/pages/configuration/build-configuration/#environment-variables)

## 建議日常操作

```text
main → 工程／管理 ticket branch → PR → main
                                      └→ 自動同步 PR → staging

main → 文章 A ticket branch → 整合到 staging（共用預覽）
                           └→ 核准後選文 PR → main

main → 文章 B ticket branch → 整合到 staging（同一預覽）
                           └→ 繼續審稿
```

1. 文章來源以 main 為基底，不從混稿 staging 切出。正文、圖片與文章專屬設定留在可辨識的 ticket branch，經整合進 staging 後共用預覽。作者回饋修改到來源，再更新 staging；只改 staging 的文字不能假定已回到選文來源。
2. 工程與管理修正從 main 建立單一 PR。需要先在 staging 驗證時，可先整合相同乾淨 topic；避免另外修改第二份同義程式。main 合併後，自動建立／更新同步 PR。
3. 核准 A 時，從 pinned main 與 A 的乾淨來源重建候選，列出正文、assets、listing、共用依賴的精確差異。確認審稿版本與選文產物一致，通過檢查後只合併 A。
4. main 更新後同步 staging，保留 B 等未選文。其他文章只從正式 main 取得必要更新；不要把 staging 合回文章來源。正式文章仍留在 staging，只有「尚未核准候選」的身分退出候選清單。

上述是建議，不是已實作自動化。Git 的穩定修正往整合分支傳遞、topic 源自最早需接收它的分支，提供合併方向依據；官方亦反對無理由頻繁把整合分支合回 topic。[gitworkflows](https://git-scm.com/docs/gitworkflows)

## 同步可以自動化，衝突不能假裝消失

可以讓 main 合併事件觸發同步工作：鎖定 main/staging SHA，建立同步分支，合併、執行驗證，再建立或更新一份同步 PR。成功才更新 staging；衝突或檢查失敗就保留目前 staging，回報具體檔案供處理。Git 在不能自動解決時本來就會停止。[git-merge](https://git-scm.com/docs/git-merge)

**專案推論：**若使用者未來授權只讓全部 required checks 通過的同步 PR 自動合併，就能省去日常第二次人工審批；目前的「先不要 merge」仍適用這次兩份 PR，沒有被研究文件撤銷。一般同步無法保證永不衝突，尤其共用 listing、設定、元件與管理記錄同時修改時。不可用整份 ours/theirs、force push 或 staging tree 覆蓋 main 解決。

本次麻煩有兩個已觀察到的來源：大量工程／管理成果先存在 staging，main 的精確發布邊界只接受另份投影；而 ticket 狀態也是被歷史快照保護的檔案。選文 PR 又複製部分元件與記錄，回同步時就需要逐項協調。候選文章共用網址本身不會要求如此做。

## 合併方法的選擇

| 方法 | 可確認的行為 | 對本案的判斷 |
|---|---|---|
| 乾淨 topic 的 merge commit | 保留 topic commits 與父系祖先關係 | 優先考慮，兩個整合面更容易辨識同一修改已納入 |
| squash | 建立新合併 commit，不保留原 topic commits 作祖先 | 可用於完成後結束的短分支；不建議長期反覆 squash main↔staging |
| cherry-pick | 依 commit 套用變更並建立新 commits | 少量明確獨立修正可用；混稿 commit 不會自動成為安全選文 |
| source snapshot | 取得指定來源的檔案內容 | 可比對最終 tree，但不證明原始來源歷史乾淨；直接覆蓋共用檔可能倒退 main 更新 |

GitHub 明示 squash 後繼續重用同一 head branch，舊 commits 可能再列入下一個 PR，衝突也可能反覆處理；GitHub rebase merge 也會建立新的 SHA。[GitHub merge methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github) Cherry-pick 與 restore 的語意分別見 [git-cherry-pick](https://git-scm.com/docs/git-cherry-pick)、[git-restore](https://git-scm.com/docs/git-restore)。

**既有混稿需先整理：**只把 staging 檔案 restore 或 cherry-pick 到新分支，不能因新 SHA 看來乾淨就宣稱原來源契約已滿足。現有 CLI 明確拒絕 staging-only 祖先；若文章原始來源已混入其他稿件，須另訂有完整 provenance、ownership、diff 與審查的遷移方案，保留舊拒絕案例，不靠改 SHA 規避。

## 選文的驗證與競爭條件

建議 manifest 綁定完整 main/staging/source/依賴 SHA、核准 article IDs、精確增改刪路徑與 modes/hashes、candidate tree、審稿部署 SHA、build/output inventory。正文、圖片、導航與共用 index 都要有 ownership；沒有選入的文章、route、搜尋/RSS/index 資料與專屬 assets 也要檢查。

不能只看首頁未顯示。VitePress 依 Markdown 路徑產生頁面；`public` 目錄檔案會原樣進輸出，未選文圖片即使沒有頁面引用，也可能已被部署。[Routing](https://vitepress.dev/guide/routing#file-based-routing)、[Asset handling](https://vitepress.dev/guide/asset-handling#the-public-directory)

**專案推論：**approval 應綁定內容與固定 SHA；main、來源或依賴漂移須重新 prepare/verify/build。合併前的查驗不能直接證明稍後的 tree：promotion 與同步應串行，required checks 驗證最新 base，合併後再核對實際 main/deployed tree。GitHub merge API 的 `sha` 可檢查 PR head，不能等同鎖定 base SHA。[Merge API](https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request)、[Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)、[Actions concurrency](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#concurrency)

自動同步的 CI 觸發也須明訂：目前官方文件指出，使用 `GITHUB_TOKEN` 的 push 不會再觸發一般 push workflow；`workflow_dispatch`／`repository_dispatch` 是例外。另有較新的 PR 例外：由它建立或更新 PR 的 `opened`／`synchronize`／`reopened` 可產生 workflow runs，但處於需要人工批准的狀態。因此不能假定 bot push／開 PR 就能無人介入跑完 checks。若希望同步不增加第二次人工操作，可設計明確 dispatch／可重用驗證流程，或適當 GitHub App；權限、成本與事件鏈需另審。這不代表外部 Cloudflare 部署也必然受同一規則抑制。[Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)

## 專案目前做到哪裡

以下是 staging c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7 的本機靜態查核，不能讀成遠端部署證明。

| 已有／限制 | 證據 |
|---|---|
| 只有 preview、prepare、verify，沒有遠端 promotion 命令 | scripts/article-publication.py:390-395 |
| 完整 SHA pins，拒絕 staging-only／其他候選祖先，包含曾加入後撤回的污染 | scripts/article-publication.py:131-149 |
| 從 main 重建單一選文，精確 paths/dependency ownership，遇 conflict 停止 | scripts/article-publication.py:187-229 |
| receipt 記錄 candidate tree、paths、inventory、pins，但 publishable:false | scripts/article-publication.py:337-344 |
| verify 重算 source/receipt/tree，不執行 build | scripts/article-publication.py:355-386；managing-article-publication/references/local.md:68-89 |
| remote publication 是未來工作，禁止整批 staging 發布 | managing-article-publication/references/future-actions.md:3-18 |
| 本機 .github 未觀察到 workflow YAML | 只讀目錄盤點；沒有宣稱查核遠端設定 |
| 歷史契約與現行 source successor 分離，禁止目錄全面放行 | .proj.specs/0009-test-contract-repair/spec.en.md:56-77；verify-harness-adoption.py:444-461 |

## 後續討論與遷移前提

已確定需求：main 只含正式文章、候選集中 staging、單一審稿網址、指定文章才進 main。可逆的建議是先將工程成果改成 main 優先與可驗證同步，再將每篇候選來源整理乾淨，保留既有 staging 網址。這次尚未改 AGENTS、ADR、技能、Actions 或 Cloudflare 設定。

實作規格前須查清：現有候選各自的乾淨來源；目前 main/staging verifier 的後繼邊界；Cloudflare 實際 preview controls 與 deployed SHA；GitHub merge methods／保護規則；自動同步的身分、權限、觸發與衝突處理。若要把預覽成功、作者 approval、production build 與發佈回執連成流程，也必須各自留下實際證據，不能只用本機 build 取代。

## 建議遷移順序與這次問題的直接關係

1. 先盤點並核准一個共同的工程基底：只將必要工程／管理差異送 main，候選正文與專屬 assets 留 staging。main、staging 目前的 dispatcher／精確 preservation successor 各有不同責任，不能直接複製整份 staging 來完成這一步。
2. 另寫同步與 promotion 的 spec、traceability、既有 seam 測試表，審查後實作自動 main→staging 與選文 plan。先以只開 PR、遇衝突停止的模式驗證；日後是否自動合併僅限同步 PR，由作者另外決定。
3. 逐篇盤點既有候選來源。乾淨來源沿用；混稿或 staging-only 來源需要明確的 provenance 修復與審查，不能單純換分支名字。這是一次性整理，不應變成每次發布都手工重建整個專案。

另外，歷史不可變證據與會持續變動的 tracker／現行程式必須分開。這次 T-0001 原始 ticket 連 status 都被 release snapshot 固定，正是結案也會觸發保存衝突的原因。建議後續契約保留原始歷史 fixture 與斷言，為現行管理狀態與正式工程演進訂明確、經審查的後繼規則；不能為了方便把整個資料夾放行，也不能讓每篇文章順帶複製一份不同工程狀態。這是未來契約設計，不是本次已解除任何保護。
