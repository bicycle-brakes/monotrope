---
title: "Decisions — time-records-data"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-v6vk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# time-records-data — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a
reasoned skip below). Reason for the class: one writer command for time
records and its use by the runner and the orchestrator; readers count only its
entries; no gate, ADR or architecture changes.

## SKIP · interview

status: skipped
reason: the bead (coding-harness-v6vk) states the remedy — one writer (for example `harness time-log`) used by the runner and the orchestrator alike, `plan.md` time lines written only through it, and `make report` and other readers counting only those entries — and the maintainer agreed on 2026-10-29 after the run report needed five loop rows on parsing free-text time records (L1-1, L3-1, L4-1, L5-1, L6-1 of coding-harness-o2yc); no question remains that only the maintainer can answer. In the context of time records in plan.md, facing readers that guessed at free-text lines, we keep the maintainer's agreement of 2026-10-29 and give every record one writer and one fixed line format, to achieve readers that parse only that format, accepting that older prose lines stay readable to people and unread by tools. — 2026-10-31

## Details for the draft

[DETAIL] **The direction is the writer side.** The record stays a line in
`plan.md` "Time used", in the runner's existing fixed format; the new command
writes it for the orchestrator too. No separate store (JSON, database).
Reason: the bead names one writer for plan.md lines; the research found no
other store, and `make report` already reads the runner's format.

[DETAIL] **Old lines are not rewritten.** Reason: they are history; the
report already shows non-format lines as unread (PR #277).

[DETAIL] **The entry point lives with the existing harness CLI**
(`scripts/harness.py`), not as a new script. Reason: one command surface;
the bead's own example is `harness time-log`.
