---
title: "Decisions — stage2-mimo"
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
tags: [decisions]
---

# stage2-mimo — Decisions

Phase 1a (interview) records the maintainer's request of 2026-10-06. No
formal interview is called; the task is clear in scope (add MiMo-V2.6 as a
reviewer in phase 4b) and in class (a `feature` — a new endpoint, new runner
logic, and an amendment to ADR 0007).

## What the maintainer decided on 2026-10-06

Maintainer (in a Claude Code session, bead coding-harness-ymx): "Plane das
als Stufe 2 reviewer ein — als zusätzlicher Prüfer in der Review-Schleife
(4b)." — Plan MiMo-V2.6 as a Stage 2 reviewer, as an additional reviewer in
the review loop (phase 4b).

The maintainer did not specify:
- Which endpoint to use (Xiaomi's own API, OpenRouter, or Z.ai's expansion).
- Whether MiMo runs in the same round as GLM, or in round 2 after GLM, or in
  a separate optional round.
- Whether the model family has a `pro` (reasoning) and `flash` (fast)
  variant, and which to choose for reviews.
- Whether the change also covers Codex replacement or phase 1/4 expansion (per
  ADR 0007 §5, those are open items of the stage-2-codex-glm change; the
  maintainer widened that scope on 2026-10-06, but may limit this change to 4b
  only).

## [DECISION] 1 — the class of this change (not answered yet)

The spec author must state the class. Two readings are plausible:

```text
Goal in one sentence:  Should MiMo be added to the review loop phase 4b only,
                       or to the entire stage-2 framework (review loop, spec
                       review, phase-6 review, and possibly explore/implement)?
Options:
  1. bounded.          It adds MiMo to phase 4b only, as an additional
                       reviewer running after or alongside GLM. The runner,
                       the endpoint declaration and the evidence rule change
                       for one phase. Spec review (2a) and review (6) stay
                       Codex and GLM; phases 1 and 4 stay Haiku/Sonnet (or
                       Flash when that runner verb is built). Consequence: no
                       ADR question; smaller scope; one revert removes phase-4b
                       MiMo calls only.
  2. feature.          It is a framework expansion: MiMo is added as a
                       reviewer option throughout stage 2, complementing Codex
                       (which reviews specs and code) and GLM (which reviews in
                       loops). Where each reviews depends on change class and
                       on the maintainer's stated preferences. Consequence:
                       ADR 0007 is substantially amended, not patched; the
                       architecture documents shift; every change routing may
                       change. Higher risk; more reversible by an architecture
                       decision than by a code revert.
Recommendation:        Option 1 — phase 4b only. Rationale: (a) the
                       maintainer said "in der Review-Schleife (4b)"
                       explicitly; (b) the spec-review and review phases are
                       already covered by Codex; (c) Codex and GLM track
                       well; MiMo adds a third opinion, not a replacement;
                       (d) the decision scope stays narrow; (e) if MiMo
                       findings are poor (e.g., many false positives), the
                       feature is easily disabled by the spec author,
                       requiring no ADR amendment. If findings are good and
                       want expansion, an ADR amendment comes later.
If you say "ok":       `class: feature` in spec.md; the spec header gains
                       `change: adr-0007-amendment`; an ADR 0007 amendment
                       proposal is written as part of the spec; the gate
                       `adr-answers` keeps `make verify` red until the
                       maintainer answers in the chat.
What is lost:         If this is option 1 (phase 4b only), the change is
                       reversible with one git revert and no ADR write-up. If
                       the maintainer later wants MiMo in spec review or phase
                       6, a separate `feature` change adds it.
```

The recommendation is Option 1: class `feature`, but scoped to phase 4b only.
(Note: "feature" is the class; "phase 4b only" is the implementation scope.)

## [DECISION] 2 — the endpoint: Xiaomi API, OpenRouter, or Z.ai?

Three vendors could serve MiMo-V2.6:

1. **Xiaomi's official API** — if it exists and is accessible to external
   developers. Unknown: whether it is Anthropic-compatible (like GLM),
   OpenAI-compatible (like Codex), or a third API shape. Auth: unknown.
   Residency: unknown. Data policy: unknown.

2. **OpenRouter** (openrouter.ai) — an aggregator serving hundreds of models.
   If MiMo is listed there, it is likely OpenAI-compatible; OpenRouter's data
   policy is known. Cost is typically higher than direct access. One credential
   (API key) handles all OpenRouter models.

3. **Z.ai** (the current GLM host, `https://api.z.ai/api/anthropic`) — if it
   has expanded to host MiMo alongside GLM. Anthropic-compatible. Uses the
   same subscription and auth as GLM. No new credential to manage.

**Recommendation:** Check Z.ai first; if MiMo is listed there, use that
endpoint (reduces credential management to one file, auth method is known,
residency is China like GLM). If not, OpenRouter is next (aggregator,
OpenAI-compatible likely, documented data policy). Xiaomi's own API is a
fallback only if it is shown to be OpenAI-compatible or the maintainer wants
to manage a third endpoint.

Consequence: endpoint declaration, runner's environment variables, and the
launch logic differ by vendor. The spec will propose one; the maintainer will
decide.

## [DECISION] 3 — scheduling: same round as GLM, or round 2?

If both GLM and MiMo run in phase 4b, they can run in parallel (same round,
same diff) or sequentially (GLM round 1, MiMo round 2, both on merged-base
diff).

1. **Parallel (same round).** Both see the same code. Two reviewers, two
   verdict columns. Rows marked open for the implementer to decide. Cost: 2×
   review cost per round; `MAX_ROUNDS = 2` means up to 4 rows per round, all
   from two reviewers. Wall-clock: fast (both calls in parallel). Implementer
   sees all findings at once.

2. **Sequential (GLM round 1, MiMo round 2).** GLM runs first on merged-base
   diff; implementer decides GLM rows (taken/rejected); then MiMo runs on the
   same merged-base diff (original code, not repaired). Two separate
   `review-loop` calls. Rows marked open for the implementer. Cost: 2× review
   cost per round, but less wall-clock; implementer can fix GLM findings
   before MiMo runs. Wall-clock: slower (serial); implementer sees GLM verdict
   first, may reduce MiMo findings if the fixes address the root cause.

**Recommendation:** Sequential (option 2). Rationale: (a) compatible with
current runner structure (one `review-loop` call per reviewer); (b) lower
wall-clock time is less important than seeing one reviewer's verdict before
the next; (c) cost per round is the same, but implementer can act on GLM
findings before MiMo sees the code, which may improve both sets of findings;
(d) the current `MAX_ROUNDS = 2` is clear per reviewer; if both run, two
rounds each is four total, which is acceptable given the two-reviewer constraint
(ADR 0007 §1 names a fallback rule on the third run).

Consequence: the runner gains a new verb (`review-loop-mimo`) or a scheduler
that calls both in order. The spec will propose the verb structure; the
maintainer will decide.

## No [DETAIL] is open yet

All details (model name, API shape, auth method, data residency) depend on
reading the endpoint's documentation, which is blocked on [DECISION] 2. Once
the endpoint is chosen, those details are looked up and recorded in the spec.

