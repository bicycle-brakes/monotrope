---
title: "Session handover — afternoon of 2026-11-24: five lanes, JSON instruction, re-slice"
category: handover
created: 2026-11-24
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "Opus 5.5, 2026-11-24"
tags: [handover, lanes, spec-review, state-first, re-slice]
target_ref: a5b117f8
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
updated: 2026-11-25
---

# Resume here

## Where we are

Session 9fd82f45 (profile `~/.claude-bddh`) took over from session c820a13d after
its usage limit (that session's handover: PR #444, open). It ran five lanes and
hands back to the `claude-mp` session at the maintainer's request. No runner call
is running at hand-over; every lane branch is pushed and clean (heads below).
This session wrote the tracker until the hand-over; from now on only the
receiving session writes it.

## Next step

1. **repair-scope-guard** (bead coding-harness-t83): row R1 (MAJOR, an
   out-of-scope file left after a failed inventory can be committed by the next
   attempt) is taken; maintainer: repair, then one more phase-6 re-check.
   Run `scripts/stage2.py repair repair-scope-guard`, then `review`. Clean →
   ready-for-merge commit with `Closes-Bead: coding-harness-t83` and the PR.
2. **findings-per-model** (bead coding-harness-qut1): the phase-6 re-check
   never started because `make verify` was red on `leerprobe` (kit probe).
   Fixed by an orchestrator hand edit the maintainer allowed (59734574,
   `MODEL_ID` now lives in `scripts/findings_reader.py`). Next: `review
   findings-per-model`. The branch is 405 commits behind main.
3. **Plan cards to the maintainer** (unchanged, with the plain-words
   explanation): detached-job-launcher (a6ns.1, final draft 7287b91d),
   ladder-next-step (hwll, final draft fa7b1e55), advance-verb (z40g, final
   draft 47353855). All three used their last spec-review round; no further
   round can run.
4. **isolated-writing-attempts** (bead coding-harness-s9r, re-sliced, worktree
   `.claude/worktrees/isolated-attempts`, branch feat/isolated-attempts):
   first draft verified (acba0122); next `spec-review isolated-writing-attempts`
   (round 1).

## Needed from the maintainer

1. Merge PR #446 (house rule 11, code before prose; CI green) and PR #444 (the
   day handover of session c820a13d).
2. PR #445 (audit synthesis and state-first ADR draft): reviewed, mergeable as
   research once CI is green. Two points were not yet posted as a comment: the
   draft claims "zero conflicts" although advance-verb planned Markdown and YAML
   state (since superseded by the JSON decision below), and `AGENTS.md:123`
   should read 127.
3. PR #447 (visitor docs refresh by another session): not read by this session.
4. Implementation order (maintainer, 2026-11-24): advance-verb waits for
   ladder-next-step (hwll), review-fewer-rounds (3rtn) waits for
   findings-per-model (qut1). hwll's own order from 2026-11-21 still stands:
   red-first-baseline, review-diff-4000, then ladder-next-step — all three are
   only drafted and about 400 commits behind main.

## Decisions and preferences

- **House rule 11 — code before prose** (maintainer, 2026-11-24): state a
  program reads back is a schema-validated JSON file written by code, never
  Markdown parsed back; Markdown only where a person reads it and it cannot be
  avoided. The maintainer allowed this agent edit of `AGENTS.md` (PR #446).
- **Option B for the next-step instruction:** ladder-next-step writes
  `next.json` beside the loop record (hwll Q-6); advance-verb reads only that
  file and owns `lanes.json` with `add`, `remove`, `clear`, `hold` subcommands
  (z40g Q-20, Q-22). A fourth spec-review round was authorized for both.
- **isolated-attempts re-sliced** (Q-25 in
  `plans/changes/isolated-writing-attempts/decisions.md`): slice 1 isolates the
  writing verbs with JSON state. Follow-up beads: coding-harness-cl45 (review
  isolation), coding-harness-1ml1 (attempt CLI for other harnesses),
  coding-harness-oekl (ref clean-up and the PR 2 gate). The superseded change's
  undecided ADR draft `docs/adr/0026-isolated-attempts.md` was removed from the
  branch (81db41b6).
- **detached-job-launcher:** JSON job records; the four critical answers
  (S-21 process groups written by stage2, S-22 PID plus start time, S-24 the
  caller's environment, never the tmux server's, S-25 program name only in the
  report) were explained and confirmed (Q-15..Q-19).
- **review-fewer-rounds:** free-round replacements are the most expensive free
  model first, by fewest requests per five hours (Q-45).
- PR #437 closed (findings live under epic coding-harness-5ane); bead
  coding-harness-5ane.2 raised to P1.
- New beads under epic coding-harness-5ane (P2): 5ane.16 decisions.yaml,
  5ane.17 ledger and time records as data, 5ane.18 generated indices, 5ane.19
  clean-up in order (close-merged before archive).

## Open work and blockers

| Lane | Bead | Branch @ head | State |
|---|---|---|---|
| repair-scope-guard | coding-harness-t83 | fix/repair-scope-guard @ 10a7efe8 | R1 taken, repair + re-check next |
| findings-per-model | coding-harness-qut1 | feat/findings-per-model @ 59734574 | phase-6 re-check next |
| detached-job-launcher | coding-harness-a6ns.1 | feat/detached-job-launcher @ 7287b91d | plan card to the maintainer |
| ladder-next-step | coding-harness-hwll | feat/ladder-next-step @ fa7b1e55 | plan card; after red-first-baseline, review-diff-4000 |
| advance-verb | coding-harness-z40g | feat/advance-verb @ 47353855 | plan card; waits for hwll |
| isolated-writing-attempts | coding-harness-s9r | feat/isolated-attempts @ acba0122 | spec-review round 1 next |
| review-fewer-rounds | coding-harness-3rtn | feat/review-fewer-rounds @ faf1a263 | plan card shown; waits for qut1; reconcile its ADR 0027 |

## Working state

- Runner logs of this session: the session scratchpad
  `/private/tmp/claude-501/-Users-mikypiky-coding-harness/9fd82f45-02b2-4eeb-b2c1-020ee1770204/scratchpad/`.
- ADR numbering: 0026 is claimed by feat/central-config, 0027 by
  feat/review-fewer-rounds; isolated-writing-attempts and detached-job-launcher
  will claim theirs at merge.
- The GLM fallback route of `draft` failed with
  `[claude-code:unrecognized_model] glm-5.4` (isolated-writing-attempts, attempt
  3); not investigated.
- When Opus is unavailable, `spec-review` falls back to deepseek-v4.1-flash,
  whose terms expire on 2026-11-30.

## Orchestrator mistakes

- The previous session's flake measurement left 16 busy loops running for 21
  hours (system load 58): in zsh `kill $PIDS` with a space-joined string passes
  one argument, and `2>/dev/null` hid the error. The maintainer stopped them;
  recorded as project memory `zsh-kill-word-splitting`.
- This session wrote `PIDS`-style zsh commands with unquoted `$M:path` and
  `$T` lists twice before noticing the same word-splitting rule; no harm done.

## Validation

- Every runner step above has its result line in the lane's findings.md and in
  the scratchpad logs; decision gates (interview-minimums, question-context,
  research-handoff, decision-continuity, adr-answers) were green after each
  decisions.md edit.
- The qut1 hand fix: ruff clean, 209 affected tests green, kit probe with the
  venv on PATH without a block (1575 of 1619 cases carry).
- Not read: PR #447.
