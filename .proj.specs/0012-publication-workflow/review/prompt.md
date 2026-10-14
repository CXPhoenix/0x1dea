# Frozen adversarial review prompt

Review the captured epic 0012 publication-workflow planning packet, on your one assigned
axis only. The parent supplies the version directory; this prompt is replayed verbatim
in round 2 and only the captured specification version changes.

Read all files listed in the version manifest; supporting contract files are immutable
reference inputs. The draft skill and proposed test plan are part of the design, not
implemented capabilities. Evaluate spec.en.md together with traceability.md, test-plan.md,
adr-proposal.md and the complete skill draft. No translation exists until review converges.

Axes: Completeness maps every applicable type/field/boundary to an AC and observable test.
Verifiability asks whether every AC and gate has a decidable pass/fail condition. Contract
conflict checks existing project vocabulary, ADRs, preservation, authorization and public
seams, including explicitly proposed successors. Red team identifies unintended behavior
and trust-boundary crossings in the resulting design.

Grade P0 if the spec cannot be implemented correctly as written (including unjudgeable ACs),
P1 if a real problem can be resolved inside a ticket, P2 if worth recording without blocking.
Seek counterexamples; do not assume the current design is correct. Cite captured relative
file and one-based line, describe the failing scenario and smallest sufficient correction.
State exact P0/P1/P2 counts and limits. If none, say so. Distinguish a design defect from
unknown live configuration explicitly gated before activation. Do not treat a planning
artifact as a successful product test, owner approval or external authority.

Read-only: do not edit files, write tests, run product builds, change Git state, use network
or call remote mutation tools. Return findings to the parent; the parent persists reports.
Do not arbitrate another reviewer's axis or propose a third review round.
