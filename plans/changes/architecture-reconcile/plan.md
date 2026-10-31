---
title: "Plan — architecture-reconcile"
category: plan
status: draft
implementation_status: none
created: 2026-10-31
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-190
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, architecture, reconciliation]
---

# Plan — architecture-reconcile

```text
For you:     One dated comparison shows which architecture promises hold, remain open or were amended.
Done when:   Target sections, M0–M4/W0–W2 and every original gap have dated evidence or an explicit reading limit, discrepancies have proposed remedies, and CI is green.
Appetite:    2 hours of phase 4, repairs included; stop at the limit.
Not now:     Implementing gaps, changing decisions, rewriting the original architecture documents or updating tracker status.
Pre-mortem:  suppose it failed: most likely because file existence was mistaken for proof that a promise works.
Starts unless you say stop.
```

## Files and steps

1. Create `docs/research/2026-10-31-architecture-reconciliation.md` with research
   frontmatter, provenance and the baseline
   `b58c72e75af3283f4cc9e39148ecfb02642026f9` (2026-10-31); explain snapshot
   limits before the tables. Use source links/anchors, original obligation,
   disposition, evidence and residual gap/remedy as columns; each row inherits
   the declared commit/date unless an explicitly dated tracker snapshot differs.
2. In that file, map every main target section: Outcome and boundaries;
   Decision continuity; Source of truth and execution topology; Run limits,
   context and recovery; Trust and enforcement; Human planning and attention
   support; Acceptance scenarios. Identify relevant subsection obligations
   within each row; split rows where evidence or disposition differs. Read
   `docs/architecture/2026-09-17-omnigent-first-target.md` as the contract and
   `docs/architecture/target-architecture.md` only as its superseded predecessor.
3. Add delivery rows for M0–M4 and W0–W2 from
   `docs/architecture/2026-09-17-implementation-plan.md`, retaining their entry,
   exit and stop obligations in the assessment. Add one row per original gap
   in `docs/architecture/2026-09-17-gap-analysis.md`, preserving priority and
   gap title; there are 26 at the baseline. Read applicable accepted ADRs
   through ADR 0021, especially 0004–0007, 0009–0010 and 0011–0021, as
   amendment evidence; distinguish decisions from proof of delivery.
4. Read evidence in the baseline's `Makefile`, `scripts/verify_all.sh`,
   `decisions/gates.yaml`, `scripts/check_decision_continuity.py`,
   `tests/test_stage2.py`, `docs/WORKFLOW.md`, `model-endpoints.yaml`,
   `tools/omnigent/`, `templates/`, `prompts/`, `scripts/kit/manifest.yaml`,
   `docs/governance/quality-gates.md` and `docs/governance/gate-catalog.md` as
   applicable to each claim. Search for claimed paths before declaring absence;
   do not equate a test definition with an executed test. Record unread or
   unrun evidence honestly, with the reason. Do not run live qualification.
5. Obtain cited gap beads' title/status via `scripts/bead_render.py` in a
   single reader process and record the snapshot date/source. If access would
   leave the authorized reading boundary or the renderer is unavailable,
   write "not read" and the limitation. No direct Dolt reads or tracker writes.
   Add discrepancy/remedy rows for routing, licence, M0 and onboarding/scan;
   compare `LICENSE`, `COMMERCIAL.md`, `README.md` and
   `docs/research/2026-10-20-public-readiness.md` without adopting a remedy.
6. Update `plans/changes/architecture-reconcile/findings.md` with review/check
   evidence, candidate remedies and limits; preserve prior entries. Update
   `plans/changes/architecture-reconcile/spec.md` and
   `plans/changes/architecture-reconcile/plan.md` only for truthful lifecycle,
   verification and time records, never to weaken criteria. The orchestrator
   regenerates `plans/INDEX.md` after accepting the attempt. No files are deleted.

## Verification

Review the tables against the ledger, then run the applicable checks verbatim:

```sh
python3 scripts/check_interview_minimums.py --change architecture-reconcile
python3 scripts/check_research_handoff.py --change architecture-reconcile
python3 scripts/check_criterion_ledger.py
python3 scripts/check_docs.py --base docs/research
python3 scripts/check_docs.py --base plans/changes/architecture-reconcile
python3 scripts/plans_registry.py --index
python3 scripts/plans_registry.py --check
```

The orchestrator runs the last two commands after acceptance, with authorized
tracker access. `python3 scripts/validate_change_artefacts.py --check` is owed
by the prompt but unavailable at the baseline; do not create its implementation.
No new tests are warranted for this evidence report. Local `make verify` is
skipped under the text-only rule; CI remains the completion gate. Record any
failing or unmeasured check rather than repairing unrelated work or relaxing it.

## Criterion ledger

- 1: not a test — phase-6 review reads the report header and baseline; an absent date or full commit refutes it.
- 2: not a test — phase-6 review maps each target contract heading to report rows; an omitted section or unsplit mixed verdict refutes it.
- 3: not a test — phase-6 review checks the M0–M4/W0–W2 inventory against the source plan; an omitted step or unqualified M0 prerequisite refutes it.
- 4: not a test — phase-6 review matches all 26 original gap titles at the baseline one-to-one; an omitted or conflated gap refutes it.
- 5: not a test — phase-6 review follows each row's evidence at its declared commit/date; unsupported runtime claims or unread-as-absent wording refute it.
- 6: not a test — phase-6 review compares bead assertions with the dated access-point snapshot or explicit access limit; inferred status or closure-as-delivery refutes it.
- 7: not a test — phase-6 review checks all four discrepancy topics against separate proposed remedies; a missing contradiction or self-adopted decision refutes it.
- 8: not a test — phase-6 review inspects the diff against the spec's protected areas; a source, mechanism or permission edit refutes it.

## Boundaries and route

Read `spec.md` with this plan. No design or ADR draft is due for `bounded`.
Exploration used Stage 2, GLM 5.3 Flash, on 2026-10-31; no Stage-1 fallback
was recorded. Preserve `decisions.md` and all protected paths from the spec.
No held-path edit is planned; any necessary policy or mechanism repair is
returned to the orchestrator as a finding, outside this accepted attempt.

## Runner route — 2026-10-31

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-10-31 15:49:01–16:45:15 UTC, 3373 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
2026-10-31 17:22:00–17:49:13 UTC, 1633 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 17:49:21–18:31:33 UTC, 2532 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 18:31:39–18:45:11 UTC, 811 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-31 19:06:47–19:21:08 UTC, 862 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner

Appetite: 2 hours of phase 4, repairs included. Used by 2026-10-31 19:40 UTC: 3373 + 1633 + 2532 + 811 + 862 s, about 2 h 34 min — over the stop by about 34 minutes, a large part of it spent waiting for the shared verify slot while five lanes ran. Recorded by the orchestrator (review row L2-3); remaining work: the review loop to a clean round, phase 6 and the pull request. Continuing past the stop is the maintainer's call; the structural remedy is the runner stop at the appetite (bead coding-harness-uxa9).
2026-10-31 19:54:21–20:56:58 UTC, 3757 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
