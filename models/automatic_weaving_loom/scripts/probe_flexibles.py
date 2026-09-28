"""Diagnostic inventory of operating-cord/spring contacts with rigid
parts.

Run from the gallery root with its Python environment. This
intentionally
reports termination contacts too; it is a locator, not an acceptance
test.
"""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import logging
import sys
from pathlib import Path

import numpy as np
import trimesh

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
# Direct invocation needs the gallery root on sys.path first.
from models.automatic_weaving_loom.model import (
    AutomaticWeavingLoom,
)  # noqa: E402
from models.automatic_weaving_loom.checks import rigid_parts  # noqa: E402


def main():
    logging.disable(logging.CRITICAL)
    machine = AutomaticWeavingLoom()
    machine.set_state(phase=0, run=0, time=0)
    machine.assemble()
    machine.build_stls()
    rigid = list(rigid_parts(machine))
    flexible = []
    for name in ("left", "right", "reed"):
        group = getattr(machine.cords, name)
        flexible.extend(
            (
                (name + ".haul", group.haul.cord),
                (name + ".return", group.returning.cord),
            )
        )
    flexible.extend(
        (
            ("left.spring", machine.carrier.left.spring),
            ("right.spring", machine.carrier.right.spring),
        )
    )
    for phase in (
        0,
        30,
        40,
        60,
        90,
        110,
        120,
        130,
        150,
        180,
        220,
        240,
        270,
        300,
        320,
        360,
    ):
        machine.set_state(phase=phase, run=0, time=0)
        meshes = [(name, part.mesh) for name, part in rigid]
        for label, leaf in flexible:
            mesh = leaf.mesh
            a = mesh.bounds
            for name, other in meshes:
                b = other.bounds
                if np.all(a[0] < b[1]) and np.all(b[0] < a[1]):
                    overlap = trimesh.boolean.intersection(
                        [mesh, other], engine="manifold"
                    )
                    if len(overlap.faces):
                        print(
                            phase,
                            label,
                            name,
                            "volume",
                            overlap.volume,
                            "bounds",
                            overlap.bounds.tolist(),
                            flush=True,
                        )
    print("Contact inventory complete", flush=True)


if __name__ == "__main__":
    main()
