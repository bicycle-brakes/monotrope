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

## Addendum — 2026-10-20, review passes 2 to 19

Seventeen further read-only passes over the same subject add fifteen findings
(R-14 to R-28), correct two statements of the first pass, and document one.
Six of the seventeen passes found nothing new: from pass 14 on the yield of
that method drops visibly, and the loop's own core is thoroughly covered (125
loop, swarm, release and round tests, green). **The recommendation of this
addendum is to stop reviewing and start repairing.**

Cut-off: the first pass reviewed `59630b7`; this addendum reviews `94ae6cc`.
`git diff --stat 94ae6cc..5c7db34` is empty for `scripts/stage2.py`,
`scripts/stage2_availability.py`, `scripts/stage2_runs.py`,
`model-endpoints.yaml`, `prompts/04b-review-loop.md`, `docs/WORKFLOW.md`,
`provenance.yaml` and `decisions/gates.yaml` — every finding applies to the
current main (`5c7db34`, measured 2026-10-20). No file was changed in this
repository, no foreign model was called, no bead was written.

### Where the review stands

| Pass | Slice | Result |
|---|---|---|
| 2 | Governance, admission, Pi invocation | R-4, R-5 (already reported), negative results |
| 3 | Release parsing, red-first, projections | R-13 |
| 4 | Mutual exclusion, prompts | **R-14** |
| 5 | Round size, diff bounds | **R-15**; R-9 narrowed |
| 6 | Commit path, provenance, `PATH` | **R-16**, **R-17**, **R-18** |
| 7 | Post-run preparation, time limits | **R-19**, **R-20** |
| 8 | Formatter, gate definitions, `leakcheck.py` | **R-21**, **R-22**, negative result |
| 9 | Evidence chain of `repair` | **R-23**, **R-24**, R-11 documented |
| 10 | `parse_rows` with hostile answers | **R-25**, **R-26** |
| 11 | Release and round arithmetic over two releases | in order (measured) |
| 12 | Receipt lifecycle | in order |
| 13 | Exit codes, orchestrator contract | R-11 documented |
| 14 | Stage machine, simulated | in order |
| 15 | Credential path | in order |
| 16 | Paid prompt against the parser | in order |
| 17 | `probe` | **R-27** |
| 18 | Concurrency in `run_swarm` | in order |
| 19 | Doctrine against code | **R-28** |

### The new findings at a glance

| ID | Severity | Class | One line |
|---|---|---|---|
| R-14 | MAJOR | state | No mutual exclusion: two `review-loop` calls run the same stage twice |
| R-15 | MAJOR | cost | The paid diff is unbounded; Pi may silently summarise it and a `No finding.` then ends the loop |
| R-16 | MAJOR | control | The success path commits every changed path; the path guard exists only on the failure path |
| R-17 | MINOR | control | `git` is the only executable resolved through `PATH` |
| R-18 | note | planning | The free round's answer vocabulary must be added in `scripts/stage2.py`, not in `prompts/` |
| R-19 | MAJOR | control | The runner executes `scripts/plans_registry.py` from the attempt's tree, unsandboxed |
| R-20 | MINOR | time | The runner's own steps (`make verify`, `git`, ruff) have no time limit |
| R-21 | MAJOR | control | The runner executes `.venv/bin/ruff` from the attempt's tree; gitignored, invisible to the audit |
| R-22 | MAJOR | control | `decisions/gates.yaml` has no provenance class; an attempt may weaken the gates it must pass |
| R-23 | MINOR | evidence | A test inside a class (or `async def`) is refused as "defines no function" |
| R-24 | note | evidence | The runner proves the test but leaves the `Broke a test` mark to a human |
| R-25 | MINOR | parsing | An unescaped `|` in `Where` silently shifts the cells |
| R-26 | MINOR | parsing | A decorative blank table row becomes a finding |
| R-27 | MINOR | verbs | `probe` refuses when the free selection is empty, exactly when it is needed |
| R-28 | note | display | A continued run's release says `Rounds run: 1` above rows `L3-…` |

### Detail

#### R-14 — No mutual exclusion on the loop record (MAJOR)

**Evidence (read; no lock primitive exists anywhere in the runner).** No
`flock`, no lock file, no `O_EXCL` in `scripts/stage2.py` or
`scripts/stage2_availability.py`. The record is read, a round is appended and
the snapshot is written as separate file operations (`record_dir`,
`scripts/stage2.py:2036`; `write_state`, `:2270`; `release`, `:2373`). The
receipt is **not** consumed: `consume` (`stage2_availability.py:184`) returns
the state and leaves the file, and its `state["consumed"] == []` check stays
true until the first round has been written.

**Consequence.** Two invocations in the same moment — the repository allows two
writing sessions, and a retry started too early is the same situation — both
read `consumed: []`, both call the same free and Flash members, both pay, and
both append a round with the **same round number** into one record. The ids
`L<n>-<m>` then collide; `repair` refuses doubled taken ids (`:4245`) and
`release` cannot assign the reviewer marks any more. Together with R-2 the same
happens across two worktrees.

**Proposed repair.** `flock` the record directory in `prepare-loop`,
`review-loop` and `release-loop`; delete the receipt in `consume` once it has
been accepted, or mark it used.

#### R-15 — The paid diff is unbounded; Pi may silently summarise it (MAJOR)

**Evidence (read).** The free stage is capped by construction:
`FREE_DIFF_MAX_LINES = 400` per file and `FREE_DIFF_MAX_TOTAL = 2000` overall,
with a visible cut marker (`scripts/stage2.py:321`, `:322`, `:1507`, `:1546`).
The paid prompt takes `change_diff(root)` (`:2435`) with no bound at all and
puts it into the prompt (`prompt_for` inside `review_loop`); `change_diff`
includes every uncommitted and untracked file. Pi 1.2.0 compacts on overflow
instead of failing (read: `tools/pi/node_modules/@earendil-works/
pi-coding-agent/docs/compaction.md`, auto-compaction at
`contextTokens > contextWindow - reserveTokens`; "a provider context-overflow
error ... can select one compact-and-retry recovery attempt").

**Consequence.** On a large change a paid member reviews a **summary** of the
diff. A `No finding.` then makes the round clean and ends the loop — certified
on a diff nobody read in full. If the call fails instead, R-1 applies: the
stage cannot be retired. Both outcomes look identical in the record.

**Not measured:** whether Pi 1.2.0 in a `--print` run summarises or errors —
that needs a real call.

**Proposed repair.** Apply the free stage's bound to the paid diff (per file
and overall, with a cut marker in the prompt) and write into the round record
that the diff was cut.

#### R-16 — The success path commits every changed path (MAJOR)

**Evidence (read).** `run_attempts` (`scripts/stage2.py:3657`) computes
`allowed = {ctx.findings.relative_to(root)}` and uses it **only in the failure
branch**, in `restore_baseline(root, baseline, allowed, ignored_before)`
(`:3781`). A successful attempt ends in `checkpoint` (`:3079`), which runs
`git add -A` and commits. There is no path filter on that side. The prompt
boundary ("Change nothing else: the runner puts back every changed path outside
the change folder", `:264`) is an instruction plus clean-up in the *failure*
case only.

**Consequence.** A repair whose taken row names an ADR can edit the decision
document, and the runner commits it as `fix(<change>): …`. House rule 8
(decision pull request, `decide(...)` title, decision template, maintainer
merge) is then a human habit, not a check. The same holds for `prompts/`
(which `provenance.yaml:244` reserves for `human-written`) and for
`.claude/settings.json`, the file the merge brake lives in.

**Proposed repair.** Before the commit, intersect `changed_paths(root)` with
the `human-decided` and `human-written` prefixes of `provenance.yaml` (the
change folder excluded — ADR drafts live there) and refuse with
`restore_baseline`; the `paths:` reader already exists in
`check_frontmatter_current.py:112`.

#### R-17 — `git` is the only executable resolved through `PATH` (MINOR)

**Evidence (read; ruff reports six `S607`).** `RUFF` is deliberately a path
("the worktree's own ruff by a path with a slash, so `PATH` is never consulted",
`scripts/stage2.py:2508`), `python3` comes from `.venv` or `sys.executable`;
`git` is called as `["git", …]` in `_git_output` (`:2427`), `_free_candidate`,
`restore_baseline` and `red_first`.

**Consequence.** A `git` shim earlier on `PATH` disables `changed_paths`,
`restore_baseline` and the ref snapshot at the same time — exactly the guards
of R-16. Threat model is a local user, so this is minor, but it contradicts
the repository's own pinning discipline.

**Proposed repair.** Resolve `git` once at start and use that path everywhere.

#### R-18 — Where the free round's vocabulary belongs (note)

**Evidence (read).** `provenance.yaml` allows `ai-drafted-reviewed` for
`docs/WORKFLOW.md` and `plans/`, but only `human-written` for `prompts/`
(`:244`). The free round's missing vocabulary (R-9, below) therefore belongs in
`scripts/stage2.py` (`FREE_REVIEW_BODY`, `:1563`), not in
`prompts/04b-review-loop.md`.

#### R-19 — Runner-owned tooling runs from the attempt's tree (MAJOR)

**Evidence (read).** `prepare_derived` guards its own writes carefully —
outside the worktree refused, aliased paths refused, hard links refused
(`scripts/stage2.py:2862`–`2894`) — and then calls
`launch([sys.executable, "scripts/plans_registry.py", "--index"], root, env, key)`
(`:2891`) with `cwd = root`, that is: the worktree the model has just written.
`env` is `foreign_env({…})` (`:3051`), an allow-list, but it carries the
**real `HOME`, `PATH`, `TMPDIR`**. The API keys are not in it; the rest of the
account is.

**Consequence.** A model with write access (GLM `Edit`/`Write`, Codex
`workspace-write`) can place a line in `scripts/plans_registry.py` that the
runner then executes **outside the model's sandbox**, with network and home
directory. The guards around `stamp` show that the tree was treated as
untrusted; the launch from that same tree does not. `make verify` runs from the
same tree and with the same real `HOME` (`:3064`, `:4042`) — that is
unavoidable, because the gates must measure the attempt. `plans_registry.py`
is runner-owned tooling, not a gate, and could come from the baseline.

**Not measured:** that a model would do this.

**Proposed repair.** Read `scripts/plans_registry.py` from the baseline
(`git show <baseline>:…`) into a temporary directory and run it there, with a
scratch `HOME`. One test: an attempt that edits `plans_registry.py` must not
have that code run.

#### R-20 — The runner's own steps have no time limit (MINOR)

**Evidence (read).** Every foreign call is bounded (`REVIEWER_MINUTES = 30`,
`PI_DISCOVERY_SECONDS = 120`, `RED_FIRST_MINUTES`), and `docs/WORKFLOW.md:882`
names the 30 minutes for loop calls. The runner's own steps run without a
limit: `make verify` (`scripts/stage2.py:3064`, `:4042`), `plans_registry.py`
(`:2891`), ruff (`:3011`), every `git` call (`_git_output`, `:2427`).

**Consequence.** A hanging gate (a test waiting on the network, a stale
`index.lock`) blocks the verb without a diagnostic, and a killed run leaves the
attempt's files behind without the clean-up audit a failed attempt gets.

**Proposed repair.** A generous bound (e.g. 60 minutes) with a **named**
abort — never a silent cut, because a truncated gate would be a wrong result.

#### R-21 — The formatter the runner trusts lies in the attempt's tree (MAJOR)

**Evidence (read).** `RUFF = ".venv/bin/ruff"` (`scripts/stage2.py:2508`) and
`launch([RUFF, *command, *targets], root, env, key)` (`:3011`) with
`cwd = root`. `.venv/` is gitignored (`.gitignore:30`), so `changed_paths` and
`attempt_files` (`:2711`, `git diff-tree`) never see it. `ignored_snapshot`
(`:2475`) knows which ignored files changed, but only uses that to search them
for the API key (`remove_changed_credential`). `restore_baseline` removes only
**created** ignored paths (`created = keys - ignored_before`) — an
**overwritten** `ruff` stays.

**Consequence.** A model with write access places a line in `.venv/bin/ruff`;
the runner executes it afterwards, unsandboxed, with the real `HOME`. That is a
sandbox escape, and no audit line names it.

**Proposed repair.** Hash the executables the runner itself starts (`ruff`,
`pytest`, `make`) before the call, compare before use, and fail the attempt
with the path named on a mismatch. `.venv` stays per worktree by design;
comparing is cheaper than forbidding.

#### R-22 — `decisions/gates.yaml` has no provenance class (MAJOR)

**Evidence (measured).** `grep "gates.yaml" provenance.yaml` finds nothing.
`docs/adr/`, `decisions/answers/` and `decisions/adoption.yaml` are
`human-decided` (`provenance.yaml:140`–`153`); the gate definition is not
classified at all. That file is the single source of the gates: `verify_all.sh`
asks `scripts/ci_gates.py`, which reads it, and `.github/workflows/ci.yml` is
generated from it (`decisions/gates.yaml:1`–`10`). `enforcement` is the closed
vocabulary `advisory / report / block`.

**Consequence, together with R-16.** A repair attempt can turn
`enforcement: block` into `advisory`, `make verify` then reports green (it *is*
green), the runner commits it as `fix(...)`, and CI inherits the weakened set.
No gate checks the file's strictness: `gate-schema` checks its shape,
`ci-drift` its agreement with the generated workflow.

**Proposed repair.** A provenance class for `decisions/gates.yaml` (and for
`provenance.yaml` itself) — the maintainer's decision, not an agent pull
request; afterwards the commit guard from R-16 covers it.

#### R-23 — A test inside a class is refused as missing (MINOR, reproduced)

**Evidence (reproduced with the runner's own predicate).**
`check_repair_answer` looks the test up with
`any(line.startswith(f"def {function}(") for line in body.splitlines())`
(`scripts/stage2.py:3525`). `FIXED_TEST` (`:354`) accepts the name `test_…`
before that, so only the lookup is wrong:

| line in the test file | accepted |
|---|---|
| `def test_reports_doubled_failure(monkeypatch):` | yes |
| `async def test_reports_doubled_failure(monkeypatch):` | **no** |
| `    def test_reports_doubled_failure(self):` | **no** |

**Consequence.** A repair whose only evidence is a `unittest.TestCase` test (or
an `async` test) is refused with "`<file>` defines no function `def <name>(`"
— one paid attempt is gone and, with R-1, the stage cannot be retired. This
repository has no `class Test` in `tests/` (measured); an instance with classic
tests does.

**Proposed repair.**
`re.search(rf"^\s*(?:async\s+)?def\s+{re.escape(function)}\s*\(", body, re.M)`.

#### R-24 — The runner proves the test and leaves the mark to a human (note)

**Evidence (read).** `repair` proves red-first and writes `fixed — tests/…`
(`scripts/stage2.py:3529`–`3535`), but writes **no** `Broke a test` mark —
ADR 0017 and the docstring of `mark_repaired_findings` ("Only the Status cell
(index 7) of a taken row changes", `:3550`). The human writes the mark and
`undecided_refusal` (`:2106`) demands it for `fixed` rows.

**Consequence.** The mark can contradict the proof: the runner has just shown
the test was red on the baseline (`yes`), the human writes `no`, and nothing
checks it.

**For decision.** For `fixed — tests/…` the runner could write `yes` itself
(it holds the proof) and refuse a contradicting hand mark; for
`fixed — not a test` the mark stays the human's.

#### R-25 — An unescaped `|` in `Where` shifts the cells (MINOR, reproduced)

**Evidence (reproduced).** `parse_rows` (`scripts/stage2.py:635`) takes
`cells[:5]` and joins `cells[5:]` into the finding when a row has more than six
cells and its second cell is a severity (`:653`).
`| L1 | MAJOR | SPEC | base | a|b | a defect |` becomes
`Where = "a"`, `Finding = "b \| a defect"`. The row stays valid; the location
is wrong; nothing warns.

**Consequence.** The prompt asks for `\|`; a model that forgets it gets a
misfiled row instead of a refusal, and the orchestrator decides on a finding
whose `Where` is meaningless.

**Proposed repair.** Refuse a row whose cell count exceeds six and whose
finding was joined — or name the repair in the round's notes (`Where`
ambiguous, row kept as it came).

#### R-26 — A decorative blank table row becomes a finding (MINOR, reproduced)

**Evidence (reproduced).** `| | | | | | |` yields
`['', '', '', '', '', '']` and is accepted as a row (`parse_rows`).

**Consequence.** `numbered` makes `L<n>-<m>` with empty cells, `undecided`
demands a decision, `release` writes the empty row into `findings.md`, and
`stage2_runs.measure` counts it.

**Proposed repair.** Drop a row whose cells are all empty, as `_furniture`
drops the header and the separator.

#### R-27 — `probe` refuses when the free selection is empty (MINOR)

**Evidence (read).** `probe` calls `discover_free(root)` without `allow_empty`
(`scripts/stage2.py:4552`); `prepare` calls
`discover_free(root, allow_empty=True)` (`stage2_availability.py:103`). When no
id matches the free rule — exactly the case in which the compatibility probe
for the paid ids is wanted — `probe` refuses before any call.

**Proposed repair.** `allow_empty=True` and skip the free stage, as `prepare`
does.

#### R-28 — A continued run's release says `Rounds run: 1` above rows `L3-…` (note)

**Evidence (read).** `release` writes
`Rounds run: {len(ROUND_HEADING.findall(record))}` (`scripts/stage2.py:2400`),
that is, only the rounds of the current record. After an earlier release and
three further rounds the block says `Rounds run: 1` above rows whose ids begin
`L4-`. The *count* is right (`rounds_run` sums every block); the *display*
confuses.

**Proposed repair.** Name the round numbers of the block, or the total, beside
the count.

### Corrections to the first pass

- **R-13 is half wrong.** `prompts/04b-review-loop.md:9`–`13` already
distinguishes the three cheapest reachable members of an availability-enabled
run from the legacy `flash_swarm` list. Only `docs/WORKFLOW.md:1099` is stale.
The merged text of this file overstates the prompt half; the finding stands for
`WORKFLOW.md` only, and that file allows `ai-drafted-reviewed`.
- **R-9 is narrower than written.** Severity is not validated for a six-cell
row; the reporting module (`scripts/stage2_runs.py:152`) deliberately counts an
unknown word as `other`, and no gate hangs on it. What remains: the free prompt
names no vocabulary while the paid prompt names `SPEC`/`MAINT` and
`BLOCKER`/`MAJOR`/`MINOR` (`prompts/04b-review-loop.md:48`), and round 1 of the
real run answered "Medium/Security/Correctness".
- **R-11 is a documentation gap, now measured.** The loop's clean end is a
`Refused` with exit 2 and the word `refused:` (`scripts/stage2.py:4367`,
`:4712`); no document explains that a finished clean loop is reported as a
refusal (`grep "exit 2"` in `docs/WORKFLOW.md` and
`prompts/04b-review-loop.md` finds only the Pi version check).

### What the later passes confirmed — so nobody repeats them

- **`leakcheck.py` is sound** (471 lines read): it scans the change folder, the
  whole tree, the message and patch of every commit reachable from a branch,
  the staged diff and every prompt text; it refuses a missing, empty or invalid
  denylist, so a clean report cannot come from measuring nothing; it never
  prints the match; only `secret:` rules are exempt under `tests/`; and it
  states what it cannot see (reflog, stash, tags, `refs/dolt/`).
- **The red-first machinery holds** (`red_first`, `scripts/stage2.py:3160` ff.):
  token-bound private report, exit 2/3 not read as red, fixture and skip
  outcomes refuse, refs snapshotted before and after, temporary worktree
  removed before pruning — and it runs in a **baseline** worktree, unlike R-19.
- **The evidence chain of `repair` is not escapable:** `fixed — not a test` on a
  code row is refused by name (`:3513`–`3516`); `fixed_status` refuses `.`/`..`
  segments and non-`test_` files (`:3424`–`3428`); the attempt's own edits to
  `findings.md` are reverted and row counts are compared.
- **No lock primitive exists in the repository** to reuse — `tests/test_lock.py`
  is about the dependency lock; R-14 needs a new `fcntl` helper.
- **`scripts/stage2_runs.py` is a counter, not a second state store:** it reads
  `findings.md`/`research.md`, tolerates unknown severities and extra columns,
  and counts only **released** loop rows (a running loop shows 0 rows, by
  design).
- **The Pi invocation is contract-tested:** `tests/test_pi_contract.py` with
  `tests/pi_contract_driver.mjs` starts the pinned install offline; every flag
  and tool name the runner uses exists in 1.2.0 (measured with
  `tools/pi/pi --help`), and `--append-system-prompt <path>` really reads the
  file (`dist/core/resource-loader.js:104`).
- **The loop is well tested:** `pytest tests/test_stage2.py -k "loop or swarm or
  release or record or round"` → **125 passed, none skipped, none xfail**
  (measured 2026-10-20, 106 s).
- **Argument handling is tight:** `--stage2-off` only for
  explore/implement/repair, `--availability-reported` only for `review-loop`,
  `--model`/`--handover` only for `session`, including the refusal of the
  `--stage2-off <change>` mix-up (`:4688`–`4702`).

### Suggested pull-request cut

1. **R-25 + R-26 + R-27 + R-23** — parser and evidence lookups; four small
   changes, one test each; no decision needed.
2. **R-16 + R-17 + R-22** — the commit guard and the gate definition; R-22 is
   the maintainer's provenance decision, R-16 and R-17 are code.
3. **R-19 + R-21 + R-20** — the runner executes only its own, hashed, bounded
   tooling.
4. **R-14 + R-2 + R-3** — state and files: lock, worktree-keyed record,
   line-anchored cut.
5. **R-15** — the paid diff bound, on its own, because it changes what a
   review sees.

Decisions still open for the maintainer: **R-1** (may a stage be retired?),
**R-4** (does the deny list bind the code?), **R-5** (is the read boundary
accepted in writing or enforced?), **R-22** (provenance class for the gate
definition), **R-24** (may the runner set the `Broke a test` mark it proved?).

### Next step for the orchestrator

Open the block of four small parser and evidence fixes (R-25, R-26, R-27,
R-23) as one pull request with tests; it needs no decision, removes four ways a
round can be misfiled or refused, and is the cheapest place to start. Then the
state block (R-14, R-2, R-3).

### Validation of this addendum

- `git diff --stat 94ae6cc..5c7db34 -- <reviewed files>`: empty (measured
  2026-10-20), so every finding applies to `5c7db34`.
- `tests/test_feedback_channel.py`: 54 passed, 13 skipped (measured
  2026-10-20 on the first pass; re-run with this addendum).
- `scripts/check_frontmatter_current.py --root .`: green over 309 documents
  (first pass); re-run with this addendum.
- Reproduced with the runner's own functions: R-23 (the `def` predicate),
  R-25 and R-26 (`stage2.parse_rows`), R-21's visibility gap
  (`ignored_snapshot`/`restore_baseline` read).
- Not run: any foreign model call, `make verify` (no code changed).
