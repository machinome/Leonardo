# Gallery commission — 12 September 2026

The pilot commissioned a single Leonardo da Vinci gallery, consolidating
the hydraulic sawmill and automatic loom while preserving their Git
histories. Each machine keeps its own OpenSpec; the sawmill receives the
missing record. All original work uses AGPL with the pilot's copyright:
Luis Henrique Cassis Fagundes.

Authorship statement supplied by the pilot: the designs are single-shot
prompts implemented by Astra as a machinome demo. Exact original machine
prompts were not stored in the imported repositories; do not invent them.
Future machines use the written queue brief plus the one continuation
prompt as their recorded commission. Single prompt does not mean one
attempt, no research, or no tests: the agent must iterate to verified work.

The pilot will open one new session per queue item with:

> See the Leonardo project, build next work on the queue.

This authorizes designing, implementing, testing, documenting and locally
committing the next item, including its project-owned OpenSpec cycle.
The pilot explicitly delegates ordinary design choices to Astra and will
not repair a broken gallery. Admit bounded, demonstrable mechanisms and
finish their checks. The final queue item builds the actual static public
site with Sphinx and `machinome export` for every machine. The pilot publishes
after the queue is consumed; no push, deployment or publication is delegated.

The pilot added this requirement during consolidation:

> this is also a demo of machinome, so the site must mention machinome
> and must point to the Leonardo gallery at github

Record the destination centrally in `gallery.toml`. The reversible working
assumption is `https://github.com/LibreSolid/Leonardo`, following the
workspace's LibreSolid organization. Neither original repo had a remote.
The site builder must reconcile this with an existing `origin` if the pilot
has since configured one, and must not claim an uncreated remote is live.
