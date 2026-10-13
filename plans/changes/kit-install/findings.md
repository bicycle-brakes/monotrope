---
title: "Findings — kit-install"
category: findings
status: draft
implementation_status: none
date: 2026-10-13
created: 2026-10-13
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-2uk
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — kit-install

Stage-2 call, 2026-10-13: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 410 files, 1032 commits, 12 rules.

ADR answer owed: decisions/answers/kit-install/adr.yaml does not exist and the gate tolerated that for this run; the answer is the maintainer's (python3 scripts/harness.py decide adr).

Stage-2 call, 2026-10-13: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 416 files, 1036 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `spec.md`, Terms "Fresh target", AC 4–5; `research.md` §2 | [AMBIGUITY] Terms say "Missing kit paths alone do not establish freshness", yet AC 5 refuses only an unpinned target that holds a kit-file destination. Reading A: freshness is the operator's selection and the installer tests only for a lock and for collisions. Then lakeswitch-ai at `ce88eee` passes: it has no lock, its three same-path files are exactly the three templates of AC 3 (preserved by AC 4) and the other 80 kit paths are absent, so install writes 80 files and a lock into it. Reading B: the installer itself must refuse a separately reimplemented workflow, and nothing states what it recognises one by. | Opus | in spec — freshness allowlist and refusal are explicit (Terms; AC 5) | — |
| F-2 | MAJOR | SPEC | base | `spec.md`, AC 3, AC 23, Protected areas, Non-goals; `scripts/kit/manifest.yaml:268` | [AMBIGUITY] Which paths carry the `template` role beyond the three AC 3 names. Protected areas list `AGENTS.md`, `provenance.yaml`, dependency pins, `.claude/`, `.codex/` and `tools/` with "fresh-instance starting content is kept separately in the kit". Reading A: only what AC 23 needs is added (Makefile, dependency declaration), and `provenance.yaml` stays `mechanismus` as the manifest has it today. It then arrives with the source's path map and every update overwrites it. Reading B: each listed path has a starter that install places. A fresh target then receives an `AGENTS.md`, harness settings and a tracker pin, against the non-goal that excludes installing trackers and local harness settings. | Opus | in spec — exactly five templates; agent/provenance/tracker configuration excluded (AC 2–3) | — |
| F-3 | MAJOR | SPEC | base | `spec.md`, AC 11, AC 14; `decisions.md`, Q-3 | [AMBIGUITY] A template that a later source version adds, at a path the target's lock has never recorded. AC 11 installs added kit files only; AC 14 protects paths that already belong to the target. Reading A (Q-3, "only at the first install"): update never writes a template. The new starter reaches a pinned instance only by hand or through the report, and a kit file added in the same version that reads it finds none. Reading B: that update is the template's first install into this instance, so it writes the file once when the path is absent and records it as target-owned. | Opus | in spec — update templates deferred by Q-6 (Non-goals; follow-up coding-harness-66q) | — |
| F-4 | MAJOR | SPEC | base | `spec.md`, AC 5, 11, 13, 16, 17 | [AMBIGUITY] Update meets a kit file new in the selected version whose target path is occupied by a file the lock does not record. AC 11 covers only "an absent, previously unowned target path"; AC 13 covers only recorded paths. Reading A (as AC 13 and 16): a per-path conflict. The file is preserved, the other files are applied and the lock marks the version incomplete, though AC 16's "prior baseline" does not exist for this path. Reading B (as AC 5 and AC 17's "conflicting destination"): the whole update refuses before writing. AC 17 does not say whether "conflicting destination" means two payload entries claiming one path or a destination occupied in the target. | Opus | in spec — update collisions deferred by Q-6 (Non-goals; follow-up coding-harness-66q) | — |
| F-5 | MAJOR | SPEC | base | `spec.md`, Terms "Conflict", AC 13, 15, 16; `decisions.md`, Q-2 | [AMBIGUITY] Terms define a conflict as a path that cannot receive the requested change "without replacing local work"; AC 13 triggers on any local change to a recorded kit path. The two part where the local state already equals the selected version's: the owner copied the new bytes by hand, or deleted a file the selected version also retires. Reading A (AC 13): still a conflict. The path keeps its old baseline (AC 16), the update stays incomplete and it clears only once the old bytes are put back. Reading B (Terms): nothing local would be replaced, so the path takes the new baseline or leaves the lock, and the pin is complete. Q-2's "until someone resolves it" has no criterion saying when a conflict of content or of ownership (AC 15) has ended. | Opus | in spec — update resolution deferred by Q-6 (Non-goals; follow-up coding-harness-66q) | — |
| F-6 | MAJOR | SPEC | base | `spec.md`, AC 7, AC 24; `research.md:22–25,150–151,286–287` | [AMBIGUITY] Which target state the report compares. AC 7 asks for "both repository commits" and a commit cut-off; AC 24 lists an "unreadable file" next to an "unresolved commit". Reading A: the target is read from a named commit's objects, as the research did (`ce88eee`, its `origin/main`), so uncommitted and untracked files are not seen. Reading B: the files on disk are compared and HEAD is named as cut-off. A dirty or stale checkout (the local lakeswitch `main` stood 87 commits behind) then yields a report whose named commit does not describe what was compared. On a case-insensitive filesystem the kit's `.github/pull_request_template.md` also reads as present and different, because lakeswitch holds `.github/PULL_REQUEST_TEMPLATE.md`; reading A says missing. | Opus | in spec — named committed target state and exact case-sensitive paths (Terms; AC 8, 22) | — |
| F-7 | MAJOR | SPEC | base | `spec.md`, AC 1, 3, 13; `scripts/kit/manifest.yaml:130–132`; `decisions/gates.yaml:181–188` | [GAP] `.github/workflows/ci.yml` stays `mechanismus` and is generated from the gate file, which AC 3 turns into a target-owned template with a reduced initial list. AC 1 then puts the source's workflow, derived from the source's 21 gates with tracker hydration, into a target whose gate file generates a different one. A `ci-drift` gate is red there, and a target that regenerates the file has changed a kit path locally, so AC 13 reports it on every update. The spec does not say what role the derived workflow has or who produces it in a target. | Opus | in spec — CI is derived from target gates, never installed as source bytes (Terms; AC 19) | — |
| F-8 | MAJOR | SPEC | base | `spec.md`, AC 22, AC 23, Non-goals ("portable baseline"); `scripts/verify_all.sh:92–93`; `scripts/kit/probe.py:92–189` | [GAP] What the "portable baseline" of the initial gate list contains is nowhere stated, so AC 23 cannot go red for a thin list: `verify_all.sh` rejects only an empty one, and a list of one always-green gate passes the criterion. The builder has to decide at least whether a new instance's `make verify` runs the 20 kit tests AC 1 installs. `probe.py` records 38 of their cases as red outside this repository (`REIST_NICHT`, cap 38), so `pytest tests/` as a gate is red in the target unless something deselects them. AC 23 also leaves open the git state it runs in: AC 22 forbids staging, so verification always sees an untracked payload, and "bare" does not say whether HEAD exists. | Opus | in spec — committed fresh target, untracked payload and exact portable gate/test baseline (AC 5, 17–18) | — |
| F-9 | MAJOR | SPEC | base | `spec.md`, AC 6, Open decisions (second [DETAIL]); `decisions.md`, Q-2 | [GAP] AC 6 requires the lock to identify the source repository without saying by what: a local checkout path (machine-specific, and committed into the target with the lock), a remote URL or a name. Q-2 has update fetch the new version, which needs a fetchable address; the [DETAIL] on transport leaves it open. Also unstated: whether update or report accept a source whose identity differs from the recorded one (a fork, a moved clone). The lock is the file lakeswitch-ai plans under the same name and ADR 0018 binds, so the choice is hard to revise once instances carry it. | Opus | in spec — origin URL/full commit; source migration deferred to update (Terms; AC 7, 10; Non-goals) | — |
| F-10 | MAJOR | SPEC | base | `spec.md`, AC 3, Definition of Done; `scripts/kit/probe.py:189,290–316`; `tests/test_pr_templates.py:19`; `tests/test_ci.py:355,756` | [GAP] AC 3 moves three paths out of `mechanismus`, and the spec says nothing about the probe behind the floor gate `leerprobe`. `probe.py` knows two roles (`nach_rolle`) and copies only `mechanismus` into its throwaway tree (`_baue`). Without `decisions/gates.yaml`, `ruff.toml` and the decision template there, travelling tests that read them without a skip turn red in the probe (`tests/test_pr_templates.py` reads `decision.md`; `tests/test_ci.py` reads the gate file and `ruff.toml`). The builder must decide whether the probe tree receives templates, and with which bytes, or whether `REIST_NICHT` grows past a cap that is only allowed to fall (`DECKEL = 38`). | Opus | in spec — probe carries original templates and derives CI without new exceptions (AC 21) | — |
| F-11 | MINOR | SPEC | base | `spec.md`, Terms "Fresh target", AC 5, 9, 21 | [GAP] Install against a target that already holds `harness.lock.yaml` has no criterion: Terms exclude it from "fresh", AC 5 speaks of an unpinned target only and AC 9 of update only. Refusing, behaving as update and restoring missing files are all open. The case arises after any install whose verification failed, because AC 21 leaves lock and files in place and a second install meets a pinned target. | Opus | in spec — any existing lock refuses install, including after failed verification (AC 5, 15) | — |
| F-12 | MINOR | SPEC | base | `spec.md`, AC 1, AC 6; `scripts/kit/manifest.yaml:25–28`; `scripts/kit/probe.py:314–316` | [GAP] The manifest's `geruest_ordner` (`plans/changes`, `plans/changes/archive`, `plans/specs`), folders the target needs to hold empty, appear in no criterion. AC 1 and AC 6 speak of files. Whether install creates the folders, with which placeholder (the probe writes `.gitkeep`), and whether that placeholder is kit-owned, target-owned or unrecorded has to be invented. | Opus | in spec — empty scaffold placeholders are recorded as kit-owned (AC 7, 20) | — |
| F-13 | MINOR | SPEC | base | `spec.md`, AC 13, 16, 20, 21 | [GAP] The result of an update that applied safe files, left conflicts and passed `make verify` is not stated: AC 13 and 16 say "reports", and AC 21 defines failure for verification only. The tests for AC 13 and 16 must assert a return value, and a caller reading only that value cannot tell a complete pin from a partial one. | Opus | in spec — partial-update result deferred by Q-6 (Non-goals; follow-up coding-harness-66q) | — |
| F-14 | MINOR | SPEC | base | `spec.md`, AC 19, Non-goals (crash recovery) | AC 19 cannot go red beyond what the implementation chooses to catch: "handled" puts any uncaught failure outside the criterion by its own wording, while the refutation speaks of "an injected write failure" without limit. Not stated: which steps count (replacing a file, deleting a retired one, changing a mode, creating a directory, writing the lock) and whether directories created for the payload belong to the restored state. | Opus | in spec — explicit write/mode/directory/lock failure boundary and complete rollback (AC 12) | — |
| F-15 | MINOR | SPEC | base | `spec.md`, AC 20, AC 23; `scripts/verify_all.sh:28–43`; `scripts/kit/probe.py:330–334` | [GAP] AC 20 fixes the working directory of the target's `make verify`, not its environment. `verify_all.sh` honours and exports `$PYTHON`, and the probe strips `BEAD_RENDER` before it runs a foreign tree so that tree cannot see this repository's tracker. An integration run started from this repository's own `make verify` hands both to the target, so AC 23's "without source tracker data" can be green on the source's interpreter and tracker render. | Opus | in spec — target verifier receives neither source override (AC 14, 17) | — |

Stage-2 call, 2026-10-13: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1038 commits, 12 rules.

> Attempt 1 (codex) failed its call: codex call failed: exit 1
>
> The runner put back:
> - `docs/adr/0018-pinned-kit-install-and-update.md`
> - `plans/changes/kit-install/design.md`
> - `plans/changes/kit-install/plan.md`
> - `plans/changes/kit-install/research.md`
> - `plans/changes/kit-install/spec.md`

Stage-2 call, 2026-10-13: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 416 files, 1042 commits, 12 rules.

> Attempt 2 (codex-repair) failed its call: codex call failed: exit 1

Stage-2 call, 2026-10-13: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 416 files, 1042 commits, 12 rules.

> Attempt 3 (glm) failed its call: claude call failed: exit 1

Stage-2 call, 2026-10-14: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 416 files, 1064 commits, 12 rules.

## Phase-2a incorporation — 2026-10-14

The reviewer's finding text is unchanged. F-1, F-2, F-6 to F-12, F-14 and
F-15 are incorporated into the revised spec with explicit refuting cases;
F-3, F-4, F-5 and F-13 are closed for this change by its explicit update
non-goal, as the maintainer requested in Q-6, and remain inputs to the update
follow-up. The Status cells name their destinations. The revised spec, not
these historical rows or their former criterion numbers, is the phase-4/6
yardstick. No maintainer answer or ADR-answer file was written here.
