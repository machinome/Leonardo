#!/usr/bin/env python3
"""Build the portable carpentry study and its exact cutting book."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]


def main():
    cli = shutil.which("machinome")
    if cli is None:
        raise SystemExit(
            "Activate the environment containing machinome and its viewer."
        )
    out = ROOT / "export/hydraulic_sawmill-frame"
    env = dict(
        os.environ,
        PYTHONPATH=str(ROOT),
        SOLID_BUILD_DIR=str(ROOT / "_build/hydraulic_sawmill-frame"),
    )
    subprocess.run(
        [
            cli,
            "export",
            "models/hydraulic_sawmill/frame.py:FrameCarpentry",
            "-o",
            str(out),
        ],
        cwd=ROOT,
        env=env,
        check=True,
    )
    shutil.copyfile(out / "index.html", out / "native.html")
    shutil.copyfile(
        Path(__file__).parents[1] / "carpentry.html", out / "index.html"
    )
    subprocess.run(
        [sys.executable, str(Path(__file__).with_name("cutting-book.py"))],
        cwd=ROOT,
        env=env,
        check=True,
    )
    subprocess.run(
        [
            "git",
            "archive",
            "--format=zip",
            "--prefix=Leonardo/",
            f'--output={out / "source.zip"}',
            "HEAD",
        ],
        cwd=ROOT,
        check=True,
    )
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    )
    (out / "source-revision.txt").write_text(revision)
    print(f'Frame study: {out / "index.html"}')


if __name__ == "__main__":
    main()
