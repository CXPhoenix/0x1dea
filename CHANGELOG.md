# 更新日誌 (Changelog)

本專案的所有重大變更都將記錄在此文件中。
格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，並遵守 [Semantic Versioning](https://semver.org/lang/zh-TW/)。

## [1.4.0] - 2026-03-01

### 🚀 新增功能 (Features)
- **NewPost 元件**：新增 `NewPost.vue`，可在任意頁面顯示最新 N 篇文章（透過 `count` prop 指定數量，預設 5）。使用 `PostBlock` 呈現每一列，內部 pipeline 為 `filter → sort → slice`。
- **首頁最新文章**：於 `index.md` frontmatter 區塊後直接放置 `<NewPost class="mt-8" />`，在首頁 features 區塊下方展示最新文章。
- **usePostSort composable**：新增 `composables/usePostSort.ts`，封裝 `sortPostsKey`（`InjectionKey`）與 `usePostSort()` composable。預設依 `createdTime` 由新至舊排序；修正 VitePress ContentLoader JSON 序列化後 `Date` 以 `string` 型別傳遞至 client 的問題，改以 `new Date(value)` 統一處理。
- **usePostFilter composable**：新增 `composables/usePostFilter.ts`，封裝 `filterPostsKey`（`InjectionKey`）與 `usePostFilter()` composable。預設接受全部文章，可透過 `provide` 注入自訂篩選條件（如依 category 過濾）。

### ♻️ 重構與最佳化 (Refactor)
- **全局元件擴充**：於 `index.ts` 補充全局註冊 `PostBlock` 與 `NewPost`，統一 markdown 頁面的元件存取方式。
- **composables 目錄**：建立 `theme/composables/` 目錄，確立 theme 層 composable 的組織慣例；透過 `InjectionKey<T>` 提供型別安全的 provide/inject 介面，讓使用端可覆寫排序與過濾行為而無需修改元件。

## [1.3.0] - 2026-02-15

### 🚀 新增功能 (Features)
- **CLI 工具**: `new:post` 指令現在會自動在 `docs/public/assets/` 下建立與文章對應的靜態資源資料夾。
- **自動化測試**: 新增 `vpHelper` 單元測試，並修復 `Particles` 元件測試環境。

### ♻️ 重構與優化 (Refactor)
- **核心架構**: 重構 `posts.data.ts`，引入 `Post` 型別定義並優化分類解析邏輯。
- **指令更新**: 將 `pnpm new-post` 更名為 `pnpm new:post` 以符合專案命名慣例。

## [1.0.0] - 2026-02-14

### 🚀 新增功能 (Features)
- **VitePress 核心架構**: 完成專案初始化，整合 VitePress 1.0+ 作為靜態網站生成器。
- **UnoCSS 整合**: 引入 UnoCSS 原子化 CSS 引擎，實現輕量且高效的樣式開發。
- **動態粒子背景**: 整合 `@tsparticles/vue3` 與 `@tsparticles/slim`，實作首頁與全站的動態粒子效果。
- **文章列表佈局**: 新增 `PostList` 與 `PostLayout` 元件，支援部落格文章的自動列表與分頁顯示。
- **Git Commit 規範**: 建立 `tw-emoji-commit` 規範與相關工具指引，確保提交訊息的一致性。

### 📝 文件更新 (Documentation)
- **專案說明**: 更新 `README.md`，包含專案願景、技術架構與安裝指南。
- **關於我**: 新增 `about.md`，詳細介紹作者背景、專長與證照資訊。

### 🔧 系統配置 (Configuration)
- **TypeScript 支援**: 全面採用 TypeScript 進行開發與設定檔編寫 (`config.mts`)。
- **Linting**: 設定 ESLint 與相關規則，確保程式碼品質。
