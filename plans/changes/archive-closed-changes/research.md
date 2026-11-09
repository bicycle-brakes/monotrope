---
title: "Research — archive-closed-changes"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-cqun
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06; draft-time checks appended to the recorded Flash exploration"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
neighbours: []
---

# archive closed changes — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md).
The exploration route and model are recorded below; draft-time repository
checks are appended at the end.

Stage-2 call, 2026-11-06: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 909 files, 3403 commits, 12 rules.

## Runner exploration — 2026-11-06

Research complete. Here is the phase-1 exploration for `archive-closed-changes`, ready to append to `plans/changes/archive-closed-changes/research.md`.

---

## What exists today

**The three-places model is written doctrine.** `plans/_README.md` ("Three states, three places") defines `specs/<capability>/spec.md` as living, `changes/<name>/` as active, and `changes/archive/YYYY-MM-DD-<name>/` as historical ("stays as evidence, is never cited"). `docs/WORKFLOW.md` repeats the same tree (plans/specs · plans/changes · plans/changes/archive/YYYY-MM-DD-<name> · docs/adr) and states the close doctrine in one sentence: "On close: the delta into the living capability spec, permanent architectural decisions as an ADR, the rest into the archive." `prompts/07-commit.md` (after the merge-step section) names the same lifecycle end. No ADR in `docs/adr/` (0001–0024) owns the archive or the close procedure itself; the closest are ADR 0013 (criterion proofs held after archiving) and ADR 0014 (adoption day).

**The archive exists and is stocked — but no tool moves anything.** `plans/changes/archive/` holds 19 dated folders, `2026-09-20-2ee-triage` through `2026-10-08-stage2-runs-count`, plus `.gitkeep`. In `plans/INDEX.md` every archived artifact row carries `status: accepted` and `implementation_status: done`. The Makefile has no archive target (`verify test staleness gates leakcheck venv lock change index report close-merged help` only), and the `scripts/*.py` inventory contains no archive verb — archiving so far happened manually (folder move, frontmatter edits, `make index`). Twelve handover notes under `docs/journal/handover/` match the word "archive" (glob list, not read in this session); whether one of them records the manual steps used for the 19 folders is an open question.

**The pull toward archiving is already enforced, per artifact.** `scripts/plans_registry.py` (gate `plans-registry`, block, floor, `needs_tracker`, `decisions/gates.yaml`) reports DRIFT "built and not archived" for every artifact under active `changes/` whose `implementation_status` is `done` (the `in_changes and not archived and meta.get("implementation_status") == "done"` branch), and the bead coupling demands, per artifact: bead closed → the artifact must be `done` **and** lie under `changes/archive/`; artifact `done` → bead closed. Both directions are DRIFT and only turn blocking in the nightly `plans-registry-strict` drift job — `plans/_README.md` states the window between `bd close` and archiving is deliberate. A stale `plans/INDEX.md` is BLOCK ("deviates from its inputs", fix `make index`), not DRIFT. `scripts/new_change.py` refuses a new change folder on a closed bead and refuses any name for which `plans/changes/archive/` already holds a folder in the exact dated form (`ARCHIV_PRAEFIX = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-"` plus the name) — an archived name is reserved forever.

**The gates are archive-transparent by design** — moving a folder does not escape any of them:
- `check_criterion_ledger.py` measures live and archived folders in one pass; an archived plan without a ledger is exempt only when its header `date:` lies before `CUTOFF = date(2026, 10, 11)`; a `not yet written` entry in an archived plan is a finding.
- `check_adr_answers.py` globs `plans/changes/*/spec.md` and `plans/changes/archive/*/spec.md`, stripping the date prefix from archived names.
- `check_interview_minimums.py` walks active and archived folders alike; the adoption day (`decisions/adoption.yaml`), not the folder's place, decides who is subject.
- `check_question_context.py` holds "live and archived changes" (`docs/WORKFLOW.md`); `check_research_handoff.py` documents "this repository, live and archive" and accepts all three spec forms in `neighbour_form`; `scripts/stage2_runs.py` reads findings/research "active or archived"; `stage2_research_map.py` (`_spec_folder`) knows both the active form and the archived `YYYY-MM-DD-<name>` regex form.
- `run_report.py` (`active_changes`) enumerates the immediate real folders under `plans/changes/` excluding `archive` — a change disappears from `make report` once archived.
- `scripts/kit/manifest.yaml` lists `plans/changes/archive` among the scaffold folders the kit creates in new repositories; the `leerprobe` kit probe classifies tracked files by prefix, and the archive path stays under the same prefixes.
- `check_frontmatter_current.py` (block, `needs_history`) holds each Markdown file's `updated:` against the committer date of the newest non-merge commit that changed it — a `git mv` inside the archiving commit is such a change, so every moved file's `updated:` must move to the archiving day (the gate's own `--stamp` repairs exactly this line).

**The tracker-side close machinery exists and is separate from archiving.** `prompts/07-commit.md` defines the `Closes-Bead: <id>` trailer, the post-MERGED reconciliation `make close-merged ARGS=--write` (`scripts/close_merged_beads.py`, Makefile target `close-merged`), and the SessionStart hook reconciliation (`tools/claude-code/hooks/beads-start.sh`). Closing the bead and archiving the folder are two different acts with a deliberate gap between them.

**Candidates visible today.** Two active changes carry `done` artifacts per `plans/INDEX.md`: `plans/changes/adr-0016-docs-check/` — all four artifacts `done`, status `draft`, bead coding-harness-v9xx, last_reviewed 2026-11-03; and `plans/changes/verify-duration/` — per-file mixed (decisions `partial`, findings `none`, plan `done`, research `partial`, spec `done`), bead coding-harness-1um6, last_reviewed 2026-11-04. Commit c529cd00 on this branch's history says "close the verify-duration measurement task (bead coding-harness-1um6)", but the tracker render itself was not readable in this read-only session — which bead is actually closed right now must be taken from `python3 scripts/plans_registry.py --check` at execution time. The registry's coupling is per artifact: with a closed bead, each verify-duration artifact not `done` is its own DRIFT row until it is set `done` and the folder is archived. Both candidate plans carry a `## Criterion ledger` (`plans/changes/verify-duration/plan.md:119`, `plans/changes/adr-0016-docs-check/plan.md:42`) and neither holds a `not yet written` entry (grep, no matches) — the ledger gate keeps holding both after a move. The living spec `plans/specs/implementation-verification/spec.md` is accepted/done and stays where it is; `plans_registry.py` states a spec under `specs/` is never archived.

## Where it lives

Doctrine: `plans/_README.md` (three places, frontmatter, DRIFT/BLOCK split), `docs/WORKFLOW.md` (lifecycle tree and close sentence, phase 7), `prompts/07-commit.md` (Closes-Bead, close-merged, archive sentence). Enforcement: `scripts/plans_registry.py` (built-not-archived, bead coupling, index BLOCK), `scripts/check_criterion_ledger.py` (`CUTOFF = date(2026, 10, 11)`), `scripts/check_adr_answers.py`, `scripts/check_interview_minimums.py`, `scripts/check_question_context.py`, `scripts/check_research_handoff.py`, `scripts/run_report.py`, `scripts/stage2_research_map.py`, `scripts/new_change.py` (name reservation), `scripts/check_frontmatter_current.py` (`updated:` freshness). Gate wiring: `decisions/gates.yaml` (`plans-registry`, `plans-registry-strict`, `frontmatter-current`, `criterion-ledger`, and the symmetric ones). Index: `plans/INDEX.md`, regenerated only by `make index` / `plans_registry.py --index`.

## What is unclear

- Which beads are closed today (tracker render not readable here) — the archiving set must be measured at execution time, not assumed from INDEX rows.
- Which day the archive-folder prefix `YYYY-MM-DD-` carries: all 19 folders are dated 1–6 days after their artifacts' last `last_reviewed`, but no doctrine text (plans/_README.md, WORKFLOW, new_change.py) defines the day. Not found — and "not written down" is a different statement from "the merge date is meant".
- Whether `status:` must move `draft → accepted` on archiving: the entire archived stock shows `accepted`, but no rule text says so; `plans/_README.md` only says status "moves when the project decides".
- The change's class declaration is absent from this `research.md` skeleton, and the bead description (which names the class per the 2026-10-22 rule) is not readable in this session.
- The required `neighbours:` header is now present as an empty list; no swarm run is planned. Historical candidate paths below are draft-time context, not a prepared handoff.
- Whether `check_docs.py` resolves links from `docs/` into `plans/changes/...` paths: its default basis is `REPO_ROOT / "docs"` (`--base`), so its reach beyond `docs/` was not verified in this session.

## Which files a change would have to touch

For each archived change: the folder `plans/changes/<name>/` moves to `plans/changes/archive/YYYY-MM-DD-<name>/`; every moved file's frontmatter (`status`, `implementation_status` where mixed, `updated`, `last_reviewed`) is edited in the same commit; `plans/INDEX.md` is regenerated (`make index`) — a stale index is BLOCK, so the regeneration belongs in the same pull request. Cross-references naming a moved change by path live today only inside the change itself and `plans/INDEX.md` (grep: `adr-0016-docs-check` appears in 5 files, all INDEX or own; `verify-duration` additionally by name — not path — in `scripts/verify_duration.py`, `scripts/verify_all.sh`, `docs/research/2026-11-04-verify-duration-baseline.md` and one `verify-duration.jsonl` prose mention in `docs/WORKFLOW.md`). If the change also wants tooling or doctrine for archiving, the touch set is `scripts/plans_registry.py` or a new script, `decisions/gates.yaml` (only if a gate changes), `plans/_README.md` and `docs/WORKFLOW.md` (only if the doctrine changes), and `Makefile` plus `tests/` for any new entry point. No test under `tests/` reads the real `plans/changes/` tree for these gates — they use `--root` fixture repositories (12 test files match `changes/archive`, all fixture-based as far as their gate scripts' `--root` seams show).

---

**Candidate `neighbours:` for the header** (spec paths known to relate): `plans/changes/beads-close-themselves/spec.md`, `plans/changes/criterion-test-ledger/spec.md`, `plans/changes/adr-0016-docs-check/spec.md`, `plans/changes/verify-duration/spec.md`, `plans/changes/run-report/spec.md`, `plans/specs/implementation-verification/spec.md`. `plans/changes/index-merge-regenerates/` is topically adjacent (index regeneration) but I verified only `research.md`, `findings.md` and a `plan.md` there — no `spec.md` seen, so I do not list one.


## Draft-time repository checks — 2026-11-06

Checked against HEAD `8be8751e`, without reading the tracker or anything
outside this worktree and its Git directory:

- `decisions.md` records class `bounded`, one maintainer-answered interview
  record (Q-1), and the archive-day, header-normalisation and report-default
  details. This resolves the class uncertainty above; phase 2b is not due.
- `templates/spec.md` and `templates/design.md` exist; there is no
  `templates/plan.md`. The plan therefore follows `prompts/03-plan.md` and
  the existing `plans/changes/beads-close-themselves/plan.md` structure.
- `scripts/validate_change_artefacts.py` is absent. Its named check cannot be
  reported green or implemented as part of this change. The interview,
  research-handoff and criterion-ledger checkers exist.
- `Makefile` exposes the separate `close-merged` report/write target;
  `prompts/07-commit.md` requires its writing invocation after confirmed
  `MERGED`. Adding the archive invocation there gives the answered Q-1 its
  recurring local caller without adding working-tree mutations to SessionStart.
- `scripts/ci_gates.py` declares `close_merged_beads.py` in
  `OHNE_AUFRUFER`, because it is a local command rather than a hosted gate.
  A new local archive script needs the same declaration; `tests/test_ci.py`
  checks this inventory. No new gate is needed.
- `scripts/plans_registry.py` exposes `render_index()` independently of
  tracker reads. Reuse that generator; do not duplicate its index format.
  Its CLI has no `--root` option: fixture tests should patch its repository,
  plans and index constants, as existing tests do.
- The default `check_docs.py` walks `docs/`, resolving links from each
  visited file. It does not recursively validate Markdown links inside the
  archived change folders. Moving a historical document adds a directory
  level, so its unchanged relative link text may resolve differently; this
  change promises preservation of historical bodies, not general link repair.
- The latest handover in this checkout is
  `docs/journal/handover/2026-11-03-five-lane-night.md`. Its lane state is
  historical; this branch already contains later merges. No current tracker
  state or hosted pull-request state was read. A backlog move manifest must
  consequently be measured by the orchestrator at application time; the two
  examples in the exploration are not an exhaustive eligibility list.
