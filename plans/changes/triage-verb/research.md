---
title: "Research — triage-verb"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-o2s1
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3-flash, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# triage verb — Research

Stage-2 call, 2026-11-07: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 922 files, 3562 commits, 12 rules.

## Runner exploration — 2026-11-07

Here is the phase-1 research for `triage-verb`, as repository facts ready to append to `plans/changes/triage-verb/research.md`.

---

## What exists today

**The word "triage" names no verb in the runner.** The runner's verb set (`scripts/stage2.py`, the `VERBS` dict beside `main`, and the `main` argparse choices) is: `explore`, `draft`, `implement`, `repair`, `spec-review`, `review-loop`, `release-loop`, `review`, `probe`, `prepare-loop`, plus the hidden `session` and `prepare-explore`. A grep for `triage` over `scripts/` finds the word nowhere in `scripts/stage2.py`; the only hits are comments about a different, older triage (`scripts/ramp_valves.py`, "2ee triage 2026-09-19"; `scripts/kit/probe.py`, same remark).

**Triage — deciding a review row's Status — is the orchestrator's manual act.** `docs/WORKFLOW.md` §4, "The review loop (phase 4b)": "The orchestrator writes beside each row its `Status` — `taken — <test or criterion>`, `taken — not a test — <reason>` for a finding no test can show, or `rejected — <reason>` — and, for a taken row, `Broke a test`." The repair section opens with the division of labour: "**The orchestrator decides, the verb repairs, the reviewer re-checks.**" — `repair` takes only decided rows and "refuses while a row stands undecided". A row left undecided holds the next round and the release.

**The step-by-step triage procedure lives in the loop prompt**, not only in WORKFLOW.md: `prompts/04b-review-loop.md`, "For the orchestrator", steps 1–4 — (1) write each row's Status under the evidence rule, (2) hand the taken rows to `python3 scripts/stage2.py repair <change>`, (3) write `Broke a test` from the run's evidence for each fixed row, (4) release with `release-loop` after the phase-6 verdict. The evidence rule ("a finding is taken only when a test demonstrates it or the spec supports it; otherwise it is rejected with its reason") is stated in `docs/WORKFLOW.md` §2 "The findings process", §4, and `prompts/04b-review-loop.md`; a duplicate finding is rejected explicitly, one row per member, never deleted.

**The Status vocabulary a triage writes is fixed in the template and the refusal.** `templates/findings.md`, the reference section, lists the stage-2 statuses: `taken — <reason>`, `taken — not a test — <reason>`, `taken — guard test — <reason>`, `fixed — tests/<path>::<function>`, `fixed — not a test — <reason>`, `fixed — guard test — tests/<path>::<function>`, `rejected — <reason>`, with loop rows also reading `taken — <test or criterion>`; `Broke a test` carries `yes`, `no`, `yes — guard test — tests/<path>::<function>`. The runner's refusal names the same values verbatim (`scripts/stage2.py`, `undecided_refusal`; the comment credits bead coding-harness-ll5). The column sets are the constants `ROW_COLUMNS` and `RELEASED_COLUMNS` in `scripts/stage2.py` (`… | Reviewer | Status | Broke a test`, released rows add `Phase 6`).

**The runner already reads triage state mechanically.** In `scripts/stage2.py`: `undecided()` decides a row when its Status starts `rejected`, or starts `taken`/`fixed` with a filled `Broke a test` mark; `accepted_row()` treats `taken` and `fixed` as accepted (a fixed row keeps its round not clean, criterion 11, ADR 0017 decision 6 / ADR 0021 decision 7); `clean_round()` ends the loop only when every row of a round is decided and none accepted (ADR 0021, decision 1). `undecided_refusal` is called before the repair (`repair`, "decide them first"), before a release ("nothing is released"), and at the review-loop stops ("decide them first"). Independently, `scripts/stage2_runs.py` counts "Loop rows: taken / rejected / undecided" per change from `findings.md`, reading statuses through the runner's own constants so counter and writer cannot drift (its docstring; bead coding-harness-kw0).

**Two triage decisions are reserved, one to the orchestrator alone, one to the maintainer.** Guard-test authorisation: only the orchestrator may write `taken — guard test — <reason>`, and only with a nonempty unquoted reason (`docs/WORKFLOW.md` §4, "Guard test", ADR 0023; `prompts/04b-review-loop.md` step 1). Mechanism escalation: "The second finding of one mechanism ends case-by-case repair" — the orchestrator then proposes a structural remedy and the maintainer chooses (`docs/WORKFLOW.md` §4, "When the same mechanism returns", bead coding-harness-7av1); at night the rule is record, park, continue (`docs/WORKFLOW.md` §4, "Night runs", bead coding-harness-yuw.4). The AGENTS.md rule "Findings returned as text" adds that MINOR rows on tests, security or false statements are repaired without asking, and style rows are accepted limits named in the PR. The repair brake (two consecutive rounds whose only accepted findings begin `fix-r`) stops the loop for the maintainer (`docs/WORKFLOW.md` §2 "The findings process"; `templates/findings.md`, Origin column).

**Where triage work actually accumulates today.** The night handovers show untriaged rounds holding changes open: `docs/journal/handover/2026-11-06-heartbeat-night.md` lists research-store-home (bead nxdy) "round 8 untriaged" and explore-provenance (bead g19n) "round 6 untriaged", each parked on a maintainer question (Q-M12, Q-M11) about a third finding of one mechanism. The night-run plans spell the sequence out: "Triage round N and repair taken rows … Orchestrator triages; Codex repairs, Sonnet after two failed checks (ADR 0017)" (`docs/research/2026-10-21-night-run-plan.md`, Queue item 3; same shape in `docs/research/2026-10-19-night-run-plan.md`, item 2).

**The rows a triage decides live outside the repository.** The loop record is written to `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>@<digest>/loop.md` until the phase-6 verdict releases it (`docs/WORKFLOW.md` §4); the orchestrator edits Status cells in that record, and a hand repair sets `fixed` statuses there after a backup of `loop.md` (`docs/WORKFLOW.md` §4, "Hand repairs by the orchestrator", with the follow-ups: index regeneration after header edits, the post-midnight stamp, and the targeted check instead of a full verify, bead coding-harness-24ag). Hand acceptances in released blocks are visible in practice, e.g. `plans/changes/swarm-time-limits/findings.md` rows L1-11, L3-2 to L3-4 ("fixed — orchestrator hand acceptance").

**"Triage" has one earlier, unrelated use in this repository.** The archived change `plans/changes/archive/2026-09-20-2ee-triage/research.md` (bead coding-harness-2ee) triaged 36 red tests into three maintainer-decided buckets on 2026-09-19; its traces remain as dated skip reasons in `tests/test_feedback_channel.py`, `tests/test_ci.py`, the header comment of `tests/test_ramp_valves.py`, and `scripts/ramp_valves.py`. That is a rules/tests triage, not a review-loop verb.

**The change itself.** Bead coding-harness-o2s1 is named "triage verb" in the backlog of `docs/journal/handover/2026-11-05-seven-lanes.md` ("Backlog in order: coding-harness-o2s1 (triage verb), …"); the change folder was opened by commit bcd22f6e on branch `feat/triage-verb`, and `plans/INDEX.md` lists only `changes/triage-verb/research.md` (draft, none). No research, spec, design or plan text about a triage verb exists anywhere in `plans/` beyond that skeleton — checked by grep over `plans/`, so "no matching artefact" is a finding here, not a silence.

## Where it lives

- Runner and verb set: `scripts/stage2.py` (`VERBS`, `main`, `undecided`, `undecided_refusal`, `accepted_row`, `clean_round`, `record_rows`, `ROW_COLUMNS`, `RELEASED_COLUMNS`).
- Triage procedure for the orchestrator: `prompts/04b-review-loop.md`, "For the orchestrator"; evidence rule also in `docs/WORKFLOW.md` §2 and §4.
- Status vocabulary: `templates/findings.md` (reference section); released-loop-row shape in the same file.
- Counters: `scripts/stage2_runs.py` (`Counts`, `COLUMNS`, "Loop rows: taken / rejected / undecided").
- Authority and escalation rules: `docs/WORKFLOW.md` §4 ("The review loop (phase 4b)", "Repairing taken findings (repair)", "Guard test", "When the same mechanism returns", "Hand repairs by the orchestrator", "Night runs"); `AGENTS.md` ("Findings returned as text"); `docs/adr/0017-codex-repairs-taken-findings.md`, `docs/adr/0021-review-swarms-until-clean.md`, `docs/adr/0023-guard-proof-for-test-only-repairs.md`.
- Loop-row routing table for verbs: `docs/WORKFLOW.md` §4, "Which change gets what" and "The routing" (no triage row exists there).
- Evidence of triage load: `docs/journal/handover/2026-11-06-heartbeat-night.md` (lane table, Q-M11/Q-M12), `docs/research/2026-10-21-night-run-plan.md` and `docs/research/2026-10-19-night-run-plan.md` (queue items "Orchestrator triages").
- Tests around the runner verbs and counters: `tests/test_stage2.py`, `tests/test_stage2_runs.py` (file names verified by glob; their individual triage-related test names I have not read).

## What is unclear about it

- **The bead's description was not read.** The tracker (Dolt under `.beads/`) is not hydrated in this worktree — `.beads/` holds only config, hooks and an `interactions.jsonl` that matches neither `o2s1` nor `triage`. What "triage verb" precisely scopes (decide rows with a model call? validate the orchestrator's decisions? batch-write statuses into `loop.md`?) is an open question for `tools/bd show coding-harness-o2s1` in the main checkout.
- **No repository text proposes the verb.** Beyond the backlog line and the bead id, nothing in `plans/`, `prompts/`, `docs/` or `scripts/` states what a triage verb should do, which model or route it would use, or whether it decides or only assists. "Not there" is distinct from "not found": I searched and it is absent.
- **Authority boundaries a triage verb would meet** are facts, not yet a scoped contract: the evidence rule, guard-test authorisation (`taken — guard test`, ADR 0023), the mechanism-escalation stop, and the repair brake all name the orchestrator or the maintainer as the decider; the runner's `repair` refuses undecided rows instead of deciding them. Whether any of those decisions could be delegated to a verb is stated nowhere — that would be a decision for the interview, not something this research settles.
- **Which files carry triage state is split.** Status decisions are written into the loop record outside the repository, then released into `findings.md` inside it; the phase-6 table rows (F-ids) are triaged in `findings.md` directly. A triage verb's target surface (record, released blocks, phase-6 tables, or all three) is not stated anywhere.
- The individual test names covering status parsing in `tests/test_stage2.py` were not read in this pass; the helpers they presumably pin (`undecided`, `undecided_refusal`, `accepted_row`, `clean_round`) were read in `scripts/stage2.py`.

## Which files a change would have to touch

Stated as facts about where the touched concerns live, not as a plan: `scripts/stage2.py` (verb registration in `VERBS`/`main`; the status helpers and column constants it would read or extend); `docs/WORKFLOW.md` §4 (every verb has a section there, and "The routing" names each verb's route); `prompts/04b-review-loop.md` ("For the orchestrator" steps 1–4 carry the triage procedure; the guard-test change set the precedent of editing exactly this file for triage/status wording — `plans/changes/guard-test/plan.md` lists that edit); `templates/findings.md` (the status vocabulary reference); `AGENTS.md` (the stage-2 paragraph enumerates the live verbs); `tests/test_stage2.py` and `tests/test_stage2_runs.py` (verb behaviour and the taken/rejected/undecided counters). If a verb changed what is counted, `scripts/stage2_runs.py`'s `COLUMNS` and its run-report contract (bead coding-harness-kw0) are affected too.

## Neighbours the finders suggest

- `plans/changes/guard-test/spec.md` (and its `plan.md`/`decisions.md`) — the last change that reshaped triage/status wording, ADR 0023.
- `plans/changes/swarm-time-limits/spec.md` and its `findings.md` — released loop rows showing triaged statuses and hand acceptances in practice.
- `plans/changes/archive/2026-09-20-2ee-triage/research.md` — the same word with a different meaning (red-test triage, 2026-09-19).
- `plans/specs/implementation-verification/spec.md` — the living spec of the runner's verification/repair-flow contract.
- ADRs as applicable rules: `docs/adr/0013-every-criterion-names-its-proof.md`, `docs/adr/0017-codex-repairs-taken-findings.md`, `docs/adr/0021-review-swarms-until-clean.md`, `docs/adr/0023-guard-proof-for-test-only-repairs.md`.
