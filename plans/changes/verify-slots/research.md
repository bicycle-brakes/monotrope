---
title: "Research — verify-slots"
status: draft
implementation_status: none
date: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3-flash, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# verify slots — Research

Stage-2 call, 2026-11-09: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 980 files, 3783 commits, 12 rules.

## Runner exploration — 2026-11-09

## What exists today

**The bead's intent is not readable from the tree.** The bead `coding-harness-u1ha`
is named only in this file's frontmatter and in `plans/INDEX.md` (row
`changes/verify-slots/research.md`); the bead's title/description lives in the
Dolt tracker under `.beads/`, which read-only file tools cannot query — **not
read**. No tracked file states what the change should do: a case-insensitive
search for `verify[- ]slot` and `verification slot` finds only this change's own
files, `plans/INDEX.md`, and prose that consistently says *one* slot
(`docs/how-it-works.md:293` "all lanes share one verification slot, enforced by
one admission per machine"; `docs/orchestration.md:22` "the one local
verification slot"; `docs/WORKFLOW.md:1798-1799` "under the machine's one verify
lock"). A plural concept of several verify slots exists nowhere in the tree
today. The subject is therefore ambiguous between two unrelated mechanisms that
both use the word "slot", and the interview must settle which one this change is
about.

**Meaning A — the verification slot: the machine-wide admission.** Since the
`verify-machine-lock` change (bead `coding-harness-p6mu`, spec archived at
`plans/changes/archive/2026-11-06-verify-machine-lock/spec.md`, accepted/done),
exactly one protected verification runs at a time per user per machine, across
repositories and worktrees (`scripts/verify_lock.py` module docstring, lines
1–81). Its shape today:

- **State root** `${XDG_STATE_HOME:-~/.local/state}/coding-harness/` holds
  `verify.lock` (exclusive `fcntl.flock`), `verify.holder.json` (published
  ownership: pid, command, start time), `verify.queue/` (one record per waiter
  under a liveness flock; record names match `RECORD_NAME` =
  `(\d{20})-(\d+)\.json`, `scripts/verify_lock.py:128`), and a short-held
  `verify.registry.lock` that serialises registration, pruning and turn-taking;
  registration order is the admission order (FIFO) — `flock` alone supplies no
  FIFO (`verify_lock.py:11-20`, constants at `:123-126`, `_registry_lock` at
  `:405`, `_register` at `:563`).
- **Admission = queue wait + memory check while holding the lock, before
  protected work.** Free memory via macOS `memory_pressure` or Linux
  `MemAvailable/MemTotal` (`read_available_memory`, `verify_lock.py:354`);
  floor 25 % default (`DEFAULT_MEMORY_FLOOR = 25.0`, `:115`), override
  `HARNESS_VERIFY_MEMORY_FLOOR` (`FLOOR_ENV`, `:108`), equality admits
  (`memory_floor`, `:390`); recheck every 30 s (`MEMORY_POLL_SECONDS`, `:116`);
  sustained-low refusal after 60 min (`MEMORY_DEADLINE_SECONDS`, `:118`); an
  unmeasurable reading is logged and the entry proceeds.
- **Nested work** carries `HARNESS_VERIFY_LOCK_HELD` + `HARNESS_VERIFY_LOCK_TOKEN`
  (`LOCK_ENV`/`TOKEN_ENV`, `verify_lock.py:106-107`), validated against the
  published ownership (`_names`, `:321`; `nested_holder_pid`, `:283`); the
  non-secret admission context (`admission_context`, `:461`) adds
  `HARNESS_VERIFY_ADMISSION_ID`/`HARNESS_VERIFY_ADMISSION_WAIT` (`:113-114`, bead
  `coding-harness-1um6`) so nested runs reuse the ancestor's measured wait.
- **Who holds the slot:** gate execution through `scripts/verify_all.sh` — the
  script execs `python -m scripts.verify_lock -- bash scripts/verify_all.sh …`
  unless a valid nested marker exists (`scripts/verify_all.sh:178-190`) — and
  the runner's local checks in `scripts/stage2.py` via
  `verify_lock.hold_admission(...)`: attempt post-run `make verify`
  (`stage2.py:6023`), draft post-run `make verify` (`:6210`), the red-first
  pytest import probe (`:7001`) and the red-first pytest run (`:7023`) — both
  commented as protected work of bead `coding-harness-p6mu` whose waits consume
  none of the probe's time limit — and the draft verb's docs gates
  (`hold_admission(DOCS_VERIFY)`, `:8924`). `launch()` passes the lock
  descriptor to children via `pass_fds` so ownership outlives the supervisor
  exactly as long as the child tree (`stage2.py:965-988`). The change
  `draft-gates-only` (archived `2026-11-06-draft-gates-only/spec.md:31`) records
  that a draft verb "occupies a verification slot with code checks" after a call.
- **Protected areas around it** (machine-lock spec, "Protected areas" and
  "Non-goals"): `decisions/gates.yaml`, generated CI and the `Makefile` (gate
  list, placement, direct `make test` contract stay authoritative); no priority
  scheduling, no public bypass flag, no CI-specific disabling. The admission
  protects the machine's load, not data (spec "Boundary", maintainer
  2026-10-30).
- **Worker sizing inside the slot** (verify-worker-cap, bead
  `coding-harness-l7sc`, merged as #305): `scripts/verify_all.sh:89-162` derives
  `PYTEST_XDIST_AUTO_NUM_WORKERS` when the caller did not set it — min of
  cores/2 and memory in 2-GiB steps, explicit values pass through verbatim,
  failed readings degrade to xdist auto. The recorded trade-off: on the quiet
  machine the default 4 was slower than the old `-n auto` 8 (pytest 751.57 s vs
  613.89 s, 2026-11-01, archived plan "Quiet-machine runs"); whether the bounds
  may loosen is assigned to bead `coding-harness-351h` (tracker; not in this
  tree).

**The slot is the measured bottleneck.** `scripts/verify_duration.py` (invoked
from `scripts/verify_all.sh:192-298`) gives each admitted run an identity and
records per-gate and execution seconds to a JSONL in the shared state root, with
the admission wait reported beside, never inside, execution. The baseline note
(`docs/research/2026-11-04-verify-duration-baseline.md`, bead
`coding-harness-1um6`, five green runs on 2026-11-05): execution 1,215–1,261 s
(median 1,223 s), pytest 81 % and leerprobe 16 % of it, but the **lock wait
varied 2 s–1,254 s — for a lane, queueing rivalled the run itself**. It proposes
a warning at 1,400 s execution and leaves open the actually started pytest
worker count (bead `coding-harness-xay1`). The lane doctrine
(`docs/orchestration.md`, "The resource rule") spends this scarcity by hand:
one verify-bearing step at a time across all lanes, ordered runner-attempt
first, then the lane nearest its pull request; the latest handover states the
lesson plainly — "make verify is the bottleneck — one at a time, 20–35 minutes
under load" (`docs/journal/handover/2026-11-06-heartbeat-night.md`,
"Validation"). `scripts/machine_facts.py` (bead `coding-harness-yql7`) reports
the runner and verification invocations a `ps` snapshot recognises, counting "a
verify wrapper and its child … two invocations, not one logical job"
(`docs/orchestration.md:76-80`). Concept history: the night plans first called
the slot "a file lock" (2026-10-29 plan, `:58`) and corrected to "the machine
admission, not a file lock" (2026-10-30 plan, `:62`).

**Meaning B — swarm "slots": planned model invocations of the research swarm.**
A completely separate use of the word: `scripts/stage2_research_dispatch.py`
dispatches planned slots with provider-wide queues, `PER_PROVIDER_LIMIT = 4`
(`:23` — "the Go models ride the pinned Pi, at most four per provider at a
time", `docs/WORKFLOW.md:1063`), required slots before free ones across
providers (comment F-54, `:211-212`); `research_slot_plan(roles, selected_free)`
plans the `33 + 3N` topic slots (`scripts/stage2_swarm.py:552`;
`docs/WORKFLOW.md:1061`); the resume store keys a slot by
`SLOT_KEY_FIELDS = (stage, topic, seat, endpoint, model, prompt_sha256)`
(`scripts/stage2_research_store.py:41`). Nothing in these files connects to
`make verify` except indirectly: eleven of the twelve slowest tests in the
verify baseline are research-swarm tests (`docs/research/2026-11-04-verify-duration-baseline.md`,
"Slowest single tests"), and the active change `swarm-test-speed` (bead
`coding-harness-dca4`, spec draft/partial per `plans/INDEX.md:532`) addresses
exactly that test weight, mentioning "re-measurement in the verify slot"
(`plans/changes/swarm-test-speed/plan.md:267`).

**Test coverage of meaning A:** `tests/test_verify_lock.py` carries 30 test
functions (machine lock exclusivity, FIFO registration order, queue logging,
nested-ownership validation, signal cleanup, memory readers/floor/override,
unusable state refusals, admission measurement through CLI and inherited
context). `tests/test_ci.py` holds the worker-default regression suite from
verify-worker-cap (criterion ledger in the archived plan, e.g.
`test_runner_derives_worker_default_from_machine_size`). `tests/test_stage2.py`
covers the runner's admission-holding; `tests/test_verify_duration.py` the
measurement; `tests/test_outcome_test.py` uses the path string
`scripts/verify_lock.py` only as a fixture file name for a fake tree
(`:147`) — no behavioural link. Note for any change here:
`scripts/verify_lock.py` and `scripts/verify_all.sh` are in the runner's
`SHARED_INFRASTRUCTURE` tuple (`scripts/stage2.py:4167-4174`), so a repair that
touches them falls back to the admitted full `make verify`.

## Where it lives

- Admission mechanics: `scripts/verify_lock.py` (supervise/main at `:923`/`:962`,
  `_Admission` at `:501` with `enter`/`release`/`_try_acquire_work`/`_queue_wait`/
  `_memory_gate`; `hold_admission` at `:734`; `inherit_env` at `:759`;
  `end_lingering_group` at `:903`).
- Gate runner and worker default: `scripts/verify_all.sh` (nested check
  `:172-190`, duration block `:192-298`).
- Runner call sites: `scripts/stage2.py` (listed above); targeted repair checks
  declared "all outside the machine-wide verify admission"
  (`stage2.py:4157-4162`, bead `coding-harness-gxwg`).
- Measurement: `scripts/verify_duration.py`; baseline note
  `docs/research/2026-11-04-verify-duration-baseline.md`.
- Lane doctrine: `docs/orchestration.md`; user-facing summary
  `docs/how-it-works.md:289-294`; workflow prose `docs/WORKFLOW.md` (swarm row
  `:1058-1127`, hand-repair note `:1796-1799`).
- Specs of record: `plans/specs/implementation-verification/spec.md` (accepted,
  done — derived-file preparation before each verified attempt, bead
  `coding-harness-mfv`); archived `verify-machine-lock` and `verify-worker-cap`
  specs/plans under `plans/changes/archive/2026-11-06-*`.

## What is unclear about it

- **The change's subject** — not stated in the tree; the bead description is
  **not read** (tracker database, read-only tools). Open question for the
  maintainer's interview: is `verify-slots` about the verification slot
  (meaning A — e.g. its count, sizing, accounting or ordering), or about the
  research-swarm slots (meaning B), or something else entirely?
- Whether the *targeted* repair checks (comment at `stage2.py:4157-4159`,
  "outside the machine-wide verify admission") really acquire no admission:
  the comment says so; the red-first checks at `:6999-7054` demonstrably do.
  The targeted-check implementation itself was **not read** in this pass — open
  question, not a guess.
- The sustained-low-memory refusal (60 min), the FIFO queue and the 25 % floor
  are starting policies from 2026-10-28; no re-measurement of the floor against
  the current suite size was found in the tree ("not found": no follow-up note
  matches; the baseline note measures duration, not the floor).
- Beads that neighbour this topic but live only in the tracker (not in this
  tree, so their state here is **not found**): `coding-harness-351h` (looser
  worker bounds), `coding-harness-xay1` (verify-worker-count — no
  `plans/changes/verify-worker-count/` folder exists in this worktree), and
  `coding-harness-te7q` (the runner accepting a bookkeeping-only implement
  attempt as verified — recorded in the 2026-11-06 handover; relevant because
  it gates how any implement attempt of this change would be judged).

## Which files a change would have to touch

If the subject is the verification slot (meaning A): `scripts/verify_lock.py`
(core), `scripts/verify_all.sh` (entry, nested check, worker default),
`scripts/stage2.py` (the `hold_admission` call sites), with
`tests/test_verify_lock.py`, `tests/test_ci.py`, `tests/test_stage2.py`,
`tests/test_verify_duration.py`; prose that states the one-slot rule would need
updating together (`docs/WORKFLOW.md`, `docs/orchestration.md`,
`docs/how-it-works.md`), plus `scripts/verify_duration.py` and
`scripts/machine_facts.py` if wait or invocation accounting changes;
`decisions/gates.yaml`, generated CI and the `Makefile` are protected areas of
the standing spec and should stay untouched unless the maintainer widens scope.
If the subject is the swarm slots (meaning B): `scripts/stage2_swarm.py`,
`scripts/stage2_research_dispatch.py`, `scripts/stage2_research_store.py` with
their test files and `docs/WORKFLOW.md`'s swarm row; `research-swarm-limits.yaml`
if allowances change.

## Neighbours known to this explorer

`plans/specs/implementation-verification/spec.md` (accepted, done);
`plans/changes/archive/2026-11-06-verify-machine-lock/` (accepted, done, bead
`coding-harness-p6mu`); `plans/changes/archive/2026-11-06-verify-worker-cap/`
(accepted, done, bead `coding-harness-l7sc`);
`plans/changes/archive/2026-11-06-draft-gates-only/` (accepted);
`docs/research/2026-11-04-verify-duration-baseline.md` (research note, bead
`coding-harness-1um6`); `plans/changes/swarm-test-speed/` (draft, partial, bead
`coding-harness-dca4`); `plans/changes/outcome-test/` (merged as PR #358);
`docs/orchestration.md` (status: proposed). The tracker-only beads above are
suggested neighbours the runner may add once readable.
