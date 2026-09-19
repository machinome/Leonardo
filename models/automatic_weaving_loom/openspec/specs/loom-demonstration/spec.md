# loom-demonstration Specification

## Purpose

Provide a usable and honestly documented machinome demonstration of Leonardo's loom, with tested rigid geometry and inspectable motion.

## Requirements

### Requirement: Controllable demonstration
The model SHALL expose a cycle-phase control, automatic playback and a small set of named stage instructions, retaining motion in a standalone browser export.

#### Scenario: Inspect and resume
- **WHEN** a stage instruction completes
- **THEN** the model lands on its stated phase with playback held, and the Run instruction restores automatic motion.

### Requirement: Mechanical integrity
Each rigid part SHALL be a single connected solid and distinct rigid parts SHALL remain non-interpenetrating across the demonstrated cycle.

#### Scenario: Geometry regression
- **WHEN** the complete model is checked at the recorded cycle samples and instruction trajectory
- **THEN** connectivity and whole-model rigid interference contracts pass without volume epsilon.

### Requirement: Historical and verification evidence
The project SHALL identify online design sources, distinguish design assumptions and omitted physics, and retain OpenSpec planning, accepted baseline specs and verification evidence with the completed implementation.

#### Scenario: Reproduce the demonstration
- **WHEN** a maker reads the README
- **THEN** they can build, test and open the demonstration, understand its controls, and identify which historical features and kinematic limitations it represents.
