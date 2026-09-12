# Selected geometry views

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

These default OpenSCAD-renderer snapshots of the actual model were opened
and inspected on 12 September 2026:

- [Isometric at Mid](isometric-mid.png): complete timber frame, two fixed
  wheels, moving wheel and block, separate load eye, effort grip and four
  rope lanes. Opening the anchor cheeks made its small return wrap visible.
- [Front at High](front-high.png): the four parallel lanes, three sheave
  alignments, visible dead-end return and lowered effort grip are readable.

From the gallery root, in the documented environment:

```sh
SOLID_BUILD_DIR=_build/pulley_images solid snapshot pulley_block -o models/pulley_block/docs/evidence/isometric-mid.png --time 0.25 --autocenter --viewall --imgsize 1400x1200
SOLID_BUILD_DIR=_build/pulley_images solid snapshot pulley_block -o models/pulley_block/docs/evidence/front-high.png --time 0.5 --camera 0,-550,136,0,0,136 --viewall --projection ortho --imgsize 1200x1400
```

Commands initially used `models/pulley_block/model.py:PulleyBlock` before
registration. Browser evidence is reproduced by
`python models/pulley_block/scripts/check_browser.py`, including desktop
and narrow captures under ignored `_evidence/pulley_block/`.
Images document presentation; [geometric tests](../validation.md) prove
length, attachment, capture and non-interference.
