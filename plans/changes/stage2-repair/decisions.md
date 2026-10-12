---
title: "Decisions — stage2-repair"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-g2f
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, repair]
---

# Stage-2 repair verb — Decisions

Phase 1a for bead coding-harness-g2f, on 2026-10-12, after the exploration in
`research.md`. Today the review findings the orchestrator takes are repaired
by a Claude Sonnet sub-agent; the change adds a runner verb that hands them to
GLM 5.3 (not Flash; maintainer, 2026-10-12, in the bead).

## Q-1 · Which findings one repair call takes

asked: 2026-10-12
answer: A — both kinds in one call: every loop row of phase 4b whose Status is `taken`, and every phase-6 finding the orchestrator has taken.
answered_by: maintainer
status: answered

In the context of review findings that sit in two places (the loop record and
the phase-6 table of `findings.md`), facing the choice between repairing both
in one call, only the loop rows, or one row per call, we decided on both kinds
in one call to achieve that the verb replaces what the Sonnet sub-agent does
today, accepting that a phase-6 finding needs a mark that the orchestrator
took it. — 2026-10-12

## Q-2 · How a phase-6 finding is taken for repair

asked: 2026-10-12
answer: A — the same Status words as the loop: `taken — <reason>` or `rejected — <reason>` in the phase-6 table of `findings.md`; the verb repairs only `taken` rows, and after the repair the Status reads `fixed — <test>`.
answered_by: maintainer
status: answered

In the context of phase-6 findings that carry only `open`, facing the choice
between the loop's Status words, an automatic pick by severity, or a separate
list, we decided on the loop's words in the existing Status cell to achieve
one vocabulary and one column for every decision, accepting that each phase-6
row needs an explicit orchestrator decision before the verb takes it. —
2026-10-12

## Q-3 · Who starts the re-check after a repair

asked: 2026-10-12
answer: A — the orchestrator, with the existing verbs: the loop's next round for loop rows, `review` (Codex) for phase-6 findings; the repair verb ends with its checkpoint commit.
answered_by: maintainer
status: answered

In the context of the flow reviewer reports → orchestrator decides → GLM
repairs → reviewer re-checks, facing the choice between a separate re-check
started by the orchestrator and one the repair verb starts itself, we decided
on the orchestrator starting it with the existing verbs to achieve that each
verb does one thing and the loop's round budget counts as today, accepting
one more command per cycle. — 2026-10-12

## Q-4 · Does the change need an ADR

asked: 2026-10-12
answer: A — yes: a short new ADR that amends ADR 0011: the repair of taken findings runs on GLM 5.3; a reviewer never repairs its own findings.
answered_by: maintainer
status: answered

In the context of ADR 0007 and ADR 0011, which route every stage-2 phase to a
model and name none for repairs, facing the choice between a new ADR and an
entry in `docs/WORKFLOW.md` alone, we decided on a short ADR amending ADR 0011
to achieve that the model routing stays where the ADRs keep it, accepting the
ADR minimum of five answered questions. — 2026-10-12

## Q-5 · Findings no test can prove

asked: 2026-10-12
answer: A — GLM repairs text-only findings too; their Status reads `fixed — not a test — <reason>`, the form of ADR 0013's criterion ledger; a finding on code still needs a test that was red first.
answered_by: maintainer
status: answered

In the context of findings on comments, plans or specs (the loop rows L2-1,
L2-2 and L3-1 of change provenance-location), facing the choice between
letting GLM repair them with a stated reason and keeping them with the
orchestrator, we decided on GLM repairing them with `not a test — <reason>`
to achieve that one call clears all taken rows in a form already known,
accepting that a text repair is proven by the re-check, not by a test. —
2026-10-12

## Decisions taken by the agent

[DETAIL] Class `feature` with an ADR: a new runner verb, its tests, doctrine
text and a new ADR; five answered questions meet the minimum.

[DETAIL] The attempt sequence follows the bead and `implement`: one GLM 5.3
attempt, one GLM 5.3 repair attempt carrying the first attempt's
diagnostics, then one Sonnet 5.5 Stage-1 fallback; `--stage2-off [REASON]`
runs the Sonnet attempt alone, as for `implement`. A leak-check BLOCK stops
without fallback.

[DETAIL] The verb reuses `implement`'s guards as they are — preflight against
`model-endpoints.yaml`, the leak check of the exact prompt, the credential
clean-up, `make verify` through `verify_attempt`, the baseline restore and the
one checkpoint commit — rather than a second copy.

[DETAIL] `model-endpoints.yaml` keeps `glm-5.3` as declared; only the entry's
remark, which names the work verbs, gains the repair verb (its pinning test
moves with it).
