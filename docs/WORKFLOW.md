---
title: "Workflow and model routing — phases and stages"
category: governance
status: current
created: 2026-09-05
last_reviewed: 2026-09-29
updated: 2026-10-06
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-29"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [workflow, model-routing, agentic-coding, phases, artefacts]
---

# Workflow and model routing

> **Starting a session:** `make change NAME=<name> BEAD=<id>` creates
> `plans/changes/<name>/`, links it to a bead that **already exists**, and
> points to phase 1. In Claude Code: `/workflow-start`.
> Then: "Read `docs/WORKFLOW.md` and work at phase N."
> **Standing:** stage 1 is binding. Stages 2 and 3 are prepared, not active.
> **Language:** this file was German until 2026-09-29 and is English since, like
> every other artefact of this repository (`AGENTS.md`, house rule 1).
>
> **Not all of it is here yet.** This file came over from
> `portfolio-agentic-engineering`, and the mechanism follows it in steps
> (`AGENTS.md`, "Status: bootstrapping"). Checked on 2026-09-29 against the
> tree at `9f14283`, these pieces it names are **not** in this repository:
> `scripts/validate_change_artefacts.py`, the sub-agents
> `.claude/agents/explorer.md` and `reviewer.md`, the stop hook
> `.claude/hooks/session-stop/check-tests-green.sh`, `.claude/commands/`, the
> targets `make change` and `make index` (the entry is `python3 scripts/new_change.py <name>
> --bead <id>`), `tests/test_repo_settings.py`, `templates/findings.md`,
> `templates/plan-marking.md`, `scripts/run_change.sh`, the `scripts/cc-*.sh`
> profiles and `tests/test_model_profiles.py`. Where the text below says one of
> them does something, it describes the target, not this tree.
>
> One thing is missing on purpose and is not on that list: the brakes on the
> irreversible (force push, `rm -rf`, deploys) in `.claude/settings.json`, which
> holds only the Omnigent rules. This repository deploys nothing, and a `Bash`
> pattern for a force push is passed by the next spelling, so they were left out
> by decision, not deferred; §3, item 3, gives the reason.

## 1 · Why

How work is done with agents in this repository, and which model gets which
phase. The cut is made so that **stage 1 is productive at once** and the later
stages sit on top of it without a rebuild.

Two decisions underlie everything.

**Harness portability.** Everything of value lives in repository files and
standard tooling: `AGENTS.md`, the artefacts under `plans/`, the phase prompts
under `prompts/`, `Makefile`, git hooks, CI. What is harness-specific —
`.claude/agents/`, `.claude/commands/`, `.claude/hooks/` — is a thin comfort
layer you throw away. Moving to another harness keeps the core; what has to be
rebuilt is the sub-agent definitions, the slash-command wrappers and the hooks.

**Deterministic outside, model in the middle.** Discovery and inventory are
mechanical. The model sits in the interpretation and design layer. Generation
and verification are deterministic again and repeatable at will. Between the
layers sit gates, and gates are not negotiated.

## 2 · The phases

Each produces one versioned artefact in the repository. **The artefact is the
handover to the next phase — not the chat history.**

| # | Phase | Artefact | Gate | Prompt |
|---|---|---|---|---|
| 1 | Explore | `plans/changes/<name>/research.md` | — | [`prompts/01-explore.md`](../prompts/01-explore.md) |
| 1a | Interview | `plans/changes/<name>/decisions.md` | every `[DECISION]` answered — or its skip given a reason | [`01a-interview.md`](../prompts/01a-interview.md) |
| 2 | Spec | `plans/changes/<name>/spec.md` | validator green, no open `[DECISION]` | [`02-spec.md`](../prompts/02-spec.md) |
| 2a | Spec review | rows for `findings.md`, dimension `SPEC`; then the revised `spec.md` | every row worked into the spec or rejected with a reason; no open `[AMBIGUITY]` | [`02a-spec-review.md`](../prompts/02a-spec-review.md) |
| 3 | Plan | `plans/changes/<name>/plan.md` | validator green | [`03-plan.md`](../prompts/03-plan.md) |
| 4 | Implement | code + tests | `make verify` green | [`04-implement.md`](../prompts/04-implement.md) |
| 5 | Verify | test output as evidence | the stop hook blocks on a red tree | [`05-verify.md`](../prompts/05-verify.md) |
| 6 | Review | `plans/changes/<name>/findings.md` | no open `[AMBIGUITY]`, no open BLOCKER — `[DIVERGENT]` counts as a BLOCKER | [`06-review.md`](../prompts/06-review.md) |
| 7 | Commit | pull request | CI green | [`07-commit.md`](../prompts/07-commit.md) |

Phase 1a is **optional and called by a person**. What fits in one sentence needs
no interview; skipping it is given a one-sentence reason in `decisions.md`, not
left unsaid.

Across all of them runs the **session handover** — it belongs to no phase but to
the end of a session; see below.

### Who decides what

The person is the **owner of the intent**, not the technical reviewer. Whether
something is built right is answered by verify, review and CI — not by them.

| Level | Example | Decides |
|---|---|---|
| **Intent** | May the import overwrite old data? · Is downtime acceptable? · external contracts, accepting a risk | **the person** |
| **Mechanics** | library, algorithm, data structure — derivable from `research.md` and `spec.md` | **the model** |
| **Detail** | a variable name, formatting, an order — revisable at will | **the agent**, with the reason in the artefact |

From this follows the separation that shapes the gates: **a phase gate checks
whether the artefact is there and complete — a machine can do that, and since
`validate_change_artefacts.py` one does.** What reaches a person is only what is
actually open. The gate becomes more mechanical, not more bureaucratic.

### The findings process

A review result is a table, not prose — its form and vocabulary, severities
(`BLOCKER`/`MAJOR`/`MINOR`) included, live in
[`templates/findings.md`](../templates/findings.md) and are not kept twice here.
Without a fixed form a review round cannot be resumed, and nobody sees whether a
finding comes from the build or from the repair before it.

Two columns carry more than they seem to. **Dimension** separates `SPEC`
(measured against the spec) from `MAINT` (a stranger's view of error handling,
edge cases and external contracts) — a spec does not see its own gaps.
**Origin** records whether a finding existed before (`base`) or was produced by a
repair round (`fix-r<N>`); two consecutive rounds of `fix-r` origin are an
escalation, not a third round. That is the mechanical form of what four repair
rounds showed: every defect of rounds two to four came from a rebuild, none from
a small change.

**Disagreements are recorded, not resolved.** That one reviewer flags something
and another does not *is* the information; netting it into one verdict throws it
away.

### The question protocol

Every open point is sorted **before** anything is asked:

```
[DECISION] → person   irreversible · an external contract · a risk · or two
                      plausible readings of what was asked for
[GAP]      → explore  answerable from the repository → add it to research.md; do not ask
[DETAIL]   → agent    revisable at will → decide, and write the reason into the artefact
```

Whoever cannot give a recommendation has a gap in knowledge, not a decision, and
reads first. A question about mechanics put to the owner of the intent breaks
the protocol; it is not thoroughness. An earlier session failed exactly there,
asking questions that lay too deep technically to be answerable.

The form of a question to a person is set out in
[`prompts/02-spec.md`](../prompts/02-spec.md): the goal in one sentence, the
options as **consequences** rather than mechanisms, a recommendation with its
reason, and what happens if the answer is "ok". That is the decision record
(MADR) in the form of a question.

**An ambiguity is not mechanics.** "The plan is the contract" governs departures
from an *unambiguous* contract. Where the plan allows two readings, nothing is
chosen: the note is `[DECISION]`, the rest is finished, then stop.

### The eighth movement: the session handover

The seven phases are the cycle of **one change**. The session handover runs
across it: it closes **one session**, and a session seldom ends where a change
ends. Context full in phase 4, the end of the day between spec and plan, a review
waiting overnight — each time the next reader is a session without memory.

| When | Artefact | Gate |
|---|---|---|
| end of a session, whatever the phase | `docs/journal/handover/<date>-<name>.md` after [`templates/handover.md`](../templates/handover.md) | frontmatter against `scripts/handover_schema.py`; direction, provenance and the goal's standing are required |

The same two rules hold as for the phase artefacts, for the same reason:

**The handover is the file, not the chat.** What stands only in the history has
not happened for the next session. The reason is the same as for `/clear`
between phases 3 and 4 — except that here nobody has the choice.

**Every number carries its cut-off.** A handover ages by design; it is appended
to, never overwritten. A number without a commit or a date reads, next time, as a
current measurement and is a historical one — the most common way a history
document turns into a false statement.

### The five rules that make the difference

**`/clear` between phases 3 and 4.** The plan is a file. Whoever implements it
does not need the planning context, only `plan.md` and `spec.md`. Fresh context
beats continuity. From about 60 % context use, start a new session anyway.

**Never plan what one sentence describes.** A typo, a rename, an obvious fix: do
it. Otherwise the phase overhead eats the benefit, and the workflow is
experienced as bureaucracy instead of a tool.

**The plan is the contract.** Where the implementation departs from it, the plan
is *revised* — never silently overwritten. The agent stops and reports: expected
/ found / why it matters / what now. A departure that lives only in the code is,
at the next reading, no longer a departure but the plan.

**A gate is sensible, proportionate and more than an end in itself.** Its
checklist stands once, in
[`gate-catalog.md`](governance/gate-catalog.md#bevor-ein-gate-scharfgestellt-wird)
— not kept twice here, with a gap that has cost this file once already. Only the
gates of phase 2 and phase 3 are pure presence checklists — *is it there?* —, run
as one line that ends with the next step, by `validate_change_artefacts.py`.
Phase 4 asks `make verify` (red is red), phase 5 the stop hook, phase 6 the
comparison against `spec.md`, phase 7 the CI — four verdicts, not presence
checks: a red run is not "not there" but the gate taking hold. Open decisions
are something else: sort first, then ask. What is reversible is decided and
written into the artefact with its reason; the veto is one word. What is
irreversible is asked — as a question with a decision aid, in the form from
[`02-spec.md`](../prompts/02-spec.md). None of this is invented here: Stage-Gate
(Cooper) gives every gate the option *kill*, PRINCE2 steers by exception within
tolerances set in advance, and the reversible/irreversible distinction is Bezos's
two-way against one-way door.

**Texts for people carry their own meaning.** A question, a finding, a pull
request text, a commit body is read by someone who did not see the session and
does not have the artefacts open beside it. Bead ids, spec items and invariant
numbers are the writer's shorthand — a trailing aside in parentheses, never the
carrier of the sentence. The test: a sentence that makes sense only with
`plan.md` beside it is rewritten. That is Nielsen's second and sixth heuristic —
the user's language, recognition rather than recall — and the form of the
question is that of the decision record (ADR/MADR): context, options with
consequences, a recommendation.

### Artefact lifecycle

```
plans/specs/<capability>/spec.md          LIVING      — what should hold today
plans/changes/<name>/                     ACTIVE      — one change in flight
plans/changes/archive/YYYY-MM-DD-<name>/  HISTORICAL  — closed
docs/adr/NNNN-title.md                    PERMANENT   — append-only
```

Two separate status fields: `status` moves when the project decides;
`implementation_status` when the code moves. One field for both cannot say
whether an accepted spec is still unbuilt or whether built code rests on a
withdrawn spec — and those are exactly the interesting cases.

On close: the delta into the living capability spec, permanent architectural
decisions as an ADR, the rest into the archive. **An implemented feature spec
does not stay as a living document** — the code and the git history are the
truth. Details in [`plans/_README.md`](../plans/_README.md).

The **rule against making a second one** stands verbatim in `AGENTS.md`, because
an agent does not necessarily read `plans/_README.md`: before an artefact is
created, search with `rg` first; where one exists, it is updated. `make
staleness` checks the consequences — missing frontmatter, contradictory status,
done and never archived, one-sided supersession.

### Change classes, the ADR question and decision pull requests

Every change says in its spec header what kind of change it is — `class:`,
one of four:

- `spike` — answers a question; its output is a recommendation.
- `bounded` — changes an existing, readable flow without deciding anything new.
- `feature` — a self-contained deliverable that changes what the system must
  do or how it is checked.
- `architectural` — a new subsystem or a break of an interface; it carries its
  ADR already, so it is not asked.

**Only a `feature` owes an answer to the ADR question:** is this change an
architecture decision that needs an ADR? The spec author proposes, in the same
header: `change: <folder name>` and `adr_question: {proposed: "yes"|"no",
reason: "<one sentence>"}` (`prompts/02-spec.md`). The proposal only proposes.
The maintainer answers, and the answer lives in
`decisions/answers/<change>/adr.yaml`, in the format of the LakeSwitch pilot
(`schema_version: 1`), so LakeSwitch reads it unchanged.

There are two ways to answer, both through `python3 scripts/harness.py decide
adr`:

1. **Typed in a terminal** by the maintainer: the command shows each open
   question with its title, anchor and proposal, takes `y` or `n` and a
   one-sentence reason, and asks for three explain-back lines at the end.
2. **Stated in the conversation**, and recorded by the agent exactly as stated,
   one change per run: `--change <name> --answer yes|no --reason "<English
   sentence>" --stated-in "<where the maintainer said it>"`. The source goes
   into the commit message, not into the answer file.

Either way the command writes the answer files and a commit message, and
stages, commits and merges nothing. The gate `adr-answers`
(`scripts/check_adr_answers.py`, in `decisions/gates.yaml`) holds every
feature, active or archived, to an answer file that exists, has the format and
names its own change.

**A decision takes effect when the maintainer merges its pull request**, or
asks an agent in the conversation to merge it. There is no commit signing in
Coding Harness (ADR 0008, 2026-09-30). A pull request that adds, changes or
removes a file `provenance.yaml` reserves for `human-decided` — an ADR, an ADR
answer, the rule set — is a **decision pull request**: its title is
`decide(<scope>): <the decision as a statement>`, it carries the label
`decision`, and its body begins with the block from
`.github/PULL_REQUEST_TEMPLATE/decision.md` — what is decided, that the merge
is the confirmation, what it confirms, the options and what follows. Every
other pull request takes `.github/pull_request_template.md`, whose first lines
say that nothing is decided. How an agent merges on request is in
`prompts/07-commit.md`, "The merge".

What this does not do:

- The gate holds existence and format only. It cannot see who wrote an answer
  or who merged it.
- Agents act under the maintainer's GitHub account, so nobody can tell from
  GitHub who pressed merge. The merge rule is a rule, not proof.
- The ask rules in `.claude/settings.json` are a brake against an accidental
  merge, not a lock: they match a command's text, and another spelling passes
  them — `curl` against the API, the web page, `gh` run through `sh -c '…'`,
  by an absolute path or from a script file, a flag of the merge moved before
  `merge` (`gh pr --squash 54 merge`), a GraphQL merge mutation read from a
  file (`gh api graphql --input <file>` or `-F query=@<file>`), and an alias
  set by `gh alias import` or by editing gh's own config file.
- Nothing checks that the class is right, that a "yes" is followed by an ADR,
  or that a decision pull request carries its label and block. The review
  before the merge holds them.
- The upgrade, if an agent is ever found deciding on the maintainer's behalf:
  agents under a bot identity of their own, and branch protection that asks for
  an approval by someone other than the pusher.

## 3 · Stage 1 — only Claude Code, only Anthropic

### What stands in the repository for it

| Piece | Where | What it does |
|---|---|---|
| Instructions | `AGENTS.md` | the one source and the only file; Claude Code reads it itself since 2.1.277, no `CLAUDE.md` beside it |
| Artefacts | `plans/` | `specs/` · `changes/` · `changes/archive/` |
| Phase prompts | `prompts/` | independent of the harness |
| Entry commands | `Makefile` | `change` · `verify` · `gates` · `test` · `staleness` · `index` |
| The call | `scripts/new_change.py` | creates the change folder; requires an existing bead, creates none |
| Hygiene | `scripts/plans_registry.py` | `--check` reports, `--index` writes `plans/INDEX.md` |
| Sub-agents | `.claude/agents/explorer.md`, `reviewer.md` | read-only, model pinned |
| Stop hook | `.claude/hooks/session-stop/check-tests-green.sh` | blocks the end of a turn on a red tree |
| Enforcement | `decisions/gates.yaml` | **the one gate list** (D-10); `.github/workflows/ci.yml` is generated from it |
| Decisions | `scripts/check_adr_answers.py`, `scripts/harness.py`, `.github/PULL_REQUEST_TEMPLATE/decision.md` | the gate `adr-answers`; `decide adr` records the maintainer's ADR answers; the decision pull request's block |

### Verification runs through git and CI, not through the harness

```bash
make verify     # every locally runnable gate — the same the CI runs
make gates      # what the CI runs, read from decisions/gates.yaml
make staleness  # hygiene of the plans/ artefacts
make index      # regenerate plans/INDEX.md
```

`make` holds **no list of its own**. It calls `scripts/verify_all.sh`, which asks
`scripts/ci_gates.py`, which reads `decisions/gates.yaml` — the same file
`ci.yml` is generated from, and a hand edit of `ci.yml` fails the `ci-drift`
gate. A second list is the reason local runs and CI drift apart — not its
symptom.

The stop hook is the comfort layer, not the enforcement. It runs only when
Python was touched since `HEAD`: a hook that costs a minute when nothing has
happened is switched off within a week — and a switched-off hook is worse than
none, because the registry keeps counting it as protection.

### Model routing

| Phase | Model | Why |
|---|---|---|
| 1 Explore | **Haiku 4.5** | much input, little output, no deep reasoning |
| 1a Interview | **Fable 5.1** | the questions are the work, and there are few of them |
| 2 Spec | **Opus 5.5** | effort `xhigh`; the highest reasoning demand, little output |
| 2a Spec review | **Opus 5.5** (until stage 2 is live) | a fresh context that does not know the author's reasoning; see below |
| 3 Plan | **Opus 5.5** | effort `xhigh`; an error here is the most expensive in the whole run |
| 4 Implement | **Sonnet 5** | a solid worker given a clear plan |
| 5 Verify | — | deterministic |
| 6 Review | **Opus 5.5** (until stage 2 is live) | finds what Sonnet misses, and reads the code a change calls instead of trusting its docstring; see below |
| 7 Commit | **Haiku 4.5** | cheap and sufficient |

Switch with `/model fable`, `/model sonnet`, `/model opus`, `/model haiku`. The
alias `opusplan` runs Opus while planning and switches to Sonnet for execution —
the cheaper variant to Fable.

**Spec and plan on Opus 5.5 at effort `xhigh`** (maintainer, 2026-09-29, for
the whole repository; until then both ran on Fable 5.1). In a session:
`/model` and `/effort xhigh`; for a phase run as its own session:
`claude --model claude-opus-5-5 --effort xhigh`. A sub-agent takes its effort
from its definition's frontmatter (`effort: xhigh`), not from the call that
starts it, and a new definition is read only when a session starts.

**Spec review and review on Opus 5.5, until stage 2 is live** (maintainer,
2026-09-30, for the whole repository). From 2026-09-29 both ran on Fable 5.1,
and before that on Opus 5. Once stage 2 is implemented and merged (bead
coding-harness-bc9), the stage-2 routing replaces this row. The cost is
known: the spec review now reads with the same model as the spec's author
(Opus 5.5), so what stays independent is the fresh context, not the error
profile.
**The spec review improves the spec first.** The spec's author works each 2a
row into `spec.md` (or rejects it with a reason) before phase 3; the revised
spec is the one yardstick for plan, code and review (`prompts/02-spec.md`,
"After the spec review"). **One reviewer for both:** phase 6 resumes the session
of phase 2a (`--session-id` there, `--resume` here; the id stands in
`findings.md`). It measures the code against the revised spec and first checks
that its 2a rows arrived there. It still never saw the author's reasoning, and
passing the spec in 2a is no argument in phase 6.

**Cost logic.** The expensive models run only in the phases with little output.
The token-heavy part runs on Sonnet.

**Check after setup.** There are reports that the `model:` field in sub-agent
definitions is ignored and sub-agents run on the parent model. Look once with
`/status` — otherwise exploration is billed at Opus prices.

**Escalation.** After two failed review rounds, move up to Fable. For rebuilds
over ~200k tokens and for code touching security or concurrency, start on Fable.
After a passed review, back to Sonnet.

### What deliberately does not happen in stage 1

No `ANTHROPIC_BASE_URL`, no router, no gateway. No framework overlay —
understand the bare process first. No deep sub-agent nesting. No embedding or
graph index: `rg` plus good naming plus the generated `plans/INDEX.md` carry a
repository up to about 50,000 lines.

**Corrected on 2026-09-06:** this paragraph used to forbid worktrees and
parallel work. Both were wrong. `bd worktree create` is a command of the
tracker, and its own help names *"multiple agents or features"* sharing one bead
database as its purpose; several worktrees hang off this repository's main
checkout — `git worktree list` gives the number, and it does not belong in a
doctrine. A rule that forbids what the tool offers and the practice does daily
is not followed — it is read past, and the rest of the paragraph with it.

### Worktrees — one per change

Written 2026-09-29 from D-5 (worktrees in the repository, through the tool's own
mechanism), ADR 0006 (parallel work, one worktree per session) and the
measurement of 2026-09-23 (`docs/research/2026-09-23-worktree-tracker-writes.md`).
The same rule holds in `lakeswitch-ai`, with the differences its
`docs/workflow.md` §9 lists.

1. **One change, one bead, one branch, one worktree, one session.** Two sessions
   never share a worktree, and nobody switches the branch of the main checkout
   while another session runs.
2. **In the repository, under `.claude/worktrees/<name>`.** That directory is in
   `.gitignore` already, and it is where Claude Code puts its own worktrees
   (`claude --worktree <name>`, and a sub-agent's `isolation: worktree`). By
   hand: `git fetch origin && git worktree add -b <branch>
   .claude/worktrees/<name> origin/main`. `bd worktree create` works as well but
   writes the worktree's path into the tracked `.gitignore`, which is one more
   change in the diff. Sibling directories beside the repository are retired
   (D-5); worktrees that still sit there are finished and removed, not moved.
3. **Always from a freshly fetched `origin/main`.** A worktree on a stale base
   produces a pull request that is behind before it opens.
4. **The tracker needs nothing.** `tools/bd` in a worktree finds the main
   checkout's tracker through the shared git directory — no variable, no
   redirect file, no copy. Concurrent writers lose nothing and a contested
   claim has exactly one winner (measured 2026-09-23 with bd 1.3.0). Who may
   write is house rule 4: the first writing session writes the tracker; every
   other session claims its one bead with `tools/bd update <id> --claim
   --actor <session>` and leaves its handover comment on that bead, nothing
   more. After tracker writes: `tools/bd dolt push` first, `git push` second.
5. **Omnigent starts inside the worktree.** Omnigent runs Claude Code as its
   authors intend (`omnigent claude --use-native-config`, ADR 0006); the session
   is started from the worktree's directory, so its hooks, its
   `.claude/settings.json` and `tools/bd` all resolve there. Omnigent's own
   tools reach the session as `mcp__omnigent__<tool>`, and neither Claude
   Code's path rules, the hooks on its file tools nor Omnigent's own Claude Code
   hook see what they do. Each one that writes, runs, spawns or changes state is
   therefore denied by name in `.claude/settings.json`; the read-only ones stay
   usable, except one that may send the task text to a routing judge
   (`sys_advise_models`), which the user is asked about each time
   (`permissions.ask`; decision of 2026-09-29). The one list, with a reason per
   tool, is `scripts/omnigent_policy.py`.
   An Omnigent default policy rendered from the same list (`tools/omnigent/`)
   refuses the denied ones and asks about the asked one server-side for every Omnigent session on the machine. The
   maintainer installs it, and nothing here depends on it alone (ADR 0006); as of
   2026-09-29 it is built but not installed. Omnigent's bridge runs its own
   `sys_os_*` tools without any policy while its relay does not advertise them,
   and there only the rule in `.claude/settings.json` holds. Not yet measured: whether `omnigent claude`
   started inside a worktree keeps that directory as the session's working
   directory in every case.
6. **After the merge, the worktree goes.** `git worktree remove
   .claude/worktrees/<name>` and the branch with it. A worktree nobody works in
   is a place where a later session finds an old state and takes it for the
   current one.

Isolation between sessions is a working agreement, not a wall: worktrees share
git's refs, hooks and configuration (`docs/architecture/2026-09-17-gap-analysis.md`).
What really does not happen is simultaneous writing *to the same change* — that
is not a tool question but a division of work.

**What isolation consists of here** — three things, no fourth:

1. **The worktree.** Separates the files. One `git worktree add` per change;
   what goes wrong there does not touch the main checkout.
2. **The harness's sandbox.** Separates execution. It is a property of the
   environment, not an artefact in this repository — there is nothing to
   install and nothing to configure.
3. **`permissions.deny` in `.claude/settings.json`.** It holds two things:
   Omnigent's writing tools (item 5 above) and
   `Edit(//**/.omnigent/config.yaml)`, so no session rewrites the policy that
   holds them. The template's brakes on the irreversible — production deploy,
   `bundle destroy`, force push, `rm -rf`, writes under `docs/decisions/` — are
   not in it: this repository deploys nothing, has no `docs/decisions/`, and a
   `Bash` pattern for a force push is passed by the next spelling. Deny survives
   every permission mode, `bypassPermissions` included. An `Edit(…)` rule reaches
   Claude Code's file tools, the file commands it recognises in `Bash` (`sed`,
   `tee`) and redirect targets (`>`, `>>`), not a program that opens files itself
   (`python -c …`) and not a tool Claude Code does not own — which is why
   Omnigent's tools are denied by name. That is a brake against accidents, not a
   lock against intent; whoever takes it for a lock relies on something that does
   not exist.

**No container belongs to it.** Neither `container-use` nor Dagger nor a
devcontainer is an operating resource of this repository; the concept document
on Dagger describes a technique, it does not use one.
`tests/test_repo_settings.py` holds the fence: a tracked `Dockerfile`,
`devcontainer.json`, `dagger.json` or `docker-compose*` fails the suite.

## 4 · Stage 2 — adding GLM and Kimi (prepared, not active)

Exactly two rows of the routing table change: **implement** moves from Sonnet 5
to GLM, **review** from Fable 5.1 to Kimi. Phases 1–3 and 7 stay with Anthropic.

**Why review across vendors.** Different training lineages have blind spots that
do not overlap. Separating the context already finds measurably more errors;
vendor diversity adds to it. A model rates its own output too kindly — a
reviewer from another house does not know, by construction, that it is checking
itself. **Disagreements are recorded, not resolved automatically.** "Kimi
flagged it, GLM did not" is the information.

### Mechanics

`ANTHROPIC_BASE_URL` holds for a whole session and cannot be switched in the
middle of one. A profile is therefore a process, not a switch: six scripts under
`scripts/cc-*.sh` over one shared base, each starting its own session. Every
`ANTHROPIC_*` variable is set explicitly — a child process would otherwise
inherit the parent profile's and keep working, only against the wrong vendor.
`tests/test_model_profiles.py` measures that with a stand-in instead of
believing it.

**The barrier without which nothing runs:** `make leakcheck NAME=<change>` scans
the change's artefacts and the diff against the base before anything goes to a
foreign endpoint. Every foreign profile calls it itself and stops when
`CC_CHANGE` is missing — without a named change there is nothing to scan. The
denylist lives outside the repository; if it is missing, that is BLOCK, because
unchecked is not the same as clean.

**The assignment stands in the plan.** Every step carries exactly one marking —
`[FLASH]`, `[GLM5.3]` or `[SONNET]`, decision rules in
[`templates/plan-marking.md`](../templates/plan-marking.md).
`scripts/run_change.sh` groups consecutive equal markings into one segment and
runs each as a session of its own with a verify gate after it. An unmarked line
is ignored, not guessed: the incomplete plan is then a finding at the plan gate,
where a person accepts it, not a surprise at run time.

The orchestrator holds **no second rule set**. The worktree precondition, the
leak check, `make verify` and the artefact gate live outside it and are called.
An open `[AMBIGUITY]`, an open BLOCKER or MAJOR finding pause with exit 2 instead
of being decided.

### Seeing agents that wait

Neither a terminal multiplexer nor an agent layer isolates anything. Isolation
comes from the worktree, the harness sandbox and `permissions.deny` (see above).
What is missing is something else: **visibility of waiting** — the moment an
agent has asked a `[DECISION]` and stands still.

`--mode herdr` uses [herdr](https://github.com/herdrdev/herdr) for that, which
knows four agent states — `working`, `blocked`, `done`, `idle` — and reads them
for Claude Code through integration hooks rather than by parsing the screen.
`blocked` is exactly what the question protocol produces; with several parallel
runs, one glance shows which one waits for a person.

**It is the person's tool, not a dependency of the workflow.** If the binary is
missing, the orchestrator carries on headless and says so. A young tool must not
stop operation by not being installed — and the landscape of these tools is
young: of the orchestrators common in 2026, several are already discontinued or
have passed into volunteer maintenance. The handover runs through files — the
foreign session starts with `@plans/changes/<name>/plan.md
@plans/changes/<name>/spec.md` and needs nothing else. That is what the plan
being a file is for.

> **Two caveats, and the second one holds here in particular.** The vendors'
> coding subscriptions are contractually limited to officially supported tools;
> in Claude Code that is covered, in a self-built harness it is not.
>
> **And: this repository contains abstracted knowledge from a productive
> customer project.** No customer names, schemas, entity names or figures go to
> endpoints outside one's own jurisdiction — not in a diff, not in a plan
> either. Whoever switches stage 2 on checks beforehand what stands in
> `spec.md` and `plan.md`. The denylist from the export tool is the right
> measure for that.

## 5 · Stage 3 — a meta-harness (evaluative)

Replaces not the process but the manual session juggling of stage 2: an agent
becomes a short YAML file that references `AGENTS.md` as `instructions:`,
switches vendor in one `harness:` line and takes the phase roles from `prompts/`
one to one. An orchestrator spreads the implementation across parallel worktrees
and routes each diff automatically to a reviewer from another vendor. Policies
can enforce `make verify` as a hard gate and cost budgets in the middle of a
session.

Not set to production.

## 6 · The order, and why it is that order

**Process, then model diversity, then orchestration.**

Start with orchestration and you debug infrastructure instead of the workflow,
and with bad results you cannot tell whether plan, model or harness was at
fault. Start with multiple vendors before the artefact handover works and you
lose context at the switch and blame the model.

Stage 1 must have run for two to three weeks in real use. **The signal to move
on:** the phase gates hold without anyone thinking about them, and the Sonnet
implementation is the noticeable cost.

## 7 · What survives each stage

| Piece | Stage 1 | Stage 2 | Stage 3 |
|---|---|---|---|
| `AGENTS.md` | ✅ | ✅ unchanged | ✅ as `instructions:` |
| `plans/` artefacts | ✅ | ✅ unchanged | ✅ unchanged |
| `prompts/` | ✅ | ✅ as text | ✅ as YAML prompt |
| `Makefile`, CI, git hooks | ✅ | ✅ unchanged | ✅ as a policy gate |
| `.claude/agents/` | ✅ | ❌ rebuild | ❌ replaced by YAML |
| `.claude/commands/` | ✅ | ❌ rebuild | ❌ replaced by YAML |
| Claude Code hooks | ✅ | ❌ rebuild | ❌ replaced by policies |

The lower half is thin on purpose. That is the price paid once, and the reason
the upper half survives the change.

## 8 · Departures from the template — and why

These points depart deliberately from the original handover. They stand here so
that the departure stays a decision and is not read as an oversight.

| Template | Here | Why |
|---|---|---|
| `Makefile` with `lint`, `typecheck`, `test` | `make verify` calls only `verify_all.sh` | `decisions/gates.yaml` is the one gate list (D-10). A check sequence spelled out in the Makefile **would be** the second list. |
| `ln -s AGENTS.md CLAUDE.md` | no `CLAUDE.md` | Since Claude Code 2.1.277, `AGENTS.md` is read directly as soon as no `CLAUDE.md` lies in the tree (maintainer decision, 2026-09-22). Conversation language and slash commands live in the user configuration, not in the repository. A known limit: the direct reading is a feature flag and fails with telemetry switched off, Bedrock/Vertex or an own `ANTHROPIC_BASE_URL` — then Claude Code reads nothing; for the Omnigent target (telemetry off) that has to be checked before M1. |
| `.pre-commit-config.yaml` | not created | It would be a second lint list beside `decisions/gates.yaml`, with the same risk of drift. Enforcement lies with the gate list and the CI generated from it. |
| `.mcp.json` | not created | This repository uses no MCP server today. An empty configuration would be a claim without content. |
| `uv`, `mypy` | `python3`, `ruff`, `pytest` | That is the toolchain pinned in `requirements-ci.txt` and run by the CI. `uv` only compiles that lock from `pyproject.toml` (`make lock`); CI and `make venv` install it with pip, and nothing calls uv to install. The local runner (`scripts/verify_all.sh`) installs nothing: it takes `$PYTHON` if that is set, otherwise the first of the checkout's `.venv/bin/python3` and the `python3` on `PATH` that imports PyYAML, and exits 2 when none does. |
| task tracking in the artefact | Beads (`bd`) | `AGENTS.md`: Beads only. The artefacts say **what** is built, the tracker says **where it stands**. |

## 9 · Standing and next thresholds

Stage 1 is set up. What is still outstanding belongs to a person:

- Check `/context` and `/status` once: does `AGENTS.md` load, does the
  sub-agents' model assignment take hold?
- Send the first real task through all seven phases and force spec and plan as
  files — not as chat.
- After two weeks, audit `plans/`: are there contradictory or orphaned
  artefacts? `make staleness` answers the mechanical part of that.

**Thresholds that change course.** Above about 30 artefacts, tighten archiving.
If the model repeatedly fails to find files despite good naming, add an LSP MCP
server — and only when that is not enough, think about a semantic index.
