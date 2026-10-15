---
title: "Spec — pi-pin"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-agx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, pi]
class: feature
appetite: 8
change: pi-pin
adr_question: {proposed: "yes", reason: "A repeatable real-Pi suite and repository-owned launcher amend the version-bound isolation rule of ADR 0011 and the Pi assumptions of ADR 0012."}
adr_files: [docs/adr/0019-repository-pinned-pi-and-contract-tests.md]
---

# Spec — pi-pin

Every Pi started by the runner comes from one repository-owned, locked install
whose relied-on behaviour is measured offline, independently of global Pi
updates (bead coding-harness-agx — the runner's own pinned Pi).
Research: `research.md`. Human answers: `decisions.md`, Q-1 through Q-6.

## Problem

- The runner finds Pi through PATH but demands exactly 1.1.0; the global update
  to 1.2.0 stopped the review loop on 2026-10-15. The session also resolves Pi
  through PATH (`research.md`, seed and “How Pi is installed and reached today”).
- Stand-in CLI tests prove the runner's arguments, not real Pi's tool,
  discovery or extension behaviour. The original isolation measurement was
  manual and version-specific (`research.md`, “What the measurement tie means”).
- Node and Pi dependencies are unpinned. CI neither installs Pi nor exercises
  the real session policy inside it (`research.md`, “Pinning precedents” and
  “The session verb's Pi surface”, read 2026-10-15).
- Zen's free tier refused Pi with 403 on 2026-10-15; the maintainer narrowed the
  requirement to live Go and offline Zen compatibility (decision Q-3).

## Terms

- **Offline contract suite:** tests starting the actual pinned Pi against a
  loopback stand-in server, using synthetic credentials and controlled tools,
  without a hosted model, user configuration or external network access.
- **Pin:** an exact Pi dependency version and npm integrity lock in `tools/pi/`;
  Node's measured major is derived from an exact CI runtime version there.
- **Isolation:** the reviewer's existing clean configuration and discovery
  restrictions; it does not confine its four read/search tools to the worktree.

## Acceptance criteria

1. When a fresh checkout runs the documented Pi installer, it installs the exact
   manifest dependency and lock-file dependency graph with lifecycle scripts disabled.
   *Refuted by:* a floating version, ignored lock mismatch/integrity error,
   executed lifecycle script, or a successful install using a different graph.
2. When `tools/pi/pi` is called from any working directory, it starts only its
   repository-local Pi, regardless of a missing, broken or newer global Pi.
   *Refuted by:* a PATH Pi sentinel running, or failure caused only by global Pi.
3. If the local install is absent, its Pi version differs from the manifest,
   or its version cannot be checked, the wrapper fails before a model request
   with an actionable diagnostic and no automatic install or global fallback.
   *Refuted by:* a request, global fallback or install on that failure path.
4. If Node is absent or its major differs from the declared measured major,
   the wrapper refuses before starting Pi; other minor/patch versions in that
   major remain eligible for the same contract suite.
   *Refuted by:* a wrong-major launch, or refusal solely for a same-major patch.
5. When the review loop, probe, or Pi session performs a version check or starts
   Pi, it uses the same repository wrapper, including the session's extension
   confirmation and Terminal dispatch.
   *Refuted by:* any of these paths resolving or invoking global Pi.
6. When the offline suite starts a real reviewer-shaped Pi, the model sees
   exactly `read,grep,find,ls` and a requested undeclared write/command tool
   cannot execute.
   *Refuted by:* a different declared set or an undeclared tool changing a sentinel.
7. When a reviewer-shaped contract call runs among planted configuration and
   discovery traps, only its controlled scratch configuration is used.
   *Refuted by:* a planted extension, MCP server, skill, context file, prompt
   template, theme, saved authentication or command-valued configuration marker
   being loaded, executed or transmitted despite the production isolation flags.
8. When a real Pi runs a test extension, the registered tool receives the
   requested structured input and returns its result through Pi's tool exchange.
   *Refuted by:* a signature change, misbound input or missing tool result being
   hidden by a fake extension API or a passing import-only check.
9. When real Pi loads the production session policy, an in-worktree read succeeds
   and reads outside the worktree, including a symlink escape, are blocked.
   *Refuted by:* an outside sentinel entering a tool result or a permitted read
   never executing; listing the policy flag alone is insufficient evidence.
10. When real Pi lists models with isolated synthetic credentials, the suite
    checks the actual table output for both `opencode-go` and `opencode`.
    *Refuted by:* parsing invented JSON, silently accepting an absent provider,
    or using the maintainer's credentials to make the test pass.
11. When the suite exercises either OpenCode provider, it verifies that
    `OPENCODE_API_KEY` authenticates the request and that the native provider
    address is respectively `https://opencode.ai/zen/go/v1` or
    `https://opencode.ai/zen/v1`, using only a loopback request override.
    *Refuted by:* a wrong native address/key mapping, a request to a hosted
    provider, or overriding the address without separately checking its native value.
12. When local verification or hosted CI runs the contract suite, missing Pi,
    missing Node, denied loopback setup, timeouts and malformed exchanges fail
    the run instead of skipping it; CI installs the exact declared Node and
    locked Pi with the same installer as local setup.
    *Refuted by:* any missing prerequisite yielding green/skipped contracts,
    or CI exercising only the stand-in CLI instead of real Pi.
13. While the runner uses the new install, its existing declaration/leak checks,
    clean reviewer environment, key scrubbing, nonzero-exit refusal and session
    sign-in through the maintainer's own agent directory remain in force.
    *Refuted by:* model dispatch before a required check, leaked keys, treating
    a failed/truncated print call as success, or copying credentials into the install.
14. When this change is delivered, setup/update instructions, the workflow and
    endpoint remark describe the repository pin and measured contracts, and
    one new ADR proposes the amendments without claiming reviewer read confinement
    or live paid-Zen validation.
    *Refuted by:* current guidance requiring global Pi 1.1.0, an amended historical
    ADR, an enabled Zen endpoint, or an unsupported safety/compatibility claim.

## Non-goals

- A scheduled update bot, automatic updates, global Pi management, vendored
  `node_modules`, or installation without access to the npm package registry.
- Live provider/model probes, paid Zen declaration or sign-in, free Zen access,
  new model selection, ladder/effort/routing changes, or a guarantee of paid Zen
  access. Declaring paid Zen later still needs that endpoint's normal review.
- Confining reviewer reads, sandboxing shell/network use in interactive sessions,
  changing policy rules, or claiming a live macOS Terminal smoke test.
- Redesigning the kit/export policy, tracker, gate system or unrelated validators.

## Protected areas

Existing ADRs and recorded human answers remain historical evidence. Customer
repositories, user configuration/credentials, `.claude/settings.json`, leak-check
logic and decision-continuity mappings remain untouched: no new data-flow
permission, D-/O-decision amendment or approval rule is needed here.

## Definition of Done

- `make verify` green with installed real Pi; the contract tests run locally and
  in CI. The pull request names the commit and measured Pi/Node versions.
- Moved with code: `tools/pi/README.md`, `docs/WORKFLOW.md`, the Pi remark in
  `model-endpoints.yaml`, and `docs/adr/0019-repository-pinned-pi-and-contract-tests.md`.
- Protected areas untouched and non-goals unbuilt, shown by the file list.
- The decision PR names and closes bead coding-harness-agx — the runner's own
  pinned Pi; its final commit carries `Closes-Bead: coding-harness-agx`.
- No live special runs are required; offline contract output is evidence, not
  an online compatibility result. Merge remains the maintainer's action.

## Open decisions

None open. The maintainer's six answers are inputs, not agent-authored approvals;
no machine-readable ADR answer is created by this draft.

- [DETAIL] Start with Pi 1.2.0, the candidate documented in the research, and
  Node 26.9.0 (major 26), recorded in the repository's 2026-10-05 research.
  These are reversible candidates, not measured compatibility claims: the real
  suite must pass on them before implementation can be called done. A failed
  contract is investigated or reported, never weakened to bless the candidate.
- [DETAIL] Store the Pi dependency pin in `tools/pi/package.json`; derive Python
  and wrapper expectations from it. Store the exact CI Node version in
  `tools/pi/.node-version` and derive the local major, avoiding duplicate pins.
- [DETAIL] Allow eight hours for phase 4 including repairs, stopping with evidence
  when spent; neither the research nor the human answers prescribe an appetite.
