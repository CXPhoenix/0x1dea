# Collaboration guide

Open Claude Code or Codex in this checkout and continue from the current spec,
ticket and evidence. 0x1DEA is an existing VitePress knowledge platform with an
approved [Project Charter](../AGENTS.md#project-charter). This adoption follows the
reviewed spec and approved test matrix; it does not create a walking skeleton.
The website lives in `blog/`; `docs/` contains project management instructions.

## Start a work session

Give the assistant the intended outcome and relevant spec or ticket paths.
[AGENTS.md](../AGENTS.md) defines the product scope and shared rules;
[workflow.md](agents/workflow.md) defines the delivery stages and gates.

| Action | Claude Code | Codex |
| --- | --- | --- |
| Converge a new requirement or Charter change | `/grill-with-docs` | `$grill-with-docs` |
| Inspect skills | `/skills` | `/skills` |
| Review a change | `/code-review` | `$code-review` |
| Save a handoff | `/handoff` | `$handoff` |

Codex project settings apply only after the owner trusts the checkout in their
own environment. Accounts, API keys and trust settings stay local. Use a fresh
session to check native discovery after an authorized skill update, so the check
reflects the current files. This adoption does not authorize account, trust or
credential changes.

## Find a skill

Each runtime has 35 physical skill packages: 32 imported framework skills and the
three product writing skills `phoenix-writing`, `maintaining-writing-skills` and
`creating-vitepress-post`. The template-only `init-template` is absent.

| Work | Skills |
| --- | --- |
| Environment and tool setup | `setup-matt-pocock-skills`, `wizard` |
| Requirements and decisions | `grilling`, `grill-me`, `grill-with-docs`, `wayfinder`, `to-questionnaire` |
| Specs and implementation | `to-spec`, `to-tickets`, `implement`, `tdd`, `prototype` |
| Architecture and diagnosis | `codebase-design`, `domain-modeling`, `diagnosing-bugs`, `improve-codebase-architecture`, `archify` |
| Review and verification | `code-review`, `security-review`, `agent-browser`, `evidence-report` |
| Git prose and collaboration | `tw-emoji-commit`, `tw-emoji-pr-note`, `tw-emoji-release-note`, `resolving-merge-conflicts`, `handoff` |
| Research and knowledge transfer | `research`, `teach`, `writing-for-agents`, `wait-what`, `i-have-adhd` |
| Product writing and scaffolding | `phoenix-writing`, `maintaining-writing-skills`, `creating-vitepress-post` |

Use the configured `.proj.specs/` and `.proj.tickets/` tracker. Only use
`setup-matt-pocock-skills` to change an explicitly requested tracker configuration;
do not restore the upstream `.scratch/` example. Skills with a manual invocation
policy, including `i-have-adhd`, require an explicit call. `tune-skills` remains a
manual framework skill for separately authorized maintenance; do not run it as
an adoption step or tune the three product writing skills.

Claude Code also has a native `/security-review`. To select this project's copy,
explicitly request `.claude/skills/security-review/SKILL.md`; Codex selects its
project copy with `$security-review`.

## Share work between runtimes

`AGENTS.md` is shared; `CLAUDE.md` imports it. Claude Code loads `.claude/skills/`
and Codex loads `.agents/skills/`. Each runtime has reviewer and researcher roles. Codex roles omit a model override
and inherit the current session. The Claude reviewer explicitly selects
`claude-opus-5-5`; the Claude researcher uses `inherit`. These are the pinned
project role settings. See [runtime.md](agents/runtime.md) for the ownership,
invocation and handoff contract.

Before switching tools, use `handoff` to record the objective, spec and ticket
paths, branch and HEAD, uncommitted changes, verification results and next action.
Handoffs live in the ignored `.proj.handoffs/` directory and state their expiration
in frontmatter. The recipient checks expiration and Git status before continuing.
Keep one writer per ticket; use separate worktrees for parallel implementation.

## Maintain skills

The 32 framework skills have independent runtime copies. An authorized future
framework change can edit the corresponding `.claude/skills/` or `.agents/skills/`
copy; behavior that applies to both runtimes must be deliberately ported and
verified in each. During this adoption, the approved framework import stays pinned.

The three product writing packages are generated from the canonical trees under
`skills/`. Edit those canonical sources once using the approved source and alias
policy; do not edit their generated runtime copies. Then run, in order:

```bash
python3 scripts/materialize-writing-skills.py --write
python3 scripts/materialize-writing-skills.py --check
python3 scripts/verify-project.py
```

Materialization validates its pinned inputs and builds physical packages for both
runtimes. `--check` verifies deterministic bytes without replacing those packages.
The structure check verifies runtime metadata and matching invocation policies.
Source-policy updates require review against the approved adoption scope.

## Verify the result

Python structure checks require Python 3.11+:

```bash
python3 scripts/verify-project.py
python3 scripts/materialize-writing-skills.py --check
python3 scripts/verify-harness-adoption.py
```

These checks cover collaboration structure, generated packages, pinned provenance,
tracker state and historical traceability. Product scripts already exist in
`package.json`: `pnpm test:unit`, `pnpm docs:build` and `pnpm new:post`. Follow the
approved test matrix for native discovery, CLI, writing, browser and rollback
verification, and distinguish inherited failures from new regressions.

Use `agent-browser` or an available host browser tool for browser-reachable
behavior; native applications, CLIs and daemons need a harness for their actual
surface. Report which surface ran. GitHub or GitLab access, MCP connections and
service logins require separate authorization when needed.

Every authorized commit, including amend, uses `tw-emoji-commit`; PR and release
prose use the corresponding `tw-emoji-*` skill. Stop that action if its required
skill is unavailable. This adoption authorizes local editing and review only;
landing on the configured `staging` target requires explicit authorization.

Windows Archify automatic opening remains disabled, including `deliver --open`
and `preview`. Open artifacts or preview URLs manually; see
[the disabled scope and checks](security/windows-opener.md).
