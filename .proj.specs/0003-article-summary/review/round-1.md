# Round 1 — captured v1 planning review

Four independent read-only native agents; session model/effort inherited. Each reviewed exactly one repo axis across both separately evaluated epics with the frozen prompt. No product tests or deploy verification.

| Axis / reviewer | ArticleSummary P0/P1/P2 | PreviewNotice P0/P1/P2 |
|---|---|---|
| Completeness / /root/completeness | 0/1/0 | 0/0/0 |
| Verifiability / /root/verifiability | 1/0/0 | 1/0/0 |
| Contract conflict / /root/contract_conflict | 0/0/0 | 0/0/0 |
| Red team / /root/red_team | 0/1/0 | 0/0/0 |

## Findings and corrections

- C-S-01 P1 — v1/article-summary/spec.en.md:28, traceability.md:11, test-plan.md:6. Malformed/unclosed tag policy has no matrix/AC mapping. Add pinned unmodified compiler baseline comparison to S3, matrix and plan; retain normal diagnostics, no custom recovery. Do not promise successful rendering for invalid author syntax.
- V-S-01 P0 — v1/article-summary/spec.en.md:38,40; traceability.md:14,17; test-plan.md:7,8. Desktop width and legible print are underspecified. Set 1280px desktop, 360px mobile; A4 portrait/100% scale, no headers/footers, background graphics enabled; white summary backgrounds, ordinary text contrast ≥4.5:1, full content and no clipped text. Reflow between pages is allowed; keeping the entire summary on one page is not required.
- V-N-01 P0 — v1/preview-notice/spec.en.md:34, traceability.md:20. Readability/correct lack an oracle. Define 360px no notice-induced page horizontal overflow, complete text, contrast ≥4.5:1, role/name, SSR↔DOM text/visibility equality, and zero hydration mismatch warnings on initial load/navigation.
- RT-S-01 P1 — v1/article-summary/spec.en.md:27, test-plan.md:6. Nested lists/container lists can accidentally inherit card grid/icons/terminal prefixes. Add structural isolation case: only direct items of the canonical top-level list receive decoration; nested lists and container descendants retain normal layout/semantics.

No conflicting reviewer positions occurred; coordinator applied all smallest corrections. No majority adjudication. v2 supersedes v1 only after round-2 findings; v1 remains immutable.

## Contract evidence

Contract reviewer checked native theme enhanceApp registration, workflow real-surface requirement (docs/agents/workflow.md:117–125), baseline PreviewNotice props and flag contract (PreviewNotice.vue:5–6), ADR-0002 and ADR-0006. No P0/P1/P2 conflict found. true/main and trusted author Markdown are intended behaviors, not vulnerabilities. Local planning does not prove slot compilation, CSS behavior or deployment.
