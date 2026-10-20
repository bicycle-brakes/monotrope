---
title: "Session handover — review of the review-swarm runner, as of 2026-10-20"
category: handover
created: 2026-10-20
updated: 2026-10-20
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: pi
  version: "Sonnet-class session through Pi, 2026-10-20"
tags: [handover, session, review-loop, stage-2, runner, swarm]
target_ref: 94ae6cc
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

A read-only session reviewed the phase-4b runner — `scripts/stage2.py` (the
ladder, the free swarm, the Flash swarm, the loop record, release) and
`scripts/stage2_availability.py` (the availability preparation) — in three
passes and found thirteen problems: five MAJOR, six MINOR, two notes. Nothing
was changed, no foreign model was called, and the tracker was not written
(another session held the checkout, see below). The review started on
`main` at `59630b7`; `scripts/stage2.py`, `scripts/stage2_availability.py`,
`model-endpoints.yaml`, `prompts/04b-review-loop.md` and
`docs/adr/0021-review-swarms-until-clean.md` are byte-identical between that
commit and today's `origin/main` `94ae6cc`, so every finding applies to
current main. Two of the MAJOR findings were reproduced with the runner's own
functions; the rest were read, not executed.

## Next step

Open one small pull request that repairs **R-3** (line-anchored cut of the
released block) and **R-2** (loop record and receipt keyed by the worktree)
with tests — both are pure code fixes and need no decision. Read the findings
below first; R-1, R-4 and R-5 wait for the maintainer.

## The review — thirteen findings in the review-swarm runner

Reference cuts off at `94ae6cc`; line numbers are that commit's.

### MAJOR

**R-1 — A failing stage can never be retired; the run wedges.**
*Evidence (measured on the real record of `failed-check-secrets`, no model
call):* `stage2.read_state` returns `consumed: ["free", "flash"]` and
`next_stage` returns `rung:glm-5.3-flash`; `prepare-loop` refuses because
`read_state(...) is not None`. The stage snapshot pins the stages
(`scripts/stage2.py:2196` ff., ADR 0021 decision 9), an edited
`model-endpoints.yaml` does not reach a started run, `release-loop` demands a
phase-6 verdict (`:2377`), and `VERBS` (`:4636`) has no skip verb. The only
escape is deleting `loop.md` by hand — which destroys the round rows, the
only copy until release.
*Consequence:* one model that times out (as `glm-5.3-flash` did on
2026-10-20 02:24Z) holds the change until a human edits outside the
repository.
*Proposed fix:* a verb (or `release-loop` flag) that marks one stage
`failed`/`consumed` with a reason, writing the reason into the record; or
`prepare-loop` may re-plan the *remaining* stages of a started run while
leaving consumed ones alone.

**R-2 — Record and receipt are keyed by change name only, not by worktree.**
*Evidence (measured):* `stage2.record_dir("demo")` →
`~/.local/state/coding-harness/stage2/demo`, from any checkout. The receipt's
`binding` carries `root` and a foreign receipt is refused
(`scripts/stage2_availability.py:60`), the record has no such check.
*Consequence:* two worktrees with the same change folder (this repository has
`research-swarm` and `research-swarm-capture` side by side) share one
`loop.md` and one `availability.json`; worktree B continues A's stages and
writes into A's record, and a `release-loop` in A deletes B's record.
*Proposed fix:* key `record_dir` by the resolved repository root (a short
digest), the way `binding()` already identifies a run; keep the change name in
the path for readability.

**R-3 — The released block is cut at a substring, so a finding can break the
continuation (reproduced).**
*Evidence (measured with the runner's own functions):* `read_state` cuts at
`block.find("Kept from the loop record:")` (`scripts/stage2.py:2291`) and
`released_rows` does the same (`:1814`); `findings_rows` (`:1845`) and
`rounds_run` (`:2326`) test `startswith` and are safe. A synthetic released
block whose table cell carries the sentence in the `Finding` column yields
`released_rows -> 0` and `read_state -> None`.
*Consequence:* after a release, a run cannot read its snapshot: `review-loop`
refuses (`the loop record has no Loop state line`), `prepare-loop` refuses
because history exists — the same wedge as R-1, entered from a document. The
review swarm reviews this very runner, so a reviewer quoting that line is
plausible; the sentence is also the natural way to describe the release.
*Liveness:* `read_state` is live today; `released_rows` has only test callers
(`tests/test_stage2.py:3428`), so it is latent.
*Proposed fix:* cut with `re.compile(r"^Kept from the loop record:[ \t]*$", re.M)`.
Table rows start with `|`, quoted reviewer text with `>`, so an anchored match
cannot be hit from a row.

**R-4 — The deny list is never read, and the free class bypasses the
allowlist.**
*Evidence:* `ausgeschlossen:` (`model-endpoints.yaml:402`) is read by no
runner code; only `tests/test_stage2.py:664` checks that the YAML looks as
intended. `free_admission_problem` (`scripts/stage2.py:1229`) and
`select_free` (`:1280`) check provider, suffix/include, `exclude`,
`darf_sehen`, `residenz` and that the id is not a `modelle` member — nothing
else.
*Consequence:* every newly appearing `*-free` id under `opencode-go` enters
round 1 automatically. The Kimi exclusion of 2026-09-30 holds today only
because `kimi-k3` is neither in `modelle` nor suffixed `-free`; a
`kimi-k4-free` would carry the implementation diff with no decision.
*Proposed fix:* one predicate over `ausgeschlossen` (substring or prefix per
entry, with its date) used by `free_admission_problem` and
`declaration_problem`; a test that a suffixed free id of a denied provider
never appears in `selected`.

**R-5 — The paid swarm's read boundary is a sentence, not a mechanism.**
*Evidence:* members get `PI_TOOLS = "read,grep,find,ls"`
(`scripts/stage2.py:217`) and the instruction `READ_REQUEST` (`:228`). Pi 1.2.0
has no built-in sandbox (measured: `tools/pi/node_modules/@earendil-works/
pi-coding-agent/docs/security.md`, "lack of a built-in sandbox"), and `read`
resolves absolute paths without a containment check (measured:
`dist/core/tools/path-utils.js:72`). The leak check gates the prompt
(`checked_prompt`, `:889`), never what a member reads and sends.
*Consequence:* nothing in the runner prevents a member from reading a sibling
checkout — house rule 6 (the customer instance is out of bounds) has no
mechanism on this path. Likelihood is low (the prompt forbids it), the
boundary is real.
*Proposed fix:* a decision first — either accept the risk in writing (ADR
0021 consequence, in the endpoint's `bemerkung`), or run the paid members in a
copy of the worktree (`red_first`'s temporary worktree shows the pattern) so
the filesystem, not the prompt, is the boundary.

### MINOR

**R-6 — The round is written before the stage is consumed.**
`review_loop` writes the snapshot, appends the round, then calls
`mark_consumed` (`scripts/stage2.py:4506`–`4516`). A crash or Ctrl-C between
the two leaves a round in the record that the snapshot does not know about;
the next call repeats the same stage as a new round with new ids (extra paid
calls, two rounds for one stage). *Fix:* mark consumed in the same write as
the round.

**R-7 — A 60-second probe at `--thinking max` can drop a reachable model.**
`stage2_availability.py:148` probes with `timeout_seconds=60`; the runner
always launches with `--thinking max`. A slow but reachable model counts as
unreachable and disappears from the ladder for the whole run, silently.
*Fix:* name the failed probe beside the model in the receipt (it is named) and
allow one longer probe for a member that timed out at 60 s.

**R-8 — The Flash replacement chain has no round deadline.**
Each replacement runs sequentially with its own `REVIEWER_MINUTES = 30`
(`scripts/stage2.py:219`), so one Flash round can take about two hours while
the documentation calls it parallel. *Fix:* one deadline per round, shared by
members and replacements.

**R-9 — The severity column is free text.**
`SEVERITIES` (`scripts/stage2.py:324`) is used only to decide whether a line
with more than six cells is still a row (`:653`); a six-cell row's severity is
never validated and `BLOCKER` has no gate in the loop. Round 1 of the real run
carried "Medium". *Fix:* either validate against the three words, or say in
the prompt that severity is free text and the orchestrator decides.

**R-10 — A misplaced `Broke a test` cell hides as status text.**
`record_rows` (`scripts/stage2.py:2087`) joins cells 7 to the second-to-last
into `Status`. An editor who shifts one column gets no refusal; `undecided`
(`:2091`) then reads the shifted cell as the mark. *Fix:* refuse a row whose
`Status` starts `taken`/`fixed` and whose join was needed, naming the row.

**R-11 — A clean loop end is reported as a refusal.**
`raise Refused(f"round {last} was clean …")` (`scripts/stage2.py:4367`) ends
with `refused: …` on stderr and exit 2 (`:4712`). Automation cannot tell a
finished clean loop from a real refusal. *Fix:* a distinct exit code or a
message without `refused:` for the clean stop.

### Notes

**R-12 — The free round has no size cap in code.** `select_free` (`:1280`)
takes every match; ADR 0021 decision 8 reckons with "F + 9 member calls, F
being the run's free count". Declared, not a defect — recorded because the
ADR's bound reads like a limit and is not one.

**R-13 — Documentation drift.** `prompts/04b-review-loop.md:11` and
`docs/WORKFLOW.md` (the 4b section) still describe round 2 as "the entry's
eligible `flash_swarm` members"; fresh runs take the reachable three cheapest
from the availability preparation, and `model-endpoints.yaml` says the list is
"legacy configuration only". The notice built by `cheapest_notice`
(`scripts/stage2.py:1088`) can therefore never fire for a preflight run.

### Checked and found sound

These were verified so the next session need not redo them.

- Every CLI flag the runner uses exists in the pinned Pi 1.2.0 (measured with
  `tools/pi/pi --help`): `--print`, `--no-session`, `--no-approve`,
  `--no-extensions`, `--no-mcp`, `--no-skills`, `--no-context-files`,
  `--no-prompt-templates`, `--no-themes`, `--offline`, `--no-tools`,
  `--tools`, `--thinking max`. Tool names `read`, `grep`, `find`, `ls` are
  1.2.0's names.
- `--append-system-prompt <path>` really reads the file in 1.2.0
  (`dist/core/resource-loader.js:104`); passing a path is correct.
- `tools/pi/pi` ends with `exec node`, so a timeout kills the real process,
  not a shell wrapper — no orphaned call.
- The free stage's isolation holds: `--no-tools`, a scratch working directory,
  `--offline`, a fresh `HOME` and agent directory, and the bounded
  implementation diff as the only input (`free_diff`, `_free_candidate`).
- The red-first machinery (`red_first`, `scripts/stage2.py:3160` ff.) is
  sound: token-bound private report, exit 2/3 not read as red, fixture and
  skip outcomes refuse, refs snapshotted before and after, temporary worktree
  removed before pruning.
- `overlay_store`/`activate_overlay` write model definitions only, never
  credentials.
- **Correction of an earlier claim in this session:** the loop record of
  `failed-check-secrets` is *not* lost. It sits outside the worktree at
  `~/.local/state/coding-harness/stage2/failed-check-secrets/loop.md`
  (40 634 bytes, rounds 1 and 2, snapshot `consumed: ["free","flash"]`).
- **Correction of a second claim:** the receipt's freshness clock starts
  *after* the probes (`checked_at` is set at the end of `prepare`,
  `stage2_availability.py:150`), not at discovery.

## Needed from the maintainer

1. **R-1, the wedge: is a stage allowed to be retired?** Recommendation: give
   `release-loop` a `--stage-failed <model> --reason <text>` (or a small
   `retire-stage` verb) that marks the stage consumed and writes the reason
   into the record, keeping the rows. Consequence of no change: a model that
   keeps timing out stops the change until someone edits
   `~/.local/state/…/loop.md` by hand.
2. **R-4, the deny list: should it bind the code?** Recommendation: yes, one
   predicate used by both admission paths. Consequence of no change: a new
   free id from a denied provider would review diffs without any decision.
3. **R-5, the read boundary: accept or enforce?** Recommendation: accept it in
   writing for now (ADR 0021 consequence, in the endpoint's `bemerkung`) and
   open a bead for a temporary-worktree sandbox; enforcing today costs one
   copied worktree per paid member.

## Decisions and preferences

- The review is read-only: no file in the repository was changed, no foreign
  model was called, and no bead was opened or closed (one-writer rule, see
  below).
- Findings are ordered code fixes first (R-2, R-3, R-6), then decisions
  (R-1, R-4, R-5), then cosmetics.
- The three review passes were deliberately kept apart (structure, governance,
  parsing/state machine); the third found the one defect the first two missed.

## Open work and blockers

Task status stays in Beads; nothing was written there. The findings above are
the work list of this review and are not yet beads. `failed-check-secrets`
(bead coding-harness-8hr) still waits for the decision in question 2 of the
ninth night run's handover — its loop round 3 stands at
`rung:glm-5.3-flash`, which is exactly R-1 in the field.

## Working state and parallel-session boundary

- Branch `docs/handover-2026-10-20-review-swarm-runner`, worktree
  `.claude/worktrees/handover-2026-10-20-review-swarm-runner`, branched from
  `origin/main` at `94ae6cc`.
- Pull request: opened from this branch; the merge is the maintainer's.
- The main checkout `/Users/mikypiky/coding-harness` is on `main` at
  `59630b7` with one untracked file, `.codex/agents/`, which was there before
  this session and is not from this session.
- **A second session was detected in the same checkout** (`session-scan.sh`
  reported `clash coding-harness-2c shell` on 2026-10-20). This session wrote
  no tracker data and changed no file in the main checkout; the only writes
  happened inside its own worktree.
- External state touched by reading only:
  `~/.local/state/coding-harness/stage2/failed-check-secrets/` (record and
  receipt read, not modified).

## Validation

- Read and measured at `59630b7`; re-checked for drift against `origin/main`
  `94ae6cc` with `git diff --stat 59630b7..origin/main -- <runner files>` —
  empty, so the findings stand.
- `tests/test_stage2_availability.py`: **24 passed in 16.94 s** (measured
  2026-10-20, on `main` at `59630b7`).
- R-1 evidence: `read_state`/`next_stage`/`prepare` conditions evaluated on the
  real `failed-check-secrets` record, no model call.
- R-3 evidence: synthetic released block through `stage2.released_rows` and
  `stage2.read_state`; result `0` rows and `None`.
- Pi facts measured with the repository's pinned install (`tools/pi/pi --help`,
  files under `tools/pi/node_modules/@earendil-works/pi-coding-agent/dist`).
- Not run: `make verify` (no code changed), any real swarm call, `black`/`ruff`
  on the runner (no change).
