
<p align="center">
  <img src="docs/assets/monotrope-banner.png"
       alt="monotrope: an infinity ribbon, a winding path, a bicycle disc brake"
       width="100%">
</p>

# Monotrope

**A model harness for coding agents, with versioned context and executable
checks.**

Monotrope structures AI-assisted software changes into research,
specification, implementation and review. It combines phase-specific prompts,
a Python runner for calls to other models, automated validation and explicit
human decisions.

State lives in versioned files rather than only in the conversation, so
another session or model can resume the work.

Its central design principle is to check an agent's claims against observable
evidence. A repair is accepted only when its regression test fails on the code
before the repair and passes after it. A call to another model is checked
against an endpoint policy, and its inputs are scanned for prohibited content
before dispatch.

Monotrope is used to develop this repository. Some boundaries are enforced by
tools; others remain workflow rules. [What works today](#what-works-today)
says which is which, and what is not built yet.

**What it is not.** Not an agent program, a server, a model gateway or a
one-line install for any repository.

> **Status:** young and moving fast — 300 pull requests merged since the first
> commit on 2026-09-16 (counted 2026-11-02). The repository and its tracker
> still carry the working name `coding-harness` in places.
>
> **License:** source-available under the PolyForm Noncommercial License 1.0.0;
> commercial use needs a separate written license ([License](#license)).

## Architecture

<p align="center">
  <img src="docs/assets/readme-who-steers-a-change.png"
       alt="Who steers a change: the person sets goals, answers decisions and merges every pull request; the orchestrating agent reads and updates the versioned state and starts the Python runner; the runner builds the phase instructions, applies the endpoint policy and leak check, and sends allowed input to external model sessions; those sessions edit the change worktree and return a response to the post-run checks, whose results go back to the agent; the worktree goes through local gates, a separate review and CI, failures return to the agent as repair work, and passed changes are merged."
       width="720">
</p>

The policy and leak-check boundary applies only to model calls dispatched
through the Python runner. Model sessions may change the worktree according to
their role; read-only instructions are not an operating-system sandbox.

| Component | What it does | Where |
| --- | --- | --- |
| Versioned state | research, interview answers, spec, plan, findings and handovers as files per change; task status in the Beads tracker | `plans/changes/<name>/`, `docs/journal/handover/`, `.beads/` |
| Orchestrating agent | runs the phases, asks the person, starts the runner | `AGENTS.md`, `prompts/` |
| Python runner | starts other models for named phases, checks the endpoint, runs the leak check, validates what comes back | `scripts/stage2.py`, `scripts/leakcheck.py`, `model-endpoints.yaml` |
| Gates | one list drives the local run and CI; each gate blocks, reports or is advisory | `decisions/gates.yaml`, `scripts/verify_all.sh` |
| Decision rules | files only a person may change are declared; a decision takes effect when its pull request is merged | `provenance.yaml`, `docs/adr/` |

The orchestrating agent coordinates the workflow. The Python runner controls
specific model calls and validates their outputs; it is not a complete
autonomous workflow engine.

### What the runner does

The runner, `python3 scripts/stage2.py <verb> <change>`, is the only way a
model other than the orchestrating agent touches a change. The agent decides
*when* a phase runs; the runner decides *how* the call is made and whether its
result is kept. Every call follows the same path:

1. **Before the call:** it builds the phase instructions from `prompts/`,
   checks the model and endpoint against `model-endpoints.yaml`, scans
   everything it will send with the leak check, and writes an audit line. A
   block stops the call, with no fallback.
2. **The call:** the model works in the change's worktree, within its role:
   reviewers read, drafters and implementers write.
3. **After the call:** the runner checks the result itself — the documents
   exist and validate, the repair's test failed before and passes after,
   `make verify` is green — and only then commits. A failed attempt goes to the
   next route with its diagnostics; a stopped one is saved on a side ref, so
   the work is not silently lost.

| Verb | Phase | What it starts |
| --- | --- | --- |
| `explore` | 1 | a research swarm (feature) or one fast model (small change) |
| `draft` | 2, 3 | spec and plan, written by another vendor's model |
| `spec-review` | 2a | a read-only review of the spec |
| `implement` | 4 | the code and its tests |
| `prepare-loop`, `review-loop` | 4b | the review swarms, round by round until clean |
| `repair` | 4b, 6 | the fixes for the findings the agent took |
| `review` | 6 | the independent review against the spec, in a fresh session |

The runner never merges, never decides which finding is taken, and never
asks the person anything; those stay with the agent and the maintainer.

### What the hooks do

Hooks are small scripts Claude Code starts on its own at fixed moments. They
show and remind; none of them is a gate — CI is.

| When | Hook | Does |
| --- | --- | --- |
| Session start | `tools/bd prime` (this repository, `.claude/settings.json`) | loads the tracker's working rules and the current state into the session |
| Session start | `handover.sh start` (user level) | shows where the last session stopped and its next step, measured against the working tree now |
| Session start, every prompt | `parallel-sessions.sh` (user level) | warns when another session works in the same checkout |
| Every prompt, end of a turn | `recap.sh` (user level) | keeps a one-line recap and a safety-net note in case a session ends without a handover |
| Always | `statusline.sh` (user level) | the status line: repository, branch, beads in progress, other sessions |

The user-level hooks live, documented, in
[`tools/claude-code/`](tools/claude-code/README.md) and are installed into
`~/.claude` by `tools/claude-code/install.sh`. A stop hook that holds a turn
end on a red tree is planned, not built (see [Not built yet](#not-built-yet)).

## A refused repair

The check that matters most is the one that says no. When an agent repairs a
bug, it must show that its new test fails on the code before the repair and
passes after it ("red first"). A test that passes on both proves nothing: it
may not detect the defect at all.

The runner checks this itself instead of trusting the agent's word. It runs the
named test against the code before the repair and accepts only a real
assertion failure; a crash, a skip or a setup error counts as "could not run",
not as red. In one night run a process slip had put a fix into that "before"
code, so the new tests passed there and the runner refused repairs that were in
fact correct. The refusal was right: it could not check the claim. A false
refusal costs a rerun; a false acceptance leaves a test that guards nothing.
How it works and where it is tested: [`docs/WORKFLOW.md`](docs/WORKFLOW.md) §4.

## Prompt advice and the mechanism behind it

The same good practice, as text in a prompt and as a mechanism here:

| Practice | As advice | As a mechanism in Monotrope | Where |
| --- | --- | --- | --- |
| Test first | "write a failing test first" | A repair counts only when the runner ran its named test on the code before the repair and saw it fail by an assertion | `scripts/stage2.py` |
| Ask before building | "interview the user" | Each change class owes a minimum of answered interview records, counted by a gate; every answer records who decided, when, and the question; a spec with an open `[DECISION]` fails its gate | `scripts/check_interview_minimums.py`, `plans/changes/<name>/decisions.md` |
| Make questions easy to answer | "give context" | Every question carries its topic, why now, today, and what changes in the repository and in the architecture; a gate checks that the context is there | `scripts/check_question_context.py`, [ADR 0018](docs/adr/0018-every-question-carries-its-context.md) |
| Review with fresh eyes | "ask a sub-agent to review" | Models from several vendors, each in a fresh session, round after round, cheapest first, until a round is clean; a cut diff never counts as clean; the reviewer never repairs | `scripts/stage2.py`, [ADR 0021](docs/adr/0021-review-swarms-until-clean.md) |
| Keep data safe | "be careful with secrets" | An endpoint allowlist by data class; the runner scans the configured inputs before dispatch and stops on a block, with no fallback; a paid model's terms reading expires, and after it the model gets no calls | `model-endpoints.yaml`, `scripts/leakcheck.py`, [ADR 0022](docs/adr/0022-paid-model-terms-expire.md) |
| Hand over | "summarise for the next session" | A dated handover file under a schema, delivered as a pull request | `scripts/handover_schema.py`, `docs/journal/handover/` |
| Keep `main` green | "run the tests" | One gate list drives the local run and CI; `main` takes a pull request only on a green `verify` of the merge candidate; one full check per machine at a time | `decisions/gates.yaml`, `scripts/verify_all.sh`, `scripts/verify_lock.py` |
| Decide, don't drift | "record decisions" | A decision takes effect when the maintainer merges its pull request; touching a file only a person may change makes a decision pull request | `provenance.yaml`, `docs/adr/` |
| Track the work | "make tickets" | A tracker in the repository's own git refs; one writer at a time, a claim for everyone else | `tools/bd`, `.beads/` |

What the leak check scans, and what it does not (the reflog, the stash, tags,
unreachable objects), is listed at the top of
[`scripts/leakcheck.py`](scripts/leakcheck.py). Paid reviewers get read-only
tools; that boundary is a prompt, not a sandbox.

## How a change runs

A change runs through seven phases; each leaves a file the next one reads.
Your moments are highlighted; agents do the rest, and machines check it.

<p align="center">
  <img src="docs/assets/readme-how-a-change-runs.png"
       alt="Three lanes — you, agents, machine checks — with the seven phases from explore to commit. Your four moments are state the goal, answer the interview questions, read the plan card, and merge. The review loop and the review send findings back to implement; a shield marks the leak check before every external model call."
       width="100%">
</p>

| # | Phase | Leaves | Answers |
| --- | --- | --- | --- |
| 1 | Explore | `research.md` | What is the situation? |
| 1a | Interview | `decisions.md` | What must a person decide? |
| 2 | Spec | `spec.md` | What exactly should change? |
| 2a | Spec review (optional) | rows in `findings.md` | Does the spec hold up? |
| 2b | Design (by class) | `design.md` | How is it built? |
| 3 | Plan | `plan.md` | In which steps, and when is it done? |
| 4 | Implement | code and tests | Does it work? |
| 4b | Review loop | a loop record; rows enter `findings.md` after phase 6 | Does it survive the swarms? |
| 5 | Verify | test output | Can we show it? |
| 6 | Review | `findings.md` | Does it match the spec? |
| 7 | Commit | a pull request | Does CI agree? |

What a change asks of you:

1. **State the goal** — what it is for, and what must not happen.
2. **Answer a few questions** — only the ones that are yours.
3. **Read the plan card** — what changes for you, when it is done, the time
   limit, what is left out. The work starts unless you say stop.
4. **Merge the pull request.**

Models are assigned per phase: one drafts, another reviews, a third
implements.

## The swarms

A **swarm** is several models reviewing the same change at once, each in a
fresh session: a reviewer cannot see its own blind spot, and models from one
vendor can share a failure mode.

**The review loop (phase 4b)** runs after implementation, one round per call,
until a round is clean or a named stop:

| Stage | Who reviews | What it sees |
| --- | --- | --- |
| 1 — free swarm | every reachable free model the `free_stage` rule selects from a live catalog | source and test hunks, no tools |
| 2 — Flash swarm | up to three of the cheapest reachable paid models whose terms allow the work, in parallel | the full diff, read-only tools |
| 3 and later — the ladder | one paid model per round, cheapest first | the full diff, read-only tools |

- A round is **clean** when every row is decided and none is accepted. Clean
  means no accepted findings remain in that round; it does not establish that
  the software is defect-free.
- The loop stops at a clean round, when the ladder is spent, or after two
  rounds that only found what earlier repairs introduced — then a person
  decides.
- A cut diff is recorded and cannot count as clean; `prepare-loop` probes
  every candidate before a fresh run and issues a short-lived receipt.
- All calls go through one operator, OpenCode Go: several vendors, one data
  recipient. A finding needs a test or the spec; reviewer and repairer are
  separate sessions.

**The research swarm (phase 1)** explores a `feature` or `architectural`
change ([ADR 0020](docs/adr/0020-phase-1-research-swarm.md)): three finder
seats map the sources, eleven topics are read by repository and online seats,
and a fresh Opus 5.5 context reconciles them into `research.md`. A gate then
holds the interview and the spec to what it found.

## Brakes that spare your attention

Agents scale with the budget; the person deciding does not. Monotrope treats
the stream of small judgements as a design problem:

| Brake | How | Level |
| --- | --- | --- |
| Constrain the agent before it writes | research, an interview with minimums by class, a spec with numbered criteria, a plan card you can veto, an appetite | interview minimums and validators enforced; veto and appetite written |
| Limit the mistakes it can make | other models only through one runner, behind an allowlist and a leak check; one worktree per change; one tracker writer | runner and leak check enforced; worktree and writer rules written |
| Check in layers | `make verify`, the review loop until clean, a separate final review, CI, a merge queue against the current `main` | enforced |
| Raise only what needs you | `[DECISION]` goes to you, `[GAP]` is explored, `[DETAIL]` is decided by the agent with its reason | an open `[DECISION]` fails the spec's gate; the rest written |
| Batch what does reach you | one decision block a day, one question at a time, each with its context | written ([ADR 0018](docs/adr/0018-every-question-carries-its-context.md)) |
| Let you step away | every step commits; a handover file per session; night runs from a written plan | handover schema enforced; night plan written |

## Working in parallel

Parallel work is expected; losing work silently is not.

1. **One change, one bead, one branch, one worktree, one session**, branched
   from a freshly fetched `origin/main` under `.claude/worktrees/<name>` and
   removed after the merge.
2. **One tracker writer.** The first-started writing session owns the tracker;
   every other session writes only its claim
   (`tools/bd update <id> --claim --actor <session>`) and its handover comment.
   At most two writing sessions by default.
3. **A clash warning** names any other session in the same checkout before
   the first edit — a warning, not a lock.
4. **The tracker travels in git.** A Dolt database under `.beads/`,
   transported via `refs/dolt/data`; concurrent claims have one winner
   (measured 2026-09-23 with bd 1.3.0). Tracker first, git second.
5. **Pull requests stay mergeable:** synced with `main` daily, asked about
   after five working days, sliced above about 800 changed lines, at most
   three open on one hot file, reviewed on a current base.

Not enforced: the one-writer rule until the write guard exists; worktrees
share git's refs, hooks and configuration, so isolation separates files, not
execution; lanes are run by one orchestrating session, by hand
([lanes](docs/orchestration.md)).

## Change classes

Not every change needs the same amount of process. A one-line fix should not
go through the same ceremony as a new subsystem, and a new subsystem should not
slip through as a quick fix. So every change states its class at the start, and
the class decides which steps it must go through.

<p align="center">
  <img src="docs/assets/readme-four-classes-of-change.png"
       alt="Four classes of change. spike: answers a question; explored by GLM 5.3 Flash; owes three interview topics or a reasoned skip; no design; no other-vendor review. bounded: changes an existing flow and decides nothing new; explored by GLM 5.3 Flash; owes one answer or a reasoned skip; no design; other-vendor review, spec review optional. feature: changes what the system must do; explored by the research swarm; owes three answers, five with an ADR; a design or a reason why not; other-vendor review. architectural: a new subsystem or a broken interface; explored by the research swarm; owes five answers with an ADR; always a design with an ADR draft; other-vendor review."
       width="100%">
</p>

The four classes, from lightest to heaviest:

- **`spike`** answers a question. Its result is a recommendation, not
  shipped behaviour.
- **`bounded`** changes a flow that already exists and decides nothing new.
- **`feature`** changes what the system must do, or how it is checked.
- **`architectural`** adds a new subsystem or breaks an existing interface.

How to read the rows:

- **Explore (1)** is who reads the code and history first. A light change is
  explored by one fast, cheap model (GLM 5.3 Flash). A heavier one goes to the
  *research swarm*: several models research eleven fixed topics in parallel,
  some in the repository and some in public sources, and one model reconciles
  their findings ([ADR 0020](docs/adr/0020-phase-1-research-swarm.md)).
- **Answers owed** is how many questions you, the person, must answer in the
  interview before the spec is written. A *reasoned skip* means the agent
  writes down why no question is needed. An *ADR* (architecture decision
  record, under `docs/adr/`) is a decision that outlives the change; a change
  that needs one owes five answers.
- **Design (2b)** is a separate design document before the plan. Light changes
  skip it; an architectural change always writes one, with a draft ADR.
- **Other-vendor review** means the change is read by models from other
  vendors than the one that wrote it: the review loop and the final review,
  plus a review of the spec where one is held. Each of those calls passes the
  leak check first (the shield). A spike skips them.

A gate counts the interview answers against the class, so a change cannot
skip its questions. Nothing yet checks that the class itself is right: a
feature declared as a spike would skip the other-vendor reviews, and only the
final review before the merge would catch it.

<details><summary>The same as a table</summary>

| | `spike` | `bounded` | `feature` | `architectural` |
| --- | --- | --- | --- | --- |
| What it is | answers a question | changes an existing flow, decides nothing new | changes what the system must do | a new subsystem or a broken interface |
| Explore (1) | GLM 5.3 Flash | GLM 5.3 Flash | research swarm | research swarm |
| Answers owed | three topics, or a reasoned skip | one, or a reasoned skip | three; five with an ADR | five with an ADR |
| Design (2b) | never | never | yes, or a reason why not | always, with an ADR draft |
| Other-vendor review | no | yes; spec review optional | yes | yes |

</details>

## Where decisions live

| Decision | Where |
| --- | --- |
| Your interview answers (`[DECISION]`) | `plans/changes/<name>/decisions.md` — your words, the date, the question |
| The agent's own choices (`[DETAIL]`) | marked lines with their reason in `spec.md`, `design.md` or `plan.md` |
| "Does this change need an ADR?" | `decisions/answers/<change>/adr.yaml` — answer, reason, who and when; a gate checks it |
| Architecture decisions | `docs/adr/`, in force from the merge |

`provenance.yaml` declares which files only a person may change. Handovers
summarise a session; they are not the record.

## Evaluation

**What is checked.** Every change runs the gate list locally and in CI. A
repair counts only when its test fails on the code before the repair, so the
test is shown to detect the defect it claims. Every gate has a mutation test —
a run that turns it red — or a stated reason in a list that may only shrink
([how the workflow tests](docs/testing.md)). Review rows need a test or the
spec as their basis.

**Against what.** A repair is compared with the code before it; a change with
its spec's numbered criteria; a review verdict with the commit it saw; a
foreign call with the endpoint policy and the leak check's denylist.

**What is not measured.**

- Whether Monotrope makes agents produce better software than a prompt-only
  workflow. There is no comparison run.
- Whether reviewers from a second vendor find more errors than one vendor.
  The loop's value is its structure — fresh sessions, several error profiles,
  evidence for every row — not a measured gain.
- How much of the maintainer's attention a change takes per day (bead
  coding-harness-n4bh).
- How good the tests are, as opposed to how many there are; mutation testing
  on one or two scripts is planned (bead coding-harness-bvy).

**In numbers.** These describe scope and activity, not quality. On `main` at
`c9692afd`, 2026-11-02:

- 23 gates in one list — 19 block, 3 report, 1 is advisory.
- 2,337 test functions in 65 test files.
- 23 architecture decision records.
- 300 merged pull requests and 2,737 commits since 2026-09-16.

## What works today

Checked on 2026-11-01 against `main` at `ac11da5d`. The commits up to
`c9692afd` (2026-11-02), the cut-off of the numbers above, change the
`verify` worker default and the kit probe; nothing in the lists below.

### Enforced by tooling

- `make verify` and CI run one gate list; every gate blocks, reports or is
  advisory.
- `scripts/stage2.py` checks the endpoint and runs the leak check before every
  call to another vendor; exploring, drafting, implementing, repairing and
  reviewing by other models all go through it.
- The review loop runs until a clean round or a named stop (ADR 0021), with
  the availability probe and its receipt before a fresh run.
- The research swarm explores `feature` and `architectural` changes
  (ADR 0020), and gates hold the interview and the spec to its findings.
- A paid model past its terms date gets no calls (ADR 0022).
- A repair counts only when its test fails on the code before the repair.
- A runner attempt fails fast: lint and its own tests run before the full
  `make verify`; a draft runs only its document gates.
- One admission per machine for `make verify` and runner checks, with a
  memory floor.
- `main` takes a pull request only on a green `verify` of the merge candidate
  (merge queue, rule RB-G7).

### Written rules, not enforced by a tool

- The three kinds of open points; the plan card as a contract; the wording of
  questions (a gate checks the context is there, not how it reads).
- One writer per tracker, until the write guard exists.
- Keeping pull requests mergeable, the daily decision block, the night-run
  rules; `python3 scripts/pr_sync.py sync` runs on request.
- The appetite: `make report CHANGE=<name>` shows the time used against it;
  nothing stops a run at the limit yet (bead coding-harness-uxa9).

### Not built yet

- A validator for the change files and a stop hook that blocks a session end
  on a red tree.
- A sandbox around paid reviewers; keeping the work of a failed model call
  (partly built).
- Lanes that run themselves: noticing an idle lane and starting its next bead
  is still done by hand (beads coding-harness-5q2p, coding-harness-4emv).

## Try it

Python 3.12+, Node 26 with npm, git and curl on macOS or Linux.

```bash
git clone https://github.com/bicycle-brakes/monotrope.git
cd monotrope
tools/beads/install.sh && tools/bd bootstrap --yes  # fresh clone: load the tracker
make venv                  # local .venv from the pinned lock (Python 3.12+)
bash tools/pi/install.sh   # pinned Pi; the real-Pi tests in make verify need it
make verify                # all gates
tools/bd ready             # open, unblocked work
```

To start a change: create its bead with the class in its description, then
`make change NAME=<name> BEAD=<id>` (in Claude Code:
`/workflow-start <name> --bead <id>`), and follow
[`docs/WORKFLOW.md`](docs/WORKFLOW.md) from phase 1. Another repository gets
the workflow as a kit; a step-by-step onboarding page is still being built.

## Go deeper

- [How it works](docs/how-it-works.md) — phases, model routing, change and
  data classes, [runner details](docs/how-it-works.md#runner-details),
  [design rules](docs/how-it-works.md#design-rules), and
  [one completed change, file by file](docs/how-it-works.md#follow-one-completed-change).
- [How the workflow tests](docs/testing.md) — the test strategy in six
  layers, and what it does not prove.
- [Lanes](docs/orchestration.md) — one session, several changes at once.
- [The doctrine](docs/WORKFLOW.md) — every rule, gate and route in full.
- [Architecture decisions](docs/adr/) and
  [session handovers](docs/journal/handover/).
- [`model-endpoints.yaml`](model-endpoints.yaml) — which model may see which
  data; [`AGENTS.md`](AGENTS.md) — the instruction file the agents read.

## Contributing

Work is tracked in Beads through `tools/bd`; a pull request names every bead
it opens, changes or closes. One change, one branch, one worktree, one
session. Per checkout run `make venv` and `bash tools/pi/install.sh` once,
then `make verify`; a text-only change is gated by CI. Decision pull requests
take effect when the maintainer merges them. Repository artefacts are in
English. By opening a pull request you agree that your contribution may be
distributed under the project's license and, if needed, under a commercial
license ([`COMMERCIAL.md`](COMMERCIAL.md)).

## License

Monotrope is **source-available** under the **PolyForm Noncommercial License
1.0.0**. Noncommercial use is free; commercial use needs a separate written
license. See [`LICENSE`](LICENSE) and [`COMMERCIAL.md`](COMMERCIAL.md).

Releases published before 2026-10-20 were under Apache 2.0. That grant remains
for those releases.
