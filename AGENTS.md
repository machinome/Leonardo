# Building Astra's Leonardo gallery

Read README.md, docs/brief.md, QUEUE.md and gallery.toml before working.
This is an independent project repository. Confirm `git rev-parse
--show-toplevel` is this directory before editing and before each commit.
Work here directly; shop worktrees, shop sprints and framework cycles do
not own this gallery. Never create a nested Git repo or pyproject.toml.

## The one-prompt session

“See the Leonardo project, build next work on the queue” means **finish
the next item**, not just propose it. Run `python scripts/gallery.py next`.
`gallery.toml` is the only authority for queue order and status; QUEUE.md
contains the commissioned briefs and acceptance gates. Resume the first
unfinished item, including an `in_progress` item left by a previous session.
Do not skip it or start a later one because implementation is difficult.

The pilot has delegated ordinary design, dimensions, presentation, OpenSpec
planning, implementation, verification and local commits within these
briefs. Record sensible choices and continue through the whole cycle in
the same session; no separate approval prompt is needed for those choices.
Changing the gallery's purpose or a brief's central mechanism still needs
the pilot. Never push, create a remote repo/PR, publish, or contact anyone.

1. Inspect existing state, history and the current item's evidence. Preserve
   unrelated edits. Confirm nobody else is working on the same item; do not
   dispatch floor agents or create a parallel editing session.
2. Set that item's status to `in_progress`. Create its machine directory
   and `openspec/config.yaml` **before** invoking OpenSpec. Run commands
   there and verify `openspec status --change <name> --json` resolves to
   that machine, never the enclosing shop or gallery root. The site uses
   root `openspec/`. Use local CLI help for installed syntax.
3. Research the cited historical source, and write proposal, design, delta
   specs and tasks. Record the queue item as the authority, the exact
   continuation prompt, reconstruction choices and historical limits.
   Commit planning before implementation. Do not invent historical
   dimensions, original prompt transcripts, or earlier ratification.
4. Build the complete model and companion geometric tests. Prove the
   relevant failure red first, then implement, inspect and iterate. Commit
   only after the acceptance gates below. Ordinary project fixes needed
   to finish the brief are authorized.
5. Update that machine's README and evidence, sync its specs, archive its
   completed change, add its name to the root registry and gallery metadata,
   and set status to `done` in the implementation commit. Record the
   commands, results, dependency content revisions and limits in durable
   evidence, including a reference to the source commit tested. Do not put
   a self-referential commit hash in its own commit.
6. Report the completed item, validation and next item, then stop. A new
   session handles the next item. If interrupted, leave `in_progress` and
   a precise resume note in the machine's docs; never label incomplete,
   timed-out or failing work `done`. When all items are done, verify the
   completed record and report ready for the pilot to publish; do not
   invent more queue work.

## Design and mechanical craft

This is original CAD authored by Astra for a public solid-node demo. No
upstream CAD imports or traced museum assets are needed. Link historical
sources and distinguish Leonardo's drawings, later museum reconstructions
and our educational choices. Do not imply Leonardo invented mechanisms
he studied or recorded, particularly Brunelleschi's crane.

In the LibreSolid Studio workspace, read the complete shared
`shop-skills/solid-node-api/SKILL.md` and `shop-skills/solid-node/SKILL.md`
before modeling. Resolve the enclosing shop within this workspace; never
search sibling workspaces or inspect framework internals for an API.
Outside this workspace, use the supported public solid-node documentation
matching the installed version. Missing capabilities are findings to
report, not permission to patch dependencies. Use Context7 for current
third-party library documentation, and primary historical sources.

Use `models/<snake_case>/model.py`, `test_model.py`, `__init__.py`,
optional `parts.py`/`kinematics.py`, README.md, docs/ and openspec/.
Follow the root registry pattern. Build identity stays geometric; a driver
changes the machine's state. Use declarative parameters, joints and
relations, and symbolic degree math that exports to the actual viewer.
Keep complete rigid components, realistic running gaps, a visible frame
and a readable power path. Do not implement a second JS machine or viewer.

Keep the public API small: typically phase plus run, meaningful named
instructions, and at most one or two useful build parameters. For an
independently controlled crane, three physical coordinates are appropriate.
All advertised controls and their combinations must stay inside the tested
demonstration envelope. Driver ranges are metadata, not safety clamps;
choose laws/ranges accordingly. Explain any end-of-loop reset visibly.

## Completion gates for every machine

- Whole-root connectedness and non-interference remain active. Sweep a
  full cycle, endpoints and transition neighborhoods; sample gear contacts
  over one tooth pitch too. Never suppress errors with epsilon, remove
  colliding parts, or narrow the root check to obtain green.
- Measure the advertised motion on actual geometry using independent
  expectations. For transmitting pairs, prove free play and blockage
  beyond it. Check frame support/capture where claimed; explicitly name
  grounded fixtures and omissions. Flexible rope/yarn needs its own
  routing, length/clearance and attachment checks beyond rigid tests.
- Run a deliberate code mutation that violates the central mechanism,
  observe the intended test fail, revert the mutation and verify green.
  Report blind spots honestly. Test default and advertised boundary
  parameter values. Finish with exact-kernel evidence for every root;
  faceted checks are the faster development loop.
- Run `python scripts/gallery.py check`, and build/test every registered
  model after shared changes. An untouched imported module needs regression,
  not a fabricated new red-first history. Existing tests and evidence are
  preserved unless new evidence justifies a documented revision.
- Render and **inspect** at least an isometric snapshot and a view of the
  important alignment at different phases. Use `solid snapshot` with the
  default OpenSCAD renderer. Save a small, intentionally selected set of
  evidence images in `docs/evidence/` for public inspection; keep raw
  batches/builds ignored. Screenshots alone do not prove engagement.
- Export the real model with `solid export`; verify manifest assets,
  drivers, instructions, playback, manual controls and a return to a prior
  pose in a real browser. Check desktop and a narrow viewport, console and
  asset failures. Retain a reproducible finite browser smoke script, register
  its command in gallery.toml as `browser_check` (optional `{base_url}`
  placeholder), and run `python scripts/check_browsers.py` for all exhibits.
- Leave readable sources, a machine README (why it matters, controls,
  sources, assumptions, build/test commands), its own archived OpenSpec,
  complete evidence and no unfinished public UI. Add only working models
  to the registry. Every original new source file carries the copyright
  and AGPL notice. Never include generated exports in Git.

The pilot will not fix this work. If evidence exposes a defect, fix it in
the project while staying within the brief. Do not weaken a central promise,
silently omit a failed item, or certify an unmeasured capability. If an
external blocker truly prevents completion, record it and leave the queue
unfinished rather than making a broken publication look ready.

## Final site

The site is the last item and depends on every machine. Follow its full
brief in QUEUE.md. Sphinx creates a static directory; `solid export`
supplies every interactive exhibit. The visible site must identify itself
as a **solid-node demonstration**, link to solid-node, credit **Astra's
single-prompt designs**, and link to the **Leonardo gallery on GitHub**.
Copyright remains Luis Henrique Cassis Fagundes, AGPL-3.0-only. Use
gallery.toml for those URLs and credits. The pilot publishes; stop with a
verified static artifact and exact build/hosting instructions.
