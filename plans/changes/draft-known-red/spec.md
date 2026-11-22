---
title: "Spec — draft-known-red"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-83e
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, draft]
class: bounded
appetite: 4
adr_files: [docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md]
neighbours: []
---

# Spec — draft-known-red

The goal in one sentence: a draft can run with Stage 2 off — `draft <change>
--stage2-off [REASON]` drafts through Opus 5.5 at effort `xhigh` in one
recorded attempt, and a Codex/GLM chain that cannot finish names that flag as
the next step on a tree that no longer blocks it (bead coding-harness-83e).
Research: `research.md`. Decisions: `decisions.md`.

## Problem

- The runner refuses the flag for the verb. `scripts/stage2.py` allows
  `--stage2-off` only for explore, implement and repair (the verb check in
  `_run`, read 2026-11-22, `research.md` "The `--stage2-off` refusal is in
  code"). Where Stage 2 is off or Z.ai is unavailable, a draft therefore has no
  runner route at all; the doctrine sends the maintainer back to drafting by
  hand (`docs/WORKFLOW.md` §4, "The draft (phases 2, 2b and 3)": "a draft
  takes no `--stage2-off`").
- The accepted ADR says the opposite of what this change builds. ADR 0016
  decision 9 reads "Where Stage 2 is off, Opus 5.5 drafts by hand as §3 says;
  `draft` has no Stage-1 route" (`docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md`,
  decision 9, read 2026-11-22). Adding the route without
  amending the ADR would leave a `human-decided` record stating the opposite
  of the code and of the `docs/WORKFLOW.md` §4 that cites it (phase-2a finding
  F-1). The maintainer's answer B amends decision 9 by an addendum and sets
  the Stage-1 draft on Opus 5.5 at effort `xhigh`, the model §3 assigns phases
  2, 2b and 3 — not on Sonnet 5.5 (`decisions.md` Q-1, 2026-11-22).
- The chain ends at GLM 5.3 and names no way on. `draft`'s routes are Codex, a
  second Codex attempt with the first's diagnostics, then GLM 5.3
  (`scripts/stage2.py`, `draft`'s routes list, read 2026-11-22, `research.md`
  "The draft verb"); when all three fail, the final message names the findings
  file but no next step, and the GLM-key refusal on the third route names only
  the missing key (phase-2a finding F-6). The bead's origin is exactly this:
  on the 2026-10-17 night run a draft failed every attempt, `--stage2-off` was
  refused, and each spec redraft cost about 30 minutes recovered from the
  attempt refs (`docs/journal/handover/2026-10-17-night-run-sixth.md`, bead
  coding-harness-83e, P1, discovered from coding-harness-icw).
- An exhausted chain leaves a tree that blocks the very rerun that would fix
  it. A failed call is put back; a failed document check leaves its tree for
  the next attempt (ADR 0016 decision 4) — but after the last attempt no next
  attempt exists, no attempt ref is saved (`save_attempt` runs only on a
  failed call, `scripts/stage2.py`, read 2026-11-22), and the final message
  names only the findings file. The leftover `spec.md` and `plan.md` then make
  `refuse_preexisting` refuse the next `draft <change> --stage2-off <reason>`
  run with exit 2 (phase-2a finding F-5).
- This change's own draft is the live case: on 2026-11-22 every Codex draft
  attempt of both runs failed its call and each run went to its third route,
  GLM 5.3 (`findings.md`, attempts of 2026-11-22). Where GLM is not an option
  either, nothing is left.
- The bead's other half is already merged and stays out of scope: a draft is
  judged only by the document subset of the gate registry (`document_gates` in
  `scripts/stage2.py`), and every draft record of 2026-11-21 says "document
  checks only, no tests ran" (`decisions.md`, "What the research changed",
  2026-11-22). A known-red test suite can no longer fail a draft; what remains
  is the route.

## Terms

**Stage-1 route:** the explicit `--stage2-off [REASON]` route through the
`claude-code-plan` endpoint, on the model `docs/WORKFLOW.md` §3 assigns the
verb's phase — Haiku 5.5 for explore (phase 1), Sonnet 5.5 at effort `medium`
for implement and repair (phase 4), and for the draft Opus 5.5 at effort
`xhigh` (phases 2, 2b and 3; `decisions.md` Q-1). **Chain:** the draft's
default three attempts — Codex, a second Codex attempt with the first's
diagnostics, then GLM 5.3. **Audit line:** the `Stage-2 call, <date>: draft ·
attempt <n> · route <route> · endpoint <endpoint> · model <model> · reason
<REASON> · leak check clean …` line the runner writes to the change's
`findings.md` before each call. **Attempt ref:** the snapshot under
`refs/stage2/attempts/<change>/` that `save_attempt` writes, parented on the
baseline, so `git diff <baseline> <ref>` shows the tree it holds.

## Acceptance criteria

1. When `python3 scripts/stage2.py draft <change> --stage2-off [REASON]` is
   invoked, the runner starts the Stage-1 route instead of refusing that
   `--stage2-off` applies only to explore, implement and repair.
   *Refuted by:* the command exits 2 with that refusal and no model call
   starts.
2. While a draft runs the Stage-1 route, its single attempt calls Opus 5.5 at
   effort `xhigh` through the `claude-code-plan` endpoint — the model
   `docs/WORKFLOW.md` §3 assigns phases 2, 2b and 3 (`decisions.md` Q-1) —
   and no Codex or GLM call starts and no GLM key is read.
   *Refuted by:* any Codex or GLM call, a read of the GLM key, or a call with
   another model or effort.
3. When a Stage-1 draft run starts, the preflight's endpoint declaration check
   clears the `claude-code-plan` endpoint — as implement and repair pass their
   Stage-1 model — not the `openai-codex` declaration (phase-2a finding F-4).
   *Refuted by:* a Stage-1 draft run exiting 2 on the `openai-codex`
   declaration wherever that declaration does not stand.
4. When a Stage-1 draft attempt begins, the audit line in the change's
   `findings.md` carries `route stage-1`, the `claude-code-plan` endpoint, the
   model `claude-opus-5-5` and, when a reason was given, `· reason <REASON>` —
   the same record line the other writing verbs write.
   *Refuted by:* an audit line without the route, or without the reason that
   was given.
5. When the Stage-1 draft attempt's call fails, the run exits 1 after that one
   attempt, puts every changed path back to the baseline except the change's
   `findings.md` — the change folder included, as the chain's call-failure
   path does (phase-2a finding F-3, reading B) — and quotes the attempt's
   diagnostics and its saved attempt ref below the audit line.
   *Refuted by:* a second model call, an exit 0, a path other than
   `findings.md` left changed, or the diagnostics or ref missing from
   `findings.md`.
6. When the Stage-1 draft attempt's document check is red, the attempt fails
   with exit 1 and its scope line and problems are quoted below its audit
   line, as on the Codex chain.
   *Refuted by:* a red document check that exits 0 or whose problems are
   absent from `findings.md`.
7. When a Stage-1 draft attempt changes a path outside the change folder —
   beyond the one new ADR file under `docs/adr/` — the runner puts that path
   back before the document check, as on the Codex chain.
   *Refuted by:* such a path left changed after the put-back or reaching the
   attempt's commit.
8. When a Stage-1 draft attempt passes, the runner makes exactly one
   descendant commit whose message names `route stage-1`, and the time entry
   under the plan's `## Time used` records `route stage-1` with the model
   `claude-opus-5-5`.
   *Refuted by:* a commit message or time entry naming another route or model,
   or more than one commit.
9. When a draft run's last attempt fails its document check, the runner first
   saves the whole tree as an attempt ref under `refs/stage2/attempts/`, then
   puts every changed path back except the change's `findings.md`, and the
   run's final message names that ref — so the next `draft <change>
   --stage2-off <reason>` run is not refused for pre-existing changes
   (phase-2a finding F-5).
   *Refuted by:* a leftover tree with no saved ref, a final message naming no
   ref, or a following `draft <change> --stage2-off <reason>` run refused with
   exit 2 for pre-existing changes.
10. When a draft run fails after its last allowed attempt — a failed call, a
    failed document check, or the GLM-key refusal on the third route — its
    final failure message names `--stage2-off` as the next step exactly when
    the run did not already carry the flag (phase-2a finding F-6).
    *Refuted by:* an exhausted chain whose message names no next step, a
    GLM-key refusal naming none, or a Stage-1 run's failure message naming the
    flag again.
11. When `--stage2-off` is passed to a verb other than explore, draft,
    implement and repair, the runner refuses with exit 2 before any call.
    *Refuted by:* any such verb starting a model call or exiting 0.
12. When the runner's own texts state which verbs accept `--stage2-off` — the
    module docstring, the flag's help text and `docs/WORKFLOW.md` — they name
    `draft` with Opus 5.5 at effort `xhigh`, and the workflow no longer says a
    draft takes no `--stage2-off`.
    *Refuted by:* any of those texts still excluding draft, naming another
    Stage-1 model for it, or the workflow keeping the old refusal sentence.
13. When the change's pull request carries the two held-text edits — the ADR
    0016 addendum and `AGENTS.md`'s `--stage2-off` sentence — decision 9 names
    the Stage-1 draft route (`--stage2-off` accepted for `draft`, Opus 5.5 at
    effort `xhigh` through `claude-code-plan`, the by-hand Opus draft of §3
    staying for a maintainer who drafts without the runner; `decisions.md`
    Q-1) and no longer says the draft has no Stage-1 route, and `AGENTS.md`
    names Opus 5.5 at effort `xhigh` for the draft.
    *Refuted by:* the merged pull request keeping the unamended decision 9 or
    the old `AGENTS.md` sentence while the code runs the route.

## Non-goals

- No automatic Stage-1 fallback inside the chain: after the GLM 5.3 attempt
  fails the run stops, and only the final message names the flag. The
  relaxation for writing attempts belongs to coding-harness-s9r /
  coding-harness-6ie, whose maintainer decision of 2026-10-16 is not yet
  implemented (`decisions.md`, [DETAIL] items, 2026-11-22).
- No change to the draft's guards, its per-attempt put-back rule (everything
  except `findings.md` and the one new ADR file) or its document-subset gate —
  that half of the bead is already merged (`decisions.md`, "What the research
  changed"). What changes is the failure tail after the last attempt, once no
  next attempt can use the tree (criteria 9 and 10).
- No route changes for explore, implement or repair — their Stage-1 routes
  keep their phase's §3 models (Haiku 5.5, Sonnet 5.5 at effort `medium`) —
  and no additional verb accepts the flag.
- No `## Runner route` block in a drafted `plan.md`: a Stage-1 draft's record
  is the `findings.md` audit line and the time entry, as for explore; that
  block belongs to implement and repair through the shared attempt loop, and a
  first draft's `plan.md` does not exist before the model writes it.
- No new ADR and no ADR edit beyond the one addendum to ADR 0016 decision 9
  (`adr_files` above); no change to `model-endpoints.yaml` — the
  `claude-code-plan` endpoint already declares `claude-opus-5-5` for the spec
  review — and the by-hand Opus 5.5 draft of §3 stays as it is.

## Protected areas

The held paths stay untouched by every model attempt: `provenance.yaml`,
`decisions/gates.yaml`, `decisions/answers/`, `docs/adr/`,
`model-endpoints.yaml`, `prompts/`, `templates/`, `AGENTS.md`, `README.md`,
`CLAUDE.md`, `.github/`, `.claude/`, `.beads/`. Two of them change in this
change's pull request all the same, as the orchestrator's bootstrap edits
after the accepted attempt, their texts verbatim in `plan.md`:
`docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md` gains the addendum
to decision 9, and `AGENTS.md`'s `--stage2-off` sentence names Opus 5.5 at
effort `xhigh` for the draft — both held by criterion 13. The prompts' Model
lines ("Where Stage 2 is off, Opus 5.5 … writes it") stay true: the Stage-1
route starts exactly that model at that effort. The shared attempt loop
`run_attempts` and the implement and repair route lists stay as they are.

## Definition of Done

- `make verify` green. Two debts stand in its way until they are paid, both
  named here so nobody meets them first at the gate: the claimed ADR edit owes
  five counted maintainer-answered records in `decisions.md` whatever the
  class (`scripts/check_interview_minimums.py`; Q-1 stands, four more are
  owed, and the maintainer's question window opens 2026-11-23 10:00), and the
  ADR addendum must be in the diff for the claim to be true.
- Moved in the same pull request: `docs/WORKFLOW.md` — the `draft` bullet of
  §4's verb list ("The runner is the only way") and the closing sentences of
  "The draft (phases 2, 2b and 3)"; the ADR 0016 addendum to decision 9 with
  the header's `updated:` moved (the orchestrator's bootstrap edit, verbatim
  in `plan.md`); `AGENTS.md` — the `--stage2-off` sentence of the Stage-2
  paragraph (the orchestrator's bootstrap edit, verbatim in `plan.md`).
- The pull request is a decision pull request: it changes a file
  `provenance.yaml` reserves for `human-decided`, so its title is
  `decide(draft-known-red): …`, it carries the label `decision`, and its body
  begins with the block from `.github/PULL_REQUEST_TEMPLATE/decision.md`
  (house rule 8).
- The protected areas untouched by the model attempts and the non-goals
  unbuilt, shown by the pull request's file list — the two held-path edits
  above are the orchestrator's, nothing else outside `scripts/stage2.py`,
  `tests/test_stage2.py`, `docs/WORKFLOW.md` and the change folder moves.
- Bead: the pull request closes coding-harness-83e, and its last commit
  carries the trailer `Closes-Bead: coding-harness-83e`.
- Special runs: none.

## Open decisions

None open. The scope decisions stand in `decisions.md` (the reasoned interview
skip, the four [DETAIL] items of 2026-11-22, and the maintainer's answer Q-1).
Freely revisable details decided here, each with its reason:

- **The class stays `bounded`.** The change wires an existing flag pattern
  into one more verb of an existing, readable flow and records a decision the
  maintainer has already made; the merged half of this bead
  (`draft-gates-only`) was `bounded` too. The ADR addendum does not reclass
  it: the workflow raises the interview debt to five "in whatever class the
  change carries" (`docs/WORKFLOW.md`, "Change classes"), and the
  `feature`-reading in `decisions.md`'s header line rests on exactly that
  non-reclassing consequence. The five-record debt is named in the Definition
  of Done either way.
- **The exact next-step text.** The exhausted chain's final message and the
  GLM-key refusal name the exact command `python3 scripts/stage2.py draft
  <change> --stage2-off <reason>`, mirroring implement's phrasing
  (`docs/WORKFLOW.md` §4: "the next step is `implement <change>
  --stage2-off`"); a Stage-1 run's failure message names the findings file and
  the saved ref, never the flag again.
- **The refusal message and the flag's help text** name draft in the verb
  list: "explore, draft, implement and repair".
