#!/usr/bin/env python3
"""Launch an unattended Antigravity run: the child is marked so the agent-policy hook denies every ask.

    python3 tools/antigravity/night.py <the arguments a normal `agy` call would take>

The repository's agent-policy hook for Antigravity (`scripts/agent_policy_hooks.py
antigravity`, registered in `.agents/hooks.json`) turns an ask into a deny when
`HARNESS_UNATTENDED` is set, nonempty and not `0`. This launcher is the named
owner of that signal for an Antigravity run (plans/changes/agent-policy-list):
it starts `agy` with the remaining arguments as an argv list and its own
environment plus `HARNESS_UNATTENDED=1`, waits for it and forwards its exit
status.

What it does not establish: whether Antigravity hands this environment on to
the hook process, and whether an `agy` started here runs in a fresh process
rather than handing the work to one already running. The one-time host check
the policy documentation records answers both; without it Antigravity is not
declared supported for unattended runs.
"""

from __future__ import annotations

import os
import subprocess
import sys

AGY = "agy"

# The signal the agent-policy hook reads: an unattended run, where every ask is a deny.
UNATTENDED = {"HARNESS_UNATTENDED": "1"}


def child_environment(base: dict[str, str] | None = None) -> dict[str, str]:
    """The child's environment: the launcher's own, marked unattended."""
    return {**(dict(os.environ) if base is None else base), **UNATTENDED}


def main(argv: list[str] | None = None) -> int:
    """Run `agy` marked unattended; the child's exit status, or 127 when it cannot be started."""
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        done = subprocess.run([AGY, *argv], env=child_environment())
    except FileNotFoundError:
        print(f"antigravity night.py: '{AGY}' was not found on the PATH", file=sys.stderr)
        return 127
    except OSError as exc:
        print(f"antigravity night.py: cannot launch '{AGY}': {exc}", file=sys.stderr)
        return 127
    return done.returncode if done.returncode >= 0 else 128 - done.returncode


if __name__ == "__main__":
    sys.exit(main())
