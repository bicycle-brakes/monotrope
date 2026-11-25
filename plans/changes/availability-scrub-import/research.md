---
title: "Research — availability-scrub-import"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-vg9.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-25", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
neighbours: []
---

# availability scrub import — Research

## Topic (bead coding-harness-vg9.2, copied by the orchestrator 2026-11-25)

Class: bounded.

Why: scripts/stage2_availability.py:145 does 'from stage2 import scrub'
inside an except block of a function, while the module otherwise receives
the runner module as a parameter. It is the one import that closes the
stage2 <-> stage2_availability cycle and a second path to the same function,
so a monkeypatched or moved scrub is missed there.

What: use the runner parameter's scrub (or the shared secrets home once vg9
decides it) and add a test that the module does not import stage2.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp), from an external stage2.py modularization analysis.



PARENT
↑ ○ coding-harness-vg9: Refactor stage2.py into cohesive runner modules P2

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu) · leak check clean over 1202 files, 5782 commits, 12 rules.

## Runner exploration — 2026-11-25

Research for `availability-scrub-import` (bead coding-harness-vg9.2, class `bounded`). Read-only pass over the worktree at 2026-11-25; I ran no commands and changed no files.

**What exists today**

- `scripts/stage2_availability.py`, function `read_intelligence(models, slugs)`: in its `except Exception` branch it runs `from stage2 import scrub` and redacts the error text with that function before storing it as `reading["status"]`. This is the only `stage2` import in the module. Its module-level imports are `stage2_go`, `stage2_research_map`, `stage2_swarm`, `leakcheck`, `venv_guard`, and `yaml`.
- The module docstring of `scripts/stage2_availability.py` states that the runner module (`scripts/stage2.py`) reaches the swarms "through the `runner` argument". Other functions in the same file already use `runner.scrub(...)`, for example `_failed(runner, …)` and the scrub calls in the probe and launch paths.
- `scripts/stage2_session.py` (module docstring, "Why the runner module travels as a parameter"): under `python3 scripts/stage2.py` the runner runs as `__main__`, so an `import stage2` in a helper loads it a second time, with second `Refused` and `CallFailed` classes that `main()` does not catch. The helper pattern is the documented rule for this cycle.
- `scrub(text, secret)` is defined once, in `scripts/stage2.py` (`def scrub`). I found no other definition and no module that could be called a "shared secrets home". Open question: the bead's alternative ("or the shared secrets home once vg9 decides it") has no counterpart in the tree.
- `read_intelligence` has no `runner` parameter. Its one production caller is `prepare_research` in `scripts/stage2_availability.py`, which has `runner` in scope and passes it a sorted model list plus `block.get("intelligence_slugs")`.
- Tests that call `read_intelligence` directly with two arguments: `tests/test_stage2_research_availability.py` (around the `broken` fetch and the `intelligence_document()` cases). They replace `INTELLIGENCE_FETCH` through `monkeypatch`. A test asserts the error path is redacted (`test_intelligence_errors_redact_credential_fragments`, cited from the archived research-swarm plan).
- An AST-based inventory test exists in `tests/test_stage2.py`, `test_every_pi_settings_writer_uses_shared_constant`. It is the existing pattern for a structural check on this module's source. I found no test that asserts `stage2_availability.py` does not import `stage2`.
- Tests that monkeypatch `scrub` itself: none found in `tests/`. The `tests/` hits for `scrub` call `stage2.scrub` directly or cover behaviour through the runner.
- `plans/changes/archive/*` and the open `coding-harness-vg9` references show that `tests/test_stage2.py` requires a full `make verify` until vg9 splits the runner. This change would touch `scripts/stage2_availability.py` only, so that note does not apply to it directly.

**What is unclear**

- The bead says the import "closes the stage2 <-> stage2_availability cycle". At module level `stage2_availability.py` does not import `stage2`. The cycle exists only at runtime through function-local imports, and `stage2.py` also imports `stage2_availability` inside functions (`prepare`, `consume`, `spend`, and the research prepare path). I did not trace every edge of this graph.
- Whether a test or a runtime path can currently observe the duplicate-module effect: the bead says a monkeypatched or moved `scrub` is missed, but I found no test that does this. Open question: is the claim from a measured failure or from analysis only? The source of the claim is an external modularization analysis, checked 2026-11-24 at `18a13d3d`.
- Whether `read_intelligence` should take `runner` as a new parameter (its caller has one) or a `scrub` callable. Both are possible; the choice belongs to the spec, not to this research.
- The four `tests/test_stage2_research_availability.py` and `tests/test_pi_contract.py` call sites that set `INTELLIGENCE_FETCH` do not pass `runner`. A signature change touches those call sites or their fixtures. I did not read every one.

**Which files a change would have to touch**

- `scripts/stage2_availability.py`: `read_intelligence` (drop the function-local import, use the passed-in scrub), and `prepare_research` (pass `runner` or its `scrub`).
- `tests/test_stage2_research_availability.py`: the direct `read_intelligence(...)` calls near the intelligence tests.
- `tests/test_stage2_availability.py` or `tests/test_stage2_research_availability.py`: a new test that the module does not import `stage2`. An AST check in the style of `test_every_pi_settings_writer_uses_shared_constant` is the nearest existing pattern.
- Not touched by the bead's own wording: `scripts/stage2.py` (the `scrub` definition) and the shared-secrets question, which the bead leaves to vg9.
