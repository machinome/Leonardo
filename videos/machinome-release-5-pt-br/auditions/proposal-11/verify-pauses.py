"""Independent words near sentence edits; no transcript supplied to ASR."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

build = Path(__file__).resolve().parent / "_build"
audio = build / "provider-original.wav"
model = WhisperModel("base", device="cpu", compute_type="int8",
                     cpu_threads=4, local_files_only=True)
pcm = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(audio),
                               "-f", "f32le", "-ar", "16000", "-ac", "1", "pipe:1"])
segments, _ = model.transcribe(np.frombuffer(pcm, dtype=np.float32), language="pt", beam_size=5,
                               vad_filter=False, word_timestamps=True)
result = [{"start": s.start, "end": s.end, "text": s.text,
           "words": [{"word": w.word, "start": w.start, "end": w.end}
                     for w in s.words]} for s in segments]
report = {"audioSha256": hashlib.sha256(audio.read_bytes()).hexdigest(),
          "scriptPromptProvided": False, "segments": result,
          "scope": "Independent word timing evidence, not emotional approval."}
(build / "pause-transcription.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n")
for s in result:
    print(f"{s['start']:.2f}–{s['end']:.2f}: {s['text']}")
