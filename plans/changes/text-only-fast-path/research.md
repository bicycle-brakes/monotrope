---
title: "Research — text-only-fast-path"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-is4h
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# text only fast path — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1149 files, 5156 commits, 12 rules.

## Runner exploration — 2026-11-21

The research is complete. Here is the report, ready to append to `plans/changes/text-only-fast-path/research.md`.

---

## What exists today

**The rule is prose, three times, with no code behind it on the direct path.** `AGENTS.md` ("A text-only change", lines 154–155) states: a text-only change — Markdown outside `scripts/`, `tests/`, `prompts/`, `decisions/` — skips the local `make verify`; CI is its gate. `docs/testing.md` ("Where tests run", closing lines 72–73) states the same rule in the same words. `README.md` ("Contributing", line 305) says "a text-only change is gated by CI". House rule 9 (`AGENTS.md:82-87`, maintainer 2026-11-16) names "the text-only verify skip" as a maintainer-decided variant that must live as "a declared parameter inside that path, never a second route beside it", carried by code at one choke point, and states: "A rule of this kind takes hold through a check that goes red, not through prose." No ADR carries the rule — a Grep over `docs/adr/*.md` for "text-only|Markdown outside" matches only `docs/adr/0015-glm-5-3-repairs-taken-findings.md` ("text-only findings repaired too", line 29), which is about findings repair, and `decisions/answers/` holds no answer directory for a verify-skip topic (Glob listing).

**The verify path has no diff-awareness.** `make verify` delegates to `scripts/verify_all.sh` (`Makefile:18-19`), which execs the shared two-phase scheduler `scripts/verify_run.py` (comment block, verify_all.sh:9–15), and both read the one gate list `decisions/gates.yaml` through `scripts/ci_gates.py` (D-10/O-4, gates.yaml header lines 1–8). A Grep over `scripts/verify_run.py` for diff/markdown/text-only finds only the tree-stability snapshot machinery (the snapshot-difference helper at line 180 and the instability checks at lines 883–953) — no path filter, no text-only skip. Not found: any implementation of the AGENTS.md sentence in `verify_all.sh`, `verify_run.py` or `ci_gates.py`. The `docs` job already exists as machinery (`verify_all.sh --job docs`, "only the document gates", verify_all.sh:20; the `subsets` schema, gates.yaml lines 39–44), and eleven verify-job gates declare `subsets: [docs]` (plans-registry, docs-links, frontmatter-current, decision-continuity, adr-answers, interview-minimums, question-context, criterion-ledger, research-handoff, markdownlint — the last an action gate, `placement: both`, enforcement report). Gates outside the docs subset that a text-only skip would leave to CI include pytest, leerprobe, bead-export, dangling-beads, guard-test-environment, gate-schema, ci-drift and ramp-valves (gates.yaml, their entries).

**The Stage-2 runner already has three partial fast paths of its own.** First, the draft verb: `verify_draft` (`scripts/stage2.py:10444`) runs only the document gates — `document_gates()` (`stage2.py:10415`) selects verify-job local gates with `"docs" in gate["subsets"]` from `ci_gates.gates()`, "no pytest, no code or kit gate" (bead coding-harness-0swp, docstring line 10419–10420). Second, the implement/repair targeted check: `verify_attempt(mode="targeted")` → `_targeted_body` (`stage2.py:7302`) → `targeted_selection` (`stage2.py:6942`). Its per-file loop skips `.md` under `plans/` or `docs/` outright (stage2.py:6989–6990), forces the admitted full check on any other non-`.py` input kind ("an input kind the targeted selector does not cover", stage2.py:6991–6992), on a changed `prompts/` path (stage2.py:6972–6973), on `SHARED_INFRASTRUCTURE` (stage2.py:4846–4854: `scripts/ci_gates.py`, `verify_all.sh`, `verify_run.py`, `stage2.py`, `verify_lock.py`, `touch_map.py`, `leakcheck.py`) and on `conftest.py` (stage2.py:6976–6977); the document-subset gates always stand in a targeted check (stage2.py:7040–7047), and a fallback runs `full_verify` (stage2.py:7364–7371) while a targeted red never falls back (docstring, stage2.py:7433–7435). Consequence, stated as fact: the selector's Markdown exemption is narrower than the AGENTS.md wording — `AGENTS.md`, `README.md` or a `tools/**/*.md` change sends a Stage-2 attempt to the full check today, while the prose rule says such a change skips it. Third, the cheap checks: `cheap_checks` (`stage2.py:6708`) skips "a command with no target (spec, criterion 4)" — `format_targets` (`stage2.py:6366`) lists only changed `.py` under `scripts/`/`tests/`, so an md-only attempt runs no ruff, and with no selected tests no pytest (stage2.py:6743–6744); pinned by `test_empty_targets_skip_their_command` (`tests/test_stage2_fail_fast.py:215-234`, ledger 4: "a zero-target check started ruff or pytest, or rejected a text-only attempt").

**The promised stop hook is not there.** `docs/WORKFLOW.md` §3 table (line 533) names `.claude/hooks/session-stop/check-tests-green.sh` ("blocks the end of a turn on a red tree"); `prompts/05-verify.md:5-6` repeats it; `docs/testing.md:61` describes its design ("only when Python changed since `HEAD` — comfort… It is not the enforcement"). `.claude/hooks/` contains no files (Glob, no matches; `.claude/` holds `agents/`, `commands/workflow-start.md`, `settings.json`), and the installed hook sets run recap.sh on Stop (`tools/claude-code/settings.json:16-18`), no verification check. `README.md:257-260` lists the stop hook under "Not built yet". Two earlier artefacts recorded the same absence: `plans/changes/archive/2026-11-06-workflow-promises/research.md:49` and the ontology-relation-layer swarm (`plans/changes/ontology-relation-layer/research.md:46211`).

**The rule has been applied by hand, never enforced.** The archived architecture-reconcile change decided it per change (`plans/changes/archive/2026-11-06-architecture-reconcile/decisions.md:55-58`, "[DETAIL] Text only… so the local `make verify` is skipped and CI is the gate (AGENTS.md, 'A text-only change')") and restated it in `plan.md:92-93` and `spec.md:124-126`. CI-side path filters were explicitly deferred: `plans/changes/archive/2026-11-06-ci-minutes/plan.md:24` lists "path filters for text-only changes" under "Not now". The targeted-check change touched the topic again (Q-6 answer mentions "the ruff start on a text-only attempt", `plans/changes/archive/2026-11-16-targeted-check-more-verbs/decisions.md:134`), as did verify-cheap-first's scope widening (`plans/changes/archive/2026-11-16-verify-cheap-first/decisions.md:55-61`).

## Where it lives

Prose: `AGENTS.md:154-155` and `AGENTS.md:82-87` (house rule 9); `docs/testing.md:61` and `72-73`; `README.md:257-260` and `305`; `docs/WORKFLOW.md:90` (phase table: "the stop hook blocks on a red tree") and `533`; `prompts/05-verify.md:5-6`. Code: `Makefile:18`, `scripts/verify_all.sh`, `scripts/verify_run.py`, `scripts/ci_gates.py`, `decisions/gates.yaml`; `scripts/stage2.py` symbols `cheap_checks` (6708), `format_targets` (6366), `targeted_selection` (6942), `_targeted_body` (7302), `verify_attempt` (7401), `verify_draft` (10444), `document_gates` (10415), `SHARED_INFRASTRUCTURE` (4846). Tests: `tests/test_stage2_fail_fast.py:215` (ledger 4). Runner-owned prompts demanding the full check without naming the exception: `prompts/04-implement.md:10,21,25`, `prompts/04b-review-loop.md:32,105,112,115` ("one full `make verify` runs on the final head before phase 6").

## What is unclear

- Whether the fast path belongs in the local runner (`verify_all.sh`/`verify_run.py`, as a declared parameter of the one path per house rule 9), in `targeted_selection` (aligning its Markdown branch with the AGENTS.md wording), or both — and what the choke point for the hand-run `make verify` is, since today three shapes exist side by side (draft's docs gates, the targeted selector's plans/docs `.md` skip, and prose-only for direct runs).
- What "Markdown" means: only `.md`? Untracked files? Non-Markdown text under `plans/`? `targeted_selection` uses `.endswith(".md")` plus a `plans/`/`docs/` prefix (stage2.py:6989); AGENTS.md words it as "Markdown outside `scripts/`, `tests/`, `prompts/`, `decisions/`", which would include `tools/**/*.md` — the two statements disagree today, and the spec must state one meaning.
- Whether "skips the local `make verify`" covers the runner-owned full check before phase 6 (`prompts/04-implement.md:25`, `prompts/04b-review-loop.md:115` name it without the exception) and the repair path's full check.
- Whether the absent stop hook (`docs/testing.md:61` describes it as keyed on "Python changed since `HEAD`") belongs to this change or a separate one — a human question, recorded here, not decided.
- The change's class is not readable from any artefact in the tree (the folder holds only the `research.md` skeleton; the tracker is not readable in this phase); the recorded stage-2 line names "route flash", which per ADR 0020 is the bounded/spike route.
- `tests/test_stage2.py` is named by the maintainer's option A as requiring the full check until bead coding-harness-vg9 splits it (stage2.py:7025–7029) — any new test placement should note that budget remark as an existing constraint.

## Which files a change would have to touch

The verify choke point — `scripts/verify_all.sh` and/or `scripts/verify_run.py`, with `scripts/ci_gates.py` and `decisions/gates.yaml` if selection or schema support is needed (the `docs` job/subset machinery exists); `scripts/stage2.py` (`targeted_selection` lines 6989–6992, `verify_draft`/`document_gates` if the draft path is the model); tests under `tests/` following the doctrine-test and mutation-name conventions (`docs/testing.md:48-53`); prose alignment in `AGENTS.md`, `docs/WORKFLOW.md`, `docs/testing.md`, `prompts/05-verify.md`, `README.md`; `plans/INDEX.md` regenerates (`make index`), and frontmatter `updated:` dates are held by the `frontmatter-current` gate (`scripts/check_frontmatter_current.py`, gates.yaml lines 143–153).

## Neighbours (for the header)

`plans/specs/implementation-verification/spec.md` (living spec: derived-file preparation and the targeted route's duration measurement) · `plans/changes/archive/2026-11-16-verify-cheap-first/` (cheap-first scheduler, bead bxxt.6) · `plans/changes/archive/2026-11-16-targeted-check-more-verbs/` (the targeted post-run check, bead 0swp) · `plans/changes/archive/2026-11-06-ci-minutes/` (deferred path filters) · `plans/changes/archive/2026-11-06-workflow-promises/` (stop-hook absence finding) · `plans/changes/archive/2026-11-06-architecture-reconcile/` (rule applied by hand) · `plans/changes/ontology-relation-layer/research.md` (swarm flagged the stop-hook row naming an absent path).
