---
title: "Research — repair-fixed-line-format"
status: draft
implementation_status: none
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-hgvp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, repair]
class: bounded
---

# repair-fixed-line-format — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `79a74f75`
(2026-10-26).

## The finding

On 2026-10-26 the repair verb rejected four Sonnet 5.5 repair attempts
(route `stage-1`, through `--stage2-off`). Each was rejected with the same
diagnostics: `<ID>: several fixed lines` for every taken row.

- ratchet-mutation-evidence, R7-1 to R7-4. The 21 evidence tests passed on
  the tree the attempt left behind. A second Sonnet attempt from a clean
  tree was accepted (`fb268b3d`).
- review-loop-deep-b, F6-1 and F6-2, rejected twice. Codex then repaired the
  same rows in one attempt (`252ff0f3`).
- ratchet-mutation-evidence, R8-1 to R8-4. Codex then repaired them in one
  attempt (`34ad6d8b`).

With `--stage2-off`, the route has one attempt, so each slip costs a whole
repair of about 11 minutes. The night-run standing rule (coding-harness-yuw.4)
sends a step to Sonnet when Codex is at capacity, so this failure would hit
every such step.

## What exists today

Read in `scripts/stage2.py` at `79a74f75`:

- `REPAIR_ANSWER` asks for "one fixed line per taken row". Headings, fences
  and prose around them are said to be ignored.
- The answer parser (the function holding `several fixed lines`, near line
  4990):
  - It strips a list marker and splits each line at the first colon.
  - It keeps every line whose left side is an active row id exactly, whatever
    its right side says.
  - For a finding-shaped id it keeps the line only when the prefix is used by
    the change's rows, or when the right side starts `fixed — `.
  - A row with more than one kept line fails with `several fixed lines`,
    before `fixed_status` reads any of them.
- So an explanatory line such as `R8-1: _is_run_call now checks the module`
  beside `R8-1: fixed — tests/…` makes the row fail, although the prompt says
  prose is ignored.
- The model's answer is not kept. The stage-1 call runs in a temporary
  directory (`claude-config` under a `TemporaryDirectory`), and `findings.md`
  records only the diagnostics. The attempt ref under
  `refs/stage2/attempts/<change>/` holds the tree, not the answer.

## Caveat

**The cause is inferred, not read.** None of the four answers survives, so
"Sonnet writes prose lines that begin with the row id" is the likeliest
reading of `several fixed lines`, not an observation. This is why the change
keeps the answer: the next rejection can then be read.

## Sources

- `scripts/stage2.py` at `79a74f75`.
- The attempt blocks dated 2026-10-26 in
  `plans/changes/ratchet-mutation-evidence/findings.md` and
  `plans/changes/review-loop-deep-b/findings.md`, on their branches.
- Bead coding-harness-hgvp.
