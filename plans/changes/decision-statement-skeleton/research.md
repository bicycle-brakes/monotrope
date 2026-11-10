---
title: "Research — decision-statement-skeleton"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-nr6h
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3-flash, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
neighbours:
  - plans/changes/archive/2026-11-06-interview-context/spec.md
---

# decision statement skeleton — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

## Intent of the change — from the bead, 2026-11-10

Written by the orchestrator before the first exploration, because an
explorer cannot read the tracker (bead coding-harness-nr6h).

Class: bounded.

A decision record in `decisions.md` needs a decision statement: one sentence
that begins "In the context of", names what was decided and what is accepted
with it, and ends with its date. A draft may not edit `decisions.md`, and the
document checks refuse a record without the statement. In the night of
2026-11-10 two changes (verify-slots, review-fewer-rounds) lost all three
draft attempts each on the missing statement alone.

Wanted: no draft starts without the statements. The skeleton that
`make change` writes and the interview prompt should lead to a statement for
every answered record, and its accepting clause — the downside the
maintainer accepts — is asked from the maintainer, not invented.

To explore: which gate requires the statement and what exactly it checks;
what `scripts/new_change.py` writes today; what the interview prompt
(`prompts/`) says about recording an answer; whether the `draft` verb could
refuse early, before a model call, when a statement is missing; which tests
pin these today.

Stage-2 call, 2026-11-10: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 993 files, 3829 commits, 12 rules.

## Runner exploration — 2026-11-10

Research complete. Here is the report, ready to append to `plans/changes/decision-statement-skeleton/research.md`.

---

## What exists today

**The gate that demands the statement.** The gate is `question-context` (`scripts/check_question_context.py`, constant `GATE`, `scripts/check_question_context.py:56`), registered in `decisions/gates.yaml` with `command: python3 scripts/check_question_context.py`, `job: verify`, `enforcement: block`, `placement: both`, `subsets: [docs]` (`decisions/gates.yaml`, entry `question-context`). Its adoption day is `2026-10-15` (`decisions/adoption.yaml`, key `question-context`), and that file's header says moving a day is a decision pull request. `docs/WORKFLOW.md` describes it in the enforcement table (row "Question context") and in the phase‑1a section around the `context` field.

**What the gate checks, exactly.** For every block `## Q-<id> · <title>` whose last outside‑fence `status:` reads `answered` (`_records`, `_status`, `scripts/check_question_context.py`), in every live and archived change folder (`_decision_files`), the gate reads the recording day from the decision statement (`_recording_day`). The statement requirements, all in `scripts/check_question_context.py`:

- a top‑level line (no leading whitespace) matching `_STATEMENT`, `^In the context of(?:\s|$)`; indented following lines are wrapped continuation;
- exactly one such statement per record — more than one is "ambiguous";
- the joined statement ends with exactly one em‑dash date `— YYYY-MM-DD`, optionally followed by one closing parenthetical remark (`_DATE_SUFFIX`); a date written without the dash ("Recorded 2026‑10‑14.") does not count; an impossible calendar date (`2026‑13‑45`) is invalid;
- a fence, a field line (`_FIELD`), a heading, or a second statement ends the paragraph.

Any of these failing raises `CannotMeasure`, and that is the key mechanic: **the recording day that decides exemption is itself read from the statement**, so a record without a readable statement is "unreadable evidence" — the whole gate exits 3 ("NOT MEASURED"), and exit 3 is a failure, "not measured, never an exemption" (module docstring, `main`). This applies to every answered record regardless of adoption day. Only records with a readable day on/after `2026‑10‑15` are then context‑checked (`_context_findings`: one non‑blank text `context` value, presence only). Exit codes: 0 ok, 1 findings, 3 could not measure.

**Where the statement is supposed to come from.** The interview record template in `prompts/01a-interview.md` ("What you write") shows the statement as the last element of a record: `In the context of <situation>, facing <constraint>, we decided <option>, to achieve <goal>, accepting <consequence>. — <date>`. The prompt says the date after the statement is the day the answer was recorded. ADR 0018 (`docs/adr/0018-every-question-carries-its-context.md`) does not mention the decision statement at all (grep: no match) — the statement requirement exists only through the gate's date extraction, not through an ADR. The five‑part question protocol (Topic / Intention / Today / Repository change / Architecture change) has no part that asks for the accepting clause; `accepting <consequence>` exists only in the statement template.

**What `make change` writes today.** `Makefile` maps `change:` to `python3 scripts/new_change.py "$$NAME" --bead "$$BEAD"`. `scripts/new_change.py` creates exactly one file, `plans/changes/<name>/research.md` (`research_path = ziel / "research.md"`), from `BODY_TEMPLATE` plus frontmatter. It does not create `decisions.md`, any record skeleton, or any statement template — that is "not there", deliberately: the script's docstring says the phase‑1 outline is not copied. `templates/` holds no `decisions.md` template (glob: adr, design, spec, findings, plan, handover and settings templates only). The script validates name, bead status, worktree state, repeated creation, and runs `plans_registry.check()` before and after, rolling back only BLOCKs the call itself added.

**Where the draft verb finds a missing statement — only after a model call.** `scripts/stage2.py`, `draft()`: `preflight(root, change, CODEX, bead_file="research.md", required=("decisions.md",))` checks only that `decisions.md` is readable (`preflight` reads each required file, no content inspection). After each attempt, `verify_draft` runs the document job `DOCS_VERIFY = ["bash", "scripts/verify_all.sh", "--job", "docs"]`, which selects gates from `decisions/gates.yaml` through `ci_gates.py --commands --job docs` — this is where `question-context` runs. A document check that cannot start or exits non‑zero becomes an attempt problem, the attempt fails, and the chain moves to the next route: codex → codex‑repair → glm. So a missing statement burns one model call per route. `DRAFT_RULES` forbid the drafter from editing `decisions.md` ("the runner puts back every changed path … except the one new ADR draft, and the change's `decisions.md`"), so the drafter cannot repair the statement itself; the only red gate a draft tolerates is its own missing ADR answer (`answer_is_owed`), which a missing statement is not.

**The failure history — four changes so far.** `docs/journal/handover/2026-11-10-night-run-interrupted.md`: verify‑slots (bead coding‑harness‑u1ha) — all three draft attempts failed only on missing decision statements; review‑fewer‑rounds (bead coding‑harness‑3rtn) — all three draft attempts failed the document job on one gate only, `decisions.md` carrying no decision statement for its twelve questions; the recorded lesson: a draft may not edit `decisions.md`, and a change opened without the statement fails every draft attempt on that alone; and "`make change` or the interview prompt should produce it". Earlier instances in findings files: `plans/changes/archive/2026-11-06-restore-symlink-parent/findings.md` (Q‑2 — "the record states no decision statement beginning `In the context of`", exit 3) and `plans/changes/go-wire-apis/findings.md` (Q‑2 — "no `— YYYY-MM-DD` date ends the decision statement", three blocked runs).

**Tests that pin these today.** `tests/test_check_question_context.py` is the gate's counterexample matrix; its unmeasured‑evidence parametrization pins `no-statement` (a record reading "We decided. — 2026‑10‑14" must exit 3), `no-dash`, `impossible-date`, `ambiguous-date`, `no-adoption-day`, `unreadable-file`, each asserting exit 3 and "NOT MEASURED". Two tests read the interview prompt itself: `test_question_forms_put_context_before_options_and_question_last` (Topic/Intention/Architecture‑change wording) and `test_interview_record_has_a_dedicated_context_field` (`"context: |"` present) — neither pins the statement template line. `tests/test_check_interview_minimums.py` pins the prompt's record fields (`answered_by`, `status: skipped`, `## SKIP · interview`) and `check_interview_minimums.py`'s naming in the spec prompt; the counting gate reads no statement (grep: no match in that script). `tests/test_workflow_entry.py` pins `new_change.py` (folder and index creation, closed‑bead refusal, detached‑HEAD refusal, missing guard); no test pins the generated body beyond what the script itself carries.

## Where it lives

Gate: `scripts/check_question_context.py`. Registration: `decisions/gates.yaml`, adoption day: `decisions/adoption.yaml` (read through `scripts/adoption.py`, `GATE` key). Statement template: `prompts/01a-interview.md` "What you write". Scaffolder: `scripts/new_change.py` via `Makefile` `change:`. Draft preflight: `scripts/stage2.py` `preflight` / `draft`; document job: `DOCS_VERIFY` in `scripts/stage2.py` → `scripts/verify_all.sh --job docs` → `scripts/ci_gates.py`. Docs descriptions: `docs/WORKFLOW.md` (enforcement table row, phase‑1a section). Failure evidence: the two handover/findings files named above. CI generation from the one gate list: `scripts/ci_gates.py --generate-ci` (the gate needs no separate CI edit).

## What is unclear

- The exact offending record text of the two night changes: the parked folders `verify-slots` and `review-fewer-rounds` are not in this worktree (glob: no such folder under `plans/changes/`; the handover says the artefacts sit on their parked commits, e.g. `2098684d` for review‑fewer‑rounds). Not read — open, only readable from those commits.
- Which session wrote those `decisions.md` records without statements: the handover records the answers as the maintainer's of 2026‑11‑09 and says the statements were added afterwards, restating the answers; the authoring path is not recorded.
- A living spec for the interview/decision‑record area: not there — `plans/specs/` holds only `implementation-verification/spec.md` and `.gitkeep`.
- Whether the interview prompt should require the accepting clause to be asked as part of the question (today it is only a template slot) — a question for the interview, not a fact this phase can settle.

## Which files a change would have to touch

`scripts/new_change.py` (body template, and the write/rollback step if more than `research.md` were scaffolded) · `prompts/01a-interview.md` (record template; the question protocol if the accepting clause becomes an asked part) · the prompt‑pinning tests `tests/test_check_question_context.py` and `tests/test_check_interview_minimums.py`, which read the prompt at test time and must stay green · `scripts/stage2.py` `preflight`/`draft` if the draft verb is to refuse before a model call (the refusal point that "precedes everything else"; it must not collide with the tolerated missing‑ADR‑answer case, `answer_is_owed`) · `docs/WORKFLOW.md` if the duty gains a written sentence. `decisions/gates.yaml` and `decisions/adoption.yaml` are not touched — the gate exists and is already wired into the docs job.

## Neighbours (for the header)

- `plans/changes/archive/2026-11-06-interview-context/spec.md` — the accepted, done change (bead coding‑harness‑zs7, ADR 0018) that introduced the `context` field and this gate's record form.
- `plans/changes/go-wire-apis/` — live change; its `findings.md` carries three question‑context NOT‑MEASURED blocks (statement without the em‑dash date).
- `plans/changes/archive/2026-11-06-restore-symlink-parent/` — archived; its `findings.md` carries the earlier "no decision statement" block.
