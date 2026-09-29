---
title: "plans/ — die Artefakte, die zwischen den Phasen übergeben werden"
category: engine
status: current
created: 2026-09-05
last_reviewed: 2026-09-05
updated: 2026-09-29
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-05"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [workflow, artefakte, spec, plan, lebenszyklus]
---

# plans/

Hier liegt das, was eine Phase des Arbeitsablaufs an die nächste übergibt. **Die
Übergabe ist die Datei, nicht der Chat-Verlauf.** Der ganze Sinn: zwischen Plan
und Umsetzung wird der Kontext gelöscht, und danach muss trotzdem alles da sein.

Der Ablauf selbst steht in [`docs/WORKFLOW.md`](../docs/WORKFLOW.md).

## Drei Zustände, drei Orte

| Ort | Was dort liegt | Lebensdauer |
|---|---|---|
| `specs/<capability>/spec.md` | **lebend** — was eine Fähigkeit heute leisten soll | bleibt, wird fortgeschrieben |
| `changes/<name>/` | **aktiv** — eine Änderung in Arbeit: `research.md`, `spec.md`, `plan.md` | bis zum Abschluss |
| `changes/archive/YYYY-MM-DD-<name>/` | **historisch** — abgeschlossen | bleibt als Beleg, wird nie zitiert |

Nach Abschluss einer Änderung: das Delta in die lebende Capability-Spec mergen,
dauerhafte Architekturentscheidungen als ADR nach `docs/adr/` heben, den Rest
archivieren. **Eine implementierte Feature-Spec bleibt nicht als lebendes
Dokument stehen** — dafür sind Code und Git-Historie da, und zwei Wahrheiten über
denselben Gegenstand sind eine zu viel.

## Frontmatter

Zwei getrennte Statusfelder, und die Trennung ist der Punkt:

```yaml
status: draft | accepted | superseded      # bewegt sich, wenn das Projekt entscheidet
implementation_status: none | partial | done   # bewegt sich, wenn der Code sich bewegt
date: 2026-09-05
last_reviewed: 2026-09-05
supersedes: null
superseded_by: null
bead: portfolio-agentic-engineering-<id>
```

Ein Feld, das beides trägt, kann nicht sagen, ob eine akzeptierte Spec noch
ungebaut ist oder ob gebauter Code auf einer zurückgezogenen Spec steht. Genau
diese beiden Fälle sind die interessanten.

`bead:` verbindet das Artefakt mit dem Tracker. Arbeit wird in Beads geführt,
nicht in Markdown-Listen (AGENTS.md) — die Artefakte hier beschreiben *was*
gebaut wird, der Tracker sagt, *wo es steht*.

**Pflicht** sind `status`, `implementation_status`, `date`, `last_reviewed`
und `bead`; `plans_registry.py --check` blockiert, wenn eines fehlt — **oder
da ist, aber leer bzw. `null`**. „Vorhanden" und „gefüllt" sind nicht dasselbe:
ein `last_reviewed:` ohne Wert ist für jede nachgelagerte Prüfung derselbe
blinde Fleck wie ein fehlendes Feld. `supersedes` und `superseded_by` sind die
einzigen zwei Felder, die `null` sein dürfen. Bis zum 06.09. war `bead` nur
Konvention — alle Artefakte trugen es, geprüft hat es niemand. Eine Regel,
die jeder befolgt und kein Gate kennt, ist eine Gewohnheit.

`bead:` ist mehr als ein Verweis: `plans_registry.py` hält `implementation_status`
gegen den Zustand desselben Vorgangs im Tracker-Render — über den einen
Zugriffspunkt `scripts/bead_render.py` (in der CI das vorgesetzte `BEAD_RENDER`,
sonst ein frisches Render). Ist der Bead
geschlossen, muss das Artefakt `done` sein **und** unter `changes/archive/`
liegen; steht es auf `done`, muss der Bead geschlossen sein. Beide Richtungen
melden DRIFT und werden erst im nächtlichen `--strict`-Lauf scharf, nicht am
Pull Request — zwischen `bd close` und dem Nacharchivieren liegt bewusst ein
Fenster von Stunden, kein Grund zum Blocken.

Bewegt sich `implementation_status` von `none` weg, muss der Ordner ein
`plan.md` tragen — DRIFT im selben `--strict`-Lauf.

`last_reviewed` altert: liegt es mehr als `STALE_AFTER_DAYS` Tage zurück (heute
90, die Zahl steht in `scripts/plans_registry.py`, nicht hier), ist das DRIFT.
Archivierte Artefakte sind ausgenommen — ein Archiv altert per Definition. Und
ein `date` oder `last_reviewed`, das sich **nicht als Datum lesen lässt**, ist
selbst ein DRIFT-Befund: ein unlesbarer Wert ist kein Grund, die Prüfung zu
überspringen, sondern der Anlass, sie zu melden.

**Alle DRIFT-Regeln zusammen** — gebaut und nicht archiviert, einseitige
Ablösung, Altersschwelle, unlesbares Datum, die Kopplung an den Vorgang, das
fehlende `plan.md` — werden nachts im `drift`-Job scharf
(`plans_registry.py --check --strict`), nicht am Pull Request. Was am Pull
Request blockt, ist BLOCK: fehlendes oder leeres Pflichtfeld, ein Status
außerhalb der erlaubten Menge, ein Ablösungszeiger ins Leere, ein veralteter
`INDEX.md`, ein fehlender Tracker-Export.

## Die Regel gegen Mehrfacherzeugung

> Vor dem Anlegen eines Spec- oder Plan-Artefakts: **immer erst** per `rg` in
> `plans/specs/` und `plans/changes/` nach dem Thema suchen. Existiert ein
> passendes Artefakt, wird es **aktualisiert** — nicht neu angelegt.

Sie steht wörtlich auch in `AGENTS.md`, weil ein Agent diese Datei hier nicht
zwangsläufig liest. Was `make staleness` prüft, ist die Folge davon: Artefakte
ohne Frontmatter, ohne Bead, mit widersprüchlichem Status, oder fertig und nie
archiviert.
