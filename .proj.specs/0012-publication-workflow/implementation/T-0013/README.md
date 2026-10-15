# T-0013：M0 盤點實作檢查點

目前只完成部分實作，具體 M0 等待作者審查。尚未建立工程基底 PR、可信的 current
successor 或 staging 整合，也沒有落地或結案。英文說明見 [README.en.md](README.en.md)。

## 公開介面

查看說明：

```sh
python3 scripts/publication-baseline.py --help
```

從儲存庫根目錄產生完整盤點：

```sh
python3 scripts/publication-baseline.py inventory --repo . --classification .proj.specs/0012-publication-workflow/implementation/T-0013/M0-classification.proposed.json
```

工具完成所有檢查後才輸出 JSON。這裡的 schema version 1 是「盤點分類格式」，與文章發布
plan v1、未來的 v2 無關。工具只讀取固定 commit 的 Git tree；不代表工作目錄或實際網站。
它不會準備發布樹、merge、部署或核准候選文章。JSON 中的 PR 狀態是輸入觀察，並非經過
驗證的 GitHub 收據；輸入也不能自行宣告已受信任。

分類表必須恰好涵蓋全部差異路徑，每筆有 `category`、`owner` 與選填的布林 `shared`。
分類包含 published、candidate、engineering、historical-management、current-management
及 target-role；共用路徑另附精確的 full-index patch。每個候選路徑只有一位所有者，連同
未變更的專屬圖片一起保留。若候選修訂刪除檔案，main 仍保留已發布狀態，盤點另記錄
staging 的缺席狀態。

目前來源全部標為 `legacy-requires-migration`，不會被視為 clean。前置觀察記錄 PR、
狀態、目標、完整 head 與選填 merge commit；只有 MERGED 觀察及本機 ancestry 都成立，
才會記錄該觀察已落地。這個唯讀提案介面仍不負責驗證遠端觀察的真實性。

分類與路徑都不是 validator 的豁免。非候選的 main 動作仍等待精確審查；候選則保留
main 既有已發布狀態，新候選維持不存在。staging 保留固定版本的完整狀態。

## 具體審查資料

- [M0 分類輸入](M0-classification.proposed.json)
- [完整雙樹、hash、mode、差異及共用 patch](M0-inventory.proposed.json)
- [給作者的 M0 審查摘要](M0-review.md)
- [測試覆蓋與驗證限制](coverage.md)

抽象 spec 與測試表的核准，不等於具體 M0 已獲核准。spec D1 明定：
「M0 is approved before it becomes trusted policy」。具體邊界核准後才繼續工程基底與
current successor 實作；後續精確 successor 的更新也必須接受同等審查，不建立管理資料夾
的整體豁免。

## T-0013 剩餘工作

實作並審查精確的 main 工程投影、從可信 target／base 選擇角色的共用 current validator，
以及有版本的精確 successor；驗證獨立 staging 整合仍保留全部候選。取得適用交付授權與
實際 main／staging 落地收據。P02、P03 的 current successor 部分，以及 P23 落地部分仍
未完成；T-0014 至 T-0018 仍依核准的阻擋關係等待。
