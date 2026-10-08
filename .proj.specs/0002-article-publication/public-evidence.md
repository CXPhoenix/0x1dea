# Public evidence boundary

This directory publishes validation summaries and sanitized logs. Machine-local
paths, runtime state locations, private authorization records, original message
identifiers and host-specific sandbox profiles are retained outside the repository.
Log hashes cover the published copies after path redaction. The public review
prompt has its local checkout label redacted; the original frozen prompt and
review packets are retained locally. Redaction changes evidence presentation, not
the reviewed skill, CLI, tests or dependency delta.

## Isolation result and scope

The observed macOS startup denial was `file-read-data /`. Adding only
`(allow file-read-data (literal "/"))` to the scoped diagnostic profile fixed
startup. It does not grant recursive root-directory reads. The profile denied
network access and file-data reads/writes by default, allowed system/runtime and
installed toolchain reads, allowed the synthetic candidate workspace and probe,
and restricted writes to disposable validation storage and device output.
Global file metadata reads were allowed. The host-specific profile is diagnostic
evidence, not a portable launcher or an installed sandbox policy.

The outside-file read/write and local network connection sentinels were denied;
inside data remained readable. The same scoped profile built the synthetic A-only
candidate. Its original source receipt remained valid, the B route/prose scan
passed, and all 27 output files lacked the outside sentinel bytes. These checks
cover this host and fixture; they are not a complete sandbox escape/IPC audit,
confidentiality proof, or publication authorization. New pins or source changes
require new candidate verification and build evidence.

## Published state and next step

The owner authorized committing the reviewed phase-1 work and non-force pushing
the ticket branch for inspection. This does not complete publication or landing.
The publication CLI remains local-only and returns `publishable: false`.

The earlier phase-1 validation observed 355 TypeScript errors and 8 manifest
errors. The authorized cleanup now uses the complete first-party scope documented
in [lint-cleanup.md](lint-cleanup.md), exposed by `pnpm lint`; final results and
exact rules/files are in [validation](evidence/lint-cleanup-validation.json).
ESLint 9.39.2 satisfies the existing plugins' peer ranges. The strict-peer frozen
clean installation, CLI/harness/Vitest, build, materializer, structure, preservation
and semantic comparisons all pass. Historical adoption and publication manifests
remain unchanged; the separate cleanup successor records only the authorized files.

The unrestricted `eslint .` diagnostic still includes immutable imported packages
and historical/educational Markdown; its failure is recorded in
[broad diagnostic](evidence/lint-cleanup-broad-diagnostic.json). No rule or ignore
was added to suppress it. This work does not claim the broader command passes.
Browser read-only comparison loaded both versions with the same article/date/order
surface. Chrome input dispatch timed out, so interactive browser verification is
blocked; Vue public-interface regression tests and built HTML/CSS comparisons pass.
These limits remain explicit and do not grant publication authority.

The owner subsequently authorized commit, non-force branch push and a combined
draft PR targeting staging for the publication skill and cleanup. Merge, direct
protected-branch push, additional deployment and security settings remain excluded.
The publication CLI stays local-only and `publishable: false`.
