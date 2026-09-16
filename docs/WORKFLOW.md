---
title: "Arbeitsablauf und Modell-Routing — Phasen und Stufen"
category: governance
status: current
created: 2026-09-05
last_reviewed: 2026-09-09
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-06"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [workflow, modell-routing, agentisches-coding, phasen, artefakte]
---

# Arbeitsablauf und Modell-Routing

> **Einstieg in einer Sitzung:** `make change NAME=<name> BEAD=<id>` legt
> `plans/changes/<name>/` an, verknüpft es mit einem Vorgang, der im Export
> **schon steht**, und verweist auf Phase 1. In Claude Code: `/workflow-start`.
> Danach: „Lies `docs/WORKFLOW.md` und arbeite nach Phase N."
> **Stand:** Stufe 1 ist verbindlich. Stufe 2 und 3 sind vorbereitet, nicht aktiv.

## 1 · Wozu

Wie in diesem Repository mit Agenten gearbeitet wird, und welches Modell welche
Phase bekommt. Der Schnitt ist so gewählt, dass **Stufe 1 sofort produktiv ist**
und die späteren Stufen ohne Umbau darauf aufsetzen.

Zwei Entscheidungen liegen allem zugrunde.

**Harness-Portabilität.** Alles Wertvolle liegt in Repo-Dateien und
Standard-Werkzeug: `AGENTS.md`, die Artefakte unter `plans/`, die Phasen-Prompts
unter `prompts/`, `Makefile`, Git-Hooks, CI. Was harness-spezifisch ist —
`.claude/agents/`, `.claude/commands/`, `.claude/hooks/` — ist ein dünner,
wegwerfbarer Komfort-Layer. Beim Wechsel auf einen anderen Harness bleibt der
Kern; neu zu bauen sind Subagent-Definitionen, Slash-Command-Wrapper und Hooks.

**Determinismus außen, Modell in der Mitte.** Erkundung und Inventarisierung sind
mechanisch. Das Modell sitzt in der Interpretations- und Entwurfsschicht.
Generierung und Verifikation sind wieder deterministisch und beliebig oft
wiederholbar. Zwischen den Schichten stehen Gates, über die nicht verhandelt wird.

## 2 · Die Phasen

Jede erzeugt ein versioniertes Artefakt im Repo. **Das Artefakt ist die Übergabe
an die nächste Phase — nicht der Chat-Verlauf.**

| # | Phase | Artefakt | Gate | Prompt |
|---|---|---|---|---|
| 1 | Explore | `plans/changes/<name>/research.md` | — | [`prompts/01-explore.md`](../prompts/01-explore.md) |
| 1a | Interview | `plans/changes/<name>/decisions.md` | jede `[DECISION]` beantwortet — oder als übersprungen begründet | [`01a-interview.md`](../prompts/01a-interview.md) |
| 2 | Spec | `plans/changes/<name>/spec.md` | Validator grün, keine offene `[DECISION]` | [`02-spec.md`](../prompts/02-spec.md) |
| 2a | Spec-Review | Zeilen für `findings.md`, Dimension `SPEC` | keine offene `[AMBIGUITY]` | [`02a-spec-review.md`](../prompts/02a-spec-review.md) |
| 3 | Plan | `plans/changes/<name>/plan.md` | Validator grün | [`03-plan.md`](../prompts/03-plan.md) |
| 4 | Implement | Code + Tests | `make verify` grün | [`04-implement.md`](../prompts/04-implement.md) |
| 5 | Verify | Testausgabe als Beleg | Stop-Hook blockt auf rotem Baum | [`05-verify.md`](../prompts/05-verify.md) |
| 6 | Review | `plans/changes/<name>/findings.md` | keine offene `[AMBIGUITY]`, kein offener BLOCKER — `[DIVERGENT]` zählt als BLOCKER | [`06-review.md`](../prompts/06-review.md) |
| 7 | Commit | Pull Request | CI grün | [`07-commit.md`](../prompts/07-commit.md) |

Phase 1a ist **optional und wird von einem Menschen gerufen**. Was in einem Satz
beschreibbar ist, braucht kein Interview; das Überspringen wird in `decisions.md`
mit einem Satz begründet, nicht verschwiegen.

Quer dazu steht die **Sitzungsübergabe** — sie gehört keiner Phase, sondern dem
Sitzungsende; siehe unten.

### Wer entscheidet was

Der Mensch ist **Absichts-Eigner**, kein technischer Prüfer. Ob etwas richtig
gebaut ist, beantworten Verify, Review und CI — nicht er.

| Ebene | Beispiel | Entscheidet |
|---|---|---|
| **Absicht** | Darf der Import alte Daten überschreiben? · Ist Ausfallzeit hinnehmbar? · externe Verträge, Risikoannahme | **Mensch** |
| **Mechanik** | Bibliothek, Algorithmus, Datenstruktur — aus `research.md` und `spec.md` ableitbar | **Modell** |
| **Detail** | Variablenname, Formatierung, Reihenfolge — beliebig revidierbar | **Agent**, begründet im Artefakt |

Daraus folgt die Trennung, die den Gates ihren Zuschnitt gibt: **ein Phasen-Gate
prüft, ob das Artefakt da und vollständig ist — das kann eine Maschine, und seit
`validate_change_artefacts.py` tut sie es.** Was ein Mensch bekommt, ist nur noch
das, was tatsächlich offen ist. Das Gate wird dadurch mechanischer, nicht
bürokratischer.

### Der Befundprozess

Ein Review-Ergebnis ist eine Tabelle, kein Fließtext — Form und Vokabular,
Schweregrade (`BLOCKER`/`MAJOR`/`MINOR`) eingeschlossen, stehen in
[`templates/findings.md`](../templates/findings.md) und werden hier nicht
zweimal geführt. Ohne feste Form ist eine Review-Runde nicht wiederaufnehmbar,
und niemand sieht, ob ein Befund aus dem Bau stammt oder aus der Reparatur
davor.

Zwei Spalten tragen dabei mehr, als sie aussehen. **Dimension** trennt `SPEC`
(gegen die Spec gemessen) von `MAINT` (der Blick eines Fremden auf
Fehlerbehandlung, Kantenfälle und Außenverträge) — eine Spec sieht ihre eigenen
Lücken nicht. **Origin** hält fest, ob ein Befund vorher bestand (`base`) oder
von einer Reparaturrunde erzeugt wurde (`fix-r<N>`); zwei aufeinanderfolgende
Runden mit `fix-r`-Ursprung sind eine Eskalation und keine dritte Runde. Das ist
die mechanische Form dessen, was vier Reparaturrunden gezeigt haben: jeder
Defekt der Runden zwei bis vier stammte aus einem Umbau, keiner aus einer
kleinen Änderung.

**Meinungsverschiedenheiten werden protokolliert, nicht aufgelöst.** Dass ein
Reviewer etwas markiert und ein anderer nicht, *ist* die Information; sie zu
einem Urteil zu verrechnen wirft sie weg.

### Das Fragen-Protokoll

Jede Unklarheit wird eingeordnet, **bevor** gefragt wird:

```
[DECISION] → Mensch   unumkehrbar · externer Vertrag · Risiko · oder zwei
                      plausible Lesarten dessen, was verlangt wurde
[GAP]      → Erkunden  im Repo beantwortbar → research.md ergänzen, nicht fragen
[DETAIL]   → Agent    beliebig revidierbar → selbst entscheiden, Grund ins Artefakt
```

Wer keine Empfehlung abgeben kann, hat eine Fachlücke, keine Entscheidung — und
liest zuerst nach. Eine Mechanikfrage an den Absichts-Eigner ist ein Verstoß
gegen das Protokoll, keine Gründlichkeit: genau daran ist eine frühere Sitzung
gescheitert, als Fragen gestellt wurden, die technisch zu tief lagen, um
beantwortbar zu sein.

Die Form einer Menschenfrage steht in
[`prompts/02-spec.md`](../prompts/02-spec.md): Ziel in einem Satz, Optionen als
**Folgen** statt als Mechanismen, Empfehlung mit Grund, und was passiert, wenn
die Antwort „ok" lautet. Das ist der Entscheidungs-Record (MADR) in Frageform.

**Eine Zweideutigkeit ist keine Mechanik.** „Der Plan ist der Vertrag" regelt
Abweichungen von einem *eindeutigen* Vertrag. Lässt der Plan zwei Lesarten zu,
wird nicht gewählt — der Vermerk lautet `[DECISION]`, der Rest wird fertig,
dann Halt.

### Die achte Bewegung: die Sitzungsübergabe

Die sieben Phasen sind der Zyklus **einer Änderung**. Die Sitzungsübergabe läuft
quer dazu: sie schließt **eine Sitzung** ab, und die endet selten dort, wo eine
Änderung endet. Kontext voll in Phase 4, Feierabend zwischen Spec und Plan, ein
Review, das über Nacht wartet — jedes Mal ist der nächste Leser eine Sitzung
ohne Gedächtnis.

| Wann | Artefakt | Gate |
|---|---|---|
| Sitzungsende, unabhängig von der Phase | `docs/journal/handover/<datum>-<name>.md` nach [`templates/handover.md`](../templates/handover.md) | Frontmatter gegen `scripts/handover_schema.py`; Richtung, Provenienz und Stand des Ziels sind Pflicht |

Es gelten dieselben zwei Regeln wie für die Phasen-Artefakte, aus demselben
Grund:

**Die Übergabe ist die Datei, nicht der Chat.** Was nur im Verlauf steht, ist
für die nächste Sitzung nicht passiert. Der Grund ist derselbe wie bei `/clear`
zwischen Phase 3 und 4 — nur dass hier niemand die Wahl hat.

**Jede Zahl trägt ihren Stand.** Eine Übergabe altert bauartgemäß; sie wird
angehängt, nie überschrieben. Eine Zahl ohne Commit oder Datum liest sich beim
nächsten Lesen wie eine aktuelle Messung und ist eine historische — der
häufigste Weg, auf dem ein Verlaufsdokument zur Falschaussage wird.

### Die fünf Regeln, die den Unterschied machen

**`/clear` zwischen Phase 3 und 4.** Der Plan ist eine Datei. Der Ausführende
braucht den Planungskontext nicht, nur `plan.md` und `spec.md`. Frischer Kontext
schlägt Kontinuität. Ab etwa 60 % Kontextauslastung ohnehin neue Sitzung.

**Nie planen, was in einem Satz beschreibbar ist.** Tippfehler, Umbenennung,
offensichtlicher Bugfix: direkt machen. Sonst frisst der Phasen-Overhead den
Nutzen, und der Ablauf wird als Bürokratie erlebt statt als Werkzeug.

**Der Plan ist der Vertrag.** Weicht die Umsetzung ab, wird der Plan *revidiert*
— nicht stillschweigend überschrieben. Der Agent hält an und meldet: erwartet /
gefunden / warum relevant / wie weiter. Eine Abweichung, die nur im Code steht,
ist beim nächsten Lesen keine Abweichung mehr, sondern der Plan.

**Ein Gate ist sinnvoll, verhältnismäßig und mehr als ein Selbstzweck.** Die
Checkliste dafür steht einmal, in
[`gate-catalog.md`](governance/gate-catalog.md#bevor-ein-gate-scharfgestellt-wird)
— hier nicht zweimal geführt, mit einer Lücke, die diese Datei schon einmal
gekostet hat. Nur die Gates von Phase 2 und Phase 3 sind reine
Präsenz-Checklisten — *ist es da?* —, gefahren als eine Zeile, die mit dem
nächsten Schritt endet, durch `validate_change_artefacts.py`. Phase 4 fragt
`make verify` (rot ist rot), Phase 5 den Stop-Hook, Phase 6 den Abgleich gegen
`spec.md`, Phase 7 die CI — vier Urteile, keine Präsenzprüfungen: ein roter
Lauf ist kein „nicht da", sondern das Gate, das greift. Offene Entscheidungen
sind etwas anderes: erst einordnen, dann fragen. Umkehrbares wird entschieden
und mit Grund ins Artefakt
geschrieben; das Veto ist ein Wort. Unumkehrbares wird gefragt — als Frage mit
Entscheidungshilfe, in der Form aus [`02-spec.md`](../prompts/02-spec.md).
Nichts davon ist hier erfunden: Stage-Gate (Cooper) gibt jedem Gate die Option
*Kill*, PRINCE2 steuert nach Ausnahmen innerhalb vorher gesetzter Toleranzen,
und die Unterscheidung umkehrbar/unumkehrbar ist Bezos' Zwei- gegen Einwegtür.

**Texte für Menschen tragen ihren Sinn selbst.** Eine Frage, ein Befund, ein
PR-Text, ein Commit-Rumpf wird von jemandem gelesen, der die Sitzung nicht
gesehen hat und die Artefakte nicht daneben offen hat. Bead-Kennungen,
Spec-Punkte, Invarianten-Nummern sind Kürzel des Schreibers — als Nachsatz in
Klammern, nie als Träger des Satzes. Die Probe: ein Satz, der nur mit `plan.md`
daneben Sinn ergibt, wird umgeschrieben. Das sind Nielsens zweite und sechste
Heuristik — die Sprache des Nutzers, Wiedererkennen statt Erinnern — und die
Form der Frage ist die des Entscheidungs-Records (ADR/MADR): Kontext, Optionen
mit Folgen, Empfehlung.

### Artefakt-Lebenszyklus

```
plans/specs/<capability>/spec.md          LEBEND      — was heute gelten soll
plans/changes/<name>/                     AKTIV       — eine Änderung in Arbeit
plans/changes/archive/YYYY-MM-DD-<name>/  HISTORISCH  — abgeschlossen
docs/adr/NNNN-titel.md                    DAUERHAFT   — append-only
```

Zwei getrennte Statusfelder: `status` bewegt sich, wenn das Projekt entscheidet;
`implementation_status`, wenn der Code sich bewegt. Ein Feld für beides kann
nicht sagen, ob eine akzeptierte Spec noch ungebaut ist oder ob gebauter Code auf
einer zurückgezogenen Spec steht — und genau das sind die interessanten Fälle.

Nach Abschluss: Delta in die lebende Capability-Spec, dauerhafte
Architekturentscheidungen als ADR, Rest ins Archiv. **Eine implementierte
Feature-Spec bleibt nicht als lebendes Dokument stehen** — Code und Git-Historie
sind die Wahrheit. Details in [`plans/_README.md`](../plans/_README.md).

Die **Regel gegen Mehrfacherzeugung** steht wörtlich in `AGENTS.md`, weil ein
Agent `plans/_README.md` nicht zwangsläufig liest: vor dem Anlegen eines
Artefakts erst per `rg` suchen; existiert eines, wird es aktualisiert.
`make staleness` prüft die Folgen — fehlendes Frontmatter, widersprüchlicher
Status, fertig und nie archiviert, einseitige Ablösung.

## 3 · Stufe 1 — nur Claude Code, nur Anthropic

### Was dafür im Repo steht

| Baustein | Wo | Was er tut |
|---|---|---|
| Instruktionen | `AGENTS.md` | die eine Quelle; `CLAUDE.md` importiert sie mit `@AGENTS.md` |
| Artefakte | `plans/` | `specs/` · `changes/` · `changes/archive/` |
| Phasen-Prompts | `prompts/` | harness-unabhängig |
| Einstiegsbefehle | `Makefile` | `change` · `verify` · `gates` · `test` · `staleness` · `index` |
| Der Aufruf | `scripts/new_change.py` | legt den Änderungsordner an; verlangt einen vorhandenen Bead, legt keinen an |
| Hygiene | `scripts/plans_registry.py` | `--check` meldet, `--index` erzeugt `plans/INDEX.md` |
| Subagents | `.claude/agents/explorer.md`, `reviewer.md` | read-only, Modell gepinnt |
| Stop-Hook | `.claude/hooks/session-stop/check-tests-green.sh` | blockt das Turn-Ende auf rotem Baum |
| Erzwingung | `.github/workflows/ci.yml` | **die eine Gate-Liste** |

### Verifikation läuft über Git und CI, nicht über den Harness

```bash
make verify     # alle lokal ausführbaren Gates — dieselben, die die CI fährt
make gates      # was die CI fährt, aus ci.yml gelesen
make staleness  # Hygiene der plans/-Artefakte
make index      # plans/INDEX.md neu erzeugen
```

`make` hält **keine eigene Liste**. Es ruft `scripts/verify_all.sh`, das
`scripts/ci_gates.py` fragt, das `.github/workflows/ci.yml` liest. Eine zweite
Liste ist der Grund, warum lokal und CI auseinanderlaufen — nicht ihr Symptom.

Der Stop-Hook ist der Komfort-Layer, nicht die Erzwingung. Er läuft nur, wenn
seit `HEAD` Python angefasst wurde: ein Hook, der eine Minute kostet, wenn
nichts passiert ist, wird binnen einer Woche abgeschaltet — und ein
abgeschalteter Hook ist schlechter als keiner, weil die Registry ihn weiter als
Schutz zählt.

### Modell-Routing

| Phase | Modell | Warum |
|---|---|---|
| 1 Explore | **Haiku 4.5** | viel Input, wenig Output, kein tiefes Reasoning |
| 1a Interview | **Fable 5.1** | die Fragen sind die Arbeit, und es sind wenige |
| 2 Spec | **Fable 5.1** | höchster Reasoning-Bedarf, wenig Output |
| 2a Spec-Review | **Opus 5** | ein anderes Modell mit anderem Fehlerprofil, und ein frischer Kontext, der den Denkweg des Autors nicht kennt |
| 3 Plan | **Fable 5.1** | ein Fehler hier ist der teuerste im ganzen Ablauf |
| 4 Implement | **Sonnet 5** | solider Arbeiter bei klarem Plan |
| 5 Verify | — | deterministisch |
| 6 Review | **Opus 5** | findet, was Sonnet übersieht |
| 7 Commit | **Haiku 4.5** | billig und ausreichend |

Umschalten mit `/model fable`, `/model sonnet`, `/model opus`, `/model haiku`.
Der Alias `opusplan` fährt Opus in der Planung und wechselt zur Ausführung auf
Sonnet — die Sparvariante zu Fable.

**Kostenlogik.** Fable läuft nur in den Phasen mit wenig Output. Der
token-intensive Teil läuft auf Sonnet.

**Nach dem Setup prüfen.** Es gibt Berichte, nach denen das `model:`-Feld in
Subagent-Definitionen ignoriert wird und Subagents auf dem Parent-Modell laufen.
Einmal mit `/status` nachsehen — sonst zahlt man Opus-Preise für Exploration.

**Eskalation.** Nach zwei fehlgeschlagenen Review-Runden auf Fable hochstufen.
Bei Umbauten über ~200k Token und bei Code mit Sicherheits- oder
Nebenläufigkeitsbezug direkt Fable. Nach bestandenem Review zurück auf Sonnet.

### Was in Stufe 1 bewusst nicht passiert

Kein `ANTHROPIC_BASE_URL`, kein Router, kein Gateway. Kein Framework-Overlay —
erst den nackten Prozess verstehen. Keine tiefe Subagent-Verschachtelung. Kein
Embedding- oder Graph-Index: `rg` plus gutes Naming plus das erzeugte
`plans/INDEX.md` reichen bis etwa 50.000 Zeilen.

**Korrigiert am 06.09.:** Hier stand ein Verbot von Arbeitsbäumen und
Parallelisierung. Beides war falsch. `bd worktree create` ist ein Kommando des
Trackers, und seine eigene Hilfe nennt als Zweck ausdrücklich *„multiple agents
or features"* bei geteilter Bead-Datenbank; am Hauptcheckout dieses Repos hängen
mehrere Arbeitsbäume — die Zahl sagt `git worktree list`, sie gehört nicht in
eine Doktrin. Eine Regel, die verbietet, was das Werkzeug anbietet und die
Praxis täglich tut, wird nicht befolgt — sie wird überlesen, und mit ihr der
Rest des Absatzes.

Was stattdessen gilt: **ein Arbeitsbaum je Änderung — unter einer Bedingung mit
zwei Hälften.**

1. **Jeder Arbeitsbaum sieht denselben Trackerstand.** Das trägt die Bauart des
   Werkzeugs: der Store wird über das gemeinsame Git-Verzeichnis gefunden, nicht
   kopiert. Zwei Bäume schreiben in dieselbe Datenbank.
2. **Der getrackte Export bewegt sich nur um das, was eine Sitzung getan hat.**
   Das trägt heute **nichts** — es ist dreimal in vier Tagen gebrochen worden,
   zuletzt am 06.09. mit Konfliktmarkern in genau der Datei, die jedes Bead-Gate
   als Quelle liest.

Solange Hälfte 2 offen ist, ist die Erlaubnis eine Absichtserklärung und kein
Zustand. Was hier wirklich nicht passiert, ist gleichzeitiges Schreiben *am
selben Vorgang* — das ist keine Werkzeugfrage, sondern Arbeitsteilung.

**Und woraus Isolation hier besteht** — drei Dinge, kein viertes:

1. **Der Arbeitsbaum.** Trennt die Dateien. Ein `git worktree add` je Änderung;
   was dort schiefgeht, betrifft den Hauptcheckout nicht.
2. **Die Sandbox des Harness.** Trennt die Ausführung. Sie ist eine Eigenschaft
   der Umgebung, kein Artefakt in diesem Repo — es gibt nichts zu installieren
   und nichts zu konfigurieren.
3. **`permissions.deny` in `.claude/settings.json`.** Bremst das Unumkehrbare:
   Prod-Deploy, `bundle destroy`, Force-Push, `rm -rf`, und die Entscheidungen
   unter `docs/decisions/`. Deny überlebt jeden Permission-Mode — aber die
   pfadgebundenen Regeln greifen nur bei `Write` und `Edit`. **Ein Schreibzugriff
   über `Bash` fällt durch sie hindurch** (`echo … >> docs/decisions/x.md`). Das
   ist eine Bremse gegen Versehen, keine Sperre gegen Absicht; wer sie für eine
   Sperre hält, verlässt sich auf etwas, das es nicht gibt.

**Kein Container gehört dazu.** Weder `container-use` noch Dagger noch ein
Devcontainer ist Betriebsmittel dieses Repos; das Konzeptdokument zu Dagger
beschreibt eine Technik, es benutzt sie nicht. `tests/test_repo_settings.py`
hält den Zaun: ein getracktes `Dockerfile`, `devcontainer.json`, `dagger.json`
oder `docker-compose*` lässt die Suite fallen.

## 4 · Stufe 2 — GLM und Kimi ergänzen (vorbereitet, nicht aktiv)

Es ändern sich genau zwei Zeilen der Routing-Tabelle: **Implement** von Sonnet 5
auf GLM, **Review** von Opus 5 auf Kimi. Die Phasen 1–3 und 7 bleiben bei
Anthropic.

**Warum Review über Anbietergrenzen.** Unterschiedliche Trainings-Linien haben
nicht überlappende blinde Flecken. Schon die Kontexttrennung findet messbar mehr
Fehler; Anbietervielfalt legt drauf. Ein Modell bewertet eigene Erzeugnisse zu
positiv — ein Reviewer aus einem anderen Haus weiß bauartbedingt nicht, dass er
sich selbst prüft. **Meinungsverschiedenheiten werden protokolliert, nicht
automatisch aufgelöst.** „Kimi hat es markiert, GLM nicht" ist die Information.

### Mechanik

`ANTHROPIC_BASE_URL` gilt sitzungsweit und lässt sich mitten in einer Sitzung
nicht wechseln. Ein Profil ist deshalb ein Prozess, kein Schalter: sechs Skripte
unter `scripts/cc-*.sh` über einer gemeinsamen Basis, jedes startet seine eigene
Sitzung. Jede `ANTHROPIC_*`-Variable wird ausdrücklich gesetzt — ein Kind-Prozess
erbt sonst die des Eltern-Profils und arbeitet weiter, nur gegen den falschen
Anbieter. `tests/test_model_profiles.py` misst das mit einer Attrappe, statt es
zu glauben.

**Die Barriere, ohne die nichts läuft:** `make leakcheck NAME=<change>` scannt
die Artefakte der Änderung und den Diff gegen die Basis, bevor irgendetwas an
einen fremden Endpunkt geht. Jedes Fremdprofil ruft sie selbst und hält an, wenn
`CC_CHANGE` fehlt — ohne benannte Änderung gibt es nichts zu scannen. Die
Denylist liegt außerhalb des Repositoriums; fehlt sie, ist das BLOCK, denn
ungeprüft ist nicht dasselbe wie sauber.

**Die Zuordnung steht im Plan.** Jeder Teilschritt trägt genau eine Markierung —
`[FLASH]`, `[GLM5.3]` oder `[SONNET]`, Entscheidungsregeln in
[`templates/plan-marking.md`](../templates/plan-marking.md). `scripts/run_change.sh`
gruppiert aufeinanderfolgende gleiche Markierungen zu einem Segment und fährt
jedes als eigene Sitzung mit Verify-Gate danach. Eine unmarkierte Zeile wird
ignoriert und nicht geraten: der unvollständige Plan ist dann ein Befund am
Plan-Gate, wo ein Mensch ihn annimmt, keine Überraschung zur Laufzeit.

Der Orchestrator hält **kein zweites Regelwerk**. Arbeitsbaum-Vorbedingung,
Leakcheck, `make verify` und das Artefakt-Gate leben außerhalb und werden
gerufen. Eine offene `[AMBIGUITY]`, ein offener BLOCKER- oder MAJOR-Befund
pausieren mit Exit 2, statt entschieden zu werden.

### Die Sicht auf wartende Agenten

Weder ein Terminal-Multiplexer noch eine Agentenschicht isoliert etwas.
Isolation kommt aus dem Arbeitsbaum, der Harness-Sandbox und `permissions.deny`
(siehe oben). Was fehlt, ist etwas anderes: **Sichtbarkeit des Wartens** — der
Moment, in dem ein Agent eine `[DECISION]` gestellt hat und stillsteht.

`--mode herdr` nutzt dafür [herdr](https://github.com/herdrdev/herdr), das vier
Agentenzustände kennt — `working`, `blocked`, `done`, `idle` — und sie bei Claude
Code über Integrationshooks liest statt über Bildschirm-Parsing. `blocked` ist
genau das, was das Fragen-Protokoll erzeugt; bei mehreren parallelen Läufen sieht
man auf einen Blick, welcher auf einen Menschen wartet.

**Es ist Werkzeug des Menschen, keine Abhängigkeit des Ablaufs.** Fehlt das
Binary, läuft der Orchestrator headless weiter und sagt es. Ein junges Werkzeug
darf den Betrieb nicht dadurch anhalten, dass es nicht installiert ist — und die
Landschaft dieser Werkzeuge ist jung: von den 2026 verbreiteten Orchestratoren
sind mehrere bereits eingestellt oder in Freiwilligenpflege übergegangen.
Die Übergabe läuft über Dateien — die fremde Sitzung startet mit
`@plans/changes/<name>/plan.md @plans/changes/<name>/spec.md` und braucht sonst
nichts. Genau dafür ist der Plan eine Datei.

> **Zwei Vorbehalte, und der zweite gilt hier besonders.** Die Coding-Abos der
> Anbieter sind vertraglich auf offiziell unterstützte Werkzeuge beschränkt; in
> Claude Code ist das gedeckt, in einem selbstgebauten Harness nicht.
>
> **Und: dieses Repository enthält abstrahiertes Wissen aus einem produktiven
> Kundenprojekt.** An Endpunkte außerhalb der eigenen Rechtsordnung gehen keine
> Kundennamen, Schemas, Entity-Namen oder Kennzahlen — auch nicht in einem
> Diff, auch nicht in einem Plan. Wer Stufe 2 anschaltet, prüft vorher, was in
> `spec.md` und `plan.md` steht. Die Denylist aus dem Export-Werkzeug ist dafür
> der richtige Maßstab.

## 5 · Stufe 3 — Meta-Harness (evaluativ)

Ersetzt nicht den Prozess, sondern das manuelle Sitzungs-Jonglieren aus Stufe 2:
ein Agent wird eine kurze YAML-Datei, die `AGENTS.md` als `instructions:`
referenziert, den Anbieter in einer `harness:`-Zeile umschaltet und die
Phasen-Rollen aus `prompts/` eins zu eins übernimmt. Ein Orchestrator verteilt
die Umsetzung auf parallele Worktrees und routet jeden Diff automatisch an einen
Reviewer eines anderen Anbieters. Policies können `make verify` als hartes Gate
und Kostenbudgets mitten in der Sitzung erzwingen.

Nicht produktiv gesetzt.

## 6 · Reihenfolge, und warum sie so ist

**Prozess, dann Modellvielfalt, dann Orchestrierung.**

Wer mit der Orchestrierung anfängt, debuggt Infrastruktur statt Ablauf und weiß
bei schlechten Ergebnissen nicht, ob Plan, Modell oder Harness schuld war. Wer
mit Multi-Anbieter anfängt, bevor die Artefakt-Übergabe sitzt, verliert beim
Wechsel Kontext und schiebt es auf das Modell.

Stufe 1 muss zwei bis drei Wochen im echten Betrieb gelaufen sein. **Signal für
den Wechsel:** die Phasen-Gates greifen ohne Nachdenken, und die
Sonnet-Umsetzung ist der spürbare Kostenblock.

## 7 · Was pro Stufe erhalten bleibt

| Baustein | Stufe 1 | Stufe 2 | Stufe 3 |
|---|---|---|---|
| `AGENTS.md` | ✅ | ✅ unverändert | ✅ als `instructions:` |
| `plans/`-Artefakte | ✅ | ✅ unverändert | ✅ unverändert |
| `prompts/` | ✅ | ✅ als Text | ✅ als YAML-Prompt |
| `Makefile`, CI, Git-Hooks | ✅ | ✅ unverändert | ✅ als Policy-Gate |
| `.claude/agents/` | ✅ | ❌ neu bauen | ❌ ersetzt durch YAML |
| `.claude/commands/` | ✅ | ❌ neu bauen | ❌ ersetzt durch YAML |
| Claude-Code-Hooks | ✅ | ❌ neu bauen | ❌ ersetzt durch Policies |

Die untere Hälfte ist bewusst dünn. Das ist der Preis, den man einmal zahlt, und
der Grund, warum die obere Hälfte den Wechsel überlebt.

## 8 · Abweichungen von der Vorlage — und warum

Sechs Punkte weichen bewusst von der ursprünglichen Übergabe ab. Sie stehen hier,
damit die Abweichung eine Entscheidung bleibt und nicht als Versehen gelesen wird.

| Vorlage | Hier | Grund |
|---|---|---|
| `Makefile` mit `lint`, `typecheck`, `test` | `make verify` ruft nur `verify_all.sh` | `ci.yml` ist die eine Gate-Liste (`AGENTS.md`). Eine ausgeschriebene Prüfreihenfolge im Makefile **wäre** die zweite Liste. |
| `ln -s AGENTS.md CLAUDE.md` | `CLAUDE.md` = `@AGENTS.md` + deutsches Addendum | Das Addendum trägt die Konversationssprache und die Slash-Commands. In einem Symlink kann es nicht existieren. |
| `.pre-commit-config.yaml` | nicht angelegt | Es wäre eine zweite Lint-Liste neben `ci.yml`, mit demselben Drift-Risiko. Die Erzwingung liegt bei `ci.yml` und `.claude/hooks/`. |
| `.mcp.json` | nicht angelegt | Dieses Repository nutzt heute keinen MCP-Server. Eine leere Konfiguration wäre eine Behauptung ohne Inhalt. |
| `uv`, `mypy` | `python3`, `ruff`, `pytest` | Das ist die Werkzeugkette, die in `requirements-ci.txt` gepinnt ist und die die CI fährt. |
| Task-Verfolgung im Artefakt | Beads (`bd`) | `AGENTS.md`: Beads only. Die Artefakte sagen **was** gebaut wird, der Tracker sagt **wo es steht**. |

## 9 · Stand und nächste Schwellen

Stufe 1 ist eingerichtet. Was noch aussteht, gehört einem Menschen:

- Einmal `/context` und `/status` prüfen: lädt `AGENTS.md`, greift die
  Modellzuweisung der Subagents?
- Den ersten echten Task durch alle sieben Phasen schicken und Spec und Plan als
  Dateien erzwingen — nicht als Chat.
- Nach zwei Wochen `plans/` auditieren: gibt es widersprüchliche oder verwaiste
  Artefakte? `make staleness` beantwortet den mechanischen Teil davon.

**Schwellen, die den Kurs ändern.** Über etwa 30 Artefakte die Archivierung
verschärfen. Findet das Modell trotz gutem Naming wiederholt Dateien nicht,
einen LSP-MCP ergänzen — und erst wenn das nicht reicht, über einen semantischen
Index nachdenken.
