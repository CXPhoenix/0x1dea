<div align="center">
  <div>
    <img src="./assets/banner.png" alt="0x1DEA Banner" width="100%">
  </div>

  <h1 style="margin-top: 10px;">0x1DEA</h1>

  <h2>想像力的溢位 —— 結合資通安全、軟體工程與 AI 探索的個人知識平台</h2>

  <div align="center">
    <a href="https://github.com/CXPhoenix/0x1dea/graphs/commit-activity"><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/CXPhoenix/0x1dea"/></a>
    <a href="https://github.com/CXPhoenix/0x1dea/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/badge/LICENSE-CC%20BY--SA%204.0-lightgrey"/></a>
    <a href="https://github.com/CXPhoenix/0x1dea/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/CXPhoenix/0x1dea?style=social"/></a>
    <a href="https://github.com/CXPhoenix/0x1dea/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/CXPhoenix/0x1dea"/></a>
    <a href="https://github.com/CXPhoenix/0x1dea/pulls"><img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/CXPhoenix/0x1dea"/></a>
    <img alt="Vue Version" src="https://img.shields.io/badge/vue-3.5+-green.svg"/>
    <img alt="VitePress" src="https://img.shields.io/badge/VitePress-1.6+-8a2be2.svg"/>
    <img alt="Version" src="https://img.shields.io/badge/version-1.4.0-blue.svg"/>
  </div>

  <p>
    <a href="#why-0x1dea">為什麼選擇本專案？</a>
    ◆ <a href="#quick-start">快速開始</a>
    ◆ <a href="#features">核心功能</a>
    ◆ <a href="#installation">安裝指南</a>
    ◆ <a href="#architecture">技術架構</a>
  </p>
</div>

## *最新消息* 🔥

- **[2026/03]** ✨ **v1.4.0 發布**！新增 `NewPost` 元件與 `composables/` 層，首頁現可自動展示最新文章。
- **[2026/02]** 🚀 **v1.3.0 發布**！新增 CLI 自動化資源管理與單元測試。
- **[2026/02]** 🚀 **v1.0.0 正式發布**！查看 [完整更新日誌](./CHANGELOG.md)。
- **[2026/02]** 🎉 專案正式啟動，整合 VitePress 技術文件架構。
- **[2026/02]** 🛡️ 強化資安專題內容，新增紅隊與滲透測試知識模組。

## 為什麼選擇 0x1DEA？ 🌟

本專案不僅是一個技術部落格，更是一個動態的知識實驗室。我們相信「魔法是想像力的領域，資安也是」。

- **🛡️ 資安核心** - 深入淺出的資通安全教學，涵蓋從基礎意識到高階攻防技術。
- **🏗️ 軟體工程** - 記錄現代 Web 開發實務，強調高品質程式碼與系統架構設計。
- **🤖 AI 驅動** - 探索人工智慧在日常開發與安全防禦中的實際裝載與應用。
- **🎨 極致視覺** - 使用 VitePress 展示主題，搭配 `tsparticles` 打造沈浸式的閱讀體驗。
- **📚 結構化知識** - 透過系統化的導覽與內容分類，讓學習路徑一目瞭然。
- **🆕 最新文章 Widget** - `NewPost` 元件可嵌入任意頁面，以 `count` prop 控制顯示篇數（預設 5），支援透過 `provide/inject` 注入自訂排序與過濾邏輯。

## 快速開始 🚀

```bash
# 1. 複製專案
git clone https://github.com/CXPhoenix/0x1dea.git
cd 0x1dea

# 2. 安裝 dependencies
pnpm install

# 3. 啟動開發伺服器
pnpm docs:dev
```

> **📋 前置需求**：Node.js 18+、pnpm 10.0+
>
> **🔍 需要更多選項？** 請參閱下方的 [安裝指南](#installation) 段落。

## 展示 🎬

### 現代化首頁設計 📝

> **任務描述**：打造一個充滿科技感且易於導尋的入口網頁。
>
> **視覺要素**：動態粒子背景 (Particles) + 漸層文字 + 響應式佈局。

<div align="center">
  <img src="./docs/public/heroImage.png" alt="首頁展示" width="750">
</div>

## 安裝指南 📦

本段落提供詳細的開發環境設定說明。

### 環境設定 🛠️

```bash
# 複製 repository
git clone https://github.com/CXPhoenix/0x1dea.git
cd 0x1dea

# 使用 pnpm 安裝 (建議)
pnpm install

# 執行測試 (確保環境正確)
pnpm test:unit
```

設定程式會自動：
- ✅ 安裝 VitePress 與相關插件
- ✅ 設定 UnoCSS 樣式引擎
- ✅ 配置 Vitest 測試環境

### 常用指令 ⚙️

| 指令 | 描述 |
|------|------|
| `pnpm docs:dev` | 啟動本地開發模式 |
| `pnpm docs:build` | 建立生產環境靜態檔案 |
| `pnpm docs:preview` | 預覽打包後的網站 |
| `pnpm new:post` | 建立新文章與資源資料夾 |
| `pnpm test:unit` | 執行單元測試 |

### 🛠️ 輔助工具詳細說明

#### `pnpm new:post`

快速建立新文章的 CLI 工具，支援自動分類與靜態資源資料夾管理。

> [!NOTE]
> 預設文章資料夾在 `docs/post` 下。

```bash
# 基本用法
pnpm new:post "文章標題"

# 指定分類 (建立在 docs/post/tech 資料夾)
pnpm new:post "Vue3 教學" -c tech

# 指定完整路徑
pnpm new:post "系統架構" -d docs/design
```

**自動化行為**：
1.  **文章建立**：生成標準 frontmatter 的 Markdown 檔案。
2.  **資源管理**：在 `docs/public/assets` 自動建立對應名稱的資料夾 (如 `post_tech_vue3_tutorial`)，方便存放該文章專屬圖片。

## 架構 🏗️

### 系統概覽 📊

0x1DEA 採用現代化的 Jamstack 架構，確保高性能與極致的 SEO 表現。

```
┌─────────────────────────────────────────────────────────┐
│                    VitePress 核心系統 🚀                  │
│               (Markdown 驅動 + Vue 3 整合)               │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  前端技術堆疊 🎨                                         │
│  • UnoCSS: 引擎式 CSS 框架                                │
│  • @tsparticles: 高性能粒子效果                             │
│  • Vitest: 極速測試框架                                   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Theme 元件層 🧩                                         │
│  • PostCard / PostBlock / PostList: 文章呈現元件           │
│  • NewPost: 可嵌入任意頁面的最新文章 widget               │
│  • composables/usePostSort: 可注入排序邏輯                 │
│  • composables/usePostFilter: 可注入過濾邏輯               │
└──────────────────────┬───────────────┬──────────────────┘
                       │               │
                       ▼               ▼
                ┌─────────────┐ ┌─────────────┐
                │ 資安知識庫 🛡️ │ │ AI 探索實驗 🤖 │
                └─────────────┘ └─────────────┘
```

### 關鍵設計決策 💡

- **VitePress**: 選擇 VitePress 是因為其卓越的開發體驗與靜態生成效能。
- **UnoCSS**: 採用按需生成的樣式引擎，極端縮減打包後的 CSS 體積。
- **Theme Customization**: 透過 Vue Components 自定義 Hero Section 與佈局，強化視覺個人化。
- **Composable DI 架構**: `NewPost` 元件透過 `provide/inject` 注入排序與過濾策略，行為可依頁面需求彈性覆寫，無需修改元件本身。

### NewPost 元件使用指南 📦

#### 基本用法

直接在任意 markdown 頁面中使用，預設顯示最新 5 篇：

```markdown
<NewPost />
```

指定顯示篇數：

```markdown
<NewPost :count="3" />
```

---

#### 自訂排序（provide）

在頁面的 `<script setup>` 中 `provide` 自訂排序函式，`NewPost` 會自動注入並使用。

**最舊優先**：

```vue
<script setup>
import { provide } from 'vue'
import { sortPostsKey } from './.vitepress/theme/composables/usePostSort'

provide(sortPostsKey, (a, b) =>
  new Date(a.createdTime).getTime() - new Date(b.createdTime).getTime()
)
</script>

<NewPost :count="5" />
```

> `sortPostsKey` 的型別為 `InjectionKey<(a: Post, b: Post) => number>`，
> 回傳負值表示 `a` 排在前面，正值表示 `b` 排在前面。

---

#### 自訂過濾（provide）

**只顯示特定 category 的文章**：

```vue
<script setup>
import { provide } from 'vue'
import { filterPostsKey } from './.vitepress/theme/composables/usePostFilter'

provide(filterPostsKey, (post) => post.category.startsWith('course'))
</script>

<NewPost :count="5" />
```

**同時自訂排序與過濾**：

```vue
<script setup>
import { provide } from 'vue'
import { sortPostsKey } from './.vitepress/theme/composables/usePostSort'
import { filterPostsKey } from './.vitepress/theme/composables/usePostFilter'

provide(filterPostsKey, (post) => post.category === 'ctf')
provide(sortPostsKey, (a, b) =>
  new Date(a.createdTime).getTime() - new Date(b.createdTime).getTime()
)
</script>

<NewPost :count="3" />
```

> **Note**：內部 pipeline 順序為 `filter → sort → slice(0, count)`，
> 即先過濾、再排序、最後取前 N 篇。

---

#### Provider API 一覽

| Key | 位置 | 型別 | 預設行為 |
|-----|------|------|----------|
| `sortPostsKey` | `composables/usePostSort.ts` | `(a: Post, b: Post) => number` | 依 `createdTime` 由新至舊 |
| `filterPostsKey` | `composables/usePostFilter.ts` | `(post: Post) => boolean` | 接受全部文章 |

## 貢獻 🤝

本專案為個人知識庫，但非常歡迎建議與勘誤！詳情請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) (待發布)。

### 貢獻領域 ✨

- **📚 內容補充**：如果您發現資安技術內容有誤或可優化之處。
- **🎨 UI/UX 改善**：針對視覺效果與佈局的建議。
- **🧪 漏洞回報**：如果您在本站架構中發現安全性問題。

## 授權 📄

本專案採用 **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** 授權 - 詳情請參閱 [LICENSE](LICENSE) 檔案。

<div align="center">
  <a href="https://creativecommons.org/licenses/by-sa/4.0/">
    <img src="https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg?style=for-the-badge" alt="CC BY-SA 4.0"/>
  </a>
</div>

## 致謝 🙏

### 理念 💭

> **「魔法是想像力的領域，資安也是。」**

感謝所有在資安路上的前輩與夥伴，本專案的靈感源自於無數場 CTF 比賽與深夜的 Code Review。

## 貢獻者 👥

| 姓名 | 角色 | 聯絡方式 |
|------|------|---------|
| **CXPh03n1x** | 創始人 / 主要維護者 🚀 | [GitHub](https://github.com/CXPhoenix) |

---

<div align="center">
  <p>
    <strong>用 ❤️ 打造，來自 0x1DEA Project</strong><br>
    <sub>探索、學習、想像力溢位 ✨</sub>
  </p>
</div>
