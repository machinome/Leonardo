<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
## Context

Five exhibits exist. This is the final machine before the static site.
The queue brief and continuation prompt delegate the following ordinary design
choices. This record is advance planning, not historical ratification.

## Goals / Non-Goals

Demonstrate independent slew, screw traverse and a continuous 2:1 hoist route.
Make the complete original mechanism readable at desktop scale. No dynamics,
brake/holding torque, worksite stability, load rating or historical dimensions.

## Decisions

- Fixed footing, captured vertical spindle and integral timber mast/jib.
  Mast axis is world Z; screw axis is the rotating jib's local X. The hoist
  travels with the trolley, so traverse does not consume hoisting rope.
  This deliberately modern simplification keeps the independent inputs legible.
- Nominal screw lead 12 mm, 60 mm trolley travel (radius 80–140 mm),
  slew ±60 degrees, hoist rise 0–25 mm. A single-start original thread mates
  with a clearance-cut nut; carriage rails prevent the nut rotating. Screw
  angle changes by minus 360 degrees per 12 mm traverse for its handedness.
  Implementation evidence rejected periodic helical surfaces: OCCT Boolean
  intersections disagreed with their meshes. The final thread uses explicit
  ruled stations every 20°, five points on each radial sector edge, spanning
  x=60–168 mm; the matching pocket retains the positive 0.4 mm clearance.
  This original geometric approximation keeps the same mechanism and lead.
  Demonstration dimensions are constants; no untested size knob is advertised.
- Rope route: trolley dead end → lower moving sheave → upper guide sheave
  → horizontal span → drum wrap → rotating drum termination. Route plane is
  offset from the screw and mast. Drum pitch radius 18 mm; initial wrap 90°;
  hoisting 25 mm stores 50 mm of rope, adding 159.15° wrap. Less than one
  turn avoids self-crossing and layer buildup. Drum termination follows the
  same angular law as the rope's endpoint. Winding and upright suspension
  are prescribed; no winding dynamics or tension solver is claimed.
- Three physical controls plus a demonstration blend. Four instructions
  set all three coordinates and stop automatic motion. A continuous closed
  trajectory lifts before swinging and returns to the starting pose. Any
  blend with manual settings remains inside the Cartesian tested envelope.
- Model-specific page embeds the real export. The viewer owns all geometry,
  controls and playback; page prose explains the power path and limits. The
  host mounts the shipped widget with a camera covering the swept envelope,
  widened and lowered on a narrow screen; fitting only the initial pose was
  observed to crop the jib after slewing.

## Risks / Trade-offs

- Helical fit errors → independent travel measurements plus free/blocked
  perturbations at multiple phases within one screw turn, and a sign mutation.
- Ancestor pose overwrites → mesh comparisons in mixed control states and
  return-to-pose tests in Python and the real browser.
- Flexible geometry is outside rigid integrity checks → measure rope seam
  positions, arc angles, total length, endpoints, clearance and self-separation.
- Cantilever loading → explicitly ground footing and identify ideal suspension
  and held coordinates; validate capture, do not infer a rated structure.
- Approximation error → faceted development checks followed by exact tests.

## Integration

Commit this planning record first. Build and verify in this machine directory;
then register the working model, regress all six roots and browser exhibits,
sync baseline specs, archive and mark the queue item done. Publish nothing.

## Open Questions

None requiring a pilot choice. Exact clearance and frame details will be
refined from geometry evidence while retaining these mechanisms and ranges.
