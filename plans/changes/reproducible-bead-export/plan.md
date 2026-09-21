---
title: "Plan — reproducible bead export"
category: plan
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
status: draft
implementation_status: none
date: 2026-09-21
last_reviewed: 2026-09-21
bead: coding-harness-1jg.1
---

# Plan — reproducible bead export

## Files

- `scripts/render_beads_export.py` — changed. One constant `MASCHINENLOKAL`
  names the omitted keys with the reason (criterion 4). `_render_nach` passes
  the raw export through `_ohne_maschinenlokales` before anything else sees
  it, so the write path and `--check` share the omission (criterion 3). A line
  without such a key is passed through untouched. A line with one is parsed,
  the keys are removed and the line is serialised the way the tracker writes
  JSON (compact separators, `<`, `>`, `&`, U+2028 and U+2029 escaped); before
  that serialiser is trusted it must reproduce the unmodified input line byte
  for byte, otherwise the render is refused with exit 1 (criterion 2). The
  existing line check stays where it is (criterion 5).
- `tests/test_gate_machinery.py` — changed. Six tests, below.
- `.beads/issues.jsonl` — re-rendered once by the script.

## Verification command

```
bash scripts/verify_all.sh
```

## Test per criterion

| Criterion | Test | Fault that turns it red |
|---|---|---|
| 1 | `test_the_render_omits_machine_local_lease_fields` | a lease key survives `_ohne_maschinenlokales` |
| 1, 3 | `test_the_omission_is_wired_into_the_one_render_path` | the omission is removed from `_render_nach` (proved by mutation on 2026-09-21: 1 failed) |
| 2 | `test_the_render_leaves_every_other_byte_alone` | lines without a lease key are re-serialised, or escaping differs |
| 2 | `test_the_render_refuses_a_line_it_cannot_reproduce` | the self-check is removed and a foreign serialisation is rewritten |
| 2 | `test_a_record_with_a_raw_line_separator_stays_one_line` | records are split with `str.splitlines()` again (review F-1) |
| 4 | `test_the_omitted_keys_are_named_once` | a test or gate carries its own list instead of reading the constant |

Criterion 5 is held by the existing
`test_export_identity_gate_*` tests and the unchanged call of
`check_bead_export.run`.

## Not touched

`tools/bd`, `.beads/config.yaml`, `decisions/gates.yaml` (stage 2),
`scripts/check_bead_export.py`, `scripts/new_change.py`.
