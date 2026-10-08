---
title: "Spec — interview-minimums"
status: draft
implementation_status: none
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-6yg
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: cline, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, interview, gates, workflow]
class: feature
appetite: 6
change: interview-minimums
adr_question: {proposed: "no", reason: "prompts, one gate script and documentation follow the existing check_adr_answers pattern; no new subsystem and no interface break"}
---

# Spec — `interview-minimums`

The goal in one sentence: after this change the phase-1a interview is
mandatory where the maintainer set minimums — features, spikes and ADR
changes — and a gate counts it, so an uninterrogated feature can no longer
reach a green tree (bead `coding-harness-6yg`). Research: `research.md`.
Decisions: `decisions.md`.

## Problem

Phase 1a is voluntary today, and nothing measures it:

- `prompts/01a-interview.md` opens with "**Optional**, and called by a human";
  `docs/WORKFLOW.md` (§2, after the phase table) and `AGENTS.md` ("The
  workflow in one screen", row 1a) say the same.
- A `feature` can merge with no interview at all: no gate counts questions in
  `decisions.md` (research, "What is not there"). The ADR question is held by
  the `adr-answers` gate — whether the human behind the change was *asked*
  anything first is not.
- The gap is known and named: `docs/journal/handover/2026-10-08-runner-derived-files.md`
  closes with "mandatory feature/ADR interviews (at least three/five
  substantive questions) are not implemented by this PR", and
  `plans/changes/runner-derived-files/decisions.md` already writes "Feature/ADR
  minimums do not apply" in anticipation of a rule that does not exist.

## Terms

- **Interview record** — one question block in `decisions.md`: a `## Q-<n> ·`
  heading with the fields `asked`, `answer`, `answered_by`, `status`, then the
  Y-statement. The format's one home is `prompts/01a-interview.md`
  ("What you write").
- **Skip record** — the recorded end of an interview without questions: a
  `## SKIP · interview` block whose fields are `status: skipped` and a
  `reason:` line with the one-sentence justification. A skip without its
  reason is not a skip record.
- **Counted record** — an interview record with `status: answered`,
  `answered_by: maintainer`, and a stated question and answer, whose question
  id has no earlier *counted* record in the same file: an earlier record that
  does not count — an agent's answer, an open status — does not spend the id
  (loop row L1-1); a block without the question and answer fields is not an
  interview record, whatever its other fields claim (phase-6 row F-12).
- **Owning change** — the change whose folder the measured diff touches: a
  `plans/changes/<name>/` path among the changed files. ADR changes are
  attributed to the owning change; a diff that touches `docs/adr/` and owns
  no change, or more than one, is a finding, never a silent pass (F-5).

## Acceptance criteria

1. When a change's spec says `class: feature` and its `decisions.md` holds
   fewer than three counted records, `scripts/check_interview_minimums.py`
   exits non-zero and names the change.
   *Refuted by:* the check exits 0 on such a tree.
2. When the measured diff changes a file under `docs/adr/` — committed,
   staged against the index, unstaged, untracked, or renamed out of that
   directory — the owning change owes five counted records whatever its
   class and however old its folder: the
   cut-off exempts a folder's own class minimums, never a new ADR edit (loop
   row L1-3). A diff that touches `docs/adr/` and owns no change folder, or
   more than one, is a finding and the check exits non-zero.
   *Refuted by:* a `bounded` change with a staged new ADR and four counted
   records exits 0; a bare ADR edit outside any change folder exits 0; an
   ADR edit attributed to a pre-cut-off folder exits 0; a staged ADR edit
   whose working file matches the base goes unseen.
3. When a change is both a feature and an ADR change, five counted records
   satisfy both minimums; the check never demands the sum.
   *Refuted by:* the check demands eight.
4. When records carry `answered_by: agent`, or `status: open`, or repeat a
   question id already counted earlier in the same file, they do not count
   toward any minimum. The gate counts records; whether counted records are
   substantively distinct questions is the phase-6 review's judgment
   (decisions.md G-4).
   *Refuted by:* three agent-answered records satisfy a feature's minimum;
   a repeated `Q-1` raises the count.
5. When a change's class is `bounded` and its diff touches no ADR path, the
   check accepts it exactly when its `decisions.md` holds at least one
   counted record or a skip record with a reason; when the class is `spike`
   and no ADR path is touched, three counted records — the topics learning
   goal, time budget, expected outcome — or a skip record with a reason.
   *Refuted by:* a `bounded` change with an empty `decisions.md` exits 0.
6. When the check cannot build its comparison base — no merge base with
   `origin/main`, or a shallow clone without the history it needs — it exits
   3 and says so; it never exits 0 on a state it could not read.
   *Refuted by:* exit 0 from a repository without history.
7. When HEAD sits on the main line — a genuine `main` checkout, or the
   hosted run that pushed `main` (`GITHUB_REF: refs/heads/main`) — the
   comparison base is the first parent, so the merged landfall is still
   measured (loop row L1-2). Everywhere else — a named feature branch, an
   older ancestor, any other state — it is the merge base with
   `origin/main`; on a named branch, HEAD equal to the merge base proves
   nothing was committed beyond main, so uncommitted work is still measured.
   *Refuted by:* exit 0 after a merge onto `main` because the base diff came
   out empty; a newly begun branch at `origin/main` wrongly charged with
   main's previous ADR landfall (phase-6 rows F-14, F-15).
8. When a change's spec `date` is not later than the cut-off constant, the
   check skips it — quoted, commented and unparseable dates do not exempt a
   change, they measure it (phase-6 row F-10); a change dated after the
   cut-off owes its minimum also once archived (phase-6 row F-11). The
   constant is the merge date of this change and stands in the gate script
   and in `docs/WORKFLOW.md`.
   *Refuted by:* a change dated the cut-off day itself turns red; an
   archived post-cut-off feature with no interview exits 0; a quoted date
   exempts a subject change.
9. When phase 2 runs, its prompt names the interview check as part of the
   spec gate: the spec passes only when the check is green for this change
   and no `[DECISION]` is open.
   *Refuted by:* `prompts/02-spec.md`'s gate line without the interview check.
10. When the tree is verified, `decisions/gates.yaml` declares the gate
    `interview-minimums` (job verify, enforcement block, placement both), the
    regenerated `.github/workflows/ci.yml` matches it, and a test asserts the
    declaration exists — deleting the entry turns that test red.
    *Refuted by:* the test green with the entry removed from `gates.yaml`.
11. When the documentation is read, `docs/WORKFLOW.md` (phase table, the
    paragraph after it, the "Change classes…" section, the stage-1 table) and
    `AGENTS.md` (row 1a) state the mandatory duty with the minimums, and no
    place still calls the interview optional without the class limits.
    *Refuted by:* a reader of `AGENTS.md` alone concludes the interview is
    voluntary for a feature.
12. When the spec gate invokes `--change <name>` and no change folder of
    that name exists under `plans/changes/`, the check exits non-zero — a
    typo cannot pass silently (loop row L1-6).
    *Refuted by:* exit 0 for a name no folder carries.

## Non-goals

- No `scripts/validate_change_artefacts.py`: that validator is bead
  coding-harness-jc3's work; this change waits for nothing and builds on the
  gates that exist (`plans_registry.py --check`, review, the new gate).
- No change to the `adr-answers` gate or to `scripts/harness.py decide adr`;
  the ADR answer keeps its own flow.
- No template for `decisions.md`: the question record's one home is
  `prompts/01a-interview.md` — a second place describing what phase 1a
  produces is exactly what the no-second-place rule refuses
  (`scripts/new_change.py`, AK-2 reasoning).
- No changes in `lakeswitch-ai` or `portfolio-agentic-engineering`; the
  tracker write-guard (D-60) is bead coding-harness-36z's subject.
- No `design.md`: this change reuses the existing gate pattern
  (`check_adr_answers.py`), the existing diff machinery (`stage2.change_diff()`
  states) and the existing gate list — nothing architectural is decided, so
  the feature runs without phase 2b per `prompts/02b-design.md`.

## Protected areas

- The worktrees of parallel sessions, above all `.claude/worktrees/stage2-mimo`
  (OpenCode's) and `mimo-watch-audit` (detached, audit-only).
- `docs/adr/` — `human-decided` in `provenance.yaml`; this change creates no
  ADR.
- `decisions/answers/` — `human-decided`; exactly one file is written there,
  `decisions/answers/interview-minimums/adr.yaml`, and only through
  `python3 scripts/harness.py decide adr` from the maintainer's stated answer
  (decisions.md G-3; ADR 0008). Nothing else in that tree.
- `.beads/` — tracker writes only through `tools/bd`, pushed before git.

## Definition of Done

- `verify` green.
- Moved in the same pull request: `prompts/01a-interview.md`,
  `prompts/02-spec.md`, `docs/WORKFLOW.md`, `AGENTS.md`,
  `scripts/check_interview_minimums.py`,
  `tests/test_check_interview_minimums.py`, `decisions/gates.yaml`,
  `.github/workflows/ci.yml` (regenerated), and
  `decisions/answers/interview-minimums/adr.yaml` (the recorded ADR answer,
  carried by this decision pull request) — each by name, or "none": none
  beyond these.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes `coding-harness-6yg`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-6yg`
  (`prompts/07-commit.md`).
- Special runs: none.

## Open decisions

None open. The four `[AMBIGUITY]` rows of the spec review are settled by the
maintainer and recorded as `decisions.md` Q-5 to Q-8; the ADR answer is
recorded (`decisions/answers/interview-minimums/adr.yaml`, answer "no") and
takes effect when this decision pull request merges.
