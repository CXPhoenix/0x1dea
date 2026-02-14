# 更新日誌 (Changelog)

本專案的所有重大變更都將記錄在此文件中。
格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)，並遵守 [Semantic Versioning](https://semver.org/lang/zh-TW/)。

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
