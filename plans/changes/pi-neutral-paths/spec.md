---
title: "Spec — pi-neutral-paths"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-xul8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, pi, privacy]
class: bounded
appetite: 2
adr_files: []
neighbours: [plans/changes/research-swarm/spec.md, plans/changes/pi-pin/spec.md, plans/changes/stage2-session/spec.md]
---

# Spec — pi-neutral-paths

Every Pi launch with model contact keeps machine-local location identifiers
out of the outgoing request without moving its tools' working directory
(bead coding-harness-xul8 — neutral paths in Pi requests). Research:
`research.md`; scope and mechanism: `decisions.md`, Q-1 and Q-2.

## Problem

As read on 2026-10-29, Pi 1.2.0 adds the process working directory and its
installation's absolute documentation paths to its system prompt. Disabling
context discovery does not suppress either section. Repository seats and paid
reviewers expose the checkout path; scratch-based online seats, free
reviewers and probes still expose local scratch and installation paths
(`research.md`, "What exists today").

The leak check examines the runner's prompt before Pi adds these sections,
so its clean result does not establish that the outgoing request is free of
local paths. The same mechanism affects research, reviews, availability
probes and interactive Pi sessions. Moving the actual working directory
would disturb repository tools and the research read boundary
(`research.md`, "What is unclear about it" and the 2026-10-29 addendum).

## Terms

- **Local location identifiers:** the launch machine's home-directory path,
  checkout/worktree path and identifying worktree name, scratch-directory
  path, and Pi-installation path; neutral values and repository-relative
  file references are not local absolute locations.
- **Complete outgoing payload:** the provider request body, including every
  system/user/assistant message, tool declaration and tool result; checking
  only the runner's input prompt does not measure it.
- **Covered launches:** Pi research repository/public/free seats, review-loop
  free/Flash/ladder members, availability probes for research and reviews,
  and the interactive Pi session transport.

## Acceptance criteria

1. When a covered launch starts Pi with model contact, it explicitly loads
   the same repository-owned neutral-path extension alongside its existing
   role-specific extensions.
   *Refuted by:* any covered command lacks that extension, or replacing it
   drops the research path lock, public tools or session policy.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.

2. When Pi prepares a run, the working-directory section visible to the
   model contains the fixed neutral value `.`.
   *Refuted by:* the first or a later run exposes the process working
   directory instead of `.`.
   *Basis:* decisions.md#Q-2.

3. When Pi prepares a run, the model-visible system prompt omits Pi's
   installation-documentation section.
   *Refuted by:* a `<docs>` section or its machine-local documentation
   locations remains in a captured request.
   *Basis:* decisions.md#Q-2.

4. While a covered Pi conversation sends requests, every complete outgoing
   payload is free of local location identifiers.
   *Refuted by:* an identifier appears anywhere in the first request, a
   follow-up request after a tool result or error, or a subsequent user turn;
   planted identifiers in context labels and tool-result metadata count too.
   *Basis:* decisions.md#Q-2; decisions.md, "Decided by the agent" (whole
   outgoing payload).

5. When a covered launch executes a file tool, its working-directory and
   access-boundary behavior remains the same as before neutralization.
   *Refuted by:* a relative in-worktree read fails or resolves elsewhere,
   the process working directory moves, a research path lock admits an
   outside/symlink escape, or the session policy loses its existing boundary.
   *Basis:* decisions.md#Q-2.

6. When neutralization changes a request, it preserves the non-location
   instructions and tool declarations supplied by Pi and the launch role.
   *Refuted by:* neutralization removes or changes the preamble, tool
   descriptions/rules, appended task, public custom tools or session project
   instructions beyond removing local location identifiers, or corrupts a
   repository-relative file reference.
   *Basis:* decisions.md#Q-2.

## Non-goals

- Changing Claude Code or Codex transports, including GLM explore/implement
  calls and Claude Code research roles.
- Changing model admission, selection, availability receipts, review order,
  credentials, leak-check rules or research-capture storage.
- Changing Pi's version, install location, wrapper, real working directory,
  tool permissions or discovery settings; catalog/version/help operations
  without model contact need no neutralization.
- Providing a general content/secret filter or an operating-system sandbox.
- Design phase 2b and an ADR draft: this is a bounded fix using the
  maintainer-selected extension hook, so neither is due.

## Protected areas

- `scripts/stage2_repository_pathlock.mjs` and
  `scripts/stage2_session_policy.mjs`: keep their enforcement mechanisms;
  only their tests' launch combinations change.
- `tools/pi/`, `model-endpoints.yaml`, `decisions/`, `docs/adr/` and
  `AGENTS.md`: no pin, policy or governance change is needed.
- `scripts/stage2.py`: implementation waits for lane A's merge/release,
  as recorded in `decisions.md`; an independent launch site is not a reason
  to edit that shared file early.

## Definition of Done

- `make verify` is green after implementation; the runner owns the full run.
- Real pinned-Pi offline contracts capture complete requests through a
  loopback provider, with external network denied and synthetic credentials.
  Every covered launch shape is exercised, including tool/error follow-ups
  and a second user turn for the session shape. Missing prerequisites fail
  instead of skipping; omitting the extension demonstrably exposes a planted
  local identifier. The PR records the evidence and its commit.
- Documents moved with the code: this change's `spec.md`, `plan.md` and
  `findings.md`; no ADR, model record or workflow document changes are owed.
- The PR file list shows the protected areas untouched and non-goals unbuilt.
- The PR closes the neutral-Pi-paths work item (coding-harness-xul8); its
  final commit carries `Closes-Bead: coding-harness-xul8`.
- No hosted-model capture or live research run is required for this fix.

## Open decisions

None open. The following reversible details are chosen here with reasons.

- [DETAIL] Use `.` for the model-visible working directory: it conveys
  relative-path use without pretending that a new absolute tool root exists.
- [DETAIL] Preserve Pi's generated tools and rules while dropping `<docs>`:
  setting only a custom preamble would also omit tools/rules in Pi 1.2.0
  (`dist/core/system-prompt.js:78–96`, read on 2026-10-29).
- [DETAIL] Measure the full payload using the existing offline contract
  transport, rather than making a hosted call: it observes what the provider
  receives without sending the very identifiers the test is meant to detect.
- [DETAIL] Allow two hours of phase-4 work, including repairs; stop and report
  unfinished work at that limit. Neither input artifact states an appetite.
