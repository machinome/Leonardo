# The sawmill's fixed timber frame

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

The 24 September 2026 commission asks for a buildable frame that demonstrates
carpentry as well as the already working mechanism. This design replaces the
two fused stationary timber groups with **24 individual timbers and 34 wooden
pins**. The same pieces appear in the working saw and the separate assembly
study. The moving sash, carriage, wheel and water trough retain their existing
construction; those are separate future carpentry increments.

## What the photographs show

The reference is Milan museum model IGB-37, designed by Arturo Uccelli and
built by Alessandro Siriati in 1952–1953. It is an interpretative model, not
a surviving Renaissance mill. The [museum catalogue](https://collezioni-online.museoscienza.org/detail/IT-MUST-NTR001-008357/sega-idraulica)
lists wood, iron and rope, and an approximately 785 × 505 × 645 mm envelope.
It does not identify the wood species or provide a cutting list.

Re-inspected on 24 September 2026:

- [Overall museum photograph](https://www.museoscienza.org/besrv/sites/default/files/2019-11/sega-idraulica.jpg):
  four table legs, long upper rails, low stretchers, exposed end grain of
  crossmembers, paired grooved saw uprights and a crosshead at their tops.
- [Lower transmission detail](https://www.museoscienza.org/besrv/sites/default/files/2019-11/sega-idraulica2.jpg):
  separate stepped wooden shaft seats and housed-looking bearer intersections;
  large dark heads on the upper rail belong to the iron mechanism, not evidence
  that every timber joint is bolted.
- Catalogue views `IGB-000037_20151123_001` and `002`: the rectangular bed from
  both sides, continuous running rails, crossmember ends and the tower/bed
  intersections. No diagonal bed braces are visible.
- Catalogue `IGB-000037_20090323_002`: the lower bearer and shaft seat close up.

Downloads remain private under `_reference/hydraulic_sawmill/`; the gallery
does not redistribute museum images. Leonardo's Atlanticus 1078r establishes
the machine study but supplies no complete frame manufacturing dimensions.

**Inferred here:** the concealed mortises, exact shoulder/tenon dimensions,
peg placement, head recesses, the removable bearing-foot connection and the
short tower-to-bed ties. These complete the photographed topology as a
cuttable structure. They are not claimed as joints measured on the museum
object or specified by Leonardo.

## Wood and available tools

Specify straight-grained oak for the timbers and riven oak for the pins.
Keep grain along each member's long direction and along a pin's shank;
avoid knots and short grain through tenons, cheeks and journal seats. Oak
is our plausible material choice, not an identification of the museum wood.

Richard Darrah's archaeological workshop presentation,
[The development of timber joints](https://holzverwendung.boku.ac.at/dokumente/secondworkshop/Darrah.pdf),
documents shouldered, pegged mortise-and-tenon work in medieval England,
prefitting and marking frames, hewing axes and spoon augers. It demonstrates
that the techniques predate Leonardo; it does not establish an Italian
regional joint tradition or this sawmill's concealed details.

Rough-hew stock with axe/adze, saw the shoulders and cheeks, remove mortise
waste with an auger and chisel, and pare to a trial fit. The grooves can be
sawn at their boundaries and cleared with a narrow chisel or plough plane.
Make the top housings and rebates with straight saw cuts and chisel work.
Bore journals through the temporarily assembled supports from an aligned
centreline. Pare pins from riven stock; a headed vertical pin is carved
from a larger blank, not made by gluing on a cap. No router pockets, plywood,
adhesives or modern screw fittings are needed for the modeled frame joints.

## Member families and joints

The generated [cutting book](../../../../export/hydraulic_sawmill-frame/carpentry/)
contains the exact stock envelope, all cut sizes and locations, four views
and a STEP file for every member. Coordinates are measured from that member's
blank corner. It also supplies separate timber and pin CSV schedules.

| IDs | Pieces | Construction |
| --- | --- | --- |
| L1–L4 | Four table legs | Shouldered upper tenons; staggered lower mortises. L1/L2 retain an offset head from a wider blank. L1/L3 carry the compound shaft journals. |
| B1–B2 | Two long upper side rails | Post-head mortises, top housings for end crossmembers, tower-tie mortises and iron journal/pivot bores. |
| S1–S2 | Two low long stretchers | High tenons at their ends; centre mortise for the tower bearer. |
| C1–C2 | Two low end crossmembers | Lower tenons into the legs, below the long stretcher tenons. |
| C3–C4 | Two upper end crossmembers | Housed ends above the rail shoulders; shallow seats for the running rails. |
| R1–R2 | Two continuous running rails | Pegged to the end crossmembers; roller journal at the return end. Pin heads are recessed below the wheel surface. |
| F1–F2 | Two feed-pivot bearers | Pegged tenons into B2; F1 also houses and pins R2. |
| T1 | Lower tower bearer | Tenoned into S1/S2, halved into the uprights, mortised for the inner shaft bearing. |
| T2–T3 | Two grooved saw uprights | Continuous guide faces and lower journal slots; lower side housings, upper bridle slots and outer tie mortises. |
| T4 | Tower crosshead | Drops into open-top bridle joints, retained by transverse pins. |
| T5–T6 | Two short shoulder ties | Connect the tower to the upper bed; preserve the open saw and rope course. |
| A1–A2 | Two stepped shaft-bearing blocks | Round journals; A2 has a pegged foot tenon in T1. A1 rests directly on the plinth. |

The two low tenons in each corner occupy different heights: the long
stretcher's neck is at Z=73–79 mm and the crossmember's at Z=64–70 mm.
They leave wood between the mortises and cannot cut each other away. The
short post-head tenon stays below the housed upper crossmember. Shoulders
and housing floors locate the assembly; pins secure withdrawal.

All dimensions remain at the established museum-model scale: 645 mm tower,
760 mm running rails and the unchanged moving-mechanism datums. This is a
buildable geometric model at that scale, not a full-size production mill
designed by multiplying every dimension by a scale factor.

## Fit and retention

The geometric assembly uses 0.15 mm clearance at mortise cheeks, 0.1 mm
nominal seating allowance at shoulders and 0.1 mm radial pin play. These
are explicit modeling fits, not a universal woodworking tolerance. Trial-fit
the actual wood, mark matched joints and fit the pins to the material.
The simulation does not deform a drawbored pin or represent a tapered
interference fit. Vertical pins have heads so their support does not depend
on assumed friction; horizontal pins use the normal fitted-wood retention
assumption, with no axial peg driving forces simulated.

Every pin must geometrically engage both named members. The frame tests
also check single solids, absence of shared volume, shoulders and necks,
guide/journal fits, the disassembly path and repeatable reassembly. The
working machine retains the complete course, tooth-transition, rope and
carriage clearance contracts, including the new separate pins.

The display plinth is the ground fixture. The support check identifies two
explicit cantilever holds, F1/B2 and F2/B2: their pegged-tenon moment reaction
is outside the framework's vertical-contact static model. Separate joint
geometry tests verify their capture; the declaration is not a strength
calculation. Wood shrinkage, bending, splitting, fatigue, water loading,
cutting loads and full-size foundation design remain outside this simulation.

## Assembly sequence

The study's slider runs from assembled (0) to separated (11); its named
buttons select stages. Reverse the sequence to erect the frame. Hold loose
members and support subassemblies on trestles while removing pins: the
study demonstrates placement and access, not freely falling timber.

1. Withdraw the wooden pins along their bores; pull tower pins toward the
   clear side, away from the feed bearers.
2. Lift the running rails from their shallow housings and lift the outer
   bearing clear of the path the wheel-side lower stretcher will take.
3. Lift the tower crosshead from the open bridle slots.
4. Lift the two upper end crossmembers.
5. Move the two long side frames outward together. This releases the lower
   crossmember ends, tower bearer ends, ties and feed bearer tenons.
6. Withdraw the short tower ties and feed-pivot bearers.
7. Move the grooved uprights sideways out of their open lower housings.
8. Lift the inner shaft bearing from its foot mortise; the outer bearing
   has already been removed.
9. Lift the lower end crossmembers and tower bearer.
10. Lift the upper side rails off the leg-head tenons.
11. Withdraw the legs from the long stretcher tenons.

For the complete machine, trial-fit the frame first, then fit shafts, sash
and rope transmission before closing their surrounding members. The frame
study excludes those mechanisms; its extraction path is not a claim that
the assembled waterwheel and all ropes can stay installed during dismantling.

## Reproduce

From the Leonardo repository root in the configured workspace environment:

```sh
python models/hydraulic_sawmill/scripts/demo.py --build-only
machinome test models/hydraulic_sawmill/frame.py --mesh
machinome test hydraulic_sawmill --mesh
machinome test models/hydraulic_sawmill/frame.py --brep
machinome test hydraulic_sawmill --brep
```

The finite build writes the working export, the frame study at
`export/hydraulic_sawmill-frame/`, and its `carpentry/` cutting book. Serve
the repository over HTTP as documented in the machine README. The book's
SVGs are illustrations rather than print-to-scale templates; its machining
coordinates and STEP solids are the dimensional records.
