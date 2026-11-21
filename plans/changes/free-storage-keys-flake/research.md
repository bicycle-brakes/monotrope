---
title: "Research — free-storage-keys-flake"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-068l
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# free storage keys flake — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1161 files, 5216 commits, 12 rules.

## Runner exploration — 2026-11-21

Phase‑1 exploration for `free-storage-keys-flake` is done — here is the research, ready to append to `plans/changes/free-storage-keys-flake/research.md`.

## Proposed `neighbours:` header

```yaml
neighbours:
  - plans/changes/swarm-test-speed/research.md
  - plans/changes/swarm-test-speed/spec.md
  - plans/changes/flaky-swarm-leak-test/spec.md
  - plans/changes/verify-cheap-before-admission/spec.md
  - plans/changes/research-currency/spec.md
  - plans/changes/archive/2026-11-06-research-swarm/plan.md
  - plans/changes/archive/2026-11-06-free-member-rate-limit/research.md
  - plans/changes/archive/2026-11-16-runner-clock/decisions.md
  - plans/changes/archive/2026-11-06-terms-test-fixtures/research.md
```

## Research (prose for `research.md`)

### What exists today

**The change folder is a skeleton.** `plans/changes/free-storage-keys-flake/` holds only `research.md` (bead `coding-harness-068l`, owner Data Architect, `provenance: human-written`, registry row `plans/INDEX.md:610`); no spec, plan or decisions exist yet. The branch is `fix/free-storage-keys-flake`, opened by commit `ee349b78` ("chore(free-storage-keys-flake): open change folder for coding-harness-068l").

**The name matches exactly two things in the tree** (case‑insensitive search over the repository — only these, plus the change's own files):

- `free_slot_id` (`scripts/stage2_research_run.py:73-78`): docstring "Keep ordinary ids stable; hash unrestricted catalog identities into bounded storage keys." It builds the candidate `f"{stage}-{topic}-free-{model}"`; if the model does not start with `sha256-` and the candidate fullmatches `[A-Za-z0-9][A-Za-z0-9._+-]{0,119}` the candidate is the id, otherwise the id is `f"{stage}-{topic}-free-sha256-{sha256(model)}"`. The `sha256-` prefix guard prevents a literally `sha256-…`‑named model from producing an id shaped like a hash.
- `tests/test_stage2_swarm.py::test_free_model_storage_keys_preserve_best_effort_completion` (`tests/test_stage2_swarm.py:4174-4189`), parametrized 3 models × 2 faults = 6 cases. Models: `"vendor/alpha-free"` (contains `/` → hashed), `"vendor/" + "a"*130 + "-free"` (over‑long candidate → hashed), `"alpha-free"` (plain id kept). Fault: `failed` True/False, planting `online:10:{model.rsplit('/', 1)[-1]}: [{"exit": 1}]` via `SwarmWorld.complete` (`tests/test_stage2_swarm.py:508-529`). Assertions: `sworld.run() == 0` even with the failed free seat; exactly 3 manifest slots carry the model (topics 9, 10, 11); their `slot_id`s are 3 distinct values each fullmatching the store's slot‑id shape; all launched and `not required`; outcomes `{9: "ok", 10: "failed" if failed else "ok", 11: "ok"}`; the judge ran.

**The test is the phase‑6 finding F‑51 of the research‑swarm change.** `plans/changes/archive/2026-11-06-research-swarm/plan.md:2443` records it ("`free_slot_id` hashes model ids that are not safe filenames"), and the criterion items at `plan.md:1013-1014` pin the test by name: "A free model id with a slash or over-long name makes an unsafe storage key, so the best-effort slot aborts required work."

**Slot ids are storage keys of the sealed state store.** `scripts/stage2_research_store.py` defines `SLOT_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,119}")` (`:35`), refuses any other id with `StoreWriteError("unsafe slot id for the state store")` (`_slot_id`, `:115-118`), stores per‑slot records as `<slot_id>.<kind>.json` and re‑checks the shape when scanning (`:421`), and binds a stored result to its planned slot by `SLOT_KEY_FIELDS = ("stage", "topic", "seat", "endpoint", "model", "prompt_sha256")` (`:41`).

**Where free slot ids are derived.** `Run.entry` calls `free_slot_id(stage, topic, spec["model"])` for role `online_free` (`scripts/stage2_research_run.py:1083-1087`); `Run.expected_slots` plans one free slot per topic 9–11 per `sorted(self.free)` with `required=False` (`:1788-1792`); `Run.correction_slot_id` bounds correction keys — `slot_id + CORRECTION_SUFFIX` when that still matches `SLOT_ID` and is unused, else `"topics-correction-sha256-" + digest(identity)` (`:1272-1283`, `CORRECTION_SUFFIX` at `:219`). Both derivation sites call the same `free_slot_id`, so planned and launched ids agree by construction.

**Best‑effort free seats.** `Run.gate` skips `research_terms_problem` for role `online_free` (`scripts/stage2_research_run.py:693,704`) but runs the leak check for every role; `Run.launch` requires a refreshed definition from the selection's `catalog.models_store` (`:870-875`, `stage2_go.definition_of`) and passes `admission=free_admission` only for free seats (`:857-889`). The test supplies the definition through `with_go_store` (`tests/test_stage2_swarm.py:114-130`), which adds every free id to the synthetic `models_store`. Free admission itself is `stage2_swarm.invocation_problem(..., "online_free", ...)` (`scripts/stage2_swarm.py:476-496`): suffix policy, exclude/include, `stage2_free.model_veto(model, paid=…, plain=False)` and membership in the frozen `selected_free`.

**The dispatcher names six outcomes** — `OUTCOMES = ("ok", "failed", "timed-out", "cancelled", "not-started-deadline", "refused")` (`scripts/stage2_research_dispatch.py:26`); a queued slot whose stage deadline passes finishes `not-started-deadline` (`:221,248`); children are supervised with `communicate(timeout=TICK)` in a loop (`:263`).

**The stand‑in protocol the test runs on.** The `STAND_IN` source (`tests/test_stage2_swarm.py:277-459`) resolves its scenario key as `f"{kind}:{topic}:{model.split('/')[-1]}"`, then `f"{kind}:{topic}"`, then `kind` (`:342-344`); the step index is the count of prior logged calls with the same resolved key, read from the log before this call appends its own record (`previous = read_records(log)` `:297`, `index = sum(...)` `:345`), falling back to the last step only when `repeat_last` is set (`:346`). Every append and read of `calls.jsonl` goes through `atomic_test_log.append_record`/`read_records` under an advisory `flock` (`tests/atomic_test_log.py:101-125`), embedded verbatim into the stand‑ins at the `@ATOMIC_LOG@` marker by the `sworld` fixture (`tests/test_stage2_swarm.py:592`). My reading of the mechanism, not an observed failure: two concurrent calls with the same key can both count the same `previous` and get the same index — in this test's scenario every key holds exactly one step and `SwarmWorld.complete` sets `repeat_last: True` (`tests/test_stage2_swarm.py:514-521`), so a duplicated index still selects the same step. A lock that cannot be taken within 60 s raises `TimeoutError` (`tests/atomic_test_log.py:53-68`), and the leak check's git helper fails closed on any `OSError` ("git cannot be started", `scripts/leakcheck.py:244-256`) — both would turn a slot into a non‑`ok` outcome under load.

**This suite has a recorded flake history.** `flaky-swarm-leak-test` (bead `coding-harness-yb1l`, active change, `decisions.md:37`) fixed torn reads of concurrently appended stand‑in logs with the shared locked helper; its helper docstring states the cause was an inferred explanation, the original CI diagnostics never read (`tests/atomic_test_log.py:1-13`). An interrupt test flaked on PR 404 (`docs/journal/handover/2026-11-16-day-six-lanes.md:155-157`) and a second on #419 (bead `coding-harness-oag7`, `docs/journal/handover/2026-11-20-day-run.md:116-117`). Two load‑flaky timing tests were repaired by the runner‑clock change (archived `plans/changes/archive/2026-11-16-runner-clock/`, bead `pph3`, `decisions.md:27`), and the archived research‑swarm plan records two more repaired timing flakes (`plan.md:2322-2323`). `swarm-test-speed` (bead `coding-harness-dca4`, active) maps this same file as the suite's most expensive (`research.md:70-75`, naming this test's 3×2 parametrisation) and excludes fixture rewrites for now (`plan.md:24`).

### Where it lives

- The test and its world: `tests/test_stage2_swarm.py` (`test_free_model_storage_keys_preserve_best_effort_completion` `:4174`, `SwarmWorld` `:463`, `sworld` fixture `:532`, `STAND_IN` `:277`, `complete` `:508`, `selection_for` `:101`, `with_go_store` `:114`, `manifest_of` `:2181`); the log helper `tests/atomic_test_log.py`.
- The key derivation and best‑effort path: `scripts/stage2_research_run.py` (`free_slot_id` `:73`, `entry` `:1084`, `expected_slots` `:1788`, `correction_slot_id` `:1272`, `gate` `:683`, `launch` `:830`); `scripts/stage2_swarm.py` (`invocation_problem` `:450`); `scripts/stage2_free.py` (`model_veto` `:46`); `scripts/stage2_go.py` (`assess`, notices never change admission).
- The store that owns the key rule: `scripts/stage2_research_store.py` (`SLOT_ID` `:35`, `_slot_id` `:115`, `SLOT_KEY_FIELDS` `:41`); the dispatcher `scripts/stage2_research_dispatch.py` (`OUTCOMES` `:26`).
- The ledger that pins the test name: `plans/changes/archive/2026-11-06-research-swarm/plan.md:1013-1014,2443`; held like a live plan by `scripts/check_criterion_ledger.py` (docstring `:26-36`, archived plans with a ledger section are measured too).

### What is unclear

- **The bead text was not read.** The title, description and notes of bead `coding-harness-068l` live in the Dolt tracker under `.beads/`; reading them needs `tools/bd show`, which this phase does not run. Which CI run or local `make verify` round went red, which of the six parametrized cases failed, and the failure output itself are therefore not read.
- **No repository artefact records this flake.** A search over `docs/journal/handover/` finds no handover naming `free-storage-keys-flake`, `068l`, or this test as flaky, and no `findings.md` under `plans/changes/` mentions it; the only mentions of the test are the research‑swarm archive and `swarm-test-speed`'s research. "Not recorded in the repository" and "the evidence sits unread in the bead" are both true here.
- **The flake mechanism is not established by reading.** Candidate surfaces found in the tree, each unproven: (a) the stand‑in's per‑key step index read before appending (`tests/test_stage2_swarm.py:345`) — in this scenario mitigated by single‑step lists and `repeat_last`; (b) fail‑closed surfaces that turn one slow or transiently failing git/lock into a non‑`ok` free slot (`scripts/leakcheck.py:252-253`, `tests/atomic_test_log.py:67`, `OUTCOMES` `refused`/`not-started-deadline`); (c) something in the production key derivation — no run‑to‑run variance is visible in `free_slot_id`; hashing and prefix tests are deterministic. Whether the flake is in the test's scaffolding or in production behaviour is the interview question.
- Whether `swarm-test-speed` (bead `dca4`) is expected to touch the same test file in parallel, and which change may edit the archived ledger row, are session‑ownership questions.

### Which files a change would have to touch

- `tests/test_stage2_swarm.py` — the test itself and/or the stand‑in's scenario resolution (`:342-346`) and `SwarmWorld.complete`, whichever surface the flake sits on.
- `scripts/stage2_research_run.py` — only if the key derivation or the best‑effort free path changes (`free_slot_id`, `expected_slots`, `correction_slot_id`, `gate`/`launch`).
- `scripts/stage2_research_dispatch.py` or `tests/atomic_test_log.py` — only if the flake sits in supervision/queueing or in the shared log protocol.
- `plans/changes/archive/2026-11-06-research-swarm/plan.md` — a rename or deletion of the pinned test turns the criterion‑ledger gate red until its rows (`:1013-1014`) are updated; a behaviour‑only fix does not.
- `plans/INDEX.md` — the registry row updates with the change's own artefacts as they appear.

Nothing was designed, recommended or changed; the tree is untouched.
