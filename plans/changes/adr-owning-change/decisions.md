---
title: "Decisions — adr-owning-change"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-afa
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, gates, adr]
---

# ADR owning change — Decisions

Phase 1a for bead coding-harness-afa, on 2026-10-12. The gate
interview-minimums infers an ADR's owning change from the diff; pull request
#126 carries an interim rule for that inference (a folder touched through
`plan.md` alone is no owner; beside other owners the ADR text decides). This
change replaces the inference with an explicit statement.

## Q-1 · Where the owning change is stated

asked: 2026-10-12
answer: A — the change claims the ADR files it creates or changes in its own spec header.
answered_by: maintainer
status: answered

In the context of an ADR edit that must be attributed to exactly one change
folder, facing that `owner:` in an ADR header already names a role and that
the answer-file format (schema_version 1) is frozen "not now", we decided that
a change names the ADR files it creates or changes in the header of its own
`spec.md`, to achieve an attribution that holds per edit — a later change that
amends an ADR claims that amendment itself — without touching the ADR or the
answer-file format, accepting that the claim lives in the change folder, not
in the ADR a reader opens. — 2026-10-12

## Q-2 · An ADR edit no change claims

asked: 2026-10-12
answer: A — the gate blocks and names the remedy; the inference from the diff goes, the interim rule of pull request #126 with it.
answered_by: maintainer
status: answered

In the context of a diff that changes a file under `docs/adr/` which no
change's spec header claims, facing the choice between one explicit rule and
the explicit rule beside the old inference, we decided that the gate reports a
finding that names the remedy (claim the file in the spec header of your
change) and no longer infers an owner from the diff, to achieve one rule
instead of two, accepting that even a typo fix in an ADR needs a change folder
with a spec — which the five-question duty for every ADR edit already asks
today. — 2026-10-12

## Q-3 · The ADR question, and whether the gate travels

asked: 2026-10-12
answer: Yes to both — the rule gets an ADR of its own, and it travels with the kit together with the interview-minimums gate ("Das soll auch reisen, beides").
answered_by: maintainer
status: answered

In the context of a rule that so far would hold in this repository alone —
the interview-minimums gate has no entry in `scripts/kit/manifest.yaml` —
facing that a rule for other repositories is what an ADR records, we decided
that the change answers the ADR question yes and that the gate travels with
the kit, to achieve that every instance attributes an ADR edit the same way,
accepting a decision pull request and five interview records for this change.
The answer is recorded with `scripts/harness.py decide adr` once the spec
header names the change; on 2026-10-12 the command refused, because no change
anchor exists before phase 2. — 2026-10-12

## Q-4 · What travels to an instance

asked: 2026-10-12
answer: A — the whole interview-minimums gate travels, with a cut-off date per repository.
answered_by: maintainer
status: answered

In the context of an interview-minimums gate that measures two things — the
interview minimums per change class and the attribution of an ADR edit —
facing that an instance such as LakeSwitch has changes begun before it takes
the kit, we decided that the whole gate travels and that changes begun before
the day an instance adopts it are exempt, to achieve one equally strict
workflow in every repository without breaking the stock on adoption, accepting
that each instance must record its adoption date. — 2026-10-12

## Q-5 · The reverse direction: answer and ADR files agree

asked: 2026-10-12
answer: A — the gate checks both directions: an answer yes needs at least one claimed ADR file, an answer no admits none.
answered_by: maintainer
status: answered

In the context of the gap `docs/WORKFLOW.md` §2 names — nothing checks that a
`yes` to the ADR question is followed by an ADR — facing that the spec-header
claim makes the check cheap, we decided that the gate also checks that an
answer `yes` comes with at least one claimed ADR file and an answer `no` with
none, to achieve that the recorded answer and the ADR files of a change cannot
drift apart, accepting that a change like criterion-test-ledger (answer no,
ADR 0013 written at the maintainer's request) goes red after the cut-off until
its answer is corrected in a decision pull request. — 2026-10-12

## Decisions taken by the agent

[DETAIL] Class `feature`: the change adds a header field and tightens an
existing gate; the ADR answer (Q-3) raises the interview minimum to five, met
by Q-1 to Q-5. Revisable in the spec.

[DETAIL] The field's name is left to the spec (working name `adr_files`, a
list of paths under `docs/adr/`); it must not be `owner`, which names a role.

[DETAIL] Where an instance records its adoption date (Q-4) is left to the
spec; bead coding-harness-wpv asks the same for the criterion-ledger gate, and
the spec reads it before choosing, so both gates use one mechanism.
