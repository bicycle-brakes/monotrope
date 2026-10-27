---
title: "Five parked runner pull requests against the restructured main, 2026-10-27"
category: research
status: current
created: 2026-10-27
last_reviewed: 2026-10-27
owner: framework-architect
updated: 2026-10-27
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Sonnet 5.5 sub-agent, read-only, 2026-10-27"
tags: [research, review-loop, stage-2, merge-conflicts]
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Five parked runner pull requests against the restructured main

On 2026-10-27 five draft pull requests from the 2026-10-24/25 cloud session
no longer merged into `main` (bead coding-harness-s05q). A read-only
sub-agent compared each with `origin/main` as fetched that day. It ran no
tests and did not read the pull requests' test files line by line; every
statement below is read, not measured. The rules this led to stand in
`AGENTS.md`, "Pull requests stay mergeable".

All five share a merge base of `f8a6b330` or older. Each conflicts in
`scripts/stage2.py`, in `tests/test_stage2.py` (one append-against-append
hunk of about 2,000 to 2,600 lines, mechanical) and in `plans/INDEX.md`
(18 to 24 lines, mechanical).

| PR | Defect | Does main cover it? | Conflict in `stage2.py` | Decision (maintainer, 2026-10-27) |
|---|---|---|---|---|
| #228 (coding-harness-10w) | Restoring a failed attempt unlinks a symlinked parent and goes on, so a write outside the worktree was possible; the spec wants a refusal without writing or falling back | No: `restore_work_input` still unlinks the link and creates a directory | semantic, 4 hunks, about 149 lines (main's `CheckpointRolledBack` and answer-evidence flow) | keep, bring onto main next |
| #229 (coding-harness-i70) | A forged `Loop state:` line in reviewer text could select models | Mostly: reviewer text is quoted and skipped when state is read (`quote_reviewer`, `read_state`); not covered are the delimited state block and its state-format refusal | semantic, 8 hunks, about 369 lines | close as superseded |
| #235 (coding-harness-6jg) | A member whose table has no readable row counts as an ordinary failed member, so a peer's "No finding." can end the loop clean and the paid swarm replaces it | Partly: row ids are numbered by the runner; a malformed answer is asked again with a format reminder (`MalformedAnswer`), but a twice-malformed member is still replaced and the round still succeeds | semantic, 1 hunk, about 161 lines (retry-then-replace against refuse) | shrink, after the maintainer decides refuse against replace |
| #236 (coding-harness-2i9j) | A finding row without its closing pipe is not read as a row | No: `split_row` requires a closing pipe; the message names no offending line | mixed, 2 hunks, about 322 lines, stacked on #235 | shrink to the open-row parse and the first-bad-line message, unstacked |
| #238 (coding-harness-vque) | A finding-shaped line the parser cannot read, beside readable rows, does not refuse the round | No: such lines stay as quoted non-row text and the round is written | semantic, stacked on #235 and #236 | defer until #235 and #236 are settled |

The #228 worktree holds an uncommitted `findings.md` block with three repair
attempts of 2026-10-24: attempt 1 (Codex) failed on the gate
`question-context`, attempt 2 (Codex) on one alias-chain test, and attempt 3
(Sonnet 5.5) recorded no result.
