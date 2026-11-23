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
