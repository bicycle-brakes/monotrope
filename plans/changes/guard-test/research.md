---
title: "Research — guard-test"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-0ho
class: feature
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair, red-first]
---

# A guard-test mark for test-only repairs — Research

Phase 1 for bead coding-harness-0ho ("stage2 repair: red-first exception for
fixes that live only in test code"), which since 2026-10-27 also carries bead
coding-harness-y17 ("stage2 repair: a test-strength finding has no red-first
form").

## Refresh against main — 2026-10-29

Read by the orchestrating session on 2026-10-29 against `origin/main` at
`5f57f4e9`. The sections below this one are the phase-1 research of
2026-10-15/16, copied unchanged from `plans/changes/guard-test/research.md`
on the dropped branch `explore/guard-test` at `1d6cd430`; their symbol names
still hold unless this section says otherwise, and their line-free anchors
were checked against the current tree. Maintainer decision of 2026-10-29:
redraft spec and plan on current main with the answers Q-1 to Q-5 of
`decisions.md`, no new interview.

### What moved since 2026-10-16

- **Class.** The bead now names the change `feature` (2026-10-27), not
  `bounded` as the 2026-10-15 text below says. The interview minimum is
  three answers, five with an ADR edit; five stand (`decisions.md`).
- **Bead a7m is closed.** Change `red-first-pytest-failed` (bead
  coding-harness-a7m) taught `red_first` that pytest's own failed outcome
  counts as red, not only an `AssertionError`: DID-NOT-RAISE, DID-NOT-WARN
  and a body `pytest.fail` (`scripts/stage2.py`, `red_first` docstring, its
  Q-1 and Q-2). Fourteen of the 32 failed attempts the bead cites
  (2026-10-27) were of this kind; that cause is gone. What remains is the
  case this change is about: a correct test over correct code is green on
  the baseline, whatever its failure type.
- **`red_first` no longer trusts the exit code.** A runner-owned pytest
  plugin (`RED_PROBE_NAME`, `RED_PROBE_SOURCE`, read back by
  `_red_record_fault`) is written into the temporary checkout and records
  which cases ran and how each setup, call and teardown ended; the proof
  holds only for exit 1 with a qualifying failure of the named test (bead
  coding-harness-omp). The red-first interpreter and pytest come from
  `.venv/`, and a changed tool tree is refused (`tool_problem`, R-21).
- **A green proof after the fix.** `fixed_test_proof` runs the named test on
  the fixed code with the same probe and requires a pass; only then is the
  loop row's `Broke a test` mark written, and it now reads
  `yes — <test>` ("the proof ran"), `no — not a test` for a not-a-test row
  (`check_repair_answer`, the `marks` dictionary; R-24, the maintainer's
  answer C of the night interview of 2026-10-20). A guard-test row needs
  its own mark wording here.
- **The environment of a red-first run is an allow-list.** Both pytest
  launches go through `runner_env(foreign_env({...}))`; `foreign_env`
  copies only `ENV_ALLOW` from the caller and adds the call's own variables
  (`STAGE2_RED_REPORT`, `STAGE2_RED_TOKEN`, `STAGE2_RED_SELECTOR`). The
  `STAGE2_PLANT_FAULT` switch of Q-1 therefore never leaks in from the
  caller; the runner must set it explicitly in the planted run's own
  variables, and leave it out of the clean run.
- **Where the guard proof would run.** Q-1 asks for two runs of the guard
  test: with the switch red, without it green. The fixed-code green run
  already exists (`fixed_test_proof`). The red run is new: it runs on the
  attempt's tree (the code is right, so the baseline proves nothing), with
  the switch set, through the same probe; a qualifying failure is required
  as in `red_first`. Whether it reuses `red_first`'s temporary-worktree
  machinery started from the attempt's tree, or runs in place like
  `fixed_test_proof`, is a design detail for the spec.
- **The answer constant grew.** `REPAIR_ANSWER` (shared by `REPAIR_FORMAT`
  and `REPAIR_FORMAT_FILE_TOOLS`) now also states the id rules, the
  one-fixed-line rule and the hand-repair booking; `fixed_status` and
  `check_repair_answer` are as described below, plus the doubled-claim and
  climb-out rules. The guard form `fixed — guard test — tests/<path>::<function>`
  (Q-1, Q-2) slots into `fixed_status` beside the `not a test` branch, and
  the row check beside the one that refuses a `not a test` answer for a code row.
- **Taken-row grammar.** `RECORD_INTRO` and `repair_targets` still read
  `taken — <test or criterion>`, `taken — not a test — <reason>` and
  `rejected — <reason>`; `taken — guard test — <reason>` (Q-2) is new to
  `RECORD_INTRO`, `templates/findings.md`, `prompts/04b-review-loop.md` and
  `docs/WORKFLOW.md` §4. `repair_targets` selects by the prefix `taken`, so
  it needs no change.
- **Phase 6** (Q-3). `review` still builds its prompt with
  `phase_prompt(root, "06-review.md", change, ...)`; the 2026-10-16 gap
  check below (the shared rows-only answer format) still applies.
- **The gate** (Q-5). `decisions/gates.yaml` holds 23 gates on 2026-10-29;
  `scripts/verify_all.sh` and the generated CI read it, so a gate that
  refuses a set `STAGE2_PLANT_FAULT` is one entry plus its seeded-red test
  (`tests/test_ci.py`).
- **Doctrine places** unchanged in role: `prompts/04-implement.md`
  ("Repair."), `docs/WORKFLOW.md` §4 ("Repairing taken findings", the
  `Broke a test` column: "the finding's own new test does not count: the
  evidence rule expects it to be red first"), ADR 0017, ADR 0013 (criterion
  ledger; Q-4 keeps the guard form out of it).
- **Tests.** The repair tests still live in `tests/test_stage2.py` (301
  `Planted fault` comments on 2026-10-29); the helpers `repair_step`,
  `script_repair`, `seed_tests` and `repair_world` were not re-read.

### The test-strength rows (bead y17)

`plans/changes/test-strength-rows/research.md` (on main since PR #261)
explored y17 on 2026-10-14 and listed four candidate forms (a fault patch
run by the runner; the orchestrator naming the fault; old test versus new
test on the planted fault; a green test without proof). The maintainer's
answers for this change settle that question: the test itself plants the
fault behind `STAGE2_PLANT_FAULT` (Q-1), only a row the orchestrator took
as `taken — guard test` may use it (Q-2), and phase 6 checks that the fault
is real (Q-3). A test-strength row is therefore taken as
`taken — guard test — <reason>`; no fault patch and no old-versus-new run
are part of this change.

### Not read

- The live tracker beyond the two beads' descriptions and notes.
- The 133 uncommitted lines of `findings.md` in the old worktree
  `.claude/worktrees/guard-test` (left untouched, per the bead's comment of
  2026-10-19).
- The old branch's `spec.md` and `plan.md`; they are superseded by the
  redraft and serve at most as a reference for the drafter.

## The question

The repair verb (`python3 scripts/stage2.py repair <change>`) demands, for
every taken row, a named test that is red on the baseline production code
and green after the repair ("red-first"). On 2026-10-14/15 the right fix
was three times a test or a test helper over production code that was
already right (sol-effort L1-1 and L3-1, haiku-5-5 F-1/F-2): a new test is
then green on the baseline, the runner refuses, and one Codex attempt moved
checker logic into `scripts/stage2.py` only to satisfy the check. The
orchestrating session finished those rows by hand or through an Opus
sub-agent.

The maintainer chose (2026-10-15, answer "A") a "guard test" mark: for a row
marked that way, the test plants the fault itself (for example by swapping
a function or a fixture inside the test) and must be red with the planted
fault and green without it; the runner checks that instead of red on the
baseline. Rejected: a runner-side mutation check, and an exception without
proof. It is to be built before the implementation of coding-harness-agx,
whose contract suite is mostly tests over code that is already right.

## To explore

How the repair verb reads the answer's fixed lines and runs the red-first
proof today (the functions around the "no fixed line" check and the
red-first runs in `scripts/stage2.py`); how the existing "not a test" form
and the status forms (`fixed — <test>`) work; how the existing tests plant
faults ("planted fault" in `tests/`); what a guard-test line would have to
name so the runner can run the test once with and once without the planted
fault, without trusting the model's own word; where the doctrine
(`docs/WORKFLOW.md`, `prompts/04-implement.md`, ADR 0017) describes
red-first and would need the new mark.

Stage-2 call, 2026-10-15: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 440 files, 1257 commits, 12 rules.

## Runner exploration — 2026-10-15

Exploration is complete. Here is the research prose, ready to append to `plans/changes/guard-test/research.md` under the seed's "To explore" section.

---

## What exists today (explored 2026-10-15, branch `explore/guard-test`)

### The repair verb and its baseline

`repair(root, change, stage2_off)` (`scripts/stage2.py`, `def repair`) takes the taken rows from the loop record through `repair_targets(ctx, read_record(change))`, refuses waiting, missing or doubled ids, and fixes `baseline` once at verb start as `rev-parse HEAD` (`scripts/stage2.py`, `repair`, the line `baseline = _git_output(root, "rev-parse", "HEAD").strip()`). It runs three routes in order — Codex, a fresh Codex attempt with the first one's diagnostics, then a Sonnet 5.5 stage-1 fallback (`scripts/stage2.py`, `repair`, the `routes` list; ADR `docs/adr/0017-codex-repairs-taken-findings.md`) — and hands each attempt's answer to `check_repair_answer` through the `answer_check` callback (`scripts/stage2.py`, `repair`, `def check` and the `run_attempts(...)` call, where `answer_check=check`, `before_commit=mark_repaired_findings`, `after_commit=mark_repaired_record`). The loop record itself lives outside the repository at `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md` (`docs/WORKFLOW.md`, "The review loop (phase 4b)").

### How the answer's fixed lines are read today

The prompt constant `REPAIR_ANSWER` (`scripts/stage2.py`, near the top, "Answer with one fixed line per row…") offers the model exactly two forms: `<ID>: fixed — tests/<path>::<function>` or `<ID>: fixed — not a test — <reason>`, and says "A code row needs a test that fails on the baseline's code, which the runner runs". `REPAIR_FORMAT` and `REPAIR_FORMAT_FILE_TOOLS` (`scripts/stage2.py`, directly below) prepend the do-not-commit rules to it. `fixed_status(ident, rest)` (`scripts/stage2.py`, `def fixed_status`) parses one line: it full-matches `fixed — (.+)`, routes a `not a test`/`not a test —` body through a reason-required branch that re-escapes `|`, and otherwise accepts a body only when `FIXED_TEST` matches — the regex `^tests/(?P<file>[^|\s]+\.py)::(?P<function>test_\w+)$` (`scripts/stage2.py`, `FIXED_TEST =`), which its comment says mirrors the criterion ledger's gate in `scripts/check_criterion_ledger.py` — plus a climb-out guard that refuses `.`/`..` path segments. Anything else becomes the problem "is neither a test … nor `not a test — <reason>`".

`check_repair_answer(ctx, answer, taken, baseline, key, before, audit_line, findings_before)` (`scripts/stage2.py`, `def check_repair_answer`) checks in order: form problems per line, then findings.md integrity (the audit line still present, the body unchanged outside the frontmatter, released and phase-6 rows compared as `Counter` multisets so a duplicated or removed copy fails too), then — only when no problem stands — the per-row checks: a `fixed — not a test` answer is accepted only when the row's Status cell (`row[7]`) starts with `taken — not a test`, otherwise "it needs a test that was red first"; a test answer must define `def <function>(` in the named file, read through `_read_quietly`. That existence check is the only thing the runner ever reads inside a named test file; the test's body is never inspected.

### How the red-first proof runs today

`red_first(root, baseline, test, key)` (`scripts/stage2.py`, `def red_first`) runs the named test exactly once. It creates a temporary git worktree (`tempfile.mkdtemp(prefix="stage2-red-")`, `git worktree add --detach` at `baseline`), replaces the checkout's `tests/` with the attempt's `tests/` (`shutil.copytree`, ignoring `__pycache__` and `.pytest_cache` — the docstring: "a test of the new tests against the old code is what 'red first' means"), proves the interpreter can start pytest (`red_first_python(root)`, `scripts/stage2.py`, `def red_first_python`: the checkout's `.venv/bin/python3` when executable, else `sys.executable`; a failed startup is named, not read as red — phase 6, F-1), then runs one pytest command `-m pytest -q -p no:cacheprovider <file>::<function>` under `RED_FIRST_MINUTES = 10` (`scripts/stage2.py`, `RED_FIRST_MINUTES =`). Exit 1 or 2 is red; exit 0 (or anything else) returns "pytest ended 0 on the baseline's code; red first is exit 1 or 2". Before and after, `_ref_targets(root)` (`scripts/stage2.py`, `def _ref_targets`) snapshots every ref; any difference fails the proof and nothing is deleted (phase 6, F-6 and F-7). Clean-up removes the worktree before pruning and names a failed removal (repair round 3, L3-4). There is no second, fault-free invocation and no mechanism by which the runner plants or unplants a fault — a fault exists only if the attempt's own `tests/` copy contains one.

### The status and mark vocabulary today

The orchestrator writes a loop row's Status as `taken — <test or criterion>`, `taken — not a test — <reason>` or `rejected — <reason>`, plus `Broke a test` (`yes`/`no`) — `RECORD_INTRO` (`scripts/stage2.py`, "Write `Status` …") and `docs/WORKFLOW.md` ("The review loop (phase 4b)" and "Two columns for every stage-2 change"). The `Broke a test` column definition already states the relevant rule: "The finding's own new test does not count: the evidence rule expects it to be red first" (`docs/WORKFLOW.md`, "Two columns for every stage-2 change"). After a green repair, `mark_repaired_findings` (`scripts/stage2.py`, `def mark_repaired_findings`) writes each fixed line into the taken row's Status cell (index 7) of `findings.md` before the checkpoint commit, and `mark_repaired_record` does the same for the loop record (called as `after_commit` in `repair`; its body was not opened). The findings template names the Status words `taken — <reason>`, `taken — not a test — <reason>`, `fixed — tests/<path>::<function>`, `fixed — not a test — <reason>` and `rejected — <reason>`, plus `taken — <test or criterion>` for loop rows (`templates/findings.md`, the Status vocabulary section).

### Precedent: guard tests that plant their own faults

The two rows the seed names as the trigger stand in `plans/changes/haiku-5-5/findings.md` (phase-6 table, rows F-1 and F-2), both closed with Status text "guard test, plants each fault itself; red first impossible because the code was already right — completed by the orchestrating session". They exist as `tests/test_stage2.py::test_both_anthropic_endpoints_authorize_haiku_5_5_instead_of_4_5`, which deep-copies `model-endpoints.yaml`, plants the three faults `missing`/`replaced`/`retained` and asserts `anthropic_haiku_problems` flags each, and `tests/test_stage2.py::test_the_current_haiku_instructions_reject_4_5`, which replaces every `Haiku 5.5` pin with `Haiku 4.5` in the operative texts and asserts `haiku_instruction_problems` flags it. The house pattern is stated in the test module docstrings: "was planted one by one and each one turned a test here red" (`tests/test_stage2.py`, module docstring), "Each test names the fault that turns it red; the plan's time log says that each was planted once" (`tests/test_stage2_runs.py`, `tests/test_stage2_session.py`, same wording), and "a gate that has never been red measures nothing" (`tests/test_touch_map.py`, module docstring; `tests/test_research_currency.py` likewise). On the runner side, tests plant faults through scripted model steps: `repair_step(plant={...})` (`tests/test_stage2.py`, `def repair_step`) writes files into the attempt before the runner reads the answer, `script_repair` (`tests/test_stage2.py`, `def script_repair`) scripts the Codex–Codex–Sonnet order of ADR 0017, and `seed_tests`/`repair_world` (`tests/test_stage2.py`) commit a `tests/` directory so the red-first worktree has a baseline tree.

### Doctrine that names red-first and the tests that pin it

Red-first appears in: `prompts/04-implement.md`, the "Repair" paragraph ("A code row needs a test that is red first — it fails on the baseline's code — and the runner runs that proof itself"); `docs/WORKFLOW.md`, "The evidence rule" (§2: taken only when a test demonstrates it or the spec supports it) and the §4 repair statuses ("The review loop (phase 4b)" continuation, referencing the evidence rule) and the `Broke a test` column; and `docs/adr/0017-codex-repairs-taken-findings.md` (the taken/fixed forms: "a taken finding with a defined test the runner demonstrates red against baseline code; a finding taken as `not a test` is proven by the separate re-check. Fixed rows read `fixed — tests/<path>::<function>` or `fixed — not a test — <reason>`"). `AGENTS.md` contains no `red first`/`red-first` match — the repo-wide search found none there. Three runner tests pin the current wording and semantics: `test_the_prompts_name_the_repair_verb_and_red_first` (`tests/test_stage2.py`, criterion 31 — `repair_prompt_problems` requires "red first" in `prompts/04-implement.md` and the repair command in `prompts/04b-review-loop.md`), `template_problems`/`test_the_findings_template_names_the_repair_statuses` (`tests/test_stage2.py`, criterion 32 — the `REPAIR_STATUS_WORDS` list must all stand in `templates/findings.md`), and `test_a_named_test_that_is_not_red_first_fails_the_attempt` (`tests/test_stage2.py`, criterion 18 — a green-on-baseline test is refused with the "pytest ended 0" sentence; today unconditional, with no mark to opt out). The remaining red-first runner tests: `test_a_red_first_interpreter_that_cannot_start_pytest_fails_the_attempt`, `test_the_red_first_run_leaves_no_worktree_behind`, `test_a_ref_created_while_the_named_test_ran_fails_the_proof_and_is_never_deleted`, `test_an_existing_ref_moved_while_the_named_test_ran_fails_the_proof`, `test_a_failed_worktree_remove_leaves_no_dead_entry_and_is_named` (all `tests/test_stage2.py`; the last calls `stage2.red_first` directly). Some tests also assert `stage2.REPAIR_FORMAT` verbatim in the prompt (`tests/test_stage2.py`, e.g. the assertion `stage2.REPAIR_FORMAT in prompt`).

## What is unclear

- The bead coding-harness-0ho's own wording was not read: the tracker is the Dolt database under `.beads/` with no rendered copy committed (AGENTS.md, house rule 2), and this phase's read-only tool set (Read/Grep/Glob) cannot render it. The seed research above carries the maintainer's decision (2026-10-15, answer "A").
- The bodies of `repair_targets`, `read_record`, `repair_prompt` and `mark_repaired_record` (`scripts/stage2.py`) were not opened; their roles are known from the call sites in `repair` (row selection from the loop record, prompt rendering, record rewrite). If the mark travels in the loop record's Status, it passes through `repair_targets` and `mark_repaired_record`.
- How the runner could run a named test once with and once without a fault the test plants itself, without trusting the model's word, is the seed's own open question; the facts collected here bound it: `red_first` runs one pytest command per call, the runner's only look into the test file is the `def <function>(` existence check in `check_repair_answer`, and the fault, if any, lives only in the attempt's copy of `tests/` inside the temporary worktree.
- Whether the criterion ledger's sibling `not a test` form (`scripts/check_criterion_ledger.py`, `NOT_A_TEST =` and its format sentence) is in scope is not stated anywhere; it governs plan.md criterion entries, not findings rows.

## Files a change would have to touch

`scripts/stage2.py` (the answer constants `REPAIR_ANSWER`/`REPAIR_FORMAT`/`REPAIR_FORMAT_FILE_TOOLS`, `FIXED_TEST`, `RED_FIRST_MINUTES`, `RECORD_INTRO`, `fixed_status`, `check_repair_answer`, `red_first`, `mark_repaired_findings`, `repair`) · `templates/findings.md` (the Status vocabulary) · `prompts/04-implement.md` (the Repair paragraph) · `docs/WORKFLOW.md` (the evidence rule, the §4 repair statuses, the `Broke a test` column) · `docs/adr/0017-codex-repairs-taken-findings.md` (the repair doctrine the seed says would need the mark; whether by amendment or successor ADR is a decision, not a fact of today) · `tests/test_stage2.py` (the red-first runner tests, the criterion 31 and 32 wording tests, and the helpers `repair_step`/`script_repair`/`seed_tests`/`repair_world`).

---

Stage-2 explore call for this phase, per the seed's record: attempt 1, route flash, model glm-5.3-flash, leak check clean. Nothing was designed, recommended or edited; every statement above names its file and symbol.

## Draft-stage gap checks — 2026-10-15

Read against `a4b0780813ca2cf14b41c03b23c9bf6e698df77b`:

- The interview settles the switch and the answer spelling; the earlier
  exploration's uncertainty about separating the runs is closed by Q-1 in
  `decisions.md`.
- `repair_targets` selects statuses beginning `taken` and treats statuses
  beginning `fixed` as already decided. `mark_repaired_findings` and
  `mark_repaired_record` copy the supplied fixed status into the row's Status
  cell. The guard mark therefore needs no new taken-row grammar or record
  field (`scripts/stage2.py`, the three named functions).
- The criterion ledger accepts test references, not repair-answer statuses;
  the guard mark does not belong in its grammar
  (`scripts/check_criterion_ledger.py`, `TEST`, `NOT_YET`, `NOT_A_TEST`).
- There is no plan template under `templates/`; the plan follows
  `prompts/03-plan.md` and the existing bounded example
  `plans/changes/haiku-5-5/plan.md`. The requested
  `scripts/validate_change_artefacts.py` is also absent; it cannot provide a
  green result at this baseline.
- The planned note in ADR 0017 is still an ADR edit: the interview gate
  requires five human answers for any claimed ADR file actually edited,
  whatever the class; a bounded change otherwise requires one. There is
  one answered record in this change's `decisions.md`. Thus a green check
  before the ADR edit does not discharge the four additional records owed
  before implementation (`scripts/check_interview_minimums.py`, `measure`;
  `docs/WORKFLOW.md`, "Change classes, the ADR question and decision pull
  requests"). This is an interview prerequisite, not an unanswered choice
  about the switch. No answers or skip records are invented in this draft.
- ADR files are reserved for `human-decided` provenance. Its planned note
  consequently makes the eventual implementation pull request a decision
  pull request; no new ADR is due under the recorded bounded classification
  (`provenance.yaml`, prefix `docs/adr/`; `docs/WORKFLOW.md`, the same section).

The latest handover read was `docs/journal/handover/2026-10-15-night-run-fourth.md`;
its test-only repair blockage agrees with the seed. The local branch and its
remote-tracking ref both name the commit above. Live pull-request state and
other sessions were not read; this runner task changes no tracker state.

### Draft validation — 2026-10-15, uncommitted artifacts over `a4b0780`

- `python3 scripts/check_interview_minimums.py --change guard-test` through
  the worktree's `.venv/bin/python3`: exit 0 for the current draft-only diff;
  ADR 0017 is not edited yet. Counting the recorded human answers separately
  confirms one of the five needed for its planned edit, so phase 4 remains
  blocked on phase 1a.
- `python3 scripts/check_criterion_ledger.py` through the same interpreter:
  exit 0, including the new plan's not-yet-written test entries.
- Frontmatter parsed with `plans_registry._frontmatter`: both new artifacts
  have the required nonempty fields and remain draft/unimplemented; the
  spec retains `bounded` and claims ADR 0017; the plan opens with its card,
  has one ledger and an empty time section. No design file was created.
- `git diff --check`: exit 0. The complete registry check was not run:
  its tracker renderer can read the main checkout outside this task's read
  boundary. The absent change-artifact validator was not run. Full
  `make verify`, derived-file refresh and the commit belong to the runner.


## Redraft gap checks — 2026-10-16

Checked at `a2a58e82404634dd9fddbd54e99208ef45fcaf18`, before implementation:

- Five answered human records now stand in `decisions.md`. The earlier
  interview debt is discharged: `_counted(_parse_records(...)[0])` returns
  5 and the change-specific interview check exits 0. The gate must still
  run with the planned ADR edit present. The new answers require explicit
  orchestrator authorisation, review of every guard test, repair-only scope
  and retained planting branches guarded by verification.
- `phase_prompt` appends the shared rows-only `ANSWER_FORMAT` after the
  phase-6 prompt. Changing only `prompts/06-review.md` would therefore leave
  conflicting instructions. A phase-6-specific allowance for guard
  evidence lines is needed in `scripts/stage2.py`; `parse_rows`,
  `answer_parts` and `answer_block` already retain non-row text verbatim
  under `NOT_ROWS_NOTE`. No new findings-table schema is needed. The
  pre-verdict review must identify tests from their code without reading
  the private loop rows (`review`, `prompts/06-review.md`).
- Both local verification and generated CI consume `decisions/gates.yaml`;
  `scripts/verify_all.sh` runs blocking local commands and
  `scripts/ci_gates.py --generate-ci` emits the hosted workflow. A new
  blocking gate with placement `both` needs no Makefile or runner change.
  The generated workflow is `.github/workflows/ci.yml`, and generation
  prints to stdout. `tests/test_ci.py` requires mutation evidence for a
  new gate, including a recognised seeded-red test name.
- No phase-2a rows stand in the existing `findings.md`; its two audit lines
  are preserved. No design is due for `bounded`, and no new ADR is due.
- The change-artifact validator and plan template are still absent.
  Full registry/verification checks are left to the orchestrator because
  their tracker render can resolve to the main checkout outside this
  task's read boundary. Live PR state and parallel-session state were not
  read; this runner task makes no tracker write or git mutation.

Draft validation on 2026-10-16: the interview check and criterion ledger
exit 0, required frontmatter parses with nonempty fields, and
`git diff --check` exits 0. These validate the draft, not implementation.

## Current draft gap checks — 2026-10-29

Read at `9987eaca` in the dedicated `guard-test-redraft` worktree:

- `fixed_test_proof` already uses the attempt's tree, a private absolute
  probe path, invocation-bound records, tool checks and tree/ref snapshots.
  Its environment is built through `runner_env(foreign_env(...))`; a guard
  mode can reuse this execution boundary with an explicitly supplied switch
  and the existing red classifier, leaving the default clean mode intact.
- The current phase-6 `review` rejects a no-row answer unless it is exactly
  `No finding.`. Merely adding evidence prose to the prompt would therefore
  fail on a clean verdict, despite `answer_parts` retaining non-row text.
  Both the phase-specific answer instruction and verdict validation need
  the narrow evidence-line allowance; evidence alone must not become a verdict.
- `RUNNER_HELD` and `_held_prefixes` prohibit implementation attempts from
  committing prompts, templates, generated CI, the gate definitions and
  accepted ADR files. The plan assigns those coordinated changes outside
  the model attempt, with the gate definition remaining maintainer-owned;
  it does not propose weakening checkpoint protection.
- The highest existing ADR is 0022. The feature draft proposes a single new
  numbered addendum, 0023, under the current draft-output rule; it leaves
  accepted ADR 0017 untouched and records no formal feature ADR answer.
- `templates/plan.md` and `scripts/validate_change_artefacts.py` are still
  absent. Invoking the latter exits 2 (missing file), not green. The full
  registry check was not run because its live tracker renderer can resolve
  outside this task's read boundary; live PR and other-session state were
  not read. No tracker state or git state was changed.

Draft-only checks on 2026-10-29: the change-specific interview check exits 0;
the criterion ledger exits 0; research handoff reports the legacy/no-v2
exemption and exits 0. The four new documents have valid YAML headers,
the feature proposal and plan card parse, all twelve criteria have refuting
cases and basis lines, and the plan's time section is empty. Full
`make verify`, registry/index regeneration and the commit belong to the runner.
