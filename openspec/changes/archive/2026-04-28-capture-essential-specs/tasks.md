## 1. post-content-model

- [x] 1.1 撰寫 Post interface SHALL define eight required fields 與 Index pages SHALL declare isIndex and provide an inheritable category 兩條需求，鎖定 Post 介面欄位形狀與索引頁的角色。
- [x] 1.2 撰寫 Loader SHALL discover posts via createContentLoader and exclude index pages 與 Loader SHALL resolve category through a three-tier priority chain 兩條需求，鎖定載入入口與分類解析優先序。
- [x] 1.3 撰寫 Loader SHALL always populate categoryFromPath and categoryRootPath from the URL、Loader SHALL apply field fallbacks for missing frontmatter、以及 Post frontmatter SHALL use ISO-8601 with +08:00 offset for createdTime 三條需求，鎖定 URL 衍生欄位、fallback 規則與 createdTime 的時間格式契約。

## 2. post-display-views

- [x] 2.1 撰寫 PostCard and PostBlock SHALL accept a Post and an optional showCategory prop 與 PostCard and PostBlock SHALL format createdTime in zh-TW for three input shapes 兩條需求，鎖定卡片與條列元件的 props、可選類別顯示與三種日期輸入形狀。
- [x] 2.2 撰寫 PostList SHALL accept a posts array and provide search, sort, and view-mode controls 與 PostList search SHALL filter by title in time mode and by title or category in category mode 兩條需求，鎖定 PostList 的 props 與搜尋過濾邏輯。
- [x] 2.3 撰寫 PostList SHALL sort by time numerically and by category lexicographically with a newest-first tiebreaker 與 PostList in category mode SHALL render posts grouped under category headers linking to categoryRootPath 兩條需求，鎖定排序演算法、群組顯示與類別標題的連結。
- [x] 2.4 撰寫 PostCard, PostBlock, PostList, and NewPost SHALL be globally registered by the theme 需求，鎖定主題層的全域元件註冊。

## 3. newest-posts-widget

- [x] 3.1 撰寫 NewPost SHALL accept count and showCategory props with documented defaults 與 NewPost SHALL apply the pipeline filter then sort then slice in that exact order 兩條需求，鎖定 widget 的 props 預設值與 filter→sort→slice 管線順序。
- [x] 3.2 撰寫 usePostSort SHALL export sortPostsKey and default to descending createdTime、usePostFilter SHALL export filterPostsKey and default to accept-all、以及 Consuming pages SHALL be able to override sort and filter independently via provide 三條需求，鎖定 InjectionKey 型別、預設行為與 provide 覆寫介面。

## 4. theme-layout-particles

- [x] 4.1 撰寫 Custom theme SHALL register Layout.vue and globally register four post components 與 Layout.vue SHALL inject the particles canvas via the layout-top slot when showParticleBg is truthy 兩條需求，鎖定主題入口設定與粒子背景的注入位置。
- [x] 4.2 撰寫 Particles.vue SHALL adapt color to isDark and remount when the theme toggles 與 config.mts transformPageData SHALL set five frontmatter defaults for subdirectory index.md pages 兩條需求，鎖定深淺色適配、ClientOnly 包裝與 index.md 子目錄頁面的 frontmatter 預設值。

## 5. 驗證與封存

- [x] 5.1 執行 spectra analyze、修正 Critical 與 Warning findings、再執行 spectra validate 確認通過，最後以 spectra park 將本次變更暫存等待後續 apply。
