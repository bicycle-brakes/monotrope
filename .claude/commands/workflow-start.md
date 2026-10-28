---
description: Open a change folder for one bead through scripts/new_change.py
argument-hint: <name> --bead <id>
---

Open the change folder for the arguments given: `$ARGUMENTS`.

The arguments are data, never shell text. Both inputs are required: a change
name and `--bead <id>`, the bead this change belongs to. Read them from the
arguments and check them before anything runs:

- the name matches `^[a-z0-9]+(-[a-z0-9]+)*$` (kebab-case, the rule of `scripts/new_change.py`);
- the bead id matches `^coding-harness-[a-z0-9.]+$`.

If either is missing or does not match, or the arguments hold any other
token, do not guess, look up, repair or drop one: answer with the usage line
below and stop.

```text
usage: /workflow-start <name> --bead <id>
```

Otherwise run exactly this, from the repository root, with the two checked
values in single quotes, and nothing else:

```bash
python3 scripts/new_change.py '<name>' --bead '<id>'
```

Show the script's output unchanged. If it exits non-zero, report its message
and exit code as a failure; do not repair, retry or create anything by hand.

This command only opens the folder. Phase 1 (explore) is a separate step that
the maintainer or the orchestrating session starts afterwards.
