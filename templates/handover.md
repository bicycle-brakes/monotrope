# Vorlage — Übergabe

Kopiervorlage für eine Datei unter `docs/journal/handover/`. Sie trägt **kein
eigenes Frontmatter**: `provenance.yaml` setzt für `templates/`
`frontmatter: none`, weil ein Frontmatter in einer Vorlage in jede Instanz
mitkopiert würde und dort eine Provenienz-Behauptung aufstellte, die niemand
geprüft hat. Das Schema steht deshalb in Codeblöcken.

**Die geltende Feldliste steht in `scripts/handover_schema.py`**, nicht hier und
nicht in der Prosa des Feedback-Loops. Diese Datei zeigt sie, sie definiert sie
nicht — `tests/test_feedback_channel.py` prüft beides gegeneinander.

## Erst entscheiden: welche Richtung?

`direction` ist Pflichtfeld **jeder** Übergabe. Ohne das Feld fällt die Datei
aus jeder Prüfung des Kanals heraus — genau das war am 2026-09-08 bei 14 von 24
Dateien der Fall.

| Wert | Wann | Was der Empfänger tut |
|---|---|---|
| `framework->framework` | Sitzungsübergabe in diesem Repo. Ein Stand zum Stichtag, für die nächste Sitzung | nichts — niemand wartet auf eine Quittung |
| `framework->project` | Der Rückkanal in eine Projekt-Instanz. Das Framework darf dort nicht schreiben (ADR-011/015), also legt es ab und wartet | quittiert per Pull Request in dieses Repo |

Im Zweifel `framework->framework`. Eine Übergabe zum Kanal zu erklären, die
niemand abholt, erzeugt eine offene Zusage, die für immer offen bleibt.

## Variante A — Sitzungsübergabe

```yaml
title: "Sitzungsübergabe — <Thema>, Stand <JJJJ-MM-TT>"
category: handover
created: 2026-01-01
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-01-01"
tags: [handover, sitzung]
# Ab hier optional, in beiden Richtungen zulässig:
# Die Kennzahlen des Ablaufs — wo eine Sitzung Phasen gefahren hat, gehören sie
# hierher. Sie sind die einzige Grundlage, auf der sich die Doktrin korrigieren
# kann; ohne sie bleibt jede Aussage über Gate-Wirkung eine Erwartung.
review_rounds: 2
fix_regen_rounds: 0
late_findings: 0
questions: "3 ([E]1 [F]1 [D]1)"   # nach Klasse: Entscheidung · Fachlücke · Detail
target_ref: a1b2c3d4        # der Commit, über den berichtet wird
bead: portfolio-agentic-engineering-<id>
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
```

Danach der Text. Was hineingehört, sagt nicht diese Vorlage, sondern die
Erfahrung: **was gemacht wurde, was gemessen ist, was offen ist, und was beim
nächsten Mal zuerst zu tun ist.** Zahlen immer mit ihrem Stichtag — ein
Verlaufs-Dokument altert planmäßig (RB-P5).

## Variante B — Rückkanal in eine Projekt-Instanz

Zusätzlich zu Variante A, und hier ist jedes Feld Pflicht:

```yaml
direction: framework->project
target_repo: <repo-name>
target_ref: a1b2c3d4         # kurzer Commit-Hash, gegen den erhoben wurde
status: pending              # pending -> acknowledged -> closed
bead: portfolio-agentic-engineering-<id>
record_sha256: "sha256:<hash>"
acknowledged_by: null        # setzt NUR das Projektteam
acknowledged_at: null        # setzt NUR das Projektteam
closed_at: null              # setzt NUR das Projektteam
```

`acknowledged_by`, `acknowledged_at` und `closed_at` gehören dem Projektteam.
Das Framework setzt `pending` und rührt die drei nie an — wer sein eigenes
Ergebnis quittiert, quittiert nichts.

### Der Befundblock ist unveränderlich

Der Teil der Übergabe, auf den sich jemand verlässt, steht zwischen zwei
Markern. `record_sha256` ist der SHA-256 über **genau** den Text dazwischen —
ohne die Marker selbst.

```markdown
<!-- record:begin -->

| # | Befund | Fundstelle | Signifikanz |
|---|---|---|---|
| 1 | … | … | hoch |

<!-- record:end -->
```

Widerspruch kommt **unter** den Block, nie hinein (RB-P5). Eine Unterschrift
unter einem Text, der sich danach ändert, ist keine.

Den Hash erzeugen:

```bash
python3 - <<'PY'
import hashlib, pathlib, sys
t = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs/journal/handover/<datei>.md").read_text(encoding="utf-8")
block = t.split("<!-- record:begin -->\n", 1)[1].split("<!-- record:end -->", 1)[0]
print("sha256:" + hashlib.sha256(block.encode()).hexdigest())
PY
```

### Und dann in den Index

Eine Übergabe mit `direction: framework->project` **muss** in der Tabelle in
`docs/journal/_INDEX.md` stehen, solange ihr Status nicht `closed` ist. Eine
Übergabe, die der Index nicht kennt, holt niemand ab — sie ist dann keine
Übergabe, sondern eine Datei, die jemand geschrieben hat.

## Prüfen, bevor es ein Pull Request wird

```bash
python3 -m pytest tests/test_feedback_channel.py -q
```
