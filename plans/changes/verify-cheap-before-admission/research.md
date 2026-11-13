---
title: "Research — verify-cheap-before-admission"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# verify cheap before admission — Research

Phase 1's runner-returned exploration is preserved below; the dated draft
addendum resolves repository gaps needed for the specification and plan.

Stage-2 call, 2026-11-13: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1044 files, 4105 commits, 12 rules.

## Runner exploration — 2026-11-13

Research complete. Below is the prose ready to append to `plans/changes/verify-cheap-before-admission/research.md`.

---

## What exists today

**The admission wraps the whole run, not single gates.** `scripts/verify_all.sh` (the local runner of the one gate list) hands itself to the admission supervisor before anything else is chosen: after interpreter selection it probes `"$PYTHON" -m scripts.verify_lock --held` and, when no valid inherited marker exists, `exec`s `scripts.verify_lock -- bash scripts/verify_all.sh <original args>` (verify_all.sh, `ORIGINAL_ARGS`, the `--held` probe and the re-exec; comment cites bead coding-harness-p6mu). The report (`ci_gates.py --report`, gate-list fetch (`--commands --placement lokal --tsv`), run identity (`dur_call RUN_ID start`) and every gate command therefore all run inside the one admission today. The ruff failure the interview cites (decisions.md Q-1: a lane waited 710 s and then failed in seconds) is exactly this order — every seconds gate sits behind the lock.

**The gate list carries the cost class already.** `decisions/gates.yaml` is `schema_version: 3`; `cost` is a required closed vocabulary (`seconds`/`minutes`, header block "cost", bead coding-harness-bxxt.1), validated in `validate_schema()` in `scripts/ci_gates.py` (`cost muss eins von …`). Of the 24 declared gates exactly two are `minutes`: `pytest` and `leerprobe`; the other 22 are `seconds` — matching the count in decisions.md Q-1. The local run already orders by it: `kostenordnung()` (ci_gates.py) sorts selected gates seconds-before-minutes, applied only under `--commands --placement lokal` (the `main()` commands path), and the runner stops at the first red blocking gate and names the gates it did not run (verify_all.sh, the `stop_gate`/`verbleibend` loop and not-run summary; bead coding-harness-bxxt.1).

**But the runner cannot see the class.** The TSV the runner consumes is `id<TAB>enforcement<TAB>command` only (`--tsv` help text and the print in `main()`, ci_gates.py; consumed in verify_all.sh's `while IFS=… read -r gid enf cmd` loop). The cost class exists in `gates()`'s dict (`"cost": g["cost"]`) but never reaches the runner.

**The admission mechanism itself.** `scripts/verify_lock.py` queues protected entries of one user on one machine (registration order FIFO in `verify.queue/` under the shared state root `${XDG_STATE_HOME:-~/.local/state}/coding-harness/`), holds the work lock `verify.lock` (flock, descriptor inherited by the protected child), publishes ownership `verify.holder.json` (pid, token, command, start, admission id and measured wait), gates on system free memory (25 % floor, `HARNESS_VERIFY_MEMORY_FLOOR`, refusal after 60 minutes below it), and supports nested entries via `HARNESS_VERIFY_LOCK_HELD`/`HARNESS_VERIFY_LOCK_TOKEN` (`nested_holder_pid()`; refusals exit 2/3 via `VerifyLockRefused`/`MemoryFloorRefused`). The docstring states `scripts.stage2` holds the same admission around its timed local checks, and that queue/memory waits consume neither `VERIFY_SECONDS` nor a pytest proof's execution timeout. Nesting already works: a runner check descended from a live admission re-enters without a second queue wait (`hold_admission`/`supervise` inherited path).

**Measurement history exists and already reads the tree.** `scripts/verify_duration.py` appends version-1 events (`run_start`, `gate`, `run_end`) to `verify-duration.jsonl` under the same shared state root. `cmd_start` records commit, `dirty` from `git status --porcelain`, gate-file digest, job, placement, memory percentage, worker setting and the admission context (`_context_fields` → `admission_id`, `admission_wait_seconds`, `admission_reused`; bead coding-harness-1um6). verify_all.sh measures around each gate command (`dur_call g_t0/g_t1`, per-gate seconds beside the verdict) and its comment defines execution seconds as "from the admitted runner's measurement start to its final verdict; the admission wait is reported beside it, never inside it" — a definition the two-phase order touches.

**A precedent for cheap-before-expensive inside one runner exists in stage 2:** the runner's cheap checks and the repair's targeted check run ruff/pytest subsets before/outside the admitted full `make verify` (scripts/stage2.py, `CHEAP_LABEL`, `TARGETED_LABEL`, comment "all outside the machine-wide verify admission"); touching `scripts/verify_all.sh`, `ci_gates.py` or `verify_lock.py` is in `SHARED_INFRASTRUCTURE`, which forces the full check for repairs of this change.

**Demand analysis neighbour.** `docs/research/2026-11-09-make-verify-long-term.md` measured the slot as the bottleneck: one ~22-minute slot serves at most ~65 runs a day, lanes ask 34–43, waits reach the size of a run; "the wait at the full check (`make verify`) is a demand problem"; its target picture already holds "Full: once per change before phase 6; again only when the tree changed". This change is the "need the admission less" lever that note names.

**Doctrine text describing today's order:** `docs/WORKFLOW.md` ("Local verification orders selected gates by declared cost…"; "One admission per user and machine — Before its gates, `verify_all.sh` hands the run to `scripts.verify_lock`"; the duration-history paragraph), `docs/how-it-works.md` ("One admission per machine"), `docs/orchestration.md` (the "One verify-bearing step at a time, memory floor" table row). `Makefile`'s `verify` target delegates to `bash scripts/verify_all.sh`; hosted CI runs each gate as its own derived step and never enters this path (`generate_ci()` in ci_gates.py; "Hosted CI is untouched", WORKFLOW.md admission section).

**Kit travel.** `scripts/kit/manifest.yaml` classifies as mechanism: `scripts/verify_all.sh`, `scripts/verify_lock.py`, `scripts/verify_duration.py`, `scripts/ci_gates.py`, `decisions/` (incl. gates.yaml), `tests/test_verify_lock.py`, `tests/test_verify_duration.py`. `tests/test_verify_cheap_first.py` has no own rule and falls under the `tests/` catch-all (bestand) — it does not travel. Any new helper script needs its own classification rule (longest matching prefix wins).

**Tests holding today's behaviour.** `tests/test_verify_cheap_first.py` (18 tests: cost-schema rejection, local order with ties, catalogue costs, early stop, not-run summary, green run, nonblocking continue, `--ci` exhaustive, repair-diagnostics parsing, history-only-executed, transferred-kit smoke `test_transferred_kit_stops_before_expensive_gate`); `tests/test_verify_lock.py` (~30 tests: queue order, nesting, memory floor, signals, refusals, admission measurement); `tests/test_verify_duration.py`; and the frame guard `tests/test_stage2.py::test_the_frames_red_sections_reads_are_the_ones_verify_all_prints`, which pins the printed gate frames (`── [<gate>] $ `, `── [<gate>] RED (block)`) that the repair-evidence parser reads.

**Jobs other than verify are seconds-only today.** `drift` holds two seconds gates (`plans-registry-strict`, `research-currency`); the `docs` subset gates are all `seconds` (per `subsets: [docs]` entries in gates.yaml). A local run of `--job drift` or `--job docs` therefore never contains a minutes gate today.

## Where it lives

Admission boundary: `scripts/verify_all.sh` (re-exec block, then report/selection/loop). Cost classes and ordering: `decisions/gates.yaml`, `scripts/ci_gates.py` (`validate_schema`, `gates()`, `kostenordnung`, the `--commands/--tsv` path). Admission engine: `scripts/verify_lock.py`. Measurement: `scripts/verify_duration.py`. Doctrine: `docs/WORKFLOW.md`, `docs/how-it-works.md`, `docs/orchestration.md`, `docs/testing.md`. Demand analysis: `docs/research/2026-11-09-make-verify-long-term.md`. Runner-behaviour tests: `tests/test_verify_cheap_first.py`; admission tests: `tests/test_verify_lock.py`. Kit classification: `scripts/kit/manifest.yaml`. Interview: `plans/changes/verify-cheap-before-admission/decisions.md` (Q-1…Q-5, answered 2026-11-13).

## What is unclear about it

- Whether any current `seconds` gate writes shared state and needs Q-1's explicit exception mark now: the gate reasons in decisions/gates.yaml describe readers (tracker render, full history checkout) and no declared writer. The mark may be schema headroom only — the spec must say which.
- How Q-2's "tree changed during the wait" is compared: `git status --porcelain` exists as a recorded reading (`cmd_start`'s `dirty` field) and `report()` binds commit/base/config hash, but no tree-fingerprint helper exists anywhere in `scripts/`. What counts (tracked edits, untracked files, index) is not stated in any artifact.
- The duration-event meaning under two phases: `run_start` is created after admission today and execution seconds are defined from that point (verify_all.sh duration comment). Whether one run identity spans both phases or the pre-admission phase records separately is decided nowhere.
- The two regimes' interplay: the current runner has one regime (cheap-first, stop at first red, bead bxxt.1); Q-3 adds an exhaustive pass for the pre-admission seconds gates ("all red ones reported at once", then end without requesting admission). Whether the stop-at-first-red regime stays for the admitted phase, and how the not-run summary and the evidence parser describe each phase, is open.
- Job scope: Q-1's rule is per gate; how `--job docs` and `--job drift` behave under it (today seconds-only, hence admission-free under the rule) is implied but not written.
- `plans/changes/verify-step-limit/` (bead coding-harness-xkvr, implementation_status: partial) raises the runner's `VERIFY_SECONDS` around `make verify`; its launch sites measure the whole check, and the change interacts with any two-phase split. Its exact launch sites were not read in this pass.
- The stop hook (phase 5, "blocks on a red tree") appears in the repository only as doctrine text (docs/WORKFLOW.md; docs/testing.md:94); no hook script exists in the tree (Glob `**/*stop*` matches only vendored node_modules files). Whether it invokes `make verify` and is affected was not readable here.
- The tracker state of bead coding-harness-bxxt/.6 was not read: no rendered copy is committed and the reader (`scripts/bead_render.py`) was not run in this phase.

## Which files a change would have to touch

`scripts/verify_all.sh` (admission boundary, run identity/report/selection placement, gate loop, summaries); `scripts/ci_gates.py` (the TSV payload must carry the cost class or a new flag; `kostenordnung()` already supplies the split); `decisions/gates.yaml` only if the Q-1 exception mark becomes a schema field (held path — the orchestrator owns it, per verify-cheap-first spec "Protected areas"; a schema bump and the derived `.github/workflows/ci.yml` + `docs/governance/gate-catalog.md` regeneration follow via the `gate-schema`/`ci-drift` gates); `scripts/verify_lock.py` likely unchanged (`supervise`/`hold_admission` accept any command); `scripts/verify_duration.py` if events must distinguish phases; doctrine text in `docs/WORKFLOW.md`, `docs/how-it-works.md`, `docs/orchestration.md`, `docs/testing.md`, `prompts/05-verify.md`; tests in `tests/test_verify_cheap_first.py` (or a sibling), `tests/test_verify_duration.py` (if event schema changes), and the frame guard in `tests/test_stage2.py`; `scripts/kit/manifest.yaml` only if a new script is added.

Neighbours found: `plans/changes/verify-cheap-first/spec.md` (bead coding-harness-bxxt.1, implemented, phase 6 clean 2026-11-12), `plans/changes/verify-step-limit/spec.md` (bead coding-harness-xkvr, partial), `plans/specs/implementation-verification/spec.md` (living spec, bead coding-harness-mfv), `plans/changes/archive/2026-11-06-verify-machine-lock/spec.md`, `plans/changes/archive/2026-11-06-verify-duration/spec.md`, `plans/changes/archive/2026-11-06-verify-worker-cap/spec.md` (all archived; not read in this pass beyond their existence), `docs/research/2026-11-09-make-verify-long-term.md`.

## Draft gap resolution — 2026-11-13

Repository evidence below was read at `b1d4e621`; implementation is not started.

- **The outer runner must participate.** `scripts/stage2.py::full_verify`,
  `verify_attempt` in full mode, and `verify_draft` each acquire
  `verify_lock.hold_admission` before launching the full or document check.
  Full-mode preparation, including formatting and the attempt's cheap checks,
  also sits inside that admission. Moving only the shell's admission would
  leave these paths waiting before cheap gates. The targeted path already
  prepares outside admission. The common gate scheduler must therefore also
  serve these three runner paths; targeted checks and independently admitted
  proof/import probes are separate operations and retain their rules.
- **Execution limits have an existing seam.** `stage2.launch` takes a timeout,
  starts a process group, registers it for cancellation, kills it on timeout,
  and ends lingering descendants before returning. The new scheduler can use
  it as its gate-execution callback, with the remaining shared execution
  allowance. Waiting in `hold_admission` stays outside that allowance without
  adding an unbounded outer `make` subprocess. This changes the runner's
  internal launch route, not gate membership: the shell entry point and the
  runner use the same scheduler and reader. Existing tests of a whole-run
  `make` stand-in must become tests of real scheduler gates and preserve the
  timeout, cleanup, refusal, environment and diagnostic assertions.
- **Selection need not change the TSV contract.** `ci_gates.gates()` already
  returns normalized records, and `in_job`, `misst_in`, and `kostenordnung`
  supply selection and local ordering. A common Python scheduler can consume
  those records directly. Existing `--tsv` consumers in
  `tests/test_gate_machinery.py`, `tests/test_ci.py`, and
  `tests/test_verify_cheap_first.py` can keep their three-column interface.
- **No current exception is identified.** The declared seconds commands use
  read/check modes, including `plans_registry.py --check`,
  `check_frontmatter_current.py` without `--stamp`, schema/CI comparisons,
  and the ruleset assertion tests. Tracker readers use
  `bead_render.py`/`render_beads_export.py::_render_nach`, which exports through
  `tools/bd` into a private temporary file; this is not a tracker update.
  `check_research_currency.py` can append to the caller's
  `GITHUB_STEP_SUMMARY`; that is a job's report, not machine-shared verification
  work. Tool caches and per-run reports do not alone require the machine's
  expensive-work slot. None of the current seconds gates is proposed for the
  exception mark. Implementation must audit these entry points again before
  activating the held gate-list documentation; no blanket claim is made about
  future gates or third-party tool internals.
- **Fingerprint scope is an implementation detail still to define.** A dirty
  boolean or porcelain status alone cannot detect a second edit to an already
  dirty file. Compare HEAD identity, semantic index entries, tracked working
  contents/types/modes/deletions, and non-ignored untracked paths and contents.
  Use NUL-delimited Git path inventories and bounded reads; an unreadable or
  unstable snapshot cannot authorize reuse. This is an in-run comparison, not
  a cache of gate results between invocations. External tracker, network and
  machine state are not frozen by a repository comparison.
- **Available draft gates.** `templates/plan.md` and
  `scripts/validate_change_artefacts.py` do not exist in this checkout. The
  spec/design templates, phase-3 prompt, interview check, criterion-ledger
  check and plans registry do. `findings.md` contains the draft-call record
  only; it has no phase-2a rows to resolve. Live pull-request state, current
  interactive-session inventory and tracker task state were not read within
  this runner's worktree-only boundary. The latest local handover read was
  `docs/journal/handover/2026-11-13-night-five-lanes.md`; it predates this change.
