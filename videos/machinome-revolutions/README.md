# Revolutions — Machinome release film

Copyright (C) 2026 Luis Henrique Cassis Fagundes. AGPL-3.0-only.

Commissioned on 27 September 2026 as Machinome's release video, using the
Leonardo hydraulic sawmill reconstructed under the pilot's direction.
The brief connects the revolution of a wheel, historical changes in work,
and present AI-assisted making. The narrator speaks as a machine looking
at an ancestor in the history of human tools. Human intention and judgment
remain the subject. The pilot supplied the name's origin: machine + genome.

The pilot explicitly corrected the first production approach: the former
mechanism rehearsal is not a creative reference for this release film.
This film starts with human purpose, connects two generations of tools,
uses the mechanism as evidence, and devotes its second half to source code,
human correction and the present change in how people make things.

The film makes Machinome concrete:
parts, connections and motion expressed in source that people can inspect,
change and test. Historical language does not claim Leonardo invented the
water-powered saw, or date the Industrial Revolution to his lifetime.
The first-person narrator considers its place in a human history of making:
a present-day tool looking at an ancestor in that tradition.

Production choices: English; 2 minutes 57 seconds; 1920×1080 landscape; 30 fps;
George synthetic voice; restrained warm background; original restrained
electronic sound design; a new episode that
preserves the earlier hydraulic-sawmill rehearsal as history. The existing
Videomaker format is sufficient: this commission changes video content,
not simulation behavior, tool behavior or project architecture.

Read [episode.yaml](episode.yaml) for narration beside each shot, and
[production.yaml](production.yaml) for cameras, layers, voice and evidence.
[description.md](description.md) carries attribution and upload copy.
[research.md](research.md) records checked sources and editorial limits.
Build output is ignored under `_build/`.

The existing model export is pinned to
`a01fb865426de9967f690b4a7a1230684eb1e523`. Its 1460-second course includes
the corrected two-rope drive and fitted timber frame. The old 84-second
rehearsal predates both: its feed-on-return explanation and 296-second
duration must not be reused. The present model feeds on the downstroke,
then dwells while the blade and driving hook recover.

The film uses a continuous excerpt from the middle of the actual course;
it does not reset the model, invent water physics, or add simulated sawdust.
Hidden structural layers are explanatory reveals. Neither CAD nor the
viewer is changed during production. AI involvement is part of the pilot's
explicitly commissioned subject, not an appended product or author credit.

From `/home/asa/devel/machinome/videomaker`:

```sh
node bin/videomaker.mjs check ../projects/Leonardo/videos/machinome-revolutions/episode.yaml
node bin/videomaker.mjs speech ../projects/Leonardo/videos/machinome-revolutions/episode.yaml
node bin/videomaker.mjs preview ../projects/Leonardo/videos/machinome-revolutions/episode.yaml --viewer ../machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node bin/videomaker.mjs render ../projects/Leonardo/videos/machinome-revolutions/episode.yaml --viewer ../machinome-viewer/machinome_viewer/widget/dist/machinome-viewer.js
node ../projects/Leonardo/videos/machinome-revolutions/finish.mjs
```

`speech` can make paid requests for uncached narration; `render` uses cached
speech only. Never put the provider key in this repository. Publication is
the pilot's decision. Public source and simulation addresses remain
placeholders until verified; film completion does not publish anything.

The final file is `_build/machinome-revolutions.mp4`. `finish.mjs` composes
an original deterministic electronic score, ducks it beneath narration,
masters the mix to -16 LUFS / -1.5 dBTP, and preserves the captured H.264
picture without another lossy encode. The score is illustrative sound design,
not recorded water or machinery. `_build/rehearsal.mp4` retains the
narration-only rendition. `release-manifest.json` records final media checks
and hashes; `rehearsal-manifest.json` records the actual model and capture.

Speech is measured at voice speed 0.88; the edit includes deliberate short
pauses. The pawl recovery starts 5.366 seconds into its shot; the downstroke
and upstroke explanation starts 5.448 and 8.571 seconds into the rope shot;
the model stops 6.899 seconds into the genome shot on “Pause it.” These
points use cached character alignment, not estimated reading speed.
