---
title: "Research — appetite-stop"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-uxa9
owner: Data Architect
provenance: human-written
tags: [research]
---

# appetite stop — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-03: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 837 files, 3122 commits, 12 rules.

## Runner exploration — 2026-11-03

All facts gathered. Here is the research, ready to append to `plans/changes/appetite-stop/research.md`.

---

## What exists today

**The appetite is a written rule, not a runner behavior.** The appetite is defined in `templates/spec.md` (frontmatter comment on the `appetite:` field): "hours of phase 4, repair rounds included — a stop, not an estimate". The plan card carries it as the `Appetite:` line (`prompts/03-plan.md`, card format block: "Appetite: <time for phase 4; a stop, not an estimate>"), and a card whose appetite is larger than what `decisions.md` or `spec.md` state is a widening card that needs the maintainer's "ok" before phase 4 (`prompts/03-plan.md`, "A card widens the scope…"). `docs/adr/` contains no ADR mentioning appetite (grep over `docs/adr/`: no matches) — the rule lives only in prompts, doctrine and templates.

**The interactive rule** (`prompts/04-implement.md`, section "The appetite is a stop"): a Stage-1 session reads `date` at named moments, appends its spans under `## Time used` in `plan.md`, and "when a reading shows the time used has reached the appetite, stop once": the session extends the appetite by itself once, up to twice the card's appetite, says so in its next status message, and asks with the four-line stop block only at twice the appetite, at an open `[DECISION]`, or at a structural choice. The four answers are continue (maintainer only), cut, park, drop; "the stop comes once per appetite"; "a plan without a card has no appetite"; the phase-4 end line reads `done: <evidence> · <time used> of <appetite>`. The doctrine restates this in `docs/WORKFLOW.md` §4, "When the same mechanism returns" (bullet "By day the session stops and asks…", maintainer 2026-10-30).

**The night rule**: `docs/orchestration.md` ("The appetite"): "It is a stop, not an estimate. At night the orchestrator may answer cut, park or drop, never continue." The 2026-11-02 night plan codifies the same ("Night answers are cut, park or drop, never continue", rules §8) and the run used it as a working bound ("B repairs on until clean or its appetite", answers §6).

**The self-extension came from PR #292** (bead coding-harness-6fdk): "the appetite extends once by itself, up to twice the card's appetite (maintainer, 2026-10-30; PR #292 not merged yet)" is recorded in `docs/research/2026-10-30-night-run-plan.md` (changes §3), and `docs/research/2026-10-31-run-plan.md` ("Merged today") shows #292 merged on 2026-10-31.

**What the runner already measures.** `scripts/stage2.py` writes one measured line per completed `implement`/`repair` attempt under `## Time used`: `time_entry()` (format `<date> <start>–<end> UTC, <N> s — <verb> · attempt <n> · route <r> · model <m> · accepted|rejected · measured by the runner`), persisted by `persist_time_entry()` through `with_time_entry()`. Both verbs pass through the shared loop `run_attempts()` over a fixed route list — implement: `flash`, `flash-repair`, `stage-1` Sonnet (a single `stage-1` Sonnet on `--stage2-off`); repair: `codex`, `codex-repair`, `stage-1` Sonnet. A completed call keeps its measured entry whatever post-call check stops the run (the finalization boundary at the verdict and in the exception handler of `run_attempts`; change runner-time-line-exits, bead coding-harness-9wp); a call that never completed gets no entry. `draft` has its own loop and writes no measured entries; neither does `explore`. Both work verbs require the `## Time used` heading to exist before any call (`time_log(ctx.plan)` in `implement` and `repair`) but do **not** validate the plan card — `card_problem()`/`CARD_LABELS` run only in the draft's post-run check `verify_draft`.

**What already reads the appetite.** Exactly one consumer exists: `scripts/run_report.py` (`make report`, change run-report, bead coding-harness-o2yc) — `card_appetite_value()` lifts the `Appetite:` line via `stage2.CARD_LABELS`, `appetite_seconds()`/`APPETITE_VALUE` parse positive hours/minutes (a competing second value or unitless number is refused), and `read_time()`/`RUNNER_ENTRY` sum **only** runner-format entries; any other time record counts as `unread lines` and stays out of the subtotal (deliberate: run-report spec criterion 4, maintainer 2026-10-29, "Only that format counts"). The report warns when recorded time is at or over half the appetite (inclusive boundary, rejected time counts, the card wins over frontmatter) and says so is "advice on the snapshot, not a stop" (`run_report.py`, warning text; `docs/WORKFLOW.md` §"The run report": "It is a snapshot … **not a gate**"). Dependency direction: `run_report.py` imports `stage2` optionally; `stage2.py` never imports `run_report`, and grep for "appetite" in `scripts/` matches `run_report.py` only — the runner has no appetite reading at all today (not there).

**The gap this bead names.** `README.md` ("Written rules, not enforced by a tool"): "The appetite: `make report CHANGE=<name>` shows the time used against it; nothing stops a run at the limit yet (bead coding-harness-uxa9)." `docs/orchestration.md` (table "Stated, enforced, planned"): "The appetite stops the next attempt | kept by hand; the runner keeps trying | the runner stops itself (bead coding-harness-uxa9)."

**The bead's own direction** (quoted from the run plans; the tracker itself is a Dolt database with no rendered copy in the tree, so I could not read the bead record directly): "uxa9, the runner stops at the appetite (bead coding-harness-uxa9, **bounded**). The maintainer approved it on 2026-10-28 ('Mach das'), so it is built, not stopped at the plan card. It runs in lane A after 4tr4's draft, because it changes `scripts/stage2.py`. **The stop counts the self-extension of PR #292.**" (`docs/research/2026-10-31-run-plan.md`, queue additions).

**The stop has been missed in practice, by hand, three times recorded:** `plans/changes/architecture-reconcile/plan.md` (Time used note of 2026-10-31): appetite 2 h, about 2 h 34 min used at 19:40, further accepted repair attempts after the note — "Continuing past the stop is the maintainer's call; the structural remedy is the runner stop at the appetite (bead coding-harness-uxa9)". `plans/changes/verify-worker-cap/plan.md` ("Appetite, stated plainly"): 30151 s recorded against the appetite, much of it waiting for the shared verify slot. `docs/journal/handover/2026-11-02-five-lane-night.md` (question item 2): "continue past the appetite?" asked of the maintainer for bead wkxm.

**External research attached to the bead** (2026-11-02, model-wiki evaluation): row 5 records dsh-superagent's "Stop by impact, not by effort" against the harness's appetite-as-stop and marks it "Input for bead coding-harness-uxa9: the appetite as the point to report, impact as the point to stop — for the maintainer to weigh"; notes were added to coding-harness-uxa9 that day (`docs/research/2026-11-02-model-wiki-and-egm.md`, table row 5 and the bead list).

## What is unclear about it

- **What the runner does at the stop** — refuse before attempt 1, stop between attempts, a distinct closing message, or a `Refused`/`CallFailed` — is not found anywhere in the repository. Only the table phrasing "the appetite stops the next attempt" (`docs/orchestration.md`) exists.
- **The threshold arithmetic.** "The stop counts the self-extension of PR #292" says the self-extension is part of the runner's arithmetic, but whether the runner stops at 1× (and records the extension) or at 2× is not written.
- **What the sum counts.** The report sums runner-format entries only and leaves interactive/orchestrator spans as unread lines; whether the runner's stop reuses exactly that rule is an open question (the run-report spec's Terms define "Recorded time" both ways: criterion 4 counts only runner format, the Terms paragraph mentions "dated orchestrator records").
- **Scope of verbs.** The appetite is defined over phase 4, and only `implement`/`repair` are phase-4 verbs that write measured entries — but no artifact states explicitly that `draft`/`explore` are exempt from a runner-side stop, nor whether `--stage2-off` single-attempt runs stop at all.
- **Interaction with the review loop** (rounds until clean, ADR 0021, change loop-until-clean): how a runner-side stop in `repair` hands over to the orchestrator's cut/park/drop decision is not found.
- **Scheduling discrepancy for this change:** the 2026-10-31 run plan says uxa9 is build-approved ("not stopped at the plan card"), while the 2026-11-01 and 2026-11-02 night plans list it as "explore with GLM Flash, draft up to the plan card". Which holds now is a maintainer question.
- **The impact-vs-effort note** on the bead (2026-11-02) is recorded as input "for the maintainer to weigh" — undecided.

## Which files a change would have to touch

- `scripts/stage2.py` — the attach points that exist today: `run_attempts()` (the shared route loop where "the next attempt" begins), `implement()` and `repair()` (route lists, preflight, `closing` messages), `time_log()`/`CARD_LABELS`/`card_problem()` (the only card parsing the runner has), `persist_time_entry()` (the one-writer boundary a stop must coexist with).
- `tests/test_stage2.py` — the existing time-entry and preflight suites (`test_a_plan_without_time_used_fails_the_attempt`, `test_each_repair_retry_must_add_its_own_time_entry`, `test_runner_time_entry_identifies_attempt_and_midnight_span`, among others) are the neighborhood any stop test joins.
- `scripts/run_report.py` and `tests/test_run_report.py` — the existing appetite parser and its warning wording ("not a stop"), which a runner-side stop may invalidate or reuse.
- Rule texts that state the behavior: `prompts/04-implement.md` ("The appetite is a stop"), `docs/WORKFLOW.md` (§"The run report", §"When the same mechanism returns"), `docs/orchestration.md` (the Today/Planned row), `README.md` ("Written rules, not enforced by a tool").
- No ADR: none exists on appetite, and the bead is `bounded` (`adr_files: []` is the template norm for that class); note the night-plan standing rule that agents do not write `docs/adr/`, `AGENTS.md` or `.github/workflows/` — such text goes to the maintainer as a proposal.

## Suggested neighbours (for the header)

`plans/changes/runner-time-line/spec.md` · `plans/changes/runner-time-line-exits/spec.md` · `plans/changes/run-report/spec.md` · `plans/changes/loop-until-clean/spec.md` · `plans/changes/fail-fast-attempts/spec.md` · `plans/changes/verify-worker-cap/spec.md` · `plans/changes/architecture-reconcile/spec.md` · the living spec `plans/specs/implementation-verification/spec.md`
