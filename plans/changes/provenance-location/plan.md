---
title: "Plan — provenance-location"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-3ar.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, provenance, adr-answers, kit]
---

# Plan — provenance-location

```text
For you:     The ADR-answer command also works where the provenance map is decisions/provenance.yaml (LakeSwitch), and refuses clearly when both places hold one.
Done when:   tests/test_harness_decide_adr.py holds criteria 1-8 of spec.md, and make verify is green.
Appetite:    2 hours of phase 4, repair rounds included; a stop, not an estimate.
Not now:     the map's other readers, a configurable place, LakeSwitch adding roles:.
Pre-mortem:  suppose it failed: most likely because presence was tested with Path.exists, so a broken link at one place silently hands over to the map at the other.
Starts unless you say stop.
```

Implements [`spec.md`](spec.md). Explore ran on stage 2 (GLM 5.3 Flash);
`research.md` records no stage-1 fallback to carry.

## Files

1. `scripts/harness.py` — `PROVENANCE` becomes `PROVENANCE_PLACES =
   ("provenance.yaml", "decisions/provenance.yaml")`. A new
   `provenance_map(root) -> tuple[Path, str]` returns the one place present
   by `os.path.lexists` (path, and its text from the top of the tree), else
   raises `Refused`: none present → `no provenance map: looked for
   provenance.yaml and decisions/provenance.yaml; one of them must name who
   answers, under paths:` plus today's entry text; both present → `two
   provenance maps, provenance.yaml and decisions/provenance.yaml — keep one
   of them`. `answering_role` calls it first and puts that text wherever its
   messages say `{PROVENANCE}` today; its signature stays. The module
   docstring gains one sentence: the two places, in order, and the refusal
   over both.
2. `tests/test_harness_decide_adr.py` — `_repo` gains `map_at:
   str = "provenance.yaml"`; `_written` counts files under
   `decisions/answers/` (plus the message) instead of all of `decisions/`, so
   a map at `decisions/provenance.yaml` is not taken for a written file; the
   tests of the table below.
3. `plans/changes/provenance-location/plan.md` and the rendered
   `plans/INDEX.md` — this phase.

Not touched, though they read or name the map: `scripts/check_adr_answers.py`
(never opens it), `scripts/check_frontmatter_current.py`,
`scripts/ramp_valves.py`, `scripts/stage2.py`, `provenance.yaml`,
`scripts/kit/manifest.yaml`, and the order of checks in `main()`.

## Verification

```bash
.venv/bin/python3 -m pytest -q tests/test_harness_decide_adr.py
make verify
```

Baseline at `12d9aa9`: 46 passed in the first command.

## Tests per criterion

All in `tests/test_harness_decide_adr.py`; "both flows" means the loop over
`()` and `_record()` the refusal test already runs.

| # | Test | Must go red when |
|---|---|---|
| 1, 2 | `test_answered_by_is_the_role_the_map_names`, parametrised over `map_at` (the two places) | the second place is never looked at; the top-level map is no longer read |
| 3 | new `test_two_maps_refuse_before_asking`, both flows, over (top, `decisions/`) = (map, same map), (map, not YAML), (map, a directory), (a link to nowhere, map); asserts both paths and `keep one` | presence follows links, so the broken top-level link hands over to the other map; one place silently wins; one path unnamed |
| 4 | new `test_without_a_map_the_refusal_names_both_places`, both flows — the "no map" case moves here from the refusal test | the message names one place only, or loses `prefix: "decisions/answers/"` |
| 5, 6 | `test_a_map_without_the_role_refuses_before_asking`, cases not YAML, not a mapping, no entry, no `owner_role`, role not declared, no `roles:` key, each at both places; asserts the place's path in the output, and for the top-level map that `decisions/provenance.yaml` is not | a message still says `provenance.yaml` about the map under `decisions/`; a missing `roles:` key passes |
| 7 | new `test_root_names_the_tree_not_the_working_directory` — `monkeypatch.chdir` into a directory whose `provenance.yaml` names `decoy`; `--root` a tree whose `decisions/provenance.yaml` names `someone-else` | the places are resolved against the working directory |
| 8 | `test_this_repository_declares_the_answering_role`, unchanged | a `decisions/provenance.yaml` added here, or the top-level map no longer read |

## Criterion ledger

- 1: tests/test_harness_decide_adr.py::test_answered_by_is_the_role_the_map_names
- 2: tests/test_harness_decide_adr.py::test_answered_by_is_the_role_the_map_names — parametrised over the two places
- 3: tests/test_harness_decide_adr.py::test_two_maps_refuse_before_asking
- 4: tests/test_harness_decide_adr.py::test_without_a_map_the_refusal_names_both_places
- 5: tests/test_harness_decide_adr.py::test_a_map_without_the_role_refuses_before_asking — both places, the place's path in the message
- 6: tests/test_harness_decide_adr.py::test_a_map_without_the_role_refuses_before_asking — case "no roles: key"
- 7: tests/test_harness_decide_adr.py::test_root_names_the_tree_not_the_working_directory
- 8: tests/test_harness_decide_adr.py::test_this_repository_declares_the_answering_role

## Time used

2026-10-12 — the implement session ran on the stage-2 runner with file tools
only: it read the date at its start (2026-10-12) and again at its stop
(2026-10-12) and claims no span; the runner's clock measures the real span
against the appetite of 2 h, and no duration is invented here.

2026-10-12 — the repair round after attempt 1 (ruff-format red on both code
files) ran the same way, file tools only: it read the date at its start and at
its stop (2026-10-12) and claims no span; the runner's clock measures the real
span against the appetite of 2 h. It changed formatting only — no test, no
message, no criterion.
