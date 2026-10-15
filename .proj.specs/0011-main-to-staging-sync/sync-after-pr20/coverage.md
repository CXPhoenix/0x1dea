# Synchronization coverage after PR20

| Seam / criterion | Measured result | Evidence and boundaries |
|---|---|---|
| S1 exact engineering/candidate identity | pass | source-audit.json:111blog/50candidate/376historical paths unchanged; all716 original main common identities retained;13 non-policy engineering/doc/test delta paths exact main |
| S1 independent target merge | reviewed metadata resolutions | independent-merge.json pins actual stage/main; only T11 coverage/ticket conflict, both resolved to already-approved exact main successors. Resolved tree82570216ca00e91467f782deb5cfbf7354aab9ab matches proposed sources except the exact map extension/new sync evidence. Real staging history is joined after the tested source commit, with full-tree identity checked |
| S2/S3 native/historical tests | pass | current shared controller, all original fixtures/assertions, no fallback/new freezing/skip; legacy helper and original test_main_release exact main |
| S4 full Python | pass193 | python.txt:95live harness+88live publication+10explicit fixed#22 historical;0failures/errors/skips. Real synthetic macOS isolated-build test executes |
| S4 renderer/runner | pass87 | unit.txt:8 files/87tests, no altered assertions |
| S4 lint | pass,zero warnings | lint.txt/exit0 with max-warnings0, unchanged first-party scope |
| S4 actual staging build | pass | build.json/build.txt:Node24.13.0,CF_PAGES_BRANCH=staging,actual VitePress build. Deny-default macOS boundary allowed inside-read and denied outside-read/outside-write/network. Original profile hash and separately labeled public path projection retained |
| S4 structure/materializer/native | pass at checkpoint | separate raw records;178generated/56source packages;native staging role. Final metadata identity check follows recording these reports |
| S4 local browser | pass specified acceptance | browser/browser.json + snapshots/screens:1440x900/390x844 light/dark, correct sole card/title/date/frontmatter description/href, no horizontal overflow; real focus+Enter reaches exact article, correct h1 and visible staging notice. Parent inspected all5 screenshots |
| S4 independent reviews | initial axes/security clear, final supplement review follows | separate code/security reports; final code matches approved main, candidate text never executable policy |
| S5 delivery | pinned,not yet remote delivery in this record | original T11 topic/PR21→staging, noforce/noauto/no target merge/deploy; latest refs reread before push, then actual PR/head/base/files readback |

No new behavior, test or seam was introduced: all engineering/test sources are approved main bytes. After full runs only additive evidence/map metadata is recorded and native/structure/materializer are rechecked; a source-identical ancestry merge does not replace any execution result. T11 done is its original PR19 landing; current PR21 is unmerged, and T12/T14/T15 remain review until actual required landing/closeout.

## Attempts and limits

The first browser URL-glob wait timed out at25s; subsequent observation showed the expected destination/title/notice. The record does not distinguish latency from matcher behavior. A retry initially stopped at an already-existing output directory before browser actions. The final run uses a new output directory and an equivalent exact pathname DOM condition, plus the same article/title/notice checks; application source is unchanged. Incomplete attempts remain labeled incomplete, not red→green product fixes.

Local static HTTP logged a pre-existing FontAwesome regular stylesheet404: unchanged fixed-stage config references /assets/fontawesome/regular.min.css, while the preserved actual asset exists under /assets/fontawesome/css/regular.min.css. No new HTTP-clean or Production acceptance is claimed; the specified listing/card/keyboard/notice checks pass. This unrelated existing path mismatch is recorded rather than expanding approved engineering/article/deployment scope.

This browser evidence does not close old T3/T4/T8 browser/SSR/print/Production gaps. No remote CI, deployed staging alias or Production behavior is verified. New public logs replace only named absolute checkout/runtime labels; validation hashes cover published bytes. Original private raw/profile/partial screenshots remain outside Git; all pre-existing historical evidence stays byte-identical.
