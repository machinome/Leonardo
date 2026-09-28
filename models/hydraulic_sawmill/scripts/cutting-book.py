#!/usr/bin/env python3
"""Export the frame's actual cut solids, stock schedule and illustrated
book."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
import csv
from html import escape
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

# Direct invocation needs the gallery root on sys.path first.
from cadquery import exporters, importers  # noqa: E402

from models.hydraulic_sawmill.carpentry import (
    MEMBERS,
    PEGS,
    FIT,
    PEG_PLAY,
)  # noqa: E402
from models.hydraulic_sawmill.frame import CutTimber, HardwoodPeg  # noqa: E402


def numbers(values):
    return " × ".join(f"{x:.3f}".rstrip("0").rstrip(".") for x in values)


def write_step(shape, path):
    """Verify each delivered part survives a fresh STEP import."""
    exporters.export(shape, str(path))
    restored = importers.importStep(str(path)).val()
    assert restored.isValid() and len(restored.Solids()) == 1, path
    assert abs(restored.Volume() - shape.Volume()) < max(
        1e-7, shape.Volume() * 1e-8
    ), path
    original, actual = shape.BoundingBox(), restored.BoundingBox()
    for bound in ("xmin", "ymin", "zmin", "xmax", "ymax", "zmax"):
        assert abs(getattr(original, bound) - getattr(actual, bound)) < 1e-6, (
            path,
            bound,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "export/hydraulic_sawmill-frame/carpentry",
    )
    args = parser.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    rows, sections, features = [], [], []
    for index, member in enumerate(MEMBERS):
        shape = CutTimber(member=index).render().val()
        # A blank is the bounding stock before any machining, including
        # tenons.
        blocks = [("box", member.stock, member.centre), *member.additions]
        low = tuple(
            min(c[i] - s[i] / 2 for _, s, c in blocks) for i in range(3)
        )
        high = tuple(
            max(c[i] + s[i] / 2 for _, s, c in blocks) for i in range(3)
        )
        size = tuple(b - a for a, b in zip(low, high))
        local = shape.translate(tuple(-v for v in low))
        write_step(local, out / f"{member.code}.step")
        for view, direction in (
            ("iso", (1, -1, 1)),
            ("front", (0, -1, 0)),
            ("side", (1, 0, 0)),
            ("top", (0, 0, 1)),
        ):
            exporters.export(
                local,
                str(out / f"{member.code}-{view}.svg"),
                opt={
                    "width": 420,
                    "height": 240,
                    "projectionDir": direction,
                    "marginLeft": 20,
                    "marginTop": 20,
                    "showAxes": False,
                    "showHidden": True,
                    "strokeWidth": 0.35,
                    "strokeColor": (58, 42, 27),
                    "hiddenColor": (155, 135, 115),
                },
            )
        rows.append(
            [member.code, member.label, "oak", 1, *size, member.grain, *low]
        )
        machining = []
        for operation, feature in [
            *(("retain", b) for b in blocks),
            *(("cut", c) for c in member.cuts),
        ]:
            if feature[0] == "box":
                _, dims, centre = feature
                coords = tuple(c - l for c, l in zip(centre, low))
                detail = f"Box {numbers(dims)}; centre ({numbers(coords)})"
            else:
                _, radius, length, centre, axis = feature
                coords = tuple(c - l for c, l in zip(centre, low))
                detail = (
                    f"Bore Ø{2 * radius:g}, axis {axis.upper()}, "
                    f"length {length:g}; centre ({numbers(coords)})"
                )
            machining.append(
                f"<tr><td>{operation}</td><td>{escape(detail)}</td></tr>"
            )
            features.append(
                {
                    "member": member.code,
                    "operation": operation,
                    "feature": feature,
                    "blank_origin_world": low,
                }
            )
        images = "".join(
            f'<figure><img src="{member.code}-{v}.svg" '
            f'alt="{v} view of {member.code}">'
            f"<figcaption>{v}</figcaption></figure>"
            for v in ("iso", "front", "side", "top")
        )
        notes = "".join(f"<li>{escape(note)}</li>" for note in member.notes)
        sections.append(
            f'<section id="{member.code}"><h2>{member.code} · '
            f"{escape(member.label)}</h2>"
            f"<p>One oak blank: {numbers(size)} mm (X × Y × Z). "
            f"Grain along {member.grain}. "
            f'<a href="{member.code}.step">Exact cut part — STEP</a>'
            f'</p><div class="views">{images}</div>'
            f"<ul>{notes}</ul><details><summary>Dimensioned machining "
            "coordinates from the blank corner</summary>"
            "<table><thead><tr><th>Operation</th><th>Dimensions in mm"
            "</th></tr></thead>"
            f'<tbody>{"".join(machining)}</tbody></table></details></section>'
        )
    for index, peg in enumerate(PEGS):
        shape = HardwoodPeg(peg=index).render().val()
        write_step(shape, out / f"{peg.code}.step")
    with (out / "cut-list.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            [
                "id",
                "member",
                "material",
                "quantity",
                "blank_x_mm",
                "blank_y_mm",
                "blank_z_mm",
                "grain_axis",
                "world_datum_x",
                "world_datum_y",
                "world_datum_z",
            ]
        )
        writer.writerows(rows)
    with (out / "pegs.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            [
                "id",
                "member_a",
                "member_b",
                "axis",
                "diameter_mm",
                "shank_length_mm",
                "head_diameter_mm",
                "head_depth_mm",
                "x",
                "y",
                "z",
            ]
        )
        writer.writerows(
            [
                p.code,
                *p.members,
                p.axis,
                2 * p.radius,
                p.length,
                2 * (p.radius + 1) if p.axis == "z" else 0,
                2 if p.axis == "z" else 0,
                *p.centre,
            ]
            for p in PEGS
        )
    (out / "machining.json").write_text(json.dumps(features, indent=2) + "\n")
    toc = " · ".join(f'<a href="#{m.code}">{m.code}</a>' for m in MEMBERS)
    page = f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>Sawmill frame — cutting book</title><style>
body{{max-width:1000px;margin:40px auto;padding:0 20px;
background:#f7f2e8;color:#392e23;font:17px/1.5 system-ui}}
a{{color:#73502b}}h1,h2{{font-family:Georgia,serif}}
section{{border-top:1px solid #bbae98;margin-top:40px;padding-top:20px}}
.views{{display:grid;grid-template-columns:1fr 1fr}}
figure{{margin:10px}}img{{width:100%;background:white}}
figcaption{{text-align:center}}
table{{border-collapse:collapse;font-size:14px}}
td,th{{padding:8px;border:1px solid #c7bba8}}
details{{margin:20px 0}}
@media(max-width:600px){{.views{{grid-template-columns:1fr}}}}
@media print{{section{{break-before:page}}details{{display:block}}}}
</style><h1>The sawmill frame: cutting book</h1>
<p>{len(MEMBERS)} individual oak timbers and {len(PEGS)} riven oak pins.
All dimensions are millimetres at the existing museum-model scale.
Photographs establish the arrangement; these concealed joints and
dimensions are reconstruction choices.</p>
<p><a href="../index.html">Interactive assembly study</a> ·
<a href="../../hydraulic_sawmill/index.html">Working model</a> ·
<a href="cut-list.csv">Stock list CSV</a> ·
<a href="pegs.csv">Peg schedule CSV</a> ·
<a href="machining.json">Machining data</a></p>
<p>Each STEP timber uses its blank's minimum X/Y/Z corner as zero.
The views are orthographic/isometric illustrations, not print-to-scale
templates. Peg STEP files retain their assembly coordinates; their schedule
gives the shank centre, axis and head dimensions. Member notes quote assembly
coordinates; the machining tables below convert every centre to that blank's
local coordinates. Views are from −Y (front), +X (side), and +Z (top).
For each member, retain the union of the listed stock envelopes, then make
the listed cuts. Stock-envelope unions describe a single carved timber,
not glued pieces. Bore centres and box sizes below specify the cuts
numerically. Grain follows the long member axis.</p>
<p>Nominal dry-fit cheek clearance: {FIT} mm per side; peg radial play:
{PEG_PLAY} mm. Shoulder seating allowance is 0.1 mm. Real pegs are pared
to fit. The model does not simulate drawbore deformation, moisture movement
or full-size structural loads. Vertical pins have whittled heads; heads in
running rails are recessed below the wheel surface. The plinth is a display
ground fixture.</p>
<nav>{toc}</nav>{''.join(sections)}
<footer>Copyright (C) 2026 Luis Henrique Cassis Fagundes · AGPL-3.0-only ·
Machinome Leonardo gallery</footer></html>"""
    (out / "index.html").write_text(page)
    print(
        f"{len(MEMBERS)} timbers, {len(PEGS)} pegs; verified STEP "
        f"round trips, SVG views, schedules: {out}"
    )


if __name__ == "__main__":
    main()
