# P13 A1 bootstrap — actual blocked observation

The authorized private lab exists. Its actual strict staging check is0x1DEA-publication-validation/App15368 with enforce_admins=true; private protection support exists. Zero self-hosted runners is not evidence that hosted macos-15 is unavailable. The actual manual hosted run started and completed, so runner execution is observed.

One reviewed read-only probe was imported into lab main as e7d6a9607e93dcd372ee57853540692c2185cff9, based on reviewed production main6b7da90. Workflow SHA3275d7add6b4b881bd6413f09dd885f1760f0ce672b95366c72b7755993ea168. Run39103693455/attempt1, workflow_dispatch/main at exactly that SHA, completed failure with a unique matching probe identity. This is the intended preflight refusal when prerequisites are missing, not successful P13 acceptance.

Observed default PATH: Nodev22.23.2, no pnpm executable, Python3.14.7, Git2.55.0. sandbox-exec is available, but availability does not prove deny-default isolation. The exact required Node24.13.0/pnpm10.28.0 pair is not established; this probe does not enumerate every alternate preinstalled toolcache. PUBLICATION_CONFIG_DIR, validator job digest and writer job digest selections are absent; REST inventory also has0 variables/0 secrets. Only bootstrap administrator is listed; separate limited writer/validator/reporter/non-bypass merge capabilities are not proved.

Stop dependent controller, protected candidate checks, race/merge and landing exercises. No package/runner installation, scope expansion, protection removal or fabricated ready flags. The own bootstrap workflow is now disabled_manually. Lab staging remains05fc16c30f978bbafab4b8cc89f24f8657ab3045 and production main/staging remain6b7da90/500d02b. T-0016 stays review; P13 is blocked, not passed.

Next prerequisite work requires an owner-designated provisioned runner/toolchain/dependencies with original enforced isolation; reproducible external source/registry/runtime/state/admission inputs and independent digests; separately verified limited roles/check reporter and non-bypass merge capability. A hosted runner able to start is insufficient. Do not switch to unrestricted builds or grant broader roles. The original P13 a-l table remains unchanged; see coverage.md for this checkpoint.

Evidence is a whitelist projection of API/run output, not raw repository/token responses. Private raw runner logs remain outside the public-source checkout; only the exact controlled JSON marker is retained here. No production commit/push/PR accompanies this operational result.
