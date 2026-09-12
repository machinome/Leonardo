## ADDED Requirements

### Requirement: Connected reciprocating saw
The sawmill SHALL show a waterwheel and keyed shaft turning a crank whose connected rod moves a guided saw sash through a 48 mm stroke.

#### Scenario: A turn of the wheel
- **WHEN** a full wheel revolution is inspected
- **THEN** the sash traverses both dead centers, the crank pin stays captured by the rod, and the sash stays inside its guides without rigid interpenetration.

### Requirement: Indexed timber feed
The carriage SHALL dwell on the cutting downstroke and advance 8 mm during the return, completing a 32 mm advance over the four-cycle demonstration.

#### Scenario: Cutting and return
- **WHEN** the phase advances through 0, 180 and 360 degrees
- **THEN** the carriage dwells between the first two poses and is 8 mm farther forward at the last pose.

#### Scenario: Four-cycle pass
- **WHEN** the pass reaches 1440 degrees
- **THEN** the carriage has advanced 32 mm and the repeating presentation identifies its carriage reset.

### Requirement: Cleared blade path
The blade SHALL remain clear of both halves of the pre-slotted timber throughout the demonstration.

#### Scenario: Inspect the kerf
- **WHEN** the saw cycle is sampled at the supported kerf boundary
- **THEN** the blade does not intersect either timber half.

