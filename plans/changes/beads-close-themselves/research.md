---
title: "Research — beads-close-themselves"
status: draft
implementation_status: partial
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-l1if
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: pi, version: "GLM 5.3 Flash, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# beads close themselves — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md), run by GLM 5.3 Flash.

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 788 files, 2822 commits, 12 rules.

## Runner exploration — 2026-10-31

Research complete. Here is the phase-1 report, ready to append to `plans/changes/beads-close-themselves/research.md`.

---

## What exists today

**The declared closure contract is written down; its executor is not.**

- `prompts/07-commit.md` ("If this commit finishes the work item, say so") defines the declaration: a commit that finishes a work item carries a `Closes-Bead: <id>` trailer, "like GitHub's `Closes #123`". Without the trailer the item stays open — stated as the right default, because "a merged pull request often leaves work behind".
- The same file then promises the execution: "After the merge, `make close-merged ARGS=--write` closes what was declared and what is an ancestor of the integration branch — both are checked, not claimed. Without `--write` the command only reports." It also fixes the placement: "It runs locally: the tracker writes to a database this repository does not carry. CI only reports — a declared closure nobody carried out is a finding, not a job for the machine."
- `templates/spec.md` (acceptance card, "Bead:" bullet) requires every spec to declare: "the pull request closes `<bead id>`, and its last commit carries the trailer `Closes-Bead: <bead id>`". `tests/test_templates.py:405` pins that wording.
- The PR templates carry the reporting side: `- Beads: <title> (<id>), opened / changed / closed` in `.github/pull_request_template.md` (Evidence block) and in `.github/PULL_REQUEST_TEMPLATE/decision.md`.

**The rule of who closes.** AGENTS.md house rule 4: the first writing session "closes, reprioritises and links" (AGENTS.md, house rule 4 list) and "a pull request names in its body every bead it opens, changes or closes" (maintainer, 2026-09-23). ADR 0005 (`docs/adr/0005-workers-claim-their-own-bead.md`, "The decision" section) decided option (b) — workers "close it after the merge" — and rejected option (c), the coordinator closing, because a path-level sandbox cannot tell the writes apart. It also records a mechanical constraint: bd itself refuses a close of a bead claimed by another actor ("assignee is worker-a, actor is worker-b") without `--force` (ADR 0005, layer 1). The `tools/bd` wrapper allows `close` — it blocks only `init`, `migrate`, `upgrade` (`tools/bd`, verb loop). The generic beads skill adds one rule any mechanism must reconcile with: "Do not auto-close or mutate tasks unless the work is actually complete" (`.agents/skills/beads/SKILL.md`, Rules).

**The enforcement that does exist is the staleness coupling, not closure.**

- `scripts/plans_registry.py --check` couples artefact and bead state for everything under `plans/changes/`: a bead `closed` while the artefact is not `done` and archived is DRIFT ("bead … is closed in the export, but the artefact is not 'done' and archived"); `implementation_status: done` while the bead is open is DRIFT ("implementation_status is 'done', but bead … is not closed"). The comment states why both directions are DRIFT, not BLOCK: "`bd close` typically runs AFTER the merge, so a BLOCK here would hit not the commit that caused it but the next uninvolved pull request".
- Gate `plans-registry` (`decisions/gates.yaml`, id `plans-registry`) runs that command without `--strict` in verify and in `make staleness` — DRIFT reports there without failing the run. Gate `plans-registry-strict` runs `--check --strict` in the scheduled `drift` job with `enforcement: block`; its reason says DRIFT blocks only on the timer (ADR-028 R2).
- The reverse direction: a bead `in_progress` with no artefact under `plans/changes/` is DRIFT, with the fix hint `make change NAME=<name> BEAD=<id>` (`plans_registry.py`, coupling block end).
- Reading the tracker: `scripts/bead_render.py` `render_pfad()` (preset `BEAD_RENDER` or one fresh render) and `scripts/plans_registry.py` `_bead_export_path()` — commented as "the ONE access point to the tracker state (bead 1jg.3)". In CI, the generated hydration step `setup-tracker` (emitted by `scripts/ci_gates.py`, `_tracker_hydratation`) fetches `refs/dolt/data`, bootstraps the pinned bd and presets `BEAD_RENDER`.

**The executor is absent — confirmed, not assumed.** `make close-merged` is not there: the `Makefile` (read in full) declares only `verify test staleness gates leakcheck venv lock change index report help`, and no script under `scripts/` matches `close` (glob `scripts/*close*` empty; `scripts/harness.py` has no close or `tools/bd` match). Three committed sources state the absence independently: the archived adhd-frame findings ("This repository has no `close-merged` target yet, so the trailer is a declaration nothing here carries out" — `plans/changes/archive/2026-09-30-adhd-frame/findings.md`), the merge-queue research ("absent from `Makefile` and `scripts/` since at least 2026-10-08" — `plans/changes/merge-queue/research.md`, gap list), and the handover of 2026-10-08 ("The documented `make close-merged` target and its script are absent at this commit; closure must use the verified trailer and ancestry explicitly" — `docs/journal/handover/2026-10-08-runner-derived-files.md`). No script in `scripts/` writes the tracker at all — the only `tools/bd` uses there render (`render_beads_export.py`, `bead_render.py`), validate (`new_change.py --bead`) or bootstrap in generated CI (`ci_gates.py`); I searched for `bd close`/`bd update` calls and found none. The reporting CI job the commit prompt presupposes is also not there: `.github/workflows/ci.yml` is the only workflow file (glob) and contains no `close` match. The corpus comparison attributes such a job — `ci.yml#merged-beads`, "reports a declared close nobody carried out" — to the portfolio repository, the workflow's origin, and records the doctrine as "Declared by `Closes-Bead:` trailer, executed on the integration branch … keep — strictest, and enforced" (`docs/research/2026-09-16-review-corpus-vs-running-workflow.md`, findings D8 and the topic table row "Bead closing").

**One mechanic was already measured.** The archived adhd-frame findings verified on a merged commit (`coding-harness-q24`) that both `git interpret-trailers --parse` and `%(trailers:key=Closes-Bead)` read the trailer, and that with the merge form of `prompts/07-commit.md` the commit reaches `main` unchanged.

**The entry gate already respects closure state.** `scripts/new_change.py` refuses a `--bead` that points at a closed bead; `tests/test_workflow_entry.py` pins it (`test_new_change_refuses_a_closed_bead`, and the Makefile-level table in the same file).

## Where it lives

- Declaration contract: `prompts/07-commit.md` (phase-7 prompt), `templates/spec.md` (acceptance card), `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/decision.md`.
- Who may close: `AGENTS.md` house rule 4; `docs/adr/0005-workers-claim-their-own-bead.md` (accepted, partly superseded by ADR 0006); `docs/WORKFLOW.md` tracker quick reference (`tools/bd close <id> --reason="…"`, `tools/bd dolt push` after writes); `tools/bd` (wrapper verb blocklist).
- Detection: `scripts/plans_registry.py` (coupling block), `decisions/gates.yaml` (`plans-registry`, `plans-registry-strict`, `bead-export`, `dangling-beads`), `scripts/bead_render.py`, `scripts/ci_gates.py` (hydration).
- Doctrine history: `docs/research/2026-09-16-review-corpus-vs-running-workflow.md` (D8), `docs/adr/0004-tracker-render-is-the-contract.md` ("The two conveniences and their successors" — the PR-body rule is the successor of the committed export; the CI job summary of changed beads was decided as bead `coding-harness-1jg.4`).
- The gap's paper trail: `plans/changes/archive/2026-09-30-adhd-frame/findings.md`, `plans/changes/merge-queue/research.md`, `docs/journal/handover/2026-10-08-runner-derived-files.md` and `2026-10-08-runner-derived-close-claude.md`.

## What is unclear

- The bead's own words are unreadable in this phase. The tracker is the Dolt database under `.beads/` (`sync.remote` in `.beads/config.yaml`); no rendered copy is committed (house rule 2), so title, description and class of `coding-harness-l1if` wait for `tools/bd show` — the same limitation the merge-queue research recorded. What "close themselves" concretely means (a `close-merged` executor, CI execution, or something else) is therefore an open question, not a guess I will write down.
- The class declaration: the research skeleton declares none and `spec.md` does not exist yet, so the runner's class sources cannot agree or disagree — there is nothing to read.
- The provenance of the coupling: the comment "State coupling artefact <-> bead (AK-5, spec.md D3)" in `plans_registry.py` cites a spec that is not in the tree — repo-wide, `AK-5` matches only that comment. Which artefact owned it is unknown from committed files.
- Test coverage of the coupling: I searched `tests/` for the coupling's message strings ("closed in the export", "not appear in the tracker", "in_progress but has no artefact") and for `close-merged`/`Closes-Bead` — the only hits are `test_templates.py:405` (spec-template wording), `test_workflow_entry.py` (closed-bead refusal at entry) and `test_ci.py:2168` (`test_no_declared_reason_cites_a_closed_or_unknown_bead`, which is gate-file hygiene, a different topic). Whether the coupling has coverage under other wording is unchecked, not found absent.
- The sentence "CI only reports — a declared closure nobody carried out is a finding" in `prompts/07-commit.md` presupposes a reporting job this repository does not carry. Whether it describes the portfolio origin or an unbuilt plan here is stated in no committed file I read.
- Whether the `make close-merged` absence is decided deferral or drift: the merge-queue research kept it "out of scope here" without naming an owner, and no bead id for it appears in any tracked file.
- Whether every merged, trailer-declared bead was in fact closed by hand is tracker state this phase cannot read; the handover of 2026-10-08 shows the step had to be done explicitly at least once.

## Which files a change would have to touch

- `Makefile` — where every entry command lives (the `Makefile` help block and `docs/WORKFLOW.md` "Entry commands" row name this as the entry surface).
- A closure script under `scripts/` — none exists today; it would be the first script that writes the tracker, so it goes through the pinned `tools/bd` (house rule 3) and ends with `tools/bd dolt push` (house rule 4).
- `decisions/gates.yaml` and the regenerated `.github/workflows/ci.yml` — a new gate enters the one list and ci.yml is generated (`ci_gates.py --generate-ci`; a hand edit fails the `ci-drift` gate). If the gate needs the PR body or a new per-gate feature, `scripts/ci_gates.py` changes too — the per-gate `env:` the ci-bead-summary research asked about does not exist yet.
- `prompts/07-commit.md` — its `make close-merged` wording must match whatever exists.
- `scripts/plans_registry.py` — only if the coupling's DRIFT timing changes; its two gates live in `decisions/gates.yaml`.
- Tests: `tests/test_ci.py` (gate-list pins, `_bead_status` fixture), `tests/test_workflow_entry.py` (closed-bead refusal), `tests/test_gate_machinery.py` (placement vocabulary), plus whatever pins the new script — nothing pins trailer parsing today.
- Constraint to carry, from the sources above: closure writes run locally, not in CI (`prompts/07-commit.md`); only the first writing session writes the tracker (house rule 4); bd refuses closing a foreign-claimed bead (ADR 0005 layer 1); and the beads skill's "no auto-close unless actually complete" rule.

## Suggested neighbours (for the `neighbours:` header)

`plans/changes/merge-queue/spec.md` (active; deferred `close-merged` out of scope) · `plans/changes/ci-bead-summary/spec.md` (active; the CI bead summary, bead `coding-harness-1jg.4`) · `plans/specs/implementation-verification/spec.md` (the one living capability spec) · `plans/changes/archive/2026-09-30-adhd-frame/findings.md` (trailer mechanics measured) · `plans/changes/archive/2026-09-21-reproducible-bead-export/` (render/export lineage).
