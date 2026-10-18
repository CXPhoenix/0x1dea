# Source-v1 independent review checkpoint

Packet: /private/tmp/T21-source-review; base=HEAD=64b31a2c38959ef5490892fa2a001bb0bf2f8ca0; files_sha256=b6d37405e32c863b7e0b752ea75d9bf2db56e85c34c78bf32d32f1410b7e0b68. Captured staged WIP, 2946 entries (2943 regular, 3 symlink literals).

| Axis / independent reviewer | Result | Scope |
|---|---|---|
| Standards / t21_standards | P0/P1/P2=0/0/0; smells=0 | Project rules, closeout evidence, language, preservation; no test rerun or live P13 |
| Spec / t21_spec | P0/P1/P2=0/2/0 | C3 check identity reuse and C4 local non-bypass evidence gaps; closure records otherwise supported |
| Security finder / t21_security | HIGH/MEDIUM=0/0 at confidence >=0.8; no confirmed candidates | Source only; actual platform rights/rules/Actions/manual races and P13 unverified |

Spec finding 1: scripts/publication_reporting.py:188-194,210-224 saved check_id but would accept replacement ID81->82 with otherwise matching list/direct payload. Confirmed identity must be pinned.
Spec finding 2: scripts/publication_reporting.py:128-138 only observed strict/check/app/admin/write/site_admin; local-ready lacked explicit independent non-bypass data.
Both are retained as historical findings and reproduced/fixed in source v2. Reviewer explicitly accepted refusing every live=True request under requirements.en.md:47; this local prerequisite ticket does not require live readiness.
Security rejected classic-only protection as an exploitable live bypass because live=True refuses; trusted callbacks outside the attacker boundary; journal race lacked attacker write access; point-in-time races are declared and no merge API exists.
Full source-v1 regressions were pending and then interrupted, never accepted as passing.
