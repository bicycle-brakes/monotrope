---
title: "Session handover — stage2-mimo: implement failed after three attempts, the two red review-loop tests and 4b–7 remain, 2026-10-08"
category: handover
created: 2026-10-08
updated: 2026-10-08
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: opencode
  version: "2026-10-08"
tags: [handover, stage-2, stage2-mimo, mimo, opencode-go]
target_ref: "ae93969"
bead: coding-harness-ymx
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

The change `stage2-mimo` (bead `coding-harness-ymx` — Stage 2: MiMo-V2.6 as an
additional reviewer in the review loop (4b)) implements the maintainer's model
ladder for every stage-2 review — round 1 DeepSeek V4.1 Flash, round 2
MiMo-V2.6-Flash, round 3 only when needed MiMo-V2.6-Pro — reached through
OpenCode Go behind the leak check. Phases 1–3 are done and pushed on
`feat/stage2-mimo` up to `ae93969` (2026-10-07): research and decisions, the
spec with 26 criteria, the spec-review (four rows, all `in spec`), the design
with the ADR 0011 draft, and the plan with its eight steps. Phase 4 ran as
Route B (`python3 scripts/stage2.py implement stage2-mimo`, GLM 5.3 Flash via
the Stage-2 runner) from 2026-10-07 22:59 to 2026-10-08 01:03 and **failed**:
three attempts (flash, flash-repair, stage-1 Sonnet 5.5), each one turned away
by the runner's post-run checks, so the run ended `failed: implementation
post-run checks failed after the allowed attempts` and left all of its work
**uncommitted** in the worktree. `make verify` on that tree, run by the closing
OpenCode session on 2026-10-08 at about 08:55, is red on pytest: two
review-loop tests fail. Everything else in the tree looks complete.

## Next step

In the worktree `.claude/worktrees/stage2-mimo`, make the two red review-loop
tests green and commit the checkpoint: `tests/test_stage2.py:1508` (a round
that reports no finding must still write its model line —
`mimo-v2.6-flash reported no finding.` is missing from the loop record) and
`tests/test_stage2.py:1585` (round 3 must start after a taken row, while the
runner currently refuses with `round 2 wrote no taken row; the loop stops at
2.`), then `make verify` green. The probe and phases 4b–7 follow behind that
one repair (see Open work).

## Needed from the maintainer

Nothing right now.

## Decisions and preferences

- Every stage-2 review — 2a, 4b and 6 — runs through OpenCode Go in rounds:
  round 1 DeepSeek V4.1 Flash, round 2 MiMo-V2.6-Flash, round 3 only when
  needed MiMo-V2.6-Pro; the models stand in an ordered list in
  `model-endpoints.yaml`, so changing one is a one-line pull request without a
  code change (maintainer, 2026-10-07, recorded in the bead notes of
  `coding-harness-ymx` and in `plans/changes/stage2-mimo/decisions.md`).
- The compatibility probe runs in phase 4 **before the merge**: one special
  run, three calls (one per round), declaration and leak check before each,
  the commits named in the pull request body (maintainer answered "1" on
  2026-10-07, recorded in `plans/changes/stage2-mimo/decisions.md`).
- Phase 4 runs as Route B: the implementation is requested through
  `python3 scripts/stage2.py implement <change>` (GLM 5.3 Flash); the probe and
  the decision pull request are executed by this line of sessions (maintainer,
  2026-10-07).
- The delivery is one pull request and that pull request is itself the decision
  pull request: `docs/adr/0011-stage-2-reviews-through-opencode-go.md` and
  `decisions/answers/stage2-mimo/adr.yaml` are both held `human-decided`
  (`decisions/provenance.yaml`), so the title is `decide(stage2): …`, the label
  `decision`, the body from the decision template. ADR 0011 amends ADR 0007
  only; D-13 and `scripts/check_decision_continuity.py` stay untouched. The
  probe becomes its own `probe` verb in `scripts/stage2.py` (both settled on
  2026-10-07 in `plans/changes/stage2-mimo/decisions.md`, details 7 and 8).
- The tracker stays untouched in this stretch of the work: no `tools/bd` write
  at all, not even the closing comment — the comment that would have gone to
  the bead is kept in this handover instead (maintainer, 2026-10-08).

## Open work and blockers

- Bead `coding-harness-ymx` — Stage 2: MiMo-V2.6 as an additional reviewer in
  the review loop (4b) — stands `IN_PROGRESS` in the tracker, assignee
  `opencode`, its lease expired (heartbeat 17 hours old as of 2026-10-08
  08:55). Withheld tracker comment, kept here for the record: phase 4 (Route B,
  GLM 5.3 Flash) ran 2026-10-07 22:59 → 2026-10-08 01:03 and failed after
  three attempts on the runner's post-run checks; the work is uncommitted in
  `.claude/worktrees/stage2-mimo` at `ae93969` plus 14 dirty paths;
  `make verify` on 2026-10-08 is red on two review-loop tests; the probe
  (plan step 7) and phases 4b–7 remain.
- Blocker: those two failing tests in `tests/test_stage2.py` (measured under
  Validation). Everything else waits behind them.
- After the repair: run the probe (three live calls through OpenCode Go — they
  spend the subscription's credit, approved by the maintainer on 2026-10-07),
  repair what it finds, then the 4b review loop
  (`python3 scripts/stage2.py review-loop stage2-mimo`), phase 5 `make verify`,
  phase 6 `python3 scripts/stage2.py review stage2-mimo`, and phase 7 the
  decision pull request with the probe commits named in its body.

## Working state and parallel-session boundary

- Change worktree: `.claude/worktrees/stage2-mimo`, branch `feat/stage2-mimo`,
  HEAD `ae93969` (`docs(changes): plan carries the empty time heading phase 4
  writes into`, pushed 2026-10-07). No pull request exists for that branch yet.
- Uncommitted in that worktree as of 2026-10-08 09:00 — modified: `AGENTS.md`,
  `decisions/answers/stage2-mimo/adr.yaml`, `docs/WORKFLOW.md`,
  `model-endpoints.yaml`, `plans/changes/stage2-mimo/design.md`,
  `plans/changes/stage2-mimo/findings.md`, `plans/changes/stage2-mimo/plan.md`,
  `prompts/02a-spec-review.md`, `prompts/04b-review-loop.md`,
  `prompts/06-review.md`, `scripts/stage2.py`, `tests/test_model_endpoints.py`,
  `tests/test_stage2.py`; new: `docs/adr/0011-stage-2-reviews-through-opencode-go.md`.
  The three `Stage-2 call` lines at the end of `findings.md` record the three
  attempts, and `plan.md` under `## Time used` carries the two measured
  session entries of the runner.
- This handover is written by an OpenCode session (model mimo-v2.6-pro through
  OpenCode Go) and handed to a Claude Code session at the maintainer's word
  (2026-10-08).
- Parallel session: the scan reports one other session in the main checkout
  `/Users/mikypiky/coding-harness` (id `c9f8d717-a975-4a74-a7a5-874ef58195cb`,
  state "waiting", read 2026-10-08 morning). House rule one-writer holds: that
  session writes the tracker, this change line writes nothing there.
- The night handover of 2026-10-08
  (`docs/journal/handover/2026-10-08-night-run-session-runner-touch-map.md`,
  pull request #94) is a different topic and was still open when this was
  written (read from `gh pr view 94`, 2026-10-08).

## Validation

- Green: `make verify` at `ae93969` on 2026-10-07, before the implement run
  (the run records this itself in `plan.md` under `## Time used`).
- Red: `make verify` on the uncommitted tree, run by this session on 2026-10-08
  about 08:55 — `2 failed, 1149 passed, 16 skipped in 115.34s`, `ruff-check`
  green, `markdownlint` red but report-only (`decisions/gates.yaml`,
  `enforcement: report`, so it does not block). The two failures:
  `tests/test_stage2.py::test_a_round_without_a_finding_still_counts` (line
  1508 — the loop record does not contain `mimo-v2.6-flash reported no
  finding.` after round 2) and
  `tests/test_stage2.py::test_round_three_starts_only_after_a_taken_row` (line
  1585 — `review-loop` exits 2 with `refused: round 2 wrote no taken row; the
  loop stops at 2.`).
- The Stage-2 runner's leak check ran clean on all three attempts (273–274
  files, 618–627 commits, 12 secret rules, 2026-10-07/08).
- Not run by this session: the probe (plan step 7), the 4b review loop,
  phase 6 review.
- Not read: the values in `~/.config/cc-routing/secrets.env` — names only,
  never values.

## Addendum — 2026-10-08, the ladder repair stands, the rungs are refused, one launcher question

Written for a Claude Code session that takes the change over from the OpenCode
session (model MiMo-V2.6-Pro through OpenCode Go). The "Next step" above is
historical: those two tests were repaired at the test side and everything
after it is described here.

### Where we are

The two red tests were test bugs and stand repaired in `1f7c298` (2026-10-08,
reasons as detail decisions in `plan.md`); `origin/main` was merged in with the
session verb and its stricter declaration checks (`52a8f5a`), and the merge's
red — seven failures in `tests/test_stage2_session.py` — was repaired in
`dedecf5` (the failed-call line prints to standard error again, and the
undeclared case names a rung no entry lists). The maintainer then narrowed the
review routes (2026-10-08, recorded as a dated addendum in
`plans/changes/stage2-mimo/decisions.md` and as a comment on the bead): the
OpenCode Go ladder runs **only the 4b review loop**, phases 2a and 6 stay with
Codex exactly as on main, phase 6 keeps resuming the phase-2a session — after
Codex's phase 6 found two real BLOCKERs in `rb-g7-merge-freshness` after the
GLM loop had passed it, as on every change of the night run. That repair
stands in `3af0c9c`: `spec_review` and `review` run `codex exec` again with
main's Codex tests restored unchanged, and the prompts, `docs/WORKFLOW.md` §4,
`AGENTS.md`, the endpoint remarks, the ADR 0011 draft and the answer file's
reason carry the narrowed text. `make verify` is green at `5001a65` on
2026-10-08 (1253 passed, 16 skipped).

The probe and the first loop round are measured and refused. Rung 1
(`deepseek-v4.1-flash`) was attempted three times on 2026-10-08 — two probe
runs and one review-loop round — and every one stopped with
`[claude-code:unrecognized_model]`, exit 1. What is measured behind that
sentence: the client sends the id correctly (a local blind server receives
`model: "deepseek-v4.1-flash"` and a 200 is accepted, the `[1m]` suffix is
stripped), the route `https://opencode.ai/zen/go/v1/messages` exists (an empty
POST answers 401, not 404), `GET https://opencode.ai/zen/go/v1/models` lists
all three ids, and Claude Code 2.1.294 renames **every** non-2xx answer of the
server into that model message (a local 404 "no such route" produces the
identical text). The Go page lists the three ids under the OpenAI-compatible
address only (`research.md` §F). So the Anthropic-compatible address refuses
the rungs' ids as Claude Code calls them; criterion 17 stopped and reported
each run, and no second address was built around it.

Two repairs stand pushed with it. `74ab180`: the runner sets
`CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1` in every Claude Code
call's environment — the vendor's own error message names that variable, and
the ids stay exactly as `model-endpoints.yaml` lists them. `5001a65`: the
planted OpenCode key of the tests now keeps its distance from the planted GLM
key — an inserted line beside it had pulled the key line into every diff's
three-line context, the loop's prompt carries the diff, and the leak check
rightly refused to send it (measured 2026-10-08, prompt line 3647); the loop's
leak check is clean since.

### Next step

Put the launcher question below to the maintainer; his word decides it. Then,
through the launcher he names, run the probe and the loop again, then 4b
(`python3 scripts/stage2.py review-loop stage2-mimo`), phase 5 `make verify`,
phase 6 `python3 scripts/stage2.py review stage2-mimo`, and the decision pull
request `decide(stage2): …` (label `decision`, body from the decision
template, the probe result named in it: `deepseek-v4.1-flash` refused, run
stopped under criterion 17, 2026-10-08).

### Needed from the maintainer

**Shall the loop's rounds be launched through `opencode run -m
opencode-go/<rung>` instead of Claude Code?** He said "deepseek und mimi
laufen über open code, mache weiter" (2026-10-08), and the models do run
through OpenCode — this addendum was written on `mimo-v2.6-pro` through
OpenCode Go. The repository already starts `opencode` for the session verbs
(pull request #91), and `opencode run` takes `--model provider/model`,
`--format json` and a resumable `--session`. The consequence of yes: criterion
8 of the spec and the launcher paragraph of ADR 0011 are rewritten (they say
"through Claude Code" today), while the ladder, the three rounds and the
round-3 rule stay. The alternative is to keep Claude Code and learn from the
Go side why the address refuses the ids for it.

### Working state and parallel-session boundary

`feat/stage2-mimo` stands at `5001a65`, pushed, with no pull request open for
it; one dirty file in the worktree (`plans/changes/stage2-mimo/findings.md`)
carries the three `Stage-2 call` lines of the refused attempts. `main` moved to
`8f097a3` on 2026-10-08 (pull requests #91–#100 merged, RB-G7 among them at
`902c0f7`): the branch must merge `main` again before its pull request (RB-G7
touched `tests/test_ci.py`, `tests/test_repo_settings.py`, `docs/governance/`
and `prompts/07-commit.md`), and the ruleset of 5.0.0 requires an up-to-date
branch before a merge. No tracker write happened in this stretch — the
maintainer held the tracker back on 2026-10-08, and the comment that would
have gone to the bead `coding-harness-ymx` (Stage 2: MiMo-V2.6 as an
additional reviewer in the review loop (4b)) is this addendum's working state.
The watching session handed its watch to Codex
(`docs/journal/handover/2026-10-08-codex-takes-over-mimo-watch.md`, pull
request #100).

### Validation

`make verify` green at `5001a65` on 2026-10-08 (1253 passed, 16 skipped); the
leak check clean in every runner run since `5001a65`; the probe and one loop
round measured as described above. **Not run since the repair:** a successful
probe, 4b, phase 6, the decision pull request. **Not read:** the values in
`~/.config/cc-routing/secrets.env` — names only, never values.
