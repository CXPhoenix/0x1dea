## ADDED Requirements

### Requirement: Figure prose and guided-reading boundary

Phoenix prose SHALL explain a figure or table's mechanism, evidence and limits within the argument. It SHALL NOT replace that argument with commands to move the reader's gaze. Explicit requests for procedural figure-reading instruction SHALL permit accurate stepwise guidance. Neither mode SHALL require a question opener or prohibit reader dialogue.

#### Scenario: Figure integrated into prose

- **WHEN** a user asks for prose explaining a single-cache timeline with data updated at 10:00 and invalidation at 10:05
- **THEN** the prose explains the interval of potential stale reads and the single-cache scope without directing gaze movement
- **AND** it preserves uncertainty and does not claim multi-service coordination

#### Scenario: Explicit guided-reading lesson

- **WHEN** a user explicitly asks for two steps teaching how to read that timeline
- **THEN** the output provides two accurate reading steps and the requested caption
- **AND** guidance serves the requested lesson without inventing figure data

#### Scenario: Preserving failed evaluation history

- **WHEN** parent QA rejects an earlier output for gaze-direction prose and a mismatched opener rubric
- **THEN** original inputs, outputs and judgments remain unchanged, with a separate parent-QA correction
- **AND** a frozen revised skill is evaluated only on the affected positive and boundary cases by fresh writers and an independent judge
