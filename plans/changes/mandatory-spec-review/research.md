---
title: "Research — mandatory-spec-review"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-ttic
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-17", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# mandatory spec review — Research

Stage-2 call, 2026-11-17: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1110 files, 4538 commits, 12 rules.

## Runner exploration — 2026-11-17

Die Exploration ist abgeschlossen. Hier ist die Recherche, bereit zum Anhang an `plans/changes/mandatory-spec-review/research.md`:

---

## Was es heute gibt

**Die Phase und ihr optionaler Status.** Phase 2a (Spec review) läuft auf Opus 5.5 in einem neuen Kontext, der nie die Begründung des Autors gesehen hat, mit schreibgeschützten Tools, und schreibt Zeilen der Dimension `SPEC` in den `findings.md` des Changes (`prompts/02a-spec-review.md`, Model-Zeile; `docs/WORKFLOW.md` §3 Modell-Tabelle, Zeile „2a Spec review“). Die Übersichtstabelle auf einem Bildschirm in `AGENTS.md` markiert die Phase als `2a | Spec-Review *(optional)*` mit der Gate-Formulierung „no open `[AMBIGUITY]`“. Die Phasentabelle in `docs/WORKFLOW.md` §1 führt dieselbe Phase ohne den Marker „(optional)“ und gibt das Gate mit „every row worked into the spec or rejected with a reason; no open `[AMBIGUITY]`“ wieder — die beiden Überschriften stimmen mit ihrem Wortlaut nicht überein (gelesen, ungelöst).

**Klassenabhängige Verriegelung, nur in der Doktrin.** Die Tabelle „Which change gets what“ in `docs/WORKFLOW.md` §4 routet die Reviews: ein Ein-Satz-Change oder ein `spike` erhält „no stage 2“, ein `bounded` Change erhält den Spec Review „Opus 5.5, where one is held“, ein `feature`- oder `architectural`-Change erhält „Opus 5.5“. Direkt darunter steht: „**Nothing checks a change's class beyond explore.** Ein `feature`, das als `spike` deklariert ist, überspringt jede Stage-2-Review, und ein als `bounded` deklarierter überspringt möglicherweise den Spec Review, der dort optional ist; nur die Review vor dem Merge fängt beides ab. Wer den Change ausführt, führt die Verben aus, die seine Zeile zulassen.“ Die Klasse selbst wird nur bei `explore` deklariert und überprüft — über das explizite Argument `--class` und die Header von `research.md` und `spec.md`, die alle übereinstimmen müssen, bevor ein Modell aufgerufen wird, sonst wird abgelehnt (`docs/WORKFLOW.md` §4, Routing-Absätze). Der Frontmatter-Matter dieses Changes in `plans/changes/mandatory-spec-review/research.md` enthält kein `class:`-Feld (gelesen: Titel, Status, Implementierungsstatus, Datum, zuletzt überprüft, aktualisiert, ersetzt, ersetzt durch, Bead, Eigentümer, Provenienz, Tags).

**Keine mechanische Durchsetzung existiert.** Eine Suche nach `AMBIGUITY` über `scripts/` findet keine Datei — die Gate-Sätze „no open `[AMBIGUITY]`“ der Phasen 2a und 6 sind rein textliche Doktrin, ohne alles andere als ein menschliches Lesen. Die einzigen Code-Leser einer `## Phase 2a` Überschrift sind: `spec_review` in `scripts/stage2.py` (der Verb selbst), `recorded_2a_session` im selben File (entscheidet, ob Phase 6 einen aufgezeichneten Codex-2a-Block fortsetzen kann; ein Block mit der Überschrift `Opus 5.5` wird nie fortgesetzt) und `_section` in `scripts/stage2_runs.py` (der Zählmechanismus, der 2a-Zeilen nach Schweregrad in `Counts.spec_review` einliest; das Tool „zählt; es wendet keine Regel an“ gemäß `docs/WORKFLOW.md` §4, „Measuring the first three stage-2 runs“). Keine Ablehnung von `implement`, `review` oder einem Merge wegen eines fehlenden 2a-Blocks wurde gefunden (suchte nach `Phase 2a` über `scripts/`). Die Verbindungen, die existieren, sind Modellanweisungen: `DRAFT_RULES` in `scripts/stage2.py` teilt dem zweiten `draft`-Aufruf mit, offene 2a-Zeilen in `spec.md` einzuarbeiten, und `prompts/06-review.md` fordert den Phase-6-Reviewer auf, zuerst zu prüfen, ob jede 2a-Zeile im überarbeiteten Spec angekommen ist.

**Der Verb und seine Preflight-Anforderungen.** `spec_review` (`scripts/stage2.py`, bei ~3656, eingetragen in `VERBS` bei ~11274, Verwendungszeile in der Docstring bei 23) ruft `preflight(root, change, OPUS)` mit Standardwerten auf: es erfordert, dass `plans/changes/<change>/spec.md` existiert und einen Bead im Header trägt, mit `required=()` — `research.md` und `decisions.md`, die deklarierten Inputs des Prompts, werden vom Runner nicht auf Existenz geprüft. Es fügt einen Block `## Phase 2a — Opus 5.5, <date>` mit den geparsten Sechs-Zellen-Zeilen ein; ein fehlgeschlagener Aufruf schreibt keine Zeilen (`tests/test_stage2.py::test_a_failed_spec_review_call_writes_no_rows`), und der schreibgeschützte Start ist als Kriterium 27 verankert (`tests/test_stage2.py::test_the_spec_review_starts_opus_with_read_only_tools`).

**Wo die Review im Fluss sitzt.** Die Draft-Kette (`docs/WORKFLOW.md` §4, „The draft“): `draft` → die orchestrierende Sitzung liest den gesamten Draft → `spec-review` → ein zweiter `draft` arbeitet die offenen Zeilen ein, sobeld der Maintainer jede `[AMBIGUITY]` beantwortet hat, die eine Zeile aufgeworfen hat → die Plan-Karte erreicht den Maintainer unverändert. `prompts/02-spec.md`, „After the spec review“: vor Phase 3 wird jede Zeile zu `in spec` oder `rejected — <reason>`; der überarbeitete Spec ist der Maßstab für Plan, Code und Review. `prompts/02b-design.md` listet den nach 2a überarbeiteten Spec als Input auf. ADR 0016 (akzeptiert, `docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md`, Entscheidung 5 und 7) machte die Opus-Review zur Review für jeden Change, den Stage 2 routet, und zu einer der vier Prüfungen, die ein gedrafteter Change vor Phase 4 besteht. Die Zeilen-/Blockform und die Sitzungsregeln sind als Kriterien 28–31 des archivierten Changes verankert, der den ADR eingeführt hat (`plans/changes/archive/2026-11-06-codex-drafts/spec.md`).

**Übungsbeweise dafür, dass es heute gehalten wird.** Das Night-Run-Handover `docs/journal/handover/2026-11-17-night-run-2026-11-16-a.md` zeichnet Spec-Review-Zeilen auf Live-Beads auf (S2-1 BLOCKER auf Bead coding-harness-u1ha; F-18–F-21 auf coding-harness-f9sv, Zeilen 65–73) und einen Hintergrundprozess für Spec-Reviews, der bei einem Neustart abbrach (Zeilen 120–122).

## Wo es liegt

- Doktrin: `AGENTS.md` (2a-Zeile der Phasentabelle); `docs/WORKFLOW.md` — Phasentabelle Zeile 2a, §3 Modelltabellenzeile, „The spec review improves the spec first“ (§3, das festhält, dass One-Reviewer-for-both seit ADR 0016 nur für einen `spike` gilt), die §4-Klassentabelle plus der Paragraph „Nothing checks…“, die Runner-Routing-Tabelle Zeile „2a Spec review“, die Verbliste (`spec-review — Opus 5.5, phase 2a, a headless call with read-only tools and no session kept`), die Draft-Kette und die `stage2_runs.py`-Beschreibung.
- Prompts: `prompts/02a-spec-review.md` (die gesamte Phase: drei Fragen, „What you do not do“, „If you find nothing“; die Spike-Hand-Nah-Pfad mit einer festen Session-ID unter der Tabelle), `prompts/02-spec.md` („After the spec review“), `prompts/06-review.md` (Fresh-vs.-Resume-Regeln, Zeilen 8–25, 49), `prompts/02b-design.md` (Input-Zeile). Unter den suchten Begriffen (`2a|spec review|spec-review`) erwähnt keiner von `prompts/01-explore.md`, `01a-interview.md`, `03-plan.md`, `04-implement.md`, `07-commit.md` die Spec-Review — „nicht dort“ für diese Files.
- Runner: `scripts/stage2.py` (`spec_review`, `recorded_2a_session`, `DRAFT_RULES`, `VERBS["spec-review"]`); `scripts/stage2_runs.py` (`_section`, `Counts.spec_review`); `scripts/kit/probe.py` (Endpoint-Versöhnungs-Allowlist-Eintrag für `02a-spec-review.md-Opus 5.5` und die Historiennotiz, die das Prompt auf 2026-09-10 datiert).
- Template: `templates/findings.md` — 2a- und Phase-6-Zeilen teilen eine Tabelle; Dimensionen `SPEC`/`MAINT`, Marker `[AMBIGUITY]` (niemals lokal entschieden) und `[DIVERGENT]`, Statuswerte einschließlich `in spec`, `rejected — <reason>`, `answered`.
- Tests: `tests/test_stage2.py` — Verhaltens-Verankerungen bei den Asserts `spec-review` (Zeilen ~766, ~1486, ~1522, ~1538, ~1544, ~1621–1666, ~1704–1726, ~1788, ~6586 für den Fall Exit-2, ~7739–7790) und Routing-Text-Verankerungen (~19843, `review_prompt_problems` bei ~20143–20151, was verlangt, dass die 02a-Modellzeile Opus 5.5 und den Runner-Befehl benennt; ~20388; ~20429; ~21006, WORKFLOW Reads Wortlaut „implement, repair, `spec-review`“).
- Nachbarn, die ich kenne: `plans/changes/archive/2026-11-06-codex-drafts/spec.md` (Kriterien 28–33 verankern die heutige Zeilen-/Blockform und das Routing); `plans/changes/stage2-session/spec.md` (aktiver Change über Runner-Sitzungs-/Ablehnungsverhalten; seine `research.md` und `findings.md` erwähnen Spec-Review — ich habe nur den Research-Header gelesen, die Überlappung wurde nicht weiter gelesen); `plans/specs/implementation-verification/spec.md`, die eine lebende Spec, in der eine Suche nach `2a|spec review` keine Übereinstimmung findet — „nicht dort“: die lebende Spec spricht heute nicht über die Spec-Review.

## Was unklar ist

- Die Absicht des Beads: Die Beschreibung und Notizen von `coding-harness-ttic` wurden **nicht gelesen** — der Tracker ist die Dolt-Datenbank unter `.beads/`, gelesen durch `tools/bd` / `scripts/bead_render.py`, keine gerenderte Kopie ist committed, und ich führe keine Befehle aus. Welche Klassen ein verpflichtender 2a abdecken muss und ob „verpflichtend“ ein roter Check oder nur eine Doktrin-Prosa sein soll, wurde nicht in irgendetwas festgestellt, das ich gelesen habe. Was der Ordner selbst bietet, ist der Name und der „may skip the spec review“-Satz von `docs/WORKFLOW.md` §4.
- Die Klasse des Changes ist nirgendwo deklariert, das ich gelesen habe: kein `class:`-Feld im Frontmatter von `research.md`, und die Bead-Beschreibung, die ihn benennen würde, wurde nicht gelesen.
- Die Gate-Wortlaut-Abweichung zwischen `AGENTS.md` und `docs/WORKFLOW.md` (siehe oben) wurde gefunden, aber nicht aufgelöst.
- Ob `spec-review` auf der `--stage2-off`-Route laufen kann, wurde über die zwei Sätze hinaus nicht gelesen, die ich habe: Die Verbliste nennt keine Stage-1-Route dafür, und ADR 0016 Entscheidung 9 sagt nur, dass `draft` keine hat.
- `docs/governance/gate-catalog.md` und die komplette `GATES`-Deklaration in `scripts/ci_gates.py` wurden nicht gelesen; was heute deklariert ist, über die Fakten hinaus, dass `SUBSETS=("docs",)` das `--job docs` lokal auswählt und dass `ci.yml` und der Katalog von dieser einen Liste generiert werden (gehalten durch das `ci-drift` Gate), bleibt unverifiziert.

## Welche Files ein Change anfassen müsste

- Doktrin-Texte: `AGENTS.md` (2a-Zeile), `docs/WORKFLOW.md` (Phasentabellenzeile 2a, §3 Modellzeile, §4-Klassentabelle und „Nothing checks“-Paragraph, Verbliste, Draft-Kette), `prompts/02a-spec-review.md`, und die Fluss-Wortlaut-Files `prompts/02-spec.md`, `prompts/06-review.md`, `prompts/02b-design.md`.
- Runner-Code, falls die Regel Runner-Verhalten wird: `scripts/stage2.py` (`spec_review`, die `preflight`-Aufrufer der Verben, deren Ausführung von einem gehaltenen 2a abhängen würde, `VERBS`), möglicherweise `scripts/stage2_runs.py`, falls ein neuer Count geschuldet wird.
- Ein neues mechanisches Gate wäre ein neuer `scripts/check_*.py` Eintrag plus eine Deklaration in `scripts/ci_gates.py`, von der `.github/workflows/ci.yml` und `docs/governance/gate-catalog.md` generiert werden; `scripts/verify_all.sh` delegiert seine Gate-Liste an `ci_gates.py --commands --job`.
- Tests, die das heutige Wortlaut und Verhalten verankern: `tests/test_stage2.py` (Routing-Text-Checks und Spec-Review-Verhaltenstests oben aufgelistet) — jede Wortlautänderung in der Doktrin oder in der 02a-Modellzeile löst sie aus.
- `plans/INDEX.md` trägt die Zeile des Changes für `research.md` (Bead-Spalte `coding-harness-ttic`).
- Der Change-Ordner selbst enthält derzeit nur `research.md` — `spec.md`, `decisions.md`, `findings.md` existieren dort noch nicht (Glob).
