---
title: "Findings — explore-provenance"
category: findings
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — explore-provenance

Stage-2 call, 2026-11-04: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 889 files, 3263 commits, 12 rules.

Stage-2 call, 2026-11-04: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 892 files, 3265 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/explore-provenance/plan.md` +14 -14
> - `plans/changes/explore-provenance/spec.md` +1 -1
> - `scripts/stage2.py` +140 -1
> - `scripts/stage2_research_run.py` +27 -16
> - `scripts/stage2_research_snapshot.py` +18 -4
> - `tests/test_explore_provenance.py` +34 -0
> - `tests/test_stage2.py` +100 -0
> - `tests/test_stage2_research_deep_review.py` +140 -1
> - `tests/test_stage2_research_store.py` +62 -0
> - `tests/test_stage2_swarm.py` +52 -8
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> tests/test_stage2.py:1884:5: F841 Local variable `before_second` is assigned to but never used
>      |
> 1882 |     assert quoted in rest, "the authored section lost its own quote of the skeleton"
> 1883 |     assert "provenance: ai-drafted-reviewed" in text.split("---", 2)[1]
> 1884 |     before_second = world.research.read_bytes()
>      |     ^^^^^^^^^^^^^ F841
> 1885 |     world.script(claude=[{"stdout": "Second fact from `src/app.py`."}])
> 1886 |     assert world.run("explore") == 0
>      |
>      = help: Remove assignment to unused variable `before_second`
>
> Found 1 error.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-04: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 893 files, 3269 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2.py` +3 -1
> - `tests/test_stage2_research_store.py` +1 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_deep_review.py::test_research_publication_preserves_unrelated_bytes
> FAILED tests/test_stage2_research_deep_review.py::test_research_publication_is_one_atomic_replacement
> FAILED tests/test_stage2.py::test_explore_removes_only_opening_skeleton_text
> FAILED tests/test_stage2.py::test_explore_publishes_truthful_research_provenance[True]
> FAILED tests/test_stage2.py::test_explore_publishes_truthful_research_provenance[False]
> FAILED tests/test_stage2.py::test_explore_resets_review_without_changing_lifecycle
> FAILED tests/test_stage2_research_store.py::test_binding_accepts_only_exact_research_provenance_publication
> FAILED tests/test_stage2_research_deep_review.py::test_corrected_skeleton_publication_keeps_swarm_resume
> FAILED tests/test_stage2_research_deep_review.py::test_publication_keeps_earlier_research_bytes_and_their_resume
> FAILED tests/test_stage2_swarm.py::test_a_run_killed_after_staging_the_clear_is_recovered_on_resume
> FAILED tests/test_stage2_swarm.py::test_a_failed_publication_keeps_the_results_reusable
> FAILED tests/test_stage2_swarm.py::test_only_the_runner_appends_research - Ty...
> FAILED tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance
> 13 failed, 1 skipped in 21.66s
> ```

Stage-2 call, 2026-11-04: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 893 files, 3269 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/explore-provenance/plan.md` +13 -13
> - `scripts/stage2.py` +3 -2
> - `scripts/stage2_research_snapshot.py` +5 -6
> - `tests/test_stage2_research_deep_review.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> swarm: eleven reconciled topics appended to plans/changes/demo/research.md · run 9e0df63ef154f9cffa51ccd3aba82319
> ----------------------------- Captured stderr call -----------------------------
> failed: the research run 6552fdc8a84301ac3aa437dfc0635cfa is incomplete: incomplete - the judge failed: judge (failed); no later stage starts.
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_deep_review.py::test_publication_keeps_earlier_research_bytes_and_their_resume
> FAILED tests/test_stage2_research_deep_review.py::test_corrected_skeleton_publication_keeps_swarm_resume
> FAILED tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance
> 3 failed, 10 passed, 1 skipped in 26.74s
> ```

Stage-2 call, 2026-11-04: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM 5.3 Flash failed both attempts (ruff, then six red tests), 2026-11-04; continues from the kept attempt · leak check clean over 893 files, 3274 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2_swarm.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 25 files, 2 commits, 1 rules, 1 prompt texts
> swarm: eleven reconciled topics appended to plans/changes/demo/research.md · run f758ddbeec92783f31fb51d5758b07c7
> ----------------------------- Captured stderr call -----------------------------
> failed: the research run 35456e0b206672e1857f4a8ad6f99d90 is incomplete: incomplete - the judge failed: judge (failed); no later stage starts.
> =========================== short test summary info ============================
> FAILED tests/test_stage2_research_deep_review.py::test_corrected_skeleton_publication_keeps_swarm_resume
> FAILED tests/test_stage2_swarm.py::test_swarm_publication_corrects_research_provenance
> 2 failed, 7 passed, 1 skipped in 18.36s
> ```

Stage-2 call, 2026-11-04: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason second Sonnet attempt, 2026-11-04: test_corrected_skeleton_publication_keeps_swarm_resume and test_swarm_publication_corrects_research_provenance are red because a resume after the corrected publication reruns every finder and seat; trace where the resume compares research.md (stage2_research_snapshot.changed_against_stored and the caller that records publication= in stored_binding) and make the stored binding carry the prepared corrected bytes before the write · leak check clean over 893 files, 3275 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 893 files, 3281 commits, 12 rules.

Stage-2 call, 2026-11-04: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 893 files, 3285 commits, 12 rules.

Stage-2 call, 2026-11-05: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 893 files, 3309 commits, 12 rules.

Stage-2 call, 2026-11-05: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 893 files, 3309 commits, 12 rules.
