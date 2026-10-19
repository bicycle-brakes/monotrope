# coding-harness

**Let AI agents do the work. Keep the decisions and the evidence.**

A file-based workflow for AI coding agents. Claude Code, Codex and Cline all
read the same instruction file, so a change survives the harness it was
started in and stays resumable, inspectable and handover-ready.

Agents research, plan, implement and review changes. You own the intent and
the consequential decisions. Versioned files keep the working context, the
reasons behind decisions, the review findings and the handover, so the next
session continues from a recorded state instead of a chat that is gone.

This repository holds the workflow rules, the phase prompts, the templates and
the supporting tools. It uses the workflow for its own development.

**Status:** actively bootstrapping. Some enforcement tooling is still being
migrated, and calls to models from other vendors cover this repository's own
framework content only. [What works today](#what-works-today-and-what-is-still-coming)
says exactly which parts are enforced.

## What you get

**Work survives the session.**
Research, decisions, spec, plan, findings and handover are files in the
repository. A new session, a colleague or another agent picks up a change
without reconstructing it from chats. You do not have to keep the state of the
project in your head.

**Agents act; you own the decisions that matter.**
Decisions come in three levels. You decide intent: what should happen, what
cannot be undone, what carries a risk. The model and the agent decide
mechanics and details, and write down why. So the agent keeps working without
asking you about every small thing, and you can see afterwards where it
decided and where it departed from the plan.

```mermaid
flowchart TD
    Q[Open point] --> K{What kind of point?}
    K -->|Intent: irreversible, risky, external| P[You decide]
    K -->|Mechanics: library, structure| M[Model decides, reason written down]
    K -->|Detail: names, order, format| A[Agent decides, reason written down]
    P --> F[Recorded in the change's files]
    M --> F
    A --> F
```

**Checks leave evidence.**
Tests and CI run during the work, not only at the end: a red *blocking* gate
stops it. The nightly drift job reports and does not block — the tracker and
the outside world move without a commit here, so a red night is a finding to
work, not a stop. Reviewers write their findings into a table, a finding is
acted on only when a test or the spec backs it, and when two reviewers
disagree, both views stay. At the merge you judge a change by its evidence,
not by a summary.

**Model access has explicit boundaries.**
Calls to models from other vendors go through one runner. It checks that the
endpoint is allowed for the data, and it runs a leak check before every call.
A leak stops the call; there is no silent fallback to another model. Whether a
second vendor finds more errors is being measured, not assumed.

### Built for focus

Every question to you comes with its context: the topic, why it comes up now,
how things stand, and what would change. Every session opens with where we
stand, the next step, and what is needed from you. Messages lead with the
result and ask one question at a time. This form is written for readers with
ADHD, and it holds for every reader: nobody should get lost in the work.

## Follow one completed change

The change "frontmatter-current" (bead coding-harness-qd7, archived
2026-09-29) shows each step with real files:

| Question | Where to see it |
|---|---|
| What was the task? | A document's header said when it was last *reviewed*, not when its content last changed — and nothing failed on a stale one. [`research.md`](plans/changes/archive/2026-09-29-frontmatter-current/research.md) |
| What did a person decide? | In the maintainer's words: "The frontmatter headers in the files must always be maintained and current. This must be a basic mechanism." [`decisions.md`](plans/changes/archive/2026-09-29-frontmatter-current/decisions.md) |
| What did the agent decide itself? | Mechanics, each marked `[DETAIL]` with its reason — for example which of the two key lists owns the held prefixes. [`spec.md`](plans/changes/archive/2026-09-29-frontmatter-current/spec.md) |
| What was the contract? | The plan card: written for one option of a `[DECISION]`, with the one step the other option would change. [`plan.md`](plans/changes/archive/2026-09-29-frontmatter-current/plan.md) |
| Which check found a defect? | Review finding F-1 (MAJOR): the ADR headers said `status: accepted` where the body recorded the ADR as superseded — a reader of the header alone would believe ADR 0001 is in force. The row reads `fixed in 0f4101f`. [`findings.md`](plans/changes/archive/2026-09-29-frontmatter-current/findings.md) |
| What evidence stood at the merge? | The findings table with every row decided, and green CI — and the gate that came out of it, `frontmatter-current`, still runs on every pull request. |

## What a change asks of you

1. **Answer the questions.** A few, each with its context, only where the
   answer is yours to give.
2. **Read the plan card.** It says what changes for you, when it is done, the
   time limit and what is left out. The work starts unless you say stop.
3. **Merge the pull request.** A person merges, or explicitly asks an agent to.

```mermaid
flowchart LR
    E[Explore] --> I[Interview]
    I -->|you answer| S[Spec]
    S --> PL[Plan]
    PL -->|you read the card| IM[Implement]
    IM --> V[Verify]
    V -->|red: back to implementing| IM
    V -->|green| R[Review]
    R --> C[Commit]
    C -->|you merge| D[Merged]
```

## What works today and what is still coming

Checked on 2026-10-19 against `origin/main` at `59630b7`.

**Enforced by tooling**

- `make verify` and CI run the gate list in `decisions/gates.yaml`: tests,
  lint, and process checks such as the interview minimums, the context on
  every recorded answer and a named proof for every acceptance criterion.
  Every gate declares whether it blocks or only reports; the document-link
  check still reports (35 known corpus findings), the others block.
- The stage-2 runner (`scripts/stage2.py`) checks the endpoint and runs the
  leak check before every call to another vendor.

**Written rules that agents follow, not enforced by a tool**

- The three decision levels, the plan as a contract, the communication form
  (the gate checks only that the context is there, not its wording), and one
  writer per tracker.

**Not built yet**

- The artefact validator, the stop hook that blocks on a red tree, the slash
  commands, the `make change` target (the script `scripts/new_change.py`
  exists; the target does not) and the gate catalogue that the doctrine
  names. Where the doctrine describes them, it describes the target.
- The research swarm: an open decision pull request (ADR 0020). The review
  swarm is merged (ADR 0021) and its loop runs until a round is clean.
- Keeping the work of a failed model call instead of deleting it: in
  progress.
- Stage 3, orchestration of parallel agents: evaluative only.

## Try it

```bash
git clone https://github.com/MPAdesso/coding-harness.git
cd coding-harness
tools/beads/install.sh && tools/bd bootstrap --yes  # fresh clone only: load the tracker
make venv                  # local .venv, built from the pinned lock
bash tools/pi/install.sh   # pinned Pi; the real-Pi tests in make verify need it
make verify                # all gates
tools/bd ready             # open, unblocked work
```

To start a change, the bead must already exist:
`python3 scripts/new_change.py <name> --bead <id>`. Then read
`docs/WORKFLOW.md` and work at phase 1.

## Go deeper

- [How the workflow works](docs/how-it-works.md): the phases, who does which
  job (Claude as orchestrator; Codex, Pi with OpenCode Go, GLM), the change and
  data classes, the swarms and the three stages.
- [The doctrine](docs/WORKFLOW.md): every rule, gate and route in full.
- [Architecture decisions](docs/adr/): why it is built this way.
- [The session handovers](docs/journal/handover/): the file a session leaves
  for the next one — objective, evidence, what is open, and where to resume.
- [`model-endpoints.yaml`](model-endpoints.yaml): which model may see which data.
- [`AGENTS.md`](AGENTS.md): the instructions every agent harness reads.

## Contributing

- **Tracker.** Beads with the `coding-harness-` prefix, read and written only
  through `tools/bd`. Pull requests name every bead they open, change or close.
- **Decisions** take effect when the maintainer merges their pull request.
- **One change, one worktree,** under `.claude/worktrees/`.
- **Language.** Repository artefacts are in English.

| Related repository | Role |
|---|---|
| `portfolio-agentic-engineering` | framework governance; the origin this repository migrates from |
| `lakeswitch-ai` | a product repository that runs a clean-room instance of the workflow |
