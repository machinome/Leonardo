Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Context

The gallery has four completed machines and an existing flexible-part stack.
Queue 030 and this session's exact prompt (proposal.md) authorize its build.
No other process was found assigned to pulley_block; a floor session owns
cam_hammer, which this work does not edit. Existing screenshots are unrelated.

The [Museo Leonardiano object record](https://museoleonardiano.it/opera/tirare-composto/),
accessed 12 September 2026, identifies Madrid I f.36v and a 1979 reconstruction
with 33 pulleys. Its linked manuscript is the historical reference; dimensions
and the reduced mechanism here are original. The queue also cites
[Museo Galileo](https://brunelleschi.imss.fi.it/genscheda.asp?appl=LIR&chiave=100851&indice=63&lingua=ENG&xsl=paginamanoscritto);
the web reader could not decode that page during initial research. Do not
pretend this model reproduces 33 pulleys or establishes invention priority.

## Goals / Non-Goals

Demonstrate three supporting rope spans, invariant total rope length,
3:1 effort/load displacement, visible end attachments, captured rotating
sheaves and a coherent raise/lower loop. Deliver a readable original exhibit.
Exclude friction, tension solving, efficiency, certified capacity, elastic
rope, dynamic sway, realistic joinery and construction-ready rigging.

## Decisions

Use one plane XZ (Y=0) with separate side-by-side tangent lanes and three
distinct parallel Y axles. Coplanar staggered sheaves keep the entire route
visible without skew spans; coaxial sheaves in different depth lanes would
need additional fleet-angle geometry. The two fixed sheaves have centres
(-36,0,230) and (36,0,230) mm, the moving sheave (0,0,90+h).
Pitch radii are 18 mm. Four vertical lanes are x=-54,-18,18,54; the first
three support the moving block and the last is the effort. All dimensions
are educational choices and fixed for this exhibit; phase/run are the only
public controls, so there is no unvalidated size envelope.

The dead end makes a small 4 mm radius lower half-wrap around a pin at
(-58,0,106+h), then rises in the x=-54 lane. Its short 6 mm tail starts
at (-62,0,112+h), retained by a capped socket attached to the block.
The half-wrap and socket explicitly represent a secured end; no knot or
crimp force calculation is implied. The effort rope ends at (54,0,200-3h)
in a deep socket on a visible grip. The moving block carries a separate
weight through a pinned eye. Its support fixture is the timber stand;
ideal taut rope and a held effort end prescribe the vertical equilibrium.

The route is ONE molejo Shape with round 1.25 mm radius profile, alternating
lines and arcs, and parameter-bound heights. Its local origin follows the
dead tail. Four circular wraps (three sheaves and the anchor) add the
constant pi*(3*18+4) mm. Straight lengths are 6, 124-h, 140-h, 140-h,
30+3h mm; total length is 440+58*pi = 622.212373908 mm. Derive and verify
these values independently against the resulting geometry before evidence
is finalized. The rope bottom/sheave groove has a stated small running gap,
with flanges retaining it; no penetration is accepted to depict tension.

A smooth raised-cosine law moves h between 0 and 40 mm and back. Run blends
the static phase with the phase-plus-timeline pose, preserving bounds and
loop closure even for fractional run. Prismatic joints place block and
effort; relations enforce effort=-3h. Revolute joints follow no-slip travel:
first fixed +h/R, moving -2h/R, second fixed +3h/R radians about +Y.
The rope's ports receive derived coordinates and its origin follows h.

CadQuery authors connected fixture/carrier solids and turned grooved wheels.
Grooves, journals, collars, attachment depths and the separate load eye are
measured, including perturbations bracketing running play. Independent
mesh-ring centres recover the complete flexible route; segment lengths and
arc radii recover its length without using the model's kinematic helper.
Full-root rigid contracts remain active; flexible collisions, routing and
attachments receive separate tests. Deliberately replace the rope's local
effort-end height coefficient -4 with -3 to prove the geometry/length tests
detect a wrong reeving law; the rigid grip still travels the correct distance.

The exhibit embeds the real solid export. Read-only explanatory arithmetic
derives length labels from the viewer's displayed phase/run/timeline state;
the browser check compares those labels with independently measured Python
meshes. No JavaScript changes CAD or duplicates the viewer. During playback
labels are rounded to the displayed timeline frame and say so visibly.
Low/Mid/High/Run remain native instructions. Browser smoke verifies assets,
controls, motion, pose return and desktop/narrow layouts.

## Risks / Trade-offs

- A flexible route can be clear while its length changes → measure both
  length and endpoint displacement through the full cycle and all controls.
- A sleeve alone does not model a knot → show the anchor wrap and captive
  tail; declare the effort socket as a secured termination, not solved friction.
- Rigid support checks do not account for rope tension → test the actual
  rope attachments/capture and declare ideal suspension in the evidence.
- Finite samples miss behavior between samples → analytic length derivation,
  reversal neighborhoods and exact-kernel checks complement mesh sweeps.
- Parametric rope evaluator cost → faceted development, exact certification
  at completion; never suppress intersections with volume thresholds.

## Migration Plan

Add only this machine, then register it when its tests/build/export work.
Run existing exhibit regressions and all browser checks after root metadata
changes. Commit tested source, reference that commit in final evidence,
sync/archive, mark done and refresh source archives. No external publication.

## Open Questions

None requiring pilot input. Fit and presentation refinements remain ordinary
commissioned design choices and will be recorded with measured evidence.
