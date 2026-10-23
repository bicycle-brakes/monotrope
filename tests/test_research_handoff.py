"""The gate `research-handoff`: what a research run hands to the interview and the spec stays measured.

Criteria 29-34 of plans/changes/research-swarm/spec.md. Every tree is built in `tmp_path` from fixture
records written the way the research runner writes them (fenced `research-swarm/v2` blocks inside
`research.md`); nothing here starts a model, reads the tracker or touches the network. Each test comes
with its fault: the planted mutation is named in the comment. The checker derives the obligation
inventory itself, through the same pure function the runner uses (`scripts/research_handoff.py`).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "check_research_handoff.py"
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_research_handoff as gate  # noqa: E402
import research_handoff  # noqa: E402

RUN1 = "a1" * 16
RUN2 = "b2" * 16
RUN3 = "c3" * 16
SEATS = ("opencode-go:a", "opencode-go:b", "claude-code-plan:c")
P = "plans/changes/other/spec.md"
Q = "plans/changes/third/spec.md"
NEW = "plans/changes/fresh/spec.md"


def fenced(info: str, value: object) -> str:
    return f"```research-swarm/v2 {info}\n{json.dumps(value, sort_keys=True, indent=2)}\n```"


def gid(run: str, topic: int, seat: str, local: str) -> str:
    return f"{run}/{topic}/{seat}/{local}"


def make_report(run: str, topic: int, seat: str, *, valid: bool = True, **extra: object) -> dict:
    claims = [{"id": gid(run, topic, seat, "C1"), "evidence_status": "valid" if valid else "unsupported"}]
    if not valid:
        claims.append({"id": gid(run, topic, seat, "C2"), "evidence_status": "valid"})
    return {"run_id": run, "topic": topic, "seat": seat, "claims": claims, "questions": [], **extra}


def run_text(
    run: str,
    *,
    status: str = "complete",
    klass: str = "feature",
    given: tuple[str, ...] = (),
    suggested: tuple[str, ...] = (),
    kinds: dict[str, tuple[str, str, str]] | None = None,
    unsupported: tuple[str, ...] = (),
    decision: str | None = "Which store?",
    assessed: str = "feature",
    disagreements: tuple[dict, ...] = (),
    inventory: str = "derive",
    supported: str = "all",
    extra_blocks: tuple[str, ...] = (),
    question_link: str | None = None,
    manifest_given: tuple[str, ...] | None = None,
) -> str:
    """One run, written like the runner writes it; `inventory` is derive, none, drop or corrupt."""
    packet = [{"path": p, "status": "given", "map_keys": []} for p in given]
    packet += [{"path": p, "status": "suggested", "map_keys": []} for p in suggested]
    reports = []
    for number, seat in enumerate(SEATS):
        report = make_report(run, 1, seat)
        if decision:
            report["questions"] = [
                {"id": gid(run, 1, seat, "Q1"), "question": decision, "classification": "[DECISION]",
                 "claims": [question_link or gid(run, 1, seat, "C1")]}
            ]  # fmt: skip
        reports.append(report)
        if seat == SEATS[0]:
            reports.append(
                make_report(
                    run,
                    3,
                    seat,
                    class_assessment={"class": assessed, "claims": [gid(run, 3, seat, "C1")]},
                )  # fmt: skip
            )
        relations = []
        for path in [*given, *suggested]:
            kind = (kinds or {}).get(path, ("related",) * 3)[number]
            relations.append({"path": path, "relation": kind, "claims": [gid(run, 5, seat, "C1")]})
        reports.append(make_report(run, 5, seat, valid=seat not in unsupported, neighbour_relations=relations))
    manifest = {
        "schema": "research-swarm/v2",
        "run_id": run,
        "class": klass,
        "status": status,
        "given_neighbours": list(given if manifest_given is None else manifest_given),
    }
    judge = {"disagreements": list(disagreements)}
    scores = []
    for report in reports:
        ids = [c["id"] for c in report["claims"] if c["evidence_status"] == "valid"]
        ids = ids if supported == "all" else [i for i in ids if i not in supported.split(",")]
        buckets = {
            name: {"count": 0, "claims": []}
            for name in ("supported", "refuted", "off-brief", "unresolved", "unsupported", "unique")
        }
        for claim in report["claims"]:
            disposition = (
                "unsupported"
                if claim["evidence_status"] == "unsupported"
                else "supported"
                if claim["id"] in ids
                else "unresolved"
            )
            buckets[disposition]["claims"].append(claim["id"])
            buckets[disposition]["count"] += 1
            if disposition != "unsupported":
                judge.setdefault("claim_judgements", []).append(
                    {"claim": claim["id"], "disposition": disposition, "unique": False}
                )
        scores.append({"topic": report["topic"], "seat": report["seat"], **buckets})
    parts = [
        f"<!-- research-swarm/v2 run {run} -->",
        f"## Research swarm - 2026-10-19\n\nrun {run}",
        fenced("manifest", manifest),
        fenced("map", {"neighbours": packet}),
        *(fenced("report", r) for r in reports),
        fenced("reconciliation", {"reconciliation": judge, "scores": scores}),
    ]
    derived = research_handoff.derive_inventory(
        run_id=run, declared_class=klass, packet=packet, reports=reports, disagreements=list(disagreements)
    )
    if inventory == "derive":
        parts.append(fenced("inventory", derived))
    elif inventory == "drop":
        derived["items"] = derived["items"][1:]
        parts.append(fenced("inventory", derived))
    elif inventory == "corrupt":
        parts.append("```research-swarm/v2 inventory\n{not json\n```")
    parts += list(extra_blocks)
    parts += [f"run {run} status: {status}.", "<!-- /research-swarm/v2 -->"]
    return "\n\n".join(parts) + "\n"


def q_record(number: int, *, items: tuple[str, ...] = (), claims: tuple[str, ...] = (), keep=None, drop=None,
             add=None, answered_by: str = "maintainer", status: str = "answered", answer: str = "yes",
             context: bool = True, extra: str = "") -> str:  # fmt: skip
    lines = [f"## Q-{number} · record {number}", "", "asked: 2026-10-19", f'answer: "{answer}"']
    lines += [f"answered_by: {answered_by}", f"status: {status}"]
    if items:
        lines.append(f"research_items: [{', '.join(items)}]")
    if claims:
        lines.append("research_claims:\n" + "\n".join(f"  - {c}" for c in claims))
    if keep is not None or drop is not None or add is not None:
        parts = [f"{k}: [{', '.join(v or [])}]" for k, v in (("keep", keep), ("drop", drop), ("add", add))]
        lines.append("research_neighbours: {" + ", ".join(parts) + "}")
    if context:
        lines.append("context: |\n  Topic: demo.")
    return "\n".join(lines) + extra + "\n"


def spec_text(neighbours: list[str] | None = (), basis: tuple[str, ...] = ("`decisions.md#Q-1`",)) -> str:
    header = "---\ntitle: Spec\nclass: feature\n"
    if neighbours is not None:
        header += f"neighbours: [{', '.join(neighbours)}]\n"
    header += "---\n\n## Acceptance criteria\n\n"
    body = ""
    for number, line in enumerate(basis, 1):
        body += f"{number}. When x, y.\n   *Refuted by:* z.\n   *Basis:* {line}.\n"
    return header + body


class World:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.folder = root / "plans" / "changes" / "demo"
        self.folder.mkdir(parents=True)

    def write(self, runs: list[str], records: list[str] | None = None, spec: str | None = "default") -> World:
        (self.folder / "research.md").write_text(
            "---\ntitle: Research\n---\n\n# Research\n\n" + "\n".join(runs), encoding="utf-8"
        )
        items = (f"{RUN1}/H-1",)
        recs = [q_record(1, items=items)] if records is None else records
        (self.folder / "decisions.md").write_text("# Decisions\n\n" + "\n".join(recs), encoding="utf-8")
        spec_file = self.folder / "spec.md"
        if spec is None:
            spec_file.unlink(missing_ok=True)
        else:
            spec_file.write_text(spec_text() if spec == "default" else spec, encoding="utf-8")
        return self

    def check(self, capsys: pytest.CaptureFixture[str], *extra: str) -> tuple[int, str]:
        capsys.readouterr()
        code = gate.main(["--root", str(self.root), *extra])
        captured = capsys.readouterr()
        return code, captured.out + captured.err


@pytest.fixture
def world(tmp_path: Path) -> World:
    return World(tmp_path)


def test_a_lost_research_decision_turns_the_gate_red(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criteria 31, 32. Planted fault: the class minimums hide a lost item, an open/agent answer passes, or an
    # inventory that dropped a derived item is believed.
    run = run_text(RUN1)
    world.write([run])
    assert world.check(capsys)[0] == 0
    world.write([run], records=[])
    code, out = world.check(capsys)
    assert code == 1 and f"{RUN1}/H-1" in out, "no answer: the item is open"
    for record in (
        q_record(1, items=(f"{RUN1}/H-1",), answered_by="agent"),
        q_record(1, items=(f"{RUN1}/H-1",), status="open"),
        q_record(1, items=(f"{RUN1}/H-1",), context=False),
        q_record(1, items=(f"{RUN1}/H-1",), answer=" "),
    ):
        world.write([run], records=[record])
        assert world.check(capsys)[0] == 1, record
    world.write([run], records=[q_record(1, items=(f"{RUN1}/H-1",)), q_record(2, answer="no")])
    assert world.check(capsys)[0] == 0, "an explicit human rejection counts as an answer"
    world.write([run_text(RUN1, inventory="drop")])
    code, out = world.check(capsys)
    assert code == 1 and "inventory" in out, "an inventory that lost a derived item"
    world.write([run_text(RUN1, inventory="none")])
    assert world.check(capsys)[0] == 1


def test_pending_handoff_is_green_only_before_spec(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 32. Planted fault: pre-spec pending items fail, or the same unanswered items pass with a spec.
    world.write([run_text(RUN1)], records=[], spec=None)
    code, out = world.check(capsys)
    assert code == 0 and f"pending: {RUN1}/H-1" in out
    world.write([run_text(RUN1)], records=[], spec="default")
    assert world.check(capsys)[0] == 1


def test_only_complete_runs_supply_handoff_and_prior_obligations_survive(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 32. Planted fault: an incomplete run's claims support a spec, no complete run passes, or a
    # rerun erases an earlier obligation.
    incomplete = run_text(RUN1, status="incomplete - the judge failed")
    world.write([incomplete], records=[])
    code, out = world.check(capsys)
    assert code == 1 and "no complete" in out, "a spec with v2 runs but none complete"
    world.write([incomplete], records=[], spec=None)
    assert world.check(capsys)[0] == 0, "before the spec, an incomplete run is not an error"
    # a later complete run with another decision keeps the earlier complete run's item open
    first, second = run_text(RUN1), run_text(RUN2, decision="Which queue?")
    world.write([first, second], records=[q_record(1, items=(f"{RUN2}/H-1",))])
    code, out = world.check(capsys)
    assert code == 1 and f"{RUN1}/H-1" in out
    world.write([first, second], records=[q_record(1, items=(f"{RUN1}/H-1", f"{RUN2}/H-1"))])
    assert world.check(capsys)[0] == 0, "one Q-record answers items from several runs"
    # an incomplete run carries no obligation
    world.write([first, run_text(RUN2, status="incomplete - stopped", decision="Which queue?")])
    assert world.check(capsys)[0] == 0
    # its claims cannot be a basis
    spec = spec_text(basis=(f"`{gid(RUN2, 1, SEATS[0], 'C1')}`",))
    world.write([first, run_text(RUN2, status="incomplete - stopped")], spec=spec)
    assert world.check(capsys)[0] == 1


def test_live_archive_and_legacy_handoff_scope(
    world: World, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 32. Planted fault: archived changes escape the gate, a legacy folder without v2 evidence
    # fails, or an exemption is not reported.
    legacy = world.root / "plans" / "changes" / "legacy"
    legacy.mkdir(parents=True)
    (legacy / "research.md").write_text("# Research\n\nplain old notes\n", encoding="utf-8")
    (legacy / "spec.md").write_text("---\ntitle: Old\n---\n", encoding="utf-8")
    world.write([run_text(RUN1)])
    code, out = world.check(capsys)
    assert code == 0 and "legacy" in out and "exempt" in out
    archive = world.root / "plans" / "changes" / "archive" / "2026-10-01-old"
    archive.mkdir(parents=True)
    (archive / "research.md").write_text("# Research\n\n" + run_text(RUN2), encoding="utf-8")
    (archive / "spec.md").write_text(spec_text(), encoding="utf-8")
    (archive / "decisions.md").write_text("# Decisions\n", encoding="utf-8")
    code, out = world.check(capsys)
    assert code == 1 and "2026-10-01-old" in out, "an archived change keeps its obligations"
    (archive / "decisions.md").write_text("# Decisions\n\n" + q_record(1, items=(f"{RUN2}/H-1",)), encoding="utf-8")
    assert world.check(capsys)[0] == 0
    assert world.check(capsys, "--change", "demo")[0] == 0
    (archive / "decisions.md").write_text("# Decisions\n", encoding="utf-8")
    assert world.check(capsys, "--change", "demo")[0] == 0, "--change limits the scope"
    assert world.check(capsys, "--change", "old")[0] == 1, "the archive folder is found by its change name"
    code, out = world.check(capsys, "--change", "no-such-change")
    assert code == 3
    empty = tmp_path / "empty"
    empty.mkdir()
    assert gate.main(["--root", str(empty)]) == 3, "a tree without plans/changes is not measured"
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(world.root), "--change", "demo"],
        capture_output=True, text=True, check=False,
    )  # fmt: skip
    assert done.returncode == 0


def test_unread_or_ambiguous_handoff_is_not_measured(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 33. Planted fault: malformed manifests/inventories, duplicate global ids, missing linked files
    # or ambiguous answers pass.
    good = run_text(RUN1)
    for bad in (
        run_text(RUN1, inventory="corrupt"),
        good.replace("<!-- /research-swarm/v2 -->", ""),
        good.replace(f'"run_id": "{RUN1}"', f'"run_id": "{RUN2}"', 1),
        good + good,  # the same run twice
        good.replace('"schema": "research-swarm/v2"', '"schema": "research-swarm/v1"'),
        run_text(RUN1, extra_blocks=("```research-swarm/v2 report\n[1]\n```",)),
    ):
        world.write([bad])
        code, out = world.check(capsys)
        assert code == 3, (out, bad[:80])
    duplicate = make_report(RUN1, 1, SEATS[0])
    world.write([run_text(RUN1, extra_blocks=(fenced("report", duplicate),))])
    assert world.check(capsys)[0] == 3, "a second report for one topic and seat repeats global claim ids"
    world.write([good], records=[q_record(1, items=(f"{RUN1}/H-99",))])
    assert world.check(capsys)[0] == 3, "a link to an item no run has"
    world.write([good], records=[q_record(1, items=(f"{RUN1}/H-1",), claims=(f"{RUN1}/9/x/C1",))])
    assert world.check(capsys)[0] == 3, "a link to a claim no run has"
    world.write([good], records=[q_record(1, items=(f"{RUN1}/H-1",)), q_record(1, items=(f"{RUN1}/H-1",))])
    assert world.check(capsys)[0] == 3, "one question id answered twice is ambiguous"
    world.write([good], records=[q_record(1, items=(f"{RUN1}/H-1",), extra="\nresearch_items: [x]")])
    assert world.check(capsys)[0] == 3, "a field twice in one record"
    world.write([good], records=[q_record(1, items=(f"{RUN1}/H-1",), extra="\nresearch_neighbours: [1]")])
    assert world.check(capsys)[0] == 3, "a neighbour field that is no mapping"


def test_a_dangling_question_claim_link_is_not_measured(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 33 (phase-6 F-33). Planted fault: a report question linking a claim no report holds still
    # lets an answered record close the derived item, and the gate finds nothing.
    world.write([run_text(RUN1)], records=[q_record(1, items=(f"{RUN1}/H-1",))])
    assert world.check(capsys)[0] == 0, "the same report with a real link is measured"
    dangling = run_text(RUN1, question_link=gid(RUN1, 1, SEATS[0], "C2"))
    world.write([dangling], records=[q_record(1, items=(f"{RUN1}/H-1",))])
    code, out = world.check(capsys)
    assert code == 3, out


def test_a_manifest_given_path_the_map_omits_is_not_measured(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criteria 30, 33 (phase-6 F-36). Planted fault: the manifest gives a spec path, the map omits it, and the
    # contradictory records silently erase the human-given dependency from the required neighbours.
    agree = run_text(RUN1, given=(P,))
    world.write([agree], records=[q_record(1, items=(item_of(RUN1, 1),))], spec=spec_text(neighbours=[P]))
    assert world.check(capsys)[0] == 0, "consistent records are measured"
    contradictory = run_text(RUN1, given=(), manifest_given=(P,))
    world.write([contradictory], records=[q_record(1, items=(item_of(RUN1, 1),))], spec=spec_text(neighbours=[]))
    code, out = world.check(capsys)
    assert code == 3, out
    assert P in out


def item_of(run: str, number: int) -> str:
    return f"{run}/H-{number}"


def with_header(world: World, runs: list[str], header: list[str], records: list[str]) -> None:
    world.write(runs, records=records, spec=spec_text(neighbours=header))


def test_spec_neighbours_match_confirmed_research_paths(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 30. Planted fault: a required path disappears, or an extra path outside the confirmed/given/
    # linked-human sets passes.
    run = run_text(RUN1, given=(Q,), suggested=(P,))
    records = [q_record(1, items=(item_of(RUN1, 1),))]
    with_header(world, [run], [P, Q], records)
    assert world.check(capsys)[0] == 0
    with_header(world, [run], [P], records)
    code, out = world.check(capsys)
    assert code == 1 and Q in out
    with_header(world, [run], [P, Q, NEW], records)
    code, out = world.check(capsys)
    assert code == 1 and NEW in out
    world.write([run], records=records, spec=spec_text(neighbours=None))
    assert world.check(capsys)[0] == 1, "a spec without the neighbours key"
    with_header(world, [run], [P, P, Q], records)
    assert world.check(capsys)[0] == 1, "a duplicate path"
    with_header(world, [run], ["plans/changes/../x/spec.md", P, Q], records)
    assert world.check(capsys)[0] == 1, "an escaping path"


def test_given_neighbour_drop_requires_linked_human_answer(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criteria 29, 30. Planted fault: three unrelated judgements remove a given neighbour without an answered,
    # item-linked structured drop.
    run = run_text(RUN1, given=(Q,), kinds={Q: ("unrelated",) * 3})
    assert gate_items(run) == [item_of(RUN1, 1), item_of(RUN1, 2)]
    prose = [q_record(1, items=(item_of(RUN1, 1), item_of(RUN1, 2)), answer="drop Q please")]
    with_header(world, [run], [], prose)
    assert world.check(capsys)[0] == 1, "the given path leaves the set without a structured drop"
    with_header(world, [run], [Q], prose)
    assert world.check(capsys)[0] == 1, "a prose answer leaves the item open"
    structured = [q_record(1, items=(item_of(RUN1, 1), item_of(RUN1, 2)), drop=[Q])]
    with_header(world, [run], [], structured)
    assert world.check(capsys)[0] == 0
    with_header(world, [run], [Q], structured)
    assert world.check(capsys)[0] == 1, "a drop requires omission"


def gate_items(run: str) -> list[str]:
    blocks = gate.parse_text(run, "test")
    (parsed,) = blocks
    return [f"{parsed.run_id}/{item['id']}" for item in parsed.derived["items"]]


def test_structured_neighbour_answers_enforce_keep_drop_and_unlinked_add(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 30. Planted fault: prose-only or path-free linked answers close items, keep/drop allow the
    # wrong header, an add needs an item link, or a prose-only addition passes.
    run = run_text(RUN1, suggested=(P,), kinds={P: ("related", "contradicts", "related")})
    both = (item_of(RUN1, 1), item_of(RUN1, 2))
    with_header(world, [run], [P], [q_record(1, items=both)])
    assert world.check(capsys)[0] == 1, "a linked answer without the path leaves the contradiction open"
    with_header(world, [run], [P], [q_record(1, items=both, keep=[P])])
    assert world.check(capsys)[0] == 0
    with_header(world, [run], [], [q_record(1, items=both, keep=[P])])
    assert world.check(capsys)[0] == 1, "keep requires the path"
    with_header(world, [run], [], [q_record(1, items=both, drop=[P])])
    assert world.check(capsys)[0] == 0
    with_header(world, [run], [P], [q_record(1, items=both, drop=[P])])
    assert world.check(capsys)[0] == 1, "drop requires omission"
    answered = q_record(1, items=both, keep=[P])
    with_header(world, [run], [P, NEW], [answered, q_record(2, add=[NEW])])
    assert world.check(capsys)[0] == 0, "an add needs no item link"
    with_header(world, [run], [P, NEW], [answered, q_record(2, answer="please also add fresh")])
    assert world.check(capsys)[0] == 1, "a prose-only addition"
    with_header(world, [run], [P], [answered, q_record(2, add=[NEW])])
    assert world.check(capsys)[0] == 1, "an add requires inclusion"
    with_header(world, [run], [P, NEW], [answered, q_record(2, add=[NEW], answered_by="agent")])
    assert world.check(capsys)[0] == 1, "no agent waiver"


@pytest.mark.parametrize("unsupported", [(), (SEATS[2],)], ids=["judge-confirmed-split", "evidence-gap-split"])
def test_split_neighbours_need_item_link_and_structured_keep_or_drop(
    world: World, capsys: pytest.CaptureFixture[str], unsupported: tuple[str, ...]
) -> None:
    # Criteria 30, 32. Planted fault: an unanswered split passes either header, a judge confirmation substitutes
    # for the maintainer, or an evidence-gap split (three related, one without valid evidence) is confirmed.
    kinds = {P: ("related", "unrelated", "related")} if not unsupported else {P: ("related",) * 3}
    run = run_text(RUN1, suggested=(P,), kinds=kinds, unsupported=unsupported)  # the judge supports every valid claim
    items = (item_of(RUN1, 1), item_of(RUN1, 2))
    for header in ([P], []):
        with_header(world, [run], header, [q_record(1, items=(item_of(RUN1, 1),))])
        code, out = world.check(capsys)
        assert code == 1 and "split" in out, (header, out)
    with_header(world, [run], [P], [q_record(1, items=items, keep=[P])])
    assert world.check(capsys)[0] == 0
    with_header(world, [run], [], [q_record(1, items=items, keep=[P])])
    assert world.check(capsys)[0] == 1
    with_header(world, [run], [], [q_record(1, items=items, drop=[P])])
    assert world.check(capsys)[0] == 0
    with_header(world, [run], [P], [q_record(1, items=items, drop=[P])])
    assert world.check(capsys)[0] == 1
    with_header(world, [run], [P], [q_record(1, items=(item_of(RUN1, 1),), keep=[P])])
    assert world.check(capsys)[0] == 1, "keep without the item link leaves the split open"
    # a split is not required in the header before the human keep
    with_header(world, [run], [P], [q_record(1, items=(item_of(RUN1, 1),))])
    assert world.check(capsys)[0] == 1


def test_neighbour_evidence_gap_requires_structured_answer(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criteria 30, 32. Planted fault: an evidence-gap split joins the required header without structured keep, or
    # passes with an unsupported-relation split lacking an item-linked keep/drop once the spec exists.
    run = run_text(RUN1, suggested=(P,), unsupported=(SEATS[2],))
    pre = world.write([run], records=[], spec=None)
    code, out = pre.check(capsys)
    assert code == 0 and "split" in out, "listed as pending before the spec"
    with_header(world, [run], [P], [q_record(1, items=(item_of(RUN1, 1), item_of(RUN1, 2)))])
    assert world.check(capsys)[0] == 1, "prose-only keep leaves the item open"
    with_header(world, [run], [P], [q_record(1, items=(item_of(RUN1, 1), item_of(RUN1, 2)), keep=[P])])
    assert world.check(capsys)[0] == 0


def test_cross_run_neighbour_conflicts_require_linked_human_answers(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criteria 29-32. Planted fault: a path confirmed then rejected, or a given path omitted by a later run,
    # loses its derived human item; latest-only parity passes; an unlinked drop closes it.
    confirm = run_text(RUN1, suggested=(P,))
    reject = run_text(RUN2, suggested=(P,), kinds={P: ("unrelated",) * 3}, decision=None)
    conflict = f"{RUN2}/X-1"
    first = q_record(1, items=(item_of(RUN1, 1),))
    for header in ([P], []):
        with_header(world, [confirm, reject], header, [first])
        code, out = world.check(capsys)
        assert code == 1 and conflict in out and RUN1 in out, (header, out)
    with_header(world, [confirm, reject], [P], [first, q_record(2, items=(conflict,), keep=[P])])
    assert world.check(capsys)[0] == 0
    with_header(world, [confirm, reject], [], [first, q_record(2, items=(conflict,), keep=[P])])
    assert world.check(capsys)[0] == 1, "keep passes only with the path"
    with_header(world, [confirm, reject], [], [first, q_record(2, items=(conflict,), drop=[P])])
    assert world.check(capsys)[0] == 0
    with_header(world, [confirm, reject], [P], [first, q_record(2, items=(conflict,), drop=[P])])
    assert world.check(capsys)[0] == 1
    with_header(world, [confirm, reject], [], [first, q_record(2, drop=[P])])
    assert world.check(capsys)[0] == 1, "a drop without the item link leaves the conflict open"
    # the earlier run keeps its authority: a rejection alone does not erase the confirmed path
    with_header(world, [confirm, run_text(RUN2, decision=None)], [], [first])
    assert world.check(capsys)[0] == 1, "the later run lists no neighbours: the confirmed path is still required"
    # a given path that a later run omits
    given = run_text(RUN1, given=(Q,))
    omitted = run_text(RUN2, decision=None)
    omission = f"{RUN2}/X-1"
    for header in ([Q], []):
        with_header(world, [given, omitted], header, [first])
        code, out = world.check(capsys)
        assert code == 1 and omission in out, (header, out)
    with_header(world, [given, omitted], [], [first, q_record(2, items=(omission,), drop=[Q])])
    assert world.check(capsys)[0] == 0
    with_header(world, [given, omitted], [Q], [first, q_record(2, items=(omission,), drop=[Q])])
    assert world.check(capsys)[0] == 1
    # confirmed-path drops
    only = run_text(RUN1, suggested=(P,))
    with_header(world, [only], [], [first, q_record(2, drop=[P])])
    assert world.check(capsys)[0] == 0
    with_header(world, [only], [P], [first, q_record(2, drop=[P])])
    assert world.check(capsys)[0] == 1


def test_neighbour_parity_allows_only_linked_additions_and_given_drops(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 30. Planted fault: an arbitrary extra path passes unless structured as a human add or confirmed
    # by a new complete run; a drop outside a maintainer record removes a required path.
    run = run_text(RUN1, given=(Q,))
    first = q_record(1, items=(item_of(RUN1, 1),))
    with_header(world, [run], [Q, NEW], [first])
    assert world.check(capsys)[0] == 1
    with_header(world, [run], [Q, NEW], [first, q_record(2, add=[NEW])])
    assert world.check(capsys)[0] == 0
    newer = run_text(RUN2, given=(Q,), suggested=(NEW,), decision=None)
    with_header(world, [run, newer], [Q, NEW], [first])
    assert world.check(capsys)[0] == 0, "a new complete run confirms the discovery"
    with_header(world, [run], [], [first, q_record(2, drop=[Q], answered_by="agent")])
    assert world.check(capsys)[0] == 1, "only a maintainer-answered record drops a path"


def test_conflicting_neighbour_directives_are_not_measured(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 33. Planted fault: a path in two directive lists, or incompatible answered records, passes
    # instead of exit 3.
    run = run_text(RUN1, given=(Q,))
    first = q_record(1, items=(item_of(RUN1, 1),))
    for records in (
        [first, q_record(2, keep=[Q], drop=[Q])],
        [first, q_record(2, keep=[Q]), q_record(3, drop=[Q])],
        [first, q_record(2, add=[NEW]), q_record(3, drop=[NEW])],
        [first, q_record(2, add=[NEW], keep=[NEW])],
    ):
        with_header(world, [run], [Q], records)
        assert world.check(capsys)[0] == 3, records
    with_header(world, [run], [Q], [first, q_record(2, keep=[Q], answered_by="agent"), q_record(3, drop=[Q])])
    assert world.check(capsys)[0] != 3, "an agent record carries no directive"


def test_neighbour_directives_check_form_without_current_existence(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criterion 30. Planted fault: an invalid form passes, or archival invalidates a structurally valid
    # historical path.
    run = run_text(RUN1)
    first = q_record(1, items=(item_of(RUN1, 1),))
    gone = "plans/changes/archive/2026-01-01-gone/spec.md"
    living = "plans/specs/living/spec.md"
    with_header(world, [run], [gone, living], [first, q_record(2, add=[gone, living])])
    assert world.check(capsys)[0] == 0, "none of the added specs exists, yet the form is valid"
    for bad in ("plans/changes/x/plan.md", "../outside/spec.md", "/abs/spec.md", "plans/changes/archive/x/spec.md", ""):
        with_header(world, [run], [], [first, q_record(2, add=[f'"{bad}"'])])
        code, out = world.check(capsys)
        assert code == 1 and "form" in out, (bad, out)


def claim_basis(run: str, seat: str = SEATS[0], topic: int = 1) -> str:
    return f"`{gid(run, topic, seat, 'C1')}`"


def test_every_criterion_names_existing_claims_or_answers(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 34. Planted fault: a missing, incomplete-run or unsupported claim id, a missing origin or an
    # unanswered Q-record passes.
    run = run_text(RUN1)
    records = [q_record(1, items=(item_of(RUN1, 1),)), q_record(2, status="open", answer="")]

    def spec(*bases: str) -> str:
        return spec_text(neighbours=[], basis=bases)

    for bases, code in [
        ((claim_basis(RUN1),), 0),
        (("`decisions.md#Q-1`", claim_basis(RUN1, SEATS[1])), 0),
        (("`decisions.md#Q-9`",), 1),  # no such record
        (("`decisions.md#Q-2`",), 1),  # unanswered
        ((claim_basis(RUN1, "opencode-go:zzz"),), 1),  # a claim no report holds
        (("see the research",), 1),  # no origin at all
        (("`decisions.md#Q-1`", "nothing"), 1),
    ]:
        world.write([run], records=records, spec=spec(*bases))
        assert world.check(capsys)[0] == code, bases
    world.write(
        [run],
        records=records,
        spec=spec_text(neighbours=[], basis=("`decisions.md#Q-1`",)).replace("*Basis:*", "*Foundation:*"),
    )
    assert world.check(capsys)[0] == 1, "a criterion without a Basis line"


def test_every_direct_basis_claim_must_be_supported(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 34. Planted fault: any non-supported disposition passes, including alongside a supported claim,
    # or an answered Q-record mediation is refused.
    weak = gid(RUN1, 1, SEATS[0], "C1")
    run = run_text(RUN1, supported=weak)  # the judge left the first seat's claim out of "supported"
    items = (item_of(RUN1, 1),)
    world.write([run], records=[q_record(1, items=items)], spec=spec_text(neighbours=[], basis=(f"`{weak}`",)))
    code, out = world.check(capsys)
    assert code == 1 and weak in out
    mixed = f"`{gid(RUN1, 1, SEATS[1], 'C1')}` and `{weak}`"
    world.write([run], records=[q_record(1, items=items)], spec=spec_text(neighbours=[], basis=(mixed,)))
    assert world.check(capsys)[0] == 1, "a mixed Basis fails when any named claim is not supported"
    world.write(
        [run],
        records=[q_record(1, items=items, claims=(weak,))],
        spec=spec_text(neighbours=[], basis=("`decisions.md#Q-1`",)),
    )
    assert world.check(capsys)[0] == 0, "an answered Q-record mediates the weak claim through research_claims"
    ok = f"`{gid(RUN1, 1, SEATS[1], 'C1')}`"
    world.write([run], records=[q_record(1, items=items)], spec=spec_text(neighbours=[], basis=(ok,)))
    assert world.check(capsys)[0] == 0


def test_a_supported_list_contradicting_the_claim_evidence_status_is_not_measured(
    world: World, capsys: pytest.CaptureFixture[str]
) -> None:
    # Criteria 33, 34 (phase-6 F-23). Planted fault: the stored supported list is trusted without the claim's
    # own evidence status, so a claim its report marks unsupported passes as a criterion basis.
    claim = gid(RUN1, 1, SEATS[0], "C1")
    run = run_text(RUN1)
    contradicted = run.replace(
        f'"evidence_status": "valid",\n      "id": "{claim}"',
        f'"evidence_status": "unsupported",\n      "id": "{claim}"',
        1,
    )
    assert contradicted != run, "the planted contradiction must change the record"
    world.write(
        [contradicted],
        records=[q_record(1, items=(item_of(RUN1, 1),))],
        spec=spec_text(neighbours=[], basis=(f"`{claim}`",)),
    )
    code, out = world.check(capsys)
    assert code == 3 and claim in out, out
    world.write(
        [run], records=[q_record(1, items=(item_of(RUN1, 1),))], spec=spec_text(neighbours=[], basis=(f"`{claim}`",))
    )
    assert world.check(capsys)[0] == 0, "the untouched record stays green"


def test_duplicate_keys_in_records_are_not_measured(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 33 (phase-6 F-16). Planted fault: the last of two equal JSON or YAML keys wins silently.
    good = run_text(RUN1)
    neighbours = "\nresearch_neighbours:\n  keep: [plans/changes/a/spec.md]\n  keep: [plans/changes/b/spec.md]"
    record = q_record(1, items=(f"{RUN1}/H-1",)) + neighbours
    world.write([good], records=[record], spec=spec_text(neighbours=["plans/changes/b/spec.md"]))
    assert world.check(capsys)[0] == 3, "a nested YAML key twice: A would be discarded silently"
    twice = good.replace('"class": "feature"', '"class": "feature",\n  "class": "spike"', 1)
    assert twice != good
    world.write([twice])
    assert world.check(capsys)[0] == 3, "a manifest with two contradictory class keys"


def test_a_subsection_heading_does_not_end_basis_checking(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criterion 34 (phase-6 F-25). Planted fault: a level-three heading under "## Acceptance criteria" ends
    # Basis checking, so a criterion below it without an origin passes with no findings.
    run = run_text(RUN1)
    plain = spec_text(neighbours=[], basis=("`decisions.md#Q-1`",))
    world.write([run], spec=plain)
    assert world.check(capsys)[0] == 0
    sectioned = plain.replace("1. When x, y.", "### Functional\n\n1. When x, y.")
    without_origin = sectioned.replace("   *Basis:* `decisions.md#Q-1`.\n", "")
    assert without_origin != sectioned
    world.write([run], spec=without_origin)
    code, out = world.check(capsys)
    assert code == 1, "a criterion inside a subsection without a Basis line is a finding"
    world.write([run], spec=sectioned)
    assert world.check(capsys)[0] == 0, "a criterion inside a subsection with an origin passes"
    other = sectioned.replace("### Functional", "## Notes")
    world.write([run], spec=other.replace("   *Basis:* `decisions.md#Q-1`.\n", ""))
    assert world.check(capsys)[0] == 1, "a later main section must not hide an acceptance criterion"


@pytest.mark.parametrize("link_kind", ["question", "class", "neighbour", "disagreement"])
@pytest.mark.parametrize("target", ["other-report", "other-run", "missing"])
def test_evidence_links_stay_in_their_report_or_judge_run(world: World, capsys, link_kind, target) -> None:
    own = gid(RUN1, 1, SEATS[0], "C1")
    peer = gid(RUN1, 1, SEATS[1], "C1")
    foreign = gid(RUN2, 1, SEATS[0], "C1")
    link = {"other-report": peer, "other-run": foreign, "missing": "missing-claim"}[target]
    records = [q_record(1, items=(f"{RUN1}/H-1",))]
    if link_kind == "disagreement":
        run = run_text(RUN1, decision=None, disagreements=({"claims": [own, link], "summary": "Dissent"},))
    else:
        run = run_text(RUN1, given=(P,) if link_kind == "neighbour" else ())
        if link_kind == "question":
            run = run_text(RUN1, question_link=link)
        else:
            source = gid(RUN1, 3 if link_kind == "class" else 5, SEATS[0], "C1")
            # Replace just the link, keeping the claim itself and the stored inventory consistent.
            blocks = gate.parse_text(run, "fixture")[0]
            reports = blocks.reports
            report = next(r for r in reports if r["topic"] == (3 if link_kind == "class" else 5))
            changed = json.loads(json.dumps(report))
            field = changed["class_assessment"] if link_kind == "class" else changed["neighbour_relations"][0]
            assert field["claims"] == [source]
            field["claims"] = [link]
            run = run.replace(fenced("report", report), fenced("report", changed))
    runs = [run]
    if target == "other-run":
        runs.append(run_text(RUN2, decision=None))
    world.write(runs, records=records, spec=spec_text(neighbours=[P] if link_kind == "neighbour" else []))
    code, output = world.check(capsys)
    if link_kind == "disagreement" and target == "other-report":
        assert code == 0, output  # Judges may compare claims across seats of their own run.
    else:
        assert code == 3, output


def test_duplicate_criterion_numbers_are_not_measured(world: World, capsys: pytest.CaptureFixture[str]) -> None:
    # Criteria 33-34: a later answered basis cannot overwrite the earlier missing claim.
    bad = gid(RUN1, 1, SEATS[0], "C7")
    good = spec_text(basis=(f"`{bad}`", "`decisions.md#Q-1`"))
    world.write([run_text(RUN1)], spec=good)
    assert world.check(capsys)[0] == 1
    world.write([run_text(RUN1)], spec=good.replace("2. When", "1. When"))
    code, out = world.check(capsys)
    assert code == 3 and "criterion" in out.lower(), out


@pytest.mark.parametrize("bad", [None, 1, {}, [None], [{"claims": None}], [{"claims": [None]}]])
def test_malformed_incomplete_disagreements_are_not_measured(
    world: World, capsys: pytest.CaptureFixture[str], bad: object
) -> None:
    # Criterion 33: incomplete evidence is still shape checked before traversing links.
    incomplete = run_text(RUN2, status="incomplete", decision=None)
    world.write([run_text(RUN1), incomplete])
    assert world.check(capsys)[0] == 0
    broken = incomplete.replace('"disagreements": []', '"disagreements": ' + json.dumps(bad))
    assert broken != incomplete
    world.write([run_text(RUN1), broken])
    code, out = world.check(capsys)
    assert code == 3 and "disagreement" in out.lower(), out


@pytest.mark.parametrize("bad", [42, "x", {}, [1], [None], [["a"]]])
def test_malformed_inventory_items_are_not_measured(world: World, capsys, bad: object) -> None:
    # Criterion 33 (F-55): an inventory field of the wrong shape is unmeasured (exit 3), not a traceback.
    run = run_text(RUN1)
    inventory = gate.parse_text(run, "fixture")[0].inventory
    broken = json.loads(json.dumps(inventory))
    broken["items"] = bad
    changed = run.replace(fenced("inventory", inventory), fenced("inventory", broken))
    assert changed != run
    world.write([changed])
    code, out = world.check(capsys)
    assert code == 3, out


@pytest.mark.parametrize("fault", ["double", "judge", "duplicate", "unique", "missing", "count", "wrong-seat"])
def test_contradictory_claim_dispositions_are_not_measured(world: World, capsys, fault) -> None:
    """F-45: persisted scores must be exclusive and agree with the judge."""
    run = run_text(RUN1)
    parsed = gate.parse_text(run, "fixture")[0]
    reconciliation = parsed.reconciliation
    claim = gid(RUN1, 1, SEATS[0], "C1")
    score = next(s for s in reconciliation["scores"] if claim in s["supported"]["claims"])
    if fault == "double":
        score["refuted"] = {"count": 1, "claims": [claim]}
        next(j for j in reconciliation["reconciliation"]["claim_judgements"] if j["claim"] == claim)["disposition"] = (
            "refuted"
        )
    elif fault == "judge":
        next(j for j in reconciliation["reconciliation"]["claim_judgements"] if j["claim"] == claim)["disposition"] = (
            "refuted"
        )
    elif fault == "duplicate":
        score["supported"] = {"count": 2, "claims": [claim, claim]}
    elif fault == "unique":
        score["unique"] = {"count": 1, "claims": [claim]}
    elif fault == "missing":
        score["supported"] = {"count": 0, "claims": []}
    elif fault == "count":
        score["supported"]["count"] = 9
    else:
        score["seat"] = "opencode-go:foreign"
    bad = run.replace(
        fenced("reconciliation", gate.parse_text(run, "fixture")[0].reconciliation),
        fenced("reconciliation", reconciliation),
    )
    assert bad != run
    world.write([bad], spec=spec_text(neighbours=[], basis=(f"`{claim}`",)))
    code, out = world.check(capsys)
    assert code == 3, out
    world.write([run], spec=spec_text(neighbours=[], basis=(f"`{claim}`",)))
    assert world.check(capsys)[0] == 0


@pytest.mark.parametrize(
    "disposition,unique",
    [
        ("supported", False),
        ("supported", True),
        ("refuted", False),
        ("unresolved", False),
        ("off-brief", False),
    ],
)
def test_consistent_judge_and_score_dispositions_remain_measured(world: World, capsys, disposition, unique) -> None:
    run = run_text(RUN1)
    original = gate.parse_text(run, "fixture")[0].reconciliation
    changed = json.loads(json.dumps(original))
    claim = gid(RUN1, 1, SEATS[0], "C1")
    score = next(s for s in changed["scores"] if claim in s["supported"]["claims"])
    score["supported"] = {"count": 0, "claims": []}
    score[disposition] = {"count": 1, "claims": [claim]}
    if unique:
        score["unique"] = {"count": 1, "claims": [claim]}
    verdict = next(j for j in changed["reconciliation"]["claim_judgements"] if j["claim"] == claim)
    verdict.update(disposition=disposition, unique=unique)
    run = run.replace(fenced("reconciliation", original), fenced("reconciliation", changed))
    world.write([run])  # an answered maintainer record supplies the criterion basis
    code, out = world.check(capsys)
    assert code == 0, out


@pytest.mark.parametrize("key", ["? [bad,key]\n: value", "? {bad: key}\n: value"])
def test_unhashable_spec_header_keys_are_not_measured(world: World, capsys, key: str) -> None:
    # Criterion 33: malformed YAML key identities report unreadable evidence rather than crashing.
    good = spec_text()
    world.write([run_text(RUN1)], spec=good)
    assert world.check(capsys)[0] == 0
    world.write([run_text(RUN1)], spec=good.replace("title: Spec", f"title: Spec\n{key}"))
    code, out = world.check(capsys)
    assert code == 3 and "not readable" in out, out


def test_unreadable_spec_is_not_measured(tmp_path: Path) -> None:
    world = World(tmp_path).write([run_text(RUN1)])
    assert gate.run(tmp_path, "demo", out=lambda _: None) == 0
    (world.folder / "spec.md").write_bytes(b"\xff")
    lines = []
    assert gate.run(tmp_path, "demo", out=lines.append) == 3
    assert any("not measured" in line and "spec.md" in line for line in lines)


@pytest.mark.parametrize("linked_repeat", [False, True])
def test_duplicate_question_identity_is_not_measured(world: World, capsys, linked_repeat: bool) -> None:
    first = q_record(1, items=(f"{RUN1}/H-1",), answer="keep the neighbour")
    repeat = q_record(1, answer="drop the neighbour", claims=(gid(RUN1, 1, SEATS[0], "C1"),) if linked_repeat else ())
    world.write([run_text(RUN1)], records=[first])
    assert world.check(capsys)[0] == 0
    world.write([run_text(RUN1)], records=[first, repeat])
    code, out = world.check(capsys)
    assert code == 3, out


@pytest.mark.parametrize("answer", ["# answer pending", "null", "~", "", "   # pending"])
def test_empty_yaml_answer_cannot_close_item_or_supply_basis(world: World, capsys, answer: str) -> None:
    record = q_record(1, items=(f"{RUN1}/H-1",)).replace('answer: "yes"', f"answer: {answer}")
    world.write([run_text(RUN1)], records=[record])
    code, output = world.check(capsys)
    assert code == 1 and f"{RUN1}/H-1" in output
    world.write(
        [run_text(RUN1, decision=None)], records=[record.replace(f"research_items: [{RUN1}/H-1]", "research_items: []")]
    )
    assert world.check(capsys)[0] == 1, "an empty answer supplied a criterion Basis"


@pytest.mark.parametrize("answer", ["[]", "{}", "\n  []", "\n  {}"])
def test_empty_yaml_containers_cannot_close_item_or_supply_basis(world: World, capsys, answer: str) -> None:
    # Empty parsed containers have no maintainer content, despite their nonblank string form.
    record = q_record(1, items=(f"{RUN1}/H-1",)).replace('answer: "yes"', f"answer: {answer}")
    world.write([run_text(RUN1)], records=[record])
    code, output = world.check(capsys)
    assert code == 1 and f"{RUN1}/H-1" in output
    world.write(
        [run_text(RUN1, decision=None)], records=[record.replace(f"research_items: [{RUN1}/H-1]", "research_items: []")]
    )
    assert world.check(capsys)[0] == 1, "an empty container supplied a criterion Basis"


@pytest.mark.parametrize(
    "answer",
    [
        '"null"',
        '"# actual answer"',
        '"Keep this." (maintainer stated)',
        "yes # stated",
        "|\n  Keep this.",
        ">-\n  Keep this.",
    ],
)
def test_real_inline_and_block_answers_still_close_handoff(world: World, capsys, answer: str) -> None:
    record = q_record(1, items=(f"{RUN1}/H-1",)).replace('answer: "yes"', f"answer: {answer}")
    world.write([run_text(RUN1)], records=[record])
    assert world.check(capsys)[0] == 0


@pytest.mark.parametrize(
    "answer",
    [
        "\n  choice: keep\n  choice: drop",
        "{choice: keep, choice: drop}",
        "\n  choices:\n    - {choice: keep, choice: drop}",
    ],
)
@pytest.mark.parametrize("use", ["obligation", "basis", "before-spec"])
def test_duplicate_yaml_answer_keys_are_not_measured(world: World, capsys, answer: str, use: str) -> None:
    record = q_record(1, items=(f"{RUN1}/H-1",))
    # The valid answer closes the item and supplies its criterion Basis first.
    world.write([run_text(RUN1)], records=[record])
    assert world.check(capsys)[0] == 0
    record = record.replace('answer: "yes"', f"answer: {answer}")
    run = run_text(RUN1, decision=None) if use == "basis" else run_text(RUN1)
    if use == "basis":
        record = record.replace(f"research_items: [{RUN1}/H-1]", "research_items: []")
    world.write([run], records=[record], spec=None if use == "before-spec" else "default")
    code, output = world.check(capsys)
    assert code == 3, output
    assert "not measured" in output and "answer" in output and "choice" in output


@pytest.mark.parametrize(
    "heading", ["## Amendment — later criteria", "# Amendment", "## Acceptance criteria — amendment"]
)
def test_amended_criteria_after_main_headings_require_basis(world: World, capsys, heading: str) -> None:
    plain = spec_text(neighbours=[])
    amendment = f"\n## Notes\n\nExplanatory prose.\n\n{heading}\n\n62. When amended, check its origin.\n"
    world.write([run_text(RUN1)], spec=plain + amendment + "   *Basis:* `decisions.md#Q-1`.\n")
    assert world.check(capsys)[0] == 0
    world.write([run_text(RUN1)], spec=plain + amendment)
    code, output = world.check(capsys)
    assert code == 1, output
    assert "62" in output and "basis" in output
    world.write([run_text(RUN1)], spec=plain + amendment + "   *Basis:* `missing-claim`.\n")
    assert world.check(capsys)[0] == 1, "amendment bases must also be resolved"


def test_research_swarm_seat_amendment_has_answered_bases(world: World, capsys) -> None:
    source = Path(__file__).resolve().parents[1] / "plans/changes/research-swarm/spec.md"
    if not source.exists():
        pytest.skip("the framework research spec is not shipped in the kit")
    amendment = (
        "## Amendment — 2026-10-21" + source.read_text(encoding="utf-8").split("## Amendment — 2026-10-21", 1)[1]
    )
    records = [q_record(1, items=(f"{RUN1}/H-1",)), q_record(18)]
    world.write([run_text(RUN1)], records=records, spec=spec_text() + amendment)
    code, output = world.check(capsys)
    assert code == 0, output
    # Removing any one origin must make the real amendment fail the gate.
    for number in range(62, 66):
        before, criterion = amendment.split(f"{number}. ", 1)
        broken = before + f"{number}. " + criterion.replace("   *Basis:* `decisions.md#Q-18`.\n", "", 1)
        world.write([run_text(RUN1)], records=records, spec=spec_text() + broken)
        code, output = world.check(capsys)
        assert code == 1 and str(number) in output, output


@pytest.mark.parametrize(
    "answer",
    [
        "\n  <<: {source: maintainer}\n  choice: keep\n  choice: drop",
        "{<<: {source: maintainer}, choice: keep, choice: drop}",
        "{? [unhashable, key]: keep}",
        "[keep",
        "{choice: keep",
        "!unknown keep",
        '"unterminated',
        "Keep this: because: approved",
    ],
)
@pytest.mark.parametrize("use", ["obligation", "basis", "before-spec"])
def test_yaml_answer_errors_are_not_measured(world: World, capsys, answer: str, use: str) -> None:
    record = q_record(1, items=(f"{RUN1}/H-1",))
    world.write([run_text(RUN1)], records=[record])
    assert world.check(capsys)[0] == 0
    record = record.replace('answer: "yes"', f"answer: {answer}")
    run = run_text(RUN1, decision=None) if use == "basis" else run_text(RUN1)
    if use == "basis":
        record = record.replace(f"research_items: [{RUN1}/H-1]", "research_items: []")
    world.write([run], records=[record], spec=None if use == "before-spec" else "default")
    code, output = world.check(capsys)
    assert code == 3, output
    assert "not measured" in output and "answer" in output
