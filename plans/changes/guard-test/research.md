---
title: "Research — guard-test"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-0ho
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair, red-first]
---

# A guard-test mark for test-only repairs — Research

Phase 1 for bead coding-harness-0ho, seeded by the orchestrating session on
2026-10-15 against `origin/main`.

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
