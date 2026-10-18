# T-0020 approved coverage

Public test surface: scripts/publication-job.py prepare/verify, real disposable full Git trees, actual installed runtime and sandbox-exec probes. Reused public remote controller uses a labeled FakeGitHub adapter, not actual GitHub. Each row corresponds to the preapproved PB table; no original P01–P24 result changes.

| Row | Executed subcases | Result |
| --- | --- | --- |
| PB-01 | Wrong/missing Node, pnpm, dependencies; noncanonical Node; escaped deps; actual enforced isolation; explicit older-Python/Linux observation fixtures; no install/source Git write | PASS |
| PB-02 | Fresh separate writer/validator sealed inputs, external independent digests, full refs/tree/role/policy; same recomputed operation; actual outside-read/write/network denials | PASS |
| PB-03 | Root mode/UID, file mode/UID/type/link-count, content/digest, symlink, directory input, extra file, read stability; actual remote consumer rechecks metadata and directly consumes verified in-memory inputs; actual filesystem plus explicitly labeled UID/fstat-time observation fixtures | PASS |
| PB-04 | Both roles reject each of four API credential sentinels; no leaked sentinel/output/source-object write; validator has no writer credential; isolated host probe retained | PASS |
| PB-05 | Durable journal reused across fresh jobs; API accepted-unknown recovered by readback with one advance/create; foreign/unknown-source state refused; inactive parsed YAML binds shared writer and distinct validator groups, no cancellation | PASS |
| PB-06 | Shallow/missing refs/source, wrong source/pin/tree/registry identity/digest/state, invented permission/dispatch/exercise fields; no output or remote proof | PASS |

Focused run: six methods successful; source uses existing dependencies explicitly, no installation. Full regression66+122+10 passed on unchanged v2 production code. The later test-only predicate expansion was separately rerun (six methods); it is a supplement, not a second full-suite claim. Standards/Spec/security source review passed; final evidence supplement pending. Actual authorized main/staging landings pending. T-0016 P13 NOT RUN. This ticket remains review after local checks and cannot be done based on these local results.
