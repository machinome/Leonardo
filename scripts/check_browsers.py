#!/usr/bin/env python3
"""Run every registered exhibit's browser check on an ephemeral local
server."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import subprocess
import sys
from threading import Thread

from gallery import ROOT, read_catalogue, validate


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    catalogue, solid = read_catalogue()
    validate(catalogue, solid)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT))
    )
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        base = f"http://127.0.0.1:{server.server_port}"
        for name, model in catalogue["models"].items():
            command = model.get("browser_check")
            if not command:
                raise ValueError(f"No browser check registered for {name}")
            print(f"Browser check: {name}", flush=True)
            subprocess.run(
                [
                    sys.executable,
                    *[arg.replace("{base_url}", base) for arg in command],
                ],
                cwd=ROOT,
                check=True,
                timeout=model.get("browser_timeout", 180),
            )
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


if __name__ == "__main__":
    main()
