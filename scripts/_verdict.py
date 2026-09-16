"""Drei Stufen fuer Drift-Werkzeuge — damit ein Exit-Code ueberall dasselbe heisst.

Ohne gemeinsames Vokabular bedeutet „Exit 1" in jedem Script etwas anderes, und
die Folge ist immer dieselbe: Entweder das Gate blockt an einem Tag, an dem
niemand etwas falsch gemacht hat — dann wird es abgeschaltet — oder es meldet
gruen ueber echter Abweichung, dann misst es nichts.

Die drei Stufen unterscheiden **wer den Befund verursacht hat**:

| Stufe   | Bedeutung                                              | Exit | Wer blockt        |
|---------|--------------------------------------------------------|:----:|-------------------|
| `INFO`  | Bemerkenswert, aber niemand hat etwas falsch gemacht   |  0   | niemand, gezaehlt |
| `DRIFT` | Die Projekt-Instanz hat sich vom Stand hier entfernt   |  1   | nur `--strict`    |
| `BLOCK` | Artefakte **dieses** Repos widersprechen einander      |  2   | immer             |

Der wichtigste Fall ist `INFO`. Ein Promotions-Kandidat — die Instanz hat ein
Muster, das das Framework noch nicht hat — ist **kein Fehler**. Die Instanz ist
der Ort, an dem neue Muster entstehen; das Framework *darf* dahinter liegen.
Zaehlte man das als Drift, waere das Gate ab dem Tag seiner Verdrahtung dauerhaft
rot, ohne dass ein Pull Request die Ursache waere.

Der Unterschied zwischen `DRIFT` und `BLOCK` ist die **Beweglichkeit der beiden
Seiten**: Bei `BLOCK` wandern beide Seiten per Commit in diesem Repo — ein
Widerspruch ist also immer die Schuld des Commits, der ihn erzeugt hat, und
gehoert an den Pull Request. Bei `DRIFT` bewegt sich die andere Seite ohne jeden
Commit hier; das gehoert in einen zeitgesteuerten Lauf, nicht an einen fremden
Pull Request.

## Das Transitions-Ventil

Ein neuer Check, der am Tag seiner Einfuehrung den halben Bestand rot faerbt,
wird gewaivt — und ein gewaivtes Gate misst nichts. Ein `Ramp` erlaubt deshalb,
einen Befund **vorlaeufig** eine Stufe tiefer zu melden. Er trägt zwei Dinge,
die ihn von einer stillen Ausnahme unterscheiden:

- eine **Bedingung in Worten**, unter der hochgeschaltet wird, und
- ein **Praedikat**, das misst, ob sie erfuellt ist.

Ist die Bedingung erfuellt, meldet `Ramp.due` das — und ein Test schlaegt fehl,
solange nicht hochgeschaltet wurde. Damit haengt das Hochschalten an einer
Pruefung und nicht am Gedaechtnis.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from enum import IntEnum


class Level(IntEnum):
    """Exit-Code und Schwere in einem — `max()` ueber alle Befunde ist der Exit-Code."""

    INFO = 0
    DRIFT = 1
    BLOCK = 2


LEVEL_LABEL = {
    Level.INFO: "INFO ",
    Level.DRIFT: "DRIFT",
    Level.BLOCK: "BLOCK",
}


@dataclass(frozen=True)
class Ramp:
    """Ein Befund wird vorlaeufig tiefer gemeldet, bis eine benannte Bedingung haelt.

    `condition` steht im Report und sagt dem Menschen, worauf gewartet wird.
    `predicate` sagt dem Test, ob weiter gewartet werden darf.
    `deadline` ist die zweite, unabhaengige Faelligkeit: ein Datum, ab dem das
    Ventil auch dann hochschaltet, wenn die Bedingung nie eingetreten ist.

    Warum beides: Ein Praedikat misst, ob der Bestand geraeumt wurde. Es misst
    nicht, ob jemand daran gearbeitet hat. Ein Ventil, dessen Bedingung nie
    eintritt, weil niemand sie angeht, bleibt ohne Datum fuer immer offen — und
    ist damit genau die Ausnahme mit besserem Namen, gegen die diese Datei
    geschrieben ist. Das Datum ist kein Kalendereintrag: es macht den Test rot,
    und ein roter Test ist eine Entscheidung, kein Erinnerungszettel.
    """

    name: str
    condition: str
    predicate: Callable[[], bool]
    target: Level = Level.BLOCK
    until_then: Level = Level.INFO
    deadline: date | None = None

    @property
    def due(self) -> bool:
        """Ist die Bedingung erfuellt oder die Frist abgelaufen?"""
        if self.deadline is not None and date.today() >= self.deadline:
            return True
        return self.predicate()

    def level(self) -> Level:
        return self.target if self.due else self.until_then


@dataclass
class Finding:
    level: Level
    message: str
    detail: str = ""
    ramp: Ramp | None = None

    def effective_level(self) -> Level:
        """Die Stufe, mit der dieser Befund heute zaehlt (Ventil beruecksichtigt)."""
        if self.ramp is None:
            return self.level
        return self.level if self.ramp.due else self.ramp.until_then


@dataclass
class Verdict:
    """Sammelt Befunde und rechnet daraus einen Exit-Code aus."""

    findings: list[Finding] = field(default_factory=list)

    def add(
        self,
        level: Level,
        message: str,
        detail: str = "",
        ramp: Ramp | None = None,
    ) -> None:
        self.findings.append(Finding(level, message, detail, ramp))

    def info(self, message: str, detail: str = "") -> None:
        self.add(Level.INFO, message, detail)

    def drift(self, message: str, detail: str = "", ramp: Ramp | None = None) -> None:
        self.add(Level.DRIFT, message, detail, ramp)

    def block(self, message: str, detail: str = "", ramp: Ramp | None = None) -> None:
        self.add(Level.BLOCK, message, detail, ramp)

    def at(self, level: Level) -> list[Finding]:
        return [f for f in self.findings if f.effective_level() == level]

    def exit_code(self, strict: bool = False) -> int:
        """Hoechste erreichte Stufe. Ohne `--strict` blockt DRIFT nicht.

        Der Grund steht oben: die Gegenseite eines DRIFT-Befundes bewegt sich
        ohne Commit in diesem Repo. An einem fremden Pull Request waere das
        Rauschen; in einem zeitgesteuerten Lauf (`--strict`) ist es das Signal.
        """
        if not self.findings:
            return 0
        worst = max(f.effective_level() for f in self.findings)
        if worst == Level.DRIFT and not strict:
            return 0
        return int(worst)

    def render(self) -> str:
        """Report in Lesereihenfolge: erst was blockt, dann was nur auffaellt."""
        if not self.findings:
            return "OK — keine Abweichung."
        out: list[str] = []
        for level in (Level.BLOCK, Level.DRIFT, Level.INFO):
            group = self.at(level)
            if not group:
                continue
            out.append(f"{LEVEL_LABEL[level]} ({len(group)}):")
            for f in group:
                out.append(f"  - {f.message}")
                if f.detail:
                    out.extend(f"      {line}" for line in f.detail.splitlines())
                if f.ramp is not None and not f.ramp.due:
                    out.append(
                        f"      [Ventil {f.ramp.name}] gemeldet als "
                        f"{LEVEL_LABEL[f.ramp.until_then].strip()} statt "
                        f"{LEVEL_LABEL[f.ramp.target].strip()}, bis: {f.ramp.condition}"
                    )
            out.append("")
        return "\n".join(out).rstrip()


# ---------------------------------------------------------------------------
# Das Vokabular der Schreiber
# ---------------------------------------------------------------------------


def check_verdict(stale: list[str], missing: list[str], regenerate: str) -> int:
    """Exit-Code fuer ein `--check` eines Schreib-Subkommandos.

        0  aktuell
        1  veraltet — das Kommando zum Neuerzeugen steht in der Meldung
        2  fehlt oder ist nicht lesbar

    Warum getrennt von INFO/DRIFT/BLOCK: `Verdict.exit_code()` liefert ohne
    `--strict` bei DRIFT eine Null, weil sich die Gegenseite eines DRIFT-Befundes
    ohne Commit in diesem Repo bewegt. Bei einem Schreiber ist das nicht so —
    beide Seiten liegen hier, und ein veraltetes Schema muss am Pull Request rot
    sein (RB-G2).

    Und warum 1 und 2 verschieden sind: „fehlt" und „veraltet" haben
    verschiedene Ursachen und verschiedene Reparaturen. Ein Werkzeug, das beide
    gleich meldet, hat in einer Projekt-Instanz wochenlang eine fehlende Eingabe
    als Staleness gemeldet — und jeder hat den Regenerier-Lauf gestartet, der
    nichts finden konnte (F-A-11).
    """
    if missing:
        print(f"FEHLT: {', '.join(missing)} — nie erzeugt oder nicht lesbar.", file=sys.stderr)
        return 2
    if stale:
        print(f"VERALTET: {', '.join(stale)} — neu erzeugen mit: {regenerate}", file=sys.stderr)
        return 1
    return 0
