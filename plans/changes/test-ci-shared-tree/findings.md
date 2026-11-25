---
title: "Findings — test-ci-shared-tree"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.12
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — test-ci-shared-tree

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5751 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5752 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:3a05bca3b4859876c1aa85ea06e95dc90c775df50756e0e5a08b20fcaaf3a571

Spec review commit: 20f05467788bb5582608925fb82dd1558e29a4b2

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md, criterion 2 ("the same script glob") | Reading A: the control test calls the real `_scripts()` (e.g. aimed at the temporary tree through a parameter) and `_heimatlose_namen()`. Then dropping `*.sh` from `_scripts()` at `tests/test_ci.py:3534` turns the control test red. Reading B: the test repeats the glob pattern (`*.py` plus `*.sh`, minus `test_*`) over its temporary tree. Then dropping `*.sh` from `_scripts()` leaves the control test green while the real checks lose sight of `.sh` scripts again. The "Refuted by" line ("Omitting `.sh` from the glob") does not say which glob it means. Reading B defeats the purpose stated in the test's own docstring (`tests/test_ci.py:3606-3612`: prove that `_scripts()` sees a `.sh` file). | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-4 (2026-11-25) | — |
| S-2 | [AMBIGUITY] | SPEC | base | spec.md, criterion 3, "Refuted by" | "A real script under that directory is omitted". Reading A: omitted compared with today's set, which is the top-level `*.py` and `*.sh` files in `scripts/` that do not start with `test_`. The criterion holds on today's code and pins only the default root. Reading B: any script anywhere below `scripts/`. `scripts/kit/probe.py` is already left out by the non-recursive glob (`tests/test_ci.py:3534`), so the criterion is red before any change. Making it green would need a recursive glob, which changes the inventory policy (a non-goal) and would make the caller check report `probe.py`. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-5 (2026-11-25) | — |
| S-3 | MAJOR | SPEC | base | spec.md, criterion 1 | The refuting state is easy to build: keep the write to `REPO_ROOT / "scripts"` at `tests/test_ci.py:3619`. But nothing turns red in that state. The control test passes wherever its file lies, and the inventory tests pass when the tests run one at a time. The spec names nothing that checks where the file is written, so the criterion ledger would have to name a test invented while building. The obvious candidate, the control test asserting on its own path, only checks itself. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-6 (2026-11-25) | — |
| S-4 | MAJOR | SPEC | base | spec.md, criterion 3 | Refuting state: `_scripts()` defaults to an empty or temporary tree, or its callers at `tests/test_ci.py:3568` and `:3729` pass one. Then `test_every_script_has_a_caller_or_a_declared_reason` and `test_every_script_has_a_test_or_a_declared_reason` both pass on an empty list, because neither checks that the list has entries. No other test catches it. The spec's purpose is "without weakening the real script inventory checks", and nothing that could go red guards that part. The spec names no such check. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-7 (2026-11-25) | — |
| S-5 | MINOR | SPEC | base | spec.md, Problem and criteria 1–2 ("the orphan-shell-script control test") | The spec never gives the test's id. In `tests/test_ci.py`, `test_an_orphan_shell_script_gets_flagged` (docstring: "The control test to finding 11") fits the phrase as well as `test_the_glob_itself_finds_a_real_orphan_shell_script` (docstring: "The second half of the control test"). The first already meets criterion 1, because it writes no file. Only the Problem's "creates a file" and the indirect reference to the kit probe's comment point to the second; the id itself appears only in research.md. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-8 (2026-11-25) | — |
| S-6 | MINOR | SPEC | base | spec.md, criterion 2; decisions.md D-1 | The spec does not say what the orphan classification reads in the isolated case. Today the test passes the real `ci.yml`, `verify_all.sh` and `OHNE_AUFRUFER` (`tests/test_ci.py:3622-3626`). D-1 says the temporary tree holds "the files the orphan check reads", which suggests copies. Blank inputs, as in `test_an_orphan_shell_script_gets_flagged`, would also meet criterion 2. Each choice checks against a different set of callers (the real ones, copies, or none), and the implementer has to pick one without guidance. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-9 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5753 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5754 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:ffa706cfadf53a7e15440513071f17734e987cb82fc82b8db82f38522d2b4175

Spec review commit: cf14e3801620eeb3384609d6448d01977f148877

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-7 | BLOCKER | SPEC | base | spec.md, criterion 4; Protected areas; Non-goals; Definition of Done ("`make verify` green") | Refuting input: the kit probe. It is the `leerprobe` gate in `decisions/gates.yaml:110-118`, with enforcement block, and it runs in `make verify`. `tests/test_ci.py` travels to the probe's throwaway repo. `scripts/stage2.py` does not: it falls under the `scripts/` catch-all `bestand` (`scripts/kit/manifest.yaml:374-376`). `test_every_script_has_a_caller_or_a_declared_reason` is not in `REIST_NICHT` (`scripts/kit/probe.py:193-238`), so it is green there today. Criterion 4's `stage2.py` assertion turns it red there, and a red case without an entry blocks (`probe.py:532-539`). The probe's own remedy is a new `REIST_NICHT` entry and raising `DECKEL` from 44 to 45 in `scripts/kit/probe.py`. But production scripts are a protected area, and changing kit-probe behaviour is a non-goal. Skipping the assertion under `HARNESS_KIT_PROBE` would break criterion 4's "when either real inventory test runs". The docstring at `tests/test_ci.py:3585-3590` warns against this kind of real-inventory check for this reason. As written, criterion 4, the protected area and "`make verify` green" cannot all hold, and the implementer would have to pick which one gives way. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-10 (2026-11-25) | — |
| S-8 | MAJOR | SPEC | base | spec.md, criteria 1 and 5; Open decisions ("the isolation regression must also observe writes during the run") | Refuting state for criterion 1: today's code. It writes `REPO_ROOT/scripts/verwaistes_werkzeug__test_ci_nie_committen.sh` and unlinks it in `finally` (`tests/test_ci.py:3619-3633`). In that state the before-and-after listing of `scripts/` from criterion 5 is unchanged. So the only check the criteria name stays green while criterion 1 is refuted. The Open decisions paragraph admits this and requires an "isolation regression" that observes writes during the run. No criterion carries that requirement, and nothing says how the writes are observed. Patching `Path.write_text`/`open` to record target paths, redirecting `REPO_ROOT` to a copy and watching the directory would each catch a different set of writes. The implementer has to invent one, and without it criterion 1 has no check that can go red. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-11 (2026-11-25) | — |
| S-9 | [AMBIGUITY] | SPEC | base | spec.md, criterion 5, "Refuted by"; decisions.md D-6 | The spec does not say where the guard puts its "lasting write". Reading A follows D-6's wording ("plants a write into the repository's scripts/"): the guard writes a real file into the checkout's `scripts/` while the control test runs. That brings the shared-tree write back, now inside the guard test. Parallel `_scripts()` callers (`tests/test_ci.py:3568`, `:3729`) and the probe's untracked-file list can see it, which is the race the Problem describes. Reading B: the guard writes into a stand-in checkout, such as a temporary copy with `REPO_ROOT` or the listing root redirected. Then the control test's checkout root has to be injectable, and the guard proves the listing logic rather than anything about the real directory. The two readings give different code and different parallel safety. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-12 (2026-11-25) | — |
| S-10 | MINOR | SPEC | base | spec.md, criterion 2, "Refuted by" ("or classification uses different caller inputs") | Refuting state: the control test passes `ci=""`, `runner=""` and `ohne_aufrufer={}`, or copies, to `_heimatlose_namen()` instead of the checkout's `ci.yml`, `verify_all.sh` and `OHNE_AUFRUFER`. The orphan is still reported, so the control test stays green, and no criterion names a check that turns red. The other two refutations are mutations of `_scripts()` and `_heimatlose_namen()`, and the control test catches those. Only reading the code can check this clause. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-13 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5755 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5756 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:9889c75a20fa5e1470a311bb9e5d118fce44aa6796fd9dad48950ea5989b5738

Spec review commit: ca6851d889c7451ab95189f7462a63eb65b0cc34

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-11 | MINOR | SPEC | base | spec.md, criterion 1 "Refuted by"; criterion 5 | Criterion 1 can be refuted in ways criterion 5's watcher cannot see, so nothing turns red. (a) The control test creates the orphan in the checkout's `scripts/` with `Path.touch()`, which goes through `os.open`. Or it builds the orphan in tmp, moves it in with `Path.replace`/`os.rename`, then unlinks it in `finally`. `_scripts()` sees the file and the control test passes, but no `Path.write_text`, `Path.write_bytes` or `open` call targets that path. If "write-mode `open`" means the builtin only, `Path.open("w")` also slips past, because pathlib calls `io.open`. (b) The temporary tree is made inside the checkout but outside `scripts/` (e.g. `tempfile.mkdtemp(dir=REPO_ROOT)`). That breaks criterion 1's "outside the repository checkout", but criterion 5 watches only `scripts/`. The untracked directory still reaches the probe's `git ls-files --others` list, which is the cache the Problem names. So criterion 1 goes red only for the three named write kinds aimed at `scripts/`. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-14 (2026-11-25) | — |
| S-12 | MINOR | SPEC | base | spec.md, criterion 6, "Refuted by" ("or the guard writes into the real checkout") | Refuting state: the planted variant writes into the checkout's real `scripts/`, and the watcher it runs under also watches the checkout's `scripts/`. The watcher reports the write, so the guard's assertion holds and the guard stays green. Meanwhile the shared-tree write from the Problem is back, now inside the guard, where parallel `_scripts()` callers can see it. No criterion names a check that turns red for this clause. Only reading the code can show where the guard writes. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-15 (2026-11-25) | — |
| S-13 | MINOR | SPEC | base | spec.md, criterion 7, "Refuted by" ("copied caller inputs") | Refuting state: the control test copies `.github/workflows/ci.yml` and `scripts/verify_all.sh` unchanged into its temporary tree and reads them from there. That also breaks the [DETAIL] "the temporary tree holds the orphan only". The texts that reach `_heimatlose_namen()` are byte-for-byte the checkout's, so a spy that compares its arguments sees equal strings and stays green. Only `OHNE_AUFRUFER` can be told apart from a copy, by object identity. The spy sees the texts but not the path they were read from, so the "copied" clause cannot go red for the workflow and runner texts. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-16 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5759 commits, 12 rules.
