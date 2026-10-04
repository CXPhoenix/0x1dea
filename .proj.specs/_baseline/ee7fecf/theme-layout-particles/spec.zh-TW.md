---
language: zh-TW
authority: spec.en.md
synced_from: spec.en.md
synced_from_sha: 62dee28aeb554c0f453ca6324ef2a55171db0b53
source_path: openspec/specs/theme-layout-particles/spec.md
source_commit: ee7fecfff72f47abc735d26ac7e9a943de04ebbf
historical_harness_review: not-recorded-under-harness
---
# theme-layout-particles 規格稽核翻譯

> 英文原文是歷史權威；本頁是全文稽核翻譯。歷史 Harness review、TDD 與 landing 未記錄，不在此次重建。 Harness 歷史狀態為 `not recorded under harness`；`historical review not recreated`。下文保留歷史 docs 路徑；目前採用的 blog 路徑投影另見 adoption 規格。

## 目的

固定包裝預設版型的自訂 VitePress 主題：`docs/.vitepress/theme/index.ts` 全域註冊 `PostCard`／`PostBlock`／`PostList`／`NewPost`，並依 SSR 條件載入 `@tsparticles/vue3`；自訂 `Layout.vue` 在 `frontmatter.layout === 'home'` 或 `frontmatter.showParticle` 為 truthy 時，將粒子 canvas 放入 `#layout-top`；`Particles.vue` 隨 `isDark` 調色，主題切換時透過 `:key` 重新掛載；`config.mts` 的 `transformPageData` 對 `docs/` 子目錄下每個 `index.md` 套用五項 frontmatter 預設：`sidebar:false`、`aside:false`、`footer:true`、`showParticle:true`、`next:false`。日後修改版型 slot、粒子啟用邏輯或子目錄 `index.md` 預設，必須針對此 capability 提出差異規格。

## 需求

### Requirement: 自訂主題必須註冊 Layout.vue 及四個全域文章元件

`docs/.vitepress/theme/index.ts` 必須匯出 `Theme` 物件：

1. 擴充 `vitepress/theme` 的 `DefaultTheme`。
2. 將 `Layout` 設為自訂 `Layout.vue`，讓所有頁面使用自訂版型。
3. 在 `enhanceApp` 中對 `PostCard`、`PostBlock`、`PostList`、`NewPost` 各呼叫正好一次 `app.component(...)`，以其元件名稱註冊。
4. 非同步載入 `@tsparticles/vue3` 與 `loadSlim` 引擎，且只在 `import.meta.env.SSR` 為 `false` 時載入，避免將 tsparticles bundle 引入 SSR build。

#### Scenario: Markdown 可免匯入使用四個文章元件

- **WHEN** Markdown 引用 `<PostCard />`、`<PostBlock />`、`<PostList />` 或 `<NewPost />`
- **THEN** 不必宣告明確 `import` 即可顯示
- **AND** 不發出「failed to resolve component」警告

#### Scenario: SSR 階段不執行 tsparticles 匯入

- **WHEN** `vitepress build` 進行伺服器端顯示
- **THEN** `enhanceApp` 中 `await import('@tsparticles/vue3')` 與 `await import('@tsparticles/slim')` 不執行，因外層 `if (!import.meta.env.SSR)` 在 SSR 時短路
- **AND** 用戶端 bundle 只在 `import.meta.env.SSR` 判為 `false` 後執行兩個動態匯入

---
### Requirement: Layout.vue 在 showParticleBg 為 truthy 時，必須透過 layout-top slot 放入粒子 canvas

`Layout.vue` 必須擴充 `DefaultTheme.Layout`（以 `const { Layout } = DefaultTheme` 匯入），在 `#layout-top` slot 顯示內容。slot 必須有 classes 為 `visual-effects-container fixed inset-0 z-0 pointer-events-none` 的包裝 `<div>`，內部以 `v-if="showParticleBg"` 決定是否顯示 `<Particles />`。

`showParticleBg` 必須是從 `useData().frontmatter` 衍生的 `computed`：

```
showParticleBg = frontmatter.value.layout === 'home' || frontmatter.value.showParticle
```

此運算式**沒有**包在 `Boolean(...)`。`layout !== 'home'` 時，computed 直接回傳 `frontmatter.value.showParticle`，可能是 boolean、字串、數字或 `undefined`；truthy／falsy 由 Vue `v-if` 在顯示時判斷。作者與工具必須使用 YAML boolean `true`／`false` 宣告 `showParticle`。`showParticle: "false"` 這種帶引號字串是 **truthy**，會意外啟用粒子。`showParticleBg` 為 falsy 時不得顯示 `<Particles />`，但包裝 `<div>` 必須仍存在，作為不接收 pointer event 的空 overlay。

#### Scenario: 首頁由 layout=home 啟用粒子

- **WHEN** frontmatter 宣告 `layout: home`
- **THEN** `<Particles />` 顯示於 `#layout-top` slot
- **AND** 外層 `<div>` 有 `visual-effects-container`、`fixed`、`inset-0`、`z-0`、`pointer-events-none`

#### Scenario: 頁面透過 showParticle 選擇啟用

- **WHEN** 非首頁宣告 `showParticle: true`
- **THEN** 顯示 `<Particles />`

#### Scenario: 一般文章預設不顯示粒子

- **WHEN** `docs/post/**/*.md` 未宣告 `layout: home` 或 `showParticle`
- **THEN** 不顯示 `<Particles />`

#### Scenario: 頁面覆寫 showParticle 可停用粒子

- **WHEN** 子目錄 `index.md` 宣告 `showParticle: false`，覆寫 `transformPageData` 的預設值
- **THEN** 不顯示 `<Particles />`

##### 範例：showParticleBg 結果

| 頁面 | `frontmatter.layout` | `frontmatter.showParticle` | `showParticleBg` |
| --- | --- | --- | --- |
| `docs/index.md` | `home` | 省略 | `true` |
| `docs/posts.md` | 省略 | `true` | `true` |
| `docs/post/course/cybersec/index.md` | 省略 | `true`（預設） | `true` |
| `docs/post/course/cybersec/what-is-safety.md` | 省略 | 省略 | `false` |
| 任意頁面 | 省略 | `false` | `false` |

---
### Requirement: Particles.vue 必須依 isDark 調色並在主題切換時重新掛載

`Particles.vue` 必須：

1. 透過 VitePress `useData()` 取得 `isDark`。
2. `isDark.value` 為 `true` 時，`color` 與 `linksColor` 為 `'#ffffff'`； `isDark.value` 為 `false` 時為 `'#000000'`。
3. 底層 `<vue-particles>` 的 Vue `:key` 綁定 `isDark ? 'dark' : 'light'`。這是 template 語法，Vue 自動解開 `isDark` ref；使用者切換主題時，引擎重新掛載，而非原地修改。
4. 將 `<vue-particles>` 包在 `<ClientOnly>` 中，確保 SSR 不顯示 `<canvas>`，引擎只在用戶端初始化。

必須套用 `fixed inset-0 z-0 pointer-events-none opacity-60`，讓粒子全螢幕、位於互動內容後方，視覺效果輕淡。

#### Scenario: 淺色模式使用黑粒子

- **WHEN** `isDark` 為 `false`
- **THEN** `options.particles.color.value` 為 `'#000000'`
- **AND** `options.particles.links.color` 為 `'#000000'`

#### Scenario: 深色模式使用白粒子

- **WHEN** `isDark` 為 `true`
- **THEN** `options.particles.color.value` 為 `'#ffffff'`
- **AND** `options.particles.links.color` 為 `'#ffffff'`

#### Scenario: 主題切換重新掛載引擎

- **WHEN** 使用者將 VitePress 主題由淺色切為深色
- **THEN** `<vue-particles>` 的 Vue `key` 由 `'light'` 變為 `'dark'`
- **AND** 底層粒子引擎重新初始化，而非重新顯示相同實例

#### Scenario: SSR 不顯示 canvas

- **WHEN** 頁面在伺服器端顯示
- **THEN** HTML 不包含 `<canvas id="tsparticles">`
- **AND** 完全沒有 `vue-particles` 產生的 markup；`<ClientOnly>` 在 SSR 隱藏其 slot 子樹，Vue 不輸出字面 `<ClientOnly>` 標籤，而是完全不顯示該子樹

---
### Requirement: config.mts transformPageData 必須為子目錄 index.md 設定五個 frontmatter 預設

`docs/.vitepress/config.mts` 的 `transformPageData` 必須對同時符合 `pageData.relativePath.endsWith('index.md')` 與 `pageData.relativePath !== 'index.md'` 的頁面套用預設。原意是 `docs/` 子目錄的每個 `index.md`，排除根首頁；但字面 `endsWith('index.md')` 也會符合 **`docs/` 任何位置** 的假想檔名 `myindex.md`，沒有前導斜線限制，也不限於 `docs/post/`。作者不得在 `docs/` 任何位置建立 `relativePath` 以 `index.md` 子字串結尾、但 basename 不正好為 `index.md` 的檔案，例如 `docs/notes/myindex.md`、`docs/post/foo-index.md`；它們即使不是分類入口頁，也會無提示套用五項預設。

必須使用 nullish-coalescing assignment `??=` 設定預設。`??=` 左側為 `undefined` **或 `null`** 時都會指定預設，因此明確宣告 `null`（例如 YAML `sidebar: ~` 或 `sidebar: null`）也不會覆寫預設。只有非 null、非 undefined 值能覆寫。五項預設為：

| frontmatter key | 預設 | 理由 |
| --- | --- | --- |
| `sidebar` | `false` | 分類 index 不顯示 sidebar |
| `aside` | `false` | 分類 index 不顯示 aside |
| `footer` | `true` | 分類 index 保留網站 footer |
| `showParticle` | `true` | 分類 index 啟用粒子 |
| `next` | `false` | 分類 index 隱藏「下一篇」連結 |

hook 不得修改 `docs/index.md` 根首頁或非 index 頁。

#### Scenario: 子目錄 index.md 繼承全部五項預設

- **WHEN** `docs/post/course/cybersec/index.md` frontmatter 只宣告 `title`、`isIndex`、`category`
- **THEN** 執行 `transformPageData` 後 frontmatter 有 `sidebar: false`、`aside: false`、`footer: true`、`showParticle: true`、`next: false`

#### Scenario: 明確非 null frontmatter 覆寫預設

- **WHEN** `docs/post/course/cybersec/index.md` frontmatter 宣告 `sidebar: true`
- **THEN** 執行 `transformPageData` 後 `sidebar` 為 `true`，明確值優先
- **AND** 另外四個未宣告的 key 仍套用預設

#### Scenario: 明確 YAML null 不覆寫預設

- **WHEN** `docs/post/course/cybersec/index.md` 宣告 `showParticle: null` 或等效 `showParticle: ~`
- **THEN** 執行 `transformPageData` 後 `showParticle` 為 `true`，因 `??=` 對 `null` 與 `undefined` 都套用預設
- **AND** 要停用粒子的作者必須宣告非 null 的 falsy 值 `showParticle: false`，不可用 `null`

#### Scenario: 非 index basename 若以 index.md 結尾，也會被 hook 無提示納入

- **WHEN** 處理假想檔案 `docs/notes/myindex.md`
- **THEN** 因 `'notes/myindex.md'.endsWith('index.md')` 為 `true`，且 `'notes/myindex.md' !== 'index.md'`，套用全部五項預設
- **AND** 作者不得建立此類檔名；只有正好為 `index.md` 的 basename 支援作為分類入口頁

#### Scenario: 不修改根 index.md

- **WHEN** 處理 `docs/index.md`
- **THEN** `transformPageData` 不注入任何五項預設
- **AND** 完全沿用作者宣告的 frontmatter

#### Scenario: 不修改一般文章

- **WHEN** 處理 `docs/post/course/cybersec/what-is-safety.md`
- **THEN** `transformPageData` 不注入任何預設
- **AND** 完全沿用作者宣告的 frontmatter

##### 範例：hook 結果

| `relativePath` | 套用預設 |
| --- | --- |
| `index.md` | 否，根首頁 |
| `post/course/cybersec/index.md` | 是 |
| `post/course/rm/index.md` | 是 |
| `post/course/cybersec/what-is-safety.md` | 否，非 index.md |
| `posts.md` | 否，非 index.md |
