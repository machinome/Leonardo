"""Explicit control-state sweeps, independent of prior tests' held poses."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from functools import wraps


def rigid_parts(node, path="loom"):
    """Public-tree traversal in the same topmost-rigid unit as root checks."""
    if node.rigid:
        yield path, node
    else:
        for child in node.children:
            yield from rigid_parts(child, path + "." + child.name)


def sampled_poses(count, end=1):
    def decorate(check):
        @wraps(check)
        def run(self):
            try:
                for index in range(count):
                    time = end * index / (count - 1)
                    self.node.set_state(phase=0, run=1, time=time)
                    try:
                        check(self)
                    except AssertionError as error:
                        raise AssertionError(
                            f"explicit time={time}: {error}"
                        ) from error
            finally:
                # clear_state() unbinds drivers; it is not a reset to their
                # defaults. Restore an explicit neutral snapshot instead.
                self.node.set_state(phase=0, run=1, time=0)

        return run

    return decorate
