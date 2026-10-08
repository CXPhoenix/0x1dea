# Authorized validation follow-up

The owner explicitly authorized continued isolation diagnosis and installation of
the missing dependency in the isolated clone on 2026-10-08 at 16:57 Asia/Taipei.
The owner approved this bounded scope; private authorization records are retained locally.
This supersedes the previous operator-level installation restriction for this
bounded follow-up only. AP-06 still prohibits the publication CLI from installing
dependencies or granting publication authority. No product CLI behavior changes.

Scope: add exactly `@unocss/eslint-plugin` 66.6.0 from npm's official registry,
update the isolated manifest, lockfile, node_modules and necessary pnpm cache;
retain Node 24.13.0, pnpm 10.28.0 and all existing dependency versions. Installation
scripts are disabled. Original repository, global configuration, security/trust,
credentials, commits, push, PR, merge and deployment remain outside authorization.

## Follow-up test plan and observed result

| Seam | Counterexample / check | Result |
| --- | --- | --- |
| Runtime read boundary | Same scoped profile fails before runtime startup; kernel reports denied root-directory read | Initial exit 134 preserved; one literal `/` read rule fixes startup without permitting descendants |
| Forced boundary | Synthetic outside-file read/write and local network connection | All denied; inside sentinel readable; no system permission changed |
| Candidate build/output | A-only reconstructed candidate, B route/prose exclusion, immutable original candidate receipt | Same sandbox build exit 0; receipt verified; supplementary output scan passes; publishable false |
| Authorized manifest delta | Version drift, existing dependency drift, unrelated package or missing required addition | Red test before helper; all counterexamples rejected after fix |
| Historical preservation | Dependency addition initially rejected as changed preserved source | Exact successor before/after hashes added; historical adoption manifests retained |
| Lint | Existing TS files and package baseline versus final manifest | Runs successfully; existing failures remain: TS 355, manifest 8; no new manifest diagnostics |

Evidence: [resolution](evidence/followup-resolution.json),
[check results](evidence/followup-checks.json),
[public isolation summary](public-evidence.md),
[sentinels](evidence/isolation-sentinel-followup.json),
[output verification](evidence/isolated-output-verification.json).
The profile is a host-specific diagnostic artifact, not an installed or portable
sandbox launcher. Build evidence covers the synthetic candidate, not deployment
or future candidates. Pin/content changes require reconstruction and revalidation.

The existing ESLint 10 peer-range warnings remain visible. Lint failures are not
suppressed, rules are not disabled and unrelated source is not reformatted.
