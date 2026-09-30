---
name: handover
description: Schreibt die Sitzungsübergabe als Datei im Repository nach dessen Konvention (coding-harness und portfolio - docs/journal/handover/ mit Schema; lakeswitch - journal/), öffnet dafür immer einen Pull Request und verlinkt beides. Verwenden, wenn die Person die Session beenden oder neu starten will, „Übergabe“, „Schluss für heute“, „ich mache Feierabend“ oder „handover“ sagt, oder bevor der Kontext knapp wird.
---

# Übergabe schreiben

Die Übergabe ist die Datei, nicht der Chat. Die nächste Session muss allein aus
ihr weiterarbeiten können, ohne dass die Person den Kontext wiederholt.
Grundlage: `~/coding-harness/AGENTS.md`, Abschnitt „Communication and session
continuity“, und `~/coding-harness/templates/handover.md`. Wo das Repository
selbst etwas anderes regelt (AGENTS.md, CLAUDE.md, Provenienz-Regeln), gilt das
Repository.

## 1. Konvention des Repositorys feststellen

```bash
~/.claude/hooks/handover.sh where
```

- `harness <dir>`: neue Datei `<dir>/JJJJ-MM-TT-<thema>.md` mit Frontmatter (3a).
- `journal <dir>`: neue Datei `<dir>/JJJJ-MM-TT-<thema>.md` ohne Frontmatter;
  der Ordner ist nur zum Anhängen da (3b).
- `none`: die Person einmal fragen, ob `docs/journal/handover/` nach der
  Harness-Konvention angelegt oder die Übergabe privat unter
  `~/.claude/handover/<repo>/` abgelegt werden soll. Keine andere Struktur
  erfinden.

Die Ausgabe listet die jüngsten Übergaben. Lies die neueste, bevor du schreibst.

## 2. Den Stand messen statt ihn zu erinnern

Jede Aussage trägt ihren Stichtag (Datum, Commit).

- `git status --short`, `git branch --show-current`, `git rev-parse --short HEAD`,
  Abstand zum Upstream
- offener Pull Request, wenn `gh` da ist: `gh pr view --json number,url,state,isDraft`
- Beads in Arbeit, nur lesend (mit dem Wrapper `tools/bd`, falls vorhanden):
  Titel, ID in Klammern
- parallele Sessions: `~/.claude/hooks/session-scan.sh "${CLAUDE_SESSION_ID}" "$PWD"`
  (Spalte 1 `clash` = selber Checkout)
- was diese Session geprüft hat (Tests, verify), und was nicht

Was nicht gelesen werden konnte, steht als „nicht gelesen“ drin, nie als „keine“.

## 3. Schreiben

Die Datei ist in der Sprache des Repositorys geschrieben: in coding-harness,
portfolio und lakeswitch ist das Englisch. Mit der Person sprichst du Deutsch.

Gibt es von heute schon eine Übergabe zum selben Thema, hängst du einen
**Nachtrag** an (`## Addendum — JJJJ-MM-TT, <Anlass>`). Frühere Abschnitte
bleiben, wie sie sind.

Die Reihenfolge der Abschnitte ist fest. Die ersten drei tragen den Einstieg
der nächsten Session, und der Start-Hook liest den Abschnitt „Next step“.

1. `# Resume here`
2. `## Where we are`: Ziel und Stand, drei bis fünf Sätze
3. `## Next step`: genau eine konkrete Handlung zum Wiedereinstieg
4. `## Needed from the maintainer`: offene Entscheidung als Frage mit
   Empfehlung und Folge, sonst „Nothing right now.“
5. `## Decisions and preferences`: was entschieden ist und nicht noch einmal
   gefragt wird
6. `## Open work and blockers`: Der Aufgabenstatus bleibt in Beads. Hier wird
   darauf verwiesen, nichts dupliziert.
7. `## Working state and parallel-session boundary`: Branch, Commit, Pull
   Request, Worktrees, uncommittete Dateien, andere Sessions und wem was gehört
8. `## Validation`: was lief, mit Datum und Commit, und was nicht lief

### 3a. Frontmatter (harness)

Die Feldliste steht in `scripts/handover_schema.py` des Repositorys, falls
vorhanden, sonst in Variante A (Variant A) von `templates/handover.md`:

```yaml
---
title: "Session handover — <topic>, <JJJJ-MM-TT>"
category: handover
created: <JJJJ-MM-TT>
updated: <JJJJ-MM-TT>
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "<JJJJ-MM-TT>"
tags: [handover, <topic>]
target_ref: <kurzer HEAD>
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---
```

### 3b. journal/ (lakeswitch)

Kein Frontmatter (`decisions/provenance.yaml`: `frontmatter: none`). Nur neue
Dateien anlegen oder am Ende anhängen.

## 4. Regeln

- Ein Satz muss ohne diese Session verständlich sein. Bead-IDs und Dateinamen
  stehen in Klammern hinter der Aussage, nie als ihr Träger.
- Keine Zahl ohne Stichtag. Nichts behaupten, was nicht gelesen wurde.
- Keine Schreibvorgänge im Tracker, solange eine andere Session im selben
  Repository läuft (one-writer rule).
- **Die Übergabe kommt immer als Pull Request**, ohne Rückfrage (Regel der
  Person vom 27.09.2026). Sie entsteht in einem eigenen Worktree auf einem
  eigenen Branch vom aktuellen `main` (coding-harness: `.claude/worktrees/<name>`,
  Branch `docs/handover-<datum>-<thema>`; lakeswitch: `~/lakeswitch-wt/<name>`,
  Branch `docs/journal-<datum>-<thema>`; in einem Repository, das keinen Ort
  nennt: `.claude/worktrees/<name>`), nie im Haupt-Checkout. Committen,
  pushen und den Pull Request öffnen gehören zur Übergabe. **Mergen tut nur
  die Person.**
- Commit-Nachricht und PR-Text sind Englisch, mit der Attribution, die das
  Repository verlangt. Nachricht über eine Datei (`git commit -F`), nie mit
  Heredoc oder `-m`, wenn sie einen geschützten Namen nennt.
- Ausnahme: Hat das Repository keinen Remote oder läuft eine andere Session im
  selben Checkout, wird die Datei geschrieben, aber nicht committet, und die
  Schlussnachricht sagt, warum.

## 5. Prüfen und abschließen

1. Die Prüfung des Repositorys, falls es eine hat: in coding-harness und
   portfolio `python3 -m pytest tests/test_feedback_channel.py -q`, in
   lakeswitch `lakeswitch verify`.
2. Vorschau des Einstiegs, den die nächste Session sieht:
   `~/.claude/hooks/handover.sh show`
3. Committen, pushen, Pull Request öffnen (Abschnitt 4). Der PR-Text sagt, was
   die Übergabe festhält und dass `verify` gelaufen ist.
4. Schlussnachricht an die Person, ADHS-gerecht: zuerst das Ergebnis, dann der
   **Link zur Übergabe-Datei und zum Pull Request**, der nächste Schritt und
   der Hinweis, dass der Merge bei ihr liegt.
