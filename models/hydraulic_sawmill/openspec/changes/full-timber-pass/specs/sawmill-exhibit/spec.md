## MODIFIED Requirements

### Requirement: Controllable browser exhibit
A visitor SHALL control the actual model with animation timeline transport
only, including play, pause, speed and full-pass scrubbing; no machine input
drivers or instruction buttons SHALL be exposed. Views and reveal remain available.

#### Scenario: Inspect and resume
- **WHEN** the visitor scrubs within the full-pass timeline
- **THEN** the model and measured readouts follow that instant, playback can
  resume, and one complete pass lasts 108 seconds at normal speed.

### Requirement: Rigid integrity
Every rigid piece SHALL be connected and distinct rigid pieces SHALL remain free of shared volume across the sampled demonstration poses.

#### Scenario: Whole-machine regression
- **WHEN** the default and recorded boundary configurations are tested
- **THEN** the full-root integrity contracts pass, with the exact kernel providing the recorded certificate.

### Requirement: Honest reconstruction and source
The exhibit SHALL identify Leonardo's drawing and the later Milan museum
model, document reconstruction dimensions and uncertain hidden fittings,
explain all modeled mechanisms and omitted physics, and provide source/license.

#### Scenario: Read the model record
- **WHEN** a visitor opens the README or reconstruction note
- **THEN** it identifies Atlanticus f.1078r and MUST IGB-37, separates observed
  topology from dimensional and contact interpretations, and explains the
  illustrative water, started kerf and absence of cutting, fluid and force simulation.

#### Scenario: Retrieve source
- **WHEN** a visitor follows the source link after a committed gallery export
- **THEN** a downloadable source archive and the AGPL license are available.

## ADDED Requirements
### Requirement: Functional assembly navigation
The assembly tree SHALL group the machine by frame, water drive, saw mechanism,
timber carriage and feed mechanism, with readable names and timber/running-gear subgroups.

#### Scenario: Find a mechanism
- **WHEN** a visitor opens the tree and selects the timber or a feed component
- **THEN** the relevant physical parts are reachable under their functional group.
