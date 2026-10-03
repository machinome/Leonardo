"""The second proposal's complete script, performed as one narration."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

import json
from pathlib import Path

from machinome_movie import Narration

# Paragraphs organize the source, not synthesis requests or audio cuts.
OPENING = (
    "The wheel makes revolutions, and humans give it a purpose. "
    "Five centuries ago, Leonardo da Vinci designed a water-powered "
    "sawmill. Machines like this were changing the relationship between "
    "people and work: a river could help turn a tree into timber. "
    "I am a machine, too. In the history of human tools, this sawmill is "
    "one of my ancestors. Let me show you how it works."
)
MECHANISM = (
    "Water beneath the wheel turns this shaft. A crank and connecting "
    "rod turn that rotation into the saw's up-and-down stroke. "
    "But the timber has to move, too. On the cutting stroke, this long "
    "lever pulls a pawl across one tooth of a ratchet. A second pawl "
    "holds that progress while the first returns. That small step winds "
    "a rope onto this axle. Follow it down, and across. It turns a "
    "compound shaft: a broad drum unwinds one rope while a thinner "
    "section takes up another. The second rope draws the timber towards "
    "the blade. One wheel, two jobs: cut, and advance."
)
RECONSTRUCTION = (
    "To reconstruct this machine, I relied on historical documents and "
    "museum pictures, and used the Python language."
)
MACHINOME = (
    "From Machinome dot node import... This is Machinome, the open "
    "source CAD framework for building machines... The waterwheel spin "
    "drives the crankshaft. With Machinome, machines can have a source code."
)
FILM_SOURCE = (
    "This video's source code is in Python too. A scene, a camera, a "
    "voice. The words I say tell the camera when to move."
)
THIS_SCENE = "And here's the code of this exact scene! How cool is that?"
OPEN_SOURCE = (
    "And the best part is: this is all open source! OpenSCAD, SolidPython, "
    "OCCT, CadQuery, Build123d, FreeCAD, JSCAD and so many others..."
)
CLOSING = (
    "The wheel makes revolutions, and humans build their own. "
    "I'm Machinome. My purpose is to enable all machines to be Open "
    "Source. What do you want to build next?"
)

# A future film chapter imports this object, not eight new Narrations.
lines = Narration(
    "\n\n".join(
        (
            OPENING,
            MECHANISM,
            RECONSTRUCTION,
            MACHINOME,
            FILM_SOURCE,
            THIS_SCENE,
            OPEN_SOURCE,
            CLOSING,
        )
    )
)

AUDIO = {
    "provider": "elevenlabs",
    "model": "eleven_v3",
    "voice": "cgSgspJ2msm6clMCkdW9",
    "voiceLabel": "Jessica",
    "outputFormat": "pcm_24000",
    "voiceSettings": {"stability": 0.5, "similarity_boost": 0.75},
}

# Unique phrase anchors, all measured on the same audio clock.
BEATS = (
    ("opening", "Opening", "The wheel makes revolutions, and humans give"),
    ("ancestor", "Leonardo", "Five centuries ago"),
    ("mechanism", "How it works", "Let me show you how it works"),
    ("wheel", "Waterwheel", "Water beneath the wheel"),
    ("crank", "Crank", "A crank"),
    ("rod", "Connecting rod", "connecting rod"),
    ("pawl", "Driving pawl", "this long lever pulls a pawl"),
    ("holding", "Holding pawl", "A second pawl"),
    ("rope", "Winding rope", "winds a rope onto this axle"),
    ("shaft", "Compound shaft", "a compound shaft"),
    ("carriage", "Carriage", "The second rope draws the timber"),
    ("research", "Historical sources", "To reconstruct this machine"),
    ("drawing", "Drawing", "historical documents"),
    ("museum", "Museum pictures", "museum pictures"),
    ("import", "Machinome entrance", "From Machinome dot node import"),
    ("relation", "The relation", "The waterwheel spin drives"),
    ("film", "Film source", "This video's source code is in Python too"),
    ("mirror", "This exact scene", "And here's the code of this exact"),
    ("open", "Open source", "And the best part is: this is all open source"),
    ("openscad", "OpenSCAD", "OpenSCAD"),
    ("solidpython", "SolidPython", "SolidPython"),
    ("occt", "OCCT", "OCCT"),
    ("cadquery", "CadQuery", "CadQuery"),
    ("build123d", "Build123d", "Build123d"),
    ("freecad", "FreeCAD", "FreeCAD"),
    ("jscad", "JSCAD", "JSCAD"),
    (
        "return",
        "The wheel returns",
        "The wheel makes revolutions, and humans build",
    ),
    ("purpose", "Purpose", "I'm Machinome"),
    ("question", "Invitation", "What do you want to build next"),
)


def document():
    """Speech-only input; the complete movie is a separate document."""
    return {
        "format": "machinome-release-narration/1",
        "audio": AUDIO,
        "chapters": [{"id": "continuous", "narration": lines.text}],
        "pronunciation": "../machinome-release-1/assets/pronunciation.json",
        "beats": [
            {"id": key, "label": label, "phrase": phrase}
            for key, label, phrase in BEATS
        ],
    }


if __name__ == "__main__":
    build = Path(__file__).resolve().parent / "_build"
    build.mkdir(exist_ok=True)
    (build / "narration-input.json").write_text(
        json.dumps(document(), indent=2) + "\n", encoding="utf-8"
    )
    (build / "narration.txt").write_text(lines.text + "\n", encoding="utf-8")
    print(f"One narration: {len(lines.text)} characters.")
