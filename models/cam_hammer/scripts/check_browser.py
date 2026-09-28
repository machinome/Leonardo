#!/usr/bin/env python3
"""Finite smoke of the actual exported viewer; optionally use gallery
server."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import json
from pathlib import Path
from threading import Thread

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "_evidence/cam_hammer"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def pixels(png):
    return Image.open(BytesIO(png)).convert("RGB")


def scene_pixels(page, canvas):
    """Capture the CAD viewport between its control overlays.

    Moving sliders or changing readout text must not satisfy a motion
    test.
    The original screenshot is framed at capture time, never edited.
    """
    canvas.scroll_into_view_if_needed()
    bounds = canvas.bounding_box()
    return pixels(
        page.screenshot(
            clip={
                "x": bounds["x"],
                "y": bounds["y"] + 170,
                "width": bounds["width"],
                "height": bounds["height"] - 205,
            }
        )
    )


def check(url):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(
        (ROOT / "export/cam_hammer/manifest.json").read_text()
    )
    assert set(manifest["drivers"]) == {"phase", "run"}
    assert set(manifest["instructions"]) == {
        "Lift",
        "Release",
        "Strike",
        "Run",
    }

    def walk(node):
        if "model" in node:
            assert (
                ROOT / "export/cam_hammer" / node["model"]
            ).is_file(), node["model"]
        for child in node.get("children", []):
            walk(child)

    walk(manifest["root"])
    errors, failures = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1440, "height": 1100}, device_scale_factor=1
        )
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on(
            "console",
            lambda msg: (
                errors.append(msg.text) if msg.type == "error" else None
            ),
        )
        page.on(
            "response",
            lambda r: (
                failures.append(f"{r.status} {r.url}")
                if r.status >= 400
                else None
            ),
        )
        page.on(
            "requestfailed", lambda r: failures.append(f"{r.url}: {r.failure}")
        )
        for width, height, label in (
            (1440, 1100, "desktop"),
            (390, 844, "narrow"),
        ):
            page.set_viewport_size({"width": width, "height": height})
            page.goto(url, wait_until="networkidle")
            frame = page.frame_locator("iframe")
            canvas = frame.locator("canvas")
            expect(canvas).to_be_visible()
            phase = frame.get_by_label("phase exact value (deg)", exact=True)
            run = frame.get_by_label("run exact value (play)", exact=True)
            # Native instructions are real viewer controls, including
            # the ramp.
            frame.get_by_role("button", name="Run Lift", exact=True).click()
            expect(phase).to_have_value("120.0000")
            expect(run).to_have_value("0.0000")
            # The controls overlay the canvas. Hold the timeline too so
            # a changed scrubber thumb cannot masquerade as changed CAD.
            frame.get_by_title("Pause", exact=True).click()
            timeline = frame.locator('input[type="range"]').first
            timeline.fill("0")
            timeline.dispatch_event("input")
            page.wait_for_timeout(150)
            canvas.screenshot(path=str(OUTPUT / f"{label}-lift.png"))
            lifted = scene_pixels(page, canvas)
            for name, target in (
                ("Release", "250.0000"),
                ("Strike", "320.0000"),
            ):
                frame.get_by_role(
                    "button", name=f"Run {name}", exact=True
                ).click()
                expect(phase).to_have_value(target)
                expect(run).to_have_value("0.0000")
            page.wait_for_timeout(150)
            struck = scene_pixels(page, canvas)
            assert ImageChops.difference(
                lifted, struck
            ).getbbox(), "Stage geometry did not move"
            # Manual exact entry returns to the previous rendered
            # geometry.
            frame.get_by_role(
                "button", name="Edit phase exact value (deg)", exact=True
            ).click()
            phase.fill("120")
            phase.press("Enter")
            expect(phase).to_have_value("120.0000")
            page.wait_for_timeout(150)
            canvas.screenshot(path=str(OUTPUT / f"{label}-return.png"))
            returned = scene_pixels(page, canvas)
            difference = ImageChops.difference(lifted, returned)
            assert (
                difference.getbbox() is None
            ), f"Pose return changed geometry: {difference.getbbox()}"
            frame.get_by_label("phase (deg)", exact=True).fill("60")
            frame.get_by_label("phase (deg)", exact=True).dispatch_event(
                "input"
            )
            expect(phase).to_have_value("60.0000")
            frame.get_by_role("button", name="Run Run", exact=True).click()
            expect(run).to_have_value("1.0000")
            expect(phase).to_have_value("0.0000")
            frame.get_by_title("Play", exact=True).click()
            timeline = frame.locator('input[type="range"]').first
            initial_tick = timeline.input_value()
            expect(timeline).not_to_have_value(initial_tick)
            first_play = scene_pixels(page, canvas)
            page.wait_for_timeout(500)
            assert ImageChops.difference(
                first_play, scene_pixels(page, canvas)
            ).getbbox(), "Playback did not animate geometry"
            frame.get_by_title("Pause", exact=True).click()
            timeline.fill("0")
            timeline.dispatch_event("input")
            start = scene_pixels(page, canvas)
            timeline.fill("180")
            timeline.dispatch_event("input")
            page.wait_for_timeout(150)
            assert ImageChops.difference(
                start, scene_pixels(page, canvas)
            ).getbbox(), "Timeline scrubbing did not move geometry"
            assert page.evaluate(
                "document.documentElement.scrollWidth <= innerWidth"
            ), "Exhibit overflow"
            inner = page.frames[1]
            assert inner.evaluate(
                "document.documentElement.scrollWidth <= innerWidth"
            ), "Viewer overflow"
            page.screenshot(
                path=str(OUTPUT / f"browser-{label}.png"), full_page=True
            )
        source = page.get_by_role(
            "link", name="Download gallery source"
        ).get_attribute("href")
        from urllib.parse import urljoin

        response = page.request.get(urljoin(url, source))
        assert response.status == 200 and response.body().startswith(b"PK")
        assert not errors, errors
        assert not failures, failures
        browser.close()
    print(
        "PASS: cam hammer assets, named stages, manual input/slider, "
        "pixel pose return, playback/scrub, source ZIP, desktop/narrow; "
        "no console or network failures."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url")
    args = parser.parse_args()
    if args.url:
        check(args.url)
        return
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT))
    )
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        check(f"http://127.0.0.1:{server.server_port}/models/cam_hammer/")
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


if __name__ == "__main__":
    main()
