---
title: "Research — codex-capacity-retry"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-m98e
owner: Data Architect
provenance: human-written
tags: [research]
---

# codex capacity retry — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-07: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 922 files, 3560 commits, 12 rules.

## Runner exploration — 2026-11-07

The exploration is complete. Here is the phase-1 research for `codex-capacity-retry`, written as prose ready to append to `plans/changes/codex-capacity-retry/research.md` (below the existing stage-2 call line). A `neighbours:` proposal for the header follows at the end.

---

## What exists today

**The manual doctrine this change automates.** `docs/WORKFLOW.md`, section "Night runs" (the section starting at the heading "### Night runs", around line 1702): "Codex at capacity: wait four minutes and retry once. If the retry fails too, Sonnet 5.5 takes that one step — a repair through `stage2.py repair <change> --stage2-off "<reason>"`, a phase-6 review or re-check through a read-only Sonnet 5.5 sub-agent whose rows the orchestrator records unchanged. The step carries a note with the reason, and the run continues. **The runner automates this once bead coding-harness-m98e lands.**" The same rule appears in three night plans: `docs/research/2026-10-26-night-run-plan.md` (answer 1, replacing the 2026-10-25 stop rule "when Codex does not start, stop", which `docs/research/2026-10-25-night-run-plan.md` line 112 still states), `docs/research/2026-10-28-night-run-plan.md` and `docs/research/2026-10-30-night-run-plan.md`. The bead is described there as "detect Codex at capacity and fall back; its interview is done" and "m98e ends in a decision pull request, because it amends ADR 0017" (`docs/research/2026-10-26-night-run-plan.md`, answer 3). A live instance shows the cost: lane B's round-4 repair failed on the night of 2026-11-02 with "Codex at capacity, Sonnet left 2 tests red, Codex retry stopped by the disk" (`docs/journal/handover/2026-11-02-five-lane-night.md`, lane table). The bead was still "not started" after the 2026-10-27 night (`docs/journal/handover/2026-10-27-night-run.md`, "Not started from the night plan"); no later handover mentions it.

**How each runner verb behaves on a dead Codex call today.** The verbs live in `scripts/stage2.py` (`VERBS`, in `main`). Behavior differs by verb:

- `repair`: the route ladder is `codex` → `codex-repair` (reason "first Codex post-run check failed") → `stage-1`/Sonnet (reason "two Codex post-run checks failed") in the `routes` list inside `repair`. It advances only on *post-run check failures*. A call that itself fails is caught in `run_attempts` (the shared attempt loop; the `call_error is not None` branch) and re-raised as `CallFailed` after baseline restore and attempt save — the whole run stops; no further route starts. This is pinned by `plans/changes/codex-repairs/spec.md` criterion 6: "If a repair model call fails, the run stops without another model call or a runner checkpoint. *Refuted by:* automatic fallback after an unavailable Codex call…". Tests pin the ladder labels and reasons (`tests/test_stage2.py`, the assertions naming "route codex-repair", "reason first Codex post-run check failed" and "reason two Codex post-run checks failed").
- `implement`: same shared `run_attempts` loop, routes Flash → Flash-repair → Sonnet stage-1; the same dead-call stop applies.
- `draft`: the opposite — a hand-written loop where a failed call does *not* stop the run. It saves the attempt, puts the tree back, appends a quoted block "Attempt N (route) failed its call" and `continue`s to the next route (second Codex attempt labeled `codex-repair`, then GLM 5.3) (`draft` loop; `plans/changes/codex-drafts/spec.md` criterion 20 and its `[DETAIL]` note stating a failed call is one of the failure kinds that moves along the same ladder). Tests: `test_a_failed_draft_call_is_put_back_and_recorded` and its companion in `tests/test_stage2.py`.
- `review` (phase 6): a single Codex call (`run_codex`, verb `review`), no route ladder at all; a failed call raises `CallFailed` and stops (`review`).

**Existing capacity detection precedent — review loop only.** The runner already classifies rate-limit failures for free review-swarm members: the `_RATE_LIMITED` regex (429 / "rate limit" / "too many requests" / "unavailable" spellings), the `rate_limited()` predicate (only a failed exit that is not `StepTimedOut` and starts `pi call failed: exit `), the `FreeStageUnavailable` exception (bead coding-harness-pj98) raised when *every* member of a free round failed that way, and the handler that marks the free stage skipped and lets the next stage take the round (with a refusal when no paid stage is left). The failure text these match is built by `fail()`, which appends the last stderr line of the dead process to the message. `plans/changes/free-member-rate-limit/spec.md` (class bounded, header `implementation_status: partial`) pins this and names its non-goals: "Retrying a rate-limited member, or treating a paid member's 429 any differently than today" — the paid Codex side was explicitly left out there. Tests: the rate-limited-round tests and the `rate_limited` message table in `tests/test_stage2.py` (including the false positives it must not match: a request id containing "429", an empty answer with a 429 warning, time-outs). The predicate is applied only to Pi review-loop outcomes today; nothing applies it to Codex (`run_codex`) or to draft/implement/repair outcomes.

**No wait or backoff exists on the call path.** A search for `time.sleep` in `scripts/stage2.py` finds no match — there is no existing wait to build on. The only retry-adjacent timing constants are the availability probes' limits (`PROBE_SECONDS`/`PROBE_RETRY_SECONDS` and the doubled free variants in `scripts/stage2_availability.py`), which belong to the pre-swarm probes, not to the work verbs; `PROBE_SECONDS` is assigned twice in that module (once near the top, once beside the retry constants).

**`--stage2-off`, the fallback the doctrine names.** `repair` and `implement` accept `--stage2-off <reason>` and route to Sonnet alone with the reason carried in the route block ("Stage-1 route: … · reason: …", written by `insert_before_time` beside the plan's time heading) and the audit line. `review` (phase 6) has no such parameter — its signature takes only root and change — so the doctrine's "phase-6 review or re-check through a read-only Sonnet 5.5 sub-agent" is an orchestrator-side action outside the runner today. The `--stage2-off` verb coverage is documented in `docs/WORKFLOW.md` §4.

**ADR 0017 is the decision an amendment must speak to.** `docs/adr/0017-codex-repairs-taken-findings.md` (accepted 2026-10-13): option "Automatic fallback on Codex call failure" was rejected in Q-4 because it "hides an availability-driven budget switch"; decision 2 states "When Codex is unavailable, the orchestrator deliberately starts `--stage2-off <reason>`"; Consequences: "A dead Codex call needs an explicit retry or Stage-1 restart. It does not consume the post-check fallback without the orchestrator's choice." The night plan already says m98e ends in a decision pull request amending this ADR.

**Package context of the branch.** The change folder was opened by commit d5d8baff as a package with coding-harness-jmtl and coding-harness-y125. jmtl is the `stage2.cut_rounds` ValueError (strict `zip`) on a loop record with no round headings — recorded in `docs/journal/handover/2026-10-25-cloud-runner-fixes.md` and confirmed still open on main in `docs/journal/handover/2026-11-02-five-lane-night.md`; the code stands unchanged on this branch (`cut_rounds` in `scripts/stage2.py`: with an empty round-heading list, `ends` holds one element against zero `heads`, so `zip(..., strict=True)` raises). y125: not found anywhere in tracked files — its subject is tracker-only and was not read.

## Where it lives

Doctrine: `docs/WORKFLOW.md` "Night runs"; night plans `docs/research/2026-10-26|28|30-night-run-plan.md`. Runner: `scripts/stage2.py` — route lists in `repair` and `implement`, the shared loop `run_attempts` (dead-call stop), the `draft` loop (dead-call advance), `review` (single call), the classifier precedent `_RATE_LIMITED`/`rate_limited`/`FreeStageUnavailable` and its handler. Probes: `scripts/stage2_availability.py`. Declaration: `model-endpoints.yaml` (entry `openai-codex`, with the 2026-09-30 terms remark in its comment block). Specs: `plans/changes/codex-repairs/spec.md` (criterion 6), `plans/changes/codex-drafts/spec.md` (criterion 20), `plans/changes/free-member-rate-limit/spec.md`. ADR: `docs/adr/0017-codex-repairs-taken-findings.md`. Tests: `tests/test_stage2.py` (ladder reasons, draft dead-call, rate-limit table).

## What is unclear about it

1. The m98e interview answers are not in the repository — the change folder holds only `research.md` (folder listing), while the 2026-10-26 night plan says "its interview is done"; they presumably live in the bead's tracker notes, and the tracker (Dolt database under `.beads/`) was not read here.
2. What a Codex capacity failure looks like on this machine (exit code and stderr wording of `codex exec`) is not recorded anywhere in the repository. That is "not found" — no sample was recorded; it is distinct from "not there", for the Pi wording is recorded and pinned by tests, and nothing pins the Codex CLI's wording.
3. Bead coding-harness-y125's subject is unknown from tracked files (repository-wide search: no matches; only the opening commit message names it).
4. The doctrine names repair and phase-6 review/re-check, never `draft` — whether the four-minute wait is meant where the draft ladder already advances on a dead call is unstated in every artifact read.
5. `plans/changes/codex-repairs/spec.md`'s frontmatter says `implementation_status: none` (and `plans/INDEX.md` mirrors it, dated 2026-10-13), while the repair route ladder and its tests exist on this branch. Whether that header is stale was not verified.
6. How a wait plus one retry interacts with the runner's time accounting is unstated: `run_attempts` gives a call that never completed no time entry, and whether a wait-plus-retry is one attempt or two audit lines is written nowhere read.
7. Whether phase-6 `review` gains a runner-side fallback or stays an orchestrator-side Sonnet action is not stated by the doctrine; the runner has no `--stage2-off` parameter for `review` today.

## Which files a change would have to touch

`scripts/stage2.py` (route lists in `repair` and `implement`, the dead-call branch of `run_attempts`, the `draft` loop, `review`, and the classifier precedent beside `_RATE_LIMITED`/`rate_limited`); `tests/test_stage2.py` (the ladder-reason, dead-call and rate-limit tests named above); `docs/WORKFLOW.md` ("Night runs", including the sentence that names this bead, and the §4 `--stage2-off` verb descriptions); `docs/adr/0017-codex-repairs-taken-findings.md` (the amendment; Q-4, decision 2 and the Consequences sentence are the passages that constrain automation today); `plans/changes/codex-repairs/spec.md` (criterion 6, subject to unclear item 5); `plans/INDEX.md` regenerates through `scripts/plans_registry.py --index` after frontmatter edits.

**Proposed `neighbours:` header** (specs of active/archived changes that speak to this topic):

- `plans/changes/codex-repairs/spec.md` (bead coding-harness-0ga — the repair route and its dead-call criterion)
- `plans/changes/codex-drafts/spec.md` (bead coding-harness-rhq — the draft route ladder and criterion 20)
- `plans/changes/free-member-rate-limit/spec.md` (bead coding-harness-pj98 — the rate-limit classifier and its non-goals)
- `plans/changes/loop-until-clean/spec.md` (bead of ADR 0021 — the stage ladder the free-stage drop rides on)
- `plans/changes/fail-fast-attempts/spec.md` (attempt/failure semantics of the work verbs)
