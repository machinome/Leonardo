# The compound pulley — pull three lengths, lift one

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Astra's original single-prompt educational design, a
[machinome demonstration](https://machinome.readthedocs.io/) in the
[Leonardo gallery](https://github.com/LibreSolid/Leonardo) (publication pending).
Commission: [queue 030](../../QUEUE.md#030-pulley-block). Exact session prompt:

> See the projects/Leonardo. Build next project.

Open the [interactive exhibit](index.html) through an HTTP server.
This original tackle has two fixed sheaves and one moving sheave carrying
a separate demonstrator load. It is not a dimensioned historical replica.

## Follow the rope

From a capped dead-tail socket on the moving block, the orange rope wraps
under a small anchor pin. It rises over the first fixed sheave, descends
under the moving sheave, rises over the second fixed sheave and descends
into the effort grip. It is one continuous molejo flexible shape, with no
hidden discontinuity, winding drum, reset or accumulating length.

The three supporting spans occupy separate lanes at x=-54, -18 and +18 mm;
the effort occupies x=+54. All run in the same XZ plane. Staggering the
parallel axles keeps the route legible without skew spans between different
depth planes. The small anchor return contributes a fixed length.

| Stage | Load rise | Effort pull | A: anchor→fixed | B: fixed→moving | C: moving→fixed | D: effort |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Low | 0 mm | 0 mm | 124 mm | 140 mm | 140 mm | 30 mm |
| Mid | 20 mm | 60 mm | 104 mm | 120 mm | 120 mm | 90 mm |
| High | 40 mm | 120 mm | 84 mm | 100 mm | 100 mm | 150 mm |

The four wraps add `58*pi` mm and the short tail adds 6 mm. Total rope
length is **622.212373908 mm** at every setting. Shortening three supporting
spans by h requires lengthening the effort span by 3h. Live explanatory
labels follow the viewer's controls, rounded to its displayed frame during
playback; the browser check compares them against Python mesh measurements.

## Controls

- **Low / Mid / High:** hold phase 0° / 90° / 180°, with run=0.
- **Run:** restore phase=0 and run=1; play the native timeline for the loop.
- **phase:** one complete smooth lift and return, 0–360°. It is cycle phase,
  not a sheave angle. With run=0, the slider inspects static positions.
- **run:** blends the selected static pose with the cycling pose. Fractional
  values reduce excursion; all slider combinations close at t=0/1.

The 40 mm lift and all dimensions are fixed educational choices. There is
no advertised size parameter. Exact entries outside the declared control
ranges are not additional advertised settings.

## Geometry and limits

The 190×76 mm base supports a 272 mm tall stand. Fixed sheave centres are
x=±36, z=230 mm; the moving centre rises from z=90 to 130. Each sheave has
an 18 mm pitch radius, 41.4 mm outside diameter and 6.5 mm bore on a 6 mm
pin. Axial cheek gaps are 0.3 mm. The 2.5 mm diameter rope clears the groove
floor by 0.35 mm; sloped flanges constrain its axial escape. The small
anchor pin has a 0.25 mm radial rope gap.

The moving yoke is one connected part, with open anchor supports exposing
the return wrap, a pinned sheave and a separate weight on a bored eye.
The tail is retained in a downward-facing blind socket; the effort end
enters an 8 mm deep socket. Secured terminations are prescribed, not solved
knots/crimps or assertions of frictional grip.

The timber stand is grounded, with simplified joinery and integral bearing
pins. Ideal taut-rope suspension and a held effort end prescribe the upright
block pose. Rigid support tests explicitly ground the suspended carrier and
effort grip, then prove sheave and load-eye support. Separate flexible
tests measure routing, insertion, wrap capture, length and clearance. The
rigid support solver alone does not prove rope tension or block stability.

The measured 3:1 relationship is displacement, not a load rating. Equal
ideal tensions suggest a force advantage, but friction, tension, rope
elasticity, sway, efficiency, strength, knot/crimp behavior and load capacity
are not simulated. This exhibit is not a manufacturing or rigging plan.

## Historical source

[Museo Leonardiano: Tirare composto](https://museoleonardiano.it/opera/tirare-composto/)
identifies Madrid I f.36v and Luigi Boldetti's 1979 museum reconstruction
with 33 pulleys. It links the
[digitized manuscript folio](https://www.leonardodigitale.com/sfoglia/madrid-I/0036-v/).
The object record was accessed 12 September 2026. It establishes the study
and later reconstruction, not our dimensions or invention priority.

The commission also cites
[Museo Galileo's 33-pulley record](https://brunelleschi.imss.fi.it/genscheda.asp?appl=LIR&chiave=100851&indice=63&lingua=ENG&xsl=paginamanoscritto).
The initial web reader could not decode that source, so its wording is not
represented here as newly verified. This three-part tackle is a deliberately
reduced teaching model, **not a replica of 33 pulleys**. No museum CAD,
drawing trace or image asset is imported.

## Build and verify

Use the gallery's documented post-0.6 machinome environment and local
viewer API 7. From the gallery root, with `../../.venv` activated:

```sh
SOLID_BUILD_DIR=_build/pulley_tests machinome test pulley_block --faceted
SOLID_BUILD_DIR=_build/pulley_exact machinome test pulley_block --exact
python scripts/gallery.py build pulley_block
python scripts/gallery.py export pulley_block
python models/pulley_block/scripts/check_browser.py
python scripts/gallery.py check
python scripts/check_browsers.py
python -m http.server 8769 --bind 127.0.0.1
```

Open `http://127.0.0.1:8769/models/pulley_block/`.
The standalone viewer is `export/pulley_block/index.html`. Exports and raw
captures are ignored; `gallery.py export` refreshes committed source ZIPs.
No push or publication is part of building.

See [validation](docs/validation.md), [selected inspected images](docs/evidence/README.md)
and this machine's [OpenSpec](openspec/) for the durable record.
