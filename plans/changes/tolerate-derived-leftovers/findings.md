---
title: "Findings — tolerate-derived-leftovers"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-b5w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — tolerate-derived-leftovers

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: both
new tests failed before the edit.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- A content edit that also changes the `updated:` line has more than one
  changed line, so it is not a stamp-only diff and stays refused.
- A tolerated leftover is not in the restore's `keep` set: a failed
  attempt puts it back to the baseline with the rest, and a passing one
  commits it re-stamped and re-rendered.
- `clear_derived_leftovers` in the tests is now redundant for the index;
  it is left as it is, outside this change.

## Independent runner review, 2026-10-25

An Opus sub-agent of the orchestrating session reviewed the runner with all
open pull requests merged (read-only, in a separate context). Its row for
this change:

| ID | Severity | Finding | Status |
|---|---|---|---|
| R-3 | MINOR | `derived_leftover` dropped diff lines starting `---`/`+++` as file headers, so a removed Markdown rule (`---`) or an added line starting `++` hid a content edit beside an `updated:` change; criterion 2 was broken (reproduced). | fixed — tests/test_stage2.py::test_a_content_edit_behind_dash_lines_is_no_derived_leftover |

The check now compares the `HEAD` version and the working file with their
first `updated:` line masked; a symlink, a non-file, undecodable bytes or
identical bytes are no stamp-only change.

## Pre-review by an Opus 5.5 subagent, 2026-10-25

At the maintainer's request a read-only Opus 5.5 subagent reviewed the change
before phase 6 (Codex, unreachable here). Phase 6 is still owed. Repairs were
made by a Sonnet 5.5 subagent at the orchestrator's direction.

| ID | Severity | Finding | Status |
|---|---|---|---|
| P243-1 | MAJOR | `derived_leftover` read `HEAD` in text mode, so CRLF and lone CR became LF while the worktree was raw: a whole-file CRLF-to-LF conversion plus a new stamp was tolerated and later committed. | fixed, HEAD read as bytes and decoded strictly as UTF-8, no newline translation, `"\ufffd"` heuristic dropped — tests/test_stage2.py::test_derived_leftover_is_a_frontmatter_stamp_and_nothing_else (ids `crlf-to-lf-plus-stamp`, `lf-to-crlf-plus-stamp`, `lone-cr-to-lf-plus-stamp`) |
| P243-2 | MAJOR | Same cause: a genuine CRLF file whose only change is the stamp was refused. | fixed by the same change — same test, id `crlf-stamp` |
| P243-3 | MINOR | The mask hit the first line starting `updated: ` anywhere, any value, any file. | fixed, only the single frontmatter `updated:` line is masked (`check_frontmatter_current._BLOCK`, `_UPDATED_LINE`) and the new value must be `updated: YYYY-MM-DD` — same test, ids `body-updated-line-changed`, `body-updated-no-frontmatter`, `non-date-value`, `python-file`, `second-frontmatter-updated-line-changed` |
| P243-4 | MINOR | `stamp` accepts `updated:` without a space and can insert a line where none was. | fixed for the no-space form (id `no-space-stamp`); an inserted line is refused and named a non-goal in spec.md (id `inserted-stamp-line`) |
| P243-5 | MINOR | In `draft`, a leftover the run started with was put back and listed as "the runner put back what a draft may not change", blaming the model. | fixed, the leftovers are computed before the first call and left out of that listing (still put back) — tests/test_stage2.py::test_a_draft_does_not_blame_the_model_for_a_derived_leftover |
| P243-6 | MINOR | No unit test of `derived_leftover` over the stamp variants. | fixed, parametrised test; it fails when every frontmatter `updated:` line is masked (`second-frontmatter-updated-line-changed`) and when the match is `startswith("updated")` (`updated-prefixed-key-kept`) — tests/test_stage2.py::test_derived_leftover_is_a_frontmatter_stamp_and_nothing_else |
| P243-7 | NIT | The `.pyc` clause tolerates files that this repository ignores. | not now, no code change: `.pyc` is gitignored here, so the clause matters only in target repositories that track bytecode |

## Review loop skipped, 2026-10-25

The review loop (phase 4b) did not run on this change. The maintainer
answered on 2026-10-25 (night-run plan, `docs/research/2026-10-25-night-run-plan.md`,
answer 1) that the small cloud-session fixes get phase 6 only tonight,
because each had the Opus 5.5 pre-review recorded above. Phase 6 follows in
a fresh Codex session.

Stage-2 call, 2026-10-25: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 553 files, 2128 commits, 12 rules.

## Phase 6 — Codex, 2026-10-25

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | Phase 6 | scripts/stage2.py:3242–3251 | Changing a tracked document from mode 100644 to 100755 alongside its `updated:` date is accepted as a derived leftover: the comparison checks bytes but never the executable bit. With `core.filemode=true`, `implement` and `repair` can therefore commit an unrelated permission change. Reject mode changes even when the masked contents match. [Non-goal: tolerate no other change.] | Codex | open | — |
| F-2 | MAJOR | SPEC | Phase 6 | scripts/stage2.py:3277–3282; scripts/stage2.py:4129–4149 | A stamp-only leftover in an existing `docs/adr/` document passes the new pre-existing-change check but remains forbidden by `uncommittable`, because that prefix is human-decided. Even after successful verification, the checkpoint fails and restores the implementation. The promised successful retry therefore fails when this is its only initial leftover; reconcile admission with checkpoint handling while preserving protection of substantive ADR edits. [Acceptance criterion 1.] | Codex | open | — |

Phase 6 verdict: codex 01a174e9-59f6-7ac1-b5dc-59ee50d0af43, 2026-10-25
Reviewer session: codex 01a174e9-59f6-7ac1-b5dc-59ee50d0af43 — a fresh session reviewed: no phase-2a session was recorded

Loop rows: none — the loop did not run for this change.
