---
title: "Research — red-first-own-refs"
status: draft
implementation_status: none
date: 2026-11-01
last_reviewed: 2026-11-01
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-wkxm
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "stage-2 explore, 2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
---

# red first own refs — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-01: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 807 files, 2946 commits, 12 rules.

## Runner exploration — 2026-11-01

The research is complete. Here is the content for `plans/changes/red-first-own-refs/research.md`, ready for the runner to append below the existing stage-2 call line.

---

Suggested frontmatter addition (the skeleton lacks it; the sibling research `plans/changes/red-first-pytest-failed/research.md` carries the same field):

```yaml
neighbours:
  - plans/changes/red-first-install/spec.md
  - plans/changes/red-first-pytest-failed/spec.md
  - plans/changes/stage2-repair/spec.md
  - plans/changes/guard-test/research.md
  - plans/changes/repair-fixed-line-format/findings.md
  - plans/changes/terms-expiry/findings.md
```

# red first own refs — Research

## What exists today

**The red-first proof and its ref protection.** `red_first` (`scripts/stage2.py`, function `red_first`) runs the repair's named test against the baseline's code in a detached scratch worktree: `git worktree add --detach` at the baseline, the attempt's whole `tests/` copied over it, the runner-owned probe written in (`RED_PROBE_NAME`, `RED_PROBE_SOURCE`; the constant block near the top of the file, whose header comment says the probe records "what pytest actually did"), an interpreter pre-check, then exactly the named selector under `RED_FIRST_MINUTES` (the constant's comment: a red-first run that has not ended after this many minutes is stopped). Around the pytest run stands a ref guard: `_ref_targets` (function `_ref_targets`) lists every ref with `git for-each-ref --format=%(refname) %(objectname)` — **no prefix pattern is passed**, and its docstring states the scope: "Every ref of the repository, remote-tracking ones included". `red_first` snapshots before the run (the comment there: "Branches are shared with the temporary checkout; a failed snapshot fails the attempt, because branch state could not be proven preserved") and compares in its `finally` block. Any difference in a ref's name or target fails the proof with the refs named — "refs changed while the named test ran: …" — and, per the docstring, "nothing is deleted, so another session's branch is never touched (phase 6, F-6 and F-7)".

**Where that rule comes from.** Phase 6 of `stage2-repair` (`plans/changes/stage2-repair/findings.md`, the Codex table of 2026-10-12, bead coding-harness-g2f): row **F-6** (BLOCKER) — cleanup deleted a branch another session created while the red-first test ran, and the finding's own text records the design limit: "The snapshot records no ownership information and covers all refs, including remote-tracking refs. Cleanup must preserve refs created by other sessions." Row **F-7** (BLOCKER) — the snapshot stored ref names without targets, so a moved branch passed as red first. Both fixes are pinned today by `tests/test_stage2.py`: `test_a_ref_created_while_the_named_test_ran_fails_the_proof_and_is_never_deleted` (docstring "Phase 6, F-6"; its planted test creates `refs/heads/red-first-probe` from the scratch checkout with plain `git branch`, the proof fails with that ref named, and the test asserts the branch still stands in the root's `for-each-ref` — which also demonstrates that a scratch checkout's git writes land in the shared, linked worktree's ref store) and `test_an_existing_ref_moved_while_the_named_test_ran_fails_the_proof` (docstring "Phase 6, F-7"; a moved `refs/heads/keep-me` fails the proof).

**The fixed-code proof compares refs too, but names none.** `fixed_test_proof` (`scripts/stage2.py`, function `fixed_test_proof`) runs the same named test on the fixed code — in the real worktree, `root` itself as cwd — and snapshots `_ref_targets(root)` and `worktree_tree(root)` around the run. On a difference it sets the fault "refs changed while the fixed-code proof ran" (its docstring: "A proof that changes the tree or any ref is refused, and no changed ref is deleted or reset"). Unlike `red_first`'s message, this refusal **does not name which refs changed** — the two proofs' diagnostics are asymmetric by construction.

**The runner's own refs live in that same compared namespace.** `save_attempt` (function in `scripts/stage2.py`) writes `refs/stage2/attempts/<change>/<label>-<stamp>` via `git update-ref` on every failed attempt (docstring: "The ref lives under `refs/stage2/attempts/`, which no branch push carries"); `checkpoint` (function `checkpoint`) creates the one checkpoint commit on the current branch — inside one repair run this happens after both proofs (`check_repair_answer` calls `red_first` and then `fixed_test_proof` per fixed code row; the checkpoint calls sit at the repair flow's end), but another session's checkpoint moves that session's branch ref in the same shared git dir. Worktrees under `.claude/worktrees/` are linked worktrees: one ref store for every session. The 2026-10-31 handover (`docs/journal/handover/2026-10-31-night-and-day-run.md`, "Working state and parallel-session boundary") lists seven active worktrees from one night, so concurrent proof windows are the normal case, not an edge.

**Recorded real refusals from ref movement.** Two exist in the tree. `plans/changes/repair-fixed-line-format/findings.md`, attempt-1 diagnostics of 2026-10-26: "L1-9: tests/test_stage2.py::test_repair_malformed_fixed_claim_still_conflicts: refs changed while the named test ran: refs/heads/decide/terms-expiry" — a decision branch of the terms-expiry change appeared during the red-first window and failed the attempt. `plans/changes/terms-expiry/findings.md`, attempt-2 diagnostics of 2026-10-27: "F6-6: tests/test_stage2_terms_expiry.py::test_dispatch_time_warnings_reach_every_callers_evidence: fixed-code proof: refs changed while the fixed-code proof ran" — with no ref named (that message cannot name one), and the same file's attempt-1 diagnostic records `make verify` stopped by the runner's 30-minute step limit; the repair went on to a third attempt.

**The contract of record and the series.** `plans/changes/red-first-install/spec.md` (bead coding-harness-omp) holds the ref-protection contract in criterion 8: after a baseline check, "the existing worktree cleanup and shared-reference protection still apply", refuted by "a leftover scratch worktree, an undetected created or moved reference, or cleanup deleting another session's reference". Its successor `plans/changes/red-first-pytest-failed/spec.md` (bead coding-harness-a7m) amended the failure classification, not the ref guard, and its non-goals explicitly exclude "any change to routing, attempts, timeouts, scratch-checkout construction, cleanup, ref protection or credential scrubbing". The doctrine wording is generic and may stand: `prompts/04-implement.md` ("A code row needs a test that is red first — it fails on the baseline's code — and the runner runs that proof itself") and `docs/WORKFLOW.md` ("Two columns for every stage-2 change": the finding's own test does not count as `Broke a test` because "the evidence rule expects it to be red first").

**A neighbour edits these seams.** `guard-test` (bead coding-harness-0ho) is an active change on the same function: its research (`plans/changes/guard-test/research.md`, "Current draft gap checks — 2026-10-29", read at `9987eaca` in the `guard-test-redraft` worktree) states that `fixed_test_proof` already uses "…tool checks and tree/ref snapshots" and that a guard mode "can reuse this execution boundary". `plans/changes/red-first-install/decisions.md`, detail 3, records the standing coordination duty: both that change and guard-test edit `red_first` in `scripts/stage2.py`, so an implementation lands after or rebases onto it.

## Where it lives

- `scripts/stage2.py` — `_ref_targets` (the all-refs listing); `red_first` (snapshot, compare-in-`finally`, the named-refs refusal message); `fixed_test_proof` (snapshot of refs and tree, the unnamed-refs refusal message); `RED_PROBE_NAME`/`RED_PROBE_SOURCE`/`RED_FIRST_MINUTES`; `save_attempt` (writes `refs/stage2/attempts/…`); `checkpoint` (the commit that moves the current branch); `worktree_tree` (the tree digest beside the ref digest).
- `tests/test_stage2.py` — the ref-protection cluster: `test_the_red_first_run_leaves_no_worktree_behind` (asserts `for-each-ref` unchanged across a whole repair), the F-6 test, the F-7 test, and `test_a_failed_worktree_remove_leaves_no_dead_entry_and_is_named` beside them; the red-first classification cluster under the comment heading "The red-first outcome classification (bead coding-harness-omp)"; `save_attempt` behavior tests at the `refs/stage2/attempts/demo/` assertions (several sites, e.g. the implement-attempt and draft-attempt ref checks).
- `plans/changes/red-first-install/spec.md` — criterion 8, the living ref-protection sentence.
- `plans/changes/stage2-repair/findings.md` — F-6 and F-7, the origin rows with the "no ownership information" statement.
- `plans/changes/repair-fixed-line-format/findings.md` (L1-9) and `plans/changes/terms-expiry/findings.md` (F6-6) — the two real refusals.
- `plans/changes/red-first-pytest-failed/research.md`, `spec.md`, `decisions.md` — the series' predecessor and its interview answers Q-1/Q-2.
- `plans/changes/guard-test/research.md` and `plans/changes/red-first-install/decisions.md` (detail 3) — the coordination duty on the shared function.
- `prompts/04-implement.md`, `docs/WORKFLOW.md` — the doctrine wording.

## What is unclear

1. **The bead's own text is not readable.** The tracker is the Dolt database under `.beads/`, transported via `refs/dolt/data` on origin (repository `AGENTS.md`, house rule 2); no rendered copy is committed, and a Grep over this worktree's `.beads/` files (including `interactions.jsonl`) finds no line for `coding-harness-wkxm`. What the maintainer means by "own refs" is therefore nowhere on record in this tree — this research states the candidate readings with their evidence, not a choice.
2. **Four readings the tree supports**, each anchored in facts above: (a) the runner family's own refs — `refs/stage2/attempts/…` that any lane's `save_attempt` writes into the shared store during another lane's proof window; (b) the blind comparison scope — `_ref_targets` covers remote-tracking refs and every other ref (its docstring; no pattern argument; stage2-repair F-6 already named the remote-tracking coverage as a design property); (c) refs the scratch checkout's named test itself creates — worktrees share branches (`red_first`'s snapshot comment), and the F-6 test pins that such a ref fails the proof and must never be deleted, so a repair whose named test legitimately exercises git cannot pass today; (d) only the fixed-code proof's diagnostic gap — it refuses without naming the refs that moved, where `red_first` names them.
3. **Which refs moved in the terms-expiry F6-6 refusal was never identified**: the message names none by construction, and no file in this tree records the ref set (searched: the findings file's diagnostics and the surrounding entries). This is "not found", not "nothing moved".
4. **No test pins the fixed-code proof's ref branch.** A Grep for "refs changed while" over the whole worktree returns the two `red_first` tests and the two findings diagnostics — no test exercises `fixed_test_proof`'s ref-difference branch. Stated as "not found by that search", not "not there by design".
5. **No exclusion or own-namespace mechanism exists today.** Nothing in `scripts/stage2.py` scopes the snapshot to a ref prefix, and no test asserts that `refs/stage2/**` is inside or outside the comparison (Grep over `tests/` for `refs/stage2` finds only `save_attempt` behavior tests). Whether `refs/stash`, remote-tracking movement by a fetch, or a sibling's checkpoint branch should count as "own" or as "neighbour" is decided nowhere in the tree.
6. **Guard-test's current diff is unreadable from this worktree**; only its research's reuse statement is on record. The branch was not read — not "the branch changes nothing here".

## Files a change would have to touch

- `scripts/stage2.py` — `_ref_targets` (any scope or ownership change to the listing), the snapshot/compare blocks and refusal messages of `red_first` and `fixed_test_proof`, possibly `save_attempt` and `checkpoint` if own refs get a namespace or a timing of their own; the docstrings of both proofs state the rule and would need to say the new one.
- `tests/test_stage2.py` — the ref-protection cluster (the no-worktree test, F-6, F-7, the failed-removal test) pins today's any-difference-fails rule and would change meaning; the fixed-code proof's ref branch has no test today (unclear item 4), so that coverage point is new either way.
- `plans/changes/red-first-install/spec.md` — its criterion 8 is the contract a change would amend; how the amendment relates to that living spec is a workflow question for the spec phase, stated here only as the point of contact (the predecessor research did the same for its predecessor).
- `prompts/04-implement.md` / `docs/WORKFLOW.md` — only if the doctrine wording ("fails on the baseline's code", "the evidence rule expects it to be red first") must name the ref rule; both are generic today.
- `plans/INDEX.md` — the runner renders it; the change folder's row already exists (bead coding-harness-wkxm, draft, none).
