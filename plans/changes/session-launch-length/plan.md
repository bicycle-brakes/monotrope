---
title: "Plan — session-launch-length"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-rm8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, session]
---

# Plan — session-launch-length

```text
For you:     Long checked handovers reach Codex and Pi intact through a short Terminal command.
Done when:   A terminal-input stand-in executes the short command and records the complete boundary-size prompt for both CLIs; the criterion ledger and make verify pass.
Appetite:    2 h of phase 4 including repair; stop at the limit.
Not now:     CLI startup detection, VS Code transport, unrelated unexecuted input, or live model qualification.
Pre-mortem:  suppose it failed: most likely because tests inspect the launcher text without executing the dispatched command.
Starts unless you say stop.
```

Implements `spec.md` at baseline `da2e7cd0` (2026-11-07), class `bounded`;
no design or ADR is due. Explore used Stage 2 route `flash`, endpoint
`glm-coding-plan`, model `glm-5.3-flash` on 2026-11-07; no Stage-1 fallback
was recorded. The interview's answered skip permits this transport repair.

## Steps and files

1. **Implementer: `scripts/stage2_session.py`.** Add a fixed launcher name
   `terminal-session.sh` and a 1,024-byte terminal-input budget. Keep
   `cli_argv` and the quoting in `terminal_command`: write its existing
   `cd ... && exec /usr/bin/env -i ... <argv>` body into the launcher instead
   of sending it through Terminal. Use `/bin/sh <quoted absolute launcher>`
   as the short dispatched command; preserve interactive stdin, with no
   command substitution or prompt-file argument sent to either CLI.
   Create each fresh attempt directory with mode 0700 before writing any
   content and the launcher with mode 0600, independent of umask. Keep the
   existing 32 KiB prompt check and 64 KiB full-command bound; add the short
   command's UTF-8 byte and CR/LF checks before dispatch, with exit-2 reasons.
   Prepare the launcher before the second `checked_prompt` call so that scan
   remains immediately before audit/dispatch; it checks the exact same prompt
   passed to `cli_argv`. Keep Go binding and `dispatch_go` around the send.
   Put all new writes inside attempt cleanup handling: preparation/write/bound
   failures refuse and clean up, dispatch failures clean up and audit failure,
   accepted attempts retain files even if final audit updating fails.
   Update the module description to state that the launcher contains the
   checked prompt but no copied credentials.
2. **Implementer: `tests/test_stage2_session.py`.** Extend the osascript
   stand-in with a 1,024-byte input ceiling that drops excess input before
   shell execution; use it in the new transport tests, never a real window.
   Parameterize Codex/Pi with normal, exactly 32,768-byte assembled UTF-8 and
   multibyte/quote/newline-heavy prompts; record actual CLI argv and its tail
   sentinel after executing the short command. The positive boundary test
   must go red with the old inline-prompt dispatch. Test NUL, 32,769 bytes,
   oversized short paths and line-breaking launch paths before dispatch.
   Inject launcher-write failure and run under a permissive umask to check
   owner-only modes, failure cleanup and accepted retention. Adapt existing
   assertions that parse inline argv or expect only the AppleScript file:
   read the launcher for construction checks, keep recorded CLI argv as the
   behavioral oracle. Extend hostile-value coverage to allowed environment
   values and quoted worktree paths; confirm sentinels never execute.
   Preserve audit, second-scan, flags, credentials and policy regression tests.
3. **Implementer: `docs/WORKFLOW.md`.** In “The interactive session”, describe
   the short 1,024-byte Terminal input, unchanged 32 KiB prompt and 64 KiB
   full-command ceilings, prompt-bearing private launcher and retained-file
   lifecycle. Replace “no prompt” for launch files; retain dispatch-only
   acceptance, credential handling and launch-only leak-check wording.
4. **Implementer: this `plan.md`.** Convert each new ledger entry to a test
   entry when defined and record measured phase-4 time below. Change
   `spec.md`'s and `plan.md`'s implementation status only as work advances.
   The runner/orchestrator regenerates `plans/INDEX.md` after header changes
   and owns verification, commit and any held-path bootstrap edits; none are
   required for this implementation. Run the verification commands below.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2_session.py tests/test_stage2_go_access.py tests/test_stage2_session_policy.py tests/test_run_report.py tests/test_pi_contract.py -q
.venv/bin/python scripts/check_interview_minimums.py --change session-launch-length
.venv/bin/python scripts/check_criterion_ledger.py
make verify
```

The runner runs the final `make verify` and commit. No live CLI/model or macOS
window is needed. `scripts/validate_change_artefacts.py` and a plan template
are absent at this baseline; use the phase-3 prompt's form and existing gates.

## Criterion ledger

- 1: not yet written tests/test_stage2_session.py::test_long_prompts_use_a_bounded_terminal_command — inline payload exceeds the stand-in's input ceiling or changes command length.
- 2: not yet written tests/test_stage2_session.py::test_boundary_prompts_reach_both_interactive_clis_intact — shell execution loses the final sentinel or changes one argument byte.
- 3: not yet written tests/test_stage2_session.py::test_invalid_prompt_or_launch_line_refuses_before_dispatch — NUL, byte overflow or line-breaking launch path reaches osascript.
- 4: tests/test_stage2_session.py::test_hostile_prompt_text_stays_data — prompt shell syntax executes a planted sentinel.
- 4: not yet written tests/test_stage2_session.py::test_launcher_paths_and_environment_stay_data — quoted path or environment value executes shell syntax or changes value.
- 5: not yet written tests/test_stage2_session.py::test_prompt_launcher_is_private_and_follows_attempt_lifecycle — permissive umask exposes content, failed write dispatches, or cleanup touches siblings.
- 5: tests/test_stage2_session.py::test_a_failed_terminal_dispatch_is_recorded_and_cleaned — a rejected dispatch leaves the attempt directory.
- 6: tests/test_stage2_session.py::test_the_second_scan_catches_what_arrived_after_the_first — second-scan leak still dispatches.
- 6: tests/test_stage2_session.py::test_codex_is_dispatched_interactively_with_its_exact_safety_flags — argv, worktree or safety flags change.
- 6: tests/test_stage2_session.py::test_pi_is_dispatched_interactively_with_the_policy_extension — policy or interactive discovery flags disappear.
- 6: tests/test_stage2_session.py::test_the_pi_session_hands_over_no_key_and_writes_no_credential — caller credentials reach the launcher or CLI environment.
- 6: tests/test_stage2_go_access.py::test_the_session_binds_the_checked_model_without_reading_auth — the launcher bypasses the assessed model binding.
- 7: tests/test_stage2_session.py::test_the_audit_names_the_attempt_and_keeps_prior_findings — transport changes erase the audit or its facts.
- 7: tests/test_stage2_session.py::test_a_failed_terminal_dispatch_is_recorded_and_cleaned — rejected Terminal dispatch returns success or records acceptance.
- 7: tests/test_stage2_session.py::test_codex_is_dispatched_interactively_with_its_exact_safety_flags — accepted stand-in dispatch fails the existing exit-0 contract.
- 8: not yet written tests/test_stage2_session.py::test_session_transport_documentation_matches_private_launcher — workflow/module still promise no stored prompt or CLI-start acknowledgement.

## Not touched

`scripts/stage2.py`, `scripts/stage2_session_policy.mjs`, `tests/test_stage2_go_access.py`,
`tests/test_pi_contract.py`, `tests/test_run_report.py`, neighbouring change specs,
endpoint declarations, ADRs, held configuration, prompts and templates stay
unchanged; existing Go/Pi/audit tests verify the shared route without edits.
No new production script or CI caller is introduced: the launcher is per-attempt
runtime data invoked through the already-covered session entry point.

## Time used
