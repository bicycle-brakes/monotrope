---
title: "Regelwerk — die normativen Regeln für Agents, Hooks, Gates, Human Gates, Provenienz und Struktur"
category: governance
subcategory: regelwerk
status: current
version: 2.0.0
created: 2026-08-14
last_reviewed: 2026-09-19
owner: Data Architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-08-14"}
review:
  status: pending
  approved_by: null
  approved_at: null
adopted_by: [portfolio-agentic-engineering, lakeswitch-ai, project-instances]
lakeswitch_ref: "docs/reference/rules.md"
disclosure: extern
id_scheme: "RB-<Familie><n>; A Agents · H Hooks · G Gates · M Human Gates · P Provenienz · S Struktur; IDs stabil, nie wiederverwendet"
rating_scheme: "Durchsetzungsstufe 1–5 (§3); eine Regel ohne Erzwinger steht höchstens auf Stufe 2 und nennt dann ein Ventil"
tags: [governance, regelwerk, normativ, agents, hooks, gates, provenienz, struktur]
---

# Regelwerk

## 1 Wozu diese Seite

Dieses Repository hatte seine Regeln, aber es hatte sie **verteilt**: eine
Anti-Fabrikations-Erwartung in Prosa, eine Hook-Konvention in einem README, ein
Gate-Vokabular in einem ADR, eine Namensregel in einem Konzeptpapier. Jede
einzelne war richtig. Zusammen waren sie unprüfbar — man konnte nicht sagen, ob
eine Regel gilt, weil es keine Liste gab, gegen die man das hätte fragen können.

Diese Seite ist diese Liste. Sie **erklärt** nicht: warum es Human Gates gibt,
steht in [Quality Gates](quality-gates.md); warum Provenienz deklariert wird,
in [ADR-027](../adr/027-evidenz-und-provenienz.md); warum ein Gate INFO, DRIFT
oder BLOCK meldet, in [ADR-028](../adr/028-gate-und-guard-design.md). Sie **setzt**:
je Regel ein Satz, eine Durchsetzungsstufe, der Test, der sie hält, und wo sie
gilt.

Der Nutzen ist genau der: eine Regel, die nirgends steht, wird nicht befolgt —
eine Regel, die überall steht, auch nicht.

## 2 Wie man eine Regel liest

| Spalte | Bedeutung |
|---|---|
| **ID** | `RB-<Familie><n>`. Stabil. Wird eine Regel gestrichen, bleibt ihre Nummer verbrannt — sonst zeigt ein alter Verweis auf etwas Neues |
| **Regel** | ein Satz im Indikativ. Was gilt, nicht was wünschenswert wäre |
| **Stufe** | 1–5, siehe §3 |
| **Erzwingender Test/Gate** | `tests/<datei>.py::<funktion>` · `ci.yml#<step-id>` · `Ramp:<ventil>` · `lakeswitch:<pfad>` |
| **Gilt in** | **P** portfolio-agentic-engineering · **L** lakeswitch-ai · **I** Projekt-Instanz |

Ein Eintrag `Ramp:<ventil>` heißt: **dieser Teil der Regel ist noch nicht
erzwungen.** Das Ventil steht in `scripts/ramp_valves.py` und nennt seine
Fälligkeit. Eine Regel auf Stufe 1 oder 2 **muss** ein Ventil nennen — sonst ist
sie eine Bitte, die sich als Regel ausgibt.

## 3 Die Leiter

Fünf Stufen, von der Konvention bis zur Sperre. Sie stammen aus
[Component Guardrails](component-guardrails.md) §„Wie hart ist eine Regel
wirklich".

| Stufe | Was passiert, wenn jemand die Regel bricht |
|---|---|
| **1 Konvention** | nichts. Sie steht geschrieben, und jemand merkt es vielleicht |
| **2 Review** | ein Mensch sieht es im Pull Request — wenn er hinsieht |
| **3 CI berichtend** | der Lauf meldet es sichtbar und läuft weiter (DRIFT) |
| **4 CI blockierend** | der Lauf schlägt fehl (BLOCK); ohne Fix kein Merge |
| **5 Sperre** | der Vorgang kommt gar nicht erst zustande (Exit 2, überlebt jeden Permission-Mode) |

Die Stufe ist **keine** Wichtigkeit. RB-A1 ist die folgenreichste Regel dieser
Seite und steht auf 4, nicht auf 5 — weil ein Hook nicht prüfen kann, ob ein
Satz beobachtet wurde. Die Stufe sagt, **wie** eine Regel gehalten wird, nicht
wie sehr sie zählt.

**Zur Stufe 5 — der Sperre im Hook — gehört eine Warnung.** Ein Hook, der die falschen Vorgänge sperrt,
wird abgeschaltet — und dann sperrt er gar nichts mehr. Stufe 5 ist deshalb für
Vorgänge reserviert, die sich präzise benennen lassen: ein Schreibzugriff auf
einen Pfad, ein Kommando mit einem Ziel. Nicht für Urteile.

## 4 SYNC IMPACT — was eine Änderung dieser Seite auslöst

Diese Seite gilt in drei Repositories. Eine Änderung hier, die dort nicht
nachgezogen wird, ist schlimmer als keine Änderung: sie erzeugt zwei Fassungen
derselben Regel, und ab da beantworten zwei Dokumente dieselbe Frage
verschieden.

Deshalb: **jede Änderung erhöht `version:` und trägt einen Eintrag im
Änderungsverlauf (§7) mit genau vier Zeilen.**

| Zeile | Inhalt |
|---|---|
| `Geändert:` | die betroffenen IDs |
| `Tests:` | welche Erzwinger neu sind, umbenannt wurden oder wegfallen |
| `Agents/Hooks/Templates:` | was im Repo nachgezogen werden muss |
| `lakeswitch-ai:` | was dort nachzuziehen ist — oder „nichts" |

Ein Eintrag ohne eine der vier Zeilen ist ein Testfehler, keine Nachlässigkeit.

**Semver:** MAJOR = eine Regel entfernt oder ihre Bedeutung geändert · MINOR =
neue Regel · PATCH = Wortlaut oder Testname.

## 5 Die Regeln

### A — Agents

| ID | Regel | Stufe | Erzwingender Test/Gate | Gilt in |
|---|---|---|---|---|
| **RB-A1** | Ein Agent berichtet nur, was er in dieser Sitzung beobachtet hat; Nicht-Beobachtetes ist `UNKNOWN`, nie `NO`; jede Behauptung trägt `evidence:`; Proxys heißen Proxys; negative Antworten sind nicht symmetrisch; vor einem „liest nichts"-Urteil folgt er den Imports; er nimmt seine eigene Arbeit nie ab (§6) | 2 | `Ramp:agents-evidence-contract` | P L I |
| **RB-A2** | Read-only-Agents führen kein `Bash`, `Write` oder `Edit`; wer eine Shell hat, deklariert ihren Umfang; `permissions.deny` enthält mindestens Prod-Deploy, `bundle destroy`, Force-Push und `rm -rf` | 2 | `Ramp:agents-tool-scopes` | P L I |
| **RB-A3** | Eine selbst erklärte Verifikation ist keine: ein Verdikt gilt erst, wenn ein zweiter unabhängiger Leser oder ein Script es aus den Findings nachgerechnet hat | 2 | `Ramp:skill-outputs-transfer` | P L I |
| **RB-A4** | Ein schreibender Agent deklariert, wohin er schreiben darf — nie in den Entscheidungs-Baum, nie in seinen eigenen Abnahmebericht —, führt einen Abschnitt „was ein Mensch prüft" und liefert ein Ergebnis, in dem `UNKNOWN` vorkommen darf | 2 | `Ramp:agent-writes-allowlist` | P L I |
| **RB-A5** | Wo ein Agent entscheidet, steht ein geschlossenes Vokabular, kein Freitext. Ein Freitextfeld lässt ihn das Ergebnis umdefinieren, statt es zu melden | 2 | `Ramp:closed-vocabulary` | P L I |
| **RB-A6** | Jedes Modell, das hier genannt wird, löst gegen einen deklarierten Endpunkt auf — mit Betreiber, Datenresidenz und Abrechnungsart. Kundencode geht nur an einen Endpunkt mit erklärter Residenz; Kundendaten an keinen. Nicht gelistet ist BLOCK, nicht „vermutlich in Ordnung" | 4 | `tests/test_model_endpoints.py`::test_every_agent_model_resolves_to_a_declared_endpoint · ::test_customer_code_never_reaches_an_endpoint_without_stated_residency · ::test_no_endpoint_is_cleared_for_customer_rows | P L I |

### H — Hooks

| ID | Regel | Stufe | Erzwingender Test/Gate | Gilt in |
|---|---|---|---|---|
| **RB-H1** | Auf einer Guard-Registrierung oder in ihrem Script steht weder `\|\| true` noch `2>/dev/null`; Report-Hooks werden nicht stummgeschaltet | 2 | `Ramp:hook-behaviour-tests` | P L I |
| **RB-H2** | Ein Guard fällt geschlossen aus: fehlender Interpreter oder unlesbare Eingabe → Exit 2 mit Begründung auf stderr | 2 | `Ramp:hook-behaviour-tests` | P L I |
| **RB-H3** | Der Matcher ist ein Tool-Name; Argumente filtert ein Parser, nie `grep` in der Shell | 2 | `Ramp:hook-behaviour-tests` | P L I |
| **RB-H4** | Jedes Hook-Script ist registriert und jede Registrierung zeigt auf ein lauffähiges Script — bidirektional, auch in Vorlage und Skelett | 2 | `Ramp:hooks-registered-tests` | P L I |

### G — Gates (Maschine)

| ID | Regel | Stufe | Erzwingender Test/Gate | Gilt in |
|---|---|---|---|---|
| **RB-G1** | Es gibt genau eine Gate-Liste. Der lokale Runner hält keine eigene | 4 | `tests/test_ci.py`::test_runner_holds_no_command_list_of_its_own · ::test_no_second_verification_workflow | P L I |
| **RB-G2** | Die Gate-Stufe folgt aus Signifikanz und Beweglichkeit: kritisch oder hoch und beide Seiten wandern per Commit → BLOCK; liegt die Gegenseite außerhalb → DRIFT mit Timer; mittel → DRIFT; niedrig → INFO | 2 | `Ramp:fehler-katalog-transfer` | P L I |
| **RB-G3** | Jeder DRIFT-Check hat einen Aufrufer am Timer **oder** einen deklarierten Grund. Ohne beides ist er ein Bericht, kein Gate | 4 | `tests/test_ci.py`::test_every_script_has_a_caller_or_a_declared_reason · ::test_drift_job_runs_on_schedule_and_dispatch_only · ::test_no_declared_reason_stands_for_a_script_that_has_a_caller | P L I |
| **RB-G4** | Jedes Gate hat einen Mutationstest: einen Lauf, der rot wird, wenn man das kaputtmacht, wovor das Gate schützt — oder einen Grund in der Sperrklinke, die nur schrumpfen darf | 4 | `tests/test_ci.py`::test_every_gate_step_has_a_mutation_test · ::test_the_mutation_ratchet_only_turns_one_way | P L I |
| **RB-G5** | Fehlender Input ist nicht „veraltet". Prüfer melden über das gemeinsame Vokabular, Schreiber über `check_verdict` — aktuell, veraltet, fehlend sind drei Zustände | 2 | `Ramp:kit-transfer` | P L I |
| **RB-G6** | `--check` ist ein deklariertes Flag; ein unbekanntes Flag ist ein Fehler und kein Lauf; `--check` schreibt nie | 2 | `Ramp:kit-transfer` | P L I |
| **RB-G7** | Eine leere Menge ist kein Ergebnis: jedes Gate behauptet seine Schlüsselmenge als nicht leer. Geprüft wird der Merge-Stand, nicht der Branch-Kopf | 4 | `tests/test_ramp_valves.py`::test_the_valve_list_is_not_empty · `tests/test_regelwerk.py`::test_the_list_is_not_empty · `Ramp:merge-freshness` | P L I |

### M — Human Gates

| ID | Regel | Stufe | Erzwingender Test/Gate | Gilt in |
|---|---|---|---|---|
| **RB-M1** | Ein Gate-Record durchläuft `DRAFT → IN_REVIEW → ACCEPTED → WITHDRAWN`, führt seine Geschichte mit und ist über den Hash seines Gegenstands gebunden: was nach der Signatur geändert wird, ist wieder unsigniert. Einen Zustand „abgenommen, aber ohne Unterschrift" gibt es nicht | 4 | `tests/test_gate_record.py`::test_accepted_is_derived_not_set · ::test_a_changed_subject_invalidates_the_signature · ::test_a_gate_with_a_missing_required_role_is_not_accepted · ::test_the_required_roles_match_the_governance_table · `Ramp:gate-record-validators` | P L I |
| **RB-M2** | Eine Signatur ist eine Zustimmung im Pull Request, transkribiert von einem Werkzeug, das nicht urteilen kann. Wer zustimmt, ist weder Autor noch letzter Pusher | 2 | `Ramp:signature-transcription` | P L I |
| **RB-M3** | Ein abgenommener Contract setzt eine adversariale Quellverifikation voraus — jemand hat versucht, ihn zu widerlegen, und es nicht geschafft | 2 | `Ramp:adversarial-record` | P L I |
| **RB-M4** | Das Reconciliation-Ergebnis hat einen benannten Unterzeichner, und jede Toleranz trägt ihre Begründung. Eine nackte Prozentzahl ist keine Schwelle, sondern eine Vermutung | 2 | `Ramp:human-gates-transfer` | P L I |
| **RB-M5** | Alle Gates einer Liefereinheit schließen **vor** der Liefereinheit. Die Grenze ist keine Warteschlange. Die Reihenfolge selbst ist der Mechanismus: Protokoll vor Ergebnis, Duplikat-Befund vor Deduplizierung, Erwartung vor Verdikt, Generalprobe vor dem ersten Lauf | 2 | `Ramp:boundary-before-close` | P L I |
| **RB-M6** | Die Branch-Regeln werden aus dem Repository heraus behauptet: geforderte Prüfungen gleich der Gate-Liste, Code-Owner-Review an, Zustimmung nicht vom letzten Pusher. Eine unerreichbare Verwaltungs-Schnittstelle ist BLOCK, nicht grün | 2 | `tests/test_repo_settings.py`::test_master_has_a_ruleset_with_required_checks · `Ramp:ruleset-assert` | P L I |
| **RB-M7** | Die Eigentümer-Datei deckt jeden Entscheidungs-Pfad ab Tag eins — mit einer **eigenen** Zeile. Ein Auffangeintrag benennt niemanden für einen Pfad, sondern jemanden für alles | 2 | `Ramp:codeowners-here` | P L I |
| **RB-M8** | Rollen sind Rollen. Der Roster löst Rolle auf Handle auf, nie umgekehrt; eine unbesetzte Rolle ist ein sichtbarer Befund mit Fälligkeit, keine Leerstelle | 2 | `Ramp:owner-roles-here` | P L I |

### P — Provenienz

| ID | Regel | Stufe | Erzwingender Test/Gate | Gilt in |
|---|---|---|---|---|
| **RB-P1** | Jedes Artefakt nennt seine Klasse und die Hand, die es erzeugt hat; abgenommene Klassen nennen zusätzlich, wer abgenommen hat und wann; maschinell gerenderte nennen ihren Generator und die Prüfsumme ihrer Eingaben | 2 | `Ramp:provenance-validators` | P L I |
| **RB-P2** | Klasse und Verzeichnis entsprechen einander eins zu eins, und die Karte steht neben dem Prüfer, nicht in ihm. Jede aktive Ebene hat einen Eintrag | 2 | `Ramp:provenance-validators` | P L I |
| **RB-P3** | Generierte Blöcke tragen ihre Marker samt Eingabe-Prüfsumme, die CI rendert neu und vergleicht; außerhalb steht keine handgetippte Bestandszahl. **Was gegen einen Fehler schützen soll, wird bei jedem Lauf erzeugt und geprüft — oder gar nicht geführt** | 2 | `ci.yml#export-identity` · `Ramp:kit-transfer` | P L I |
| **RB-P4** | Commits tragen eine echte Identität und, wo ein Assistent beigetragen hat, den entsprechenden Trailer. Auf Entscheidungs-Pfaden lehnt die CI Verstöße ab | 2 | `Ramp:commit-identity` | P L I |
| **RB-P5** | Der Verlauf ist append-only und wird nie ohne sein Datum zitiert. Ein Befundblock ist unveränderlich; Widerspruch kommt darunter, nie hinein | 4 | `tests/test_feedback_channel.py`::test_handover_records_are_immutable · `Ramp:journal-date-citation` | P L I |

### S — Struktur

| ID | Regel | Stufe | Erzwingender Test/Gate | Gilt in |
|---|---|---|---|---|
| **RB-S1** | Das Instruktionsbudget ist eine Grenze, keine Empfehlung: eine Instruktionsdatei, ein Import, eine Obergrenze. Das README wird nie importiert | 4 | `tests/test_entry_points.py`::test_claude_md_imports_agents_md_and_stays_short · ::test_instruction_files_are_under_200_lines · ::test_readme_is_never_imported | P L I |
| **RB-S2** | Prozeduren leben in Skills, Erklärungen in der Dokumentation hinter einem generierten Index, bereichsgebundene Regeln in pfadgebundenen Regeldateien | 2 | `Ramp:procedures-in-skills` | P L I |
| **RB-S3** | Eine Seite hat genau einen Aussagetyp; nur Referenz-Seiten werden aus Instruktionsdateien zitiert | 2 | `Ramp:doc-type` | P L I |
| **RB-S4** | Jede Wissensseite nennt ihren Eigentümer und wann sie zuletzt geprüft wurde; eine abgekündigte Seite ist nur noch ein Zeiger; Ablösungen sind gegenseitig verlinkt | 2 | `Ramp:freshness-per-page` | P L I |

## 6 RB-A1 im Wortlaut

Dieser Absatz ist **normativ und wird kopiert, nicht nacherzählt.** Er steht
byte-gleich in jeder Agent-Definition dieses Repositories und in der
gemeinsamen Klausel von lakeswitch-ai; `tests/test_regelwerk.py` vergleicht ihn.

Der Grund für die Byte-Gleichheit ist nicht Pedanterie. Vierzehn leicht
verschiedene Fassungen wären vierzehn Regeln, und die Unterschiede fielen
niemandem auf — weil jede einzelne für sich richtig klingt.

> **Evidence contract.** Report only what you observed in this session: a run, a deploy, a count, or a verdict you did not execute or read yourself does not exist for the purpose of your report. Anything you could not observe is `UNKNOWN`, never `NO` — a missing artefact, an unreachable endpoint or an empty result set is a fact about your observation, not about the world. Every claim carries `evidence:` naming the file, symbol, command or statement id it rests on; a proxy — a metadata call instead of a data read, a step conclusion instead of a job result, a list price instead of an invoice — must be named as a proxy inside the claim itself. Negative answers are not symmetric: `NOT_FOUND`, a permission error and "does not exist" are three different findings and are reported as three. Before you judge that code "reads nothing" or "touches nothing", follow its imports and includes. You never accept, pass or sign your own work: the verdict is computed from the findings by a validator, and a human signs it.

Vier Teile, einzeln referenzierbar:

| Teil | Satz | Woher der Befund stammt |
|---|---|---|
| **(a) nur Beobachtetes** | 1–2 | ein Reconciliation-Bericht, der sich bei sechs von sechs selbst abnahm (F-A-14); vier erfundene Messungen in einer Sitzung (F-A-42) |
| **(b) Proxys heißen Proxys** | 3 | eine Sonde, die eine Metadaten-Schnittstelle befragte und „erreichbar" meldete (F-A-41) |
| **(c) Negative sind nicht symmetrisch** | 4 | eine erfundene Aufgabe, entstanden aus einem `NOT_FOUND` (F-A-43); drei verschiedene Negativ-Antworten, als eine berichtet (F-B-16) |
| **(d) den Imports folgen** | 5 | ein flacher Suchlauf, der Lesezugriffe in importierten Modulen übersah (F-A-46) |

## 7 Änderungsverlauf

Append-only. Jeder Eintrag trägt die vier Pflichtzeilen aus §4.

### 2.0.0 — 2026-09-19

Dieses Repository hat das Regelwerk aus dem Ursprungs-Korpus geerbt — samt
Erzwinger-Verweisen auf Tests, die dort leben, nicht hier. Die 2ee-Triage hat
je Regel gemessen: **existiert der benannte Erzwinger in diesem Repo?** Diese
Fassung ist das Ergebnis des Mappings (Bead `coding-harness-2ee`, Welle 2):

- **Geändert:** Stufen verschoben — RB-A1, RB-A2, RB-A3, RB-H1–H4, RB-G2, RB-G5, RB-G6, RB-M4, RB-M7, RB-M8, RB-P1, RB-P2, RB-P3 stehen jetzt auf 2, je mit datiertem Ventil, dessen Prädikat die Arbeit misst (*existiert der benannte Test?*). Erzwinger neu gezeigt — RB-G7 auf `tests/test_ramp_valves.py` und die Regel-Liste selbst, RB-M1 auf `tests/test_gate_record.py` plus Ventil, RB-P5 auf die Unveränderlichkeits-Prüfung plus Ventil, RB-P3 auf `ci.yml#export-identity` als Teil-Erzwinger plus Ventil. Keine ID geändert, keine entfernt, kein Regeltext geändert
- **Tests:** neu `tests/test_ramp_valves.py` (RB-G7) und `tests/test_entry_points.py` (RB-S1, Bead `21f`); `scripts/ramp_valves.py` führt dreizehn neue Ventile mit Frist. Kein bestehender Test geändert
- **Agents/Hooks/Templates:** nichts. RB-A1 §6 bleibt unverändert — sein Verbatim-Vergleich wartet auf die Agent-Definitionen (Cluster D der 2ee-Triage); die Regel steht deshalb solange auf 2
- **lakeswitch-ai:** die Erzwinger, die im Ursprungs-Repo leben (Skill-Outputs, Human-Gates, Export-Schemas, Evidence-Pipeline, Repo-Settings), reisen mit dem Kit-Transfer; die Ventile `skill-outputs-transfer`, `human-gates-transfer`, `kit-transfer` und `fehler-katalog-transfer` nennen die Frist

MAJOR, weil sich die Durchsetzungs-Zusage ändert: siebzehn Regeln, die hier
behauptet hatten, eine Maschine halte sie, sagen jetzt ehrlich, dass ein Mensch
hinsieht — bis der benannte Test existiert oder die Frist fällt.

### 1.1.0 — 2026-09-08

**RB-A6** kommt hinzu: wo ein Modell läuft und was es sehen darf, stand bis
heute nirgends normativ. `docs/WORKFLOW.md` regelt, *welches* Modell je Phase
läuft — nicht, bei wem es läuft, unter welcher Datenresidenz und auf wessen
Rechnung. Die Deklaration steht in `model-endpoints.yaml`; nicht gelistet ist
BLOCK.

Die Residenzauflage ist als **Zulassungsliste** gefasst, nicht als Verbotsliste:
verlangt wird eine erklärte Residenz, nicht die Abwesenheit bestimmter Anbieter.
Eine Verbotsliste altert mit jedem neuen Anbieter, eine Zulassungsliste nicht.

MINOR, weil §4 es so vorschreibt: eine neue Regel hebt die Nebenversion. Der
erste Anlauf am 2026-09-08 trug die Regel ein und ließ die Version stehen — und
`test_regelwerk.py` blieb grün, weil es nur prüft, ob zur *deklarierten* Version
ein Eintrag existiert. Es fand den alten. Eine Prüfung, die die Änderung nicht
sehen kann, für die sie geschrieben wurde.

- **Geändert:** RB-A6 kommt hinzu. Keine bestehende ID geändert, keine entfernt, keine Stufe verschoben
- **Tests:** neu `tests/test_model_endpoints.py` mit den drei in der Regel benannten Erzwingern, dazu `::test_every_model_in_the_routing_table_resolves` und `::test_every_model_in_a_phase_prompt_resolves`. Kein bestehender Test fällt weg
- **Agents/Hooks/Templates:** `templates/run-log/run-log-schema.yaml` nannte `claude-opus-4`, das in keinem Endpunkt steht — auf `claude-opus-5` gezogen. Die sechzehn Agent-Definitionen lösen auf; dass vierzehn davon eine ältere Generation pinnen als `docs/WORKFLOW.md` routet, ist ein eigener Vorgang
- **lakeswitch-ai:** nichts. Dort läuft kein Modell aus diesem Repo; die Regel gilt dort, sobald es eines tut

### 1.0.1 — 2026-08-14

Das Zielrepositorium heißt jetzt **LakeSwitch AI**. Geändert hat sich ein Name,
keine Regel: keine ID, kein Regeltext, keine Stufe, kein Erzwinger. Der Eintrag
steht hier trotzdem, weil §4 ihn verlangt — eine Seite, die ihre eigene
Änderungspflicht bei der ersten unbequemen Gelegenheit übergeht, ist keine
normative Seite mehr.

Nicht mitgezogen wurden die Verlaufs-Dokumente unter `docs/journal/`. Sie
tragen den alten Namen weiter, und das ist richtig so: sie beschreiben einen
Stand zu einem Zeitpunkt, an dem das Repositorium anders hieß. Wer sie
umschriebe, vernichtete die Antwort auf die Frage, was wann galt (RB-P5).

- **Geändert:** keine Regel-ID. Nur der Name des Zielrepositoriums in `adopted_by`, in `lakeswitch_ref`, in der Referenzform `lakeswitch:<pfad>` aus §2 und in der Pflichtzeile aus §4
- **Tests:** `tests/test_regelwerk.py` erwartet die neuen Namen (Frontmatter-Schlüssel, Präfix `lakeswitch:`, Pflichtzeile `**lakeswitch-ai:**`). Kein Test kommt hinzu, keiner fällt weg
- **Agents/Hooks/Templates:** nichts. RB-A1 §6 ist unverändert — der Wortlaut der Klausel nennt kein Produkt, und genau deshalb überlebt er eine Umbenennung
- **lakeswitch-ai:** das Repository existiert seit dem 2026-08-14 privat unter diesem Namen. Die englische Fassung unter docs/reference/rules.md steht weiter aus

### 1.0.0 — 2026-08-14

Erstfassung. Die Regeln sind nicht neu — sie standen verstreut in ADRs, in
`AGENTS.md`, in Hook-READMEs, in Agent-Definitionen und in Testdocstrings. Neu
ist, dass sie **an einer Stelle** stehen und dass **jede** von ihnen sagt, wer
sie hält.

Der unbequeme Teil dieser Fassung ist die Spalte „Stufe": von den 33 Regeln
stehen zehn auf Stufe 2. Sie gelten, aber nichts fällt um, wenn jemand sie
bricht. Das ist keine Nachlässigkeit, sondern der gemessene Zustand — und jede
dieser zehn trägt ein Ventil mit Datum, dessen Bedingung **nicht** der Bestand
ist, sondern die Arbeit daran: *existiert der benannte Erzwinger?* Schreibt
jemand den Test, wird das Ventil fällig, und
`tests/test_ramp_valves.py::test_no_valve_is_due_and_still_open` verlangt, dass
die Regel hier hochgestuft wird. So kann „vorläufig nur Konvention" nicht der
Dauerzustand werden, der es sonst immer wird.

- **Geändert:** alle — alle 33 IDs der Familien A (fünf), H (vier), G (sieben), M (acht), P (fünf) und S (vier)
- **Tests:** `tests/test_regelwerk.py` und `tests/test_ci.py`::test_every_gate_step_has_a_mutation_test sind neu; `scripts/ramp_valves.py` führt dreizehn Regel-Ventile mit Frist. Kein bestehender Test ändert sich — die Erzwinger existierten bereits, sie hatten nur keine Liste, die sie einer Regel zuordnet
- **Agents/Hooks/Templates:** nichts. RB-A1 §6 steht bereits byte-gleich in allen vierzehn Agent-Definitionen (seit PR #88); dieser Eintrag macht die Quelle normativ, nicht den Text neu
- **lakeswitch-ai:** die englische Fassung unter docs/reference/rules.md wird aus denselben IDs gerendert. Steht noch aus — das Repository existiert zum Zeitpunkt dieser Fassung nicht

## 8 Verwandte Seiten

- [Quality Gates](quality-gates.md) — was HG-1…HG-4 und MG-0…MG-3 bedeuten und wer unterschreibt
- [Gate-Katalog](gate-catalog.md) — die zwölf Gate-Familien, nach *was findet es* sortiert
- [Fehler-Katalog](fehler-katalog.md) — die Befunde, aus denen diese Regeln entstanden sind
- [Component Guardrails](component-guardrails.md) — die Leiter aus §3 und was eine Kontrolle kostet
- [ADR-027](../adr/027-evidenz-und-provenienz.md) · [ADR-028](../adr/028-gate-und-guard-design.md)
