---
title: "Research — runner-precheck"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-csm
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# runner precheck — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Orchestrator exploration — 2026-10-20

Explored by the orchestrator (Opus 5.5) by reading `scripts/stage2.py` at
`origin/main` `ff1e1de`: the runner's explore route with `--stage2-off`
currently answers with no research (bead coding-harness-e7m), so it was not
used.

### Result first

- `verify_attempt` (`scripts/stage2.py:3035`) runs, in order: derived-file
  preparation, ruff's safe fixes and formatter on the changed Python files,
  the full `make verify`, and only then the check that `plan.md` gained a
  measured line under `## Time used` (`scripts/stage2.py:3068–3076`). A
  missing time line is found after the full run (about 5 to 7 minutes with
  `pytest-xdist`, measured 2026-10-20), and it fails an attempt whose code is
  green.
- On a red `make verify`, the evidence is the framed red gates' last lines
  (`red_sections`, `TAIL_LINES = 80`, `scripts/stage2.py:2783–2830`) plus the
  tail of standard error. For a pytest gate with hundreds of lines, the
  assertion text of the first failing test can fall outside those lines; the
  bead's measurement of 2026-10-16 saw `FAILED` lines cut to `As...`.
- Nothing runs before `make verify` that is cheaper and could stop a hopeless
  attempt early. The tests named in `plan.md`'s criterion ledger
  (`tests/…::test_…`, ADR 0013) are exactly the attempt's own proofs and run
  in seconds.

### Measured cost (night of 2026-10-19/20)

- Research swarm, rounds 8 and 9: four repair attempts failed only because
  `plan.md` gained no measured line; each had paid a full `make verify`
  first. The code of the last attempt passed a full `make verify` when the
  orchestrator ran it by hand.
- Rounds 8 and 9 also lost one attempt each to a single load-sensitive test
  (bead coding-harness-jik), and round 7 two attempts to the ruleset gate
  (HTTP 403 before the organisation's Team plan). Those are not this change's
  cause, but the same pre-check would have shown in seconds that the
  attempt's own tests were green.
- Together about 1 h 45 min of runner time that ended in a hand repair.

### The maintainer's direction (2026-10-16, recorded in the bead)

1. Before the full `make verify`, run ruff on the changed Python files and
   the tests named in `plan.md`'s criterion ledger; if that is red, fail the
   attempt with those tests' full assertion messages (scrubbed, bounded) and
   skip `make verify` for that attempt.
2. On a red `make verify`, the evidence adds the assertion text of the first
   failing tests, not only their names.
3. `make verify` stays the only check after which the runner commits; a green
   pre-check proves nothing on its own.
4. Rejected: letting the foreign model run pytest itself during the call
   (ADR 0007 boundary).

### Where the change sits

- `verify_attempt`: a pre-check step between `format_step` and
  `make verify`; the time-line check moves before `make verify` as part of it
  (it needs no run at all).
- A small reader of the criterion ledger's `tests/<path>::<test>` entries
  (the form `check_criterion_ledger.py` already parses).
- `verify_evidence`: the first failing tests' assertion blocks from pytest's
  output, bounded and scrubbed, ahead of the gate tails.
- `run_attempts`, `draft` and `repair` use `verify_attempt`; all three gain
  the pre-check without their own code.

### Questions

- `[DECISION]` answered (maintainer, 2026-10-16): the pre-check as above;
  recorded as Q-1 in `decisions.md`.
- `[DETAIL]` The time-line check runs before `make verify`: it reads one
  file, and a missing line already fails the attempt today, only later.
- `[DETAIL]` A ledger entry whose test does not exist yet is not run by the
  pre-check (a ledger row "not yet written" names no test); `make verify`
  still runs the suite.
- `[GAP]` Whether the pre-check's pytest run uses `-n` (xdist) or runs
  serially: a handful of tests start faster serially; to be measured in
  phase 4.
- Not in this change: the runner writing the measured time line itself
  (it knows the attempt's start and end); a single retry of one failed test
  (bead coding-harness-jik). Both are proposals for the maintainer, not part
  of the decided direction.

## Draft-time repository checks — 2026-10-20

Read at draft baseline `52e440d`; these checks resolve repository gaps without
changing the maintainer's answer above.

- Correction to "Where the change sits": `run_attempts` calls
  `verify_attempt` for implement and repair. Draft uses `verify_draft`, a
  separate function: it requires the time heading but deliberately no measured
  implementation line. Both verification functions use `verify_evidence`.
  Therefore only implement and repair gain the pre-check; draft gains richer
  failure evidence without changing its checks (`scripts/stage2.py`).
- The ledger gate already exposes `ledger_sections`, `parse_entry` and
  `Entry.kind`; only kind `test` is runnable. Its section reader ignores
  fenced headings. Reuse those readers rather than searching the whole plan
  for test-looking text (`scripts/check_criterion_ledger.py`).
- `format_step` currently reports ruff problems without failing the attempt;
  existing tests explicitly require that behavior. A separate strict check
  after safe fixes can make the new pre-check decisive without inferring a
  verdict from its human-readable formatting note. Related expectations in
  `tests/test_stage2.py` need to reflect the new early-abort contract.
- The worktree pytest configuration adds no xdist workers by default
  (`pyproject.toml`). A serial targeted run is the reversible initial choice;
  no serial-versus-parallel timing comparison has been measured here. Use the
  worktree interpreter as `red_first_python` already does, and the existing
  credential-free verification environment (`scripts/stage2.py`).
- Neither `templates/plan.md` nor
  `scripts/validate_change_artefacts.py` exists at this baseline. The plan
  follows `prompts/03-plan.md` and the existing bounded plan form; the absent
  validator cannot be reported green. No new template or validator is in scope.
- `findings.md` contains the draft-call audit line only, with no phase-2a
  finding rows to resolve. Local branch `feat/runner-precheck` and its
  remote-tracking ref both point to `52e440d`; hosted pull-request state and
  current parallel-session ownership were not read. No tracker write is needed.

