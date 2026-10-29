---
title: "How the workflow tests — the strategy that travels with the kit"
category: architecture
status: proposed
created: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [testing, gates, kit, verification]
---

# How the workflow tests

**A claim counts when a run can turn red on it.** A sentence in a document
proves nothing. A test, a gate or a probe that fails when the claim stops
holding does. This page is part of the kit, so it describes the strategy, not
one repository's numbers.

## Six layers

| # | Layer | What it holds | Where |
| --- | --- | --- | --- |
| 1 | Every criterion names its proof | Each acceptance criterion in `spec.md` says what refutes it. The plan's `## Criterion ledger` names the test that proves it. A gate turns red when that test disappears. | `spec.md`, `plan.md`, gate `criterion-ledger` (`scripts/check_criterion_ledger.py`) |
| 2 | Red first | A repair of code counts only when its test fails on the code before the repair. The runner checks this itself: it runs the named test alone against the old code in a temporary worktree. | [Repairing taken findings](WORKFLOW.md#repairing-taken-findings-repair) |
| 3 | One gate list | `make verify` and the hosted CI run the same list. `scripts/verify_all.sh` asks `scripts/ci_gates.py`, and that reads [`decisions/gates.yaml`](../decisions/gates.yaml). `ci.yml` is generated from the same file, and a hand edit fails the gate `ci-drift`. | [Verification](WORKFLOW.md#verification-runs-through-git-and-ci-not-through-the-harness), [gate catalog](governance/gate-catalog.md) |
| 4 | The gates test themselves | Every gate has a mutation test: a run that turns red when the thing the gate protects is broken. A gate without one needs a reason in a list that may only shrink (rule RB-G4). An empty set is no result: every gate asserts that what it measured is not empty (rule RB-G7). | [Rule table](governance/regelwerk.md), `scripts/mutation_evidence.py`, `tests/test_ci.py` |
| 5 | A locked environment | Each checkout builds its own `.venv` from a lock with a hash for every package. Pinned outside tools are tested as the real program against offline contracts, not as expected arguments. A local green means what a CI green means. | `requirements-ci.txt`, `make venv` |
| 6 | The kit probe | The probe copies everything the kit manifest marks as mechanism into an empty repository and runs the tests there. A red case must be listed with its reason, or the gate `leerprobe` blocks. This is how "the workflow can be handed over" becomes a run. | `scripts/kit/probe.py`, `scripts/kit/manifest.yaml` |

Layer 1 is a trust rule against models. A model cannot make a red test go away
without a visible edit of the plan. Layer 2 stops the most common weak repair,
a test that would have passed anyway.

## How a test is written

- **Stand-ins, never live calls.** A test that drives the runner puts small
  programs on `PATH` in place of the model tools. They record their
  arguments, environment and input, print canned output and contact nothing.
  Credentials are synthetic. No test reads the maintainer's denylist, secrets
  or loop records.
- **Each new test names its fault.** Its docstring says which fault the test
  was red on (`Planted fault: …`); this is the convention for new tests, and
  older ones are not all rewritten. A test that has never been red is a test of
  nothing.
- **Doctrine tests.** Some tests read the workflow's own documents and prompts
  and pin a rule there. Each one checks its fault on a planted copy of the
  text, so the test is shown to catch the drift it guards.
- **Mutation names.** A test that proves a gate goes red carries the fact in
  its name (`…_goes_red…`, `…_refuses…`, `…_is_caught…`). A name moves with a
  rename, a comment does not. The gate ratchet counts these names.
- **A test reads only what travels**, or it skips with its reason. Otherwise
  the kit probe turns it red in a repository that lacks the file.

## Where tests run

| Where | When | Role |
| --- | --- | --- |
| Stop hook | at the end of an agent's turn, only when Python changed since `HEAD` | comfort: an agent does not hand back a red tree. It is not the enforcement. |
| `make verify` | before a commit of code, and inside every runner attempt | the full local run of every gate that can measure on this machine |
| Hosted CI, job `verify` | on each pull request, against its merge commit with `main` | the merge gate; the branch ruleset requires it |
| Hosted CI, job `drift` | on a schedule | gates that change with time, not with a commit (strict plan hygiene, research currency) |

A change to Markdown outside `scripts/`, `tests/`, `prompts/` and
`decisions/` skips the local `make verify`; CI is its gate.

## Reviews find, tests prove

Reviewers find candidates; they do not prove anything. Examples are the review
loop's model swarm, the phase-6 review and the spec review. A finding is taken
only when a test demonstrates it or the spec supports it. Otherwise it is
rejected with its reason and stays recorded as a disagreement. A taken finding
about code is repaired with a red-first test. Where a fix lives only in test
code, the old code cannot show it red. Today the orchestrator then shows, by
hand, a planted fault that turns the new test red while the old test stays
green; a runner form for it is open work.

## What this does not prove

- **Counts measure how much is checked, not how well.** A large suite can
  still miss a fault nobody wrote down. Mutation testing of the scripts is
  planned, not built.
- **Stand-ins prove the runner's handling, not the models.** Whether a model
  reviews or implements well is measured on real runs, not in the suite.
- **A green run proves the named criteria.** What no criterion names, no
  gate holds.
- **The stop hook can be skipped.** The hosted `verify` job is the gate that
  cannot.
