#!/usr/bin/env python3
"""Build the portable exhibit and optionally serve it on localhost."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
import functools
import http.server
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8769)
    parser.add_argument('--build-only', action='store_true')
    parser.add_argument('--no-build', action='store_true')
    args = parser.parse_args()
    if not args.no_build:
        solid = shutil.which('machinome')
        if solid is None:
            raise SystemExit('Activate the Python environment containing machinome and its viewer extra.')
        subprocess.run([sys.executable, str(ROOT / 'scripts/gallery.py'),
                        'export', 'hydraulic_sawmill'], cwd=ROOT, check=True)
        print('Browser export and committed source: export/hydraulic_sawmill/', flush=True)
    if args.build_only:
        return
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    print(f'Leonardo’s hydraulic sawmill: http://127.0.0.1:{args.port}/models/hydraulic_sawmill/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == '__main__':
    main()
