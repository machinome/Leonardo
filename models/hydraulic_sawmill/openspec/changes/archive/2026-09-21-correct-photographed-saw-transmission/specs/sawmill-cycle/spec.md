## MODIFIED Requirements

### Requirement: Indexed timber feed
The carriage SHALL advance through the two-rope compound winding reduction
on the driving hook's pulling downstroke and dwell during its recovery,
covering the entire timber in a pass. Feed SHALL derive from ratchet pitch,
winding radii and conserved rope paths, and full-pass time SHALL derive
from the required waterwheel turns at the declared wheel period.

#### Scenario: Cutting and return
- **WHEN** phase advances through 0, 180 and 360 degrees
- **THEN** the carriage advances during the first half turn and retains
  that advance during the recovery half turn.

#### Scenario: Complete timber pass
- **WHEN** the timeline travels from beginning to end
- **THEN** the timber starts wholly before the blade, finishes wholly beyond it,
  remains supported on the carriage with all rollers on the rails, and any
  repeat identifies its carriage reset as a replay operation.

#### Scenario: Follow the reduction
- **WHEN** the ratchet advances one tooth
- **THEN** winding directly on the slender ratchet axle draws the drive rope
  from the gear's inward side, turns the larger section of the cross-shaft, and
  the input coil's growing radius is reflected in that take-up, and
  the thinner section takes up less carriage rope in the same shaft turn,
  with both ropes remaining attached, continuous and length-conserving.

#### Scenario: Time a complete cut
- **WHEN** the waterwheel runs at its declared period
- **THEN** the timeline covers the turns needed by that transmission for
  the complete timber course, without accelerating the carriage to meet
  the superseded 296-second duration.
