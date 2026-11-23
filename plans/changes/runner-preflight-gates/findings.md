---
title: "Findings — runner-preflight-gates"
category: findings
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — runner-preflight-gates

Stage-2 call, 2026-11-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1185 files, 5522 commits, 12 rules.

Stage-2 call, 2026-11-23: spec-review · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1188 files, 5526 commits, 12 rules.
## Phase 2a — fallback deepseek-v4.1-flash, 2026-11-23

Spec fingerprint: sha256:ac6b2318050d927110718707454861a64fbeaa526c4ebffbfa445d96c5a13df6

Spec review commit: e8e79326f4c556afaedde377de95f88b89885d3e

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] MAJOR | SPEC | base | spec.md AC 2; Problem; header | The header and Problem say the waste to prevent is "a fault the attempt cannot fix", but AC 2 stops the run on any blocking document-gate failure. Reading A: any red blocking document gate refuses, including a document fault inside the change folder that the verb itself would rewrite (a stale `updated:` on this change's `spec.md` or `findings.md`, a `plan.md` line `criterion-ledger` rejects, a `research-handoff` neighbours header mismatch), so a second draft round cannot start until the operator hand-edits the files the draft exists to write; the only tolerance stated is the ADR answer. Reading B: only faults outside the verb's writable scope refuse, which requires a per-verb writable-scope rule the spec never states. Both readings satisfy the stated refutation (a fake model records no call), so the criteria and the planned regressions are identical while operator behaviour for every refusal inside `plans/changes/<change>/` differs. | deepseek-v4.1-flash | open | — |
| S-2 | MINOR | SPEC | base | spec.md AC 1 | Cannot go red as written: "non-admitted" selects nothing out. Every gate carrying `subsets: [docs]` is declared `cost: seconds` and none sets `needs_admission`, so `ci_gates.declared_cheap` is true and `gate["admission"]` is false for all of them (`decisions/gates.yaml`; `scripts/ci_gates.py:489-501`), which makes a preflight that also selects admitted gates run exactly the same set. No input the repository presents distinguishes the two, so the qualifier is a statement of intent until a document gate is declared admitted or exempted from the seconds class. The second half of the same criterion's refutation, "uses a separate hand-maintained gate list", is likewise a property of the source and not of any run. | deepseek-v4.1-flash | in spec | — |

Stage-2 call, 2026-11-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1188 files, 5532 commits, 12 rules.

Stage-2 call, 2026-11-23: spec-review · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1188 files, 5536 commits, 12 rules.
## Phase 2a — fallback deepseek-v4.1-flash, 2026-11-23

Spec fingerprint: sha256:66a178146ee2d1165712c32638edae9fe4690526c6eacc230aae2d2331295bee

Spec review commit: efc52ddf39f5a1c5478324a63827d50ccf466753

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| R-1 | [AMBIGUITY] MAJOR | SPEC | base | spec.md AC 2 and its refutation; `## Open decisions` [DECISION]; decisions.md S-1 | AC 2 and its refutation admit only reading A: any red blocking gate refuses, including a fault in a file the verb itself may write — a stale `updated:` on this change's own `findings.md`, an unrendered `plans/INDEX.md` that the runner's own `prepare_derived` (scripts/stage2.py:7758) would refresh before any gate runs after an attempt, a `research-handoff` neighbours mismatch in `research.md`. The [DECISION] block and decisions.md S-1 leave the scope unresolved and prefer reading B, under which that same input must proceed to a model call — exactly what AC 2's refutation calls a failure, so no criterion can express B. B also needs a per-verb writable-scope rule that the spec never states: the draft's is only implied in decisions.md (which the spec marks as not a maintainer answer), and implement and repair have far wider, undefined scopes (scripts/stage2.py:12276, 12850). Both readings satisfy every refutation and yield the same regressions. | deepseek-v4.1-flash | open | — |
| R-2 | [AMBIGUITY] MAJOR | SPEC | base | spec.md AC 1, AC 2, AC 5; scripts/stage2.py:12300-12303, 12955, 13011-13019 | The spec never fixes the boundary at which the gates run. Reading X: once per verb invocation, on the tree as it stands at entry — so the check excludes the runner's own pre-call writes (a repair writes the hand-step listing into `findings.md` at 12955, and a hand-only repair writes it and exits 0 with no model call at 13019), and implement's Flash repair and Sonnet fallback (12300-12303) and repair's Codex retry (13013-13014) start without a new check. Reading Y: before every attempt or route, since each is "about to make its first model call" — which makes a fault the previous attempt itself introduced stop the retry, and refuses a hand-only run that would make no call at all. Every stated refutation holds under both, and the two differ exactly for the incident's pattern (an attempt that leaves a red document behind). | deepseek-v4.1-flash | open | — |
| R-3 | MINOR | SPEC | base | spec.md AC 1 vs `## Open decisions` [DETAIL]; scripts/stage2.py:12498-12507 `document_gates()` | The two stated selections differ and no input can tell them apart. AC 1 fixes the set as `subsets: [docs]` intersected with `ci_gates.declared_cheap` (`scripts/ci_gates.py:499`); the [DETAIL] says to use the existing document-gate selection, which is `document_gates()` — job verify, `local_runnable`, placement not hosted, docs subset — with its callers then dropping `gate['admission']`. Today all eleven docs gates are `cost: seconds`, `placement: both` and have a local command (`decisions/gates.yaml:120-310`), so both readings select the same set and no regression distinguishes them; the divergence appears only for a docs gate declared hosted-only or without a local command, where AC 1 would demand it run, `run_gates` could not, and AC 4 would refuse every start. The spec names no input that refutes either selector. | deepseek-v4.1-flash | in spec | — |
| R-4 | MINOR | SPEC | base | spec.md AC 6 and its refutation | "Preserves the tree" has two readings and the refutation covers neither fully. Reading (i): no tracked path changes, so ignored files may appear; reading (ii): nothing appears under the root at all. The gates AC 1 mandates do write outside the refutation's list — the two `needs_tracker` docs gates render the tracker, markdownlint is spawned as `npx --yes markdownlint-cli2` (`scripts/ci_gates.py:314`), and every `python3 scripts/...` gate may leave `__pycache__` — while the refutation names only a stamped document or a written spec, plan or index. A regression written to the refutation passes under both readings and will not notice a check that leaves the tree dirtier than `git status` shows; the spec states no input that separates the readings. | deepseek-v4.1-flash | in spec | — |

Stage-2 call, 2026-11-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1188 files, 5542 commits, 12 rules.

Stage-2 call, 2026-11-23: spec-review · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1188 files, 5543 commits, 12 rules.
## Phase 2a — fallback deepseek-v4.1-flash, 2026-11-23

Spec fingerprint: sha256:12bceb7b83110c25ed9350a15dd9cac85a7200616bc767fa37f02df5cb221fca

Spec review commit: 485d00ba4c49c4674c5a3368bb6025e00d4fadd4

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| T-1 | [AMBIGUITY] MAJOR | SPEC | base | spec.md AC 2, its "(provisional pending the decision below)" and `## Open decisions` [DECISION]; decisions.md R-1 | The record contradicts itself. decisions.md R-1 says the [DECISION] block is removed and AC 2 rewritten to Reading B, but the block is still printed with options A and B and an unanswered maintainer question, AC 2 still calls itself provisional pending that block, and the [DETAIL] still says the blocking scope "remains unresolved". Reading (i): B is settled, the block is dead text, the plan card and implementation proceed on B. Reading (ii): the maintainer's A/B answer is still owed, so implementation may not start, and an answer of A would make AC 2's "outside the verb's writable scope" wrong in every regression it names. Both readings pass the same refutations, one stops the change and the other builds it. | deepseek-v4.1-flash | open | — |
| T-2 | [AMBIGUITY] MAJOR | SPEC | base | spec.md AC 2 ("the verb's writable scope"), AC 1's three verbs; scripts/stage2.py:12380 `draft_keep`, 12281 implement's `allowed` | The spec never defines a verb's writable scope, and the repository's one draft rule contradicts the list the spec inherits. `draft_keep` is every changed path under `plans/changes/<change>/` except `decisions.md` plus a new ADR file, which puts `spec.md`, `plan.md`, `findings.md` and `research.md` inside it, while decisions.md R-1 puts `research.md` outside. Input: a stale `updated:` in `research.md` — under `draft_keep` the fault is inside scope, AC 2 forbids refusing and a model call runs; under the R-1 list it is outside scope and must refuse before any call. Every stated refutation uses `decisions.md`, so no regression separates the two. For implement and repair no scope exists at all: read as the writing sandbox (any tracked file) no fault is ever outside scope and AC 2 refuses nothing for two of the three verbs; read as a keep list (implement's `allowed` is `findings.md` alone) almost every blocking red refuses. | deepseek-v4.1-flash | open | — |
| T-3 | [AMBIGUITY] MAJOR | SPEC | base | spec.md AC 1, AC 2, AC 5 and `## Open decisions` [DETAIL] ("the check boundary ... remains unresolved"); scripts/stage2.py:12285-12303, 13011-13019 | The spec states the boundary as unresolved and both readings satisfy every refutation. Reading X, once per verb invocation on the tree as it stands at entry: the runner's own pre-call and pre-commit writes are outside the check, so a repair's hand-only run that writes the hand listing and exits with no model call is refused after it has already written, and implement's Flash repair and Sonnet fallback start without a new check. Reading Y, before every attempt or route: a fault the previous attempt itself introduced stops the retry, and the hand-only run that would make no call is refused before it writes anything. No criterion names an input that tells X from Y. | deepseek-v4.1-flash | open | — |
| T-4 | MAJOR | SPEC | base | spec.md AC 2 and AC 5; `## Open decisions` [DETAIL] | The state the change exists for after the first attempt is covered by no criterion. A blocking gate that is red on a fault inside the verb's scope — this change's own stale `findings.md` or `spec.md` date, an unrendered `plans/INDEX.md` that `prepare_derived` refreshes (scripts/stage2.py:7758) — is not stopped by AC 2, and AC 5 speaks only of the case where every blocking gate passes. So the spec is silent on whether that start becomes a model call with the faults shown to the operator, a call with nothing said, or a refusal. The builder has to invent one of the three, and the operator-visible difference is large for an in-scope red. | deepseek-v4.1-flash | open | — |
| T-5 | MINOR | SPEC | base | spec.md AC 4 and its refutation; scripts/stage2.py:12556; plan.md line 33 | The empty selection is left to be decided while building. AC 4 refuses when "gate selection ... cannot complete", which one reading stretches to a selector that returns no gate and the other does not, since the selection did complete and only the set is empty; the refutation names only "invalid gate selection". The existing hand-off check refuses on an empty set ("no locally runnable document gates were selected"), plan.md says "empty runnable set" refuses, and the spec says neither, so the same registry state could be built as a refusal in one verb and as a start with nothing checked in another. | deepseek-v4.1-flash | open | — |
