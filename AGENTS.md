# coding-harness — Agent Instructions

The home of the coding workflow: **seven phases, three stages**, the session handover, the kit that carries the process into new repositories, and the research corpus behind it. This repository is the source of truth for the process; `portfolio-agentic-engineering` and `lakeswitch-ai` run instances of it.

**Status: bootstrapping.** The mechanism (WORKFLOW.md, prompts, templates,
kit scripts) migrates from `portfolio-agentic-engineering` in measured steps.
The migration plan and current state live in the bootstrap handover:
`docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`.

This is the only instruction file: Claude Code (≥ 2.1.277) reads it itself, and
a `CLAUDE.md` would silently replace it (`tests/test_entry_points.py`).

## The workflow in one screen

| # | Phase | Artifact | Gate |
|---|---|---|---|
| 1 | Explore | `plans/changes/<name>/research.md` | — |
| 1a | Interview | `decisions.md` | the class minimums met — feature ≥ 3 · ADR change ≥ 5 (feature with ADR: 5 total) · spike 3 topics or reasoned skip · bounded 1 or reasoned skip — gate `interview-minimums` |
| 2 | Spec | `spec.md` | validator green, no open `[DECISION]` |
| 2a | Spec-Review *(optional)* | lines for `findings.md`, dimension SPEC | no open `[AMBIGUITY]` |
| 2b | Design *(by class)* | `design.md` | validator green; an ADR draft when `architectural` |
| 3 | Plan | `plan.md` | validator green |
| 4 | Implement | code + tests | `make verify` green |
| 4b | Review loop *(stage 2)* | loop rows, into `findings.md` after the phase-6 verdict | rounds until a clean round — the free swarm, the Flash swarm, then the paid ladder (ADR 0021); `make verify` green after each repair |
| 5 | Verify | test output as evidence | stop-hook blocks on a red tree |
| 6 | Review | `findings.md` | no open BLOCKER — `[DIVERGENT]` counts as BLOCKER |
| 7 | Commit | pull request | CI green |

**Stage 2** (framework content, ADR 0007 as amended by ADR 0011 and ADR 0016): a foreign model is started only through `python3 scripts/stage2.py`, which runs the leak check before every call. Codex drafts spec, design and plan (`draft <change>`; GLM 5.3 after two failed attempts) and reviews 6; Opus 5.5 reviews 2a (`spec-review <change>`); the review loop (4b) runs on OpenCode Go through Pi until a clean round (ADR 0021): round 1 is the free swarm, the models the `free_stage` rule selects from a forced live catalog refresh, on the implementation diff alone with no tools; round 2 is the Flash swarm, up to three cheapest reachable admitted paid models in parallel; then one id of the `opencode-go` entry's `modelle` set per round, cheapest first: the runner orders it by the declared `anfragen_5h` (requests per 5 hours, more is cheaper); a failed Flash member is replaced by the cheapest unconsumed one. GLM 5.3 Flash explores a `bounded` change or a `spike` (a `feature` or `architectural` change goes to the research swarm, ADR 0020) and implements, and Codex repairs the findings the orchestrator takes (`repair <change>`, ADR 0017: a fresh Codex attempt after a failed post-run check, then Sonnet 5.5; phase 6 re-checks in a fresh read-only Codex session — a reviewer's own session never repairs); `explore <change>`, `draft <change>`, `implement <change>` and `repair <change>` are live;
`--stage2-off [REASON]` uses Haiku 5.5 or Sonnet 5.5 and records why when Stage 2 is off or Z.ai unavailable. A leak-check BLOCK stops without fallback. Reviews go by class, and so does phase 1 now (ADR 0020): a `feature` or `architectural` change explores through the research swarm (ADR 0020; a finder trio maps the sources, six seats research eleven topics, online topics on public sources only, Opus 5.5 reconciling; `prepare-explore <change>` first, its report shown to the maintainer, then `explore <change> --availability-reported <id>`; an aborted run resumes; the gate `research-handoff` holds interview and spec to the findings), a `bounded` change or a `spike` through GLM 5.3 Flash; `explore` reads the class from `--class` and the headers of `research.md` and `spec.md`, wherever stated, and refuses missing, invalid or disagreeing declarations (`docs/WORKFLOW.md` §4). Beyond that, explore, draft, implement and repair do not.

**Temporary GLM availability override (maintainer, 2026-10-17):** GLM through **Z.ai** (the Z.ai API and GLM inside Claude Code) is unavailable until **2026-10-21 20:34 Asia/Singapore** (12:34 UTC; 14:34 Europe/Berlin); GLM through **OpenCode Go** (Pi) works and is not affected (maintainer, 2026-10-18). Before that cutoff, do not launch GLM through Z.ai; implement with **Sol 6.1 (`gpt-6.1-sol`) or Sonnet 5.5** instead. The maintainer's Claude budget is currently exhausted, so use the active Sol session for implementation. When Claude budget is available, the Sonnet route is `stage2.py implement <change> --stage2-off "GLM unavailable until 2026-10-21T20:34+08:00"`. This temporary instruction applies to Codex and Claude Code alike; it does not change permanent model assignments or the foreign-call leak checks. After the cutoff, normal routing applies; future GLM reachability is not measured by this instruction.

Plus the session handover (the eighth movement — `docs/journal/handover/`,
`direction: framework->framework`) and the question protocol:
`[DECISION]` → human · `[GAP]` → explore, don't ask · `[DETAIL]` → agent
decides, reason into the artifact.

Before each fresh availability-enabled run, `prepare-loop` checks actual reachability with static, tool-free probes. Report its selected stages and failures in the main Claude Code or Codex conversation, then use `review-loop --availability-reported <id>`; the input-bound receipt expires after 900 seconds. Existing snapshots retain their membership.

Full doctrine: `docs/WORKFLOW.md`, in English since 2026-09-29.

## House rules

1. **The repository is English** — documents, code, identifiers, comments,
   messages, tests, commit messages and PR bodies. German is the language of
   the conversation with the maintainer and of the texts the maintainer's
   display shows at run time (`tools/claude-code/`), nothing else. German
   that is still in the tree (2026-09-29: mainly `scripts/`, `tests/` and
   `docs/governance/`) is translated in pull requests of its own, never in
   passing inside an unrelated change (bead coding-harness-yim).
2. **Beads only.** The tracker is the Dolt database under `.beads/`,
   transported via `refs/dolt/data` on origin. No rendered copy is committed:
   the hosted CI hydrates, renders once and presets `BEAD_RENDER`; every
   reader goes through `scripts/bead_render.py`. A fresh clone needs
   `tools/beads/install.sh && tools/bd bootstrap --yes` before any
   tracker-reading gate can measure.
3. **Use `tools/bd`, never bare `bd`.** The wrapper pins the version and
   refuses `init`, `migrate`, `upgrade` — the three verbs that can change the
   shared database for everyone. The prefix (`coding-harness-`) was fixed at
   init and cannot be corrected afterwards.
4. **One writer per tracker, and one exception.** While more than one
   writing session runs in a repository, the session that started first
   writes the tracker: it hands out beads, runs `tools/bd ready`, creates
   follow-up work as `discovered-from`, closes, reprioritises and links.
   Every other writing session works in a worktree of its own and writes
   exactly two things: the claim of the one bead it works on
   (`tools/bd update <id> --claim`) and its handover comment on that bead —
   nothing more (ADR 0006, lakeswitch-ai D-60). At most
   `writing_sessions_per_repository` writing sessions (default 2) run in one
   repository. Until the D-60 write guard exists, this is stated, not
   enforced: the start hook and the status line show a second session, and
   a session that is not first checks before any tracker write. After the
   writes run `tools/bd dolt push`. The push order is tracker first, git
   second: CI renders the gate from `refs/dolt/data`, so a git push that
   outruns the tracker push merges against a stand the commits claim to
   include — and goes red on exactly that gap (bead coding-harness-4t8).
   Auto-export is off, and no rendered copy is committed (bead
   coding-harness-1jg.3): a local reader renders fresh through
   `scripts/bead_render.py`. Because the diff no longer shows tracker
   changes, a pull request names in its body every bead it opens, changes
   or closes (maintainer, 2026-09-23).
5. **The handover is the file, not the chat.** Session end → a file under
   `docs/journal/handover/`. A number without its commit or date reads as a
   historical one — every count carries its cut-off.
6. **The customer instance is out of bounds.** What is needed from the
   customer instance (private, never named) travels as a *requirement*, never
   as an expression — no filename, field name, entity or layer name from there
   appears in a framework artifact.
7. **Texts carry their own meaning.** A reader without this session must
   understand every sentence; bead ids and file names go in parentheses as a
   suffix, never as the carrier of a sentence.
8. **A decision takes effect when the maintainer merges its pull request**
   (ADR 0008). A pull request touching a file `provenance.yaml` reserves for
   `human-decided` is a decision PR: title `decide(<scope>): …`, label
   `decision`, body from the decision template
   (`.github/PULL_REQUEST_TEMPLATE/decision.md`). Record an ADR answer only as
   the maintainer stated it (`python3 scripts/harness.py
   decide adr … --stated-in …`), never one of your own. Merge only when the
   maintainer asks in the conversation, after restating the decision block
   (`prompts/07-commit.md`, "The merge"); `.claude/settings.json` asks before
   every merge command it recognises — a brake, not a lock: another spelling
   passes (`docs/WORKFLOW.md`).

## Communication and session continuity

- Speak German with the maintainer; keep repository artifacts English.
- Use short, plainly worded messages with clear headings. Explain technical
  terms and identifiers at first use in every message. Lead with the main
  point and one concrete next action; show at most three immediate priorities.
  Keep optional detail separate.
- **Every question carries its context** (ADR 0018): before any options, short
  Topic; Intention (why now); Today; Repository change; Architecture change,
  in plain words, the question last on its own line. It covers every question
  — interviews, spec decisions, review ambiguities, plan cards, conversation
  — in every harness, for everyone; the reason is ADHD (`docs/WORKFLOW.md`,
  "The question protocol").
- Say what behavior changed and why it matters; mark proposed, implemented and
  tested work apart. Ask one decision at a time, with a recommendation and its
  consequence; do not re-ask settled decisions or existing permission.
- An orchestrating session shows a sub-agent's plan card to the maintainer
  unchanged; the veto stays the maintainer's (`prompts/03-plan.md`).
- At session start or after a break, read the latest relevant handover and its addenda;
  check the working tree and current PR state before acting. Begin with a short orientation:
  **Where we are / Next step / Needed from you**. Say "nothing right now" when no answer is
  needed; never make the user rebuild the chat or read the whole backlog.
- Before ending or handing over a session, maintain a dated file under
  `docs/journal/handover/`. Record the objective, completed work and evidence,
  decisions and preferences, unfinished work/blockers, branch/commit/PR,
  parallel-session ownership, and one concrete resumption action. Preserve
  prior records with a dated addendum; task status stays in Beads.
- Link the handover in the closing message; the next session resumes from it.
- A bead for a change names its class (`spike` … `architectural`) in its description (2026-10-22).

## Tracker quick reference

```bash
tools/bd ready              # open, unblocked work
tools/bd show <id>          # detail view
tools/bd create "title" -d "description" -p 1
tools/bd update <id> --claim
tools/bd close <id> --reason="…"
tools/bd prime              # full tracker context for a session
tools/bd dolt push          # push tracker data to origin (refs/dolt/data)
```

## Sessions across checkouts

- **Another session in the same checkout:** say so before changing a file,
  committing or switching the branch, and offer a worktree. House rule 4 holds
  for the tracker meanwhile.
- **Worktrees: one change, one bead, one branch, one worktree, one session.**
  A worktree lives under `.claude/worktrees/<name>`, is branched from a
  freshly fetched `origin/main`, and is removed after the merge. Sibling
  directories are retired (D-5). `tools/bd` finds the main checkout's tracker
  from there, and concurrent writers lose nothing
  (`docs/research/2026-09-23-worktree-tracker-writes.md`); who may write is
  still house rule 4, and a worker claims with `--actor <session>`. Each new
  checkout or worktree runs `make venv` and `bash tools/pi/install.sh` once before `make verify`
  (`PYTHON=` picks a 3.12+ interpreter; one that does not match the lock fails the suite, bead
  coding-harness-ei0; the Pi tests and the swarms need the pinned Pi, bead coding-harness-hs0o).
- **A text-only change (Markdown outside `scripts/`, `tests/`, `prompts/`,
  `decisions/`) skips the local `make verify`;** CI is its gate.
- **Omnigent starts inside the worktree** (`omnigent claude
  --use-native-config`, ADR 0006). Its tools that write, run, spawn or change
  state are denied by name in `.claude/settings.json`; the one that may send
  task text to a routing judge (`sys_advise_models`) is asked each time. Its
  Omnigent default policy (`tools/omnigent/`) is a second layer the maintainer
  installs; nothing depends on it alone. The one list and details:
  `docs/WORKFLOW.md` §3, "Worktrees".
- **What could not be read is "not read", never "none"** — an unopened file
  and an empty query say different things.
- **A standing rule belongs in the repository's `AGENTS.md`** — every harness
  reads it; chat, memory and a user file do not reach the next one. Where an
  agent may not write it (lakeswitch: `human-decided`), propose the text.
- **Research about this repository lives in `docs/research/`.** A vault note,
  chat or rendered page is a view of it: it names the source path and commit,
  and a finding is never first written there. Personal reasons to care stay
  outside the repository.
- **The maintainer's Claude Code display** (status line, session entry,
  handover safety net, `/handover`) lives, documented, in `tools/claude-code/`;
  change it there and reinstall with `tools/claude-code/install.sh`, never
  only in `~/.claude`.
- **Sub-agents survive a budget pause** (maintainer, 2026-10-06). Each commits
  and pushes after every green step and ends its report with a `Resume:` line;
  the orchestrator keeps a list (agent id, branch, last pushed commit, next
  step) and resumes or restarts there. One change at a time, with few agents
  and a visible queue.
- **Findings returned as text** (when the harness refuses a reviewer's write)
  are committed unchanged by the orchestrator, which says so in the commit.
  MINOR rows on tests, security or false statements are repaired without
  asking; style rows are named in the pull request as accepted limits.

## Sibling repositories

| Repo | Role |
|---|---|
| `portfolio-agentic-engineering` | framework governance (rule set, gates, ADRs, lessons), OSI→lakeswitch transfer logistics, domain content — the origin this repo migrates from |
| `lakeswitch-ai` | product repo running a clean-room instance of the workflow |
| the customer instance (private, not named) | read-only boundary for framework sessions |
