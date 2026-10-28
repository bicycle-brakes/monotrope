---
title: "Research — fail-fast-attempts"
status: draft
implementation_status: none
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-5tyh
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
---

# fail fast attempts — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-28: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 713 files, 2436 commits, 12 rules.

## Runner exploration — 2026-10-28

Exploration complete. Here is the research, ready to append to `plans/changes/fail-fast-attempts/research.md`.

---

## What exists today

**The change's own state.** The folder `plans/changes/fail-fast-attempts/` holds only the skeleton `research.md` (bead `coding-harness-5tyh`, `implementation_status: none`, frontmatter dated 2026-10-27, runner log line of 2026-10-28). Its header carries **no `class:` field**. The runner log says `route flash`, which per `explore()` in `scripts/stage2.py` (`SWARM_CLASSES`/`declared_class`, the class check at the top of `explore`) means Stage 2 was on and the class was declared `bounded` or `spike` through the `--class` argument — `declared_class` refuses when no statement is present, so an argument must have been given. Which of the two, and the bead's description (which names its class per the AGENTS.md rule of 2026-10-22), are **not readable from this tree**: the tracker is the Dolt database under `.beads/` and no rendered copy is committed (`.beads/metadata.json`, AGENTS.md house rule 2); `.beads/interactions.jsonl` holds only two stale 2026-09-16 rows. I did not read the bead.

**"Fail fast" appears in the tree in three unrelated senses.** A case-insensitive search for `fail[-_ ]?fast` finds ten files, all cited below; nothing in `plans/` treats fail-fast attempts as its own subject yet.

1. **The work verbs' attempt ladders** (`scripts/stage2.py`). One shared loop (`for attempt, (endpoint, credential, route, reason) in enumerate(routes, 1)`) runs each verb's route list. `implement` defines flash → flash-repair ("first Flash post-run check failed") → stage-1 Sonnet ("two Flash post-run checks failed"), with a single Sonnet route under `--stage2-off`; `draft` defines codex → codex-repair → glm ("two Codex draft attempts failed", ADR 0016); `repair` defines codex → codex-repair → stage-1 Sonnet ("two Codex post-run checks failed", ADR 0017, "No route reads the GLM credential"). What **advances** the ladder is only a post-run-check failure (`verify_attempt` problems, `answer_check`): the attempt's block is appended to `findings.md` (`attempt_block`, `attempt_files`, bounds `ATTEMPT_FILES = 40` and `QUOTE_LINE_CHARS = 500`), inputs are restored, the next route starts. What **stops the run outright** is: a failed model call including an empty Codex answer (`CallFailed` raised after recovery — the attempt is saved under `refs/stage2/attempts/` by `save_attempt`, answers kept by `save_answer_evidence` in the git directory, baseline restored); a Codex attempt that moved HEAD; a failed answer-evidence write; `cannot_start` ("`make verify` could not be run … no further attempt"); and a leaked credential (`Refused` — docs/WORKFLOW.md: "A leak refusal always stops the call; it never selects the fallback"). The per-attempt time entry flags `retry=bool(problems) and attempt < len(routes) and cannot_start is None and not exposed`. Closing failures: "implementation post-run checks failed after the allowed attempts…" (implement), "the draft failed after the allowed attempts…" (draft), "repair post-run checks failed after the allowed attempts…" (repair). Five tests pin this chain (`tests/test_stage2.py`): `test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics`, `test_sonnet_fallback_starts_with_both_diagnostics_when_both_flash_attempts_deleted_the_heading`, `test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason`, `test_a_leak_between_work_attempts_stops_before_fallback`, `test_a_key_in_the_gate_output_never_reaches_the_next_attempt`. The living spec `plans/specs/implementation-verification/spec.md` fixes the derived-file preparation that runs before *every* attempt, "including retries".

2. **The review loop's member failures** (`scripts/stage2.py`, `run_swarm` and the round assembly). A `MalformedAnswer` (no six-cell row, not exactly "No finding.") is retried exactly once per member with the format reminder (`ask_malformed_again`), inside the round's single deadline `REVIEWER_MINUTES = 45` (raised from 30 on 2026-10-24). In the paid-swarm stage a still-failing member is **replaced**, not refused: the cheapest admitted, unconsumed ladder rung, each model at most once (Q-13); a refused rung is passed over unconsumed (DL-B-1); a replacement that cannot start inside the deadline is `NotStarted` and unconsumed (DL-B-10). In the free stage, all members rate-limited raises `FreeStageUnavailable` — the active change `free-member-rate-limit` (partial) makes that drop the stage and continue, while a mixed failure class still fails the round ("writes nothing and consumes no more stages", spec criterion 2). No member succeeded at all raises `CallFailed` naming each failure. A failed round writes no round; the marker "Loop attempt: \<date\> — no round was written" accounts only for that attempt's calls (`NO_ROUND_KEY`/`NO_ROUND_LINE`, DL-A-6). Stage order and exits are fixed by ADR 0021 and docs/WORKFLOW.md (`review-loop`: exit 0 round written, 2 refusal, 3 clean round); `release-loop --stage-failed` retires a stage without a round and the loop continues; `--restart` is maintainer-only.

3. **The research swarm's staging doctrine** (`plans/changes/research-swarm/design.md`, "Queue → invocation"): "Fail fast between preparatory stages: a failed finder, map or sentence (including filter rejection, exit 1) prevents every later stage. Within the topic stage ordinary failures allow siblings to finish; call the judge only if every required topic report is valid… No failure spends an extra call or retries." Budget frozen at `39 + 3N`. In code, `Run.gate` (`scripts/stage2_research_run.py`) validates the declaration, terms and leak check per call and refuses before a launch; the known open finding F6-3 (PR #258, handover `docs/journal/handover/2026-10-27-night-run.md`) says `Run.gate` and the probes in `scripts/stage2_availability.py` admit a paid model **without rechecking its terms date**. The single-explorer route (this change's route) makes exactly one call with the attempt hardcoded to 1, runs no post-run check, has no retry, and refuses to append an answer that names no repository file (bead coding-harness-e7m).

**Two smaller attempt sites.** `scripts/stage2_session.py`: each session launch gets an attempt id; its audit line goes "pending." → "accepted"/"failed (…)" (`finalize`); "a failed attempt removes it [the credential], an accepted one keeps it". CI: `strategy: fail-fast: false` in `.github/workflows/ci.yml` (gates job) and in the generated matrix job (`scripts/ci_gates.py`, "a red leg must not cancel the other", reason bead coding-harness-bl2) — fail-fast is deliberately *off* there. `scripts/stage2_runs.py` counts attempts from the runner's own line constants.

## Where it lives

`scripts/stage2.py` (route lists and the shared loop; `attempt_block`/`attempt_files`; `MalformedAnswer`, `NotStarted`, `CheckpointRolledBack`, `FreeStageUnavailable`; `run_swarm`/`ask_malformed_again`; `explore`, `declared_class`, `CLASSES`/`SWARM_CLASSES`, `REVIEWER_MINUTES`), `scripts/stage2_session.py`, `scripts/stage2_research_run.py`, `scripts/stage2_availability.py`, `scripts/stage2_runs.py`, `tests/test_stage2.py`, `.github/workflows/ci.yml`, `scripts/ci_gates.py`; doctrine in `docs/WORKFLOW.md` (routing table, ADR 0016/0017/0020/0021 summaries) and `docs/adr/`.

## What is unclear

- **The change's objective and class.** The bead description and class are in the tracker only; not read. The name fits at least three existing behaviours (work-ladder retries, loop retry-then-replace, swarm staging), and "fail fast" is already an in-tree term of art in two of them — the interview must state which one this change means.
- **The header has no `class:` field** even though `declared_class` reads one from `research.md`; the declaration currently lives only in the runner invocation.
- **Open decisions that constrain any attempt-ladder work:** the parked PRs #235/#236/#238 (`docs/research/2026-10-27-parked-runner-prs.md`) leave "refuse against replace" for unreadable member answers explicitly to the maintainer; the mixed-failure free-stage case moved to bead coding-harness-pj98 with an ADR 0021 amendment and its own interview.
- **Not found** (searched, absent): any existing artifact naming fail-fast attempts as its subject. **Not read**: the Dolt tracker, PR #258's branch contents, the parked PR branches (outside this worktree).

## Which files a change would have to touch

By sense: work ladders → `scripts/stage2.py` (route lists, shared loop, closing messages, time-entry retry flag) + `tests/test_stage2.py` (the five retry-chain tests are pinned text per `attempt-diagnostics` criterion 16) + `docs/WORKFLOW.md` routing; loop → `run_swarm`/round assembly + loop tests + ADR 0021 amendment if stage semantics move; swarm → `scripts/stage2_research_run.py`/`stage2_swarm.py`/`stage2_availability.py`; session → `scripts/stage2_session.py` + its tests.

**Neighbours for the header:** `plans/changes/attempt-diagnostics/` (cit, partial), `plans/changes/free-member-rate-limit/` (pj98, partial), `plans/changes/failed-check-spans/` and `failed-check-secrets/` (8hr), `plans/changes/research-swarm/` (icw), `plans/changes/terms-expiry/` (abra, PR #258), `plans/changes/stage2-session/` (amp), `plans/changes/codex-drafts/` (rhq), `plans/specs/implementation-verification/spec.md`, archived `plans/changes/archive/2026-10-07-stage2-flash-runner/`.

## Orchestrator addendum — 2026-10-28

The explorer could not read the tracker, so it names the objective and the
class as unread. Both are in the bead (coding-harness-5tyh, read through
`tools/bd show` on 2026-10-28): class `bounded`, runner behaviour inside the
existing phases, no ADR. The objective is the first sense the exploration
lists, the work verbs' attempt ladders (`implement`, `repair`), not the
review loop or the research swarm.

The bead records the measurement behind it (2026-10-27, three parallel
lanes): every first GLM Flash implement attempt failed, and each cost 40–55
minutes because every attempt ends in the full `make verify` (15–24 minutes
under that load). In one lane, attempt 1 (2952 s) failed on ruff findings
the runner had already detected before `make verify`, plus the test the
plan card's pre-mortem had named; attempt 2 (1465 s) was rejected whole
because it edited `findings.md`. All three plans passed their appetite on
failed attempts. The maintainer approved one package of three levers on
2026-10-27:

1. Cheap checks first: after an attempt, ruff and the tests of the changed
   files run before `make verify`; red there ends the attempt and hands
   exactly that output to the next one.
2. The plan's pre-mortem tests as a must-run: the implement and repair
   prompts tell the model to run them, and ruff, before handing back
   (`prompts/04-implement.md` has no such instruction, grep 2026-10-27).
3. Protected files restored: an attempt's edit to a runner-owned file
   (`findings.md` outside its bookkeeping) is put back, as the draft verb
   already does, and the rest of the attempt is checked; the repair prompt
   names `findings.md` as runner-owned.

