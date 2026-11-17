---
title: "Plan — pi-neutral-paths"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-11-16
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-xul8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-terra, 2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, pi, privacy]
---

# Plan — pi-neutral-paths

```text
For you:     Pi model calls stop exposing local machine locations and the session excludes outside context files while keeping repository instructions.
Done when:   Offline captures show neutral paths, exclude outside context, retain repository instructions, and prove a surviving home or worktree path stops delivery; make verify is green.
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
2. Add one import-independent ESM extension using the pinned Pi 1.5.0
   `before_agent_start` hook: set the prompt cwd to `.` and remove the docs
   section while preserving the remaining prompt. Neutralize known local
   prefixes in the outgoing payload without modifying the local transcript,
   tool arguments or repository-relative references. In the provider-request
   hook, fail closed before delivery if a home or worktree path survives in
   the rendered prompt. Exercise both the initial request and later turns;
   verify the hook's actual failure behavior with the pinned Pi.
3. Copy the extension to each launch's existing scratch/private directory and
   explicitly load it alongside role-specific extensions. Fail preparation if
   the source cannot be copied. Preserve the actual cwd, admission, tool permissions and existing role extensions. For the session,
   filter Pi's context-file options to paths whose canonical resolved target
   is inside the repository; refuse if the boundary cannot be established.
   Keep in-repository context, including the root instructions, available.
   Apply the filter on every run, including reloads and subsequent turns.
4. Wire all builders, including the review builder in `scripts/stage2.py`;
   reconcile with its current contents and preserve existing changes.
5. Capture each production builder's command at the existing dispatch seam,
   changing only test transport/model configuration to reach loopback. For
   the interactive command, use a test-only RPC adapter after capturing its
   argv, keeping all production extension/context/tool flags; submit two user
   turns and script a tool-result/error round trip. Assert allowed relative
   reads still return their sentinel, forbidden outside/symlink reads remain
   blocked, and unrelated instructions/tools survive. Plant distinct parent,
   global, symlink-escape and repository context canaries; inspect their paths
   and content in complete requests across repeated turns, with a control
   proving outside discovery would otherwise reach the provider. Do not open
   Terminal or contact a hosted provider. Promote `not yet written` ledger entries when
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
- Change `scripts/stage2.py`: install/load it in
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
  copies while retaining policy confirmation, repository context and real cwd;
  replace the assertion that unrestricted context discovery stays on.
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

- 7: tests/test_pi_contract.py::test_surviving_prompt_path_blocks_delivery — a planted home or worktree path reaches the provider or the launch succeeds
- 8: tests/test_pi_contract.py::test_session_excludes_outside_context_files — a parent, global or symlink-escaped context path or content reaches the provider
- 9: tests/test_pi_contract.py::test_session_retains_repository_context_files — repository instruction content is absent from the request

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
governance, non-context discovery flags and non-Pi transports untouched.
Exploration used Stage 2, GLM 5.3 Flash on 2026-10-29; no Stage-1 fallback was recorded.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent in
this worktree at draft time; use the phase-3 prompt's form and the available
interview, handoff and criterion-ledger checks. The runner owns generated
index updates and the final `make verify` gate.

## Runner route — 2026-11-16

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM Flash attempts 1 and 2 failed their post-run checks; Sonnet continues from the saved attempt (night run 2026-11-16-a).

## Runner route — 2026-11-16

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM Flash attempts 1 and 2 failed their post-run checks; the first Sonnet call was cut off by a session restart (night run 2026-11-16-a).

## Time used

2026-10-30 22:28:29–23:27:54 UTC, 3564 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-30 23:28:00–23:33:27 UTC, 327 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-30 23:33:33–23:37:17 UTC, 225 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-31 about 16:55–18:05 UTC, about 4200 s — hand reading of the red tests by the orchestrator (maintainer's choice of 2026-10-31, "Rote Tests lesen"), five stale tests repaired, targeted checks green; measured from the session's own timestamps, not by the runner

Appetite: 2 hours of phase 4. Used by 2026-10-31 18:05 UTC: about 8300 s (2 h 18 min) — over the stop by about 18 minutes. The hand reading was owed 51 minutes and took about 70; the overrun is recorded here, and continuing past it is the maintainer's call.
2026-10-31 19:35:29–22:39:29 UTC, 11038 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 22:39:35–23:09:19 UTC, 1783 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 23:09:27–2026-11-01 00:02:23 UTC, 3175 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-01 07:36:46–07:53:57 UTC, 1031 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-01 07:54:04–08:21:03 UTC, 1620 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-01 08:21:10–08:34:36 UTC, 806 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-01 08:56:33–09:30:02 UTC, 2009 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-01 09:30:09–10:10:17 UTC, 2408 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-01 10:10:24–10:50:39 UTC, 2416 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-16 14:20:59–14:22:48 UTC, 109 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 14:25:12–14:27:11 UTC, 119 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 22:58:06–23:08:52 UTC, 645 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
