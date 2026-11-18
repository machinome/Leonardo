"""Independent local transcription, without a script prompt."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

import dataclasses
import hashlib
import json
import os
import re
import unicodedata
from pathlib import Path

from faster_whisper import WhisperModel

base = Path(__file__).resolve().parent
manifest = json.loads((base / "_build/narration-manifest.json").read_text())
audio = Path(manifest["cacheFile"])
assert hashlib.sha256(audio.read_bytes()).hexdigest() == manifest["sha256"]
model_name = os.environ.get("STUDY_ASR_MODEL", "small")
assert model_name in ("small", "medium", "large-v3-turbo")
suffix = (
    ".whisper.json" if model_name == "small"
    else ".whisper-" + model_name + ".json"
)
output = Path(str(audio) + suffix)
if output.exists():
    report = json.loads(output.read_text())
    assert report["audioSha256"] == manifest["sha256"]
else:
    model = WhisperModel(
        model_name, device="cpu", compute_type="int8", cpu_threads=4
    )
    segments, info = model.transcribe(
        str(audio), language="pt", beam_size=5,
        word_timestamps=True, vad_filter=False,
    )
    segments = [dataclasses.asdict(s) for s in segments]
    report = {
        "audioSha256": manifest["sha256"],
        "model": "Systran/faster-whisper-" + model_name,
        "language": info.language,
        "scriptPromptProvided": False,
        "text": " ".join(s["text"].strip() for s in segments),
        "segments": segments,
    }
    with output.open("x") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
        file.write("\n")
print(report["text"])
print(output)


def words(text):
    # Orthographic crasis (a/à) is not an acoustic word substitution.
    text = "".join(
        c for c in unicodedata.normalize("NFD", text.lower())
        if not unicodedata.combining(c)
    )
    return re.findall(r"[a-z0-9]+", text)


assert words(report["text"]) == words(manifest["text"]), (
    "Independent transcription differs: inspect before delivery."
)
print("All 175 spoken words match; no script prompt supplied to Whisper.")
