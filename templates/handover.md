# Template — Handover

Template to copy for a file under `docs/journal/handover/`. It carries **no
frontmatter of its own**: `provenance.yaml` sets `frontmatter: none` for
`templates/`, because frontmatter in a template would be copied into every
instance and there make a provenance claim that nobody has checked. The schema
is therefore shown in code blocks.

**The valid field list lives in `scripts/handover_schema.py`**, not here and not
in the prose of the feedback loop. This file shows it, it does not define it —
`tests/test_feedback_channel.py` checks the two against each other.

## Decide first: which direction?

`direction` is a required field of **every** handover. Without it the file
falls out of every check of the channel — which is exactly what happened to 14
of 24 files on 2026-09-08.

| Value | When | What the recipient does |
|---|---|---|
| `framework->framework` | Session handover within this repo. A state as of a cut-off date, for the next session | nothing — nobody waits for an acknowledgement |
| `framework->project` | The return channel into a project instance. The framework may not write there (ADR-011/015), so it files the handover and waits | acknowledges by pull request into this repo |

When in doubt, `framework->framework`. Declaring a handover that nobody
collects to be a channel item creates an open commitment that stays open forever.

## Variant A — session handover

```yaml
title: "Session handover — <topic>, as of <YYYY-MM-DD>"
category: handover
created: 2026-01-01
updated: 2026-01-01
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-01-01"
tags: [handover, session]
# From here on optional, allowed in both directions:
# The process metrics — where a session ran phases, they belong here. They are
# the only basis on which the doctrine can correct itself; without them every
# statement about a gate's effect remains an expectation.
review_rounds: 2
fix_regen_rounds: 0
late_findings: 0
questions: "3 ([E]1 [F]1 [D]1)"   # by class: [E] decision · [F] domain gap · [D] detail
target_ref: a1b2c3d4        # the commit being reported on
bead: portfolio-agentic-engineering-<id>
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
```

Then the text. What belongs in it is told not by this template but by
experience: **what was done, what is measured, what is open, and what to do
first next time.** Numbers always with their cut-off date — a history
document ages by design (RB-P5).

## Variant B — return channel into a project instance

In addition to Variant A, and here every field is required:

```yaml
direction: framework->project
target_repo: <repo-name>
target_ref: a1b2c3d4         # short commit hash the findings were taken against
status: pending              # pending -> acknowledged -> closed
bead: portfolio-agentic-engineering-<id>
record_sha256: "sha256:<hash>"
acknowledged_by: null        # set ONLY by the project team
acknowledged_at: null        # set ONLY by the project team
closed_at: null              # set ONLY by the project team
```

`acknowledged_by`, `acknowledged_at` and `closed_at` belong to the project team.
The framework sets `pending` and never touches the other three — whoever
acknowledges their own result acknowledges nothing.

### The findings block is immutable

The part of the handover that someone relies on sits between two markers.
`record_sha256` is the SHA-256 over **exactly** the text between them — without
the markers themselves.

```markdown
<!-- record:begin -->

| # | Finding | Location | Significance |
|---|---|---|---|
| 1 | … | … | high |

<!-- record:end -->
```

Objections go **below** the block, never into it (RB-P5). A signature under a
text that changes afterwards is none.

Generating the hash:

```bash
python3 - <<'PY'
import hashlib, pathlib, sys
t = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs/journal/handover/<file>.md").read_text(encoding="utf-8")
block = t.split("<!-- record:begin -->\n", 1)[1].split("<!-- record:end -->", 1)[0]
print("sha256:" + hashlib.sha256(block.encode()).hexdigest())
PY
```

### And then into the index

A handover with `direction: framework->project` **must** be listed in the table
in `docs/journal/_INDEX.md` for as long as its status is not `closed`. A handover
that the index does not know is collected by nobody — it is then not a handover
but a file that somebody wrote.

## Check before it becomes a pull request

```bash
python3 -m pytest tests/test_feedback_channel.py -q
```
