---
title: "Workflow and model routing — phases and stages"
category: governance
status: current
created: 2026-09-05
last_reviewed: 2026-09-29
updated: 2026-10-16
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
| 4b | Review loop *(stage 2)* | the loop rows — outside the repository until the phase-6 verdict, then in `findings.md` (`release-loop`) | at most three rounds — round 3 only when round 2 wrote a taken row; `make verify` green after each repair | [`04b-review-loop.md`](../prompts/04b-review-loop.md) |
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
when its spec `date` is later than the repository's adoption day, which
`decisions/adoption.yaml` records per repository and `scripts/adoption.py`
reads — here **2026-10-08**, the merge date of the change that introduced the
rule. The stock before that day stays exempt wherever it lies, and a change
dated after it owes its interview also once archived. The record stays in its
repository; without it the gate is not measured (exit 3), and moving a day is
a decision pull request (ADR 0014).

An ADR edit belongs to the change that **claims** the file: the list
`adr_files` in the header of its `spec.md`, in every class, names each file
under `docs/adr/` the change creates, changes or removes. The gate attributes
an edit to the claimant among the changes of the diff and to nobody else,
whichever other change folders the diff touches and whatever the ADR says; the
claimant owes its five records whatever its class and date; the adoption day
exempts a change begun on or before it from the class minimums and from the
agreement of answer and claim, never an ADR edit. An edit no change of the diff claims is a
finding that names the remedy — list the file under `adr_files` in the spec
header of the change it belongs to — and so is an edit two changes claim, or
a claim that cannot be read. A subject `feature`'s answer to the ADR question
agrees with its claim: "yes" with at least one claimed file, "no" with none.
An amendment costs one header line: the amending change lists the file in its
own spec, and nothing else moves. A correct claim — one whose edit the change made — is never removed to settle
a clash; an erroneous claim, one the change's own "no" answer contradicts, is
corrected by removing it. Two claimants of one file in one diff are a finding,
and its only remedy is to split the pull request: the amendment in one, the
edit to the earlier change's folder in another.

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

**The evidence rule.** A finding of Codex or of a rung of the review loop is
taken only when a test
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

**Every question carries its context** (ADR 0018). Before any options, the
question shows five short parts in this order — Topic; Intention, including
why it comes up now; Today; Repository change; Architecture change — and the
question stands last on its own line. The form is written for a reader with
ADHD, and that is the reason the rule holds for everyone, without a profile:
every question an agent puts to a person, in every harness — interviews,
spec decisions, review ambiguities, the plan card's presentation and
ordinary conversation. Plain language; an identifier or technical term is
explained at first use; an unchanged area says why it stays as it is. In
conversation the five labels are translated; in a recorded answer the shown
context is preserved faithfully in English, in the record's own `context`
field. The gate `question-context`
(`scripts/check_question_context.py`) holds every `status: answered` record
recorded on or after the repository's adoption day
(`decisions/adoption.yaml`, read through `scripts/adoption.py`) to one
non-blank `context` text value — presence only, never a grade of wording —
in live and archived changes, with or without a spec. The cut-off is each
answer's own recording day, the one em-dash date (`— YYYY-MM-DD`) that ends
its decision statement (a closing parenthetical remark may follow it); the adoption day itself is included, older answers
stay exempt and unchanged, and evidence the gate cannot read is not measured
(exit 3) instead of passing.

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
ADR (one it claims under `adr_files`) raises the debt to five in whatever class the change carries; a `spike`
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
- Nothing checks that the class is right, that a claimed ADR file exists, or
  that a decision pull request carries its label and block. The review
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
| Interview | `scripts/check_interview_minimums.py` | the gate `interview-minimums`: counts counted interview records per class at the spec gate and in verify, sees ADR paths in every diff state, compares per context — first parent on the main line (a `main` checkout or the hosted main-line run), else the merge base; a detached HEAD at `origin/main` is not measured and exits 3 — attributes an ADR edit to the change that claims it under `adr_files` (ADR 0014) — subject after the adoption day of `decisions/adoption.yaml`, here 2026-10-08 |
| Question context | `scripts/check_question_context.py` | the gate `question-context`: every `status: answered` record recorded on or after the adoption day keeps the context that was shown with it in its own `context` field — presence only, in live and archived `decisions.md`, with or without a spec; the cut-off is each answer's own recording day, read from the one em-dash date (`— YYYY-MM-DD`) that ends its decision statement (a closing parenthetical remark may follow); the adoption day itself is subject, older answers stay exempt, unreadable evidence exits 3 (ADR 0018) |
| Criterion tests | `scripts/check_criterion_ledger.py` | the gate `criterion-ledger`: every test a plan's `## Criterion ledger` names is defined, every criterion of the spec has an entry, a not-yet-written entry stands only while the change is live; ledgers stay held after archiving, and archived plans dated before 2026-10-11 without one are exempt (ADR 0013); moving that cut-off date is a governance act — a decision pull request, never a drive-by edit of the gate |

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

CI runs on pull requests (a superseded run is cancelled) and on pushes to
`main`, under Python 3.12; a branch without a pull request gets no hosted run,
and the schedule runs only the drift gates.

The stop hook is the comfort layer, not the enforcement. It runs only when
Python was touched since `HEAD`: a hook that costs a minute when nothing has
happened is switched off within a week — and a switched-off hook is worse than
none, because the registry keeps counting it as protection.

### Model routing

| Phase | Model | Why |
|---|---|---|
| 1 Explore | **Haiku 5.5** | much input, little output, no deep reasoning; where the runner starts the phase (§4), GLM 5.3 Flash explores instead |
| 1a Interview | **Opus 5.5** | the questions are the work, and there are few of them |
| 2 Spec | **Opus 5.5** | effort `xhigh`; the highest reasoning demand, little output; where the runner drafts (§4), `gpt-6.1-sol` at effort [`CODEX_EFFORTS["draft"]`](../scripts/stage2.py) writes it instead |
| 2a Spec review | **Opus 5.5** | a fresh context that does not know the author's reasoning; where the runner starts it (§4), a headless Claude Code call |
| 2b Design | **Opus 5.5** | effort `xhigh`; the same demand as spec and plan; where the runner drafts (§4), `gpt-6.1-sol` at effort [`CODEX_EFFORTS["draft"]`](../scripts/stage2.py) writes it instead |
| 3 Plan | **Opus 5.5** | effort `xhigh`; an error here is the most expensive in the whole run; where the runner drafts (§4), `gpt-6.1-sol` at effort [`CODEX_EFFORTS["draft"]`](../scripts/stage2.py) writes it instead |
| 4 Implement | **Sonnet 5.5** | effort `medium`; a solid worker given a clear plan; where the runner starts the phase (§4), GLM 5.3 Flash builds instead |
| 5 Verify | — | deterministic |
| 6 Review | **Opus 5.5** | finds what Sonnet misses, and reads the code a change calls instead of trusting its docstring; a `bounded`, `feature` or `architectural` change goes to Codex (§4) |
| 7 Commit | **Haiku 5.5** | cheap and sufficient |

**No Fable** (maintainer, 2026-10-06): no phase runs on Fable 5.1; Opus 5.5
takes its places — the interview, the escalation below and the fallback of
stage 2 (§4). **Where stage 2 applies (§4), five rows leave this table:** where
the runner drafts (§4), Codex writes spec, design and plan instead, and explore
and implement go to GLM 5.3 Flash; where the runner starts the spec review
(§4), it stays on Opus 5.5 as a headless call. The rows above stay what runs
wherever the runner does not start a phase — a `spike`'s reviews, and every
phase until the runner starts it.

Switch with `/model sonnet`, `/model opus`, `/model haiku`. The alias
`opusplan` runs Opus while planning and switches to Sonnet for execution.

**Spec and plan on Opus 5.5 at effort `xhigh` by hand** — a spike, or Stage 2
off (maintainer, 2026-09-29, for the whole repository; until then both ran on
Fable 5.1); where the runner drafts (§4), Codex writes them instead — the
default since ADR 0016. In a session: `/model` and `/effort xhigh`; for a
phase run as its own session:
`claude --model claude-opus-5-5 --effort xhigh`. A sub-agent takes its effort
from its definition's frontmatter (`effort: xhigh`), not from the call that
starts it, and a new definition is read only when a session starts.

**Spec review on Opus 5.5 for every change since ADR 0016; review on Opus 5.5,
except the `bounded`, `feature` and `architectural` changes that §4 routes to
Codex** (maintainer, 2026-09-30 and 2026-10-06, for the whole repository; ADR
0016 moved the spec review off Codex on 2026-10-12). From 2026-09-29 both ran on Fable 5.1,
and before that on Opus 5. An interim routing put both on Opus 5.5 from
2026-09-30 until stage 2 was live; the merge of ADR 0007 ends it for the
changes §4 routes to Codex. The cost is known: where the runner drafts (§4),
the spec's author is Codex or GLM 5.3 and the review reads another vendor's
error profile; where a person writes the spec by hand — a spike, or Stage 2
off — the author is Opus 5.5 itself, so what stays independent is the fresh
context, not the error profile.

**Implement on Sonnet 5.5 at effort `medium`, wherever the runner does not start
the phase** (maintainer, 2026-09-30; until then Sonnet 5; §4 moves the phase to
GLM 5.3 Flash, 2026-10-06). In a session: `/model sonnet` and `/effort
medium`; for a phase run as its own session: `claude --model claude-sonnet-5-5
--effort medium`.

**The spec review improves the spec first.** The spec's author works each 2a
row into `spec.md` (or rejects it with a reason) before phase 3; the revised
spec is the one yardstick for plan, code and review (`prompts/02-spec.md`,
"After the spec review"). **One reviewer for both:** since ADR 0016 this holds
for a `spike` only — a routed change's phase 6 is a fresh Codex session that
first checks that each 2a row arrived in the revised `spec.md`. A change
reviewed before ADR 0016 keeps its recorded Codex 2a session (`Reviewer
session: codex <id>` in `findings.md`), and the runner resumes it while that
block is the change's last one (§4). It measures the code against the revised
spec and first checks that its 2a rows arrived there. It still never saw the
author's reasoning, and passing the spec in 2a is no argument in phase 6.

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

### Tracker commands

Use `tools/bd` for every tracker command; house rules 2–4 in `AGENTS.md`
govern tracker ownership and the order of tracker and git pushes.

```bash
tools/bd ready              # open, unblocked work
tools/bd show <id>          # detail view
tools/bd create "title" -d "description" -p 1
tools/bd update <id> --claim
tools/bd close <id> --reason="…"
tools/bd prime              # full tracker context for a session
tools/bd dolt push          # push tracker data to origin (refs/dolt/data)
```

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
   tool, is `scripts/omnigent_policy.py`. Read-only tools stay usable.
   The default policy in `tools/omnigent/` is the second layer, rendered from
   that same list. It refuses the denied ones and asks about the asked one
   server-side for every Omnigent session on the machine. The
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

## 4 · Stage 2 — Codex and the review loop on OpenCode Go (active for framework content)

Since ADR 0007 (2026-09-30) a reviewer from another vendor reads a change
before it merges — for **framework content only**: this repository's own tree,
the class `framework` of `model-endpoints.yaml`. Codex (`gpt-6.1-sol`, OpenAI)
drafts the spec, the design and the plan (2, 2b and 3, the `draft` verb) and
reviews the code (6). **Since ADR 0016 (2026-10-12)** the spec review (2a) runs
on Opus 5.5 through the `spec-review` verb — a fresh context, and a model other
than the Codex or GLM 5.3 that drafted the artefacts it reads: no model reviews
its own draft.
**Since ADR 0011 (2026-10-08)** the
review loop (4b) between implementation and the code review runs on OpenCode
Go (`opencode-go` in `model-endpoints.yaml`) through Pi — **since ADR 0019
(2026-10-15)** the repository's own pinned install under `tools/pi/`, whose
exact version `tools/pi/package.json` pins — calling OpenCode Go's
chat-completions address, and which
model answers a round comes from the entry's ordered `modelle` list, the
ladder. The maintainer put the ladder to the loop alone on 2026-10-08 — after
Codex's phase 6 found two real BLOCKERs in a change the loop had passed, as on
every change of the night run — so GLM has left the reviewer roles.
**Since 2026-10-06** (maintainer) GLM 5.3 Flash
(`glm-5.3-flash`, the Z.ai endpoint) also explores (phase 1) and implements
(phase 4) — the two phases that read the repository broadly and write its
code. **Since 2026-10-12** (ADR 0015) GLM 5.3 (`glm-5.3`, the same endpoint)
repaired the findings the orchestrator takes, of the loop (4b) and of phase 6;
**since the merge of ADR 0017** Codex (`gpt-6.1-sol`) does, with Sonnet 5.5
after two failed post-run checks, through the runner's `repair` verb — since the
first day `taken` on a row means
decided and waiting for the repair, and `fixed` means repaired. Phases 1a, 2a
and 7 stay with Anthropic (2a on Opus 5.5).
**No Fable and no Kimi:** Fable 5.1 left the routing on 2026-10-06 and Opus
5.5 takes its places, the fallback below included. ADR 0007 also amends
decision D-13 of the 2026-09-16 interview, which had set four criteria before
any foreign call: a green leak check and a declared endpoint stay and are
enforced on every call, lakeswitch-ai's own disclosure decision governs
lakeswitch-ai's content (which is never sent), and three measured runs before
the first call are replaced by the measurement at the end of this section.

**Why review across vendors.** Different training lineages have blind spots
that do not overlap. Separating the context already finds measurably more
errors; vendor diversity adds to it. A model rates its own output too kindly —
a reviewer from another house does not know, by construction, that it is
checking itself. The ladder's rungs are three lineages — DeepSeek, and
Xiaomi's MiMo in two sizes — so a round sees what the round before it did not.
**Disagreements are recorded, not resolved automatically.**
"Rung 1 flagged it, rung 2 did not" is the information. Kimi was considered
and dropped (ADR 0007).

### Which change gets what

| Change | Spec review (2a) | Review loop (4b) | Review (6) |
|---|---|---|---|
| a one-sentence change, a `spike` | no stage 2 | no stage 2 | no stage 2 |
| `bounded` | Opus 5.5, where one is held | the ladder | Codex, a fresh session |
| `feature`, `architectural` | Opus 5.5 | the ladder | Codex, a fresh session |

This table routes the reviews. A `spike` or a one-sentence change gets no stage-2
review and is reviewed by Opus 5.5 where §3 asks for a review. Explore, the
draft and implement are not routed by class — the class is stated in the spec,
after phase 1 — and are set by the table below.

**Nothing checks a change's class.** A `feature` stated as a `spike` skips every
stage-2 review, and one stated as `bounded` may skip the spec review, which is
optional there; only the review before the merge catches either. The runner
below does not read the class either: whoever runs the change runs the verbs
its row allows.

### The routing

The rows are in the form of §3's table. Which model the review loop calls is
the ladder's order in `model-endpoints.yaml`, not a line here: reordering that
list is a one-line pull request that touches nothing else.

| Phase | Model | Why |
|---|---|---|
| 1 Explore | **GLM 5.3 Flash** | much input, little output, no deep reasoning; through Claude Code against Z.ai and the runner, for every change |
| 2 Spec | **gpt-6.1-sol** | effort [`CODEX_EFFORTS["draft"]`](../scripts/stage2.py), one call for 2, 2b and 3 through the Codex CLI and `draft`, writing in the CLI's workspace-write sandbox; `glm-5.3` drafts through Claude Code against Z.ai after two failed Codex attempts (ADR 0016) |
| 2b Design | **gpt-6.1-sol** | effort [`CODEX_EFFORTS["draft"]`](../scripts/stage2.py), drafted in the same call as 2 and 3 |
| 3 Plan | **gpt-6.1-sol** | effort [`CODEX_EFFORTS["draft"]`](../scripts/stage2.py), drafted in the same call as 2 and 2b |
| 2a Spec review | **Opus 5.5** | effort `xhigh`, through Claude Code and `spec-review`, read-only tools |
| 4 Implement | **GLM 5.3 Flash** | a worker given a clear plan; through Claude Code against Z.ai and the runner, for every change |
| 4b Review loop | **the ladder** | the ordered `modelle` list of the `opencode-go` entry in `model-endpoints.yaml`: round *n* calls its *n*-th id (`modelle[n-1]`), through Pi, effort `max` (Pi clamps it to `high` for a rung that takes no `max`), round 3 only when round 2 wrote a taken row |
| Repair after 4b and 6 | **gpt-6.1-sol** | a Codex attempt in the configured `workspace-write` sandbox, effort [`CODEX_EFFORTS["repair"]`](../scripts/stage2.py); one fresh Codex attempt after a failed post-run check, and Sonnet 5.5 at effort `medium` after two failed ones; no GLM credential (`repair`, ADR 0017) |
| 6 Review | **gpt-6.1-sol** | effort [`CODEX_EFFORTS["review"]`](../scripts/stage2.py), through the Codex CLI and `review`, a fresh Codex session |

The effort text in ADR 0016 and ADR 0017 awaits its separately agreed
amendments; the table above carries the live setting.

**The two Flash rows are live through the runner.** `explore` starts phase 1
on GLM 5.3 Flash with read/search tools; `implement` starts phase 4 with file
read/search/edit/write tools but no shell. The runner, not the implementation
model, runs `make verify`, checks for a measured line below `## Time used` and
makes the local checkpoint commit. An explicit `--stage2-off [REASON]` uses
§3's Haiku 5.5 or Sonnet 5.5 route and records why. A leak refusal always stops
the call; it never selects the fallback.
If the model process itself fails, the runner restores the worktree to the
baseline commit (every path except the change's `findings.md`), says what it
undid and exits 1; the next step is `implement <change> --stage2-off`.
If an attempt fails its post-run checks, the runner quotes its diagnostics and
the files its model changed (lines added and removed) into `findings.md` below
that attempt's audit line, before the next attempt starts or the run exits 1; a
passing attempt leaves its audit line only.
Before `make verify`, the runner runs the worktree's own `.venv/bin/ruff` —
`check --fix` with safe fixes only, then `format` — on the change's Python
files under `scripts/` and `tests/`; what that changed stands first in a failed
attempt's diagnostics and in the checkpoint commit's message, and a ruff that
cannot run or leaves findings leaves the verdict to `make verify`.

### The runner is the only way

A foreign model is started only through `python3 scripts/stage2.py <verb>
<change>`, never by typing `codex`, `pi`, or `claude` against another endpoint,
into a shell. Ten verbs exist:

- `explore` — GLM 5.3 Flash, phase 1; `--stage2-off [REASON]` uses Haiku 5.5.
- `draft` — Codex, phases 2, 2b and 3 in one call; GLM 5.3 (`glm-5.3`) after
  two failed Codex attempts ("The draft" below).
- `spec-review` — Opus 5.5, phase 2a, a headless call with read-only tools and
  no session kept.
- `implement` — GLM 5.3 Flash, phase 4; `--stage2-off [REASON]` uses Sonnet
  5.5 at effort `medium`.
- `repair` — Codex, every taken finding of the loop record, the released
  blocks and the phase-6 tables in one call; `--stage2-off [REASON]` uses
  Sonnet 5.5 at effort `medium` ("Repairing taken findings" below).
- `review-loop` — one round of phase 4b, started through Pi; round *n* goes
  to the ladder's *n*-th rung.
- `release-loop` — the loop rows into `findings.md`, after the phase-6 verdict.
- `review` — Codex, phase 6. A re-check after an earlier `## Phase 6` block
  in `findings.md` starts a fresh read-only Codex session. The first phase-6
  review resumes a recorded Codex phase-2a session with `codex exec resume`;
  otherwise it starts fresh. It then releases the loop rows and has Codex
  mark each one.
- `probe` — one call per rung of the ladder through Pi, the pinned version
  checked once first, the declaration and the leak check in front of each
  call; measures the address, writes no loop record (its call lines go to
  `findings.md` like any call; a change's declared special run).
- `session` — one interactive Pi or Codex session in a new Terminal window; a
  Go model (`opencode-go/<model>`) starts the pinned Pi, never the OpenCode CLI
  ("The interactive session" below).

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

**Explore, the draft, implement and repair send more than a review does.** A
reviewer reads one diff and one spec; explore reads the repository broadly,
a draft's prompt carries the three phase prompts, the repository rules and the
change's inputs and its call writes into the worktree, implement
reads the tree and writes code into the worktree, and every repair prompt
carries the change's spec, plan and repository rules plus the taken rows of
the loop record — rows the repository does not hold until the phase-6 verdict
releases them into `findings.md`. Under ADR 0017 those repair prompts send the
rows to Codex (OpenAI) before the verdict; the Sonnet 5.5 fallback or an
explicit Stage-1 repair sends them to Anthropic. The leak check covers what
these four runs send — the same scan, immediately before each call, over the
tree, the staged changes, the commits reachable from the branches and the
call's own prompt — and what stays out
stays out: LakeSwitch and customer content never go, to any endpoint, and the
check is what blocks it (the maintainer asked about it on 2026-10-06 and kept
it). How the runner confines the tools and writes of these runs is stated
below.

What every call then carries: one audit line (in `research.md` for Explore,
otherwise `findings.md`), an empty standard input and an environment built
from an allow-list, not the caller's. The runner starts Codex with the
read-only sandbox for a review call, its session kept and its hooks and
memories switched off. A draft's Codex call runs in the `workspace-write`
sandbox; the runner puts back its writes outside the change folder before it
verifies ("The draft" below). A repair's first two attempts run as Codex calls
in the `workspace-write` sandbox. What a repair's Codex call writes is checked
and committed by the runner, including changes outside the change folder; a
checkpoint requires all checks to pass. A `draft`, `repair` or `spec-review`
call keeps no session. Before the loop's first call the runner runs the
repository wrapper `tools/pi/pi --version`; anything but the exact version
pinned in `tools/pi/package.json` refuses with exit 2, before the leak check.
The wrapper is the runner's only path to Pi (ADR 0019): a missing, mismatched
or unusable local install refuses with setup guidance before any model
request, and no call installs, uses `npx` or falls back to a global Pi. It starts the
review loop's rung as Pi (`--print`, no session) against OpenCode Go's
chat-completions address, with the rung under the `opencode-go` provider,
thinking `max`, the tools `read`, `grep`, `find` and `ls`, extensions, MCP
servers, skills, context files, prompt templates and themes switched off,
retries off, and a fresh home and agent directory per call. Explore and
implement start Claude Code against Z.ai with `--restricted` and the project's
settings, hooks and MCP servers skipped; implement also gets
`Edit` and `Write`, never Bash or another command tool. On a successful
implementation answer the runner runs exactly
`make verify`; a failed post-check gets one fresh Flash repair, then one
Sonnet 5.5 fallback, and every attempt repeats the leak check. A failed model
process stops instead of silently changing route, and a review-loop call (through Pi) that has
not ended 30 minutes after it started is stopped. For the other foreign CLIs,
isolation settings are configured on every call, not measured
by these Pi contracts (the maintainer's decision of 2026-09-30, ADR 0007).
The loop's Pi flags were first measured by hand on the pinned version;
**since ADR 0019** the offline suite (`tests/test_pi_contract.py`) starts the
real pinned install. It measures the four-tool declaration and refusal,
extension and MCP startup suppression, skill/prompt/theme discovery reads,
context-file exclusion and scratch-agent separation from saved authentication
and command-valued model configuration. Positive controls run through Pi;
project-resource controls also grant trust so trust refusal cannot mask a
missing discovery flag. Provider contracts read native addresses from the installed Pi catalog and
measure synthetic-key requests and model ids through loopback transport. These contracts do not
measure every other model CLI's isolation settings.
If hooks are not in fact off for a call, the tracked `.codex/hooks.json` shows
the kind of text such a switch would inject into a call that the leak check
does not scan; the runner starts Codex with hooks and memories off, and the ask rule
below still guards one typed by hand. The reviewer's credential
(`OPENCODE_GO_KEY` in `~/.config/cc-routing/secrets.env`) reaches the loop's
Pi call as `OPENCODE_API_KEY` in its environment, never in an argument or a
file; GLM's (`GLM_KEY`, the same file) stays in the runner's environment for
its own call only. Both are scrubbed from everything the runner prints or
writes. GLM's file tools are outside the reach of the Claude Code file tools'
`--restricted` (see "Reads" below; not measured); the loop's are not. The
Stage-1 fallback uses normal Claude Code authentication and never reads
either key.

`.claude/settings.json` asks before a `codex` typed directly in a Claude Code
session (`Bash(codex *)`). That is a brake, not a lock: `sh -c`, an absolute
path or a script file passes it, as it does for the merge rules in §2.

**Reads: confined for the Claude Code calls, asked for Codex and for the
loop.** Every Claude Code call (explore, the draft's GLM attempt, implement,
`spec-review` and the Sonnet 5.5 fallback attempts) starts in the worktree
with `--restricted` and no `--add-dir`.
`claude --help` says `--restricted` "confines the file tools to the working
directories", so the credential file `~/.config/cc-routing/secrets.env`, which
lies outside the worktree, is outside what those calls' file tools reach.
**That is the program's documented behaviour, not measured here:** no test has
run it against a path outside the worktree. Codex's review, draft and repair
calls are not confined in their reads: only the prompt's request bounds them.
ADR 0017 retains ADR 0016's residual risks for ignored files, external paths
and the git directory. **The review loop's Pi calls are not Claude Code calls,
and they are not confined:** a round's `read` reaches files outside the
worktree (measured with Pi 1.1.0), and the secrets file is among
them; only the prompt's request bounds it. Every Codex prompt and every
reviewer's prompt asks the model to read nothing outside the worktree and the
repository's git directory, and **that is a request, not a lock** — the program can read the
rest of the disk, the customer instance's checkout included. Pi's isolation
flags (no extensions, MCP servers, skills, context files, prompt templates or
themes; no approval; a fresh agent directory and home per call) are configured
on every call and were measured once by hand on the pinned version; the suite
starts no real Pi — a statement of 2026-10-08 that ADR 0019 retired: the
offline contract suite now starts the real pinned install against a loopback
stand-in and holds the tool declaration, the ambient-configuration isolation,
the session policy's foreign-read blocking and the provider address and key
mapping, while the reviewer's reads stay unconfined. The maintainer accepted the unconfined reads as a residual
risk for ADR 0007's reviewers on 2026-09-30, and ADR 0011 accepts it again for
the rungs, naming Pi and the secrets file: the unconfined reads ADR 0007
accepted for its reviewers extend to them. The leak check scans what this
repository presents, not what else the disk holds.

### The draft (phases 2, 2b and 3)

`python3 scripts/stage2.py draft <change>` has Codex (`gpt-6.1-sol`, effort [`CODEX_EFFORTS["draft"]`](../scripts/stage2.py)) write
`spec.md`, `design.md` and `plan.md` in one call (ADR 0016). The
guards are `implement`'s: the preflight (a `research.md` with its bead, a
`decisions.md`), the refusal of pre-existing changes outside the change's
`findings.md`, the declaration and the leak check before each attempt's call,
the credential scans, and exactly one commit when an attempt passes. A draft's
Codex call runs in the CLI's `workspace-write` sandbox; what the runner can
see — what git reports changed — it bounds: every path outside the change
folder is put back at the baseline before verification, a new ADR file under
`docs/adr/` excepted, and the change's `decisions.md` is put back with them.
If the call moved `HEAD`, the run stops without a rewrite. `make verify` runs
after the put-back, and a red run fails the attempt — with one exception:
the runner sets `ADR_ANSWERS_TOLERATE_CHANGE=<change>` for that one run, and
the gate `adr-answers` then reports this change's own missing ADR answer
without failing (another change's missing answer, a refused answer file and
every other gate still do), so the exit code of `make verify` decides and the
runner reads no gate output. Only the maintainer's stated answer may create
that file (`decisions/answers/<change>/adr.yaml`); `findings.md` then says the
answer is owed. A new ADR file is one that exists now and that the merge base
of the baseline and `origin/main` does not hold, so a second draft edits (or
renames) the first draft's ADR instead of adding another. The chain is three attempts: Codex, a second
Codex attempt with the first one's diagnostics, then `glm-5.3` with both — a
failed call is put back and moves along the same chain, a failed post-run
check leaves its tree and its quoted block, and three failures exit 1. The
GLM key is read only when the GLM attempt is due, and a draft takes no
`--stage2-off`: where Stage 2 is off, Opus 5.5 drafts as §3 says, by hand.

A drafted change runs in this order:

1. `python3 scripts/stage2.py draft <change>` — Codex writes `spec.md`,
   `design.md` and `plan.md`, up to three attempts, GLM 5.3 after two failed
   Codex attempts.
2. The orchestrating session reads the whole draft against the change's
   problem.
3. `python3 scripts/stage2.py spec-review <change>` — Opus 5.5 reviews the
   spec (phase 2a), its rows into `findings.md`.
4. A second `draft <change>` works the review's open rows in, once the
   maintainer has answered every `[AMBIGUITY]` a row raised.
5. The plan card reaches the maintainer unchanged — the veto stays theirs.

What the runner cannot see: which paths a draft's Codex call reads, and
whether its sandbox in fact confines its writes. The put-back bounds what git
sees, not what the program touched elsewhere — not an ignored file, not a
path outside the worktree, and not the repository's git directory (`.git`:
hooks, config), which `git restore` and `git clean` never touch although the
runner commits right after the draft; that residual risk is ADR 0016's to
state, and the first real draft is a later change's.

### The interactive session (`session`)

`python3 scripts/stage2.py session <change> --model <id>` starts one interactive
model session for the change in a new macOS Terminal window, from the same
checked runner as every other call. The `--model <id>` is required and taken
literally: a plain id selects what `openai-codex` lists and dispatches the
official Codex CLI; a full `opencode-go/<model>` id selects `opencode-go` when
that entry lists the bare `<model>`, as the reviewer declaration writes it, and
dispatches the pinned Pi through the repository wrapper `tools/pi/pi` with the
full id: the id names the endpoint, not the
program, and the OpenCode CLI is never called. No alias, no prefix guessing, and the
session approves no endpoint: a model the declaration does not list for a session
transport is refused before anything starts, and the Pi path opens only for the
models that `opencode-go` lists for framework content in `model-endpoints.yaml`.
A Pi that is not the pinned version is refused; the runner checks the pin after
its argument and handover checks and before any call, so nothing is sent first —
the pin check and the confirm-load, like the dispatch itself, go through the
wrapper (ADR 0019), never a global `pi`. `--handover <path>` names another
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
permissions are a configuration, not a confinement at the operating-system
level. Codex gets `workspace-write` with approval on request. Pi asks for no
approval and has no sandbox, so the runner supplies one policy extension, copied
into the session's private directory and loaded alone (`--no-extensions -e`).
The session also takes `--no-mcp`, `--no-skills`, `--no-prompt-templates` and
`--no-themes`, so an MCP server cannot add a file tool that the extension does
not see; context files stay on, so the session reads the repository's
`AGENTS.md` (maintainer, 2026-10-09). The extension keeps `read`, `grep`, `find`, `ls`, `edit` and `write` inside the worktree,
keeps `edit` and `write` off its own file, `.stage2-sessions/` and `.pi/` (not
`.git/`), and asks before a recursive `rm`, `sudo`, `chmod` or `chown` with 777,
and before the git commands that discard unsaved work (`git reset --hard`,
`git clean`, `git checkout -- <path>`, `git checkout .`, `git checkout -f`, and
`git restore` unless it only unstages), blocking them when no UI can ask. The
patterns read the command's text and do not parse the shell: a word split by
quotes (`s""udo`), built by expansion or run through `eval` or `sh -c` is not
recognised, and everything else the list leaves out runs unasked. The runner
confirms only that the extension loaded (Pi lists its flag in `--help`); how its
handlers behave is held by tests that run without Pi. Every shell command
outside the dangerous patterns runs without a question, network programs and
`git push` included, and a shell command, asked or not, can read what the user
can read, the sign-in directory `~/.pi/agent` included: `cat` on it does not
ask, and its output goes to the endpoint. The Pi session signs in with that
directory, which may hold other providers' credentials, so a model switched
inside the session can leave the declared endpoint unscanned. The runner
passes neither `PI_CODING_AGENT_DIR` nor `SSH_AUTH_SOCK` on, so a custom agent
directory is ignored and `git push` over SSH fails inside the session.

One audit line goes into the change's `findings.md` per attempt, first with
`dispatch pending.`, then `dispatch accepted.` or `dispatch failed (<why>).`
(the file's `updated:` date follows the write; no other line changes) Accepted means Terminal took the command, nothing
more: whether the CLI started, authenticated or answered shows in the new
window, and a missing CLI or `osascript` is refused beforehand as a
prerequisite. The runner's launch files live in a fresh private directory under
the gitignored `.stage2-sessions/` in the worktree; they carry the launch script
and, for Pi, the policy extension, no prompt and no credential. A refused or failed attempt, or one
stopped before the dispatch, removes its directory, an accepted one keeps it for the session to load, and
nothing user-owned there is ever written or deleted. The runner reads no
credential file, copies no caller token, hands Pi no key and sets no Pi agent
directory, and starts no headless verb — no `codex exec`, no Pi print or RPC
mode, and no call to the OpenCode CLI. The verb neither runs the review loop nor
changes which reviewer sees what: the review order is not this verb's business.
Its decision record is ADR 0012.

### The review loop (phase 4b)

After implementation and before phase 6, `review-loop` runs one round: the
round's rung reads the change's diff against its merge base with `origin/main`,
uncommitted changes included, and answers in table rows. **At most three
rounds, and round 3 only when round 2 wrote at least one taken row.** The rows
go into a **loop record** outside the worktree and outside the git directory
(`${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md`),
not into the repository: the phase-6 reviewer writes its verdict before it
reads any loop row.

The orchestrator writes beside each row its `Status` — `taken — <test or
criterion>`, `taken — not a test — <reason>` for a finding no test can show,
or `rejected — <reason>` — and, for a taken row, `Broke a test`. The runner's
`repair` verb repairs the taken rows ("Repairing taken findings" below) and
runs `make verify`, which must be green before the next round starts. **The
evidence rule of §2 holds here:** a finding is taken
only when a test demonstrates it or the spec supports it. A row left
undecided holds the next round and the release.

The phase-6 reviewer writes its verdict first: the table, and under it the line
`Phase 6 verdict: <reviewer> <session>, <date>` (the runner writes it for the
resumed reviewer; an Opus reviewer writes its own). Only then does
`release-loop` carry every loop row into `findings.md` with the reviewer its
round had, and the reviewer marks each row in its `Phase 6` column, `agree` or
`disagree — <reason>`. Nothing is netted: the reviewer's view of the loop's
rows is the information.

### Repairing taken findings (repair)

**The orchestrator decides, the verb repairs, the reviewer re-checks.** The
orchestrator writes `taken` or `rejected` on a phase-6 finding as into a loop
row, marks a finding no test can show `taken — not a test — <reason>` when
taking it, and starts the re-check afterwards: the loop's next round for loop
rows, `review` for phase-6 findings. The verb starts no review of its own.

`python3 scripts/stage2.py repair <change>` takes every taken row — of the
loop record, of every released block and of every phase-6 table — to Codex
in one guarded call, and refuses while a row stands undecided or an ID is
doubled. The model answers one **fixed line** per row, `<ID>: fixed —
tests/<path>::<function>` or `<ID>: fixed — not a test — <reason>`, in the
form of ADR 0013's criterion ledger; only a row taken as `taken — not a test`
may be answered `not a test`. Headings, fences and report prose around the
fixed lines are ignored; a colon line whose id looks like a finding id
(`L1-2`, `F-12`) and names no taken row still fails the attempt. Loop ids
always count; letters-hyphen-digits ids count only when their prefix occurs
in the change's row ids, including rejected and fixed rows. Other prefixes
(such as `ADR-0017:` or `UTF-8:`) remain report prose. A hand
repair books itself in the row's Status alone: replace the finished row's
`taken — …` with one of the two fixed statuses and set the loop row's
`Broke a test` mark from the evidence. A Status that still begins `taken`
while naming a fix in the old form (`; fixed by …`, `; fixed: …`,
`; repaired by …`) stops the repair before any call, and the row stands as it
is. **Red first:** the runner proves each repair of code by running the named test alone against the baseline's code, in a
temporary git worktree whose `tests/` is the attempt's, and accepts a test
only when pytest exits 1 or 2 there. When every post-run check passes —
`make verify` green, a measured line in the time log, every fixed line
checked — the runner writes each row's Status `fixed` in its place, makes the
one checkpoint commit `fix(<change>): repair taken findings <IDs>` and marks
the loop record after it. The attempts are Codex, one fresh Codex attempt
with the first one's diagnostics, and Sonnet 5.5 at effort `medium`, the last
only after two failed post-run checks; a failed call stops the run without a
fallback and `--stage2-off [REASON]` runs Sonnet 5.5 alone and records why. A
leak-check BLOCK stops without a fallback, and a Codex call that moves HEAD
stops the run unrewritten. A fixed row counts as a taken one for round 3
and for the run count; **`Broke a test` stays the orchestrator's mark**,
written from the run's evidence before the next round or the release. The
rungs keep their read-only tools. **The exception (ADR 0017):** Codex, which
reviews phase 6, also repairs; its own session never does both — a phase-6
re-check (a `review` run after an earlier `## Phase 6` block) starts a fresh
read-only Codex session, resuming neither the repair nor an earlier thread.
The sandbox is the CLI's configured `workspace-write`; the tests show the
configured call, not the CLI's confinement.

### Two columns for every stage-2 change

Beyond the vocabulary of §2, a stage-2 change's `findings.md` carries two
columns, defined here because the findings template is not in this repository
yet:

- **`Reviewer`** — the rung that raised the finding (an id of the ladder), Codex, or Opus: who raised it.
- **`Broke a test`** — for each taken row, `yes` when its repair turned a test
  red that was green before it, `no` when it did not. The finding's own new
  test does not count: the evidence rule expects it to be red first.

### Measuring the first three stage-2 runs

A **stage-2 run** is a change whose review made at least one call; runs are
counted in the order their pull requests merge. Every finding records its
reviewer, whether it was taken or rejected and, if taken, whether it broke a
test. **After the third run, a short evaluation is written under
`docs/research/`. If at least one taken finding of Codex or of a rung broke a test, stage 2
falls back to Opus 5.5 until the maintainer decides again** — a taken finding
of a rung counts like a GLM finding counted before 2026-10-07, a Codex one
still counts as ADR 0007 set it, and
Opus 5.5 reviews every change, and phases 1 and 4 return to §3's Haiku 5.5 and
Sonnet 5.5. The rule is written, not counted by a script: a person reads the
evaluation, and its pull request applies the fallback. This replaces the three measured runs that
D-13 asked for before the first foreign call; what the replacement gives up is
the measured stage-1 baseline (ADR 0007).

**The count is generated, not typed.** `python3 scripts/stage2_runs.py
<change> … [--rev <commit>]` reads each change's `findings.md` and
`research.md` (active or archived) with the runner's own row and line
constants and prints, per change, the loop rows taken / rejected, the rows
whose repair broke a test, the phase-6 rounds, the phase-2a and phase-6 rows
by severity, the loop rows marked `disagree`, and the calls behind a clean
leak check; under that, D-13's criteria as numbers. It counts; it applies no
rule. At `cc020f5` (2026-10-08), over the first three runs:

| D-13 criterion | Number at `cc020f5` |
|---|---|
| 1 — replaced by the first three stage-2 runs | 3 runs measured; 0 rows marked as having broken a test |
| 2 — lakeswitch-ai's disclosure decision | no number: it governs content this repository never sends, and stays lakeswitch-ai's (ADR 0007) |
| 3 — leak check green in every run | 18 of 18 recorded calls clean; a refused call writes no line, so a refusal is not in the count |
| 4 — foreign endpoint declared with residency | 3 of 3 foreign routes cleared by `model-endpoints.yaml` |

Tokens and cost per vendor are not recorded by the runner and are not in
the count. The generated table and what it adds to the typed one:
`docs/research/2026-10-08-stage2-three-runs.md`, addendum of 2026-10-08.

> **Two caveats, and the second one holds here in particular.** The vendors'
> coding subscriptions are contractually limited to officially supported tools,
> and each runs through its own client: Claude Code for Z.ai, the Codex CLI for
> OpenAI and Pi for OpenCode Go. Pi is a client the Go page lists as validated,
> under terms of service that name no third-party client — a risk the
> maintainer accepted on 2026-10-08. In a self-built harness none of this is
> covered. The runner starts those programs, it does not replace them.
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
