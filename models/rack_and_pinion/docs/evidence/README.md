# Selected rack-lift images

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Both images use the default OpenSCAD renderer, the actual root model,
default module 3, and default phase/run. They were opened and inspected.
Generated batch images and browser captures remain ignored under `_evidence/`.

- [Isometric mid-lift](isometric-mid-lift.png), time 0.25: timber stand,
  crank, meshing rack, guide sleeves and the hook with its perpendicular eye.
- [Front at the top](front-top.png), time 0.5: sight along the shaft shows
  tooth engagement, both guides, the stop shoulders and the suspended weight.

From the gallery root with the documented environment activated:

```sh
SOLID_BUILD_DIR=_build/rack_snapshot machinome snapshot rack_and_pinion --time 0.25 --autocenter --viewall --imgsize 1200x1200 -o models/rack_and_pinion/docs/evidence/isometric-mid-lift.png
SOLID_BUILD_DIR=_build/rack_snapshot machinome snapshot rack_and_pinion --time 0.5 --camera 0,-800,210,0,0,210 --autocenter --viewall --projection ortho --imgsize 1200x1200 -o models/rack_and_pinion/docs/evidence/front-top.png
```

The first isometric inspection exposed a post hiding the hook. Moving the
right-hand posts outward and extending their guide supports made the
connection visible. The final front view uses view-all to retain the rack
tip and base. Neither image replaces the geometric engagement, capture,
connectedness or non-interference contracts in `test_model.py`.
