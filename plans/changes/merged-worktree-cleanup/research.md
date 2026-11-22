---
title: "Research — merged-worktree-cleanup"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.4
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-22", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# merged worktree cleanup — Research

Stage-2 call, 2026-11-22: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1167 files, 5311 commits, 12 rules.

## Runner exploration — 2026-11-22

Research complete. The following is append-ready for `plans/changes/merged-worktree-cleanup/research.md`.

---

## What exists today

**The rule, and that it is manual.** `docs/WORKFLOW.md`, §3 "Worktrees — one per change" (section header at `### Worktrees — one per change`), holds six numbered rules. Rule 2 fixes the placement: worktrees live in the repository under `.claude/worktrees/<name>`, created by hand with `git fetch origin && git worktree add -b <branch> .claude/worktrees/<name> origin/main` (or by Claude Code itself: `claude --worktree <name>` and a sub-agent's `isolation: worktree`). Rule 6 is the cleanup rule: "After the merge, the worktree goes. `git worktree remove .claude/worktrees/<name>` and the branch with it. A worktree nobody works in is a place where a later session finds an old state and takes it for the current one." No tool, gate or hook implements rule 6 — it exists only as prose.

**Placement is gitignored.** `.gitignore` lines 9–11 ignore `.claude/worktrees/` with the comment naming D-5 and bead `coding-harness-m34` ("Claude Code puts them here, and the main checkout must not list them as untracked"). Removing a worktree therefore never touches tracked files. The same comment block records that sibling placements beside the repository are retired (D-5, lifted 2026-09-23).

**Isolation doctrine.** `docs/adr/0006-parallel-work-without-a-pilot.md` (accepted 2026-09-27, `provenance: human-decided`): isolation by worktree, one worktree per session (D-60), at most `writing_sessions_per_repository` (default 2) writing sessions per repository. A grep of `docs/adr/` for "worktree" shows ADRs 0001, 0005, 0006 and 0007 discuss worktrees for isolation and review reach — no ADR covers worktree removal, decay or cleanup; that concept appears only in a research note (below).

**The measured problem.** `docs/research/2026-11-18-trust-pyramid-against-the-harness.md`: its layer table names "38 finished worktrees" (§3, "One 11.5k-line file, 38 finished worktrees") and §6 states "the 97 worktrees are the symptom, the missing decay is the cause". Point 10 of §6, "Make worktrees decay", sketches an entry point `scripts/worktree_prune.py`: "`--check` lists worktrees on merged branches, older than seven days, or dirty; `--prune` removes only merged, clean, unpushed ones and refuses the rest. A writer gate reports the count, and a valve turns it blocking on a date." That sketch is research prose, not an accepted decision, and the script it names does not exist: a Glob for `scripts/*worktree*` returns only `scripts/check_worktree_state.sh`, and a Glob for `**/*worktree_prune*` returns nothing. Note the sketch's own wording is ambiguous — whether "unpushed" in that sentence means "has unpushed work" (must refuse) or "with nothing unpushed" (safe to remove) is not decidable from the sentence; it is quoted here verbatim, not interpreted.

**The accumulation is visible in the machine snapshot.** `scripts/machine_facts.py::worktree_field` (symbol `worktree_field`, docstring "stale ones included, never pruned") counts non-bare worktrees from `git worktree list --porcelain -z` and reports the count with the caveat "stale registrations included". The latest handover snapshot: `docs/journal/handover/2026-11-21-day-run.md` reports "117 registered worktrees" (machine snapshot `2026-11-21T11:37Z`) and notes separately that `.claude/worktrees/handover-2026-11-21` (from PR #424) "remains in place at `ac38bed9` and can be pruned after cleanup". `docs/journal/handover/2026-11-20-night-run-2026-11-19-b.md` records the manual pattern working: "#416 merged (cheap gates before admission); bead coding-harness-bxxt.6 closed, its worktree removed." No current count was taken in this session — this explorer runs no commands; 117 (2026-11-21) and 97 (2026-11-18) are the newest numbers on file, each with its cut-off.

**The tooling that exists around worktrees (and what it does not do).**

- `scripts/check_worktree_state.sh` — fail-closed precondition for an agent session in a worktree: refuses a rebase/merge/cherry-pick in progress, a detached HEAD it cannot safely reattach, a wrong branch, and a HEAD that moved backward since a recorded sha (`[min-known-sha]`). Its one auto-repair is reattaching a detached HEAD that is an ancestor of the expected branch. It is a precondition, not a cleanup: it never removes anything.
- `scripts/new_change.py` calls it before `make change` writes (`_worktree_is_sane`, constant `WAECHTER` at `scripts/new_change.py` `WAECHTER = Path(...)/"check_worktree_state.sh"`). Its docstring records the incident class: "At times five worktrees of this repo's main checkout were in exactly this state" (detached HEAD on a commit no branch holds).
- Tests: `tests/test_worktree_state.py` ("The guard before every session — and its five counter-checks") and `tests/test_workflow_entry.py` exercise it.
- `scripts/ci_gates.py`, entry for `check_worktree_state.sh` (the `SKRIPT_EXP` dict): declared a precondition with "no gate of its own, because CI runs from a clean checkout anyway" (the entry text is still German — translation debt, bead coding-harness-yim). The `OHNE_TEST` exemption list right below is documented as "may shrink, never grow" and is empty since 2026-09-22.
- `scripts/kit/manifest.yaml` carries `scripts/check_worktree_state.sh` (manifest entry with prefix `scripts/check_worktree_state.sh`) into new repositories — the kit would need to carry any new worktree script too.
- A grep of `scripts/` for worktree remove/prune finds **no** script that removes or prunes an agent worktree. The only hits are `machine_facts.py`'s "never pruned" docstring and the loop-record key machinery in `scripts/stage2.py` (see interactions below).

**The post-merge cleanup sequence that does exist — for beads and folders, not worktrees.** `prompts/07-commit.md` ("The merge" and the trailer section) fixes three steps: (1) merge via `gh pr merge <n> --merge --match-head-commit <sha>` (merge queue rule RB-G7, bead coding-harness-eh42, `docs/WORKFLOW.md` "Merging a series, one at a time"); (2) once `gh pr view` shows `MERGED`, the tracker writer runs `make close-merged ARGS=--write` — `scripts/close_merged_beads.py`, which closes beads declared by a `Closes-Bead:` trailer on merged history only; (3) the cleanup session runs `make archive` / `ARGS=--write` — `scripts/archive_closed_changes.py`, which moves change folders with closed beads into `plans/changes/archive/` and regenerates `plans/INDEX.md`. The Makefile exposes both (`close-merged` target with an ARGS whitelist of "" or `--write`; `archive` "as close-merged above"). The SessionStart hook `tools/claude-code/hooks/beads-start.sh` re-runs `close_merged_beads.py --write` at session start when the starting session is the sole writer. **No step in this sequence removes the worktree** — rule 6 of WORKFLOW.md §3 is applied by hand, somewhere, by whoever remembers.

**Interactions any cleanup has to respect (facts in the tree today).**

- *Live sibling sessions.* `tools/claude-code/hooks/session-scan.sh` classifies sessions per line as `clash` (same git toplevel), `sibling` (same repository, other worktree) or `other` (header comment of that script); `beads-start.sh` skips its tracker write when the scan reports `clash` or `sibling`. The vocabulary for detecting a live session in another worktree already exists.
- *Loop records keyed by worktree.* `docs/WORKFLOW.md` (loop-record sections) and `scripts/stage2.py::other_record_keys`: record keys are derived from `git worktree list` alone — "a listed worktree remains discoverable even if its directory is gone"; records of worktrees no longer listed by git are excluded; the verb refuses to supersede a record whose key "names no worktree of this repository" (`scripts/stage2.py`, the `Refused` message at the supersession check). `plans/changes/loop-record-other-worktree/decisions.md` states the named limit: "once pruned from git metadata, its record is not seen". A removed worktree path being reused has its own rule in the same section (the old record is not adopted; supersession names every active other-worktree key).
- *Branch protection.* The `pr_sync.py` merge/sync refuses "branches a local worktree holds with uncommitted or unpushed work" (`docs/WORKFLOW.md`, the sync refusal list). The distinction pushed/unpushed and clean/dirty is therefore already doctrine language, used by an existing tool.
- *Worktrees that Claude Code creates itself* (`claude --worktree`, sub-agent `isolation: worktree` — WORKFLOW.md §3 rule 2) land in the same ignored directory without passing `scripts/new_change.py`, so a cleanup keyed only on the harness's own change flow would miss them.

**The bead.** This change's folder carries `bead: coding-harness-bxxt.4` (frontmatter of this research file; `plans/INDEX.md` lists the change as draft under that bead). The `bxxt` family is the "verify speed and machine load" epic (`docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md`, lane table row 8). Sibling sub-beads on file: bxxt.1 (verify-cheap-first, gate cost classes), bxxt.6 (verify slot admission), bxxt.9 (ledger ids), bxxt.11 (per-slot worker tuning) — each seen through `decisions/gates.yaml` comments and handovers.

## Where it lives

- Rule: `docs/WORKFLOW.md` §3 "Worktrees — one per change", rule 6 (removal), rules 1–5 (placement, base, tracker, omnigent).
- Doctrine: `docs/adr/0006-parallel-work-without-a-pilot.md`; measurement `docs/research/2026-09-23-worktree-tracker-writes.md` (five checks green on bd 1.3.0; dated note: pin moved to 1.3.4 without repeating them).
- Proposal sketch: `docs/research/2026-11-18-trust-pyramid-against-the-harness.md` §6 point 10 (plus the count gate and dated valve in point 9).
- Precondition tool: `scripts/check_worktree_state.sh` + `scripts/new_change.py::_worktree_is_sane` + `tests/test_worktree_state.py` + `tests/test_workflow_entry.py` + kit entry `scripts/kit/manifest.yaml`.
- Counter/observer: `scripts/machine_facts.py::worktree_field`.
- Post-merge sequence: `prompts/07-commit.md`, `Makefile` targets `close-merged` and `archive`, `scripts/close_merged_beads.py`, `scripts/archive_closed_changes.py`, hook `tools/claude-code/hooks/beads-start.sh`.
- Interactions: `tools/claude-code/hooks/session-scan.sh`, `scripts/stage2.py` record-key discovery and supersession refusal, `scripts/pr_sync.py` refusal list (via `docs/WORKFLOW.md`), `.gitignore`.
- Gate registry: `decisions/gates.yaml` (schema comment block: `enforcement` report/block, `placement` writer/hosted/both, `cost` seconds/minutes, `needs_admission`; the schema comment also defines a dated valve vocabulary in prose: advisory/report gates with an `until` date per the research note point 9).

## What is unclear about it

- **The exact scope and class of bead `coding-harness-bxxt.4` is not readable from the tree.** The tracker is the Dolt database under `.beads/`; this explorer read no tracker state and ran no `tools/bd` command. The orchestrator can read it with `tools/bd show coding-harness-bxxt.4`. Everything above about the bead is inference from the epic name and sibling sub-beads — treat it as unconfirmed.
- **Whether the trust-pyramid point 10 sketch is the maintainer's intent.** It stands in a research document, not an ADR or a decision record; no accepted artifact selects its thresholds (merged-only, seven days, dirty) or its gate shape. The note's own wording on "unpushed" is ambiguous as quoted above.
- **Whether a `--check`/report gate should be a writer gate, a drift gate, or both** is undecided on file; `decisions/gates.yaml` has the vocabulary (`placement`, `enforcement: report`) but nothing for worktrees is declared there today.
- **Current worktree count and how many are merged/clean.** Not measured here (no commands); newest on file: 117 registered (2026-11-21 handover snapshot), 97 (2026-11-18 research note), 38 "finished" (same note's layer table — the difference between "97 worktrees" and "38 finished worktrees" in one note is itself unexplained on file).
- **What "the branch with it" means for branches `pr_sync.py` still protects** (a worktree branch with unpushed work is refused by the sync; a merged branch is not). The overlap of rule 6's "remove the branch" with the sync's protection list is not spelled out anywhere in the tree.
- Not read, and therefore not claimed: `scripts/pr_sync.py` source (known through `docs/WORKFLOW.md`'s refusal list), `tools/claude-code/hooks/session-scan.sh` beyond its header comment, the full trust-pyramid note beyond §§3–6, and any tracker state.

## Which files a change would have to touch

- A new removal/prune entry point under `scripts/` (nothing in `scripts/` removes an agent worktree today; the name `scripts/worktree_prune.py` exists only as a sketch in the research note).
- `Makefile` — a target beside `close-merged`/`archive`, following the same ARGS-whitelist pattern, if the house entry-point pattern (one verb per action) is kept.
- `prompts/07-commit.md` — the merge-step sequence (merge → close-merged → archive), where worktree removal would be named as a step or as its own entry point, instead of WORKFLOW.md rule 6 remaining prose-only.
- `docs/WORKFLOW.md` §3 rule 6 — the rule text any tool would implement; the loop-record sections (record keys from `git worktree list`, path-reuse rule) if removal changes what is discoverable.
- `decisions/gates.yaml` and `scripts/ci_gates.py` — only if the change declares a gate (count report / valve); the `SKRIPT_EXP` dict needs an entry for any new non-gate script, and the `OHNE_TEST` list must only shrink.
- `scripts/machine_facts.py::worktree_field` — the existing observer of the count; unchanged unless its "never pruned" caveat must change meaning.
- `scripts/kit/manifest.yaml` — carries worktree tooling into new repositories; a new script must be added there or deliberately left out.
- A new test file beside the existing pattern (`tests/test_close_merged_beads.py` is the closest analogue: executor script + dedicated test file), plus the interaction points named above if the tool must coordinate with `session-scan.sh` relations, `stage2.py` record keys, or `pr_sync.py` protections.
