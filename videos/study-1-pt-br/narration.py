"""Original opening and mechanism script, without rewriting."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. CERN-OHL-S-2.0+.

import json
import re
from pathlib import Path

from machinome.movie import Narration

delivery = json.loads(
    (Path(__file__).resolve().parent / "delivery.json").read_text()
)
lines = Narration(delivery["text"])
assert delivery["model"] == "eleven_v3", "Pilot-fixed synthesis model"
DIRECTED = delivery["directedText"]
assert " ".join(
    re.sub(r'\[[^\]]+\]|<break time="[0-9.]+s"\s*/>', "", DIRECTED).split()
) == lines.text

AUDIO = {
    "provider": "elevenlabs",
    "model": delivery["model"],
    "voice": "EbiSUflQjzm4g7S895SC",
    "voiceLabel": "Leo Antonio — Português (Brasil)",
    "outputFormat": "pcm_24000",
    "voiceSettings": delivery["voiceSettings"],
    "replacements": {lines.text: DIRECTED},
}
