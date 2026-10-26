"""Mutation evidence for the gate ratchet (RB-G4): which script a gate runs, and
which test files hold a mutation-named test for it.

Moved unchanged out of `tests/test_ci.py` (bead coding-harness-diic), so that a
repair of the analyzer can be shown red first: a test in `tests/` now runs
against the analyzer in `scripts/`, not against a copy in its own file.
"""

from __future__ import annotations

import re
from pathlib import Path

# These name forms count as mutation evidence. The list is deliberately bound to
# names and not to comments: a name is carried along when something is renamed,
# a comment is not.
MUTATIONS_NAMEN = re.compile(
    r"^def (test_\w*(?:goes_red|red_on|detects_tampering|refuses|is_caught|catches|"
    r"not_a_write|is_an_error|is_exit_2|never_writes|is_not_a_pass|notices)\w*)\(",
    re.M,
)


def pruefling(gate: dict) -> str:
    """The subject of this gate — the script it runs."""
    befehl = gate.get("command") or ""
    # The subfolder has to be included: until 2026-09-08 the pattern ended before
    # the second `/`, and a script under `scripts/kit/` was invisible to the
    # ratchet — it reported "no script recognisable" and demanded an exception
    # for a gate that had long had its mutation evidence.
    m = re.search(r"(?:scripts|docs/patterns)/(?:[A-Za-z_]+/)*([A-Za-z_]+\.py)", befehl)
    if m:
        return m.group(1)
    # A gate can also run a test file itself — `ruleset-drift` checks a statement
    # about the repo configuration for which there is no script and there should
    # be none: a tool that can change rulesets would be a greater risk than the
    # finding it makes. Its mutation evidence then lies in exactly that file, and
    # that is where the ratchet looks for it too.
    m = re.search(r"(tests/[A-Za-z_]+\.py)", befehl)
    return m.group(1) if m else ""


def belegt(ziel: str, quellen: dict[Path, str], root: Path) -> bool:
    """Whether the gate subject `ziel` has mutation evidence in `quellen`."""
    if ziel.startswith("tests/"):
        # If the gate runs a test file, its evidence lies IN that file. The
        # search below would instead accept every file that merely MENTIONS
        # the path — on 2026-09-08 that made `test_workflow_entry.py` the
        # evidence for `ruleset-drift`, because it names the name in a list
        # and has some mutation evidence of its own. A coverage that assumes
        # from a mention covers nothing.
        datei = root / ziel
        return datei.is_file() and bool(MUTATIONS_NAMEN.search(datei.read_text(encoding="utf-8")))
    return any(MUTATIONS_NAMEN.search(text) for p, text in quellen.items() if ziel in text)
