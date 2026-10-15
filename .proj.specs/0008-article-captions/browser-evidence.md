# Browser and SSR evidence

Surface: locally served VitePress website in agent-browser Chromium, not staging/production. Local dev server on 127.0.0.1:5178. The article retains draft/previewOnly frontmatter. No external publication, install or remote action.

## Observed outcomes

- Actual article: three semantic figures, six native reference links and all eight images loaded with nonzero natural width. Captions are `圖 1：模擬總功率`, the original NILMTK explanation/source link and the original occupancy explanation/source link. Banner and four meme images have no figure wrapper/caption/number.
- Temporary acceptance fixture: two numbered figures and two captioned tables plus an ordinary unnumbered table; table caption is the first child of its table. Source links and `<small>` references work. `<b>原文</b> {{ value }} @fig:literal` remains literal caption text; no caption `<b>` element executes.
- Eight layout cases: article/fixture × 1280/390px × light/dark. All captions computed at 17.5px, no clipped caption text and no document overflow. Measured base caption text contrast: 10.94:1 light, 12.81:1 dark. Measurements in evidence/browser-matrix.json. Theme switched using the actual desktop control before measuring each viewport; the mobile-hidden switch was not bypassed.
- Keyboard: focus first reference then Tab reaches another native reference with `:focus-visible`, solid 2px outline. Enter on article reference updates hash to `#fig-simulated-ems`; Enter on table reference updates hash to `#tbl-power`, with both targets present. Screenshots visually inspected for article/table mobile dark.
- Client navigation: from fixture's existing return link to article, a window probe survives navigation, confirming SPA transition. The article still has exactly three figures, six reference links and correct labels, without duplication.
- Built SSR HTML contains three figures/figcaptions and six reference links; authored reference markers absent from article main content. The temporary fixture was created after the first build and removed before final build; no fixture remains in source or built output.
- Browser error output empty after the final article interaction.

## Evidence locations and cleanup

Screenshots saved outside the repository in the task's local visualization directory: `caption-article-mobile-dark.png`, `caption-article-desktop-light.png`, `caption-table-mobile-dark.png`. They contain only the locally rendered task article/fixture. The browser fixture was removed after verification. The local article preview remains available for owner inspection; only local behavior is verified.
