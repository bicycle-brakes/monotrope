---
title: "ADR 0015 — GLM 5.3 repairs the findings the orchestrator takes, and no reviewer repairs its own"
category: adr
status: superseded
created: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-13
superseded_by: "0017"
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, glm, repair, review-loop]
---

# ADR 0015 — GLM 5.3 repairs the findings the orchestrator takes, and no reviewer repairs its own

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends ADR 0011 (decisions 2 and 3);
  supersedes no ADR. Decision D-13 stands as ADR 0007 set it.
* Review: the maintainer's ask of 2026-10-12 in bead coding-harness-g2f — the
  repair runs on GLM 5.3, not Flash, with the guards of `implement` — and the
  answers of 2026-10-12 recorded as Q-1 to Q-5 in
  `plans/changes/stage2-repair/decisions.md`: both kinds of finding in one
  call (Q-1); the loop's Status words for a phase-6 finding and `fixed —
  <test>` after the repair (Q-2); the orchestrator starts the re-check with
  the existing verbs (Q-3); this record, as an amendment of ADR 0011 (Q-4);
  text-only findings repaired too, as `fixed — not a test — <reason>` (Q-5) —
  and the answer "yes" to the ADR question
  (`decisions/answers/stage2-repair/adr.yaml`) · the acceptance is the merge
  commit and is written nowhere else, so the header's `review` stays empty
  (ADR 0008) · Decider: maintainer · prepared by a Claude Code session
* Date: 2026-10-12 · takes effect on merge
* Note, 2026-10-13: [ADR 0017](0017-codex-repairs-taken-findings.md) supersedes
  this decision; it takes effect when the pull request that carries it is
  merged (ADR 0008). The text below is kept unchanged as history: the repair
  route, the same-model prohibition and the Z.ai spend it records are
  replaced, while its evidence, status and loop-budget rules stand in ADR 0017.

## Context

* **Who repairs today.** A Claude Sonnet sub-agent repairs the findings the
  orchestrator takes: the loop rows of phase 4b marked `taken`, and the
  findings of phase 6 (`plans/changes/stage2-repair/research.md`, opening,
  2026-10-12). It spends Claude tokens, and its edits pass none of the
  runner's checks.
* **What routes where.** ADR 0007 lets framework content flow to
  `openai-codex` and, through Claude Code, to `glm-coding-plan`. ADR 0011
  moved the review loop to the ladder on `opencode-go`, kept the spec review
  and the review with Codex, and left explore and implement on GLM 5.3 Flash.
  Neither names a model for a repair (`research.md`, "Documents that name the
  repair step today").
* **What is declared.** `model-endpoints.yaml` lists `glm-5.3` and
  `glm-5.3-flash` on `glm-coding-plan`, with `framework` among what it may see
  and the residency `anbieter-erklaert`; no review phase has routed to it since
  2026-10-07 (`research.md`, "Models, endpoints", read 2026-10-12).
* **The reviewers are read-only.** A rung runs Pi with `read`, `grep`, `find`
  and `ls` (`PI_TOOLS`); Codex runs in its read-only sandbox
  (`scripts/stage2.py`, read 2026-10-12).
* **Where the findings stand.** A loop row lives in the loop record outside
  the worktree until the phase-6 verdict, then in `findings.md`; a phase-6
  finding stands in `findings.md` with the Status `open`. A loop row reads
  `taken — …` or `rejected — …`, and round 3 starts only when round 2 wrote a
  row whose Status begins `taken` (ADR 0011, decision 3).
* **A model under the runner has no command tool.** `implement`'s model edits
  files; the runner runs `make verify` and makes the checkpoint commit
  (`docs/WORKFLOW.md` §4). The evidence rule asks for a test that
  demonstrates a finding, and no such model can run one.

## Decision Drivers

* Repairs leave Claude's budget and run behind the runner's guards (bead
  coding-harness-g2f).
* A reviewer does not judge its own repair (Q-4).
* One vocabulary for every decision on a finding (Q-2).
* The loop's round budget counts as before (Q-3).
* A repair of code is proven by a test that was red first; a repair of text
  by the re-check (Q-5).

## Considered Options

* **GLM 5.3 through a runner verb `repair`** — chosen.
* **GLM 5.3 Flash, the implement model.** Chosen against: the maintainer
  named GLM 5.3, not Flash (bead coding-harness-g2f, 2026-10-12).
* **Keep the Claude Sonnet sub-agent.** Chosen against: it spends Claude
  tokens, and its edits pass no leak check, no `make verify` and no checkpoint
  of the runner.
* **The reviewer repairs its own findings** — Codex or the round's rung, given
  write tools. Chosen against: it would judge its own fix, and the reviewers'
  read-only tools are what ADR 0007 and ADR 0011 accepted their unconfined
  reads for.
* **One call per row.** Chosen against: one leak check, one `make verify` and
  one checkpoint per row; the maintainer chose both kinds in one call (Q-1).
* **An entry in `docs/WORKFLOW.md` alone.** Chosen against: the maintainer
  keeps model routing in ADRs (Q-4).

## Decision

Chosen option: "GLM 5.3 through a runner verb `repair`", because it takes the
repairs off Claude's budget behind the guards every other GLM call passes,
while the reviewers stay read-only.

1. **The repair of taken findings runs on GLM 5.3** — `glm-5.3` on
   `glm-coding-plan`, through Claude Code, started only by `python3
   scripts/stage2.py repair <change>`. One call takes every loop row and every
   phase-6 finding whose Status begins `taken`. The attempts are GLM 5.3, one
   GLM 5.3 repair attempt that carries the first one's diagnostics, and one
   Sonnet 5.5 stage-1 fallback; `--stage2-off [REASON]` runs Sonnet 5.5 alone
   and records why; a leak-check BLOCK stops without a fallback. The guards of
   `implement` hold: the declaration and the leak check before each attempt,
   file tools without a command tool, the credential clean-up, `make verify`
   run by the runner, a measured line in the time log, one checkpoint commit.
   This amends ADR 0011's decision 2, whose last sentence names what still
   routes to GLM: the repair joins explore and implement there, on GLM 5.3.
2. **A reviewer never repairs its own findings.** The rungs and Codex keep
   their read-only tools; the repair is a separate call by a model no review
   phase routes to. A change that routes a review phase to `glm-coding-plan`
   again has to say who repairs that phase's findings.
3. **The orchestrator decides, the verb repairs, the reviewer re-checks.** The
   orchestrator writes `taken — <reason>` or `rejected — <reason>` into a
   phase-6 finding as into a loop row, and `taken — not a test — <reason>` for
   a finding no test can show. The verb repairs only the taken rows and ends
   with its checkpoint commit; the orchestrator then re-checks with the loop's
   next round and with `review`.
4. **A repaired row reads `fixed`.** Its Status becomes `fixed —
   tests/<path>::<function>` or `fixed — not a test — <reason>`, the forms of
   ADR 0013's criterion ledger. A finding on code is fixed only with a test
   that the runner ran against the baseline's code and saw fail; a finding on
   text is proven by the re-check.
5. **A fixed row counts as a taken one.** Round 3 starts when round 2 wrote a
   row whose Status begins `taken` or `fixed`, which amends ADR 0011's
   decision 3; the stage-2 run count counts a fixed loop row as taken.
   `Broke a test` stays the orchestrator's mark, written before the next round
   or the release.

## Consequences

* The Claude tokens of a repair move to the GLM subscription; the Sonnet
  fallback still spends them when both GLM attempts fail.
* More framework content goes to Z.ai: the taken rows, the spec and the plan
  in each prompt. The loop rows, held outside the repository until the
  phase-6 verdict, now reach Z.ai in a prompt — never Codex, so they still
  cannot shape that verdict. The leak check scans each prompt.
* The orchestrator writes a Status on every phase-6 finding before a repair,
  and marks a finding no test can show with `not a test` when it takes it.
* Each repaired finding on code costs one pytest run on a temporary checkout
  of the baseline. A finding no test can show red cannot be fixed as code:
  the evidence rule, held by the runner.
* `taken` changes its meaning. Before this record a loop row's `taken —
  <test>` meant taken and repaired; from now on `taken` means decided and
  waiting for the repair, and `fixed` means repaired. Findings written before
  are not rewritten.
* The continuity chain stops at ADR 0011: no D- or O-number changes, so the
  map in `scripts/check_decision_continuity.py` gains nothing. ADR 0011's file
  is not edited; this record amends it.

## Validation

* `python3 -m pytest tests/test_stage2.py tests/test_stage2_runs.py -q` green:
  the verb's routes, refusals, prompt and post-run checks — the red-first run
  included —, the statuses it writes and its one commit; `review-loop`,
  `review`, `release-loop` and the run count reading a fixed row; the doctrine
  texts naming the verb.
* `make verify` green, and the pull request's file list leaves
  `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`,
  `docs/adr/0011-stage-2-reviews-through-opencode-go.md`,
  `scripts/leakcheck.py`, `provenance.yaml` and `.claude/settings.json`
  untouched.
* The phase-6 review of the change that carries this record reads it against
  `plans/changes/stage2-repair/decisions.md`, Q-1 to Q-5.
