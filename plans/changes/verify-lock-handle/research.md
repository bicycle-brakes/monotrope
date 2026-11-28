---
title: "Research — verify-lock-handle"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-42em
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# verify lock handle — Research

## Topic (bead coding-harness-42em)

Class: bounded.

Why: scripts/verify_lock.py keeps the running admission in module-global state (_ACTIVE, _ACTIVE_ADMISSIONS); inherit_fds, inherit_env and the slot marker read only the latest admission, and the temporary publish file is named by pid only. Review round 3 of verify-slots (bead coding-harness-u1ha) found the third fault of this one design where two admissions overlap in one process. On 2026-11-11 the maintainer chose a Boundary for verify-slots (a second admission in one process is refused) and this bead for the lasting fix.

What: hold_admission returns an admission object carrying its lock, slot index and token; callers that spawn children pass it explicitly (inherit_fds(admission), inherit_env(admission); today the one caller is scripts/stage2.py); temporary files are named by the admission token, not the pid; the verify-slots Boundary is lifted. Contract test: two admissions in one process share nothing (descriptors, environment marker, holder file).

Fits the maintainer's long-term Rust direction: an admission is a value with an owner.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1325 files, 6176 commits, 12 rules.

## Runner exploration — 2026-11-28

The research for `verify-lock-handle` is below as prose, ready to append to `research.md`. I have not written any file. Phase 1 runs only read-only tools here, and the runner writes `research.md`.

## What exists today

**The bead's module state is partly named differently.** In `scripts/verify_lock.py`, the module-global state is `_ACTIVE: _Admission | None` and `_ACQUIRING: bool`, guarded by `_ACTIVE_LOCK`. The name `_ACTIVE_ADMISSIONS` from the bead was not found anywhere in the repository. `_ACTIVE` is read or written by `_active_pid()`, `_active_token()`, `_active_context()`, `_Admission.enter()` and `_Admission.release()`. `_independent_admission_guard()` refuses a second independent admission in one process, whether held or still being acquired. `tests/test_verify_lock.py` reads `verify_lock._ACTIVE` directly (around the `_ACTIVE is None` assertion after release).

**`inherit_fds` was not found.** The repository has no function of that name. Its nearest equivalent is the method `_Admission.pass_fds()`, which returns `(state.lock_fd,)` or `(state.lock_fd, slot_fd)` for a reserved slot. `inherit_env(env)` exists in `scripts/verify_lock.py`. It reads the module globals through `_active_pid()`, `_active_token()` and `admission_context()`, so it takes no admission argument.

**`hold_admission` does not return an admission object.** It is a `contextlib.contextmanager` that yields `admission.pass_fds()`, a tuple of descriptors, or `None` when the entry is nested through `nested_holder_pid()`. The `_Admission` object stays internal to the context manager. Its fields include `token`, `admission_id`, `wait_seconds`, `reserved_slot` and `setting`.

**The publish temporary file is named by pid.** `_Admission._publish()` writes `fresh = state.root / f".{path.name}.{os.getpid()}"`, then renames it over the record path. The record path is one of `verify.holder.1.json`, `verify.holder.2.json` or `verify.holder.exclusive.json`, chosen by `_record_path()`. `_register()` also embeds the pid in queue record names (`{n:020d}-{pid}.json`), but those are queue records, not temporary files.

**Callers of `hold_admission`, found by grep and not read in full:**
- `scripts/stage2.py` calls it at several points, including the pytest and import-probe paths. It passes `pass_fds=_lock_fds(owned)` to child launches and `verify_lock.inherit_env(...)` to the environment.
- `scripts/verify_run.py` calls it in the admission block around the protected gates, binding the result to `lock_fds`. It calls `inherit_env(gate_env)` for the child environment and `admission_context()` for measurements.
- `scripts/verify_lock.py` `supervise()` does **not** use `hold_admission`. It builds `_Admission` directly, calls `enter()`, spawns the child with `_spawn_child(command, admission.pass_fds(), admission)` and calls `release()` in `finally`.

**The "one admission per process" rule is documented.** The archived spec `plans/changes/archive/2026-11-26-verify-two-slots/spec.md` names it under "Boundary": one process has at most one independent admission, including while acquiring it. That spec also says "explicit multiple admission handles are deferred to bead `coding-harness-42em`". The module docstring of `scripts/verify_lock.py` repeats the rule under "Refusals".

**Other places that name the module:**
- `docs/WORKFLOW.md` (near the `scripts.verify_lock` section) and `docs/how-it-works.md` describe its behaviour.
- `scripts/ci_gates.py` has an entry for `verify_lock.py`.
- `scripts/kit/manifest.yaml` lists `scripts/verify_lock.py` and `tests/test_verify_lock.py`.
- `scripts/verify_duration.py` calls `verify_lock.admission_context()`.

**Tests that exercise the module:**
- `tests/test_verify_lock.py`, the main suite. It covers nesting, slots, the memory floor, the single-admission refusal (around the lines that assert `VerifyLockRefused` on a second `hold_admission`), and the admission-context functions.
- `tests/test_stage2.py` and `tests/test_verify_before_admission.py` monkeypatch `hold_admission` in several places and assert on `pass_fds` and `LOCK_ENV`.
- `tests/test_verify_duration.py` runs child processes through `inherit_env`.

**Planning artefacts.** `plans/changes/verify-lock-handle/decisions.md` records the phase-1a skip for this bounded change. The archived `plans/changes/archive/2026-11-26-verify-two-slots/` is the direct predecessor: its spec lists `coding-harness-42em` as the follow-up for explicit admission handles.

## Where it lives

- Module: `scripts/verify_lock.py`.
- Callers: `scripts/stage2.py`, `scripts/verify_run.py`, and the module's own `supervise()`.
- Tests: `tests/test_verify_lock.py`, `tests/test_stage2.py`, `tests/test_verify_before_admission.py`, `tests/test_verify_duration.py`.
- Doctrine: `docs/WORKFLOW.md`, `docs/how-it-works.md`, and the archived verify-two-slots spec.

## What is unclear

1. **The contract test conflicts with the current guard.** The bead asks for a test that two admissions in one process share nothing. `_independent_admission_guard()` refuses that case today, and the archived spec's Boundary states it as a rule. Lifting the Boundary means removing or changing the guard. Whether the guard goes or is reshaped is not stated in any artefact I read.
2. **Two `flock` calls on separate descriptors in one process probably conflict.** Under `flock(2)`, each `os.open` creates a new open file description, and a second `LOCK_EX` on a different description of the same file conflicts even within one process. I have not verified this on the target platform. If it holds, two admissions in one process would block on their own slot lock and never reach the contract test's assertions. This should be checked before the design is settled.
3. **"Share nothing" is not defined.** The bead lists descriptors, the environment marker and the holder file. It is unclear whether the environment marker is the `HARNESS_VERIFY_LOCK_HELD` and `HARNESS_VERIFY_LOCK_TOKEN` pair from `inherit_env()`, and whether a per-admission holder file means a distinct record name per admission.
4. **The temporary-file name and the queue record name.** The bead says temporary files are named by the token. The temporary file in `_publish()` is currently `.{name}.{pid}`. The queue record name `{n:020d}-{pid}.json` in `_register()` also contains the pid. It is not stated whether that is in scope.
5. **The bead names `stage2.py` as the one caller.** The repository has at least two callers of `hold_admission`, `scripts/stage2.py` and `scripts/verify_run.py`, and `supervise()` builds `_Admission` directly. Any change to the signature touches all three.
6. **Header facts.** `research.md` has no `neighbours:` header in its frontmatter, and the class is stated in the body ("Class: bounded.") rather than in a header. Both are required by the runner.
7. **Not searched.** I did not search for the "Rust direction" that the bead mentions, nor for the bead text of `coding-harness-42em` outside this change folder. The bead's own notes were not available to me.

## Neighbours I have read

- `plans/changes/archive/2026-11-26-verify-two-slots/spec.md`: its Boundary and its Non-goals (the explicit handles are deferred to `coding-harness-42em`).
- `plans/changes/archive/2026-11-26-verify-two-slots/decisions.md`: the record of the Option A choice behind the verify-slots Boundary.
- `plans/changes/archive/2026-11-26-verify-two-slots/research.md`: its mention of the unmerged `feat/verify-slots` lane.

## Files a change would have to touch (read, or found by grep)

- `scripts/verify_lock.py`: `hold_admission`, `inherit_env`, `_Admission` (`pass_fds`, `_publish`, `release`), `_independent_admission_guard`, the `_ACTIVE` and `_ACQUIRING` globals, and `supervise()`.
- `scripts/stage2.py`: every `hold_admission` call site and the `_lock_fds` helper.
- `scripts/verify_run.py`: the `hold_admission` block around the protected gates.
- `tests/test_verify_lock.py`: the single-admission refusal test, the `_ACTIVE` assertions, and the nesting tests.
- `tests/test_stage2.py` and `tests/test_verify_before_admission.py`: monkeypatched `hold_admission` stubs whose signatures a change would alter.
- `docs/WORKFLOW.md` and `docs/how-it-works.md`: the descriptions of the admission.
- `scripts/kit/manifest.yaml` and `scripts/ci_gates.py`: entries that name the module, which may need an update if the module's public surface changes.

I did not read `scripts/verify_run.py` or `scripts/stage2.py` in full, so the call-site claims above are from grep.
