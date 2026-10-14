---
title: "Research — interview-context"
status: draft
implementation_status: partial
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-zs7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# interview context — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 418 files, 1122 commits, 12 rules.

## Runner exploration — 2026-10-14

Phase 1 (Explore) for `interview-context` is finished — read: the interview prompt, the gate script with its tests, the workflow's question protocol, the ADHD evidence chain, the kit manifest, and the handover of 2026-10-14. Since I am not permitted to edit files in this phase, what follows is the complete content for `plans/changes/interview-context/research.md`, ready to be committed. The frontmatter changes only in three places according to the note in the skeleton: `provenance: ai-drafted-reviewed` plus `produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}` and `review: {status: pending, approved_by: null, approved_at: null}`; bead, owner, and dates remain as they are.

---

```markdown
# interview context — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md), run
2026-10-14. Topic: the rule that an interview question carries its context,
written for a reader with ADHD — what exists around it today.

## What exists today

1. **The rule stands already, in one home.** `prompts/01a-interview.md`,
   section "How you ask", paragraph "Every question brings its context,
   written for a reader with ADHD" (maintainer, 2026-10-14): before the
   options, two to four short sentences say what the question is about, why
   it comes up now and what happens today — in plain words, without assuming
   the reader knows the code, the finding or an earlier conversation; every
   id and technical term is explained where it first appears; the question
   itself comes last, on its own line. It entered the tree with commit
   f287278 ("docs(zs7): interview questions carry their context, written for
   a reader with ADHD"), one commit before the change folder was opened
   (390876e, "docs(zs7): open change interview-context").
2. **Neighbouring rules in the same section** (`prompts/01a-interview.md`,
   "How you ask"): one question at a time; only questions answerable without
   reading the code, sorted by the `[DECISION]`/`[GAP]`/`[DETAIL]`
   classification; every question carries its consequence (options named
   after what they do to users, operations or risk, never their mechanism);
   stop when the design tree has no unresolved branch left. The context
   paragraph sits between the consequence rule and the stop rule.
3. **The question form of the spec phase has no context line.**
   `prompts/02-spec.md` defines the question block "Goal in one sentence /
   Options / Recommendation / If you say ok / What is lost" — "the decision
   record (MADR) in question form". `docs/WORKFLOW.md`, section "The
   question protocol", points to exactly that block as "the form of a
   question to a person". Neither mentions background sentences or the
   ADHD-context rule.
4. **The question protocol and the communication rules carry no context
   rule.** `docs/WORKFLOW.md` §"The question protocol" sorts open points
   (`[DECISION]` → person, `[GAP]` → explore, `[DETAIL]` → agent) and says
   nothing about carrying context; `AGENTS.md`, "Communication and session
   continuity" ("Ask one decision at a time when possible, with a
   recommendation and its consequence"), likewise. A search for "ADHD" over
   the tree finds the word under `prompts/` only in
   `prompts/01a-interview.md`.
5. **The interview's record and its gate.** The record form (`## Q-1 ·
   <title>` with `asked`/`answer`/`answered_by`/`status` plus the MADR
   sentence; `## SKIP · interview` with `status`/`reason`) is defined only in
   `prompts/01a-interview.md`, "What you write" — the archived spec of the
   minimums change names that file the format's one home
   (`plans/changes/archive/2026-10-08-interview-minimums/spec.md`). No
   `templates/decisions.md` exists: `templates/` holds `adr.md`, `arc42.md`,
   `design.md`, `findings.md`, `gate-record.yaml`, `handover.md`,
   `spec.md`. `scripts/check_interview_minimums.py` parses the records
   (`_FIELDS` is asked, answer, answered_by, status, reason; `_parse_records`,
   `_counted`) and counts per class (`MINIMUMS`: feature 3, spike 3,
   bounded 1, architectural 0; five for a change that claims ADR files under
   `adr_files`). No field and no check concerns the question's context — the
   gate sees answers, not how a question was put. The gate runs in
   `make verify` (`decisions/gates.yaml`, id `interview-minimums`, pinned by
   `tests/test_check_interview_minimums.py::test_gates_yaml_declares_interview_minimums`)
   and is prospective from the adoption day 2026-10-08
   (`docs/WORKFLOW.md`, the paragraph after the phase table, read through
   `scripts/adoption.py`).
6. **Tests pin prompt and gate together.**
   `tests/test_check_interview_minimums.py::test_interview_prompt_defines_the_records`
   asserts `answered_by`, `status: skipped` and `## SKIP · interview` in the
   prompt text; `test_spec_prompt_names_the_interview_check` and
   `test_workflow_and_agents_state_the_duty` pin the duty's other mentions.
   `scripts/kit/probe.py` pins the model-endpoint test id of the 01a prompt
   ("…[01a-interview.md-Opus 5.5]"); the prompt header names Opus 5.5 as the
   interview's model (`prompts/01a-interview.md`, header block).
7. **Evidence base and older siblings.** The writing patterns trace to
   `docs/research/2026-09-30-decision-pull-requests.md` §2.4 "Cognitive
   accessibility and ADHD" (W3C COGA and others) and
   `docs/research/2026-09-30-adhd-frame.md` §2.8 (main point first; purpose
   clear at a glance; do not rely on memory). The adhd-frame change
   (`plans/changes/archive/2026-09-30-adhd-frame/`, answers confirmed by the
   maintainer on 2026-10-05) already gave ADHD-shaped forms to the plan card
   (`prompts/03-plan.md`: "For you / Done when / Appetite / Not now /
   Pre-mortem") and the acceptance card in the pull-request templates. The
   interview-context paragraph of 2026-10-14 is the newest piece of that
   family.
8. **Distribution.** The kit carries the whole `prompts/` prefix
   (`scripts/kit/manifest.yaml`, entry `prefix: prompts/`), so the paragraph
   reaches every kit install; the manifest lists no per-file entry for the
   01a prompt.
9. **The change itself.** `plans/changes/interview-context/` holds only this
   `research.md`; the plans index carries its row
   (`plans/INDEX.md`, entry `changes/interview-context/research.md`, bead
   coding-harness-zs7). No `spec.md`, `decisions.md`, `design.md` or
   `plan.md` exists for it. Live examples of the record exist — twelve
   `decisions.md` files carry `## Q-1` headings (search over
   `plans/changes/`), e.g. `plans/changes/adr-owning-change/decisions.md`;
   none was read in full in this phase.

## Where it lives

- The rule itself: `prompts/01a-interview.md`, "How you ask".
- The question form outside the interview: `prompts/02-spec.md` (the MADR
  question block) and `docs/WORKFLOW.md` §"The question protocol".
- The record and its counting: `prompts/01a-interview.md`, "What you write";
  `scripts/check_interview_minimums.py`; `tests/test_check_interview_minimums.py`.
- The evidence: `docs/research/2026-09-30-decision-pull-requests.md` §2.4;
  `docs/research/2026-09-30-adhd-frame.md` §2.8.
- The earlier ADHD-shaped forms: `prompts/03-plan.md` (plan card); the pull
  request templates (adhd-frame decisions, answer Q-2).
- The distribution: `scripts/kit/manifest.yaml`; `scripts/kit/probe.py`.

## What is unclear

1. **The bead's own description was not read.** The tracker is the Dolt
   database under `.beads/`, read through `tools/bd`; no rendered copy is
   committed, and this phase had no shell access to run
   `tools/bd show coding-harness-zs7`. What the change must deliver beyond
   the landed paragraph is taken only from the two commit subjects and the
   change name — an open question for the interview, not a fact.
2. **The maintainer's statement beyond the prompt citation: not found.** The
   only 2026-10-14 handover in the tree
   (`docs/journal/handover/2026-10-14-night-run-third.md`, with its
   addendum) does not mention bead zs7 or the statement; a handover of the
   session that wrote f287278 and 390876e was not found (search over
   `docs/journal/handover/2026-10-14*` returns exactly one file). The
   citation "(maintainer, 2026-10-14)" in the prompt and the commit subject
   are what stands.
3. **Scope: interview only, or every question to a person?** The landed
   paragraph speaks of the interview's questions. Where else a person is
   asked — the spec-phase decision question (`prompts/02-spec.md`), the
   plan-card veto (`prompts/03-plan.md`), `[DECISION]` notes resolved in
   conversation (`docs/WORKFLOW.md`, "The question protocol") — nothing read
   decides whether the rule reaches them. That is a `[DECISION]` for phase
   1a, not a fact of phase 1.
4. **Whether any check should ever see the context.** The gate parses five
   fields and counts answers; no text in the tree states whether that stays
   so or whether the record should one day show the context it carried.
5. **The prompt's own broken pointer.** `prompts/01a-interview.md`, "Terms
   count", sends settled terms to `docs/glossar/` and
   `docs/governance/begriffs-disziplin.md`; neither path exists in this tree
   ("not there" — glob), a break already recorded in
   `docs/research/2026-10-06-mattpocock-skills.md` ("A broken pointer",
   observed at commit d5813ec). It touches this change only if term
   explanations grow.

## Which files a change would have to touch

- `prompts/01a-interview.md` — the rule's one home; where any restatement or
  extension of the paragraph lands.
- `prompts/02-spec.md` — the MADR question block, if the form of a question
  gains a context requirement outside the interview.
- `docs/WORKFLOW.md` — §"The question protocol" and the phase-1a passages
  (the paragraph after the phase table; "The interview goes by class too").
- `AGENTS.md` — "Communication and session continuity", if the rule becomes
  house-wide for every question to the maintainer.
- `scripts/check_interview_minimums.py` and
  `tests/test_check_interview_minimums.py` — the record parser (`_FIELDS`)
  and the prompt pins, only if the record itself gains a field.
- `templates/` — holds no decisions template today; a decisions template
  would be created, not changed.
- `scripts/kit/manifest.yaml` and `scripts/kit/probe.py` — the `prompts/`
  prefix travels wholesale and probe pins a test id of the 01a prompt;
  whether they must change depends on what the change does to the prompt,
  which is not decidable from what was read.
```

---

Stage-2 call line of the skeleton stays untouched below the body. No design, no recommendation — open points 3 and 4 are written as `[DECISION]` material for phase 1a, as the header demands.

## Draft gap resolution — 2026-10-14

Read at `c7fa059`, before the draft's uncommitted additions:

- The five answered interview records now settle scope, enforcement,
  distribution, form and the prospective cut-off (`decisions.md`, Q-1 to
  Q-5); the exploration's statements that this file does not exist and that
  scope is undecided describe the earlier exploration only.
- The class definitions distinguish a self-contained new check (`feature`)
  from a new subsystem or broken interface (`architectural`); an ADR does
  not itself make a change architectural (`docs/WORKFLOW.md`, "Change
  classes, the ADR question and decision pull requests").
- The existing record ends its decision statement with `— YYYY-MM-DD`
  (`prompts/01a-interview.md`, "What you write"). A scan of answered
  Q-records under `plans/changes/`, including its archive, found 55 records
  and exactly one such date in each, as of `c7fa059`, 2026-10-14. The
  existing gate reads `asked`, not this date, and does not collect context
  (`scripts/check_interview_minimums.py`, `_FIELDS`, `_parse_records`).
- The one adoption reader returns a day per gate, and rejects an absent or
  unreadable day; the adoption record belongs to each repository
  (`scripts/adoption.py`; `decisions/adoption.yaml`). The current
  interview-minimums exemption uses the spec's date strictly after its
  adoption day; that rule differs from Q-5's inclusive answer-date cut-off.
- The workflow and prompts travel, while this repository's `AGENTS.md` and
  adoption record stay here; new scripts and tests need explicit mechanism
  entries (`scripts/kit/manifest.yaml`). The probe creates a repository
  from that mechanism and runs its tests (`scripts/kit/probe.py`, `_baue`).
- There is no plan template under `templates/`, and the named
  `scripts/validate_change_artefacts.py` does not exist at this commit. The
  plan's form is supplied by `prompts/03-plan.md`; existing checks include
  the plans registry, interview minimums and criterion ledger. The runner
  prepares derived files and runs verification after a draft
  (`scripts/stage2.py`, `verify_draft`).
- The current five answers have no field preserving their originally
  displayed context. If their date is on or after the eventual adoption
  day, the implementation needs that actual context from the orchestrator;
  this worktree does not supply it, and it must not be invented. Q-5 does
  not exempt answers from the adoption day itself.
