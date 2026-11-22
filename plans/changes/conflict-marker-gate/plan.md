---
title: "Plan — conflict-marker-gate"
status: draft
implementation_status: none
date: 2026-11-05
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-i76l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, gate, merge]
---

# Plan — conflict-marker-gate

```text
For you:     Verification blocks conflict markers in tracked text; the existing main-merge helper stops with the conflicting paths.
Done when:   Offline Git tests prove marker detection and safe merge refusal, the gate runs locally and in CI, and make verify is green.
Appetite:    2 hours of phase 4 including repairs; stop at the limit.
Not now:     Git hooks, push interception, automatic conflict resolution or a second merge helper.
Pre-mortem:  suppose it failed: most likely because checking only a diff misses markers already committed in a clean tree.
Starts unless you say stop.
```

Implements `spec.md`, criteria 1–9; bounded, no design or ADR due.
Revised 2026-11-22 after two phase-2a rounds: findings S-1 to S-5 (terms,
criteria 4, 6, 7, the new criterion 9) and S-6 to S-8 (the Unchanged term,
criteria 2, 4 and 7, no doctrine edit) are worked into `spec.md`.
Explore used Stage 2, GLM 5.3 Flash, on 2026-11-05; no Stage-1 fallback.

## Files and steps

1. **Implementation attempt — create `tests/test_check_conflict_markers.py`:**
   add the ledger's tests against disposable real Git repositories, with
   passing controls before each planted fault. Parameterize all three
   marker prefixes, suffix/no suffix/longer markers, source/docs/plans,
   fenced examples, CRLF, non-UTF-8 text and committed-clean versus dirty
   states. Check multiple paths and line numbers, unchanged HEAD, staged
   entries (`git ls-files -s`) and file bytes — a refreshed index stat
   cache is not a change — staged and unstaged whitespace (also a restored
   working file), binary/untracked/deleted/symlink/submodule cases, exact
   fixture matching, an allowlist entry naming an untracked or absent
   path, and Git/read failures; prove the whitespace verdict cannot be
   changed by a hostile global or system Git configuration
   (`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` pointing at a file that
   disables a whitespace rule) or by attribute sources outside the
   repository (`core.attributesFile` naming a file with `*  -whitespace`
   for every path, and a system attributes file). Construct data in
   temporary directories, so no marker-bearing fixture file needs
   committing. Execute the CLI for the mutation proof, with a literal
   `scripts/check_conflict_markers.py` path visible to the existing
   mutation-evidence analyzer.
2. **Implementation attempt — create `scripts/check_conflict_markers.py`:**
   expose `--root` (default repository root), with no skip flag; enumerate
   tracked modes using NUL-delimited Git output and argument arrays. Scan
   present regular-file bytes for column-one prefixes `<<<<<<<`, `=======`,
   `>>>>>>>`; NUL means binary, not failed decoding. Never follow symlinks,
   submodules or parent symlinks outside the root. Use an exact
   relative-path fixture allowlist — a module-level constant, initially
   empty — shared by scanning and diff pathspec exclusions; tests inject a
   named exception without broadening production defaults, and an entry
   naming no tracked path is itself a finding. Run `git diff --check` and
   `git diff --cached --check` from the root over the same
   exception-filtered paths, each invocation carrying a fixed
   `core.whitespace` rule set (`-c
   core.whitespace=blank-at-eol,blank-at-eof,space-before-tab`), an empty
   `core.attributesFile` (`-c core.attributesFile=`) and
   `GIT_ATTR_NOSYSTEM=1` in its environment, so neither global and system
   configuration nor attribute sources outside the repository can change
   the verdict, with external diff/textconv disabled. Collect all marker
   locations, preserve Git diagnostics, and report inspection/read
   failures as failures, never empty success. Use `_verdict` BLOCK/exit 2
   for findings and measurement errors, exit 0 for a measured pass; leave
   file bytes, staged entries and refs unchanged — a refreshed index stat
   cache is not a modification.
3. **Implementation attempt — change `tests/test_pr_sync.py`:** extend
   `test_other_conflicts_preserve_target` to conflict in two ordinary files
   and assert both paths, nonzero exit, unchanged HEAD, staged entries
   (`git ls-files -s`), both working files, the generated index and the
   branch on origin, allowing local remote-tracking refs to move by the
   fetch and a refreshed index stat cache. Keep using
   `python3 scripts/pr_sync.py merge-main --root .`; production helper code
   already meets the approved requirement. Retain its clean/index-only tests.
4. **Implementation attempt — change `scripts/kit/manifest.yaml`:** classify
   the new scanner and test file as `mechanismus`, with reasons, so they
   travel with the gate list; no new portability exemption or dependency.
5. **Orchestrator bootstrap after the accepted attempt — held files:** add
   `conflict-markers` to `decisions/gates.yaml`, command
   `python3 scripts/check_conflict_markers.py`, job `verify`, cost
   `seconds`, enforcement `block`, placement `both`, subset `docs`,
   `floor: false`, without tracker or history requirements. Regenerate
   `.github/workflows/ci.yml` with
   `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`.
   The attempt must not edit either held path. The declared command and
   cost class are the spec's (criterion 6), so the attempt's wiring test
   and this entry agree by construction. Do not add a temporary
   caller/mutation exemption to hide the not-yet-registered gate; final
   caller, CI-drift and wiring verification needs the combined bootstrap tree.
6. **Orchestrator — change `docs/governance/gate-catalog.md`:** replace only
   its generated inventory block with `python3 scripts/ci_gates.py --catalog`
   output and refresh `updated`; retain the enabling checklist. The counter
   proof is the ledger's committed-marker test; criterion 1's stock query
   found no raw prefix hits at `2d4b1a3d` on 2026-11-05, so no ramp is needed.
   **Change `plans/changes/conflict-marker-gate/plan.md` and
   `plans/changes/conflict-marker-gate/findings.md`:** update ledger states,
   phase-4 time and evidence; regenerate `plans/INDEX.md` with
   `python3 scripts/plans_registry.py --index`. Publish as a decision pull
   request because the gate list is human-decided: title
   `decide(conflict-marker-gate): block conflict markers in tracked text`,
   label `decision`, body from `.github/PULL_REQUEST_TEMPLATE/decision.md`,
   naming the conflict-marker gate task (coding-harness-i76l). No ADR answer.

## Not touched

No deletions. Keep `scripts/pr_sync.py`, its fence-aware renderer validation,
`scripts/stage2.py`, `scripts/ci_gates.py`, the Makefile, `provenance.yaml`,
`docs/WORKFLOW.md`, prompts, templates, ADRs, endpoints, installed configuration,
tracker data and sibling repositories unchanged. The generated-index-only
merge exception remains; no blanket test-directory or Markdown-fence exception
is introduced in the new gate.

## Verification

Run the planted gate tests before the scanner edit to record red, then:

```sh
python3 -m pytest tests/test_check_conflict_markers.py tests/test_pr_sync.py -q
```

After orchestrator bootstrap, verify wiring, catalog and kit, then the full tree:

```sh
python3 scripts/check_conflict_markers.py
python3 scripts/ci_gates.py --check-ci
python3 -m pytest tests/test_ci.py tests/test_gate_catalog.py tests/test_kit.py -q
python3 scripts/kit/probe.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_check_conflict_markers.py::test_gate_goes_red_when_committed_text_contains_markers — any approved marker prefix in an otherwise clean committed tree passes
- 2: not yet written tests/test_check_conflict_markers.py::test_reports_all_marker_locations_without_writes — a path or line number is omitted, or checking changes file bytes, staged entries or refs (a refreshed stat cache is not a change)
- 3: not yet written tests/test_check_conflict_markers.py::test_only_tracked_text_and_exact_fixture_names_are_measured — a binary/untracked/exact fixture is rejected or a sibling fixture name bypasses scanning
- 4: not yet written tests/test_check_conflict_markers.py::test_gate_goes_red_when_git_diff_check_finds_a_fault — staged or unstaged whitespace is ignored, including staged-only damage; the verdict follows the invoking user's Git configuration or attribute files outside the repository
- 5: not yet written tests/test_check_conflict_markers.py::test_gate_goes_red_when_inspection_cannot_complete — a failed Git command or unreadable tracked file yields success
- 6: not yet written tests/test_check_conflict_markers.py::test_gate_is_blocking_in_every_verification_path — the declared command, enforcement, placement, cost class or docs membership differs, or derived commands/workflow omit it
- 7: tests/test_pr_sync.py::test_other_conflicts_preserve_target — an ordinary conflict succeeds, omits paths or changes the branch, staged entries, generated index, checkout or the branch on origin
- 7: tests/test_pr_sync.py::test_index_only_conflict_is_regenerated — the existing generated-index exception stops working
- 8: not yet written tests/test_check_conflict_markers.py::test_gate_and_tests_travel_with_the_kit — either new path is absent from the mechanism copy
- 8: not a test — python3 scripts/kit/probe.py exercises the isolated copy; a new failure caused by the scanner or its tests refutes portability
- 9: not yet written tests/test_check_conflict_markers.py::test_gate_goes_red_when_an_allowlist_entry_names_no_tracked_path — a stale or pre-registered allowlist entry is silently ignored

## Time used

2026-11-22 15:50:28–15:56:17 UTC, 349 s — draft · attempt 3 · route glm · model glm-5.3 · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-22 18:26:29–18:32:00 UTC, 331 s — draft · attempt 3 · route glm · model glm-5.3 · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
