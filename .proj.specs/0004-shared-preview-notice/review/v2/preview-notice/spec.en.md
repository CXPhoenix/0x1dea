# Shared preview notice — draft, not approved

## Problem Statement

The homepage has an environment-controlled preview notice, but the baseline article's handwritten staging message ignores that control. Authors need content-owned copy and readers on the production site must not receive a staging message under the supported production configuration. The historical implementation lacks a corresponding local spec/ticket record found in this inspection.

## Solution

Document the existing homepage behavior retrospectively with its actual commit and evidence, then apply the same reusable PreviewNotice to the selected article and verify both surfaces through preview and production builds. Do not claim that specification preceded the existing implementation.

## User Stories

1. As an author, I want title and text owned by each Markdown page so that wording does not require an environment change.
2. As a maintainer, I want one environment flag shared by homepage and article so that preview-only wording is hidden consistently.
3. As a production reader, I want staging wording hidden under the verified production configuration so that the site does not misrepresent publication status.
4. As a preview reader, I want a visible, accessible note so that I understand the article's review status.
5. As a maintainer, I want an honest retrospective record so that the tracker does not fabricate historical gates or approvals.

## Implementation Decisions

- Retain the existing pure-text title/text props, trimmed outer whitespace, internal newlines, omitted empty fields and whole-note suppression when both are blank. Title provides the accessible note name; text-only uses the existing preview-note fallback name. No Markdown or HTML parsing for props.
- Retain VITE_SITE_NOTICE_ENABLED as the sole explicit build-time visibility switch. Exact string true enables; every other supplied value (false, empty, whitespace, TRUE, 1, padded true) disables. When absent, exact CF_PAGES_BRANCH=staging enables, and all other or absent branch values disable. CF branch metadata is the existing fallback, not a second new switch.
- Retain root environment loading and tracked public example. Never read or copy environment secrets. The user requested a local .env on macOS. The existing local .env and variants are ignored, and the public example remains tracked; no new environment source or ignore requirement is needed.
- Replace only the selected article's manual staging block with shared notice props. Preserve surrounding article bytes, metadata and URL except the specifically approved notice replacement. No automatic removal of other article containers.
- Existing true has priority even for main. Preserve that contract for minimum change: enforce and verify explicit false in the production build/deployment configuration; preview can use true or absent flag plus staging branch. Do not add a branch guard: true/main is valid under the existing explicit env-switch contract.
- Changes require a restart/rebuild. Vite production mode is not a preview-vs-production discriminator: both deployment types can use production builds. Do not change deployment configuration in this planning task.

## Acceptance Criteria

- N1: Both homepage and selected article show their own supplied title/text when enabled, preserve escaped text/newlines, omit empty fields, and emit no note when both fields are blank.
- N2: The exact flag/branch truth table in traceability holds for both SSR and browser hydration, including true/main intentionally enabled under the preserved contract.
- N3: Preview build with true or absent flag/staging shows both notices. Supported production build with false/main, and clean absent/main or absent/absent builds, show neither notice in generated HTML or browser DOM; surrounding article text remains.
- N4: Production release evidence records resolved false and the served artifact result; missing or contaminated build evidence blocks publication. A true/main build is a valid diagnostic of the override contract, but is not the supported Production acceptance configuration.
- N5: Pure-text hostile strings cannot create executable elements; the note has role=note and the specified title/fallback accessible name. At 360px mobile width all notice text is visible without notice-induced page horizontal overflow. Ordinary notice text contrast is ≥4.5:1 in light/dark themes. Surrounding links remain keyboard-focusable; SSR HTML and hydrated DOM have identical notice text and visibility, with zero hydration mismatch warnings on initial load and client navigation.
- N6: Public example is trackable and local .env variants are ignored without storing secrets. No new visibility env or parser is introduced.
- N7: The history record distinguishes homepage commit f981af27b4992a938ac9f0065b57b857083e8737, baseline article manual block, and unlanded article integration. It records actual future gate/landing dates only when they occur; retrospective documentation is not proof of original compliance.

## Testing Decisions

Reuse the existing Vue Test Utils/Vitest PreviewNotice seam for flag/props (the existing suite includes 22 cases). Proposed material expansion is actual VitePress build→SSR HTML→served browser, covering homepage and article as consumers and a clean environment matrix. Use isolated output directories and publicly specified env strings; never mutate another worker's build or run install. Authoritative deployment verification remains separate from local build verification. No retrospective red/green evidence is invented for existing code.

## Out of Scope

Global article migration, changing article facts or publication state, new parser/API, Notion updates, public issues, rewriting old approvals, changing Cloudflare accounts/settings or pushing main/staging during this draft task.

## Further Notes

Create an explicitly retrospective record for existing behavior and one prospective ticket for article sharing plus real environment/surface verification. No fake completed ticket is necessary for the historical homepage feature. The supplied Notion #16 is an external index, not the local ticket identifier. Notice and summary are separate epics with no technical blocking edge.

Public build-time env behavior: https://vite.dev/guide/env-and-mode . Existing root environment configuration and branch define must be evaluated on the pinned local toolchain. Do not infer deployment safety from unit stubs alone.
