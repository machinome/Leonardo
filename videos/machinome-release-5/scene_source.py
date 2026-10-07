"""Read scene classes for their words and on-screen source."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

import ast
import hashlib
import subprocess
import textwrap
from pathlib import Path


def scene_source(name):
    """Inspect declarations without importing or executing the movie."""
    source = Path(__file__).with_name("movie.py").read_text()
    nodes = [node for node in ast.parse(source).body
             if isinstance(node, ast.ClassDef) and node.name == name]
    if len(nodes) != 1:
        raise ValueError(f"Expected one movie scene class: {name}")
    return source, nodes[0]


def scene_narration(name):
    """The class's literal feeds the single continuous take."""
    _, node = scene_source(name)
    for statement in node.body:
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "narration"
            for target in statement.targets
        ):
            text = ast.literal_eval(statement.value)
            if isinstance(text, str) and text.strip():
                return text
    raise ValueError(f"Scene needs literal narration: {name}")


def excerpt(name):
    """Return the complete class, not a display-only example."""
    source, node = scene_source(name)
    return dict(
        code="\n".join(source.splitlines()[node.lineno - 1:node.end_lineno]),
        file=f"movie.py / {name}",
        digest=hashlib.sha256(source.encode()).hexdigest(),
        numbers=list(range(node.lineno, node.end_lineno + 1)),
    )


def model_excerpt(relative, ranges):
    """Read exact committed project source, retaining original line numbers."""
    root = Path(__file__).resolve().parents[2]
    source = (root / relative).read_bytes()
    committed = subprocess.check_output(
        ["git", "show", f"HEAD:{relative}"], cwd=root
    )
    if committed != source:
        raise ValueError(f"Uncommitted model source: {relative}")
    lines = source.decode().splitlines()
    numbers = [n for first, last in ranges for n in range(first, last + 1)]
    return dict(
        code=textwrap.dedent("\n".join(lines[n - 1] for n in numbers)),
        file=relative,
        digest=hashlib.sha256(source).hexdigest(),
        numbers=numbers,
    )


def token_line(name, row, token):
    """Locate a unique source row for a word-aligned highlight."""
    data = excerpt(name)
    matches = [number for number, line in zip(data["numbers"], data["code"].splitlines())
               if line.lstrip().startswith(row) and token in line]
    if len(matches) != 1:
        raise ValueError(f"Expected one row for {name}: {row}")
    return matches[0]
