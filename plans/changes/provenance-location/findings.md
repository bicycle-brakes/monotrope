---
title: "Findings — provenance-location"
category: findings
status: draft
implementation_status: partial
date: 2026-10-12
created: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-3ar.1
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — provenance-location

Stage-2 call, 2026-10-12: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 360 files, 895 commits, 12 rules.

Stage-2 call, 2026-10-12: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 361 files, 897 commits, 12 rules.

Stage-2 call, 2026-10-12: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 361 files, 900 commits, 12 rules.

Stage-2 call, 2026-10-12: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 361 files, 902 commits, 12 rules.

Stage-2 call, 2026-10-12: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 361 files, 903 commits, 12 rules.

Stage-2 call, 2026-10-12: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 361 files, 904 commits, 12 rules.

## Phase 6 — Codex, 2026-10-12

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `scripts/harness.py:93` | A sole map at either supported location containing `paths: 1` or `paths: true` raises an uncaught `TypeError` in both invocation modes. The command exits 1 without a refusal message; a mapping without the answers entry must refuse with exit 2 and name the selected map. [AC 5] | Codex | open | — |
| F-2 | BLOCKER | SPEC | base | `scripts/harness.py:88-90` | An otherwise valid map containing `last_reviewed: 2026-13-01` makes PyYAML raise `ValueError`, which the handler does not catch. At either location, both invocation modes exit 1 with a traceback instead of the required exit 2 refusal naming the unreadable map. [AC 5] | Codex | open | — |
| F-3 | BLOCKER | SPEC | base | `scripts/harness.py:71` | When both maps exist but `decisions/` lacks traversal permission, `os.path.lexists` reports the lower map as absent and silently selects the top-level map. Reproduced with directory mode `000`: recording exits 1 with an uncaught `PermissionError`, rather than refusing with exit 2, naming both locations and saying to keep one. [AC 3] | Codex | open | — |

Phase 6 verdict: codex 01a12fe2-05b0-72a0-9df0-a666fd319af8, 2026-10-12
Reviewer session: codex 01a12fe2-05b0-72a0-9df0-a666fd319af8 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-10-12

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MINOR | SPEC | base | plans/changes/provenance-location/spec.md:4, and likewise decisions.md, findings.md, plan.md and research.md, with their rows in plans/INDEX.md | Every artefact of this change still declares implementation_status: none, and the rendered index prints none beside each, although the branch carries the implemented lookup and its tests. The field is defined to move when the code moves, so a maintainer scanning the index reads that no code exists where the code is the point of the change; the honest value at this state is at least partial. | deepseek-v4.1-flash | taken — the five artefacts and their plans/INDEX.md rows now say partial | no | agree |
| L1-2 | MINOR | MAINT | base | scripts/harness.py, answering_role, the except (OSError, yaml.YAMLError) around path.read_text | A map at either place whose bytes are not valid UTF-8 ends the command in a traceback and exit 1, because read_text raises UnicodeDecodeError, a ValueError, and nothing catches it. Instead of the clear refused: message with the map's path and the entry to add that every other unreadable map gets, the maintainer sees a Python stack trace; a test that writes such bytes at both places shows it. [criterion 5] | deepseek-v4.1-flash | taken — tests/test_harness_decide_adr.py::test_a_map_that_is_not_utf8_refuses_before_asking | no | agree |
| L2-1 | MINOR | MAINT | impl | tests/test_harness_decide_adr.py:3 | The test module's docstring still scopes the file to "Criteria 7-10 of plans/changes/harness-decide-adr/spec.md" and states "The one file of this repository read is provenance.yaml", but the file now also holds the tests of criteria 1-8 of plans/changes/provenance-location/spec.md and the command reads one of two places; the new tests also sit under the old "criterion 10 — who answered is configuration" banner, so a maintainer looking for where test_two_maps_refuse_before_asking comes from finds no pointer to the new spec. | mimo-v2.6-flash | taken — module docstring and the criterion-10 banner name plans/changes/provenance-location/spec.md (a text statement, no test) | no | disagree — The additional maps belong to temporary fixtures, so the statement about the sole repository file read remains true; the missing spec pointer demonstrates no correctness fault, spec gap or ineffective gate. |
| L2-2 | MINOR | MAINT | plan | plans/changes/provenance-location/plan.md:89 | The criterion ledger names test_a_map_that_is_not_utf8_refuses_before_asking for criterion 5, but the plan's "Tests per criterion" table (line 68) lists no UTF-8 case and its "Time used" (line 94) records only the attempt-1 formatting repair, although that repair episode added the test and put UnicodeDecodeError into answering_role's except tuple; the plan's narrative no longer matches its own ledger and the code. | mimo-v2.6-flash | taken — plan.md: the UTF-8 test in Tests per criterion, the round's repairs under Time used (a text statement, no test) | no | disagree — The UTF-8 test is recorded in the ledger and implemented; omissions from the plan summary and repair narrative demonstrate no correctness fault, missing criterion test or ineffective gate. |
| L3-1 | MAJOR | SPEC | promised, not done | plans/changes/provenance-location/plan.md ("For you") · scripts/harness.py, `answering_role` | The plan's "For you" line and the spec's problem promise the ADR command also works where the map lies at `decisions/provenance.yaml`, naming the instance this package serves. But `answering_role` still accepts only a `paths:` entry with prefix `decisions/answers/`, while the pin plan this change cites (its differences table, the `answered_by` row) records that instance's owner entry as `decisions/` — so after this change, and after the instance's own recorded half (adding `roles:` only), the command still refuses there with "has no \`paths:\` entry with prefix …". The decisions [DETAIL] fixes the lookup to `decisions/answers/` while admitting the instance's map was never read, and no test covers an owner entry at `decisions/`. Either a criterion demonstrates the named instance's map shape, or the plan must record the missing entry as its remaining step and the promise corrected. | mimo-v2.6-pro | taken — plan.md card and spec.md LakeSwitch's half corrected; no code change (scope stays the decided lookup) | no | agree |
| L3-2 | MINOR | MAINT | maintainer trip | tests/test_harness_decide_adr.py, `_written` | The refusal tests are named `…_never_writes` / `…_refuses_before_asking` and use `_written(repo) == []` as the proof of the refusal contract "before any file is written", but `_written` was narrowed to `decisions/answers/**` plus the message file; a repair that creates or rewrites `decisions/provenance.yaml` — the very file the two-map tests place there — or writes any path outside `decisions/answers/` now stays green. Excluding only the two map paths instead of the whole `decisions/` level keeps the old reach. | mimo-v2.6-pro | taken — tests/test_harness_decide_adr.py::_written covers all of decisions/ except the placed map | no | agree |

Rounds run: 3

Stage-2 call, 2026-10-12: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 361 files, 904 commits, 12 rules.
