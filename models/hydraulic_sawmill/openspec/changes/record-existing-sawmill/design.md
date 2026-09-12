## Context

The sawmill was built before this record, at original commit 9f4cc67.
Its existing docs/design.md and docs/validation.md state the chosen
dimensions, original tests and limitations. The current commission
consolidates the gallery and asks for the missing OpenSpec.

## Goals / Non-Goals

Goals: retain a machine-owned behavioral baseline, preserve provenance,
and verify the unchanged mechanism after moving its import paths.

Non-goals: invent prior planning, redesign the sawmill, complete the
historical feed linkage, or add cutting/fluid/contact dynamics.

## Decisions

- Record two capabilities: the machine's cycle and its inspectable exhibit.
  This separates what a visitor observes from the evidence/presentation
  promise while keeping both owned by the same machine.
- Preserve the existing exact CadQuery parts and declarative motion laws.
  A rebuild of geometry would introduce unnecessary mechanical change.
- Adopt the gallery's root registry and export directory. Retain the
  existing exhibit shell and adapt its asset URLs to that shared layout.
- Promote the written retrospective requirements to baseline as part of
  this record; archive with spec sync skipped after verification because
  those identical requirements are already in the baseline.

## Risks / Trade-offs

- Historical evidence could be mistaken for a fresh run → keep the original
  record intact and add consolidation results separately.
- A shifted Python path could break discovery → test both named roots.
- A shifted asset URL could yield a blank exhibit → inspect real browser
  playback and controls after exporting from the consolidated root.
- The phase-driven feed is not a complete historical transmission → keep
  that limitation explicit in both source documentation and the exhibit.

## Migration Plan

No mechanical migration. The original content is recoverable from
history/hydraulic-sawmill. Reversal of the gallery layout would be a new
documented change, not deletion of its preserved history.

## Open Questions

None for the retrospective baseline. The public dependency installation
and common Sphinx presentation belong to the gallery's final queue item.

