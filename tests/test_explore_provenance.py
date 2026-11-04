"""The active research census (bead coding-harness-g19n): published model research never says human-written.

Scans every active ``plans/changes/<name>/research.md`` — never the archive — for a header that still
declares ``provenance: human-written`` while the body carries published model research: a Stage-2 call
line or a research-swarm/v2 envelope. The bootstrap correction of the affected files is the
orchestrator's step 7 of the plan (done 2026-11-04); the test guards that no active file falls back.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLANS = REPO_ROOT / "plans" / "changes"


def active_research_files() -> list[Path]:
    archive = PLANS / "archive"
    return sorted(path for path in PLANS.glob("*/research.md") if archive not in path.parents)


def test_active_model_research_has_no_false_human_provenance() -> None:
    affected = []
    for path in active_research_files():
        text = path.read_text(encoding="utf-8")
        header = text.split("---", 2)[1]
        published = "Stage-2 call," in text or "research-swarm/v2" in text
        if published and re.search(r"(?m)^provenance: human-written[ \t]*$", header):
            affected.append(path.relative_to(REPO_ROOT).as_posix())
    assert affected == [], f"active research declares human-written over published model research: {affected}"
