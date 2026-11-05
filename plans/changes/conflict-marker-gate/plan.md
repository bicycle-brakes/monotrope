---
title: "Plan — conflict-marker-gate"
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
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-05"}
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

Implements `spec.md`, criteria 1–8; bounded, no design or ADR due.
Explore used Stage 2, GLM 5.3 Flash, on 2026-11-05; no Stage-1 fallback.

## Files and steps

1. **Implementation attempt — create `tests/test_check_conflict_markers.py`:**
   add the ledger's tests against disposable real Git repositories, with
   passing controls before each planted fault. Parameterize all three
   marker prefixes, suffix/no suffix/longer markers, source/docs/plans,
   fenced examples, CRLF, non-UTF-8 text and committed-clean versus dirty
   states. Check multiple paths and line numbers, unchanged HEAD/index/file
   bytes, staged and unstaged whitespace (also a restored working file),
   binary/untracked/deleted/symlink/submodule cases, exact fixture matching,
   and Git/read failures; construct data in temporary directories, so no
   marker-bearing fixture file needs committing. Execute the CLI for the
   mutation proof, with a literal `scripts/check_conflict_markers.py` path
   visible to the existing mutation-evidence analyzer.
2. **Implementation attempt — create `scripts/check_conflict_markers.py`:**
   expose `--root` (default repository root), with no skip flag; enumerate
   tracked modes using NUL-delimited Git output and argument arrays. Scan
   present regular-file bytes for column-one prefixes `<<<<<<<`, `=======`,
   `>>>>>>>`; NUL means binary, not failed decoding. Never follow symlinks,
   submodules or parent symlinks outside the root. Use an exact relative-path
   fixture allowlist, initially empty, shared by scanning and diff pathspec
   exclusions; tests inject a named exception without broadening production
   defaults. Run `git diff --check` and `git diff --cached --check` from the
   root over the same exception-filtered paths, with external diff/textconv
   disabled. Collect all marker locations, preserve Git diagnostics, and
   report inspection/read failures as failures, never empty success.
   Use `_verdict` BLOCK/exit 2 for findings and measurement errors, exit 0
   for a measured pass; do not modify files, the index or refs.
3. **Implementation attempt — change `tests/test_pr_sync.py`:** extend
   `test_other_conflicts_preserve_target` to conflict in two ordinary files
   and assert both paths, nonzero exit, unchanged HEAD, Git index bytes,
   both working files, generated index and remote branch. Keep using
   `python3 scripts/pr_sync.py merge-main --root .`; production helper code
   already meets the approved requirement. Retain its clean/index-only tests.
4. **Implementation attempt — change `scripts/kit/manifest.yaml`:** classify
   the new scanner and test file as `mechanismus`, with reasons, so they
   travel with the gate list; no new portability exemption or dependency.
5. **Orchestrator bootstrap after the accepted attempt — held files:** add
   `conflict-markers` to `decisions/gates.yaml`, command
   `python3 scripts/check_conflict_markers.py`, job `verify`, enforcement
   `block`, placement `both`, subset `docs`, `floor: false`, without tracker
   or history requirements. Regenerate `.github/workflows/ci.yml` with
   `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`.
   The attempt must not edit either held path. Do not add a temporary
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
- 2: not yet written tests/test_check_conflict_markers.py::test_reports_all_marker_locations_without_writes — a path or line number is omitted or checking changes repository state
- 3: not yet written tests/test_check_conflict_markers.py::test_only_tracked_text_and_exact_fixture_names_are_measured — a binary/untracked/exact fixture is rejected or a sibling fixture name bypasses scanning
- 4: not yet written tests/test_check_conflict_markers.py::test_gate_goes_red_when_git_diff_check_finds_a_fault — staged or unstaged whitespace is ignored, including staged-only damage
- 5: not yet written tests/test_check_conflict_markers.py::test_gate_goes_red_when_inspection_cannot_complete — a failed Git command or unreadable tracked file yields success
- 6: not yet written tests/test_check_conflict_markers.py::test_gate_is_blocking_in_every_verification_path — the declared command, enforcement, placement or docs membership differs, or derived commands/workflow omit it
- 7: tests/test_pr_sync.py::test_other_conflicts_preserve_target — an ordinary conflict succeeds, omits paths or changes the branch, index, checkout or remote
- 7: tests/test_pr_sync.py::test_index_only_conflict_is_regenerated — the existing generated-index exception stops working
- 8: not yet written tests/test_check_conflict_markers.py::test_gate_and_tests_travel_with_the_kit — either new path is absent from the mechanism copy
- 8: not a test — python3 scripts/kit/probe.py exercises the isolated copy; a new failure caused by the scanner or its tests refutes portability

## Time used
