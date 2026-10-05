---
title: "Research — research-currency"
status: draft
implementation_status: none
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-pu9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, docs-research, drift-job, frontmatter]
---

# research currency — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). Facts
only, read on 2026-10-05 in the worktree at `87daf91` (branch
`feat/research-currency`, fresh from `origin/main`). Every statement names its
source; what was not read says so.

The task: part 1 of bead coding-harness-pu9 — a deterministic list of the
research notes under `docs/research/` whose last review is too old,
report-only, in the nightly `drift` job (maintainer, 2026-10-05). Part 2, a
recurring agent that re-checks content on the web, is not in this change.

## 0 · Existing artefacts on the topic

`rg -i "currency|last_reviewed|stale|freshness|reviewed"` over `plans/specs/`
and `plans/changes/` finds no artefact on this topic except this scaffold.
`plans/specs/` holds no spec file. Nothing to update instead of create.

## 1 · What exists today

### 1.1 The corpus

`docs/research/` holds 17 files, no subdirectory: 15 notes, `_INDEX.md` and
`.gitkeep` (`find docs/research -type f`). Every `.md` file opens with a YAML
header, and each header carries `created:`, `last_reviewed:` and `updated:`
as unquoted `YYYY-MM-DD` values, which PyYAML reads as dates (measured with
`yaml.safe_load` on each header; no CRLF line endings, no byte-order mark).

| File | `last_reviewed` | `updated` | Age of the review on 2026-10-05 |
| --- | --- | --- | --- |
| `2026-09-16-review-corpus-vs-running-workflow.md` | 2026-09-16 | 2026-09-29 | 19 days |
| `arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md` | 2026-09-16 | 2026-09-29 | 19 days |
| `Lake-Switch-Architektur-arc42.md` | 2026-09-16 | 2026-09-29 | 19 days |
| `Migrationsplan_Omnigent_Referenzarchitektur.md` | 2026-09-16 | 2026-09-29 | 19 days |
| `2026-09-18-agent-skills-assessment.md` | 2026-09-18 | 2026-09-29 | 17 days |
| `2026-09-18-crewai-assessment.md` | 2026-09-18 | 2026-09-29 | 17 days |
| `2026-09-18-human-planning-and-harness-gaps.md` | 2026-09-18 | 2026-09-29 | 17 days |
| `2026-09-18-open-code-review-assessment.md` | 2026-09-18 | 2026-09-29 | 17 days |
| `_INDEX.md` | 2026-09-18 | 2026-10-05 | 17 days |
| `2026-09-23-worktree-tracker-writes.md` | 2026-09-23 | 2026-09-29 | 12 days |
| `2026-09-26-agent-sdk-and-formal-models.md` | 2026-09-26 | 2026-09-29 | 9 days |
| `2026-09-23-obsidian-as-reader.md` | 2026-09-27 | 2026-09-29 | 8 days |
| `2026-09-26-kubernetes-gate-runner.md` | 2026-09-27 | 2026-09-29 | 8 days |
| `2026-09-30-adhd-frame.md` | 2026-09-30 | 2026-09-30 | 5 days |
| `2026-09-30-decision-pull-requests.md` | 2026-09-30 | 2026-09-30 | 5 days |
| `2026-10-05-likec4-roadmap-arc42.md` | 2026-10-05 | 2026-10-05 | 0 days |

- **Three notes are German:** the two arc42 documents and the migration plan.
  Their headers carry the same keys as the others, without `produced_by:`
  (read in each header). `_INDEX.md` calls them, with the 2026-09-16 review
  note, the "four intake sources" that "recover the original rationale"
  (section "Reading routes").
- **`updated:` is not a review date.** It moved to 2026-09-29 in 12 notes
  whose `last_reviewed:` did not move — the stamp that came with the gate
  `frontmatter-current` (bead coding-harness-qd7). That change's spec says it
  in so many words: "`last_reviewed` records a review, not a change"
  (`plans/changes/archive/2026-09-29-frontmatter-current/spec.md`, "Problem").
- **`last_reviewed:` is used as a re-check date.** The Obsidian note was
  created 2026-09-23 and carries `last_reviewed: 2026-09-27`; the index row
  for it reads "re-checked 2026-09-27" (`_INDEX.md`, table "New assessments
  and planning research"). The Kubernetes note: created 2026-09-26, reviewed
  2026-09-27.
- **`review:` in the header is something else:** the provenance sign-off
  (`status: pending`, `approved_by: null` in every note), which waits for a
  second person in the roster (`scripts/ramp_valves.py`,
  `provenance_review_valve`).
- **No rule says who sets `last_reviewed:` or when.** No script writes it for
  `docs/`; `scripts/new_change.py` (`_frontmatter_template`) writes it only for
  a new `plans/changes/` scaffold; `scripts/check_frontmatter_current.py`
  (`stamp`) inserts `updated:` after it but never changes it.
- The oldest review is 2026-09-16 (four notes). With a threshold of 90 days
  ("more than 90", as below), the first note would be listed on 2026-12-16.
- Not read: the note in progress on branch `docs/research-hermes` (bead
  coding-harness-6hx); it is not on `origin/main`.

### 1.2 What reads `last_reviewed` today

- `scripts/check_docs.py`, `PFlicht` — only that the key is present, for
  every file under `docs/` that has a header. Gate `docs-links`, job `verify`,
  `enforcement: report` (`decisions/gates.yaml`).
- `scripts/plans_registry.py`, `STALE_AFTER_DAYS = 90` and `_age_days` — the
  one age rule in the repository: a `plans/` artefact not under `archive/`
  whose `last_reviewed` is more than 90 days old (`age > STALE_AFTER_DAYS`) is
  DRIFT; an unreadable date is DRIFT too ("An unreadable value is a finding,
  not a reason to skip the check"). It looks only at `plans/`; `artefacts()`
  skips files whose name starts with `_`. `plans/_README.md` ("Frontmatter")
  documents the 90 days and says the number lives in the script.
- `scripts/check_frontmatter_current.py` reads `updated:` only.
- Nothing reads the age of `last_reviewed` under `docs/research/` (`rg
  last_reviewed scripts/ tests/`).

### 1.3 The rule set

`docs/governance/regelwerk.md`, row RB-S4 (German; in English): every
knowledge page names its owner and when it was last checked; a deprecated page
is only a pointer; supersessions link both ways. Level 2 (a request, nothing
fails). Its valve `freshness-per-page` in `scripts/ramp_valves.py`
(`REGEL_VENTILE`) becomes due when
`tests/test_validators.py::test_deprecated_pages_are_pointers_only` exists, at
the latest 2026-12-31. Row RB-G7 (level 4): an empty set is no result —
every gate asserts that the set it measures is not empty.

`docs/architecture/target-architecture.md`, constraint C3: Claude Code,
Codex, Cline and Omnigent "change monthly".

### 1.4 The gate file and the generated workflow

- **One list.** `decisions/gates.yaml` enumerates every gate; `scripts/ci_gates.py`
  reads it and generates `.github/workflows/ci.yml` (`generate_ci`); the gate
  `ci-drift` (`--check-ci`) fails on a hand edit. The header of
  `decisions/gates.yaml` documents the schema: `id`, `title`, `command` or
  `action`, `job` (`verify` | `drift`), `enforcement` (`advisory` | `report` |
  `block`), `floor`, `placement` (`hosted` | `writer` | `both`), `reason`,
  optional `needs_tracker` and `needs_history`.
- **Report-only is declared by `enforcement`.** `_schritt` adds
  `continue-on-error: true` to every `advisory` or `report` step, so a non-zero
  exit does not fail the job. The local runner (`scripts/verify_all.sh`)
  turns only `block` red and prints "rot, aber nur report" for the others.
  Examples: `docs-links` and `markdownlint` (`report`), `lychee` (`advisory`).
  The reason line of `docs-links` names when it will be switched up; a gate
  reported low "for now" needs a valve with a condition
  (`scripts/ramp_valves.py`, module docstring).
- **The `drift` job** runs on `schedule` (`cron: "23 4 * * *"`) and
  `workflow_dispatch` only (`generate_ci`; held by
  `tests/test_ci.py::test_drift_job_runs_on_schedule_and_dispatch_only`).
  Today it holds one gate, `plans-registry-strict`, which needs the tracker,
  so the job hydrates it first. Its checkout has one commit unless a gate in
  the job declares `needs_history` (`_checkout`). Every gate step carries
  `if: ${{ !cancelled() }}`.
- On 2026-10-05, `plans_registry.py --check --strict` is red locally for
  reasons outside this change: four beads in progress without an artefact
  under `plans/changes/` (run in this worktree).
- `make verify` runs only the `verify` job; `bash scripts/verify_all.sh --job
  drift` runs the drift job's gates locally.

### 1.5 Ratchets a new script and gate meet (`tests/test_ci.py`)

- `test_every_script_has_a_caller_or_a_declared_reason` — the script's path
  stands in `ci.yml` (or the runner), or it is listed in
  `ci_gates.OHNE_AUFRUFER` with a reason.
- `test_every_script_has_a_test_or_a_declared_reason` — a test file imports it
  or names it as a string in its syntax tree; `OHNE_TEST` is empty and may
  only shrink.
- `test_every_gate_step_has_a_mutation_test` — some test file that contains
  the script's file name has a test whose name matches `MUTATIONS_NAMEN`
  (`goes_red`, `catches`, `notices`, …); `OHNE_MUTATIONSTEST` may only shrink
  (cap 12, 7 entries).
- `test_der_echte_lesepfad_des_bead_gates_wird_erkannt` — only
  `scripts/plans_registry.py` may name the tracker's directory as a path
  literal.
- `test_the_drift_job_holds_only_steps_that_can_run` — no drift step may need
  the customer instance or `--project-path`.

### 1.6 The kit

- `scripts/kit/manifest.yaml`: the longest prefix wins; the catch-alls
  `scripts/`, `tests/` and `docs/` are `bestand` (stay here); `decisions/` and
  `.github/workflows/ci.yml` are `mechanismus` (travel). The scripts behind
  gates are `mechanismus` with reasons such as "the gate file travels, so its
  script does" (`scripts/check_frontmatter_current.py`). A test that builds
  its own trees is `mechanismus` (`tests/test_frontmatter_current.py`: "never
  reads this one's dates; holds in the probe copy").
- `scripts/kit/probe.py` runs `pytest` in a copy of the `mechanismus` files
  and compares the red cases with `REIST_NICHT`, whose size may only fall.
  `docs/research/` is not in that copy.
- `scripts/export/manifest.yaml` ends in a catch-all `drop`; the sibling
  check `check_frontmatter_current.py` has no line there.
- The convention "research about this repository lives in `docs/research/`"
  stands in `AGENTS.md` ("Sessions across checkouts"), which is `bestand`;
  `docs/WORKFLOW.md` does not define it.

### 1.7 How a drift-job result reaches the maintainer

- **The run page only.** Nothing in the tree writes a GitHub job summary:
  `rg GITHUB_STEP_SUMMARY` finds no hit; a job summary of changed beads is an
  open idea (bead coding-harness-1jg.4, open, P3).
- **Not the display.** `tools/claude-code/` shows git state, beads in
  progress, other sessions, the latest handover and the recap
  (`tools/claude-code/README.md`, "What it shows"); it reads no CI result.
  Its texts are German because the maintainer reads them (`AGENTS.md`, house
  rule 1).
- What GitHub itself notifies about a scheduled run is outside the
  repository: not read.
- `tests/test_ci.py::test_the_drift_job_holds_only_steps_that_can_run`: "A
  job that is red every morning is not read".

### 1.8 Class, ADR question and the phase gate

- `docs/WORKFLOW.md`, "Change classes, the ADR question and decision pull
  requests": `bounded` "changes an existing, readable flow without deciding
  anything new"; `feature` is "a self-contained deliverable that changes what
  the system must do or how it is checked" and owes the ADR question.
- `scripts/check_adr_answers.py` (`examine`): a `feature` spec under
  `plans/changes/` without `decisions/answers/<change>/adr.yaml` is a finding,
  exit 1; the gate `adr-answers` is `block`, so `make verify` is red until
  the maintainer answers with `python3 scripts/harness.py decide adr`.
- Precedents: `frontmatter-current` (one check over the same headers, one
  gate key) is a `feature`, answered "no" on 2026-09-30
  (`decisions/answers/frontmatter-current/adr.yaml`); `adhd-frame` asked its
  class as `[DECISION] 1` and took `bounded` provisionally
  (`plans/changes/adhd-frame/spec.md`, "Open decisions").
- Bead coding-harness-pu9 is of type `feature`; it covers both parts.
- `scripts/validate_change_artefacts.py`, the gate of phases 2 and 3, does
  not exist (`docs/WORKFLOW.md`, note "Not all of it is here yet");
  `plans/changes/harness-decide-adr/spec.md` used `plans_registry.py
  --check` in its place.
- `decisions/gates.yaml` has no prefix of its own in `provenance.yaml` (only
  `decisions/answers/` is `human-decided`), so a pull request changing it is
  not a decision pull request. A gate with `floor: true` is "a governance act"
  to change (`decisions/gates.yaml`, schema comment).

### 1.9 Part 2, as the bead describes it

Bead coding-harness-pu9 (maintainer, 2026-10-05): a recurring agent
"re-checks the oldest note's dated facts and sources on the web and opens a
pull request with an addendum (holds / overtaken / new), never editing
findings in place and never writing the tracker"; its prompt "lives in the
repository and is runner-neutral"; its runner waits for the Hermes
assessment (bead coding-harness-6hx). So part 2 needs from part 1: which note
is the oldest, and a way to read the list without parsing prose.

## 2 · What is unclear

1. The threshold. `docs/research/` has no review rhythm; the only one in the
   repository is the 90 days for `plans/` (1.2).
2. Whether `_INDEX.md` is a note. It is a reading map, not a source review;
   `plans_registry.py` skips `_`-prefixed files.
3. Whether the German intake documents age like the others (1.1).
4. What a note without a readable `last_reviewed:` is in the list.
5. Whether "report-only, never red" allows a non-zero exit when the list could
   not be measured at all (1.4: `report` keeps the job green either way).
6. Where the maintainer sees the list (1.7).
7. The class, and with it whether the ADR question is asked (1.8).
8. The machine-readable form part 2 reads (1.9).

## 3 · Files a change would touch

- `scripts/check_research_currency.py` — new: the list.
- `tests/test_research_currency.py` — new: its tests, on trees of their own.
- `decisions/gates.yaml` — one entry in job `drift`.
- `.github/workflows/ci.yml` — regenerated, never edited.
- `scripts/kit/manifest.yaml` — the role of the two new files.
- `docs/research/_INDEX.md` — possibly, a sentence on what `last_reviewed:`
  means for a note.
- `plans/INDEX.md` — regenerated.
