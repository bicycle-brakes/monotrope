---
title: "Findings — reproducible bead export"
category: findings
created: 2026-09-21
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-21"
review:
  status: pending
  approved_by: null
  approved_at: null
status: accepted
implementation_status: done
date: 2026-09-21
last_reviewed: 2026-09-21
bead: coding-harness-1jg.1
---

# Findings — reproducible bead export

Phase 6, round 1, on commit `c65a548`. The reviewer ran in a fresh context
and did not write to the checkout. Verdict: no open BLOCKER, no
`[AMBIGUITY]`, no `[DIVERGENT]`.

| ID | Severity | Dimension | Origin | Where | Finding | Disposition |
|---|---|---|---|---|---|---|
| F-1 | MINOR | MAINT | base | `scripts/render_beads_export.py`, `_ohne_maschinenlokales` | `str.splitlines()` also cuts at U+0085 and U+2028, which the tracker writes raw inside a text; one record became two broken lines, the write was refused and `--check` reported DRIFT for identical content. Failed closed, but broke criterion 2. Reproduced with a stand-in `bd`. | Fixed in round `fix-r1`: records are split on `\n` only; held by `test_a_record_with_a_raw_line_separator_stays_one_line`. |
| F-2 | MINOR | SPEC | base | `tests/test_gate_machinery.py`, `test_the_omitted_keys_are_named_once` | The test could not bite on its own refutation case: it scanned `scripts/*.py` only and required both keys in double quotes, so a single-quoted list or a list in `decisions/` escaped. | Fixed in round `fix-r1`: the bare key names are searched in `scripts/` and `decisions/`; `tests/` stays out because the keys appear there as fixture data, and the test asserts that its search sees the renderer. |

## Checked without a finding

The committed export differs from `origin/main` only by this session's new
beads and by the two omitted keys on the ADR bead; the tracker's JSON spelling
is reproduced byte for byte on all 33 real lines; the write path and `--check`
share the omission; the line check still runs after it. A wrongful refusal by
the self-check needs a lease-carrying line that also holds a float, an escaped
replacement character, a pre-1.22 Go control escape or a duplicate key — none
occur today, and the failure is loud and leaves the committed file untouched.

## Not checked

Go's encoder was not run (claims about it come from the 33 real lines and
from memory); no second physical machine rendered; Windows newline
translation.
