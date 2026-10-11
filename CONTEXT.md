# Product context

0x1DEA is an existing VitePress knowledge website with a local TypeScript post helper.
The website lives in `blog/`; management documentation lives in `docs/`. Public URLs,
article bytes, image bytes, frontmatter times and existing behavior are preserved.

The executable tracker is local Markdown under `.proj.specs/` and `.proj.tickets/`.
Notion DAILY9 is a parent-managed external index. `openspec/`, `.spectra.yaml` and the
four archives are immutable historical evidence. Their old Harness reviews, TDD and
landing records are not recreated.

Runtime framework skills are pinned initialized template copies. Product writing
has one canonical source and deterministic complete physical packages. Editing a
generated file creates drift and is rejected by the materializer's `--check`.

Resolve the actual branch and commit with `git branch --show-current` and
`git rev-parse HEAD`; historical context is not a live Git status. Ticket landing
requires its actual owner authorization receipt and commit containment in the
configured `staging` target (ADR-0006). A local merge or cached remote ref alone
cannot establish authorization or deployment. Current test entrypoints are
`pnpm test` (Vitest plus both Python suites) and `pnpm test:python`.

Read [AGENTS.md](AGENTS.md), [the adoption spec](.proj.specs/0001-harness-adoption/spec.en.md)
and [approved receipts](maintenance/harness-adoption/APPROVALS.md) before relying on gates.
