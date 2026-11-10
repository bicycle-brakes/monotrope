---
title: "Research — central-config"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-twvx
owner: Data Architect
provenance: human-written
tags: [research]
---

# central config — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-10: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason the research swarm's reports failed their format check twice on 2026-11-09 (bead coding-harness-4q9y); night plan step 5 · leak check clean over 980 files, 3799 commits, 12 rules.

## Runner exploration — 2026-11-10

I could only establish a thin picture of central-config: the change is a skeleton with no description of what it should do. The most likely reading, from the surrounding notes, is the "one central place for each phase's model" idea. Findings below are from read-only inspection; nothing was run.

## What exists today

**The change folder** (`plans/changes/central-config/`) holds only `research.md`, a skeleton with frontmatter (`status: draft`, `bead: coding-harness-twvx`, `owner: Data Architect`, `provenance: human-written`) and the sentence "this file is empty until it has run". It has no `spec.md`, `decisions.md`, `design.md` or `plan.md`. Its last paragraph records a Stage-2 call on 2026-11-10 (explore, attempt 1, claude-haiku-5-5, leak check clean over 980 files, 3799 commits, 12 rules). That call came from the night plan, step 5, after the research swarm's reports failed their format check twice on 2026-11-09 (bead coding-harness-4q9y). The git status shows `research.md` modified, and HEAD is `5b5a39f9`, "chore(central-config): open the change".

**The index** (`plans/INDEX.md`, the central-config row) lists the change as `draft`, implementation status `none`, dated 2026-11-10, bead coding-harness-twvx. This is the only index entry that names central-config.

**The name is used for no existing artefact.** A search for `central[- _]config`, and for "central" with "config" or "configuration", found no spec, decision, script or test named central-config. Matches for the bare word "central" concern other topics, listed below.

**Related prior work on "one central place" for model choices** (the closest existing concept):

- `docs/research/2026-10-31-run-plan.md`, section "Tracker hygiene": bead coding-harness-ylu ("one central place for each phase's model") is marked superseded by coding-harness-wq1m (the model registry).
- `plans/changes/archive/2026-11-06-go-access-point/` (spec, decisions, plan): exactly one source for the Go address, "fitting the later central model registry (bead coding-harness-wq1m)". Its spec's non-goals exclude "the general model registry, phase and model routing, the catalog sources". Those are handed to wq1m.
- `plans/changes/archive/2026-11-06-sol-effort/` (spec, decisions, research, plan): the effort of each Sol verb is set in one central declaration, and runner, instructions and tests read it from there. The archived research says that declaration "stands once in `scripts/stage2.py`". A grep for an effort-mapping identifier in that file found no match, so the exact symbol is not confirmed.
- `plans/changes/archive/2026-11-06-explorer-reviewer-agents/decisions.md`: the pinned sub-agent models were chosen "accepting that the registry (bead coding-harness-wq1m) will later take these choices over".
- `model-endpoints.yaml`: a comment near the `research_swarm` block (which states "the roles are declared here, not hard-coded in a script") says the research-swarm roles are declared in this file. A comment near the endpoint at line 505 refers to "bead coding-harness-k0ub with coding-harness-wq1m".
- `docs/research/2026-11-07-night-run-plan.md`, lanes table: "the central model state (coding-harness-atxy)" waits for lane 1, "One central free-model selection (coding-harness-wb40)". Lane 1 is the central free selection, not central-config.
- `docs/research/2026-10-31-run-plan.md`, "Backlog" section: the phrase "the maintainer decided on one central place" is attached to the research-swarm hot-fix decision.
- `plans/changes/archive/2026-11-06-research-swarm/` and `plans/changes/research-free-paid/decisions.md` record "one central free selection" (Q-1 there) as an architecture choice already made.

**Files that carry central-style configuration today** (names only, not read in full): `scripts/stage2.py`, `scripts/stage2_go.py`, `scripts/stage2_availability.py`, `scripts/stage2_swarm.py`, `scripts/stage2_runs.py`, `scripts/stage2_session.py`, `model-endpoints.yaml` (the endpoint and data-class register, with German comments), and the manifests `scripts/kit/manifest.yaml` and `scripts/export/manifest.yaml`.

## What is unclear

- **The change's intent is not written anywhere in the repository.** No description, decision or spec says what central-config should centralise. The reading "a single central place for per-phase model and effort settings, superseding ylu and fitting wq1m" is inferred from neighbouring work, not stated. [GAP → interview]
- **The bead's text is not read.** The bead coding-harness-twvx description, which must name the class (house rule: "a bead for a change names its class"), could not be read with read-only tools. The class of this change is therefore not known. [GAP → explore with the tracker, or maintainer]
- **Relation to wq1m (the model registry).** The archived notes say wq1m takes over model-registry work. Whether central-config is wq1m, a part of it, or a separate change is not stated. [DECISION → maintainer]
- **Relation to atxy ("central model state") and wb40 ("one central free-model selection").** Both are named in the night plan, and neither is described as central-config. Whether they overlap is not established.
- **Whether a central config file already exists.** No file with `central` in its name was found. The search covered the repository but not the bead database, so a tracker-only definition cannot be excluded.

## Which files a change would have to touch

Not determinable until the intent is stated. Candidate surfaces that the notes name as already holding per-phase or per-endpoint settings are `scripts/stage2.py`, `scripts/stage2_go.py`, `scripts/stage2_availability.py`, `model-endpoints.yaml`, and the tests that read them: `tests/test_stage2.py`, `tests/test_model_endpoints.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_declaration.py`. Changing any of them touches the Stage-2 routing that the night plan lists as lane 1 and lane 6 work, so the overlap with those lanes is a real risk to note.

## Structural gaps in `research.md` (for the runner and the maintainer)

- **No `neighbours:` header.** The phase doctrine requires a `neighbours:` list in the header of `research.md`; a missing header refuses the swarm. The skeleton has none. Neighbours I can already name are `plans/changes/archive/2026-11-06-go-access-point/spec.md`, `plans/changes/archive/2026-11-06-sol-effort/spec.md`, `plans/changes/archive/2026-11-06-research-swarm/spec.md` and `plans/changes/archive/2026-11-06-explorer-reviewer-agents/decisions.md`.
- **No class declaration** in `research.md` or `spec.md` (the class header required for phase-1 routing). Blocked on the bead text above.
- **Provenance** is still `human-written` in the frontmatter, while the content here is model-produced. The skeleton's own note says whoever fills it with a language model sets `ai-drafted-reviewed` with `produced_by:` and `review:`.

## Next actions

1. The maintainer states, in one sentence, what central-config should centralise, and whether it is wq1m or a separate change. This is the question that blocks interview and spec.
2. The bead coding-harness-twvx description is read in the main session (`tools/bd show coding-harness-twvx`) to fix the class.
3. Before any swarm run, `research.md` gets its `neighbours:` header.

## Orchestrator addendum — the bead's intent (2026-11-10)

The runner exploration above could not read the tracker, so it guessed the
intent from the change's name. The bead states it; its description is quoted
here unchanged so that a second exploration starts from the stated goal.

Class: architectural (bead coding-harness-twvx, maintainer 2026-11-08).

Title of the bead: "One central harness configuration: models, routes, rounds,
lanes, limits, thresholds, metrics and decision rules in one validated file".

> Class: architectural (maintainer 2026-11-08, repeated across topics: model
> selection, rounds and seating, lane limit, size limits, watchdog and
> heartbeat parameters, metrics, evaluations, monitoring and the rules that
> turn metrics into decisions must all be central and easy to change). Today
> these values sit in runner constants (scripts/stage2.py),
> model-endpoints.yaml, docs tables, prompts and prose. One declarative file
> (or one directory with one schema) holds them; a validator checks it; runner,
> scripts, prompts, docs and tests read it and no constant repeats it (a gate
> finds repeats); a change is a one-line edit through a pull request. Builds
> on the closed routing decision coding-harness-ylu and the implement route of
> coding-harness-9ycy. Consumers: coding-harness-3rtn (review seating),
> coding-harness-9ycy (implement route), coding-harness-g8g7 (size limits),
> coding-harness-5q2p (watchdog), coding-harness-6pn3 (heartbeat),
> coding-harness-nqaf (metrics and decision rules).

The tracker lists six beads as waiting for this one (read 2026-11-10): the
metrics and nightly experiments (coding-harness-nqaf), the heartbeat as a
feature (coding-harness-6pn3), the lane watch (coding-harness-5q2p), the size
gate (coding-harness-g8g7), the implement route in one central file
(coding-harness-9ycy) and the review loop with fewer rounds
(coding-harness-3rtn). A seventh consumer was decided on 2026-11-09: the slot
count of the verify lock (bead coding-harness-u1ha,
`plans/changes/verify-slots/decisions.md` on its branch, Q-2) moves into the
central configuration later.

What the second exploration should establish: where each of the named kinds
of value sits today (constant, YAML key, table, prompt sentence), which
readers each has, which values are repeated in more than one place, and what
the existing declarations (`model-endpoints.yaml`, `gates.yaml`,
`provenance.yaml`) already validate.
