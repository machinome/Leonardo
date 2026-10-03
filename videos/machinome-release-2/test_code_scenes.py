"""Keep the film's two source reveals literal, contextual and spoken."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

import ast
import json
from pathlib import Path
import unittest


HERE = Path(__file__).resolve().parent


class CodeScenesTest(unittest.TestCase):
    def setUp(self):
        self.source = (HERE / "movie.py").read_text()
        self.tree = ast.parse(self.source)

    def scene(self, name):
        matches = [
            node for node in self.tree.body
            if isinstance(node, ast.ClassDef) and node.name == name
        ]
        self.assertEqual(len(matches), 1, f"Missing scene class: {name}")
        return matches[0]

    def words(self, node):
        values = [
            statement.value for statement in node.body
            if isinstance(statement, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "narration"
                    for t in statement.targets)
        ]
        self.assertEqual(len(values), 1)
        return ast.literal_eval(values[0])

    def test_both_reveals_are_complete_classes(self):
        for name in ("CrankStroke", "ThisScene"):
            node = self.scene(name)
            self.assertIn("shot = Shot(", ast.get_source_segment(
                self.source, node))
            self.assertLessEqual(node.end_lineno - node.lineno + 1, 24)

    def test_punchline_is_executable_narration_not_a_comment(self):
        self.assertEqual(
            self.words(self.scene("ThisScene")),
            "And here's the code of this exact scene! How cool is that?",
        )

    def test_simulation_context_keeps_camera_and_highlights(self):
        node = self.scene("CrankStroke")
        source = ast.get_source_segment(self.source, node)
        self.assertIn("view = View(Sawmill", source)
        self.assertIn("view.move(Sawmill.saw", source)
        self.assertIn("view.highlight(Mill.water_drive.crank", source)
        self.assertNotIn("How cool", source)

    def test_scene_words_are_the_source_of_the_one_approved_script(self):
        from narration import MECHANISM, THIS_SCENE, document
        self.assertIn(self.words(self.scene("CrankStroke")), MECHANISM)
        self.assertEqual(self.words(self.scene("ThisScene")), THIS_SCENE)
        approved = json.loads((HERE / "_build/narration-manifest.json")
                              .read_text())
        self.assertEqual(document()["chapters"][0]["narration"],
                         approved["text"])
        self.assertEqual(len(document()["chapters"]), 1)

    def test_literal_excerpts_are_complete_and_not_transcribed(self):
        from scene_source import excerpt, scene_narration
        for name in ("CrankStroke", "ThisScene"):
            node = self.scene(name)
            self.assertEqual(excerpt(name)["code"],
                             ast.get_source_segment(self.source, node))
            self.assertEqual(scene_narration(name), self.words(node))

    def test_class_literal_drives_speech_instead_of_a_second_copy(self):
        from scene_source import scene_narration
        from unittest.mock import patch
        modified = self.source.replace("How cool is that?", "Changed words.")
        with patch("scene_source.Path.read_text", return_value=modified):
            self.assertTrue(scene_narration("ThisScene")
                            .endswith("Changed words."))


if __name__ == "__main__":
    unittest.main()
