# coding-harness

A workflow for building software with AI agents: **seven phases, three
stages**. Every phase leaves an artefact in the repository. Gates decide
whether a phase passes, and a person decides what cannot be undone.

This repository is the source of truth for that process: the doctrine, the
phase prompts, the templates, the model routing and the research behind them.
Other repositories run an instance of it.

## Principles

1. **The file is the handover.** Each phase ends in a file under `plans/`. The
   next session, human or agent, starts from that file, not from the chat.
2. **Gates are verdicts.** A phase passes when a check says so, for example
   `make verify` green or CI green. Between the artefacts stand gates that are
   not negotiated with: a red result stops the work.
3. **Decisions go to whoever owns them.** Intent belongs to the person.
   Mechanics belong to the model, with the reason written down. Details belong
   to the agent, with the reason in the artefact. Irreversible choices are
   asked; reversible ones are decided, recorded, and can be vetoed.
4. **Questions carry their context.** Before the options, a question to a
   person names the topic, why it comes up now, the situation today, and the
   change to the repository and to the architecture. The architecture decision
   record (ADR) 0018 makes this a rule for every question.
5. **Disagreements are kept, not netted.** When two reviewers disagree, both
   views stay in `findings.md`. A finding is taken only when a test or the
   spec supports it.
6. **Data decides which model may look.** Stage 2 calls to foreign models go
   only through `scripts/stage2.py`, which runs a leak check before every call.
   An endpoint that is not listed in `model-endpoints.yaml` is blocked. A leak
   finding stops the call; there is no fallback to another model.
7. **Who runs which phase is written down.** `docs/WORKFLOW.md` names the model
   for each phase. Reviews follow the change class; the other phases follow the
   phase.
8. **Process first, then model diversity, then orchestration.** The method
   works with one model and one session before more models or parallel agents
   are added on top of the artefacts.
9. **The core travels.** The method lives in repository files: `AGENTS.md`,
   `plans/`, `prompts/`, the `Makefile` and CI. The layer specific to one
   harness (`.claude/`) is thin and can be replaced.
10. **Texts carry their own meaning.** A reader without the session must
    understand every sentence. Ids and file names go in parentheses, never as
    the carrier of a sentence.

## The phases

| # | Phase | Leaves behind |
|---|---|---|
| 1 | Explore | `plans/changes/<name>/research.md` |
| 1a | Interview | `decisions.md` |
| 2 | Spec | `spec.md` |
| 2a | Spec review (optional) | review rows in `findings.md` |
| 2b | Design, by change class | `design.md` |
| 3 | Plan | `plan.md` |
| 4 | Implement | code and tests; loop rows in stage 2 (4b) |
| 5 | Verify | test output as evidence |
| 6 | Review | `findings.md` |
| 7 | Commit | a pull request, with CI green |

Across all phases runs the **session handover**: at the end of a session,
a file under `docs/journal/handover/`. The gate for each phase is in
`docs/WORKFLOW.md`, section 2.

## The three stages

- **Stage 1 — Claude Code only.** All seven phases run in Claude Code with
  Anthropic models. This is the binding baseline.
- **Stage 2 — other vendors for framework content.** Models from other vendors
  draft, review and repair this repository's own content. The calls go only
  through `scripts/stage2.py`. The scope is framework content only (ADR 0007,
  amended since). The routing is in `docs/WORKFLOW.md`, section 4.
- **Stage 3 — meta-harness.** Agents as YAML files, parallel worktrees and
  automatic routing. This stage is evaluative and not in production.

## Status

**Bootstrapping.** The mechanism is moved over from
`portfolio-agentic-engineering` in measured steps.

Checked on 2026-10-16 against `origin/main` at `6029bbf`, these pieces that the
doctrine names are **not in this repository yet**:

- `scripts/validate_change_artefacts.py`, the artefact validator
- the sub-agent definitions `.claude/agents/explorer.md` and `reviewer.md`
- the stop hook `.claude/hooks/session-stop/check-tests-green.sh`
- `.claude/commands/`, the slash commands
- the `make change` and `make index` targets. Start a change with
  `python3 scripts/new_change.py <name> --bead <id>` instead.
- `docs/governance/gate-catalog.md`

Where the doctrine describes one of them, it describes the target, not the
current tree. The status note at the top of `docs/WORKFLOW.md` has the details.

History: the bootstrap handover is
`docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`; the 2026-09-17
targets are in `docs/architecture/`.

## Repository layout

| Path | What it holds |
|---|---|
| `AGENTS.md` | Instructions that every agent harness reads |
| `docs/WORKFLOW.md` | The doctrine: phases, routing, rules |
| `prompts/` | One prompt per phase |
| `templates/` | Artefact templates, for example findings and handover |
| `plans/` | Changes in flight, archived changes and living specs |
| `decisions/` | The gate list (`gates.yaml`), the adoption record and recorded answers |
| `docs/adr/` | Architecture decision records (append-only) |
| `docs/journal/handover/` | Session handovers |
| `docs/research/` | Research notes |
| `model-endpoints.yaml` | Allowed model endpoints and the data classes they may see |
| `scripts/` | Gates, the stage-2 runner (`stage2.py`) and kit tooling |
| `tools/` | Tracker wrapper (`bd`), the pinned Pi install and Claude Code display |
| `tests/` | The test suite |

## Quick start

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

## Working in this repository

- **Tracker.** Beads with the `coding-harness-` prefix. Read and write them
  only through `tools/bd`. The tracker moves through `refs/dolt/data` on
  origin; no rendered copy is committed.
- **Pull requests** name every bead they open, change or close, because the
  diff does not show tracker changes.
- **Decisions** take effect when the maintainer merges their pull request
  (ADR 0008).
- **One change, one worktree.** Worktrees live under `.claude/worktrees/`.
- **Language.** Repository artefacts are in English.

## Related repositories

| Repository | Role |
|---|---|
| `coding-harness` (this one) | process source of truth: doctrine, prompts, templates, model routing, research |
| `portfolio-agentic-engineering` | framework governance: rule set, gates, ADRs, lessons; the origin this repository migrates from |
| `lakeswitch-ai` | product repository that runs a clean-room instance of the workflow |
