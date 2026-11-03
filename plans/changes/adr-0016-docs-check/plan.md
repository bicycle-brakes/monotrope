---
title: "Plan — adr-0016-docs-check"
status: draft
implementation_status: done
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-v9xx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, adr]
---

# Plan — adr-0016-docs-check

```text
For you:     ADR 0016 names the document check the draft runner really runs.
Done when:   Decisions 2, 3 and 7 name it, the dated note stands, and the document check is green.
Appetite:    1 hour, text only; stop at the limit.
Not now:     Any code, gate or WORKFLOW change.
Pre-mortem:  suppose it failed: most likely because a fourth place in the ADR still names make verify for the draft.
Starts unless you say stop.
```

## Files and steps

1. `docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md`: replace the
   three draft mentions of `make verify` and add the dated note.
2. This folder: research, decisions, spec and plan; `plans/INDEX.md` is
   regenerated.

## Verification

```sh
bash scripts/verify_all.sh --job docs
```

## Criterion ledger

- 1: not a test — the ADR text, read by the maintainer in the decision pull request
- 2: not a test — the ADR text, read by the maintainer in the decision pull request

## Time used

2026-11-03 06:50–07:10 UTC — orchestrator, by hand, text only
