---
title: "Plan — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3, version: "2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, provenance]
---

# Plan — runner-stamps-provenance

```text
For you:     The runner stamps the provenance of the draft artifacts it publishes, a red check holds every producer header under plans/, and the ~50 free-form headers are migrated once, archived included.
Done when:   Runner tests prove the draft stamp and its byte preservation, the registry check goes red on a planted free-form header, the tree test finds no free-form producer header under plans/, and make verify is green.
Appetite:    3 hours of phase 4, repair rounds included; stop at the limit.
Not now:     A general side-route detector, allowed-class enforcement, the new-change skeleton, checks outside plans/, approval automation.
Pre-mortem:  suppose it failed: most likely because the migration could not derive a truthful producer for some archived header and invented one instead of reporting it.
Starts unless you say stop.
```

## Scope confirmation first

0. The orchestrating session reads the work item (`tools/bd show
   coding-harness-f9sv`) before implementation starts: its description names
   a four-part fix that no artifact of this checkout quotes
   (`research.md`, "What is unclear"). Whatever it names beyond the spec's
   criteria enters `spec.md` as an amendment with its own criteria and
   ledger entries before that part is built; a part needing a maintainer
   choice goes to `decisions.md` as a question. Nothing is built beyond the
   spec on the bead's word alone.

## Files and steps

1. `scripts/research_census.py`: expose the producer-record form of the
   metadata contract as one importable reader (for example
   `producer_form_problems(header)` — the name is freely revisable), so the
   census and the registry check share the one contract reader.
2. `scripts/plans_registry.py`: in `check()`, a present `produced_by`
   outside the record form is a BLOCK finding for that artifact — the
   header's own check (spec, criterion 2). A missing `produced_by` stays
   allowed (spec, Open decisions).
3. `scripts/stage2.py`: generalize the in-place header correction of
   `research_publication()` (first span replaced, further occurrences
   dropped, missing fields inserted before `tags:`) into one shared helper;
   `draft()` stamps the kept `spec.md`, `design.md` and `plan.md` with it
   after `draft_keep()` and `put_back`, before `verify_draft()` — producer
   from `producer_for()` of the draft route, day from the runner clock,
   `provenance`/`review` in the contract's form. Undecodable bytes or
   missing frontmatter refuse the publication, as research publication
   refuses them.
4. `scripts/migrate_producer_headers.py` (new): the one-time, idempotent
   migration of every `produced_by` under `plans/` into the record form.
   Producer and day derive from the file's own evidence — the runner audit
   lines standing in it, then its git history; a header nothing derives is
   reported, never invented. The implementing session resolves each
   reported header from its file's history, and the tree test (step 7)
   holds the result.
5. `tests/test_stage2_draft_publication.py` (new): the draft stamp over all
   three artifacts — a free-form header the drafting session wrote comes
   out conforming; bytes outside the stamped fields are preserved (prose,
   card, fences, unrelated fields); the refusal paths.
6. `tests/test_plans_registry_producer_form.py` (new): the registry check —
   a planted free-form `produced_by` blocks, live and archived; a conforming
   one and an absent one stay green.
7. `tests/test_runner_stamps_provenance.py` (new):
   `test_no_free_form_producer_header_under_plans` walks the repository's
   `plans/` tree and holds criterion 3; beside it the migration tests —
   idempotence, derivation from a planted audit line, the no-invention
   report — run against a fixture tree.
8. `plans/changes/runner-stamps-provenance/plan.md`: clear the
   not-yet-written markers as the tests land and record phase-4 time below.
   `plans/INDEX.md`: the runner regenerates the index. The migration diff
   over `plans/` — the ~50 headers, archived included — is part of this
   change's pull request.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2_draft_publication.py tests/test_plans_registry_producer_form.py tests/test_runner_stamps_provenance.py
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2_draft_publication.py::test_draft_stamps_published_artifact_headers — a draft attempt's kept artifact still carries the free-form produced_by the session wrote.
- 2: not yet written tests/test_plans_registry_producer_form.py::test_free_form_producer_header_blocks_the_registry — a planted free-form produced_by leaves the registry check green.
- 3: not yet written tests/test_runner_stamps_provenance.py::test_no_free_form_producer_header_under_plans — a free-form produced_by remains anywhere under plans/.
- 4: not yet written tests/test_stage2_draft_publication.py::test_stamp_preserves_authored_bytes — the stamp moves a byte outside provenance, produced_by, review and updated.

## What is not touched

`provenance.yaml`, `decisions/gates.yaml`, `prompts/`, `templates/`,
`.github/`, `.beads/`, `AGENTS.md`, `README.md`, `CLAUDE.md`, `.claude/`,
`.codex/`, `.agents/`, `.pi/`, `.mcp.json` — no step edits a held path: the
red check lands in the existing `plans-registry` gate, so the gate list
stays. `scripts/new_change.py` (the skeleton), `docs/adr/` (no ADR is due),
`docs/journal/**` (handover checks stay presence-only), the change folders'
`decisions.md` bodies (the migration rewrites headers only), and the loop
record outside the git directory.

## Boundaries and route

No design phase and no ADR are due for this bounded change. Explore ran
through Stage 2 on 2026-11-16, route flash, endpoint `glm-coding-plan`,
model `glm-5.3-flash`; no Stage-1 fallback is recorded.

## Time used

2026-11-16 16:05:48–16:16:58 UTC, 670 s — draft · attempt 3 · route glm · model glm-5.3 · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
