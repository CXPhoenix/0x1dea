# Retrospective — T-0009

- Fixed Git epochs need frozen accepted product inputs even when the verifier
  implementation is current. Begin negative probes from a proven positive control.
- Keep historical migration proof separate from later editorial source. Preserve
  independent oracles rather than updating expected hashes from mutable input.
- Treat zero discovery as failure; report methods and subtest failure records
  separately. Run both named suites through the complete command.
- Complete the measured coverage table before change review. The T-0009 review
  caught and closed this ordering issue; retain its initial report honestly.
- A reviewed-code hash exemption still requires file existence and regular type.
- Capture owner landing authority and actual remote containment separately. Close
  tickets only after verified landing, then publish the status/evidence commit.

These apply existing contracts and need no new ADR. No unresolved architecture
decision or security chain remains within this epic's scope. Future source
successors still require a new reviewed increment.
