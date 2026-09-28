<!-- Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only. -->
# Evidence for the revised script

Checked 28 September 2026. This is a script audit, not a new mechanical
validation or a claim that this production has already been filmed.

## Museum and opening

The [Milan museum catalogue, IGB-37](https://collezioni-online.museoscienza.org/detail/IT-MUST-NTR001-008357/sega-idraulica)
identifies a 1952–1953 interpretative model, designed by Arturo Uccelli and
built by Alessandro Siriati. It places Leonardo da Vinci's study in an older
tradition of hydraulic saws and describes the synchronized saw/carriage,
crank/rod, pawl, ropes and rollers. Thus the opening says he **studied** a
sawmill; it does not credit him with inventing powered sawing. Revolution is
the opening wheel metaphor and a change in work, not a dating claim about the
Industrial Revolution.

The inspected closing image is the project's existing private research copy
`_reference/hydraulic_sawmill/milan-overall.jpg`, from the museum's
[overall photograph](https://www.museoscienza.org/besrv/sites/default/files/2019-11/sega-idraulica.jpg).
Its black backdrop is compatible with the chosen dark presentation. It is
not copied into tracked video assets. The catalogue links to
[image/site terms](https://www.museoscienza.org/it/termini-condizioni-catalogo-collezioni),
but that JavaScript page did not expose its terms to the text fetcher. The
script does not assume a licence or publication permission. Confirm rights
and the required credit before release, without substituting invented imagery.

## Mechanical explanation

The project's [reconstruction record](../../models/hydraulic_sawmill/docs/reconstruction.md)
and [transmission validation](../../models/hydraulic_sawmill/docs/transmission-validation.md)
establish the actual path: undershot wheel → crankshaft/crank → rod and sash
→ tied rocker and pulling pawl → ratchet/bare winding axle → first rope and
lower idler → large compound-shaft winding section → thin take-up section
and separate hauling rope → upper roller → centred carriage attachment.

The two compound-shaft sections rotate together. The first rope unwinds
from the larger radius; the other winds at the smaller radius, reducing
linear take-up. The feed is not a constant ratio across the full cut: radial
input buildup, helical winding and changing free spans are in the equations.
The script deliberately avoids an oversimplified fixed overall ratio.
Winding order, tension, no slip and secured timber are assumptions; the
animation cannot prove real rope stability or cutting performance.

The current model's chosen stroke is 48 mm. That is not a measured historical
dimension. Its test compares actual upper/lower mesh bounds within 0.01 mm.
The test itself is shown, not rewritten; all selected excerpts are checked
against the export's pinned source revision. The complete wheel class is
`Wheel(CadQueryNode)`, and the mill is `LeonardoHydraulicSawmill(AssemblyNode)`.

Existing [frame/mechanism evidence](../../models/hydraulic_sawmill/docs/carpentry-validation.md)
records sampled geometric checks, including interference and rope clearance.
The voice claims tests can catch errors, not certify historical fidelity,
continuous contact dynamics, strength or real cutting loads.

## Human work and invitation

The reconstruction record explicitly documents the pilot identifying the
two-rope reduction and correcting the input winding placement. This grounds
the single human-piloting example without reenacting a private transcript or
claiming all choices came from the assistant. The model is inspectable; the
viewer is invited to disagree. Comments are proposed input for a later
human-directed improvement, not a promised autonomous monitoring service.

The public destinations for the exact current simulation and source remain
unverified. Keep the upload-description placeholders until those artifacts
have working public addresses. No upload, push, outreach or permission request
to the museum is authorized by this script task.
