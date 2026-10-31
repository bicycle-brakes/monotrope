---
title: "Decisions — draft-gates-only"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-77qj
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# draft-gates-only — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a
reasoned skip below). Reason for the class: the draft verb's post-run check
calls the existing `docs` gate job instead of the full `make verify`; the job
itself was decided in its own pull request; no ADR or architecture changes.

## SKIP · interview

status: skipped
reason: the bead (coding-harness-77qj) states the remedy — the draft verb runs only the document gates and leaves the full suite to implement, repair and the orchestrator — and the maintainer decided on 2026-10-29 at about 14:05 UTC to schedule it as two steps: first the decision PR adding a `docs` gate job to decisions/gates.yaml (merged as PR #280), then this draft-verb change; no question remains that only the maintainer can answer. In the context of the draft verb's post-run check, facing a full make verify of about 12 minutes after a run that writes only spec, design and plan documents, we keep the maintainer's two-step plan of 2026-10-29 and let draft run the `docs` job, to achieve shorter draft cycles and a freer verify slot, accepting that code-level gates run only from implement on. — 2026-10-31

## Details for the draft

[DETAIL] **The draft verb runs `verify_all.sh --job docs`** under the same
machine admission as every runner check. Reason: the job exists (PR #280),
and the admission is how every check queues since PR #284.

[DETAIL] **The step limit stays `VERIFY_SECONDS`.** Reason: no measurement
asks for a shorter bound; one limit is simpler, and a docs run ends early.

[DETAIL] **The docs subset's membership is out of scope.** Reason: it was
decided with PR #280; this change only calls it.

[DETAIL] **The `--report` asymmetry the research names stays out.** Reason:
it is a reporting detail of the job mechanism, not of the draft verb; it gets
a bead of its own if it matters.
