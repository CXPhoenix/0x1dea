# 保留的未完成嘗試

第一次隔離 build 在專案的隔離 profile 啟動前，被工具外層 sandbox 拒絕建立 localhost listener（PermissionError）。只變更測試控制程序的執行權限，使用同一份來源與原有 deny-default macOS profile 後，實際 build 成功；沒有改動程式、測試或專案保護。

同一外層限制下的完整 Python run 在精確核對 PID／PGID 與 cwd 後中止（exit130），未列為成功。後續從頭完整重跑另存 full-python.txt，包含原始歷史 fixtures，未使用 skip、fallback 或停用斷言。兩份未完成 log 與其原始／公開 SHA-256 均保留在 validation-records.json。
