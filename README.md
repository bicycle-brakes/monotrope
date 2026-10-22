<p align="center">
  <img src="docs/assets/monotrope-banner.png"
       alt="monotrope: an infinity ribbon, a winding path, a bicycle disc brake"
       width="100%">
</p>

# Monotrope

**Let AI agents do the work. Keep the decisions and the evidence.**

Monotrope is a file-based workflow for AI coding agents. Agents research,
specify, plan, implement and review a change; you decide what the change is
for and what must not happen. Everything in between — the research, your
answers, the agent's own choices, the contract, the review findings and where
the next session resumes — is written to versioned files in the repository.

Most agent workflows keep that state in the conversation. Monotrope keeps it
in the repository, so the next session, model or person can pick it up.

No server of its own: Markdown and YAML in git, a small Python toolchain, and
a tracker that travels in the repository's git refs. One instruction file
(`AGENTS.md`) is the only instruction entry; Claude Code and Codex read it
today. The files are designed to outlive the harness (the agent program), so
a change can be finished in another session by a different model; the full
orchestration path is Claude Code for now.

This repository holds the workflow rules, the phase prompts, the templates and
the tools, and it develops itself with the same workflow.

> **Status:** early and moving fast. [What works today](#what-works-today)
> separates what a tool enforces from what is a written rule and from what is
> not built yet. The repository and its tracker still carry the working name
> `coding-harness` in places.

> **License:** source-available under the PolyForm Noncommercial License 1.0.0.
> Noncommercial use is free; commercial use needs a separate written license.
> See [License](#license).

## The problem it answers

What goes wrong when agents do the work and nothing records it:

- **The chat is the state.** A session ends and the context goes with it. The
  next session starts from scratch, or from a summary nobody can check — and
  the work dies with the harness that ran it.
- **The decisions are invisible.** The agent chose a format, a name, an
  order — and nobody wrote down why, so nobody can review it afterwards.
- **Nothing stops a red tree.** Tests run at the end, if at all, and a defect
  ships behind a green summary.
- **One reviewer has one blind spot.** A model reviewing its own work, or the
  only model in the loop, cannot see what it is systematically missing. Models
  from one vendor share a way of being wrong.
- **Parallel work overwrites itself.** Two sessions in one checkout, or two
  writers in one tracker, can lose each other's work without either noticing.
- **A foreign model can see too much.** Sending work to another vendor risks
  exposing data that vendor may not see.

Monotrope turns each of them into files, roles and checks.

## What Monotrope does about it

| Failure | The mechanism | Where to see it |
| --- | --- | --- |
| The chat is the state | Every phase leaves its result as a file; a session ends with a dated handover, and the next session reads the files instead of a summary | `plans/changes/<name>/`, `docs/journal/handover/` |
| Decisions are invisible | Open points are classified; every answer records who decided and when; a decision takes effect when its pull request is merged | `decisions.md`, `spec.md`, `provenance.yaml`, `docs/adr/` |
| A red tree ships | One gate list drives the local run and CI; every gate is block, report or advisory; a repair's test must fail before the repair | `decisions/gates.yaml`, `scripts/verify_all.sh` |
| One reviewer has one blind spot | A review loop of swarms from several vendors, cheapest first; a finding needs a test or the spec; the reviewer never repairs | `findings.md`, `scripts/stage2.py`, [ADR 0021](docs/adr/0021-review-swarms-until-clean.md) |
| Parallel sessions overwrite each other | One worktree per change, one tracker writer, a claim for every other session, a warning when sessions share a checkout | `AGENTS.md`, `tools/bd`, `tools/claude-code/` |
| Context dies with the harness | Files outlive the tool; one instruction entry; models are assigned per phase and per job | `AGENTS.md`, `plans/`, `docs/adr/` |
| A foreign model can see too much | An endpoint allowlist by data class and a leak check before every call; a leak stops without a fallback | `model-endpoints.yaml`, `scripts/stage2.py` |

Not all of it is enforced by a tool. [What works today](#what-works-today)
separates the three levels: enforced, written rule, not built.

Two mechanisms need more room than a table cell — the review swarms and work
in parallel. Both follow the process overview below.

## How a change runs

A change runs through seven phases. Each phase leaves its result in the
repository, and the next phase reads that instead of a chat.

The highlighted moments are yours; everything else is done by agents and
checked by machines.

<p align="center">
  <img src="docs/assets/readme-how-a-change-runs.png"
       alt="Three lanes — you, agents, machine checks — with the seven phases from explore to commit. Your four moments are state the goal, answer the interview questions, read the plan card, and merge. The review loop and the review send findings back to implement; a shield marks the leak check before every external model call."
       width="100%">
</p>

The diagram shows who acts in each lane; the table below lists every phase
and what it leaves behind.

| # | Phase | What it leaves | The question it answers |
| --- | --- | --- | --- |
| 1 | Explore | `research.md` | What is the situation? |
| 1a | Interview | `decisions.md` | What must a person decide? |
| 2 | Spec | `spec.md` | What exactly should change? |
| 3 | Plan | `plan.md` | In which steps, and when is it done? |
| 4 | Implement | code and tests | Does it work? |
| 5 | Verify | test output | Can we show it? |
| 6 | Review | `findings.md` | Does it match the spec? |
| 7 | Commit | a pull request | Does CI agree? |

A spec review (2a), a design (2b) and the review loop between implementing and
verifying (4b) join when a change needs them. The review loop is the subject
of [the next section](#the-swarms). A session that ends leaves a dated
handover file: the objective, the evidence, what is open, and the one action
to resume with.

What a change asks of you is short:

1. **State the goal** — what the change is for, and what must not happen.
2. **Answer a few questions** — only the ones that are yours to answer.
3. **Read the plan card** — what changes for you, when it is done, the time
   limit, what is left out. The work starts unless you say stop.
4. **Merge the pull request.**

Models are assigned per phase and per job: one drafts, another reviews, a
third implements. The model that fixes a finding is never the one that judges
the fix.

## The swarms

A **swarm** is several models reviewing the same change at the same time, each
in a fresh session of its own. It exists because a reviewer's blind spot is
invisible to that reviewer, and because models from one vendor share a way of
being wrong. The review loop adds vendors and strength only while findings
remain: cheap rounds run first, expensive ones only when needed.

### The review loop (phase 4b)

The loop runs after implementation and before the final review. One call runs
one round; the orchestrator calls it again until a round is clean or a stop is
reached.

| Round | Who reviews | How | What it sees |
| --- | --- | --- | --- |
| 1 — free swarm | every model the `free_stage` rule selects from a forced live refresh of the OpenCode Go catalog | in parallel | the implementation diff only, no tools |
| 2 — Flash swarm | up to three of the cheapest reachable paid models whose terms admit the work | in parallel | the same diff, read-only tools |
| 3 and later — the ladder | one eligible paid model per round, cheapest first by its declared request allowance (more requests per five hours means cheaper) | one at a time | the same diff, read-only tools |

Pi, the pinned agent program, carries the calls. The ladder is read from the
`modelle` set of the `opencode-go` entry in `model-endpoints.yaml`; a failed
Flash member is replaced by the cheapest unused one. A round is **clean** when
every row is decided and none is accepted.

The loop stops at a clean round, when the paid ladder is exhausted, or after
two consecutive rounds accepted only findings that earlier repairs introduced.
The last case is a brake: a person decides how to go on. A run that has
consumed every stage without a clean round stops and reports; no model is
substituted silently.

**What a round sees.** The bounded hunks of source and test code against the
merge base with `origin/main`, uncommitted and untracked code included. The
prompt carries at most 2,000 diff lines; a cut diff is recorded, and a round
over a cut diff can never count as clean. A change without source hunks skips
the free stage.

**Before a fresh availability-enabled run**, `prepare-loop` probes the admitted
candidates with static input and no tools and reports which are reachable,
failed or skipped. Its receipt is bound to the worktree, the configuration and
the diff and expires after 900 seconds.

**The guardrails.**

- All calls to another vendor go through one runner. It checks the endpoint
  against `model-endpoints.yaml` and runs a leak check before every call; a
  leak stops the call, with no silent fallback to another model.
- A finding is acted on only when a test demonstrates it or the spec supports
  it. When two reviewers disagree, both views stay in the table, and the
  disagreement blocks like a defect.
- Each round is a fresh, read-only session. The model that repairs a finding
  never reviews the repair. The final review is a fresh read-only Codex
  session, and it writes its verdict before it reads any loop row.
- The paid rounds get read-only tools. That read boundary is a prompt today,
  not a sandbox — an accepted limit, not a guarantee.

### The research swarm

Phase 1 would run three independent researchers — one on the existing system,
one on outside practice, one on how the change fits the rest — then one round
of critique and a fresh judge. The result becomes `research.md`. The proposal
is a draft in
[`docs/research/2026-10-08-explore-swarm-proposal.md`](docs/research/2026-10-08-explore-swarm-proposal.md),
not built.

### What the swarms have found

On 2026-10-20 at `5c7db34`, reviewers in the loop kept finding new defects
round after round in a change whose suite was green. That is evidence that
the loop sees something a green suite does not; it is not a measurement of how
many faults the tests catch. Whether a second vendor finds more errors is
being measured, not assumed.

## Working in parallel

Parallel work is allowed and expected; what it must not do is lose work
silently. The workflow makes the boundaries explicit:

1. **One change, one worktree.** One change, one bead (the tracker item), one
   branch, one worktree, one session. The worktree is branched from a freshly
   fetched `origin/main`, lives under `.claude/worktrees/<name>`, and is
   removed after the merge. Nobody switches the branch of the main checkout
   while another session is running.
2. **One tracker writer.** While more than one session writes in a repository,
   the first-started writing session owns the tracker: it hands out beads,
   reprioritises, links and closes. Every other writing session writes exactly
   two things — the claim of the one bead it works on
   (`tools/bd update <id> --claim --actor <session>`) and its handover comment
   on that bead. The default limit is two writing sessions per repository.
3. **A clash warning before the first edit.** In this repository's Claude Code
   setup, a hook scans the live sessions at start and on each prompt and names
   any that share the checkout. The person then decides whether to continue
   or open a worktree. It is a warning, not a lock.
4. **A handover, not a shared chat.** A session that ends leaves a dated
   handover file; the next session starts from it. Sessions working in
   parallel read each other's committed state, not a live conversation.
5. **The tracker travels safely.** The tracker is a Dolt database under
   `.beads/`, transported via `refs/dolt/data`. `tools/bd` finds the main
   checkout's tracker from any worktree, and concurrent claims have exactly
   one winner (measured 2026-09-23 with bd 1.3.0). The push order is tracker
   first, git second: CI renders the gate from the tracker, so a git push that
   outruns it goes red on exactly that gap.

What is not enforced: the one-writer rule is a working agreement until the
write guard exists; worktrees share git's refs, hooks and configuration, so
isolation separates files, not execution; and orchestrating many agents in
parallel is evaluated, not built (stage 3).

## Not every change is the same size

Every change names its class in the head of its spec. The class sets how much
process the change gets; the kind of an open point (below) sets who decides
it.

| | `spike` | `bounded` | `feature` | `architectural` |
| --- | --- | --- | --- | --- |
| What it is | answers a question; the output is a recommendation | changes an existing, readable flow without deciding anything new | a self-contained deliverable that changes what the system must do or how it is checked | a new subsystem or a broken interface |
| Questions you must answer | three topics, or a reasoned skip | one, or a reasoned skip | at least three; five when it changes an ADR | five when it creates or changes an ADR |
| Design phase (2b) | never | never | yes, or one sentence why not | always, with an ADR draft |
| Review by another vendor | no | yes | yes | yes |

A gate counts the answered questions against the class's minimum. Nothing yet
checks that the class itself is right: a `feature` declared as a `spike` would
skip the other-vendor reviews, and only the review before the merge catches
it.

## Where decisions live

Every decision is a file, and each kind has one place:

| Decision | Where it is recorded |
| --- | --- |
| Your answers in a change's interview — the `[DECISION]` points | `plans/changes/<name>/decisions.md`, in your words where you gave them, with the date and the question asked |
| The agent's own choices — the `[DETAIL]` points — and departures from the plan | marked lines with their reason in the same change's `spec.md`, `design.md` or `plan.md` |
| Your answer to "does this change need an architecture decision record?" | `decisions/answers/<change>/adr.yaml`: the answer, the reason, the proposal you were shown, who answered and when; a gate checks it |
| Architecture decisions | `docs/adr/`; a record takes effect when its pull request is merged |

Open points come in three kinds:

| Kind | Who decides | What happens |
| --- | --- | --- |
| `[DECISION]` | you | intent, anything irreversible or risky; your answer goes into `decisions.md` |
| `[GAP]` | the agent | a missing fact; the agent looks it up and does not ask |
| `[DETAIL]` | the agent | a name, an order, a format; the agent decides and writes down why |

Which files only a person may change is declared in `provenance.yaml`; a pull
request that touches one is a decision pull request. A finished change leaves
its lasting parts in `plans/specs/` or `docs/adr/`; the rest is archived under
`plans/changes/archive/` with its decisions. Session handovers repeat the
decisions of a session, but they are a summary, not the record.

## Design rules

- **Files, because a change must outlive the session, the machine and the
  harness.** A state kept inside a tool dies with the tool.
- **It travels.** The mechanism moves to another repository as a kit; a probe
  copies it into a throwaway tree and runs its tests there, so the workflow is
  proven outside its home.
- **One list, because two lists drift.** 22 gates live in one file
  (`decisions/gates.yaml`); 18 block, 3 report, 1 advises (as of 2026-10-22).
  The gate file drives the local runner and the CI generator, and a gate holds
  the generated workflow to it byte for byte. One instruction file
  (`AGENTS.md`) plays the same role for the agents; a test fails if a
  harness-specific file would silently replace it.
- **A merge, because a decision that lives in a chat is not a decision.** A
  rule or a person-reserved file changes when its pull request is merged, not
  when someone typed "yes".
- **Evidence over summaries.** You judge a change by its tests, its findings
  table and green checks, not by an agent's account of itself. A repair counts
  only when its test fails on the code before the repair, and the runner
  checks that itself.
- **Numbers carry their cut-off.** Every count names its commit or date, and
  what could not be read is written as "not read", never as "none".
- **Block, report or advisory, because a gate whose red means nothing is
  noise.** Every gate says which of the three it is, so a red run always means
  something specific.
- **Built for focus.** Every question comes with its context: the topic, why it
  comes up now, how things stand today, and what would change. Every session
  opens with where things stand, the next step and what is needed from you.
  Messages lead with the result and ask one question at a time.

## How testing works, and what it does not prove

**One command, the same checks as CI.** `make verify` runs
`scripts/verify_all.sh`, which holds no commands of its own: it reads the gate
list in `decisions/gates.yaml`, the same list the CI workflow is generated
from. The pytest suite is one of those gates and runs in parallel
(`pytest -n auto`). The others check documents and process rules, not code.

**A locked environment.** Each checkout builds its own `.venv` with
`make venv` from `requirements-ci.txt`, where every package is pinned with its
hash. Results then depend on the lock, not on what happens to be installed on
a machine, and a local green means what a CI green means.

**Red first.** A repair counts only when its test fails on the code before the
repair; the runner checks this itself. A test that would have passed anyway
proves nothing, and models readily write such tests.

**What the numbers say, and what they do not.** On 2026-10-20 at `5c7db34`,
`tests/` held 2306 tests in 40 files: about 29,800 lines of test code against
about 13,900 lines in `scripts/`. That count measures how much is checked, not
how well. On the same day, reviewers in the review loop kept finding new
defects round after round in a change whose suite was green. How many injected
faults the tests catch has not been measured yet; a mutation-testing run on one
or two scripts is planned (bead coding-harness-bvy).

## What works today

Checked on 2026-10-22 against `main` at `1d9674b`.

### Enforced by tooling

- `make verify` and CI run the gate list: tests, lint and the process checks
  above. Every gate declares whether it blocks, reports or advises.
- The stage-2 runner (`scripts/stage2.py`) checks the endpoint and runs the
  leak check before every call to another vendor. Exploring, drafting,
  implementing, repairing and reviewing by other models all go through it.
- The review loop runs until a round is clean or a named stop (ADR 0021), with
  the availability probe and its receipt before a fresh run.

### Written rules agents follow, not enforced by a tool

- The three kinds of open points, the plan card as a contract, the
  communication form (a gate checks that the context is there, not its
  wording), and one writer per tracker until the write guard exists.

### Not built yet

- The artefact validator, the stop hook that blocks a session end on a red
  tree, the slash commands, the `make change` target (the script
  `scripts/new_change.py` exists; the target does not) and the gate catalogue
  that the doctrine names. Where the doctrine describes them, it describes
  the target.
- The research swarm for larger changes: a draft proposal in
  [`docs/research/2026-10-08-explore-swarm-proposal.md`](docs/research/2026-10-08-explore-swarm-proposal.md),
  not built.
- Keeping the work of a failed model call: partly built. `scripts/stage2.py`
  saves failed implement and draft attempts; the rest is in progress.
- A sandbox around paid reviewers: the read boundary is a prompt today, not a
  mechanism (bead coding-harness-8df).
- Orchestration of many agents in parallel: evaluated, not built.

## Follow one completed change

The change "frontmatter-current" (archived 2026-09-29) shows each step with
real files:

| Question | Where to see it |
| --- | --- |
| What was the task? | A document's header said when it was last *reviewed*, not when its content last changed — and nothing failed on a stale one. [`research.md`](plans/changes/archive/2026-09-29-frontmatter-current/research.md) |
| What did a person decide? | In the maintainer's words: "The frontmatter headers in the files must always be maintained and current. This must be a basic mechanism." [`decisions.md`](plans/changes/archive/2026-09-29-frontmatter-current/decisions.md) |
| What did the agent decide itself? | Mechanics, each marked `[DETAIL]` with its reason — for example which of the two key lists owns the held prefixes. [`spec.md`](plans/changes/archive/2026-09-29-frontmatter-current/spec.md) |
| What was the contract? | The plan card: written for one option of a `[DECISION]`, with the one step the other option would change. [`plan.md`](plans/changes/archive/2026-09-29-frontmatter-current/plan.md) |
| Which check found a defect? | Review finding F-1 (MAJOR): the ADR headers said `status: accepted` where the body recorded the ADR as superseded — a reader of the header alone would believe ADR 0001 is in force. The row reads `fixed in 0f4101f`. [`findings.md`](plans/changes/archive/2026-09-29-frontmatter-current/findings.md) |
| What evidence stood at the merge? | The findings table with every row decided, and green CI — and the gate that came out of it, `frontmatter-current`, still runs on every pull request. |

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

These commands run this repository itself. A step-by-step onboarding page for
other repositories is still being built; until then,
[`docs/WORKFLOW.md`](docs/WORKFLOW.md) is the reference.

To start a change, create its bead (the tracker item) first, then
`python3 scripts/new_change.py <name> --bead <id>`, and read
[`docs/WORKFLOW.md`](docs/WORKFLOW.md) from phase 1.

## Go deeper

- [How the workflow works](docs/how-it-works.md): the phases, which model does
  which job, the change and data classes, and the swarms.
- [The doctrine](docs/WORKFLOW.md): every rule, gate and route in full.
- [Architecture decisions](docs/adr/): why it is built this way.
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
- **Before a pull request.** `make venv` once, then `make verify`; a text-only
  change is gated by CI.
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
