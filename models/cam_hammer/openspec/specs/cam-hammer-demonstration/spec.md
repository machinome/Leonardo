# Cam hammer demonstration Specification

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Purpose

Let visitors follow the contact, lift, release and strike of an original
educational cam hammer, using the actual machinome model and controls.

## Requirements

### Requirement: Readable complete hammer mechanism
The exhibit SHALL show a hand crank, cam, pivoted lever and hammer, anvil,
timber frame and journals with a readable rotary-to-intermittent power path.

#### Scenario: Inspect the assembly
- **WHEN** the visitor views the machine isometrically and along the shaft
- **THEN** the cam-to-tail contact and the hammer-to-anvil alignment are visible
- **AND** rigid components are connected, supported and mutually clear.

### Requirement: Engaged lift and released strike
The cam SHALL engage the tail during lift, then release the hammer for a
bounded return that lands on the anvil face without penetration.

#### Scenario: Complete cycle
- **WHEN** the visitor advances through a full revolution
- **THEN** intermediate lift positions follow the cam's contact envelope
- **AND** the pivot stays captured, the hammer clears the frame, and a visible
  released interval precedes the strike.

#### Scenario: Advertised size envelope
- **WHEN** the model is built at either limit of its advertised lift adjustment
- **THEN** lift engagement, release, capture and clearances remain valid.

### Requirement: Operable export
The exhibit SHALL provide phase/run controls and Lift, Release, Strike and
Run instructions in its real machinome viewer on desktop and narrow screens.

#### Scenario: Inspect and return
- **WHEN** a visitor plays, manually poses, selects named stages and returns
  to an earlier pose
- **THEN** the visible geometry follows those controls, returns consistently,
  and the page loads all required assets without browser errors.

### Requirement: Honest historical and simulation claims
The exhibit SHALL identify Astra's original educational reconstruction,
its historical sources, the machinome demonstration and the gallery source.

#### Scenario: Read the exhibit's interpretation
- **WHEN** a visitor reads the exhibit
- **THEN** chosen dimensions and cam geometry are distinguished from historical
  evidence, with no invented folio or invention priority
- **AND** return timing and impact are explicitly illustrative, without a
  gravity, impact, material or manufacturing performance claim.
