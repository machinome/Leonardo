#!/usr/bin/env python3
"""Build the portable exhibit and optionally serve it on localhost."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
import functools
import http.server
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8769)
    parser.add_argument('--build-only', action='store_true')
    parser.add_argument('--no-build', action='store_true')
    args = parser.parse_args()
    if not args.no_build:
        solid = shutil.which('solid')
        if solid is None:
            raise SystemExit('Activate the Python environment containing solid-node and its viewer extra.')
        subprocess.run([solid, 'build'], cwd=ROOT, check=True)
        subprocess.run([solid, 'export', '-o', 'export', '--frames', '480', '--fps', '30'], cwd=ROOT, check=True)
        # Ship the complete authored project, excluding generated or private state.
        source_files = ['LICENSE', 'README.md', 'pyproject.toml', '.gitignore', 'index.html', 'exhibit.js', 'exhibit.css']
        for folder in ('Leonardo_hydraulic_sawmill', 'docs', 'scripts'):
            source_files.extend(str(p.relative_to(ROOT)) for p in (ROOT / folder).rglob('*')
                                if p.is_file() and '__pycache__' not in p.parts)
        with zipfile.ZipFile(ROOT/'export/source.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
            for name in source_files:
                archive.write(ROOT/name, f'Leonardo-hydraulic-sawmill/{name}')
        print('Browser export and corresponding source: export/', flush=True)
    if args.build_only:
        return
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    print(f'Leonardo’s hydraulic sawmill: http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

if __name__ == '__main__':
    main()
