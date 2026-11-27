---
title: "Plan — bd-trust-check"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
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
Done when:   Marker tests cover all three paths, trusted and fallback behavior, blank lines, and make verify is green.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Changing Antigravity trust or granting code execution through the handover content list.
Pre-mortem:  suppose it failed: most likely because an indirect start-hook call still reaches the local wrapper.
Starts unless you say stop.
```

## Build sequence

1. Add `tools/claude-code/hooks/tracker-trust.sh` as the single trust and executable-selection helper: compare the Git origin literally against nonblank lines of `${XDG_CONFIG_HOME:-$HOME/.config}/coding-harness/trusted-repositories`; reject missing or unreadable list or origin. Resolve `bd` from `PATH` to an executable outside the repository, rejecting relative or symlink paths that resolve inside it. Fail closed if the helper is unavailable. The repository start hook uses its sibling helper; installed scripts use the installed helper, never a helper from the repository being displayed.
2. In `tools/claude-code/statusline.sh` and `tools/claude-code/hooks/handover.sh`, use the helper before selecting the wrapper or fallback; retain caching and timeout behavior. In `tools/claude-code/hooks/beads-start.sh`, skip reconciliation when untrusted, then run prime through the same selection or report it unavailable; keep existing writer and timeout checks for trusted repositories.
3. In `tools/claude-code/hooks/handover.sh`, ignore blank lines when matching the separate `HANDOVER_TRUST` content list while preserving its nonblank extended regular expressions. Add the helper to `tools/claude-code/install.sh` and document both trust lists and setup in `tools/claude-code/README.md`.
4. Extend `tests/test_beads_start.py` and `tests/test_handover_entry.py`, and add `tests/test_tracker_trust.py`; exercise actual scripts with isolated repositories, marker wrappers, trusted and untrusted origins, missing dependencies, symlink and relative PATH fallbacks, and isolated caches. Update the existing start fixtures to grant trust explicitly where they test reconciliation. No files are deleted; this bounded change has no design or ADR.
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
- 3: not yet written tests/test_tracker_trust.py::test_untrusted_external_fallback_or_skip — external fallback fails to run or local code runs when unavailable.
- 4: not yet written tests/test_tracker_trust.py::test_missing_trust_inputs_fail_closed — an absent, unreadable or blank list or missing origin authorizes execution.
- 5: not yet written tests/test_tracker_trust.py::test_origin_matching_is_literal_and_exact — a partial or regex match grants trust.
- 6: not yet written tests/test_handover_entry.py::test_blank_trust_patterns_do_not_authorize — blank lines expose untrusted content or a matching pattern is rejected.
- 7: not yet written tests/test_tracker_trust.py::test_installed_helper_and_missing_helper — installation omits the helper or absence grants trust.

## Explore fallback

On 2026-11-27 explore used the Stage-1 route, `claude-haiku-5-5`, because GLM through Z.ai had reached its weekly limit until 2026-11-29 (`research.md`).

## Time used

2026-11-27 21:12:54–21:15:06 UTC, 131 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
