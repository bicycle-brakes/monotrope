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

Stage-2 call, 2026-11-10: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason the research swarm's reports failed their format check twice on 2026-11-09 (bead coding-harness-4q9y); night plan step 5; second pass with the bead's intent stated · leak check clean over 980 files, 3800 commits, 12 rules.

## Runner exploration — 2026-11-10

## Exploration: central-config, second pass (bead intent stated)

Read-only, tools Read, Grep and Glob. Nothing was run and no file was edited. The earlier pass in this file guessed the intent from neighbouring notes; the bead's stated intent is now in the orchestrator addendum, and this pass maps the repository against it. Where a value was not found in the places searched, that is stated as "not found in `<path>`", not as "none".

### What exists today

**Declarations that already exist as one file each**

- `decisions/gates.yaml` (header comment "THE ONE LIST", bead bo0): the single enumeration of machine gates. `scripts/verify_all.sh` asks `scripts/ci_gates.py`, which reads this file. `.github/workflows/ci.yml` is generated from it (`--generate-ci`) and held to it by the `ci-drift` gate. This is the closest existing precedent for "one file, a validator, a generator, a drift check". Schema v2, with `tools`, `gates` and per-gate fields (`id`, `command`, `job`, `enforcement`, `floor`, `placement`, `needs_tracker`, `needs_history`, `subsets`, `reason`).
- `model-endpoints.yaml`: the data-class and endpoint register (German comments). Top-level keys: `schema_version`, `datenklassen`, `endpunkte`, `research_swarm` (paid endpoint, `topic_author`, `judge`, six seat pins, `intelligence_slugs`, `availability_preflight.max_age_seconds: 900`, `online_free`), and `ausgeschlossen`. The `research_swarm` comment states that the roles are declared here and not hard-coded in a script, and that the order of `opencode-go.modelle` is the review-loop ladder (phase 4b), which that block does not change. `tests/test_model_endpoints.py` reads it.
- `research-swarm-limits.yaml` (repository root): `run_minutes: 160` and `role_minutes` for `finders`, `merge`, `sentence`, `topics`, `judge`. It is read once per invocation by `scripts/stage2_research_limits.py` (constants `FILE_NAME`, `RUN_KEY`, `ROLE_KEY`, `ROLES`), which refuses with exit 2 when a value is missing, unknown or implausible. `tests/test_stage2_research_limits.py` covers it. This file already follows the target shape for its own values.
- `provenance.yaml`: the file-class register (`human-decided` and others). Read by the provenance checks. Its validator was not read in this pass.
- `scripts/kit/manifest.yaml` and `scripts/export/manifest.yaml`: manifests for the kit and export, read by `scripts/kit/probe.py` and related scripts. Not read in full.

**Values in runner code (constants in Python)**

Read by grep for `^[A-Z_]+ =` and names; values quoted as found.

- `scripts/stage2.py` (the runner): model triples `GLM_FLASH`, `GLM`, `HAIKU`, `SONNET`, `CODEX`, `OPUS` (each a tuple of endpoint, model ID and effort, e.g. `OPUS = ("claude-code-plan", "claude-opus-5-5", "xhigh")`); `CODEX_EFFORTS = {"draft": "high", "repair": "medium", "review": "high"}`; `CLASSES`, `SWARM_CLASSES`; `REVIEWER_MINUTES = 45`; `CLEAN_CODE = 3`; `PI_VERSION_SECONDS = 30`; `PI_DISCOVERY_SECONDS = 120`; `RED_FIRST_MINUTES = 10`; `KILL_DRAIN_SECONDS = 5`; `FREE_DIFF_MAX_LINES = 400`, `FREE_DIFF_MAX_TOTAL = 2000`, `REVIEW_DIFF_MAX_LINES = 2000`; `TOOL_SECONDS = 5 * 60`, `VERIFY_SECONDS = 30 * 60`, `GIT_SECONDS = 2 * 60`; `TERMS_WARNING_DAYS = 7`; `GLM_CONTEXT_TOKENS = "200000"`; `PI_TOOLS = "read,grep,find,ls"`; `DOCS_VERIFY = ["bash", "scripts/verify_all.sh", "--job", "docs"]`.
- `scripts/stage2.py` also holds the prompt-text constants (`CARD_LABELS`, `DRAFT_PROMPTS`, `PHASE6_*`, `REPAIR_*`, `FORMAT_REMINDER` and so on), which duplicate sentences that appear in `prompts/*.md`. This was not checked line by line.
- `scripts/stage2_swarm.py`: `GO_ENDPOINT`, `CLAUDE_ENDPOINT`, `PRIVATE_ROLES`, `PUBLIC_ROLES`, `OPUS_ROLES`, `ROLE_CLASS`, `LAUNCHERS`, `SEAT_KEYS`, `PUBLIC_TOOLS`. The role table is in code, while the seats are in YAML.
- `scripts/stage2_research_dispatch.py`: `PER_PROVIDER_LIMIT = 4`, `TICK = 0.05`.
- `scripts/stage2_research_run.py`: `PREPARATION_SECONDS = 60.0`, `EMPTY_PACKET_GAP`, `TOPIC_NAMES`, `TOPIC_SCOPES`, `JUDGE_KEYS`. Also `scripts/stage2_research_judge.py`: `REPORT_FLOOR_CHARACTERS = 5_000`, `DISPOSITIONS`, `TOPIC_OUTCOMES`.
- `scripts/stage2_research_store.py`: `STATES`, `SLOT_KEY_FIELDS`, `REUSABLE_OUTCOME`, `STOP_REASON`.
- `scripts/stage2_availability.py`: `PROBE_SECONDS = 60`, `CATALOG_SECONDS = 70`, `PROBE_TEXT`.
- `scripts/stage2_session.py`: `PROMPT_LIMIT = 32 * 1024`, `COMMAND_LIMIT = 64 * 1024`, `CLI_TIMEOUT = 30.0`, `OSASCRIPT_TIMEOUT = 30.0`, `TRANSPORTS`, `LAUNCH_LIMITS`.
- `scripts/stage2_research_map.py`: `CATEGORIES`.
- `scripts/research_handoff.py`: `COUNTING_NEEDED = 3`, `NEIGHBOUR_KIND_ORDER`.
- `scripts/check_interview_minimums.py`: `CLASSES`, `MINIMUMS = {"feature": 3, "spike": 3, "bounded": 1, "architectural": 0}`.
- `scripts/kit/probe.py`: `DECKEL = 44`, with a long comment of raises and lowers of the value since 2026-09-29 (the comment is itself a change log).
- `scripts/pr_sync.py`: `WORKING_DAYS_OVERDUE = 5`, `LIST_LIMIT = 1000`, and several timeouts.
- `scripts/close_merged_beads.py`: `GIT_TIMEOUT = 30.0`, `FETCH_TIMEOUT = 60.0`, `BD_TIMEOUT` (read from an environment variable).
- `scripts/render_beads_export.py`: `BD_FEHLT = 127`, `MASCHINENLOKAL`.

**Values repeated in more than one code place (by reading the constants)**

- `STALE_AFTER_DAYS = 90` appears separately in `scripts/check_research_currency.py` and `scripts/plans_registry.py`.
- `REVIEWER_MINUTES`, `RED_FIRST_MINUTES` and the timeouts sit in `stage2.py`, while `research-swarm-limits.yaml` gives the research-swarm timeouts a separate source.
- `anfragen_5h` is read in `scripts/stage2.py` (ordering, notices) and in `scripts/stage2_availability.py`. The value itself is declared in `opencode-go` terms (a model file), which was not read in this pass.
- Model IDs: `claude-opus-5-5`, `claude-haiku-5-5`, `glm-5.3-flash` and `gpt-6.1-sol` each appear in `model-endpoints.yaml` (22 matches for the four IDs together) and in code, prompts and docs (grep counts outside `tests/`, with `plans/` included in the count, were in the hundreds). A count restricted to the non-archive, non-plan repository paths was not taken in this pass; the figure is "many", not a measured total.
- Model IDs in prompts: `prompts/02-spec.md`, `02b-design.md`, `03-plan.md`, `02a-spec-review.md`, `04-implement.md`, `06-review.md` each carry model or effort text (1 to 2 matches each for the four IDs together).
- `docs/WORKFLOW.md` carries 13 matches for the same four model IDs, so the workflow doctrine repeats the values as prose.

**Consumers named in the bead addendum (checked by existence only)**

- `coding-harness-3rtn`, `9ycy`, `g8g7`, `5q2p`, `6pn3`, `nqaf`, `u1ha`: bead IDs only. The bead text was not read here (no tracker access), so the claimed "waiting for this one" relation rests on the addendum.
- `plans/changes/night-heartbeat/`: exists, with a `spec.md`, `plan.md` and `findings.md`. This is the heartbeat work that the addendum names as a consumer (6pn3); its values were not read.
- `plans/changes/verify-slots/decisions.md`: the addendum says it sits on a branch. In this worktree it was not found under `plans/changes/`, so it is not read here.

**Not found**

- `watchdog`: no match in `scripts/` (case-insensitive grep). Other locations (`tools/`, `docs/`, `plans/`) were not searched in this pass.
- `lane limit` / `lane_limit` / `LANE`: no constant matched in `scripts/`. The night-run lane concept is documented in `docs/WORKFLOW.md` ("Night runs") and in `docs/research/2026-11-07-night-run-plan.md`, not in code. Whether a numeric lane limit lives in a file is not established.
- `metrics` and `decision rules` as code objects: not searched for specifically in this pass.
- A gate that finds repeated constants (the addendum says "a gate finds repeats"): no such gate was identified in `decisions/gates.yaml` by the titles read; a full list of gates was not read.
- `gates.yaml` is at `decisions/gates.yaml`, not at the repository root.

### Where each kind of value lives (summary, from the above)

| Kind | Where it sits today |
|---|---|
| Model choices per role | `model-endpoints.yaml` (`research_swarm`, `opencode-go.modelle`) and Python triples in `scripts/stage2.py` (`OPUS`, `SONNET`, `HAIKU`, ...) |
| Seat / route assignment | `model-endpoints.yaml` (`research_swarm` seats); role-to-endpoint map in `scripts/stage2_swarm.py` |
| Research-swarm time limits | `research-swarm-limits.yaml` (one YAML, own validator) |
| Other timeouts | Python constants across `stage2.py`, `stage2_session.py`, `stage2_availability.py`, `pr_sync.py`, `close_merged_beads.py` |
| Size limits (diff, prompt, report) | Python constants: `FREE_DIFF_MAX_LINES`, `REVIEW_DIFF_MAX_LINES`, `PROMPT_LIMIT`, `REPORT_FLOOR_CHARACTERS`, `DECKEL` |
| Rounds / clean-round count | `CLEAN_CODE = 3` in `stage2.py`; round text parsing in `stage2.py` |
| Gate list | `decisions/gates.yaml` (one file, generator, drift gate) |
| Prompt sentences | `prompts/*.md` and the duplicate constants in `stage2.py` (`CARD_LABELS`, `REPAIR_*`, ...) |
| Doctrine values in prose | `docs/WORKFLOW.md` (model IDs, limits, timeouts as prose) |
| Interview minimums | `scripts/check_interview_minimums.py` (`MINIMUMS`) |
| Pinned Pi version | `tools/pi/package.json`, read by `stage2.py` (`_pi_pin()`) |

### What is unclear

- **Which readers would switch to a central file, and which must keep a local copy.** The addendum asks for "no constant repeats it". For example, `docs/WORKFLOW.md` is prose; whether it can read a file or must be checked by a gate is not established.
- **Whether `model-endpoints.yaml` and `decisions/gates.yaml` already validate anything that the new file would need.** Their validators were not read in full. `tests/test_model_endpoints.py` and `scripts/ci_gates.py` were not opened.
- **The status of `anfragen_5h` and the `opencode-go` model list.** The file where the cost value lives, and its validator, were not read.
- **Whether the seven consumer beads depend on this change in the tracker.** The addendum states it; tracker access was not available to this pass.
- **Whether `verify-slots` exists on this branch.** Not found under `plans/changes/` in this worktree.
- **How many repeats there are in total.** Counting every constant against every occurrence was not done; the numbers above are per-file or per-pattern grep counts, and a count of the whole tree (`plans/`, `docs/research/`, `handover/`) would mix history with live code.
- **Whether a central file would hold prompt prose or only the values.** The bead says "models, routes, rounds, lanes, limits, thresholds, metrics and decision rules". Prompt sentences are named in the title list only through the phrase "prompt sentence" in the addendum's kind list; their status is open.

### Which files a change would have to touch

Not determinable until the interview fixes the scope. The files that would certainly be read or changed by the named kinds are:

- `scripts/stage2.py` (constants, `CLEAN_CODE`, `REVIEWER_MINUTES`, triples, `CODEX_EFFORTS`, size limits), `scripts/stage2_swarm.py`, `scripts/stage2_research_limits.py`, `scripts/stage2_availability.py`, `scripts/stage2_session.py`, `scripts/stage2_research_dispatch.py`, `scripts/stage2_research_run.py`, `scripts/stage2_research_judge.py`, `scripts/kit/probe.py`, `scripts/pr_sync.py`, `scripts/close_merged_beads.py`, `scripts/check_interview_minimums.py`, `scripts/check_research_currency.py`, `scripts/plans_registry.py`.
- `model-endpoints.yaml`, `research-swarm-limits.yaml`, `decisions/gates.yaml` (as a precedent and possibly a consumer).
- `prompts/*.md` (model and effort text), `docs/WORKFLOW.md` (13 matches for the four model IDs).
- Tests: `tests/test_model_endpoints.py`, `tests/test_stage2_research_limits.py`, `tests/test_stage2.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_session.py`, and `tests/test_ci.py` (the drift gate).

### Structural gaps in `research.md`

- **No `neighbours:` header.** The phase doctrine requires it; a missing header refuses the swarm. The neighbours named by the first pass remain valid candidates (`plans/changes/archive/2026-11-06-go-access-point/spec.md`, `plans/changes/archive/2026-11-06-sol-effort/spec.md`, `plans/changes/archive/2026-11-06-research-swarm/spec.md`, `plans/changes/archive/2026-11-06-explorer-reviewer-agents/decisions.md`). Two more are now named by the addendum's wiring: `decisions/gates.yaml` (as the precedent) and `research-swarm-limits.yaml` (as the existing one-file case).
- **No class declaration in `research.md` or `spec.md`.** The addendum states `architectural` (bead coding-harness-twvx, maintainer 2026-11-08). The header still needs the declaration.
- **Provenance** is still `human-written`. The content is model-produced, so the skeleton's own rule applies (`ai-drafted-reviewed` with `produced_by:` and `review:`).
- **Tracker not read by this pass.** The class and the consumer list come from the addendum and were not checked against the tracker.
