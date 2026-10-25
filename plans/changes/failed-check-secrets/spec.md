---
title: "Spec — failed-check-secrets"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-8hr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, leak-check]
class: bounded
appetite: 2
adr_files: []
---

# Spec — failed-check-secrets

Failed-check diagnostics may carry synthetic test secrets without poisoning
the runner's next attempt, while the leak check retains its blocking force
(bead coding-harness-8hr). Sources: `research.md` and `decisions.md`.

## Problem

The exploration, seeded against `6029bbf` and checked during drafting at
`2cc2c81` on 2026-10-16, identifies two copies of failure evidence: a quoted
block in `findings.md` and an accumulated string in the retry prompt.
`verify_evidence` scrubs the routing credential alone; other secret-rule
matches survive both copies. The leak check exempts test files from secret
rules, but neither diagnostics copy is a test file, so an otherwise legal
fixture can stop the next model call.

The research seed reports this sequence after a disk-full failure during the
pi-pin draft. Its exact traceback was not found in the committed incident
record; that report is motivation, not measured reproduction. The observable
raw-string path is the basis for the regression test.

## Terms

- **Secret rule:** an active denylist rule whose name starts with `secret:`.
- **Failed-check diagnostics:** the runner's evidence for failed post-run
  checks in `draft`, `implement` and `repair`, including verification output,
  preparation failures and other postcondition messages.
- **Rule marker:** `[secret:<rule name>]`, with the matched rule's name and
  no matched value; the routing credential retains its `[credential]` marker.

## Acceptance criteria

1. When failed-check diagnostics are written to `findings.md` or included in
   a retry prompt, secret-rule matches are redacted using the active leak
   check's rule set on every draft, implement and repair route.
   *Refuted by:* either destination retains a matched value, including on a
   Codex or Stage-1 route where no routing credential was read.
2. When a secret-rule match is redacted, its rule marker replaces the matched
   span in place while unmatched diagnostic text and traceback line breaks
   remain intact within the existing output bounds.
   *Refuted by:* a value survives an overlapping or multiline match, a marker
   loses its rule name, or an unrelated exception/location line disappears.
3. When a first attempt fails verification with a synthetic fixture secret
   in its traceback and the next attempt fixes the failure, the next attempt
   passes its real pre-call leak check and the run completes successfully.
   *Refuted by:* the retry is refused because of either diagnostics copy, or
   the test succeeds only by bypassing the leak check.
4. If the active denylist is missing, unreadable, invalid or empty when
   diagnostics need redaction, the runner refuses before publishing those
   diagnostics or calling another model.
   *Refuted by:* raw evidence is appended or sent, another attempt starts, or
   an unchecked rule set is treated as clean; the refusal itself leaks text.
5. If a non-secret rule matches failed-check diagnostics, that match still
   prevents another model call even when a secret rule overlaps its span.
   *Refuted by:* secret redaction hides the non-secret match and the retry or
   a fallback model is called.
6. While diagnostics are redacted, a secret-rule violation in a non-exempt
   repository file or reachable history still blocks the next model call.
   *Refuted by:* the runner cleans source/history or skips a pre-call scan to
   make the retry pass.
7. When diagnostics also contain the known routing credential or its already
   protected fragments, the existing credential protection still applies.
   *Refuted by:* a protected fragment reaches the findings block or retry
   prompt, or a route that did not need the routing key starts reading it.

## Non-goals

- Weakening the leak check, broadening the test exemption, redacting customer
  rules, or deciding whether a diagnostic value is synthetic or real: every
  secret-rule match in this diagnostic channel is treated alike.
- Cleaning earlier findings, source files, history, model answers or provider
  failure output; changing the review loop or session handover machinery.
- Changing attempt limits, routing, quoting, evidence budgets or audit formats.
- Design phase 2b and an ADR: this is a bounded repair within the existing
  runner boundary, not an architecture change.

## Protected areas

- `scripts/leakcheck.py` and `tests/test_leakcheck.py`: reuse the existing
  rule reader and scanner contract without changing their semantics.
- `model-endpoints.yaml`, `prompts/`, `decisions/`, `docs/adr/` and
  `provenance.yaml`: this change needs no routing or governance decision.
- The real denylist and secrets files: read through existing APIs only;
  tests use isolated synthetic rules and never require real credentials.

## Definition of Done

- Criteria 1–7 have the ledger's regression evidence; `make verify` is green.
- Documents changed with the code: this change's `plan.md` ledger and measured
  time; `plans/INDEX.md` is regenerated. No design, ADR or workflow update.
- The pull request's file list shows protected areas untouched and non-goals
  unbuilt; tests use stand-ins, with no live model call.
- The pull request closes the diagnostic-redaction work item and its final
  commit carries `Closes-Bead: coding-harness-8hr`.
- Special runs: none beyond the commands in `plan.md`.

## Open decisions

None open. The five `[DETAIL]` records in `decisions.md` govern secret-only
redaction, markers, the two destinations, refusal and the regression shape.
I chose the following reversible details and recorded their reasons:

- `[DETAIL]` The phase-4 appetite is two hours, repairs included, as a stop:
  one shared diagnostic path and the existing stand-ins bound the work.
- `[DETAIL]` Overlapping matches are handled from the original text, and
  non-secret matches are checked before replacement: otherwise redaction
  could accidentally weaken a blocking rule.
- `[DETAIL]` Markers retain the full rule name; multiline replacements keep
  line breaks so the traceback's location remains useful for repair.
