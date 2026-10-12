"""Check the recorded ending independently, without a script prompt."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

build = Path(__file__).resolve().parent / "_build"
audio = build / "provider-original.wav"
digest = hashlib.sha256(audio.read_bytes()).hexdigest()
pcm = subprocess.check_output([
    "ffmpeg", "-v", "error", "-i", str(audio), "-ss", "170",
    "-f", "f32le", "-ar", "16000", "-ac", "1", "pipe:1",
])
model = WhisperModel(
    "base", device="cpu", compute_type="int8", cpu_threads=4,
    local_files_only=True,
)
segments, _ = model.transcribe(
    np.frombuffer(pcm, dtype=np.float32), language="pt", beam_size=5,
    vad_filter=False, word_timestamps=True,
)
result = [{"start": s.start + 170, "end": s.end + 170,
           "text": s.text.strip()} for s in segments]
text = " ".join(s["text"] for s in result)
report = {
    "audioSha256": digest, "model": "faster-whisper/base",
    "scriptPromptProvided": False, "audioOffset": 170,
    "segments": result, "text": text,
    # ASR punctuation is inferred, not an acoustic completeness signal.
    "completeEnding": text.lower().rstrip(".?! ").endswith(
        "o que você quer construir"
    ),
    "scope": "Ending completeness only; not emotional or bilingual approval.",
}
(build / "ending-check.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n"
)
assert report["completeEnding"], "Review the ending before delivery."
print(text)
print("Complete closing question verified without a script prompt.")
