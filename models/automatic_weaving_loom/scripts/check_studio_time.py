"""Check the declared Python clock in an already-open Studio loom session.

This only inspects the existing session and changes controls in its own browser.
It does not open a project, dispatch agents or send any project messages.
"""

# Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.
import argparse
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

from inspect_demo import cad_pixels

OUTPUT = (
    Path(__file__).resolve().parents[3] / "_evidence/automatic_weaving_loom/browser"
)


def check(base):
    with sync_playwright() as p:
        api = p.request.new_context(base_url=base)
        entries = api.get("/api/entries?folder=Leonardo")
        assert entries.ok, "Studio's project catalogue is unavailable"
        project = next(
            item
            for item in entries.json()["entries"]
            if item["name"] == "automatic_weaving_loom"
        )
        assert (
            project["state"] == "open"
        ), "Open the loom in Studio before running this check"
        document = api.get(
            f"/api/sessions/{project['session_id']}/artifacts/viewer.json"
        )
        assert document.ok
        assert document.json()["animation"]["loop"] == 60
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--enable-webgl",
                "--use-gl=angle",
                "--use-angle=swiftshader",
                "--enable-unsafe-swiftshader",
            ],
        )
        page = browser.new_page(viewport={"width": 1500, "height": 1100})
        page.goto(
            base + "/projects/Leonardo/automatic_weaving_loom",
            wait_until="domcontentloaded",
        )
        speed = page.get_by_label("Playback speed", exact=True)
        expect(speed).to_be_attached(timeout=60000)
        page.get_by_role("button", name="Timeline", exact=True).click()
        expect(speed).to_be_visible()
        expect(speed).to_have_value("1")
        for value in ("0.1", "0.25", "0.5"):
            speed.select_option(value)
            expect(speed).to_have_value(value)
        page.get_by_title("Pause", exact=True).click()
        timeline = page.locator('.animation-controls input[type="range"]')
        timeline.fill(timeline.get_attribute("max"))
        timeline.dispatch_event("input")
        expect(page.locator(".machine-time")).to_have_text("1:00.0")
        canvas = page.get_by_role("img", name="Functional model", exact=True)
        final = cad_pixels(canvas)
        timeline.fill("0")
        timeline.dispatch_event("input")
        expect(page.locator(".machine-time")).to_have_text("0:00.0")
        assert final != cad_pixels(canvas), "Reset did not change the actual CAD"
        page.get_by_title("Play", exact=True).click()
        expect(timeline).not_to_have_value("0", timeout=10000)
        page.get_by_title("Pause", exact=True).click()
        OUTPUT.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(OUTPUT / "studio-time-controls.png"), timeout=60000)
        browser.close()
        api.dispose()
    print(
        "PASS: live Studio publishes loop=60; native ×0.1/×0.25/×0.5 controls, 1:00.0 endpoint, changed CAD and slow playback"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:9000")
    check(parser.parse_args().base_url.rstrip("/"))
