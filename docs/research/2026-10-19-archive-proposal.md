---
title: "Archive proposal for the finished changes behind the red drift gate — 2026-10-19"
category: research
created: 2026-10-19
updated: 2026-10-19
last_reviewed: 2026-10-19
status: draft
owner: framework-architect
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Sonnet 5.5, 2026-10-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plans, archive, staleness, drift-gate]
---

# Archive proposal for the finished changes behind the red drift gate

This is a proposal for the maintainer to decide, change by change. **Nothing is
moved, edited or deleted**: every directory under `plans/changes/` stays where
it is. For each of the 17 changes whose bead is closed but whose artefacts the
drift check still reports, the table below says what the doctrine would do with
it (living spec, ADR, plain archive, or keep) and why. It relates to pull
request #169, whose handover reports the same gate; where this measurement
differs from that handover, the difference is named below.

## How it was measured

- Command: `python3 scripts/plans_registry.py --check` (the recipe of
  `make staleness`, `Makefile`), run in a worktree of `origin/main` at commit
  `59630b7`, with the main checkout's interpreter
  (`.venv/bin/python`, Python 3.12.15). Date: 2026-10-19. Read-only; exit code 0
  (DRIFT does not fail without `--strict`).
- Result: **91 DRIFT findings** and 2 INFO lines (199 artefacts checked).
  - 89 findings are artefact lines of **17 changes** whose bead is closed:
    "the artefact is not 'done' and archived".
  - 2 findings are beads that are `in_progress` with no artefact under
    `plans/changes/`: `coding-harness-6th` (stage2 runner: Claude Code refuses
    the GLM model names as unrecognized) and `coding-harness-icw` (Phase 1 as a
    bounded research swarm). They are not finished changes and are outside the
    table.
- Differences from #169: it counts 83 artefact lines across 16 changes; this
  run counts 89 across 17 (the 91 total agrees). It also names bead
  `coding-harness-omp` as a Pi-install topic; that bead is the red-first
  baseline fault (`red-first-install`), a missing Pi install being only its
  trigger.
- Bead status was read with `tools/bd show` on 2026-10-19; all 17 are CLOSED.
  The merge pull requests named in the reasons are quoted from the beads'
  close reasons, and the ones with a merge commit were found in the history of
  `origin/main`. Pull request #155 (red-first-install) is on `main`; the bead
  `omp` names no number.
- Not classified: the phase-6 verdict of each `findings.md`. Only two files
  (`pi-pin`, `repair-fixed-lines`) carry an `Open BLOCKER:` line; both end on
  "no". For the others the verdict was **not read**.

## What the doctrine says happens after a change

`docs/WORKFLOW.md`, section "Artefact lifecycle", and `plans/_README.md`,
"Three states, three places": on close, the delta goes into the living
capability spec under `plans/specs/`, lasting architectural decisions go into
an ADR under `docs/adr/`, and the rest goes into
`plans/changes/archive/YYYY-MM-DD-<name>/`. "An implemented feature spec does
not stay as a living document." The drift rule (`scripts/plans_registry.py`,
line 366) wants a change whose bead is closed to be `done` and archived.

Precedent on `main` (2026-10-19): `plans/changes/archive/` holds 20 archived
changes, all `accepted` / `done`. `plans/specs/` holds one living spec
(`implementation-verification`, a bounded runner contract). The 17 changes
below still say `status: draft` and `implementation_status: none` or `partial`
in every artefact; archiving one therefore also means setting those two fields,
which is part of what the maintainer would be deciding.

## The table

Artefact status fields are given as `status / implementation_status`; "all"
means every artefact of the change carries the same pair. Class is the `class:`
of `spec.md`.

| Change | Bead (closed) | Artefacts and status fields | Proposal | Reason |
|---|---|---|---|---|
| `adr-owning-change` | `coding-harness-afa` — interview-minimums: an ADR names its owning change instead of the gate inferring it from the diff | decisions, design, findings, plan, research, spec; all draft / none; class feature | plain archive | Delivered by PR #135 (9cad4a8); its decision already lives in ADR 0014 (accepted). |
| `attempt-diagnostics` | `coding-harness-cit` — stage2 implement: keep each failed attempt's post-run diagnostics in findings.md | decisions, findings, plan, research, spec; all draft / partial; bounded | living spec | Delivered by PR #127 (6e6f8f7); a bounded runner contract like the existing `implementation-verification` spec, and no ADR holds it. |
| `ci-minutes` | `coding-harness-cac` — ci: cut hosted CI minutes | decisions, findings, plan, research, spec; all draft / none; bounded | plain archive | Merged in PR #136 (3199a28); the behaviour is the workflow file itself, which is the truth. |
| `codex-drafts` | `coding-harness-rhq` — Stage 2: Codex drafts spec and plan, a Claude model reviews the spec | decisions, design, findings, plan, research, spec; all draft / none; feature | plain archive | Delivered by PR #133 (cd89ac5); its decision already lives in ADR 0016 (accepted). |
| `codex-repairs` | `coding-harness-0ga` — stage2 runner: Codex (gpt-6.1-sol) repairs the taken review findings instead of GLM 5.3 | decisions, design, findings, plan, research, spec; all draft / none; feature | plain archive | Merged as PR #138 (c52bf14); its decision already lives in ADR 0017 (accepted). |
| `codex-takeover` | `coding-harness-nsm` — Research: which workflow tasks Codex can take over to save Claude tokens | research only; draft / none | plain archive | Research without a spec; the bead closed when the maintainer chose two candidates, which became `coding-harness-g2f` and `coding-harness-rhq`. |
| `criterion-test-ledger` | `coding-harness-909` — Per-criterion tests are held by no gate | decisions, design, findings, plan, research, spec; all draft / partial; feature | plain archive | Delivered by PR #126 (b02e2f8); its decision already lives in ADR 0013 (accepted) and the `criterion-ledger` gate. The "partial" field is not explained by the close reason (not read further). |
| `haiku-5-5` | `coding-harness-eao` — Haiku 5.5 instead of Haiku 4.5 everywhere | decisions, findings, plan, research, spec; all draft / none; bounded | plain archive | Merged in PR #147 (9f1543f); a one-off sweep of model names, no durable contract of its own. |
| `interview-context` | `coding-harness-zs7` — interview: every question carries its context (ADR) | decisions, design, findings, plan, research, spec; all draft / partial; feature | plain archive | Decision PR #148 (b17f9f2) accepted ADR 0018 and adopted the `question-context` gate. The "partial" field is not explained by the close reason (not read further). |
| `loop-until-clean` | `coding-harness-4fk` — Review of the implementation as a swarm of OpenCode Go models | decisions, design, findings, plan, research, spec; all draft / none; feature | plain archive | PR #157 merged 2026-10-18 (b9cbd40); ADR 0021 (accepted) holds the decision and the runner code is on `main` (`scripts/stage2_availability.py` exists). Latest change here is 2026-10-19, the closing day. |
| `pi-pin` | `coding-harness-agx` — Runner: move the pinned Pi from 1.1.0 to 1.2.0, and keep the version from drifting | decisions, design, findings, plan, research, spec; all draft / none; feature | plain archive | Merged as PR #149 (135f029); its decision already lives in ADR 0019 (accepted). Last `Open BLOCKER:` line says no. |
| `provenance-location` | `coding-harness-3ar.1` — ADR-answer pin, package 1: provenance location | decisions, findings, plan, research, spec; all draft / partial; bounded | plain archive | Merged in PR #130 (f2c31cb); a code behaviour of `harness.py decide adr`, the code is the truth. "Partial" not explained (not read further). |
| `red-first-install` | `coding-harness-omp` — stage2 red-first: a missing install counts as red | decisions, findings, plan, research, spec; draft / none and partial; bounded | living spec | PR #155 merged (76b90a8); a bounded runner contract like `implementation-verification`. Its open follow-up question lives in bead `coding-harness-a7m` (OPEN), not in this change. |
| `repair-fixed-lines` | `coding-harness-ugi` — stage2 repair: answer parser misreads repaired rows | decisions, findings, plan, research, spec; all draft / partial; bounded | living spec | Merged in PR #151 (6029bbf); a bounded runner contract on how repair answers are read. Last `Open BLOCKER:` line says no. |
| `sol-effort` | `coding-harness-yzk` — stage2 runner: Sol effort per verb | decisions, findings, plan, research, spec; all draft / none; bounded | plain archive | Merged in PR #143 (e1bf225); a configuration choice, with the effort per verb set in code and doctrine. |
| `stage2-format` | `coding-harness-52r` — stage2 runner formats the attempt before make verify | decisions, findings, plan, research, spec; all draft / none; bounded | living spec | PR #132 merged (43cc834); a bounded runner contract like `implementation-verification`; the spec says the ADR question was answered no. |
| `stage2-repair` | `coding-harness-g2f` — stage2 repair verb: GLM repairs the review findings the orchestrator took | decisions, design, findings, plan, research, spec; all draft / none; feature | plain archive | Merged with PR #131 (14f6e1a); ADR 0015 was written for it and is now `superseded` by ADR 0017, so there is nothing current to lift. |

Rows per proposal: plain archive 12 · living spec 4 · ADR 0 · keep 0 (the 17
total as of the 2026-10-19 measurement).

The "living spec" rows are the judgment calls: the only living spec on `main`
is a bounded runner contract, and these four are of the same kind, but
`WORKFLOW.md` does not say which bounded changes earn one. Choosing plain
archive for them is equally consistent with the 20 archived changes. No
change is proposed as an ADR because every decision of the feature-class rows
already has its ADR. Not read: the code behind each row beyond the existence
of the cited ADR file and of `scripts/stage2_availability.py`.

## Decision for the maintainer

Merging this pull request changes nothing but adds this file. It moves no
directory, edits no artefact, and changes no bead. The red gate stays red until
a later, separate act archives the changes.

Each row is decided separately: for any row the maintainer may accept the
proposal, pick another of the four outcomes, or leave the change as it is. Only
after such a decision would a pull request move that change (and set its
status fields to `accepted` / `done`, as the 20 archived changes show).
