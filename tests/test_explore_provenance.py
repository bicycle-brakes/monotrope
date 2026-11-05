"""The active research census (bead coding-harness-g19n): published model research never says human-written.

Scans every active ``plans/changes/<name>/research.md`` — never the archive — for a header that still
declares ``provenance: human-written`` while the body carries published model research: a published Runner exploration
answer or a research-swarm/v2 envelope. The bootstrap correction of the affected files is the
orchestrator's step 7 of the plan (done 2026-11-04); the test guards that no active file falls back.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PLANS = REPO_ROOT / "plans" / "changes"


def active_research_files() -> list[Path]:
    archive = PLANS / "archive"
    return sorted(path for path in PLANS.glob("*/research.md") if archive not in path.parents)


def test_active_model_research_has_no_false_human_provenance() -> None:
    affected = []
    for path in active_research_files():
        text = path.read_text(encoding="utf-8")
        _, header, body = text.split("---", 2)
        # Quoted examples and fenced code are not runner publication evidence.
        visible = re.sub(r"(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$", "", body)
        published = re.search(r"(?m)^## Runner exploration — \d{4}-\d{2}-\d{2}\s*\n\s*\S", visible) or re.search(
            r"(?ms)^<!-- research-swarm/v2 run [0-9a-f]+ -->\n.+?^<!-- /research-swarm/v2 -->[ \t]*$", visible
        )
        if published and yaml.safe_load(header).get("provenance") == "human-written":
            affected.append(path.relative_to(REPO_ROOT).as_posix())
    assert affected == [], f"active research declares human-written over published model research: {affected}"


@pytest.mark.parametrize("provenance", ["human-written", "'human-written'", '"human-written"'])
@pytest.mark.parametrize("eol", ["\n", "\r\n"])
@pytest.mark.parametrize("published", [None, "single", "swarm"])
def test_census_requires_publication_and_reads_scalar_spellings(tmp_path, monkeypatch, provenance, eol, published):
    # L1-1/L1-2: failed-call audits and quoted marker mentions cannot establish publication;
    # YAML quotes and CRLF cannot hide the same false declaration once an answer is published.
    import sys

    folder = tmp_path / "demo"
    folder.mkdir()
    body = "Stage-2 call, 2026-11-04: explore · rejected\nA mention of research-swarm/v2.\n"
    body += "> ## Runner exploration — 2026-11-04\n> quoted answer\n"
    body += "```text\n## Runner exploration — 2026-11-04\nexample answer\n```\n"
    if published == "single":
        body += "## Runner exploration — 2026-11-04\n\nAccepted answer naming scripts/stage2.py.\n"
    elif published == "swarm":
        body += "<!-- research-swarm/v2 run abc123 -->\n## Research swarm\n"
        body += '```research-swarm/v2 manifest\n{"status": "incomplete"}\n```\n'
        body += "<!-- /research-swarm/v2 -->\n"
    (folder / "research.md").write_bytes((f"---\nprovenance: {provenance}\n---\n" + body).replace("\n", eol).encode())
    monkeypatch.setattr(sys.modules[__name__], "PLANS", tmp_path)
    monkeypatch.setattr(sys.modules[__name__], "REPO_ROOT", tmp_path)
    if published:
        with pytest.raises(AssertionError, match="demo/research.md"):
            test_active_model_research_has_no_false_human_provenance()
    else:
        test_active_model_research_has_no_false_human_provenance()
