---
title: "Findings — journal-citation-gate"
category: findings
status: draft
implementation_status: none
date: 2026-11-19
created: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-19
supersedes: null
superseded_by: null
bead: coding-harness-x9ed
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — journal-citation-gate

Stage-2 call, 2026-11-19: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1115 files, 4784 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/journal-citation-gate/plan.md` +47 -0
> - `plans/changes/journal-citation-gate/spec.md` +71 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - `plan.md` does not open with the plan card (For you:, Done when:, Appetite:, Not now:, Pre-mortem:)
> ```

Stage-2 call, 2026-11-19: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1118 files, 4785 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-19: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1118 files, 4790 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | BLOCKER | SPEC | base | plans/changes/journal-citation-gate/research.md:38; spec.md:41, spec.md:62 | This change's own `research.md:38` is in the runner-written "Runner exploration — 2026-11-19" section. That section is prose, not a research-swarm/v2 record. Line 38 cites the handover directory with the target `…` (U+2026). `_ZITAT` stops only at whitespace, a backtick, `)`, `]`, `,` or `;`, so `…` is the captured target. It is not empty, has no `*`, does not start with `<`, has no ISO date and is not inside a runner record. So AC3 reports it and the check stays red. This was measured from the text; the test was not run. The DoD still requires `make verify` green, and WORKFLOW.md:1144 says only the runner writes `research.md`. decisions.md names two red places; this is a third that nobody decided on. The spec does not say which way out phase 4 takes: (a) exempt the `…` elision, a third exemption Q-1 never granted; (b) hand-edit a file that only the runner writes; or (c) treat single-explorer runner sections as runner records. Each gives a different check, and whichever one is picked will be picked silently. | Opus | in spec | — |
| S-2 | MAJOR | SPEC | base | plans/changes/journal-citation-gate/spec.md:35 (AC1) vs spec.md:41 (AC3) | [AMBIGUITY] What "target contains `*`" covers. `_ZITAT` keeps `*` in the target. So a hand-written undated citation in Markdown emphasis, such as the handover path to `…/bootstrap.md` wrapped in `*…*` or `**…**`, gives the target `bootstrap.md*` or `bootstrap.md**`. Reading A (AC1 taken literally): any `*` exempts the target, so emphasised undated citations pass. That goes against Q-1, which says a hand-written undated citation stays red. Reading B (`*` means a glob wildcard): emphasis markers are not a pattern, so the citation is reported under AC3. AC1 and AC3 give opposite verdicts on the same input, and neither refutation case covers it. | Opus | in spec | — |
| S-3 | MAJOR | SPEC | base | plans/changes/journal-citation-gate/spec.md:31 (Terms), spec.md:47 (AC5), spec.md:69 | [AMBIGUITY] Which files can hold a runner record. The check scans every tracked Markdown file. The runner writes envelopes only into a change's `research.md` (WORKFLOW.md:1144), and `scripts/stage2.py::quote_research_records` only defuses forged markers in text appended there. Reading A (from spec.md:69, where only malformed markers "do not establish runner authorship"): a complete envelope with a fenced record exempts its contents in any file. That includes a findings row, a handover, or a spec that quotes the format inside a foreign example fence, so a hand-written undated citation there passes. Reading B ("runner-written" in Terms): only envelopes in `plans/changes/**/research.md` count, and the same block in any other file is scanned and reported. AC2 and AC5 pass under both readings, so no criterion decides between them. | Opus | in spec | — |
| S-4 | MAJOR | SPEC | base | plans/changes/journal-citation-gate/spec.md:31, spec.md:39, spec.md:47, spec.md:69 | [AMBIGUITY] "Matching run envelope" is not defined, and the closing marker `<!-- /research-swarm/v2 -->` carries no run id. Reading A: an opener pairs with the next closer. Then an opener with no closer, followed by a later complete envelope, forms one "complete" envelope, and the first run's fenced records are exempt. Reading B: "matching" means the well-formedness that `scripts/check_research_handoff.py:203-262` enforces. No run opens inside an open run, the record kind is in KINDS, the record closes with exactly its opening ticks, envelope markers end a foreign fence, and the manifest `run_id` equals the envelope id. Under B that first run is not exempt. AC5 can be refuted for a record with no envelope at all. Its "outside a matching run envelope" case cannot be built until this is settled. | Opus | in spec | — |
| S-5 | MINOR | SPEC | base | plans/changes/journal-citation-gate/spec.md:31 vs decisions.md:39, decisions.md:53 | [AMBIGUITY] Q-1 exempts "every citation inside a runner-written research-swarm record block". The Terms narrow that to fenced records. The runner's envelope also holds runner-written text outside any fence (`scripts/stage2_research_run.py:1799-1857`): the `## Research swarm` heading, the run header line, `public topic: <sentence>`, the `### Audit` list and the status line. Reading A (the Terms): a journal path in the public-topic sentence or an audit line is reported under AC3. That is machine-written text turning the check red, the case Q-1 was meant to end. Reading B ("record block" means the whole run envelope): it passes. AC2 and AC3 both give Q-1 as their basis, so the spec does not show which reading the maintainer chose. | Opus | in spec | — |

Stage-2 call, 2026-11-19: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1118 files, 4793 commits, 12 rules.
