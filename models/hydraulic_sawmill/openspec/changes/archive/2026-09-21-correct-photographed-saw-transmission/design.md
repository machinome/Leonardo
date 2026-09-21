## Context

Authority: the pilot's 20 September 2026 request to improve the existing
reconstruction against `sega-idraulica.jpg`, `sega-idraulica1.jpg` and
`sega-idraulica2.jpg` at the Milan museum, including the follow-up to examine
how the wood holds the iron. All three originals were downloaded and inspected.
The gallery base is `5349757`; no other machine is in scope.

## Goals / Non-Goals

Reproduce the photographed handedness and supported mechanical chain, with
geometric evidence for pull, hold, capture and clearance throughout the pass.
Retain 320 mm timber, 48 mm stroke, 32 teeth, four seconds per waterwheel
revolution and kerf 2–5 mm. Derive pass turns and duration from the compound
winding transmission; the old 74-turn/296-second limit is withdrawn.
No force, strength, water or cutting simulation.

## Decisions

1. Keep water approaching from +X and the wheel on negative Y. Reverse the
   blade/carriage/feed arrangement about Z: the teeth face +X, the timber
   travels toward -X and the ratchet lies at positive X. This is a mechanical
   change, not a camera reversal. Apply consistent placements to the rope,
   carriage fittings and supporting timbers.
   The gear is across the timber from the wheel, but this does not put the
   main crank on the far side: the pilot explicitly rejected that intermediate
   interpretation. Main traction must stay central, with crank, saw and feed
   iron in that layer order. Remove the duplicate horizontal frame timber.
2. Keep the long rocker and its short downward branch shown in the last
   photograph. Its lower journal retreats from the tooth as the saw descends:
   that is the pulling stroke. Reverse the ratchet's working face and derive
   its motion from that closure; recover the hook while the holding pawl
   retains the wheel. The earlier return-stroke feed was an inference and
   is superseded by the pilot's explicit pull correction.
3. A collision with a frozen pawl proves too little. Verify the contact
   normal's moment about each pawl pivot as well as free play and blockage.
   The hook's working face must transmit tension; the holding pawl's reaction
   must seat it, not lift it. Preserve real journal holes and retained pins.
4. Bring the iron links into adjacent axial layers inside the frame. Extend
   the round input shaft to its inner wooden saddle, put a separate square-
   bored crank on its squared end, and retain the crankpin and link eyes with
   visible iron collars/bolts. Timber saddles and crossmembers support the
   shafts and fixed pivots; they do not bridge the moving transmission.
5. Preserve the rectangular frame and haul from the top center of the wooden
   carriage. The pilot rejected the hanging iron strap, outboard pulley
   bracket, cut end crossmember and single-pulley route. Do not retain these
   as hidden reconstruction choices. The upper roller is carried at the rail
   ends; the lower transverse shaft is supported between the end legs.
   Tangency, attachments, winding direction and conserved rope length must
   agree with carriage travel without relying on negligible guide friction.
   The previously specified single return leg fleeting to the ratchet drum
   is withdrawn pending source reconstruction.

## Confirmed rope-drive interpretation — 21 September 2026

Enlargements of the supplied overall view and catalogue photographs
`IGB-000037_20151123_002` and `IGB-000037_20190122_002` expose a central
rope wrap/tie on the lower cross-shaft and a pulley nearer one end of that
shaft. The pilot confirmed two ropes coupled by the common shaft, and
specified a drive rope descending from the ratchet around a lower redirecting
pulley then rising to the larger-radius winding section. The central haul
rope winds onto the thinner section and passes over the upper roller to the
carriage. The unequal radii reduce carriage travel per tooth. The pilot
explicitly requests the resulting longer cycle, with advancement and time
derived from physical proportions.

Use rope pitch radii (including rope thickness), actual tangent paths and
separate conserved rope lengths. One tooth determines input take-up, then
compound-shaft rotation and output take-up; the remaining hauling path
determines carriage position. No independent feed-speed multiplier or
manually stretched timeline is allowed. Keep the rectangular frame, with
the upper roller in the rail ends and reduction shaft journalled in the end
legs. The pilot's further correction places the lower idler on the inward
face of the fixed saw tower's upright opposite the waterwheel, not on an
end leg. The compound shaft and its large winding section remain inside
the bed. The first rope winds inward directly on the slender ratchet axle:
there is no added ratchet drum or pulley. These replace the rejected
outboard winding train. Initial rope reserves must cover the whole pass.

The fixed saw tower must be independently identifiable in the assembly tree,
distinct from the horizontal bed and moving sash. Preserve its woodwork and
the rectangular bed; identify the members rather than adding supports.
Account for winding lead and changing free-span lengths when calculating
the two rope transmissions. Do not reuse the rejected 259-turn/1036-second
result, which assumed a large input drum.

Implementation now follows this confirmed topology. The red-first top-haul,
rectangular-frame, bare-axle and inward-idler contracts pass on meshes. Earlier
single-rope/outboard snapshots remain superseded. Final acceptance still
requires the complete evidence gates; see docs/transmission-validation.md.

## Fixed-plane radial winding — pilot follow-up

The pilot identified that traversing the input rope along the axle crosses
its feed rocker. Keep the input coil close to the ratchet's inward face in
one axial plane, building over previous turns. Select the tangent consistent
with take-up in the working rotation, not a reversed display-only coil.
The growing radius changes the first transmission: derive spiral length,
contact tangency and lower-pulley wrap before solving the compound shaft
and carriage. The 967-turn axial-winding result is superseded.

The model assumes the rope maintains orderly radial stacking under tension.
A bare shaft does not establish lateral winding stability. Do not invent
flanges or a level-winder to imply a solved physical constraint.

## Risks / Trade-offs

The pilot's later 21 September inspection found holding-pawl chatter after
the drop. A non-periodic contact table let floating-point tooth-boundary
roundoff select poses about 6.9 degrees apart during a stationary return.
Warm the connected contact branch through a tooth and make its seam periodic.
Fit the tip reach so the departing tooth clears before dwell; preserve the
fixed pivot and prove locking contact within the existing play bound. Test
every recovery numerically and selected actual meshes/browser pixels. Do not
add a damping animation or hide the pawl to suppress the symptom.

Queued pilot follow-up, 21 September: the rectangular frame carrying the
timber has visible gaps and would not support itself as shown. After the
rope transmission, inspect those joins and restore a complete load-bearing
rectangle while retaining the blade's working clearance. A connectedness
test alone is not evidence of the intended rectangular structure.

- Static photos do not establish dimensions or forces → label chosen fits,
  prescribed gravity seating and the absence of force analysis explicitly.
- Correcting handedness and timing can invalidate otherwise sound rope tests
  → retain their independent length/attachment assertions with new geometry.
- Sparse phase sampling can miss tooth release → sample the tooth transitions
  densely, including neighborhoods, with both whole-root integrity checks.
- Existing evidence overstates holding → retain history but supersede its
  certificate with the new tests and deliberately failing geometry mutations.
