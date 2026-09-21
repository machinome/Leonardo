## ADDED Requirements

### Requirement: Photographed blade and feed handedness
The blade teeth SHALL face the incoming timber on the upstream side of the
fixed water channel, with the ratchet on that same side of the saw tower.

#### Scenario: Compare the three museum views
- **WHEN** the water channel and wheel fix the viewing orientation
- **THEN** the tooth edge, ratchet, carriage course and return pulley agree
  with the museum arrangement, without reversing the camera to imply agreement.

### Requirement: Pulling and self-seating pawls
The driving hook SHALL pull a tooth on its working stroke, and the fixed
holding pawl SHALL resist rollback through a reaction that keeps it seated.

#### Scenario: Follow a feed and recovery stroke
- **WHEN** the rocker pulls the driving hook
- **THEN** its working face draws the wheel through one tooth pitch and the
  holding pawl rides the passing tooth before retaining the wheel on recovery.

#### Scenario: Attempt rollback
- **WHEN** a seated wheel is displaced backward beyond its running play
- **THEN** its locking face encounters the holding pawl and the reaction
  about that pawl's actual pivot acts toward engagement.

#### Scenario: Remain seated after dropping
- **WHEN** the tooth has passed and the ratchet dwells during recovery
- **THEN** the holding pawl remains seated without oscillation at tooth-boundary
  wraps, in both the CAD poses and the exported animation, throughout the pass.

### Requirement: Supported iron transmission
The wheel SHALL drive a round iron shaft seated in timber, with a squared
end engaging the crank, and adjacent retained iron joints connecting the
crank, rod, saw and rocker within the frame. The second wooden bearing SHALL
carry the shaft just before its central crank, not beyond the saw plane.

#### Scenario: Inspect the lower drive
- **WHEN** the crank passes through a complete turn
- **THEN** the shaft remains captured by its timber bearings, the squared
  connection transmits rotation, and every iron eye remains on its journal
  without a wooden member bridging an axial displacement in the moving drive.

#### Scenario: Inspect the transverse load path
- **WHEN** the drive layers are viewed across the machine
- **THEN** crank, centered saw connection and feed rocker appear in order,
  without a far-side crank returning its main load through an extended pin
  or a duplicate horizontal frame timber hiding the ratchet.

### Requirement: Centered carriage traction
The hauling rope SHALL pull from the top center of the wooden carriage,
rather than rely on negligible guide friction or a hanging iron attachment
to tolerate an eccentric hauling force.

#### Scenario: Haul the complete timber course
- **WHEN** the carriage advances from the start to the end of the pass
- **THEN** the hauling leg and carriage attachment remain centered at the
  carriage, pass over the photographed upper roller and clear all moving
  and fixed parts throughout the course.

### Requirement: Preserve the photographed rectangular frame
The reconstruction SHALL retain a rectangular supporting frame and the
photographed upper-roller/lower-shaft arrangement, without an invented
outboard wooden extension or a rope-clearance notch in its end crossmember.

#### Scenario: Inspect the end rope transmission
- **WHEN** the end of the frame is compared with the museum overall views
- **THEN** the upper roller is supported at the rail ends and the lower
  transverse shaft between the end legs, with a continuous end crossmember
  and no support detour outside the frame.

#### Scenario: Inspect the inward rope train
- **WHEN** the ratchet and fixed saw tower are inspected from inside the bed
- **THEN** the first rope winds on the inward side of the slender ratchet axle without
  an added drum, remaining near the gear in one axial plane and building
  radially over its previous turns without crossing the moving rocker;
  the lower idler is carried by the inward face of the tower's
  opposite upright from the waterwheel, and the compound winding shaft's
  large and small working sections are inside the bed.

#### Scenario: Inspect the timber-carrying rectangles
- **WHEN** the fixed running rails and moving carriage are inspected
- **THEN** the rails remain continuous at the saw plane and both carriage
  end members join its side timbers, without removing material to avoid a
  blade that does not reach those members during the working course.

## MODIFIED Requirements

### Requirement: Complete visible transmission
The reconstruction SHALL include the museum's wheel, crank and rod, guided
and retained blade, rocking feed linkage, driving and holding pawls, ratchet
and slender winding axle, two-rope compound winding shaft, lower pulley,
upper roller and captured timber carriage as mechanically connected components.

#### Scenario: Follow the working machine
- **WHEN** the wheel is turned through a complete revolution
- **THEN** the connecting eyes remain captured, the rocker reciprocates without
  stretching its tie, the driving hook advances the ratchet on its pulling
  stroke, the holding pawl prevents reverse motion, and the two-rope reduction
  draws the carriage from its top centre.

### Requirement: Rope transmits carriage travel
Both ropes SHALL remain attached to their winding sections and carriage,
follow the lower pulley and upper roller respectively, and separately conserve
their total modeled lengths through the growing input coil and compound reduction.

#### Scenario: Inspect a complete pass
- **WHEN** the machine traverses the full timber course
- **THEN** winding, unwinding and free-span changes balance in each rope,
  pulley rotation follows rope travel, and the ropes clear the frame and
  moving feed links without axial migration of the input coil into the rocker.
