"""research_handoff.py - the obligation inventory of one research run, derived from raw reports.

The research runner (`stage2_research_run.py`) persists the result and the handoff gate
(`check_research_handoff.py`) derives it again independently, so the two cannot drift: one
pure function, standard library only, no model, tracker or network.

An obligation is a question the maintainer owes an answer before the spec rests on the run:

- `decision` - every accepted raw report's `[DECISION]` question, whatever the judge made of its claims;
- `class` - a topic-3 class assessment that differs from the declared class;
- `disagreement` - a structured judge disagreement (the judge may add items, never remove one);
- `neighbour` - a topic-5 `contradicts` relation, an `unrelated` relation for a given path, and a
  suggested neighbour whose evidence is `split`.

A neighbour status is the runner's alone. A relation counts only when at least one listed claim is
runner-valid; three counting related/contradicts relations confirm a suggestion, three counting
unrelated relations reject it, every other case is split. A given path stays given. No judge
disposition enters this calculation: the function takes none.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence

COUNTING_NEEDED = 3
NEIGHBOUR_KIND_ORDER = ("contradicts", "unrelated-given", "split")


def _norm(text: str) -> str:
    return " ".join(str(text).casefold().split())


def _valid_claims(report: Mapping) -> set[str]:
    return {claim["id"] for claim in report.get("claims", ()) if claim.get("evidence_status") == "valid"}


def neighbour_records(packet: Sequence[Mapping], reports: Iterable[Mapping]) -> list[dict]:
    """One record per packet neighbour: its runner-derived status, reason and every seat's relation."""
    rows: dict[str, list[dict]] = {item["path"]: [] for item in packet}
    for report in reports:
        if report.get("topic") != 5:
            continue
        valid = _valid_claims(report)
        for relation in report.get("neighbour_relations", ()):
            if relation["path"] in rows:
                claims = list(relation["claims"])
                rows[relation["path"]].append(
                    {
                        "seat": report["seat"],
                        "relation": relation["relation"],
                        "claims": claims,
                        "counting": any(claim in valid for claim in claims),
                    }
                )
    records = []
    for item in sorted(packet, key=lambda entry: entry["path"]):
        seats = sorted(rows[item["path"]], key=lambda row: row["seat"])
        counting = [row for row in seats if row["counting"]]
        positive = sum(row["relation"] in ("related", "contradicts") for row in counting)
        negative = sum(row["relation"] == "unrelated" for row in counting)
        if item["status"] == "given":
            status, reason = "given", "supplied by the maintainer; the runner never removes it"
        elif len(counting) == COUNTING_NEEDED and positive == COUNTING_NEEDED:
            status, reason = "confirmed", "three counting related or contradicts relations"
        elif len(counting) == COUNTING_NEEDED and negative == COUNTING_NEEDED:
            status, reason = "rejected", "three counting unrelated relations"
        else:
            status = "split"
            reason = f"{len(counting)} counting relations ({positive} related or contradicts, {negative} unrelated)"
        records.append({"path": item["path"], "status": status, "reason": reason, "relations": seats})
    return records


def derive_inventory(
    *,
    run_id: str,
    declared_class: str,
    packet: Sequence[Mapping],
    reports: Sequence[Mapping],
    disagreements: Sequence[Mapping],
) -> dict:
    """The run's neighbour records and its numbered obligation items (`H-1`, `H-2`, ...)."""
    drafts: list[tuple[tuple, dict]] = []
    groups: dict[str, dict] = {}
    for report in reports:
        for question in report.get("questions", ()):
            if question["classification"] != "[DECISION]":
                continue
            group = groups.setdefault(
                _norm(question["question"]), {"summary": question["question"], "questions": set(), "claims": set()}
            )
            group["questions"].add(question["id"])
            group["claims"].update(question["claims"])
    for group in groups.values():
        questions = sorted(group["questions"])
        drafts.append(
            (
                (0, questions[0]),
                {
                    "reason": "decision",
                    "summary": group["summary"],
                    "questions": questions,
                    "claims": sorted(group["claims"]),
                },
            )
        )
    differing: dict[str, dict] = {}
    for report in reports:
        assessment = report.get("class_assessment")
        if report.get("topic") == 3 and assessment and assessment["class"] != declared_class:
            entry = differing.setdefault(assessment["class"], {"claims": set(), "seats": set()})
            entry["claims"].update(assessment["claims"])
            entry["seats"].add(report["seat"])
    for assessed, entry in sorted(differing.items()):
        drafts.append(
            (
                (1, assessed),
                {
                    "reason": "class",
                    "summary": f"topic 3 assesses the class {assessed}; the declared class is {declared_class}",
                    "questions": [],
                    "claims": sorted(entry["claims"]),
                },
            )
        )
    seen = set()
    for item in disagreements:
        claims = sorted(set(item["claims"]))
        if tuple(claims) in seen:
            continue
        seen.add(tuple(claims))
        drafts.append(
            ((2, *claims), {"reason": "disagreement", "summary": item["summary"], "questions": [], "claims": claims})
        )
    neighbours = neighbour_records(packet, reports)
    for record in neighbours:
        wanted = {
            "contradicts": [row for row in record["relations"] if row["relation"] == "contradicts"],
            "unrelated-given": (
                [row for row in record["relations"] if row["relation"] == "unrelated"]
                if record["status"] == "given"
                else []
            ),
            "split": record["relations"] if record["status"] == "split" else [],
        }
        for kind in NEIGHBOUR_KIND_ORDER:
            rows = wanted[kind]
            if not rows:
                continue
            drafts.append(
                (
                    (3, record["path"], NEIGHBOUR_KIND_ORDER.index(kind)),
                    {
                        "reason": "neighbour",
                        "kind": kind,
                        "path": record["path"],
                        "summary": f"{kind} for {record['path']}: {record['reason']}",
                        "questions": [],
                        "claims": sorted({claim for row in rows for claim in row["claims"]}),
                    },
                )
            )
    drafts.sort(key=lambda pair: pair[0])
    items = [{"id": f"H-{number}", **body} for number, (_key, body) in enumerate(drafts, 1)]
    return {"run_id": run_id, "declared_class": declared_class, "neighbours": neighbours, "items": items}
