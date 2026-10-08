# Combined publication and lint cleanup code review

Reviewed staging `64799e6df56cc1fab6673ce387f78794938619cb` to predecessor
HEAD `8890d5250e22ec4ee0e0493c1e72bab89d16489b`, plus complete staged,
unstaged and relevant untracked final files on
`tickets/T-0002/article-publication-preparation`. The first packet contained 144
paths; the final packet contains 145, with six evidence/text-only changes. The
checkout label is portable; raw local packets remain outside the public repository.
Independent read-only reviewers used the project code-review skill and the same
frozen surface. Actual file hashes and base/HEAD/merge-base were unchanged at each
final review. No requested change layer was excluded.

## Standards

初次發現 P2 1：coverage-report.md:43 混用「確认」，違反專案繁中規則。
已改為「確認」；獨立 delta 重核確認解決。另依安全審查修正 clean logs
的本機暫存路徑並重算 hashes，四份公開 log hashes 均吻合。

完整第一方 lint scope 有明確邊界，未加 ignore 或關閉規則；廣域診斷的
失敗與限制保留。獨立 successor 與歷史契約分開；canonical/materialized
ownership 有依據，沒有直接修改 generated packs。原始 P0 0／P1 0／P2 1；
殘留 P0 0／P1 0／P2 0。Smell heuristics 無確認 finding。

## Spec

獨立 Spec review 的原始與殘留 P0／P1／P2 皆 0。AP-01–AP-09 與
cleanup 要求相符；CLI 保持 local-only、`publishable: false`。相依性、
精確保存後繼、範圍／竄改反例及 red→green／乾淨安裝證據完整，沒有
弱化既有 assertion。最後 lint 22 檔零 errors／warnings，CLI 16、harness 53、
Vitest 14，以及 build/materializer/structure/preservation 通過。

## Limits and final delta

兩軸都是唯讀審查，沒有重跑安裝、測試或 OS sandbox。Chrome 輸入逾時，
互動瀏覽器驗證仍 blocked；Vue 介面 regression 與建置比較不能替代完整
瀏覽器驗證。既有隔離證據只適用其合成候選，未宣稱重新做過 escape audit。
三份 log 遮罩、hash 更新、繁中錯字及 targeted public scan 的六檔 delta
已由兩位 reviewer 獨立補核，產品 code/tests/successor 未變。
