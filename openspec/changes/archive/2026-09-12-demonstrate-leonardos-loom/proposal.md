## Why

Leonardo's automatic loom is difficult to understand from a still drawing: the warp must open before the weft crosses, the carrier must leave before beat-up, and the next pick must reverse the interlacing. This one-shot demonstration makes those relationships visible and testable in solid-node.

Pilot scope: “This is a one-shot demo of Astra mechanical skills. You will build projects/Leonardo/Automatic-weaving-loom, Da Vinci's machine, based on design material you find online. I want a functional demonstration of how it works in solid-node. Create the project with solid new. Use openspec discipline.”

## What Changes

- Create an independent project using `solid new`, preserving the generated Python package and both integrity contracts.
- Reconstruct an educational narrow loom inspired by Codex Atlanticus f.985r-v and the Museo Leonardiano's alternating carrier arms, with a timber frame, handwheel, mechanical drive, two heddle frames, reed, spool carrier, warp and cloth rollers.
- Animate a repeatable two-pick cycle, flexible contrasting warp yarns, spool transfer, beat-up and take-up from one drive phase.
- Provide clear demonstration controls, a standalone browser export, geometric and timing contracts, inspected snapshots and source/assumption records.

## Capabilities

### New Capabilities

- `weaving-cycle`: coordinated shedding, accompanied weft insertion, beat-up and cloth advance.
- `loom-demonstration`: inspectable and controllable historical reconstruction with material colors, intact rigid solids, clearance contracts and stated limits.

### Modified Capabilities

None; this is a new project.

## Impact

Only this project's manifest, Python package, documentation and OpenSpec records change. Uses installed solid-node, CadQuery and molejo through public APIs. No upstream CAD was located for reuse; geometry is original, based on documented principles and museum imagery. Dimensions, simplified drive laws and clearances are demonstrator design choices, not measurements of Leonardo's drawing. Yarn tension, impact dynamics, manufacture and a claim of exact historical reconstruction are outside this educational kinematic model.
