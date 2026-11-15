---
title: "Research — swarm-report-format"
status: draft
implementation_status: none
date: 2026-11-09
last_reviewed: 2026-11-10
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-4q9y
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by:
  - {kind: llm-session, name: claude-code, model: glm-5.3-flash, version: "2026-11-09"}
  - {kind: llm-session, name: claude-code, version: "2026-11-09"}
  - {kind: llm-session, name: codex, model: gpt-6.1-sol, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# swarm report format — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md).

Stage-2 call, 2026-11-09: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 980 files, 3790 commits, 12 rules.

## Runner exploration — 2026-11-09

Die Recherche ist vollständig. Der folgende Text ist_APPEND-fertig für `plans/changes/swarm-report-format/research.md` (Englisch, da Repository-Artefakt):

---

## What exists today

**The topic names two distinct "swarm report" surfaces.** Which one the change targets is stated in the bead `coding-harness-4q9y`, whose description is not readable from the tree (the tracker is the Dolt database under `.beads/`; no rendered copy is committed, per house rule 2, and this phase has no tracker access). Both surfaces are documented below. No artifact in the tree that I read states a defect, complaint or goal about either format — "not found", not "not there".

### Surface 1 — the phase-1 research swarm record (`research-swarm/v2`)

The record is machine JSON in fenced blocks between two HTML markers, appended to `plans/changes/<name>/research.md` by `ResearchRun.compose` (`scripts/stage2_research_run.py`, `compose`, together with `publish` which appends once and stamps status). Exact shape:

- Opening marker `<!-- research-swarm/v2 (quoted) run <id> -->`, heading `## Research swarm — <date>`, a line `run <id> · class <class> · baseline HEAD <head> · input digest <digest>`; closing marker `<!-- /research-swarm/v2 (quoted) -->`; final line `run <id> status: <status>.`
- Fenced JSON blocks, each labeled `research-swarm/v2 <kind>`: `manifest` (`manifest_record`, `scripts/stage2_research_run.py` — schema, run_id, change, class, status, receipt_id, head, digest, untracked, free_selected/free_count, budget `39 + 3N`, judge_packet, selection seats, catalog, preparation, resume, given_neighbours, per-slot records), `map` (the Opus finder-merge union), `history` (topic-6 commit packet), one `report` per seat, `partial` for failed/unstored slots, `reconciliation` (judge verdict + scores), and the runner-derived `inventory`.
- The only human-readable prose in the whole record: the heading, the run line, an optional `public topic: <sentence>` line, the `### Audit` bullet list, and the status line. Everything else is sorted-key, indented JSON.

The report schema is validated by `validate_research_report` (`scripts/stage2_research_report.py`): required keys `claims`, `counter_evidence`, `not_read`, `neighbour_relation`, `questions`; topic 3 adds `class_assessment`, topic 5 adds `neighbour_relations`; at most 7 claims with local ids `C[1-7]`; questions with ids `Q[1-9][0-9]*` and classification `[DECISION]`/`[GAP]`/`[DETAIL]`; every claim needs `id/statement/kind (fact|assumption|judgement)/evidence/confidence/basis`; topic 6 adds a `volatile` bool and a `governance` proposal (`central|runtime|dated`); a report is invalid without at least one runner-backed (`valid`) evidence claim, except the empty-packet topic 5; evidence excerpts share one 4,000-character budget per claim (`_evidence`); global ids are `<run>/<topic>/<seat>/C<n>`. The finder map format is exactly four locator categories `("code", "rules", "tests", "neighbours")` with entries `{path, reference, reason}`, merged form `{path, reference, origins}`, and the merge must equal the exact finder union (`merge_research_map`, `scripts/stage2_research_map.py` — "merged map adds/drops a locator or changes finder reasons"). The judge answer schema is checked in `validate_judge` (`scripts/stage2_research_run.py`, `JUDGE_KEYS`): five list-of-strings fields, three nonempty comparison texts, `disagreements` (≥2 known claim ids + summary), and `claim_judgements` as `{claim, disposition, unique}` with dispositions `supported|refuted|off-brief|unresolved` (`research_claim_scores`, `scripts/stage2_research_judge.py`; packet schema `research-swarm/judge-packet/v2` in `_packet_text`). The obligation inventory is derived twice from the raw reports — runner and gate — by the one shared function `derive_inventory` (`scripts/research_handoff.py`): H-items with reasons `decision`/`class`/`disagreement`/`neighbour`, neighbour statuses `given|confirmed|rejected|split` under the three-counting-relations rule.

The format is load-bearing — five independent consumers parse it:

1. `check_research_handoff.py` (gate `research-handoff`): `_OPEN`/`_CLOSE`/`_FENCE_V2` regexes and the block-kind tuple `KINDS` (`scripts/check_research_handoff.py`), requires `manifest["schema"] == "research-swarm/v2"` exactly; unreadable or ambiguous evidence exits 3.
2. Publication detection in the state store: the substring `research-swarm/v2 run <id> -->` (`scripts/stage2_research_store.py`, `set_append`/read paths around the "published" checks).
3. Resume: the `BLOCK` regex strips whole envelopes from the frozen private brief (`scripts/stage2_research_run.py`, `BLOCK`).
4. Injection guard: `quote_research_records` (`scripts/stage2.py`) makes the markers and fence labels inert inside model answers (deep review RS-1-10), so an answer cannot forge or terminate a record.
5. Tests pin the exact fence names and marker lines: `tests/test_stage2_swarm.py` (map/partial/manifest/reconciliation fences), `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_store.py`, `tests/test_stage2_research_report.py`, `tests/test_research_handoff.py` (including a wrong-schema `research-swarm/v1` negative case).

The v2 contract is a decided artifact: ADR 0020 (`docs/adr/0020-phase-1-research-swarm.md`, "a fixed report/scoring contract", decision 5 "Reports hold at most seven identified claims…") and the archived spec `plans/changes/archive/2026-11-06-research-swarm/spec.md` ([DETAIL] "Version manifests research-swarm/v2", plus the handoff/derivation details); implementation decisions in the archived `design.md`/`plan.md` of the same change (persistence as fenced blocks; the plan note that the inventory was later added). `prompts/01a-interview.md` and `prompts/02-spec.md` describe the interview and spec consuming a complete v2 run; the gate's rationale in `decisions/gates.yaml` (`research-handoff`) names the fenced records.

### Surface 2 — the phase-4b review-loop answer and the loop record

The reviewer answer format is six-cell Markdown rows: `| ID | Severity | Dimension | Origin | Where | Finding |`, no header, `|` escaped as `\|`, severity as free text, and exactly `No finding.` when empty — defined in `ANSWER_FORMAT` (`scripts/stage2.py`) and repeated for the reviewer in `prompts/04b-review-loop.md` ("For the reviewer", dimensions `SPEC`/`MAINT`, severities `BLOCKER`/`MAJOR`/`MINOR`). Phase 6 replaces it with `PHASE6_ANSWER_FORMAT`, which additionally allows guard-evidence lines matching `GUARD_EVIDENCE_LINE` beside the rows. A malformed answer (no six-cell row, not exactly `No finding.`) raises `MalformedAnswer` and the member is asked once more with `FORMAT_REMINDER` (bead coding-harness-70rw); a second malformed answer fails the member (`docs/WORKFLOW.md` §4, swarm rounds).

The parser is `parse_rows` (`scripts/stage2.py`): exactly six cells are a row; a longer line whose second cell is a severity widens its last cell with escaped pipes and is noted; furniture/empty lines are dropped; anything else stays in the non-row text (`split_row`, `_furniture`, `SEVERITIES`; `answer_parts` and `NOT_ROWS_NOTE` build the findings prose). Persisted tables use `ROW_COLUMNS` (`… Reviewer`, `Status`, `Broke a test`) and `RELEASED_COLUMNS` (adds `Phase 6`), rendered by `render_table` with pipe escaping; released rows enter `findings.md` (frontmatter from `findings_header`) via `release-loop` only after the phase-6 verdict, and the phase-6 reviewer marks each row `agree`/`disagree — <reason>` (`docs/WORKFLOW.md` §4; ADR 0021). Between rounds the rows live in the loop record outside the repository: `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>@<digest>/loop.md` (`record_dir` in `scripts/stage2.py`; `docs/WORKFLOW.md` §4, "loop record"), written whole-or-not-at-all, carrying the run snapshot; a lost record refuses rather than restarts.

Adjacent by name only: `scripts/run_report.py` and the archived change `plans/changes/archive/2026-11-06-run-report/` concern the night-run report, not a swarm report; `scripts/research_capture.py` is the attended offline isolation capture (F-1) and uses `"No finding."` only as a stand-in answer.

## Where it lives

Producer and schema: `scripts/stage2_research_run.py` (`compose`, `publish`, `manifest_record`, `validate_judge`, `BLOCK`), `scripts/stage2_research_report.py` (`validate_research_report`, `_evidence`, `research_seat_id`), `scripts/stage2_research_map.py` (`validate_locator_report`, `merge_research_map`, `validate_given_neighbours`), `scripts/stage2_research_judge.py` (`_packet_text`, `research_claim_scores`, `REPORT_FLOOR_CHARACTERS`), `scripts/research_handoff.py` (`derive_inventory`, `neighbour_records`). Consumers: `scripts/check_research_handoff.py` (`KINDS`, `_OPEN`, `_CLOSE`, `_FENCE_V2`, schema check), `scripts/stage2_research_store.py` (publication substring), `scripts/stage2.py` (`quote_research_records`, `ANSWER_FORMAT`, `PHASE6_ANSWER_FORMAT`, `GUARD_EVIDENCE_LINE`, `FORMAT_REMINDER`, `MalformedAnswer`, `parse_rows`, `ROW_COLUMNS`, `RELEASED_COLUMNS`, `render_table`, `record_dir`). Prompts: `prompts/01-explore.md`, `prompts/01a-interview.md`, `prompts/02-spec.md`, `prompts/04b-review-loop.md`. Governance: `docs/adr/0020-phase-1-research-swarm.md`, `docs/adr/0021-review-swarms-until-clean.md`, `docs/WORKFLOW.md` §4, `decisions/gates.yaml` (`research-handoff`). Tests: `tests/test_stage2_swarm.py`, `tests/test_stage2_research_report.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_store.py`, `tests/test_research_handoff.py`, `tests/test_stage2.py` (row parsing), `tests/test_stage2_availability.py` and `tests/test_pi_contract.py` (`"No finding."` scripted answers).

## What is unclear about it

- **[DECISION-candidate, needs the maintainer or the bead]** Which surface `swarm-report-format` targets — the `research-swarm/v2` record, the review-loop answer/loop record, both, or something else (for example the `prepare-explore` selection report printed in the main conversation). The bead `coding-harness-4q9y` description is not readable from the tree; no tree artifact I read states the goal, and the branch name (`fix/swarm-report-format`) names no surface.
- What defect or inconvenience motivates the change is stated nowhere I read — not found in `docs/`, `prompts/`, `plans/`, or the ADRs.
- This change's own declarations are incomplete: the skeleton `plans/changes/swarm-report-format/research.md` carries neither a `class:` nor a `neighbours:` header line (read directly; the skeleton comes from `scripts/new_change.py`, which writes no such lines). The runner reads the class from `--class` or the `research.md`/`spec.md` headers and refuses disagreement, and the neighbours header is validated with exit 2 when missing or invalid (`scripts/stage2_research_map.py`, `validate_given_neighbours`; `scripts/stage2_availability.py`, neighbours-header reader).
- Not read (stated as unread, not as absent): `scripts/stage2_runs.py`, `scripts/stage2_research_history.py`, `scripts/stage2_research_snapshot.py`, `scripts/stage2_research_limits.py`, `research-swarm-limits.yaml`, the full body of `tests/test_stage2_swarm.py`, and the archived research-swarm `design.md`/`findings.md`; their possible extra format constraints are an open question.

## Which files a change would have to touch

For a change to the research-swarm record: `scripts/stage2_research_run.py` (`compose`/`manifest_record`), `scripts/stage2_research_report.py`, `scripts/stage2_research_map.py`, `scripts/stage2_research_judge.py`, `scripts/research_handoff.py`, `scripts/check_research_handoff.py`, `scripts/stage2_research_store.py`, `scripts/stage2.py` (`quote_research_records`), the tests listed above, and — because the version string `research-swarm/v2` is checked literally by the gate and asserted in tests — a version-bump decision touching `docs/adr/0020-phase-1-research-swarm.md` and the archived v2 spec would be unavoidable context. For a change to the review-loop report: `scripts/stage2.py` (`ANSWER_FORMAT`, `parse_rows`, `ROW_COLUMNS`/`RELEASED_COLUMNS`, loop-record writer), `prompts/04b-review-loop.md`, `docs/WORKFLOW.md` §4, `docs/adr/0021-review-swarms-until-clean.md`, and the row-parsing tests. Either way: `prompts/01a-interview.md` and `prompts/02-spec.md` describe consumption of the current format and would need to stay true.

## Neighbours (suggested for the `neighbours:` header)

- `plans/changes/archive/2026-11-06-research-swarm/spec.md` — the decided v2 report/handoff contract (primary neighbour for surface 1)
- `plans/changes/archive/2026-11-06-research-swarm/design.md` — same change's design decisions
- `plans/changes/archive/2026-11-06-swarm-time-limits/spec.md` — swarm timing limits
- `plans/changes/archive/2026-11-06-loop-until-clean/spec.md` — review-loop round rules
- `plans/changes/swarm-test-speed/spec.md` — open draft touching swarm run performance

---

**Hinweis an die Orchestrierung:** Die Recherche deckt beide möglichen Themenauffassungen ab, weil die Bead-Beschreibung (`coding-harness-4q9y`) nicht aus dem Baum lesbar ist — das steht oben ausdrücklich als offene Frage drin. Der Skeleton-Header der `research.md` hat weder `class:` noch `neighbours:`; beides braucht der Läufer vor einem Schwarmlauf (`stage2_research_map.validate_given_neighbours` bricht mit Exit 2 ab).

## Orchestrator addendum — the failed run, replayed (2026-11-09)

The runner exploration above could not read the tracker and so described two
surfaces. The bead (coding-harness-4q9y) names one: the report a research
swarm seat returns (`prompts/research-swarm/report.md`, checked by
`validate_research_report` in `scripts/stage2_research_report.py`). The bead
is done when a swarm explore completes with every seat's report accepted and
a test pins the failing format. Class: bounded (maintainer, 2026-11-09).

What was measured: the eight `partial` records of the failed run `1938a24f`
(change `testing-strategy`, 2026-11-08, notes in bead coding-harness-1ga5),
read from the envelope saved outside the repository and replayed against the
parser at commit 01fb3e38. One record is an empty answer (a seat that never
answered); the other seven were rejected for five different reasons:

| Slot | Runner error | What the answer actually contained |
|---|---|---|
| topics-9-2, topics-11-2 | `invalid report JSON` | one sentence of prose, then a complete, valid-looking JSON object in a `json` fence |
| topics-5-2 | `invalid report JSON` | the JSON object in a fence, followed by tool-call residue (`</arg_value></tool_call>`) |
| topics-1-3 | `invalid claims/questions template` | eight claims; the limit is seven |
| topics-1-2 | `report fields do not match the template` | one claim carried an extra field, `basis_note` |
| topics-4-2 | `report fields do not match the template` | two extra top-level fields, `gate_route` and `neighbours` |
| topics-5-3 | `report fields do not match the template` | topic 5 without its required `neighbour_relations` |

Where the strictness sits:

- `payload_text` (`scripts/stage2_research_run.py`) accepts the bare object
  or an answer that is exactly one fenced block. Text before or after the
  fence makes the whole answer `invalid report JSON`. Three of the seven
  rejections are this case alone.
- `_keys` (`scripts/stage2_research_report.py`) refuses any extra field at
  the top level, in a claim, in a question and in the topic-specific
  objects. Two rejections are an extra field beside an otherwise complete
  report.
- The seven-claim limit and the topic-5 field are part of the decided
  contract (ADR 0020, decision 5). Two rejections are real contract breaks
  by the model.
- A rejected seat is not asked again. The review loop asks a member once
  more with a format reminder after a malformed answer
  (`FORMAT_REMINDER`, `MalformedAnswer` in `scripts/stage2.py`, bead
  coding-harness-70rw); the research swarm has no such step — not found in
  `scripts/stage2_research_run.py`, which was searched for the two names,
  not read in full.

Limits: only run `1938a24f` was replayed. Run `63b74c37` failed on timeouts
of one model and is not a format case. The prompt
(`prompts/research-swarm/report.md`) was read to line 70 of 100; the
topic-specific sections were not read.

## Draft gap check — invocation ceiling (2026-11-09)

Read at b9a87940: ADR 0020, decision 9, explicitly caps model invocations at
`39 + 3N` and prohibits retries; `N` is the selected free-model count.
`ResearchRun.expected_slots` and `manifest_record` in
`scripts/stage2_research_run.py` preserve that fixed budget; `stage_topics`
invalidates rejected reports without redispatch. The requested one correction
per topic contribution can add `33 + 3N` invocations, giving a proposed maximum
of `72 + 6N`. Renaming calls as attempts within a slot does not preserve the
decided invocation ceiling. This is a governance decision, not an answerable
implementation detail; the draft spec records it as open.

The report prompt was now read in full: its topic-3, topic-5 and topic-6
requirements agree with the strict validator. No prompt or schema relaxation
is needed for extracting wrapped reports. The shared `payload_text` helper is
also used by non-topic stages, so topic-only extraction avoids changing them.
