"""Measure where the provider's word clock drifts, sentence by sentence."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
#
# The provider's timestamps run late around performed pauses, by more than a
# second near the end of this take. Sentence boundaries are re-anchored to
# sustained acoustic silence in the untouched recording. The independent
# transcription only says which silence belongs to which boundary; it supplies
# no timestamp to the film. Nothing here changes a sample of audio.
import difflib
import json
import re
import statistics
import struct
from pathlib import Path

# The untouched audition is kept apart from the film's working cache.
build = Path(__file__).resolve().parent / "_build" / "audition-1"
manifest = json.loads((build / "narration-manifest.json").read_text())
record = json.loads(Path(manifest["cacheFile"] + ".json").read_text())
alignment = record["alignment"]
text = "".join(alignment["characters"])
starts = alignment["character_start_times_seconds"]
ends = alignment["character_end_times_seconds"]
assert text == manifest["text"]

wav = Path(manifest["cacheFile"]).read_bytes()
assert wav[36:40] == b"data" and struct.unpack_from("<I", wav, 24)[0] == 24000
count = (len(wav) - 44) // 2
pcm = struct.unpack_from(f"<{count}h", wav, 44)
RATE, FLOOR, SUSTAIN = 24000, 184, 0.12  # below -45 dBFS for at least 120 ms

runs, quiet = [], None
for n, value in enumerate(pcm):
    silent = abs(value) < FLOOR
    if silent and quiet is None:
        quiet = n
    if not silent and quiet is not None:
        if n - quiet >= SUSTAIN * RATE:
            runs.append((quiet / RATE, n / RATE))
        quiet = None
if quiet is not None:
    runs.append((quiet / RATE, count / RATE))
voiced = [n for n, value in enumerate(pcm) if abs(value) >= FLOOR]
onset, release = voiced[0] / RATE, (voiced[-1] + 1) / RATE

check = json.loads((build / "ending-check.json").read_text())
assert check["audioSha256"] == manifest["sha256"] and check["completeEnding"]
heard = [w for s in check["segments"] for w in s["words"]]


def token(word):
    return re.sub(r"[^a-z0-9]", "", word.lower())


script = [(m.start(), m.end() - 1, token(m.group())) for m in re.finditer(r"\S+", text)]
matcher = difflib.SequenceMatcher(
    None, [w[2] for w in script], [token(w["word"]) for w in heard], autojunk=False)
late = {}  # script word index -> provider start minus transcribed start
witness = {}  # script word index -> the transcribed word
for block in matcher.get_matching_blocks():
    for k in range(block.size):
        first = script[block.a + k][0]
        late[block.a + k] = starts[first] - heard[block.b + k]["start"]
        witness[block.a + k] = heard[block.b + k]
word_at = {w[0]: i for i, w in enumerate(script)}
word_ending = {w[1]: i for i, w in enumerate(script)}

# Sentences end at terminal punctuation followed by a space.
cuts = [m.end() for m in re.finditer(r"[.!?:]+ ", text)]
sentences = list(zip([0, *cuts], [*(c - 2 for c in cuts), len(text) - 1]))
drift, previous = [], 0.0
for first, last in sentences:
    inside = [late[i] for i, w in enumerate(script) if first < w[0] <= last and i in late]
    previous = statistics.median(inside) if len(inside) >= 2 else previous
    drift.append(previous)

points = [{"from": starts[0], "to": onset, "anchor": "first voiced sample"}]
boundaries = []
for (_, last), (first, _), offset in zip(sentences, sentences[1:], drift[1:]):
    entry = {"after": text[max(0, last - 23):last + 1], "before": text[first:first + 24],
             "providerEnd": ends[last], "providerNext": starts[first],
             "sentenceDrift": offset}
    said, resumed = witness.get(word_ending[last]), witness.get(word_at[first])
    if said and resumed:
        # Every silence between the two transcribed words is the same pause,
        # even when a breath divides it.
        low, high = said["end"] - 0.2, resumed["start"] + 0.2
        entry["witness"] = {"lastWordEnd": said["end"], "nextWordStart": resumed["start"]}
        near = [r for r in runs if r[1] > low and r[0] < high and r[0] > points[-1]["to"]]
    else:
        expected = starts[first] - offset
        near = [r for r in runs if abs(r[1] - expected) <= 0.4 and r[0] > points[-1]["to"]]
        near = near and [min(near, key=lambda r: abs(r[1] - expected))]
    if near and ends[last] > points[-1]["from"]:
        entry["acousticSilence"] = {"start": near[0][0], "end": near[-1][1],
                                    "runs": [list(r) for r in near]}
        points.append({"from": ends[last], "to": near[0][0]})
        points.append({"from": starts[first], "to": near[-1][1]})
    boundaries.append(entry)
points.append({"from": ends[-1], "to": release, "anchor": "last voiced sample"})

# Inside one stretch of speech, pauses at commas and colons are anchored too
# when every one of them is accounted for: as many silences as marks, in
# order. A list of three or more is taken on that count alone; fewer must
# also fall where the stretch's own clock already expects them.
marks = [(m.start(), m.end()) for m in re.finditer(r"[,.!?:]+ ", text)]
refined, phrases = [], []
for a, b in zip(points[0::2], points[1::2]):
    refined.append(a)
    inner = [(e, n) for e, n in marks if a["from"] < ends[e] and starts[n] < b["from"]]
    quiet = [r for r in runs if r[0] > a["to"] + 0.05 and r[1] < b["to"] - 0.05]

    def expected(t):
        return a["to"] + (b["to"] - a["to"]) * (t - a["from"]) / (b["from"] - a["from"])

    if inner and len(inner) == len(quiet) and (len(inner) >= 3 or all(
            abs(expected(starts[n]) - r[1]) <= 0.35 for (e, n), r in zip(inner, quiet))):
        for (e, n), r in zip(inner, quiet):
            refined.append({"from": ends[e], "to": r[0]})
            refined.append({"from": starts[n], "to": r[1]})
            phrases.append({"after": text[max(0, e - 15):e + 1], "before": text[n:n + 16],
                            "providerEnd": ends[e], "providerNext": starts[n],
                            "acousticSilence": {"start": r[0], "end": r[1]}})
    refined.append(b)
points = refined
assert all(a["from"] < b["from"] and a["to"] <= b["to"] for a, b in zip(points, points[1:]))


def correct(t):
    for a, b in zip(points, points[1:]):
        if t <= b["from"]:
            span = b["from"] - a["from"]
            return a["to"] + (b["to"] - a["to"]) * max(0.0, t - a["from"]) / span
    return points[-1]["to"]


# The transcription is a witness, not a source: report agreement before/after.
before = [abs(late[i]) for i in late]
after = [abs(correct(starts[script[i][0]]) - (starts[script[i][0]] - late[i])) for i in late]
report = {
    "schema": "revolutions-alignment-calibration/1",
    "audioSha256": manifest["sha256"], "duration": count / RATE,
    "method": "Sentence boundaries mapped to sustained acoustic silence "
              "(below -45 dBFS for 120 ms or more); linear between anchors.",
    "silenceRuns": len(runs), "sentences": len(sentences),
    "anchoredBoundaries": sum("acousticSilence" in b for b in boundaries),
    "matchedWords": len(late), "scriptWords": len(script),
    "witness": {
        "model": check["model"],
        "medianProviderDisagreement": statistics.median(before),
        "medianCalibratedDisagreement": statistics.median(after),
        "worstProviderDisagreement": max(before),
        "worstCalibratedDisagreement": max(after),
    },
    "anchoredPhrases": len(phrases),
    "points": points, "boundaries": boundaries, "phrases": phrases,
}
(build / "calibration.json").write_text(json.dumps(report, indent=2) + "\n")
for b in boundaries:
    s = b.get("acousticSilence")
    measured = f"{s['start']:7.2f}-{s['end']:7.2f}" if s else "   (no anchor)  "
    w = b.get("witness")
    seen = f"{w['lastWordEnd']:7.2f}-{w['nextWordStart']:7.2f}" if w else "  (unmatched)  "
    print(f"{b['providerEnd']:7.2f}-{b['providerNext']:7.2f} -> {measured}  heard {seen}  "
          f"{len(s['runs']) if s else 0}  {b['after'][-18:]!r} | {b['before'][:14]!r}")
for f in phrases:
    s = f["acousticSilence"]
    print(f"{f['providerEnd']:7.2f}-{f['providerNext']:7.2f} -> {s['start']:7.2f}-{s['end']:7.2f}  "
          f"phrase  {f['after'][-14:]!r} | {f['before'][:14]!r}")
print(json.dumps({k: report[k] for k in (
    "sentences", "anchoredBoundaries", "anchoredPhrases", "matchedWords", "scriptWords",
    "witness")}, indent=2))
