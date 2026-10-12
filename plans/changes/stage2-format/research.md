---
title: "Research — stage2-format"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-52r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, implement, formatting]
---

# Stage-2 runner formats the attempt — Research

Phase 1 for bead coding-harness-52r, read against `origin/main` on
2026-10-12. In change stage2-repair (bead coding-harness-g2f) every attempt
of `implement` (GLM 5.3 Flash, its repair, the Sonnet 5.5 fallback) and every
attempt of the new `repair` verb failed `make verify` on the gates
`ruff-format` or `ruff-check` alone: the work models have file tools and no
command tool, so they cannot run the formatter. The orchestrator then ran
`ruff format` by hand and `make verify` went green. The bead asks the runner
to format the attempt's changed Python files (and apply ruff's safe fixes)
before `make verify`, so that a pure formatting miss no longer burns all
attempts. The change is meant to be small.

## Questions for the exploration

1. How `verify_attempt` and `prepare_derived` in `scripts/stage2.py` run
   today: which paths they read (`changed_paths`), which environment and
   which process launcher they use, and how a failure of the preparation
   becomes a diagnostic.
2. How the `ruff-format` and `ruff-check` gates of `make verify` call ruff
   (`scripts/verify_all.sh`, `Makefile`, `pyproject.toml` or `ruff.toml`):
   the version, the configuration, the paths they cover, and where the ruff
   executable lives in a worktree's `.venv`.
3. Which of ruff's fixes count as safe (`ruff check --fix` without
   `--unsafe-fixes`) under this repository's rule selection, and whether a
   safe fix can change behaviour or a test's meaning.
4. Which tests in `tests/test_stage2.py` pin the preparation step and the
   attempt sequence, and how a stand-in for `make` and for ruff is planted in
   the test world.
5. Whether formatting must run on changed `.py` files only or on the whole
   tree, and what happens to a file the model did not change but ruff would
   reformat.
6. Whether the step must be recorded (in `findings.md` or the commit) so a
   reader sees that the runner, not the model, formatted the code.
