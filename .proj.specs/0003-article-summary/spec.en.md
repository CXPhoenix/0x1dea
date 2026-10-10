# Article summary — approved scope

## Problem Statement

Authors need three reusable summary appearances in 0x1DEA articles without maintaining duplicated wrappers or conflicting with VitePress custom containers. Readers need the same three author-owned takeaways in every appearance.

## Solution

Offer note (pale note with a thin border), cards (three decorative icons and one takeaway per card, stacked on mobile), and terminal (a dark terminal window with a title bar and three prompt rows). Use a PascalCase Vue component in Markdown and let VitePress compile the default slot. The author supplies content; the component does not generate summaries.

## User Stories

1. As an author, I want to use a reusable Markdown component so that summaries are consistent across articles.
2. As an author, I want to select note, cards or terminal so that all three agreed designs are available.
3. As an author, I want normal Markdown content so that links, emphasis and code keep their ordinary meaning.
4. As a reader, I want identical takeaway content and order across appearances so that styling does not change the claim.
5. As a mobile or keyboard reader, I want readable, accessible summaries so that decorative styling does not block reading or links.
6. As a reader printing an article, I want all summary text preserved so that the printout remains useful.
7. As a maintainer, I want default containers and following article text preserved so that this feature does not alter the Markdown parser contract.

## Implementation Decisions

User-approved decisions; the pinned renderer behavior must be verified by the approved test plan:

- Public component name ArticleSummary; optional string variant supports note/cards/terminal, omitted or invalid values resolve to note. Optional plain-text title defaults to TL;DR; empty or whitespace title falls back to TL;DR.
- For terminal, the plain-text title (TL;DR by default) is the static window title bar. Each direct item of the top-level takeaway list starts with one decorative $ prompt; wrapping lines, nested items and container descendants do not acquire another prompt. The window has no command input, execution, active window buttons or fake interactive controls. The prompt is absent from accessible text and copying authored takeaway text.
- Native default slot owns authored Markdown. The canonical three-takeaway form is one top-level unordered list with three items; each variant preserves its text, links and order. Decorative icons/prefixes convey no additional meaning and must not be announced as content.
- Paragraphs, lists, links, emphasis, inline code and fences remain readable slot content, including richer or noncanonical input. Do not discard, truncate, reparse, count or rewrite slot nodes to manufacture exactly three sentences. Cards style the top-level takeaway list; other blocks retain ordinary readable flow.
- Opening/closing component tags are block boundaries with blank lines around Markdown slot content. Document a verified authoring form; malformed/unclosed tags retain the compiler's normal error behavior rather than inventing recovery.
- Register through the existing theme extension; no custom container syntax, no markdown-it rule, no v-html or parsing of arbitrary input strings, no client-only wrapper. Plain-text props remain escaped; authored Markdown has the website's existing trusted-author compilation boundary, not a new untrusted-input sanitizer guarantee.
- Preserve SSR content and hydration consistency; use local styles that do not restyle built-in containers or unrelated article content. No dependency upgrade or new package is needed.

## Acceptance Criteria

- S1: A documented Markdown usage renders the same three takeaways with all note/cards/terminal appearances; terminal has a window frame and title bar with TL;DR (or the author title), and one decorative $ per top-level takeaway item, none on wrapped/nested lines, no extra announced or copied prompt, and no active command/window controls; note is the omitted/invalid variant fallback.
- S2: Paragraph, list, link, strong/emphasis, inline code and fence content retain semantics and content in every variant.
- S3: Closing tags keep subsequent sentinel text outside the component; neighboring and nested built-in info/tip/warning/details retain normal behavior; two summaries do not capture each other. Malformed/unclosed tag diagnostics and output match the unmodified pinned compiler baseline, without component-specific recovery. Only direct items of the canonical top-level list receive card/icon/terminal decoration; nested lists and container-contained lists retain their ordinary structure and layout.
- S4: Static built HTML contains authored text before hydration; initial load and client navigation have no hydration mismatch or unresolved component warning.
- S5: At 360px mobile width all takeaways are visible, cards stack vertically and ordinary text/links do not cause page overflow; long URLs/inline code wrap, fences may scroll inside their own region. At 1280px desktop width cards show three cards in one row.
- S6: Light/dark themes retain WCAG AA ordinary text contrast and visible links/focus; decorative icons do not change accessible names or reading order. An accessible note name uses the title and no active controls are added beyond authored links.
- S7: At A4 portrait, 100% scale, headers/footers disabled and background graphics enabled, print contains all authored summary text, white summary backgrounds and ordinary text contrast ≥4.5:1. No text is clipped; page-to-page reflow is allowed.
- S8: No new arbitrary string-to-HTML path, parser override or article-copy generation is introduced; only the approved demonstration article is integrated and unrelated prose/assets/URLs/frontmatter remain unchanged.

## Testing Decisions

Primary proposed seam: the existing VitePress build and served generated article (SSR HTML plus browser hydration, navigation, keyboard and layout). Add a fixture using the installed pinned VitePress 2.0.0-alpha.16, not a different Markdown renderer. Existing Vue Test Utils/Vitest seam complements variant fallback, title escaping and slot preservation; mounted HTML alone does not prove Markdown compilation. The accompanying test plan and seams were approved by the user before this implementation. Current unapproved prototype tests are prior observations, not accepted test evidence.

## Out of Scope

Automated summary generation, new containers, markdown-it changes, migration of all articles, dependencies, article fact editing, banner work, production publication, public issues or Notion updates.

## Further Notes

This is a new epic, independent of notice functionality. One complete implementation ticket is sufficient for the small component, shared native-slot contract and three CSS appearances; avoid extra dependencies solely to split appearances. If pinned compilation exposes materially different structures or scope exceeds one fresh context, revise to note first then independent cards and terminal tickets, each blocked only by the shared completed contract. Such a split requires approval.

Official guidance supports Vue components in Markdown, PascalCase block names and existing theme registration: https://vitepress.dev/guide/using-vue . Current docs describe alpha.20; installed alpha.16 build remains authoritative. Default containers: https://vitepress.dev/guide/markdown . These sources support the direction, not proof of this specific slot authoring form.
