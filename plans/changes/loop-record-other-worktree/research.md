---
title: "Research — loop-record-other-worktree"
status: draft
implementation_status: none
date: 2026-11-18
last_reviewed: 2026-11-18
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-e82i
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-18", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# loop record other worktree — Research

Stage-2 call, 2026-11-18: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1113 files, 4587 commits, 12 rules.

## Runner exploration — 2026-11-18

The exploration is complete. Below is the research as prose, ready to append to `plans/changes/loop-record-other-worktree/research.md`.

---

## What exists today

**The loop record and its per-worktree key.** The phase-4b loop keeps its rows outside the repository, at `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>@<digest>/loop.md`, until the phase-6 verdict releases them into `findings.md`; the release is the only thing that deletes the record (`scripts/stage2.py`, module docstring, "The loop record"). The key is built by `record_base()` (reads `XDG_STATE_HOME` at call time, default `~/.local/state`) and `record_key(change, root)`, which is `f"{change}@{sha256(str(root.resolve()).encode('utf-8'))[:8]}"` (`record_key`, `scripts/stage2.py`). Its docstring states the intent: "Two worktrees may hold the same change folder, and one `release-loop` must not delete the other's record or hand it another's state (R-2 of the review-swarm review)." `record_dir` and `lock_path` sit beside it, and `holding_record` takes an advisory `flock` so one runner per record runs at a time (R-14). Because the digest input is the resolved root path string, the same change name continued in a differently named worktree computes a different key — the record is bound to the checkout, not to the change.

**Where the keying came from.** Review finding R-2 (2026-10-20 runner review of the review-swarm runner, `docs/journal/handover/2026-10-20-review-swarm-runner-review.md`, "R-2 — Record and receipt are keyed by change name only, not by worktree") measured that two worktrees sharing a change folder shared one `loop.md`, so worktree B continued A's stages and a release in A deleted B's record; the proposed fix was the resolved-root digest key. It merged as PR #189, merge commit `4c7629d` (merge-day handover `docs/journal/handover/2026-10-21-merge-day.md`, "Done today"); the record lock R-14 followed as PR #190, `378879a`.

**Who reads the record, and what happens when it is "missing" at this root's key.** `read_record(change, root)` returns `None` when `loop.md` does not exist under this root's key (`read_record`, `scripts/stage2.py`). On `None`, `lost_record_refusal(change, root, text)` fires — in `review_loop`, in `release`, in `retire_stage`, and in `prepare-loop` through `prepare` (`scripts/stage2_availability.py`, `prepare`, which calls `runner.lost_record_refusal` when `runner.read_record` is `None`) — but only when `findings.md` shows review-loop audit lines still unaccounted for after the last release or restart line (`lost_record_refusal`; each no-round marker accounts for exactly its failed attempt's audit calls, DL-A-6). The refusal names the expected path and diagnoses two causes: "the loop ran and its record is lost or under another state directory (XDG_STATE_HOME)" (`lost_record_refusal`, message text). A record under *another worktree's key of the same state directory* — the third, and per the incident below actual, cause — is not named by this message. `triage` refuses separately, with "the change has no loop record here; the loop has not run for it in this worktree." (`triage`, `scripts/stage2.py`). Conversely `write_round` happily starts a fresh record (heading, intro, snapshot) at the new key when none exists, so a continued run in a new worktree does not inherit the old run's snapshot, consumed stages or rows.

**The record directory holds more than the loop.** The same `record_dir(change, root)` directory carries the phase-1 research state store and the availability receipt: `research_receipt_path` returns `record_dir(change, root) / "research-availability.json"`, and `_ProbeAudit` writes `research-probe-*.json` there (`scripts/stage2_availability.py`); `stage2_research_store.research_dir` re-implements the identical key formula and cites R-2 for it (`scripts/stage2_research_store.py`, `research_dir`). The research receipt additionally binds `root.resolve()` (plus change, configuration digest and neighbours) in its `binding` field, checked on reuse (`research_binding` and the receipt validity check, `scripts/stage2_availability.py`) — so a foreign receipt is *invalid* where the loop record is simply *absent*. `remove_loop_record` deletes the directory on release but preserves `research/` and `research-*` entries (`remove_loop_record`, `scripts/stage2.py`).

**Recovery paths that exist today.** `release-loop --restart --reason <reason>` is the maintainer's way past the refusal (`release_loop` dispatch and `restart_loop`, `scripts/stage2.py`; documented as the restart amendment in `docs/WORKFLOW.md`, "the loop record" section): it needs a completed round in `findings.md`, and without one it refuses with "the maintainer must account for the stale audit lines in findings.md by hand before retrying" (`restart_loop`, refusal text; test `test_restarting_a_lost_first_record_names_manual_accounting`, `tests/test_stage2.py`). `release-loop --stage-failed` retires a wedged stage (maintainer decision bead coding-harness-tex, recorded in `retire_stage`'s docstring). A verb that lists or adopts a record under another worktree's key does not exist: a search of `scripts/` for any enumeration of `record_base()` (`glob`/`iterdir`/sibling/other-key) returned no match — not there as of this worktree's head.

**The incident the change name points at.** Night run 2026-11-17-a, lane L4, change `pi-neutral-paths` (bead coding-harness-xul8), continued in a second worktree `pi-neutral-paths-v2`, branch `fix/pi-neutral-paths-v2` (lane table, `docs/journal/handover/2026-11-17-night-plan-2026-11-17-a.md`). There `prepare-loop pi-neutral-paths` refused "because the loop record under `stage2/pi-neutral-paths@ee410726` is missing. Only v1's state from 2026-11-01 exists" (`docs/journal/handover/2026-11-18-night-run-2026-11-17-a.md`, lane L4). The lane parked on the maintainer question whether the maintainer-only `release-loop --restart` may be used (same handover, "Needed from the maintainer", recommendation yes; the decision itself is not recorded in the repository files read here). This change's folder was opened as follow-up bead coding-harness-e82i (`plans/INDEX.md`; commit df9ed9ba).

**Existing tests that pin the behaviour.** The per-root keying: `test_the_record_is_keyed_by_the_worktree_too` and `test_release_in_one_worktree_leaves_the_other_worktrees_record` (`tests/test_stage2.py`); triage's sibling-record guard `test_triage_records_each_supported_decision_in_the_worktree_record` plants a sibling repo's record and asserts it is untouched (`tests/test_stage2.py`). The lost-record refusals: `test_a_lost_record_stops_release_and_the_loop`, which simulates the loss by pointing `XDG_STATE_HOME` elsewhere — the "other state directory" cause, not the sibling-key cause (`tests/test_stage2.py`); `test_a_stage_retirement_over_a_lost_record_is_refused` and the restart-over-a-lost-record case in the same test. The record lock: assertions naming `stage2.record_key('demo', world.root)` in `tests/test_stage2.py` and `tests/test_stage2_availability.py`. No test covers "the record exists under another key of the same state directory" — not found in the test files searched.

## Where it lives

- Key and record primitives: `record_base`, `record_key`, `record_dir`, `lock_path`, `holding_record`, `read_record`, `write_round`, `replace_record`, `remove_loop_record` — all in `scripts/stage2.py` ("The loop record, release, and the round" section).
- Refusal sites: `lost_record_refusal` (used by `review_loop`, `release`, `retire_stage`), `triage`'s own no-record refusal, all `scripts/stage2.py`; `prepare`'s call into `lost_record_refusal` in `scripts/stage2_availability.py`.
- Same key formula duplicated outside the runner: `research_dir` in `scripts/stage2_research_store.py`; receipt path and binding in `scripts/stage2_availability.py`.
- Verbs and lock ownership at dispatch: `main`'s verb dispatch in `scripts/stage2.py` (the six record-owning verbs — repair, triage, review-loop, release-loop, prepare-loop, review — each under `holding_record`).
- Doctrine: `docs/WORKFLOW.md` §4 "the loop record" (record location, lost-record stop, restart amendment) and §3 worktree rules ("One change, one bead, one branch, one worktree, one session"; worktrees under `.claude/worktrees/<name>`, removed after merge); the runner's own docstring "The loop record"; `prompts/04b-review-loop.md` ("The rows are in the loop record, outside the worktree. Never copy them into it."); ADR 0021 (`docs/adr/0021-review-swarms-until-clean.md`, decision 9 and the restart amendment).
- History: R-2/R-3/R-14 findings in `docs/journal/handover/2026-10-20-review-swarm-runner-review.md`; merge record in `docs/journal/handover/2026-10-21-merge-day.md`; incident in `docs/journal/handover/2026-11-17-night-plan-2026-11-17-a.md` and `docs/journal/handover/2026-11-18-night-run-2026-11-17-a.md`.
- Neighbouring, undecided thread: the deep-review open question "a loop record lost for good blocks the change: `--restart` needs a completed round, so no verb continues — a recovery verb; it touches ADR 0021 decision 9" (`docs/journal/handover/2026-10-25-cloud-runner-fixes.md`, DL-A open 1). It concerns record recovery in general, not the worktree-key case specifically.
- The triage verb's archived spec defines the established wording "Active record: the change and worktree's private `loop.md`, before release" (`plans/changes/archive/2026-11-16-triage-verb/spec.md`).

## What is unclear about it

- **The bead text: not read.** coding-harness-e82i's description — the change's exact intent and class — is not readable in this worktree: `.beads/` here holds only hooks, config and metadata (glob listed no database file); the tracker is the Dolt database transported on `refs/dolt/data` (house rule 2). The same "not read" precedent is recorded in `plans/changes/archive/2026-11-06-go-access-point/research.md`. The research.md frontmatter carries no `class:` field yet; per ADR 0020 the runner reads the class from `--class` and the artifact headers, and all declarations must agree.
- **The state directory: not read.** Which record keys exist for `pi-neutral-paths` under `~/.local/state/coding-harness/stage2/`, and what v1's 2026-11-01 record contains, lies outside this worktree, which this phase must not read. The only repository evidence is the two handover sentences quoted above.
- **The v1 change folder: not found.** No `plans/changes/pi-neutral-paths/` folder and no archive entry matches it (`plans/**/*pi-neutral*` glob empty; archive spec greps for "Pi neutral" empty). Only branch names quoted in older findings (`fix/pi-neutral-paths`) and the night handovers record that lane; where its change artifacts went is an open question.
- **The maintainer's answer to L4's restart question** (handover lists the recommendation "yes", not a decision) is not on record in the files read here.
- **Whether the runner should ever look across keys at all is undecided doctrine:** the R-2 isolation and the restart amendment both treat each root's record as private, while the `lost_record_refusal` message already admits records can sit "under another state directory"; no artifact read here states what a cross-key case should do.

## Which files a change would have to touch

- `scripts/stage2.py` — the key/lookup primitives (`record_base`, `record_key`, `record_dir`, `read_record`), the refusal sites (`lost_record_refusal`, `triage`'s no-record refusal), and the verb dispatch under `holding_record`, if the cross-key case is to behave differently.
- `scripts/stage2_availability.py` — `prepare`'s lost-record path and, if receipts are concerned, `research_receipt_path`/`research_binding`.
- `scripts/stage2_research_store.py` — its duplicated key formula, which any change to the key must keep in agreement.
- Tests: `tests/test_stage2.py` (record-keying tests, lost-record tests, triage sibling test), `tests/test_stage2_availability.py` (lock assertion naming `record_key`), plus the research-store/availability tests that read `record_dir`.
- Doctrine and prompts, depending on scope: `docs/WORKFLOW.md` §4 loop-record section and §3 worktree rules; `prompts/04b-review-loop.md`; ADR 0021 if decision 9 (stops not reset) is touched — the archived DL-A note says a recovery verb touches it.

## Neighbours already known (for the `neighbours:` header)

- `plans/specs/implementation-verification/spec.md` (living spec, runner derived-file preparation — same runner, adjacent contract)
- `plans/changes/archive/2026-09-30-stage-2-codex-glm/spec.md` (the loop record's original contract, "lives outside the worktree and the git directory")
- `plans/changes/archive/2026-11-16-triage-verb/spec.md` (triage verb; "active record" definition)
- `docs/adr/0021-review-swarms-until-clean.md` (ADR, decision 9 and restart amendment)
- `docs/journal/handover/2026-10-20-review-swarm-runner-review.md` (R-2 origin), `docs/journal/handover/2026-10-21-merge-day.md` (merge of #189/#190), `docs/journal/handover/2026-11-17-night-plan-2026-11-17-a.md` and `docs/journal/handover/2026-11-18-night-run-2026-11-17-a.md` (the incident)
