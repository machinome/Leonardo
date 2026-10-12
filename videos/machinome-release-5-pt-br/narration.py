"""Release candidate 5: one fresh Jessica performance, with directed emphasis."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

import json
from pathlib import Path

from machinome.movie import Narration
from scene_source import scene_narration

# Ellipsis and paragraph separation request a pause; YOU requests vocal emphasis.
# One complete Eleven v3 request, no name pickups or stitching.
OPENING = (
    "The wheel makes revolutions, and humans give it a purpose. "
    "Five centuries ago, Leonardo da Vinci designed a water-powered "
    "sawmill. Machines like this were changing the relationship between "
    "people and work: a river could help turn a tree into timber. "
    "I am a machine, too. In the history of human tools, this sawmill is "
    "one of my ancestors. Let me show you how it works."
)
MECHANISM = (
    "Water beneath the wheel turns this shaft. "
    + scene_narration("CrankStroke")
    + " But the timber has to move, too. On the cutting stroke, this long "
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
    "From Machinome dot node dot assembly import AssemblyNode. This is Machinome, the open "
    "source CAD framework for building machines... The waterwheel spin "
    "drives the crankshaft."
)
STUDIO = (
    "You can build models from your browser, using Machinome Studio, "
    "where you can prompt your agents, "
    "see the source code, build the project, and interact with the model "
    "to see different angles and moments of the animation."
)
TESTING = (
    "Machinome also provides a testing framework, "
    "that allows us to test how parts fit together. "
    "This test checks that the blade does not intersect either half "
    "of the timber. Testing steps repeats those assertions at thirteen "
    "instants from zero to four seconds: one full wheel turn. "
    "Each sample poses the machine again, then checks the geometry. "
)
FILM_SOURCE = (
    "This video's source code is in Python too. "
    "A narration, a camera, a shot. "
    "Cues move the camera and highlight the saw in sync with the spoken words."
)
THIS_SCENE = scene_narration("ThisScene")
OPEN_SOURCE = (
    "And the best part is: this is all open source! "
    "Machinome connects existing CAD technologies: "
    "OpenSCAD, SolidPython, CadQuery, Build123d, FreeCAD, JSCAD, OCCT, Trimesh."
)
STREAM = "And beneath it all, a stream of open source technologies..."
CLOSING = (
    "The wheel... makes revolutions... and humans... build their own. "
    "I'm Machinome. My purpose is to enable all machines to be Open "
    "Source. What do YOU want to BUILD?"
)

# A future film chapter imports this object, not eight new Narrations.
lines = Narration(
    "\n\n".join(
        (
            OPENING,
            MECHANISM,
            RECONSTRUCTION,
            MACHINOME,
            STUDIO,
            TESTING,
            FILM_SOURCE,
            THIS_SCENE,
            OPEN_SOURCE,
            STREAM,
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
    # Narration normalizes whitespace; restore this delivery break in TTS only.
    "replacements": {"technologies... The wheel": "technologies...\n\nThe wheel"},
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
    ("import", "Machinome entrance", "From Machinome dot node dot assembly import"),
    ("relation", "The relation", "The waterwheel spin drives"),
    ("studio-transition", "Into the browser", "You can build models from your browser"),
    ("studio", "Machinome Studio", "using Machinome Studio"),
    ("prompt", "Prompt your agents", "prompt your agents"),
    ("source-menu", "Source code", "see the source code"),
    ("build-menu", "Build the project", "build the project"),
    ("interact", "Interact with the model", "interact with the model"),
    ("angles", "Different angles", "different angles"),
    ("moments", "Animation timeline", "moments of the animation"),
    ("testing", "Testing geometry", "Machinome also provides a testing framework"),
    ("test-code", "Testing source", "to test how parts fit together"),
    ("steps", "Testing steps", "Testing steps repeats"),
    ("film", "Film source", "This video's source code is in Python too"),
    ("mirror", "This exact scene", "And here's the code of this exact"),
    ("open", "Open source", "And the best part is: this is all open source"),
    ("cad", "CAD technologies", "Machinome connects existing CAD technologies"),
    ("openscad", "OpenSCAD", "OpenSCAD"),
    ("solidpython", "SolidPython", "SolidPython"),
    ("occt", "OCCT", "OCCT"),
    ("cadquery", "CadQuery", "CadQuery"),
    ("build123d", "Build123d", "Build123d"),
    ("freecad", "FreeCAD", "FreeCAD"),
    ("jscad", "JSCAD", "JSCAD"),
    ("trimesh", "Trimesh", "Trimesh"),
    ("stream", "Open source stream", "And beneath it all"),
    (
        "return",
        "The wheel returns",
        "The wheel... makes revolutions... and humans... build",
    ),
    ("purpose", "Purpose", "I'm Machinome"),
    ("question", "Invitation", "What do YOU want to BUILD"),
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
