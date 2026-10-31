---
title: "Decisions — repair-targeted-check"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-gxwg
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# repair-targeted-check — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a
reasoned skip below). Reason for the class: the runner's repair verb runs a
narrower post-run check; one full `make verify` before phase 6 stays; no gate
definition, ADR or architecture changes.

## SKIP · interview

status: skipped
reason: the maintainer chose on 2026-10-30, for the lock bottleneck, option 2 (a targeted check after a hand repair: the touched and linked tests, ruff and the gates the touched files feed; one full make verify before phase 6 and before a pull request leaves draft; PR #291), and this bead (coding-harness-gxwg) carries the same rule to the runner's repair verb; no question remains that only the maintainer can answer. In the context of the repair verb's post-run check, facing a full make verify of about 12 minutes after every runner repair, we keep the maintainer's rule of 2026-10-30 and apply it to the runner too, to achieve shorter repair cycles, accepting that a repair is fully verified only once before phase 6. — 2026-10-31

## Details for the draft

[DETAIL] **The full verify stays before phase 6.** The repair verb's
post-run check becomes targeted; `stage2.py review` (phase 6) refuses unless
a full `make verify` is green at the head. Reason: the rule of PR #291.

[DETAIL] **A change under `prompts/` still owes a full verify.** Reason: the
same rule; prompt changes have no linked tests.

[DETAIL] **The linked tests come from the working tree.** `touch_map.py`
reads committed objects only (research); the repair's touched paths come from
the runner's `changed_paths`. Reason: a repair is checked before it commits.
