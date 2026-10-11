# Local repair retrospective

The historical verifier's refusal correctly prevented silently refreshing earlier product hashes, but the historical fixture used the live checkout as accepted input. Future epoch tests must materialize their accepted source from fixed Git objects while running current verifier code.

A selected main publication needs its own exact verification successor and a real-main positive control. Staging-only successors cannot establish selected production scope. Future publication preparation should check both Python suites and the public preservation CLI before claiming the release gate is clear; green test:unit establishes Vitest only.

The first new guard also reused a new-path policy to select old protected inputs. Independent Spec review found this error despite green tests. The current guard separates immutable existing entries from allowed additions and limits mutable code to the four reviewed trust roots. Keep the failure/review/red/green evidence, rather than rewriting a pass onto the initial snapshot.

No new architecture decision, external automation or dependency is introduced. Source history and original PR failure records remain unchanged. This follow-up is locally reviewable and requires separate authority before landing.
