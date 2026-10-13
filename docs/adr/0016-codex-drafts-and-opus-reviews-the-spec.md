---
title: "ADR 0016 — Codex drafts spec, design and plan through the runner, and Opus 5.5 reviews the spec"
category: adr
status: accepted
created: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-13
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, codex, draft, spec-review]
---

# ADR 0016 — Codex drafts spec, design and plan through the runner, and Opus 5.5 reviews the spec

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Amends ADR 0007 (decisions 2 and 4) and
  ADR 0011 (decision 2); supersedes no ADR. Decision D-13 stands as ADR 0007
  set it, and no other D- or O-number of the 2026-09-16 interview changes:
  the draft runs inside the seven phases, not as a job outside them.
* Review: the maintainer's answers of 2026-10-12, recorded as Q-1 to Q-5 in
  `plans/changes/codex-drafts/decisions.md` — the spec review alone moves to
  a Claude model, Codex keeps phase 6 (Q-1); that model is Opus 5.5 (Q-2); a
  writing runner verb with the guards of `implement` (Q-3); `make verify`, the
  Opus spec review, the plan card shown unchanged, and the orchestrating
  session reading the whole draft before the review (Q-4); GLM 5.3 as the
  fallback, after one Codex attempt and one Codex repair, as the maintainer
  was told the answer would be read (Q-5). The spec proposes "yes" to the ADR
  question; the maintainer's answer is not recorded when this draft is
  written · the acceptance is the merge commit and is written nowhere else,
  so the header's `review` stays empty (ADR 0008) · Decider: maintainer ·
  prepared by a Claude Code session
* Date: 2026-10-12 · takes effect on merge

## Context

* **Who drafts today.** Phases 2 (spec), 2b (design) and 3 (plan) run in an
  interactive Claude Code session on Opus 5.5 at effort `xhigh`
  (`docs/WORKFLOW.md` §3), the phases with the highest reasoning demand. No
  runner verb drafts them (`VERBS` in `scripts/stage2.py`, read 2026-10-12).
  The maintainer wants them off Claude tokens (bead coding-harness-rhq;
  `plans/changes/codex-takeover/research.md`, candidate 2).
* **Codex cannot write headless today.** Every `run_codex` call pins
  `sandbox_mode="read-only"`; the one writing Codex path is the interactive
  `session` verb of ADR 0012, which needs a person at a terminal.
  `codex exec` of codex-cli 0.162.0 offers the sandbox `workspace-write`
  beside `--add-dir`, `--approve-for-me` and
  `--dangerously-bypass-approvals-and-sandbox` (`codex exec --help`, read
  2026-10-12).
* **Codex reviews the spec today.** ADR 0011 decision 2 keeps the spec review
  and the review with Codex, and phase 6 resumes the phase-2a session
  (`SESSION_LINE` in `scripts/stage2.py`). A Codex that drafts the spec would
  review its own draft — "A model rates its own output too kindly"
  (`docs/WORKFLOW.md` §4).
* **A drafted feature meets one gate no drafter can satisfy.** `adr-answers`
  holds every `feature` to `decisions/answers/<change>/adr.yaml`, which only
  the maintainer's answer may create (`scripts/check_adr_answers.py`; house
  rule 8 of `AGENTS.md`).
* **What the guards of `implement` are** (`scripts/stage2.py`, read
  2026-10-12): the declaration and the leak check before every attempt, a
  refusal of changes outside `findings.md` before the first, the worktree put
  back after a dead model process, `make verify` and the derived files run by
  the runner, a quoted block for a failed attempt, and exactly one commit.

## Decision Drivers

* No model reviews its own draft.
* The drafting stays off Claude tokens, even when Codex fails.
* A draft can run unattended, and what it may change is enforced by the
  runner, not asked of the model.
* The maintainer's answers — the interview's and the ADR question's — are
  written only from what the maintainer stated.

## Considered Options

* **A writing runner verb with `implement`'s guards** (chosen, Q-3).
* **The interactive session of ADR 0012.** Codex already writes there, but a
  person must sit at the terminal, so no draft runs in the night run.
* **A read-only Codex whose answer the runner writes into files.** Nothing
  new may write, but the runner would parse three documents out of one
  answer, and Codex could not read back what it had drafted.
* **The spec review on Sonnet 5.5 or Haiku 4.5** — cheaper, rejected for the
  strongest review where it matters most (Q-2); **2a and 6 both on a Claude
  model** — rejected, since in phase 6 Codex reviews GLM's code, nothing of
  its own (Q-1).
* **The Opus `spec-planner` as the fallback, or no fallback** — rejected:
  the first spends Claude tokens exactly when Codex fails, the second leaves
  an unattended run with nothing (Q-5).
* **An Opus review of the plan as a further check** — rejected for the
  orchestrating session's full read of the draft (Q-4).

## Decision

Chosen option: "a writing runner verb with `implement`'s guards", because it
is the only one in which the draft runs unattended while the runner, not the
model, decides what may change.

1. **Codex drafts phases 2, 2b and 3** through `python3 scripts/stage2.py
   draft <change>`: one headless `codex exec` call per attempt writes
   `spec.md`, `design.md` when due, `plan.md` and, when due, one ADR draft;
   `gpt-6.1-sol` at effort `max`, sandbox `workspace-write`, hooks and
   memories off, and no added directory, no automatic approval and no bypass.
   Framework content goes to `openai-codex` as before; Codex now also writes.
2. **The runner's guards.** Before every attempt: the declaration and the
   leak check over the exact prompt, and an audit line. Before the first: a
   refusal of changes outside the change's `findings.md`. After every call:
   a moved `HEAD` stops the run with no rewrite; every path git reports as
   changed outside the change folder, and the change's `decisions.md`, is put
   back at the baseline, except one new `docs/adr/<NNNN>-<slug>.md` file;
   then the derived files, `make verify`, and the checks that `spec.md` and
   `plan.md` exist and `plan.md` carries its card and `## Time used`. A
   passing attempt makes exactly one commit.
3. **The one red gate a draft accepts** is `adr-answers` reporting that the
   drafted change has no answer file, and nothing else; `findings.md` says
   the answer is owed. The orchestrating session records the maintainer's
   stated answer afterwards (`python3 scripts/harness.py decide adr …
   --stated-in …`); no drafting model records one.
4. **The chain** (Q-5): Codex; Codex again with the first attempt's
   diagnostics; then `glm-5.3` on `glm-coding-plan` through Claude Code with
   file tools only and both diagnostics. A failed call puts the worktree back
   and moves on; a failed post-run check leaves the tree for the next
   attempt. Each later attempt's audit line records why it started. A leak
   refusal never falls back. The GLM key is read only when the GLM attempt
   is due. Framework content may go to `glm-coding-plan` for this attempt.
5. **Opus 5.5 reviews the spec** (phase 2a) for every change stage 2 routes,
   through `python3 scripts/stage2.py spec-review <change>`: Claude Code on
   `claude-opus-5-5` at effort `xhigh`, read-only tools, the 2a prompt in
   full, no session kept. Codex leaves phase 2a.
6. **Codex keeps phase 6, in a fresh session.** Phase 6 no longer resumes a
   2a session for a change reviewed after this record; a change whose Codex
   2a session is recorded is still resumed. The phase-6 reviewer first checks
   that each 2a row arrived in the revised spec.
7. **A draft passes four checks before phase 4** (Q-4): `make verify`, the
   Opus spec review, the orchestrating session's reading of the whole draft
   before that review, and the plan card shown to the maintainer unchanged.
   The author works the 2a rows in with a second `draft` run, and an
   `[AMBIGUITY]` goes to the maintainer before it.
8. **The residual risk extends.** ADR 0007 decision 4 accepted unconfined
   reads for the reviewers, and ADR 0012 decision 6 a Codex that writes in
   a session a person watches. Here Codex writes unattended: it can read what
   the maintainer's user can read and send it to OpenAI, and inside its
   sandbox it writes and runs commands. The runner does not verify that
   sandbox, and it puts back only what git sees in the worktree — not an
   ignored file, not a path outside the worktree, and not the repository's
   git directory: `git restore` and `git clean` never touch `.git`, so a
   draft call in a plain checkout can leave `.git/hooks` or `.git/config`
   changed while the runner commits right after it.
9. **Where Stage 2 is off**, Opus 5.5 drafts by hand as §3 says; `draft` has
   no Stage-1 route.

## Consequences

* **Claude tokens** are spent on the spec review and the orchestrating
  session's reading, no longer on drafting; Codex's subscription limit is
  spent on drafting and the phase-6 review. Neither is measured by the
  runner.
* **Codex stands on both sides of a change**: author of the spec, reviewer
  of the code, and the judge of the 2a rows against its own spec. Q-1
  accepted this; the plan card and the maintainer's veto stay after it.
* **The stage-2 stop rule** (`docs/WORKFLOW.md` §4, "Measuring the first
  three stage-2 runs") counts taken findings of Codex and of the rungs; the
  rows of an Opus spec review are not among them.
* **A drafted feature's commit carries a red `adr-answers`** until the
  orchestrating session records the maintainer's answer.
* **The doctrine moves in the same pull request**: `docs/WORKFLOW.md` §3 and
  §4, `AGENTS.md`, the remarks of `openai-codex`, `opencode-go` and
  `glm-coding-plan`, and the Model lines of the phase prompts.
* **The continuity map gains nothing**: no D- or O-number changes, so
  `scripts/check_decision_continuity.py` and the target document stay as
  they are.

## Validation

* `python3 -m pytest tests/test_stage2.py tests/test_model_endpoints.py -q`
  green: the draft's Codex argv, the put-back, the `HEAD` stop, the chain and
  its reasons, the one tolerated gate, the single commit; the spec review's
  Claude Code launch and its rows; the fresh phase-6 session; and the routing
  text of the doctrine, the prompts, `AGENTS.md` and the endpoint remarks.
* `make verify` green once the maintainer's answer is recorded, and
  `python3 scripts/touch_map.py origin/main HEAD` showing that `docs/adr/`
  gains only this file.
* **Configured, not measured**: no test runs a real Codex, so that
  `workspace-write` confines Codex's writes as its documentation says is not
  shown here. The first real draft, in a later change, is the first
  measurement, and its pull request names it.
