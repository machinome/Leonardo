#!/usr/bin/env python3
"""Inspect the queue and build, test or export registered Leonardo models."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def read_catalogue():
    with (ROOT / "gallery.toml").open("rb") as stream:
        catalogue = tomllib.load(stream)
    with (ROOT / "pyproject.toml").open("rb") as stream:
        manifest = tomllib.load(stream)
    return catalogue, manifest["tool"]["solid-node"]


def validate(catalogue, solid):
    models = solid["models"]
    if set(models) != set(catalogue["models"]):
        raise ValueError("gallery.toml and pyproject.toml model inventories differ")
    if solid["model"] not in models:
        raise ValueError("The default model is not registered")
    queue = catalogue["queue"]
    if not queue or queue[-1]["kind"] != "site":
        raise ValueError("The public site must be the final queue item")
    seen = set()
    unfinished = False
    for index, item in enumerate(queue):
        if item["id"] in seen:
            raise ValueError(f"Duplicate queue item: {item['id']}")
        seen.add(item["id"])
        if item["status"] not in {"pending", "in_progress", "done"}:
            raise ValueError(f"Unknown status: {item['id']}")
        if item["kind"] not in {"machine", "site"}:
            raise ValueError(f"Unknown kind: {item['id']}")
        if item["kind"] == "site" and index != len(queue) - 1:
            raise ValueError("Only the last item may be a site")
        if unfinished and item["status"] != "pending":
            raise ValueError(f"Queue order violated at {item['id']}")
        unfinished |= item["status"] != "done"
        if item["kind"] == "machine" and item["status"] == "done":
            if item["model"] not in models:
                raise ValueError(f"Completed model is not registered: {item['id']}")
            archive = ROOT / catalogue["models"][item["model"]]["directory"] / "openspec/changes/archive"
            if not list(archive.glob("*/tasks.md")):
                raise ValueError(f"Completed model has no archived cycle: {item['id']}")
    for name, ref in models.items():
        folder = ROOT / catalogue["models"][name]["directory"]
        if folder != ROOT / "models" / name:
            raise ValueError(f"Unexpected machine directory: {name}")
        for required in ("model.py", "test_model.py", "README.md", "openspec/config.yaml"):
            if not (folder / required).is_file():
                raise ValueError(f"Missing {name}/{required}")
        module, separator, cls = ref.partition(":")
        if not separator or not cls or module != f"models.{name}.model":
            raise ValueError(f"Unexpected model reference: {name} = {ref}")
        if not list((folder / "openspec/specs").glob("*/spec.md")):
            raise ValueError(f"Missing machine baseline specs: {name}")
    for path in (ROOT / "models").rglob("pyproject.toml"):
        raise ValueError(f"Nested manifest is not allowed: {path.relative_to(ROOT)}")
    for path in (ROOT / "models").rglob(".git"):
        raise ValueError(f"Nested repository is not allowed: {path.relative_to(ROOT)}")


def run_models(command, names, catalogue, kernel):
    solid = shutil.which("solid")
    if not solid:
        raise ValueError("Activate the environment with solid-node and its viewer")
    for name in names:
        info = catalogue["models"][name]
        env = os.environ.copy()
        env["SOLID_BUILD_DIR"] = str(ROOT / "_build" / name)
        env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(ROOT), env.get("PYTHONPATH")]))
        args = [solid, command, name]
        if command == "test":
            args.append(f"--{kernel}")
        elif command == "export":
            args.extend(["-o", str(ROOT / "export" / name), "--fps", str(info["fps"]),
                         "--frames", str(info["frames"])])
        print(f"{name}: {' '.join(args)}", flush=True)
        subprocess.run(args, cwd=ROOT, env=env, check=True)
        if command == "export":
            # A git archive contains committed source, never ignored/private files.
            destination = ROOT / "export" / name
            subprocess.run(["git", "archive", "--format=zip", "--prefix=Leonardo/",
                            f"--output={destination / 'source.zip'}", "HEAD"],
                           cwd=ROOT, check=True)
            revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True)
            (destination / "source-revision.txt").write_text(revision)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["next", "list", "check", "build", "test", "export"])
    parser.add_argument("models", nargs="*")
    parser.add_argument("--kernel", choices=["exact", "faceted"], default="exact")
    args = parser.parse_args()
    catalogue, solid = read_catalogue()
    # Queue reading must work while a new machine's baseline is being written.
    if args.command == "next":
        item = next((item for item in catalogue["queue"] if item["status"] != "done"), None)
        if item is None:
            print("Queue complete. Verify the site record; publication belongs to the pilot.")
        else:
            print(f"{item['id']} [{item['status']}]: {item['title']}\nRead AGENTS.md and {item['brief']}")
        return
    if args.command == "list":
        for name, ref in solid["models"].items():
            print(f"{name}: {ref}")
        for item in catalogue["queue"]:
            print(f"{item['id']} [{item['status']}]: {item['title']}")
        return
    validate(catalogue, solid)
    if args.command == "check":
        print(f"PASS: {len(solid['models'])} models, separate OpenSpec roots, one repository; queue coherent.")
        return
    names = args.models or list(solid["models"])
    unknown = set(names) - set(solid["models"])
    if unknown:
        parser.error(f"Unknown model(s): {', '.join(sorted(unknown))}")
    run_models(args.command, names, catalogue, args.kernel)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
