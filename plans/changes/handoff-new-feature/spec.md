---
title: "Spec — handoff-new-feature"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-in27
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-handoff, gate]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — handoff-new-feature

The gate requires complete research-swarm evidence for a new feature or
architectural change at the spec boundary, unless the maintainer explicitly
granted a reasoned interview exception (bead coding-harness-in27).
Research: `research.md`. Decision: `decisions.md#Q-1`.

## Problem

- The exploration identified the research-to-spec gate but left its code
  unread; the interview settled that this gate, rather than the session
  handover, is the subject. The dated research addendum checks the code:
  missing research and research without v2 records both return before the
  checker looks at the spec's class or the change's age. Consequently a new
  feature can pass as legacy without research (read at `a98c09c1`, 2026-11-04).
- The same early return never reads an interview exception. A legitimate
  waiver and an unnoticed omission are therefore indistinguishable in the
  gate output (research addendum, same revision and date).

## Terms

- **Complete run:** a `research-swarm/v2` run accepted as complete by the
  existing record validator; prose saying that exploration finished is insufficient.
- **Start day:** `research.md` frontmatter `date`, or the spec's `date` when
  research is absent. An existing research file with no readable start day
  does not authorize fallback to the spec. Review dates and archive names
  do not date creation.
- **New change:** its start day is strictly later than this repository's
  recorded adoption day for `research-handoff`. The adoption day in this
  repository is 2026-10-26, when research-swarm pull request #158 merged
  (`79a74f75d1e9ab7892388d643c4feea0d3ffeea2`).
- **Granted exception:** exactly one interview question record contains
  `research_swarm_exception: {granted: true, reason: "non-blank text"}`, an
  actual non-blank text answer, `answered_by: maintainer`, `status: answered`
  and non-blank context. The field records a grant; it never grants one.

## Acceptance criteria

1. When a new `feature` or `architectural` change has a spec, lacks a complete
   run and has no granted exception, the gate exits 1 and names that change's
   missing complete research, including when research is absent, unstructured
   or contains only valid incomplete runs.
   *Refuted by:* any of those cases exits 0, or is described as legacy.
   *Basis:* `decisions.md#Q-1`.

2. When a spec-bearing change without v2 evidence started on or before the
   adoption day, the gate reports a dated legacy exemption without imposing
   a retrospective swarm obligation.
   *Refuted by:* such a change fails solely for missing swarm evidence, or a
   changed review date or move to the archive removes its exemption.
   *Basis:* `decisions.md#Q-1`.

3. When a `bounded` change or `spike` has no v2 evidence, the gate reports
   its class-based exemption without calling it legacy.
   *Refuted by:* either class owes a swarm solely because it is new, or its
   exemption is labelled as an old change.
   *Basis:* `decisions.md#Q-1`; the existing class routing recorded in `research.md`.

4. When a new spec-bearing feature or architectural change lacks a complete
   run but has a granted exception, the gate reports that exception with the
   change, question identifier and reason instead of a missing-run finding.
   *Refuted by:* that missing-run condition still fails, the reason or question
   is hidden, or an agent/open/unanswered/contextless/reasonless record grants exemption.
   *Basis:* `decisions.md#Q-1`.

5. If evidence required to decide applicability or an exception is unreadable
   or ambiguous, the gate exits 3 with the affected input identified.
   *Refuted by:* missing or invalid adoption dates, required start dates,
   invalid/conflicting class declarations, duplicate exception fields or
   multiple exception records become success, legacy, or an uncaught traceback.
   *Basis:* `decisions.md#Q-1`; the existing unmeasured-input contract in `research.md`.

6. While an exception is recorded, malformed v2 evidence and obligations
   from every complete run retain their existing nonzero verdicts.
   *Refuted by:* an exception hides a malformed record, lost inventory item,
   unanswered research item, wrong neighbour header or invalid criterion basis.
   *Basis:* `decisions.md#Q-1`; existing handoff checks read in `research.md`.

7. When no spec exists, the gate retains its pre-spec pending behavior
   without claiming a missing run is a legacy exemption.
   *Refuted by:* absent or valid incomplete research alone blocks exploration,
   or malformed evidence passes because drafting has not begun.
   *Basis:* `decisions.md#Q-1`; the existing pre-spec boundary in `research.md`.

8. When the gate measures live or archived changes, including a named
   `--change` selection, the same applicability and exception rules hold
   without reading tracker state, Git history or the network.
   *Refuted by:* archiving bypasses a missing-run failure, selection measures
   a different change, or a passing offline fixture depends on an external service.
   *Basis:* `decisions.md#Q-1`; existing gate interfaces in `research.md`.

## Non-goals

- Changing research execution, model selection, class definitions, interview
  minimums, ADR decisions or the meaning of a complete v2 run.
- Session handovers, the Claude Code display and automatic handover thresholds.
- Generating exception answers, inferring grants from policy approval or
  migrating other changes' prose waivers without maintainer authority.
- A design document or ADR: this remains the interviewed `bounded` repair;
  phase 2b does not run for that class.

## Protected areas

The runner, shared inventory derivation, gate catalogue, CI placement,
prompts, templates, model configuration and existing ADRs remain unchanged.
Other change folders remain untouched, except one orchestrator record the maintainer authorised: the structured exception Q-6 in `plans/changes/go-access-point/decisions.md` (`decisions.md#Q-2`). Only the orchestrator may edit the
human-decided adoption record; no model attempt receives that edit.

## Definition of Done

- Targeted gate tests demonstrate red-before/green-after for the missing-run
  bypass, the legacy boundary and invalid exceptions; `make verify` is green.
- Updated together: `scripts/check_research_handoff.py`,
  `tests/test_research_handoff.py`, `tests/test_this_repository_adoption.py`,
  `decisions/adoption.yaml`, `docs/WORKFLOW.md`, this change's artifacts and the
  orchestrator's Q-6 record in `plans/changes/go-access-point/decisions.md`;
  the derived `plans/INDEX.md` is regenerated. No ADR is changed.
- The pull request file list shows protected areas and non-goals respected.
- The pull request closes the missing-research bypass task and its last
  commit carries `Closes-Bead: coding-harness-in27`.
- No model or network integration run is needed. A repository-wide failure
  exposed in another change is reported and blocks completion; it is not
  silently waived to obtain green verification.

## Open decisions

None open. The following reversible implementation details are chosen here
and recorded so they remain visible; none is a maintainer answer.

- [DETAIL] Reuse the per-repository adoption record and reader. Interpret its
  date at day precision, like the existing interview gate: the adoption day
  itself belongs to the old stock. This avoids inventing timestamps or
  adding Git-history access to an offline gate.
- [DETAIL] Prefer the research start date to the later spec date, preserving
  an exploration begun before adoption when its spec is written afterward.
  Old stock may lack a class; a post-adoption spec must declare one of the
  four classes. A research class, where present, must agree with the spec.
- [DETAIL] Use the explicit exception field defined above, not prose matching;
  missing/false grants and incomplete authorizations do not exempt a change,
  while malformed field types or contradictory records are unmeasurable.
  An exception waives only absence of a complete run.
- [DETAIL] Allow two hours of phase 4 including repairs; stop at that limit.
