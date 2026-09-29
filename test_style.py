"""PEP 8 regression checks for the gallery's Python source."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from pathlib import Path
import subprocess
import unittest

import pycodestyle

ROOT = Path(__file__).resolve().parent


def check_python_style(directory=ROOT):
    """Check existing and new source files, excluding build output."""
    paths = (
        subprocess.check_output(
            [
                "git",
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "*.py",
            ],
            cwd=directory,
        )
        .decode()
        .split("\0")
    )
    files = [str(directory / path) for path in paths if path]
    if not files:
        raise AssertionError(f"No Python sources found in {directory}")
    style = pycodestyle.StyleGuide(config_file=str(ROOT / "setup.cfg"))
    report = style.check_files(files)
    if report.total_errors:
        raise AssertionError(f"{report.total_errors} PEP 8 violations")


class PythonStyleTest(unittest.TestCase):
    def test_python_sources_follow_pep8(self):
        check_python_style()


if __name__ == "__main__":
    unittest.main()
