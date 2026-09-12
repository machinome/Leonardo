"""Finite browser check against an ephemeral localhost server; no shop session."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json

from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=ROOT))
    Thread(target=server.serve_forever, daemon=True).start()
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1600, "height": 1000})
            page.on("pageerror", lambda error: errors.append(str(error)))
            response = page.goto(f"http://127.0.0.1:{server.server_port}/demo.html", wait_until="networkidle")
            assert response.status == 200
            frame = page.frames[1]
            frame.get_by_text("Handoff", exact=True).click()
            expect(frame.get_by_label("phase exact value (deg)", exact=True)).to_have_value("90.0000")
            expect(frame.get_by_label("run exact value (play)", exact=True)).to_have_value("0.0000")
            frame.get_by_text("Return pick", exact=True).click()
            expect(frame.get_by_label("phase exact value (deg)", exact=True)).to_have_value("270.0000")
            frame.get_by_text("Run", exact=True).click()
            expect(frame.get_by_label("run exact value (play)", exact=True)).to_have_value("1.0000")
            # The exported animation runs without a custom viewer API.
            timeline = frame.locator('input[type="range"]').first
            first_tick = timeline.input_value()
            expect(timeline).not_to_have_value(first_tick)
            print(json.dumps({"body": frame.locator("body").inner_text(),
                              "buttons": frame.locator("button").all_text_contents(),
                              "inputs": frame.locator("input").evaluate_all(
                                  "els => els.map(e => ({type:e.type, value:e.value, title:e.title, aria:e.getAttribute('aria-label')}))"),
                              "errors": errors}, indent=2))
            page.screenshot(path=str(ROOT / "_evidence" / "browser-demo.png"))
            assert not errors, errors
            browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
