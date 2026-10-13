---
title: "Findings — ci-minutes"
category: findings
status: draft
implementation_status: none
date: 2026-10-13
created: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-cac
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — ci-minutes

Stage-2 call, 2026-10-13: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Claude Code 2.1.296 refused glm-5.3(-flash) as an unrecognized model before any call (bead coding-harness-6th) · leak check clean over 407 files, 1010 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `.github/workflows/ci.yml` +3 -2
> - `decisions/gates.yaml` +2 -2
> - `docs/WORKFLOW.md` +4 -0
> - `plans/changes/ci-minutes/plan.md` +6 -4
> - `pyproject.toml` +1 -1
> - `ruff.toml` +1 -1
> - `scripts/check_research_currency.py` +1 -1
> - `scripts/ci_gates.py` +6 -1
> - `tests/test_ci.py` +40 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> ........................................................................ [  3%]
> ........................................................................ [  7%]
> ........................................................................ [ 11%]
> ................................s..........s..............F...ss........ [ 15%]
> .........................ss.sssssss..s.......s.......................... [ 19%]
> ........................................................................ [ 22%]
> ........................................................................ [ 26%]
> ........................................................................ [ 30%]
> ........................................................................ [ 34%]
> ........................................................................ [ 38%]
> ........................................................................ [ 41%]
> ......................................................................s. [ 45%]
> ........................................................................ [ 49%]
> ........................................................................ [ 53%]
> ........................................................................ [ 57%]
> ........................................................................ [ 60%]
> ........................................................................ [ 64%]
> ........................................................................ [ 68%]
> ........................................................................ [ 72%]
> ........................................................................ [ 76%]
> ........................................................................ [ 79%]
> ........................................................................ [ 83%]
> ........................................................................ [ 87%]
> ........................................................................ [ 91%]
> ........................................................................ [ 95%]
> ........................................................................ [ 98%]
> ....................                                                     [100%]
> =================================== FAILURES ===================================
> _________________ test_the_mutation_ratchet_only_turns_one_way _________________
>
>     def test_the_mutation_ratchet_only_turns_one_way() -> None:
>         """An entry in the ratchet whose gate has long been covered lies.
>     
>         And an entry for a gate that no longer exists keeps an exception open for
>         something nobody runs any more.
>         """
>         quellen = {p: p.read_text(encoding="utf-8") for p in _testdateien()}
>         bekannt = {g["id"]: g for g in gates()}
>     
>         verwaist = sorted(set(OHNE_MUTATIONSTEST) - set(bekannt))
>         assert not verwaist, f"Exception for a gate that does not exist: {verwaist}"
>     
>         ueberholt = []
>         for gid in OHNE_MUTATIONSTEST:
>             ziel = _pruefling(bekannt[gid])
>             if ziel and any(MUTATIONS_NAMEN.search(t) for p, t in quellen.items() if ziel in t):
>                 ueberholt.append(gid)
> >       assert not ueberholt, f"long since covered, but still in the ratchet: {ueberholt}"
> E       AssertionError: long since covered, but still in the ratchet: ['plans-registry', 'plans-registry-strict']
> E       assert not ['plans-registry', 'plans-registry-strict']
>
> tests/test_ci.py:1885: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_the_mutation_ratchet_only_turns_one_way - Asser...
> 1 failed, 1875 passed, 16 skipped in 310.68s (0:05:10)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [leerprobe] $ lauf_cmd
> BLOCK (1):
>   - 2 rote(r) Fall/Faelle ohne deklarierten Grund
>       tests.test_ci::test_the_interpreter_floor_is_declared_once
>       tests.test_ci::test_the_mutation_ratchet_only_turns_one_way
>       
>       Nachtragen mit: python3 scripts/kit/probe.py --messen
>
> INFO  (1):
>   - 932 von 970 Faellen tragen in ein fremdes Repo (96 %)
>       mechanismus 83 · bestand 324 Datei(en)
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 8617 earlier lines left out …]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 408 files, 1011 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Z.ai weekly limit exhausted until 2026-10-14 14:34 CEST (HTTP 429, code 1310), and Claude Code 2.1.296 refuses the GLM names (bead coding-harness-6th) · leak check clean over 408 files, 1011 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/ci-minutes/spec.md` +3 -2
> - `scripts/kit/probe.py` +6 -4
> - `tests/test_ci.py` +10 -0
> - `tools/cloud-env/README.md` +5 -3
> - `tools/cloud-env/setup.sh` +3 -3
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 408 files, 1012 commits, 12 rules.
