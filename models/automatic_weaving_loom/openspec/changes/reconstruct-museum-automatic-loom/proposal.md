## Why

The pilot commissions a historical reconstruction of the Vinci museum's
automatic ribbon loom, replacing the earlier illustrative mechanism. The
existing model has no intermediate gears, physical carrier/reed transmissions,
grip latches or connected beam drive, so its animation cannot explain the
whole machine.

Authority, 12 September 2026, is the pilot's request:

> See the Leonardo project. we started with educational, now I want historical reconstruction. I did that with hydraulic_sawmill, now I want the same with automatic_weaving_loom. right now it's illustrative. Now I want an historical reconstruction fully simulated. See https://museoleonardiano.it/en/opera/automatic-weaving-loom/. There are several missing gears. Make the simulation with all gears, everything connected properly.

## What Changes

- Reconstruct the complete mechanical power path of the narrow, accompanied
  spool interpretation identified by the Vinci museum: common drive, shedding,
  carrier arms and their grips, reed, intermittent gearing, and lower linked
  warp/cloth winding apparatus, with journals, guides and retention.
- Account explicitly for the one-tooth, six-tooth and twelve-tooth train
  described on Atlanticus 985r and for every toothed wheel visible in the
  reference photographs. A turning wheel without an engaged mate is not a
  completed mechanism.
- Replace independently prescribed output motions with relations derived
  from the modeled transmitting contacts and closed links; verify tooth
  clearance, engagement, handoff, feed and complete assembly integrity.
- Rebuild the exhibit around the historical reconstruction, allowing inspection
  of each mechanism in the actual exported model.
- Preserve the original archive and document primary observations, uncertain
  details and the dimensional/profile choices required to make a working
  reconstruction. Boldetti's 1954 model is not an original Renaissance object.

## Capabilities

### New Capabilities

- `museum-loom-mechanisms`: complete connected transmissions, winding and
  carrier retention, with source-by-source evidence.

### Modified Capabilities

- `weaving-cycle`: mechanically derived shedding, insertion, beat and feed.
- `loom-demonstration`: inspect the historical mechanism and its evidence,
  with a bounded, repeatable demonstration and clearly described replay.

## Impact

The existing `automatic_weaving_loom` model, companion tests, presentation,
machine-owned OpenSpec and evidence; focused gallery metadata and README
corrections if needed. No other model, dependency, shop or remote changes.
Original CAD remains project-owned; downloaded reference images are ignored
research material. As with the sawmill reconstruction, geometric/kinematic
simulation does not certify forces, friction, yarn constitutive behavior or
manufacturing tolerances. Ordinary reconstruction dimensions are delegated;
unresolved historical mechanism choices must remain explicit.
