## Why

0x1DEA 的程式碼庫已經對外公開多項契約（NewPost widget 的 props 與 provide/inject 介面、Post 資料模型與 frontmatter 慣例、自訂主題的粒子背景開關等），但目前只有 `vitepress-post-scaffolding` 一條 spec 受到 Spectra 規範保護。其餘契約僅由原始碼與 README 共同維繫，未來只要有人重新命名某個 InjectionKey、移除 `categoryFromPath`、或變動 `createdTime` 的格式，便會在沒有任何 spec delta 的情況下破壞既有的公開行為。本次變更回填這些必要 spec，把現況凍結為可審查的契約。

## What Changes

- 新增 4 條 capability spec，分別涵蓋：
  - `post-content-model`：Post interface、`docs/shared/posts.data.ts` 的 loader pipeline、frontmatter 慣例（含 `isIndex` 索引頁）、分類解析優先順序、`createdTime` 的 ISO-8601 +08:00 格式、以及各欄位缺失時的 fallback 規則。
  - `post-display-views`：`PostCard` / `PostBlock` / `PostList` 的 props 與行為，包括 PostList 的搜尋、time/category 排序軸切換、asc/desc 順序切換、card/block 視圖切換、以及 category 模式下的群組顯示。
  - `newest-posts-widget`：`NewPost` 元件（`count` 預設 `-1`、`showCategory` 預設 `false`、`filter → sort → slice` 管線順序），以及 `usePostSort` / `usePostFilter` 的 InjectionKey、預設行為與 provide override 介面。
  - `theme-layout-particles`：自訂 `Layout.vue` 的條件式粒子注入、`Particles.vue` 對 `isDark` 的色彩適配、`docs/.vitepress/config.mts` 的 `transformPageData` 對子目錄 `index.md` 套用的 frontmatter 預設值。
- 不修改任何現有 production code（`docs/**`、`scripts/**`、`tests/**`、設定檔皆維持不變）。
- 不新增 `design.md`：此為現況回填，無架構決策需要記錄；以 Non-Goals 取代設計討論。

## Non-Goals

- 不重寫或刪除現有的 `vitepress-post-scaffolding` spec（探索結果顯示該 spec 與目前 `pnpm new:post` 行為零漂移，無更新必要）。
- 不對 `nav.yml` / `sidebar.yml` 的 YAML 載入流程立 spec：屬於純資料配線，無公開行為契約。
- 不為 UnoCSS、FontAwesome、`style.css` 視覺微調立 spec：屬於樣式微調，非公開 API。
- 不改 `openspec/config.yaml` 或 Spectra 自身設定。
- 不新增任何測試、元件或擴充點；本次純為文件化既有行為。

## Capabilities

### New Capabilities

- `post-content-model`: Lock down the `Post` interface, the `posts.data.ts` content-loader pipeline, post and index-page frontmatter conventions, the category resolution priority chain, `createdTime` format, and field-fallback rules.
- `post-display-views`: Lock down the `PostCard` / `PostBlock` / `PostList` rendering surface — props, view-mode toggle, sort-axis toggle, search filter, and category-grouped rendering.
- `newest-posts-widget`: Lock down the `NewPost` widget's props and `filter → sort → slice` pipeline, plus the `usePostSort` / `usePostFilter` `InjectionKey` contract used to override sort and filter from any consuming page.
- `theme-layout-particles`: Lock down the custom `Layout.vue` slot injection, `Particles.vue` dark-mode adaptation, the `showParticle` frontmatter trigger, and the `transformPageData` defaults for subdirectory `index.md` pages.

### Modified Capabilities

(none)

## Impact

- Affected specs: 4 new capabilities listed above (each creates `openspec/specs/<name>/spec.md` once this change is archived).
- Affected code:
  - New: `openspec/changes/capture-essential-specs/proposal.md`, `openspec/changes/capture-essential-specs/tasks.md`, `openspec/changes/capture-essential-specs/specs/post-content-model/spec.md`, `openspec/changes/capture-essential-specs/specs/post-display-views/spec.md`, `openspec/changes/capture-essential-specs/specs/newest-posts-widget/spec.md`, `openspec/changes/capture-essential-specs/specs/theme-layout-particles/spec.md`
  - Modified: (none)
  - Removed: (none)
- 對 production code 零影響：specs 僅描述目前行為，後續若要修改行為，需另外提出 delta 變更。
