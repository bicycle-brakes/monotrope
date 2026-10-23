---
title: "Spec — failed-check-spans"
status: draft
implementation_status: none
date: 2026-10-22
last_reviewed: 2026-10-22
updated: 2026-10-22
supersedes: null
superseded_by: null
bead: coding-harness-8hr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, leak-check]
class: bounded
appetite: 1
adr_files: []
---

# Spec — failed-check-spans

Failed-check diagnostics are protected on their original text: no protection
pass may destroy a match another pass needs (bead coding-harness-8hr, the
open rows F-4 and F-5 of pull request #215). Sources: `research.md` and
`decisions.md`.

## Problem

Two passes still replace the routing credential before another pass has read
the text. The format step's line is credential-scrubbed before secret spans
are collected, so a secret match overlapping the credential leaves its
suffix in `findings.md` and the retry prompt (F-4). The non-secret rules read
credential-scrubbed text, so a blocking match that extends beyond the
credential is not seen and the secret replacement then hides it (F-5).

## Terms

- **Original diagnostic:** the text as the check produced it, before any
  credential or secret replacement.
- **Span:** a (start, end) range of the original diagnostic that one rule or
  the routing credential matches.

## Acceptance criteria

1. When the format step's line contains a secret-rule match that overlaps the
   routing credential, the line written to `findings.md`, the retry prompt
   and the checkpoint record carries the rule marker over the whole match.
   *Refuted by:* any part of the matched value, such as the suffix after the
   credential, survives in the format line or in its later protection.
2. When a non-secret rule matches the original diagnostic in a span that is
   not wholly inside a routing-credential span, the runner refuses before
   publishing the diagnostics or calling another model, naming the rule and
   line, never the value.
   *Refuted by:* the match is redacted instead of refused because the
   credential was replaced first.
3. When a non-secret rule matches only within the routing credential, the
   diagnostics are published with the credential marker, as today.
   *Refuted by:* a refusal caused by the credential alone.
4. The criteria of `plans/changes/failed-check-secrets/spec.md` keep holding.
   *Refuted by:* any of its regression tests turns red.

## Non-goals

- Changing the leak check, the denylist, marker formats or the credential
  fragment rule.
- Other users of `scrub` outside the failed-check diagnostics.

## Protected areas

- `scripts/leakcheck.py`, `model-endpoints.yaml`, `prompts/`, `decisions/`,
  `docs/adr/`.

## Definition of Done

- Criteria 1–4 have the ledger's regression evidence; `make verify` is green.
- `plans/INDEX.md` regenerated; no design, ADR or workflow update.

## Open decisions

None open. Q-1 in `decisions.md` holds the maintainer's answer; the two
`[DETAIL]` records there fix the seam and the credential-only exception.
