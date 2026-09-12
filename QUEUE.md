# Astra's Leonardo build queue

Commission: [docs/brief.md](docs/brief.md). Order and status:
[gallery.toml](gallery.toml), read with `python scripts/gallery.py next`.
One session completes one item. The two imported exhibits are the starting
collection, not unfinished queue items. All future work is in this one repo.

The intended finished collection is six exhibits: sawmill, loom, cam
hammer, rack lift, compound pulley and swivel crane, followed by the site.
The sequence builds from one-input contact to flexible reeving and finally
three independent movements. Each brief below is a complete commission,
not a suggestion requiring another prompt.

## Admission judgment

These four candidates have a documented historical basis, compact original
geometry, bounded motion expressible by the current public API, and
independent geometric checks for their central teaching point. Viability
is Astra's engineering judgment, not a claim that unbuilt models have
passed. The scope is deliberately an educational reconstruction, at a
readable desktop scale, with dimensions chosen and documented by the agent.

No flying machine, self-propelled spring cart, perpetual-motion device,
fluid pump performance simulation, weapon, or sprawling production machine
is queued. Flight, stored-energy dynamics, cloth formation and cutting
physics are unnecessary to demonstrate this framework. The final site
may discuss limits, but cannot substitute a static poster for a promised
working mechanism or hide failed exhibits to consume the queue.

## 010-cam-hammer

**Build:** a complete hand-cranked cam hammer on a timber frame: crank and
cam, pivoted lever, hammer, anvil and supporting journals. One visible cycle
lifts the hammer, releases it and returns it to the anvil. Make the contact
region readable from a side view and show the lift/drop stages as buttons.
Model `cam_hammer`; OpenSpec lives at `models/cam_hammer/openspec/`.

**Evidence:** [Museum of Science, Gadget Anatomy](https://www.mos.org/leonardo/activities/gadget-anatomy.html)
describes the cam acting on the lever of a gravity trip hammer;
[the Venice Leonardo exhibition](https://www.leonardoavenezia.com/en/)
also identifies this rotary-to-intermittent mechanism. Accessed
12 September 2026. These establish the mechanism, not our dimensions or a
specific folio: do not invent a folio number from conflicting reconstructions.

**Why viable:** a small planar mechanism, one rotary input and one lever
angle. CadQuery can express a smooth rising cam and its release sector;
the follower law must be derived from that same designed contact envelope,
with an independent mesh test. A bounded, explicitly prescribed return
represents the drop; no impact or gravity solver is required.

**Acceptance specific to this item:** the cam genuinely reaches the lever
during lift, the pivot stays seated, the hammer clears its frame and lands
at the anvil's face without penetration. Measure lift at intermediate
phases, not only dead centers; sample immediately around release. Explain
that return timing and impact are illustrative. A phase/geometry mutation
must break the contact test. Deliver phase/run, Lift, Release, Strike, Run.

## 020-rack-and-pinion

**Build:** Leonardo's rack-and-pinion lifting study as an open timber
stand, hand crank, pinion, vertically guided toothed rack and visible hook
carrying a small demonstrator weight. Model `rack_and_pinion`; own OpenSpec.

**Evidence:** [Museo Leonardiano's rack-and-pinion record](https://museoleonardiano.it/en/opera/page/5/)
identifies Codex Atlanticus f.998r and the crank-driven vertical rack with
a hook. Accessed 12 September 2026. Use the object's own page if available
when building, preserving this catalogue reference if its URL changes.

**Why viable:** one revolute and one prismatic coordinate, a finite rack,
and a linear pitch-circle travel law. Original standard conjugate teeth
are an explicitly modern educational choice; no imported gear package is
necessary. Choose conservative tooth counts, module and positive backlash.

**Acceptance:** measure travel from crank rotation; prove both tooth
engagement and freedom within backlash at several tooth phases. Prove the
rack stays captured and clears the stand and travel stops over its whole
range. The hook and load must connect. The animation raises then lowers
within that range, with no tooth jumping or invisible reset. Label the
holding brake/torque and lifting capacity as outside the demonstration.
Deliver phase/run and Bottom, Mid-lift, Top, Run, with one useful size knob.

## 030-pulley-block

**Build:** a compact three-part tackle study with two fixed sheaves, one
moving sheave/block, a continuous rope with its dead end attached to the
moving block, a hanging demonstrator
load and a visible effort end. Model `pulley_block`; own OpenSpec. Choose
the reeving with **three supporting rope segments** so a measured 3:1
displacement relationship is legible: moving-block dead end → first fixed
sheave → moving sheave → second fixed sheave → effort end. Lay out tangent spans and wrap arcs
in separate axial lanes; the model's geometry must agree with its diagram.

**Evidence:** [Museo Leonardiano, Tirare composto](https://museoleonardiano.it/opera/tirare-composto/)
and [Museo Galileo, block of 33 pulleys](https://brunelleschi.imss.fi.it/genscheda.asp?appl=LIR&chiave=100851&indice=63&lingua=ENG&xsl=paginamanoscritto)
identify Madrid I f.36v. Our three-part tackle is a deliberately reduced
teaching model of the principle, **not a replica of the 33-pulley drawing**.
The Galileo record specifically notes that the historical calculation
omits friction. Accessed 12 September 2026.

**Why viable:** one linear input and a fixed-length, planar rope route
with simple circular wraps. Molejo already supplies the flexible shape
surface used by the existing gallery; the route can be expressed without
contact dynamics or an accumulating winding drum.

**Acceptance:** independently measure effort travel and load rise at 3:1,
total rope length through the full range (including arcs and the dead end),
sheave capture and real rope attachment. Prove no rope passes through a
sheave hub/frame or crosses itself. Show changing lengths with labels,
clear Low/Mid/High/Run controls and a bounded raise/lower loop. The frame
is the named support fixture; tension/efficiency and load rating are not
solved. A wrong segment or travel sign must fail the length/geometry test.

## 040-swivel-crane

**Build:** a complete, compact construction crane with fixed footing,
rotating mast, horizontal jib, screw-positioned trolley, visible hoist
sheaves/rope and a suspended stone. Model `swivel_crane`; own OpenSpec.
Let the visitor independently slew, traverse and hoist. Provide a short
Pick up → Lift clear → Swing → Place demonstration within a bounded work
envelope, and an informative view down the mast and along the screw.

**Evidence:** [Museo Leonardiano, swivel crane](https://museoleonardiano.it/en/opera/swivel-crane/)
identifies Codex Atlanticus f.105v and credits machinery probably designed
by Brunelleschi and recorded by Leonardo. Preserve that distinction. The
record describes the rotating mast, lifting pulleys and transverse screw.
Accessed 12 September 2026.

**Why viable:** three independently positioned coordinates with explicit
frame composition; each has simple bounded geometry. Use an original
short lead screw and mating trolley with a stated pitch, and a hoist
route derived from the preceding tackle's validated method if useful.
This is a kinematic construction study, not a simulated worksite.

**Acceptance:** geometry measures slew about the mast's actual axis,
trolley travel per screw turn, and hook displacement from rope take-up.
Show continuous rope/sheave/drum routing and label any prescribed winding
interpretation. Check corners and intermediate combinations of all three
controls, plus the entire named trajectory; the suspended stone and rope
must clear the frame everywhere advertised. Explicitly ground the crane's
footing; do not imply certified stability or load capacity. No workers,
landscape, extra cranes or exact historical reconstruction is required.
Two inputs must not overwrite each other's poses; replay is repeatable.

## 050-public-site

**Build the actual public gallery last.** All four machine items must be
done, and all six registered exhibits must pass the mechanical and browser
gates in AGENTS.md. Site-wide OpenSpec belongs at root `openspec/`.

Produce an attractive static **Sphinx** site with a gallery index, one page
per exhibit and an about/source page. Give each exhibit an inspected preview,
a clear explanation of its mechanism, usable controls, historical citations
and concise reconstruction limits. Use a consistent warm timber/iron visual
language, legible typography, generous model space and restrained motion.
Let visitors open a full-size model; do not load six WebGL contexts on the
index page. Use local assets, keyboard access, useful iframe titles, narrow
screen layouts and reduced-motion behavior. Inspect the rendered result.

The landing page and persistent site navigation/footer must visibly say
that this is a **demonstration of solid-node**, link to
`gallery.solid_node_url`, credit **Astra: single-prompt mechanical designs**,
and link to the **Leonardo gallery on GitHub** at `gallery.source_url`.
Read the values from gallery.toml; do not hardcode divergent destinations.
Reconcile the intended `https://github.com/LibreSolid/Leonardo` with a
configured publishing remote if one now exists. Publication by the pilot
is pending, not an error to conceal or authority to create a remote.

### Build contract

One documented finite command from a fresh clone/environment must:

1. Validate queue and model inventory, then run `solid export <model>` for
   **every registered model**, with per-model build and export directories.
   Keep instructions, drivers and animation in the real viewer. No manually
   animated alternate geometry, screenshots posing as 3D, remote renderer,
   shop service or Python backend may be needed by visitors.
2. Copy the exports and local viewer assets into the Sphinx output, retaining
   each manifest's relative paths. `html_extra_path` is an appropriate
   route; see [Sphinx configuration](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_extra_path).
   Keep generated manifests out of Git and keep Sphinx from parsing exhibit
   assets as documents. Use `sphinx-build -b html -W --keep-going` or the
   current equivalent that makes warnings fail the build.
3. Include copyright, the unchanged AGPL text, corresponding gallery source
   from the tested commit, dependency notices and source availability for
   bundled assets. Inspect the viewer distribution's actual notices when
   packaging it; gallery licensing does not overwrite dependency licenses.
4. Produce a standalone output directory (`_site/` by convention), a build
   inventory naming every model, and exact local-preview/hosting commands.
   Hosting must work at both `/` and a prefix such as `/Leonardo/` on a
   basic static HTTP server. Use relative asset and exhibit links.

### Final verification and reproducibility

Build from committed sources and a clean staging directory. Resolve and
record an actually obtainable dependency set: the current models need
post-release solid-node and a local viewer. Use compatible published
versions if then available, otherwise include redistributable dependency
source snapshots with their own licenses and deterministic build commands.
Do not pin an unreachable development commit on a public URL or claim
that `pip install solid-node==0.6.0` reproduces these models. Do not push or
publish dependencies as a side effect. Test the documented setup in a
throwaway environment before saying the public source reproduces the site.

Run all roots' exact tests. In a browser, serve only the generated static
directory, once at root and once under `/Leonardo/`. Open every exhibit,
change a control and trigger an instruction, observe actual geometry change,
pause/play and revisit a pose. Fail on console errors, missing model assets,
broken internal links, empty previews or narrow-screen overflow. Verify
the solid-node credit/link and GitHub gallery link appear in generated HTML
and are usable. Required runtime assets must work with external network
requests blocked; historical links may of course leave the site.

Retain a finite reproducible browser check, reviewed desktop/mobile images,
build/test results and source revision evidence. Write publication
instructions usable without fixes. Mark this final item `done` only when
the static artifact and these checks are complete. Leave the pilot the
output location and publish instructions; do not deploy it yourself.
