"""Finite acceptance of the real loom export at desktop and narrow viewports."""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
from functools import partial
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
from threading import Thread
from zipfile import ZipFile
from base64 import b64decode
import json
from PIL import Image
from playwright.sync_api import sync_playwright, expect

MACHINE = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "_evidence/automatic_weaving_loom/browser"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def cad_pixels(canvas):
    """Read actual WebGL pixels after drawing, without HTML control overlays.

    Nested-iframe element screenshots can stall while scrolling a full-height
    canvas into view. Its bounds were stable in six consecutive browser frames;
    sampling the canvas in a render frame avoids that capture-only failure.
    """
    uri = canvas.evaluate("""canvas => new Promise((done, fail) => {
        const timeout = setTimeout(() => fail(new Error('CAD pixel capture timed out')), 10000);
        requestAnimationFrame(() => {
            try { const image = canvas.toDataURL('image/png'); clearTimeout(timeout); done(image); }
            catch (error) { clearTimeout(timeout); fail(error); }
        });
    })""")
    data = b64decode(uri.split(",", 1)[1])
    picture = Image.open(BytesIO(data)).convert("RGB")
    assert any(
        high - low > 30 for low, high in picture.getextrema()
    ), "CAD canvas is blank"
    return data


def check_duration():
    """A Python-declared loop, not export frame count, enables native speed UI."""
    destination = ROOT / "export/automatic_weaving_loom"
    animation = json.loads((destination / "manifest.json").read_text())["animation"]
    assert animation.get("loop") == 60, "Python's 60-second time base was not published"


def check(url):
    check_duration()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = ROOT / "export/automatic_weaving_loom"
    manifest = json.loads((destination / "manifest.json").read_text())
    assert set(manifest["drivers"]) == {"phase", "run"}
    assert len(manifest["instructions"]) == 6
    names = set()

    def assets(node):
        names.add(node["name"])
        if "model" in node:
            assert (destination / node["model"]).is_file(), node["model"]
        for child in node.get("children", []):
            assets(child)

    assets(manifest["root"])
    assert {
        "timing",
        "six",
        "twelve",
        "winding",
        "rack",
        "rear_upper",
        "rear_lower",
        "front_upper",
        "front_lower",
        "belt",
        "head_drive",
        "selector_a",
        "selector_b",
        "jaw",
        "spring",
        "cords",
        "cloth_web",
    } <= names
    errors, failures = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--enable-webgl",
                "--use-gl=angle",
                "--use-angle=swiftshader",
                "--enable-unsafe-swiftshader",
            ],
        )
        page = browser.new_page(
            viewport={"width": 1500, "height": 1100}, device_scale_factor=1
        )
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on(
            "console", lambda m: errors.append(m.text) if m.type == "error" else None
        )
        page.on(
            "response",
            lambda r: (
                failures.append(f"{r.status} {r.url}") if r.status >= 400 else None
            ),
        )
        page.on("requestfailed", lambda r: failures.append(f"{r.url}: {r.failure}"))
        for width, height, label in ((1500, 1100, "desktop"), (390, 844, "narrow")):
            page.set_viewport_size({"width": width, "height": height})
            response = page.goto(url, wait_until="networkidle")
            assert response.status == 200
            frame = page.frame_locator("iframe")
            canvas = frame.locator("canvas")
            expect(canvas).to_be_visible(timeout=60000)
            # Exercise the native pause control before measuring held poses.
            # Otherwise the viewer keeps tessellating the full flexible loom
            # while a full-page screenshot waits for its compositor.
            frame.get_by_title("Pause", exact=True).click()
            phase = frame.get_by_label("phase exact value (deg)", exact=True)
            run = frame.get_by_label("run exact value (play)", exact=True)

            def stage(name, value):
                print(f"Checking {label}: {name}", flush=True)
                frame.get_by_role("button", name=f"Run {name}", exact=True).click()
                expect(phase).to_have_value(f"{value:.4f}", timeout=25000)
                expect(run).to_have_value("0.0000")
                canvas.evaluate(
                    "() => new Promise(done => requestAnimationFrame(() => requestAnimationFrame(done)))"
                )

            stage("Handoff", 90)
            first = cad_pixels(canvas)
            stage("Beat right", 180)
            assert (
                sha256(first).digest() != sha256(cad_pixels(canvas)).digest()
            ), "CAD did not change pose"
            stage("Return pick", 270)
            stage("Handoff", 90)
            assert first == cad_pixels(
                canvas
            ), "Returning to the same phase changed the CAD pixels"
            for name, value in (("Beat left", 0), ("Open shed", 60)):
                stage(name, value)
            slider = frame.get_by_label("phase (deg)", exact=True)
            slider.fill("45")
            slider.dispatch_event("input")
            expect(phase).to_have_value("45.0000")
            frame.get_by_role(
                "button", name="Edit phase exact value (deg)", exact=True
            ).click()
            phase.fill("90")
            phase.press("Enter")
            expect(phase).to_have_value("90.0000")
            page.screenshot(
                path=str(OUTPUT / f"{label}-handoff.png"), full_page=True, timeout=60000
            )
            frame.get_by_role("button", name="Run Run", exact=True).click()
            expect(run).to_have_value("1.0000")
            timeline = frame.locator('input[type="range"]').first
            timeline.fill("0")
            timeline.dispatch_event("input")
            frame.get_by_title("Play", exact=True).click()
            seconds = timeline.evaluate("""el => new Promise((done, fail) => {
                const timeout = setTimeout(() => fail(new Error('Playback clock stalled')), 15000);
                let first;
                function sample(now) {
                    const value = Number(el.value);
                    if (!first) first = {now, value};
                    if (now - first.now >= 5000 && value > first.value) {
                        clearTimeout(timeout);
                        done((now-first.now)/1000 * (Number(el.max)-Number(el.min))/(value-first.value));
                    } else requestAnimationFrame(sample);
                }
                requestAnimationFrame(sample);
            })""")
            assert (
                57 <= seconds <= 63
            ), f"Browser playback spans {seconds:.2f}s, not 60s"
            print(
                f"PASS: {label}, measured browser playback period {seconds:.2f}s",
                flush=True,
            )
            tick = timeline.input_value()
            expect(timeline).not_to_have_value(tick)
            moving = cad_pixels(canvas)
            expect(timeline).not_to_have_value(timeline.input_value())
            assert moving != cad_pixels(canvas), "Timeline playback did not move CAD"
            frame.get_by_title("Pause", exact=True).click()
            stage("Handoff", 90)
            assert page.evaluate(
                "document.documentElement.scrollWidth<=innerWidth"
            ), "Exhibit overflows horizontally"
            assert canvas.evaluate(
                "() => document.documentElement.scrollWidth<=innerWidth"
            ), "Viewer overflows horizontally"
            print(
                f"PASS: {label}, all stages, exact/slider controls, CAD pose return, playback and layout",
                flush=True,
            )
        source = page.request.get(
            f"{url.rsplit('/models/',1)[0]}/export/automatic_weaving_loom/source.zip"
        )
        assert source.status == 200
        with ZipFile(BytesIO(source.body())) as archive:
            for file in (
                "head.py",
                "timing.py",
                "winding.py",
                "cords.py",
                "textile.py",
            ):
                assert (
                    f"Leonardo/models/automatic_weaving_loom/{file}"
                    in archive.namelist()
                ), "Source ZIP is stale"
        assert not errors, errors
        assert not failures, failures
        browser.close()
    print(
        "PASS: actual manifest assets, desktop/narrow browser controls and pixels; no console or network errors."
    )


def main():
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=ROOT)
    )
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        check(
            f"http://127.0.0.1:{server.server_port}/models/automatic_weaving_loom/demo.html"
        )
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


if __name__ == "__main__":
    main()
