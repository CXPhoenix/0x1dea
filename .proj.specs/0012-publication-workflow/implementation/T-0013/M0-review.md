# Concrete M0 review — proposal only

## 給使用者（zh-TW）

這份 M0 是本次實際版本的完整盤點，尚未核准為可信政策。核准分類不等於授權 merge、部署或發布文章。

| 項目 | 盤點結果 |
|---|---|
| main | `eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a`，1831 個路徑 |
| staging | `c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7`，2174 個路徑 |
| 差異 | 363 個路徑，完整逐檔資料見 JSON |
| 前置 PR | #20、#21 均為 OPEN，未視為已落地 |
| 歷史驗證 | 保留原版本；尚未授權新的精確 successor |
| main 候選內容 | 保留 main 既有已發布版本；新候選維持不存在 |
| staging 候選內容 | 保留完整文章、時間中繼資料、圖片、Git mode 與 blob |

| 候選單位 | 文章／資源路徑數 | 狀態 |
|---|---:|---|
| `agent-experiment` | 7 | 歷史混合來源，需另行審查遷移；未標為 clean |
| `browser-lab` | 7 | 歷史混合來源，需另行審查遷移；未標為 clean |
| `idor` | 8 | 歷史混合來源，需另行審查遷移；未標為 clean |
| `jwt` | 7 | 歷史混合來源，需另行審查遷移；未標為 clean |
| `sqli` | 8 | 歷史混合來源，需另行審查遷移；未標為 clean |
| `electricity-privacy-revision` | 13 | 歷史混合來源，需另行審查遷移；未標為 clean |

分類中的 engineering 與 target-role 只是所有權提案，尚未核准把 staging 的整檔帶入 main。尤其三套既有寫作技能的差異、歷史 verifier、preview 設定及首頁／側邊欄，必須逐項形成精確 successor 或 patch 後再審查。

這次僅產生提案與唯讀工具，沒有改文章、部署設定，也沒有執行 merge。T-0013 維持 processing。

## Exact evidence bindings

Repository: `https://github.com/CXPhoenix/0x1dea.git`. Observations refreshed during 2026-10-11 Asia/Taipei.

Classification covers every delta; full-tree entries also protect unchanged owned assets.
All source candidates retain their original full source pin (staging above); original and
reconstructed clean source commits are not asserted. Source migrations are blocked pending
separate exact original/new commits and owner-reviewed migration.

| Protected historical contract | Main blob | Staging blob |
|---|---|---|
| `maintenance/harness-adoption/baseline-files.json` | `e886c9397ae1631b56c40081520af61a7de6b21d` | `e886c9397ae1631b56c40081520af61a7de6b21d` |
| `maintenance/harness-adoption/candidate-delta.json` | `31b7b5ae0813915e04a553d6ef146e2cf7436eeb` | `31b7b5ae0813915e04a553d6ef146e2cf7436eeb` |
| `maintenance/harness-adoption/framework-import-manifest.json` | `110e41732c3e08b542c61723ccb72485ab4f29a0` | `110e41732c3e08b542c61723ccb72485ab4f29a0` |
| `maintenance/article-publication/source-boundary.json` | `d990cfd294deee88db61e2796622a609fddc895d` | `d990cfd294deee88db61e2796622a609fddc895d` |
| `maintenance/lint-cleanup/source-boundary.json` | `4caed7f10772d0ab019bcd97a9fca601f61a113c` | `4caed7f10772d0ab019bcd97a9fca601f61a113c` |
| `scripts/main_publication_verification.py` | `8bd34dd4e04e17327db4ce6eb89abc052bb8b486` | `8bd34dd4e04e17327db4ce6eb89abc052bb8b486` |
| `scripts/harness_reconciliation.py` | `absent` | `42fc35c2cc041ca45e6a4c3549488f0c30224ff3` |
| `scripts/verify-harness-adoption.py` | `19004c95d9f8b92e7c4c139eb950f9bfce172ba3` | `e882d7d2cfd3855ea30ae7d325b40cd755a91266` |
| `docs/adr/0006-local-tracker-and-authorized-landing.md` | `ab7f5cd6bfda5d9385c847bda8f709a187476f57` | `ab7f5cd6bfda5d9385c847bda8f709a187476f57` |

Before/after modes and all other boundaries are in the complete tree JSON. No historical
record is replaced by a mutable tracker oracle. ADR-0008 records only the approved design.

| Review input | SHA-256 |
|---|---|
| `M0-classification.proposed.json` | `71e88f0f2187505145701fd13145f9e156692d0e40d1bba7852b7c5290e03b49` |
| `M0-inventory.proposed.json` | `6d95e0c7036fef827ce3c4c7b97beae811597e908d755837cce4431b526ea89a` |
