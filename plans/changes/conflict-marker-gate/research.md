---
title: "Research — conflict-marker-gate"
status: draft
implementation_status: none
date: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-i76l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# conflict marker gate — Research

Stage-2 call, 2026-11-05: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 901 files, 3333 commits, 12 rules.

## Runner exploration — 2026-11-05

Exploration complete. Here is the research, ready to append to `plans/changes/conflict-marker-gate/research.md` (the runner owns the file; I have written nothing).

---

## Research findings — conflict-marker-gate (phase 1, GLM 5.3 Flash, 2026-11-05, worktree `conflict-marker-gate` at branch `fix/conflict-marker-gate`)

### What exists today

**No gate measures conflict markers today.** `decisions/gates.yaml` — "THE ONE LIST" (D-10/O-4, bead coding-harness-bo0), the artefact every runner derives from — contains no entry whose id, title, command or reason names conflict markers. Its gate ids are: pytest, ruff-check, ruff-format, leerprobe, plans-registry, docs-links, frontmatter-current, bead-export, dangling-beads, decision-continuity, adr-answers, interview-minimums, question-context, criterion-ledger, research-handoff, guard-test-environment, gate-schema, ci-drift, ramp-valves, ruleset, markdownlint, lychee, plans-registry-strict, research-currency. This is "not there", verified by reading the whole file, not only by grep.

**Detection exists at exactly one place in code.** `scripts/pr_sync.py`, `_validate()` ("Every artefact the renderer consumes has readable frontmatter and no unresolved conflict markers; otherwise the run refuses to render"): it walks every `plans/**/*.md` in the mirror (skipping `INDEX.md` and `_`-prefixed files), requires readable frontmatter, and raises `Failed("{rel}: unresolved conflict markers")` when a line starts `<<<<<<< ` or `>>>>>>> ` (each with a trailing space) outside a fenced code block. The scan is fence-aware — ` ``` `/`~~~` toggling, with the comment "A marker quoted in a fenced example is text, not a conflict (review row L1-11)". Only the two angle-bracket markers are checked; `=======` and `|||||||` are not checked anywhere in the tree.

**That detection guards one path only.** `_validate` runs inside the sync/render flow of `pr_sync.py` (`run()` → validate before render). A file carrying conflict markers anywhere else — `docs/`, `scripts/`, `templates/`, a non-plans path, or a `plans` file committed outside a sync run — reaches no gate. A repo-wide ripgrep over `conflict[ -]marker|<<<<<<<|>>>>>>>` matched 11 files: `scripts/pr_sync.py`, `tests/test_pr_sync.py`, the `index-merge-regenerates` change artefacts, the archived `2026-09-30-template-bundle` artefacts, `docs/research/2026-09-16-review-corpus-vs-running-workflow.md` (D-4, "an export that never carries conflict markers" — about the tracker JSONL export, a different subject), `plans/INDEX.md` (this change's own row) and this research file. No other scanner exists.

**Indirect, partial detection through the registry gate.** `scripts/plans_registry.py` `check()` reports BLOCK "{rel}: no readable frontmatter" for a held artefact whose YAML frontmatter is unreadable — which is how an artefact torn open by conflict markers usually surfaces — but nothing in `plans_registry.py` names or detects conflict markers as such (grep over `conflict|marker` in that file matched neither word). The neighbour research already observed this: during a merge with unresolved markers in a sibling artefact, that artefact reports "no readable frontmatter" and the regenerate step presupposes real conflicts resolved first (`plans/changes/index-merge-regenerates/research.md`, "The generator and its guard").

**The merge machinery knows git conflicts, not text markers.** `scripts/pr_sync.py` `merge_tree()` runs `git merge-tree --write-tree -z` and reports conflicted paths; the supported local merge `python3 scripts/pr_sync.py merge-main --root .` and the on-request `sync` resolve an index-only conflict by regenerating `plans/INDEX.md` and refuse a conflict outside the index, reporting its paths (docs/WORKFLOW.md §3 "Pull requests stay mergeable", bullets "Synced on request, by the helper" and "Generated files are regenerated"; bead coding-harness-eq6y, coding-harness-hfsz; criteria 1–4 of `plans/changes/index-merge-regenerates/spec.md`). This measures a conflict at merge time; it measures no tree that already carries markers — for example a commit made by hand or through GitHub's server-side merge buttons, which the same spec's non-goals state cannot run the helper ("the unchanged registry gate remains their backstop" — and the registry gate detects markers only indirectly, as above).

**Tests holding the existing detection.** `tests/test_pr_sync.py`: `test_a_fenced_conflict_marker_does_not_refuse_the_render` (row L1-11; planted fault: a marker quoted in a fenced example refused every merge), the `feat/markers` fixture that commits and pushes an artefact carrying `<<<<<<< ours` and expects the render refusal, `test_index_only_conflict_is_regenerated` (asserts no `<<<<<<<` in the merged result), `test_other_conflicts_preserve_target`, and `test_sync_reports_conflicting_paths_without_push`.

**Precedent for counting markers per file in a tree.** The archived template-bundle change used hunk counts — "conflict markers per file in the tree that `git merge-tree --write-tree` prints" — as its criterion-64 evidence (`plans/changes/archive/2026-09-30-template-bundle/plan.md`, review row 6-11: 3 hunks in `docs/WORKFLOW.md`, 2 in `scripts/kit/probe.py`, 1 in `plans/INDEX.md` at `8822677`). Per-file marker counting over a tree is an established measurement style here.

**Scope-relevant stock measurement.** No tracked line consists of seven or more equals signs (ripgrep `^={7,}` over the worktree: no matches), so a `=======` middle-marker rule would hit no legitimate setext heading in today's stock. The existing detector's trailing-space spelling (`<<<<<<< ` / `>>>>>>> `) matches what Git writes for a conflicted file's side labels.

**The gate machinery a new gate must enter** (facts, not choices):

- One list, one reader, two derived artefacts: `decisions/gates.yaml` is read only by `scripts/ci_gates.py`; `.github/workflows/ci.yml` is generated (`--generate-ci`) and held by the `ci-drift` gate (`--check-ci`); the readable inventory `docs/governance/gate-catalog.md` is regenerated (`--catalog`) and held by `tests/test_gate_catalog.py` (`test_catalog_matches_declared_gates`, `test_catalog_drift_is_rejected` — a row missing, extra, duplicated or changed in any displayed field fails the suite).
- Schema (`decisions/gates.yaml` header comment): `id`, `title`, `command`/`action`, `job` (verify|drift), `enforcement` (advisory|report|block), `floor`, `placement` (hosted|writer|both), optional `needs_tracker`, `needs_history`, `subsets` (e.g. `docs`), `reason`.
- The enabling checklist "sensible, proportionate and more than an end in itself" stands once, in `docs/governance/gate-catalog.md` §"Before enabling a gate", pointed to from `docs/WORKFLOW.md` ("A gate is sensible, proportionate and more than an end in itself"); "proportionate" names report/advisory as the honest level while a finding stock is not cleared, citing `docs-links` and `markdownlint` as gates living at that level. It also states: what refutes a gate is the counter-check that plants the fault and shows the run going red.
- Mutation evidence: `tests/test_ci.py::test_every_gate_step_has_a_mutation_test` demands a `*_goes_red_when_*` test for every new gate, or an entry in `OHNE_MUTATIONSTEST` — a ratchet that "may shrink, never grow", capped at 12 by `test_the_mutation_exemption_list_only_shrinks` (7 entries today, so a new gate cannot take an exemption without approaching the cap; a third-party-tool entry would not fit a self-built scanner).
- Script coverage: `tests/test_ci.py::test_every_script_has_a_test_or_a_declared_reason` demands a test that imports or starts a script, or a line in `OHNE_TEST` (`scripts/ci_gates.py`, currently an empty dict).
- Makefile: `tests/test_ci.py::test_the_makefile_runs_what_the_one_list_runs` pins only the two deliberately duplicated commands (`make test`, `make staleness`) as whole recipe lines; a new gate command needs no Makefile target, and the Makefile header forbids restating gate commands.
- Local runner: `scripts/verify_all.sh` holds no commands of its own; it asks `ci_gates.py --commands --job … --placement lokal|ci` and respects the enforcement vocabulary (only `block` turns the run red).
- Verdict vocabulary: `scripts/_verdict.py` — INFO (exit 0, nobody blocks), DRIFT (exit 1, only `--strict`), BLOCK (exit 2, always); BLOCK is for contradictions whose both sides move by commit in this repo, DRIFT for a side that moves without a commit here. Every sibling `check_*.py` uses it. `Ramp` exists for a new check that would raise half the stock red on day one (used by `plans_registry.py` ramps; the `ramp-valves` gate turns due transitions loud) — the arming pattern for a block gate over an existing tree.
- Kit travel: `scripts/kit/manifest.yaml` carries the gate machinery to new repositories — `scripts/ci_gates.py`, `scripts/verify_all.sh`, `scripts/verify_lock.py`, the `check_*` scripts (`check_docs.py`, `check_frontmatter_current.py`, `check_guard_test_environment.py`, `check_research_currency.py`, `check_adr_answers.py`, `check_criterion_ledger.py`, `check_research_handoff.py`, `check_interview_minimums.py`, `check_question_context.py`, `check_bead_export.py`, `check_dangling_bead_ids.py`, `check_decision_continuity.py`), `decisions/gates.yaml` ("die EINE Gate-Liste … reist mit"), `.github/workflows/ci.yml` (travels paired with the gate file "sonst driftet die Kopie"), and `docs/governance/gate-catalog.md`/`quality-gates.md`. A new gate script therefore raises the kit question: travel as a manifest entry, or stay `bestand` (named but not carried).
- Naming convention: every self-built check script sits directly in `scripts/` as `check_<subject>.py` with a `tests/test_check_<subject>.py` beside it (manifest and tests layout).

### Where it lives

- The one gate list: `decisions/gates.yaml`; its reader `scripts/ci_gates.py`; derived `ci.yml` and `docs/governance/gate-catalog.md`; local runner `scripts/verify_all.sh` (under the machine-wide admission `scripts/verify_lock.py`).
- Existing conflict-marker detection: `scripts/pr_sync.py` `_validate` (fence-aware scan, plans-only), `merge_tree` (git conflicts); its tests in `tests/test_pr_sync.py`.
- Indirect detection: `scripts/plans_registry.py` `check()` ("no readable frontmatter" BLOCK rows).
- Doctrine: `docs/WORKFLOW.md` §3 "Pull requests stay mergeable" (sync, `merge-main`, "Generated files are regenerated"); enabling checklist `docs/governance/gate-catalog.md` §"Before enabling a gate"; kit copies `templates/agents-mergeable-prs.md` (per the neighbour research).
- Verdict and ramp vocabulary: `scripts/_verdict.py`; ratchets `tests/test_ci.py` (`OHNE_MUTATIONSTEST`, script-coverage and Makefile pins), `scripts/ci_gates.py` (`OHNE_TEST`).
- Kit manifest: `scripts/kit/manifest.yaml`.
- This change: `plans/changes/conflict-marker-gate/research.md` only (skeleton, bead coding-harness-i76l, status draft, implementation none, opened by commit `a67d427c`); no `spec.md`, `decisions.md`, `plan.md` or `design.md` exists in the folder yet.

### What is unclear about it

- **The bead's content is not read.** `coding-harness-i76l` appears in the tree only twice (`plans/INDEX.md` row, the research frontmatter). Tracker state lives in the Dolt database rendered only through `scripts/bead_render.py` (house rule 2; `.beads/` carries config, metadata and interactions only), and a read-only explorer runs no command. The bead's description — its stated class, appetite and scope — is unknown; the change name in the branch and folder is the only stated intent. Interview question (`[DECISION]`).
- **Scope is unstated in the tree.** Whole tracked tree vs `plans/` only vs docs-only; which markers (`<<<<<<< `/`>>>>>>> ` only, as today's detector, or also `=======`/`|||||||`); binary and non-UTF-8 files (today's scanner reads `encoding="utf-8"` and refuses on `UnicodeDecodeError`); enforcement level (block vs report — the proportionality checklist); job and placement. The machinery facts are above; the appetite is not in the tree. Interview questions.
- **Kit travel is undecided by any artefact.** The manifest carries every check script today, but whether a tree-wide marker scan is framework-general or repository-specific is nowhere written. Interview question.
- **No shared scanner exists.** The fence-aware loop is embedded in `_validate` inside `pr_sync.py`; whether a new gate reuses it, extracts it, or stands alone is a design question the tree does not answer (it names no second consumer). Left to phase 2.
- **"Not found" vs "not there".** `tests/` was grepped, not exhaustively read; the statements above name greps and files actually read. The whole-tree `^={7,}` measurement covers the worktree ripgrep sees (tracked tree, `.gitignore` respected).

### Which files a change would have to touch

By today's facts, the candidates are: a new `scripts/check_*.py` (sibling naming convention) or an extension of an existing scanner; `decisions/gates.yaml` (a new entry in the one list); `.github/workflows/ci.yml` (regenerated by `--generate-ci`, never hand-edited — the `ci-drift` gate holds it); `docs/governance/gate-catalog.md` (regenerated inventory via `--catalog`); `tests/` — the gate's `*_goes_red_when_*` mutation test and a test file for the new script (`test_every_script_has_a_test_or_a_declared_reason` and `test_a_mere_mention_does_not_count_as_a_test` set the yardstick); possibly `scripts/kit/manifest.yaml` (with the gates.yaml/`.github` pairing rule if it travels); `docs/WORKFLOW.md` and/or `templates/` only if doctrine wording moves; `plans/INDEX.md` is output, regenerated, never edited; plus this change's own artefacts (`spec.md` and later files under `plans/changes/conflict-marker-gate/`). The Makefile needs no change (the duplication pin names exactly two commands).

### Suggested `neighbours:` header value

`plans/changes/index-merge-regenerates/spec.md`, `plans/specs/implementation-verification/spec.md`, `plans/changes/archive/2026-09-30-template-bundle/spec.md`, `plans/changes/dirty-index/spec.md`, `plans/changes/ledger-marker/spec.md`

Grounds: `index-merge-regenerates` (bead coding-harness-njtm) owns the supported merge, `merge_tree` and the `_validate` render refusal; `implementation-verification` (living spec, bead coding-harness-mfv) holds the runner's regenerate-before-verify contract, the other place a marker-torn artefact surfaces; `2026-09-30-template-bundle` (archived) carries the merge-tree marker-counting precedent; `dirty-index` (bead coding-harness-0c8) and `ledger-marker` (bead coding-harness-7g6h) share the words "index" and "marker" but are different subjects (the git index in `stage2.changed_paths`; criterion-ledger `not yet written` markers) — named so the spec can state the difference.
