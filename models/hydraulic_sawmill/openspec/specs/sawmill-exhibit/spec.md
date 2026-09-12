# sawmill-exhibit Specification

## Purpose

Provide an inspectable, exportable and honestly documented presentation of the hydraulic sawmill.

## Requirements

### Requirement: Controllable browser exhibit
A visitor SHALL be able to play, pause, change speed, scrub four cycles,
select mechanism views, reveal the drive and reset the actual exported model.

#### Scenario: Inspect and resume
- **WHEN** the visitor scrubs to 450 degrees and selects the feed view
- **THEN** geometry changes, the phase readout shows 90 degrees within the
  second cycle, the carriage shows one completed increment, the connected
  feed linkage is visible, and playback can resume.

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
