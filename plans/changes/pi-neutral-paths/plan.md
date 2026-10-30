---
title: "Plan — pi-neutral-paths"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-xul8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, pi, privacy]
---

# Plan — pi-neutral-paths

```text
For you:     Pi model calls stop exposing local machine locations while repository tools keep their working directory.
Done when:   Offline captures for every Pi launch shape contain no local location identifiers and make verify is green.
Appetite:    2 hours of phase 4, repairs included; stop at the limit.
Not now:     Claude Code/Codex transports, Pi upgrades, model policy or moving the checkout/install.
Pre-mortem:  suppose it failed: most likely because a later request reintroduces a local path through tool or project context.
Starts unless you say stop.
```

## Implementation

1. Write the ledger's failing tests first, using the installed pinned Pi and
   the existing loopback `StandIn`, network guard and synthetic credentials.
   Use distinct synthetic HOME, checkout/worktree and scratch canaries plus
   the actual pinned-install prefix; do not move the install. Make the
   worktree name distinct from logical task names. Check serialized
   **whole** request bodies, not `message_text` or prompt excerpts alone.
   An extension-omitted control must expose the original cwd/docs leak.
2. Add one import-independent ESM extension. In `before_agent_start`, set
   `event.systemPromptOptions.cwd = "."`, then return the rendered
   `event.systemPrompt` with only its `<docs>…</docs>` block removed. Pi's
   getter renders the mutated options; returning `systemPrompt` is the
   supported full-prompt override. Do not set `customPrompt` to just the
   preamble: Pi 1.2.0 would omit the generated tools/rules too.
   Remove remaining location metadata from a copy of the outgoing payload
   through `before_provider_request` so context labels and tool errors/results
   cannot restore the leak; match known local path prefixes, longest first,
   including native and slash-normalized forms. Preserve relative references,
   protocol structure, and the local transcript/tool arguments; do not blindly
   replace a basename inside a repository-relative file reference. Verify
   this against the canaries rather than adding a general content filter.
3. Copy that source into each launch's existing scratch/private directory as
   `neutral-paths.mjs` and add explicit `-e <copy>` after the existing role
   extensions, with discovery still disabled. Missing/unreadable source fails
   launch preparation before dispatch. Research repository seats retain the
   path lock; public/free research retains public tools; the session retains
   its policy and project context. Reuse the same source in all four builders;
   keep actual cwd, environment, prompt inputs, admission and dispatch intact.
4. Complete independent builders/tests first. **Before editing
   `scripts/stage2.py`, obtain lane A's merge/release from the orchestrator**
   and reconcile with its merged version; the absence of a local edit is not
   evidence of release. Then wire the review builder for free, Flash and
   ladder members. If release has not arrived, report that remaining blocker.
5. Capture each production builder's command at the existing dispatch seam,
   changing only test transport/model configuration to reach loopback. For
   the interactive command, use a test-only RPC adapter after capturing its
   argv, keeping all production extension/context/tool flags; submit two user
   turns and script a tool-result/error round trip. Assert allowed relative
   reads still return their sentinel, forbidden outside/symlink reads remain
   blocked, and unrelated instructions/tools survive. Do not open Terminal or
   contact a hosted provider. Promote `not yet written` ledger entries when
   each top-level test exists, record evidence, then run the verification.

## Files

- Create `scripts/stage2_pi_neutral_paths.mjs`: the shared prompt/payload
  neutralization extension, with pure helpers for deterministic checks.
- Change `scripts/stage2_research_run.py`: install/load the extension in
  `Run.pi_command` for repository and public/free research seats.
- Change `scripts/stage2_availability.py`: install/load it for Pi research
  and review availability probes.
- Change `scripts/stage2_session.py`: copy it into the protected private
  session directory and load it alongside the existing session policy.
- Change `scripts/stage2.py`: after lane A releases it, install/load it in
  `run_go_reviewer` for every free and paid reviewer.
- Change `tests/test_pi_contract.py`: add the ledger's production-builder
  request captures and repeat-turn/tool/boundary/negative controls, reusing
  the existing stand-in and network guard.
- Change `tests/test_stage2.py`: adjust exact reviewer argv expectations and
  add coverage that free, Flash and ladder commands load the extension.
- Change `tests/test_stage2_swarm.py`: assert repository/public/free command
  combinations retain their existing extensions and real cwd.
- Change `tests/test_stage2_availability.py`: assert review probes load the
  extension while remaining tool-free and scratch-based.
- Change `tests/test_stage2_research_availability.py`: assert the same for
  research probes without changing their fixed input or admission.
- Change `tests/test_stage2_session.py`: assert the session loads both private
  copies while retaining policy confirmation, context files and real cwd.
- Update `plans/changes/pi-neutral-paths/plan.md` ledger references and
  `plans/changes/pi-neutral-paths/findings.md` evidence as implementation and
  review progress; the runner alone writes time entries. No files are deleted.

## Criterion ledger

- 1: tests/test_stage2.py::test_all_review_members_load_neutral_paths — a free, Flash or ladder command omits the extension
- 1: tests/test_stage2_swarm.py::test_research_seats_load_neutral_paths — a repository/public/free command omits it or loses its role extension
- 1: tests/test_stage2_availability.py::test_review_probes_load_neutral_paths — a review probe omits it
- 1: tests/test_stage2_research_availability.py::test_research_probes_load_neutral_paths — a research probe omits it
- 1: tests/test_stage2_session.py::test_pi_session_loads_neutral_paths_with_policy — a session omits either extension
- 2: tests/test_pi_contract.py::test_real_pi_neutral_cwd_on_every_run — the initial or subsequent run exposes its real cwd
- 3: tests/test_pi_contract.py::test_real_pi_omits_local_docs — the installed Pi still sends its docs section or installation paths
- 4: tests/test_pi_contract.py::test_real_launch_payloads_have_no_local_identifiers — any complete initial/tool/error/repeated-turn request contains a planted location identifier
- 5: tests/test_pi_contract.py::test_real_neutralization_preserves_tool_roots_and_boundaries — allowed relative reads fail or outside/symlink reads succeed
- 6: tests/test_pi_contract.py::test_real_neutralization_preserves_instructions_and_tools — non-location instructions, tool declarations or relative references change

## Verification

```sh
python3 scripts/check_interview_minimums.py --change pi-neutral-paths
python3 scripts/check_research_handoff.py --change pi-neutral-paths
python3 scripts/check_criterion_ledger.py
.venv/bin/python3 -m pytest tests/test_pi_contract.py tests/test_stage2.py tests/test_stage2_swarm.py tests/test_stage2_availability.py tests/test_stage2_research_availability.py tests/test_stage2_session.py -q
make verify
```

The full run belongs to the orchestrator/runner and runs once the focused
checks pass; it must not overlap another full verification on this machine.
This drafting call does not implement code, commit or run the full suite.

## Boundaries and provenance

No design document or ADR is due for class `bounded`. Leave the Pi pin/wrapper,
path-lock and session-policy enforcement, capture storage, model declarations,
governance, discovery flags and non-Pi transports untouched. Exploration used
Stage 2, GLM 5.3 Flash on 2026-10-29; no Stage-1 fallback was recorded.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent in
this worktree at draft time; use the phase-3 prompt's form and the available
interview, handoff and criterion-ledger checks. The runner owns generated
index updates and the final `make verify` gate.

## Runner route — 2026-10-31

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-30 22:28:29–23:27:54 UTC, 3564 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-30 23:28:00–23:33:27 UTC, 327 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-30 23:33:33–23:37:17 UTC, 225 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
