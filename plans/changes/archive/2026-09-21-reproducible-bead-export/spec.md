---
title: "Spec — reproducible bead export"
category: spec
created: 2026-09-21
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-21"
review:
  status: pending
  approved_by: null
  approved_at: null
status: accepted
implementation_status: done
date: 2026-09-21
last_reviewed: 2026-09-21
bead: coding-harness-1jg.1
---

# Spec — reproducible bead export

Class: Bounded.

## Problem

Two machines render different bytes from the same tracker state, because the
export carries machine-local lease fields (`research.md`, "What was
measured"). The identity gate therefore cannot hold anywhere but on the
machine that rendered last, and a second writer or a hosted run would report
DRIFT for identical content.

## Acceptance criteria

1. The rendered export contains no machine-local lease field
   (`heartbeat_at`, `lease_expires_at`) on any issue. *Refuted by:* a render of
   a tracker with a claimed issue that still shows either key.
2. Every other key and value of `tools/bd export` reaches the file unchanged,
   in the same line order. *Refuted by:* any differing key, value or order
   between the raw export and the render, apart from the omitted keys.
3. `--check` compares like with like: the fresh render it compares is produced
   by the same omission. *Refuted by:* `--check` reporting DRIFT directly after
   a render on the same machine with a claimed issue present.
4. The set of omitted keys is stated once, in the renderer, with the reason.
   *Refuted by:* a second list in a test or a gate.
5. A render that would be empty or invalid still never reaches the committed
   file. *Refuted by:* the existing line check no longer running on the
   render.

## Non-goals

- Where the gate runs and whether it is a floor gate (stage 2).
- Removing the committed file or installing bd in hosted CI (stage 3).
- Changing what `tools/bd export` emits, or any tracker configuration.
- Repairing `scripts/new_change.py` (finding recorded in `research.md`).

## Open decisions

None for the human. `[DETAIL]`, decided here: the keys are removed rather than
set to `null`, because an absent key is what a fresh clone renders for an
unclaimed issue and removal makes both machines agree; the output is
re-serialised with the separators and key order of the input line so that
criterion 2 holds byte for byte where nothing is omitted.
