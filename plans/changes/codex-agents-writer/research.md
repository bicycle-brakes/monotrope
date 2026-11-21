---
title: "Research — codex-agents-writer"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-xrcd
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# codex agents writer — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1156 files, 5174 commits, 12 rules.

## Runner exploration — 2026-11-21

Research complete. Here is the prose for `plans/changes/codex-agents-writer/research.md`, ready to append after the stage-2 audit line.

---

## What exists today

**The change's frame, as the tree records it.** The folder was opened 2026-11-21 for bead coding-harness-xrcd (branch commit `81bf739c`, "chore(codex-agents-writer): open change folder for coding-harness-xrcd"; row in `plans/INDEX.md` line 600). The bead's own text was not read — the tracker is the Dolt database under `.beads/` and carries no rendered copy in the tree (`AGENTS.md` house rule 2). What the tree records about the bead is one sentence in the night-run handover: "A runner repair of finder-partial-report was refused once because files appeared under `.codex/agents/` (bead coding-harness-xrcd); the retry passed." (`docs/journal/handover/2026-11-20-night-run-2026-11-19-b.md`, "Open work and blockers", last bullet). The change name reads as "the writer of the `.codex/agents/` files" — that parse is this exploration's reading of the name, not a statement found in the tree.

**What `.codex/` holds in the tree (tracked).** Exactly two files exist in this worktree (Glob over `.codex/**`): `.codex/config.toml`, whose whole content is `[features] hooks = true`, and `.codex/hooks.json`, which registers four hooks (SessionStart on `startup|resume|clear`, UserPromptSubmit, PreCompact, PostCompact), each calling `"$(git rev-parse --show-toplevel)"/tools/bd codex-hook …`. The verb `codex-hook` is not implemented in this repository: `tools/bd` is a version-pinning wrapper that execs the pinned `bd` binary (`tools/bd`, final `exec "$BD_BIN" "$@"`), so what the hook does is not readable here. `.codex/agents/` does not exist in this worktree.

**The untracked `.codex/agents/` of the main checkout, as handovers record it.** It has existed since at least 2026-10-17 as "pre-existing untracked" (`docs/journal/handover/2026-10-17-night-run-sixth.md`), and every handover from 2026-10-19 through 2026-11-21 records it as untracked, belonging to the maintainer or "another owner", never touched by a session — most recently `docs/journal/handover/2026-11-21-day-run.md` ("Working state": main checkout's pre-existing uncommitted files include `.codex/agents/`). Its content is known only indirectly: one file name, `.codex/agents/code-generation-orchestrator.toml` (`plans/changes/archive/2026-11-16-night-stall-guard/findings.md`, runner diagnostics), and the Regelwerk's description: Codex definitions under `.codex/agents/*.toml` "embed the clause in `developer_instructions`" (`docs/governance/regelwerk.md` §7.0.0, "Agents/Hooks/Templates" line). They are therefore TOML counterparts of the nine tracked `.claude/agents/*.md` definitions (Glob: code-generation-orchestrator, consistency-auditor, entity-builder, entity-deployer, explorer, migration-supervisor, preconditions-gate-runner, reconciliation-orchestrator, reviewer), which carry the RB-A1 evidence-contract clause byte-identically in Markdown (`docs/governance/regelwerk.md` §6; `tests/test_regelwerk.py::test_rb_a1_clause_is_present_verbatim`). No inventory of the TOML set exists in the tree — only one file is named anywhere ("not found" as an inventory, which is not the statement "only one file exists").

**Why appearances of these files break runner runs — four mechanisms, all measured in `scripts/stage2.py`:**

1. `changed_paths` includes untracked, non-ignored files (`git ls-files -z --others --exclude-standard`, symbol `changed_paths`); `.gitignore` does not ignore `.codex/agents/` (read whole), so an untracked copy is a changed path.
2. Targeted verification: any touched path that is neither `.py` nor a `plans/`/`docs/` Markdown document makes the check full — "`…` is an input kind the targeted selector does not cover" (`targeted_selection`, the `.py` gate near its end). Measured consequence, 2026-11-09, night-stall-guard worktree: two runner repair attempts were forced to the full `make verify` because `.codex/agents/code-generation-orchestrator.toml` appeared; one attempt hit the runner's 30-minute step limit (archive `findings.md`, attempts 2 and 3 diagnostics).
3. Checkpoint: `checkpoint` refuses and rolls the attempt back when a changed path falls under a held prefix — `.codex/` is an entry of the `RUNNER_HELD` tuple (with the comment "`​.codex/` holds the hook list"), refusal message "the attempt changed paths a stage-2 run does not commit" (`uncommittable` and `checkpoint`). This is the mechanism behind the finder-partial-report refusal that bead coding-harness-xrcd records.
4. Phase-6 review refuses a dirty tree outright ("phase 6 reviews a committed tree … these paths differ from HEAD", the `standing()` check before `review`); the 2026-11-19 handover records the runner "refused to start in both" lane worktrees after byte-identical copies of the main checkout's `.codex/agents/` appeared there on 2026-11-18 at 20:22 (`docs/journal/handover/2026-11-19-night-run-2026-11-18-a.md`, "Needed from the maintainer" question 2).

The refusals behaved as designed: the retry passed once the files were gone, and the worktree copies were moved to a session scratchpad (2026-11-20 handover; 2026-11-19 handover, scratchpad path in question 2).

**Who writes them — what the tree can say.** No repository script references `.codex/agents` (search over `scripts/` and `tools/`: only the kit manifest's `.codex/` prefix entry and `RUNNER_HELD` name `.codex/`), and no script creates worktrees or copies files into them (search `worktree add` over `scripts/` and `tools/`: no match; worktrees are created by Claude Code or by hand per `docs/WORKFLOW.md` §3 "Worktrees — one per change"). The runner's two Codex start paths differ: headless `run_codex` pins `--disable hooks --disable memories` and passes `HOME`/`CODEX_HOME` through (`ENV_ALLOW`; command construction in `run_codex`), and does not pass the `--ignore-user-config` flag the CLI offers (`plans/changes/archive/2026-09-30-stage-2-codex-glm/research.md`, "Resume" section) — `docs/WORKFLOW.md` §4 states "the runner starts Codex with hooks and memories off". The interactive `session` verb starts `codex --no-daemon … --sandbox workspace-write` with neither hooks nor memories disabled (`cli_argv` in `scripts/stage2_session.py`), so such a session loads the tracked `.codex/config.toml` and `.codex/hooks.json` and runs `tools/bd codex-hook`. Which of these — Codex CLI, the bd binary's hook, or a hand copy — produced the worktree appearances is not decidable from this tree: both binaries live outside it. The byte-identical copies suggest a copy of the main checkout's files rather than a fresh generation, but no tree text names the copier. The maintainer's question "Who copies `.codex/agents/` into worktrees?" stands unanswered in the 2026-11-19 handover.

**Governance the files run into when they land.** The Regelwerk reserves the extension for exactly this change: "When the Codex definitions under `.codex/agents/*.toml` land, the enforcer must grow a TOML branch … the current paragraph parser reads Markdown only. That extension belongs to the change that commits them" (`docs/governance/regelwerk.md` §7.0.0). Today's enforcer is Markdown-only in three places: `_klausel_aus_agent` finds a `## Evidence contract (RB-A1)` heading and reads paragraphs (`tests/test_regelwerk.py`), and both `test_rb_a1_clause_is_present_verbatim` and `test_agent_definitions_carry_no_instance_terms` glob `.claude/agents/*.md` only; `agent_modelle()` in `tests/test_model_endpoints.py` likewise reads only `*.md` with a `model:` line regex, so a TOML definition's model would not be held against `model-endpoints.yaml`. Elsewhere: `.claude/agents/x.md` is explicitly "not held" by the frontmatter gate because "its frontmatter is configuration" (`tests/test_frontmatter_current.py`, `test_the_map_holds_documents_not_harness_configuration`) — a TOML file has no Markdown frontmatter at all; `scripts/kit/manifest.yaml` classifies prefix `.codex/` as `bestand` with the reason "offen, dieselbe Frage wie .claude/ (D3)"; `RUNNER_HELD` protects `.codex/` whether tracked or not, held in step by `tests/test_stage2.py::test_an_attempt_that_writes_an_agent_entry_point_is_refused` (parametrized list includes `.codex/config.toml`) and by the plan prompt's restatement (`prompts/03-plan.md`, the held-path list; pinned by `test_the_plan_prompt_names_every_runner_held_path`); `provenance.yaml` has no entry whose prefix names `.codex` — its five classes are a closed enum (`provenance.yaml`, "Die fuenf Klassen").

## Where it lives

Incident record: `docs/journal/handover/2026-11-19-night-run-2026-11-18-a.md` (question 2), `docs/journal/handover/2026-11-20-night-run-2026-11-19-b.md` (blockers bullet naming bead coding-harness-xrcd), plus the recurring "untracked `.codex/agents/` untouched" lines in the handovers of 2026-10-17 through 2026-11-21. Runner mechanisms: `changed_paths`, `targeted_selection`, `RUNNER_HELD`, `_held_prefixes`, `uncommittable`, `checkpoint` in `scripts/stage2.py`; `run_codex` (hooks/memories off) and `ENV_ALLOW` in the same file; `cli_argv` in `scripts/stage2_session.py`. Pins: `tests/test_stage2.py` (held entry points), `tests/test_regelwerk.py`, `tests/test_model_endpoints.py`, `tests/test_frontmatter_current.py`. Doctrine: `docs/WORKFLOW.md` §3 (worktrees; Codex isolation paragraph), §4 (hooks-off sentence), `docs/governance/regelwerk.md` §6 and §7.0.0. Tracked Codex config: `.codex/config.toml`, `.codex/hooks.json`; the `codex-hook` verb behind them lives in the pinned bd binary (`tools/bd` wrapper). The untracked definitions: main checkout only, not in this worktree; one name known (`code-generation-orchestrator.toml`).

## What is unclear (open questions, not guesses)

1. The bead coding-harness-xrcd's title, description and class were not read (tracker outside this phase's reach); whether the change is "identify the writer", "commit the definitions with the enforcer TOML branch", or both is stated nowhere in the tree.
2. The writer of the worktree copies is not identified by anything in the tree; the maintainer's handover question stands. Answering it needs observation outside this worktree (a machine-level look at what a Codex start or a `bd codex-hook` run writes), which this phase could not perform.
3. The full inventory and content of the maintainer's `.codex/agents/` is unreadable from this worktree; only `code-generation-orchestrator.toml` is named anywhere, and the Regelwerk's `developer_instructions` description is prose, not a file read.
4. Whether the appearances correlate with headless `run_codex` calls, interactive session-verb sessions, the `bd codex-hook`, or something else: the recorded timestamps fall in runner-active windows, but no tree evidence names the process.
5. Whether `--disable hooks` also suppresses whatever writes `.codex/agents/` is a CLI-behavior question; nothing in the tree answers it, and the 2026-11-19/20 appearance during a runner repair (whose model calls run hooks-off) hints it does not — a hint, not a measurement.
6. What `bd codex-hook` injects or writes was already untested in the predecessor research (`plans/changes/archive/2026-09-30-stage-2-codex-glm/research.md`: "what `codex-hook` injects, was not tested"); nothing newer was found.
7. Whether the definitions are meant to be committed (the Regelwerk's provision presupposes "the change that commits them") or to stay untracked machine-local files is the maintainer's call; the tree states only the conditional.

## Which files a change would have to touch

- The Regelwerk side the §7.0.0 note reserves: `tests/test_regelwerk.py` (`_klausel_aus_agent`, the two `*.md` globs) for a TOML branch, and `docs/governance/regelwerk.md` §7 (append-only entry with the four duty lines §4 requires) — the note says the extension belongs to the change that commits the definitions.
- The model pin, if the TOML definitions' models are to be held like the Markdown ones: `tests/test_model_endpoints.py` (`agent_modelle`); `model-endpoints.yaml` already declares the endpoint models, so no new entry exists to write there.
- The runner side, only if the runner's reaction itself should change: `scripts/stage2.py` (`changed_paths`, `targeted_selection`, `RUNNER_HELD`, `checkpoint`) and its pin `tests/test_stage2.py::test_an_attempt_that_writes_an_agent_entry_point_is_refused`.
- The classification files, depending on what the files are declared to be: `.gitignore` (today `.codex/agents/` is not ignored, which is exactly why the runner sees it), `provenance.yaml` (no `.codex` entry exists; a committed definition set would need a class from the closed enum), `scripts/kit/manifest.yaml` (the `.codex/` prefix is `bestand`, role "offen, D3").
- The definitions themselves are the maintainer's files and are not in this tree; the tracked `.codex/config.toml` and `.codex/hooks.json` are the only Codex files a commit could build on.
