---
title: "Research — pi-no-compaction"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: stage2, version: "glm-5.3-flash, 2026-11-06; Codex repair, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# pi no compaction — Research

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3379 commits, 12 rules.

## Runner exploration — 2026-11-06

## What exists today

**The change's origin and purpose.** Bead `coding-harness-mwzv.2` ("the runner writes `compaction.enabled=false` into every Pi settings file", P1, `bounded`) was created in the 2026-11-03 five-lane night as lane C's backlog item (`docs/journal/handover/2026-11-03-five-lane-night.md`, "Created tonight", and the backlog table in `docs/research/2026-11-03-night-run-plan.md`, "Backlog added"). Its parent bead `coding-harness-mwzv` is the review-loop/review-swarms bead (`docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md`, lane table). The motivation is recorded in the comment above `REVIEW_DIFF_MAX_LINES` in `scripts/stage2.py` (`REVIEW_DIFF_MAX_LINES`, lines ~421–426): Pi compacts an oversized context instead of failing, so a "No finding." could rest on a summary the member never saw in full — "R-15 of the review-swarm review".

**The measurement behind the change.** `docs/research/2026-11-03-pi-context-overflow.md` (bead `coding-harness-ut8q`, frontmatter `review: {status: pending}`) measured on 2026-11-03, Pi 1.2.0: with `"compaction": {"enabled": false}` added to the agent `settings.json`, an oversized prompt ends as exit 1 in the runner's `--print` text mode, stderr carries the provider's 400, and `run_reviewer` raises `CallFailed` — a failed member, no summary, no second request. With compaction left on, Pi runs a `compaction_start` (reason `overflow`), a summary request and one retry that cannot succeed, because the oversized text sits in the system prompt, which compaction never shortens. The same note records: json output mode exits 0 even on the error (the runner uses text mode); the overflow-from-tool-reads case (a paid reviewer reading past its window) was **not measured**, only read in code; and the project-level `.pi/settings.json` is not the place, because the runner passes `--no-approve`, which ignores project-local files. The note is a research record with review pending, not a merged decision (ADR 0008) — its steps are recorded context, not doctrine.

**Pi's compaction mechanism as installed (1.5.0).** The pinned dependency in this worktree is `@earendil-works/pi-coding-agent` `1.5.0` (`tools/pi/package.json`, `dependencies`). Auto-compaction is on by default: `SETTINGS_DEFAULTS.compaction` is `{enabled: true, reserveTokens: 16384, keepRecentTokens: 20000}` (`tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/settings-defaults.js`, `SETTINGS_DEFAULTS`). The trigger is `shouldCompact(contextTokens, contextWindow, settings)` in `dist/core/compaction/compaction.js`, which returns `false` immediately when `settings.enabled` is false and otherwise fires at `contextTokens > contextWindow - settings.reserveTokens` (`shouldCompact`, ~lines 173–177). Settings are read through `getCompactionEnabled`/`getCompactionSettings` in `dist/core/settings-manager.js` (~lines 643–684), schema-declared in `dist/core/settings-schema.js` (`compaction.enabled`, boolean with default). In 1.5.0 the gate is consulted at three places in `dist/core/agent-session.js`: the between-turn check (~line 434, via `shouldCompact`), the auto-compact routine (~line 2524, settings from `getCompactionSettings` at ~2541), and the overflow-recovery block (~lines 2259–2261, `getCompactionSettings` → `prepareCompaction`). The shipped package doc `tools/pi/node_modules/@earendil-works/pi-coding-agent/docs/compaction.md` states the same trigger formula, the settings table with default `enabled: true`, "Disable auto-compaction with `"enabled": false`" (manual `/compact` stays available), and that the resolved values govern "manual compaction, all automatic threshold checks, overflow recovery".

**Settings-file resolution in Pi.** Pi merges two files: the global `<agentDir>/settings.json` and the project `<cwd>/.pi/settings.json`, project winning (`dist/core/settings-manager.js`, `globalSettingsPath`/`projectSettingsPath`, deep-merged into `this.settings`). The agent directory is `PI_CODING_AGENT_DIR` when set, else `~/.pi/agent` (`dist/config.js`, `getAgentDir`). `--no-approve` means "Ignore project-local files for this run" (usage text in `dist/bundle/chunks/chunk-44DLKSKE.js` and `dist/package-manager-cli.js`) — and every runner Pi call passes it.

**Where the runner writes Pi settings files today — five sites, all identical content `{"retry": {"enabled": False}}`:**

1. `scripts/stage2.py` in `discover_free` — the scratch agent directory for the forced catalog refresh (`pi update --models`) and the `--list-models` listing; these two CLI verbs run no agent turn.
2. `scripts/stage2.py`, same function — the `listing_agent` copy, a byte copy of the first file's `settings.json`, so it inherits whatever the first file holds.
3. `scripts/stage2.py` in the reviewer-call function whose docstring says "an agent directory with retry settings" — every paid and free review-loop member call; argv is `--print --no-session --no-approve … --offline` with `--append-system-prompt`, cwd is the worktree root for paid members and the scratch directory for free calls, env carries `PI_CODING_AGENT_DIR` at the scratch agent.
4. `scripts/stage2_research_run.py` in `Run.pi_command` — every research-swarm member call; same flag shape (`--print --no-session --no-approve … --offline`); repository seats run with cwd = the worktree root, public seats with cwd = scratch. `scripts/research_capture.py` builds its launches through the swarm's own `Run.pi_command` (its header says so), so it inherits this shape.
5. `scripts/stage2_availability.py` in the Go probe helper — the `prepare-loop`/`prepare-explore` reachability probe; `--print --no-session --no-approve … --no-tools`, cwd scratch.

**The route that writes no settings file.** The interactive Terminal-window session route (`scripts/stage2_session.py`, `cli_argv` Pi form plus `terminal_command`) dispatches `pi --no-extensions … -e <policy> --offline --no-approve --model … -- <prompt>` with env `runner.foreign_env({})`; `ENV_ALLOW` in `scripts/stage2.py` passes `HOME` through, so this session reads the maintainer's own `~/.pi/agent/settings.json`. A search of `stage2_session.py` for settings writes found none (the two `confirm_*` checks use a temp `PI_CODING_AGENT_DIR` and write no `settings.json` either). "Every Pi settings file" as written by the runner today therefore means the five scratch files above; the interactive session reads a file the runner never writes.

**Test pins that measure the content today.** `tests/test_stage2.py::test_the_review_loop_launches_pi_isolated` asserts the reviewer agent directory's exact settings content `{"retry": {"enabled": False}}` (the `agent_settings` assertion; the fake-Pi harness records it via the `agent_settings` field defined near the top of that file and surfaces it in diagnostics). `tests/test_pi_contract.py`'s launch helper writes the same retry-only content into its own scratch agent for every real-Pi contract run. No test in `tests/` measures Pi compaction behavior: the only `compaction` match there is `tests/test_beads_start.py`'s unrelated "no compaction" (session-scan terminology about Claude Code, not Pi).

**Version and citation drift.** The compaction measurement is from Pi 1.2.0; the pin moved to 1.5.0 through the `pi-catalog-move` change (`plans/changes/pi-catalog-move/decisions.md`, Q-1, 2026-11-04: "pin Pi 1.5.0"; its `spec.md` records that at baseline `c7886ea5` on 2026-11-04 the manifest still said 1.2.0). The `stage2.py` comment still labels the behavior "Pi 1.2.0" and cites `dist/core/agent-session.js:418` — a 1.2.0-era line number that does not match the installed 1.5.0 layout (the consult points sit at ~434, ~2259–2261 and ~2524 there). The 1.5.0 source read above shows the same `enabled` gate and the same defaults; `docs/WORKFLOW.md` does not mention compaction at all (searched "compact" — no match), and `docs/` nowhere records the 1.5.0 move (searched "1.5.0" — no match outside `plans/changes/pi-catalog-move/`).

## Where it lives

- Intent and provenance: `docs/research/2026-11-03-night-run-plan.md` (backlog table, lane C), `docs/journal/handover/2026-11-03-five-lane-night.md` ("Created tonight"), `docs/research/2026-11-03-pi-context-overflow.md` (the measurement), `scripts/stage2.py` comment above `REVIEW_DIFF_MAX_LINES`.
- Pi mechanism: `tools/pi/package.json` (the pin); `tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/settings-defaults.js`, `settings-schema.js`, `settings-manager.js`, `compaction/compaction.js`, `agent-session.js`, `dist/config.js`, `docs/compaction.md` — all inside the pinned install the contract suite measures.
- Runner write sites: `scripts/stage2.py` (`discover_free` ×2, reviewer call), `scripts/stage2_research_run.py` (`Run.pi_command`), `scripts/stage2_availability.py` (probe helper); the no-write route `scripts/stage2_session.py`.
- Test pins: `tests/test_stage2.py` (exact-content assertion + `agent_settings` harness field), `tests/test_pi_contract.py` (contract launch helper).

## What is unclear about it

1. **No 1.5.0 end-to-end measurement exists.** The clean-failure-on-overflow behavior was measured on Pi 1.2.0 (`docs/research/2026-11-03-pi-context-overflow.md`, method section). The installed 1.5.0 source shows the same `enabled` gate (`shouldCompact` returns false when disabled), but whether 1.5.0 behaves identically on a real overflow has not been re-measured in this repository as far as this pass read. The offline contract suite is the repository's stated instrument for relied-on Pi behavior (`tools/pi/README.md`, "What the tests install versus what they run"); no compaction contract exists today.
2. **Scope of "every Pi settings file" for the interactive route.** `stage2_session.py`'s Terminal-window sessions write no settings file and read the maintainer's own `~/.pi/agent/settings.json` through the passed-through `HOME`. Whether that route is in scope — and whether writing into the maintainer's home directory is acceptable at all — is settled in nothing I read. The bead text itself ("every Pi settings file", handover and night-run plan) does not name the files.
3. **Whether discovery needs the setting.** `discover_free`'s two verbs (`update --models`, `--list-models`) run no agent turn, so compaction cannot trigger there as far as the code read shows; the measurement note's wording ("every other Pi agent directory the runner writes") would include them. Both readings are recorded; nothing decides between them.
4. **Which contract pins the new content, and where a behavior contract belongs.** The exact-content assertion in `tests/test_stage2.py` must move when the content changes; whether a behavior contract (compaction off → clean failure against real Pi) belongs in `tests/test_pi_contract.py` now or with the neighbour bead `coding-harness-z4oo` ("contract tests read the pinned Pi's real data", night-run plan backlog) is not settled. No `plans/` artifact for `coding-harness-z4oo` exists yet (not found under `plans/changes/` or `plans/INDEX.md` in this pass).
5. **The R-15 source document.** "R-15 of the review-swarm review" is cited in `scripts/stage2.py` and the overflow note, but the review document carrying R-15 was not located in this pass (searched `docs/research/` and `plans/` for "R-15"/"review-swarm review" — only citations came back). The maintainer's four-part split decision (2026-10-26, at most four parts of 2000 lines, each reviewed in full) is likewise known only through the overflow note's citation.
6. **The stale comment.** Whether the `stage2.py` comment's "Pi 1.2.0" label and 1.2.0-era line citation get brought to the installed pin in this change or another is stated nowhere I read.

## Which files a change would have to touch

- `scripts/stage2.py` — the reviewer-call settings write and the `discover_free` write (the `listing_agent` copy inherits); possibly the `REVIEW_DIFF_MAX_LINES` comment block.
- `scripts/stage2_research_run.py` — the `Run.pi_command` settings write (also inherited by `scripts/research_capture.py`).
- `scripts/stage2_availability.py` — the probe settings write.
- `tests/test_stage2.py` — the exact-content assertion and, through it, the harness field; any test that pins the research-run and probe settings shape would follow the same pattern (none exists today beyond the reviewer one).
- Possibly `tests/test_pi_contract.py` — if a compaction behavior contract is added, its launch helper's own settings write is the seam.
- `docs/WORKFLOW.md` holds no compaction text today, so no doctrine file is forced by what exists; whether it should name the runner's no-compaction guarantee is an interview question, not a fact.

## Neighbours

- `plans/changes/pi-pin/spec.md` — the pinned install, wrapper and contract suite (ADR 0019); owns "relied-on behaviour the contract suite measures".
- `plans/changes/pi-catalog-move/spec.md` — the pin move to 1.5.0 (bead `coding-harness-vku6`); the reason the measurement's version label has drifted.
- `plans/changes/pi-catalog-redirect/spec.md` and `plans/changes/pi-catalog-move/research.md` — catalog acquisition paths touching `discover_free`.
- `plans/changes/research-swarm/spec.md` — the research swarm whose member calls carry the settings write.
- `plans/changes/loop-until-clean/spec.md`, `plans/changes/review-release-lock/spec.md`, `plans/changes/review-verdict-validated/spec.md` — review-loop ending and release rules the overflow failure kind interacts with (ADR 0021 territory; the overflow note records that an amendment is needed only if overflow becomes its own named failure kind).
- `plans/specs/implementation-verification/spec.md` — living spec of the runner's attempt preparation, the phase whose derived-file checks surround the loop.
- Bead `coding-harness-z4oo` (contract tests reading the pinned Pi's real data) — named in the night-run plan backlog; no `plans/` folder yet.

## Repair measurement — 2026-11-07

The phase-1 observations above describe the pre-implementation tree. The offline
contract now measures the installed Pi 1.5.0 through the production reviewer
launch with synthetic credentials and a loopback provider; no paid provider is
called. The repair started from `ba80de2ccbb90a9baa39ffecd9626f93cecd2fdd`.

`tests/test_pi_contract.py::test_real_truncated_pi_print_failure_is_refused`
passes with the narrower 1.5.0 expectations: exactly one request, process exit
1, stderr containing `Response was truncated`, and the runner's `CallFailed`
containing `output token limit`. The old 1.2.0 measurement returned zero with
empty stdout. Keeping that older expectation would describe the wrong refusal
path for the pinned runtime; the test now pins the measured 1.5.0 path rather
than accepting either version's behavior.

`tests/test_pi_contract.py::test_real_context_overflow_fails_without_compaction`
also passes on Pi 1.5.0. Its production-setting fault and restoration evidence
are recorded in this change's plan, under the repair verification section.
