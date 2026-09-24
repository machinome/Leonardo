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

### 24 September 2026 carpentry commission

The pilot asked to replace the single-piece frame with buildable period
carpentry while preserving the reliable mechanism. Overall and lower-drive
museum images, both 2015 catalogue views and the 2009 bearing close-up were
re-inspected. [carpentry.md](carpentry.md) separates photographed members from
inferred joints and records the pre-Renaissance joinery evidence. The result
is 24 cut oak members and 34 separate pins, including staggered corner tenons,
housed crossmembers, a bridled crosshead and separate shaft seats. Oak and
the hidden joinery are reconstruction choices, not museum identifications.

### 20–21 September 2026 correction

The pilot identified errors by comparing the [overall photograph](https://www.museoscienza.org/besrv/sites/default/files/2019-11/sega-idraulica.jpg),
[blade and ratchet detail](https://www.museoscienza.org/besrv/sites/default/files/2019-11/sega-idraulica1.jpg)
and [lower iron transmission and wooden support](https://www.museoscienza.org/besrv/sites/default/files/2019-11/sega-idraulica2.jpg).
These three files were downloaded and inspected again for this correction.
The teeth were reversed, the gear's side was wrong, the hook must pull, and
the holding pawl needed a seating reaction rather than just a frozen collision.
The last view shows the round iron axle, its squared crank connection, the
adjacent bolted iron layers, and a shaped wooden bearing on a timber bearer.
The pilot further specified the gear opposite the waterwheel across the
timber and an extended axle with a second wooden support. These observations
supersede the earlier drive placement and operating-sequence interpretation.
Chosen bore sizes, stepped bearing outline and joint clearances reproduce
that topology, not measured museum joinery or certified load capacity.

The pilot then clarified the load-bearing layers: crank, saw, then feed
rocker, with the saw pulled in the middle. The intermediate far-side crank
and long return pin were rejected. So was the side rope haul and the extra
horizontal timber piled above the frame rail. The final crank stops before
the center plane; a centered forked rod drives the saw and a nearby iron tie
takes off feed motion. The rope's hauling leg and carriage attachment are
centered at the top of the carriage. The pilot then identified the two-rope
reduction: the first rope winds directly on the slender ratchet axle just inside the gear,
passes down around a pulley on the inward face of the opposite fixed saw
upright, and rises to the large winding section of the lower cross-shaft.
That shaft's thin central section winds a separate hauling rope over the
upper roller. The compound shaft is entirely inside the bed. This supersedes
the rejected single-rope drive, hanging strap, wooden outrigger, notched
crossmember and outboard reduction. The queued frame correction restores
continuous running rails and both carriage end members. The pilot then
identified that axial winding crossed the feed rocker. The input rope now
builds radially over itself in one fixed plane close to the gear; its growing
radius changes the feed law. No extra support
is invented to route around the rectangular frame.

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
| Ratchet and spindle | Carriage and mechanism details | 32 asymmetric teeth, slender bare iron axle and fixed-plane radial winding; tooth profile and clearances dimensioned here |
| Two-rope reduction | Supplied overall/lower views, enlarged 2015/2019 details and pilot's confirmed interpretation | Lower idler inside the saw tower; large and thin winding sections on the inboard compound shaft; separate carriage rope over upper roller. Winding leads, diameters and through-bore ties are choices |
| Carriage and timber | Overall and carriage detail | Four flanged rollers, retained axles, two cradles, side/end timbers and hauled attachment; a started central kerf clears the blade |
| Frame and supports | Overall views; lower-drive and 2015/2009 details | Four-legged table, low stretchers, rails, two-post tower and bearing blocks; bed and tower now contain individual cut members and matching wooden pins. Hidden joints are inferred |

This table accounts for the functional systems visible in the supplied museum
views. It does not certify hidden joinery or claim a measured replica of every
bolt, grain pattern or surface mark. The museum's overall envelope anchors the
model; internal dimensions are a mechanically checked reconstruction.

## Dimensions and physical relationships

Coordinates: -X is carriage advance; +Y follows the axle toward the feed
linkage; +Z is up. The channel approaches from +X and flows toward −X, so
positive wheel rotation carries the lower paddles downstream. Axle height is
120 mm. The wheel has 80 mm rims and projecting paddle tips at about 92 mm;
water is shown below those tips. The revised plinth is 875 × 505 × 18 mm and tower
height is 645 mm.

The crank throw is 24 mm, the connecting rod 146 mm and the saw stroke 48 mm.
These are reconstruction dimensions, retained where useful from the former
exhibit. The sash is 300 mm high. A 235 mm rocker and 50 mm tie form a closed
link with the lower saw journal. Circle intersection determines the rocker
angle; its approximately 55.820 mm short arm is solved so the 75 mm driving
pawl's contact circle traverses one 11.25° tooth pitch between dead centers.

The ratchet has 32 teeth. Its bare axle radius is 5 mm, with a 6.2 mm rope
initial core pitch radius. Input turns stack at 1.82 mm radial pitch rather
than travel axially; the outer rope centre reaches 27.050 mm radius. The compound shaft's large and small
pitch radii are 26.4 and 7.2 mm, both at 3.2 mm lead. Rope radius is 0.9 mm,
with 0.3 mm radial running clearance. Separate conserved-length equations
include radial input buildup, output helical take-up and changing tangent
spans/pulley wrap. The first waterwheel
turn gives 0.334454 mm feed; the complete pass takes 365 turns at four seconds
per turn: 1460 seconds and 341.017588 mm travel. These are results of the
chosen geometry, not measured historical cutting performance.

Following the pilot's proportion and tight-fit corrections, the timber is
320 mm rather than the original 350 mm (the short 100 mm trial was rejected).
The carriage grows from 360 to 420 mm, table from 610 to 720, and rails from
650 to 760. Cradles stand at +/-120 mm; axle stations at +/-185 mm remain
outside the blade throughout. Timber centre starts at X=+171 mm, leaving
1 mm leading-face clearance and about 5.02 mm trailing-face clearance at
completion. The tower and waterwheel proportions are retained.
The lower redirecting pulley is at (0,50,120) mm, the compound shaft at
X=-335, Z=285, and the upper roller at (-370,0,340). Input winding begins
with 15°, the large section with 7.5 reserve turns, and the thin take-up
with half a turn. Coils stay separated throughout the pass.
These are educational reconstruction choices, not newly discovered museum
measurements. Orderly winding is prescribed without a level-winding device.

Pawl recovery is a cam construction against the same polygon profiles used
by the CAD. Each recovery is sampled at 181 points; the first clear position
at 0.25 mm tooth clearance forms an interpolated seating table. The holding
pawl follows the connected clear branch rather than jumping through a tooth
to a lower clear landing. A neighboring-sample envelope protects release.
The closed
pivot lengths remain exact at intermediate poses. This approximates gravity
seating geometrically rather than solving impact, spring or contact forces.

Bearing bores, spacers, pawl profiles, rope tie bores and fastener forms are
construction choices. The model has no force solver: the drive laws enforce
closed geometric joints and one-way engagement, while gravity seating of
pawls, maintained rope tension and holding the log in its cradles are assumed.
The screw is shown at a set tension; thread load and blade strain are not solved.

## Operating sequence

Water turns the wheel continuously. Its crank pulls the rod and guided sash
through the downstroke, with the teeth facing the incoming timber. The tied
rocker's short arm retreats from the gear, pulling the driving hook and
advancing one tooth. The holding pawl rides the passing tooth and drops
behind its locking face. On the upstroke it retains the wheel while the
driving hook recovers. Radial winding beside the gear on its slender axle pulls the
first rope around the lower idler and unwinds the large winding section.
The same shaft's thin centre winds the second rope, which passes over the
upper roller and pulls through the top centre of the wooden carriage.
The two winding radii reduce the haul distance; no independent feed factor
or artificially stretched timeline is used.

At a finished cut an operator must stop the water, release the pawls, unwind
the haul rope, return/reload the carriage and secure the timber for the next
board. The full-course viewer replay is labelled as a replay reset; it is not
an automatic reverse mechanism attributed to the historical saw. The visible
kerf in the rigid halves is filled ahead of the teeth by a shrinking molejo
insert: it illustrates progressive cutting, without material-removal or fluid physics.

## Verification status

See [carpentry-validation.md](carpentry-validation.md) for the current frame,
mechanism regression and browser evidence. [transmission-validation.md](transmission-validation.md)
records the preceding correction. The earlier [full-pass certificate](full-pass-validation.md)
is retained as history, not certification of the corrected drive. The
mechanism inventory above is implemented. The historical confidence limits
remain: unseen dimensions and fittings are interpretations, not newly
discovered facts about Leonardo's drawing or the museum object.
