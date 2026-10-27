"""The one shared builder for a synthetic terms record a test baseline may rely on.

Several suites hand-built their own admissible record, so a new required
admission field broke them only after a merge: adding mandatory expiry left 55
research-availability tests failing on 2026-10-27. `admissible_terms` is the
one construction site for a record the unchanged production check admits
(`stage2.terms_problem` in `scripts/stage2.py`, held by
`tests/test_terms_fixtures.py`); a test that needs a refusal removes or
replaces a field on its own copy instead of building a second baseline. The
record is synthetic: no field is read from the repository's real
`model-endpoints.yaml`, so renewing the real terms cannot change a baseline.
"""

from __future__ import annotations


def admissible_terms(**overrides: object) -> dict:
    """One admissible terms record, dated far ahead, with the given fields replaced.

    The defaults satisfy the full production admission rule: a dated, sourced
    reading, a retention reading, training ruled out, and a usable expiry. The
    far-future quoted expiry keeps no fixture from aging into a skip; a test
    that wants a boundary sets its own date and pins the terms clock.
    Overrides are applied last and never repaired - a test wanting an invalid
    record passes the invalid value or deletes the field from its copy. There
    is no default cost (`anfragen_5h`) and no skip marker: cost is optional
    metadata, not an implicit property of an admissible record, and a skip is
    always a deliberate act.

    Every call returns a fresh dictionary, so overrides, deletions and planted
    markers on one result never reach a later call's defaults.
    """
    record = {
        "gelesen": "2026-10-07",
        "quelle": "privacy table of the Go page, https://opencode.ai/docs/go",
        "aufbewahrung": "0 days",
        "training": "Not used",
        "valid_until": "2099-01-01",
    }
    record.update(overrides)
    return record
