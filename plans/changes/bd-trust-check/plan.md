---
title: "Plan — bd-trust-check"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, security, tracker]
---

# Plan — bd-trust-check

```text
For you:     Opening an untrusted repository no longer runs its tracker wrapper through the status line or the two hooks.
Done when:   Marker tests cover all three paths, trusted, untrusted (no bd at all) and wrapper-less behavior, blank lines, the cache order, the reports, and make verify is green.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Changing Antigravity trust or granting code execution through the handover content list.
Pre-mortem:  suppose it failed: most likely because an indirect start-hook call still reaches the local wrapper.
Starts unless you say stop.
```

## Build sequence

1. Add `tools/claude-code/hooks/tracker-trust.sh` as the single trust and executable-selection helper: decide whether the tracker root holds an executable `tools/bd` (a wrapper repository); for a wrapper repository compare the Git origin literally against the entries (trimmed, blank and `#` lines skipped) of `${XDG_CONFIG_HOME:-$HOME/.config}/coding-harness/trusted-repositories`; reject a missing or unreadable list or origin. An untrusted wrapper repository selects no `bd` at all; a wrapper-less repository keeps the `bd` on `PATH` as today. Fail closed (untrusted plus one warning) if the helper is unavailable. The repository start hook uses its sibling helper; installed scripts use the installed helper, never a helper from the repository being displayed.
2. In `tools/claude-code/statusline.sh` and `tools/claude-code/hooks/handover.sh`, use the helper before reading the beads cache and before selecting a `bd`; show `bd: not trusted` or `bd: trust check unavailable` for an untrusted wrapper repository; retain caching and timeout behavior otherwise. In `tools/claude-code/hooks/beads-start.sh`, skip reconciliation and prime for an untrusted wrapper repository with one stderr line and exit 0; keep existing writer and timeout checks for trusted repositories.
3. In `tools/claude-code/hooks/handover.sh`, ignore blank lines when matching the separate `HANDOVER_TRUST` content list while preserving its nonblank extended regular expressions. Add the helper to `tools/claude-code/install.sh` and document both trust lists and setup in `tools/claude-code/README.md`.
4. Extend `tests/test_beads_start.py` and `tests/test_handover_entry.py`, and add `tests/test_tracker_trust.py`; exercise actual scripts with isolated repositories, marker wrappers, trusted and untrusted origins, missing dependencies, a recording `bd` on `PATH` that must stay uncalled, wrapper-less repositories, and isolated caches. Update the existing start fixtures to grant trust explicitly where they test reconciliation. No files are deleted; this bounded change has no design or ADR.
5. Update this plan's ledger markers when tests exist; the runner records findings, elapsed time and regenerates the plans index. An orchestrator reinstalls the display from the repository after acceptance; installed user files are not committed.

## Files and limits

- `tools/claude-code/hooks/tracker-trust.sh`: new shared trust and executable selector.
- `tools/claude-code/statusline.sh`: apply selection to background refresh.
- `tools/claude-code/hooks/handover.sh`: apply selection and ignore blank content-trust patterns.
- `tools/claude-code/hooks/beads-start.sh`: gate indirect reconciliation and select prime executable.
- `tools/claude-code/install.sh`: install and check the helper.
- `tools/claude-code/README.md`: explain trust setup and changed behavior.
- `tests/test_tracker_trust.py`: exercise trust, selection, status line and installation.
- `tests/test_beads_start.py`: exercise start behavior and update trusted fixtures.
- `tests/test_handover_entry.py`: exercise handover behavior and blank patterns.
- `plans/changes/bd-trust-check/plan.md`: update ledger and phase-4 time.
- `plans/changes/bd-trust-check/findings.md` and `plans/INDEX.md`: runner records review evidence and regenerates the index.

Do not edit `.agents/hooks/session-start.sh`, workspace trust settings, the tracker, or the handover content trust format beyond blank-line handling. No held path needs an implementation edit.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_tracker_trust.py tests/test_beads_start.py tests/test_handover_entry.py
python3 scripts/jobs.py start -- make verify
```

Inspect the detached verification job's exit before phase 6.

## Criterion ledger

- 1: not yet written tests/test_tracker_trust.py::test_untrusted_paths_never_run_local_wrapper — any of the three paths writes the marker, including reconciliation.
- 2: not yet written tests/test_tracker_trust.py::test_trusted_paths_use_local_wrapper — any expected invocation is missing.
- 1: not yet written tests/test_tracker_trust.py::test_untrusted_wrapper_repository_runs_no_path_bd — a recording bd on PATH is called for an untrusted wrapper repository.
- 3: not yet written tests/test_tracker_trust.py::test_wrapperless_repository_keeps_todays_behavior — a repository without tools/bd shows bd: not trusted or loses its beads line.
- 8: not yet written tests/test_tracker_trust.py::test_trust_skip_reports_once_per_path — a skip is shown as a timeout, hides silently, repeats, or the start hook exits non-zero.
- 9: not yet written tests/test_tracker_trust.py::test_trust_decided_before_cache_read — a pre-written cache of an untrusted wrapper repository is shown or injected.
- 4: not yet written tests/test_tracker_trust.py::test_missing_trust_inputs_fail_closed — an absent, unreadable or blank list or missing origin authorizes execution.
- 5: not yet written tests/test_tracker_trust.py::test_origin_matching_is_literal_and_exact — a partial or regex match grants trust.
- 6: not yet written tests/test_handover_entry.py::test_blank_trust_patterns_do_not_authorize — blank lines expose untrusted content or a matching pattern is rejected.
- 7: not yet written tests/test_tracker_trust.py::test_installed_helper_and_missing_helper — installation omits the helper or absence grants trust.

## Explore fallback

On 2026-11-27 explore used the Stage-1 route, `claude-haiku-5-5`, because GLM through Z.ai had reached its weekly limit until 2026-11-29 (`research.md`).

## Time used

2026-11-27 21:12:54–21:15:06 UTC, 131 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
