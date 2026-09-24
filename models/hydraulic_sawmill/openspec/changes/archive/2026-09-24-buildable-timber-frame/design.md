## Context

Authority: the pilot's current commission, not another gallery queue item.
Continue with: “Complete buildable-timber-frame: separate and join the fixed
timbers, prove the fits and erection, preserve the working mechanism.”
Baseline source is Leonardo `9729d2e`. The independent project is clean;
no other sawmill editing process was found. Ordinary project design and
local commits are delegated by AGENTS.md and this implementation request.

Inspected Milan overall, 2015 front and oblique, 2009 mechanism, and lower
drive photographs in `_reference/hydraulic_sawmill/`. Crossmember end grain,
housed intersections, unbraced rectangular bed, paired grooved uprights,
top crosshead and stepped wooden bearings are visible. Concealed mortises,
peg layout, stock species and all joint dimensions are reconstruction choices.
Sources and full cut schedule will be recorded in `docs/carpentry.md`.

## Goals / Non-Goals

Complete the fixed timber bed, tower, feed-bearing blocks and shaft seats
as individual cuttable members with matched joinery and real fasteners.
Keep the 645 mm tower, rail contact surfaces and every moving shaft/guide
datum. Explain hand-tool cutting and a feasible assembly order at the
existing museum-model scale. The display plinth is the ground fixture.

Moving wooden components and channel carpentry are subsequent work. No
fluid/force solver, wood constitutive model, full-size mill foundation or
load-rating claim is added. No new framing invented just for symmetry.

## Decisions

- Use shouldered mortise-and-tenon joints for lower stretchers, housed/lapped
  crossings for top members, and separate hardwood pegs. Opposing joints in
  corner posts must not erase each other's tenons. Peg bores are aligned in
  the geometric model; drawboring and elastic interference are not simulated.
- Keep the two familiar bed/tower groups as assemblies. One rigid leaf is
  one timber or peg. The shaped axle-bearing blocks become removable parts
  with seated feet, replacing fused connections and the artificial thin
  connecting strip at the bottom of the tower.
- Define timber stock and machining features in a project-owned schedule;
  use it to locate parts and produce a cut list, never as the expected
  geometry in tests. Tests independently measure remaining walls, shoulders,
  clearances, peg capture and withdrawal after removing fasteners.
- Reuse exactly these leaves in a frame-only study. The working machine
  remains assembled; the study exposes joinery using explicit staged
  placements and the supported machinome controls. Document which stages
  handle complete subassemblies. Verify extraction paths against remaining
  members rather than claiming an arbitrary radial explosion is erection.
- Choose straight-grained oak timbers and riven oak pegs as an explicit
  period-plausible reconstruction specification, not an identification of
  the museum object's wood. Use saw, axe/adze, chisel, mallet and auger work.

## Risks / Trade-offs

- Thin scale-model members → offset intersecting joints, retain measured
  cheeks, use localized housed joints and verify single connected solids.
- Hidden historical joinery → distinguish photographic observations from
  inferred fittings; do not label an invented dimension “Leonardo's.”
- Dense existing transmission → keep its contracts and complete motion
  sweep, test boundary kerfs, and inspect actual CAD snapshots.
- A fit is not a strength result → prove geometric support/retention and
  construction access, state that shrinkage, fatigue and full-size loads
  remain unmodeled.

## Migration Plan

Commit planning, add a failing independent frame contract, implement and
verify incrementally, export and inspect the real viewer, update evidence,
sync the new spec and archive locally. Preserve the previous mechanism's
source and certificates as history. No publication or remote changes.

## Open Questions

No pilot decision is outstanding. Concealed joint details are delegated
working choices, revised if geometry or assembly evidence rejects them.

## Implementation findings

The completed layout has 24 timbers and 34 separate oak pins. Lower corner
tenons are staggered vertically; vertical pins have integral whittled heads,
recessed below running surfaces where needed. Positive seating allowances
of 0.1 mm eliminate coplanar mesh ambiguity without an interference epsilon.
The ratchet's existing underside running-rail relief is preserved.

The verified eleven-step extraction first withdraws pins, then removes rails
and the outer bearing, crosshead and top crossmembers; the side frames move
outward to release the transverse tenons. Tower pins withdraw toward −X,
away from F2. The outer bearing must leave early to clear the wheel-side
stretcher's later path. Those are geometric assembly findings, not arbitrary
explosion offsets. The reverse sequence erects the unloaded frame.

The plinth remains the explicit display ground. F1/B2 and F2/B2 need named
cantilever holds in the vertical-support solver; independent pin engagement
and ±2° tipping checks measure their actual capture. This is not a calculated
load rating. A1 rests on the plinth; A2 has a removable pegged foot in T1.
