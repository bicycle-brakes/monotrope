---
title: "Research — stage2-mimo"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: null
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-ymx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, mimo]
---

# Research — stage2-mimo

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). Facts only, read on 2026-10-07 in the worktree at the current head of `feat/stage2-mimo` (branched from `feat/stage-2-codex-glm`, 83c545a). Every statement names its source; what was not read says so.

The task (maintainer, 2026-10-06): "Plane das als Stufe 2 reviewer ein — als zusätzlicher Prüfer in der Review-Schleife (4b)" — plan MiMo-V2.6 as a Stage 2 reviewer, as an additional reviewer in the review loop (phase 4b).

## 0 · Existing artefacts on the topic

`rg -i "mimo|xiaomi|stage.?2|review.?loop"` over `plans/specs/` and `plans/changes/` (2026-10-07) finds `plans/changes/stage-2-codex-glm/` (current and related), but no artefact on MiMo specifically. Nothing to update instead of create.

## 1 · What exists today

### 1.1 Stage 2 as of 2026-10-07

ADR 0007 (`docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`, merged) sets the current stage-2 routing:

- **Codex** (`openai-codex`, model `gpt-6.1-sol`, official Codex CLI): spec review (phase 2a) and code review (phase 6) for all change classes. Declared for framework content only; runs through an ask rule; read-only request (not confined); personal ChatGPT subscription (2026-09-30).

- **GLM** (`glm-coding-plan`, model `glm-5.3` for review loop / `glm-5.3-flash` for phases 1 and 4, Z.ai's Anthropic-compatible endpoint at `https://api.z.ai/api/anthropic`): review loop (phase 4b) for all changes; started by `python3 scripts/stage2.py review-loop <change>`; for framework content only; through Claude Code only; reads broadly, writes code.

- **Leak check** (`scripts/leakcheck.py`): required before every call, enforced by `scripts/stage2.py` at lines 437–440. Checks three rules: framework content only, no customer schema or figures, no secrets planted in fixtures.

- **Max rounds**: 2 (line 117 of `scripts/stage2.py`).

- **Evidence rule** (`prompts/04b-review-loop.md`, §For the implementer): a GLM or Codex finding is taken only when a test demonstrates it or the spec supports it; otherwise it is rejected with reason and stays in findings.md as a disagreement.

- **Disagreement recording** (`docs/WORKFLOW.md` §2.3): disagreements are recorded, not resolved. One reviewer flags something and another does not — that is the information.

### 1.2 The call path (phase 4b)

`scripts/stage2.py review-loop` (lines 789–852) prepares and runs a GLM call:

1. Preflight: change exists, spec.md has a `bead`, endpoint `glm-coding-plan` is declared for framework with residency (line 791–801).
2. Leak check (line 809): `scripts/leakcheck.py` runs; exits 2 if not clean.
3. Diff build (line 804): `change_diff()` constructs the merge-base diff against `origin/main`, uncommitted and untracked files included.
4. Prompt build (lines 806–808): prompt is `04b-review-loop.md` body, answer format, read request, the diff again, read request again.
5. Claude Code call (lines 815–835): `claude` command with `--model glm-5.3`, `--effort max`, `-p` and `--append-system-prompt-file` for the prompt, `--tools Read,Grep,Glob`, restricted sandbox, no session persistence, permission mode `dontAsk`. Environment: `ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic`, `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` from `~/.config/cc-routing/secrets.env`, GLM model name set in all model variables.
6. Rows written to loop record (lines 843–851): outside the repository at `~/.local/state/coding-harness/stage2/<change>/loop.md`, numbered `L<round>-<k>`, GLM marked as reviewer, status and test mark left empty for the implementer.
7. `findings.md` entry (line 445–447): date, verb, endpoint, model, leak check stats.

### 1.3 How a MiMo call would fit

The task says "zusätzlicher Prüfer" — an additional reviewer. The current architecture (ADR 0007, section 4, phase 4b):

> "Disagreements are recorded, not resolved. That one reviewer flags something and another does not *is* the information."

So MiMo could be a second or third foreign reviewer in the loop, alongside or after GLM. The `findings.md` already distinguishes reviewers by name (`Reviewer` column in tables, line 118).

What the task asks for is not yet in ADR 0007: the amendment (section 4) covers Codex and GLM only. Where MiMo would sit — after GLM, both on the same diff, a fallback condition, or a separate optional path — is open and marked in the current ADR as a detail for the maintainer to decide.

## 2 · MiMo-V2.6 hosting and access

### 2.1 Xiaomi's MiMo models — not read

Xiaomi's official model page and API documentation: not read from the web (2026-10-07). The model's public announcement, supported vendors, residency, auth method and API shape are unknown.

[GAP: Is MiMo-V2.6 (or MiMo-V2.*) a product Xiaomi offers to external developers, and if so, through which endpoints? Is there an official Xiaomi API, and is it Anthropic- or OpenAI-compatible?]

### 2.2 Aggregators — OpenRouter status

**OpenRouter** (openrouter.ai): [not read from web, 2026-10-07] Whether OpenRouter currently lists any MiMo model and which regions it serves are unknown.

[GAP: Does OpenRouter host MiMo-V2.6 or any MiMo model, and if so, is it OpenAI-compatible? Which data policy does OpenRouter apply to MiMo calls?]

### 2.3 Z.ai (the current GLM host) — not read

Whether Z.ai hosts MiMo-V2.6 or any Xiaomi model is unknown (2026-10-07).

[GAP: Does Z.ai offer MiMo models alongside GLM, and if so, under what terms?]

### 2.4 Data retention and training — vendor claims not verified

Xiaomi's terms for data use, retention and training use on any of its models are unknown (2026-10-07).

[GAP: What is Xiaomi's stated data policy for personal-use API access? Is there an opt-out for training use?]

## 3 · How MiMo would integrate

### 3.1 model-endpoints.yaml

To run a MiMo call, a new endpoint must be declared (or MiMo added to an existing endpoint). The declaration would follow lines 293–335 for GLM and 347–358 for Codex:

```yaml
- name: mimo-endpoint-name  # TBD: Xiaomi's official API, OpenRouter, or Z.ai?
  betreiber: Xiaomi  # or "aggregator (OpenRouter)" etc.
  residenz: [TBD: where data stays]
  abrechnung: token  # or abonnement
  darf_sehen: [framework]
  modelle:
    - mimo-v2.6
    # or mimo-v2-*, depending on the model family
  bemerkung: >-
    [TBD: access method, data terms, auth]
```

### 3.2 scripts/stage2.py changes

Lines 75–78 define the endpoints and models for Codex and GLM:

```python
CODEX = ("openai-codex", "gpt-6.1-sol", "max")
GLM = ("glm-coding-plan", "glm-5.3", "max")
GLM_BASE_URL = "https://api.z.ai/api/anthropic"
```

A MiMo endpoint would need similar constants (or a third verb). If MiMo is OpenAI-compatible, it could reuse the `foreign_env()` pattern; if it is something else, new launch logic is needed.

Where MiMo runs (after GLM in round 2, both in round 1, a separate optional round) would shape how the runner schedules it. Currently, `MAX_ROUNDS = 2` (line 117) counts GLM rounds; if MiMo runs after GLM's verdict, that limit may change.

### 3.3 Verb: `review-loop-mimo` or `review-loop-all`?

The maintainer's request says "zusätzlicher Prüfer" (additional reviewer), which suggests MiMo runs in the same loop as GLM, not instead of it. The runner would then have two options:

- **`review-loop` stays GLM-only, and a new verb `review-loop-mimo` runs MiMo.** Implementer decides the order; could run `review-loop` then `review-loop-mimo` in sequence.
- **`review-loop-all` runs both GLM and MiMo in one call** (the maintainer decides the order). Simpler for the implementer; less flexible.

Current `review-loop` (lines 789–852) would need adaptation either way.

## 4 · Pro vs Flash for review

### 4.1 GLM in phase 4b: 5.3 (current) or 5.3-flash?

ADR 0007 section 5 notes that exploration and implementation on GLM 5.3 Flash are decided but not built. The review loop (phase 4b) uses `glm-5.3` at effort `max` (lines 76–77, line 824). Why the distinction is not explained in the current tree.

[DETAIL: Whether MiMo's model family has a "pro" (reasoning) and "flash" (fast) variant, and whether the review loop should choose speed or reasoning capability for finding defects, depends on Xiaomi's model line-up and the maintainer's risk tolerance. A faster model means lower cost per round; a reasoning model means potentially deeper findings. The current GLM choice (not Flash) suggests reasoning is preferred for reviews.]

### 4.2 Cost estimate — not measured

No benchmark data for cost or latency of MiMo-V2.6 (or any MiMo model) in a review context is known (2026-10-07). GLM 5.3 at effort `max` on a typical diff size in this repository is not measured either.

[GAP: What is the estimated cost per review round (input + output tokens × rate) for MiMo-V2.6 versus GLM 5.3, at typical diff sizes in this repository?]

## 5 · Where MiMo sits in phase 4b

### 5.1 Same round, both GLM and MiMo?

If both reviewers run on the same diff in round 1, the implementer gets two columns of findings, both marked as "open" until decided. The loop record would have two sets of rows, distinguished by reviewer. The evidence rule still applies: a finding is taken only when a test demonstrates it or the spec supports it.

**Consequence:** one round, two verdict columns, double the findings to filter. Cost is 2× the review cost per round. With `MAX_ROUNDS = 2`, up to 4 total rounds is possible if one reviewer needs repair feedback.

### 5.2 Sequential: GLM then MiMo?

Round 1 GLM, round 2 MiMo, both on the same merged-base diff. If GLM finds something, the implementer decides whether to fix it before MiMo sees the same code (or the original code). This keeps the current verb structure (one `review-loop` call = one reviewer).

**Consequence:** up to 2 rounds each, 4 rounds total; serial, so longer wall-clock time; implementer can fix GLM findings before MiMo sees them, which may reduce MiMo findings.

### 5.3 After phase-6 verdict

Both GLM and MiMo as pre-phase-6 reviewers, but a third optional round if needed. Lines 529–572 of `scripts/stage2.py` release the loop rows into findings.md after Codex's phase-6 verdict; the phase-6 reviewer (Codex) reads the loop findings and marks them agree/disagree.

If MiMo runs before phase 6, its rows are part of the loop; if it runs after the loop but before phase 6, it would need new machinery.

**[DECISION] In phase 4b, where should MiMo run relative to GLM?**

Recommendation: **GLM round 1, MiMo round 2, both on the same merged-base diff**, keeping the serial structure (one `review-loop` call per reviewer). This limits `MAX_ROUNDS` to 2 rounds per reviewer, 4 total. Rationale: (a) lower total cost than running both in parallel; (b) implementer can see GLM's verdict first, fixing obvious issues before MiMo sees the code; (c) disagree/agree marks from both reviewers in one findings.md table.

Consequence: the current `MAX_ROUNDS = 2` may need to clarify that it is per reviewer, or the limit changes to 2 total (one per reviewer). The maintainer will decide after seeing the first live runs.

## 6 · What ADR 0007 must gain

ADR 0007 section 4 (page 9) covers Codex and GLM only. The amendment needed:

> "**Where framework content may flow.** This repository's tree — the class `framework` of `model-endpoints.yaml`: rules, templates, process, tests — may go to `openai-codex` through the official Codex CLI, and to `glm-coding-plan` through Claude Code: ... Nothing else goes, and nowhere else."

Must be widened to include MiMo if it is added as a stage-2 reviewer. The new text would be:

> "... and to `glm-coding-plan` through Claude Code, and to `[mimo-endpoint-name]` [through OpenRouter|through Xiaomi's API|...]: the reviews to Codex, GLM and MiMo, ... Nothing else goes, and nowhere else."

The endpoint declaration, residency, data policy and auth method must be added before the amendment is complete (open questions in section 2 above).

The current decision continuity map (`docs/architecture/` and `scripts/check_decision_continuity.py`, line 56) maps D-13 to ADR 0007; if ADR 0007 is amended, the D-13 row in the target document must be updated to name the addition.

## 7 · Open questions, tagged

**[DECISION]** Whether a new endpoint or an aggregator is preferred, and which vendor Xiaomi should flow through (Xiaomi's own API, OpenRouter, Z.ai). Consequence: the endpoint declaration and the runner's environment setup differ.

**Recommendation:** Check whether Z.ai (the current GLM vendor) offers MiMo-V2.6, and if so, use that endpoint to reduce credential management (one secrets file, one Anthropic-compatible base URL). If not, OpenRouter is the next choice for compatibility. Xiaomi's own API is a fallback only if it is OpenAI-compatible; otherwise, new runner logic is needed.

**[DECISION]** Whether both GLM and MiMo run in round 1 (parallel, same diff), or GLM round 1 and MiMo round 2 (sequential, both on merged-base diff), or another order. Consequence: cost, wall-clock time, implementer decision flow, and whether `MAX_ROUNDS` is per-reviewer or total.

**Recommendation:** Sequential (GLM round 1, MiMo round 2) as described in section 5.2. Rationale: compatible with current runner structure; lower cost; implementer sees GLM verdict first.

**[DETAIL]** The exact model name if Xiaomi has a model family (e.g., `mimo-v2.6` or `mimo-v2` or `mimoR7`). Decided by vendor's official listing once the endpoint is chosen.

**[DETAIL]** Whether MiMo-V2.6's API is Anthropic-compatible (like GLM), OpenAI-compatible (like Codex), or something else. Impacts the runner's environment setup and the launch logic. Decided by reading the endpoint's API docs once the endpoint is chosen.

**[DETAIL]** The auth method (API key, OAuth, subscription token). Decided by the endpoint's documentation and the secrets file format.

## 8 · Files a change would touch

- `model-endpoints.yaml`: add MiMo endpoint declaration
- `scripts/stage2.py`: add MiMo endpoint constants, GLM/MiMo scheduling logic, possibly a new verb or conditional in `review-loop`
- `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`: amend section 4 ("Where framework content may flow") to include MiMo
- `docs/architecture/target-architecture.md` or its successor: update the D-13 row to reflect the MiMo addition
- `tests/test_stage2.py`: test the new endpoint declaration and the MiMo scheduling
- `tests/test_leakcheck.py`: if MiMo is a new data class, verify leakcheck still holds
- Possible: `prompts/04b-review-loop.md`, if a separate prompt for MiMo is needed (unlikely; the answer format and evidence rule are universal)
- Possible: `~/.config/cc-routing/secrets.env` (user setup, not in the repository): add `MIMO_KEY` or equivalent

## 9 · Next steps

1. Read Xiaomi's documentation on MiMo-V2.6: model card, API shape (Anthropic or OpenAI compatible), access methods, data residency, data use terms, pricing.
2. Check Z.ai's current model roster: does it list MiMo, and if so, what terms?
3. Check OpenRouter's current model roster and pricing for MiMo, and compare with direct access.
4. (Blocked on [DECISION]s above) Measure cost and latency of a typical phase-4b call with the chosen endpoint.
5. Propose the endpoint declaration and runner changes (phase 2, Spec).

