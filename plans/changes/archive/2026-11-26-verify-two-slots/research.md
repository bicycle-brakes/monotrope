---
title: "Research — verify-two-slots"
status: accepted
implementation_status: done
date: 2026-11-20
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-20", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# verify two slots — Research

Stage-2 call, 2026-11-20: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1145 files, 4927 commits, 12 rules.

## Runner exploration — 2026-11-20

Research complete. Here is the phase-1 report for `verify-two-slots`, ready to append to `plans/changes/verify-two-slots/research.md`.

---

## What exists today

**The bead and why.** Bead `coding-harness-u1ha` ("two verify slots") was decided on 2026-11-09 as a stopgap against the wait at the full check: `docs/research/2026-11-09-make-verify-long-term.md` ("What the figures say together") measures 151 full runs over 2026-11-04..09 with 77.3 h queue wait against 57.1 h execution, median wait 22–30 min, one slot serving at most ~65 runs/day; "A second slot … halves the load per slot" — bounded by the machine (Darwin arm64, 8 logical cores, 8 GiB, per bead `coding-harness-351h`, figures not re-read today). The same note records the anti-target: three concurrent full runs once took >30 min each against 11–12 min serial (bead `coding-harness-p6mu`), which is why the lock exists and why two is the ceiling, not three. The note's "Proposed order of work" step 1 names u1ha "a stopgap, measured as its decisions record demands".

**Prior lane state (the re-slice).** The work lived as `verify-slots` on branch `feat/verify-slots` (worktree `verify-slots`). `docs/journal/handover/2026-11-11-day-decisions-six-lanes.md` records the then-decided Boundary — "one process holds at most one admission; a second is refused (spec 'Boundary', `bca8a129`)" — and that the lasting fix, "each admission an explicit handle", was split out as bead `coding-harness-42em`. Later handovers trace the lane's end: two repair rounds accepted (`bb1c93ca`, handover 2026-11-11-night-run-twelve-lanes), a serial full verify green at `8a94178f` with "2×6 and 4×3 trials owed" (handover 2026-11-15-night-run-2026-11-14-a-ended), spec redrafted twice with phase-2a holding (`feat/verify-slots` @ `b5c2105b`, handover 2026-11-18-night-run-2026-11-17-a), and the phase-6 row F6-1 failing all three repair attempts — "Codex twice with 'no tests ran', then Sonnet on its own test. Attempt 3's tree is in the worktree's `stash@{0}`" (same handover, L2). The maintainer's 2026-11-17 answers, carried in `docs/journal/handover/2026-11-17-night-plan-2026-11-17-a.md` (L2 row): S2-1 answer B "record the figures and do not gate 3×4"; "The 1.6× of decision Q-4 is scoped to two slots" — a measured wall-time figure for two slots vs serial, recorded only in handover prose in this tree. The 2026-11-19 handover lists "L2 (coding-harness-u1ha) still needs its re-slice"; this folder, opened by commit `7e48774f` on `feat/verify-two-slots`, is that re-slice.

**The admission, as this branch's code has it.** `scripts/verify_lock.py` is "one machine-wide admission for protected verification work" (module docstring, line 2), shared across repositories and worktrees through `${XDG_STATE_HOME:-~/.local/state}/coding-harness/` (`state_root()`, lines 198–200):

- One exclusive work lock `verify.lock` (`LOCK_NAME`, line 125), kernel-backed `fcntl.flock`. FIFO comes from records in `verify.queue/` (`RECORD_NAME`, line 130) under a short-held `verify.registry.lock`; the turn-taking rule is "only the first live record may try the work lock" (docstring line 20, enforced at `_Admission._queue_wait` line 692: `records[0] == self.record_name and self._try_acquire_work()`).
- One published holder record `verify.holder.json` (`HOLDER_NAME`, line 126), written atomically (`_Admission._publish`, lines 651–679); `read_holder` (248–273) and `_describe_holder` (276–282) assume exactly one holder.
- A memory gate held per admission after the lock: `_Admission._memory_gate` (708–732), floor 25 % (`DEFAULT_MEMORY_FLOOR`, line 117; override `HARNESS_VERIFY_MEMORY_FLOOR`, `memory_floor()` 392–403, equality admits), 30 s recheck, refusal after 60 min (`MemoryFloorRefused`, exit 3); an unmeasurable reading logs and proceeds (`read_available_memory`, 356–389).
- Nested entries reuse the ancestor's admission through `HARNESS_VERIFY_LOCK_HELD` + `HARNESS_VERIFY_LOCK_TOKEN`, validated against the published holder and a probe that the lock is genuinely held (`nested_holder_pid`, 285–318); `hold_admission` (735–758) yields `None` for a valid nested entry. A killed supervisor's inherited descriptor keeps the lock (`release`, 553–555; pinned by `test_release_keeps_the_lock_held_by_an_inherited_descriptor`, `tests/test_verify_lock.py:872`).
- Admission context (bead `coding-harness-1um6`): `admission_id` and measured wait published in the holder record and handed to protected children (`_spawn_child`, 856–872); `admission_context()` (463–491) resolves own → handed → inherited with a `reused` flag.

**The boundary refusal is not on this branch.** `hold_admission` consults only the environment marker; `_ACTIVE` (lines 416–437) serves only to publish pid/token to children, and a grep for "at most one"/"second admission" over `scripts/` finds no refusal. So on this tree a second in-process admission would queue behind itself; the one-admission-per-process refusal named in the 2026-11-11 decision exists, as far as this tree shows, only on the unmerged `feat/verify-slots` branch (commit `bca8a129` is not verifiable from here). This is a not-there statement about this branch, not about the lane's history.

**The scheduler and its callers.** `scripts/verify_run.py` runs the two phases: all unprotected (`seconds`) gates first, then ONE admission `verify_lock.hold_admission(admission_command or ["verify-run", job])` around the whole protected set (`run_verification` steps 3–5, lines 917–968), with tree snapshots around the cheap pass (`tree_snapshot`, 278–300) and cheap-result reuse inside a stable tree. The held lock descriptor is published into `lock_slot`/`slot` `{"fd": …}` and handed to protected gates via `pass_fds` (`gate_process`, 493–505). `scripts/verify_all.sh` is bootstrap only (docstring lines 9–15) and already gives each run a pid-named pytest temporary area under a managed per-user parent (`verify-runs-<uid>`, lines 121–160, bead `coding-harness-bxxt.3`) — slot-independent today. `scripts/stage2.py` calls `run_verification` in-process for the full check (imports at line 208; call at 6345–6346; `full_verify` at 7255) and the targeted check takes its own admission through `verify_lock.hold_admission` (lines 8067, 8257, 8279) — targeted checks and full checks share the same slots. Worker sizing (`worker_bound`/`worker_default`, `scripts/verify_run.py:324-365`, bead `coding-harness-l7sc`: half the cores, memory in 2-GiB steps) is what two concurrent full checks will exercise; it is exported as `PYTEST_XDIST_AUTO_NUM_WORKERS` per run.

**Doctrine and pins.** `docs/WORKFLOW.md` §"One admission per user and machine" (lines 583–613) states the single admission, registration order, wait logs naming the holder, the memory floor and the refusals; line 560 says "one admission" in the two-phase paragraph. `decisions/gates.yaml` header lines 50–59 say "The minutes gates then run inside one admission"; `docs/governance/gate-catalog.md` lines 36–40 describe admission as "that machine slot". The seconds-gate audit (`plans/changes/verify-cheap-before-admission/seconds-gate-audit.md`, 2026-11-14) found no `seconds` gate needing `needs_admission` and measured six concurrent lanes of the 21 unprotected gates against serial verdicts — the existing evidence that concurrent cheap work is safe. `scripts/ci_gates.py:255-258` carries the manifest description of `verify_lock.py`; `scripts/kit/manifest.yaml` lists `scripts/verify_lock.py` (line 94) and `tests/test_verify_lock.py` (line 240). Single-slot behaviour is pinned by `tests/test_verify_lock.py` (`test_independent_entries_share_one_machine_lock` :185, `test_live_waiters_enter_in_registration_order` :211, `test_queue_wait_logs_live_holder_and_progress` :248, `test_only_live_ancestor_ownership_allows_nested_admission` :312, the memory-gate cluster :508–:763, `test_admission_measurement_survives_cli_and_inherited_context` :1187) and by `tests/test_verify_before_admission.py` (`test_only_protected_work_enters_one_admission` :380, cheap-result reuse :444/:473, wait-exclusion :542). `tests/test_verify_duration.py` pins the history rows (`admission_requested`, `admission_id`, `admission_wait_seconds`, `admission_reused` — `scripts/verify_duration.py` `_context_fields`, 281–287). Unrelated: `scripts/outcome_test.py` has its own flock loop (lines 767–775), not this admission.

## Where it lives

`scripts/verify_lock.py` (the admission) · `scripts/verify_run.py` (two-phase scheduler, in-process admission) · `scripts/verify_all.sh` (bootstrap, tmp areas) · `scripts/verify_duration.py` (history) · `scripts/stage2.py` (full and targeted checks) · `decisions/gates.yaml`, `docs/governance/gate-catalog.md`, `docs/WORKFLOW.md` (doctrine) · `tests/test_verify_lock.py`, `tests/test_verify_before_admission.py`, `tests/test_verify_duration.py` · `docs/research/2026-11-09-make-verify-long-term.md` (the framing note) · the handovers of 2026-11-11 through 2026-11-19 (lane history and the maintainer's answers) · the unmerged branch `feat/verify-slots` (old lane's spec, decisions and attempts).

## What is unclear

- The content of unmerged `feat/verify-slots` (`bca8a129`, `bb1c93ca`, `8a94178f`, `0b7a776b`, `cb16d3d9`, `b5c2105b`) is not readable from this worktree: whether the re-slice salvages its commits or restarts from main is undecided in any artifact I could read here.
- The Q-4 "1.6×" measurement's exact conditions and the S2-1 answer live only in handover prose in this tree; their canonical records are on the old branch.
- The owed 2×6 and 4×3 (slots × workers) trials were never run; no artifact here fixes per-slot worker sizing for two slots.
- "Why the cheap pytest ran no tests" in the three failed F6-1 repairs was never diagnosed (handover 2026-11-18); attempt 3's tree sits in the verify-slots worktree's `stash@{0}`.
- The tracker state of `coding-harness-u1ha` and `coding-harness-42em` (class, description, notes) lives in the Dolt database under `.beads/` and was not read in this phase.
- With two slots, the shape of the published holder state (one record file vs per-slot records) and what wait logs name with two holders is decided nowhere in this tree.

## Which files a change would have to touch

`scripts/verify_lock.py` — slot count, queue turn-taking (`_queue_wait`), holder record(s) (`HOLDER_NAME`, `_publish`, `read_holder`, `nested_holder_pid`, `_describe_holder`), per-admission memory gate, `hold_admission`/`supervise`, plus the boundary refusal if carried over · `scripts/verify_run.py` — the `hold_admission` call site and wait/context plumbing (descriptor passing through `lock_slot` is slot-count-neutral on its face) · `scripts/verify_duration.py` — only if a slot identity field is added to the history · `scripts/ci_gates.py:255-258` and `scripts/kit/manifest.yaml` — manifest description currency · `decisions/gates.yaml` header (lines 50–59), `docs/governance/gate-catalog.md` (lines 36–40), `docs/WORKFLOW.md` (lines 555–577 and 583–613) · `tests/test_verify_lock.py` and `tests/test_verify_before_admission.py` (the single-slot pins named above), plus `tests/test_verify_duration.py` where wait rows are pinned.
