<p align="center">
  <img src="docs/assets/monotrope-banner.png"
       alt="monotrope: an infinity ribbon, a winding path, a bicycle disc brake"
       width="100%">
</p>

# Monotrope

**Let AI agents do the work. Keep the decisions and the evidence.**

**What this is.** Monotrope is a file-based workflow for AI coding agents, and
this repository is its home: the rules, phase prompts, templates, gates and
reference implementation. It defines how a change is researched, specified,
planned, implemented and reviewed; Claude Code and Codex do the work, and you
decide what it is for and what must not happen. It develops itself with the
same workflow. It is for people who need an audit trail they can resume from.

**What this is not.** Not an agent program, not a server, not a model gateway,
not a general runner for arbitrary harnesses, and not a ready-to-install
product for every repository. The one runner here, `scripts/stage2.py`, starts
foreign models for specific phases; it does not orchestrate the workflow.

Almost everything in between — research, answers, choices, contract, findings
and the next session's starting point — is written to versioned files. The
review loop's working rows are the exception: they stay outside until phase 6.
Most agent workflows keep that state in the conversation; Monotrope keeps it in
the repository.

Markdown and YAML in git, a small Python toolchain, a tracker in the
repository's git refs, and one instruction entry (`AGENTS.md`) that Claude Code
and Codex read. The files outlive the harness, so another session or model can
finish a change; Claude Code is the full orchestration path for now.

> **Status:** early and moving fast. [What works today](#what-works-today)
> separates what a tool enforces from what is a written rule and from what is
> not built yet. The repository and its tracker still carry the working name
> `coding-harness` in places.

> **License:** source-available under the PolyForm Noncommercial License 1.0.0.
> Noncommercial use is free; commercial use needs a separate written license.
> See [License](#license).

## The problems, and what Monotrope does

Seven failures show up when agents do the work without a process around them.
The table maps each to the mechanism that answers it, and to where that
mechanism lives.

| Failure | The mechanism | Where to see it |
| --- | --- | --- |
| The chat is the state | Steps leave their results as files; a session ends with a dated handover, and the next session reads the files instead of a summary | `plans/changes/<name>/`, `docs/journal/handover/` |
| Context dies with the harness | Files outlive the tool; one instruction entry; models are assigned per phase and per job | `AGENTS.md`, `plans/`, `docs/adr/` |
| Decisions are invisible | Open points are classified; every answer records who decided and when; a decision takes effect when its pull request is merged | `plans/changes/<name>/decisions.md`, `plans/changes/<name>/spec.md`, `decisions/answers/<change>/adr.yaml`, `provenance.yaml`, `docs/adr/` |
| A red tree ships | One gate list drives the local run and CI; every gate is block, report or advisory; a repair's test must fail before the repair | `decisions/gates.yaml`, `scripts/verify_all.sh`, `scripts/stage2.py` |
| One reviewer has one blind spot | A review loop of several models from different vendors, served through one operator, cheapest first; a finding needs a test or the spec; the reviewer session never repairs | `plans/changes/<name>/findings.md`, `scripts/stage2.py`, [ADR 0021](docs/adr/0021-review-swarms-until-clean.md) |
| Parallel work overwrites itself | One worktree per change, one tracker writer, a claim for every other session, a warning when sessions share a checkout | `AGENTS.md`, `tools/bd`, `tools/claude-code/` |
| A foreign model can see too much | An endpoint allowlist by data class and a leak check before every call; a leak stops without a fallback | `model-endpoints.yaml`, `scripts/stage2.py` |

Not all of it is enforced by a tool. [What works today](#what-works-today)
separates the three levels: enforced, written rule, not built.

Two mechanisms need more room than a table cell — the review swarms and work
in parallel. Both follow the process overview below.

### What sets it apart

- **Resumable by anyone.** The state is in versioned files, so another
  session, harness or model can finish a change.
- **Proof that cannot quietly vanish.** Every criterion names its test, a
  gate holds that test, and a repair counts only when its test failed first.
- **Gates that test themselves.** One list drives the local run and CI, and
  every gate has a run that turns it red.
- **Several vendors review, none repairs its own finding.** The swarm runs
  cheapest first until a round is clean, behind a data allowlist and a leak
  check that stops without a fallback.
- **The human keeps the decisions.** An answer records who decided. It takes
  effect on merge. Every question arrives with its context.
- **It hands itself over.** The kit runs green in an empty repository, and
  the workflow develops itself with its own rules.
- **Three lanes, one writer.** One session keeps three changes moving and is
  the only one writing the tracker
  ([three lanes](docs/orchestration.md)).

### Brakes that spare your attention

Agents scale with the budget; the person deciding does not. When every
change ends in a review and every step in a question, the day turns into a
stream of small judgements. Monotrope treats that as a design problem: besides
the parts that make agents faster, it builds brakes that keep their output
safe and that decide what reaches you at all.

| Brake | How Monotrope does it | Level |
| --- | --- | --- |
| Constrain the agent before it writes | Research, an interview with minimums by class, a spec with numbered criteria, a plan card you can veto, an appetite that stops the work at its limit (it extends once by itself, up to twice its size) | interview minimums and validators enforced; veto and appetite are written rules |
| Limit the mistakes it can make | Foreign models start only through one runner, behind an endpoint allowlist and a leak check that stops without a fallback; one worktree per change; one tracker writer | runner and leak check enforced; worktree and writer rules written |
| Check in layers before anything merges | `make verify`, a review loop of several vendors until a clean round, a separate phase-6 review, CI, and a merge queue that tests each pull request against the current `main` | enforced |
| Raise only what needs you | Open points are sorted: `[DECISION]` goes to you, `[GAP]` is explored, `[DETAIL]` is decided by the agent with its reason written down; only decision pull requests wait for your merge, the rest merge themselves on green CI | a spec with an open `[DECISION]` fails its gate; decision PRs by template; self-merge is a written rule |
| Batch what does reach you | Questions wait for one daily block, one at a time, each with its context (topic, why now, today, what changes); plan cards and status come together, not per step | written rules ([ADR 0018](docs/adr/0018-every-question-carries-its-context.md)) |
| Let you step away | Every step commits; a session ends with a handover file, so the next one resumes without you rebuilding the chat; a night run works from a written plan | handover schema enforced; night plan written |

Not built yet: a measurement of how many questions, decisions and reviews
reach you per day, and a rule that routes your attention by a change's risk
rather than by its class alone (bead coding-harness-n4bh).

## How a change runs

A change runs through seven core phases, plus the optional steps the table
lists. Almost every step leaves its result in the repository, and the next step
reads that instead of a chat.

Your moments are highlighted; the rest is done by agents and checked by
machines.

<p align="center">
  <img src="docs/assets/readme-how-a-change-runs.png"
       alt="Three lanes — you, agents, machine checks — with the seven phases from explore to commit. Your four moments are state the goal, answer the interview questions, read the plan card, and merge. The review loop and the review send findings back to implement; a shield marks the leak check before every external model call."
       width="100%">
</p>

The table lists every step and what it leaves behind.

| # | Phase | What it leaves | The question it answers |
| --- | --- | --- | --- |
| 1 | Explore | `research.md` | What is the situation? |
| 1a | Interview | `decisions.md` | What must a person decide? |
| 2 | Spec | `spec.md` | What exactly should change? |
| 2a | Spec review (optional) | rows in `findings.md` | Does the spec hold up? |
| 2b | Design (by class) | `design.md` | How is it built? |
| 3 | Plan | `plan.md` | In which steps, and when is it done? |
| 4 | Implement | code and tests | Does it work? |
| 4b | Review loop (when it runs) | a loop record outside the repository; rows enter `findings.md` after the phase-6 verdict | Does the change survive the swarms? |
| 5 | Verify | test output | Can we show it? |
| 6 | Review | `findings.md` | Does it match the spec? |
| 7 | Commit | a pull request | Does CI agree? |

The interview (1a), spec review (2a), design (2b) and review loop (4b) join
when a change needs them. A session that ends leaves a dated handover file:
the objective, the evidence, what is open, and the one action to resume with.

What a change asks of you is short:

1. **State the goal** — what the change is for, and what must not happen.
2. **Answer a few questions** — only the ones that are yours to answer.
3. **Read the plan card** — what changes for you, when it is done, the time
   limit, what is left out. The work starts unless you say stop.
4. **Merge the pull request.**

One finding looks like this, shortened from the
[archived example](plans/changes/archive/2026-09-29-frontmatter-current/findings.md):

| ID | Severity | Dimension | Where | Finding |
| --- | --- | --- | --- | --- |
| F-1 | MAJOR | MAINT | `docs/adr/0001-early-parallelism.md` | The header says `status: accepted`; the body records the ADR as superseded. |

Models are assigned per phase: one drafts, another reviews, a third
implements.

## The swarms

A **swarm** is several models reviewing the same change at once, each in a
fresh session. It exists because a reviewer cannot see its own blind spot, and
because models from one vendor can share a failure mode. The loop adds models
from other vendors and higher-cost models only while no clean round has been
reached: cheap rounds first, expensive ones only when a round is not clean.

All loop calls go through one operator, OpenCode Go. The models come from
several vendors, but the data recipient is the same.

### The review loop (phase 4b)

The loop runs after implementation and before the final review. One call runs
one round; the orchestrator calls it again until a round is clean or a stop is
reached.

| Review stage | Who reviews | How | What it sees |
| --- | --- | --- | --- |
| 1 — free swarm | every reachable free model the `free_stage` rule selects from a live catalog refresh | in parallel | source and test hunks only, no tool access |
| 2 — Flash swarm | up to three of the cheapest reachable paid models whose data terms allow the work | in parallel | the full change diff, read-only tools |
| 3 and later — the ladder | one eligible paid model per round, cheapest first by its declared request allowance | one at a time | the full change diff, read-only tools |

A skipped review stage — the free stage on a change without source or test
hunks — does not use a round number. Pi, the pinned agent program, carries the
calls; the ladder is ordered by declared cost, and a failed Flash member is
replaced by the cheapest unused rung. A round is **clean** when every row is
decided and none is accepted.

The loop stops at a clean round, when the ladder is exhausted, or after two
consecutive rounds accepted only findings that earlier repairs introduced. The
last is a brake: a person decides. A spent ladder is not refilled. A reviewer
whose answer cannot be read is asked once more with a format reminder, and a
free round that is rate-limited moves on to the Flash swarm.

**What a round sees.** The free round sees bounded source and test hunks
against the merge base with `origin/main`; the paid rounds see the whole change
diff. Both include uncommitted changes, and the runner adds untracked files. A
cut diff is recorded and cannot count as clean; the exact bounds are in
[how it works](docs/how-it-works.md#runner-details).

`prepare-loop` probes the admitted candidates at least once, with static input
and no tools, and issues a short-lived receipt. A probe is a call per
candidate, including the expensive end, not a review round; the details are in
[how it works](docs/how-it-works.md#runner-details).

**The guardrails.**

- All calls go through one runner: endpoint allowlist, a leak check before
  every call, no fallback. Free models run under unread terms, diff-only and
  without tools. A paid model needs a terms reading with a declared expiry
  date; once that date has passed it gets no calls until a renewed reading
  is merged, and the runner warns before it runs out
  ([ADR 0022](docs/adr/0022-paid-model-terms-expire.md)).
- A finding needs a test or the spec; a disagreement blocks like a defect.
- Reviewer and repairer are separate sessions. The final review may resume the
  recorded 2a thread, a re-check starts fresh, and its verdict comes before any
  loop row.
- Paid rounds get read-only tools; that boundary is a prompt, not a sandbox.

### The research swarm (phase 1)

A `feature` or `architectural` change explores through a swarm
([ADR 0020](docs/adr/0020-phase-1-research-swarm.md)); a `bounded` change
or a `spike` keeps a single explorer. The swarm runs in stages:

1. **Finders** — three repository seats map the sources independently; one
   Opus 5.5 context merges their maps.
2. **Topics** — eleven topics on the same brief: eight about the repository
   (code, interfaces, rules, architecture, neighbours, history, tests,
   risks), each read by the three repository seats, and three about outside
   practice (best practice, existing tools, public failure reports), each
   read by three online seats. Selected free models add public topics, best
   effort.
3. **Judge** — one fresh Opus 5.5 context reconciles the reports into
   `research.md`.

Every call goes through the runner and its leak check; a run that misses a
required part is marked incomplete and exits with an error. A gate then checks
that the interview answers each item the research raised and that the spec
names the same neighbours and cites the research for each criterion.

### What the swarms do not prove

The loop is a mechanism, not a measured claim: whether a second vendor finds
more errors than one has not been measured. Its value is the structure — fresh
sessions, several error profiles, evidence for every row.

## Working in parallel

Parallel work is allowed and expected; what it must not do is lose work
silently. The workflow makes the boundaries explicit:

1. **One change, one worktree.** One change, one bead (the tracker item, with
   the class in its description), one branch, one worktree, one session. The
   worktree is branched from a freshly fetched `origin/main` and lives under
   `.claude/worktrees/<name>`. Run `make venv` and `bash tools/pi/install.sh`
   once in it before `make verify`; remove it after the merge. Nobody switches
   the branch of the main checkout while another session is running.
2. **One tracker writer.** While more than one session writes, the first-started
   writing session owns the tracker: it hands out, reprioritises, links and
   closes beads. Every other writing session writes only its claim
   (`tools/bd update <id> --claim --actor <session>`) and its handover comment
   on that bead. At most two writing sessions run by default.
3. **A clash warning before the first edit.** In this repository's Claude Code
   setup, a hook scans the live sessions at start, and again on a prompt when
   the set of clashing sessions changed, and names any that share the
   checkout. The person then decides whether to continue or open a worktree.
   It is a warning, not a lock.
4. **A handover, not a shared chat.** A session that ends leaves a dated
   handover file; the next session starts from it. Sessions working in
   parallel read each other's committed state, not a live conversation.
5. **The tracker travels safely.** The tracker is a Dolt database under
   `.beads/`, transported via `refs/dolt/data`. `tools/bd` finds it from any
   worktree; concurrent claims have one winner (measured 2026-09-23 with bd
   1.3.0). Push tracker first, git second: CI renders the gate from the
   tracker, so a git push that outruns it goes red.

### Pull requests stay mergeable

On 2026-10-27 five open pull requests could no longer merge `main`. The rules
since then (maintainer, 2026-10-27; [`docs/WORKFLOW.md`](docs/WORKFLOW.md),
§3):

- **Synced daily.** Each open pull request is test-merged against `main`;
  a clean one gets `main` merged in, a conflicting one is reported with its
  files.
- **Asked about after five working days:** finish, shrink or close.
- **Small enough to review:** above about 800 changed lines, a change is cut
  into slices, one pull request each.
- **Few at once on a hot file:** at most three open pull requests change the
  same heavily used file; the oldest is finished first.
- **Reviewed on a current base:** the final review runs after `main` is
  merged, and its verdict holds only for the commit it saw.
- **Generated files are regenerated** on a conflict, never merged by hand
  (`python3 scripts/pr_sync.py merge-main` does it for `plans/INDEX.md`).

### The rhythm of a working day

- **One decision block a day.** Questions and merge requests for the
  maintainer are collected for one block at 15:00 local time; work that
  does not depend on them goes on. A security question, a leak-check block
  or a stop that blocks every lane is asked at once.
- **The second finding of one mechanism ends case-by-case repair.** When the
  final review finds another case of a mechanism a repair already
  addressed, the orchestrator proposes a structural remedy and the
  maintainer chooses.
- **Night runs** work their queue alone and in order. When Codex is at
  capacity they wait and retry once, then let Sonnet 5.5 take that one step;
  a further case of the same mechanism is recorded and parked for the
  morning.

What is not enforced: the one-writer rule is a working agreement until the
write guard exists; worktrees share git's refs, hooks and configuration, so
isolation separates files, not execution; and orchestrating many agents in
parallel is evaluated, not built (the third development stage:
orchestration).

## Not every change is the same size

Every change names its class in the bead description and in the head of its
spec. The class sets how much process the change gets; the kind of an open
point (below) sets who decides it.

| | `spike` | `bounded` | `feature` | `architectural` |
| --- | --- | --- | --- | --- |
| What it is | answers a question; the output is a recommendation | changes an existing, readable flow without deciding anything new | a self-contained deliverable that changes what the system must do or how it is checked | a new subsystem or a broken interface |
| Questions you must answer | three topics, or a reasoned skip | one, or a reasoned skip | at least three; five total when it creates or changes an ADR | five when it creates or changes an ADR |
| Design phase (2b) | never | never | yes, or one sentence why not | always, with an ADR draft |
| Review by another vendor | no | yes | yes | yes |

A gate counts the answered questions against the class's minimum. In every
class, a change that claims an ADR file in its spec header and changes it owes
five answers. Nothing yet checks that the class itself is right: a `feature`
declared as a `spike` would skip the other-vendor reviews, and only the review
before the merge catches it.

## Where decisions live

Every decision is a file, and each kind has one place:

| Decision | Where it is recorded |
| --- | --- |
| Your answers in a change's interview — the `[DECISION]` points | `plans/changes/<name>/decisions.md`: your words where you gave them, with the date and the question |
| The agent's own choices — the `[DETAIL]` points — and departures from the plan | marked lines with their reason in the change's `spec.md`, `design.md` or `plan.md` |
| Your answer to "does this change need an architecture decision record?" | `decisions/answers/<change>/adr.yaml`: answer, reason, the proposal shown, who answered and when; a gate checks it |
| Architecture decisions | `docs/adr/`; a record takes effect when its pull request is merged |

Open points come in three kinds:

| Kind | Who decides | What happens |
| --- | --- | --- |
| `[DECISION]` | you | intent, anything irreversible or risky; your answer goes into `decisions.md` |
| `[GAP]` | the agent | a missing fact; the agent looks it up and does not ask |
| `[DETAIL]` | the agent | a name, an order, a format; the agent decides and writes down why |

`provenance.yaml` declares which files only a person may change; touching one
makes a decision pull request. A finished change leaves its lasting parts in
`plans/specs/` or `docs/adr/`; the rest is archived with its decisions.
Handovers summarize a session; they are not the record.

## Design rules

Files, because a change must outlive the tool; one list, because two drift; a
merge, because a decision in a chat is not a decision; evidence over
summaries. The full set, with the gate count and the focus rules, is in
[how it works](docs/how-it-works.md#design-rules).

## How it is checked

`make verify` runs the same gate list as CI: tests, lint, the kit's classified
tree, documents and process rules. The environment is locked, and a repair
counts only when its test fails on the code before the repair. One machine runs
one `make verify` or runner check at a time; the next one queues, and waits
while free memory is low. The strategy,
in six layers and with what it does not prove, is in
[how the workflow tests](docs/testing.md); this repository's numbers are in
[how it works](docs/how-it-works.md#how-testing-works-and-what-it-does-not-prove).

## What works today

Checked on 2026-11-01 against `main` at `ac11da5d`.

### Enforced by tooling

- `make verify` and CI run the gate list: tests, lint and the process checks
  above. Every gate declares whether it blocks, reports or is advisory.
- The foreign-model runner (`scripts/stage2.py`) checks the endpoint and runs
  the leak check before every call to another vendor. Exploring, drafting,
  implementing, repairing and reviewing by other models all go through it.
- The review loop runs until a round is clean or a named stop (ADR 0021), with
  the availability probe and its receipt before a fresh run.
- The research swarm explores `feature` and `architectural` changes
  (ADR 0020), and gates check that the interview and the spec carry what it
  found.
- A paid model whose terms reading has passed its declared date gets no calls
  (ADR 0022).
- A repair counts only when its test fails on the code before the repair —
  by an assertion or pytest's own failed outcome, never by a crash.
- A runner attempt fails fast: lint and the attempt's own tests run before the
  full `make verify`, and a draft runs only its document gates.
- One admission per machine: a second `make verify` or runner check queues
  instead of overloading the machine, and waits while free memory is below a
  floor.
- `main` takes a pull request only when the `verify` check is green on the
  merge candidate: through the merge queue, or, without it, once the branch is
  up to date with `main` (repository ruleset, rule RB-G7).

### Written rules agents follow, not enforced by a tool

- The three kinds of open points.
- The plan card as a contract.
- The communication form: a gate checks that the context is there, not how it
  is worded.
- One writer per tracker, until the write guard exists.
- The rules that keep pull requests mergeable, the daily decision block and
  the night-run rules. The sync of open pull requests is a script
  (`python3 scripts/pr_sync.py sync`), run on request; nothing schedules it.
- The appetite: it extends once by itself, up to twice its size, and the
  extension is written into the plan. `make report CHANGE=<name>` shows the
  time used against it, read-only; nothing stops a run at the limit yet (bead
  coding-harness-uxa9).

### Not built yet

- A validator for the change files and a stop hook that blocks a session end
  on a red tree: described in the doctrine, not built. The `/workflow-start`
  command, the `make change` and `make index` targets and the gate catalogue
  (`docs/governance/gate-catalog.md`) exist since bead coding-harness-i0l.
- A sandbox around paid reviewers, and keeping the work of a failed model
  call (partly built).
- Orchestration of many agents in parallel: evaluated, not built.

## See a completed change

The archived "frontmatter-current" change shows every step with real files —
research, decisions, spec, plan, a finding and its fix. The table is in
[how it works](docs/how-it-works.md#follow-one-completed-change).

## Try it

You need Python 3.12 or newer, Node 26 with npm, git and curl on macOS or
Linux. `make venv` picks `python3.12` or `python3`; name another interpreter
with `make venv PYTHON=/path/to/python3.12`.

```bash
git clone https://github.com/bicycle-brakes/monotrope.git
cd monotrope
tools/beads/install.sh && tools/bd bootstrap --yes  # fresh clone: load the tracker
make venv                  # local .venv from the pinned lock (Python 3.12+)
bash tools/pi/install.sh   # pinned Pi; the real-Pi tests in make verify need it
make verify                # all gates
tools/bd ready             # open, unblocked work
```

These commands run this repository itself. There is no one-line install for
another repository yet: the mechanism travels as a kit, and a probe copies it
into a throwaway tree and runs its tests there, but the step-by-step onboarding
page is still being built. Until then, [`docs/WORKFLOW.md`](docs/WORKFLOW.md)
is the reference.

To start a change, create its bead (the tracker item) first, with the class in
its description, then `make change NAME=<name> BEAD=<id>` (in Claude Code:
`/workflow-start <name> --bead <id>`), and
read [`docs/WORKFLOW.md`](docs/WORKFLOW.md) from phase 1.

## Go deeper

- [How the workflow works](docs/how-it-works.md): the phases, which model does
  which job, the change and data classes, and the swarms.
- [How the workflow tests](docs/testing.md): the test strategy, part of the
  kit.
- [Three lanes](docs/orchestration.md): how one session runs three changes
  at once, and what is still kept by hand.
- [The doctrine](docs/WORKFLOW.md): every rule, gate and route in full.
- [Architecture decisions](docs/adr/): why it is built this way.
- [The research swarm](docs/adr/0020-phase-1-research-swarm.md): how phase 1
  explores a larger change.
- [Session handovers](docs/journal/handover/): what each session left for the
  next one.
- [`model-endpoints.yaml`](model-endpoints.yaml): which model may see which
  data.
- [`AGENTS.md`](AGENTS.md): the instruction file the agents read.

## Contributing

- **Tracker.** Work is tracked in Beads, read and written only through
  `tools/bd`. A pull request names every bead it opens, changes or closes.
  While more than one session writes, the first-started session owns the
  tracker; every other session only claims its bead and comments its handover
  there.
- **Decision pull requests** take effect when the maintainer merges them.
- **One change, one branch, one worktree, one session.**
- **Before a pull request.** Per checkout: `make venv` and
  `bash tools/pi/install.sh` once, then `make verify`; a text-only change is
  gated by CI.
- **Contributions.** By opening a pull request you agree that your
  contribution may be distributed under the project's license and, if needed,
  under a commercial license. See [`COMMERCIAL.md`](COMMERCIAL.md).
- **Language.** Repository artefacts are in English.

## License

Monotrope is **source-available** under the **PolyForm Noncommercial License
1.0.0**. Noncommercial use is free; commercial use needs a separate written
license. See [`LICENSE`](LICENSE) and [`COMMERCIAL.md`](COMMERCIAL.md).

Releases published before 2026-10-20 were under Apache 2.0. That grant remains
for those releases.
