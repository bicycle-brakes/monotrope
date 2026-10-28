---
title: "Research — swarm-test-speed"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-dca4
owner: Data Architect
provenance: human-written
tags: [research]
class: bounded
---

# swarm test speed — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-28: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 714 files, 2461 commits, 12 rules.

## Runner exploration — 2026-10-28

Die Exploration ist abgeschlossen — hier ist der Forschungsbericht als Prosa zum Anhängen an `plans/changes/swarm-test-speed/research.md` (Englisch, wie es für Repository-Artefakte vorgesehen ist; alle Aussagen benennen ihre Quelle):

---

## Runner-Exploration — 2026-10-28

**Vorgeschlagene Header-Zeile (der Runner ergänzt, was seine Finder vorschlagen):**

```
neighbours:
  - plans/changes/research-swarm/spec.md
  - plans/changes/terms-test-fixtures/research.md
  - plans/changes/terms-expiry/spec.md
  - plans/changes/runner-time-line/spec.md
  - plans/changes/free-member-rate-limit/spec.md
  - plans/changes/pi-pin/research.md
```

### Was heute existiert

**Der Änderungsordner ist ein Skelett.** `plans/changes/swarm-test-speed/` enthält nur `research.md` (Klasse `bounded`, Perle `coding-harness-dca4`, Eigentümer Data Architect, `provenance: human-written`); es existieren noch keine Spezifikation, Plan oder Entscheidungen. Die Registry-Zeile ist vorhanden (`plans/INDEX.md`, Zeile `changes/swarm-test-speed/research.md`, Draft, 2026-10-28). Der Eröffnungs-Commit benennt die Perle im Betreff: `change(swarm-test-speed): open the change folder, class bounded (bead coding-harness-dca4)` (Branch `perf/swarm-test-speed`, Commit `e8da4068`).

**Die Suite hat genau einen Speed-Hebel, und er ist an drei Stellen fixiert.** Der Pytest-Aufruf lautet `python3 -m pytest tests/ -q -n auto`, deklariert einmal in `decisions/gates.yaml` (Gate-ID `pytest`, Job `verify`, Enforcement `block`), lokal ausgeführt von `scripts/verify_all.sh` (das seine Befehle nur aus dieser einen Gate-Liste bezieht) und generiert in `.github/workflows/ci.yml` (Schritt-ID `pytest`; der Workflow-Header besagt, dass Handänderungen das `ci-drift`-Gate auslösen). `Makefile` `make test` führt denselben Befehl aus, und `tests/test_ci.py` fixiert die Zeichenketten-Zuordnung `"python3 -m pytest tests/ -q -n auto": "make test"`. Die Dev-Abhängigkeiten sind `pytest==8.3.4`, `pytest-xdist==3.8.0`, `ruff==0.9.10` (`pyproject.toml`): Es gibt kein Timeout-Plugin, keine Test-Marker, keine `-durations`-Berichterstattung und keine `conftest.py` irgendwo unter `tests/` (Glob und die terms-test-fixtures-Forschung kommen zum selben Schluss). Die CI führt ein Leg auf Python 3.12 aus (`tools.python` in `gates.yaml`); der Job hat kein `timeout-minutes`.

**Die Schwarm-Testdatei ist der zweitgrößte und pro Test teuerste Verhaltenscode der Suite.** `tests/test_stage2_swarm.py` umfasst 3051 Zeilen mit 123 Testfunktionen vor Parametrisierung (die Parametrisierung fügt Dutzende hinzu: z. B. führt `test_invalid_given_neighbours_refuse_before_models` 8 Fälle aus, `test_failed_pi_calls_preserve_partial_evidence` 2×3, `test_free_model_storage_keys_preserve_best_effort_completion` 3×2). Ihr Aufbau:

- Das `sworld`-Fixture (Datenklasse `SwarmWorld`) erstellt pro Test ein temporäres Repository: `git init` plus einen ersten Commit (zwei Git-Subprozesse über `SwarmWorld.commit`), Seed `research.md`/`spec.md`/`plan.md`, ein `AGENTS.md` und `src/app.py`; kopiert die echten `prompts/` des Repositorys (12 Dateien) und `model-endpoints.yaml` (578 Zeilen) hinein; schreibt die Sitzmodelle der echten Erklärung mit `admissible_terms` aus `tests/terms_fixtures.py` neu; kompiliert die beiden Stand-in-Programme `pin-pi` und `claude` aus dem eingebetteten `STAND_IN`-Quelltext plus einer fehlerhaften reinen `pi`-Falle; beschränkt `PATH`, `HOME`, `XDG_STATE_HOME`, Secrets und Denylist; und monkeypatcht `stage2_availability.consume_research`, um eine verbrauchte Auswahl zurückzugeben.
- Jeder Verhaltenstest ruft `sworld.run()` auf, was `stage2.main(["explore", "demo", ...])` *im Prozess* ausführt. Eine vollständige Verteilung umfasst 39 + 3N Slots — die Tests bestätigen `len(sworld.calls()) == 39 + 3*len(FREE)` (`test_selected_free_models_cover_all_online_topics_on_identical_briefs`) — und jeder Slot ist ein echter Subprozess: ein neuer CPython-Interpreter, der das Stand-in-Skript ausführt (`Run.launch`, `scripts/stage2_research_run.py`, `subprocess.Popen(..., start_new_session=True)`).
- Die Datei führt ungefähr 130 `sworld.run()`/`fx.prepare()` Aufrufe durch (Zählung per grep); davon sind etwa 60+ vollständige Läufe, der Rest sind kurze Läufe (Refusals beenden Vorgang 2, bevor ein Modell startet und kosten nur Fixture-Arbeit) und Zweier-/Dreier-Loop-Wiederausführungen für Resume- und Store-Fault-Fälle (`test_a_resumed_run_is_a_new_run_within_its_slot_budget`, der Store-Fault-Cluster um `test_a_failed_store_write_keeps_every_outcome_and_still_publishes_incomplete`). Als Arithmetik, nicht als Messung: ~60 vollständige Läufe × ~40–45 Subprozesse ergeben allein in dieser Datei einige Tausend Interpreter-Starts, plus einige hundert kurze Läufe.
- Absichtliche Wanduhr-Schlafenszeiten (Wall-Clock-Sleeps) im Szenario der Stand-ins: `sleep: 20` in `test_leak_block_cancels_queued_dispatch` (gekürzt, weil der Verteiler laufende Kinder bei einem Leak-BLOCK stoppt — `supervise` in `scripts/stage2_research_dispatch.py` ruft `_stop_and_reap` auf, wenn `stop.is_set()`; die 20 s sind Sicherheitsrand, keine Laufzeit), `sleep: 5` auf dem Finder-Trio in `test_stages_dispatch_concurrently_within_provider_limits` (vollständig erwartet, ≈5 s Laufzeit), `sleep: 0.2–0.4` auf allen Topic-Slots in `test_concurrent_slots_keep_distinct_audits_and_outcomes` und `test_provider_limit_is_shared_across_topics_and_roles` (geleitet durch die ≤4 breite Go-Warteschlange, jeder im Bereich von 2–3 s), und `sleep: 30` Timeout-Fehler, die durch `monkeypatch.setitem(stage2_research_run.MINUTES, "topics", 0.03)` auf ≈1,8 s begrenzt werden (zwei parametrisierte Fälle von `test_failed_pi_calls_preserve_partial_evidence`, plus `test_a_receipt_without_output_survives_a_complete_run`). Die Tests bestätigen die Zeitmessung indirekt: `stage2_research_run.MINUTES == {"finders": 10.0, "merge": 10.0, "sentence": 5.0, "topics": 10.0, "judge": 15.0}` und `RUN_MINUTES == 150.0` (`test_amended_graph_and_deadlines_bound_every_launch`), und die `CLOCK`-Monkeypatches verschieben die falsche Zeit, anstatt zu warten (`test_required_slots_precede_free_and_reserve_judge_time`, `test_no_call_starts_once_the_run_deadline_is_spent`).

**Pro-Slot-Kosten in der Verteilung, die jede dieser ~40-Aufruf-Läufe zahlt.** Vor jedem Start führt `Run.gate` (`scripts/stage2_research_run.py`) `stage2_availability.read_declaration` aus — eine vollständige Neu-Lese- und YAML-Parsung der 578-Zeilen-Erklärung —, plus bis zu zwei `research_terms_problem`-Aufrufe und einen Leak-Check über Dateien, Commits und Regeln (`runner.leakcheck.check`); der freie Einlass liest die Erklärung erneut (`free_admission` in `Run.launch`). Jeder Slot erhält ein eigenes `tempfile.TemporaryDirectory` und schreibt einen Start- und ein Ergebnisdatensatz durch den versiegelten Store (`stage2_research_store`, sha256 `_seal`/`_read_sealed`). Der Verteiler überwacht jedes Kind mit `communicate(timeout=TICK)` wobei `TICK = 0.05` (`scripts/stage2_research_dispatch.py`) und wartende Worker in einem 0,01-s-Schlaf stehen.

**Nachbarschaftstestdateien teilen sich diese Welt.** `tests/test_stage2_terms_expiry.py` importiert das Fixture (`from test_stage2_swarm import sworld as research_world`) und `tests/test_stage2_research_deep_review.py` importiert `SwarmWorld`, `manifest_of` und `status_line`; beide führen die gleichen temporären Repository-Läufe durch. `tests/test_stage2_research_dispatch.py` (31 Tests) übt den Verteiler direkt mit echten Kinderprozessen und eigenen `sleeper()`-Skripten aus (Schlafenszeiten 0,05–0,4 s, mit 30/60-s-Fehlern, die durch Slot-Zulagen früh beendet werden). Der breitere Suite-Kontext: 2142 Testfunktionen über 58 Dateien (Zählung per grep); `tests/test_stage2.py` hat 691 mit eigenen großen Schlafdauern und ist die Suite des Single-Explorer-Runner, nicht des Schwarms; `tests/test_pi_contract.py` startet die echte installierte Pi-Version gegen Loopbacks seit ADR 0019 (`docs/WORKFLOW.md`, Abschnitt „Review-Loop-Pi-Flags").

**Kopplungen, die jede Temp-Änderung einschränken.** Das Kriterium-Ledger-Gate (`scripts/check_criterion_ledger.py`; Gate `criterion-ledger`, Grund in `gates.yaml`: das Löschen von 29 von 30 Kriteriumstests ließ `make verify` grün, Perle coding-harness-909) — `plans/changes/research-swarm/plan.md` fixiert ~80 benannte Tests in `test_stage2_swarm.py` (Ledger-Block, Zeilen ~779–911), und ein umbenannter oder gelöschter Eintrag wird ROT, während diese Änderung lebt und nach der Archivierung. Ein grep über `plans/` zeigt, dass nur die Artefakte der research-swarm-Änderung diese Testnamen referenzieren. Die synthetischen Laufzeitsitzbedingungen müssen die vollständige ADR-0022-Zulassungsregel erfüllen — die genaue Falle, die der in Auftrag gegebene Nachbar `terms-test-fixtures` (Perle hxkw, `implementation_status: partial`) dokumentiert, dessen Forschung bereits dieselben Fixture-Standorte mapped, einschließlich des `sworld`-Fixtures dieser Datei.

### Wo es liegt

- Suite selbst: `tests/test_stage2_swarm.py` (`SwarmWorld`, `sworld`, `STAND_IN`, `SwarmWorld.run/rewind/commit/complete`); geteilter Builder `tests/terms_fixtures.py`; Fixture-Wiederverwendung `tests/test_stage2_terms_expiry.py`, `tests/test_stage2_research_deep_review.py`; Verteilerebene `tests/test_stage2_research_dispatch.py`.
- Produktionskostenpfad (nur lesen, für den Fall, dass die Maschinerie imScope liegt): `scripts/stage2_research_run.py` (`Run.gate`, `Run.launch`, `Run.on_terminal`), `scripts/stage2_research_dispatch.py` (`TICK`, `supervise`, `worker`), `scripts/stage2_availability.py` (`read_declaration`, `research_terms_problem`), `scripts/stage2_research_store.py` (`_seal`, `_read_sealed`, `write_launch`, `write_result`).
- Suite-Verkabelung: `decisions/gates.yaml` (Gate `pytest`), `Makefile`, `scripts/verify_all.sh`, generiertes `.github/workflows/ci.yml`, das Pin `tests/test_ci.py` (~Zeile 459), `pyproject.toml` `[tool.pytest.ini_options]`.
- Ledger-Einschränkung: `plans/changes/research-swarm/plan.md` (Kriterium-Ledger-Block), durchgesetzt von `scripts/check_criterion_ledger.py`.

### Was unklar ist

- Die genaue Motivation und der Umfang der Perle: Der Titel/die Beschreibung von Perle `coding-harness-dca4` konnte in dieser Phase nicht gelesen werden (der Tracker ist die Dolt-Datenbank unter `.beads/`; das Lesen erfordert `tools/bd show`, was der Runner, nicht der Explorer ausführt). Ob „Schwarm-Test-Geschwindigkeit" nur `tests/test_stage2_swarm.py` bedeutet oder auch die Dispatch-/Deep-Review-/Terms-Dateien, die dieselbe Welt wiederverwenden, ist eine Interviewfrage.
- Ob `plans/changes/research-swarm/plan.md` (Perle icw, selbst noch Draft gemäß `plans/INDEX.md`) geändert werden darf — das entscheidet, ob Tests in der Ledger-Datei umbenannt/zusammengeführt werden dürfen oder nur an Ort und Stelle beschleunigt werden können.
- Im Repository existiert keine Baseline-Messung: kein Gate oder Artefakt zeichnet Suite- oder Testdauern auf (keine `-durations`-Flagge, kein Benchmark-Notizbuch in `docs/research/`; in `gates.yaml`, `Makefile` und `docs/WORKFLOW.md` nachgeschaut — nicht gefunden). Jedes „schneller"-Ziel hat derzeit keine Zahl, mit der man es vergleichen könnte.
- Keine Ablösung in `docs/journal/handover/` nennt `swarm-test-speed` oder `dca4` (grep über das Verzeichnis — keine Übereinstimmung), also ist der Beweggrund nicht im Journal festgehalten; das Eröffnen der Änderung geschah auf diesem Zweig, nachdem die letzte Ablösung geschrieben wurde.

### Welche Dateien eine Änderung berühren müsste

- Unvermeidlich: `tests/test_stage2_swarm.py` (Fixture, Stand-in, Schlafdauern, Anzahl der Läufe pro Fall).
- Wahrscheinlich: `tests/terms_fixtures.py` und die beiden wiederverwendenden Dateien `tests/test_stage2_terms_expiry.py`, `tests/test_stage2_research_deep_review.py` (wenn das Fixture/der Aufbau eine gemeinsame Optimierung erhält).
- Nur wenn das Gate selbst aktiviert wird: `decisions/gates.yaml` plus das Pin `tests/test_ci.py` plus das neu generierte `.github/workflows/ci.yml` (jede Änderung am Pytest-Aufruf, z. B. Dauerberichterstattung oder Sharding, berührt alle drei).
- Nur wenn ein fixierter Testname wechselt: `plans/changes/research-swarm/plan.md` (Kriterium-Ledger).
- Nur wenn die pro Slot anfallenden Kosten (Neu-Parsen der Erklärung, Leak-Check-Umfang, `TICK`) im Rahmen liegen: `scripts/stage2_research_run.py`, `scripts/stage2_research_dispatch.py`, `scripts/stage2_availability.py` — eine Verhaltensänderung dort wäre mehr als eine test-only begrenzte Änderung und sollte im Interview benannt werden.

---

Zum Rahmen: Das war Phase 1 für `swarm-test-speed` (Klasse `bounded`, GLM-5.3-Flash-Route). Ich habe nichts entworfen, empfohlen, bewertet oder eine Datei geändert; der Bericht oben ist reiner Befund mit Quellen. Offen für das Interview bleibt vor allem der Perle-Text (`tools/bd show coding-harness-dca4`) als konkreter nächster Schritt des Runner, plus die Basismessung, die noch fehlt.
