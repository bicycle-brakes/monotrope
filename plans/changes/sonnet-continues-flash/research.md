---
title: "Research — sonnet-continues-flash"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-6ie
owner: Data Architect
provenance: human-written
tags: [research]
---

# sonnet continues flash — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 788 files, 2844 commits, 12 rules.

## Runner exploration — 2026-10-31

Research complete. The prose below is ready to append to `plans/changes/sonnet-continues-flash/research.md`.

---

## What exists today

**The change's stated intent, as the tree carries it.** The folder `plans/changes/sonnet-continues-flash/` holds only the skeleton `research.md` (frontmatter `bead: coding-harness-6ie`, the note "this file is empty until it has run", and the stage-2 call line of 2026-10-31, route flash); no spec, plan or decisions exist yet. Outside the folder the change name appears only in `plans/INDEX.md` (row for `changes/sonnet-continues-flash/research.md`, draft, implementation none, 2026-10-31, coding-harness-6ie). The bead's description and its open question live in the Dolt tracker, which no rendered copy accompanies (AGENTS.md house rule 2) — I did not read the bead. The intent is stated in dated plans instead: `docs/research/2026-10-26-night-run-plan.md` item 8.3 reads "the Sonnet fallback must continue from Flash's edits, and a Flash call error must not wipe them", and `docs/research/2026-10-28-night-run-plan.md` Lane A item 4 repeats it; the 2026-10-26 plan's item 8 preamble counts it among "runner faults that cost the day session whole attempts". The 2026-10-21 plan (`docs/research/2026-10-21-night-run-plan.md:184-187`) paraphrases the bead title as "the Sonnet fallback that loses Flash's edits" and moved it to the interview queue because it "overlaps with writing-attempt isolation (`coding-harness-s9r`) and preserved failed work (`coding-harness-znc`)". Both night-run plans name the class: **bounded**. The research.md frontmatter carries no `class:` field (read directly); which declaration this explore's invocation used is not visible in the tree — the call line records only "route flash".

**The implement attempt ladder.** `scripts/stage2.py` defines the endpoints as tuples (`GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")`, `SONNET = ("claude-code-plan", "claude-sonnet-5-5", "medium")`, `scripts/stage2.py:186-190`). `implement` (`scripts/stage2.py:7296-7300`, function at 7283) runs three routes through the shared loop `run_attempts` (`scripts/stage2.py:6762`): `flash` → `flash-repair` (reason "first Flash post-run check failed") → `stage-1` Sonnet (reason "two Flash post-run checks failed"); with `--stage2-off` a single Sonnet route runs (7303).

**What advances the ladder, what stops it.** Only a failed post-run check or answer check advances to the next route: the runner appends the attempt's quoted block to `findings.md`, restores the snapshotted prompt inputs and the plan, and starts the next route — the attempt's code edits stay in the worktree ("Failed edits stay in the attempt's evidence", `scripts/stage2.py:7233-7243`), and the next prompt carries "## Earlier post-run diagnostics" (71842-6849 region, assembly at `scripts/stage2.py:6842-6849`). A **failed call** (`CallFailed` — quota, network, empty answer) does neither: the call boundary captures it (6909-6910), then the recovery branch (`scripts/stage2.py:7000-7021`) runs `plan_baseline_restore`, `put_findings_back`, `save_attempt`, `restore_baseline` — the tree is rolled back to the baseline — and raises; the loop's `except BaseException` re-raises (7244-7279), so **no later route starts**. The failed call also gets no measured time entry ("a call that never completed … gets no entry", docstring `scripts/stage2.py:6802-6810`). What survives is evidence only: the partial answer under `save_answer_evidence` (`scripts/stage2.py:4266`, git-directory `stage2/attempts/<change>/`) and the file snapshot under `refs/stage2/attempts/` (`save_attempt`, `scripts/stage2.py:4187`, whose docstring cites bead coding-harness-znc: "a run that hits a spent budget after hours of edits still holds them").

**The doctrine sentences pinning this.** Implement: "a failed post-check gets one fresh Flash repair, then one Sonnet 5.5 fallback … A failed model process stops instead of silently changing route" (`docs/WORKFLOW.md:1139-1141`). Repair: "a failed call stops the run without a fallback" (`docs/WORKFLOW.md:1536`; `repair` docstring `scripts/stage2.py:7692-7694`, ADR 0017). Explore: a single call per run (`scripts/stage2.py:6445-6497`), `writable=False`, no chain, no snapshot on failure; swarm classes route to `stage2_swarm.run` instead (6454-6465).

**The draft precedent — the asymmetry the change addresses.** `draft` runs its own loop and, on a call error, saves the attempt, puts the tree back, records the diagnostics and `continue`s to the next route (`scripts/stage2.py:7587-7596`); its doctrine reads "a failed call is put back and moves along the same chain, a failed post-run check leaves its tree and its quoted block, and three failures exit 1" (`docs/WORKFLOW.md:1225-1228`). Note the nuance: even draft does not hand the failed attempt's edits to the next route — it restores the tree (`put_back(root, baseline, allowed)`, 7589) and what carries over is the diagnostics text. For the *failed-check* path, by contrast, draft states "The next attempt starts on the tree this one left" (`scripts/stage2.py:7622-7623`), and implement behaves the same.

**Tests pinning today's behavior** (`tests/test_stage2.py` unless noted): `test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics` (1844), `test_sonnet_fallback_starts_with_both_diagnostics_when_both_flash_attempts_deleted_the_heading` (2534), `test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason` (2560), `test_a_leak_between_work_attempts_stops_before_fallback` (2577), `test_a_key_in_the_gate_output_never_reaches_the_next_attempt` (2738), `test_a_leak_before_a_draft_attempt_stops_the_chain` (3477 — pins that a `Refused` is never caught as a failed call, so a credential refusal must not fall through), `test_repair_retains_each_attempt_answer` (10937; its comment at 10969 pins "a failed call keeps the output it returned … nothing is retried after it"). The cheap-check and findings-restore contracts around the ladder are pinned across `tests/test_stage2_fail_fast.py` (ledger tests 1–10 and rows L1–L8).

## Where it lives

`scripts/stage2.py` — route lists (`implement` 7296-7303, `draft` 7539-7543, `repair` 7729-7735), the shared loop `run_attempts` (6762, call-error branch 7000-7021, re-raise 7244-7279), the recovery primitives `save_attempt` (4187), `plan_baseline_restore` (4242), `restore_baseline` (4318), `save_answer_evidence` (4266), the endpoint constants (186-197). Doctrine: `docs/WORKFLOW.md` §4 (1139-1141 implement, 1225-1230 draft, 1534-1537 repair). Tests: `tests/test_stage2.py`, `tests/test_stage2_fail_fast.py`. The implement prompt's header (`prompts/04-implement.md:3-8`) describes the ladder and the leak-stop but says nothing about the call-error stop — no prompt text describes it (not found).

## Incident history and neighbours

- The open question as recorded: "coding-harness-6ie with coding-harness-s9r (attempts keep the earlier attempt's edits; isolated attempts): one shared design; open question whether a failed GLM call falls through to Sonnet 5.5 instead of reverting" (`docs/journal/handover/2026-10-15-night-run-fifth.md:90-92`). A 2026-10-25 handover adds that 6ie (with 83e) "each hold an open question in their bead text, so they were left for the maintainer" (`docs/journal/handover/2026-10-25-cloud-runner-fixes.md:167-168`) — the question's exact wording is unreadable from this tree.
- 6ie stood among the nine P1 "Stage 2 that can be trusted" beads, "the largest open risk bundle in the tracker" (`docs/journal/handover/2026-10-19-optimization-exploration.md:112-118`); the bead ranking of 2026-10-19 groups it as "the lost-attempt group (s9r, znc, 6ie, b5w)" (`docs/journal/handover/2026-10-20-night-run-ninth.md:102-104`).
- Two of the group are delivered: znc's preservation is `save_attempt` (pinned at `tests/test_stage2.py:2215`, 2249, 4106); b5w is the merged change `plans/changes/tolerate-derived-leftovers/` (merged as #243 per `docs/journal/handover/2026-10-25-cloud-runner-fixes.md:57`). s9r is the structural, feature-class neighbour: "Isolate each writing attempt (closes znc, 6ie, b5w as one class)", container choice open since 2026-10-15 (`docs/research/2026-10-24-weekend-run-plan.md:103`, three isolation levels at 120-125), with partial work pushed on `explore/isolated-attempts` (`docs/journal/handover/2026-10-15-night-run-fourth.md:42`).
- In-flight neighbour sharing the mechanism map: `fail-fast-attempts` (coding-harness-5tyh, branch `fix/fail-fast-attempts`, parked mid-implement — "the last Sonnet attempt was stopped for low memory", `docs/research/2026-10-28-night-run-plan.md:31`); its `research.md` §"What exists today" item 1 (`plans/changes/fail-fast-attempts/research.md:44`) describes the same advance/stop split and names the same pinning tests.
- A live example of the ladder working as designed (failed *checks*, not a failed call): the stage2-mimo implement of 2026-10-07/08 ran all three routes, each rejected by post-run checks, and left the work uncommitted (`docs/journal/handover/2026-10-08-stage2-mimo-implement-failed-takeover.md:35-41`).

## What is unclear

- The bead text's own open question is not readable here (tracker is the Dolt store; `docs/journal/handover/2026-10-25-cloud-runner-fixes.md:167-168`); the interview must restate it from the maintainer.
- **Scope: implement only, or repair too.** ADR 0017 explicitly decided "a failed call stops the run without a fallback" for repair (`docs/WORKFLOW.md:1536`, `repair` docstring `scripts/stage2.py:7692-7694`); the night-run plans name only Flash→Sonnet, i.e. `implement`. Extending the fall-through to repair revisits a decided ADR — the maintainer's call, not derivable from the tree.
- **What "continue from Flash's edits" means on a call error.** Two readings stand in the sources: the 2026-10-15 handover asks whether a failed GLM call "falls through to Sonnet 5.5 instead of reverting"; the 2026-10-26/28 plans say the fallback "continues from Flash's edits" and the call error "must not wipe them". Today even the fall-through verb (`draft`) puts the tree back before the next route and carries only diagnostics (`scripts/stage2.py:7587-7596`), so "continue from the edits" as a kept dirty tree exists today for no verb on the call-error path. This is the design core; undecided here.
- **Relationship to s9r.** The 2026-10-21 plan queued 6ie into the interview precisely because of the overlap with writing-attempt isolation and preserved failed work (184-187); the weekend plan has s9r closing 6ie as one class, yet the 2026-10-26/28 plans queue 6ie as its own bounded change. Whether s9r stays open after a bounded 6ie lands is not stated anywhere in the tree.
- The class declaration for this change: frontmatter of `research.md` has no `class:` field; the plans say bounded; the invocation's `--class` argument is not recorded in the tree. Not contradictory, but unstated in the artifact.
- Explore is named nowhere in the bead's phrasing and makes no edits (`writable=False`), so it reads as out of scope — not there, not merely not found.

## Which files a change would have to touch

- `scripts/stage2.py` — the call-error branch of `run_attempts` (`scripts/stage2.py:7000-7021`) and the loop's stop semantics (7244-7279); possibly the `implement` route reasons (7296-7300) if the reason strings change; `save_attempt` / `plan_baseline_restore` / `restore_baseline` (4187, 4242, 4318) are the primitives the behavior is written from.
- `tests/test_stage2.py` — the pinning tests listed above would need to state the new contract; `tests/test_stage2_fail_fast.py` if the diagnostics or findings-restore contracts around the ladder move.
- `docs/WORKFLOW.md` — the implement doctrine sentence (1139-1141); the repair sentence (1534-1537) only if repair joins the scope, which would be an ADR 0017 amendment for the maintainer.
- `prompts/04-implement.md` — likely untouched: no prompt text describes the call-error stop today (not found), and the behavior is the runner's.
- `plans/INDEX.md` — regenerated as the change's artifacts appear.
