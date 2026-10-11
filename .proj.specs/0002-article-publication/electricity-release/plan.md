# Electricity article publication candidate

The owner approved publishing the electricity article and requested modifications followed by a PR to main, exclusively for this article. This authorizes a dedicated non-force branch push and PR creation; no merge or deployment is performed here.

This is execution of the approved AP-01–AP-09 publication contract, not a new product feature. The original specs and test plans remain unchanged. The selected production article preserves the staging body, image alternative text, figure captions, timestamps and references. Only draft/previewOnly frontmatter and the staging PreviewNotice are removed. The category landing is a static selected-article index, avoiding an unnecessary new executable Markdown input.

Pinned main: `e457143e8be2f7d54f69bc3e9b80230375be49de`.
Selected editorial source: staging `4005ee45f2f3267a8b53ce24fa97af7b49cfb144`, used only as a byte source for manual extraction, never as release ancestry.
Branch: `tickets/T-0002/electricity-publication`, based directly on pinned main.

## Ownership

- Selected content: the electricity article, its category index, twelve article-owned current/legacy images and exact old-preview redirects.
- Shared dependencies: unchanged ArticleSummary, EncoreTicket, caption parser and their tests/guides; minimal main-relative registration/configuration and article/caption styles.
- Excluded: all five local-preview articles and assets, homepage preview notice, PreviewNotice feature, other writing-skill changes, T-0009 tooling and staging history.
- Management: this release record and its exact scope/evidence; no unrelated ticket status changes.

## Verification mapping

Reuse the approved AP test table and existing summary/EncoreTicket/caption renderer tests. No new testing seam is introduced. The frozen historical caption fixtures and independent oracle remain byte-identical. The current article expectation changes only for the explicitly approved production metadata/notice removal.

| Existing seam | Release verification | Criteria |
|---|---|---|
| Git/source ownership | Main ancestry, no staging-only ancestry, exact changed-path inventory and source comparison | AP-02, AP-03, AP-09 |
| Prepare/verify | Selected main-based candidate, immutable receipt and source state | AP-01, AP-04 |
| Markdown/Vue | Existing component and caption tests, article sources/citations/media | Approved component/caption tables |
| Build/output | OS-isolated build, outside read/write/network sentinel, full unselected route/prose/asset scan | AP-07 |
| Browser | Actual candidate route, figures/references/recommendation, mobile/light/dark | Existing browser acceptance |
| Reviews | Independent Standards, Spec and security passes on the captured main-relative diff | Project stages 6–7 |

Other candidates currently lack valid independent heads. They cannot truthfully be placed into a standard prepare plan. Their exact staging source paths and signatures are recorded separately for exclusion auditing; this is not a fabricated claim that those branches are valid publication sources.

The historical adoption verifier enforces immutable predecessor source hashes. Its result is recorded separately; it is not weakened or rewritten for this article release.
