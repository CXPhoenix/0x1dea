# T-0020：可重現的同步 job 輸入

本機前置檢查會確認完整 Git 歷史、兩個來源的精確身分、既有 runtime、外部設定與持久 journal。缺少條件便停止，不安裝套件或降低隔離要求。

每個 writer／validator 使用各自新建的輸入資料夾；先核對外部 manifest 與獨立 SHA-256，建立後封存為資料夾 0500、檔案 0400。消費時重新核對 UID、一般檔案、連結數、開啟與讀取期間身分，並從記憶體使用已驗證內容。系統無法安全變更的 UID／競態條件以明示的觀測 fixture 測試，不聲稱曾實際變更主機擁有者。

`publication-job.py prepare` 需要 `--manifest`、`--manifest-sha256`、`--repository`、`--role writer|validator`；`verify` 需要 `--snapshot-root`、獨立保存的 `--binding-sha256` 與相同 repository／role。外部 manifest 必須另行提供完整來源 pin、registry／runtime 及獨立摘要、既有 pnpm 路徑、全新 snapshot root、持久 state 路徑及其 identity 摘要。檔案不接受 permission／dispatch／exercise 的自行宣告。

前置檢查拒絕 API token；正式 writer transport 在隔離檢查完成後才另行使用其憑證。持久 journal 透過 repository 身分與來源祖先關係核對，未知結果先讀回再重試。writer 共用不取消的排程群組，validator 使用另一群組；這不代表限制所有人工操作者。

維護資料夾中的 workflow 仍為 inactive。這份交付只證明本機 CLI／Git／隔離邊界與 API adapter 契約，尚未證明 GitHub runner、權限、分支保護、排程或 P13。正式專案未啟用自動化，候選文章與歷史驗證契約保持原樣。

實際 writer／validator 消費入口會在同一流程內重新核對封存 snapshot，直接使用已驗證的 registry／runtime 記憶體內容，不再於檢查後另開原檔案。
