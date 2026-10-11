# Fresh T-0010 delivery validation

The owner explicitly authorized commit, non-force push and a PR to main, with no other candidates and no merge. See authorization.md. Capture base: 88b9c53852f527ee636bcc4b4ca5e166f6ec10fd; branch tickets/T-0010/main-verification-repair. At this capture, the delivery mutations had not yet run; this report is the pre-commit gate, not a claim of landing. Ticket status remains review.

| Check | Current result | Evidence |
|---|---|---|
| pnpm test:unit | 54 passed across 6 files | unit.txt/json |
| Python harness discover | 66 passed; 0 failures/errors/skips | harness.txt/json |
| Python publication discover | 16 passed; 0 failures/errors/skips | publication.txt/json |
| pnpm lint | exit 0, max warnings 0 | lint.txt/json |
| verify-project.py | exit 0 | structure.txt/json |
| materialize-writing-skills.py --check | exit 0 | materializer.txt/json |
| verify-harness-adoption.py | exit 0; historical/current contracts remain active | verifier.txt/json |
| OS sandbox docs:build | exit 0, exact current blog/config projection | sandbox-build.txt/json |
| Sandbox sentinels | permitted inside read; outside read/write and network denied | sandbox-probe.txt |
| Scope/preservation audit | 1716 of 1719 existing release entries unchanged; only one blog index and original two tracked repair files differ; five candidates absent | scope-audit.json |

Toolchain remains existing Node24.13.0, pnpm10.28.0, Python3.14.3. No package was installed. Sandbox denial warnings for personal package-manager config remain expected and unchanged. The publication CLI executable Markdown restriction remains intact; the exact existing category template was reviewed and built inside the OS sandbox.

All five implementation hashes still match the final independent review packet. Standards and final Spec unresolved P0/P1/P2=0/0/0; security HIGH/MEDIUM=0/0. Reviews cover the combined verifier/harness plus listing repair. This delivery adds authority, fresh raw command records and scoped screenshots only, with no implementation delta since that review.

Browser verification is the previously captured actual local surface for those identical source bytes: desktop/mobile, light/dark, exact one article row/date/link, no horizontal overflow and Tab/Enter navigation. The initial mobile viewport evidence finding was retained and independently closed using direct live DOM measurement. Screenshot artifact dimensions are not substituted for viewport measurements. Existing Font Awesome stylesheet404s are unchanged and recorded; no CI or production verification is claimed. See ../listing-followup/review/code-final.md and ../listing-followup/evidence/mobile-viewport-supplement.json.

The complete historical release oracle, original scope/evidence, article body/times and assets remain byte-identical. The only website change is blog/post/course/security-awareness/index.md. Staging ancestry and the five local-preview candidate articles are excluded. The PR must stay unmerged.

Raw command .txt logs retain their original output bytes, including trailing blank lines and one progress-line trailing space. The broad Git whitespace check reports those evidence-only differences; the source/Markdown/JSON check excludes raw .txt logs and must pass. No original command output is silently normalized.
