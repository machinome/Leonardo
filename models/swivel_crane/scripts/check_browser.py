#!/usr/bin/env python3
"""Finite smoke of the real crane export, controls, geometry and local assets."""
# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
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
OUTPUT = ROOT / "_evidence/swivel_crane"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def scene_pixels(page, canvas):
    """Capture only CAD pixels below controls, so changed input text cannot pass."""
    canvas.scroll_into_view_if_needed()
    b = canvas.bounding_box()
    result = Image.open(BytesIO(page.screenshot(clip={
        "x": b["x"], "y": b["y"]+275, "width": b["width"],
        "height": b["height"]-315}))).convert("RGB")
    background = Image.new("RGB", result.size, result.getpixel((0, 0)))
    bounds = ImageChops.difference(result, background).getbbox()
    assert bounds and bounds[0] > 2 and bounds[2] < result.width-2, "CAD is empty or horizontally cropped"
    return result


def check(url):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    export = ROOT / "export/swivel_crane"
    manifest = json.loads((export / "manifest.json").read_text())
    assert set(manifest["drivers"]) == {"slew", "traverse", "hoist", "run"}
    assert set(manifest["instructions"]) == {"Pick up", "Lift clear", "Swing", "Place", "Demonstrate"}

    def walk(node):
        if "model" in node:
            assert (export / node["model"]).is_file(), node["model"]
        for child in node.get("children", []):
            walk(child)

    walk(manifest["root"])
    errors, failures = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1200}, device_scale_factor=1)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("response", lambda r: failures.append(f"{r.status} {r.url}") if r.status >= 400 else None)
        page.on("requestfailed", lambda r: failures.append(f"{r.url}: {r.failure}"))
        for width, height, label in ((1440, 1200, "desktop"), (390, 1000, "narrow")):
            print(f"Checking crane {label} controls and geometry", flush=True)
            page.set_viewport_size({"width": width, "height": height})
            page.goto(url, wait_until="networkidle")
            frame = page.frame_locator("iframe")
            canvas = frame.locator("canvas")
            expect(canvas).to_be_visible()

            def value(name):
                unit = "deg" if name == "slew" else "play" if name == "run" else "mm"
                return frame.get_by_label(f"{name} exact value ({unit})", exact=True)

            def stage(name, coords):
                frame.get_by_role("button", name=f"Run {name}", exact=True).click()
                for key, target in zip(("slew", "traverse", "hoist", "run"), coords):
                    expect(value(key)).to_have_value(f"{target:.4f}")
                page.wait_for_timeout(120)

            stage("Pick up", (-45, 0, 0, 0))
            frame.get_by_title("Pause", exact=True).click()
            timeline = frame.locator('input[type="range"]').first
            timeline.fill("0")
            timeline.dispatch_event("input")
            page.wait_for_timeout(120)
            pickup = scene_pixels(page, canvas)
            previous = pickup
            for name, coords in (("Lift clear", (-45, 0, 25, 0)),
                                 ("Swing", (45, 60, 25, 0)), ("Place", (45, 60, 0, 0))):
                stage(name, coords)
                current = scene_pixels(page, canvas)
                assert ImageChops.difference(previous, current).getbbox(), f"{name} did not move CAD"
                previous = current
            stage("Pick up", (-45, 0, 0, 0))
            assert ImageChops.difference(pickup, scene_pixels(page, canvas)).getbbox() is None, "Pose return drifted"
            # Every physical coordinate changes CAD independently and preserves the others.
            for name, target, unit in (("slew", 17, "deg"), ("traverse", 23, "mm"), ("hoist", 11, "mm")):
                before = scene_pixels(page, canvas)
                held = {key: value(key).input_value() for key in ("slew", "traverse", "hoist") if key != name}
                frame.get_by_role("button", name=f"Edit {name} exact value ({unit})", exact=True).click()
                value(name).fill(str(target))
                value(name).press("Enter")
                expect(value(name)).to_have_value(f"{target:.4f}")
                for key, prior in held.items():
                    expect(value(key)).to_have_value(prior)
                page.wait_for_timeout(120)
                assert ImageChops.difference(before, scene_pixels(page, canvas)).getbbox(), f"Manual {name} did not move CAD"
            # Slider, playback, timeline scrub and closure all use the real viewer.
            slider = frame.get_by_label("traverse (mm)", exact=True)
            slider.fill("30")
            slider.dispatch_event("input")
            expect(value("traverse")).to_have_value("30.0000")
            if label == "narrow":
                # All three manual controls and four named stages were exercised
                # at both widths. Playback/loop mechanics are checked on desktop.
                stage("Swing", (45, 60, 25, 0))
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Page overflow"
                assert page.frames[1].evaluate("document.documentElement.scrollWidth <= innerWidth"), "Viewer overflow"
                page.screenshot(path=str(OUTPUT / f"browser-{label}.png"), full_page=True)
                continue
            frame.get_by_role("button", name="Run Demonstrate", exact=True).click()
            expect(value("run")).to_have_value("1.0000")
            timeline.fill("0")
            timeline.dispatch_event("input")
            page.wait_for_timeout(120)
            loop_start = scene_pixels(page, canvas)
            timeline.fill(timeline.get_attribute("max"))
            timeline.dispatch_event("input")
            page.wait_for_timeout(120)
            assert ImageChops.difference(loop_start, scene_pixels(page, canvas)).getbbox() is None, "Loop reset jumped"
            timeline.fill("100")
            timeline.dispatch_event("input")
            page.wait_for_timeout(120)
            assert ImageChops.difference(loop_start, scene_pixels(page, canvas)).getbbox(), "Scrub did not move CAD"
            frame.get_by_title("Play", exact=True).click()
            tick = timeline.input_value()
            expect(timeline).not_to_have_value(tick)
            playing = scene_pixels(page, canvas)
            page.wait_for_timeout(500)
            assert ImageChops.difference(playing, scene_pixels(page, canvas)).getbbox(), "Playback did not move CAD"
            frame.get_by_title("Pause", exact=True).click()
            stage("Swing", (45, 60, 25, 0))
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Page overflow"
            assert page.frames[1].evaluate("document.documentElement.scrollWidth <= innerWidth"), "Viewer overflow"
            page.screenshot(path=str(OUTPUT / f"browser-{label}.png"), full_page=True)
        for link in page.locator("a").all():
            href = link.get_attribute("href")
            if href and not href.startswith(("https:", "http:")):
                response = page.request.get(urljoin(url, href))
                assert response.status == 200, href
        source = page.get_by_role("link", name="Download gallery source").get_attribute("href")
        assert page.request.get(urljoin(url, source)).body().startswith(b"PK")
        assert not errors, errors
        assert not failures, failures
        browser.close()
    print("PASS: crane assets, stages, three independent manual inputs, slider, pixel pose return, playback, scrub/loop, local links/source and desktop/narrow layout; no console/network failures.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url")
    args = parser.parse_args()
    if args.url:
        check(args.url)
        return
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        check(f"http://127.0.0.1:{server.server_port}/models/swivel_crane/")
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


if __name__ == "__main__":
    main()
