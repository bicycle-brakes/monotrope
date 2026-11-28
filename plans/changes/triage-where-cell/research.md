---
title: "Research — triage-where-cell"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-3ha6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# triage where cell — Research

## Topic (bead coding-harness-3ha6)

Class: bounded. Follow-up of change triage-verb (bead coding-harness-o2s1): review-loop round 4 rows L4-1 (MAJOR: a Where location without a slash — bare file name or file::test — is classified like any path, so a test-only row is still refused), L4-2 and L4-5 (read Where through ROW_COLUMNS; a slash token counts only when it names a tracked path), L4-3, L4-4 and L4-6 (prompt and help wording; prompts/04b-review-loop.md is a held path the orchestrator edits). The round-4 repair failed because the model edited the held prompt; appetite spent. Maintainer 2026-11-09: phase 6 now, round-4 rows as follow-up bead.

Further evidence (orchestrator, 2026-11-28): two review-loop rows of 2026-11-27/28 could not be triaged or repaired without a hand edit of the reviewer's record: `enqueue-pr-rulesets` L1-1 has `Where` = `scripts/enqueue_pr.py:runner_state_line` (a symbol after the colon, refused as 'unrecognised Where location') and Origin `Implementation`; `bead-topic-in-research` L1-1 has Origin `implementation` (repair refuses: 'selected repair rows carry an invalid Origin'). The runner then asks the orchestrator to correct the cells by hand; an unattended session's permission layer blocks that hand edit, so both lanes stop. Whether this change should also let `triage` set the Origin cell and accept a `path symbol` Where is for the spec to settle within the bead's scope.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1325 files, 6190 commits, 12 rules.

## Runner exploration — 2026-11-28

I am the phase-1 explorer, so I have not written `research.md`. The runner appends the text below. Scope: the repository as it stands, read through Read, Grep and Glob only. The loop record lives outside this worktree, so I did not read the rows themselves. What I say about them comes from the change's own `research.md` and is marked as such.

## Research — triage-where-cell

### What exists today

**Strict Where reader (classification for `triage`).** `where_locations(cell, root)` in `scripts/stage2.py` splits the cell on whitespace, commas, semicolons and escaped pipes. It strips matched wrappers (backtick, asterisk, quotes, brackets), skips external URLs, and then accepts a token when it is an exact entry of `git ls-files`, or when it is a tracked path after removing a location suffix (`:n`, `:n-n`, `#Ln`, `#Ln-Ln`). Any other token that contains a `/` or matches `\.[\w-]+` raises `Refused("unrecognised Where location …")`. The refusal text tells the reader to use an exact tracked path, or `taken — not a test — <reason>` for test-only work. A token that has neither a slash nor a dot and is not tracked is ignored silently.

**Test-only trigger.** `where_is_test_only(cell, root)` in `scripts/stage2.py` is true only when `where_locations` returns at least one location and every location is `tests` or below `tests/`. It depends on the strict reader, so a refusal there propagates before any classification.

**Triage verb.** `triage(root, change, row_status, reason)` in `scripts/stage2.py` checks the operands and the status vocabulary (`TRIAGE_STATUSES`), then, under `holding_record`, reads the row from `record_rows(strict=True)`. It refuses rows already `fixed` or carrying a `Broke a test` mark. It calls `where_is_test_only(targets[0][4])` and refuses a plain `taken` on a test-only row. It then calls `_write_triage_row`, which rewrites only the `Status` cell (column index from `ROW_COLUMNS`) and preserves all other cells and line endings. The status string comes from `triage_status`, which joins decision and escaped reason with ` — `.

**Lenient Where reader (repair scope and hand rows).** `_where_token_path`, `where_named_tokens`, `where_named_paths`, `repair_scope_locations`, `repair_scope` and `repair_hand_rows` in `scripts/stage2.py` form a second grammar. Its docstring says it refuses nothing. It normalises `./`, absolute paths inside the checkout, `..`, case, and tracked directories with a trailing slash. `where_named_tokens` describes itself as "the one grammar all its readers share", but `triage` uses `where_locations`, not this reader. So two readers of the same cell exist in the code.

**Origin validation.** `origin_refusal` and `target_origin_refusal` in `scripts/stage2.py` check `ORIGIN_VALUE` on accepted rows (`taken` or `fixed`) in the loop record and the phase-6 table, and on selected repair targets. Their diagnostics say that the orchestrator sets Origin to `base` or `fix-r<N>`. `_write_triage_row` and `triage` do not write the Origin cell. I did not search the rest of `scripts/` for another writer of that cell.

**Column definition.** `ROW_COLUMNS` = ID, Severity, Dimension, Origin, Where, Finding, Reviewer, Status, Broke a test, in `scripts/stage2.py`. `findings_reader.py` keeps its own copy, and `tests/test_findings_per_model.py` asserts the two are equal.

**Prompt and help wording.** `prompts/04b-review-loop.md` (step 1, around the `triage` command) names the triage command, says it refuses a plain `taken` on a test-only row, and gives the corrective form `taken — not a test — <reason>`. The argparse help for `row_status` in `scripts/stage2.py` (`main`) says the same. The change's `decisions.md` records that `prompts/04b-review-loop.md` is a held path edited by the orchestrator, not by the model.

**Existing tests.** `tests/test_stage2.py` has a triage block from about `test_triage_refuses_unrecognised_path_spellings_without_prefix_matching` to `test_triage_refuses_a_quoted_guard_reason`, plus `test_triage_help_and_instructions_match_the_cli_and_proof_ownership`. Cases I read cover:
- unrecognised spellings such as `tests/test_stage2.py:12#anchor`, which must refuse;
- tracked root files with and without a suffix (`Makefile:12`, `LICENSE`, `.gitignore:2`, a Markdown link to `Makefile#L12`), which must be accepted;
- external URLs, which are ignored;
- the suffix forms `:n`, `:n-n`, `:n–n`, `#Ln`, `#Ln-Ln`, `#Ln–Ln`, in bare, Markdown and quoted layouts;
- refusal of malformed table rows;
- the help text matching the CLI.

I did not read the full parametrize list at the start of the first case (around the lines before `test_triage_refuses_unrecognised_path_spellings_without_prefix_matching`), so I cannot say whether a bare untracked file name without a slash is among the refused spellings.

**Enqueue row, as stated by the change.** `research.md` says `enqueue-pr-rulesets` L1-1 has Where `scripts/enqueue_pr.py:runner_state_line` and Origin `Implementation`. `scripts/enqueue_pr.py` exists (Glob). A grep for `runner_state_line` in it returns nothing. Under `where_locations`, that token is not tracked, and the suffix regex does not strip a `:symbol`, so the token contains a slash and is refused. The reading is consistent with the code. I did not run it.

### Where it lives

- `scripts/stage2.py`: `where_locations`, `where_is_test_only`, `triage`, `triage_status`, `_write_triage_row`, `origin_refusal`, `target_origin_refusal`, `where_named_tokens`, `_where_token_path`, `repair_scope_locations`, `repair_hand_rows`, `ROW_COLUMNS`, `TRIAGE_STATUSES`, the argparse help for `row_status`.
- `scripts/findings_reader.py`: its own `ROW_COLUMNS`.
- `prompts/04b-review-loop.md`: the triage step and the held-path wording.
- `tests/test_stage2.py`: the triage tests named above.
- `tests/test_findings_per_model.py`: the equality assertion on `ROW_COLUMNS`.

### What is unclear

1. **The exact wording of L4-3, L4-4 and L4-6** is in the loop record, which lies outside this worktree. I could not read it. The change's `research.md` names them only as "prompt and help wording".
2. **Whether a bare file name without a slash, such as `test_stage2.py`, is currently refused.** The code path suggests yes, because the token has a dot and is not tracked. I have not confirmed it against the test list.
3. **Which of the two Where readers `triage` should use.** The docstrings disagree on whether one grammar is shared.
4. **Who writes Origin today.** No `triage` path writes it. The diagnostics assign it to the orchestrator. Whether any other command or a manual edit is the real writer is not established by my reading.
5. **What `_held_prefixes(root)` contains.** It decides which paths a hand edit may reach. I did not read it, so I cannot say whether `prompts/` is in the held list.
6. **Whether the scope of this change includes the Origin cell and a `path symbol` Where.** The change's `research.md` leaves that to the spec. This research records only that both are currently refused or unset.

### Files a change would have to touch (named by the code, not a design)

- `scripts/stage2.py`: `where_locations` and its suffix handling; `where_is_test_only`; `triage` and `_write_triage_row` if triage is to set anything beyond Status; the `row_status` help text.
- `prompts/04b-review-loop.md`: triage step wording (held; the orchestrator edits it).
- `tests/test_stage2.py`: the triage tests, and any new cases for bare names and symbol suffixes.
- `scripts/findings_reader.py` only if `ROW_COLUMNS` changes, since its copy is asserted equal in `tests/test_findings_per_model.py`.
