---
title: "Quality Gates — welche Tore es gibt, wer sie schließt und was eine Unterschrift bedeutet"
category: governance
subcategory: quality-gates
status: current
created: 2026-04-17
last_reviewed: 2026-08-14
owner: Data Architect
provenance: human-decided
review:
  status: reviewed
  approved_by: "MPAdesso"
  approved_at: 2026-08-14
normative_for: [portfolio-agentic-engineering, project-instances]
lakeswitch_ref: "src/lakeswitchai/gates/catalog.yaml"
disclosure: intern
id_scheme: "MG-n Maschine · HG-n Mensch; IDs stabil, nie wiederverwendet"
tags: [governance, quality, gates, human-gates, abnahme, signatur]
---

# Quality Gates

> **Ein Gate ist eine Unterschrift über einem Hash, kein Kommentar unter einem
> Pull Request.** Die Maschine sortiert vor, der Mensch entscheidet — und wer
> nichts signiert hat, hat nichts abgenommen.

## Wozu diese Seite

Sie ist die **eine normative Heimat** für Gate-Bezeichnungen. Vor dem 2026-08-14
gab es vier Nummerierungen desselben Gegenstands in achtundfünfzig aktiven
Dateien — `G1–G4`, `G1/G2/Human/G3`, `Gate 0.5 / READY / Gate 3` und
`Pre-/In-/Post-Flight` — und keine Seite, die sagte, welche gilt. Der
Produktverantwortliche wurde vom Einstieg auf eine Seite geschickt, die vom
*Schreiben* von Konzepten handelte.

Vier Nummerierungen sind nicht vier Meinungen. Sie sind vier Zustände desselben
Prozesses, die niemand aufeinander abgebildet hat — und solange das so ist,
kann niemand sagen, ob ein Block abgenommen ist.

## Wie man diese Seite liest

Zwei Präfixe, mehr nicht:

- **`MG-n` — Maschinen-Gate.** Läuft ohne Menschen, blockt oder meldet. Es kann
  einen Fehler finden; es kann nichts freigeben.
- **`HG-n` — Human Gate.** Eine benannte Rolle unterschreibt über einem
  benannten Gegenstand. Nur hier entsteht eine Abnahme.

Wer einen Gate-Namen sucht: §4. Wer eine alte Bezeichnung übersetzen will: §5.
Wer wissen will, wie eine Unterschrift technisch festgehalten wird: §6.

## Was diese Seite nicht sagt

Sie nennt **keine Schwellen** — welche Abweichung eine Reconciliation noch
passieren lässt, steht im Contract der Entity, mit Begründung je Schwelle. Sie
beschreibt **keine Prozessschritte** — wie man ein Review fährt, steht in
[Review und Abnahme](../how-to/review-und-abnahme.md). Und sie ersetzt den
[Gate-Katalog](gate-catalog.md) nicht: der beschreibt zwölf *Familien* von
Prüfungen und ihre Betriebsregeln, diese Seite die *Tore* eines Liefergegenstands.

## 4 · Die Gates

### Maschinen-Gates

| ID | Name | Wann | Was es prüft | Wo es lebt |
|---|---|---|---|---|
| **MG-0** | Contract-Schema | bei jedem Contract-Write | Pydantic-Validierung der Contract-YAML | `scripts/validate_contract.py` |
| **MG-1** | Pre-Commit | vor dem Commit | Lint, YAML-Syntax, Secrets-Guard, Frontmatter | Claude-Code-Hooks |
| **MG-2** | PR-Verifikation | beim Pull Request | die eine Gate-Liste, gegen den Merge-Ref | `.github/workflows/ci.yml` |
| **MG-3** | Merge | vor dem Merge | Required Checks, Code-Owner-Review | GitHub-Ruleset |

MG-2 prüft **`refs/pull/N/merge`**, nicht den Branch-Kopf. Lokal grün und in der
CI rot ist deshalb kein Widerspruch, sondern der Normalfall: die CI baut, was
nach dem Merge entsteht.

### Human Gates

| ID | Name | Auslöser | Wer unterschreibt | Worüber |
|---|---|---|---|---|
| **HG-1** | Contract-Abnahme | Contract geht von `review` nach `accepted` | Data Architect **und** Fachseite | die Contract-Datei, über ihren semantischen Hash |
| **HG-2** | Reconciliation-Abnahme | Recon-Report ist fertig — **vor** Schluss der Liefereinheit | Data Product Owner (Consumer) **und** Data Architect | den Report, über seinen Hash |
| **HG-3** | Cutover-Freigabe | vor `cutover execute` | Produktverantwortlicher **und** Data Architect | das gerenderte Bundle **plus** den HG-2-Record |
| **HG-4** | Post-Cutover-Sign-off | nach dem Monitoring-Fenster | Operations Owner | das Run-Log |

**Drei Regeln, die für jedes HG gelten.**

*Der Gegenstand ist ein Hash, keine Datei.* Ändert sich der Gegenstand nach der
Unterschrift, ist er wieder unsigniert. In der Projekt-Instanz wurde eine
Signatur zurückgezogen, weil sich die Schlussfolgerung darunter geändert hatte —
ein Name stand gegen einen Text, den die Person nie gelesen hatte.

*Ein abgeleiteter Zustand wird nicht gesetzt, sondern gefolgert.*
`completeness_status: accepted` gilt genau dann, wenn ein HG-1-Record im Zustand
`ACCEPTED` existiert und sein Hash zum aktuellen Contract passt. Kein Feld, das
man von Hand auf `accepted` stellt.

*Kein Agent schließt ein Human Gate.* Er darf einen Antrag stellen, nie eine
Abnahme erzeugen. Das Verdikt wird aus den Findings gerechnet (Gate-Katalog
GK-8), und ein Mensch unterschreibt es.

### Was zwischen HG-2 und dem Schluss der Liefereinheit steht

Nichts. **HG-2 liegt vor dem Schluss, nicht danach.** In der Projekt-Instanz lief
die Reconciliation nach dem Schluss des Blocks: sechsundvierzig Befunde,
sechsundzwanzig davon hoch — und weil der Block schon zu war, konnten sie nur
noch eine Fix-Liste werden, nie ein Tor. Ein Befund nach dem Schluss ist kein
Gate; er ist eine Nachricht.

## 5 · Die vier Alt-Nummerierungen

Wer eine alte Bezeichnung liest, findet hier ihre heutige Bedeutung. **Die alten
IDs werden nicht mehr vergeben.**

| Alte Bezeichnung | Herkunft | Gilt heute als | Anmerkung |
|---|---|---|---|
| G1 Pre-Commit | CI/CD-Promotionslogik | **MG-1** | — |
| G2 PR-Validation | dieselbe | **MG-2** | — |
| G3 Merge-Gate | dieselbe | **MG-3** | — |
| G4 Staging-Smoke | dieselbe | **MG-2** | eine weitere Prüfung derselben Liste, kein eigenes Tor |
| G5 Promotion-Approval | dieselbe | **HG-3** | — |
| G6 Cutover-Gate | dieselbe | **HG-3** | setzt HG-2 voraus: „Recon innerhalb Toleranz" ist HG-2, nicht HG-3 |
| G7 Post-Deploy-Sign-Off | dieselbe | **HG-4** | — |
| G1 Spec-Approval | Prozess-Konzept | **HG-1** | dieselbe Ziffer, anderer Gegenstand — der Grund für diese Tabelle |
| G2 DQ-Validation | dasselbe | **HG-2** | — |
| G3 Cutover-Approval | dasselbe | **HG-3** | — |
| G4 Incident-Eskalation | dasselbe | **kein Gate** | ein Eskalationspfad, siehe [Eskalationsmodell](eskalationsmodell.md) |
| Gate 0.5 (Pydantic) | Contract-Validierung | **MG-0** | — |
| READY / OPEN / BLOCKED | Vorbedingungs-Prüfung | **kein Gate** | eine Vorbedingung von MG-0 und HG-1 |
| Pre-/In-/Post-Flight | Konzept-Entwicklung | **kein Gate** | eine Checkliste fürs Schreiben, jetzt im [Concept-Development-Workflow](concept-development-workflow.md) |
| Wave-Gate | Wellen-Modell | **entfallen** | das Wellen-Modell ist zurückgezogen (ADR-030) |

**Ersatzlos gestrichen: „AUTO-PASS".** Ein Reconciliation-Ergebnis, das sich bei
sechs von sechs bestandenen Prüfungen selbst abnimmt, ist keine Abnahme. HG-2
wird **immer** unterschrieben, auch wenn nichts abweicht — gerade dann steht
die Unterschrift für „ich habe hingesehen".

## 6 · Wie eine Unterschrift festgehalten wird

Ein Gate-Record ist eine Datei, kein Feld. Er trägt:

- `gate` und `subject: {kind, path, sha256}` — worüber unterschrieben wurde,
- `state` aus `DRAFT · IN_REVIEW · ACCEPTED · WITHDRAWN`,
- `history[]` — append-only, mit Zeitstempel, Rolle und Review-URL je Übergang,
- `signers[]` mit den Pflicht-Rollen dieses Gates.

Vier Bedingungen für `ACCEPTED`: alle Pflicht-Rollen liegen vor, jede mit
Review-URL; die Zustimmung ist **nach** dem Übergang nach `IN_REVIEW` datiert;
der Zustimmende ist weder Autor noch letzter Pusher; und `subject.sha256`
entspricht dem heutigen Hash.

Ein Record wird nach `ACCEPTED` nicht mehr geändert. Eine Rücknahme ist ein
**neuer** Record mit `WITHDRAWN` und Begründung — und sie setzt den abgeleiteten
Zustand zurück auf `review`.

**Der Zustand `accepted_unsigned` existiert nicht.** Er kollabiert zwei Fälle mit
verschiedenen Heilmitteln — „noch niemand hat unterschrieben" und „die
Unterschrift wurde zurückgezogen" — und ist blind gegen den zweiten.

Der Mechanismus wird noch gebaut (`V-34`, `V-35`). Bis dahin gilt die
Bezeichnung; ein Record ist heute ein Feld im Run-Log, und das ist die Lücke,
die diese Seite benennt statt sie zu verschweigen.

## 7 · Verwandtes

- [Gate-Katalog](gate-catalog.md) — die zwölf Prüf-Familien und ihre sieben Betriebsregeln
- [Review und Abnahme](../how-to/review-und-abnahme.md) — wie man ein Review fährt
- [Änderungsklassen](change-classification.md) — welche Gates eine Änderung braucht
- [Eskalationsmodell](eskalationsmodell.md) — was passiert, wenn ein Gate hält
- [CI/CD-Promotionslogik](../knowledge-base/cicd-promotion-logik-und-human-gates.md) — die Landkarte über Umgebungen hinweg
- [Concept-Development-Workflow](concept-development-workflow.md) — die Prüfschritte beim Schreiben
