# 保留的未完成嘗試

第一次三案例的可信驗證有兩項拒絕案例成功，正向案例則被既有 `clean_location` 擋下：新 fixture 使用 macOS `/var/folders` 別名。只將測試目錄改為 `Path(tmp).resolve()`；既有 symlink／輸出路徑保護維持原樣。後續成功執行另有獨立紀錄。

第一次集中 operation builder 時，編輯範圍索引錯誤，造成新模組的語法／縮排錯誤。已還原完整審查快照，只將重複 builder 換成共用 core 的直接引用，再成功重跑 focused suite。原失敗紀錄仍在 `tdd-evidence.json` 明列為 failed attempt，即使暫存檔名含有 green，也不改寫成成功結果。
