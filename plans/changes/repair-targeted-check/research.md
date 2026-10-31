---
title: "Research — repair-targeted-check"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-gxwg
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# repair targeted check — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 788 files, 2822 commits, 12 rules.

## Runner exploration — 2026-10-31

Research complete. Here is the report, ready to append to `plans/changes/repair-targeted-check/research.md`.

---

## What exists today

**The decision this change builds on.** The maintainer decided on 2026-10-30 (bead `coding-harness-24ag`) that after a hand repair by the orchestrator, a *targeted check* stands in for a full `make verify`: the touched and linked test files, `ruff` on the touched files, and the gates the touched kinds of file feed; one full `make verify` still runs on the final head before phase 6 and before the pull request leaves draft, and CI stays the full gate (`docs/WORKFLOW.md`, §4, "Hand repairs by the orchestrator", last bullet, lines 1606–1617). The stated reason: a full `make verify` takes 12 to 13 minutes under the machine's one verify lock, and a hand repair touches a few files. A runner repair keeps the runner's own `make verify`. The same rule appears in `prompts/04b-review-loop.md` (step 3 of "For the orchestrator", lines 90–97) and in the phase-4b row of the workflow table in `AGENTS.md`.

**The targeted check is doctrine only — no code implements it.** A case-insensitive search for `targeted` over `scripts/` finds no match at all. Over `tests/` it finds only two unrelated hits (`tests/test_stage2_research_snapshot.py:248`, "a retargeted link"; `tests/test_kit.py:298`, "the mutation targeted the catch-all rule") — no test pins the doctrine. Over `prompts/` only `prompts/04b-review-loop.md:93` matches. Over `docs/` only `docs/WORKFLOW.md:1606` and `AGENTS.md` match. `tools/` matches are all under `tools/pi/node_modules/` (vendor code, not harness code). Nothing in the runner performs, enforces or records a targeted check today; the orchestrator runs it by hand with its own tools.

**The pieces the doctrine names, as they exist today:**

- *The touched files.* `scripts/touch_map.py` ("what a pull request touches, as a list and a collapsed Mermaid map", docstring lines 1–49) is the tool the doctrine names for "the test files `scripts/touch_map.py` links to the touched code". It takes `BASE HEAD` commits, classifies files as code/test/runner/other, and draws four link kinds (`tests` — a test names or imports a file; `runs`; `reads`; `imports`). Its docstring states "Nothing is read from the working tree or the network. The script asks git for objects only" — it reads committed objects, not uncommitted edits.
- *The touched files, working-tree-aware.* `changed_paths(root, env, against="HEAD")` in `scripts/stage2.py:4005` lists tracked changes in working tree and index plus untracked files — the mechanism the runner itself uses to know what an attempt touched, including uncommitted work.
- *The gates the touched kinds of file feed.* The one gate list is `decisions/gates.yaml` (header comment: "THE ONE LIST (D-10/O-4, bead coding-harness-bo0)"): 20 verify/drift gates, each with `id`, `command`, `enforcement`, `placement`, optional `needs_tracker`/`needs_history` and optional `subsets`. The four gates the doctrine names as examples all exist there: `plans-registry` (`plans_registry.py --check`), `frontmatter-current` (`check_frontmatter_current.py`), `criterion-ledger` (`check_criterion_ledger.py`), `ci-drift` (`ci_gates.py --check-ci`). There is no mapping in code from a touched file's kind to the gates that cover it; a reader derives it from the gate list by hand.
- *A partial verify already exists.* `bash scripts/verify_all.sh --job docs` runs only the gates with `subsets: [docs]` (bead `coding-harness-77qj`; `scripts/verify_all.sh` lines 10–13 and 118, `decisions/gates.yaml` `subsets` schema comment lines 39–44). This is a file-kind-independent subset, not a touched-files subset.
- *The lock the doctrine avoids.* `make verify` runs `scripts/verify_all.sh` (`Makefile:18–19`), which under admission execs itself through `python3 -m scripts.verify_lock` (`scripts/verify_all.sh:89–100`). `scripts/verify_lock.py` (docstring lines 1–70) is the one machine-wide admission (queue, free-memory check; bead `coding-harness-p6mu`), shared across repositories and worktrees via `${XDG_STATE_HOME:-~/.local/state}/coding-harness/`. The doctrine says the targeted check runs "outside the lock" (`docs/WORKFLOW.md:1610`). The runner's own targeted pytest runs take the opposite route: `red_first`, `fixed_test_proof` and the import probe each wrap their pytest in `verify_lock.hold_admission(...)` (`scripts/stage2.py:5781, 5887, 5909`), and `verify_attempt` and `verify_draft` hold admission around `make verify` (`scripts/stage2.py:5382, 7490`).
- *The closest in-runner analogue.* `cheap_checks(root, env, plan, key, accepted_plan, previous)` (`scripts/stage2.py:5227`) runs ruff lint and format checks over the changed Python files plus pytest over exactly the selected tests before full verification (bead `coding-harness-5tyh`); its contract comment (`scripts/stage2.py:3792–3798`) states "cheap green never replaces full verification, it only earns the right to run it" — explicit targets as argv, never discovery.

**The hand-repair workflow the targeted check belongs to** (`docs/WORKFLOW.md` §4, "Hand repairs by the orchestrator", lines 1588–1605; each bullet marked as learned on the night of 2026-10-29/30): the orchestrator sets the row's status cell to `fixed — tests/<path>::<function>` or `fixed — not a test — <reason>` and its `Broke a test` cell from the evidence, after a backup of `loop.md`; a header or status edit regenerates the index via `scripts/plans_registry.py --index`; after local midnight `scripts/check_frontmatter_current.py --stamp` takes the local date. The runner side already cooperates: `repair_targets` (`scripts/stage2.py:2811`) treats `fixed` rows as decided, `legacy_completed` (`scripts/stage2.py:2845`, `LEGACY_FIXED` at 2842) refuses the legacy `; fixed by` / `; fixed:` / `; repaired by` spellings with instructions to book the hand repair canonically (refusal message at `scripts/stage2.py:7714–7722`; tests `tests/test_stage2.py::test_repair_skips_canonical_hand_repairs_in_every_location` at 8411 and `::test_repair_refuses_legacy_completed_taken_statuses_before_call` at 8516 — the `repair-fixed-lines` change, bead `coding-harness-ugi`). The loop holds the next round while taken rows are unrepaired with the message "run `repair` and make `make verify` green before the next round starts" (`scripts/stage2.py:7930–7937`) — this message does not mention the targeted-check alternative. The loop record lives outside the repository at `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>@<digest>/loop.md` (`scripts/stage2.py:122`, `record_dir` at 3023).

**The origin night.** `plans/changes/verify-machine-lock/plan.md`, time ledger lines 173–177, records 2026-10-29/30: review-loop rounds 1–4 and phase 6 of the machine-lock change, with rows "repaired by the orchestrator, each test red first" — the situation the three hand-repair follow-ups (and the targeted check) were learned from.

**Precedent for targeted tests instead of full verify.** `plans/changes/review-loop-deep-b/findings.md:170` records a phase-6 review whose checked line says "54 targeted tests run and passing … the full `make verify` was not run" — a targeted check performed by hand before the doctrine existed.

## Where it lives

- Doctrine: `docs/WORKFLOW.md` ("Hand repairs by the orchestrator", lines 1588–1617), `prompts/04b-review-loop.md` (lines 90–97), `AGENTS.md` (phase table row 4b and the "Findings returned as text" bullet).
- Touch/links: `scripts/touch_map.py` (spec of record: `plans/changes/archive/2026-10-06-touch-map/spec.md`, referenced in its docstring line 9).
- Gate list: `decisions/gates.yaml`; gate runners `scripts/verify_all.sh`, `scripts/ci_gates.py`; admission `scripts/verify_lock.py`.
- Runner surfaces the doctrine touches today: `repair_targets` and `legacy_completed` (`scripts/stage2.py:2811, 2845`), the unrepaired-rows refusal (`scripts/stage2.py:7930–7937`), `cheap_checks` (`scripts/stage2.py:5227`), `changed_paths` (`scripts/stage2.py:4005`), the pytest proofs under admission (`scripts/stage2.py:5755–5949`).
- Tests that pin the neighbouring behaviour: `tests/test_stage2.py` (repair row handling, 8366–9159), `tests/test_verify_lock.py`, `tests/test_touch_map.py`, `tests/test_ci.py` (pins Makefile against the gate list).

## What is unclear

- The bead `coding-harness-gxwg` description was **not read** — this phase has no tracker access; the class the bead description is supposed to name (house rule, 2026-10-22) is unknown here. The change's `research.md` frontmatter carries no `class:` field (`scripts/new_change.py`, `_frontmatter_template`, writes none), so the explore route needs `--class` or a later spec header. The neighbouring repair changes `repair-fixed-lines` (ugi), `repair-restore-status` (rcyf) and `verify-machine-lock` (p6mu) all declare `class: bounded, appetite: 1–3`; that is their fact, not this change's declaration.
- "The gates the touched kinds of file feed" has no code mapping today — no file-kind→gate table exists in `scripts/` (not found; the gate list carries per-gate `subsets`, nothing per file kind). What resolves it for a given hand repair is currently the orchestrator's judgment, per the doctrine's "for example" wording.
- `scripts/touch_map.py` reads committed git objects only ("Nothing is read from the working tree", docstring line 11), while a hand repair's touched files may be uncommitted; how the doctrine's "test files `touch_map.py` links to the touched code" step is meant to run on uncommitted work is not stated anywhere I found.
- The doctrine's "outside the lock" (`docs/WORKFLOW.md:1610`) and the runner's own practice of wrapping every timed pytest in `verify_lock.hold_admission` (`scripts/stage2.py:5781, 5887, 5909`) state different relations to the machine admission; which one a mechanised targeted check would take is not decided in any text I found.
- The full-verify-measurement figures differ between sources: `docs/WORKFLOW.md:1607–1608` says 12–13 minutes (measured 2026-10-30); `plans/changes/verify-machine-lock/spec.md:32–33` says 11–12 minutes sequentially (measured at the 2026-10-28 three-lane trial). Both are prose; no measurement record under `docs/research/` was found for either (not found).
- Nothing records that a targeted check happened: no row cell, no runner line, no gate — the `Broke a test` mark stays the orchestrator's (`docs/WORKFLOW.md:1547–1549`), and the loop refusal message (`scripts/stage2.py:7935`) still names only `make verify`. Whether the next round should accept a recorded targeted check in place of a green `make verify` is stated in doctrine ("Green, the next round starts") but unenforced in code.

## Which files a change would have to touch

- `scripts/stage2.py` — wherever the check is mechanised: the unrepaired-rows refusal (7930–7937), the repair verb's post-run path (`run_attempts` call at 7760–7780), or a new verb in the `VERBS` dict (`scripts/stage2.py:8360–8371`) with its `main()` argument wiring (8374–8441).
- `scripts/touch_map.py` or a caller of it — if linked test files must be derived for uncommitted touches; `scripts/stage2.py` `changed_paths` (4005) is the working-tree-aware alternative already in the runner.
- `decisions/gates.yaml` / `scripts/ci_gates.py` / `scripts/verify_all.sh` — only if a file-kind→gate mapping or a new job/subset is to be derived from the one list; `tests/test_ci.py` pins Makefile and gate list together.
- `docs/WORKFLOW.md`, `prompts/04b-review-loop.md`, `AGENTS.md` — the three texts that currently carry the doctrine and would need to follow any behaviour change.
- `tests/test_stage2.py`, `tests/test_verify_lock.py`, `tests/test_touch_map.py` — where the neighbouring behaviour is pinned today; no test currently names a targeted check.

## Neighbours

- `plans/changes/verify-machine-lock/spec.md` (bead `coding-harness-p6mu`) — the machine admission the doctrine routes around; its `plan.md` time ledger holds the hand-repair night.
- `plans/changes/repair-fixed-lines/spec.md` (bead `coding-harness-ugi`) — the canonical `fixed — …` status both writers share.
- `plans/changes/repair-restore-status/spec.md` (bead `coding-harness-rcyf`) — findings.md restored after a refused repair attempt.
- `plans/changes/repair-fixed-line-format/spec.md` (bead `coding-harness-hgvp`) — the fixed line's format.
- `plans/specs/implementation-verification/spec.md` (bead `coding-harness-mfv`) — the accepted living spec on runner verification preparation (stamp → index → `make verify`).
- `plans/changes/loop-until-clean/plan.md` — the loop-round repair records the timing ledger form comes from.
- `plans/changes/archive/2026-10-06-touch-map/spec.md` — the touch map's own spec.

## Draft gap checks — 2026-10-31, baseline `9eae5d26`

- The interview now declares `bounded` and explicitly extends targeted checking
  to runner repairs; this supersedes the exploration's uncertainty about class
  and the workflow's sentence retaining full verification after runner repairs.
- `review()` currently proceeds from preflight and undecided-row checking to
  the reviewer call without running full verification or checking a receipt.
  Running full verification there avoids introducing a persistent receipt.
- `verify_attempt()` holds admission around formatting, cheap checks, derived
  preparation and full verification. `run_attempts()` calls it for both
  implementation and repair; verification mode must therefore be explicit,
  with the existing full mode retained as the default.
- `ci_gates.gates()` exposes validated commands, enforcement, placement and
  document-subset membership. Selection can refer to gate identifiers without
  copying commands or changing the gate schema. No file-kind mapping exists.
- `touch_map.links()` works over a snapshot's path inventory and source reader;
  a working-tree adapter can reuse those rules without changing its committed
  comparison command. Baseline links remain necessary for removed paths.
- `scripts/validate_change_artefacts.py` and a plan template under `templates/`
  are absent. Use the spec template and the phase-3 prompt's plan form; do not
  build either missing artifact as part of this change.
