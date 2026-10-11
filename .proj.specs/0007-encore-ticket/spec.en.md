# Reusable encore reading ticket

## Problem Statement

The electricity/privacy article currently presents its related reading as a plain paragraph. The owner selected prototype D, the screening-ticket design, and requested a reusable component applied at this exact location.

## Solution

Provide one native Vue component, `EncoreTicket`, globally available in VitePress Markdown. Use it for the existing related article without changing the surrounding prose, recommendation copy, destination, frontmatter, or assets.

## User Stories

1. As a reader, I want a recognizable related-reading ticket so I can open the recommended article from the current reading flow.
2. As an author, I want to supply a title, destination, and optional description in Markdown so I can reuse the same ticket in other articles.

## Implementation Decisions

- Public props: required `title: string` and `href: string`, optional `description: string`. All content is author-controlled plain text rendered through Vue interpolation. No HTML parsing, slots, automatic metadata lookup, package additions, or network requests.
- Keep the approved D structure: vertical 同場加映 stub, decorative ENCORE, dashed perforation, two small notches, 延伸閱讀 label, title, optional description, and 來看這一篇 action with a decorative right arrow.
- The entire ticket is one native anchor. The action is visual text within that anchor, never a nested button or anchor. Navigation stays in the current tab; use the supplied href without changing it. The current use is the existing site-root-relative internal article URL.
- Normal HTML attribute escaping and text escaping are provided by Vue. Props originate in trusted article source; this is not a sanitizer for untrusted remote URLs. No new public user input boundary is introduced.
- Use a component-local CSS module and existing VitePress color tokens. Follow the website's light/dark theme. Decorative ENCORE, arrow, and notch shapes are excluded from the accessible name. A visible focus indicator must surround the link without clipping.
- On narrow screens retain the vertical stub and reduce its width. Content wraps; no fixed component height. Hide the description element when omitted, without leaving an empty paragraph.
- Register through the existing theme application hook. The existing electricity article is the sole production consumer added in this scope. Provide one short author usage guide with examples of both description states.
- Preserve the working-tree article as observed at task entry, including its existing figure-caption edit. Replace only its exact 同場加映 paragraph. Other article bytes, image bytes, frontmatter, and public URLs remain unchanged.

## Acceptance Criteria

- E1: Mounting two tickets with different authored titles/destinations/descriptions produces two independent native anchors with the exact supplied destinations and escaped plain text; omission of description renders no description paragraph while retaining the title, action text and original href in one anchor. The author guide contains both description-present and description-omitted Markdown examples using these public props.
- E2: The actual compiled electricity article contains one registered ticket at the former recommendation paragraph, retains its title, description and destination verbatim, and retains the following section as a separate section.
- E3: In a real browser, the article ticket has the approved stub/perforation/notch/title/action structure in light and dark themes at 1280px and 390px viewport widths. At both widths the ticket stays inside the article content width, text is neither clipped nor horizontally overflowing; description omission is verified by the explicit component-mount assertions in E1.
- E4: Keyboard Tab can focus the ticket with a visible focus indicator; the accessibility tree exposes a single link containing the authored title. Decorative ENCORE and arrow are absent from its accessible name. Activating the link opens the original recommended article in the same browser tab.
- E5: Apart from the exact paragraph replacement, the task-entry article remains byte-identical. No existing images, frontmatter timestamps, other articles, dependencies, historical preservation records, or verifier rules change. The new component, registration, author guide, tests and tracker evidence are the only other additions/edits.
- E6: Existing unit suite, lint and VitePress build pass, plus applicable structural/materializer checks. Execute the preservation verifier and report its result without claiming it passes: separately record the reproducible task-entry caption failure and the additional, expected current-source hash/inventory rejection caused by this authorized component delta. Do not weaken or refresh immutable records to make this UI change pass. Verify E5 independently through an exact task-entry-to-final article substitution and explicit file inventory. No commit, push or deployment is requested by this task.

## Testing Decisions

Reuse Vue Test Utils/Vitest for the public component mount seam, and the existing VitePress compiler/build plus served article for integration. Test observable authored content, native link behavior, Markdown placement and real browser interaction. Do not test CSS class hashes or copy the implementation into expected values. Proposed seams and table are in `test-plan.md`; the owner approved the table and single-ticket breakdown on 2026-10-11. Tests and implementation wait until the spec review has zero P0 findings.

## Out of Scope

Other prototype variants; cover art; CMS integration; arbitrary HTML descriptions; external-link policy; historical guard changes; publication; commit; push; dependency installation; external tracker writes.

## Further Notes

Direction approval is the owner's current request selecting D and asking for a reusable component. The prototype is a visual reference, not production code. Stage 4 ticket-breakdown and stage 5 test-plan approval remain separate from that direction approval. Candidate permanent ticket: T-0007, one complete vertical slice with no blocking edge; it is not published until approved. Current base/HEAD: f93237b1ed538484f24ed103ef00c7e5ee2e1828. Worktree initially on staging; implementation will use the required ticket branch after approval.
