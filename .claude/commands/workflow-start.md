---
description: Open a change folder for one bead through scripts/new_change.py
argument-hint: <name> --bead <id>
---

Open the change folder for the arguments given: `$ARGUMENTS`.

Both inputs are required: a change name (kebab-case) and `--bead <id>`, the
bead this change belongs to. If either is missing, do not guess one and do not
look one up: answer with the usage line below and stop.

```text
usage: /workflow-start <name> --bead <id>
```

Otherwise run exactly this, from the repository root, and nothing else:

```bash
python3 scripts/new_change.py $ARGUMENTS
```

Show the script's output unchanged. If it exits non-zero, report its message
and exit code as a failure; do not repair, retry or create anything by hand.

This command only opens the folder. Phase 1 (explore) is a separate step that
the maintainer or the orchestrating session starts afterwards.
