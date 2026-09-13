# Inspected reconstruction views

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Original CAD screenshots rendered and inspected on 13 September 2026 using
the default OpenSCAD renderer, plus the live Studio browser screenshot. These
are not museum photographs. Dimensions,
concealed head tracks and fittings are reconstructed choices documented in
[the evidence and inference record](../reconstruction.md).

- [Whole loom at the first handoff, 90°](museum-isometric.png): tall timber
  frame, upper head, winding beams, four lower gears, perforated belt and
  external cord returns. The continuous material route reaches both beams.
- [Transmission alignment at beat right, 180°](transmission-alignment.png):
  side view of the two lower wheel pairs, connecting belt, descending rack
  and upper indexing train. This projection shows alignment; engagement is
  proved separately by the geometric contracts.
- [Weaving head at the return handoff, 270°](weaving-head.png): opposed
  heddles, reed, carrying hands, outboard spring/selector actuation and common
  shaft cams. This is intentionally a close-up, with the lower frame cropped.
- [Live Studio with native ×0.5 playback](studio-slow-motion.png): the actual
  open Leonardo project, not the companion exhibit HTML. Expanding Timeline
  exposes the speed selector because Python declares `Time(loop=60)`.
  Captured by `scripts/check_studio_time.py` and inspected at this checkpoint.

From the gallery root with the workspace environment active:

```sh
solid snapshot automatic_weaving_loom --time 0.0625 --autocenter --viewall --camera 0,0,0,65,0,35,1200 --imgsize 1500x1100 -o models/automatic_weaving_loom/docs/evidence/museum-isometric.png
solid snapshot automatic_weaving_loom --time 0.125 --autocenter --viewall --camera 0,0,0,90,0,90,1200 --imgsize 1500x1100 -o models/automatic_weaving_loom/docs/evidence/transmission-alignment.png
solid snapshot automatic_weaving_loom --time 0.1875 --camera 550,-400,850,0,160,470 --projection ortho --imgsize 1500x1100 -o models/automatic_weaving_loom/docs/evidence/weaving-head.png
```

The timeline covers four input turns, so these normalized times correspond
to 90°, 180° and 270°. Browser layout/control evidence is generated separately
under ignored `_evidence/automatic_weaving_loom/browser/` by
`scripts/inspect_demo.py`. These views do not certify forces, rope tension,
spring preload, textile formation or manufacture.
