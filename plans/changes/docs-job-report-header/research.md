---
title: "Research — docs-job-report-header"
status: draft
implementation_status: none
date: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-ooj5
owner: Data Architect
provenance: human-written
tags: [research]
---

# docs job report header — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-02: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 815 files, 3011 commits, 12 rules.

## Runner exploration — 2026-11-02

Research complete. Here is the phase-1 result as prose, ready to append to `plans/changes/docs-job-report-header/research.md`.

---

## What exists today

**This change is about the verify run's report header, not the `make report` snapshot.** Two "report" artefacts live in this tree and must not be conflated: the local read-only snapshot `scripts/run_report.py` (`make report`, bead `coding-harness-o2yc`, `plans/changes/run-report/spec.md`), and the header the local verify run prints before its gates, produced by `ci_gates.py --report`. The bead `coding-harness-ooj5` is titled "the `--job docs` report header" (`docs/research/2026-10-31-run-plan.md`, "Bead titles" paragraph: "ooj5 the `--job docs` report header"), and the handover `docs/journal/handover/2026-10-31-night-and-day-run.md` ("Also merged" item) records it as "Opened as follow-ups of 77qj: … coding-harness-ooj5 (the report header of `--job docs`)" — so the subject is the second artefact, the verify run's report block.

**The asymmetry, as code today.** The local runner holds the selected job in `JOB` (default `verify`, `scripts/verify_all.sh:71`; parsed in the argument loop at `verify_all.sh:74-83`, choices verify|drift|docs named in the usage comment at `verify_all.sh:10-14`), fetches its gate list with that job (`verify_all.sh:193`, `ci_gates.py --commands --job "$JOB" …`), and prints a banner naming it (`verify_all.sh:198`, `── gates: job=$JOB ──…`). But the report block above that banner is produced without the job: `verify_all.sh:179` runs `"$PYTHON" scripts/ci_gates.py --report || exit 2`, and the comment above it (`verify_all.sh:177-178`) states its purpose: "The report binds the verdict to a state of the world: which commit ran, against which base, with which gate configuration." On the reader side, `report(job)` (`scripts/ci_gates.py:479-490`) returns the fields `job`, `candidate`, `base`, `config_sha256`, `gates_total` (all gates in the file) and `gates_job` (the count of gates in `job`, computed through `in_job`, `scripts/ci_gates.py:381-385`); the CLI's `--job` defaults to `"verify"` (`scripts/ci_gates.py:748`, `choices=JOBS + SUBSETS`), and `--report` prints `report(args.job)` as JSON (`scripts/ci_gates.py:796-798`). Consequence, stated as a fact: under `bash scripts/verify_all.sh --job docs`, the printed header names `job: verify` and the verify job's gate count while the run below measures the docs subset — the run's own banner and its report block disagree. `gates_total` is job-independent (`scripts/ci_gates.py:488`) and stays correct under any selection; only `job:` and `gates_job:` are wrong. The same mechanism covers `--job drift` (`verify_all.sh` accepts it, and forwards no job to the report); the bead title scopes the `docs` case, and the drift case is the same code path — stated as a fact, not as a scope extension. The selection machinery itself is already in place and correct: `ci_gates.py --job docs` is valid CLI input today (`JOBS = ("verify", "drift")`, `SUBSETS = ("docs",)` at `scripts/ci_gates.py:43-46`; `in_job` selects verify gates naming the subset at `scripts/ci_gates.py:381-385`; the schema pins subsets to non-empty lists over `SUBSETS` on verify-only gates at `scripts/ci_gates.py:354-361`, documented in the gate-file schema comment, `decisions/gates.yaml:39-44`). The missing link is only that `verify_all.sh` does not forward its `$JOB` to the `--report` invocation.

**The numbers behind the fields, read from the current tree.** `decisions/gates.yaml` holds 23 gates (count of `- id:` entries): 21 in `job: verify`, 2 in `job: drift` (`plans-registry-strict`, `decisions/gates.yaml:268-276`; `research-currency`, `decisions/gates.yaml:278-285`); 11 verify gates carry `subsets: [docs]` (`decisions/gates.yaml:100, 111, 121, 142, 153, 163, 173, 183, 193, 203, 254`), and that membership is pinned as the set `DOCS_SUBSET` in `tests/test_ci.py:373-385` (plans-registry, docs-links, frontmatter-current, dangling-beads, decision-continuity, adr-answers, interview-minimums, question-context, criterion-ledger, research-handoff, markdownlint) by `test_the_docs_subset_holds_the_document_gates_and_no_code_gate` (`tests/test_ci.py:388`), `test_the_docs_subset_derives_no_ci_job` (`tests/test_ci.py:404`) and `test_the_schema_rejects_a_malformed_subset` (`tests/test_ci.py:421`). So under a `--job docs` run the header currently claims `gates_job: 21` where 11 gates measure.

**Who prints the header: the local runner only.** A tree-wide search for `ci_gates.py --report` finds exactly one caller, `scripts/verify_all.sh:179`; the generated workflow `.github/workflows/ci.yml` contains no "report" occurrence at all (searched). Hosted CI never prints this block, so a change here touches the local run's output only.

**Where the asymmetry was first stated and why the bead exists.** The change `draft-gates-only` (bead `coding-harness-77qj`, the change that built the docs subset for the draft verb) recorded the fact and declared the fix out of scope: its research states the asymmetry verbatim (`plans/changes/draft-gates-only/research.md`, "One report asymmetry, stated as a fact"), and its spec lists it as a non-goal — "Fixing the subset report header's full-job gate count; that reporting issue is separate work if needed, as recorded in `decisions.md`" (`plans/changes/draft-gates-only/spec.md`, Non-goals). `ooj5` was opened as that separate work. Sequencing facts from the run plans: the 2026-10-31 run plan ordered the fix "only after lane B's pull request, because both touch `scripts/verify_all.sh`" (`docs/research/2026-10-31-run-plan.md`, lane D item 5); lane B's pull request was #305, the verify worker cap (bead `coding-harness-l7sc`), merged 2026-11-01 (`docs/research/2026-11-01-night-run-plan.md`, "State at the start"); the 2026-11-01 plan then listed ooj5 on lane D as "implement — free since #305 merged" and its rule 2 names ooj5 as the one backlog bead cleared for implementation (`docs/research/2026-11-01-night-run-plan.md`, Lanes table and "Rules for this run" item 2; the 2026-10-31 plan's 21:45 UTC amendment cleared lanes B and C to build past the plan card to a ready pull request). `scripts/verify_all.sh` has been touched twice recently by neighbours: the admission supervisor (`scripts.verify_lock`, bead `coding-harness-p6mu`, `verify_all.sh:164-175`, doctrine at `docs/WORKFLOW.md:460-469`) and the worker sizing block (bead `coding-harness-l7sc`, `verify_all.sh:89-162`).

**The consumer that triggers the affected run.** The draft verb's post-run document check is exactly the affected invocation: `DOCS_VERIFY = ["bash", "scripts/verify_all.sh", "--job", "docs"]` (`scripts/stage2.py`, beside `verify_draft`; the doctrine names it at `docs/WORKFLOW.md`, "The draft (phases 2, 2b and 3)"). The default `make verify` is `bash scripts/verify_all.sh` with no `--job` (`Makefile`, `verify` target), so the default run's header is already consistent; the asymmetry shows under the subset (and drift) selections.

**Test surface today.** No test pins the report's fields: a search over `tests/` for `gates_job` and `gates_total` finds no matches (the `"job"` assertions that exist are gate-list fixtures, e.g. `tests/test_ci.py:1317`, `:1711`). The runner's test harness executes `verify_all.sh` in temp trees (`tests/test_ci.py`, `RUNNER` constant and the invocations around it; the no-second-list rule at `tests/test_ci.py`, "`verify_all.sh` must not know the check commands itself"), and the stage-2 tests frame the draft check through `DOCS_ARGV = ["scripts/verify_all.sh", "--job", "docs"]` (`tests/test_stage2.py`) and pin the frame lines verify_all prints (`test_the_frames_red_sections_reads_are_the_ones_verify_all_prints`). The reconciliation report's row T12 names the report's contract — "reports bound to candidate and base SHAs" is part of the verification source-of-truth row (`docs/research/2026-10-31-architecture-reconciliation.md`, T12).

## Where it lives

- Report header call and job selection: `scripts/verify_all.sh` (`JOB` at :71, parse at :74-83, report call at :177-179, gate-list fetch at :193, job banner at :197-198, admission at :164-175, worker sizing at :89-162).
- Report producer: `scripts/ci_gates.py` (`report()` at :479-490, `in_job` at :381-385, `JOBS`/`SUBSETS` at :43-46, subset schema at :354-361, `--job` argument at :748, `--report` argument at :762, dispatch at :796-798).
- Gate data: `decisions/gates.yaml` (schema comment :1-46, the 23 gates, the eleven `subsets: [docs]`, the two drift gates).
- Selection tests: `tests/test_ci.py` (`DOCS_SUBSET` and the three subset tests at :373-429; runner tests :1254-1263 and :1359-1825).
- Doctrine: `docs/WORKFLOW.md` (:450-454 the one-list doctrine; :1215-1223 the draft gate naming `bash scripts/verify_all.sh --job docs`).
- Trail: `plans/changes/draft-gates-only/research.md` (asymmetry paragraph) and `spec.md` (non-goals); `docs/research/2026-10-31-run-plan.md` (lane D item 5 and bead titles); `docs/research/2026-11-01-night-run-plan.md` (lane table, rules); `docs/journal/handover/2026-10-31-night-and-day-run.md` (follow-up opening).

## What is unclear about it

- **The bead's own description and class are not read.** The tracker is the Dolt database under `.beads/` and every reader goes through `tools/bd` (house rule 2); I hold only file tools and run no command, so the bead record itself is "not read", not "absent". Title and intent are taken from the run plans and handover cited above; the change folder holds only the research skeleton (`plans/changes/docs-job-report-header/research.md`).
- **The fix's shape is undecided — no source in the tree decides it.** Whether `verify_all.sh` forwards `--job "$JOB"` to the report call, whether `report()` should count a subset as a job, and whether the JSON field vocabulary (`job`, `gates_job`) may change or gain fields are design questions; the tree records only that the asymmetry is real and that the fix is this bead's work (draft-gates-only non-goals; ooj5 title).
- **What a subset header should claim is an open question.** The facts: 11 gates measure under `--job docs`, 21 sit in the verify job, 23 exist in total; `gates_total` is already job-independent. Nothing in the tree states which number a subset run's header should name — that is a human decision the interview owes.
- **Documentation of the report fields does not exist.** A search over `docs/**/*.md` for `config_sha256`, `gates_total` and `gates_job` finds no matches: the fields are described nowhere outside the code, so no docs text contradicts a fix — but whether the doctrine should name the header after the fix is unrecorded. The `report()` docstring is German (`scripts/ci_gates.py:480`); per house rule 1 German in `scripts/` is translated in pull requests of its own (bead `coding-harness-yim`), never in passing.
- **Aged references in the trail.** draft-gates-only's research cites `verify_all.sh:104` for the report call; the current call sits at :179 — the file grew by the admission supervisor (bead `coding-harness-p6mu`) and the worker sizing block (bead `coding-harness-l7sc`). Anyone consuming those line numbers must re-read the file; the symbols are stable.
- **Frontmatter obligation from the skeleton itself.** The research skeleton asks whoever fills it to set `provenance: ai-drafted-reviewed` with `produced_by:` and `review:` (`plans/changes/docs-job-report-header/research.md`, the blockquote; `provenance.yaml`, class `ai-drafted-reviewed`, `review_required: true`). The runner owns that edit; I state it, I do not apply it.

## Which files a change would have to touch

- `scripts/verify_all.sh` — the only `--report` caller (:179) and the holder of `$JOB` (:71-83); also the file two recent neighbours touched (p6mu admission, l7sc worker cap), which is why the run plans sequenced this bead after #305.
- `scripts/ci_gates.py` — `report()` and the `--job`/`--report` argument surface (:479-490, :748, :762, :796-798) if the fields or their semantics change; `in_job` (:381-385) already answers subset membership.
- `tests/test_ci.py` — the report fields are unpinned today (no `gates_job`/`gates_total` assertion exists); the runner tests (:1254-1263, :1359-1825) and subset tests (:373-429) are the surrounding surface.
- The change's own artifacts under `plans/changes/docs-job-report-header/` and the regenerated `plans/INDEX.md` (the renderer owns the index; `plans/INDEX.md:142` already lists this research file).
- `docs/WORKFLOW.md` only if the doctrine should name the header (:450-454, :1215-1223) — today it does not describe the report fields, so nothing there contradicts a fix.
- Not needed for a header-only fix, stated as a fact: `decisions/gates.yaml` (the subset annotations already exist) and `.github/workflows/ci.yml` (generated, and `--report` appears nowhere in it).

**Neighbours the runner should carry into the `neighbours:` header:** `plans/changes/draft-gates-only/spec.md` (built the docs subset, declared this fix a non-goal), `plans/changes/verify-machine-lock/spec.md` (admission in the same file), `plans/changes/verify-worker-cap/spec.md` (bead `coding-harness-l7sc`, PR #305 — the sequencing neighbour), `plans/changes/run-report/spec.md` (the name-adjacent but different "run report", bead `coding-harness-o2yc` — kept as the disambiguation neighbour).
