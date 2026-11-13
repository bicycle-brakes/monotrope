"""The declared local kit-probe condition, end to end — reader, runner, history, transfer.

A schema-4 gate may declare `local_when`; the local runner then executes only
the gates whose measured change actually touches a declared trigger, while
`--ci` and the hosted workflow stay unconditional. Every case here builds its
own throwaway git repository, copies the real mechanism into it (the same
files the kit manifest classifies `mechanismus`), and runs the real reader or
the real runner against synthetic marker commands — never the entire
expensive probe, and never this checkout's own state. Each docstring names
the fault it was written against; planting it turned exactly this test red.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(1, str(REPO_ROOT / "scripts" / "kit"))
import ci_gates  # noqa: E402
import probe  # noqa: E402
import stage2  # noqa: E402
import verify_duration  # noqa: E402
import verify_lock  # noqa: E402

# The mechanism files a recipient of the kit needs for this mechanism — every
# one classified `mechanismus` by the real manifest, so the transfer below
# assembles itself from manifest-selected files only.
TRANSFER_FILES = (
    "scripts/ci_gates.py",
    "scripts/verify_all.sh",
    "scripts/verify_lock.py",
    "scripts/verify_duration.py",
    "scripts/_verdict.py",
    "scripts/kit/probe.py",
    "scripts/kit/manifest.yaml",
)

# The synthetic mini manifest of the throwaway tree: a travelling mechanism
# (`scripts/`, `decisions/`, `werk/`), an inventory (`rest/`), and `neu/`
# deliberately unclassified until a test makes it newly travelling.
MANIFEST_TEXT = """\
schema_version: 1
geruest_ordner: []
rollen:
  mechanismus:
    was: "traegt den synthetischen Ablauf"
  bestand:
    was: "Inventur des synthetischen Repos"
rules:
  - prefix: scripts/
    rolle: mechanismus
    reason: the synthetic runner mechanism
  - prefix: decisions/
    rolle: mechanismus
    reason: the synthetic gate list
  - prefix: werk/
    rolle: mechanismus
    reason: the synthetic travelling set
  - prefix: rest/
    rolle: bestand
    reason: the synthetic inventory
"""

VOLLE_DEKLARATION = {
    "paths": ["scripts/kit/manifest.yaml", "scripts/kit/probe.py"],
    "kit_manifest": "scripts/kit/manifest.yaml",
    "membership": True,
}


# ---------------------------------------------------------------------------
# The throwaway tree: real mechanism, synthetic kit, one seed commit
# ---------------------------------------------------------------------------


def _git(baum: Path, *args: str) -> str:
    """One git answer of the throwaway tree; a failing git fails the test loudly."""
    done = subprocess.run(["git", "-C", str(baum), *args], capture_output=True, text=True, check=True)
    return done.stdout


def _gate(
    baum: Path,
    gid: str,
    *,
    dekl: dict[str, Any] | None = None,
    cost: str = "seconds",
    ending: str = "true",
) -> dict[str, Any]:
    """One synthetic gate: a marker command, an optional `local_when` declaration."""
    entry: dict[str, Any] = {
        "id": gid,
        "title": f"The synthetic {gid}",
        "command": f"touch '{baum / (gid + '.ran')}'; echo {gid} >> '{baum / 'order.txt'}'; {ending}",
        "job": "verify",
        "enforcement": "block",
        "floor": True,
        "placement": "both",
        "cost": cost,
        "reason": f"synthetic {gid} of the condition matrix",
    }
    if dekl is not None:
        entry["local_when"] = dekl
    return entry


def _standard_gates(baum: Path) -> list[dict[str, Any]]:
    """The default synthetic job: a cheap gate, the declared probe, another minutes gate."""
    return [
        _gate(baum, "aa-vor"),
        _gate(baum, "zz-leerprobe", dekl=dict(VOLLE_DEKLARATION), cost="minutes"),
        _gate(baum, "mm-nach", cost="minutes"),
    ]


def _schreibe_gate_datei(baum: Path, gates: list[dict[str, Any]]) -> None:
    """The synthetic schema-4 gate list of the throwaway tree."""
    dokument = {"schema_version": 4, "tools": {"python": ["3.12"]}, "gates": gates}
    (baum / "decisions" / "gates.yaml").write_text(json.dumps(dokument, indent=2) + "\n", encoding="utf-8")


def _baum(
    basis: Path,
    *,
    gate_bauer: Any = None,
    manifest: str = MANIFEST_TEXT,
) -> Path:
    """A throwaway git tree: transferred mechanism, mini kit, one seed commit, origin/main."""
    baum = basis / "baum"
    (baum / "scripts" / "kit").mkdir(parents=True)
    (baum / "decisions").mkdir()
    (baum / "werk").mkdir()
    (baum / "rest").mkdir()
    (baum / "neu").mkdir()
    for pfad in TRANSFER_FILES:
        shutil.copy(REPO_ROOT / pfad, baum / pfad)
    (baum / "scripts" / "kit" / "manifest.yaml").write_text(manifest, encoding="utf-8")
    (baum / "werk" / "probe.txt").write_text("travelling seed\n", encoding="utf-8")
    (baum / "rest" / "notiz.txt").write_text("inventory seed\n", encoding="utf-8")
    (baum / "neu" / "datei.txt").write_text("unclassified seed\n", encoding="utf-8")
    (baum / ".gitignore").write_text("rauschen/\n", encoding="utf-8")
    liste = gate_bauer(baum) if gate_bauer is not None else _standard_gates(baum)
    _schreibe_gate_datei(baum, liste)
    _git(baum, "init", "-b", "main")
    _git(baum, "add", "-A")
    _git(baum, "-c", "user.email=bedingung@invalid", "-c", "user.name=bedingung", "commit", "-q", "-m", "seed")
    _git(baum, "update-ref", "refs/remotes/origin/main", "HEAD")
    return baum


def _verzweige(baum: Path) -> None:
    """A named feature branch: the reader then compares against the merge base."""
    _git(baum, "checkout", "-q", "-b", "arbeit")


def _entscheidungen(baum: Path, umgebung: dict[str, str] | None = None) -> dict[str, tuple[str, str, str]]:
    """The reader's five-field decisions of the tree: id → (decision, reason, enforcement)."""
    done = subprocess.run(
        [
            sys.executable,
            str(baum / "scripts" / "ci_gates.py"),
            "--commands",
            "--job",
            "verify",
            "--placement",
            "lokal",
            "--tsv",
            "--with-local-decisions",
        ],
        cwd=baum,
        capture_output=True,
        text=True,
        check=True,
        env=umgebung,
    )
    out: dict[str, tuple[str, str, str]] = {}
    for zeile in done.stdout.splitlines():
        felder = zeile.split("\t")
        assert len(felder) == 5, f"a decision row broke into {len(felder)} fields: {zeile!r}"
        out[felder[0]] = (felder[2], felder[3], felder[1])
    return out


def _lauf_laeufer(baum: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """The real runner inside the throwaway tree, with a scrubbed environment."""
    zuhause = baum.parent / "home"
    zuhause.mkdir(exist_ok=True)
    umgebung = {
        "HOME": str(zuhause),
        "PATH": "/usr/bin:/bin:/sbin:/usr/sbin",
        "XDG_STATE_HOME": str(baum.parent / "state"),
        verify_lock.FLOOR_ENV: "0",
        "PYTHON": sys.executable,
    }
    bash = shutil.which("bash") or "/bin/bash"
    return subprocess.run(
        [bash, str(baum / "scripts" / "verify_all.sh"), *args],
        cwd=baum,
        env=umgebung,
        capture_output=True,
        text=True,
    )


def _baum_geschichte(baum: Path) -> list[dict]:
    """The duration history the tree's runner recorded."""
    path = baum.parent / "state" / "coding-harness" / verify_duration.HISTORY_NAME
    return [json.loads(zeile) for zeile in path.read_text(encoding="utf-8").splitlines() if zeile.strip()]


def _index_only_aenderung(baum: Path, pfad: str) -> None:
    """Stage an edit and restore the working copy to the base: the change lives in the index only."""
    (baum / pfad).write_text("geaendert in der Staging-Area\n", encoding="utf-8")
    _git(baum, "add", pfad)
    basis_bytes = subprocess.run(
        ["git", "-C", str(baum), "show", f"HEAD:{pfad}"], capture_output=True, check=True
    ).stdout
    (baum / pfad).write_bytes(basis_bytes)
    status = _git(baum, "status", "--porcelain", pfad)
    assert status.startswith("MM"), f"the scenario is not index-only: {status!r}"


# ---------------------------------------------------------------------------
# Ledger 2 — a travelling edit in any measured state runs the probe
# ---------------------------------------------------------------------------


def test_manifest_changes_and_travelling_edits_run_probe(tmp_path: Path) -> None:
    """A committed, staged, unstaged or mode-only travelling edit runs the probe — and a new manifest rule joins the triggers.

    Planted faults: one of the four measured states missed (so a committed or
    staged kit edit was mistaken for an unchanged kit), or the classifier
    copied instead of loaded, so a newly travelling prefix never triggered.
    """
    basis = tmp_path / "reisend"
    dekl = dict(VOLLE_DEKLARATION)

    # Committed travelling edit on a feature branch.
    baum = _baum(
        basis / "committed",
        gate_bauer=lambda b: [
            _gate(b, "aa-vor"),
            _gate(b, "zz", dekl=dekl, cost="minutes"),
        ],
    )
    _verzweige(baum)
    (baum / "werk" / "probe.txt").write_text("committed geaendert\n", encoding="utf-8")
    _git(baum, "add", "-A")
    _git(baum, "-c", "user.email=bedingung@invalid", "-c", "user.name=bedingung", "commit", "-q", "-m", "reise")
    entscheidungen = _entscheidungen(baum)
    assert entscheidungen["aa-vor"][0] == "run"
    entscheidung, grund, _ = entscheidungen["zz"]
    assert entscheidung == "run"
    assert "werk/probe.txt" in grund and "kit manifest scripts/kit/manifest.yaml" in grund, grund
    assert "merge-base with origin/main" in grund, grund

    # Index-only travelling edit: staged, working copy restored to the base.
    baum = _baum(basis / "index", gate_bauer=lambda b: [_gate(b, "aa-vor"), _gate(b, "zz", dekl=dekl, cost="minutes")])
    _verzweige(baum)
    _index_only_aenderung(baum, "werk/probe.txt")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "a staged kit edit vanished behind its restored working copy"
    assert "werk/probe.txt" in grund, grund

    # Unstaged travelling edit and a mode-only edit.
    baum = _baum(
        basis / "unstaged",
        gate_bauer=lambda b: [
            _gate(b, "aa-vor"),
            _gate(b, "zz", dekl=dekl, cost="minutes"),
        ],
    )
    _verzweige(baum)
    (baum / "werk" / "probe.txt").write_text("unstaged geaendert\n", encoding="utf-8")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run"
    assert "werk/probe.txt" in grund, grund
    (baum / "werk" / "probe.txt").chmod(0o755)
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "a mode-only travelling edit was not measured"
    assert "werk/probe.txt" in grund, grund

    # A manifest edit that makes `neu/` newly travelling: the declaration names
    # only the kit manifest, so the trigger can only come from the loaded
    # classifier — and the reason names the newly travelling file first.
    baum = _baum(
        basis / "neu-reisend",
        gate_bauer=lambda b: [
            _gate(b, "aa-vor"),
            _gate(b, "zz", dekl={"kit_manifest": "scripts/kit/manifest.yaml"}, cost="minutes"),
        ],
    )
    _verzweige(baum)
    text = (baum / "scripts" / "kit" / "manifest.yaml").read_text(encoding="utf-8")
    (baum / "scripts" / "kit" / "manifest.yaml").write_text(
        text + "  - prefix: neu/\n    rolle: mechanismus\n    reason: a newly travelling prefix\n",
        encoding="utf-8",
    )
    (baum / "neu" / "datei.txt").write_text("jetzt reisend\n", encoding="utf-8")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "the newly travelling prefix never joined the triggers"
    assert grund.startswith("run: neu/datei.txt travels per kit manifest"), grund


# ---------------------------------------------------------------------------
# Ledger 3 — membership changes run the probe
# ---------------------------------------------------------------------------


def test_membership_changes_always_run_probe(tmp_path: Path) -> None:
    """Any added, removed, renamed or untracked path runs the probe, whatever its kit role.

    Planted faults: an addition or removal read as a content change, a rename
    silently folded away by rename detection, or a nonignored untracked file
    excluded from the measured change.
    """
    basis = tmp_path / "mitgliedschaft"
    dekl = dict(VOLLE_DEKLARATION)

    # A nonignored untracked file, wherever it stands.
    baum = _baum(basis / "unversioniert", gate_bauer=lambda b: [_gate(b, "zz", dekl=dekl, cost="minutes")])
    _verzweige(baum)
    (baum / "rest" / "unversioniert.txt").write_text("neu und nicht ignoriert\n", encoding="utf-8")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "an untracked file allowed a conditional skip"
    assert "membership change added rest/unversioniert.txt" in grund, grund

    # A staged addition.
    baum = _baum(basis / "staged", gate_bauer=lambda b: [_gate(b, "zz", dekl=dekl, cost="minutes")])
    _verzweige(baum)
    (baum / "rest" / "staged.txt").write_text("in der Staging-Area\n", encoding="utf-8")
    _git(baum, "add", "rest/staged.txt")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run"
    assert "membership change added rest/staged.txt" in grund, grund

    # A committed addition and a committed removal.
    baum = _baum(basis / "committed", gate_bauer=lambda b: [_gate(b, "zz", dekl=dekl, cost="minutes")])
    _verzweige(baum)
    (baum / "rest" / "dazu.txt").write_text("committet\n", encoding="utf-8")
    _git(baum, "add", "-A")
    _git(baum, "-c", "user.email=bedingung@invalid", "-c", "user.name=bedingung", "commit", "-q", "-m", "dazu")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run"
    assert "membership change added rest/dazu.txt" in grund, grund

    baum = _baum(basis / "entfernt", gate_bauer=lambda b: [_gate(b, "zz", dekl=dekl, cost="minutes")])
    _verzweige(baum)
    _git(baum, "rm", "-q", "rest/notiz.txt")
    _git(baum, "-c", "user.email=bedingung@invalid", "-c", "user.name=bedingung", "commit", "-q", "-m", "weg")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "a committed removal allowed a conditional skip"
    assert "membership change removed rest/notiz.txt" in grund, grund

    # A rename arrives as a removal and an addition — rename detection stays off.
    baum = _baum(basis / "umbenannt", gate_bauer=lambda b: [_gate(b, "zz", dekl=dekl, cost="minutes")])
    _verzweige(baum)
    _git(baum, "mv", "werk/probe.txt", "werk/um_benannt.txt")
    _git(baum, "-c", "user.email=bedingung@invalid", "-c", "user.name=bedingung", "commit", "-q", "-m", "neu genannt")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "a rename allowed a conditional skip"
    assert "membership change removed werk/probe.txt" in grund, grund


# ---------------------------------------------------------------------------
# Ledger 4 — measured absence skips the probe
# ---------------------------------------------------------------------------


def test_only_nontravelling_content_or_no_changes_skip_probe(tmp_path: Path) -> None:
    """A content-only edit to inventory, an empty change and ignored noise skip the expensive gate.

    Planted faults: a `bestand` edit launching the throwaway tests, an empty
    measured change launching them, or an ignored file counting as a change.
    """
    basis = tmp_path / "vergessen"
    dekl = dict(VOLLE_DEKLARATION)
    baum = _baum(
        basis / "baum",
        gate_bauer=lambda b: [
            _gate(b, "aa-vor"),
            _gate(b, "zz", dekl=dekl, cost="minutes"),
            _gate(b, "mm-nach", cost="minutes"),
        ],
    )
    _verzweige(baum)

    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "skip", "an empty measured change launched the probe"
    assert grund.startswith("skip:") and "merge-base with origin/main" in grund, grund

    (baum / "rest" / "notiz.txt").write_text("nur Inventur geaendert\n", encoding="utf-8")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "skip", "a content-only `bestand` edit launched the probe"
    assert "merge-base with origin/main" in grund, grund

    (baum / "rauschen").mkdir()
    (baum / "rauschen" / "x.txt").write_text("ignored\n", encoding="utf-8")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "skip", "an ignored file counted as a change"

    # The runner executes the skip: the expensive marker never appears, the
    # final wording acknowledges the declared skip.
    ergebnis = _lauf_laeufer(baum)
    assert ergebnis.returncode == 0, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"
    assert "VERIFY GREEN" in ergebnis.stdout
    assert "1 declared local skip" in ergebnis.stdout
    assert not (baum / "zz-leerprobe.ran").exists(), "the skipped gate ran its command"
    assert (baum / "aa-vor.ran").exists() and (baum / "mm-nach.ran").exists()
    assert (baum / "order.txt").read_text(encoding="utf-8") == "aa-vor\nmm-nach\n"


# ---------------------------------------------------------------------------
# Ledger 5 — an indeterminate comparison never skips
# ---------------------------------------------------------------------------


def test_indeterminate_comparison_runs_probe(tmp_path: Path) -> None:
    """Missing history, a broken git, a detached checkout or a bad manifest all run the probe.

    Planted faults: any of these read as an empty measured change — the
    fail-closed direction is the whole point of the condition.
    """
    basis = tmp_path / "unbestimmt"
    dekl = dict(VOLLE_DEKLARATION)

    # A detached checkout: no branch to compare against.
    baum = _baum(basis / "detached", gate_bauer=lambda b: [_gate(b, "zz", dekl=dekl, cost="minutes")])
    _verzweige(baum)
    _git(baum, "checkout", "-q", "--detach")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "a detached checkout was read as an empty change"
    assert "detached HEAD" in grund, grund

    # Missing origin/main: no merge base, no comparison.
    baum = _baum(basis / "ohne-basis", gate_bauer=lambda b: [_gate(b, "zz", dekl=dekl, cost="minutes")])
    _verzweige(baum)
    _git(baum, "update-ref", "-d", "refs/remotes/origin/main")
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "a missing merge base was read as an empty change"
    assert "no merge base with origin/main" in grund, grund

    # `main` at its root commit: no first parent.
    baum = _baum(basis / "wurzel", gate_bauer=lambda b: [_gate(b, "zz", dekl=dekl, cost="minutes")])
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "a root commit was read as an empty change"
    assert "no first parent" in grund, grund

    # Git itself broken: a `git` shim on PATH that always fails.
    baum = _baum(basis / "kaputtes-git", gate_bauer=lambda b: [_gate(b, "zz", dekl=dekl, cost="minutes")])
    shim = basis / "shim"
    shim.mkdir()
    (shim / "git").write_text("#!/bin/sh\nexit 97\n", encoding="utf-8")
    (shim / "git").chmod(0o755)
    umgebung = {**os.environ, "PATH": f"{shim}:{os.environ.get('PATH', '')}"}
    entscheidung, grund, _ = _entscheidungen(baum, umgebung)["zz"]
    assert entscheidung == "run", "a failing git was read as an empty change"
    assert "comparison indeterminate" in grund, grund

    # A committed malformed manifest: the kit classifier cannot answer, so the
    # manifest condition is indeterminate. The valid control tree skips.

    def nur_manifest(b: Path) -> list[dict[str, Any]]:
        """The declared gate names only the kit manifest — every trigger flows through the classifier."""
        return [_gate(b, "zz", dekl={"kit_manifest": "scripts/kit/manifest.yaml"}, cost="minutes")]

    baum = _baum(basis / "manifest-kaputt", gate_bauer=nur_manifest, manifest="rules: [\n")
    _verzweige(baum)
    entscheidung, grund, _ = _entscheidungen(baum)["zz"]
    assert entscheidung == "run", "a malformed manifest was read as an empty travelling set"
    assert "cannot be read" in grund, grund
    kontrolle = _baum(basis / "manifest-ok", gate_bauer=nur_manifest)
    _verzweige(kontrolle)
    entscheidung, grund, _ = _entscheidungen(kontrolle)["zz"]
    assert entscheidung == "skip", "the valid control tree did not skip — the comparison itself broke"
    assert grund.startswith("skip:"), grund


# ---------------------------------------------------------------------------
# Ledger 6 — the schema refuses invalid declarations
# ---------------------------------------------------------------------------


def _liste(gates: list[dict[str, Any]], *, schema_version: int = 4) -> dict[str, Any]:
    """A synthetic gate document for the schema proofs."""
    return {"schema_version": schema_version, "tools": {"python": ["3.12"]}, "gates": gates}


def _basis_gate(**ueber: Any) -> dict[str, Any]:
    """One otherwise-valid command gate with a full, valid declaration."""
    gate: dict[str, Any] = {
        "id": "bedingt",
        "title": "A conditional gate",
        "command": "true",
        "job": "verify",
        "enforcement": "block",
        "floor": True,
        "placement": "both",
        "cost": "seconds",
        "reason": "seed of the declaration proofs",
        "local_when": dict(VOLLE_DEKLARATION),
    }
    gate.update(ueber)
    return gate


def test_local_condition_schema_rejects_invalid_declarations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Empty, mistyped, escaping or unsupported declarations fail the schema — independently of other faults.

    Planted faults: an empty declaration, an unknown trigger, a path text where
    a list belongs, empty or absolute or escaping or duplicated or backslashed
    paths, a non-boolean membership, a declaration on an action or a
    hosted-only gate, or a schema-3 list carrying the field the old reader
    would silently ignore.
    """
    assert ci_gates.validate_schema(_liste([_basis_gate()])) == [], "the valid control failed"
    for nur in ({"membership": True}, {"paths": ["rest/"]}):
        assert ci_gates.validate_schema(_liste([{**_basis_gate(), "local_when": nur}])) == [], nur

    faelle = [
        _liste([{**_basis_gate(), "local_when": {}}]),
        _liste([{**_basis_gate(), "local_when": {"wenn": True}}]),
        _liste([{**_basis_gate(), "local_when": {"paths": "werk/"}}]),
        _liste([{**_basis_gate(), "local_when": {"paths": []}}]),
        _liste([{**_basis_gate(), "local_when": {"paths": [""]}}]),
        _liste([{**_basis_gate(), "local_when": {"paths": ["/absoluut"]}}]),
        _liste([{**_basis_gate(), "local_when": {"paths": ["a/../b"]}}]),
        _liste([{**_basis_gate(), "local_when": {"paths": ["back\\slash"]}}]),
        _liste([{**_basis_gate(), "local_when": {"paths": [42]}}]),
        _liste([{**_basis_gate(), "local_when": {"paths": ["werk/", "werk/"]}}]),
        _liste([{**_basis_gate(), "local_when": {"kit_manifest": "/etc/passwd"}}]),
        _liste([{**_basis_gate(), "local_when": {"kit_manifest": 7}}]),
        _liste([{**_basis_gate(), "local_when": {"membership": False}}]),
        _liste([{**_basis_gate(), "local_when": {"membership": "yes"}}]),
        _liste([{**_basis_gate(), "local_when": "werk/"}]),
        _liste([{**_basis_gate(), "placement": "hosted"}]),
    ]
    for dokument in faelle:
        fehler = ci_gates.validate_schema(dokument)
        assert fehler, dokument
        assert any("local_when" in f for f in fehler), (dokument, fehler)

    aktion = {k: v for k, v in _basis_gate().items() if k != "command"}
    aktion["action"] = "acme/probe-action@v1"
    aktion["placement"] = "hosted"
    fehler = ci_gates.validate_schema(_liste([aktion]))
    assert any("an action has no local condition" in f for f in fehler), fehler

    schema_drei = _liste([_basis_gate()], schema_version=3)
    fehler = ci_gates.validate_schema(schema_drei)
    assert any("schema_version 4" in f for f in fehler), fehler

    # The command line refuses it too, not only the function.
    schlecht = tmp_path / "gates.yaml"
    schlecht.write_text(json.dumps(faelle[0], indent=2) + "\n", encoding="utf-8")
    monkeypatch.setattr(ci_gates, "GATE_FILE", schlecht)
    monkeypatch.setattr(sys, "argv", ["ci_gates.py", "--check-schema"])
    assert ci_gates.main() != 0
    gesehen = capsys.readouterr()
    assert "local_when" in gesehen.out + gesehen.err


# ---------------------------------------------------------------------------
# Ledger 6 — the declaration, not the gate id, decides
# ---------------------------------------------------------------------------


def test_condition_comes_from_declaration_for_any_gate_id(tmp_path: Path) -> None:
    """Renaming the gate changes nothing; an undeclared gate runs even under a probe-like name.

    Planted faults: the reader branching on a gate id (only the one declared
    gate would behave conditionally), or an unconditional gate with a
    suggestive name going quiet.
    """
    basis = tmp_path / "benennung"

    def liste_mit(baum: Path, bedingt_id: str) -> list[dict[str, Any]]:
        """The synthetic job under one arbitrary conditional gate id."""
        return [
            _gate(baum, "aa-vor"),
            _gate(baum, bedingt_id, dekl={"paths": ["rest/"]}, cost="minutes"),
            _gate(baum, "zz-leerprobe", cost="seconds"),
        ]

    erstes = _baum(basis / "erstes", gate_bauer=lambda b: liste_mit(b, "tor-westlich"))
    zweites = _baum(basis / "zweites", gate_bauer=lambda b: liste_mit(b, "tor-ostlich"))
    _verzweige(erstes)
    _verzweige(zweites)

    for baum, bedingt_id in ((erstes, "tor-westlich"), (zweites, "tor-ostlich")):
        entscheidungen = _entscheidungen(baum)
        entscheidung, grund, _ = entscheidungen[bedingt_id]
        assert entscheidung == "skip", "the conditional gate ran on an empty change"
        assert grund.startswith("skip:") and "paths rest/" in grund, grund
        entscheidung, grund, _ = entscheidungen["zz-leerprobe"]
        assert entscheidung == "run", "an undeclared gate went quiet under a probe-like name"
        assert grund == "unconditional — no local condition declared", grund

    for baum in (erstes, zweites):
        (baum / "rest" / "notiz.txt").write_text("trifft die deklarierte Kartei\n", encoding="utf-8")
    erste = _entscheidungen(erstes)["tor-westlich"]
    zweite = _entscheidungen(zweites)["tor-ostlich"]
    # The equal measured state is read on the decision, the enforcement and
    # the named trigger — never on the whole reason, whose comparison base is
    # each checkout's own sha and legitimately differs between the two trees.
    assert erste[0] == zweite[0] == "run", "a renamed gate decided differently on the same measured state"
    assert erste[2] == zweite[2], (erste, zweite)
    assert "rest/notiz.txt" in erste[1] and "rest/notiz.txt" in zweite[1], (erste, zweite)


# ---------------------------------------------------------------------------
# Ledger 7 — hosted and --ci stay unconditional
# ---------------------------------------------------------------------------


def test_hosted_and_ci_mode_ignore_local_conditions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """`--ci` executes the declared gate on a clean tree, and the generated workflow knows no condition.

    Planted faults: a no-kit-change input removing or bypassing the probe on a
    `--ci` run or in `ci.yml`, or a legacy direct command list turning
    conditional.
    """
    baum = _baum(tmp_path / "gehostet")
    _verzweige(baum)

    # `--ci` on a tree whose local decision would be a skip: the gate runs.
    ergebnis = _lauf_laeufer(baum, "--ci")
    assert ergebnis.returncode == 0, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"
    assert (baum / "zz-leerprobe.ran").exists(), "--ci bypassed a declared gate on a clean tree"
    assert "── [zz-leerprobe] gruen" in ergebnis.stdout
    assert "skipped" not in ergebnis.stdout

    # The generated workflow carries the command and no local condition.
    monkeypatch.setattr(ci_gates, "GATE_FILE", baum / "decisions" / "gates.yaml")
    text = ci_gates.generate_ci()
    assert "touch" in text and "zz-leerprobe" in text
    assert "local_when" not in text, "the generated workflow leaked the local declaration"
    assert text.count("if: ${{ !cancelled() }}") >= 2

    # The legacy three-column command list stays unconditional.
    done = subprocess.run(
        [
            sys.executable,
            str(baum / "scripts" / "ci_gates.py"),
            "--commands",
            "--job",
            "verify",
            "--placement",
            "lokal",
            "--tsv",
        ],
        cwd=baum,
        capture_output=True,
        text=True,
        check=True,
    )
    zeilen = [z.split("\t") for z in done.stdout.splitlines()]
    assert all(len(felder) == 3 for felder in zeilen), zeilen
    assert any(felder[0] == "zz-leerprobe" for felder in zeilen), zeilen

    # Incompatible combinations are refused, not silently degraded.
    basis_flaggen = ["--commands", "--job", "verify", "--tsv"]
    for flaggen in (
        ["--with-local-decisions"],
        [*basis_flaggen, "--placement", "ci", "--with-local-decisions"],
        [*basis_flaggen, "--placement", "lokal", "--format", "json", "--with-local-decisions"],
        [*basis_flaggen, "--placement", "lokal", "--skip-equivalents", "--with-local-decisions"],
    ):
        schlecht = subprocess.run(
            [sys.executable, str(baum / "scripts" / "ci_gates.py"), *flaggen],
            cwd=baum,
            capture_output=True,
            text=True,
        )
        assert schlecht.returncode != 0, flaggen
        assert "with-local-decisions" in schlecht.stderr, (flaggen, schlecht.stderr)


# ---------------------------------------------------------------------------
# Ledger 9 — the skip is visible evidence, never a pass
# ---------------------------------------------------------------------------


def test_skip_output_and_history_name_reason_without_pass(tmp_path: Path) -> None:
    """The skip names its measured reason in output and history — no gate frame, no exit, no seconds.

    Planted faults: a missing skip line or base, a fabricated exit status or
    test duration, a skip parsed as a green gate section, or a history report
    counting the skip as an executed gate.
    """
    baum = _baum(tmp_path / "hinweis")
    _verzweige(baum)
    ergebnis = _lauf_laeufer(baum)
    assert ergebnis.returncode == 0, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"

    skip_zeile = next(
        (z for z in ergebnis.stdout.splitlines() if "] skipped — skip:" in z),
        "",
    )
    assert skip_zeile, ergebnis.stdout
    assert re.search(r"^──   \[zz-leerprobe\] skipped — ", skip_zeile), skip_zeile
    assert re.search(r"merge-base with origin/main [0-9a-f]{12}", skip_zeile), skip_zeile
    assert "── [zz-leerprobe] $ " not in ergebnis.stdout, "the skipped gate printed a command frame"
    assert "── [zz-leerprobe] gruen" not in ergebnis.stdout, "the skip posed as a green gate"
    assert "VERIFY GREEN" in ergebnis.stdout and "1 declared local skip" in ergebnis.stdout
    assert stage2.red_sections(ergebnis.stdout) is None, ergebnis.stdout
    assert stage2.GATE_START.match(skip_zeile) is None, "the skip line parsed as a gate frame"
    assert stage2.GATE_END.match(skip_zeile) is None, "the skip line parsed as a gate verdict"

    geschichte = _baum_geschichte(baum)
    skips = [e for e in geschichte if e["event"] == "gate_skip"]
    assert len(skips) == 1, geschichte
    assert skips[0]["gate"] == "zz-leerprobe" and skips[0]["enforcement"] == "block"
    assert "merge-base with origin/main" in skips[0]["reason"]
    assert "seconds" not in skips[0] and "exit" not in skips[0], skips[0]
    gemessen = [e["gate"] for e in geschichte if e["event"] == "gate"]
    assert gemessen == ["aa-vor", "mm-nach"], gemessen
    ende = [e for e in geschichte if e["event"] == "run_end"]
    assert len(ende) == 1 and ende[0]["verdict"] == "green"

    # The reader reports the skip separately and counts it as no execution.
    umgebung = {**os.environ, "XDG_STATE_HOME": str(baum.parent / "state")}
    gelesen = subprocess.run(
        [sys.executable, "-m", "scripts.verify_duration", "report"],
        cwd=baum,
        env=umgebung,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "2 gates · 1 skipped" in gelesen.stdout, gelesen.stdout
    assert "skipped: zz-leerprobe" in gelesen.stdout, gelesen.stdout


# ---------------------------------------------------------------------------
# Ledger 11 — the transferred kit decides with the recipient's own files
# ---------------------------------------------------------------------------


def test_transferred_kit_uses_recipient_manifest_and_condition(tmp_path: Path) -> None:
    """A recipient assembled from manifest-selected mechanism files skips and triggers by its own manifest.

    Planted faults: an import from the source checkout, a renamed recipient
    gate losing the declared condition, or a second trigger list travelling
    with the mechanism.
    """
    for pfad in TRANSFER_FILES:
        regel = probe.rolle(pfad)
        assert regel is not None and regel[0] == "mechanismus", f"{pfad} does not travel: {regel}"

    empfang_manifest = MANIFEST_TEXT + (
        "  - prefix: empfang/\n    rolle: mechanismus\n    reason: the recipient's own travelling set\n"
    )
    baum = _baum(
        tmp_path / "empfaenger",
        manifest=empfang_manifest,
        gate_bauer=lambda b: [
            _gate(b, "p-tuer"),
            _gate(
                b,
                "p-leer",
                dekl={
                    "paths": ["scripts/kit/probe.py"],
                    "kit_manifest": "scripts/kit/manifest.yaml",
                    "membership": True,
                },
                cost="minutes",
            ),
        ],
    )
    _verzweige(baum)
    (baum / "empfang").mkdir()
    (baum / "empfang" / "datei.txt").write_text("recipient inventory\n", encoding="utf-8")
    _git(baum, "add", "-A")
    _git(baum, "-c", "user.email=bedingung@invalid", "-c", "user.name=bedingung", "commit", "-q", "-m", "empfang")
    _git(baum, "update-ref", "refs/remotes/origin/main", "HEAD")
    kopf = _git(baum, "rev-parse", "HEAD")[:12]

    # Scrubbed environment: nothing from the source checkout answers.
    arm = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": str(baum.parent / "home")}
    entscheidung, grund, _ = _entscheidungen(baum, arm)["p-leer"]
    assert entscheidung == "skip", "the recipient ran its declared gate on a clean tree"
    assert kopf in grund and "merge-base with origin/main" in grund, grund

    (baum / "empfang" / "datei.txt").write_text("jetzt reisend im Empfang\n", encoding="utf-8")
    entscheidung, grund, _ = _entscheidungen(baum, arm)["p-leer"]
    assert entscheidung == "run", "the recipient's own travelling set never triggered"
    assert grund.startswith("run: empfang/datei.txt travels per kit manifest"), grund
    (baum / "empfang" / "datei.txt").write_text("recipient inventory\n", encoding="utf-8")

    # And the runner of the recipient executes exactly that, with its own state.
    ergebnis = _lauf_laeufer(baum)
    alles = ergebnis.stdout + ergebnis.stderr
    assert ergebnis.returncode == 0, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"
    assert "──   [p-leer] skipped — " in ergebnis.stdout, ergebnis.stdout
    assert not (baum / "p-leer.ran").exists()
    assert "VERIFY GREEN" in ergebnis.stdout and "1 declared local skip" in ergebnis.stdout
    assert str(REPO_ROOT) not in alles, "the recipient answered from the source checkout"
    skips = [e for e in _baum_geschichte(baum) if e["event"] == "gate_skip"]
    assert len(skips) == 1 and skips[0]["gate"] == "p-leer", _baum_geschichte(baum)


# ---------------------------------------------------------------------------
# Ledger 12 — the runner's other contracts survive the skip branch
# ---------------------------------------------------------------------------


def test_skip_preserves_early_stop_parser_and_storage_failure_contracts(tmp_path: Path) -> None:
    """A not-reached gate gains no skip event, a skip parses as no gate frame, broken storage warns without changing verdicts.

    Planted faults: a gate after a blocking failure acquiring a
    conditional-skip event, an unreached gate appearing as a parsed red
    section, or broken history changing the verification verdict instead of
    warning that evidence was not recorded.
    """
    basis = tmp_path / "vertraege"

    # A cheap red gate stops the run before the declared gate: the declared
    # gate is not reached, so it gets only the not-run summary — no skip.

    def rot_liste(b: Path) -> list[dict[str, Any]]:
        """A red seconds gate, then the declared probe, then another minutes gate."""
        return [
            _gate(b, "aa-rot", ending="echo block-rot-diagnostik; exit 1"),
            _gate(b, "zz-leerprobe", dekl=dict(VOLLE_DEKLARATION), cost="minutes"),
            _gate(b, "mm-nach", cost="minutes"),
        ]

    baum = _baum(basis / "stopp", gate_bauer=rot_liste)
    _verzweige(baum)
    ergebnis = _lauf_laeufer(baum)
    assert ergebnis.returncode == 1, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"
    assert "VERIFY RED" in ergebnis.stdout
    assert "── [aa-rot] RED (block)" in ergebnis.stdout
    assert "skipped" not in ergebnis.stdout, "an unreached gate acquired a conditional skip"
    geschichte = _baum_geschichte(baum)
    assert [e["gate"] for e in geschichte if e["event"] == "gate"] == ["aa-rot"], geschichte
    assert [e for e in geschichte if e["event"] == "gate_skip"] == [], geschichte
    ende = [e for e in geschichte if e["event"] == "run_end"]
    assert len(ende) == 1 and ende[0]["verdict"] == "red"
    rot = stage2.red_sections(ergebnis.stdout)
    assert rot is not None and "aa-rot" in rot and "block-rot-diagnostik" in rot, rot
    assert "zz-leerprobe" not in rot and "mm-nach" not in rot, rot

    # Broken measurement storage: the runner warns, the gates and the skip
    # keep their verdicts, and nothing is written through the substituted file.
    baum = _baum(
        basis / "lager",
        gate_bauer=lambda b: [
            _gate(b, "aa-vor"),
            _gate(b, "zz", dekl=dict(VOLLE_DEKLARATION), cost="minutes"),
        ],
    )
    _verzweige(baum)
    lager = baum.parent / "state" / "coding-harness"
    lager.mkdir(parents=True)
    (lager / verify_duration.HISTORY_NAME).mkdir()
    ergebnis = _lauf_laeufer(baum)
    assert ergebnis.returncode == 0, f"exit {ergebnis.returncode}\n{ergebnis.stdout}\n{ergebnis.stderr}"
    assert "measurement storage unusable" in ergebnis.stderr, ergebnis.stderr
    assert "VERIFY GREEN" in ergebnis.stdout and "1 declared local skip" in ergebnis.stdout
    assert "──   [zz-leerprobe] skipped — " in ergebnis.stdout
    assert (lager / verify_duration.HISTORY_NAME).is_dir(), "something was written through the substituted history"

    # The skip line is the not-run summary's shape: no gate frame, no verdict.
    skip_zeile = next(z for z in ergebnis.stdout.splitlines() if "] skipped — " in z)
    assert stage2.GATE_START.match(skip_zeile) is None
    assert stage2.GATE_END.match(skip_zeile) is None
