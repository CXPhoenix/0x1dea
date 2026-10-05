# theme-layout-particles Specification

## Purpose

Locks down the custom VitePress theme that wraps the default layout: the theme entry at `docs/.vitepress/theme/index.ts` (which globally registers `PostCard`/`PostBlock`/`PostList`/`NewPost` and SSR-conditionally loads `@tsparticles/vue3`), the custom `Layout.vue` (which injects a particles canvas into the `#layout-top` slot when `frontmatter.layout === 'home'` OR `frontmatter.showParticle` is truthy), the `Particles.vue` component (which adapts color to `isDark` and remounts on theme toggle via `:key`), and the `config.mts` `transformPageData` hook that applies five frontmatter defaults (`sidebar:false`, `aside:false`, `footer:true`, `showParticle:true`, `next:false`) to every `index.md` under a subdirectory of `docs/`. Future changes to the layout slot, the particle gating logic, or the subdirectory `index.md` defaults SHALL propose a delta against this capability.

## Requirements

### Requirement: Custom theme SHALL register Layout.vue and globally register four post components

The theme entry at `docs/.vitepress/theme/index.ts` SHALL export a `Theme` object that:

1. Extends `DefaultTheme` from `vitepress/theme`.
2. Sets `Layout` to the custom `Layout.vue` so every page renders inside the custom layout instead of the default VitePress layout.
3. In `enhanceApp`, calls `app.component(...)` exactly once for each of `PostCard`, `PostBlock`, `PostList`, and `NewPost`, registering each under its component name.
4. Loads `@tsparticles/vue3` and the `loadSlim` engine asynchronously and only when `import.meta.env.SSR` is `false`, so the tsparticles bundle is not pulled into the SSR build.

#### Scenario: Markdown pages can use any of the four post components without imports

- **WHEN** a markdown page references `<PostCard />`, `<PostBlock />`, `<PostList />`, or `<NewPost />`
- **THEN** the component renders without the page declaring any explicit `import` statement
- **AND** no "failed to resolve component" warning is emitted

#### Scenario: SSR pass does not execute tsparticles imports

- **WHEN** the site is rendered server-side during `vitepress build`
- **THEN** the `await import('@tsparticles/vue3')` and `await import('@tsparticles/slim')` calls inside `enhanceApp` do NOT execute, because the surrounding `if (!import.meta.env.SSR)` guard short-circuits during SSR
- **AND** the client-side bundle invokes both dynamic imports only after `import.meta.env.SSR` evaluates to `false`

---
### Requirement: Layout.vue SHALL inject the particles canvas via the layout-top slot when showParticleBg is truthy

`Layout.vue` SHALL extend `DefaultTheme.Layout` (imported as `const { Layout } = DefaultTheme`) and SHALL render content inside the `#layout-top` slot. The slot content SHALL be a wrapper `<div>` with classes `visual-effects-container fixed inset-0 z-0 pointer-events-none`. Inside that wrapper, `<Particles />` SHALL be rendered conditionally with `v-if="showParticleBg"`.

The `showParticleBg` value SHALL be a `computed` derived from `useData().frontmatter` such that:

```
showParticleBg = frontmatter.value.layout === 'home' || frontmatter.value.showParticle
```

The expression is **not** wrapped in `Boolean(...)`. The computed therefore returns whatever `frontmatter.value.showParticle` happens to be when `layout !== 'home'` — which can be a boolean, a string, a number, or `undefined`. The truthy / falsy decision is performed by Vue's `v-if` at render time. Authors and tooling SHALL declare `showParticle` as a YAML boolean (`true` / `false`); using a quoted string like `showParticle: "false"` is **truthy** and would unintentionally enable particles. When `showParticleBg` is falsy, `<Particles />` SHALL NOT be rendered, but the wrapper `<div>` SHALL still exist as an empty pointer-event-none overlay.

#### Scenario: Home page renders particles via layout=home

- **WHEN** a page declares `layout: home` in its frontmatter
- **THEN** `<Particles />` is rendered inside the `#layout-top` slot
- **AND** the surrounding wrapper `<div>` has classes `visual-effects-container`, `fixed`, `inset-0`, `z-0`, and `pointer-events-none`

#### Scenario: Page opts in via showParticle frontmatter

- **WHEN** a non-home page declares `showParticle: true` in its frontmatter
- **THEN** `<Particles />` is rendered

#### Scenario: Regular post does not render particles by default

- **WHEN** a post under `docs/post/**/*.md` does not declare `layout: home` and does not declare `showParticle`
- **THEN** `<Particles />` is NOT rendered

#### Scenario: Page can suppress particles by overriding showParticle

- **WHEN** a subdirectory `index.md` declares `showParticle: false` (overriding the default applied by `transformPageData`)
- **THEN** `<Particles />` is NOT rendered

##### Example: showParticleBg outcomes for representative pages

| Page                                          | `frontmatter.layout` | `frontmatter.showParticle` | `showParticleBg` |
| --------------------------------------------- | -------------------- | --------------------------- | ----------------- |
| `docs/index.md`                               | `home`               | (omitted)                   | `true`            |
| `docs/posts.md`                               | (omitted)            | `true`                      | `true`            |
| `docs/post/course/cybersec/index.md`          | (omitted)            | `true` (defaulted)          | `true`            |
| `docs/post/course/cybersec/what-is-safety.md` | (omitted)            | (omitted)                   | `false`           |
| arbitrary page                                | (omitted)            | `false`                     | `false`           |

---
### Requirement: Particles.vue SHALL adapt color to isDark and remount when the theme toggles

The `Particles.vue` component SHALL:

1. Read `isDark` via VitePress's `useData()` hook.
2. Compute `color` and `linksColor` as `'#ffffff'` when `isDark.value` is `true` and `'#000000'` when `isDark.value` is `false`.
3. Render the underlying `<vue-particles>` element with a Vue `:key` bound to `isDark ? 'dark' : 'light'` (template syntax — Vue auto-unwraps the `isDark` ref inside the template) so the particles engine remounts (rather than mutating in place) when the user toggles the site theme.
4. Wrap the `<vue-particles>` element inside `<ClientOnly>` so the SSR pass renders no `<canvas>` element and the engine initializes only on the client.

The component SHALL apply the classes `fixed inset-0 z-0 pointer-events-none opacity-60` so the particle layer is full-screen, behind interactive content, and visually subtle.

#### Scenario: Light mode uses black particles

- **WHEN** `isDark` is `false`
- **THEN** the rendered `options.particles.color.value` is `'#000000'`
- **AND** the rendered `options.particles.links.color` is `'#000000'`

#### Scenario: Dark mode uses white particles

- **WHEN** `isDark` is `true`
- **THEN** the rendered `options.particles.color.value` is `'#ffffff'`
- **AND** the rendered `options.particles.links.color` is `'#ffffff'`

#### Scenario: Theme toggle remounts the particles engine

- **WHEN** the user toggles the VitePress theme from light to dark
- **THEN** the `<vue-particles>` element's Vue `key` changes from `'light'` to `'dark'`
- **AND** the underlying particles engine reinitializes (rather than re-rendering the same instance)

#### Scenario: SSR pass renders no canvas

- **WHEN** the page is rendered server-side
- **THEN** the rendered HTML does NOT contain a `<canvas id="tsparticles">` element
- **AND** the rendered HTML contains no markup produced by `vue-particles` at all (the `<ClientOnly>` boundary suppresses the slot content during SSR; Vue does not emit a literal `<ClientOnly>` tag — it renders nothing for that subtree)

---
### Requirement: config.mts transformPageData SHALL set five frontmatter defaults for subdirectory index.md pages

The `transformPageData` hook in `docs/.vitepress/config.mts` SHALL apply defaults to every page where `pageData.relativePath.endsWith('index.md')` AND `pageData.relativePath !== 'index.md'`. The intent is "every `index.md` under a subdirectory of `docs/`, excluding the root homepage" — but the literal `endsWith('index.md')` check would also match a hypothetical filename like `myindex.md` (no leading slash) **anywhere under `docs/`** (the hook is not scoped to `docs/post/`). Authors SHALL NOT create files anywhere under `docs/` whose `relativePath` ends in the substring `index.md` but whose basename is not exactly `index.md` (e.g., `docs/notes/myindex.md`, `docs/post/foo-index.md`); such files would silently inherit the five defaults below despite not being category landing pages.

The defaults MUST be applied via the nullish-coalescing assignment operator `??=`. `??=` triggers (i.e., assigns the default) when the left-hand side is `undefined` **or `null`**. Therefore an explicit frontmatter declaration of `null` (e.g., `sidebar: ~` or `sidebar: null` in YAML) does NOT override the default — the default is still applied. Only non-null, non-undefined frontmatter values override the defaults. The five defaults SHALL be:

| Frontmatter key | Default value | Rationale                                     |
| --------------- | ------------- | --------------------------------------------- |
| `sidebar`       | `false`       | Category index pages render without sidebar  |
| `aside`         | `false`       | Category index pages render without aside    |
| `footer`        | `true`        | Category index pages keep the site footer    |
| `showParticle`  | `true`        | Category index pages opt in to particles     |
| `next`          | `false`       | Category index pages hide the "next" link    |

The hook MUST NOT touch `docs/index.md` (the root homepage) or any non-index page.

#### Scenario: Subdirectory index.md inherits all five defaults

- **WHEN** `docs/post/course/cybersec/index.md` declares only `title`, `isIndex`, and `category` in its frontmatter
- **THEN** after `transformPageData` runs, the page's resolved frontmatter has `sidebar: false`, `aside: false`, `footer: true`, `showParticle: true`, and `next: false`

#### Scenario: Explicit non-null frontmatter overrides each default

- **WHEN** `docs/post/course/cybersec/index.md` declares `sidebar: true` in its frontmatter
- **THEN** after `transformPageData` runs, `sidebar` is `true` (the explicit value wins)
- **AND** the other four defaults are still applied because their keys were not declared

#### Scenario: Explicit YAML null does NOT override the default

- **WHEN** `docs/post/course/cybersec/index.md` declares `showParticle: null` (or equivalently `showParticle: ~`) in its frontmatter
- **THEN** after `transformPageData` runs, `showParticle` is `true` (the default is applied because `??=` triggers on `null` exactly like on `undefined`)
- **AND** any author who wants to suppress particles SHALL declare `showParticle: false` (a non-null falsy value), not `null`

#### Scenario: Non-index basename ending in "index.md" is silently caught by the hook

- **WHEN** a hypothetical file at `docs/notes/myindex.md` is processed
- **THEN** because `'notes/myindex.md'.endsWith('index.md')` is `true` and `'notes/myindex.md' !== 'index.md'`, the hook applies all five defaults
- **AND** authors SHALL NOT create such filenames; only the exact basename `index.md` is supported as a category landing page

#### Scenario: Root index.md is not touched

- **WHEN** `docs/index.md` is processed
- **THEN** `transformPageData` does NOT inject any of the five defaults
- **AND** the homepage's frontmatter is observed exactly as authored

#### Scenario: Regular post is not touched

- **WHEN** `docs/post/course/cybersec/what-is-safety.md` is processed
- **THEN** `transformPageData` does NOT inject any defaults
- **AND** the post's frontmatter is observed exactly as authored

##### Example: hook outcomes for representative pages

| `relativePath`                                 | Defaults applied? |
| ---------------------------------------------- | ----------------- |
| `index.md`                                     | no (root homepage) |
| `post/course/cybersec/index.md`                | yes                |
| `post/course/rm/index.md`                      | yes                |
| `post/course/cybersec/what-is-safety.md`       | no (not index.md)  |
| `posts.md`                                     | no (not index.md)  |
