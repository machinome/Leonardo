# Milan hydraulic saw: reconstructed transmission

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Authority

The pilot's 12 September reconstruction commission and 20–21 September
corrections against Milan IGB-37 govern this design. The latest correction
explicitly places the lower pulley inside the fixed saw tower, requires winding on the slender ratchet axle just inside the gear, and keeps the compound winding shaft
inside the bed. Earlier single-rope and outboard arrangements are rejected.
See [reconstruction.md](reconstruction.md) for sources and historical limits.

The 24 September commission adds buildable fixed-frame carpentry without
changing that transmission. [carpentry.md](carpentry.md) owns its stock,
joinery, tool sequence, historical inferences and erection order.

## Mechanical arrangement

The waterwheel remains on negative Y. The blade teeth face positive X;
the carriage travels toward negative X. Water approaches along the channel
from positive X and passes beneath the wheel.

The round 12 mm iron wheel axle runs through wooden seats at Y=-207 and -32
to the square-fitted crank at Y=-13. Its end stops before the central saw
plane. The forked connecting rod works at Y=0; the feed tie and main rocker
occupy Y=12 and 22. The short arm reaches its adjacent pawl plane at Y=58.
The crank throw is 24 mm, rod length 146 mm and sash stroke 48 mm.
The 235 mm rocker, 50 mm tie and approximately 55.820 mm short arm close
geometrically. The driving hook pulls on the downstroke. The holding pawl's
rollback reaction seats it.

The holding-pawl seating table follows the connected clear branch as a tooth
passes. A low landing is not sufficient: the falling pawl must not pass
through the departing tooth to reach it. The table uses a 0.25 mm running
clearance and a periodic neighboring-sample envelope, warmed through a tooth
before sampling the repeating branch. Both endpoints are identical, so roundoff
across a completed tooth cannot alternate raised and dropped poses during dwell.
The pilot exposed that chatter on 21 September. The tip reach is fitted at
`START_CONTACT + 10 tooth pitches + 3 degrees` (41.425 mm pivot-to-tip),
instead of the earlier +1 degree / 42.602 mm reach, so the tooth clears before
the return stroke. The fixed pivot is unchanged. Rollback contact is measured
on the actual faces within the existing 5-degree play bound, not assumed at
2.5 degrees. This models geometric seating, not gravity, impact or friction.

The fixed timber structure exposes two separate assemblies in the tree:
**Horizontal bed frame** and **Fixed saw tower and shaft seats**. The latter
is the inner stationary vertical frame, not the moving sash. The lower
drive-rope pulley is journalled in the positive-Y tower upright, on its
inward face, opposite the wheel. The compound shaft is carried by the existing
end legs. No wooden pulley bracket, piled upper rail, end-member notch,
hanging iron haul strap or outboard winding train remains.

The running rails are continuous through the saw plane. Both ends of the
moving carriage join its side timbers; neither end member crosses the blade
during the pass. Slotted log cradles retain their kerf clearance.

## Two-rope transmission

```text
waterwheel → central crank/rod → saw sash → tie/rocker → pulling hook
                                                          ↓
                                                    32-tooth ratchet
                                                          ↓
bare axle, stacked radial coil → rope 1 → lower tower pulley → large winding section
                                                          ║ same shaft
carriage, top centre ← upper roller ← rope 2 ← thin central winding section
```

The bare ratchet axle radius is 5 mm; rope radius is 0.9 mm with 0.3 mm
display/running clearance, giving a 6.2 mm rope pitch radius. There is no
large drum or pulley on that axle. Following the pilot's additional correction, its winding remains at Y=52 mm,
just inside the gear's Y=55 mm inner face. Each turn builds on the previous
turn instead of traversing the axle into the rocker. Radial pitch is 1.82 mm:
the 1.8 mm rope diameter plus 0.02 mm modeling clearance. The initial wrap is
15 degrees. This is an orderly-stacking assumption, not a stability result. The through-bore rope tie stays at one axial
station and rotates with the shaft.

The lower pulley centre is (0,50,120) mm, with rope pitch radius 11.4 mm;
its pin seats in the tower upright at Y=78. The compound shaft centreline
is X=-335, Z=285 mm. Its large winding section, centred at Y=68, has rope
pitch radius 26.4 mm and a 7.5-turn initial reserve. The central take-up
pitch radius is 7.2 mm, initially carrying half a turn. Both use 3.2 mm lead.
The upper roller is at X=-370, Y=0, Z=340, pitch radius 7.4 mm, in the
existing rail ends. The carriage rope attaches through its front wooden
crossmember at Y=0, Z=370. Its entire hauling leg remains on that centreline.

The effective input radius grows from about 6.276 to 27.050 mm. A tooth's
take-up grows with it; a fixed input radius is no longer appropriate.
The compound shaft's large/small pitch-radius ratio is `26.4 / 7.2`.
Neither an independent feed factor nor a desired display duration determines
the carriage motion. The exact geometric law additionally accounts for
radial-spiral length, output helical length and changing free spans:

- Input spiral length gain plus changes in its tangent span and lower-pulley
  wrap equals
  large-section unwinding minus the change in the idler-to-shaft span.
- Central take-up plus the change in its descending span equals the
  shortening of the top hauling span and upper-roller wrap.

Six fixed-point steps solve tangency from the growing input spiral to the
lower pulley. Twelve-point Gaussian integration evaluates its length using
exportable arithmetic and square roots; tests use an independent asinh
antiderivative. A 512-segment spline renders the spiral, with four samples
per segment and measured radial error below 0.002 mm.
The lower-idler bend uses a 16-segment spline with six samples per segment.
Its centreline stays within 0.001 mm of the pulley circle and its measured
arc length within 0.001 mm of the circular length. This supported flexible
sweep avoids an analytic-conversion failure of the non-coplanar Line–Arc–Line
form, without changing the route or relaxing either rope's length contract.
The spline B-rep reports its own 1e-6 mm approximation tolerance; it is not
claimed to be an analytic torus.
Four fixed Newton steps solve the compound-shaft length equation; six solve carriage
position from output length. The same degree expressions are exported to
the viewer. Independent mesh measurements check both conserved rope lengths.

The selected dimensions produce 0.334454 mm on the first waterwheel turn.
Feed per turn changes with the growing input radius and hauling angle; it is not labelled constant.
The first whole tooth completing the required 339 mm travel is tooth 365:
341.017588 mm of carriage travel, at four seconds per wheel turn,
**1460 seconds (24 minutes 20 seconds)**. The 320 mm billet starts 1 mm
before the teeth and finishes 5.017588 mm beyond the blade's back.
The last whole-tooth advance is not used to tune a speed factor.

## Representation and limits

All internal dimensions, winding leads, reserve lengths, knot envelopes,
bore fits and concealed fasteners are reconstruction choices, not museum
measurements. Knots are compact rope-coloured termination envelopes through
bores, not iron attachments. Journals have explicit running play and
retaining collars. End-shaft working sections lie between the timber legs.

Ropes are inextensible, taut and orderly wound in this kinematic model.
They can fleet at the sheave and winding contacts; the short entry/exit
bends are represented by joined segments. No grooved level-winder is invented.
The model does not predict winding stability, slip, slack, tension, wood
deflection, cutting forces, water power or fastening strength.

The timber's uncut kerf is a shrinking flexible insert ahead of the teeth.
Its last 0.1 mm collapses to zero area. That visual cutting impression is not
material-removal physics. The log is assumed secured in its cradles.

## Controls and evidence

The working saw's only motion control is the complete-pass timeline. Kerf is the sole build
parameter: 2–5 mm, default 3.2. Playback speed changes presentation rate only;
the elapsed-time display retains the machine's four-second wheel period.
A replay reset is labelled and never attributed to automatic historical return.

The separate frame study reuses all 24 stationary timbers and 34 pins, with
a reversible 0–11 disassembly control and twelve numbered stage buttons.
It shows unloaded placement and access; the moving machinery must be removed
before dismantling the surrounding frame. Its cutting book is generated from
those same exact solids and feature records, not a second illustrative model.

Five camera views, frame reveal and a navigable assembly tree expose the
actual exported CAD. Labels interpolate 721 first-cycle measurements and
2921 full-pass feed samples taken from CAD meshes; they do not place parts.

Whole-root non-interference and connectedness remain mandatory. Separate
contracts check force planes, supports and retention, hook/holding contact,
fixed-plane radial winding, moving-rocker clearance, both rope lengths and clearances, frame continuity, and the
complete timber course. See [transmission-validation.md](transmission-validation.md)
for results and [evidence/](evidence/) for inspected CAD renders.
