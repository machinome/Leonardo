<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Rack lift demonstration

## Purpose

Make the conversion from crank rotation to guided vertical lift inspectable
through an original educational model, with measured engagement and clear
historical and mechanical limits.

## Requirements

### Requirement: Readable rack lift
The exhibit SHALL show an open timber stand, hand crank and pinion,
vertically guided toothed rack, open hook and demonstrator weight. Their
visible arrangement SHALL communicate a continuous power path to the load.

#### Scenario: Follow a lift
- **WHEN** a visitor turns the crank through the demonstrated lift
- **THEN** the meshing teeth move the rack and attached weight vertically
  by the distance implied by the pinion's pitch circumference and turn
- **AND** the rack stays captured, the journals stay seated and all rigid
  parts remain connected individually and free of mutual penetration

### Requirement: Engaged and bounded movement
The lift SHALL retain tooth engagement with positive backlash throughout
its advertised size and movement envelope. The weight SHALL remain seated
on its hook, and travel SHALL remain clear of the stand and travel stops.

#### Scenario: Reverse at the end of travel
- **WHEN** the lift reaches either end and the crank reverses
- **THEN** the rack raises or lowers continuously without tooth jumping,
  leaving its guides, passing a stop or resetting invisibly

### Requirement: Inspectable controls
The exhibit SHALL offer phase and run controls, Bottom, Mid-lift, Top and
Run instructions, and one useful build-size parameter. Visitors SHALL be
able to play, pause, scrub and return to a previously inspected pose on
desktop and narrow screens.

#### Scenario: Inspect and resume
- **WHEN** a visitor selects Top, returns manually to Mid-lift and runs
  the animation through a complete loop
- **THEN** the real model shows those poses, the loop closes continuously,
  and its controls and explanatory text remain usable

### Requirement: Honest educational provenance
The exhibit SHALL cite its museum source and distinguish Leonardo's study,
the later museum reconstruction and Astra's original dimensions and modern
teeth. It SHALL identify solid-node, Astra's single-prompt design credit,
the gallery source and AGPL copyright. It SHALL disclose that brake,
holding torque, lifting capacity and dynamics are outside the demonstration.

#### Scenario: Read the exhibit limits
- **WHEN** a visitor reads the exhibit and machine record
- **THEN** the historical basis, chosen geometry, controls, measured
  evidence and limitations are available without implying a load-rated tool
