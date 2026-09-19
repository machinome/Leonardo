# Full-course reconstruction choices

Authority: the pilot's two requests in this session. Ordinary dimensions,
presentation, verification and local commits are delegated by project AGENTS.md.

The pilot rejected the first 100 mm billet as visually too short. Use a
320 mm timber (originally 350), centred initially at X=-171 mm. Extend the
carriage from 360 to 420 mm, with axles at +/-185 and cradles at +/-120.
Extend the table from 610 to 720 mm and rails from 650 to 760 mm. The tower,
waterwheel and timber diameter retain their museum-inspired proportions.
Use tight clearances: the leading bark face starts 1 mm before the teeth,
and 74 indexed turns bring the trailing face just beyond the blade.

Allow four seconds per wheel turn: 296 seconds per full timeline. Declare
the duration on the model so live builds and standalone exports agree.
The longer course needs multiple rope turns: widen the drum locally and
wind a molejo helix with 3.2 mm pitch. The haul/return curve, lower straight span and winding are separate
flexible leaves meeting at their endpoints; total rope length includes
the helix and changing fleet angle. This is an analytic orderly-winding
approximation, not a simulated level-wind device. Check actual rope/cleat
clearances throughout the pass. Dimensions remain educational reconstruction
choices.

Group by frame, water drive, saw mechanism, timber carriage and feed mechanism;
subdivide timber and running gear where it helps selection. Keep physical
parts and motion relations intact. Remove drivers/instructions entirely.

Tests independently measure beginning/end clearance, cradle support and slot,
roller containment on rails, attached constant-length rope, full-course
integrity, local tooth transitions, timeline timing and empty input tables.
Inspect endpoint snapshots and both exhibit and native tree in the browser.

The pilot additionally requests a molejo insert between the timber halves.
A polygon sweep fills the uncut kerf and shortens at the incoming tooth plane
(X=-10.2 mm, 0.2 mm ahead of the teeth). This is a visual removal model,
not cutting physics. The sweep crosses the fixed kerf width: its path never
has zero length. Its polygon collapses to a line at completion, leaving
finite mesh vertices and zero visible area/volume. Molejo refuses a zero-length
Line path, so shrinking the path itself is unsuitable. The collapsed display
mesh is not an OCCT solid; endpoint tests inspect its mesh, not its B-rep.
