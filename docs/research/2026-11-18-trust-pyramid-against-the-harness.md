---
title: "The trust pyramid, against the harness"
category: research
created: 2026-11-18
updated: 2026-11-18
last_reviewed: 2026-11-18
status: draft
implementation_status: none
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: OpenCode, version: "deepseek-v4.1-flash via opencode-go, 2026-11-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [evaluation, enforcement, gates, review, outside-practice]
---

# The trust pyramid, against the harness

On 2026-11-18 the maintainer asked two questions about a conference talk:
what does it claim, and how far does this repository follow it. This note
records the answer, including the places where the answer is uncomfortable.

It is a reading by one session, not a research-swarm run. It measures the
working tree at `24632499` on 2026-11-18, which is 16 commits behind the
fetched `origin/main` of that morning (11:02 UTC). The two load-bearing
measurements were re-checked on `origin/main` and still hold there:
`scripts/stage2.py` is 11,487 lines, and `docs/WORKFLOW.md` still carries the
2026-10-31 sentence. What it could not read or run says so at the end.

## 1 · The source

- **Talk:** "All Code Is Slop (Except Mine)", Lauren Tan (poteto), Grok Bot
  team, published on the AI Engineer channel, premiered 2026-11-14.
- **URL:** <https://www.youtube.com/watch?v=O_zcc6Xl12g>
- **Transcript:** the automatic YouTube caption track, about 2,850 words. It
  is not edited: the speaker's handle appears as "Potato", the employer as
  "SpaceX SI". A working copy sits outside the repository at
  `~/Downloads/lauren-tan-all-code-is-slop-transcript.txt`.
- **Method:** the transcript was read in full; the claims below are the
  speaker's, the numbers are hers, and everything in §3 was measured against
  this tree.

## 2 · What the talk claims

**The thesis.** The job of a software engineer is to keep or improve the
quality of the code while raising productivity. The talk's word for the
result is not "software factory" but **trust**: "not blind trust but
investing in your agents' environment so you can trust that your agents are
going to do the right thing."

**The inverse pyramid.** Time goes into five layers, from the bottom up; the
lower a layer sits, the less of it there should be:

1. **The code itself** — API design, architecture, refactoring. "Anything
   that requires nuance to use well often leads to slop": `useEffect` is
   banned in product code, and the framework's renderer and main directories
   may not import each other, enforced by a dependency-graph analyser and
   lint rules.
2. **Static analysis** — types, compiler, tests, linter. "Every time we
   correct our agents, it turns into one of these deterministic checks", not
   another line in the rules file, "because it's far more reproducible when
   it's in code".
3. **Verification** — runtime verification with a **feature map** (a map of
   the product from the user's point of view, so the agent and the person
   share a vocabulary), custom CLIs inside skills so a driver is reused and
   testable, then formal methods: TLA+ for user flows such as notifications
   across devices, Lean for an own virtualisation library, property-based UI
   testing with Bombadil. "Not a silver bullet — another layer."
4. **Prose** — rules, skills, `AGENTS.md`. The layer that requires judgment,
   and the one that is deliberately thin.
5. **Human review** — the narrowest layer, and the one the slide's second
   line names: the person looks at what is left, not at everything. The
   talk's own practice is that most product pull requests no longer need
   deep human review, because the layers above removed the reasons for it.

**"Code is memory."** A second line on the same slide, and the reason the
codebase is the widest layer: what the agent reads next is the code it wrote
last. The codebase is not only the product, it is the agent's persistent
memory — which is also why a wrong pattern in it is copied rather than
corrected.

**The anti-pattern the talk names.** Markdown is an escape hatch: agents
write justifications into comments and docs for why the rule does not apply
here, and over-rotate on a small correction into a hard rule. Comments are
not enforceable, so most were banned and replaced by lint rules whose error
message sends the agent to the root cause.

**The bill.** Roughly 70 percent of the tokens go into verification. The
talk frames this as a good trade: "we are entering a golden age of software
testing", because tools that were too expensive to write and maintain before
became cheap.

**The numbers.** Around 3,000 pull requests shipped by the speaker in one
month; 11,000 for the team; about 0.5 percent reverted; a stable release
about once a day; 227 contributors in October; performance better than at
launch. The talk itself says the volume is not the interesting part — the
reverted share and the performance are.

**The order.** "If your inner coding loop produces slop, automating that
loop just produces more slop." Foundations before the factory.

## 3 · The harness against the pyramid

The four layers, measured on 2026-11-18. Maturity is given in this
repository's own vocabulary: level 4 blocks, 3 reports, 2 a person reviews,
1 convention only.

### Layer 1 — code and architecture: level 2

Present:

- The one-entry-point rule (`AGENTS.md`, house rule 9) is built as
  architecture, and for exactly one route it is also checked: RB-G1 holds
  the single gate list, with tests that the runner keeps no second command
  list.
- `decisions/gates.yaml` is the only list; `.github/workflows/ci.yml` is
  generated from it and `ci-drift` blocks a hand edit.
- Things deliberately *not* created, because each would be a second list: no
  `CLAUDE.md`, no `.mcp.json`, no pre-commit configuration.

Missing:

- `scripts/stage2.py` is **11,487 lines** — 371 functions and methods in 20
  classes, 16 percent of them docstrings, 42 bead ids cited in the code. The
  decomposition is real; the surface is the risk: every verb, guard, attempt
  and repair path shares one module namespace. The repository already names
  it as its hot file, with at most three open pull requests on it.
- **97 worktrees** stand beside the main checkout, **38 of them on branches
  already merged into `main`**. The workflow says why that is dangerous: a
  later session finds an old state and takes it for the current one.
- No type system. `mypy` was left out on purpose; nothing replaced it.

### Layer 2 — deterministic checks: level 4, with named holes

Present:

- 24 gates in one list: 20 block, 4 report or advise. `ruff check` and
  `ruff format --check`, 87 test files.
- RB-G4 requires a mutation test for every gate step, plus a ratchet that
  may only shrink.
- 25 ramp valves, each with a hard deadline; a passed deadline turns the
  gate red rather than reminding anyone.
- `tests/test_regelwerk.py` verifies that every enforcer named in the rule
  set exists as `file::function`. The edges of the rule map are checked, not
  just its cells.
- Fail-closed in several places: a leak check that cannot measure is BLOCK;
  verification refuses to run while a guard test's planting switch is
  present; a gate list that comes back empty is a configuration error, not a
  green run.

Missing:

- 13 valves fall due on 2026-11-30, 8 more on 2026-12-31. A valve is due when
  its predicate holds **or** its deadline passes, and either way `make verify`
  goes red. The predicate is the existence of the named test, so a test
  written without the rest fails the run the moment it lands: a valve closes
  as one unit — the test, the level raised in `regelwerk.md`, and the entry
  removed from `REGEL_VENTILE`, in one decision pull request. Five of the
  named test files do not exist at all.
- Six `@pytest.mark.skip` deadlines in `tests/test_feedback_channel.py:472`
  expire on the same 2026-11-30; their sentinel fails the suite when a date
  passes. Nineteen dated items therefore fall on one day, not thirteen.
- The artefact validator named for phases 2, 2a, 2b and 3
  (`scripts/validate_change_artefacts.py`) is not in the tree, although the
  phase table promises "validator green" for three artefacts.
- A change's `class:` is checked only by `explore`. A `feature` declared as
  a `spike` skips every stage-2 review; only the review before the merge
  could catch it.
- No type checker.

The suite is the larger half of the code: **86,822 lines across 86 files**
against 11,487 in `scripts/stage2.py`. It is not uniformly load-bearing, and
the weaknesses are of a kind the talk's layer 2 exists to prevent:

- Two tests cannot fail. `tests/test_gate_record.py:273` calls
  `pruefe_uebergang` with no assertion, so a no-op passes; the test above it
  catches the opposite direction. `tests/test_harness_time_log.py:296` builds
  its expected value with `time_records.insert_entry`, the function under
  test.
- Scripts with no test file of their own: `ci_gates.py`, `plans_registry.py`,
  `check_docs.py`, `handover_schema.py`, `_verdict.py`, `mutation_evidence.py`
  and `check_guard_test_environment.py`. Several are reached only indirectly,
  through `test_ci.py` or `test_gate_machinery.py`.
- Two tests are permanently skipped because they assert files this checkout
  never carries (`tests/test_ci.py:3171`, `:3385`).

A second reading pass named about a dozen further weak tests; only the two
above were checked here, and one claim of that pass did not hold (see §7).

### Layer 3 — verification: level 4 in one place, 0 elsewhere

Present, and here the repository goes beyond the talk:

- **The evidence rule:** a finding is taken only when a test demonstrates it
  or the spec supports it.
- **Red first:** every repair of code must produce a test that fails on the
  baseline in a temporary worktree (pytest exit 1 or 2). That is a
  mechanical proof, not an assertion.
- **The guard proof** (ADR 0023): a test-only repair plants a real fault
  under `STAGE2_PLANT_FAULT`, is proven red with the switch and green
  without it, and phase 6 treats a guard without a real fault as a BLOCKER.
- **The criterion ledger:** every acceptance criterion names its test, and
  the runner refuses new production code with no reachable test.
- The leak check as a boundary verification, fail-closed.
- The outcome test: a fresh session answers questions about the harness,
  which verifies the effect of the documentation rather than its wording.

Missing:

- **No runtime verification of the harness itself.** The talk's equivalent
  is "run the app and look". Here the app is the runner, and no
  deterministic end-to-end run over a synthetic change sits in the suite;
  the real verbs need credentials.
- **No formal verification where it would pay.** Lean is out of proportion.
  The verify admission lock is not: it cost nine phase-6 rounds over one
  mechanism, and its state space is small enough to model-check.
- **No property-based tests.** The parsers for loop records, findings rows
  and frontmatter are where malformed input keeps being repaired by hand.
- The reviewer sees the diff, not the verification evidence. That is a
  deliberate leak-surface decision, and it means review cannot check the
  verification story.

### Layer 4 — prose: level 2

Present:

- `docs/governance/regelwerk.md` holds 33 rules in six families, each with a
  level, an enforcer, a scope, and — below level 3 — a dated valve. No rule
  stands at level 1.
- The rule set is `human-decided` in `provenance.yaml`: changing a level is a
  decision pull request, and every change carries a version bump and a
  four-line entry.
- `AGENTS.md` stays under 200 lines, tested; one instruction file, tested.

Missing:

- The 33 rules do not cover the nine house rules of `AGENTS.md` or the
  operational rules of `docs/WORKFLOW.md`. 21 places in `AGENTS.md`,
  `WORKFLOW.md` and `prompts/` say of themselves that something is "stated,
  not enforced", "a request, not a lock" or held only by the review.
- The `docs-links` gate is `report`, not `block`, and measures **199**
  findings today; its stated reason still names 35. The backlog grew by a
  factor of 5.7 while the gate stayed non-blocking. That is the
  "report, not a gate" failure RB-G3 forbids for drift checks.
- Model routing stands in two places, `WORKFLOW.md` §3/§4 and the phase
  prompts. Only the resolution of model ids is checked, not that the two
  agree.
- `regelwerk.md` is German while house rule 1 says the repository is English;
  the normative page is the one that should be English first.
- `docs/WORKFLOW.md:1594` says the two DeepSeek readings expire 2026-10-31,
  while `model-endpoints.yaml:218` and `:294` say 2026-11-30. The renewal left
  the prose behind, and no test holds that sentence.

### Layer 5 — human review: level 2, by design

Present:

- The human layer is the **merge**, and the repository says so: RB-M2 makes
  the merge the signature, and ADR 0008 makes a decision take effect when the
  maintainer merges its pull request. The maintainer is "the owner of the
  intent, not the technical reviewer" (`WORKFLOW.md` §2).
- Nothing in the workflow asks a person to read a diff for correctness. That
  is what the four layers above are for: where they hold, the person decides
  whether the thing should exist, not whether it is built right.

Missing:

- The layer is thin in a way the pyramid does not describe: one person under
  one GitHub account holds every role, so a second approval does not exist.
  RB-M6 says it returns when a second identity exists.
- At the merge the person sees the pull request body and the diff, not the
  verification evidence. The talk's practice — review the artefacts, not the
  code — is only half followed.

### The shape

| Layer | Level | Finding |
|---|---|---|
| 5 human review | 2 | The merge is the signature; one account holds every role |
| 4 prose | 2 | The map exists; the coverage does not |
| 3 verification | 4 / 0 | Excellent at the repair proof, empty at runtime and formal |
| 2 checks | 4 | Strong; every hole is named |
| 1 code | 2 | One 11.5k-line file, 38 finished worktrees |

The harness built the middle of the pyramid first. For a harness that is
partly right: its product *is* the checks. The bill for the lower layer
arrives anyway, in a file that every path runs through and in a garden of
worktrees that no longer serve anything.

### Code is memory, here

The repository follows the principle in form. The artefact is the handover,
not the chat; a handover is appended to, never rewritten; ADRs are append-only,
and `tests/test_stage2.py:9881` keeps ADR 0011's original "at most three
rounds" standing while the live prompts forbid the phrase — the memory of what
was decided, kept next to the decision that replaced it. The test suite is the
strongest memory: 2,101 collected cases in `tests/test_stage2.py` alone, each
one a failure the repository is not allowed to repeat.

It does not follow the principle in maintenance. A worktree that stays after
its merge is an old state a later session can take for the current one; a date
in prose that no longer matches its declaration reads as current; a fact
stored twice diverges. The three answers stand in §6, points 8 to 10, and they
share one shape: one home, one date, one check. A memory that never forgets
becomes an archive, and an archive nobody prunes becomes a trap — so the
missing half of the principle is not more writing but reading on every run,
which is what a check is.

## 4 · What the reading adds beyond the talk

- **The rule map already exists, and its edges are verified.** The talk
  implies that a team writes lint rules and rules files. This repository
  keeps 33 rules with a level and an enforcer, and a test fails when a named
  enforcer stops existing. That is stronger than the talk's practice, and it
  is the part worth keeping when the rest is repaired.
- **A self-declared class is a hole in the middle of the loop.** The routing
  by class is the mechanism that decides how much review a change gets, and
  the change itself states its class. No check confirms it. This is the
  clearest instance of the talk's "Markdown is an escape hatch": a header
  field, written by the agent, that switches off the agent that would check
  it.
- **A valve is the right form for a known gap, but only with a hard date.**
  The repository already does this; the deadline is what makes it a
  mechanism rather than a promise. An undated valve is an exception under a
  better name.
- **Prose debt can be made to cost something at the moment it is written.**
  A sentence that says "not enforced" could be required to name an open
  bead in the same paragraph. That closes the class of problem instead of
  its instances, and it needs no second list: the tracker is the list.

## 5 · What to adopt, what not to

**Adopt:** the correction-to-check rule; the ratchet that only shrinks; the
verified enforcer edges; verification artefacts as the object of review
where the leak surface allows it; the refusal to automate an inner loop that
still produces slop.

**Do not adopt:**

- **Banning comments.** Here comments carry reasons no check can carry — why
  a gate looks the way it does. The transferable part is narrower: a comment
  that explains a *checkable* rule is an unfinished check.
- **Pull-request volume as a goal.** The comments under the talk make the
  same objection the talk half-makes itself; the reverted share and the
  performance are the measurements, not the count.
- **One agent writing and verifying.** The repository already refuses this:
  no model reviews its own draft, and a reviewer's session never repairs.

## 6 · The consequence, as a proposal

One session derived eleven building blocks from this reading and presented
them to the maintainer on 2026-11-18. They are a **proposal, not a
decision**: no bead, no change folder, no code. In short:

1. Correct the two promises the phase table makes and the tree does not keep.
2. Close valves one unit at a time, never as a test alone: the test, the
   level raised in `regelwerk.md`, and the valve removed from
   `REGEL_VENTILE`, in one decision pull request. Ten of the thirteen are
   buildable; three name machinery this repository does not have, so their
   valve condition needs a rule amendment before any test exists — otherwise
   the test is written against a rule that describes nothing.
3. Make prose debt name an open bead in the same paragraph.
4. Check the class mechanically: a `spike` that changes product code, or one
   that claims an ADR file, is not a spike.
5. Build the artefact validator, scoped to changes after the adoption day.
6. Report the P1 cap as a drift gate, not a blocking one.
7. Build the tracker write guard as its own change, last.
8. **Give every fact one home.** The model names leave `prompts/*.md`; the
   routing stays in `WORKFLOW.md` and `model-endpoints.yaml`. The dates in
   `WORKFLOW.md:1594` go, replaced by a pointer to the declaration.
   Duplication is removed, not reconciled: two copies that must agree are a
   check waiting to be written, one copy is not.
9. **Give every non-blocking gate a date.** Any gate with
   `enforcement: report` or `advisory` names a valve with an `until` date and
   a bead, and `ci_gates.py --check-schema` refuses a free-text reason that
   carries a count. The "35" in the `docs-links` reason is the example: a
   count in prose is memory that rots.
10. **Make worktrees decay.** One entry point, `scripts/worktree_prune.py`:
    `--check` lists worktrees on merged branches, older than seven days, or
    dirty; `--prune` removes only merged, clean, unpushed ones and refuses
    the rest. A writer gate reports the count, and a valve turns it blocking
    on a date.
11. **Lock the import direction.** No file under `scripts/check_*.py`
    imports `stage2`: a gate is read-only, while the runner writes, calls
    foreign models and takes the verify admission. Measured on 2026-11-18:
    zero violations, so the test locks in a property that already holds — a
    ratchet, in the form of RB-G4's mutation ratchet (bead
    coding-harness-7ayv).

The order matters: the dated valves first, then the ratchet, then the
missing gates. None of the last three is a cleanup — the 97 worktrees are
the symptom, the missing decay is the cause.

## 7 · How this ran, and what it did not do

This session ran on `deepseek-v4.1-flash` through the `opencode-go` provider,
inside OpenCode, on 2026-11-18. The transcript was fetched with
`youtube-transcript-api` in a temporary virtual environment outside the
repository; a working copy sits in `~/Downloads`.

Read in full: `AGENTS.md`, `docs/WORKFLOW.md`, `docs/governance/regelwerk.md`,
`scripts/verify_all.sh`, `tests/test_regelwerk.py`, `scripts/ramp_valves.py`
and the gate list in `decisions/gates.yaml`. Read in outline and in its
load-bearing parts, not line by line: `scripts/stage2.py` — `run_attempts`,
`verify_attempt`, `require_fresh_full_verification` and `main`. The 86 test
files other than `tests/test_stage2.py` were read by a second pass that
reported per file what it protects; two of its findings were spot-checked, and
one claim did not hold — the `master` name in `test_repo_settings.py:1025` is
a documented legacy name, not a contradiction. `tests/test_stage2.py`
(28,466 lines) had a reader of its own; its report is not in this note.

Measured on 2026-11-18: `make verify` came back **red** first — 108 failed,
6,169 passed, 17 skipped, 41 errors — and the cause was environmental, not a
regression. The checkout carried Pi 1.2.0 while `tools/pi/package.json` pins
1.5.0; all 108 failures in `tests/test_stage2_research_catalog.py` and all 41
errors in `tests/test_pi_contract.py` come from that one version mismatch.
After `bash tools/pi/install.sh` the two files passed (174 tests, 2:09), and a
second full run came back **green**: 6,318 passed, 17 skipped, the pytest gate
605 seconds, `leerprobe` green at 96 percent (1,408 of 1,452 cases), and
`VERIFY GREEN` over every local gate of the verify job.

Not measured:

- The bead export was not read, so the status of beads named elsewhere in the
  tree is not confirmed here.
- The talk's numbers are the speaker's, taken from the transcript; nothing in
  this note measures them.
