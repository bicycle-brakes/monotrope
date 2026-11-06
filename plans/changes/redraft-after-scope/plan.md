---
title: "Plan — redraft-after-scope"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-y0qm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, spike, scope]
---

# Plan — redraft-after-scope

```text
For you:     An evidence-based recommendation on preventing work from outrunning its recorded scope.
Done when:   A sourced report compares three remedies, proposes a bounded next step and states its limits; review and CI pass.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Adopting a remedy, changing workflow rules or implementing enforcement.
Pre-mortem:  suppose it failed: most likely because a protected-area violation is mistaken for a scope-changing answer.
Starts unless you say stop.
```

## Files and steps

1. Append dated evidence to `plans/changes/redraft-after-scope/research.md`:
   retain earlier exploration, distinguish its observations from the later
   interview skip, and check each case against source paths and commits.
   For the prompt incident, inspect `git show b04c119d` and the spec and
   decisions at that revision under `plans/changes/handoff-new-feature/`;
   these are historical inputs, not files to restore or edit. Separate the
   authorized cross-folder exception from the forbidden prompt edit.
2. Create `docs/research/2026-11-06-redraft-after-scope.md` with required
   research frontmatter and sections Evidence, Comparison, Proposed procedure,
   Recommendation and Limits. Trace guard-test, research-swarm, sol-effort and
   loop-until-clean through the source paths in research; cite a revision or
   date for every case, and mark inaccessible evidence “not read”.
   Compare redrafting, protected-area checking and current review practice
   in one matrix: trigger, detection boundary, actor, cost and residual risk.
   Replay every case against all three; distinguish demonstrated behavior
   from hypothetical prevention. Describe authorization, retained answers,
   dated evidence, spec/design/plan alignment, findings dispositions and
   rechecks without waiving interview or swarm handoff obligations. End with
   a justified recommendation, one uncovered case and proposed follow-up
   paths/class/ADR implications, leaving adoption to the maintainer.
3. Review the report against each criterion; update this change's
   `plans/changes/redraft-after-scope/plan.md` with actual evidence and time
   through the existing writer, and its
   `plans/changes/redraft-after-scope/findings.md` with review dispositions
   through the orchestrator/runner. No file deletion is planned.
   `plans/changes/redraft-after-scope/spec.md` remains the yardstick; do not
   relax it or change `decisions.md` to accommodate a preferred remedy.
4. Orchestrator/runner only: regenerate `plans/INDEX.md` for the new planning
   artifacts through the registry; the implementation attempt must not
   hand-edit derived files or any held path. Review the final file list and
   let the runner own its verification and commit.

## Criterion ledger

- 1: not a test — source review checks all five cases against dated paths/revisions; a missing case, unsupported claim or false absence fails
- 2: not a test — review checks the common comparison matrix and case replays; an omitted remedy, dimension or unsupported prevention claim fails
- 3: not a test — review checks the proposed procedure against retained answers and existing phase/handoff rules; conflation or silent waiver fails
- 4: not a test — review traces recommendation, uncovered case and concrete follow-up; an unsupported conclusion or missing boundary fails
- 5: not a test — final file-list and content review checks the spike boundary; changed enforcement/doctrine or a fabricated answer fails

## Verification

```sh
python3 scripts/check_interview_minimums.py --change redraft-after-scope
python3 scripts/check_criterion_ledger.py
python3 scripts/check_frontmatter_current.py
git diff --check
```

The orchestrator regenerates the index with
`python3 scripts/plans_registry.py --index` before its registry/CI checks.
The requested `python3 scripts/validate_change_artefacts.py --check` is not
available at draft baseline `b454eed6` (2026-11-06); do not invent a substitute
or claim it passed. Local `make verify` is skipped for this Markdown-only
spike; CI remains the gate, and the draft runner performs its own checks.
No Stage-1 Explore fallback is recorded: research names a successful Flash
exploration via `glm-5.3-flash` on 2026-11-06.

## Do not touch

No scripts, tests, workflow doctrine, prompts, templates, ADRs, governance,
endpoint or harness settings, tracker data or other change folders. No held
path needs a bootstrap edit. No `design.md` is due for class `spike`, and
there is no plan template in `templates/`; this plan follows phase 3's form.

## Runner route — 2026-11-06

Stage-1 route: implement · model claude-sonnet-5-5 · reason: spike: on 2026-11-06 Flash implement was accepted with an empty diff on both spikes tried (beads bvy and xay1; bug coding-harness-te7q), so this spike goes to Sonnet first.

## Time used

2026-11-06 04:39:21–05:48:25 UTC, 4144 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
