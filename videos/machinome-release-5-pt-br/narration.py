"""Approved Portuguese performance: source text only, never synthesize here."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import json
import re
from pathlib import Path

from machinome_movie import Narration

HERE = Path(__file__).resolve().parent
delivery = json.loads((HERE / "delivery.json").read_text())
directed = "\n\n".join(s["directedText"] for s in delivery["sections"])
text = re.sub(r"\s+", " ", re.sub(r"\[[^\]]+\]", "", directed)).strip()
lines = Narration(text)
AUDIO = delivery["audio"]
