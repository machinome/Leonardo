## MODIFIED Requirements

### Requirement: Controllable demonstration
The model SHALL expose cycle phase, automatic playback and a small set of
stage instructions in the actual standalone browser export, within the tested
mechanical envelope and with views that reveal its transmissions.

#### Scenario: Inspect and resume
- **WHEN** a stage instruction completes
- **THEN** its phase remains held until Run restores motion, and returning to
  the same input reproduces the same geometry.

#### Scenario: Combined controls and replay
- **WHEN** manual phase and playback are used together or the replay restarts
- **THEN** the machine remains inside its tested travel and any winding reset
  is described visibly rather than attributed to an automatic reverse.

#### Scenario: One-minute simulation in Studio
- **WHEN** the maker opens the Python simulation in Studio
- **THEN** its existing four input turns and eight picks span 60 seconds of
  machine time and the native viewer offers slow-motion speed controls,
  without changing the mechanical ratios, winding travel or phase controls.

### Requirement: Historical and verification evidence
The project SHALL identify primary historical sources, the later museum
interpretation, original reconstruction choices and omitted physics, and retain
accepted specifications, the completed OpenSpec record and reproducible
mechanical, visual and browser evidence.

#### Scenario: Reproduce the reconstruction
- **WHEN** a maker reads the README
- **THEN** they can build, test and open the actual reconstruction, understand
  its controls and trace each mechanical claim to evidence or an explicit
  construction choice.
