# Leonardo's hydraulic sawmill

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

## Intent and evidence

An original, browser-viewable mechanical reconstruction inspired by Leonardo's
Codex Atlanticus, folio 1078r. Reference: the Museo Leonardiano hydraulic saw
model, https://museoleonardiano.it/en/opera/hydraulic-saw/ . The museum describes
a waterwheel driving a reciprocating saw and a synchronized pawl/ratchet winding
a rope to advance the timber carriage. No museum geometry or photographs are
redistributed. Dimensions, bearings and construction details here are project
interpretations, not a claim to reproduce an original engineering drawing.

## Demonstration envelope

Millimetres; X follows the timber feed, Y follows the waterwheel shaft, Z is up.
A 200 mm wooden paddlewheel drives a 48 mm saw stroke through a 146 mm connecting
rod. The saw sash slides vertically, with a blade in the XZ plane. A timber
carriage advances on two rails, in the return half of each saw cycle. A pre-cut
longitudinal slot in the timber clears the blade throughout the demonstration.

The machine is a kinematic exhibit. It does not solve water forces, torque,
friction, cutting, fibre fracture or wear. Water is a decorative rigid surface;
the inlet flume is scenic interpretation. The pawl return is explicitly driven,
not a contact-dynamics solution. The carriage can be reset for another pass.

## Construction and control

Exact CadQuery solids, solid-node assemblies, declared joints, and symbolic
degree-based motion. Geometry is built once and motion evaluated in the viewer.
Root inputs expose phase and playback contribution. Timeline playback runs a
bounded four-cycle pass; the phase control permits inspection without playback.
Named instruction buttons provide useful poses and a complete pass.

The main crank and rod must remain connected geometrically at every pose. The
saw must stay in its guides, clear the log slot, and make a 48 mm stroke. Feed is
monotonic, dwells during the downstroke and advances on the return. Every rigid
piece must be connected; distinct pieces must not overlap across sampled poses.
All decorative solids are subject to the same integrity checks.

## Finish and delivery

Warm timber, charcoal iron, light end grain and muted blue water, with an open
structure so the power path reads from an oblique view. Ship source, licence,
tests, measured validation notes, OpenSCAD inspection images and an actual
solid-node browser export. Generated mesh/export artifacts remain ignored.
