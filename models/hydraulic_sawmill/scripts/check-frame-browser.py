#!/usr/bin/env python3
"""Finite browser acceptance of the real exported carpentry model and book."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
import csv
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import json
from pathlib import Path
from threading import Thread
from urllib.parse import urljoin

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT/'_evidence/hydraulic_sawmill/carpentry-browser'


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def pixels(canvas):
    result = Image.open(BytesIO(canvas.screenshot())).convert('RGB')
    assert len(result.getcolors(result.width*result.height) or []) > 30
    return result


def check(url):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((ROOT/'export/hydraulic_sawmill-frame/manifest.json').read_text())
    assert set(manifest['drivers']) == {'disassembly'}
    assert len(manifest['instructions']) == 12
    book = ROOT/'export/hydraulic_sawmill-frame/carpentry'
    for filename, count in (('cut-list.csv',24),('pegs.csv',34)):
        with (book/filename).open() as stream:
            assert len(list(csv.DictReader(stream))) == count
    assert len(list(book.glob('*.step'))) == 58
    errors, failures = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--enable-webgl','--use-gl=angle',
            '--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        page = browser.new_page(viewport={'width':1440,'height':1000}, reduced_motion='reduce')
        page.on('pageerror',lambda error: errors.append(str(error)))
        page.on('console',lambda message: errors.append(message.text) if message.type=='error' else None)
        page.on('response',lambda response: failures.append(f'{response.status} {response.url}') if response.status>=400 else None)
        page.on('requestfailed',lambda request: failures.append(f'{request.url}: {request.failure}'))
        for width, height, label in ((1440,1000,'desktop'), (390,844,'narrow')):
            page.set_viewport_size({'width':width,'height':height})
            page.goto(url, wait_until='networkidle')
            page.wait_for_function("document.body.dataset.ready==='true'")
            canvas = page.locator('canvas').first
            expect(canvas).to_be_visible()
            page.wait_for_timeout(300)
            slider = page.locator('input[type=range][max="11"]')
            expect(slider).to_be_visible()
            start = pixels(canvas)
            slider.fill('11')
            slider.dispatch_event('input')
            page.wait_for_timeout(300)
            assert ImageChops.difference(start, pixels(canvas)).getbbox(), 'Assembly slider did not move CAD'
            page.screenshot(path=str(OUTPUT/f'{label}-separated.png'),full_page=True)
            slider.fill('0')
            slider.dispatch_event('input')
            page.wait_for_timeout(300)
            returned = pixels(canvas)
            start.save(OUTPUT/f'{label}-start.png')
            returned.save(OUTPUT/f'{label}-returned.png')
            delta = ImageChops.difference(start,returned)
            assert delta.getbbox() is None, f'Reassembly changed pixels in {delta.getbbox()}'
            page.get_by_text('03 · Lift tower crosshead',exact=True).click()
            page.wait_for_timeout(2300)
            expect(slider).to_have_value('3')
            assert ImageChops.difference(start,pixels(canvas)).getbbox(), 'Stage instruction did not move CAD'
            page.screenshot(path=str(OUTPUT/f'{label}-crosshead.png'),full_page=True)
            page.get_by_role('button',name='Show the whole frame').click()
            page.get_by_text('Find a timber or pin',exact=True).click()
            tree = page.get_by_role('tree',name='Frame timbers and pins')
            expect(tree).to_be_visible()
            for name in ('Buildable sawmill frame','Fixed timber structure','Horizontal bed frame'):
                row = tree.get_by_role('treeitem').filter(has=page.get_by_text(name,exact=True))
                if row.get_attribute('aria-expanded') != 'true':
                    row.locator('.machinome-nav-twisty').click()
            whole = pixels(canvas)
            leaf = tree.get_by_role('treeitem').filter(has=page.get_by_text('L2 · Table leg',exact=True))
            leaf.press('Enter')
            assert ImageChops.difference(whole,pixels(canvas)).getbbox(), 'Timber isolation did not change CAD'
            page.get_by_role('button',name='Show the whole frame').click()
            assert ImageChops.difference(whole,pixels(canvas)).getbbox() is None, 'Restoring the whole frame drifted'
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
            page.goto(urljoin(url,'carpentry/'),wait_until='networkidle')
            expect(page.get_by_role('heading',name='The sawmill frame: cutting book')).to_be_visible()
            assert page.locator('section').count() == 24
            assert page.locator('img').count() == 96
            assert page.locator('img').evaluate_all('(xs)=>xs.every(x=>x.complete && x.naturalWidth>0)')
            clipped = page.evaluate('''async () => {
              const bad=[];
              for(const img of document.querySelectorAll('img')) {
                const xml=await (await fetch(img.src)).text();
                const svg=document.importNode(new DOMParser().parseFromString(xml,'image/svg+xml').documentElement,true);
                svg.style.cssText='position:absolute;left:0;top:0;visibility:hidden';document.body.append(svg);
                const g=svg.querySelector('g'), b=g.getBBox(), m=g.getCTM();
                const corners=[[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]]
                  .map(([x,y])=>new DOMPoint(x,y).matrixTransform(m));
                if(corners.some(p=>p.x<0 || p.y<0 || p.x>svg.width.baseVal.value || p.y>svg.height.baseVal.value))bad.push(img.src);
                svg.remove();
              }
              return bad;
            }''')
            assert not clipped, f'Clipped cutting drawings: {clipped}'
            page.screenshot(path=str(OUTPUT/f'{label}-book-overview.png'))
            page.locator('details').first.locator('summary').click()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1')
            page.screenshot(path=str(OUTPUT/f'{label}-cutting-book.png'))
        assert not errors, errors
        assert not failures, failures
        browser.close()
    print('PASS: frame CAD moves and reassembles, stage instructions, 24-member cutting book, desktop/narrow, assets and console.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url')
    args = parser.parse_args()
    if args.url:
        check(args.url)
    else:
        server = ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
        worker = Thread(target=server.serve_forever,daemon=True)
        worker.start()
        try:
            check(f'http://127.0.0.1:{server.server_port}/export/hydraulic_sawmill-frame/')
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=5)
