---
title: "Research — run-report"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-o2yc
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
---

# run report — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-28: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 727 files, 2499 commits, 12 rules.

Stage-2 call, 2026-10-28: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 727 files, 2503 commits, 12 rules.

## Runner exploration — 2026-10-28

Research complete. Here is the prose for `plans/changes/run-report/research.md` (ready to append below the call lines; English, per house rule 1).

## Neighbours already known

`plans/changes/runner-time-line/` (spec, research, plan; bead coding-harness-9wp), `plans/changes/runner-time-line-exits/` (spec, same bead), `plans/changes/attempt-diagnostics/` (spec, bead coding-harness-cit), `plans/changes/archive/2026-10-08-stage2-runs-count/spec.md` (bead coding-harness-kw0), `plans/changes/research-swarm/spec.md`, `plans/changes/stage2-session/`, and the living description `docs/WORKFLOW.md` §3–§4.

## What the change's own brief says — and what could not be read

The bead coding-harness-o2yc carries the change's intent, but its description was not read: the tracker is the Dolt database under `.beads/` (AGENTS.md house rule 2), no rendered copy is committed, and this explorer has read-only file tools and no shell, so nothing rendered it. `.beads/interactions.jsonl` and `.beads/metadata.json` name no o2yc. What the repository states is the name ("run report", folder `plans/changes/run-report/`, branch `feat/run-report`), the class `bounded` (frontmatter of `plans/changes/run-report/research.md`, confirmed by the commit 7cf733ac subject), and the previous explore being stopped for low memory with its call line left unchanged (commit 790fa3f3). "Run report" as a term is not there in first-party code or docs: a search over the tree hits only third-party text under `tools/pi/node_modules/`. What the bead exactly asks — a per-run artifact, a console summary, or a wider count — is therefore an open question for phase 1a, not a fact.

## What exists today: what one stage-2 run leaves behind

**Per-call audit lines in the change folder.** `call_line()` (`scripts/stage2.py`, function `call_line`) builds the one audit line of a checked call — date, verb, endpoint, model, and the leak check's three numbers — and `begin_call()` appends it to `findings.md`, creating that file with `findings_header()` when missing. The work verbs use `begin_work_call()`, whose line adds `attempt N · route <route>` and an optional reason, written into the phase artefact: for `explore` that is `research.md` (function `explore` calls it with `ctx.research`). The `session` verb writes a line ending ` · dispatch pending.` and later rewrites exactly that line to `accepted` or `failed` (`scripts/stage2_session.py`, `finalize` and the audit-line section).

**Failure traces in `findings.md`.** A failed implement or repair attempt leaves its diagnostics and the files its model changed, quoted, below its audit line (module docstring of `scripts/stage2.py`; `save_attempt`, `protect_diagnostics`) — the mechanism of the attempt-diagnostics change. A review-loop attempt whose calls ran but wrote no round leaves a `Loop attempt: <date> — no round was written …` marker (`NO_ROUND_KEY` in `scripts/stage2.py`, written in the round function's exception path).

**Runner-measured time, in `plan.md`.** One line per completed attempt under `## Time used`: `time_entry()` formats start–end UTC, seconds, verb, attempt, route, model and accepted/rejected, "measured by the runner"; `with_time_entry()` appends it and `time_log()` reads the section (`scripts/stage2.py`). This is the runner-time-line change's mechanism; both accepted and rejected attempts are logged (its `research.md`, question marked answered 2026-10-20).

**The loop record, outside the repository.** `record_base()`/`record_dir()` place it under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>@<digest>/loop.md` (module docstring of `scripts/stage2.py`, "The loop record"; `RECORD_HEADING`). It holds the rounds' rows, the run's stage snapshot (`Loop state:`, the runner's own line) and consumed stages, until `release-loop` carries everything into `findings.md` and deletes the record. `write_round()` appends a round and the updated snapshot in one write; the round's console report is a single stdout line ("round N written … rows from M of K members").

**Receipts and probe audits, in the same state directory.** The review loop's preparation receipt `availability.json` and the research swarm's `research-availability.json` both live under `record_dir(change)` (`scripts/stage2_availability.py`, `research_receipt_path` and the loop receipt path); each probe launch appends a scrubbed `research-probe-<uuid>.json` (`_ProbeAudit`). Receipts are single-use, sealed by SHA-256 over their canonical JSON (`seal`, `verify`, `write_receipt`).

**The research run store, per run id.** `record_dir(change)/research/<run-id>/` holds `run.json` and per-slot `<slot>.launch.json` / `<slot>.result.json` (`scripts/stage2_research_store.py` docstring); a slot is reused only on exact match of binding through prompt hash. No worker writes `research.md` — audit lines, reports and status are buffered and appended once by the runner at the end or abort of the run (`scripts/stage2_research_run.py` docstring).

**Console output, one line per event.** The verbs print scattered single lines, not a summary: `explore` ("answer appended to … · route …"), `review`, `release-loop`, `probe` (answered/failed member lists), implement/repair ("verified and committed · route … · attempt …"), plus stderr notices through a review-loop round (`scripts/stage2.py` print statements throughout, e.g. the round end and the interrupt/terminate line in `main`).

**The post-hoc counter.** `scripts/stage2_runs.py` reads named changes' `findings.md`/`research.md` — active or the one archived folder (`locate`) — with the runner's own constants (`CALL_LINE`, `CLEAN`, `stage2.ROW_COLUMNS`/`RELEASED_COLUMNS`) and prints a per-change Markdown row: loop rows taken/rejected/undecided, rows marked `Broke a test: yes`, phase-6 rounds, phase-2a/6 rows by severity, disagree marks, calls clean/total, then D-13's criteria as numbers. Its stated limits: a refused call writes no line and so is not counted; tokens and cost per vendor are not recorded anywhere (`stage2_runs.py` docstring; `docs/WORKFLOW.md` §4, "The count is generated, not typed"). Its origin and the evaluation it fed: the archived change 2026-10-08-stage2-runs-count and `docs/research/2026-10-08-stage2-three-runs.md`. `tests/test_stage2_runs.py` pins it with fixtures built from the runner's own renderers; `tests/test_stage2.py` pins the writers (for example, a Pi off the pin writes no call line).

## What is unclear about it

No artifact today consolidates one run: the pieces sit in four places — `findings.md`/`plan.md` in the change folder, `loop.md` outside the repository (deleted at release), the receipts and run store outside the repository, and ephemeral stdout. What the runner knows only in memory — refused calls, per-call durations, replacements, consumptions, exits — survives only in those fragments, and some (refusals, tokens, cost) nowhere at all. Whether a "run report" is meant to close that gap, and where it should live (change folder versus the runner's state directory), the repository does not say; the bead's wording was not read. Also unclear: whether the report should read the record and store after the fact (they are scrubbed JSON in the state directory, by design outside any artifact a model can edit) or be written by the runner as the run goes.

## Which files a change would have to touch

Whichever form it takes, the centre is `scripts/stage2.py` — the call-line writers (`call_line`, `begin_call`, `begin_work_call`), `write_round`, the verb ends, and `record_dir` for anything placed beside the record. If the count grows, `scripts/stage2_runs.py` and `tests/test_stage2_runs.py`; if receipts or the run store feed it, `scripts/stage2_availability.py`, `scripts/stage2_research_store.py`, `scripts/stage2_research_run.py`. Existing pins live in `tests/test_stage2.py`; documentation to move in the same pull request would be `docs/WORKFLOW.md` §3–§4 (the loop record, the generated-count block) and possibly `templates/findings.md`. A text-only wording change in `docs/WORKFLOW.md` alone would skip local `make verify` per AGENTS.md.

## Draft gap check — 2026-10-28

Read at input commit `6daf7b17`. The interview skip and agent details in
`decisions.md` supersede the explorer's uncertainty about intent and its
conditional file list: this is a separate read-only report, and
`scripts/stage2.py` must stay unchanged. The bead itself was not read by
this drafting session; the orchestrator's recorded brief is its source.

- `stage2.time_log(path)` reads only the section boundaries and returns
  text; `stage2.time_entry(...)` writes the canonical seconds, attempt,
  route, model and verdict. `stage2.card_problem(text)` validates card
  labels but does not extract an appetite. `stage2_runs.CALL_LINE`
  recognises audit lines and exposes their remainder, without parsing
  attempt durations. Reuse these existing boundaries and constants; the
  new report still needs local field extraction, without changing either
  existing module or duplicating their format-recognition expressions.
- Existing time sections contain prose and unmeasured entries as well as
  canonical runner lines (`plans/changes/runner-time-line/plan.md`). The
  research-swarm plan also holds dated orchestrator spans with ISO UTC
  endpoints, approximate spans and overlapping narrative evidence. A
  number in prose is not by itself a measured duration: unread entries
  must remain visible rather than being guessed from arbitrary numbers.
- `Makefile` has no report target. `templates/` has a spec and design
  template, but no plan template; use the phase-3 prompt's required form
  and the neighbouring runner-time-line plan's structure.
- `scripts/validate_change_artefacts.py` does not exist at this commit.
  The interview and criterion-ledger checks exist. Registry checking also
  checks the generated index and reads the tracker through
  `scripts/bead_render.py`; the runner owns that preparation and full
  verification after this draft.
- The latest handover read is
  `docs/journal/handover/2026-10-28-three-lane-night.md`. Its measured
  verification contention explains the report's advisory resource check;
  automatic verification locking remains separate work. The current PR
  state could not be read because GitHub was unreachable. The live session
  registry was not read: it is outside this draft's permitted read boundary.
