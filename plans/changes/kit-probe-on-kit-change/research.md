---
title: "Research — kit-probe-on-kit-change"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-w2ay
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: stage2, model: glm-5.3-flash, version: "2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# kit probe on kit change — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md).
The original runner exploration below is preserved as received. Its model
provenance is recorded in the header; Codex's draft-stage supplement follows
the original output.

Stage-2 call, 2026-11-13: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1044 files, 4116 commits, 12 rules.

## Runner exploration — 2026-11-13

The exploration is complete. Here is the research, ready to append to `plans/changes/kit-probe-on-kit-change/research.md`.

---

## What exists today

**The bead's intent, stated once.** Bead coding-harness-w2ay is named in `docs/research/2026-11-09-make-verify-long-term.md` ("Proposed order of work", step 3) as "Kit probe only when kit files changed, hosted CI keeps it always (bead coding-harness-w2ay): 200 s per run". The same note measured the cost: the `leerprobe` gate took 200 s median and 8.3 hours total over 151 full local runs between 2026-11-04 and 2026-11-09 (section "What was measured", bullet "Kit probe"). The duration baseline `docs/research/2026-11-04-verify-duration-baseline.md` measured 196 s (194–200 s), 16 % of a run; the test-strategy draft `docs/research/2026-11-12-test-strategy-draft.md` ("What was measured" table) gives 204 s at its later cut-off. Nothing in the repository defines which files count as "kit files" for this purpose — that predicate does not exist anywhere yet.

**The probe itself.** `scripts/kit/probe.py` ("The kit probe (Leerprobe)") copies into a throwaway repository everything `scripts/kit/manifest.yaml` classifies as role `mechanismus`, creates the empty `geruest_ordner`, commits, runs pytest there (`_faelle`), and compares red cases against the measured exemption list `REIST_NICHT` under the cap `DECKEL` (44 since 2026-11-03) and the closed reason set `GRUENDE` (three entries; two removed with dated reasons in the comments). The verdict function `pruefe()` first runs cheap checks — every tracked file classified (unclassified is BLOCK, from `nach_rolle()` over `git ls-files --cached`), untracked unclassified files reported as DRIFT (blocking only under `--strict`) — and only then calls `fahre()`, the minutes-long throwaway pytest run (`faelle = fahre() if faelle is None else faelle`). Both halves are one gate command today. The throwaway run sets `HARNESS_KIT_PROBE=1` in its environment (`_faelle`); a ratchet in `tests/test_workflow_entry.py` (`test_only_the_workflow_entry_test_reads_the_kit_probe_switch`) allows only `scripts/kit/probe.py` and `tests/test_workflow_entry.py` to read that switch.

**Where the probe runs today.** Three routes, all live:

1. **Hosted CI, always:** gate `leerprobe` in `decisions/gates.yaml` (command `python3 scripts/kit/probe.py --strict`, job verify, cost minutes, enforcement block, floor true, placement both) becomes step `The kit probe holds over the tracked tree` in the derived `.github/workflows/ci.yml`, running on every push to main, every pull request and every merge-group check.
2. **Local full run, always when reached:** `scripts/verify_all.sh` selects gates via `ci_gates.py --commands --job verify --placement lokal --tsv` and runs each selected gate unconditionally; there is no path condition anywhere in the runner. Under the schema-3 cheap-first order (`kostenordnung` in `scripts/ci_gates.py`, bead coding-harness-bxxt.1), `leerprobe` runs after the pytest gate (both minutes class, declaration order); if pytest fails (block), the probe lands in the runner's "not run" summary, and the comment there records that skipped gates get no timing events.
3. **Targeted repair check, conditionally:** `scripts/stage2.py` `targeted_selection` already includes `leerprobe` only under a condition — `(membership and gate["id"] == "leerprobe")`, where `membership` is `any((posix in before) != present[posix] for posix in touched)`: a path that appeared or vanished against the baseline selects the probe ("a changed entrypoint selects its own gate, and a path that appeared or vanished the kit probe"). The applicability row comes from `plans/changes/repair-targeted-check/plan.md` ("Added, removed or renamed files | `leerprobe` as well as the preceding rows") and is tested in `tests/test_stage2.py::test_targeted_gate_selection_matches_command_entrypoint` (parameterized: `probe.py` at root does not select it, `scripts/kit/probe.py` does).

**What the probe's verdict actually depends on** (the material a "kit change" predicate must cover): every tracked file's classification — a brand-new unclassified file blocks without any known kit file changing; the contents of every `mechanismus` file, which are copied and tested in the throwaway repository; `scripts/kit/probe.py`'s own tables (`REIST_NICHT`, `DECKEL`, `GRUENDE`) and logic; `scripts/kit/manifest.yaml`'s rules and `geruest_ordner`. The probe needs no git history — it reads `git ls-files` and `--others --exclude-standard` (`_ls_files`), a detail two incidents recorded there explain (untracked files must be seen; untracked noise must not block).

**Existing schema vocabulary has no conditional concept.** `scripts/ci_gates.py` closes the vocabularies `PLACEMENT` ("hosted", "writer", "both"), `COST_CLASSES` ("seconds", "minutes"), `ENFORCEMENT`, `JOBS`, `SUBSETS` ("docs"), at `SCHEMA_VERSION = 3`; the pinning test `tests/test_ci.py::test_repository_gate_schema_is_v3` asserts version 3, that `leerprobe` is minutes class, and that a version-2 list is rejected. A conditional local run would be a new kind of declaration — no field for it exists ("not there", verified across `validate_schema`, `gates()`, `misst_in`, `in_job`, `generate_ci`). The closest existing mechanisms are `placement: hosted` (the local runner skips a gate by declaration, `misst_in`) and the caller-chosen subset `--job docs` (bead coding-harness-77qj, `verify_all.sh --job docs`) — both unconditional decisions, not change-dependent ones. `ci.yml` is generated (`--generate-ci`) and held to the gate file by the `ci-drift` gate; hand edits fail on purpose.

**Where the evidence lives.** The run log `verify-duration.jsonl` under the shared state root (`scripts/verify_duration.py`, `HISTORY_NAME`, gate events keyed by gate id) is the source of the 200 s figure; a local skip that records nothing would leave no row for `leerprobe`. `docs/governance/gate-catalog.md` carries the machine-generated row for `leerprobe` (held to `ci_gates.py --catalog` output by `tests/test_gate_catalog.py`). `docs/testing.md` describes the probe as test layer 6, naming `scripts/kit/probe.py` and `scripts/kit/manifest.yaml`. `docs/WORKFLOW.md` requires a fresh full `make verify` before phase 6 ("The review verb requires a fresh full `make verify` before phase 6 … a green targeted repair does not replace that check"); hosted CI as the phase-6 evidence is still only a proposal in the research note (bead coding-harness-u3qg, step 4 of its order of work, not implemented). The phase-5 stop hook `.claude/hooks/session-stop/check-tests-green.sh` is named in `docs/WORKFLOW.md`'s missing-pieces notice (asserted in `tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands`) and does not exist in the tree.

**Neighbouring work.** `plans/changes/verify-cheap-first/spec.md` (bead coding-harness-bxxt.1, class bounded) introduced the cost classes and the cheap-first stop, and its frontmatter names the research note as neighbour — the established shape for this cluster. Archived neighbours that changed the probe's local behaviour: `plans/changes/archive/2026-11-06-verify-stages-new-files/spec.md` (bead coding-harness-fdz: the runner intent-to-adds untracked files so the probe's `git ls-files` sees them) and `plans/changes/archive/2026-11-06-verify-absolute-python/spec.md` (bead coding-harness-4x2c: an absolute `$PYTHON` reaches the probe's foreign repository). `plans/changes/repair-targeted-check/spec.md` (bead coding-harness-gxwg) is the targeted check whose membership rule is the only existing conditional-probe precedent. Two tests hold the probe's static half: `tests/test_kit.py` (roles, reasons, cap, two-manifest non-contradiction against `scripts/export/manifest.yaml`, including the >60-files threshold in `test_the_two_manifests_really_disagree_somewhere`, plus the mutation-named proofs the ratchet `scripts/mutation_evidence.py` maps to the `leerprobe` gate via `pruefling()` — a script under `scripts/kit/` is found because the pattern crosses the subfolder, per that function's comment).

## What is unclear about it

1. The predicate "kit files changed" is undefined. Three candidate shapes appear in the tree without a decision: the targeted check's membership proxy (any path appeared or vanished), the `mechanismus` set and its contents, or `scripts/kit/**` plus `tests/test_kit.py`. The bead note fixes only the split (local conditional, hosted always), not the set.
2. Whether a skipped throwaway run may also skip the cheap classification half. Today both live in one command; `pruefe()` runs classification checks before `fahre()`, and an unclassified new file blocks without any kit file changing — a predicate keyed only on kit files would miss exactly that case if the cheap half were skipped with the expensive one.
3. How the condition is declared in the one list. A new gate-file field would be a schema change (SCHEMA_VERSION, gates.yaml `schema_version`, and the v3-pinning test move together); a runner-side rule would contradict the runner's stated design ("It holds no commands of its own: it asks scripts/ci_gates.py", `verify_all.sh` header).
4. Whether a locally skipped probe still satisfies the phase-6 evidence chain. `docs/WORKFLOW.md` requires a fresh full local `make verify` before phase 6; hosted-CI-as-evidence (bead coding-harness-u3qg) is not implemented, so on the current rules the local run remains the evidence, and a skip needs a story for who measured the probe on that head.
5. How the predicate behaves without a base (fresh clone, shallow checkout). The probe needs no history today; a path-diff predicate would. Precedents: the `needs_history` field with the exit-3 "unmeasured, not guessed" convention (`decisions/gates.yaml` schema comment, `scripts/ci_gates.py::_checkout`) and `check_interview_minimums.py`'s merge-base comparison.
6. Whether the nightly picks up what the local run skips. The test-strategy draft places the kit probe in the system tier running "before phase 6, in CI, and nightly"; the schedule trigger exists in ci.yml (`cron "23 4 * * *"`), but the drift job runs no `leerprobe` step today.
7. Whether a locally skipped `leerprobe` should be recorded. The run log writes timing events for executed gates only ("skipped gates get no timing events" — `verify_all.sh` not-run summary comment), so the saving would be invisible in the same log that justified the change.

## Which files a change would have to touch

`decisions/gates.yaml` and `scripts/ci_gates.py` (any declaration of the condition and its derivation; schema bump if a new field; `generate_ci()` must keep or regenerate the CI leg in the same change, or `ci-drift` fails); possibly `scripts/verify_all.sh` if the runner enforces the skip; possibly `scripts/kit/probe.py` if the cheap classification half is split into its own mode or the predicate helper lives beside the probe; the pinning tests `tests/test_ci.py` (schema and cost pins), `tests/test_kit.py` (probe contracts and the two-manifest thresholds), `tests/test_stage2.py` (the targeted membership rule interplay); `docs/governance/gate-catalog.md` (regenerated row, held by `tests/test_gate_catalog.py`); `docs/testing.md` (layer-6 text); `.github/workflows/ci.yml` only through regeneration, never by hand; optionally `scripts/verify_duration.py` if skips must be recorded.

## Proposed `neighbours:` (verified to exist)

`plans/changes/verify-cheap-first/spec.md` · `plans/changes/repair-targeted-check/spec.md` · `plans/changes/archive/2026-11-06-verify-stages-new-files/spec.md` · `plans/changes/archive/2026-11-06-verify-absolute-python/spec.md` · `docs/research/2026-11-09-make-verify-long-term.md` · `docs/research/2026-11-12-test-strategy-draft.md` · `docs/research/2026-11-04-verify-duration-baseline.md`

---

Two notes for the runner: the skeleton's frontmatter reminder stands — filling this file with model output makes it `provenance: ai-drafted-reviewed` with `produced_by:` and `review:` per `provenance.yaml`. And the file's stage-2 call line (attempt 1, route flash, leak check clean) is already recorded; everything above belongs below it.

## Draft-stage repository gaps resolved — 2026-11-13

Read at `7c37d013` by Codex (`gpt-6.1-sol`), within this worktree only:

- `scripts/check_interview_minimums.py::_base` already distinguishes main's
  first parent, a named branch's merge base and an indeterminate detached
  checkout at `origin/main`. Its `_changed_paths` unions separate index and
  working-tree diffs with nonignored untracked paths using NUL delimiters
  and disabled rename detection. This is a usable comparison precedent,
  including the staged-edit/working-copy-restored case.
- `scripts/kit/manifest.yaml` classifies `scripts/kit/`, the reader, runner,
  duration helper and their needed verdict module as `mechanismus`; its
  `tests/` fallback classifies a new test file as `bestand`. Existing
  `tests/test_kit.py` travels. No new runtime module or manifest rule is
  required by the proposed split.
- `scripts/verify_duration.py` accepts version-1 run-start, gate and run-end
  events only, and groups all gate records as executed measurements. A
  conditional skip therefore needs an explicit event and reader/report
  treatment, rather than a zero-second successful gate.
- `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent.
  `templates/spec.md`, the phase-3 prompt and the existing cheap-first plan
  supply the available forms. The interview gate discovers a change through
  its spec, so the pre-draft invocation reported no measurable change folder;
  it must run again once the spec exists.
