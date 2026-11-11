---
title: "Research — targeted-check-more-verbs"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-11
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-0swp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3-flash, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
  - plans/changes/repair-targeted-check/spec.md
  - plans/changes/adr-repair-check/decisions.md
---

# targeted check more verbs — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). The
intent below was written by the orchestrator (Claude Code) before the first
call; the runner exploration (GLM 5.3 Flash) follows it unchanged.

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-0swp, class bounded. Today every implement attempt and
every draft post-check waits for the machine-wide verify lock: on 2026-11-10
runner jobs waited 44 to 59 minutes for a full check of about 28 minutes, and
a draft waited 92 minutes for a documents job of 30 seconds. A repair already
runs a targeted check through the touch map (bead coding-harness-gxwg); the
full check runs before phase 6 and in CI. Wanted: implement attempts and the
draft post-check use the same targeted selection; the review verb keeps its
fresh full check before its model call; CI keeps the full suite. No new
guarantee is given up: phase 6 and CI still run everything. The maintainer
lifted the note "wait for the testing-strategy report" on 2026-11-10 and
asked for the speed-up of the full check as fast as possible.

Questions for the exploration: how the targeted check of the repair verb
selects gates and tests (`run_targeted`, `targeted_selection`, the touch map)
and where implement and draft call the full check instead; why a change that
touches `scripts/stage2.py` always fell back to the full check (bead note of
2026-11-07: three timeouts at five minutes, nineteen fallbacks) and what a
selection for such a change would need; whether the documents job of the
draft needs the machine-wide lock at all; which tests pin today's behaviour.

Stage-2 call, 2026-11-10: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1007 files, 3889 commits, 12 rules.

## Runner exploration — 2026-11-10

The exploration is complete — I have read every mechanism the four questions name. Here is the research, ready to append to `plans/changes/targeted-check-more-verbs/research.md`.

---

## What exists today

**The four verbs run three different post-run checks.** `implement` calls `run_attempts` without a `verify_mode` (`scripts/stage2.py`, `implement`, the call at the end of the function), so the shared loop's default `verify_mode="full"` applies (`scripts/stage2.py`, `run_attempts` signature, commented "repair: \\"targeted\\"; implement keeps the full check") and `verify_attempt` runs in full mode (`scripts/stage2.py`, `verify_attempt`, `mode == "full"` branch): one `verify_lock.hold_admission(["make", "verify"])` wraps `format_step`, `cheap_checks`, the criterion-ledger clearing, `prepare_derived` and the `make verify` launch with `VERIFY_SECONDS = 30 * 60` (`scripts/stage2.py`, constants block; `TOOL_SECONDS = 5 * 60`, `GIT_SECONDS = 2 * 60` beside it). The comment there states preparation runs under the same admission deliberately, so the format step's ruff and the `make` share one verify environment. `draft` has its own loop and calls `verify_draft` (`scripts/stage2.py`, `draft` attempt loop; `verify_draft`): ADR count, tool check, `prepare_derived`, then `verify_lock.hold_admission(DOCS_VERIFY)` around `bash scripts/verify_all.sh --job docs` (`DOCS_VERIFY` constant directly above `verify_draft`, commented "Implement keeps full `make verify`; repair takes the targeted check"), with the artefact checks (plan card, `## Time used` heading) after it. `repair` alone passes `verify_mode="targeted"` (`scripts/stage2.py`, `repair`, the `run_attempts` call), routing through the `mode == "targeted"` branch into `_targeted_body` (`scripts/stage2.py`): the same preparation runs outside the admission with the lock environment variables stripped, then `targeted_selection` decides. `review` requires a fresh full check before any reviewer is called: `full_verify` runs on a committed, clean tree, and the head and tree are re-read afterwards (`scripts/stage2.py`, the phase-6 prelude function above `review`, and `review`'s docstring).

**How the targeted selection decides** (`scripts/stage2.py`, `targeted_selection`; the `Targeted` dataclass above it). The delta is `changed_paths(root, env, against)` — working tree plus index plus untracked files, `--no-renames` so a rename lists both names (`scripts/stage2.py`, `changed_paths`). It falls back to the full check (`Targeted([], [], [], reason)`) when: a Git path cannot be decoded safely; the listing is refused; a path under `prompts/` changed; a member of `SHARED_INFRASTRUCTURE` changed; a `conftest.py` changed; a touched path is a symlink or not an ordinary single-linked file; a non-`.py` file changed outside the `plans/`+`docs/` markdown that is skipped rather than fatal; a touched non-test `.py` file has no linked test; the link inventory cannot be read; `tests/test_stage2.py` is among the selected tests — the maintainer's option A of 2026-11-04, "until bead coding-harness-vg9 splits this file, its whole-file run needs the admitted full check's budget"; or a gate's command cannot be parsed. `SHARED_INFRASTRUCTURE` is `(scripts/ci_gates.py, scripts/verify_all.sh, scripts/stage2.py, scripts/verify_lock.py, scripts/touch_map.py, scripts/leakcheck.py)` (`scripts/stage2.py`, the constant above `TARGETED_LABEL`, commented "Inputs whose change makes the full check necessary") — **`scripts/stage2.py` is on that list itself, so any repair touching it falls back by construction**. The selected tests are the whole touched test files plus every test file the touch map links to a touched path, taken from the working tree and, for removed paths, the baseline snapshot (`_is_test_module` recognises `tests/**/test_*.py`). Ruff runs on touched Python files `format_targets` does not already cover. The gates are every local verify-job gate whose parsed command entrypoints intersect the touched paths, plus **the whole `docs` subset always** (in-source comment: "The document subset always stands: a repair rewrites derived plan, findings and index text"), plus `leerprobe` when a path appeared or vanished. `_parse_gate_command` maps `-m module` to module entrypoints and keeps exact `.py` file arguments; directories never match.

**How the targeted check executes** (`scripts/stage2.py`, `run_targeted`): ruff over the touched files, pytest over the whole selected test files (worker count derived from cores and memory by `targeted_pytest_env`), then the selected gates in gate-list order through the locked interpreter (`GateCommand.locked_command`), everything outside the machine admission, first blocking red ends the run, each command bounded by `TOOL_SECONDS` (five minutes).

**The machine-wide admission** (`scripts/verify_lock.py`, module docstring and `hold_admission`): one `fcntl.flock` file `verify.lock` under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/`, shared across repositories and worktrees, a registration-order FIFO queue with liveness-flocked waiter records, a free-memory gate (25 percent floor, rechecked every 30 s), nesting via `HARNESS_VERIFY_LOCK_HELD` plus a secret token. Its stated reason: concurrent full checks exhausted the machine — load above 100, checks past 30 minutes against 11–12 alone (bead coding-harness-p6mu). Crucially, **`verify_all.sh` itself execs the supervisor when no valid inherited marker is present** (`scripts/verify_all.sh`, the admission block before the gate loop), so `make verify` (`Makefile`, `verify:` target → `bash scripts/verify_all.sh`) and the docs job queue through the same admission even without stage2's own `hold_admission`; stage2's outer hold makes the script re-enter as a nested run.

**The documents job of the draft** is the gates with `subsets: [docs]` in `decisions/gates.yaml`: `plans-registry`, `docs-links`, `frontmatter-current`, `dangling-beads`, `decision-continuity`, `adr-answers`, `interview-minimums`, `question-context`, `criterion-ledger`, `research-handoff` (each with command, enforcement and, for `plans-registry` and `dangling-beads`, `needs_tracker: true`), plus `markdownlint` as a hosted action which the local runner leaves out because it has no command line. The targeted selection already includes exactly this subset always.

**Why a `scripts/stage2.py` change always fell back** — three stacked reasons: (1) `SHARED_INFRASTRUCTURE` membership refuses the selection outright; (2) even without it, the linked test of `scripts/stage2.py` is `tests/test_stage2.py` (the touch map links a test that names or imports a file — `scripts/touch_map.py` docstring, link kinds `tests` and `imports`), which triggers the option-A fallback; (3) the five-minute `TOOL_SECONDS` bound is the budget the option-A comment says that file exceeds. The practice record confirms it: `plans/changes/repair-targeted-check/findings.md` quotes a runner line "full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure".

**The neighbour report** (`docs/research/2026-11-09-make-verify-long-term.md`, bead coding-harness-bxxt) measures the demand this change addresses: 151 full runs in five and a half days, 77.3 hours of wait against 57.1 hours of execution, median wait 22–30 minutes, a green run ≈ 1,374 s with pytest about four fifths of it, the suite grown from 13,168 to 73,080 lines in a month, and 11 red runs that had a green pytest gate and failed on a cheap gate after it. It names bead coding-harness-0swp — this change — as "the largest lever" (step 2 of its proposed order) and sketches a four-layer target picture in which layers 1–2 (formalities, targeted under 2 minutes) run "local, no lock" and the full check runs once per change. Its scope note says everything in it is a proposal; nothing is implemented by that note.

## Where it lives

Selection `targeted_selection`, execution `run_targeted`, repair body `_targeted_body`, full check `full_verify`, mode routing `verify_attempt`/`run_attempts` — all `scripts/stage2.py`. Admission `scripts/verify_lock.py`. Job runner `scripts/verify_all.sh`; the one gate list `decisions/gates.yaml`; `make verify` delegates there (`Makefile`). Link inventory `scripts/touch_map.py` (`links`, `WorktreeSnapshot`, `Snapshot`, `inventory_path`, `CannotMeasure`), with its in-source caveat that links are names found in text and can be missing or false. The repair doctrine's prose lives in `docs/WORKFLOW.md` (the phase table `| 4b |` row; the draft section stating "`implement` keeps the full `make verify`; `repair` takes the targeted check … Only the draft drops to the document subset"; the review-loop paragraph naming the fallback list; "### Repairing taken findings"; the hand-repair bullet, bead coding-harness-24ag), mirrored in `AGENTS.md`'s `| 4b |` row, and in `prompts/04-implement.md` ("Gate: `make verify` green" and the runner-check paragraph with the same fallback list) and `prompts/04b-review-loop.md`. The decision text is ADR 0025 (`docs/adr/0025-targeted-check-after-repair.md`, accepted): point 1 scopes the targeted check to "after a runner repair", point 2 the full fallback, point 3 the fresh full check before phase 6, point 4 a measurement duty over five changes or two weeks, point 5 reserves amending or replacing the rule to the testing-strategy spike (bead coding-harness-1ga5). The prior change that built all of this is `plans/changes/repair-targeted-check/` (spec, research, findings) with its decision record `plans/changes/adr-repair-check/`.

## What is unclear about it

- The bead note of 2026-11-07 ("three timeouts at five minutes, nineteen fallbacks") was **not read** in this phase — the tracker needs `tools/bd`, which this read-only phase does not run. The figures exist in the tree only inside the bead-intent quote in this file. Nothing I read states which verb produced those timeouts and fallbacks, and the run log (`~/.local/state/coding-harness/verify-duration.jsonl`) lies outside the repository and was not read. The intent's "44 to 59 minutes" waits and the "92 minutes for a documents job of 30 seconds" are likewise intent-quoted, not tree-verified.
- Which delta shapes an `implement` attempt actually produces (file kinds per attempt: new production code, new tests, plan markdown) is recorded nowhere I read; whether its common case even reaches a safe selection (new production code needs a touch-map-linked test to avoid the no-linked-test fallback) is therefore an open question.
- The docs job's measured duration exists only as the intent's "30 seconds"; `verify-duration.jsonl` holds the real figure but was not read.
- Whether ADR 0025's amendment path (point 5 names the testing-strategy spike) or a new decision text should carry an extension of the targeted check to `implement` and `draft` is the maintainer's question — ADR 0025 point 1 today names only the repair.
- The result of ADR 0025 point 4's measurement duty (missed faults a targeted check let through) was not found in the tree — stated as not found, which is not the statement that it does not exist; it may live in the tracker or a handover.
- `tests/test_stage2.py`, `test_targeted_mode_is_repair_only` pins `source.count('verify_mode="targeted"') == 1` and both defaults as `"full"`; how that pin should be reshaped for two targeted verbs is an implementation question for the plan, not decided by any text I read.

## Which files a change would have to touch

`scripts/stage2.py` — the mode routing (`run_attempts` default and `implement`'s call; `verify_attempt`'s mode branch; `verify_draft`'s admitted docs job) and, if implement or draft need other refusal rules, `targeted_selection`. `tests/test_stage2.py` — the pins named above: `test_targeted_mode_is_repair_only`, `test_implement_and_fallback_repair_keep_full_verify_after_docs_draft`, `test_repair_verification_doctrine_requires_targeted_and_final_full_checks` with `repair_verification_doctrine_problems`, `test_repair_prompt_consistently_describes_targeted_verification`, `test_draft_verification_documentation_describes_targeted_repairs`, and the targeted-behaviour suite (`test_covered_repair_uses_targeted_verification` through `test_targeted_inventory_uses_bounded_sanitized_git`, including `test_targeted_stage2_test_file_requires_full_verification`). `docs/WORKFLOW.md` — the `| 4b |` row, the draft section, the review-loop repair paragraph, "### Repairing taken findings", the hand-repair bullet, and "One admission per user and machine" if the draft's relation to the lock changes. `AGENTS.md` — its `| 4b |` row (the doctrine test reads both files together). `prompts/04-implement.md` and `prompts/04b-review-loop.md` — both are quoted verbatim into model prompts (the repair-prompt test pins `04-implement.md` inside the assembled prompt). Possibly `docs/adr/` — whether an amendment ADR is needed is a decision, not a fact. `scripts/verify_lock.py` needs no change for a targeted mode that stays outside the admission; `test_targeted_commands_run_without_verify_admission` already proves that path. One fact for the plan to carry: this change itself touches `scripts/stage2.py` and `tests/test_stage2.py`, so under today's rules its own implement attempts will fall back to the full check — `SHARED_INFRASTRUCTURE` names the file, and option A names the test file.

---

Facts only; I designed nothing and judged nothing. The runner owns `research.md` and the `neighbours:` header — the neighbour list there currently names `docs/research/2026-11-09-make-verify-long-term.md`; `plans/changes/repair-targeted-check/spec.md` and `plans/changes/adr-repair-check/decisions.md` are the two neighbouring specs this exploration found beyond it, for the runner to add if it agrees.

## Repository follow-up — 2026-11-11

Read at baseline `e635f03b` while drafting; these resolve repository gaps,
not maintainer decisions:

- `scripts/touch_map.py`, `imported()` and `links()`, produces direct
  `tests` and `imports` edges only; Python imports resolve by unique stem.
  No transitive traversal is present. Current and committed snapshot
  adapters already exist, and code kinds include Python and shell. The
  existing static-link caveat remains applicable to indirect selection.
- `scripts/verify_duration.py` owns the local `verify-duration.jsonl`
  store, safe flocked append, version-1 start/gate/end records and the report
  reader. Start records include repository, commit and gate-file digest;
  gate records include ID, exit and enforcement. Neither targeted-result
  nor slip records exist, and failed-test IDs are not stored. Storage
  failures are diagnostic and do not change gate verdicts.
- `scripts/stage2.py`, `require_fresh_full_verification()`, checks head and
  dirty paths before/after `full_verify()`, with a narrow audit-only
  exception for this change's findings; it does not correlate targeted
  checkpoints with the duration history.
- `tools/claude-code/skills/handover/SKILL.md` is the repository-owned
  handover instruction. `templates/plan.md` and
  `scripts/validate_change_artefacts.py` are absent from this baseline.
- ADR 0025 is an existing accepted file under the human-decided ADR prefix
  in `provenance.yaml`; an amendment is therefore orchestrator-only work in
  a decision pull request. The change's recorded bounded class does not
  require phase 2b or a new ADR draft.
