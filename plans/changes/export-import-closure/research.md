---
title: "Research — export-import-closure"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# export import closure — Research

## Topic (bead coding-harness-5ane.7)

Class: bounded. Why (audit C-7, confirmed): scripts/export/manifest.yaml has no rule for scripts/bead_render.py, while two exported scripts import it, so an exported instance fails on import. What: export bead_render.py (or cut the import), and add a test that every exported Python script imports only exported modules. Acceptance: the import-closure test is green on the export manifest. Source: PR #437 (full codebase audit, base 24632499), re-verified against main b9ce3ac0 on 2026-11-24 by five read-only checks in session c820a13d.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1325 files, 6189 commits, 12 rules.

## Runner exploration — 2026-11-28

## Research: export-import-closure (bead coding-harness-5ane.7, class bounded)

Read-only facts, sourced from the working tree at the worktree's current HEAD. Nothing was run; every import fact comes from reading source.

### What exists today

**The export manifest** (`scripts/export/manifest.yaml`, read by `tests/test_kit.py`, `tests/test_lock.py` and `tests/test_venv_guard.py`):
- Rules are `{prefix, verdict}` pairs; `carry` travels, `geruest` travels as an empty shell, `drop` stays. The longest matching prefix decides, and the catch-all `prefix: ""` is `drop`.
- `scripts/kit/` is `carry`. Among the scripts, `carry` is set for `scripts/_verdict.py`, `scripts/venv_guard.py`, `scripts/gate_record.py`, `scripts/check_decision_continuity.py`, `scripts/check_bead_export.py`, `scripts/check_dangling_bead_ids.py` and `scripts/check_docs.py`.
- No rule names `scripts/bead_render.py` or `scripts/render_beads_export.py`. Both fall to the catch-all `drop`. `tools/`, `.beads/` and `tests/` are `drop` too.

**The kit manifest** (`scripts/kit/manifest.yaml`, role `mechanismus`) carries all four files: `scripts/check_bead_export.py` (reason: checks the rendered export line by line, bead bo0), `scripts/check_dangling_bead_ids.py` (bead bo0), `scripts/bead_render.py` (the one access point to the tracker state, bead 1jg.3) and `scripts/render_beads_export.py` (the one-writer renderer, bead bo0). The two manifests are deliberately different questions. `tests/test_kit.py::test_the_kit_list_is_not_derivable_from_the_export_list` guards that they stay independent.

**The import graph** (from reading the source):
- `scripts/check_bead_export.py`: top-level imports are stdlib only (`json`, `sys`, `pathlib`). `from bead_render import RendererNichtMoeglich, nicht_gemessen, render_pfad` sits inside `main()`.
- `scripts/check_dangling_bead_ids.py`: top-level stdlib only (`json`, `re`, `sys`, `pathlib`). The same `from bead_render import …` sits inside `main()`.
- `scripts/bead_render.py`: top-level stdlib only (`os`, `sys`, `tempfile`, `pathlib`); it inserts its own directory into `sys.path`. Inside `_frisches_render()` it runs `from render_beads_export import RendererFehlt, _render_nach`.
- `scripts/render_beads_export.py`: top-level stdlib only (`argparse`, `hashlib`, `json`, `subprocess`, `sys`, `tempfile`, `pathlib`). `from check_bead_export import run` sits inside a function.
- The resulting function-level cycle is `check_bead_export → bead_render → render_beads_export → check_bead_export`.

**Consequence, read from the code:** the two exported check scripts do not fail when they are imported. They fail when `main()` runs, because `bead_render` is missing. A static walker that follows imports inside function bodies would also reach `render_beads_export`, which is not exported either. The audit names only `bead_render`.

**The other carried Python files:** `scripts/kit/probe.py` imports `venv_guard` and `_verdict` (both carried) and `yaml`. Grepping `scripts/kit/` for a list of local module names found nothing else. The other carried scripts (`_verdict`, `venv_guard`, `gate_record`, `check_decision_continuity`, `check_docs`) import only stdlib at the top level. I did not read every file in `scripts/kit/` in full.

**Existing checks of the closure:** none found. `scripts/kit/probe.py` contains `unguarded_imports` (a venv-guard check over `ast`) and no import-closure walker. The `--strict` flag there means "DRIFT blocks too", not a closure check. The proposal in `docs/research/2026-11-24-draft-adr-state-first-and-manifest.md` (a static closure check in `probe.py --strict`) is therefore described in a research note but not implemented in `probe.py`.

**Other references:**
- The audit row `coding-harness-5ane.7` (P2) is in `docs/research/2026-11-24-verified-audit-synthesis-and-roadmap.md`. The same research note proposes adding `scripts/bead_render.py` to the manifest as a point patch.
- `scripts/ci_gates.py` describes `bead_render.py` as a library that its readers import, so it has no CI step of its own.
- Tests that reference these scripts live under `tests/` (`test_bead_render.py`, `test_archive_closed_changes.py`, `test_close_merged_beads.py`, `test_gate_machinery.py`, `test_ci.py`, and others). The `tests/` tree is `drop` in the export, so these do not travel.

### What is unclear

- **Scope of "imports only exported modules".** The audit's wording is satisfied by `bead_render` alone only if function-level imports are not counted. If they are counted, `render_beads_export` is also missing. Which reading applies is not stated in the bead or the spec; the bead description was not read (the tracker is not readable from this read-only phase).
- **Runtime dependency outside Python imports.** `render_beads_export` runs `bd` through `subprocess` and raises `RendererFehlt` when no binary is present. `tools/bd` and `.beads/` are `drop`. A static closure test would not see this; it is open whether the acceptance covers it.
- **Whether the exported check scripts are meant to run in a target repository at all.** They are carried by the export verdict, but their render depends on `bd`, which the export does not carry. The intent is not stated in the files I read.
- **Where a closure test would live.** Tests are `drop`, so a test under `tests/` would not travel with the kit. Whether the walker belongs in `scripts/kit/probe.py` (which already parses with `ast`) or in a test is not decided in any file I read.
- **The research header.** `plans/changes/export-import-closure/research.md` has no `neighbours:` line, and its class appears only in prose (`Class: bounded`), not as a header declaration. This phase writes nothing, so the header is not changed here. For a bounded change the single explorer path applies; the swarm path would refuse without the header.
- **Neighbour specs.** I did not find an active or archived `spec.md` that names `scripts/export/manifest.yaml` or the four files. The grep over `plans/` for "export" returned 53 files, and I did not open the archived ones to confirm they are unrelated.

### Which files a change would have to touch (as the code stands)

- `scripts/export/manifest.yaml`: rules for `scripts/bead_render.py`, and for `scripts/render_beads_export.py` if the function-level import counts. This is the only place verdicts live.
- A closure check: no existing file implements it, so it is new code. The `ast` pattern is already used in `scripts/kit/probe.py` (`unguarded_imports`) and `scripts/touch_map.py` (`ast.walk`).
- `tests/`: the new check's test lives there (`tests/` is `drop`, so it does not travel).
- The three tests that read the export rules are affected by any added rule and need to keep passing: `tests/test_kit.py` (AK-6 block, `_export_regeln`), `tests/test_lock.py` (`_export_verdicts`) and `tests/test_venv_guard.py` (the rules loader near its line 365). I read their loaders but not their assertions.
