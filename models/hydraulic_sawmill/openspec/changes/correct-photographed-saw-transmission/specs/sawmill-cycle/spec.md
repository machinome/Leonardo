## MODIFIED Requirements

### Requirement: Indexed timber feed
The carriage SHALL advance by one ratchet tooth's rope take-up on the
driving hook's pulling downstroke and dwell during its recovery, covering
the entire timber in a pass.

#### Scenario: Cutting and return
- **WHEN** phase advances through 0, 180 and 360 degrees
- **THEN** the carriage advances during the first half turn and retains
  that advance during the recovery half turn.

#### Scenario: Complete timber pass
- **WHEN** the timeline travels from beginning to end
- **THEN** the timber starts wholly before the blade, finishes wholly beyond it,
  remains supported on the carriage with all rollers on the rails, and any
  repeat identifies its carriage reset as a replay operation.
