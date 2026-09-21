---
title: "Research — reproducible bead export"
category: research
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

# Research — reproducible bead export

Phase 1 of the change. Facts only; measured on 2026-09-21 at `3be2f1f`.

## What exists today

- The tracker is the Dolt database under `.beads/`, transported through
  `refs/dolt/data` (`AGENTS.md`, house rule 2). `.beads/issues.jsonl` is a
  rendered export.
- Auto-export is off (`.beads/config.yaml`, `export.auto: false`). One script
  renders the file: `scripts/render_beads_export.py`, function `_render_nach`,
  which calls `tools/bd export -o <tmp>`, validates the result through
  `check_bead_export.run` and then writes `.beads/issues.jsonl` byte for byte.
- The gate `export-identity` (`decisions/gates.yaml`, `enforcement: block`,
  `floor: true`) runs the same script with `--check` and compares SHA-256 of a
  fresh render with the committed file. Where `tools/bd` finds no binary it
  skips visibly (exit 127 from the wrapper, commit `8907b42`).
- Readers of the committed file: `scripts/check_bead_export.py`,
  `scripts/check_dangling_bead_ids.py`, `scripts/plans_registry.py`
  (`_bead_statuses`), `scripts/new_change.py` (`--bead`), and tests in
  `tests/test_ci.py` and `tests/test_gate_machinery.py`.

## What was measured

- A fresh shallow clone plus `tools/bd bootstrap --yes` builds the store from
  `refs/dolt/data` in 4.4 s (1.9 MB) and `tools/bd export` then yields all 29
  issues.
- The render in that clone differs from the committed file in exactly two
  fields of one issue: `heartbeat_at` and `lease_expires_at` of the
  in-progress bead `coding-harness-nkr` are present in the writer's render
  (`2026-09-19T13:36:50Z`, `2026-09-19T13:41:50Z`) and `null`/absent in the
  clone's. All ids, statuses and every other field are equal.
- Consequence observed: `python3 scripts/render_beads_export.py --check`
  reports DRIFT in the clone although the tracker content is identical.

## What is unclear

- Whether bd 1.3.0 keeps further machine-local fields that only appear in
  other situations (for example an agent lease on a bead claimed by an agent
  rather than a person). Not found in the 29 issues; "not found" is not "not
  there".
- The upstream document `docs/SYNC_CONCEPTS.md` of beads was not reachable
  (HTTP 404 on 2026-09-21) and was not read.

## Which files a change would touch

- `scripts/render_beads_export.py` — the one place that turns `bd export`
  output into the committed file.
- `tests/test_gate_machinery.py` — holds the renderer's tests.
- `.beads/issues.jsonl` — re-rendered once.

## Finding outside this change

`scripts/new_change.py` refuses to scaffold a change in this repository: it
requires `scripts/check_worktree_state.sh` (constant `WAECHTER`), which did
not travel from the origin repository. This package was created by hand with
the frontmatter `scripts/plans_registry.py` requires (`REQUIRED`).
