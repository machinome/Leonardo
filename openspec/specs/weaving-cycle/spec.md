# weaving-cycle Specification

## Purpose

Demonstrate how a common drive coordinates the two alternating sheds, accompanied weft insertion, beat-up and cloth feed in Leonardo's narrow automatic loom.

## Requirements

### Requirement: Alternating open shed
The loom SHALL raise one set of alternate warp ends while lowering the other, reverse their roles on the return pick, and keep the carrier clear of the warp during insertion.

#### Scenario: Opposite picks
- **WHEN** the cycle is at 90 and 270 degrees
- **THEN** the two heddle frames exchange their upper and lower positions, the spool is in the central shed, and the upper/lower warp paths clear its envelope.

### Requirement: Accompanied weft carrier
Two visible arms SHALL accompany the spool from either edge toward the center and exchange it at the center, illustrating the limited-width mechanism described by the museum.

#### Scenario: Transfer across the ribbon
- **WHEN** a two-pick cycle is traversed
- **THEN** the spool travels from beyond the left selvedge to beyond the right selvedge and returns, meeting both arm tips at each center handoff.

### Requirement: Beat-up follows insertion
The reed SHALL approach the cloth fell with the carrier outside the warp and retreat while the carrier crosses the shed.

#### Scenario: Beat and retreat
- **WHEN** the cycle reaches 0 or 180 degrees
- **THEN** the reed is at its forward limit and the spool is outside the cloth width.
- **WHEN** the cycle reaches 90 or 270 degrees
- **THEN** the reed is withdrawn and the spool crosses behind it.

### Requirement: Connected shedding drive
The model SHALL show a rotating eccentric captured in a slotted follower, whose rise drives its heddle frame.

#### Scenario: Positive follower engagement
- **WHEN** the cycle is sampled across a revolution
- **THEN** the pin remains inside the follower slot without shared volume, the follower has bounded running play, and displacement beyond that play is blocked by the pin.

### Requirement: Visible cloth feed
The loom SHALL show warp and cloth beams, alternating warp threads, a weft strand and a visibly interlaced fabric sample; roller motion SHALL indicate feed in a consistent direction.

#### Scenario: A complete cycle
- **WHEN** the drive advances through two picks
- **THEN** the rollers advance consistently and the documentation distinguishes illustrative feed from simulated cloth accumulation.
