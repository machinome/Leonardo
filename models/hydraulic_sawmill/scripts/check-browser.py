#!/usr/bin/env python3
"""Check the real exported exhibit in headless Chromium."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--url', default='http://127.0.0.1:8769/models/hydraulic_sawmill/')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
(root / 'evidence').mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--enable-webgl', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    page = browser.new_page(viewport={'width':1440, 'height':1200}, device_scale_factor=1)
    errors = []
    failures = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('response', lambda r: failures.append(f'{r.status} {r.url}') if r.status >= 400 else None)
    page.goto(args.url)
    page.wait_for_function("document.body.dataset.ready === 'true'")
    assert page.locator('#stage canvas').count() == 1
    page.locator('#play').click()
    page.locator('#timeline').fill('0')
    page.locator('#timeline').dispatch_event('input')
    first_pose = page.locator('#stage canvas').screenshot()
    page.locator('#timeline').fill('450')
    page.locator('#timeline').dispatch_event('input')
    assert page.locator('#angle').inner_text() == '90°'
    assert '8.0' in page.locator('#feed').inner_text()
    assert page.locator('#stage canvas').screenshot() != first_pose, 'The geometry did not move'
    page.screenshot(path=str(root/'evidence/browser-desktop.png'), full_page=True)
    page.locator('#reveal').click()
    assert page.locator('#reveal').get_attribute('aria-pressed') == 'true'
    page.locator('.view-tabs [data-view="drive"]').click()
    page.wait_for_function("document.querySelector('.view-tabs [data-view=drive]').classList.contains('active')")
    page.screenshot(path=str(root/'evidence/browser-drive.png'), full_page=True)
    page.locator('#reveal').click()
    page.locator('.view-tabs [data-view="whole"]').click()
    page.wait_for_function("document.querySelector('.view-tabs [data-view=whole]').classList.contains('active')")
    page.locator('#reset').click()
    assert page.locator('#timeline').input_value() == '0'
    page.locator('#play').click()
    page.wait_for_function('window.exhibit.phase > 20')
    page.locator('#play').click()
    assert not page.evaluate('window.exhibit.playing')
    source_url = page.locator('.source-link').evaluate('(a) => a.href')
    assert page.request.get(source_url).status == 200
    page.set_viewport_size({'width':390, 'height':844})
    page.reload()
    page.wait_for_function("document.body.dataset.ready === 'true'")
    page.locator('#play').click()
    page.screenshot(path=str(root/'evidence/browser-mobile.png'), full_page=True)
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert not errors, errors
    assert not failures, failures
    print('PASS: WebGL model, scrubbing, feed readout, reveal, camera views, reset, playback, source archive, mobile layout; no browser errors.')
    browser.close()
