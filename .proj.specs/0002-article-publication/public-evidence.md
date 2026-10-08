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

Lint executes but remains an existing failure: 355 errors in the unchanged
TypeScript helper/tests, plus 8 manifest errors identical to the baseline.
ESLint 10 peer-range warnings remain visible. A later scoped lint cleanup must
preserve behavior, rerun tests and checks, obtain review, and update exact
preservation evidence for authorized changes without rewriting the historical
adoption manifests. PR creation, merge and deployment are separate actions.
