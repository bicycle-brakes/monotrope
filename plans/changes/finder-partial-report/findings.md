---
title: "Findings — finder-partial-report"
category: findings
status: draft
implementation_status: none
date: 2026-11-19
created: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-yd8w
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — finder-partial-report

Stage-2 call, 2026-11-19: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1115 files, 4750 commits, 12 rules.

Stage-2 call, 2026-11-19: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1118 files, 4751 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | criterion 1 (and criterion 4 "their validation errors") | [AMBIGUITY] *Two readings of "the exact validation error".* `validate_locator_report` raises on the first failing entry, and its message names only the kind of fault, not the entry (for example "locator needs a path and exact symbol/section"). `stage_finders` currently throws that message away and keeps the generic "the finder answer is not the four-list locator object". Reading A: the correction request quotes the first `ResearchMapError` message word for word. In run 2277a0ed the seat would then hear one sentence about one unnamed entry out of 36. Reading B: the validator is extended to collect every failing entry with its own error, which criterion 4 already needs, and the request lists all of them. The two readings give different prompts. The same request passes criterion 1's refutation ("missing or changing the validator error") under A and fails it under B, so until the error's form is fixed the criterion cannot be checked. | Opus | in spec | — |
| S-2 | MAJOR | SPEC | base | criterion 7; Open decisions [DETAIL] 2; decisions.md Q-1 | [AMBIGUITY] *What happens when the correction cannot be used.* Q-1's answer says: "if its second answer still fails, the runner keeps the valid locator entries … and the run continues", under the maintainer's rule that rules must reduce aborts. Reading A (criterion 7, settled by the author in a [DETAIL]): an unreadable correction, or a correction call that fails or times out, stops the run. This holds even when the first answer was a readable four-list report; the 66 valid entries of run 2277a0ed would be lost if the correction timed out. Reading B: the run falls back to the valid entries of the readable first answer and continues. Criterion 7 cites Q-1 as its basis, but Q-1 does not make this choice. The two readings give opposite run outcomes for the same input. Security refusals with exit 2 are outside this question. | Opus | in spec | — |
| S-3 | BLOCKER | SPEC | base | criterion 1; Non-goals "an ADR"; Definition of Done "no ADR … changes"; docs/adr/0020-phase-1-research-swarm.md point 9 | *What is missing — a conflict with an accepted ADR.* ADR 0020 point 9 (amended 2026-11-10) allows exactly one correction, for a topic report, and then says: "No other retry is allowed and the time limits stay as they are". It caps a run at `72 + 6N` calls, and `manifest_record` publishes that cap as `invocation_ceiling` (`scripts/stage2_research_run.py:1701`). A finder correction is such an "other retry", and three finder corrections raise the worst case to `75 + 6N`. The spec forbids changing the ADR and says nothing about the cap. The builder therefore has to choose alone between a published cap the run can exceed and a new value (and a new `correction_calls` meaning) that contradicts the ADR. | Opus | in spec | — |
| S-4 | MAJOR | SPEC | base | criterion 1 "at most one"; criterion 7 | *What is missing — the time allowance and the case of zero corrections.* A topic correction runs only on the seat's remaining original topic allowance and is withheld once that is spent (`correction_entry`, `remaining_topic_allowance`). The spec does not say which allowance a finder correction runs on: what is left of the `finders` role allowance, a fresh `finders` allowance, or something else. ADR 0020 keeps the time limits unchanged. The spec also does not say what follows when no correction can start because the allowance is spent or the run deadline or judge reserve has been reached. "At most one" allows zero, and no criterion covers that case: stop with the existing incomplete outcome, or keep the valid entries of the first answer. | Opus | in spec | — |
| S-5 | MAJOR | SPEC | base | criterion 4 "published run record … as a gap" | [AMBIGUITY] *Where the dropped entries are recorded, which decides which models see them.* Reading A: they go into the map record's `gaps`. `Run` copies `entries`, `scope`, `gaps` and `not_read` into every topic packet (`scripts/stage2_research_run.py:578`), and the judge packet also receives `map_record`, so topic seats and the judge would see the dropped finder entries. Reading B: they go only into the run's bookkeeping (a manifest slot, an audit line or a `partial` fence), and no model sees them. Reading C: a new fence kind. `check_research_handoff.py` turns any kind outside `KINDS` into `CannotMeasure` (line 235), and the Definition of Done does not let that file change. The three readings produce different published blocks and different topic prompts. | Opus | in spec | — |
| S-6 | MAJOR | SPEC | base | criterion 3 "otherwise readable four-list report" vs criterion 7 "cannot be read as the four locator lists" | *What is missing — which faults drop one entry and which stop the run.* The validator rejects many shapes, and the spec names only one of them (a whole-file locator without a reference). The builder must decide each of the following alone. A category the model itself sent as `[]` was not "emptied by filtering", so the [DETAIL] does not cover it: stop under criterion 7, or add a `not_read` marker? A category value that is not a list. An entry that is not an object, or has extra or missing fields. A locator with a blank `reason`. A `not_read` marker with a blank reason. A duplicate key inside a single entry object: the current `_json_object` hook fails the whole `json.loads`, so one bad entry makes the report "unreadable", and the run stops instead of dropping one entry. The same answer can therefore pass criterion 3 or criterion 7, depending on this unwritten boundary. | Opus | in spec | — |
| S-7 | MINOR | SPEC | base | Open decisions [DETAIL] 2 (the `not_read` marker for an emptied category) | *What is missing — the text of the marker the runner adds.* The added `{"not_read": <reason>}` becomes a `(finder, reason)` origin in the exact union, so the merge model must reproduce that reason exactly. It also reaches the map's `not_read` list and through it every topic packet. The spec does not give the reason text, does not say whether the text names the dropped entries or their count, and does not say whether the merge prompt shows it as data from the runner or from the seat. All of this is left to the builder. | Opus | in spec | — |
| S-8 | MAJOR | SPEC | base | criteria 2–4; resume (ADR 0020 point 9, `stored_correction_final`) | *What is missing — the recorded outcome of a filtered correction, and what happens on resume.* No criterion says whether a correction with dropped entries is stored and published as `ok`, `invalid-report` or a new outcome. As `ok`, `compose` publishes no `partial` fence for it, and the manifest shows a plain success. As `invalid-report`, `require_ok` and the store's reuse rule (it reuses only `ok`, `stage2_research_store.py:511`) treat it as a failure, and `compose` publishes the whole raw answer, dropped entries included, as a `partial` fence. That bears directly on criterion 4's refutation "presents it as accepted evidence". Topic corrections have a defined adoption rule on resume (`stored_correction_final`). For finder corrections the spec does not say whether a resumed run adopts the stored first attempt and its correction, or launches both again. | Opus | in spec | — |

Stage-2 call, 2026-11-19: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1118 files, 4754 commits, 12 rules.

Stage-2 call, 2026-11-19: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1118 files, 4755 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-9 | MAJOR | SPEC | base | criterion 1; criteria 12–13; scripts/stage2_research_run.py:841 (`claude_command`), `payload_text` | *What is missing: how the answer of a schema-enforced Claude finder call is read and classified.* `claude_command` launches every Claude seat with `--output-format text`, and the finder answer is whatever `payload_text` finds in stdout. The repository's own research names the schema path as `claude -p --output-format json --json-schema`, with the answer in the result's `structured_output` field (docs/research/2026-09-26-agent-sdk-and-formal-models.md:68, :304). The spec leaves four things open. Does the finder call change its output format? Where does the runner read the answer: `structured_output`, the result text, or raw stdout? What does the stored `stdout` hold, and with it the published partial fence: the bare answer, or the whole JSON envelope with session id and cost? When Claude Code ends without a schema-conforming answer, which outcome does the call get: a failed call under criterion 13, or an invalid report under criterion 12? Each choice gives different stored records, fences and run outcomes. Criterion 1's refutation checks only that the call carries the schema. It stays green even if every Claude finder answer then becomes unreadable and the run stops. | Opus | in spec | — |
| S-10 | MINOR | SPEC | base | criterion 5 "empty required value"; criterion 3; scripts/stage2_research_map.py:115, :118 | [AMBIGUITY] *Whether a blank `path` or `reference` counts as an empty required value.* Today `_entries` rejects a `reason` or `not_read` that is blank after trimming. It accepts a `path` or `reference` made of spaces; only `""` fails. Reading A: "empty" keeps today's meaning for each field. Then `{"path": " ", "reference": "x", "reason": "y"}` is retained, reaches merge and is marked unresolved there. Reading B: "empty" means blank for every required value. Then that entry is dropped and published as a filtered gap. The same answer gives different retained reports and different gaps. Criterion 3 hands this rule to the schema, but the spec does not say which rule the schema states. | Opus | in spec | — |
| S-11 | MINOR | SPEC | base | criterion 7; criterion 9; scripts/stage2_research_run.py:1833–1835 (`compose`) | [AMBIGUITY] *What the partial fence holds for a filtered record.* `compose` publishes a `partial` fence only for a record that is not `ok` (or not yet stored). That fence holds `slot_id`, `outcome`, `error`, `stdout`, `stderr` and `receipts`. Under criterion 9 a filtered record is `ok`. Reading A: today's fence shape plus the `filtered` list. The fence then says `outcome: ok` and republishes the whole raw answer in `stdout`. The retained entries appear a second time outside the map, and every dropped entry appears twice. Reading B: a fence that holds only the seat and its `filtered` list, without the raw answer. Criterion 7's refutation ("represents it as retained evidence") does not separate the two, and they publish different bytes in research.md. | Opus | in spec | — |
| S-12 | MINOR | SPEC | base | criterion 2; scripts/stage2_research_run.py:1267–1270 (`stage_finders`, `finder_prompt`); prompts/research-swarm/finder.md | [AMBIGUITY] *Whether the schema text goes into the shared finder prompt or only into the Pi prompts.* `stage_finders` builds one prompt for all three seats, and it begins with finder.md, which states the format in prose. Reading A: the schema joins the shared prompt. Claude seats then get it twice (prompt and flag), and all three seats keep one prompt hash. Reading B: only Pi seats' prompts carry the schema. The finder prompts and their `prompt_sha256` then differ by launcher, and the Claude prompt stays unchanged. Criterion 2 passes under both readings. Neither reading says whether finder.md's prose format stays beside the schema, although Q-3 says the format "exists once as a JSON Schema". | Opus | in spec | — |
| S-13 | MINOR | SPEC | base | criterion 3; criterion 7; Definition of Done "the finder map and runner and their tests"; pyproject.toml dependencies | *What is missing: where the schema lives and what interprets it in Python.* Criterion 3 requires the validator to take its locator rules from the schema the calls receive. Criterion 7 publishes that validator's per-entry error texts. The project's dependencies include no JSON Schema validator; they are PyYAML, Jinja2 and pydantic. The builder must choose among three options: a hand-written interpreter for a subset of keywords, a new locked dependency, or a pydantic model that generates the schema. Each gives different published error texts and allows different schema keywords. The spec also does not say where the schema is kept: a constant in scripts/stage2_research_map.py, or a file beside the prompts. The Definition of Done names only the finder map, the runner and their tests as files that change. | Opus | in spec | — |

Stage-2 call, 2026-11-19: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1118 files, 4756 commits, 12 rules.

Stage-2 call, 2026-11-19: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1118 files, 4757 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-14 | MAJOR | SPEC | base | criteria 14–16; Open decisions [DETAIL] 3; decisions.md S-9, S-11; scripts/stage2_research_run.py:694 (`on_terminal`), :1833–1837 (`compose`) | *What is missing: what a Claude finder record stores and publishes when the call yields no `structured_output`.* Under `--output-format json`, stdout is the JSON envelope, which holds the session id and cost. Criterion 14 removes the envelope only from a successful call. Under criterion 15 the record becomes `invalid-report`; under criterion 16 it stays `failed`. Neither is `ok`, so `compose` publishes today's partial fence with the record's `stdout` (S-11: "Records that are not `ok` keep today's fence"). Reading A: `stdout` keeps the raw envelope, and research.md publishes the very session and cost data that the [DETAIL] keeps out. Reading B: the runner reduces `stdout` to the envelope's `result` text, or drops it. The fence bytes then differ, and so does the evidence of why the answer was rejected. No criterion covers the stored or published `stdout` on these two paths, so both readings pass. | Opus | in spec | — |
| S-15 | MAJOR | SPEC | base | criterion 15 vs criterion 16; decisions.md S-9 | [AMBIGUITY] *Which outcome a Claude finder call gets when it exits 0 with an error result and no `structured_output`.* This is the likely shape of the very case the change targets: Claude Code gives up because the model could not satisfy the schema. Criterion 15 ("exits successfully without `structured_output`") makes it `invalid-report`. Criterion 16 ("returns an error result") makes it `failed`. Each criterion's refutation names the other's classification, so no implementation passes both for this input. The spec also does not define "error result": `is_error: true`, a `subtype` other than `success`, or both. Reading A gives an `invalid-report` record, with the validator error in the stop message, the manifest and the fence. Reading B gives a `failed` record, which reports a format failure as a process failure. | Opus | in spec | — |
| S-16 | MINOR | SPEC | base | criterion 3 ("locator rules" vs refutation "a change to a schema rule"); criteria 5 and 12; scripts/stage2_research_map.py:17 (`CATEGORIES`), :91 (`_entries`, shared with `merged=True`) | [AMBIGUITY] *Whether the outer answer shape is also read from the schema.* To be enforced on Claude seats, the schema must describe the whole answer: the four category names, `minItems` and closed properties. Reading A: only the entry rules come from the schema, and the four categories and their non-emptiness stay in `CATEGORIES`. An edit to the schema's category names or `minItems` then changes what Claude seats must return while validation ignores it, which is criterion 3's own refutation. Reading B: the finder's outer shape also comes from the schema. The merged-map validation uses the same `CATEGORIES` and must not change (Non-goals), so finder validation and merge validation can diverge after one schema edit. Under either reading the spec does not say how a schema violation is sorted into an outer fault (criterion 12, stop) or an entry fault (criterion 5, drop), for example by whether the violation lies inside an item of a category array. | Opus | in spec | — |
| S-17 | MINOR | SPEC | base | criterion 19; decisions.md S-13; scripts/stage2_research_run.py:1272–1282 (`stage_finders`, `valid`) | *What is missing: when a bad schema is refused, and with which outcome.* Criterion 19 says only that validation refuses an unsupported keyword. It says nothing about a schema file that is missing or is not valid JSON. If the refusal happens where finder answers are validated, the three finder calls have already run. Today `valid()` turns a `ResearchMapError` into `False`, so every seat becomes `invalid-report`: a harness fault is blamed on the seats, and the reuse check then rejects their stored records. If the refusal happens while the finder prompt and the Claude argv are built, no call starts, and the run ends incomplete with a reason that names the schema. The two give different call counts, slot outcomes and published records, and criterion 19's refutation passes under both. | Opus | in spec | — |
| S-18 | MINOR | SPEC | base | criterion 19; Open decisions [DETAIL] 2 ("replacing duplicate prose"); decisions.md S-12; prompts/research-swarm/finder.md:21–25 | [AMBIGUITY] *Whether annotation keywords count as supported, which decides where the reference rules live.* A schema shown to models naturally carries `description`, `title` or `$schema`, and validation ignores these by definition. Reading A: the interpreter accepts annotations as supported. finder.md's reference rules ("exact symbol or section", "Line numbers, bare paths and prose are not references") can then move into `description` strings and be dropped from finder.md as duplicate prose. Reading B: annotations count as unsupported and are refused, so the rules must stay as prose in finder.md. The readings give different finder prompts and prompt hashes. They also flip criterion 19 for a schema containing `description`: accepted under A, refused under B. These lines guard against the incident itself (whole-file locators without an exact reference), so whether they reach the seats matters. | Opus | in spec | — |
| S-19 | MINOR | SPEC | base | criterion 5 ("invalid fields"); decisions.md S-2/S-6, S-10 | [AMBIGUITY] *What makes a field "invalid" besides its type and blankness.* Reading A: invalid means a non-string value, and the schema states only types, closed fields and non-whitespace strings. Then `{"path": "../x.py", "reference": "line 12", "reason": "y"}` is kept, reaches merge, and appears in the map as `unresolved`, where topic seats see it. Reading B: the schema also gives `path` and `reference` a form, such as the repository-relative POSIX rule of `_parts` or finder.md's "line numbers and bare paths are not references". Then the same entry is dropped into the filtered gaps and is missing from the map. The decisions list missing, empty and extra fields and non-objects, but not this. The same answer gives different retained reports and maps. | Opus | in spec | — |

Stage-2 call, 2026-11-19: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1118 files, 4758 commits, 12 rules.

Stage-2 call, 2026-11-19: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1119 files, 4771 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/finder-partial-report/plan.md` +25 -25
> - `scripts/stage2_research_map.py` +173 -3
> - `scripts/stage2_research_run.py` +123 -7
> - `tests/test_stage2_research_map.py` +156 -5
> - `tests/test_stage2_swarm.py` +429 -8
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_stage2_swarm.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> scripts/stage2_research_map.py:162:8: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>     |
> 160 |     or unsupported schema raises ``ResearchMapError`` (S-17), never a silent default.
> 161 |     """
> 162 |     if isinstance(value, (str, bytes)):
>     |        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 163 |         try:
> 164 |             value = json.loads(value)
>     |
>     = help: Convert to `X | Y`
>
> Found 1 error.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-19: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1119 files, 4782 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2_research_map.py` +1 -1
> - `tests/test_stage2_research_map.py` +1 -0
> - `tests/test_stage2_swarm.py` +6 -3
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>     
>         Pi seats read the answer as text; the Claude seat's answer rides the result
>         envelope's structured_output, so a JSON-object stdout is wrapped for it. A stdout
>         that is no JSON object (a fault answer) passes through unchanged.
>         """
>         try:
> >           body = json.loads(step.get("stdout", ""))
> E           AttributeError: 'list' object has no attribute 'get'
>
> tests/test_stage2_swarm.py:212: AttributeError
> ___________________ test_finder_filtered_record_is_stored_ok ___________________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/finder-partial-report/.venv/bin/python3
>
> sworld = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2157/pop...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2157/popen-gw2/test_finder_filtered_record_is0/home'))
>
>     def test_finder_filtered_record_is_stored_ok(sworld: SwarmWorld) -> None:
>         # Criterion 9. Planted fault: the stored outcome is not ok or the filtered details are wrong.
> >       sworld.complete(finder=[{"stdout": partial_finder_report()}], judge=[{"exit": 1}])
>
> tests/test_stage2_swarm.py:4456: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2_swarm.py:518: in complete
>     steps.update(finder_steps(overrides.pop("finder")))
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> step = [{'stdout': '{"code": [{"path": "src/app.py", "reference": "value", "reason": "holds the value"}, {"path": "src/gone.p...les"}], "tests": [{"not_read": "the fixture has no tests"}], "neighbours": [{"not_read": "no neighbour was found"}]}'}]
>
>     def finder_steps(step: dict) -> dict:
>         """One scenario step for all three finder seats.
>     
>         Pi seats read the answer as text; the Claude seat's answer rides the result
>         envelope's structured_output, so a JSON-object stdout is wrapped for it. A stdout
>         that is no JSON object (a fault answer) passes through unchanged.
>         """
>         try:
> >           body = json.loads(step.get("stdout", ""))
> E           AttributeError: 'list' object has no attribute 'get'
>
> tests/test_stage2_swarm.py:212: AttributeError
> _______________ test_finder_filtered_record_is_reused_on_resume ________________
> [gw7] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/finder-partial-report/.venv/bin/python3
>
> sworld = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2157/pop...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2157/popen-gw7/test_finder_filtered_record_is0/home'))
>
>     def test_finder_filtered_record_is_reused_on_resume(sworld: SwarmWorld) -> None:
>         # Criterion 10. Planted fault: resume relaunches the finder, changes the retained answer or
>         # loses the gaps.
> >       sworld.complete(finder=[{"stdout": partial_finder_report()}], judge=[{"exit": 1}])
>
> tests/test_stage2_swarm.py:4470: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> tests/test_stage2_swarm.py:518: in complete
>     steps.update(finder_steps(overrides.pop("finder")))
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> step = [{'stdout': '{"code": [{"path": "src/app.py", "reference": "value", "reason": "holds the value"}, {"path": "src/gone.p...les"}], "tests": [{"not_read": "the fixture has no tests"}], "neighbours": [{"not_read": "no neighbour was found"}]}'}]
>
>     def finder_steps(step: dict) -> dict:
>         """One scenario step for all three finder seats.
>     
>         Pi seats read the answer as text; the Claude seat's answer rides the result
>         envelope's structured_output, so a JSON-object stdout is wrapped for it. A stdout
>         that is no JSON object (a fault answer) passes through unchanged.
>         """
>         try:
> >           body = json.loads(step.get("stdout", ""))
> E           AttributeError: 'list' object has no attribute 'get'
>
> tests/test_stage2_swarm.py:212: AttributeError
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_map.py::test_finder_field_form_is_resolved_at_merge
> FAILED tests/test_stage2_research_map.py::test_finder_filter_marks_emptied_category
> FAILED tests/test_stage2_swarm.py::test_finder_first_answer_filters_without_retry
> FAILED tests/test_stage2_swarm.py::test_finder_filtered_merge_preserves_exact_union
> FAILED tests/test_stage2_swarm.py::test_finder_filtered_entries_stay_out_of_map_gaps
> FAILED tests/test_stage2_swarm.py::test_finder_trio_locates_four_categories_without_judging
> FAILED tests/test_stage2_swarm.py::test_finder_filtered_gaps_are_published - ...
> FAILED tests/test_stage2_swarm.py::test_finder_filtered_record_is_stored_ok
> FAILED tests/test_stage2_swarm.py::test_finder_filtered_record_is_reused_on_resume
> 9 failed, 45 passed in 15.56s
> ```

Stage-2 call, 2026-11-19: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1119 files, 4786 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2_research_map.py` +2 -2
> - `tests/test_stage2_swarm.py` +5 -2
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: red; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_map.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); a fresh full `make verify` is still required before phase 6
> - Runner targeted checks: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ........................................................................ [  6%]
> ........................................................................ [ 13%]
> ........................................................................ [ 20%]
> ........................................................................ [ 27%]
> ........................................................................ [ 33%]
> ........................................................................ [ 40%]
> ........................................................................ [ 47%]
> ........................................................................ [ 54%]
> ........................................................................ [ 61%]
> ..................F..................................................... [ 67%]
> ........................................................................ [ 74%]
> ........................................................................ [ 81%]
> ........................................................................ [ 88%]
> ........................................................................ [ 95%]
> ...................................................                      [100%]
> =================================== FAILURES ===================================
> ________________ test_finders_use_the_repository_seat_selection ________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/finder-partial-report/.venv/bin/python3
>
> sworld = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2159/pop...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2159/popen-gw0/test_finders_use_the_repositor0/home'))
>
>     def test_finders_use_the_repository_seat_selection(sworld: SwarmWorld) -> None:
>         # Criteria 6 and 43. Planted fault: a finder runs a model other than its repository seat's selection.
>         sworld.selection = selection_for()
>         sworld.selection["seats"]["repository"][1] = {"endpoint": "opencode-go", "model": "longcat-2.0"}
>         sworld.complete()
> >       assert sworld.run() == 0
> E       AssertionError: assert 1 == 0
> E        +  where 1 = run()
> E        +    where run = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2159/pop...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2159/popen-gw0/test_finders_use_the_repositor0/home')).run
>
> tests/test_stage2_swarm.py:796: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 27 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 27 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 27 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: the research run 46b497c0c20190cce3c0b731245fc42d is incomplete: incomplete - a finder failed: finders-0-2 (invalid-report); no later stage starts.
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_finders_use_the_repository_seat_selection
> 1 failed, 1058 passed in 206.40s (0:03:26)
> ```

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1119 files, 4809 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1119 files, 4810 commits, 12 rules.

Stage-2 call, 2026-11-19: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1119 files, 4810 commits, 12 rules.

Runner restoration, 2026-11-19: repair · attempt 1 · route codex — lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged; plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged

Stage-2 call, 2026-11-19: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1119 files, 4816 commits, 12 rules.

Runner restoration, 2026-11-20: repair · attempt 1 · route codex — lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1119 files, 4834 commits, 12 rules.

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1119 files, 4834 commits, 12 rules.

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1119 files, 4834 commits, 12 rules.

Stage-2 call, 2026-11-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1119 files, 4841 commits, 12 rules.

Runner restoration, 2026-11-20: repair · attempt 1 · route codex — lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1119 files, 4865 commits, 12 rules.

Stage-2 call, 2026-11-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1119 files, 4868 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/finder-partial-report/decisions.md` +2 -1
> - `scripts/stage2_research_map.py` +9 -3
> - `scripts/stage2_research_run.py` +38 -6
> - `tests/test_stage2_research_map.py` +10 -0
> - `tests/test_stage2_swarm.py` +78 -14
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_map.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - L3-1: tests/test_stage2_swarm.py::test_finder_deep_envelope_is_invalid_without_crashing: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/finder-partial-report/stage2/attempts/finder-partial-report/attempt-1-20261120T102655717416Z-03165124.md
> ```

Stage-2 call, 2026-11-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1119 files, 4884 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/finder-partial-report/decisions.md` +1 -1
> - `scripts/stage2_research_run.py` +0 -1
> - `tests/test_stage2_swarm.py` +6 -6
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_map.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - L3-1: tests/test_stage2_swarm.py::test_finder_deep_envelope_is_invalid_without_crashing: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/finder-partial-report/stage2/attempts/finder-partial-report/attempt-2-20261120T102655717416Z-03165124.md
> ```

Stage-2 call, 2026-11-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1119 files, 4884 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/finder-partial-report/decisions.md` +1 -0
> - `tests/test_stage2_swarm.py` +7 -3
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_map.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - L3-4: tests/test_stage2_research_map.py::test_finder_filter_reports_each_invalid_entry: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/finder-partial-report/stage2/attempts/finder-partial-report/attempt-3-20261120T102655717416Z-03165124.md
> ```

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model hy3 · leak check clean over 1145 files, 4899 commits, 12 rules.

Stage-2 call, 2026-11-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1145 files, 4900 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2_research_run.py` +0 -2
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: red; test files `tests/test_pi_contract.py`, `tests/test_research_capture.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); a fresh full `make verify` is still required before phase 6
> - Runner targeted checks: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ........................................................................ [  7%]
> ........................................................................ [ 14%]
> ........................................................................ [ 22%]
> ........................................................................ [ 29%]
> ........................................................................ [ 37%]
> ........................................................................ [ 44%]
> ........................................................................ [ 51%]
> ........................................................................ [ 59%]
> ........................................................................ [ 66%]
> ........................................................................ [ 74%]
> ........................................................................ [ 81%]
> ........................................................................ [ 89%]
> .......................................................F................ [ 96%]
> ..................................                                       [100%]
> =================================== FAILURES ===================================
> __________ test_filtered_finder_output_survives_failed_terminal_write __________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/finder-partial-report/.venv/bin/python3
>
> sworld = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2602/pop...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2602/popen-gw2/test_filtered_finder_output_su0/home'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10a1c6a50>
>
>     def test_filtered_finder_output_survives_failed_terminal_write(
>         sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
>     ) -> None:
>         original = stage2_research_store.Store.write_result
>     
>         def broken(self, run_id, slot_id, record):
>             if record.get("filtered"):
>                 raise stage2_research_store.StoreWriteError("disk full")
>             return original(self, run_id, slot_id, record)
>     
>         monkeypatch.setattr(stage2_research_store.Store, "write_result", broken)
>         sworld.complete(finder=[{"stdout": partial_finder_report()}])
>         assert sworld.run() == 1
>         partial = next(p for p in partials_of(sworld.research.read_text(encoding="utf-8")) if p.get("filtered"))
> >       assert "holds the value" in partial.get("stdout", "")
> E       assert 'holds the value' in ''
> E        +  where '' = <built-in method get of dict object at 0x10a23dac0>('stdout', '')
> E        +    where <built-in method get of dict object at 0x10a23dac0> = {'filtered': [{'category': 'code', 'entry': {'path': 'src/gone.py', 'reference': 'value'}, 'errors': ["the required field 'reason' is missing"], 'index': 1}], 'outcome': 'ok', 'slot_id': 'finders-0-1'}.get
>
> tests/test_stage2_swarm.py:4768: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 27 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 27 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 27 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: the research run 489dac22ea29e819f1f527b6acca17f6 is incomplete: incomplete - the research state store failed (disk full).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_filtered_finder_output_survives_failed_terminal_write
> 1 failed, 969 passed in 377.22s (0:06:17)
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/finder-partial-report/stage2/attempts/finder-partial-report/attempt-1-20261120T133824591381Z-9246c005.md
> ```

Stage-2 call, 2026-11-20: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1145 files, 4900 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; repair the taken rows of the loop record
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> .....................................F........                           [100%]
> =================================== FAILURES ===================================
> __________ test_filtered_finder_output_survives_failed_terminal_write __________
> [gw11] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/finder-partial-report/.venv/bin/python3
>
> sworld = SwarmWorld(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2605/pop...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-2605/popen-gw11/test_filtered_finder_output_su0/home'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10775ecc0>
>
>     def test_filtered_finder_output_survives_failed_terminal_write(
>         sworld: SwarmWorld, monkeypatch: pytest.MonkeyPatch
>     ) -> None:
>         original = stage2_research_store.Store.write_result
>     
>         def broken(self, run_id, slot_id, record):
>             if record.get("filtered"):
>                 raise stage2_research_store.StoreWriteError("disk full")
>             return original(self, run_id, slot_id, record)
>     
>         monkeypatch.setattr(stage2_research_store.Store, "write_result", broken)
>         sworld.complete(finder=[{"stdout": partial_finder_report()}])
>         assert sworld.run() == 1
>         partial = next(p for p in partials_of(sworld.research.read_text(encoding="utf-8")) if p.get("filtered"))
> >       assert "holds the value" in partial.get("stdout", "")
> E       assert 'holds the value' in ''
> E        +  where '' = <built-in method get of dict object at 0x10778ad00>('stdout', '')
> E        +    where <built-in method get of dict object at 0x10778ad00> = {'filtered': [{'category': 'code', 'entry': {'path': 'src/gone.py', 'reference': 'value'}, 'errors': ["the required field 'reason' is missing"], 'index': 1}], 'outcome': 'ok', 'slot_id': 'finders-0-1'}.get
>
> tests/test_stage2_swarm.py:4768: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 27 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 27 files, 1 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 27 files, 1 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: the research run 755a3b5640bf39ab3de4a82c795c5e3f is incomplete: incomplete - the research state store failed (disk full).
> =========================== short test summary info ============================
> FAILED tests/test_stage2_swarm.py::test_filtered_finder_output_survives_failed_terminal_write
> 1 failed, 45 passed in 20.90s
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/finder-partial-report/stage2/attempts/finder-partial-report/attempt-2-20261120T133824591381Z-9246c005.md
> ```

Stage-2 call, 2026-11-20: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1145 files, 4900 commits, 12 rules.

Runner restoration, 2026-11-20: repair · attempt 3 · route stage-1 — lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1145 files, 4901 commits, 12 rules.

Loop attempt: 2026-11-20 — no round was written; the review-loop calls above consumed no stage; audit calls: 1

Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1145 files, 4911 commits, 12 rules.

Stage-2 call, 2026-11-20: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1145 files, 4924 commits, 12 rules.

Runner restoration, 2026-11-20: repair · attempt 1 · route codex — lifecycle fields: plans/changes/finder-partial-report/plan.md, plans/changes/finder-partial-report/spec.md — unchanged

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1145 files, 4946 commits, 12 rules.

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1150 files, 4954 commits, 12 rules.

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1150 files, 4957 commits, 12 rules.

Stage-2 call, 2026-11-20: review-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1150 files, 4961 commits, 12 rules.
