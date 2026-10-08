"""Original opening and mechanism script, without rewriting."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

import json
import re
from pathlib import Path

from machinome_movie import Narration

delivery = json.loads(
    (Path(__file__).resolve().parent / "delivery.json").read_text()
)
lines = Narration(delivery["text"])
DIRECTED = delivery["directedText"]
assert " ".join(re.sub(r"\[[^\]]+\]", "", DIRECTED).split()) == lines.text

AUDIO = {
    "provider": "elevenlabs",
    "model": "eleven_v3",
    "voice": "EbiSUflQjzm4g7S895SC",
    "voiceLabel": "Leo Antonio — Português (Brasil)",
    "outputFormat": "pcm_24000",
    "voiceSettings": {"stability": 0.5, "similarity_boost": 0.75},
    "replacements": {lines.text: DIRECTED},
}
