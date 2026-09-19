# Reconstructing the Milan hydraulic saw

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The pilot commissioned this reconstruction on 12 September 2026, replacing
the earlier simplified exhibit's scope. The additional instruction was:
“also, in the wheel in the museum the water goes under the wheel, not over”.
The machine therefore uses an **undershot waterwheel**, with water approaching
the lower paddles along the descending channel and leaving beneath the axle.

## Sources inspected

1. [Milan museum object page](https://www.museoscienza.org/en/collections/objects/hydraulic-saw),
   including all three photographs: overall, carriage/ratchet and lower drive.
   The object is inventory 37, attributed there to Arturo Uccelli, 1953.
2. [MUST catalogue IGB-37](https://collezioni-online.museoscienza.org/detail/IT-MUST-NTR001-008357/sega-idraulica).
   This identifies designer Arturo Uccelli and builder Alessandro Siriati,
   dates the model 1952–1953 and gives approximate dimensions of 785 mm wide,
   505 mm deep and 645 mm high. Materials include wood, iron and rope. Its
   description explicitly identifies the crank/rod, one-way pawl and toothed
   wheel, rollers and ropes, and the synchronized log carriage.
3. The same catalogue's photographs `IGB-000037_20090323_001..003`,
   `IGB-000037_20151123_001..002` and `IGB-000037_20190122_001..002`.
   The 2019 detail resolves the long diagonal rocker, short downward arm,
   hooked driving pawl and opposing holding pawl; the 2015 views expose the
   return pulley and lower drive. These are the construction references.
4. [Biblioteca Leonardiana, e-Leo, Atlanticus 1078r](https://www.leonardodigitale.com/en/browse/Codex-atlanticus/1078-r/).
   Inspected the complete folio image and transcription. The drawing shows
   the two-post saw, under-table wheel and the lever/ratchet arrangement,
   together with separate mechanism sketches. It supplies no usable complete
   set of manufacturing dimensions.
5. [Museo Leonardiano hydraulic saw](https://museoleonardiano.it/en/opera/hydraulic-saw/).
   Its independent 2010 reconstruction corroborates the wheel-driven saw and
   synchronized pawl, drum, rope and carriage. It is not the dimensional or
   construction reference for the Milan reconstruction.

All accessed 12 September 2026. The requested site renders its text and
photographs in JavaScript; research loaded that page in Chromium rather than
treating the initial empty HTML as the complete record. Full-resolution
catalogue images were reached through each image's `data-original` URL.
Private research downloads are under ignored `_reference/hydraulic_sawmill/`.
Museum photographs and manuscript scans are not redistributed in the gallery.

Leonardo recorded and studied an existing tradition of water-powered saws;
this is not presented as his invention. The Milan object is a twentieth-century
interpretative model, not an original Renaissance machine. The digital model
reconstructs its mechanisms; unseen dimensions and fittings remain our choices.

## Mechanism inventory and interpretation

| System | Evidence | Digital realization / confidence |
| --- | --- | --- |
| Undershot wheel and channel | All overall views, especially 2015 front | Eight paddle stations, lower run and sloping upstream trough; high confidence in topology and flow direction |
| Wooden wheel, spokes, square/keyed hub | Overall and lower-drive detail | Two rims/spoke planes, projecting paddles and keyed iron spindle; local fits dimensioned here |
| Shaft journals and crank | 2009 lower-drive detail, 2015 oblique | Supported axle, short crank web, retained eccentric pin and bored connecting rod |
| Two-post saw tower and sliding sash | Overall and manuscript | Continuous grooved upright guides with a lower journal slot, moving timber sash |
| Blade attachment and tension | Overall and 2015 oblique | Two pinned iron blade forks, upper threaded-stem envelope and hex tension nut; hidden screw form is inferred |
| Rocking feed lever | 2009/2019 mechanism detail | One rigid long lever and short arm, fixed table pivot, pinned tie to the saw's lower journal |
| Thin drive tie | Lower-drive detail, partly obscured | An eyed tie with 50 mm pin spacing; exact hidden seating is uncertain. It connects at the lower saw journal rather than a floating animation point |
| Driving and holding pawls | 2019 mechanism detail | Hooked moving pawl plus fixed-pivot retaining pawl; tooth-profile-derived seating, geometric engagement checked separately |
| Ratchet and spindle | Carriage and mechanism details | 32 asymmetric teeth and integral winding drum; tooth profile and clearances dimensioned here |
| Rope return | Overall and 2015 oblique | Rope winds on the ratchet spindle, travels to an end pulley, reverses and reaches the carriage. Exact groove lane and tie-off details are reconstruction choices |
| Carriage and timber | Overall and carriage detail | Four flanged rollers, retained axles, two cradles, side/end timbers and hauled attachment; a started central kerf clears the blade |
| Frame and supports | Overall views | Four-legged table, low stretchers, rails, two-post tower and bearing blocks; woodwork is fused as one display fixture |

This table accounts for the functional systems visible in the supplied museum
views. It does not certify hidden joinery or claim a measured replica of every
bolt, grain pattern or surface mark. The museum's overall envelope anchors the
model; internal dimensions are a mechanically checked reconstruction.

## Dimensions and physical relationships

Coordinates: +X is carriage advance; +Y follows the axle toward the feed
linkage; +Z is up. The channel approaches from +X and flows toward −X, so
positive wheel rotation carries the lower paddles downstream. Axle height is
120 mm. The wheel has 80 mm rims and projecting paddle tips at about 92 mm;
water is shown below those tips. The revised plinth is 875 × 505 × 18 mm and tower
height is 645 mm.

The crank throw is 24 mm, the connecting rod 146 mm and the saw stroke 48 mm.
These are reconstruction dimensions, retained where useful from the former
exhibit. The sash is 300 mm high. A 235 mm rocker and 50 mm tie form a closed
link with the lower saw journal. Circle intersection determines the rocker
angle; its approximately 49.917 mm short arm is solved so the 75 mm driving
pawl's contact circle traverses one 11.25° tooth pitch between dead centers.

The ratchet has 32 teeth. Rope centerline radius is 23.4 mm; winding pitch
is 3.2 mm per drum revolution. Approximately 4.60 mm feed per waterwheel
turn gives 340.062622 mm over the 74-turn, 296-second pass. The exact
carriage law includes helical take-up and the changing lower-span fleet
angle. The 0.9 mm rope radius leaves 0.3 mm radial running clearance.

Following the pilot's proportion and tight-fit corrections, the timber is
320 mm rather than the original 350 mm (the short 100 mm trial was rejected).
The carriage grows from 360 to 420 mm, table from 610 to 720, and rails from
650 to 760. Cradles stand at +/-120 mm; axle stations at +/-185 mm remain
outside the blade throughout. Timber centre starts at X=-171 mm, leaving
1 mm leading-face clearance and about 4.06 mm trailing-face clearance at
completion. The tower and waterwheel proportions are retained.
The return pulley moves to X=400 mm; the winding drum is locally wider.
Initial winding is 15° and final winding 847.5°, in separated helical turns.
These are educational reconstruction choices, not newly discovered museum
measurements. Orderly winding is prescribed without a level-winding device.

Pawl recovery is a cam construction against the same polygon profiles used
by the CAD. Each recovery is sampled at 181 points; the first clear position
at 0.25 mm tooth clearance forms an interpolated seating table. The closed
pivot lengths remain exact at intermediate poses. This approximates gravity
seating geometrically rather than solving impact, spring or contact forces.

Bearing bores, spacers, pawl profiles, rope cleat and fastener forms are
construction choices. The model has no force solver: the drive laws enforce
closed geometric joints and one-way engagement, while gravity seating of
pawls, maintained rope tension and holding the log in its cradles are assumed.
The screw is shown at a set tension; thread load and blade strain are not solved.

## Operating sequence

Water turns the wheel continuously. Its crank pulls the rod and guided sash
through the downstroke, with the teeth facing the incoming timber. During
this cutting half, the holding pawl retains the feed wheel while the driving
pawl recovers. During the return stroke the tied rocker raises its short arm;
the driving hook takes one tooth and winds the haul rope. The end pulley
redirects that pull to draw the carriage toward the saw. The holding hook
rides the next tooth and seats for the next cut.

At a finished cut an operator must stop the water, release the pawls, unwind
the haul rope, return/reload the carriage and secure the timber for the next
board. The full-course viewer replay is labelled as a replay reset; it is not
an automatic reverse mechanism attributed to the historical saw. The visible
kerf in the rigid halves is filled ahead of the teeth by a shrinking molejo
insert: it illustrates progressive cutting, without material-removal or fluid physics.

## Verification status

See [full-pass-validation.md](full-pass-validation.md) for the current geometric
and browser certificate: default and both kerf limits pass 23 exact tests. The
mechanism inventory above is implemented. The historical confidence limits
remain: unseen dimensions and fittings are interpretations, not newly
discovered facts about Leonardo's drawing or the museum object.
