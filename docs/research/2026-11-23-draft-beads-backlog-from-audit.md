---
title: "Draft Beads Epics and prioritized backlog from the 2026-11-23 full codebase audit"
category: research
created: 2026-11-23
updated: 2026-11-23
last_reviewed: 2026-11-23
status: draft
implementation_status: none
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: antigravity, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [beads-draft, backlog, roadmap, priority, p1-budget, security, modularization, transferability]
---

# Draft Beads Epics and prioritized backlog from the `2026-11-23` full codebase audit

> [!IMPORTANT]
> **Draft only — zero tracker writes executed:** Per repository workflow and Session-0 read-only rules, **nothing in this document was written to Dolt (`.beads/`)**. Every Epic (`DRAFT-E1`..`DRAFT-E8`) and Task (`DRAFT-E1.1`..`DRAFT-E8.3`) is a reviewable draft derived from [the full codebase audit](./2026-11-23-full-codebase-architecture-security-audit.md) and [the Target-Architecture ADR draft](./2026-11-23-draft-adr-target-architecture-and-transferability.md). Existing cited tracker IDs come strictly from verified audit baseline `24632499`.

---

## Priority model & P1 budget summary (`AGENTS.md` house rules)

* **`P0` (Urgent / before `2026-11-30`):** Active calendar cliff (`2026-11-30`), live source-code exfiltration risks, privilege/execution boundary bypasses, the `architectural: 0` interview loophole, and acute workspace bloat (`155` live worktrees measured `2026-11-23`).
* **`P1` (Next two weeks — hard cap: `<= 10` non-epic beads):** Epics do **not** count toward the 10-bead P1 limit; every non-epic task (`10 / 10`) is budgeted tightly to unlock verification speed, shared primitives, `stage2.py` splitting, and kit/transfer readiness. Before promoting these drafts via `tools/bd create`, check how many P1 beads are currently open in `.beads/` (`tools/bd list`) and displace or defer lower-priority P1 items so total open P1 stays `<= 10`.
* **`P2` (Medium-term consolidation):** Verb engine completion, remaining research-swarm speedups, entry/governance doc rewrites, `report`-gate expiration cleanup, and installer/CLI polish.
* **`P3` (Longer-term expansion):** Non-Python `ToolchainPort` and external `TrackerPort` adapters, OS kernel sandboxing (`sandbox-exec`/`bwrap`), OTel JSONL + offline Stage-2 ROI benchmark, and `pyright`/`hypothesis` gates.
* Every draft task declares its **change class** (`spike`, `bounded`, `feature`, or `architectural`) in its description, matching [`AGENTS.md`](../../AGENTS.md).

### Summary table (8 Draft Epics · 30 Draft Tasks)

| Draft Epic | Epic Title | Priority | P0 | P1 | P2 | P3 | Primary Audit / Architecture Coverage |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `DRAFT-E1` | Stop the Bleeding: `2026-11-30` Cliff, Data-Governance Leaks, & P0 Security Containment | `P0` | 5 | 0 | 0 | 0 | Cliff, `C-1`, `C-2`, `C-3`, `S-1..S-9`, `O-1`, `A-4`, `A-12` |
| `DRAFT-E2` | Restore Fast Local Verification & Break the Test Ratchet | `P1` | 0 | 3 | 1 | 0 | `C-4`, `C-5`, `R-1..R-6`, `V-7..V-12`, `A-5`, Sec 9.3 |
| `DRAFT-E3` | Shared Primitive Foundation & State-First Persistence | `P1` | 0 | 2 | 1 | 0 | `C-6`, `A-2`, `A-3`, `A-12`, `S-10`, Sec 9.2 C |
| `DRAFT-E4` | Modularize `scripts/stage2.py` (11,487 LOC) & `tests/test_stage2.py` (28,466 LOC) | `P1` | 0 | 2 | 2 | 0 | `C-8`, `C-9`, `A-1`, `A-6`, `A-7`, Sec 5, Sec 9.2 A/B |
| `DRAFT-E5` | Kit Consolidation & Greenfield/Brownfield Transferability Foundation | `P1` | 0 | 3 | 2 | 0 | `C-7`, `C-10`, `A-8`, `A-10`, `A-11`, `T-1..T-4`, `T-6..T-10` |
| `DRAFT-E6` | Onboarding Documentation, `README.md`, & Entry-Doc Alignment | `P2` | 0 | 0 | 3 | 0 | `C-4`, `C-7`, Sec 7 (`README.md`, `AGENTS.md`, `WORKFLOW.md`, `governance/*`, missing files) |
| `DRAFT-E7` | Polyglot Toolchains, External Trackers, & OS-Level Process Sandboxing | `P3` | 0 | 0 | 0 | 3 | `T-5`, `T-6`, `S-2`, `O-2` |
| `DRAFT-E8` | Observability, Static Safety, & Stage-2 Empirical Evidence Loop | `P3` | 0 | 0 | 0 | 3 | `C-9`, `A-9`, `O-3..O-7` |
| **Total** | **8 Epics · 30 Tasks** | **Cap check** | **5** | **10 / 10** | **9** | **6** | **Reconcile 10 P1 slots with live Dolt P1 count at import** |

---

## `DRAFT-E1` (Epic · `P0`) — Stop the Bleeding: `2026-11-30` Cliff, Data-Governance Leaks, & P0 Security Containment

Addresses acute operational cutoffs (`2026-11-30`), verified source/credential leakage (`C-1`, `C-2`), O(N) SessionStart subprocess bottlenecks (`A-4`), the `architectural: 0` loophole (`C-3`), and live workspace accumulation (`155` worktrees).

### `DRAFT-E1.1` · Triage `2026-11-30` calendar cliff & expired role/endpoint dates
* **Priority:** `P0` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** Section 1 warning (`2026-11-30` cliff), `A-12`, Sec 7.2 (`provenance.yaml`, `model-endpoints.yaml`, `test_feedback_channel.py`)
* **Dependencies:** None (immediate).
* **Scope:**
  1. Re-read DeepSeek privacy/retention terms and update `model-endpoints.yaml:218` with fresh `valid_until` / `reading` dates.
  2. Triage all 13 `2026-11-30` deadlines in `scripts/ramp_valves.py`, `BESTAND_OHNE_ARTEFAKT` (`scripts/plans_registry.py:188`), and overdue vacant-role deadlines (`provenance.yaml:75-82`, expired `2026-10-31`).
  3. Delete or resolve the 10 permanently skipped `2ee-triage` bootstrap tests (`tests/test_ci.py:3177,3390`, `tests/test_feedback_channel.py:473-482`) per `R-4`, and capture the overdue `2026-11-22` ADR 0025 two-week measurement.
* **Acceptance Criteria:** Re-running `python3 scripts/ramp_valves.py` and `pytest` simulated against `2026-12-01` passes exit `0`; DeepSeek readings valid past `2026-12-31`; zero `@pytest.mark.skip` expiring `2026-11-30`.

### `DRAFT-E1.2` · Close `free_stage` unread-terms exfiltration & `prepare-loop` diff leak
* **Priority:** `P0` · **Change Class:** `feature` *(ADR decision if amending ADR 0021 Decision 3)* · **P1 slot:** —
* **Audit Refs:** `C-1`, `S-7` (`stage2_availability.py:1432,1465`, `model-endpoints.yaml:490-544,729`, `stage2_go.py`, `stage2_research_run.py:866-872,1270`), `research-handoff` `H-<n>` flooding
* **Dependencies:** Maintainer choice on `Q-ARCH-2` (or immediate diff-removal fix under existing `model-endpoints.yaml:583-586` contract first).
* **Scope:**
  1. Stop `stage2_availability.prepare()` (`prepare-loop`) from calling `free_probe_prompt()` or transmitting any repository diff before maintainer acknowledgement; enforce static tool-free 1-token reachability probes.
  2. Require explicit dated privacy readings (or strict allowlist) for all free models (retiring/gating suffix auto-admission per `Q-ARCH-2`) and reconcile `research_swarm.online_free.exclude` with `free_stage.exclude`.
  3. Remove raw `models-store.json` from temporary Pi configs and call `check_overlay()` in `probe_go` and `stage2_research_run.py`; disable HTTP redirects in `_fetch_intelligence()`; reject trailing `?`/`#`/spaces/`..`/`//` in `stage2_go.url_problem()`; isolate `stage_finders()` `system=` prompt and bound optional-seat `[DECISION]` injection (`research_handoff.py:85-94`).
* **Acceptance Criteria:** Mock-HTTP & Pi contract tests prove `prepare-loop` sends zero repository filenames/diff bytes; unlisted or unread `-free` models refuse before network dispatch; `url_problem` fuzz cases reject all malformed URLs; optional research seats cannot exceed capped decision quotas.

### `DRAFT-E1.3` · Harden live Pi/red-first/hook/permission/leakcheck trust boundaries & scrub public leaks
* **Priority:** `P0` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** `C-2`, `S-1`, `S-2`, `S-3`, `S-4`, `S-5`, `S-6`, `S-8`, `S-9`, `A-4`, `O-6` (`tools/pi/node_modules/`, `STAGE2_RED_TOKEN`, `--no-extensions`, `leakcheck.py`, `.claude/settings.local.json`, `night.py`, `tools/claude-code/`, `ci_gates.py`, `close_merged_beads.py`)
* **Dependencies:** None (high-priority sliceable bundle; split into <= 800 LOC PRs during execution).
* **Scope:**
  1. Attach hardened pathlock (blocking `.git/`, `.beads/`, `.claude/worktrees/`, `.stage2-sessions/`, `.env*` + macOS `readFallbacks`) to every paid review-loop Pi invocation (drop `--no-extensions`), pass `--no-tools` in `probe()`, include `tools/pi/node_modules/` in `tool_state()`, use `_git_bytes` in `ignored_snapshot()`, and run `uncommittable()` before `verify_attempt()`.
  2. Normalize `stage2-red-`/`stage2-fixed-` scratch prefixes, strip `STAGE2_RED_*` vars from child `os.environ` passing proof outputs via `pass_fds`, and AST-check `STAGE2_PLANT_FAULT` in `GUARD_SOURCE_PROBE_SOURCE`.
  3. Scrub `secret_values()` uniformly across `discover_free()`, `run_codex()`, `_protect_diagnostics()`, and `stage2_research_run.py`; scan all flags/args in `run_codex()`, `tools/bd`, `merge_guard.py`, and `omnigent_policy.py`; enforce `leakcheck` warnings/scans on readable gitignored worktree state + all custom refs (`refs/stage2/attempts/*`, `refs/dolt/data`, reflogs).
  4. Stop `$root/tools/bd` auto-execution on untrusted repos in `statusline.sh`/`handover.sh`, fix blank-line fail-open in `handover-trust`, explicitly deny push/merge/external-model tools in `night.py` regardless of `.claude/settings.local.json`, remove `O(N)` `SessionStart` explosion in `close_merged_beads.py`, clear `GITHUB_TOKEN` `--global extraheader` and pin SHA actions/`permissions:` in `ci_gates.py`, and scrub House Rule 6 / personal SSH / handle leaks (`S-9`, incl. `tests/test_regelwerk.py:340-346`, `docs/how-to/signed-decisions.md`, `COMMERCIAL.md`, `provenance.yaml`) plus enforce the ADR 0003 CI denylist (`coding-harness-lir`).
* **Acceptance Criteria:** Regression/property tests confirm `tool_state()` catches `tools/pi/node_modules/` edits, child tests cannot read/forge `STAGE2_RED_TOKEN`, `night.py` blocks `git push`/`gh pr merge`/`codex exec` even with `.claude/settings.local.json` present, `statusline.sh`/`handover.sh` never execute untrusted repo `tools/bd`, `SessionStart` bead sync finishes in `< 100 ms`, and ADR 0003 denylist scan exits `0`.

### `DRAFT-E1.4` · Fix `architectural` interview-minimum (`0 -> 5`), ADR requirement, & `needs_history` flag
* **Priority:** `P0` · **Change Class:** `bounded` *(or `architectural` per ADR 0014 alignment)* · **P1 slot:** —
* **Audit Refs:** `C-3`, `C-4` (`scripts/check_interview_minimums.py:82,133-146,454-470`, `decisions/gates.yaml:185-195`)
* **Dependencies:** Confirm `Q-ARCH-3` if stricter ADR enforcement alters ADR 0014 expectations.
* **Scope:**
  1. Set `MINIMUMS["architectural"] = 5` in `scripts/check_interview_minimums.py:82` and require prospective `architectural` changes (`spec.date > adoption day`) to claim at least one edited/created file under `docs/adr/` (or carry a recorded waiver).
  2. Add `needs_history: true` to `interview-minimums` in `decisions/gates.yaml:185-195` and regenerate `.github/workflows/ci.yml` (`scripts/ci_gates.py --generate-ci`).
  3. Fix CRLF `_SKIP_HEADING` and unhandled `OSError`/`UnicodeDecodeError` in `check_interview_minimums.py:98,212-249`.
* **Acceptance Criteria:** Unit tests in `tests/test_check_interview_minimums.py` prove an `architectural` change without `>= 5` maintainer answers and without a claimed ADR fails exit `1` prospectively while exempted stock remains green; `ci-drift` passes with `fetch-depth: 0` on the `interview-minimums` job.

### `DRAFT-E1.5` · Clean 155 stale worktrees & add safe `make prune-worktrees` garbage collector
* **Priority:** `P0` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** `O-1`, `C-2`, `C-8` (155 registered worktrees measured `2026-11-23`)
* **Dependencies:** None.
* **Scope:**
  1. Safely inventory and prune stale `.claude/worktrees/` folders whose branches are already merged/closed cleanly (preserving any dirty or active worktrees such as active audit branches).
  2. Implement `scripts/prune_worktrees.py` + `make prune-worktrees` (`--dry-run` default, `--write` opt-in) pruning merged worktrees, stale `.stage2-sessions/`, and orphaned XDG state folders safely.
  3. Add worktree count warning threshold in `scripts/machine_facts.py`.
* **Acceptance Criteria:** Active stale count under `.claude/worktrees/` drops from `155` to only live in-flight branches (`< 5`); `make prune-worktrees` refuses dirty or unmerged worktrees cleanly and prints reclaimed count/bytes.

---

## `DRAFT-E2` (Epic · `P1`) — Restore Fast Local Verification & Break the Test Ratchet

Delivers immediate `make verify` speedup (`~24-26 min -> < 8.5 min` full; `< 60 s` targeted) by eliminating double test runs, fixing `Makefile`/Dolt/non-admin friction, unlocking test consolidation via `criterion-ledger`, and removing `test_stage2.py`'s targeted-verify bypass.

### `DRAFT-E2.1` · Quick `verify` speedups: parallel/diff-triggered `leerprobe`, `Makefile` `.venv`, single `BEAD_RENDER`, & `--dist worksteal` *(P1 Slot 1 / 10)*
* **Priority:** `P1` (`[1/10]`) · **Change Class:** `bounded` · **P1 slot:** `1 / 10`
* **Audit Refs:** `C-4`, `C-5`, `V-7`, `V-10`, `V-11`, `coding-harness-w2ay`, `coding-harness-351h` (`scripts/kit/probe.py:356`, `decisions/gates.yaml:67,271`, `Makefile:21-134`)
* **Dependencies:** None.
* **Scope:**
  1. Pass `-n auto --dist worksteal` inside `decisions/gates.yaml:67` (`pytest`) and `scripts/kit/probe.py:356` (`leerprobe`); locally skip the redundant `probe.py` full pytest sweep when git diff touches zero `mechanismus`/manifest files (CI always runs full `probe.py --strict`).
  2. Render `BEAD_RENDER` once per local verify invocation (`verify_all.sh` / runner) and update `Makefile` targets (`test`, `staleness`, `gates`, `change`, `report`, `close-merged`, `archive`) to resolve `.venv/bin/python3` first.
  3. Replace polling `time.sleep()` waits across top offending test files with `threading.Event` / pipes / deterministic clocks (`V-10`), pin local `markdownlint-cli2` with `--ignore-scripts`, and scope `ruleset` command in `gates.yaml:271` with `-k test_master_has_a_ruleset_with_required_checks`.
* **Acceptance Criteria:** Measured local `make verify` drops by `>= 4 minutes`; Dolt exports once instead of 4x per verify; external contributors using `make` targets invoke `.venv` Python cleanly.

### `DRAFT-E2.2` · Extend `criterion-ledger` with `superseded_by` / `retired`, `adoption.yaml`, & expiring transition tests *(P1 Slot 2 / 10)*
* **Priority:** `P1` (`[2/10]`) · **Change Class:** `feature` *(touches ADR 0013 behavior — needs maintainer decision `Q-ARCH-5`)* · **P1 slot:** `2 / 10`
* **Audit Refs:** `C-5`, `R-1`, `A-12`, `coding-harness-1ga5`, `coding-harness-wpv` (`scripts/check_criterion_ledger.py:63,316-317`)
* **Dependencies:** `Q-ARCH-5`.
* **Scope:**
  1. Wire `scripts/adoption.py` (`decisions/adoption.yaml`) into `check_criterion_ledger.py` (`coding-harness-wpv`) so brownfield repos exempt legacy stock and empty `plans/changes/` returns `0` rather than exit `3`.
  2. Add structured redirect/retirement support (`superseded_by: tests/<path>::<fn> — <reason>` / `retired: <reason>` or `decisions/ledger-redirects.yaml`) validated to require an active target test on `superseded_by` and a reason/bead on `retired`.
  3. Support `@pytest.mark.transition(until_bead=...)` checked automatically against `BEAD_RENDER` status so temporary regression/migration guards expire when their bead closes.
* **Acceptance Criteria:** `check_criterion_ledger.py` passes on brownfield trees without `plans/changes/`, resolves `superseded_by` transitively without false red errors, and blocks closed-bead `@pytest.mark.transition` tests; `test_stage2.py` refactoring slices (`DRAFT-E4`) can migrate ledger tests safely.

### `DRAFT-E2.3` · Parallel Python verify runner, content-hashed local verdict cache, & non-admin `ruleset` handling *(P1 Slot 3 / 10)*
* **Priority:** `P1` (`[3/10]`) · **Change Class:** `feature` · **P1 slot:** `3 / 10`
* **Audit Refs:** `C-4`, `A-5`, `V-11`, `V-12`, `coding-harness-43iz`, `coding-harness-u3qg` (`scripts/verify_all.sh`, `scripts/ci_gates.py:845-858`, `tests/test_repo_settings.py`)
* **Dependencies:** `DRAFT-E2.1`.
* **Scope:**
  1. Consolidate `scripts/verify_all.sh` Bash orchestration (including Bash 5.2 `L505-516` bug and reachable `ci_gates.py --check-schema` CLI path) into `scripts/verify_runner.py` with a thin shell shim.
  2. Run independent read-only `seconds` gates via `ThreadPoolExecutor(max_workers=4)` before `minutes` gates, calling `verify_duration` in-process (eliminating 67 subprocess spawns).
  3. Add content-hashed local green verdict cache under `$XDG_STATE_HOME` keyed on `(git tree + dirty diff + gates.yaml + requirements-ci.txt + package-lock.json + BEAD_RENDER)` (strictly disabled in CI), cache `require_installed_pi()` at pytest session scope, and degrade HTTP 403 / non-admin `gh` scope on `ruleset` locally with explicit `SKIPPED (no admin scope)` status rather than blocking non-admin contributors (`T-7`).
* **Acceptance Criteria:** Re-running `make verify` on an identical tree finishes in `< 2 s`; `seconds` gates fail-fast in `< 4 s`; external non-admin GitHub clones achieve clean local verify without failing `ruleset`; all gate timing tests remain green.

### `DRAFT-E2.4` · Test-suite consolidation (-600 to -910 `def test_*`), APFS `world` / swarm templates, & Sec 9.3 flakiness fixes
* **Priority:** `P2` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** `R-2..R-6`, `V-8`, `V-9`, `coding-harness-0swp`, `coding-harness-dca4`, `coding-harness-wnka`, Section 9.3
* **Dependencies:** `DRAFT-E2.2`, `DRAFT-E4.1` (for `stage2_support.py`).
* **Scope:**
  1. Parametrize top single-assertion and prefix-clustered micro-tests (`-300` to `-450` functions), table-consolidate 159 prose-substring tests (`-90` to `-120`), demote ~120 redundant logic tests out of `test_stage2_swarm.py`, and deduplicate `test_ci.py` / copy-pasted `_git` fixtures (`-80` to `-130` functions).
  2. Add in-process callable transport seam in `stage2_research_dispatch.py`, APFS `cp -cR` session git templates for `world`/`sworld`, `venv_pytest` routing for non-proof nested pytest calls, batched Node driver invocations (`test_stage2_session_policy.py` / `test_stage2_research_tools.py`), and fast `tool_state()` stubbing outside R-21 tests.
  3. Fix all verified Section 9.3 test-integrity & isolation gaps (`S-10` six defective tests, blinded key assertion in `test_stage2.py:1670-1700`, `pi_network_guard.mjs` `Socket.prototype.connect`/`http2`/`WebSocket`/`dns`, non-daemon `StandIn` threads, `chmod(0o000)` root dependence, `SIGINT`/`SIGTERM` worker hazards, and `test_ci.py` xdist race writing inside `scripts/`).
* **Acceptance Criteria:** Test count shrinks cleanly by `>= 20%` with full mutation coverage intact (`mutation_evidence.py`); full uncached `make verify` completes in `<= 8.5 min` with zero host-clock/xdist flakes.

---

## `DRAFT-E3` (Epic · `P1`) — Shared Primitive Foundation & State-First Persistence

Eliminates duplicated parsing/git/FS/verdict side routes (House Rule 9), resolves Section 9.2 C validator bugs, replaces fragile Markdown regex state machines with locked JSON/JSONL, and puts expiration valves on every `report` gate.

### `DRAFT-E3.1` · Consolidate shared primitives (`_yaml_strict`, `_fs_atomic`, `_git_exec`, `_verdict`) & fix Section 9.2 C gate bugs *(P1 Slot 4 / 10)*
* **Priority:** `P1` (`[4/10]`) · **Change Class:** `bounded` · **P1 slot:** `4 / 10`
* **Audit Refs:** `A-2`, Section 9.2 C (all gate & lifecycle scripts)
* **Dependencies:** None (foundation for `DRAFT-E4` slices).
* **Scope:**
  1. Extract shared `_yaml_strict.py` (consolidating 7 duplicate-rejecting `SafeLoader`s and 18 frontmatter/header parsers, handling BOM/CRLF/EOF/YAML `.nan`/`.inf`/datetime types cleanly), `_fs_atomic.py` (symlink-safe `lstat()` + `mkstemp` + `fsync` atomic writes), `_git_exec.py` (consolidating 6 git wrappers with `GIT_*` sanitization and timeouts), and `stage2_models.py` / unified `model-endpoints.yaml` reader.
  2. Route all 12 `check_*.py` validators through `scripts/_verdict.py` (including `bead_render.py` calling `check_bead_export.run()`, fixing `sys.path` guards on `check_bead_export`/`check_dangling_bead_ids`, extending `check_dangling_bead_ids.py` to `plans/` and dotted sub-beads).
  3. Fix verified Section 9.2 C defects: `gate_record.py` mandatory `author`/`last_pusher` + tz-aware dates; `check_worktree_state.sh` ancestor check + `REVERT_HEAD`/`BISECT_LOG` + `--`; `leakcheck.py` `=` parsing/symlinks/detached HEAD; `plans_registry.py` `supersedes` containment & error handling; `new_change.py` rollback on failure & removal of stale `bd export` hint; `time_records.py` CRLF split; `check_docs.py` `REPO_ROOT` containment/binary/fenced-block fixes; `archive_closed_changes.py` `_relocate` symlink check; `verify_lock.py` FD leak/`0700`/holder token/`killpg`; `verify_duration.py` dir ownership; `run_report.py` `vm_stat` regex; `mutation_evidence.py` digit script names; `ci_gates.py` scalar quoting; `ramp_valves.py` missing-`ruff` error; `touch_map.py` Mermaid label escaping; `render_beads_export.py` empty-output guard; `close_merged_beads.py` startup budget; `check_question_context.py` URL wrapping; `check_frontmatter_current.py` `--stamp` symlink safety.
* **Acceptance Criteria:** 1 shared frontmatter/strict-YAML loader, 1 git exec helper, 1 atomic writer, and all `check_*.py` scripts use `_verdict`; all Section 9.2 C edge-case tests pass under property checks.

### `DRAFT-E3.2` · Replace Markdown loop-state regexes with locked canonical `loop.state.json` + deterministic rendering *(P1 Slot 5 / 10)*
* **Priority:** `P1` (`[5/10]`) · **Change Class:** `architectural` *(or `feature` if schema-scoped under ADR 0021)* · **P1 slot:** `5 / 10`
* **Audit Refs:** `C-6`, `A-3`, `S-10` (Section 9.2 A `L3411-4735` loop state, release, marks, `receipt_lock`)
* **Dependencies:** `DRAFT-E3.1`.
* **Scope:**
  1. Define versioned JSON schema for per-change loop & availability receipts (`loop.state.json` + HMAC/lock-guarded `receipt_lock` across `prepare`/`consume`/`spend`).
  2. Persist loop state, rounds, retired stages, Phase-6 verdicts, and audit rows canonically in `loop.state.json`; render `loop.md` and `findings.md` released tables deterministically using pipe/newline/bidi escaping (fixing `_PIPE` `\\|`, `dropped_notice` `\u2028`/`\u2029`, `retire_stage`, `fill_marks`, `mark_repaired_findings` `Broke a test`, `restart_loop`, `review_audit_only`, and pre-verify `release` overlap checks).
  3. Support one-sprint read fallback for legacy in-flight `loop.md` files alongside migration notice.
* **Acceptance Criteria:** Zero state-parsing regexes read mutable prose tables for control flow; concurrent `prepare`/`consume` races rejected cleanly by `receipt_lock`; adversarial `\r\n`, `\\|`, and Unicode control characters round-trip safely.

### `DRAFT-E3.3` · Add expiration valves (`promote_by`/`sunset_by`) to all `report` gates & burn down 199 `docs-links` findings
* **Priority:** `P2` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** `C-4`, `A-12` (`decisions/gates.yaml:117-126`, `scripts/check_docs.py`, `scripts/ramp_valves.py`, `docs/orchestration.md:29`)
* **Dependencies:** `DRAFT-E3.1`.
* **Scope:**
  1. Require every `enforcement: report` gate (unless explicitly documented permanent, e.g., `research-currency`) to carry a dated `promote_by` or `sunset_by` field checked by `ramp_valves.py`.
  2. Split `check_docs.py` into a blocking `docs-links-live` check (all active docs, anchors, and non-legacy docs — fixing `docs/orchestration.md:29` and broken `governance/*` links) plus a ratcheted legacy handover frontmatter check that shrinks monotonically to zero.
* **Acceptance Criteria:** `check_docs.py` reports zero unresolved links/anchors across all active `README.md`, root, architecture, and governance docs; `docs-links` active check promoted cleanly to `enforcement: block`.

---

## `DRAFT-E4` (Epic · `P1`) — Modularize `scripts/stage2.py` (11,487 LOC) & `tests/test_stage2.py` (28,466 LOC)

Executes the Section 5 16-slice acyclic extraction (`Layers 0–4`), destroys the four circular import chains, removes `stage2.py:6911-6912` so ADR 0025 targeted checks work again, fixes all Section 9.2 A/B runtime bugs, and optimizes research swarm execution.

### `DRAFT-E4.1` · Extract `stage2` test support + Layers 0–1 leaf modules (`core`, `secrets`, `process`, `artifacts`, `git`) & fix Section 9.2 A leaf bugs *(P1 Slot 6 / 10)*
* **Priority:** `P1` (`[6/10]`) · **Change Class:** `bounded` · **P1 slot:** `6 / 10`
* **Audit Refs:** `A-1`, Section 5 (`PR 0a`–`PR 5`), Section 9.2 A (`L844-1102, 2285-3056, 4782-5474`)
* **Dependencies:** `DRAFT-E2.2`, `DRAFT-E3.1`.
* **Scope:**
  1. Extract shared fixtures (`World`, `FakeClock`, `TEST_LADDER`) into `tests/stage2_support.py`, split doctrine tests into `tests/test_stage2_doctrine.py`, and add `tests/test_stage2_architecture.py` (enforcing acyclic graph and zero `ImportFrom` on monkeypatched seams).
  2. Extract `stage2_core.py`, `stage2_secrets.py` (immediately fixing the `stage2_availability.py:144` double-import bug), `stage2_process.py`, `stage2_artifacts.py` + `stage2_research_pub.py`, and `stage2_git.py` across green PRs <= 800 lines each with parallel split test modules.
  3. Fix verified leaf defects: `_LIVE_LOCK`/PGID-reuse/untimed `launch()` (`L968-1102`), `.nan`/`.inf` in `request_value` (`L2285-2307`), `--no-renames`/`--literal-pathspecs`/`split("\n")` in `free_diff` & leading-`-` paths in `change_diff`, $O(N^2)$ `_rule_spans` + `scrub()` before `safe_boundary` (`L844-927`), `plan_baseline_restore` base (`L5382`) & `git clean -ffdq`, and `_secret_entries` fail-closed decoding.
* **Acceptance Criteria:** Zero circular imports between `stage2` and `stage2_availability`/`swarm`; `test_stage2_architecture.py` green; `test_stage2.py` shrinks by ~5,000+ lines; all PRs <= 800 lines.

### `DRAFT-E4.2` · Extract Layer 2–3 domain/execution modules (`admission`, `loop_record`, `worktree`, `runners`, `verify`, `repair_proof`), clear `runner.*` lookups *(P1 Slot 7 / 10)*
* **Priority:** `P1` (`[7/10]`) · **Change Class:** `bounded` · **P1 slot:** `7 / 10`
* **Audit Refs:** `A-1`, `A-7`, Section 5 (`PR 6`–`PR 13`), Section 9.2 A (`L2143-2866, 6748-8484`), `coding-harness-vg9`
* **Dependencies:** `DRAFT-E4.1`, `DRAFT-E3.2`.
* **Scope:**
  1. Extract Layer 2 (`stage2_admission.py`, `stage2_free_catalog.py`, `stage2_preflight.py`, `stage2_loop_record.py`, `stage2_worktree.py`, `stage2_checkpoint.py`) and Layer 3 (`stage2_runners.py`, `stage2_targeted.py`, `stage2_verify.py`, `stage2_repair_proof.py`) with matching `tests/test_stage2_<domain>.py` files.
  2. Eliminate all 66 `runner.*` dynamic service-locator lookups across `stage2_availability.py`, `stage2_session.py`, `stage2_research_run.py`, and `stage2_swarm.py` using typed L0–L3 imports.
  3. Fix lock-protected `ContextVar` collectors (`L2143-2191`), `NotStarted` vs `CallFailed` re-raising, `discover_free` `PI_OFFLINE=1` & `catalog-only` sentinel, `timeout_seconds is not None` (`0` vs `None`), and import-time `_pi_pin()` deferral (`L260-276`, exit 2 on Pi verbs only).
* **Acceptance Criteria:** Zero `runner.*` attributes left anywhere in `scripts/`; all 4 circular import chains eliminated; `tests/test_stage2.py` moves ~15,000+ lines into domain test files.

### `DRAFT-E4.3` · Complete Layer 4 (`AttemptEngine` + thin `stage2.py`), unlock ADR 0025 targeted checks, & fix Section 9.2 B swarm/session/runs bugs
* **Priority:** `P2` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** `A-1`, `A-7`, Section 5 (`PR 14a`–`PR 15`), Section 9.2 A (`L9322-10531`) & Section 9.2 B (`stage2_swarm`, `stage2_availability`, `research_capture`, `stage2_research_*`, `research_handoff`, `stage2_session`, `stage2_runs`)
* **Dependencies:** `DRAFT-E4.2`, `DRAFT-E2.2`.
* **Scope:**
  1. Extract Layer 4 verb orchestrators (`stage2_attempts.py` + unified `AttemptEngine` serving `draft`/`implement`/`repair`, `stage2_draft.py`, `stage2_repair.py`, `stage2_review_verbs.py`, `stage2_explore_triage.py`), slimming `scripts/stage2.py` to ~220 lines and `tests/test_stage2.py` below 1,000 lines.
  2. Migrate `pr_sync.py` away from AST-scraping `stage2.py:RUNNER_HELD` (`stage2_runs.py` included) and remove the hardcoded `test_stage2.py` bypass at `stage2.py:6911-6912` (`coding-harness-vg9`).
  3. Fix verified Section 9.2 B defects: `draft()` symlink/tamper/time-log parity, `stage2_swarm.py` type validation & `opencode-go` `residenz` checks, `stage2_availability.py` `darf_sehen` / `audit[1:]` loss / paid probe retries / `--seats` exit 2, `research_capture.py` pre-canary redaction order, `stage2_research_store.py` `../` traversal, `stage2_research_report.py` `_public_url` SSRF, `stage2_research_tools.mjs` receipt-before-fetch / `bytes` / `final_url` / hard tool cap / Slowloris total timeout / script stripping, `stage2_research_refs.py` Python decorators, `research_handoff.py` `claims`/empty-`relations`/block-scalars, `stage2_session.py` prompt in argv / stale pending cleanup / `0o700` dir mode, and `stage2_runs.py` missing `opencode-go` route.
* **Acceptance Criteria:** Targeted verification executes in `< 60 s` on repaired `stage2_<domain>.py` modules without falling back to full 24-minute verify; all Section 9.2 B defects covered by unit tests.

### `DRAFT-E4.4` · Eliminate research-swarm waste: commit-cached `leakcheck`, deterministic `stage_merge`, & `Run` split
* **Priority:** `P2` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** `C-9`, `A-6` (`stage2_research_run.py` 1,497-line `Run`, `stage2_research_dispatch.py` 100 Hz polling)
* **Dependencies:** `DRAFT-E4.2`.
* **Scope:**
  1. Decompose `Run` into `Snapshot`, `Planner`, `Dispatcher`, and `Reconciler` (removing `Run.__new__(Run)` bypass in `research_capture.py:1090`), synchronize `on_terminal`, replace 100 Hz polling with blocking wait, and preserve failed attempt reasons on multi-batch `stage_topics`.
  2. Cache repository/history `leakcheck` once per immutable commit OID + run only lightweight per-slot prompt scanning in parallel slots (replacing 39–90 serial full-repo scans).
  3. Replace the Opus 5.5 `stage_merge` LLM call with deterministic Python merging while escaping HTML comment markers (`<!--`/`-->`) in composed envelope lines.
* **Acceptance Criteria:** Research-swarm runs execute full `leakcheck` once per tree instead of 39–90x; zero Opus tokens billed on `stage_merge`; zero `Run.__new__` test workarounds.

---

## `DRAFT-E5` (Epic · `P1`) — Kit Consolidation & Greenfield/Brownfield Transferability Foundation

Turns Monotrope from a single-repository harness into a clean, transferable Layer A/B core with unified manifests (`DECKEL = 0`), `monotrope.yaml`, zero-tracker & additive-CI brownfield onboarding, subpackage-aware tooling, and `validate_change_artefacts.py`.

### `DRAFT-E5.1` · Promote Target-Architecture & Transferability ADR (`Q-ARCH-1..5`) via Phase 1a + `decide(...)` PR *(P1 Slot 8 / 10)*
* **Priority:** `P1` (`[8/10]`) · **Change Class:** `architectural` · **P1 slot:** `8 / 10`
* **Audit Refs:** `C-7`, `C-10`, `T-1`, `T-9`, [Target-Architecture ADR draft](./2026-11-23-draft-adr-target-architecture-and-transferability.md)
* **Dependencies:** Maintainer review & answers to `Q-ARCH-1` through `Q-ARCH-5`.
* **Scope:**
  1. Conduct Phase 1a interview with maintainer covering `Q-ARCH-1` (Open-Core Apache-2.0 for Layer A vs PolyForm-all), `Q-ARCH-2` (retire unread `-free` auto-admission), `Q-ARCH-3` (`architectural >= 5`), `Q-ARCH-4` (`tracker: none` brownfield default), and `Q-ARCH-5` (`criterion-ledger` redirects).
  2. Promote `docs/research/2026-11-23-draft-adr-target-architecture-and-transferability.md` -> `docs/adr/0026-microkernel-state-first-and-portable-transfer-architecture.md` with continuity updates if needed and open a `decide(architecture): ...` PR.
* **Acceptance Criteria:** Maintainer interview records `>= 5` answered questions in `decisions.md`; ADR 0026 merged by maintainer (`decision` PR, CI green, House Rule 8 honored).

### `DRAFT-E5.2` · Unify kit & export manifests, purge Databricks agents & hardcoded continuity floor, & drive `DECKEL` from 44 -> 0 *(P1 Slot 9 / 10)*
* **Priority:** `P1` (`[9/10]`) · **Change Class:** `bounded` · **P1 slot:** `9 / 10`
* **Audit Refs:** `C-7`, `A-8`, `T-10`, `S-10` (`scripts/kit/manifest.yaml`, `scripts/export/manifest.yaml`, `scripts/kit/probe.py:208`, `scripts/check_decision_continuity.py:28-56`)
* **Dependencies:** `DRAFT-E2.1` (optional), `DRAFT-E5.1` (if altering kit continuity contract).
* **Scope:**
  1. Retire `scripts/export/manifest.yaml`; standardize on one unified manifest distinguishing `core` (`mechanismus`), `stage2`, and `bestand` (`tests/test_this_repository_*.py` isolated cleanly), fixing duplicated `ci.yml` rules, missing `bead_render.py`, orphaned `research-swarm-limits.yaml`, and dead entries.
  2. Remove the 7 German Databricks domain agents from `.claude/agents/` (`mechanismus` -> archive/repo-local), extract a sanitized `templates/provenance.yaml` (free of personal emails/legacy paths), parameterize `BESTAND_OHNE_ARTEFAKT` (`plans_registry.py`), and move hardcoded `check_decision_continuity.py` (`2026-09-17-omnigent-first-target.md`, `D-1..D-17`) out of global portable `floor: true` into repo-local config.
  3. Fix broken throwaway-repo test imports and drive `REIST_NICHT` / `DECKEL` in `scripts/kit/probe.py` monotonically from `44` down to `0` (`kit/probe.py` quadratic filter cleanup included).
* **Acceptance Criteria:** `scripts/kit/probe.py --strict` passes with `DECKEL = 0`; zero unresolved imports, Databricks prompts, or personal handles/SSG paths inside exported core artifacts.

### `DRAFT-E5.3` · Ship `monotrope.yaml` contract, `tracker: none`, `ci: additive`, & `monotrope init / upgrade / doctor` *(P1 Slot 10 / 10)*
* **Priority:** `P1` (`[10/10]`) · **Change Class:** `feature` · **P1 slot:** `10 / 10`
* **Audit Refs:** `T-2`, `T-3`, `T-4`, `T-6`, `T-7`, `coding-harness-dj9`, `coding-harness-lir` (`check_dangling_bead_ids.py:32`, `ci_gates.py`, `adoption.py`)
* **Dependencies:** `DRAFT-E5.1` (`Q-ARCH-4`), `DRAFT-E5.2`.
* **Scope:**
  1. Implement `scripts/project_config.py` reading schema-validated `monotrope.yaml` (`project`, `default_branch`, `level: L0..L3`, `paths`, `tracker.{kind,prefix}`, `toolchain`, `ci.{forge,mode,required_check}`, `governance.{human_roles,default_owner}`, `decisions/valves.yaml`) and replace hardcoded `"coding-harness-"`, `"main"`, and `"coding-harness"` XDG names across all scripts and hooks.
  2. Support `tracker.kind: none` (`T-6`, skipping Dolt hydration and bead-prefix gates cleanly on L1 brownfield repos), `ci.mode: additive` (`T-7`, generating `.github/workflows/monotrope-gates.yml` or reusable step alongside existing CI), and `frontmatter: required`-scoped `check_docs.py`/`check_frontmatter_current.py` plus shallow-history PR-diff fallback (`T-4`).
  3. Build `monotrope init [--greenfield|--brownfield] [--level L0|L1|L2]`, `monotrope upgrade` (3-way Copier-style diff + upgrade-date `adoption.yaml` defaults), and `monotrope doctor` / `verify-pin` over SHA-256 `harness.lock.yaml` (`monotrope-core` needing stdlib + PyYAML only; `tools/beads/checksums` + `tools/cloud-env/setup.sh` multi-arch/hardening included).
* **Acceptance Criteria:** `monotrope init --brownfield --level L1` initializes an existing non-Python repo (`master`, existing `.github/workflows/ci.yml`, MkDocs docs, no Dolt) cleanly with zero manual edits and Day-1 green gates.

### `DRAFT-E5.4` · Deliver promised `validate_change_artefacts.py` (`coding-harness-jc3`) & dual greenfield/brownfield `probe.py`
* **Priority:** `P2` · **Change Class:** `feature` · **P1 slot:** —
* **Audit Refs:** `C-7`, `T-10`, `coding-harness-jc3`, Sec 7.1 (`README.md:240,259`)
* **Dependencies:** `DRAFT-E5.2`, `DRAFT-E5.3`.
* **Scope:**
  1. Implement `scripts/validate_change_artefacts.py` checking open `[DECISION]`/`[AMBIGUITY]`/`[GAP]` tags in `spec.md`, required spec/design/plan sections, and `research-handoff` integrity, wired into `decisions/gates.yaml` (`subsets: [docs]`, `adoption.yaml` cut-off).
  2. Upgrade `scripts/kit/probe.py` to test **two** disposable fixtures continuously on every PR (`DECKEL = 0`): (a) clean greenfield Python repo, and (b) non-Python brownfield repo (`master`, existing CI, existing SSG docs, `CLAUDE.md`, `tracker: none`, pre-adoption unledgered plans).
* **Acceptance Criteria:** `README.md`/`WORKFLOW.md` claims about open `[DECISION]` enforcement hold in code; both throwaway fixtures pass `--strict` with zero skips or `DECKEL`.

### `DRAFT-E5.5` · Upgrade `touch_map.py`/`test_ci.py` for subpackages, decouple Claude hooks (H6), cross-platform sessions, & D-16/enterprise endpoints
* **Priority:** `P2` · **Change Class:** `feature` · **P1 slot:** —
* **Audit Refs:** `A-10`, `A-11`, `T-8`, `T-9` (`scripts/touch_map.py:420-429`, `tests/test_ci.py`, `tools/claude-code/`, `tests/test_entry_points.py`, `scripts/stage2_session.py:72`)
* **Dependencies:** `DRAFT-E5.3`.
* **Scope:**
  1. Extend `touch_map.py` and `tests/test_ci.py:_scripts()` for dotted/relative Python subpackages (`harness/` or nested modules) and add TS/JS/Go/Rust import discovery with safe full-verify fallback (`T-5`/`A-10`).
  2. Extract `session_scan`, `night_policy`, `beads_start`, and `terminal_dispatch` into harness-neutral Python (`A-11`); add cross-platform terminal adapters (`macos-terminal`, `tmux`, `linux-terminal`, `foreground`) replacing hardcoded `osascript`; shrink `.claude/`, `tools/claude-code/`, `.codex/agents/*.toml` (adding missing tool/sandbox restrictions) to thin shims; generate drift-checked pointer shims (`CLAUDE.md` `@AGENTS.md`, `.cursor/rules/`, `.github/copilot-instructions.md`) replacing the blanket `CLAUDE.md` ban; and add an automated H6 adapter-deletion test.
  3. Complete D-16 capability-role decoupling (`model-routing.yaml`), ship enterprise cloud starter profiles (`anthropic-stage1`, `enterprise-cloud`, `openai-codex-only`), enforce `usage_context: commercial | client-paid` technically against personal subscriptions, and add `leakcheck --history-scope branch` (BSD/GNU portability in `handover.sh:84-95` included).
* **Acceptance Criteria:** Deleting `.claude/` and `tools/claude-code/` still passes H6 workflow tests; `stage2 session` launches under `tmux` on Linux; brownfield `leakcheck --history-scope branch` logs scoped coverage in audit lines.

---

## `DRAFT-E6` (Epic · `P2`) — Onboarding Documentation, `README.md`, & Entry-Doc Alignment

Aligns all human and agent entry points with actual code behavior (`24632499+`), eliminates factual contradictions (`validate_change_artefacts`, stop hooks, ADR 0023/0025 status, `199` vs `35`), breaks up `docs/WORKFLOW.md`, and creates missing standard entry files.

### `DRAFT-E6.1` · Rewrite `README.md` for 3-minute onboarding, external-cloner clarity, & honest status
* **Priority:** `P2` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** Sec 7.1 (`README.md:54-62, 89-95, 109-117, 164, 173-184, 205, 225-240, 259-261, 290-292`)
* **Dependencies:** Coordinate status wording with `DRAFT-E1.2`/`DRAFT-E2.1`/`DRAFT-E5.4`.
* **Scope:**
  1. Fix `README.md:54-62` (ADR 0023/0025 repair & targeted checks), `L89-95`/`L261` (exact pathlock / `leakcheck` / `recap.sh` boundaries), `L109-117` (all sub-phases `1a`, `2a`, `2b`, `4b` + research swarm), `L164` broken `#working-in-parallel` target, and `L240`/`L259` `[DECISION]` claim.
  2. Document external cloner steps cleanly (`--ci` / non-admin `ruleset`, `tools/beads/checksums` supported OS/arch, `.venv/bin/python3`, `~/.config/cc-routing/{secrets.env,denylist.txt}`, external `XDG_STATE_HOME` outside `$HOME`), unify cut-off dates (`L225-231`), generalize private dogfooding reference (`L205`), clarify hook side effects (`L290-292`), and add the L0–L3 adoption table upfront.
* **Acceptance Criteria:** A brand-new non-admin cloner can go from `git clone` to green local verification in <= 3 minutes following `README.md` without hitting undocumented failures; `check_docs.py` reports 0 errors on `README.md`.

### `DRAFT-E6.2` · Refactor `docs/WORKFLOW.md` (2,213 LOC) & update `AGENTS.md`, `docs/how-it-works.md`, `docs/testing.md`, & `docs/orchestration.md`
* **Priority:** `P2` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** Sec 7.2 (`AGENTS.md`, `docs/WORKFLOW.md`, `docs/how-it-works.md`, `docs/testing.md`, `docs/orchestration.md`)
* **Dependencies:** `DRAFT-E6.1`.
* **Scope:**
  1. Split `docs/WORKFLOW.md` into core 7-phase doctrine (~350–450 lines) + focused reference pages (`docs/workflow-stage2-reference.md`, `docs/workflow-operations.md`), fixing all 8 phantom validator/stop-hook claims, L837 container contradiction, L922 API list, L1799 exit codes, L2084 `templates/findings.md` misstatement, and obsolete Sept-2026 section 9.
  2. Refresh `AGENTS.md` (keep `< 200` lines; update September bootstrap note, Phase table `research-handoff`/ADR 0023/0025/actual gates, remove legacy internal phrasing), `docs/how-it-works.md` (`public-web` class, `prepare-explore`, `XDG_STATE_HOME`, targeted `implement`), `docs/testing.md` (`tools/pi/install.sh`, ADR 0023 live status, honest stop-hook status), and `docs/orchestration.md` (fix `L29` dead anchor, reconcile night-run `WORKFLOW.md` contradiction, generalize `D-60`/RAM).
* **Acceptance Criteria:** Zero contradictions between `README.md`, `AGENTS.md`, `WORKFLOW.md`, `how-it-works.md`, `testing.md`, and `orchestration.md`; `check_docs.py` resolves every link and anchor across all five documents.

### `DRAFT-E6.3` · Create missing standard entry files (`docs/_INDEX.md`, `docs/onboarding.md`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/adr/_INDEX.md`) & fix governance/tool READMEs & indices
* **Priority:** `P2` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** Sec 7.2 (`ROADMAP.md`, `COMMERCIAL.md`, `docs/governance/*`, `docs/architecture/target-architecture.md`, `tools/*/README.md`, `plans/INDEX.md`, `plans/_README.md`, `docs/*/_INDEX.md`, `.claude/commands/workflow-start.md`, `coding-harness-yim`)
* **Dependencies:** `DRAFT-E5.1` (`Q-ARCH-1` for `COMMERCIAL.md`/`LICENSE` cross-links).
* **Scope:**
  1. Author the 5 missing standard entry files (`docs/_INDEX.md`, `docs/onboarding.md` with Greenfield & Brownfield quickstarts, `CONTRIBUTING.md`, `SECURITY.md`, `docs/adr/_INDEX.md`).
  2. Triage `ROADMAP.md` (refresh or retire per `L9-10`), update `COMMERCIAL.md` (replace personal handle with neutral contact, update superseded `D-17` link) and `docs/architecture/target-architecture.md` historical banner, regenerate `docs/governance/gate-catalog.md` in English from translated `decisions/gates.yaml:126,267`, and schedule dedicated decision/translation PRs (`coding-harness-yim`) for `docs/governance/quality-gates.md` (drop `disclosure: intern`, data-warehouse gates, 8 dead links) and `docs/governance/regelwerk.md` (translate to English, fix 7 dead links).
  3. Update `tools/{claude-code,cloud-env,omnigent,pi}/README.md` (fix 27 vs 29 tools, table 6 -> 8 files, `tools/pi/install.sh` in cloud-env, Node typo), separate active vs archived in `plans/INDEX.md` + fix `plans/_README.md`, translate `docs/journal/_INDEX.md`, sync `docs/research/_INDEX.md` (closing the 45-note gap), and parameterize `.claude/commands/workflow-start.md`.
* **Acceptance Criteria:** Every index and entry file promised in docs exists, passes `check_docs.py` with 0 errors, and reflects live `main` cleanly in English.

---

## `DRAFT-E7` (Epic · `P3`) — Polyglot Toolchains, External Trackers, & OS-Level Process Sandboxing

Completes Layer B adapters (`ToolchainPort`, `TrackerPort`) and Layer C kernel sandboxing (`sandbox-exec` / `bwrap`) so Monotrope enforces equivalent verification and confinement guarantees on macOS, Linux, and non-Python stacks.

### `DRAFT-E7.1` · Implement polyglot `ToolchainPort` (Python, TS/JS, Go, Rust via JSON/JUnit/TAP)
* **Priority:** `P3` · **Change Class:** `feature` · **P1 slot:** —
* **Audit Refs:** `T-5`, Pillar 1 Layer B
* **Dependencies:** `DRAFT-E5.3`, `DRAFT-E4.3`.
* **Scope:**
  1. Support arbitrary runtimes & `setup_steps` under `tools:` in `decisions/gates.yaml`.
  2. Make `check_criterion_ledger.py` test-ID resolution pluggable across `pytest`, `vitest`/`jest`, Go `func Test`, and Rust `fn test_`.
  3. Route Stage-2 red-first proofs and cheap targeted checks through structured `ToolchainPort` adapters parsing JUnit XML, `vitest --reporter=json`, `go test -json`, `cargo test --message-format=json`, or TAP (retaining Python `RED_PROBE` as the Python adapter).
* **Acceptance Criteria:** Reference TS/Node and Go fixture repos pass Stage-1 `criterion-ledger`, targeted repair checks, and red-first proof runs natively without Python test code.

### `DRAFT-E7.2` · Enforce kernel/OS sandboxing (`sandbox-exec` / `bwrap`) & out-of-process red-first proofs
* **Priority:** `P3` · **Change Class:** `feature` · **P1 slot:** —
* **Audit Refs:** `O-2`, `C-2`, `S-2`, `README.md:261`, Pillar 3
* **Dependencies:** `DRAFT-E1.3`, `DRAFT-E4.2`.
* **Scope:**
  1. Add an OS sandbox launcher (`sandbox-exec` Seatbelt profile on macOS; `bwrap` / userns / `landlock` on Linux) around foreign CLI executions (`codex`, `claude`, `pi`, and untrusted red-first test subprocesses).
  2. Deny reads/writes to `~/.ssh`, `~/.config/cc-routing/`, `.git/`, `.beads/`, `.claude/worktrees/`, and paths outside the scoped attempt tree at the OS kernel boundary, with graceful platform checks and fail-closed strict mode.
* **Acceptance Criteria:** Integration tests attempt reading `~/.ssh`/`.beads/`/`.git/config` from simulated foreign CLIs/test suites inside the sandbox and verify kernel `EPERM`/`EACCES` rejection on macOS and Linux.

### `DRAFT-E7.3` · Add external `TrackerPort` adapters (GitHub Issues & Linear emitting ADR 0004 JSONL)
* **Priority:** `P3` · **Change Class:** `feature` · **P1 slot:** —
* **Audit Refs:** `T-6`, Pillar 1 Layer B
* **Dependencies:** `DRAFT-E5.3`.
* **Scope:**
  1. Generalize `scripts/bead_render.py` into `tracker_render.py` preserving the ADR 0004 JSONL schema contract (`{"id", "status", ...}`).
  2. Implement thin read-only snapshot adapters for `github-issues` and `linear` (configured in `monotrope.yaml`) with offline caching/preflight and matching `check_dangling_bead_ids.py` prefix matching.
* **Acceptance Criteria:** A fixture repository using `tracker.kind: github-issues` resolves `plans-registry` and `dangling-issues` gates via normalized JSONL identically to Beads without installing Dolt.

---

## `DRAFT-E8` (Epic · `P3`) — Observability, Static Safety, & Stage-2 Empirical Evidence Loop

Closes unmeasured operational gaps (`O-3..O-7`, `A-9`, `C-9`) with strict adherence to [`AGENTS.md`](../../AGENTS.md)'s plain-night-run rule (structured logs only — no dashboards or UIs).

### `DRAFT-E8.1` · Add structured OTel GenAI JSONL event log (`coding-harness-oebl`) & hard budget/appetite stops
* **Priority:** `P3` · **Change Class:** `feature` · **P1 slot:** —
* **Audit Refs:** `O-4`, `C-9`, `coding-harness-oebl`, `README.md:252`
* **Dependencies:** `DRAFT-E4.2`.
* **Scope:**
  1. Emit an append-only JSONL telemetry stream (`coding-harness-oebl`) using OpenTelemetry GenAI semantic attributes (stage, model, latency ms, input/output tokens, request count, exit/verdict, route fallback, refusal reason) — strictly plain files, zero dashboards/services.
  2. Enforce hard per-change and per-night-run appetite/request/wall-clock circuit breakers so runaway loops halt cleanly with structured handover summaries.
* **Acceptance Criteria:** `stage2` runs emit schema-validated JSONL events without leaking secrets; exceeding configured request/wall-clock limits aborts safely before dispatching the next round.

### `DRAFT-E8.2` · Build 10–15 historical-bug offline replay benchmark for Stage-2 ROI & `pydantic`/`Jinja2` decision (`A-9`)
* **Priority:** `P3` · **Change Class:** `spike` *(for ROI study + dependency decision)* · **P1 slot:** —
* **Audit Refs:** `O-5`, `C-9`, `A-9`, `README.md:268-276`
* **Dependencies:** `DRAFT-E4.4`.
* **Scope:**
  1. Assemble a reproducible anonymized suite of 10–15 real historical faults cured in `plans/changes/archive/` and measure defect catch rate, false positives, runtime, and request consumption across Stage 1 alone vs. Free swarm vs. Flash swarm vs. Paid ladder.
  2. Resolve `A-9`: benchmark whether migrating core YAML schemas (`model-endpoints.yaml`, `gates.yaml`, `provenance.yaml`, `monotrope.yaml`) to Pydantic yields net simplification or drop unused `pydantic==2.13.5` and `Jinja2==3.1.6` from `pyproject.toml` and `requirements-ci.txt`.
* **Acceptance Criteria:** Written benchmark report under `docs/research/` comparing multi-stage defect yield quantitatively; follow-up decision PR drops unused locks or adopts typed models.

### `DRAFT-E8.3` · Add fast `pyright`/`mypy` `seconds` gate, `hypothesis` parser fuzzing, & `< 3 s` Phase-5 pre-push/stop guard
* **Priority:** `P3` · **Change Class:** `bounded` · **P1 slot:** —
* **Audit Refs:** `O-3`, `O-6`, `O-7` (`docs/testing.md:61`, `AGENTS.md:25`)
* **Dependencies:** `DRAFT-E3.1`, `DRAFT-E4.2`.
* **Scope:**
  1. Configure `pyright` (or `mypy`) strictly over modularized `stage2_*.py` and primitive modules as a `seconds` gate in `decisions/gates.yaml`.
  2. Add bounded `hypothesis` property suites targeting `leakcheck.py`, `stage2_go.url_problem`, `merge_guard.py`, `omnigent_policy.py`, `tools/bd` arg guard, and `_yaml_strict` / Markdown table escaping.
  3. Implement an optional `< 3 s` bounded Phase-5 stop / pre-push guard (`.claude/hooks/session-stop/check-tests-green.sh` or CLI `monotrope quick-check`) running `ruff`, `frontmatter-current`, and fast touched tests on edited Python files (`AGENTS.md:25` / `docs/testing.md:61`).
* **Acceptance Criteria:** Static type check completes `< 4 s` with 0 errors on typed modules; `hypothesis` security suites pass within `< 5 s` under CI determinism seeds; optional quick-check exits cleanly `< 3 s`.

---

## Appendix — Ready-to-review `tools/bd create` draft commands *(unexecuted)*

> [!NOTE]
> Verify live open P1 bead count via `tools/bd list` first (`AGENTS.md`: max **10 non-epic P1 beads** open at once), then create Epics (`-t epic`) first so child tasks can carry `--parent <epic-id>` or `--deps` cleanly, and finish with `tools/bd dolt push`.

### Epics (`DRAFT-E1`..`DRAFT-E8`)

```bash
# P0 Epic
tools/bd create -t epic "Stop the Bleeding: 2026-11-30 Cliff, Data-Governance Leaks, & P0 Security Containment" \
  -d "Class: bounded (coordination epic). Covers 2026-11-30 cliff, C-1 free_stage/prepare-loop leak, C-2/S-1..S-9 trust boundaries, C-3 architectural>=5, O-1 155 worktree cleanup, and A-4 SessionStart perf." -p 0

# P1 Epics (epics do not consume the 10-bead P1 limit)
tools/bd create -t epic "Restore Fast Local Verification & Break the Test Ratchet" \
  -d "Class: bounded (coordination epic). Covers V-7..V-12, R-1..R-6, A-5 parallel Python runner, non-admin ruleset, criterion-ledger redirects, and Sec 9.3 flakiness fixes." -p 1

tools/bd create -t epic "Shared Primitive Foundation & State-First Persistence" \
  -d "Class: architectural (coordination epic). Covers A-2 shared primitives, Sec 9.2 C gate fixes, A-3 loop.state.json state-first rendering, and self-expiring report-gate valves." -p 1

tools/bd create -t epic "Modularize scripts/stage2.py (11,487 LOC) & tests/test_stage2.py (28,466 LOC)" \
  -d "Class: bounded (coordination epic). Covers Sec 5 16-slice acyclic split (Layers 0-4), AttemptEngine (A-7), ADR 0025 unlock, Research Swarm fixes/perf (A-6), and Sec 9.2 A/B bugs." -p 1

tools/bd create -t epic "Kit Consolidation & Greenfield/Brownfield Transferability Foundation" \
  -d "Class: feature (coordination epic). Covers Target-Architecture ADR 0026 promotion, manifest unification (DECKEL=0), monotrope.yaml, tracker=none, ci=additive, validate_change_artefacts.py, dual probe, H6 & D-16." -p 1

# P2 & P3 Epics
tools/bd create -t epic "Onboarding Documentation, README.md, & Entry-Doc Alignment" \
  -d "Class: bounded (coordination epic). Covers Sec 7 README.md rewrite, WORKFLOW.md split, entry/governance doc alignment, and creating 5 missing standard entry files." -p 2

tools/bd create -t epic "Polyglot Toolchains, External Trackers, & OS-Level Process Sandboxing" \
  -d "Class: feature (coordination epic). Covers ToolchainPort (TS/Go/Rust), OS sandboxing (sandbox-exec/bwrap, O-2), and TrackerPort (GitHub Issues/Linear)." -p 3

tools/bd create -t epic "Observability, Static Safety, & Stage-2 Empirical Evidence Loop" \
  -d "Class: feature (coordination epic). Covers OTel JSONL (coding-harness-oebl) + hard stops, 10-15 bug offline Stage-2 ROI benchmark (O-5) + A-9, and pyright/hypothesis/quick-check (O-3/O-6/O-7)." -p 3
```

### Priority `P0` tasks (`DRAFT-E1.1`..`DRAFT-E1.5`)

```bash
tools/bd create "Triage 2026-11-30 calendar cliff & expired role/endpoint dates" \
  -d "Class: bounded. Audit Refs: Cliff warning, A-12, R-4. Re-read DeepSeek terms (model-endpoints.yaml:218), triage 13 ramp_valves/BESTAND_OHNE_ARTEFAKT/provenance role deadlines, retire 2ee-triage skips, log ADR 0025 measurement." -p 0

tools/bd create "Close free_stage unread-terms exfiltration & prepare-loop diff leak" \
  -d "Class: feature. Audit Refs: C-1, S-7. Enforce static diff-free prepare-loop probes, remove suffix -free auto-admission per ADR 0021 decision 3 amendment, add check_overlay() everywhere, disable _fetch_intelligence redirects, fix url_problem & finder isolation." -p 0

tools/bd create "Harden Pi/red-first/hook/permission/leakcheck boundaries & scrub S-9 public leaks" \
  -d "Class: bounded. Audit Refs: C-2, S-1..S-6, S-8, S-9, A-4. Drop --no-extensions in review loop, hash tools/pi/node_modules in tool_state, isolate RED_PROBE via pass_fds, close night.py/settings.local.json/bd hook bypasses, fix SessionStart O(N), scrub S-9 leaks & enforce ADR 0003 CI gate." -p 0

tools/bd create "Set architectural interview minimum to 5, require claimed ADR, & declare needs_history" \
  -d "Class: bounded. Audit Refs: C-3, C-4. Set MINIMUMS['architectural']=5 in check_interview_minimums.py:82, require ADR claim or waiver prospectively, add needs_history: true in decisions/gates.yaml, fix CRLF/OSError parsing." -p 0

tools/bd create "Clean 155 stale worktrees & add safe make prune-worktrees garbage collector" \
  -d "Class: bounded. Audit Refs: O-1, C-2, C-8. Safely prune merged stale .claude/worktrees/ checkouts, add scripts/prune_worktrees.py (--dry-run default) + make prune-worktrees, warn on count threshold in machine_facts.py." -p 0
```

### Priority `P1` tasks (`10 / 10` slots · `DRAFT-E2.1`..`DRAFT-E5.3`)

```bash
# Slot 1/10
tools/bd create "Quick verify speedups: parallel/diff-triggered leerprobe, Makefile .venv, single BEAD_RENDER, worksteal" \
  -d "Class: bounded. Audit Refs: C-4, C-5, V-7, V-10, V-11 (coding-harness-w2ay, 351h). Add -n auto --dist worksteal to pytest/probe.py, local diff trigger for leerprobe, single BEAD_RENDER export, .venv/bin/python3 in Makefile, Event waits instead of sleep, ruleset -k scope." -p 1

# Slot 2/10
tools/bd create "Extend criterion-ledger with superseded_by/retired, adoption.yaml, & expiring transition tests" \
  -d "Class: feature. Audit Refs: C-5, R-1, A-12 (coding-harness-1ga5, wpv). Wire adoption.py into check_criterion_ledger.py, add superseded_by/retired trace redirects and BEAD_RENDER-checked @pytest.mark.transition(until_bead=...) markers." -p 1

# Slot 3/10
tools/bd create "Parallel Python verify runner, content-hashed local verdict cache, & non-admin ruleset handling" \
  -d "Class: feature. Audit Refs: C-4, A-5, V-11, V-12 (coding-harness-43iz, u3qg). Replace verify_all.sh Bash logic with verify_runner.py (ThreadPoolExecutor for seconds gates, in-process duration), add $XDG_STATE_HOME verdict cache & graceful non-admin ruleset skip." -p 1

# Slot 4/10
tools/bd create "Consolidate shared primitives (_yaml_strict, _fs_atomic, _git_exec, _verdict) & fix Sec 9.2 C gate bugs" \
  -d "Class: bounded. Audit Refs: A-2, Sec 9.2 C. Replace 18 frontmatter/7 YAML/6 git/5 atomic writers, route all 12 check_*.py validators via _verdict.py, extend dangling bead check to plans/, and resolve all verified Sec 9.2 C edge-case defects." -p 1

# Slot 5/10
tools/bd create "Replace Markdown loop-state regexes with locked canonical loop.state.json + rendered Markdown" \
  -d "Class: architectural. Audit Refs: C-6, A-3, S-10, Sec 9.2 A. Persist review-loop state atomically in loop.state.json with receipt_lock, deterministically render loop.md & findings.md tables with safe escaping, retire 50+ fragile Markdown state regexes." -p 1

# Slot 6/10
tools/bd create "Extract stage2_support + Layers 0-1 leaf modules (core, secrets, process, artifacts, git)" \
  -d "Class: bounded. Audit Refs: A-1, Sec 5 (PR 0a-5), Sec 9.2 A. Add tests/stage2_support.py & AST acyclicity/ImportFrom guard test; split Layers 0-1 modules + tests in <=800 LOC slices; fix double-import, PGID race, _rule_spans, free_diff, & .nan bugs." -p 1

# Slot 7/10
tools/bd create "Extract stage2 Layers 2-3 modules & remove all 66 runner.* dynamic lookups" \
  -d "Class: bounded. Audit Refs: A-1, A-7, Sec 5 (PR 6-13), Sec 9.2 A. Extract admission, loop_record, worktree, checkpoint, runners, targeted, verify, & repair_proof modules + tests; replace runner.* service locator with typed imports." -p 1

# Slot 8/10
tools/bd create "Promote Target-Architecture & Transferability ADR 0026 draft via Phase 1a + decide PR" \
  -d "Class: architectural. Audit Refs: C-7, C-10, T-1, T-9. Run Phase 1a interview over Q-ARCH-1..5 (Open-Core license split, free allowlist, architectural>=5, tracker=none, ledger redirects) and promote draft ADR to docs/adr/0026 via decision PR." -p 1

# Slot 9/10
tools/bd create "Unify kit/export manifests, remove Databricks agents & hardcoded continuity gate, drive DECKEL 44->0" \
  -d "Class: bounded. Audit Refs: C-7, A-8, T-10, S-10. Retire export/manifest.yaml, fix missing bead_render.py/duplicate ci.yml/orphaned swarm limits, move domain agents & hardcoded Omnigent check_decision_continuity.py out of portable kit, hit DECKEL=0." -p 1

# Slot 10/10
tools/bd create "Ship monotrope.yaml contract, tracker=none, ci=additive, & monotrope init/upgrade/doctor CLI" \
  -d "Class: feature. Audit Refs: T-2, T-3, T-4, T-6, T-7 (coding-harness-dj9, lir). Parameterize prefix/branch/roles across scripts, enable Dolt-free L1 brownfield init & additive CI, scope docs checks to provenance frontmatter:required, add harness.lock.yaml." -p 1
```

### Priority `P2` & `P3` tasks (`DRAFT-E2.4`, `E3.3`, `E4.3`, `E4.4`, `E5.4`, `E5.5`, `E6.1..3`, `E7.1..3`, `E8.1..3`)

```bash
# P2 tasks
tools/bd create "Consolidate duplicate/micro tests (-20-31%), add APFS/in-process fixtures, & fix Sec 9.3 flakes" \
  -d "Class: bounded. Audit Refs: R-2..R-6, V-8, V-9, Sec 9.3. Parametrize micro-tests, demote duplicate E2E logic out of swarm suite, add APFS world templates, batched Node drivers, & in-process stand-in transport seam; fix S-10 & host/xdist flakes." -p 2

tools/bd create "Enforce expiration valves on all report gates & resolve 199 docs-links findings" \
  -d "Class: bounded. Audit Refs: C-4, A-12. Add promote_by/sunset_by validation to ramp_valves.py, split live docs links (blocking) from legacy handover ratchet, and fix active broken anchors such as docs/orchestration.md:29." -p 2

tools/bd create "Finish stage2 Layer 4 (AttemptEngine), unlock ADR 0025 targeted checks, & fix Sec 9.2 B bugs" \
  -d "Class: bounded. Audit Refs: A-1, A-7, Sec 5 (PR 14a-15), Sec 9.2 B (coding-harness-vg9). Unify draft/implement/repair in AttemptEngine, migrate pr_sync RUNNER_HELD check, delete stage2.py:6911 bypass, fix swarm/session/availability/tools.mjs bugs." -p 2

tools/bd create "Optimize Research Swarm: split Run class, commit-cache leakcheck, deterministic stage_merge" \
  -d "Class: bounded. Audit Refs: C-9, A-6. Split 1,497-line Run god class, replace 100 Hz polling & 39-90x full leakcheck scans with commit cache, replace Opus stage_merge LLM call with deterministic Python merge." -p 2

tools/bd create "Ship validate_change_artefacts.py (jc3) & dual greenfield/brownfield continuous probe.py" \
  -d "Class: feature. Audit Refs: C-7, T-10 (coding-harness-jc3). Deliver validate_change_artefacts.py gate for [DECISION]/[AMBIGUITY] checks and run probe.py --strict (DECKEL=0) over both clean greenfield and non-Python brownfield fixtures." -p 2

tools/bd create "Subpackage touch_map/test_ci awareness, harness-neutral hooks (H6), cross-platform sessions & D-16" \
  -d "Class: feature. Audit Refs: A-10, A-11, T-8, T-9. Enable dotted/relative imports in touch_map/test_ci, decouple Claude shell hooks + H6 deletion test, replace macOS osascript, generate CLAUDE.md/Cursor/Copilot shims, add D-16 routing & branch leakcheck." -p 2

tools/bd create "Rewrite README.md for 3-minute clarity, external cloners, & honest L0-L3 status" \
  -d "Class: bounded. Audit Refs: Sec 7.1. Reconcile repair/ADR 0023/0025 docs, pathlock/recap security caveats, external cloner instructions (--ci, checksums, .venv, XDG_STATE_HOME), broken L164 anchor, L0-L3 funnel, and unified status cut-off." -p 2

tools/bd create "Refactor WORKFLOW.md (2,213 LOC) & align AGENTS.md, how-it-works, testing, & orchestration" \
  -d "Class: bounded. Audit Refs: Sec 7.2. Split WORKFLOW.md into core doctrine + Stage-2/ops reference, purge phantom hooks & internal contradictions across all five core onboarding documents." -p 2

tools/bd create "Create 5 missing standard entry files & align governance/tool READMEs & indices" \
  -d "Class: bounded. Audit Refs: Sec 7.2 (coding-harness-yim). Author docs/_INDEX.md, docs/onboarding.md, CONTRIBUTING.md, SECURITY.md, docs/adr/_INDEX.md; triage ROADMAP.md; update COMMERCIAL.md/tool READMEs/indices; translate regelwerk/quality-gates in own decision PR." -p 2

# P3 tasks
tools/bd create "Implement polyglot ToolchainPort (Python, TS/JS, Go, Rust via JSON/JUnit/TAP)" \
  -d "Class: feature. Audit Refs: T-5, ADR 0026 draft Pillar 1. Generalize gates tools setup, pluggable criterion-ledger test discovery, and red-first/targeted runner outputs across non-Python test ecosystems." -p 3

tools/bd create "Enforce OS-level sandboxing (sandbox-exec/bwrap) & out-of-process red-first proofs" \
  -d "Class: feature. Audit Refs: O-2, C-2, S-2, ADR 0026 draft Pillar 3. Wrap foreign CLIs and untrusted red-first suites in Seatbelt/Bubblewrap denying ~/.ssh, ~/.config/cc-routing, .git/, .beads/, and worktrees outside attempt root." -p 3

tools/bd create "Add TrackerPort adapters for GitHub Issues & Linear emitting ADR 0004 JSONL" \
  -d "Class: feature. Audit Refs: T-6, ADR 0026 draft Pillar 1. Generalize bead_render.py into tracker_render.py supporting normalized external issue snapshots for teams without Dolt/Beads." -p 3

tools/bd create "Emit OTel GenAI JSONL event log (oebl) & enforce hard budget/appetite circuit breakers" \
  -d "Class: feature. Audit Refs: O-4, C-9 (coding-harness-oebl). Append schema-validated plain JSONL model telemetry per call (no UI dashboard) and enforce hard request/time circuit breakers." -p 3

tools/bd create "Build 10-15 historical-bug offline benchmark for Stage-2 ROI & resolve pydantic/Jinja2 lock (A-9)" \
  -d "Class: spike. Audit Refs: O-5, C-9, A-9. Measure actual defect yield vs runtime/cost of Free/Flash/Paid swarms against archived bugs and decide whether to adopt Pydantic schemas or drop unused pydantic/Jinja2 deps." -p 3

tools/bd create "Add fast pyright/mypy seconds gate, hypothesis parser fuzzing, & <3s Phase-5 pre-push guard" \
  -d "Class: bounded. Audit Refs: O-3, O-6, O-7. Gate typed Stage-2/core modules statically, fuzz leakcheck/URL/merge_guard/YAML/bd parsers with hypothesis, and ship optional <3s local pre-push guard." -p 3
```
