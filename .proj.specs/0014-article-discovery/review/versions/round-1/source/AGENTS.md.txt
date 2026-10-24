# Agent instructions

Shared project instructions for the coding assistants Claude Code and Codex. Use the
shared contract and active-runtime section of [docs/agents/runtime.md](docs/agents/runtime.md)
when invoking skills, delegating, or configuring tools; use its handoff section when
writing or resuming from a handoff. Reuse context already read unless it changed. Each runtime owns its project
skills: Claude Code `.claude/skills/`, Codex `.agents/skills/`. Same-named skills may differ,
tuned to each vendor's prompting guidance; resolve helpers relative to the loaded skill.
Claude Code imports this file through `CLAUDE.md`; keep project rules here.

Skill names below use Claude's `/name` notation. In Codex explicitly use `$name`
or select it in `/skills`; an upstream instruction to call the Skill tool means
load and follow the named project SKILL.md using the active host's supported mechanism.

## Template maintenance

When the user asks to inspect or improve this template, keep the project tokens and
Charter placeholder intact and perform that maintenance. The product gates below
apply when adopting the template for a product; they do not force template maintainers
to invent a product or initialize the source template. Existing user authorization
and approved choices carry forward; ask only for a decision not already settled.
While `.tmpl.docs/` exists, read its README for template maintenance and save template
plans, research and change history there. Keep adopted project rules in `docs/`.

## Project Charter

**0x1DEA** — A personal knowledge platform for cybersecurity teaching, software engineering, and AI exploration.

0x1DEA serves learners and technical readers through its existing VitePress website,
curated article navigation, post views and local article-creation CLI. Preserve published
URLs, article bytes, times, images and explicitly requested Phoenix writing voice.
The owner approved local Harness adoption at 2026-10-04T07:24:41Z and the complete
website `docs/` → `blog/` move plus exactly two canonical alias-input exceptions at
2026-10-04T10:30:04Z. Receipts and boundaries are in
[APPROVALS.md](maintenance/harness-adoption/APPROVALS.md).

This is an existing product. The walking-skeleton exemption does not apply. Current
work follows the reviewed adoption spec, one globally allocated ticket and the approved
test matrix. Local implementation and independent review are complete. At 2026-10-04T11:53:10Z
the owner explicitly authorized commit and non-force push to GitHub `staging` for
inspection. This authorizes the reviewed migration and necessary public evidence;
it does not authorize main, PR, merge, separate deploy, Cloudflare, Notion,
installations, account/trust/credential changes or global skills. Keep original
checkouts untouched; publication uses the isolated clone. See APPROVALS.md.

## Delivery model

Work ships as **epics**. One epic = one spec = one pass through the pipeline = one demoable
increment. Finish an epic, then return to stage 1 for the next one.

Round 0 is the **walking skeleton**: the thinnest path that runs end to end, built so that real
**seams** exist. It carries no spec and no adversarial review, because both take seams as input and
a new repository has none yet. That exemption expires the moment the skeleton merges to `main`;
every ticket after that has a spec behind it.
See [ADR-0001](docs/adr/0001-walking-skeleton-then-epic-loop.md).

## Pipeline

| # | Stage | Skill | Gate before moving on |
|---|---|---|---|
| 1 | Converge the requirement | `/grill-with-docs` | user confirms shared understanding |
| 2 | Write the spec | `/to-spec` | spec **and** traceability matrix exist |
| 3 | Adversarial review | 4 subagents, ≤2 rounds | zero P0 findings |
| 4 | Break into tickets | `/to-tickets` | user approves the breakdown |
| 5 | Implement | `/implement` + `/tdd` | test plan table approved, then red → green |
| 6 | Review the change | `/code-review` | direction and requirement confirmed |
| 7 | Security review | `/security-review` | findings triaged and resolved |
| 8 | End-to-end | see workflow doc | behaviour verified against the real surface |
| 9 | Land it | PR, or `--no-ff` merge with no remote | authorized landing on configured `staging` target |

Stage detail, gates, exceptions, and the epic close-out: **[docs/agents/workflow.md](docs/agents/workflow.md)**.

**[docs/agents/issue-tracker.md](docs/agents/issue-tracker.md) is the tracker configuration** —
read it before `/to-spec` or `/to-tickets` writes a file. Its paths and statuses override
upstream examples; use the existing configuration without asking to set it up again.

## Hard rules

1. **One branch per ticket:** `tickets/<ticket-id>/<ticket-slug>` (e.g. `tickets/T-0007/session-store`).
   Ticket ids are global, sequential, and permanent — branch names depend on them never changing.
2. **Two tables gate a ticket's tests.** A **test plan table** before the first test is written, which
   the user approves; a **coverage report table** when the ticket closes. Between them, `/tdd` governs
   the loop: one seam, one test, one minimal implementation per cycle.
3. **Adversarial review runs a frozen prompt.** Round 2 replays round 1's prompt verbatim; only the
   spec version changes. Two rounds is the ceiling. P0 findings surviving round 2 mean the epic is
   too large: split it and restart at stage 1.
4. **Verify against the surface that actually runs the behaviour.** `/agent-browser` drives
   Chrome/Chromium and Electron over CDP, so it verifies browser-reachable surfaces only. Any other
   surface — a native client, a daemon, a CLI, a game server — needs a harness this project supplies.
   State which surface a verification covers whenever you report one.
5. **Skills own their output.** Every `git commit` invocation (including amend) must use `/tw-emoji-commit`, PR descriptions use
   `/tw-emoji-pr-note`, release notes use `/tw-emoji-release-note`. Load the project copy even if a global skill has the same name. Generate and sanitize
   the message with that skill, then use a UTF-8 message file for Git. If one is
   unavailable, stop the affected action and report; do not write a fallback message.

## Language

All Chinese output uses Taiwan Traditional Chinese, including conversation, documents,
comments and Git messages. Keep customary English technical terms (commit, PR, API,
cache, log, debug). Correct inconsistent source wording before presenting it.
Document language and bilingual sync rules: [docs/agents/language.md](docs/agents/language.md).

## Repository layout

```
.proj.specs/
  OPEN-QUESTIONS.md               deferred architecture-level decisions
  NNNN-<epic-slug>/
    spec.en.md                    source of truth
    spec.zh-TW.md                 audit translation for the user
    traceability.md               {type x field x boundary} -> acceptance criteria
    review/prompt.md              the frozen adversarial-review prompt
    review/round-N.md             findings, graded P0 / P1 / P2
    reports/*.html                standalone evidence reports
  _reports/*.html                 project-level reports
.proj.handoffs/                   session handoffs; local only, gitignored
.proj.tickets/
  NNNN-<epic-slug>/
    T-NNNN-<slug>.md              status lives in frontmatter, not in the path
docs/adr/                         architecture decisions
docs/agents/                      the docs this file points at
```

Both `.proj.specs/` and `.proj.tickets/` are committed: they are the evidence chain behind every
review and every deferral. `.proj.handoffs/` is not: a handoff expires, so it stays out of history.

## Build and test commands

Portable structure check: `python3 scripts/verify-project.py` (Python 3.11+).
Only while `tests/test_init_project.py` exists, also run
`python3 -m unittest discover -s tests -v` for template maintenance. Initialization
removes that template-only test; a product establishes its own test commands.
These checks verify template plumbing, not product behavior.

Product commands are in `package.json`: `pnpm test:unit`, `pnpm docs:build`,
`pnpm new:post`. The website root is `blog/`; `docs/` is management only.
Use existing Node 24.13.0 and pnpm 10.28.0 for the adoption evidence. Do not install.
Run `python3 scripts/materialize-writing-skills.py --check` and
`python3 scripts/verify-harness-adoption.py` for generated packages and local history/tracker.
These checks complement actual native discovery, CLI, writing, browser and rollback runs.

## Reference

- **[docs/agents/workflow.md](docs/agents/workflow.md)** — the nine stages in full: entry conditions, gates, the walking-skeleton exemption, epic close-out, branching and landing.
- **[docs/agents/issue-tracker.md](docs/agents/issue-tracker.md)** — where specs and tickets live, ticket frontmatter, the six status views, how blocking is derived.
- **[docs/agents/review.md](docs/agents/review.md)** — the four adversarial-review axes, P0/P1/P2 grading, and the two-stage security review.
- **[docs/agents/language.md](docs/agents/language.md)** — which documents are English, which are Traditional Chinese, and how the bilingual spec stays in sync.
- **[docs/agents/domain.md](docs/agents/domain.md)** — how to consume `CONTEXT.md` and ADRs while exploring.

## Product writing exception and routing

Only the three canonical trees `skills/phoenix-writing`, `skills/maintaining-writing-skills`
and `skills/creating-vitepress-post`, their generated physical runtime counterparts and
referenced writing material retain validated Taiwan Traditional Chinese v2.2 prose.
Their canonical sources are edited once; the materializer builds both runtimes.
All other new management and framework instructions remain English. Do not tune these
three skills or run a tuning workflow as an adoption step. Provenance is in
[runtime.md](docs/agents/runtime.md) and [language.md](docs/agents/language.md).

- Explicit Phoenix voice or continuing that work: load the active runtime's `phoenix-writing`.
- Creating a new site article file: load `creating-vitepress-post`; chat drafts and revisions do not scaffold.
- Writing-skill, article or instruction maintenance: load `maintaining-writing-skills`.
- New requirements, tickets and progress use only `.proj.specs/` and `.proj.tickets/`.
  `openspec/` and retired Spectra instructions are read-only historical evidence.

Notion DAILY9 is an index managed by the parent; local files are the executable tracker.
No local action implies authority to update that external index.

## Local article publication preparation

For combined article preview or selected publication preparation, load the active
runtime's `managing-article-publication`. Its English canonical source is the fourth
materialized product package; the Chinese exception above remains three trees.
Phase 1 reconstructs and verifies local candidates only. Actual publication and
rollback require separate authorization; public preview is not confidential storage.
