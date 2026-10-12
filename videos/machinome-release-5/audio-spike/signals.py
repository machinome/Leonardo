"""Read existing machine coordinates; JSON request/response on stdio."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import json
import sys

from models.hydraulic_sawmill.model import (
    LeonardoHydraulicSawmill,
    uncut_profile,
)
from models.hydraulic_sawmill.layout import TIMBER_LENGTH


def main():
    request = json.load(sys.stdin)
    machine = LeonardoHydraulicSawmill()
    rows = []
    for seconds in request["times"]:
        machine.set_keyframe(seconds)
        machine.simulate()
        phase = float(machine.cycle.value)
        blade = float(machine.saw.sash.rise.value)
        advance = float(machine.carriage.feed.value)
        remaining = float(uncut_profile(advance)[0])
        # Geometric engagement only, not a cutting-load calculation.
        engaged = 0.0001 < remaining < TIMBER_LENGTH - 0.0001
        rows.append([seconds, phase, blade, advance, int(engaged)])
    json.dump(
        {
            "columns": ["seconds", "phaseDeg", "bladeMm", "feedMm",
                        "engaged"],
            "units": "model seconds, degrees, millimetres",
            "source": "Existing root simulate() and resolved joint values",
            "rows": rows,
        },
        sys.stdout,
    )


if __name__ == "__main__":
    main()
