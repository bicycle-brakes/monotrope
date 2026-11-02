<p align="center">
  <img src="docs/assets/monotrope-banner.png"
       alt="monotrope: an infinity ribbon, a winding path, a bicycle disc brake"
       width="100%">
</p>

# Monotrope

**Let AI agents do the work. Keep the decisions and the evidence.**

Most agent workflows are advice. A prompt asks the model to write the failing
test first, to ask before it builds, to review with fresh eyes, to keep
secrets out of the call — and the run is only as good as the model's
obedience. Monotrope turns that advice into checks a tool performs. A repair
counts only when the runner has watched its test fail on the code before the
repair. A foreign model sees nothing a leak check has not passed, and a model
whose data terms have expired gets no call at all. Reviewers from several
vendors go round after round until one round is clean, and none of them ever
repairs its own finding. A decision takes effect when a person merges it, not
when a chat says so.

Everything a change produces — research, answers, contract, findings, the next
session's starting point — is a versioned file. Any session, harness or model
can pick up where another stopped.

**What it is.** A file-based workflow for AI coding agents, and its home: the
rules, phase prompts, templates, gates, the foreign-model runner
(`scripts/stage2.py`) and a kit that carries the workflow into other
repositories. Claude Code and Codex do the work; you decide what it is for and
what must not happen. The workflow develops itself under its own rules.

**What it is not.** Not an agent program, a server, a model gateway or a
one-line install for any repository.

> **Status:** young and moving fast — 300 pull requests merged since the first
> commit on 2026-09-16 (counted 2026-11-02). [What works today](#what-works-today)
> separates what a tool enforces from what is a written rule and from what is
> not built yet. The repository and its tracker still carry the working name
> `coding-harness` in places.
>
> **License:** source-available under the PolyForm Noncommercial License 1.0.0;
> commercial use needs a separate written license ([License](#license)).

## Advice a model can ignore, checks it cannot

The same good practice, as text in a prompt and as a mechanism here:

| Practice | As advice | As a mechanism in Monotrope | Where |
| --- | --- | --- | --- |
| Test first | "write a failing test first" | A repair counts only when the runner ran its named test on the code before the repair and saw it fail — by an assertion or pytest's own failed outcome, never by a crash | `scripts/stage2.py` |
| Ask before building | "interview the user" | Each change class owes a minimum of answered interview records, counted by a gate; every answer records who decided, when, and the question it settled; a spec with an open `[DECISION]` fails its gate | `scripts/check_interview_minimums.py`, `plans/changes/<name>/decisions.md` |
| Make questions easy to answer | "give context" | Every question carries its topic, why now, today, what changes in the repository and in the architecture; a gate checks that the context is there | `scripts/check_question_context.py`, [ADR 0018](docs/adr/0018-every-question-carries-its-context.md) |
| Review with fresh eyes | "ask a sub-agent to review" | Models from several vendors, each in a fresh session, round after round, cheapest first, until a round is clean; a cut diff never counts as clean; the reviewer never repairs; a final review in another fresh session | `scripts/stage2.py`, [ADR 0021](docs/adr/0021-review-swarms-until-clean.md) |
| Keep data safe | "be careful with secrets" | An endpoint allowlist by data class and a leak check before every foreign-model call, with no fallback on a block; a paid model's terms reading carries an expiry date, and after it the model gets no calls | `model-endpoints.yaml`, `scripts/leakcheck.py`, [ADR 0022](docs/adr/0022-paid-model-terms-expire.md) |
| Hand over | "summarise for the next session" | A dated handover file under a schema, delivered as a pull request; the next session starts from it | `scripts/handover_schema.py`, `docs/journal/handover/` |
| Keep `main` green | "run the tests" | One gate list drives the local run and CI, each gate declared block, report or advisory; `main` takes a pull request only on a green `verify` of the merge candidate; one full check per machine at a time, waiting while memory is low | `decisions/gates.yaml`, `scripts/verify_all.sh`, `scripts/verify_lock.py` |
| Decide, don't drift | "record decisions" | A decision takes effect when the maintainer merges its pull request; files only a person may change are declared, and touching one makes a decision pull request | `provenance.yaml`, `docs/adr/` |
| Track the work | "make tickets" | A tracker in the repository's own git refs; one writer at a time, a claim for everyone else; CI renders its gate from the tracker, so a push that outruns it goes red | `tools/bd`, `.beads/` |

**Why red first.** A test that passes after a fix proves nothing unless it
failed before it — like a smoke detector you have never heard beep. So the
runner runs the new test twice: on the code from before the repair, where it
must fail by an assertion (a crash only shows that the test could not run),
and on the repaired code, where it must pass. When a session once saved a
stopped attempt as a commit, the fix slipped into the "before" code, the test
passed there, and the runner refused the repair — rightly.

Where a rule is still text rather than a tool, [What works today](#what-works-today)
says so.

## What sets it apart

- **Resumable by anyone.** State lives in files, not in a conversation, so
  another session, harness or model finishes the change.
- **Proof that cannot quietly vanish.** Every criterion names its test, a
  gate holds that test, a repair counts only when its test failed first, and
  every gate has a run that turns it red.
- **Several vendors review, none repairs its own finding.** A free swarm, a
  cheap swarm, then a ladder of paid models, each round in fresh sessions, all
  behind one leak-checked runner.
- **The human keeps the decisions — and the attention.** Open points are
  sorted so only real decisions reach you, one at a time, each with its
  context, in one daily block.
- **Parallel without losing work.** One change, one worktree, one branch; one
  session writes the tracker and keeps several lanes moving
  ([lanes](docs/orchestration.md)).
- **It corrects its own process.** The second finding of one mechanism ends
  case-by-case repair: the fix becomes structural. Each session leaves a dated
  handover, and outside tools and practices are evaluated in research
  notes before anything is adopted.

## In numbers

On `main` at `c9692afd`, 2026-11-02:

- 23 gates in one list for the local run and CI — 19 block, 3 report, 1 is
  advisory.
- 2,337 test functions in 65 test files.
- 23 architecture decision records, each in force from the merge of its pull
  request.
- 12 phase prompts, 54 research notes, 59 session handovers, 21 archived
  changes.
- 300 merged pull requests and 2,737 commits since 2026-09-16.

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

- A round is **clean** when every row is decided and none is accepted. The
  loop stops there, when the ladder is spent, or after two rounds that only
  found what earlier repairs introduced — then a person decides.
- A cut diff is recorded and cannot count as clean; an unreadable answer is
  asked once more with a format reminder; `prepare-loop` probes every
  candidate before a fresh run and issues a short-lived receipt.
- All calls go through one operator, OpenCode Go: several vendors, one data
  recipient. A finding needs a test or the spec; reviewer and repairer are
  separate sessions. Paid rounds' read-only boundary is a prompt, not a
  sandbox.

**The research swarm (phase 1)** explores a `feature` or `architectural`
change ([ADR 0020](docs/adr/0020-phase-1-research-swarm.md)): three finder
seats map the sources, eleven topics are read by repository and online seats,
and a fresh Opus 5.5 context reconciles them into `research.md`. A gate then
holds the interview and the spec to what it found.

The loop is a mechanism, not a measured claim: whether a second vendor finds
more errors than one has not been measured.

## Brakes that spare your attention

Agents scale with the budget; the person deciding does not. Monotrope treats
the stream of small judgements as a design problem:

| Brake | How | Level |
| --- | --- | --- |
| Constrain the agent before it writes | research, an interview with minimums by class, a spec with numbered criteria, a plan card you can veto, an appetite | interview minimums and validators enforced; veto and appetite written |
| Limit the mistakes it can make | foreign models only through one runner, behind an allowlist and a leak check; one worktree per change; one tracker writer | runner and leak check enforced; worktree and writer rules written |
| Check in layers | `make verify`, the review loop until clean, a separate final review, CI, a merge queue against the current `main` | enforced |
| Raise only what needs you | `[DECISION]` goes to you, `[GAP]` is explored, `[DETAIL]` is decided by the agent with its reason; only decision pull requests wait for your merge | an open `[DECISION]` fails the spec's gate; the rest written |
| Batch what does reach you | one decision block a day, one question at a time, each with its context | written ([ADR 0018](docs/adr/0018-every-question-carries-its-context.md)) |
| Let you step away | every step commits; a handover file per session; night runs from a written plan | handover schema enforced; night plan written |

Not built yet: a measurement of what reaches you per day, and routing your
attention by a change's risk (bead coding-harness-n4bh).

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
execution; lanes are run by one orchestrating session, by hand.

## Change classes

Every change names its class; the class sets how much process it gets.

| | `spike` | `bounded` | `feature` | `architectural` |
| --- | --- | --- | --- | --- |
| What it is | answers a question | changes an existing flow, decides nothing new | changes what the system must do | a new subsystem or a broken interface |
| Answers owed | three topics, or a reasoned skip | one, or a reasoned skip | three; five with an ADR | five with an ADR |
| Design (2b) | never | never | yes, or a reason why not | always, with an ADR draft |
| Other-vendor review | no | yes | yes | yes |

A gate counts the answers against the class. Nothing yet checks that the
class itself is right.

## Where decisions live

| Decision | Where |
| --- | --- |
| Your interview answers (`[DECISION]`) | `plans/changes/<name>/decisions.md` — your words, the date, the question |
| The agent's own choices (`[DETAIL]`) | marked lines with their reason in `spec.md`, `design.md` or `plan.md` |
| "Does this change need an ADR?" | `decisions/answers/<change>/adr.yaml` — answer, reason, who and when; a gate checks it |
| Architecture decisions | `docs/adr/`, in force from the merge |

`provenance.yaml` declares which files only a person may change. Handovers
summarise a session; they are not the record.

## What works today

Checked on 2026-11-01 against `main` at `ac11da5d`.

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
