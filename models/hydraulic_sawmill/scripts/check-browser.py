#!/usr/bin/env python3
"""Finite acceptance of the real sawmill export and its explanatory exhibit."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import json
from pathlib import Path
from threading import Thread
from urllib.parse import urljoin
from zipfile import ZipFile

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[3]
OUTPUT=ROOT/'_evidence/hydraulic_sawmill/browser'


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):
        pass


def pixels(canvas):
    return Image.open(BytesIO(canvas.screenshot())).convert('RGB')


def check(url):
    OUTPUT.mkdir(parents=True,exist_ok=True)
    destination=ROOT/'export/hydraulic_sawmill'
    manifest=json.loads((destination/'manifest.json').read_text())
    assert manifest['drivers']=={}
    assert manifest['instructions']=={}
    assert manifest['animation']['loop']==296
    assert [n['name'] for n in manifest['root']['children']]==['Frame and guides','Water drive','Saw mechanism','Timber carriage','Feed mechanism']
    names=set()
    def assets(node):
        names.add(node['name'])
        if 'model' in node:
            assert (destination/node['model']).is_file()
        for child in node.get('children',[]):
            assets(child)
    assets(manifest['root'])
    assert {'Saw-to-rocker tie','Feed rocker','Driving pawl','Holding pawl','Return pulley','Haul rope','Water channel','Water surface','Uncut wood at the kerf'}<=names
    errors,failures=[],[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--enable-webgl','--use-gl=angle',
            '--use-angle=swiftshader','--enable-unsafe-swiftshader'])
        page=browser.new_page(viewport={'width':1440,'height':1200},device_scale_factor=1,
                              reduced_motion='reduce')
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.on('response',lambda r:failures.append(f'{r.status} {r.url}') if r.status>=400 else None)
        page.on('requestfailed',lambda r:failures.append(f'{r.url}: {r.failure}'))
        for width,height,label in ((1440,1200,'desktop'),(390,844,'narrow')):
            page.set_viewport_size({'width':width,'height':height})
            page.goto(url)
            page.wait_for_function("document.body.dataset.ready==='true'")
            canvas=page.locator('#stage canvas')
            expect(canvas).to_be_visible()
            assert not page.evaluate('window.exhibit.playing')
            page.locator('.assembly-tree summary').click()
            expect(page.get_by_role('tree',name='Sawmill assembly').get_by_text('Timber carriage',exact=True)).to_be_visible()
            page.locator('.assembly-tree summary').click()
            def pose(phase):
                page.locator('#timeline').fill(str(phase))
                page.locator('#timeline').dispatch_event('input')
                page.wait_for_timeout(150)
            pose(0)
            start=pixels(canvas)
            for phase,feed in ((180,'0.0'),(270,'2.0'),(360,'4.6'),(450,'4.6'),(1440,'18.4'),(4860,'59.7'),(13320,'170.0'),(26640,'340.1')):
                pose(phase)
                assert feed in page.locator('#feed').inner_text(), (phase,page.locator('#feed').inner_text())
                assert ImageChops.difference(start,pixels(canvas)).getbbox(), 'CAD did not move'
            pose(0)
            assert ImageChops.difference(start,pixels(canvas)).getbbox() is None, 'CAD pose return drifted'
            pose(13320)
            page.screenshot(path=str(OUTPUT/f'{label}-whole.png'),full_page=True)
            for name in ('drive','saw','feed'):
                page.locator(f'.view-tabs [data-view="{name}"]').click()
                page.wait_for_function(f"document.querySelector('.view-tabs [data-view={name}]').classList.contains('active')")
                page.screenshot(path=str(OUTPUT/f'{label}-{name}.png'),full_page=True)
            visible=pixels(canvas)
            page.locator('#reveal').click()
            expect(page.locator('#reveal')).to_have_attribute('aria-pressed','true')
            assert ImageChops.difference(visible,pixels(canvas)).getbbox(), 'Reveal did not hide the frame'
            page.locator('#reveal').click()
            page.locator('#reset').click()
            expect(page.locator('#timeline')).to_have_value('0')
            expect(page.locator('#status')).to_contain_text('REPLAY RESET')
            page.locator('#play').click()
            page.wait_for_function('window.exhibit.phase>20')
            moving=pixels(canvas)
            page.wait_for_timeout(250)
            assert ImageChops.difference(moving,pixels(canvas)).getbbox(), 'Playback did not move CAD'
            page.locator('#play').click()
            assert not page.evaluate('window.exhibit.playing')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'Horizontal overflow'
            print(f'PASS: {label} exhibit controls, geometry and layout',flush=True)

        source=page.request.get(page.locator('.source-link').evaluate('(a)=>a.href'))
        assert source.status==200
        with ZipFile(BytesIO(source.body())) as archive:
            assert 'Leonardo/models/hydraulic_sawmill/contact.py' in archive.namelist(), 'Source ZIP is stale'
        # Native export exposes only timeline transport and functional navigation.
        page.set_viewport_size({'width':1200,'height':950})
        page.goto(urljoin(url,'../../export/hydraulic_sawmill/?autoplay=0&sidebar=open'))
        expect(page.locator('canvas')).to_be_visible()
        expect(page.locator('input[type=range]')).to_have_count(1)
        expect(page.get_by_role('button',name='Run ',exact=False)).to_have_count(0)
        slider=page.locator('input[type=range]')
        slider.fill('0')
        slider.dispatch_event('input')
        start=pixels(page.locator('canvas'))
        slider.fill('1')
        slider.dispatch_event('input')
        page.wait_for_timeout(200)
        assert ImageChops.difference(start,pixels(page.locator('canvas'))).getbbox()
        slider.fill('0')
        slider.dispatch_event('input')
        page.wait_for_timeout(200)
        assert ImageChops.difference(start,pixels(page.locator('canvas'))).getbbox() is None
        tree=page.get_by_role('tree')
        for name in ('Frame and guides','Water drive','Saw mechanism','Timber carriage','Feed mechanism'):
            expect(tree.get_by_text(name,exact=True)).to_be_visible()
        carriage=tree.get_by_role('treeitem').filter(has=page.locator('.machinome-nav-name',has_text='Timber carriage'))
        carriage.locator('.machinome-nav-twisty').click()
        expect(tree.get_by_text('Timber',exact=True)).to_be_visible()
        timber=tree.get_by_role('treeitem').filter(has=page.get_by_text('Timber',exact=True))
        timber.press('Enter')
        expect(page.locator('.machinome-nav-full')).to_be_enabled()
        page.screenshot(path=str(OUTPUT/'native-timber-tree.png'),full_page=True)
        page.locator('.machinome-nav-full').click()
        page.screenshot(path=str(OUTPUT/'native-timeline.png'),full_page=True)
        assert not errors,errors
        assert not failures,failures
        browser.close()
    print('PASS: real export assets, timeline-only controls, functional assembly tree, complete timber course, CAD pixel return, playback, all 4 views, reveal, source ZIP, readouts, desktop/narrow; no console or network failures.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url')
    args=parser.parse_args()
    if args.url:
        check(args.url)
    else:
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT)))
        worker=Thread(target=server.serve_forever,daemon=True)
        worker.start()
        try:
            check(f'http://127.0.0.1:{server.server_port}/models/hydraulic_sawmill/')
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=5)
