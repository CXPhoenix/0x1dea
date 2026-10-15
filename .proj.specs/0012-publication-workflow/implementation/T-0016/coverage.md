# T-0016 measured coverage

Approved allocation: P10–P13; closure reuses C2/C3/P23. This reports measured seams, not line-coverage percentages or authority for remote mutations.

| Seam / row | Tests and measured execution | AC | Uncovered / limits |
|---|---|---|---|
| P10 latest refs, no-op, ownership and one retained branch/PR | 22 remote-sync cases across P10–P12, actual disposable Git plus literal fake GitHub; exact closed+merged implementation PR required, missing/wrong/unmerged/open bootstrap rejected | AC05/06 | No actual GitHub mutation; no force/target write/unrelated PR update |
| P11 shared lock, drift, recovery | Real threaded lock, lost branch/dispatch/PR response readback, journal before writes, bounded three retries; branch/PR identities reread | AC06 | Inactive shared Actions group is a template, not activated remote serialization; manual actors addressed by rereads |
| P12 exact trusted validation | 3 trusted-validation cases including actual native staging validation and enforced isolated build; wrong/missing/stale/failed/queued run negatives, JSON transport and writer-token Git-child regression in remote-sync suite | AC03/07 | Two complete runs each actually build 143 staging synthetic output files; outside read/write/network probes denied. Local synthetic trusted-main operation, not GitHub CI |
| P13 actual disposable remote exercise | Not run; explicit designated disposable repository/exercise authority absent | AC07/09 | Activation and ticket done blocked; production read-only permissions/rules/workflows inventory is not exercise evidence |
| Conditional closeout / C2/C3/P23 | 3 landed-closeout cases, finite actual receipt pins and exact target metadata; receipt ancestor substitution rejected; original fixture assertion AST lists unchanged (11/17) | T12/T14/T15 | Owner actual PR20/21/25/26 landings verified. Done tracker edits are local until authorized delivery |
| Complete Python regression | main 192=66+116+10; staging 221=95+116+10; each exit0, zero failures/errors/skips | Historical and current contracts | 849-common-path frozen source checkpoint; unchanged #22 historical context retained |
| Product regression | main54 unit/6files; staging87/8files; both lint zero warnings; main isolated build96 output files | Existing behavior | Website/config/default build sources unchanged after these checks; build is CLI surface, no HTTP/browser claim |
| Native/project/materializer | Both roles pass recorded checkpoints; materializer main176 generated/55 sources and staging178/56 | Source and preservation | Target-specific outputs intentionally differ; final metadata-only recheck saved separately |

Full outputs, exact artifact SHA-256/projection bindings and source checkpoint are under final/. All red/green and retained failed attempts are under tdd/, attempts/, tdd-evidence.json. No new skip/frozen-module bypass, no disabled assertions, no changed blog/active skill/.github/deployment bytes.

Independent source supplement: Spec P0/P1/P2=0/0/0; Security HIGH/MEDIUM=0/0; Standards remaining two English README P2 corrected to Taiwan Traditional Chinese after complete runs. Final metadata/evidence supplement is recorded in review/code-T-0016.md and review/security-T-0016.md when read back. T16 is review, not done; P13 remains unverified.
