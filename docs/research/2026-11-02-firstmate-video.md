---
title: "Evaluation — firstmate and no-mistakes (\"High Throughput Agentic Engineering with Kun\"), against the harness"
category: research
created: 2026-11-02
updated: 2026-11-02
last_reviewed: 2026-11-02
status: current
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [evaluation, orchestration, review, outside-practice]
---

# firstmate and no-mistakes, against the harness

The maintainer asked on 2026-11-02 what of a YouTube video could be taken
into this repository: "High Throughput Agentic Engineering with Kun"
(<https://www.youtube.com/watch?v=MSbacZ99E14>). The video shows Kun Chen's
own tool, **firstmate**, an orchestrator in which one agent ("the first
mate") dispatches and supervises other agents, and its delivery gate
**no-mistakes**. This is a first reading by one session, not the research
swarm.

## Sources and what was read

- **The video page** (read 2026-11-02 through its public HTML): title, channel
  (Kun Chen), publish date 2026-09-13, length 53:57, the description and its
  chapter list — Intro, Firstmate, First task, Remove distractions,
  Crewmates, Model routing, More tasks, Task tracking, Second mates,
  Interactive prototypes, Discord and X relay, Context window management,
  Yolo merge vs no mistakes, Giving feedback, Catching up, More decision
  making, PR with no mistakes.
- **Not read: what is said in the video.** The page lists an
  auto-generated English caption track, but fetching it returned an empty
  body, and no public transcript mirror was reachable (one returned HTTP 403;
  a web search found none for this title). The video was not watched.
  Everything below rests on the source code the description links, not on
  the talk; which chapter shows what is inferred from the chapter titles.
- **kunchenguid/firstmate** (<https://github.com/kunchenguid/firstmate>, MIT,
  created 2026-06-12, 8,507 stars on 2026-11-02), read through the GitHub API
  at commit `9224c90` (last push 2026-11-02 — seven weeks **after** the
  video; the video may show an older state): `README.md`, `VISION.md`,
  `AGENTS.md` (7,332 words; sections 1, 2, 4 and 6–14 read in full, 3 and 5
  not), `.no-mistakes.yaml`, `.tasks.toml`,
  `.github/workflows/no-mistakes-required.yml`, the skills `ask-user-authority`,
  `ahoy`, `stow` (first part), `harness-adapters/…/model-and-effort.md`
  (first part), and the header of `bin/fm-startup-memory-budget.sh`. Not
  read: the other skills, the 800-odd scripts, `docs/`, the tests.
- **kunchenguid/no-mistakes** (<https://github.com/kunchenguid/no-mistakes>,
  "git push no-mistakes", 9,098 stars on 2026-11-02): the README only. Not
  read: its documentation site, its code.

Star counts and the README's claims ("zero-token supervision", "ship with a
crew") are claims, not evidence; nothing was installed or run.

## What firstmate is, technically

firstmate calls itself an "agent distro": a cloned repository whose
`AGENTS.md`, skills and shell scripts turn any supported coding CLI (Claude
Code, Codex, Pi and others) into a supervisor. The maintainer ("captain")
talks to that one agent only. It never edits a project itself (`AGENTS.md`
hard rule 1); it writes a brief, spawns a worker in a disposable git worktree
inside a visible tmux or similar pane (`bin/fm-spawn.sh`), and a shell
watcher wakes it only on events. Work ships through one of three per-project
modes (`no-mistakes`, `direct-PR`, `local-only`) with an orthogonal `yolo`
flag that lets the supervisor merge green work on its own (`AGENTS.md` §7).
no-mistakes is a local git remote that runs review → test → docs → lint →
push → PR → CI in a disposable worktree and splits findings into auto-fix and
ask-user ones.

In shape it is close to this harness's orchestrator plus `scripts/stage2.py`:
one coordinating session, workers in worktrees, a scripted gate before the
pull request. The differences are in where authority sits and what is
scripted.

## Item by item

Measured against this repository at `ea33c818` (origin/main, 2026-11-02).

| # | Practice (where read) | Against the harness | Verdict |
|---|---|---|---|
| 1 | One liaison: workers never address the human; all reports go through the supervisor (`AGENTS.md` hard rule 4; chapter "Crewmates") | Same shape: sub-agents report to the orchestrator, which shows the maintainer a plan card unchanged (house AGENTS.md, "Communication") | **Have it** |
| 2 | The supervisor never does the work itself, "because trivial is a guess" (`VISION.md`, "Authority is explicit") | The orchestrator repairs by hand (`docs/WORKFLOW.md` §4 "Hand repairs by the orchestrator", lines 1597–1627), with three owed follow-ups | **Skip.** Hand repairs here are bounded and recorded; a hard ban would send one-line fixes through a full runner attempt (12–13 min verify, same section) |
| 3 | Disposable worktree per task, spawn refuses the primary checkout (`AGENTS.md` §7 "Dispatch") | One change, one worktree under `.claude/worktrees/` (`docs/WORKFLOW.md` §3 "Worktrees") | **Have it** |
| 4 | Teardown refuses unlanded work; `--force` only on the human's word (`AGENTS.md` hard rule 3, `bin/fm-teardown.sh`) | Worktree removal is a prose step, "after the merge, the worktree goes" (`docs/WORKFLOW.md` line 675); no script checks that the branch landed | **Adapt** as the counterpart of bead coding-harness-hs0o (one command sets up a worktree): one command removes it and refuses while the branch is not in `origin/main` |
| 5 | Model routing by dispatch profiles, ranked by remaining quota (`spendPriority`), every candidate accounted for (`AGENTS.md` §4, `quota-array-dispatch`) | ADR 0021: cheapest reachable model first by declared `anfragen_5h`, live reachability probes in `prepare-loop` | **Have the equivalent.** Ours is declared per route and probed; theirs reads a quota tool. No gain worth a second mechanism |
| 6 | Effort fallback: `low` for clear bounded work, `xhigh` for ambiguous design, **never `max`** without the human's standing preference (`model-and-effort.md`) | Per-verb Codex effort in `scripts/stage2.py:197` (`CODEX_EFFORTS`: draft high, repair medium, review high); xhigh for spec and plan (`docs/WORKFLOW.md` "Model routing") | **Have it** |
| 7 | "Never downgrade the intelligence doing the work" without permission (`VISION.md`) | `--stage2-off REASON` records why a fallback model ran (house AGENTS.md, stage 2) | **Have it** |
| 8 | Backlog item required before dispatch; spawn and teardown move the item themselves (`AGENTS.md` §7, §10) | `scripts/new_change.py` requires an existing bead (`--bead`, line 191; checked line 208–215); claim and close stay manual | **Mostly have it.** Automatic status moves would write the tracker from the runner — against house rule 4's one-writer rule in a second session. Skip |
| 9 | Persistent "second mates": whole supervisor homes with their own state, local or over SSH (`AGENTS.md` §6; chapter "Second mates") | At most `writing_sessions_per_repository` (default 2) writers, one tracker writer (house rule 4) | **Skip.** It multiplies writers, which this repository limits on purpose |
| 10 | Public relay: the supervisor answers mentions on X and Discord (README "Optional Relay"; chapter "Discord and X relay") | A leak check guards every foreign call; the customer instance is never named (house rule 6) | **Skip.** A public write channel is a new leak surface with no need here |
| 11 | Always-loaded contract with a stated ceiling of **9,000 words**; a change that crosses it must prune or move text behind a trigger (`VISION.md`, "Scripts own the mechanics"); a startup-memory budget script (`bin/fm-startup-memory-budget.sh`) | `AGENTS.md` is 2,342 words (measured at `ea33c818`) with no ceiling; nothing measures it. Whether firstmate's CI enforces its ceiling: not found in `ci.yml` by a text search — stated, maybe not enforced | **Adopt as a gate** (bounded): a test that holds `AGENTS.md` under a word ceiling the maintainer sets. Every session pays for every word; today only discipline holds it |
| 12 | Memory entries carry tier markers and decay; stale ones go to a cold archive, not deleted (`stow` skill) | Memory lives outside the repository; bead coding-harness-uzjq moves setup facts out of it | **Skip** for now; uzjq first. Decay is worth a look only once memory stays small |
| 13 | Project `AGENTS.md` grows only by deliberate human edits — "every entry taxes every agent session" (`AGENTS.md` §6) | "A standing rule belongs in the repository's AGENTS.md" — agents add it (house AGENTS.md, "Sessions across checkouts") | **Adapt, with item 11.** Keep the rule, add the cost: an addition names what it replaces or the ceiling stops it |
| 14 | Event-driven watcher wakes the supervisor; "no turn ends blind while work is under way" — a turn-end guard blocks a stop while workers run (`AGENTS.md` §8; README) | No turn-end guard; the promised stop hook `.claude/hooks/session-stop/check-tests-green.sh` is absent (known, `tests/test_workflow_entry.py:494`); lane watch is bead coding-harness-5q2p | **Note on 5q2p**: a stop hook that refuses to end a turn while a lane's background job runs and no watcher is armed. Not a new bead |
| 15 | Escalation etiquette: talk in outcomes; a table that rewrites internal terms (worktree → local copy, gate → the concrete approval); the **final message repeats every URL and open decision** (`AGENTS.md` §9) | ADR 0018 question context; bead coding-harness-0x6u (message only for decisions, finished beads, serious events); glossary bead coding-harness-il3o | **Adapt into 0x6u and il3o**: the final-message rule and an internal-term-to-plain-word table are concrete and fit both |
| 16 | `/ahoy`: recap since the human's last message, then walk through unanswered decisions one at a time, ordered by impact (`ahoy` skill; chapter "Catching up") | The 15:00 decision block (`docs/WORKFLOW.md` line 198); bead coding-harness-dmwz (check-in skill: collect, order by what unblocks most, ask one at a time) | **Have it planned** (dmwz). One detail to take: ahoy counts only decisions *visibly unanswered*, so nothing answered is asked again — dmwz already says so |
| 17 | A decision is a backlog item put on hold with a reason and an optional until-date; an answer closes it by record (`AGENTS.md` §10, `fm-captain-hold.sh`) | `[DECISION]` markers, decision pull requests (house rule 8), deferred beads | **Have it** |
| 18 | Finding authority: the supervisor decides a review finding that is unambiguous toward the accepted design, and escalates only when the fix would **expand the contract** — a new guarantee, threat model, subsystem, abstraction, compatibility surface, state machine, monitoring duty — or when same-theme findings keep propping up a questionable abstraction (`ask-user-authority` skill, "Decide" 3–4) | Evidence rule: a finding is taken when a test shows it or the spec supports it (`docs/WORKFLOW.md` lines 172–180); a second finding of one mechanism ends case repair (house AGENTS.md) | **Adopt the expansion list** (bounded): a finding the spec supports can still widen the change; the list names when the remedy goes to the maintainer instead of the repair verb |
| 19 | The human's words go verbatim into the brief's "Captain's intent"; the reviewer reads it as acceptance criteria; extra hardening is a follow-up, never scope (`AGENTS.md` §11) | Spec acceptance criteria and the interview record the maintainer's answers (`decisions.md`) | **Have the stronger form** (a spec with refutable criteria) |
| 20 | `yolo`: standing per-project permission for the supervisor to merge green work (`AGENTS.md` §7; chapter "Yolo merge vs no mistakes") | Merge only when the maintainer asks, after restating the decision block (house rule 8) | **Skip** — conflicts with house rule 8 |
| 21 | no-mistakes: review → test → docs → lint → push → PR → CI in a disposable worktree; safe fixes applied, intent-touching ones asked; a CI repair is published only if it builds on the reviewed head, else it goes back through review (no-mistakes README) | Review loop 4b, phase-6 re-check in a fresh session after repair (ADR 0017), CI from `decisions/gates.yaml` | **Have the equivalent**, with more review diversity (other model families). Not adopted as a tool: a second pipeline beside `scripts/stage2.py` |
| 22 | A required CI check that the pull request was raised through the pipeline, by signature (`.github/workflows/no-mistakes-required.yml`) | Gates check artefacts (criterion ledger, question context), not that a runner produced them | **Skip.** An attestation proves the tool ran, not that the result is right; the artefact gates already hold what matters |
| 23 | "Scripts own the mechanics, agents own the judgment; the two never mix" (`VISION.md`) | The runner is the only way to a foreign model; gates in `decisions/gates.yaml` | **Have it** |
| 24 | "Never add an agent name as a commit co-author" (`AGENTS.md` §1) | Provenance is declared with `Co-Authored-By:` or `Assisted-by:` (`prompts/07-commit.md` line 10) | **Skip** — the harness declares provenance on purpose |
| 25 | Interactive prototypes for visual decisions through a separate visual tool (`lavish-axi`, `AGENTS.md` §9; chapter "Interactive prototypes") | Prototype as an interview option is bead coding-harness-7izx | **Have it planned**; the video's demo itself was not read |

## Recommendation

1. **Word ceiling for `AGENTS.md`** (items 11 and 13) — a test, a number the
   maintainer sets (today 2,342 words), and the rule that an addition names
   what it replaces. Cheap, and it protects every session's context.
2. **Escalate a finding whose remedy expands the change** (item 18) — take
   firstmate's list (new guarantee, subsystem, abstraction, state machine,
   compatibility surface, monitoring duty) into the findings process as the
   test for "the remedy goes to the maintainer".
3. **A worktree removal command that refuses unlanded work** (item 4) — the
   pair of bead coding-harness-hs0o.
4. **Notes on existing beads, no new ones:** the final-message rule and an
   internal-term table (coding-harness-0x6u, coding-harness-il3o); a stop
   hook that will not end a turn while a lane job runs unwatched
   (coding-harness-5q2p).
5. **Not adopted:** second mates, the public relay, `yolo` merges, the
   pipeline attestation, the no-co-author rule, firstmate or no-mistakes as
   tools.

## Not done in this reading

The talk itself was not heard or read; a transcript would show whether the
video states measured throughput (the chapter "High Throughput" promises it)
or only demonstrates. Nothing was installed or run.
