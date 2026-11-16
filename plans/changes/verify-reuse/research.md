---
title: "Research — verify-reuse"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-rzkh
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-16", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# verify reuse — Research

Stage-2 call, 2026-11-16: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1100 files, 4453 commits, 12 rules.

## Runner exploration — 2026-11-16

Research complete. Here is the phase-1 exploration for `verify-reuse`, as prose ready to append to `plans/changes/verify-reuse/research.md`.

---

## What the change is about (traceable in the repository)

The change folder `plans/changes/verify-reuse/` (frontmatter bead `coding-harness-rzkh`, indexed as draft/none in `plans/INDEX.md`) holds only the skeleton `research.md`; no spec, decisions, plan or findings exist in this worktree — not found, not archived. The topic is traceable through three sources:

- `docs/research/2026-11-09-make-verify-long-term.md` (bead coding-harness-bxxt, owner framework-architect) proposes "Reuse of a green full result by content key (extends bead coding-harness-43iz from 'non-test gates per commit' to 'the whole verdict per tree content')" and states the rule "A full result is reused … a green full check is recorded under a key made from the tree content, the gate file and the lock file. Phase 6, the orchestrator and a rerun ask for the key first. Today the review verb runs its own full check on a tree the orchestrator has just checked."
- `docs/journal/handover/2026-11-14-night-ten-lanes-parked.md` records maintainer decisions of 2026-11-13/14 under "Seconds gates before admission", among them "reuse the result for an unchanged tree", and lists lane 9 as `verify-result-reuse` (coding-harness-bxxt.2, head `23eaf0d4`), parked because its research swarm stayed incomplete twice (its question 6 recommends resuming with another online model).
- `docs/journal/handover/2026-11-12-night-ten-lanes.md` proposes folding the commit-keyed gate cache (coding-harness-43iz) into the content-keyed reuse of a green run (coding-harness-bxxt.2).

**Not readable here, stated as not read:** the relation between bead `coding-harness-rzkh` (this folder's frontmatter) and `coding-harness-bxxt.2` (the parked lane) — the tracker is the Dolt database under `.beads/` with no rendered copy committed, and I run no commands. Whether the parked lane's prior research (head `23eaf0d4`) exists on another branch: not found in this worktree; the folder here is new and untracked (git status at session start).

## What exists today — the verification pipeline

**One gate list.** `decisions/gates.yaml` (header "THE ONE LIST (D-10/O-4, bead coding-harness-bo0)", `schema_version: 3`) declares 24 gates: 22 in job `verify`, 2 in `drift` (`plans-registry-strict`, `research-currency`). Per-gate fields: `id, title, command/action, job, enforcement (advisory/report/block), floor, placement (hosted/writer/both), needs_tracker, needs_history, subsets, cost, reason`. Exactly two verify gates are cost class `minutes` (`pytest`, `leerprobe`); every other verify gate is `seconds`. The `cost` field is required since bead coding-harness-bxxt.1 (`validate_schema`, `COST_CLASSES` in `scripts/ci_gates.py`).

**The reader.** `scripts/ci_gates.py` returns gates in declaration order (`gates()`); only the local run reorders — `kostenordnung()` is a stable sort putting `seconds` before `minutes` (`scripts/ci_gates.py`, applied in `main` under `--placement lokal`), declaration order kept within a class. Its `report(job)` already binds a run to a state of the world: candidate (`git rev-parse HEAD`), base (`git merge-base origin/main HEAD`), and `config_sha256` (SHA-256 over `decisions/gates.yaml`). No tree-content hash is computed anywhere in this file — "not there" today.

**The runner.** `scripts/verify_all.sh` fetches the gate TSV once (`--commands --job --placement --tsv`), runs each gate via `sh -c`, sets `fehler` only on `block`, and under schema 3 stops at the first blocking failure, naming every selected gate it did not run (bead coding-harness-bxxt.1, the cheap-first block and "not run" summary). `--ci` stays exhaustive. A local run therefore measures 21 verify gates (hosted-only `lychee` skipped, declared): 19 seconds gates, then `pytest` and `leerprobe`. The runner holds no command list of its own — pinned by `test_runner_holds_no_command_list_of_its_own` (`tests/test_ci.py`, allowed script callees exactly `{ci_gates.py, verify_duration.py}`).

**The admission.** `scripts/verify_lock.py` queues all protected verification of one user on one machine under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/` (`state_root()`), with a memory floor (25 % default) and token-marked nesting (`HARNESS_VERIFY_LOCK_HELD`/`HARNESS_VERIFY_LOCK_TOKEN`). The only "reuse" in the verify path today is admission-context reuse: an inherited wait is resolved from the validated ownership record and marked `reused=True` (`admission_context()`, bead coding-harness-1um6) — reuse of a *wait measurement*, never of a verdict.

**The run log.** `scripts/verify_duration.py` appends version-1 JSONL events to `verify-duration.jsonl` under the same state root: `run_start` records repository, commit, `dirty` (from `git status --porcelain`, null when git cannot answer), `config_sha256`, job, placement, memory, workers and the admission context (`cmd_start`); one `gate` event per *executed* gate; `run_end` with the verdict. It records no content hash of the tree — the long-term note names this as its own limit ("the log records 'dirty', not a content hash … The saving from verdict reuse is therefore not quantified"). Skipped gates get no timing events ("the history describes executed commands only", `verify_all.sh` comment above the not-run summary).

**Verdict text is an interface.** Gate frames `── [gid] $ cmd` / `── [gid] <verdict>` (`GATE_START`/`GATE_END` in `scripts/stage2.py`) are parsed by `red_sections()` and `verify_evidence()` as repair diagnostics; the not-run summary deliberately uses a different prefix so the parser never mistakes a skipped gate for a gate section.

**The phase-6 boundary.** `require_fresh_full_verification()` (`scripts/stage2.py`) runs a fresh full `make verify` of the committed head on *every* phase-6 invocation, a re-check included, "and leaves no receipt: it measures the head being reviewed"; it refuses a dirty tree (runner audit lines in `findings.md` excepted) and a head or tree that changed during the check; a targeted check never stands for it (bead coding-harness-gxwg). Its identity is pinned (`REAL_FULL_GATE` in `tests/test_stage2.py`). The layering rule lives in `docs/WORKFLOW.md` "Hand repairs by the orchestrator": targeted check before the next round, one full `make verify` under the lock on the final head before phase 6, CI the full gate.

**The targeted layer.** `targeted_selection()`/`run_targeted()` (`scripts/stage2.py`) run touched and linked tests, ruff and the fed gates outside the admission; unsafe coverage falls back to the admitted full check (`full_verify` running `make verify` under `hold_admission`, step limit `VERIFY_SECONDS = 45 * 60`). ADR 0025 governs this; no ADR governs verdict reuse — a search of `docs/adr/` for reuse/cache finds only research-swarm slot reuse and the Pi catalog cache, nothing about verify results ("not found").

**The stop hook does not exist here.** `docs/WORKFLOW.md` documents `.claude/hooks/session-stop/check-tests-green.sh`, but that path does not exist in this worktree (Glob finds nothing; `tests/test_workflow_entry.py` and `docs/research/2026-11-02-firstmate-video.md` treat it as documented-absent, bead coding-harness-788). The archived cheap-first research states the same. So no in-repository stop-hook consumer of a verdict exists today.

**Existing reuse precedents elsewhere in the repository** (mechanisms a verdict reuse could shape itself on; none of them touches verify):
- `scripts/stage2_research_store.py`: exact-binding reuse of research-swarm slot results, stored outside the repository — a slot is reused only on exact match of binding through prompt hash, and every stored result that is *not* reused is named with its reason (`plan_reuse`, `Source`, `ReusePlan`; change 2026-11-06-research-swarm Q-13).
- `scripts/outcome_test.py`: content fingerprints — `_take_snapshot` binds a measurement to commit + question-set SHA-256 + per-source SHA-256, `_check_snapshot` refuses a stale snapshot instead of guessing.
- `scripts/stage2_availability.py`: a bounded, bytes-keyed, process-local declaration parse cache (`_DECLARATION_CACHE`), pinned by `tests/test_stage2_declaration.py::test_unchanged_contents_reuse_a_bounded_parse_cache` (active change `swarm-test-speed`) — explicitly not stat-keyed, because an in-place edit invisible to size and mtime must not read stale.
- Text-only skip: a Markdown change outside `scripts/`, `tests/`, `prompts/`, `decisions/` skips the local `make verify`; CI is its gate (`AGENTS.md`, `docs/testing.md`).

**Measured demand behind the topic** (`docs/research/2026-11-09-make-verify-long-term.md`): 151 full runs in 5.5 days, median 7 runs per worktree, a green run 1,230–1,374 s with pytest about four fifths of it; 129 of 151 runs ran on a dirty tree, so a commit-keyed key would miss six runs of seven — the note concludes the key must come from content; 43 runs repeated a worktree-and-commit pair. The handover of 2026-11-14 measures the Mac mini: 10–13 minutes per full run (pytest ~500 s, kit probe 110–180 s, the 22 seconds gates ~25 s).

## What is unclear (open questions, not guesses)

- The change's intent and class: the folder holds no spec or decisions; whether `verify-reuse` (rzkh) continues the parked `verify-result-reuse` (bxxt.2) lane is not readable in this worktree.
- Whether the maintainer's "reuse the result for an unchanged tree" decision (handover 2026-11-14) is this change's scope, and what "result" covers — the whole verdict or per-gate results. The decision's full text lives in the unmerged lane-6 branch (`verify-cheap-before-admission`, coding-harness-bxxt.6, head `ec7629eb`), not in this worktree.
- The content key: which inputs a green verdict may be bound to. The note proposes tree content + gate file + lock file; the run log today holds only commit, dirty and the gate-file digest; what exactly belongs in the key is unanswered in the repository.
- Storage and trust model: no verdict store exists ("not there"); whether one lives in the shared state root beside `verify-duration.jsonl`, with the same symlink/no-follow refusal discipline every file there applies, is unanswered.
- Which callers may consume a reused verdict: phase 6's boundary deliberately "leaves no receipt" today, and that wording sits in doctrine (`docs/WORKFLOW.md`) behind a guard test — whether the maintainer wants that rule changed is a human decision, not derivable from the tree.
- Whether a reused verdict may ever stand on a dirty tree (the historical log says most runs were dirty) — unanswered.
- How a reused run appears to consumers: no gate frames would exist for a run that executed nothing; whether `red_sections`/`verify_evidence`, the duration history and the not-run wording need a declared skip format is unanswered.
- Whether `--ci`, the drift job or hosted CI results participate in a reuse key — nothing found in the tree; unanswered, and the note addresses the local verify job only.

## Which files a change would have to touch

`scripts/verify_all.sh` (ask-before-run in the gate loop, verdict and frame wording); `scripts/verify_duration.py` and/or a store beside it under `verify_lock.state_root()` (run/gate events; a new event kind or a sibling store); `scripts/ci_gates.py` (`report()` is the existing binding block; a tree-content hash does not exist there today); `scripts/stage2.py` (`require_fresh_full_verification`, `full_verify`, fallback wording); possibly `scripts/verify_lock.py` if a store adopts its refusal discipline. Tests: `tests/test_ci.py` (runner pins, the two-callee allowlist), `tests/test_verify_cheap_first.py` (whose `MECHANISM_FILES` — `ci_gates.py`, `verify_all.sh`, `verify_lock.py`, `verify_duration.py`, all classified `mechanismus` in `scripts/kit/manifest.yaml` — make these files part of the kit transfer proof), `tests/test_stage2.py` (phase-6 boundary guard, evidence parsers), `tests/test_verify_duration.py`, `tests/test_verify_lock.py`. Docs: `docs/WORKFLOW.md` (phase 5/6 wording), `docs/testing.md` ("Where tests run"), `docs/governance/gate-catalog.md` only if `decisions/gates.yaml` itself changes (the file is already bound whole via `config_sha256`).

## Neighbours for the header

`docs/research/2026-11-09-make-verify-long-term.md` · `plans/changes/archive/2026-11-16-verify-cheap-first/` (bxxt.1, done — same runner, schema 3, early stop) · `plans/changes/archive/2026-11-16-verify-tmp-cleanup/` (bxxt.3, done — run areas in the same runner) · `plans/changes/archive/2026-11-16-targeted-check-more-verbs/` (ADR 0025 targeted checks) · `plans/changes/archive/2026-11-06-research-swarm/` (the exact-binding reuse store, Q-13) · `plans/changes/swarm-test-speed/` (active — the bounded bytes-keyed cache precedent) · `docs/adr/0021-review-swarms-until-clean.md` and `docs/adr/0025-targeted-check-after-repair.md` · the handovers `2026-11-12-night-ten-lanes.md` and `2026-11-14-night-ten-lanes-parked.md`.
