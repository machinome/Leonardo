<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
## Context

This is gallery queue 020, under the commission and exact continuation
prompt recorded in proposal.md. Three exhibits already exist. The lift is
original CAD, authored directly here, with no imported museum geometry.

The [Museo Leonardiano catalogue](https://museoleonardiano.it/en/opera/page/5/)
was retrieved on 12 September 2026. Its Rack and pinion record describes
a crank-driven vertical rack ending in a hook and cites Codex Atlanticus
f.998r. It credits its museum reconstruction to Fausto Colombo, Giovanni
Sacchi and Giorgio Valentini (1983). These establish the interpretation,
not historical dimensions or invention priority. The attempted object
URL `/en/opera/rack-and-pinion/` is checked separately; retain the catalogue
reference if that page does not expose the same record.

## Goals / Non-Goals

Goals: a complete open stand, observable conjugate tooth engagement,
captured journals and rack, connected hook/load, continuously reversible
travel and a compact public control surface.

Non-goals: historical replication, brake design, holding torque, lifting
capacity, friction, dynamics, joinery or a manufacturing-ready lifting tool.

## Decisions

- One root `module` length parameter, 3 mm default, 2.5–3.5 mm supported.
  It sets tooth size and proportionally sizes the stand. Clearances are
  explicit and derived; this is more useful than many unrelated knobs.
- Twenty modern 20-degree involute pinion teeth: pitch radius `10*module`,
  addendum `module`, dedendum `1.25*module`. Straight rack flanks are the
  conjugate modern counterpart. Sample the involute finely into an exact
  extruded polygon; disclose its chord approximation. Split positive
  tangential backlash between rack and pinion. Do not use rectangular
  decorative teeth or import a gear generator.
- Coordinates: vertical Z, shaft along Y, pinion centred at `(0,0,80*m)`.
  The rack lies to its right, backing from `11.25*m` to `16*m` in X,
  extends from `-48*m` to `36*m` relative to the pinion, and moves `24*m`
  (72 mm nominal). Guides sit at `64*m` and `102*m`, within the rack's
  overlap envelope throughout travel. Attached shoulders approach these
  guides at either travel end. The timber base and posts form a single
  grounded fixture; shaft collars provide axial capture.
- A rigid rack/hook fusion carries a separate weight with a perpendicular
  lifting eye resting in the open hook. This makes the connection visible
  and testable; no rope law or implied flexible contact is needed.
- Class-body revolute and prismatic joints plus a pinion-to-rack relation
  state the mechanism. The degree angle turns about -Y, with rack travel
  `angle*pi*10*m/180`. No separately authored viewer motion.
- Phase 0/90/180 degrees gives Bottom/Mid-lift/Top. Run blends the static
  phase position with the periodic phase+timeline position. Both use a
  half-cosine up/down law, so every advertised run value stays bounded and
  returns to the identical pose at the timeline boundary. The hand crank
  reverses through about 137.51 degrees each stroke; it does not rotate
  continuously in one direction. Phase/run and four native instructions
  are the entire runtime interface.
- Use the existing exhibit-page pattern and actual exported viewer.
  Keep the historical account, motion explanation and limits beside it.

## Risks / Trade-offs

- Involute sampling or phase error → mesh development plus final exact
  intersections and bilateral free/blocked tests over one full tooth pitch.
- Floating parts → whole-root connectedness; journal/guide capture;
  hook-eye seating; explicitly ground the frame and held crank for static
  load support. The operator's holding torque is outside the simulation.
- Endpoint collisions → full-cycle samples, reversal neighborhoods and
  all control combinations; independently measure rack and load motion.
- Browser expressions differ from Python → exercise actual export controls,
  compare CAD pixels for movement and exact pose return at two viewports.
- Other gallery sessions → isolate this model's build directories and
  preserve unrelated edits. Run all registered roots after registry changes.

## Migration Plan

Commit planning, write tests first, build and iterate, mutate the motion
relation and prove failure, restore and validate default/boundary sizes.
Inspect OpenSCAD snapshots and exported browser views. Commit source,
record that tested source revision, sync specs, archive and mark done.
Export committed source archives. No push or publication.

## Open Questions

No pilot decision remains within the brief. Exact tooth clearance and
hook-eye seating are engineering measurements to resolve during the build.
