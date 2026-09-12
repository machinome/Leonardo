## MODIFIED Requirements

### Requirement: Connected reciprocating saw
The sawmill SHALL show a waterwheel and keyed shaft turning a crank whose
connected rod moves a guided saw sash through twice the crank throw, with
the blade held at both ends and the journals retained.

#### Scenario: A turn of the wheel
- **WHEN** a full wheel revolution is inspected
- **THEN** the sash traverses both dead centers, the crank pin stays captured
  by the rod, and the sash stays inside its guides without rigid interpenetration.

### Requirement: Indexed timber feed
The carriage SHALL dwell on the cutting downstroke and advance by one ratchet
tooth's rope take-up during the return, completing four increments in a pass.

#### Scenario: Cutting and return
- **WHEN** phase advances through 0, 180 and 360 degrees
- **THEN** the carriage dwells between the first two poses and advances by
  the rope take-up corresponding to one tooth at the last pose.

#### Scenario: Four-cycle pass
- **WHEN** the pass reaches 1440 degrees
- **THEN** the carriage has advanced four increments and the repeating
  presentation identifies its carriage reset as a replay operation.
