---
title: "Research — research-store-home"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-nxdy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
neighbours: []
---

# research store home — Research

Stage-2 call, 2026-11-04: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 888 files, 3288 commits, 12 rules.

## Runner exploration — 2026-11-04

The three home-computing sites in `scripts/` are `stage2.py record_base()`, `stage2_research_store.py research_dir()`, and `verify_lock.py state_base()`; nothing else computes a state home.

---

### What exists today

**The research state store** is the resumable store of the phase-1 research swarm (Q-13): `scripts/stage2_research_store.py`, module docstring. It is runner-owned, lives outside the repository, and holds, per run (a random 128-bit run id directory), `run.json` plus per-slot `<slot>.launch.json` / `<slot>.result.json`. Every record is credential-scrubbed, written to a temporary name, flushed, renamed and its directory flushed; readers ignore temporary names and refuse records that do not parse or fail their own SHA-256 seal (`stage2_research_store.py` docstring and `_seal`/`_read_sealed`). The store knows nothing about models; a slot is reused only on exact match of binding, stage, topic, seat, endpoint, model and prompt hash with an `ok` outcome that revalidates (docstring; spec criteria 53–55 of `plans/changes/research-swarm/spec.md`).

**The store's home rule today.** `research_dir(change, root)` (`scripts/stage2_research_store.py:59-68`) computes, read at call time: `$XDG_STATE_HOME`, else `Path.home()/.local/state`, then `coding-harness/stage2/<change>@<sha256(resolved root)[:8]>/research`. The `@<digest>` key is the runner's own record key (`record_key`, `scripts/stage2.py:3229-3235`), so two worktrees of one change keep two stores (R-2 of the review-swarm review, named in the `research_dir` docstring). The module docstring calls the location "beside the review loop record: `record_dir(change)/research/`". The same XDG default is computed independently in exactly three places: `record_base()` (`scripts/stage2.py:3223-3226`), `research_dir()` (`scripts/stage2_research_store.py:65-66`, deliberately "without importing the runner"), and `state_base()` (`scripts/verify_lock.py:174-177`) for the machine-wide verify admission. A grep over `scripts/` for home-computing spellings found no fourth site.

**What shares the record directory with the store.** `record_dir(change, root)` (`record_base()`/`record_key`) holds `loop.md` (the review-loop record, `scripts/stage2.py:3272`), `availability.json` (the review-loop receipt, `scripts/stage2_availability.py:1345-1346`), `research-availability.json` (the research receipt, `scripts/stage2_availability.py:744-745`), the probe audit (`_ProbeAudit`, `scripts/stage2_availability.py:806`), and the store directory `research/`. The loop's lock is a sibling file `<change>@<digest>.lock` (`lock_path`, `scripts/stage2.py:3243-3245`); the store's lock is `.lock` *inside* the store directory (`LOCK_NAME`, `acquire_lock`, `scripts/stage2_research_store.py:36, 186-198`).

**The placement guard and its history.** `Store.assert_outside` (`scripts/stage2_research_store.py:152-170`) refuses a store inside, equal to, or containing any forbidden directory, resolving realpaths first (F-19), and — the Q-15 way out — refuses a store beneath the real home directory that Claude research processes inherit, naming `XDG_STATE_HOME` in the message. It is wired in `Run.open` (`scripts/stage2_research_run.py:366-373`): `Store(research_dir(change, root))`, then `assert_outside(*git_boundaries(root), home=HOME)`, then `acquire_lock()`; a `StoreLocked` becomes the runner's `Refused` (exit 2), a `StoreWriteError` becomes `CallFailed` ("the research state store is unusable", exit 1). `git_boundaries` (`scripts/stage2_research_run.py:233-246`) forbids the worktree, its absolute git dir, the common git dir and the main checkout holding it — the RS-2-3 fix. This is a settled maintainer decision, not an accident: Q-15 "Where the research state store may live relative to a model's home directory" (`plans/changes/research-swarm/decisions.md:619-637`, answered 2026-10-19, "Ja zu Option 1") chose refusing a store inside the real home over a scratch home for Claude seats and over a new default path, "accepting that `XDG_STATE_HOME` must be set outside the home before a research run". Consequence recorded in that decision: without the variable, the default `~/.local/state` lies beneath HOME and a run stops before any model call.

**The store contract in the neighbour spec.** Criteria 51–58 of `plans/changes/research-swarm/spec.md` (lines 471-494) pin: durable record before the next launch (51); no store path, run-directory name or stored result reaches a model before its stage barrier, store not inside worktree, git dir, model's working, home or agent directory, owner-only (52); exact-binding reuse with every non-reused stored result named (53); a reuse is a new run with its own id, receipt and deadlines (54); reuse marking with source run id and original times (55); a security-refused run is never a resume source (56); a failed store write ends the run incomplete, exit 1, `state-store-unwritable` (57); a held lock refuses with exit 2 before any model call (58). Criterion 53's "results of a run published complete are reused" no: a complete run *clears* the store (spec prose near line 923: "A run published complete clears the change's store, so a deliberate rerun starts fresh").

**Release interplay (RS-2-1, repaired).** `remove_loop_record` (`scripts/stage2.py:3832-3846`) deletes the record directory but skips the entries `research` and `research-*`, and removes the directory itself only when nothing research-related is left; the docstring names the deep-review RS-2-1 origin. The repair is pinned by `tests/test_stage2_research_deep_review.py::test_releasing_the_loop_keeps_the_research_store_and_its_lock` (lines 378-409): the store directory and its held lock survive a release, a second store sees `StoreLocked`, and a record with no research files goes entirely. The finding's origin is `docs/journal/handover/2026-10-25-cloud-runner-fixes.md` (RS-2-1 at line 330; RS-2-3/2-4/2-5 at lines 713-733, all store-related review findings).

**Placement hard rules in code.** `_ensure` (`scripts/stage2_research_store.py:172-182`) refuses a symlink in the store's place, a foreign owner, or modes looser than 0700; files are 0600, the lock opens with `O_NOFOLLOW` at 0600 (`acquire_lock`, lines 186-198). Pinned by `tests/test_stage2_research_store.py::test_store_is_owner_only_outside_every_model_directory` (lines 308-333) and `::test_store_refuses_a_symlinked_directory` (lines 336-344).

**How tests and the offline capture place the store.** The suite always sets `XDG_STATE_HOME` to a temporary directory (fixture `state_home`, `tests/test_stage2_research_store.py:46-50`) — the suite exercises the env-set route, never the un-set default route, which Q-15 makes a refusal. The offline capture proves both routes: `research_capture.py` `state_store_guard` (lines 967-985) runs the guard on a store outside the fake HOME (accepted) and one inside it (`~/.local/state`, refused), and the evaluation requires "outside-home accepted, inside-home refused" (lines 1237-1246); the scratch world is built with a fake HOME and a fake `XDG_STATE_HOME` outside it (lines 11, 574-578, 620). The CI gate registers the store tests as "durable atomic records, SIGKILL survival, owner-only placement" (`scripts/ci_gates.py:194-196`).

**What the doctrine says.** `docs/WORKFLOW.md:1011` describes the store only as "a store outside the repository (`stage2_research_store.py`)"; the exact phrase "state store" and the symbols `research_dir`/`record_dir` do not occur anywhere in `docs/WORKFLOW.md` (grep). The shared state root is documented for the verify queue at `docs/WORKFLOW.md:463` and the loop record path at `docs/WORKFLOW.md:1451`, both as `${XDG_STATE_HOME:-~/.local/state}/coding-harness/…`.

**One observed text/code drift.** The design paragraph of the store (`plans/changes/research-swarm/design.md:447-453`) sketches the home as `…/coding-harness/stage2/<change>/` without the `@<digest>` suffix that both `record_key` (`scripts/stage2.py:3229-3235`) and `research_dir` (`scripts/stage2_research_store.py:67`) append; the suffix came later with R-2. `plans/changes/run-report/research.md:58` describes the layout with the runner-level `record_dir(change)/research/<run-id>/` spelling, consistent with the code.

### Where it lives

Mechanism: `scripts/stage2_research_store.py` (`research_dir`, `Store.assert_outside`, `Store._ensure`, `acquire_lock`, `LOCK_NAME`); home computation shared with `scripts/stage2.py` (`record_base`, `record_key`, `record_dir`, `lock_path`, `remove_loop_record`) and `scripts/verify_lock.py` (`state_base`, docstring "Shared state"). Wiring and boundaries: `scripts/stage2_research_run.py` (`Run.open` store setup, `git_boundaries`). Beside-dwellers: `scripts/stage2_availability.py` (`research_receipt_path`, `receipt_path`, `_ProbeAudit`). Capture evidence: `scripts/research_capture.py` (scratch world, `state_store_guard`). Tests: `tests/test_stage2_research_store.py`, `tests/test_stage2_research_deep_review.py` (release and bounds tests), `tests/test_stage2_swarm.py` (world setups calling `research_dir`, e.g. lines 387, 1308, 1334). Normative neighbours: `plans/changes/research-swarm/spec.md` (criteria 51-58), `plans/changes/research-swarm/design.md` (store paragraph), `plans/changes/research-swarm/decisions.md` (Q-13, Q-15). Doctrine: `docs/WORKFLOW.md` lines ~1010-1015 (Q-13 resume), 463, 1451.

### What is unclear about it

- **The bead's own scope is not read.** The description of bead `coding-harness-nxdy` lives in the Dolt tracker under `.beads/`, which this phase's read-only tools cannot query; the repository shows only the change folder opening commit ("chore(research-store-home): open the change folder (bead coding-harness-nxdy)"). Which aspect of the home the change targets — the store's cohabitation with the loop record directory, the Q-15 home-refusal of the unset default, a configuration knob, or the doctrine's silence about the path — is stated nowhere I read and is a human question for the interview.
- **`not there`: no dedicated knob.** No environment variable besides `XDG_STATE_HOME` influences the store home; greps for `store_home`/`RESEARCH_STORE` spellings across the tree return nothing outside this change folder and the generated INDEX.
- **`not there`: the living spec and two candidate neighbours hold no store content.** `plans/specs/implementation-verification/spec.md` has no state-root or store reference (grep, no match); `plans/changes/restore-symlink-parent/` has no store or `XDG_STATE_HOME` reference (grep, no match). Both are ruled out as neighbours on content, not on assumption.
- **`not there`: a `neighbours:` header** — the `research.md` skeleton carries none yet; per phase doctrine the runner owns that header, and the neighbour list below is my finder contribution to it.
- **Unresolved text drift**: whether `plans/changes/research-swarm/design.md:450`'s `<change>/` sketch (no `@<digest>`) should follow the code is undecided; the spec (`plans/changes/research-swarm/spec.md`, criteria 51-58) never names a concrete home path at all, so the code's path is not normatively pinned anywhere a validator reads.
- **Deliberately not reopened**: the tension between the default (`~/.local/state`, inside HOME) and the guard (refuses inside HOME) is the answered decision Q-15 of 2026-10-19; the interview decides whether this change touches it, and nothing here judges that.
- **Not read, therefore open**: whether the sibling instance repositories carry their own store-home conventions — nothing outside this worktree was read.

### Which files a change would have to touch

Any change to the store's home touches, at minimum: the home computation and placement guard in `scripts/stage2_research_store.py` (`research_dir`, `assert_outside`, module docstring); the runner wiring in `scripts/stage2_research_run.py` (`Run.open`); and if the record-directory key or release rules move, `scripts/stage2.py` (`record_base`, `record_key`, `record_dir`, `lock_path`, `remove_loop_record`'s `research*` skipping). Dependent consumers of the same directory: `scripts/stage2_availability.py` (`research_receipt_path`, `receipt_path`, `_ProbeAudit` sit in the record dir via `runner.record_dir`). Test surface: the `state_home` fixture and placement/modes/lock tests in `tests/test_stage2_research_store.py`; the RS-2-1 release test and RS-2-3 bounds test in `tests/test_stage2_research_deep_review.py`; the world setups in `tests/test_stage2_swarm.py`. Evidence machinery: the scratch-world state home and Q-15 guard check in `scripts/research_capture.py`. Doctrine: `docs/WORKFLOW.md` (the Q-13 paragraph at ~1010 and the state-root mentions at 463 and 1451, which today never name the store path). `scripts/verify_lock.py` is coupled only if the whole `coding-harness/` state root moves rather than the `stage2/` subtree — its docstring (`scripts/verify_lock.py:11-20`) owns the root for verify admission.

### Neighbours (finder contribution for the header)

Suggested for `neighbours:`: `plans/changes/research-swarm/` (spec criteria 51-58, design store paragraph, decisions Q-13 and Q-15 — the change that created the store and decided its home rule); `plans/changes/verify-machine-lock/` (shares the `coding-harness/` state root; `scripts/verify_lock.py` docstring, its research references the store); `plans/changes/terms-test-fixtures/` (its findings and plan carry the review repairs on `tests/test_stage2_research_store.py`); `plans/changes/run-report/` (its research documents the per-run store layout); `plans/changes/swarm-test-speed/` (its research documents the seal/read mechanism). Checked and excluded: `plans/changes/restore-symlink-parent/` and `plans/specs/implementation-verification/` (no store content — grep, no match), and `plans/changes/loop-until-clean/decisions.md` Q-15, whose identical question number covers a different topic (the probe after a failed member, `plans/changes/loop-until-clean/decisions.md:377-383`) and must not be hand-linked to this change.

---

