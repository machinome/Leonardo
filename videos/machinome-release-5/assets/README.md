# Studio background

`studio-background.png` photographs a native Mozilla Firefox window showing
`http://localhost:9000/` and Machinome Studio's real UI with the existing
Leonardo hydraulic sawmill export. `studio-capture.json` records its SHA-256,
window-relative CSS rectangles and browser-only staged conversation. Reproduce
with `../capture-studio.mjs`; it neither opens a real session nor submits a
message. The fictional checklist is a video prop, not agent-work evidence.

The model was loaded and then hidden, retaining the real assembly navigator.
The film draws its own moving View over the empty model area. The chat has
3000px of leading padding, not thousands of fabricated words.

Capture: Firefox 153.0 from Playwright, on an isolated 3840×2160 Xvfb
display at 3 pixels per CSS pixel. Native browser controls occupy the first
84⅓ CSS pixels; the live model, menu highlights and typed prompt include that
offset. `resize-capture-window.py` sizes only this private display's Firefox
window. FFmpeg captures the native window, without drawing imitation controls
or modifying the resulting pixels. The root URL is set by a tab-local history
replacement after the staged project loads, not by changing Studio's routing.
The native address bar is unfocused in the final capture. Mozilla/Firefox
names and browser artwork are used referentially, not as an endorsement.

Studio UI: Copyright (C) 2023–2026 Luis Henrique Cassis Fagundes,
AGPL-3.0-or-later, https://github.com/machinome/machinome-studio/.
Screenshot capture and original video code: Copyright (C) 2026 Luis Henrique
Cassis Fagundes, AGPL-3.0-only, as the gallery records. Brand artwork and
trademarks retain their separate terms; no trademark permission is implied.
