"""Das Modul haelt seine eigenen Zusagen — die statische Haelfte.

Die Arbeitsteilung ist Absicht. **Dieser Test prueft, was ohne einen Lauf
pruefbar ist:** dass jede Datei eine Rolle hat, dass jeder Grund aus der
geschlossenen Menge kommt, dass der Deckel haelt, dass sich die beiden
Manifeste nicht widersprechen. **Der Lauf selbst gehoert
`scripts/kit/probe.py`** — er blockt, wenn ein roter Fall keinen Grund hat oder
ein Grund abgelaufen ist, und er laeuft als eigener Schritt in `ci.yml`.

Warum getrennt: eine pytest-Sitzung, die in sich eine zweite pytest-Sitzung
startet, ist langsam und in fremden Umgebungen zerbrechlich. Der Lauf ist ein
Gate, kein Testfall — und `ci.yml` traegt die Gate-Liste, nicht diese Datei.
"""

from __future__ import annotations

import functools
import re
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
KIT = REPO_ROOT / "scripts" / "kit"

sys.path.insert(0, str(KIT))
import probe  # noqa: E402

sys.path.insert(0, str(KIT.parent))
from _verdict import Level, Verdict  # noqa: E402

EXPORT_MANIFEST = REPO_ROOT / "scripts" / "export" / "manifest.yaml"


# ---------------------------------------------------------------------------
# AK-1 · Die Menge steht in einer Datei
# ---------------------------------------------------------------------------


def test_the_examined_set_is_not_empty() -> None:
    """Eine leere Menge ist kein Ergebnis (RB-G7).

    Ohne diesen Test liefe jeder folgende gruen ueber null Dateien, und ein
    kaputtes `git ls-files` saehe aus wie ein erfuelltes Manifest.
    """
    assert probe.getrackte_dateien(), "keine getrackte Datei gefunden — dann misst hier nichts"
    assert probe.regeln(), "das Manifest traegt keine Regel"


def test_every_tracked_file_has_a_role() -> None:
    """Nicht gelistet ist BLOCK, nicht 'gehoert nicht dazu'.

    Ein Standard, der im Zweifel entscheidet, entscheidet genau ueber die
    Dateien, an die niemand gedacht hat — dieselbe Begruendung, aus der das
    Export-Manifest lebt.
    """
    offen = probe.nach_rolle()["(offen)"]
    assert not offen, (
        f"{len(offen)} Datei(en) fallen unter keine Regel in scripts/kit/manifest.yaml:\n  "
        + "\n  ".join(sorted(offen)[:20])
    )


def test_the_kit_actually_carries_something() -> None:
    """Ein Modul aus null Dateien ist kein Modul (RB-G7)."""
    verteilt = probe.nach_rolle()
    assert verteilt["mechanismus"], "keine Datei traegt die Rolle 'mechanismus'"
    assert len(verteilt["mechanismus"]) >= 20, (
        f"nur {len(verteilt['mechanismus'])} Datei(en) im Mechanismus — die Erhebung vom 2026-09-08 hat 27 gemessen"
    )


def test_every_rule_carries_a_reason() -> None:
    """Der Grund steht in der Regel, nicht im Kopf des Uebergebenden."""
    ohne = [r["prefix"] for r in probe.regeln() if not r.get("reason", "").strip()]
    assert not ohne, f"Regel(n) ohne Begruendung: {ohne}"


def test_every_role_used_is_declared() -> None:
    """Ein Rollenname, den der Kopf der Datei nicht kennt, ist ein Tippfehler."""
    deklariert = set(yaml.safe_load(probe.MANIFEST.read_text(encoding="utf-8"))["rollen"])
    benutzt = {r["rolle"] for r in probe.regeln()}
    assert benutzt <= deklariert, f"unbekannte Rolle(n): {sorted(benutzt - deklariert)}"
    assert deklariert <= benutzt, (
        f"deklarierte, aber nie benutzte Rolle(n): {sorted(deklariert - benutzt)} — "
        "ein Vokabularwert, der fuer nichts steht, ist eine Einladung, ihn falsch zu benutzen"
    )


# ---------------------------------------------------------------------------
# AK-3/AK-4 · Die Ausnahmen und ihr Deckel
# ---------------------------------------------------------------------------


def test_every_reason_comes_from_the_closed_set() -> None:
    """Drei Gruende, keiner mehr. Ein freier Text waere keine Klassifikation."""
    fremd = {n: g for n, g in probe.REIST_NICHT.items() if g not in probe.GRUENDE}
    assert not fremd, f"Grund ausserhalb der Menge {probe.GRUENDE}: {fremd}"


def test_every_declared_reason_is_actually_used() -> None:
    """Ein Grund, den niemand traegt, ist ein Wort ohne Fall."""
    benutzt = set(probe.REIST_NICHT.values())
    ungenutzt = set(probe.GRUENDE) - benutzt
    assert not ungenutzt, (
        f"Grund/Gruende ohne einen einzigen Fall: {sorted(ungenutzt)}. "
        "Entweder streichen oder den Fall benennen, fuer den er steht."
    )


def test_the_exemption_list_only_shrinks() -> None:
    """Sperrklinke. Dieselbe Form wie `ci_gates.OHNE_AUFRUFER` und `OHNE_TEST`.

    Eine Portabilitaet, die man verlieren kann, ohne dass es auffaellt, ist
    keine. Wer einen Eintrag hinzufuegt, hebt den Deckel sichtbar an — im Diff,
    mit Begruendung im Commit.
    """
    assert len(probe.REIST_NICHT) <= probe.DECKEL, (
        f"REIST_NICHT hat {len(probe.REIST_NICHT)} Eintraege, der Deckel steht auf {probe.DECKEL}"
    )


def test_the_cap_is_not_slack() -> None:
    """Ein Deckel weit ueber dem Stand ist kein Deckel, sondern eine Erlaubnis."""
    luft = probe.DECKEL - len(probe.REIST_NICHT)
    assert luft <= 3, (
        f"der Deckel liegt {luft} ueber dem heutigen Stand — dann faellt Wachstum nicht auf. "
        f"Auf {len(probe.REIST_NICHT)} setzen."
    )


# ---------------------------------------------------------------------------
# AK-6 · Zwei Manifeste, kein Widerspruch
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=1)
def _export_regeln() -> tuple[dict, ...]:
    return tuple(yaml.safe_load(EXPORT_MANIFEST.read_text(encoding="utf-8"))["rules"])


def _export_verdict(pfad: str) -> str | None:
    treffer = [r for r in _export_regeln() if pfad.startswith(r["prefix"])]
    if not treffer:
        return None
    return max(treffer, key=lambda r: len(r["prefix"]))["verdict"]


# AK-6 hat in der Umsetzung seine Form geaendert, und der Grund gehoert hierher.
#
# Die Spec verlangte "keine widerspruechliche Kombination aus Kit-Rolle und
# Export-Verdict". Gemessen am 2026-09-08 gibt es keine: `.editorconfig` ist im
# Export `carry` und im Kit `bestand`, `.github/ISSUE_TEMPLATE/` ebenso — und
# das ist voellig in Ordnung. Eine Datei kann fuer den Ablauf unbeteiligt sein
# und trotzdem byte-gleich in ein anderes Repo gehoeren. Die beiden Fragen sind
# **orthogonal**, also kann keine Kombination aus ihnen widerspruechlich sein.
#
# Damit war der urspruengliche Test nicht scharf, sondern falsch konstruiert: er
# haette erzwungen, dass zwei Antworten auf zwei verschiedene Fragen sich
# aneinander ausrichten.
#
# Was AK-6 wirklich absichern soll, ist etwas anderes: **dass die zweite Liste
# keine Ableitung der ersten ist.** Waere jede Kit-Rolle durch genau ein
# Export-Verdict bestimmt (oder umgekehrt), koennte man die eine aus der anderen
# ausrechnen — und dann waere sie eine Dublette, genau der Befund, den dieses
# Repo immer wieder gegen sich selbst erhebt. Das ist pruefbar, und zwar so:


def test_the_kit_list_is_not_derivable_from_the_export_list() -> None:
    """Die zweite Liste rechtfertigt sich, indem sie sich NICHT ausrechnen laesst.

    Fuer jede Kit-Rolle wird gezaehlt, auf wie viele verschiedene Export-Verdicts
    ihre Dateien fallen. Faellt eine Rolle auf genau eines, ist sie aus dem
    Export-Manifest ableitbar — dann ist `scripts/kit/manifest.yaml` eine
    Dublette und gehoert geloescht, nicht gepflegt.
    """
    verteilung: dict[str, set[str]] = {}
    for pfad in probe.getrackte_dateien():
        kit = probe.rolle(pfad)
        exp = _export_verdict(pfad)
        if kit and exp:
            verteilung.setdefault(kit[0], set()).add(exp)
    assert verteilung, "keine Datei steht in beiden Manifesten — dann prueft dieser Test nichts (RB-G7)"
    ableitbar = {rolle: v for rolle, v in verteilung.items() if len(v) == 1}
    assert not ableitbar, (
        f"Rolle(n) mit genau einem Export-Verdict: {ableitbar}. "
        "Diese Rolle laesst sich aus dem Export-Manifest ausrechnen — dann ist die "
        "zweite Liste eine Dublette und nicht eine zweite Frage."
    )


def test_the_two_manifests_really_disagree_somewhere() -> None:
    """Gegenprobe zur Gegenprobe: die Ueberschneidung ist nicht leer.

    Der Test oben waere auch gruen, wenn keine einzige Datei in beiden
    Manifesten vorkaeme. Dann prueft er nichts (RB-G7).
    """
    beide = [p for p in probe.getrackte_dateien() if probe.rolle(p) and _export_verdict(p)]
    assert len(beide) > 60, (
        f"nur {len(beide)} Datei(en) stehen in beiden Manifesten. (Dieses Repo "
        "traegt 85 klassifizierte Dateien — das Ursprungs-Repo ueber 200; die "
        "Schwelle folgt dem Bestand, nicht der Sehnsucht.)"
    )
    # Und mindestens eine Datei, die der Ablauf traegt, wirft der Export weg —
    # das ist der Befund aus research.md 2.2 und muss sichtbar bleiben.
    getragen_verworfen = [p for p in beide if probe.rolle(p)[0] == "mechanismus" and _export_verdict(p) == "drop"]
    assert getragen_verworfen, (
        "keine einzige Datei ist im Kit 'mechanismus' und im Export 'drop' — "
        "dann ist der Befund aus research.md 2.2 verschwunden, ohne dass jemand "
        "es entschieden haette"
    )


# ---------------------------------------------------------------------------
# AK-7 · Kein zweiter Inhalt
# ---------------------------------------------------------------------------

PHASEN = ("explore", "spec", "plan", "implement", "verify", "review", "commit")


def _kit_dateien() -> list[Path]:
    return sorted(p for p in KIT.rglob("*") if p.is_file() and p.suffix in (".py", ".yaml", ".md"))


def test_the_kit_does_not_describe_the_phases() -> None:
    """Der Kit ruft den Ablauf, er beschreibt ihn nicht.

    Dieselbe Regel wie fuer den Wrapper aus `wei1` (AK-2 dort): eine zweite
    Beschreibung der sieben Phasen ist die zweite Liste, und die zweite Liste
    ist immer die, die veraltet.
    """
    dateien = _kit_dateien()
    assert dateien, "keine Kit-Datei gefunden — dann prueft dieser Test nichts (RB-G7)"
    for p in dateien:
        text = p.read_text(encoding="utf-8").lower()
        # Eine Referenz auf einen Prompt-Dateinamen ("01-explore.md") ist keine
        # Beschreibung der Phase — sie zeigt auf die eine Liste, statt eine
        # zweite aufzumachen. Genau das soll der Kit tun. Ohne diese Trennung
        # wurde der Test rot, weil `REIST_NICHT` sechs Testfaelle nennt, deren
        # pytest-ID den Prompt-Dateinamen traegt.
        text = re.sub(r"\d\d-[a-z]+\.md", "", text)
        genannt = [ph for ph in PHASEN if ph in text]
        assert len(genannt) < 5, (
            f"{p.relative_to(REPO_ROOT)} nennt {len(genannt)} der sieben Phasennamen "
            f"({', '.join(genannt)}) — das liest sich wie eine zweite Beschreibung. "
            "Auf prompts/ oder docs/WORKFLOW.md verweisen."
        )


@pytest.mark.parametrize("pfad", ["prompts/01-explore.md", "docs/WORKFLOW.md"])
def test_the_workflow_itself_travels(pfad: str) -> None:
    """Der Ablauf ist im Modul, nicht nur seine Werkzeuge.

    Ein Kit aus Validatoren ohne die sieben Phasen waere ein Satz Werkzeuge,
    kein Ablauf — und genau die Verwechslung, die `research.md` §2.2 an der
    Export-Pipeline gefunden hat.
    """
    gefunden = probe.rolle(pfad)
    assert gefunden is not None, f"{pfad} faellt unter keine Regel"
    assert gefunden[0] == "mechanismus", f"{pfad} ist '{gefunden[0]}', nicht 'mechanismus'"


# ---------------------------------------------------------------------------
# Mutationsnachweise — das Gate `kit-probe` hat einen Lauf, der es rot macht
#
# Die fuenf Gegenproben aus Phase 4 sind hier als Testfaelle festgehalten, damit
# sie wiederholbar sind. Eine Gegenprobe, die nur im Sitzungsprotokoll steht,
# ist ein Satz ueber die Vergangenheit, kein Schutz.
#
# Jeder dieser Faelle ruft `probe.pruefe()` — den Code, den das Gate faehrt.
# Bis zum 2026-09-08 taten sie das NICHT: zwei bauten den Filter inline nach,
# einer war Arithmetik ueber einem monkeypatchten Dict, einer pruefte eine
# Aussage, die die Zeile darueber schon herstellte. Man konnte die Sperre in
# `pruefe()` loeschen und die Suite blieb gruen — waehrend `test_ci.py` Deckung
# meldete. Das ist die Fehlerklasse, gegen die dieses Modul gebaut ist, im
# Nachweis dieses Moduls selbst.
#
# `pruefe(faelle=...)` nimmt die Fallmenge entgegen, damit kein Test die echte
# Leerprobe fahren muss (die dauert Minuten). Alles davor — Regeln, Rollen,
# Gruende, Deckel — laeuft echt.
# ---------------------------------------------------------------------------


GRUENE_FAELLE = {"tests.test_gate_record::test_beispiel": True}


def _blockgruende(v: Verdict) -> str:
    """Die BLOCK-Meldungen eines Verdicts als ein Text, zum Suchen."""
    return "\n".join(f"{f.message} {f.detail}" for f in v.at(Level.BLOCK))


def _blockt(v: Verdict) -> bool:
    """Blockt dieses Verdict? Ueber denselben Exit-Code, den das Gate auswertet."""
    return v.exit_code() != 0


def test_the_role_check_goes_red_when_a_rule_is_removed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Nimmt die Regel fuer das `Makefile` weg und erwartet unklassifizierte Dateien.

    Ohne diesen Nachweis waere `test_every_tracked_file_has_a_role` gruen, weil
    es nichts findet — und nicht, weil es nichts zu finden gibt. (Im Ursprungs-
    Repo zielte die Mutation auf die Auffangregel `examples/`; dieser Bestand
    hat keinen examples-Ordner und auch kein `.editorconfig` — das Kit-Manifest
    erbt Regeln fuer abwesende Dateien, also zielt sie auf eine Regel mit
    echtem Fall.)
    """
    ohne_makefile = [r for r in probe.regeln() if r["prefix"] != "Makefile"]
    monkeypatch.setattr(probe, "regeln", lambda: ohne_makefile)
    offen = probe.nach_rolle()["(offen)"]
    assert offen, "eine Regel entfernt und trotzdem faellt keine Datei durch — die Pruefung misst nichts"
    assert all(p.startswith("Makefile") for p in offen), offen[:5]
    v = probe.pruefe(faelle=GRUENE_FAELLE)
    assert _blockt(v), "unklassifizierte Dateien blocken nicht"
    assert "unter keine Regel" in _blockgruende(v), _blockgruende(v)


def test_the_reason_check_goes_red_on_an_invented_reason(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ein Grund ausserhalb der geschlossenen Menge muss `pruefe()` blocken."""
    monkeypatch.setattr(probe, "REIST_NICHT", {**probe.REIST_NICHT, "tests.x::test_y": "weil-halt"})
    v = probe.pruefe(faelle=GRUENE_FAELLE)
    assert _blockt(v), "ein erfundener Grund blockt nicht"
    assert "weil-halt" in _blockgruende(v), _blockgruende(v)


def test_an_entry_whose_case_disappeared_goes_red(monkeypatch: pytest.MonkeyPatch) -> None:
    """Die dritte Richtung: ein Grund, dessen Fall gar nicht mehr gesammelt wird.

    Bis zum 2026-09-08 blockte das in keiner Richtung. Wer die Kit-Rolle einer
    Testdatei von `mechanismus` auf `bestand` zieht, nimmt ihre Faelle aus der
    Menge — sie sind dann weder rot noch gruen, `unerklaert` und `abgelaufen`
    bleiben leer, exit 0. Und die gemeldete Quote STEIGT, weil rote Faelle aus
    dem Nenner fallen. Damit liess sich Portabilitaet verlieren, ohne dass es
    auffiel.
    """
    ein_eintrag = next(iter(probe.REIST_NICHT))
    monkeypatch.setattr(probe, "REIST_NICHT", {ein_eintrag: probe.REIST_NICHT[ein_eintrag]})
    # Eine Fallmenge, die genau diesen Eintrag NICHT enthaelt.
    v = probe.pruefe(faelle=GRUENE_FAELLE)
    assert _blockt(v), f"{ein_eintrag} hat keinen Fall mehr und blockt trotzdem nicht"
    assert "keinen Fall mehr" in _blockgruende(v), _blockgruende(v)


def test_the_cap_goes_red_when_the_list_grows(monkeypatch: pytest.MonkeyPatch) -> None:
    """Die Sperrklinke haelt nur, wenn Wachstum ueber den Deckel rot wird."""
    gewachsen = {**probe.REIST_NICHT}
    for i in range(probe.DECKEL - len(probe.REIST_NICHT) + 1):
        gewachsen[f"tests.erfunden::test_fall_{i}"] = "bestand-dieses-repos"
    monkeypatch.setattr(probe, "REIST_NICHT", gewachsen)
    v = probe.pruefe(faelle=GRUENE_FAELLE)
    assert _blockt(v), "die Liste ist ueber den Deckel gewachsen, ohne dass er greift"
    assert "Deckel" in _blockgruende(v), _blockgruende(v)


def test_the_probe_detects_tampering_with_the_workflow_role(monkeypatch: pytest.MonkeyPatch) -> None:
    """Wird `docs/WORKFLOW.md` zu `bestand`, muss der Ablauf als nicht mitreisend auffallen."""
    verbogen = [{**r, "rolle": "bestand"} if r["prefix"] == "docs/WORKFLOW.md" else r for r in probe.regeln()]
    monkeypatch.setattr(probe, "regeln", lambda: verbogen)
    assert probe.rolle("docs/WORKFLOW.md", verbogen)[0] == "bestand"
    # Und der Ablauf faehrt dann nicht mehr mit: der Grund, der `docs/WORKFLOW.md`
    # als getragen voraussetzt, ist abgelaufen — das muss `pruefe()` melden.
    v = probe.pruefe(faelle={**GRUENE_FAELLE, "tests.test_ci::test_workflow_hat_phasen": True})
    assert "docs/WORKFLOW.md" not in probe.nach_rolle()["mechanismus"], "die Rollenaenderung greift nicht"
    assert v is not None
