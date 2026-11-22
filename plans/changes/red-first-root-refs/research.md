---
title: "Research — red-first-root-refs"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-dk0h
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-22", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# red first root refs — Research

Stage-2 call, 2026-11-22: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1167 files, 5343 commits, 12 rules.

## Runner exploration — 2026-11-22

Exploration complete. Here is the research, ready to append below the stage-2 call line in `plans/changes/red-first-root-refs/research.md` (I ran no writes; the runner owns the file).

---

## What exists today

**This change is the parked F-10 of its predecessor.** The last phase-6 row of `plans/changes/archive/2026-11-16-red-first-own-refs/findings.md` (F-10, MAJOR, SPEC, parked 2026-11-03) records the exact gap: a qualifying named test can run `git update-ref ORIG_HEAD HEAD` and leave a persistent reference change that both proofs accept, because "`_proof_ref_targets` enumerates `refs/` and HEAD only; `_ref_targets` likewise omits other root references". The row is parked as a named limit ("re-check 3 of the three the maintainer allowed on 2026-11-02 ended here") and carries the proposed remedy verbatim: "measure every root reference Git reports (`git for-each-ref --include-root-refs` where the pinned Git has it, else the files directly under `.git/` that `git rev-parse --verify -q` resolves), through the same logical name → kind and target map". The 2026-11-03 handover (`docs/journal/handover/2026-11-03-five-lane-night.md`, "Needed from the maintainer", item 1) recommended merging #320 with F-10 as a follow-up bead; that bead is `coding-harness-dk0h` (commit 74ede5da opened this change folder on 2026-11-22).

**The contract this change completes is already written.** The predecessor spec's criterion 2 (`plans/changes/archive/2026-11-16-red-first-own-refs/spec.md`, "Acceptance criteria", item 2) refuses a proof when "reference names or targets … differ in the proof repository", refuted by "a qualifying pytest outcome being accepted despite a changed proof reference, including one outside the branch namespace" — a root reference is exactly such a namespace, so F-10 is the not-yet-enforced remainder of an accepted criterion, not a new contract. The older series contract, `plans/changes/archive/2026-11-06-red-first-install/spec.md`, carries a dated amendment (2026-11-01, lines 35–43) that scopes its criterion-8 reference-change refusals to "the proof's private store"; this change widens what a move in that private store covers.

**The proof machinery the change lands on.** Three proof paths share the ref guard:

- `red_first` (`scripts/stage2.py`, function `red_first`) — baseline proof, private repository of its own.
- `fixed_test_proof` (function `fixed_test_proof`) and `guard_test_proof` (function `guard_test_proof`, ADR 0023's planted/clean legs) both delegate to `_attempt_tree_proof` (function `_attempt_tree_proof`) — the one execution the fixed-code proof and the guard proof share.

Each proof builds a private repository through `_private_repository` (function): local `git clone --quiet --no-hardlinks`, refusal on `objects/info/alternates`, `remote remove origin`, then one `update-ref --stdin` transaction that detaches HEAD and restores every source ref under its own name (the source's refs are read, never written), then `read-tree --reset -u <checkout>`. The private store therefore starts without any root reference: the restore loop consumes `_ref_targets`, which lists only `refs/` names plus `HEAD`.

**Two measurements stand around every run, both on the private store.** The logical one, `_proof_ref_targets` (function), walks `.git/refs` on the filesystem (any non-regular entry raises `Refused` — the F-9 fifo protection), adds `HEAD` (must be a regular file), parses `packed-refs` (only lines whose name starts with `refs/`; anything else raises `Refused("the private packed-refs listing is malformed")`), then resolves each name with `symbolic-ref --no-recurse -q` → `("symbolic", target)` or `rev-parse --verify -q` → `("object", oid)`. The raw one, `_ref_targets` (function), is `for-each-ref --format=%(refname) %(objectname) %(symref)` plus an explicit `HEAD` entry. Snapshot sites: `_attempt_tree_proof` (before the launch) and `red_first` (where a `Refused` refuses the proof as "the red-first ref snapshot failed"). The post-run comparison, `_proof_reference_guard` (function), re-measures both maps in `finally`, before `_remove_private` deletes the store, and emits the shared scrubbed verdict "refs changed while the named test ran: <names>" — `test_proofs_share_reference_guard_verdicts` (`tests/test_stage2.py`) pins that both proof paths produce identical verdicts, and `test_proofs_refuse_raw_reference_measurement_failure` pins that a failed re-measurement refuses and still removes the private store.

**Neither measurement sees a root reference today.** `for-each-ref` lists the `refs/` namespace; the walk reaches only `.git/refs` and the `HEAD` file. The files Git keeps directly under `.git/` — `ORIG_HEAD`, `FETCH_HEAD`, `MERGE_HEAD` and the like, as F-10 names them — are invisible to both. That acceptance is recorded by F-10 itself; a search for `ORIG_HEAD|FETCH_HEAD|MERGE_HEAD|CHERRY_PICK_HEAD|include-root-refs` over the whole tree returns no test, no runner use and no other proof-side reference (the only hits are F-10, the 2026-11-03 handover line, and unrelated merge-marker checks in `scripts/check_worktree_state.sh`, `scripts/pr_sync.py` and `scripts/close_merged_beads.py` — different mechanisms). "Not measured" is pinned by the F-10 record; "no test exercises the acceptance" is this search's result — not found, stated as such.

**The regression cluster a change lands beside** (all in `tests/test_stage2.py`): `test_proofs_accept_packing_unchanged_refs` (F-8: `pack-refs --all` over unchanged refs accepted), `test_proofs_refuse_fifo_refs_promptly` (F-9: a fifo at `.git/refs/heads/probe` is refused promptly and cleaned up), `test_proofs_refuse_dangling_symbolic_ref` (F-7), `test_proofs_refuse_symbolic_ref_at_same_commit` (F-5), `test_proofs_refuse_head_attachment_at_same_commit` (F-4), `test_proofs_preserve_existing_symbolic_refs` (F-6: a symbolic `refs/remotes/origin/HEAD` already in the source must not break setup), `test_proofs_refuse_raw_reference_file_changes` (parameterized over `HEAD` / `packed-refs` / `refs/heads/unresolved` × rewrite/delete: raw file rewrites that keep logical equality are accepted, real logical changes refused), `test_proofs_ignore_foreign_ref_changes` and `test_proofs_ignore_source_ref_created_after_clone` (source movement is never this proof's business), `test_proofs_refuse_detached_head_commits`, `test_proofs_refuse_private_ref_changes`. Shared helpers: `plant_proof`, `run_proof`, `ref_writing_test`.

**Two structural seams F-10's remedy touches** (observed in code, not decided here):

1. The `packed-refs` parser refuses any non-`refs/` name as malformed (`_proof_ref_targets`, the `startswith("refs/")` check). Root-ref names in a `packed-refs` file would refuse as malformed today; whether the measurement and this refusal should agree on such lines is written nowhere.
2. F-9's nonregular-entry protection covers `.git/refs` entries and `HEAD` only; a nonregular entry directly under `.git/` (say a fifo named `ORIG_HEAD`) is neither measured nor refused today. Parity is a decision the spec phase makes.
3. `_private_repository` restores exactly what `_ref_targets` returns: widening `_ref_targets` widens clone setup (the `update-ref --stdin` transaction and the symbolic restore loop); keeping it narrow confines root-ref listing to the proof measurement functions. Both readings fit the code's current shape.

**Git-launch and guard rails.** The one git launch is `run_git` (function, "The one launch of git in the runner (decisions.md#Q-8)"), wrapped by `_git_output`; `GIT = resolve_git()`. The AST guard `test_no_git_launch_in_the_runner_names_a_bare_git` (`tests/test_stage2.py`) now asserts exactly one command list names GIT — the one inside `run_git`. Constants: `RED_FIRST_MINUTES = 10`, `RED_PROBE_NAME`/`RED_PROBE_SOURCE`, `GUARD_SWITCH = "STAGE2_PLANT_FAULT"`. ADR 0023 (`docs/adr/0023-guard-proof-for-test-only-repairs.md`) and the doctrine wording `docs/WORKFLOW.md`, "Guard test" — "the existing outcome, environment, runtime and integrity guards of red first apply to both runs" — mean any guard change automatically reaches the guard proof's planted and clean legs.

**Git-version facts found, and their limit.** `plans/changes/harness-decide-adr/research.md` ("Local tools") records git 2.55.0 locally and CI on `ubuntu-latest`; `docs/journal/handover/2026-10-17-night-run-sixth.md` mentions "measured Git 2.56.0" in another change's plan. I found no pinned Git version in the tree (searched `pinned Git`, `git 2.`, `git version`); the two records are observations, not pins. Whether `for-each-ref --include-root-refs` and root-ref support in `update-ref --stdin` transactions exist on every Git the proofs meet cannot be read from this tree — F-10's remedy already names the filesystem fallback for exactly that.

## Where it lives

- `scripts/stage2.py` — `_ref_targets` (raw listing, `refs/` + HEAD); `_proof_ref_targets` (logical map: `.git/refs` walk, HEAD, `packed-refs` parser, kind/target per name); `_proof_reference_guard` (shared post-run verdict); `_private_repository` (clone, alternates refusal, ref restore transaction, symbolic restore loop); `_remove_private`; `_attempt_tree_proof` (shared fixed/guard execution, snapshot sites, docstring stating the guard rule); `red_first` (baseline proof, snapshot site, docstring); `fixed_test_proof`, `guard_test_proof` (entry points and docstrings); `run_git`/`_git_output`/`GIT` (launch choke point); `RED_FIRST_MINUTES`, `RED_PROBE_NAME`, `RED_PROBE_SOURCE`, `GUARD_SWITCH`.
- `tests/test_stage2.py` — the proof-ref cluster (`test_proofs_share_reference_guard_verdicts` through `test_proofs_refuse_raw_reference_measurement_failure`, plus `test_proofs_refuse_post_run_ref_exception_and_remove_repository`, `test_proofs_remove_private_repositories_on_all_exits`, `test_private_repository_restores_many_refs_in_one_process`); the AST git-launch guard; helpers `plant_proof`, `run_proof`, `ref_writing_test`.
- `plans/changes/archive/2026-11-16-red-first-own-refs/` — predecessor research, spec (criterion 2 and the "in any namespace" definition of Reference change), findings (F-1–F-10 with the whole symbolic/packing/fifo repair history), decisions.
- `plans/changes/archive/2026-11-06-red-first-install/spec.md` — criterion 8 and the 2026-11-01 amendment scoping refusals to the private store; `plans/changes/archive/2026-11-06-red-first-pytest-failed/spec.md` and `plans/changes/archive/2026-11-06-stage2-repair/findings.md` — the series' earlier contract and the original F-6/F-7 ref-protection rows.
- `docs/adr/0023-guard-proof-for-test-only-repairs.md`, `docs/WORKFLOW.md` ("Guard test", red-first evidence wording), `prompts/04-implement.md` — doctrine that states the guard rule generically.

## What is unclear

1. **The bead `coding-harness-dk0h`'s own text is not readable in this tree.** The tracker is the Dolt database (repository `AGENTS.md`, house rule 2); a Grep finds the id only in `plans/INDEX.md` (row: draft, none, 2026-11-22) and the change folder's own files. Whether the bead says more than the F-10 row is unknown — not read, not "nothing more".
2. **No Git pin exists in the tree**, so the availability of `for-each-ref --include-root-refs` and of root-ref support in `update-ref --stdin` transactions on every machine proofs run on (local 2.55.0 recorded, CI `ubuntu-latest`, cloud environments under `tools/cloud-env/`) is an open question for the spec phase; the filesystem fallback F-10 names is the recorded hedge. This is "not found in the tree", not "unsupported".
3. **Membership vs. measurement is undecided**: whether root references should also be copied into and restored within the private store (`_private_repository`'s snapshot/restore) or only measured around the run is written nowhere; the two designs have different clone-setup blast radii.
4. **`packed-refs` root-ref lines and nonregular root-ref entries** have defined behavior today (malformed refusal; unmeasured) but no recorded decision on what they should do once root refs are measured.
5. **The exact root-reference set is not enumerated anywhere in the tree** — F-10 says "ORIG_HEAD, FETCH_HEAD, MERGE_HEAD and the like"; which names Git actually keeps there (and how `rev-parse --verify -q` behaves for each, absent or present) was not verified against Git documentation in this session.
6. **No active change currently edits these seams.** A grep over `plans/changes/*/spec.md` finds `scripts/stage2.py` mentioned only by `stage2-session` (a new `session` verb) and `review-loop-deep-a` (generic); neither names the proof or ref functions. The strong neighbours are archived: `red-first-own-refs`, `guard-test`, `red-first-install`, `red-first-pytest-failed`, `stage2-repair`.

## Files a change would have to touch

- `scripts/stage2.py` — `_proof_ref_targets` (root-ref entries in the walk, the `packed-refs` parser's stance, per-name resolution); `_ref_targets` or a sibling listing (root refs in the raw measurement, and through it possibly `_private_repository`'s restore); `_proof_reference_guard` only if verdict wording changes; the docstrings of `red_first`, `fixed_test_proof`, `guard_test_proof`, `_attempt_tree_proof` and `_private_repository`, which state today's rule in prose; `run_git`/`_git_output` remain the launch path for any new verb.
- `tests/test_stage2.py` — the proof-ref cluster: `test_proofs_refuse_raw_reference_file_changes` gains root-ref paths in its parameterization; F-4/F-5/F-7 style symbolic and dangling cases get root-ref twins; `test_proofs_refuse_fifo_refs_promptly` gets the under-`.git/` twin if parity is decided; `test_proofs_accept_packing_unchanged_refs` pins the packing interaction; the red-first classification and foreign-movement tests stand unchanged.
- `plans/changes/red-first-root-refs/` — `spec.md` (and the interview's `decisions.md`) to be created; `plans/INDEX.md` is runner-rendered.
- Doctrine files (`docs/WORKFLOW.md`, `prompts/04-implement.md`) likely stand: their wording is generic about the guards and names no reference scope.

## Neighbours (suggested for the header)

`plans/changes/archive/2026-11-16-red-first-own-refs/spec.md` (contract of record, criterion 2) · `plans/changes/archive/2026-11-16-red-first-own-refs/findings.md` (F-10, the origin row) · `plans/changes/archive/2026-11-16-red-first-own-refs/research.md` · `plans/changes/archive/2026-11-06-red-first-install/spec.md` (criterion 8 + 2026-11-01 amendment) · `plans/changes/archive/2026-11-06-red-first-pytest-failed/spec.md` · `plans/changes/archive/2026-11-16-guard-test/research.md` (shares `_attempt_tree_proof` via ADR 0023) · `plans/changes/archive/2026-11-06-stage2-repair/findings.md` (original F-6/F-7).
