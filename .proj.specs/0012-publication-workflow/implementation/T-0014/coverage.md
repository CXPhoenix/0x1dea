# T-0014 coverage checkpoint

Approved rows only; public remote-free Git/CLI tests. Actual real build is macOS + existing
Node24.13.0 and pnpm10.28.0 installed toolchain. No installation, remote or browser claim.

| Row / AC | Public evidence | Observed result | Limits |
|---|---|---|---|
| P04 / AC03,04 | V1 rejects staged ancestry; explicitv2 prepares already-integrated A; independent Git tree | pass | Synthetic Git graph only |
| P05 / AC04 | Stage ancestry, B add/revert, empty B topic identity | pass; all rejected before export | Includes reviewed P1 fix |
| P06 / AC04 | Fresh main merges, exact dependency, reviewed/unreviewed conflict trees, stale/shallow/source/stage unknown histories | pass | No real source rewriting |
| P07 / AC01,04,08 | Full staging mode/blob registry, omitted B/assets, overlaps, unauthorized shared HTML/link/prose | pass | Exact reviewed policy from caller; signature scans supplementary |
| P08 / AC03,04 | Legacy without binding refuses; exact original/new extract record succeeds | pass | Synthetic owner approval only; six real candidates stay legacy |
| P14 / AC02,08 | Exact A/dependency manifest, B/new C revision/assets excluded, published C retained | pass | Published source baseline, not production observation |
| P15 / AC08 | Source/index/custom routes/raw HTML plus whole real output/search/RSS/asset inventory | pass | All output files checked; absent short revision signatures remain unverified |
| P16 / AC07,08 | Full receipt/blob/mode, new/canonical links, deletion, submodule, escaping include/import; actual OS read/write/net probes | pass | No unrestricted fallback; preserved original aliases and v1 bytes |
| P17 / AC08 | Actual VitePress receipt + output inventory, separate approved bindings, missing/altered output, short signatures | pass | MacOS boundary only; synthetic served-preview attestation does not prove HTTP |
| Shared historical/current AC03 | Versioned #22 T13 assertions unchanged plus live closed-tracker/future map cases | final run recorded separately | Historical code success cannot validate v2 |

Initial parent sandbox blocked the localhost listener; the raw failed run is retained.
Only separately authorized transient OS verification produced actual pass evidence.
18 initial vertical red→green cycles plus three review-driven red→green fixes are recorded;
additional hardening tests are labeled green regressions, not invented red cycles.
Ticket is implementation/review work only; actual authorized dual-target landing still pending.

Final current integration:66 live harness +58 live publication (24 retained live,30v2,3closed,1preflight)
plus10 immutable #22 cases=134, exit0; failures/errors0. Both target-role native closed cases
pass. Website54unit/build/lint/structure/materializer pass. Final Standards/Spec/Security
reports have zero unresolved findings. Shared guards preserve all original assertions,
reject fake M0 receipt and compare T13 to actual historical landing policy. No remote landing.
