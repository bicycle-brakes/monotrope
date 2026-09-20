# Research: 2ee-Triage der roten Tests

* Change: 2ee-triage · Bead: coding-harness-2ee
* Snapshot: feat/gate-file-and-verify @ a144e37, 2026-09-19
* Messung: 36 failed, 227 passed, 6 skipped (`pytest tests/ -q --tb=line`)
* Methode: je Fall Fehlermeldung + Testquelle gelesen; Eimer = die drei aus
  der maintainer-Entscheidung vom 2026-09-19 (1 = Erzwinger neu bauen,
  2 = Instanz-Test mit datiertem Ventil, 3 = Regeltext korrigieren).

**Diese Tabelle ist der Vorschlag. Die Cluster-Entscheidung (4 Stück, nicht
36) trifft der Maintainer; danach wandern die Eimer-2-Zeilen als datierte
Ventile in die Tests und die Eimer-1-Zeilen werden zu Arbeitspaketen.**

## Cluster A — test_regelwerk (20): Regeln nennen Erzwinger, die nicht gereist sind

Jede Zeile: die Regel verlangt Level-3+-Erzwinger; der Test prueft deren
Existenz. Die fehlenden Erzwinger sind Testdateien und teils ci.yml-Jobs.

| Regel | Verlangte Erzwinger (fehlend) | Eimer | Anmerkung |
|---|---|---|---|
| RB-A1 (+Clause-Verbatim) | tests/test_agents.py (evidence contract, no self-pass, clause) | 1 | `.claude/agents` existiert hier mit Inhalt — die Tests lassen sich schreiben |
| RB-A2 | tests/test_agents.py (bash-scope), tests/test_hook_behaviour.py | 1 | dito |
| RB-A3 | tests/test_skill_outputs.py (verdict recompute, evidence block) | 1 | dito |
| RB-G2 | tests/test_fehler_katalog.py | 1 | fehler-katalog.md reist als bestand — Test schreibbar |
| RB-G5 | tests/test_export_schemas.py, tests/test_evidence_pipeline.py | 2 | Export-Maschinarie blieb in portfolio (D-11); Ventil bis Kit-Transfer |
| RB-G6 | tests/test_export_schemas.py, tests/test_provenance.py, tests/test_entry_points.py | 2 | dito |
| RB-G7 | tests/test_ramp_valves.py, tests/test_skill_outputs.py, tests/test_skill_schema.py, tests/test_entry_points.py | 3 | ramp_valves.py existiert hier — der Regeltext kann auf die hiesigen Erzwinger neu zeigen (Review-Akt) |
| RB-H1 | tests/test_hook_behaviour.py | 1 | Hooks liegen hier (`.claude/hooks`, `.codex/hooks.json`) |
| RB-H2 | tests/test_hook_behaviour.py | 1 | dito |
| RB-H3 | tests/test_hook_behaviour.py | 1 | dito |
| RB-H4 | tests/test_hooks_registered.py | 1 | dito |
| RB-M1 | tests/test_validators.py (gate record template) | 1 | gate_record.py + templates reisen mit |
| RB-M4 | tests/test_human_gates.py | 2 | der human-gates-Katalog lebt in der lakeswitch-Instanz — gilt-erst-mit-bestand |
| RB-M7 | tests/test_repo_settings.py | 1 | `.github/CODEOWNERS` existiert hier |
| RB-M8 | tests/test_provenance.py, ci.yml#provenance | 1 | provenance.yaml existiert; der ci-Job ist mit dem Gate-System aufbaubar |
| RB-P1 | tests/test_provenance.py (3 Tests), ci.yml#provenance | 1 | dito |
| RB-P2 | tests/test_provenance.py (2 Tests) | 1 | dito |
| RB-P3 | tests/test_evidence_pipeline.py (2 Tests), ci.yml#facts-check | 2 | evidence pipeline blieb in portfolio — Ventil bis Transfer |
| RB-P5 | tests/test_provenance.py | 1 | dito wie M8 |
| RB-S1 | tests/test_entry_points.py (CLAUDE.md importiert AGENTS.md, 200 Zeilen, README nie importiert) | 1 | das ist genau Bead 21f — kleinster Eimer-1-Hebel |

Zwischenstand: **Eimer 1 = 13, Eimer 2 = 3, Eimer 3 = 1.**

## Cluster B — test_feedback_channel (11): der Kanal erwartet Bestand

| Test | Behauptung | Eimer | Anmerkung |
|---|---|---|---|
| test_every_handover_declares_a_direction | jede Uebergabe traegt direction | 1 | 4 Handovers liegen hier; je Datei Frontmatter pruefen/ergaenzen |
| test_journal_index_lists_every_open_project_handover | docs/journal/_INDEX.md listet offene Projekt-Uebergaben | 1 | `_INDEX.md` anlegen (klein) |
| test_root_index_routes_to_the_project_feedback | docs/_INDEX.md routet zum Kanal | 1 | `_INDEX.md` anlegen (klein) |
| test_the_channel_is_not_empty | es gibt framework->project-Uebergaben | 2 | der Projekt-Kanal beginnt mit lakeswitch (O-2) — gilt-erst-mit-bestand |
| test_the_checks_go_red_when_the_contract_is_broken (3 Faelle) | die Feldpruefungen lassen sich rot fahren | 2 | Fixtures sind portfolio-Handovers (2026-08-14-osi-plan-register) — Ventil bis eigene Fixtures |
| test_the_feedback_loop_documents_the_reverse_direction | der Rueckkanal ist dokumentiert | 2 | framework-witt-feedback-loop.md fehlt (portfolio) |
| test_the_feedback_loop_points_at_the_schema_instead_of_repeating_it | das Schema wird zitiert, nicht kopiert | 2 | dito |
| test_the_framework_does_not_claim_to_write_into_the_instance | keine Schreib-Zusage in die Instanz | 2 | dito |
| test_the_route_check_goes_red_when_the_route_is_removed | die Routenpruefung ist mutationsgesichert | 2 | dito |

Zwischenstand: **Eimer 1 = 3 (klein), Eimer 2 = 8 (ein gemeinsames Ventil: der Projekt-Kanal beginnt mit lakeswitch).**

## Cluster C — test_kit (3): das Export-Manifest fehlt

| Test | Behauptung | Eimer | Anmerkung |
|---|---|---|---|
| test_the_kit_list_is_not_derivable_from_the_export_list | Kit-Manifest ≠ Ableitung des Export-Manifests | 1 | `scripts/export/manifest.yaml` fehlt ganz — als Teil der lakeswitch-Transfer-Logik aufbauen |
| test_the_role_check_goes_red_when_a_rule_is_removed | die Rollenpruefung ist mutationsgesichert | 1 | gruen, sobald das Manifest existiert |
| test_the_two_manifests_really_disagree_somewhere | die beiden Manifeste widersprechen sich wirklich an einer Stelle | 1 | dito |

Zwischenstand: **Eimer 1 = 3 — ein Arbeitsthema (lakeswitch-Transfer), kein dreifaches.**

## Cluster D — test_model_endpoints (1): Agents ohne `model:`-Feld

| Test | Behauptung | Eimer | Anmerkung |
|---|---|---|---|
| test_agents_are_found_at_all | Agent-Definitionen mit `model:` werden gefunden | 1 | `.claude/agents` existiert, aber ohne `model:`-Felder — genau die qvl-Schnittstelle (Routing je Instanz) |

## Zusammenfassung fuer die Cluster-Entscheidung

| Cluster | Faelle | Eimer 1 | Eimer 2 | Eimer 3 |
|---|---|---|---|---|
| A regelwerk | 20 | 13 | 3 (+1 geteilt) | 1 |
| B feedback | 11 | 3 | 8 | — |
| C kit | 3 | 3 | — | — |
| D model_endpoints | 1 | 1 | — | — |
| Summe | 36* | ~20 | ~11 | ~1 (+3 geteilt) |

*36 = 20 + 11 + 3 + 1 + RB-G5/G6/P3 als geteilte Zeilen (drei Faelle, ein Ventil).

## Offene Punkte fuer den Maintainer

1. Cluster-B-Ventil: gilt-erst-mit-bestand bis lakeswitch beitritt (O-2) — ok?
2. RB-G5/G6/P3: Ventil bis Kit-Transfer ODER Regeltext neu zeigen — Entscheidung.
3. RB-G7: Regeltext auf die hiesigen Erzwinger neu zeigen (Review-Akt im Regelwerk) — ok?
4. Reihenfolge Eimer 1: Vorschlag 5d (model_endpoints, kleinste) → 5a (regelwerk-Mapping) → 5b/c.

