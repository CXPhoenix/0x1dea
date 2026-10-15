# T-0016 可信同步實作

已核對 main `5e6c889c` 與 staging `61292484` 的實際落地；PR #20、#25、#26 皆為兩端祖先，PR #21 的落地 tree 等於原審查 head。T-0012、T-0014、T-0015 符合條件後，在本機 tracker 標記 done。50 個候選路徑與 376 個受保護歷史路徑完整保留；main 沒有帶入候選文章。原驗證器、歷史 receipts 與原測試斷言維持啟用。驗收與來源見旁邊的 dual-landing-20261016/。

T-0016 已完成本機同步 controller、JSON API adapter、可信驗證 CLI 與停用 workflow 範本，涵蓋單一 PR、最新來源核對、共用 writer lock、未知 API 結果讀回、三次 retry 上限與驗證身分綁定。範本只放在 maintenance，沒有寫入 .github 或變更部署設定。

完整 Python 測試：main 192 項、staging 221 項，零失敗、零錯誤、零 skip；unit 各 54／87 項、lint、native、結構及 materializer 成功。本機隔離 build 也成功。詳見 coverage.md 與 final/；原始實作審查的 bootstrap、共用 builder 與 writer token 邊界問題均已修正並保留驗證紀錄，最後文件證據審查另行記錄。

T-0016 保持 review，尚未 done：P13 需另行指定並授權測試用 repository，驗證實際權限、dispatch 與最新 base/head 保護。本輪正式 repository 的唯讀資料不能代替演練。尚未 commit、push、開新 PR、merge、啟用自動化或修改部署設定。
