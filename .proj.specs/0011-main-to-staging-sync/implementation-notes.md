# Conflict resolution and contract integration

The real merge has first parent staging 4005ee45f2f3267a8b53ce24fa97af7b49cfb144 and pending second parent main eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a. All six conflict paths are resolved and the unmerged index is empty.

| Conflict | Resolution |
|---|---|
| Sidebar | Keep staging bytes/title and navigation intent. |
| Theme registration | Keep staging PreviewNotice and all existing components. |
| Electricity article | Keep exact staging draft/preview flags, review notice and content. |
| Caption tests | Keep staging's independent historical migration and current-draft assertions. |
| Public verifier | Combine strict contract routing with lazy module loading, without catching validation failures or retrying another guard. |
| Tracker harness | Keep staging views; use literal lint epoch and no-replace Git read, remove historical skip. |

Only three existing staging files change: public verifier, reconciliation CODE set and tracker harness. The two additional reviewed-code entries are the byte-identical main helper and main regression suite. All original provenance digests, expected identities, package/lockfile and historical evidence remain unchanged. The listing already has identical staging/main bytes and is retained.

Routing observes any of the four exact reconciliation records, including broken links; that path takes precedence and a failure never falls back. Otherwise a working or HEAD-recorded main scope selects the main guard. The HEAD scope lookup keeps missing-scope tampering on its existing precise diagnostic; it grants no approval and the main guard validates ancestry, scope digest and the full inventory. With neither contract, original historical adoption checks still run. Guard modules are loaded on demand with bytecode writes disabled.

The local website build uses CF_PAGES_BRANCH=staging, a regular-file source projection and installed Node 24.13.0/pnpm 10.28.0. The OS sandbox denies external read/write and network; synthetic probes pass. Initial Corepack lookup and linked Vite cache attempts failed within the boundary, were retained as failed logs, and were fixed by directly invoking cached pnpm and creating disposable regular cache directories. No dependency installation or host protection change occurred.

Browser evidence covers the local static staging build only. Canonical spec article routes appear with VitePress's generated .html suffix in the actual href and final URL. One card, matching title/description/date, Enter navigation and visible staging review notice were observed. Desktop 1440x900 and mobile window override 390x844 light/dark have equal document scrollWidth/clientWidth; mobile client width is 375 due to the scrollbar. Native screenshot pixel dimensions are independent of DOM viewport metrics. The stale staging sidebar title and review copy are intentionally preserved, as required by exact staging source preservation.

Rollback requires a reviewed staging revert; no reset, force push or main publication is part of this ticket. Existing T-0010 status/evidence remains imported history, not rewritten to imply staging landing.

## Independent-branch landing ref regression

Full Python regression found SuccessorTests' cloned branch had refs/remotes/origin/staging but no refs/heads/staging. Both receipt/approval files and the original landed commit existed. Creating only the missing local alias made the old checker pass, isolating the cause. The shared CLI now selects the local staging branch when present, otherwise its origin/staging counterpart. It never retries another ref after failed ancestry. Missing refs, wrong ancestry and missing approval still reject. A fast regression at the existing tracker seam passed after first reproducing this exact failure; all historical receipts and commit hashes remain unchanged. This is ref resolution for the same configured target, not new landing authority.

Browser server observations included the pre-existing missing FontAwesome stylesheet responses; all 111 website sources are unchanged. They do not alter the accepted listing/preview checks and are outside this synchronization repair. Temporary server and browser tab were closed and viewport reset.
