## Context

Original educational CAD, scaffolded with `solid new Automatic-weaving-loom` (CLI normalizes the generated directory to `Automatic_weaving_loom`; the outer directory was renamed to the requested spelling). No existing upstream source is replaced. Museo Leonardiano identifies the source as Codex Atlanticus f.985r-v. Its curator-authored account describes two arms accompanying and exchanging the weft spool, producing narrow ribbons. The museum photograph shows a timber rectangular frame, external drive wheels, textile rollers, overhead heddle support and mechanical links.

Sources, accessed 2026-09-12:

- https://artsandculture.google.com/story/leonardo-and-the-art-of-weaving-leonardo-da-vinci-museum/2wVxLwuL6F11KQ?hl=en — museum explanation; alternating accompanied spool and narrow fabric.
- https://museoleonardiano.it/opera/telaio-automatico-md/ — folio identification and reconstruction video record.
- https://museoleonardiano.it/en/opera/automatic-weaving-loom/ — museum object and photograph; image inspected from https://museoleonardiano.it/wp-content/uploads/2024/09/formato-immagine-sito-50.png. This photograph is reference only, ignored and not redistributed.
- https://www.dmg-lib.org/thinkMOTION/wp-content/uploads/2011_Mexico-BrixReessing.pdf — secondary engineering account of a common crank-driven shaft. The museum's description controls the carrier interpretation.

## Goals / Non-Goals

Goals: a visible, coherent two-pick weaving cycle; a measurable shed, accompanied weft spool, alternating heddles, reed beat-up, turning rollers, and original material-colored geometry. Named controls and an exported browser model explain the sequence. Retain both rigid-body integrity tests and exercise moving interfaces.

Non-goals: a facsimile, manufacturing drawings, verified historical dimensions, force/tension/contact dynamics, fully modeled yarn accumulation, or proving that the historical design was built in Leonardo's lifetime.

## Coordinates

Millimetres. X is across the cloth; Y runs from the front cloth beam toward the rear warp beam; Z is up. Ground is Z=0. Nominal weaving plane Z=180; yarn spans X=-69..69 at 6 mm spacing, demonstrating 24 warp ends. Timber uprights are outside the working width. The cloth fell is at Y=-105, the carrier crosses behind it, and two heddle frames stand farther toward the warp beam.

## Decisions

1. **Educational reconstruction.** Reference photographs and descriptions determine the architecture; all dimensions are chosen here for readable clearances. Narrow fabric and two carrier arms follow the museum account; a broad flying shuttle would imply a different reconstruction.
2. **One cyclic intent.** `phase` is the two-pick cycle in degrees and `run` multiplies the viewer timeline. Default playback runs automatically. Instructions freeze at meaningful stages or restore playback. One revolution reverses the shed twice and returns the carrier.
3. **Mechanical constraints.** Rigid parts declare their own revolute/prismatic joints. A common phase drives them through explicit relations. Opposed eccentric pins and slotted yokes demonstrate positive-drive shedding. The reed and carrier timing is prescribed kinematics; the complete historical intermediate gearing, arm latches and tension control are not reconstructed. This distinction appears in the README and demo text.
4. **Flexible yarn.** Contrasting alternate warp ends use molejo paths bound to heddle lift. A weft guide illustrates the spool's yarn. A short static interlaced cloth sample explains over/under topology; roller rotation illustrates feed, without claiming accumulated production or yarn-length conservation.
5. **No hidden interference allowance.** Use positive drawing clearances for separate rigid parts; connected timber and rigidly joined features are fused into single bodies. Test root connectivity and interference at multiple phases, pin/yoke engagement and shuttle clearance. Flexible contact and yarn dynamics have distinct limits.
6. **Evidence.** Faceted red/green checks while building, targeted wrong-placement/timing mutations, finite build and published-motion inspection, isometric plus axial snapshots, and final exact geometric regression. Planning and completed implementation are committed in this project's repository.

## Risks / Trade-offs

- Undimensioned historical material → record demonstrator measurements and avoid claiming authenticity of chosen cam laws or proportions.
- Prescribed motion can conceal disconnected drives → explicitly demonstrate and test the eccentric/yoke drive; name the omitted intermediate transmission for other motions.
- Few enlarged threads communicate weaving clearly but are not production textile density → identify the yarn scale as illustrative.
- Sampled collision checks can miss an interval → combine whole-cycle checks with denser timing and local engagement tests, and state the sampled extent.

## Findings

The complete implementation and verification are recorded in
`docs/verification.md`. The handwheel needed swept clearance in a lower rail;
the carrier needed interleaved support fingers; the reed needed a timber
bearer and close-running foot channels. Those findings were corrected in the
project's geometry while retaining the whole-model integrity contracts.

Support is tested with the timber frame explicitly grounded as a fixture;
the inferred-ground check reported an unbalanced-frame verdict at an
intermediate pose, and freestanding stability is not claimed. No moving
rigid part is exempted from the grounded support contract.

The root's `shed_lift` parameter drives both eccentric throw and heddle/yarn
motion, guarded at 16–20 mm. Exact regression passes at 16, 18 and 20 mm;
five code mutations were detected and reverted. The inspected publication
has both drivers, six instructions, 11 rigid occurrences and 81 flexible
leaves. The standalone browser demo also exercises real stage controls and
automatic playback successfully. No framework changes were necessary.
