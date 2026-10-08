---
title: "Workflow and model routing — phases and stages"
category: governance
status: current
created: 2026-09-05
last_reviewed: 2026-09-29
updated: 2026-10-08
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
> **Standing:** stage 1 is binding; stage 2 is active for framework content,
> by change class, since ADR 0007 (§4); stage 3 is not.
> **Language:** this file was German until 2026-09-29 and is English since, like
> every other artefact of this repository (`AGENTS.md`, house rule 1).
>
> **Not all of it is here yet.** This file came over from
> `portfolio-agentic-engineering`, and the mechanism follows it in steps
> (`AGENTS.md`, "Status: bootstrapping"). Checked on 2026-09-30 against the
> tree at `41abf42`, these pieces it names are **not** in this repository:
> `scripts/validate_change_artefacts.py`, the sub-agents
> `.claude/agents/explorer.md` and `reviewer.md`, the stop hook
> `.claude/hooks/session-stop/check-tests-green.sh`, `.claude/commands/`, the
> targets `make change` and `make index` (the entry is `python3 scripts/new_change.py <name>
> --bead <id>`), and `docs/governance/gate-catalog.md`.
> Where the text below says one of them does something, it describes the
> target, not this tree. Since 2026-10-05, `tests/test_repo_settings.py`
> exists: it asserts the branch ruleset (rule RB-M6); the container fence §3
> describes is not in it yet.
>
> One thing is missing on purpose and is not on that list: the brakes on the
> irreversible (force push, `rm -rf`, deploys) in `.claude/settings.json`, which
> holds the Omnigent rules, the ask rules of the merge guard (§2) and the ask
> rule on `codex` (§4), and no such brake. This repository deploys nothing, and
> a `Bash` pattern for a force push is passed by the next spelling, so they were
> left out by decision, not deferred; §3, item 3, gives the reason.

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
| 1a | Interview | `plans/changes/<name>/decisions.md` | the `interview-minimums` check — the class minimums met, or a skip record with a reason | [`01a-interview.md`](../prompts/01a-interview.md) |
| 2 | Spec | `plans/changes/<name>/spec.md` | validator green, no open `[DECISION]` | [`02-spec.md`](../prompts/02-spec.md) |
| 2a | Spec review | rows for `findings.md`, dimension `SPEC`; then the revised `spec.md` | every row worked into the spec or rejected with a reason; no open `[AMBIGUITY]` | [`02a-spec-review.md`](../prompts/02a-spec-review.md) |
| 2b | Design *(by class)* | `plans/changes/<name>/design.md` | validator green; for an `architectural` change, an ADR draft in it | [`02b-design.md`](../prompts/02b-design.md) |
| 3 | Plan | `plans/changes/<name>/plan.md` | validator green | [`03-plan.md`](../prompts/03-plan.md) |
| 4 | Implement | code + tests | `make verify` green | [`04-implement.md`](../prompts/04-implement.md) |
| 4b | Review loop *(stage 2)* | the loop rows — outside the repository until the phase-6 verdict, then in `findings.md` (`release-loop`) | at most two rounds; `make verify` green after each repair | [`04b-review-loop.md`](../prompts/04b-review-loop.md) |
| 5 | Verify | test output as evidence | the stop hook blocks on a red tree | [`05-verify.md`](../prompts/05-verify.md) |
| 6 | Review | `plans/changes/<name>/findings.md` | no open `[AMBIGUITY]`, no open BLOCKER — `[DIVERGENT]` counts as a BLOCKER | [`06-review.md`](../prompts/06-review.md) |
| 7 | Commit | pull request | CI green | [`07-commit.md`](../prompts/07-commit.md) |

Phase 1a is **owed where a minimum stands** (maintainer, 2026-10-08): a
`feature` owes at least three distinct, substantive questions the maintainer
answered; creating or changing an ADR owes five, whatever the class — a
feature that also carries an ADR owes five in total, never the sum; a `spike`
owes the three topics or a reasoned skip; a `bounded` change owes one answered
question or a reasoned skip. The gate `interview-minimums`
(`scripts/check_interview_minimums.py`) counts the records at the spec gate
and in `make verify`: only distinct, maintainer-answered records count, an
agent's answer, an open question and a repeated confirmation count for
nothing, and the check sees ADR paths in every diff state — committed,
staged, unstaged, untracked. The duty is prospective: a change is subject
when its spec `date` is later than the cut-off, **2026-10-08**, the merge
date of the change that introduced the rule — the stock before that day
stays exempt wherever it lies, and a change dated after the cut-off owes
its interview also once archived.

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

**The evidence rule.** A Codex or GLM finding is taken only when a test
demonstrates it or the spec supports it; otherwise it is rejected with its
reason and stays in `findings.md` as a disagreement. This holds in every repair
round, so a finding about something the spec does not cover needs a test, or it
is rejected. A foreign reviewer's confidence is not evidence: an implementer who
takes a finding on the reviewer's word alone repairs what nobody has shown to be
broken (stage 2, §4).

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

### Recurring jobs

A **job prompt** is a file in `prompts/` that is not a phase. It runs outside
the seven phases, for no change: a schedule or a person starts it, and it does
one bounded piece of work again and again. It names no model (its `**Model:**`
line says "none fixed"; the runner's configuration names one that
`model-endpoints.yaml` declares) and no runner, so the same text runs by hand
in any session. It writes no tracker and takes no git action of its own; what
it leaves behind goes into a pull request that a person reviews and merges. The
first one is [`prompts/research-recheck.md`](../prompts/research-recheck.md):
it re-checks one research note on the web and appends a dated addendum to it.

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

**The design phase 2b goes by class** (decision D-14,
`prompts/02b-design.md`): an `architectural` change always runs it; a `feature`
runs it or says in one sentence of its `spec.md` why not; a `bounded` change
and a `spike` never run it. Nothing checks this until the change-artefact
validator lands (bead coding-harness-jc3); the review before the merge holds
it.

**The interview goes by class too** (maintainer, 2026-10-08): a `feature`
owes at least three distinct, substantive questions; creating or changing an
ADR raises the debt to five in whatever class the change carries; a `spike`
owes its three topics or a reasoned skip; a `bounded` change one answered
question or a reasoned skip. What the gate counts and what the review judges
stands in §2, the paragraph after the phase table.

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
| Interview | `scripts/check_interview_minimums.py` | the gate `interview-minimums`: counts counted interview records per class at the spec gate and in verify, sees ADR paths in every diff state, compares per context — first parent on the main line (a `main` checkout or the hosted main-line run), else the merge base; a detached HEAD at `origin/main` is not measured and exits 3 — subject after the cut-off 2026-10-08 |

### Verification runs through git and CI, not through the harness

```bash
make verify     # every locally runnable gate — the CI runs the same, minus a `writer` gate (here only)
make gates      # what the CI runs, read from decisions/gates.yaml; a `writer` gate is marked
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
| 1 Explore | **Haiku 4.5** | much input, little output, no deep reasoning; where the runner starts the phase (§4), GLM 5.3 Flash explores instead |
| 1a Interview | **Opus 5.5** | the questions are the work, and there are few of them |
| 2 Spec | **Opus 5.5** | effort `xhigh`; the highest reasoning demand, little output |
| 2a Spec review | **Opus 5.5** | a fresh context that does not know the author's reasoning; a `bounded`, `feature` or `architectural` change goes to Codex (§4) |
| 2b Design | **Opus 5.5** | effort `xhigh`; the same demand as spec and plan |
| 3 Plan | **Opus 5.5** | effort `xhigh`; an error here is the most expensive in the whole run |
| 4 Implement | **Sonnet 5.5** | effort `medium`; a solid worker given a clear plan; where the runner starts the phase (§4), GLM 5.3 Flash builds instead |
| 5 Verify | — | deterministic |
| 6 Review | **Opus 5.5** | finds what Sonnet misses, and reads the code a change calls instead of trusting its docstring; a `bounded`, `feature` or `architectural` change goes to Codex (§4) |
| 7 Commit | **Haiku 4.5** | cheap and sufficient |

**No Fable** (maintainer, 2026-10-06): no phase runs on Fable 5.1; Opus 5.5
takes its places — the interview, the escalation below and the fallback of
stage 2 (§4). **Where stage 2 applies (§4), four rows leave this table:** the
reviews of a `bounded`, `feature` or `architectural` change go to Codex, and
explore and implement go to GLM 5.3 Flash. The rows above stay what runs
wherever the runner does not start a phase — a `spike`'s reviews, and every
phase until the runner starts it.

Switch with `/model sonnet`, `/model opus`, `/model haiku`. The alias
`opusplan` runs Opus while planning and switches to Sonnet for execution.

**Spec and plan on Opus 5.5 at effort `xhigh`** (maintainer, 2026-09-29, for
the whole repository; until then both ran on Fable 5.1). In a session:
`/model` and `/effort xhigh`; for a phase run as its own session:
`claude --model claude-opus-5-5 --effort xhigh`. A sub-agent takes its effort
from its definition's frontmatter (`effort: xhigh`), not from the call that
starts it, and a new definition is read only when a session starts.

**Spec review and review on Opus 5.5, except the `bounded`, `feature` and
`architectural` changes that §4 routes to Codex** (maintainer, 2026-09-30 and
2026-10-06, for the whole repository). From 2026-09-29 both ran on Fable 5.1,
and before that on Opus 5. An interim routing put both on Opus 5.5 from
2026-09-30 until stage 2 was live; the merge of ADR 0007 ends it for the
changes §4 routes to Codex. The cost is known: the spec review reads with the
same model as the spec's author (Opus 5.5), so what stays independent is the
fresh context, not the error profile.

**Implement on Sonnet 5.5 at effort `medium`, wherever the runner does not start
the phase** (maintainer, 2026-09-30; until then Sonnet 5; §4 moves the phase to
GLM 5.3 Flash, 2026-10-06). In a session: `/model sonnet` and `/effort
medium`; for a phase run as its own session: `claude --model claude-sonnet-5-5
--effort medium`.

**The spec review improves the spec first.** The spec's author works each 2a
row into `spec.md` (or rejects it with a reason) before phase 3; the revised
spec is the one yardstick for plan, code and review (`prompts/02-spec.md`,
"After the spec review"). **One reviewer for both:** phase 6 resumes the session
of phase 2a (`--session-id` there, `--resume` here; the id stands in
`findings.md`). For Codex the runner resumes with `codex exec resume`, reading
the id from the first call's `thread.started` event and writing it as
`Reviewer session: codex <id>`. It measures the code against the revised spec and first checks
that its 2a rows arrived there. It still never saw the author's reasoning, and
passing the spec in 2a is no argument in phase 6.

**Cost logic.** The expensive models run only in the phases with little output.
The token-heavy part runs on Sonnet — and, where the runner starts them (§4), on
GLM 5.3 Flash.

**Check after setup.** There are reports that the `model:` field in sub-agent
definitions is ignored and sub-agents run on the parent model. Look once with
`/status` — otherwise exploration is billed at Opus prices.

**Escalation.** After two failed review rounds, move up to Opus 5.5. For
rebuilds over ~200k tokens and for code touching security or concurrency, start
on Opus 5.5.
After a passed review, back to the model §3 or §4 names for phase 4.

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

## 4 · Stage 2 — Codex and GLM (active for framework content)

Since ADR 0007 (2026-09-30), reviewers from two other vendors read a change
before it merges — for **framework content only**: this repository's own tree,
the class `framework` of `model-endpoints.yaml`. Codex (`gpt-6.1-sol`, OpenAI)
reviews the spec and the code; GLM (`glm-5.3`, Z.ai) reviews in a short loop
between implementation and the code review. **Since 2026-10-06** (maintainer,
ADR 0007 as amended) GLM 5.3 Flash (`glm-5.3-flash`, the same Z.ai endpoint)
also explores (phase 1) and implements (phase 4) — the two phases that read
the repository broadly and write its code. Phases 1a, 2, 3 and 7 stay with
Anthropic (1a, 2 and 3 on Opus 5.5). **No Fable and no Kimi:** Fable 5.1 left
the routing on 2026-10-06 and Opus 5.5 takes its places, the fallback below
included. ADR 0007 also amends
decision D-13 of the 2026-09-16 interview, which had set four criteria before
any foreign call: a green leak check and a declared endpoint stay and are
enforced on every call, lakeswitch-ai's own disclosure decision governs
lakeswitch-ai's content (which is never sent), and three measured runs before
the first call are replaced by the measurement at the end of this section.

**Why review across vendors.** Different training lineages have blind spots
that do not overlap. Separating the context already finds measurably more
errors; vendor diversity adds to it. A model rates its own output too kindly —
a reviewer from another house does not know, by construction, that it is
checking itself. **Disagreements are recorded, not resolved automatically.**
"Codex flagged it, GLM did not" is the information. Kimi was considered and
dropped (ADR 0007).

### Which change gets what

| Change | Spec review (2a) | Review loop (4b) | Review (6) |
|---|---|---|---|
| a one-sentence change, a `spike` | no stage 2 | no stage 2 | no stage 2 |
| `bounded` | Codex, where one is held | GLM | Codex — the 2a session resumed where one was held, else a fresh one |
| `feature`, `architectural` | Codex | GLM | the same Codex agent, resumed |

This table routes the reviews. A `spike` or a one-sentence change gets no stage-2
review and is reviewed by Opus 5.5 where §3 asks for a review. Explore and
implement are not routed by class — the class is stated in the spec, after
phase 1 — and are set by the table below.

**Nothing checks a change's class.** A `feature` stated as a `spike` skips every
stage-2 review, and one stated as `bounded` may skip the spec review, which is
optional there; only the review before the merge catches either. The runner
below does not read the class either: whoever runs the change runs the verbs
its row allows.

### The routing

The rows are in the form of §3's table:

| Phase | Model | Why |
|---|---|---|
| 1 Explore | **GLM 5.3 Flash** | much input, little output, no deep reasoning; through Claude Code against Z.ai and the runner, for every change |
| 2a Spec review | **gpt-6.1-sol** | effort `max`, through the Codex CLI and the runner |
| 4 Implement | **GLM 5.3 Flash** | a worker given a clear plan; through Claude Code against Z.ai and the runner, for every change |
| 4b Review loop | **GLM 5.3** | effort `max`, through Claude Code against Z.ai and the runner |
| 6 Review | **gpt-6.1-sol** | effort `max`; the same Codex session as 2a, resumed where one was held |

**The two Flash rows are live through the runner.** `explore` starts phase 1
on GLM 5.3 Flash with read/search tools; `implement` starts phase 4 with file
read/search/edit/write tools but no shell. The runner, not the implementation
model, runs `make verify`, checks for a measured line below `## Time used` and
makes the local checkpoint commit. An explicit `--stage2-off [REASON]` uses
§3's Haiku 4.5 or Sonnet 5.5 route and records why. A leak refusal always stops
the call; it never selects the fallback.
If the model process itself fails, the runner restores the worktree to the
baseline commit (every path except the change's `findings.md`), says what it
undid and exits 1; the next step is `implement <change> --stage2-off`.

### The runner is the only way

A foreign model is started only through `python3 scripts/stage2.py <verb>
<change>`, never by typing `codex`, or `claude` against another endpoint, into
a shell. Seven verbs exist:

- `explore` — GLM 5.3 Flash, phase 1; `--stage2-off [REASON]` uses Haiku 4.5.
- `spec-review` — Codex, phase 2a, a fresh session.
- `implement` — GLM 5.3 Flash, phase 4; `--stage2-off [REASON]` uses Sonnet
  5.5 at effort `medium`.
- `review-loop` — GLM, one round of phase 4b.
- `release-loop` — the loop rows into `findings.md`, after the phase-6 verdict.
- `review` — Codex, phase 6, the phase-2a session resumed with `codex exec
  resume`; it then releases the loop rows and has Codex mark each one.
- `session` — one interactive OpenCode or Codex session in a new Terminal
  window; OpenCode waits on the separate Go declaration ("The interactive
  session" below).

**Before every call**, the runner checks, in this order: the change is named
and its folder exists; `model-endpoints.yaml` clears the endpoint (declared,
the model listed, `framework` among what it may see, a residency stated); and
**the leak check** (`python3 scripts/leakcheck.py`, by hand `make leakcheck
NAME=<change>`) passes in the same run, immediately before this call. The leak
check scans the change's folder, every file the tree tracks or lists as
untracked, the staged changes, the message and patch of every commit reachable
from a local or a remote-tracking branch, and the call's own prompt, against a
denylist each machine keeps outside the repository. It reports the place, the
rule's name and the length of a match, never the match. If it cannot measure —
the denylist missing, a file unreadable, a listed path that is a link to a
directory or a submodule — that is BLOCK, because unchecked is not clean.

**The secret rules skip `tests/`.** A rule of the denylist whose name starts
with `secret:` is not applied to a file under the repository's top-level
`tests/` folder — the file on disk, and the hunks of a commit's patch or of the
staged changes that name such a file — so that an invented key or password may
stand there as a test fixture. Every other rule, the ones for a customer's
names above all, scans `tests/` like the rest, and a secret rule scans
everything outside it (`tests_extra/`, `docs/tests/` and a change's own folder
are not `tests/`; neither is a link under `tests/`, a commit message or a
prompt text). **The accepted consequence** (maintainer, 2026-10-07): a real key
committed in a test file is not found by this check. Each machine marks its
secret rules in its own denylist; a rule without the prefix scans everything.

**A clean report has limits.** The check does not read the reflog, the stash,
refs outside the branches (tags, `refs/dolt/`) or objects no ref reaches. A
value taken out by rewriting a commit therefore reads clean while `git log -g
-p` still shows it, until git expires the reflog (`git reflog expire
--expire=now --all`, then `git gc --prune=now`); the check cannot tell whether
that was done, and its advice for a match in a commit says so.

**Explore and implement send more than a review does.** A reviewer reads one
diff and one spec; explore reads the repository broadly and implement reads
the tree and writes code into the worktree, so far more of this repository
goes to Z.ai than before 2026-10-06. The leak check covers what these two runs
send — the same scan, immediately before each call, over the tree, the staged
changes, the commits reachable from the branches and the call's own prompt — and
what stays out stays out: LakeSwitch and customer content never go, to any
endpoint, and the check is what blocks it (the maintainer asked about it on
2026-10-06 and kept it). How the runner confines the tools and writes of
these two runs is stated below.

What every call then carries: one audit line (in `research.md` for Explore,
otherwise `findings.md`), an empty standard input and an environment built
from an allow-list, not the caller's. The runner starts Codex with the
read-only sandbox, its session kept and its hooks and memories switched off.
It starts GLM as Claude Code against Z.ai's Anthropic-compatible endpoint,
with a fresh empty configuration directory and the project's settings, hooks
and MCP servers skipped. Explore and the review loop get only `Read`, `Grep`
and `Glob`; Implement also gets `Edit` and `Write`, never Bash or another
command tool. On a successful implementation answer the runner runs exactly
`make verify`; a failed post-check gets one fresh Flash repair, then one
Sonnet 5.5 fallback, and every attempt repeats the leak check. A failed model
process stops instead of silently changing route. **Those settings are
configured on every call, not measured** (the maintainer's decision of
2026-09-30, ADR 0007): no test has run either program to see them take effect,
on `codex exec resume` in particular, whose help lists no sandbox option. If
Codex's hooks are not in fact off, the tracked `.codex/hooks.json` injects
tracker text into the call that the leak check does not scan. GLM's credential
(`GLM_KEY` in `~/.config/cc-routing/secrets.env`) stays in the runner's
environment for that call, is outside the reach of the Claude Code file tools (`--restricted`, see
"Reads" below; not measured) and is scrubbed from everything the runner prints or writes. The
Stage-1 fallback uses normal Claude Code authentication and never reads that
key.

`.claude/settings.json` asks before a `codex` typed directly in a Claude Code
session (`Bash(codex *)`). That is a brake, not a lock: `sh -c`, an absolute
path or a script file passes it, as it does for the merge rules in §2.

**Reads: confined for the Claude Code calls, asked for Codex.** Every Claude
Code call (explore, implement, the Sonnet 5.5 fallback attempts and the GLM
review loop) starts in the worktree with `--restricted` and no `--add-dir`.
`claude --help` says `--restricted` "confines the file tools to the working
directories", so the credential file `~/.config/cc-routing/secrets.env`, which
lies outside the worktree, is outside what the model's file tools reach. **That
is the program's documented behaviour, not measured here:** no test has run it
against a path outside the worktree. The Codex calls (`spec-review`, `review`)
have no such flag. Their prompts ask the model to read nothing outside the
worktree and the repository's git directory, and **that is a request, not a
lock:** Codex can read the rest of the disk, the customer instance's checkout
included. The maintainer accepted that as a residual risk on 2026-09-30
(ADR 0007). The leak check scans what this repository presents, not what else
the disk holds.

### The interactive session (`session`)

`python3 scripts/stage2.py session <change> --model <id>` starts one interactive
model session for the change in a new macOS Terminal window, from the same
checked runner as every other call. The `--model <id>` is required and taken
literally: a plain id selects what `openai-codex` lists and dispatches the
official Codex CLI; a full `opencode-go/<model>` id selects `opencode-go` when
that entry lists the bare `<model>`, as the reviewer declaration writes it, and
dispatches OpenCode with the full id. No alias, no prefix guessing, and the
session approves no endpoint: a model the declaration does not list for a session
transport is refused before anything starts, and the OpenCode path stays closed
until `opencode-go` and that model are declared for framework content in
`model-endpoints.yaml` (coding-harness-ymx). `--handover <path>` names another
handover inside the worktree; without it the change's own `handover.md` under
`plans/changes/<change>/` is the first prompt. The file must be a readable,
nonempty UTF-8 regular file inside the dedicated worktree; the prompt is bounded
at 32 KiB and the whole command at 64 KiB.

A session runs only in the change's own dedicated worktree
(`<main checkout>/.claude/worktrees/<change>`, attached branch, that directory
as the working one) and only on macOS. Before anything opens, the runner checks
the declaration, reads the handover, and runs the leak check over the tree, the
index, the history and the exact outgoing prompt — the check runs twice in the
same invocation: once after the handover is read, and a second time immediately
before Terminal is told to start. It covers this launch only: nothing later is
scanned — not later prompts, not edits, not a model switched in the session's
own user interface — so another model goes through the runner again. The tool
permissions handed to the CLI (OpenCode gets a runner-supplied policy whose
effective agent the runner reads back and verifies; Codex gets
`workspace-write` with approval on request) are a configuration, not
a confinement at the operating-system level: shell commands approved in the
window can read what the user can read.

One audit line goes into the change's `findings.md` per attempt, first with
`dispatch pending.`, then — and only that line changes — `dispatch accepted.`
or `dispatch failed (<why>).` Accepted means Terminal took the command, nothing
more: whether the CLI started, authenticated or answered shows in the new
window, and a missing CLI or `osascript` is refused beforehand as a
prerequisite. The runner's launch files live in a fresh private directory under
the gitignored `.stage2-sessions/` in the worktree; they carry the policy and
the launch script, no prompt and no credential. A refused or failed attempt
removes its directory, an accepted one keeps it for the session to load, and
nothing user-owned there is ever written or deleted. The session reads no
credential file, copies no caller token, and starts no headless verb — no
`codex exec`, no `opencode run`. The verb neither runs the review loop nor
changes which reviewer sees what: the review order is not this verb's business.
Its ADR 0007 amendment travels as a draft in the change folder until the
decision PR is merged.

### The review loop (phase 4b)

After implementation and before phase 6, `review-loop` runs one round: GLM
reads the change's diff against its merge base with `origin/main`, uncommitted
changes included, and answers in table rows. **At most two rounds.** The rows
go into a **loop record** outside the worktree and outside the git directory
(`${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md`),
not into the repository: Codex can read the whole worktree, and it writes its
verdict before it sees them.

The implementer writes beside each row its `Status` — `taken — <test or
criterion>` or `rejected — <reason>` — and, for a taken row, `Broke a test`. It
repairs the taken rows and runs `make verify`, which must be green before the
next round starts. **The evidence rule of §2 holds here:** a finding is taken
only when a test demonstrates it or the spec supports it. A row left
undecided holds the next round and the release.

The phase-6 reviewer writes its verdict first: the table, and under it the line
`Phase 6 verdict: <reviewer> <session>, <date>` (the runner writes it for
Codex; an Opus reviewer writes its own). Only then does `release-loop` carry
every loop row into `findings.md` with reviewer `GLM`, and the reviewer marks
each row in its `Phase 6` column, `agree` or `disagree — <reason>`. Nothing is
netted: the reviewer's view of GLM's rows is the information.

### Two columns for every stage-2 change

Beyond the vocabulary of §2, a stage-2 change's `findings.md` carries two
columns, defined here because the findings template is not in this repository
yet:

- **`Reviewer`** — Codex, GLM or Opus: who raised the finding.
- **`Broke a test`** — for each taken row, `yes` when its repair turned a test
  red that was green before it, `no` when it did not. The finding's own new
  test does not count: the evidence rule expects it to be red first.

### Measuring the first three stage-2 runs

A **stage-2 run** is a change whose review made at least one call; runs are
counted in the order their pull requests merge. Every finding records its
reviewer, whether it was taken or rejected and, if taken, whether it broke a
test. **After the third run, a short evaluation is written under
`docs/research/`. If at least one taken Codex or GLM finding broke a test,
stage 2 falls back to Opus 5.5 until the maintainer decides again** — Opus 5.5
reviews every change, and phases 1 and 4 return to §3's Haiku 4.5 and Sonnet
5.5. The rule is written, not counted by a script: a person reads the
evaluation, and its pull request applies the fallback. This replaces the three measured runs that
D-13 asked for before the first foreign call; what the replacement gives up is
the measured stage-1 baseline (ADR 0007).

> **Two caveats, and the second one holds here in particular.** The vendors'
> coding subscriptions are contractually limited to officially supported tools;
> through the Codex CLI and through Claude Code that is covered, in a
> self-built harness it is not. The runner starts those programs, it does not
> replace them.
>
> **And: this repository contains abstracted knowledge from a productive
> customer project.** No customer names, schemas, entity names or figures go to
> endpoints outside one's own jurisdiction — not in a diff, not in a plan
> either. The leak check runs before every call.

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

Stage 1 was to run for two to three weeks in real use first. **The original
signal to move on:** the phase gates hold without anyone thinking about them, and
the Sonnet implementation is the noticeable cost. **It was not waited for.** ADR
0007 (2026-09-30) opened stage 2 for framework content, with the first three
stage-2 runs measured in its place (§4) — model diversity came before the
two-to-three-week signal, knowingly, and the measurement is what can send it
back.

## 7 · What survives each stage

| Piece | Stage 1 | Stage 2 | Stage 3 |
|---|---|---|---|
| `AGENTS.md` | ✅ | ✅ unchanged | ✅ as `instructions:` |
| `plans/` artefacts | ✅ | ✅ unchanged | ✅ unchanged |
| `prompts/` | ✅ | ✅ as text | ✅ as YAML prompt |
| `Makefile`, CI, git hooks | ✅ | ✅ unchanged | ✅ as a policy gate |
| `.claude/agents/` | ✅ | ✅ unchanged | ❌ replaced by YAML |
| `.claude/commands/` | ✅ | ✅ unchanged | ❌ replaced by YAML |
| Claude Code hooks | ✅ | ✅ unchanged | ❌ replaced by policies |

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
