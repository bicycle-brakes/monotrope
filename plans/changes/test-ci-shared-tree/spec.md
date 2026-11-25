---
title: "Spec — test-ci-shared-tree"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.12
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, tests, xdist]
class: bounded
appetite: 1
adr_files: []
neighbours: []
---

# Spec — test-ci-shared-tree

The orphan-script control test runs in isolation without weakening the real script inventory checks (bead `coding-harness-bxxt.12` — isolate the shared-tree test). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-25, research found that `tests/test_ci.py::test_the_glob_itself_finds_a_real_orphan_shell_script` creates a file in the checkout's `scripts/` directory while other parallel tests enumerate it. Those tests can see the temporary orphan, and the kit probe can cache untracked files during that window (`research.md`, second runner exploration; confirmed in `tests/test_ci.py` at commit `790bf418`).

## Acceptance criteria

1. When `test_the_glob_itself_finds_a_real_orphan_shell_script` runs, it creates its orphan only in a temporary tree outside the repository checkout.
   *Refuted by:* The test creates its orphan inside the checkout, even if it later removes it.
2. When the control test runs, the real `_scripts()` glob aimed at its temporary tree and the real `_heimatlose_namen()` classification report its actual temporary `.sh` file as an orphan, using the checkout's `.github/workflows/ci.yml`, `scripts/verify_all.sh` and `OHNE_AUFRUFER` read-only.
   *Refuted by:* Removing `.sh` from `_scripts()` or treating the uncalled file as called leaves the control test green, or classification uses different caller inputs.
3. When the real inventory checks enumerate scripts, the default `_scripts()` inventory contains the checkout's top-level `*.py` and `*.sh` files except names starting with `test_`, without recursion.
   *Refuted by:* A qualifying top-level script is omitted, a non-qualifying file is included, or another tree is used by default.
4. When either real inventory test runs, it asserts that its default inventory is non-empty.
   *Refuted by:* Either inventory test passes with an empty inventory.
5. When the control test runs under a write watcher, no attempted write or creation through `Path.write_text`, `Path.write_bytes`, write-mode built-in or `io.open`, write/create-flagged `os.open`, `os.replace`, `os.rename`, `Path.touch` or `Path.mkdir` targets the repository checkout.
   *Refuted by:* Any watched operation targets the checkout, including a temporary directory outside `scripts/` or a file removed before the test ends.
6. When a planted variant of the control test writes to `scripts/` in a stand-in repository under a temporary directory, the write watcher reports it.
   *Refuted by:* The watcher misses the planted write.
7. Before the guard runs the planted variant, it asserts that the target is inside its temporary stand-in repository and outside the real checkout.
   *Refuted by:* A target in the real checkout or outside the stand-in is accepted.
8. When the control test classifies the orphan, a spy verifies the inputs are the checkout's CI workflow and runner texts and the module's `OHNE_AUFRUFER`.
   *Refuted by:* Blank or different caller inputs leave the spy check green.

## Non-goals

- Changing pytest scheduling to work stealing or parallelising the kit probe; the dependent work addresses those separately.
- Changing script inventory policy, CI configuration, or kit-probe behaviour.

## Protected areas

Production scripts, CI configuration and tracker data remain untouched: the change isolates a test, not the checks' policy or execution.

## Definition of Done

- `make verify` green.
- Documents, models and ADRs moved in the same pull request: none beyond this change's phase artifacts.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead `coding-harness-bxxt.12` — isolate the shared-tree test — and its last commit carries `Closes-Bead: coding-harness-bxxt.12`.
- Special runs: none.

## Open decisions

None open. [DETAIL] Keep the existing control-test name so the kit probe's dated reference stays accurate; one hour is the phase-4 stop because this is a focused test-only correction. The temporary tree holds the orphan only; real caller inputs remain read-only so classification uses the actual caller set. The inventory stays non-recursive to preserve its existing policy. The write watcher covers the Python file operations named in criterion 5 across the checkout; native writes outside Python file APIs are a limit of that test. A stand-in repository tests the watcher without recreating the shared-tree race. The inventory guard requires no named script because the kit probe uses a different inventory.
