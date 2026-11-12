---
title: "Research — verify-cheap-first"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.1
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3-flash, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
---

# verify cheap first — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). The
intent below was written by the orchestrator (Claude Code) before the first
call; the runner exploration (GLM 5.3 Flash) follows it unchanged. The model
answered in German against the house rule; its text is kept as recorded and
the spec restates what it uses in English.

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-bxxt.1, class bounded. Between 2026-11-04 and 2026-11-09,
11 red full runs of `make verify` had a green test gate and failed afterwards
on a gate that takes seconds (front-matter currency 8 times, question context
3 times): 3.3 hours of test execution for a result that was available at
once. Wanted: `scripts/verify_all.sh` orders the blocking gates cheapest
first — the order is declared once, not hard-coded twice — and ends a local
run at the first red blocking gate, naming the gates it did not run. Hosted
CI keeps running every gate. Done when a planted red front-matter gate ends a
local run before the test gate starts, a green run still runs every gate, and
tests pin both. Source: `docs/research/2026-11-09-make-verify-long-term.md`.
The maintainer asked on 2026-11-10 for the speed-up of the full check as fast
as possible.

Questions for the exploration: where the gate order is declared today
(`decisions/gates.yaml`, `scripts/ci_gates.py`, `scripts/verify_all.sh`) and
whether the order can change without editing the held file
`decisions/gates.yaml`; how a report-only gate differs from a blocking one in
the run; which callers read the full list of gate results (the runner's
post-run check, the run log `verify-duration.jsonl`, the stop hook) and would
misread a run that ends early; how the `--job docs` subset is ordered.

Stage-2 call, 2026-11-10: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1007 files, 3865 commits, 12 rules.

## Runner exploration — 2026-11-10

Die Exploration ist abgeschlossen — alle Quellen gelesen, alle Verbraucher des Lauf-Verhaltens geprüft. Hier die Forschung als Prosa, bereit zum Anhängen an `plans/changes/verify-cheap-first/research.md`:

---

## Was es heute gibt

**Die eine Liste enthält die Reihenfolge; es gibt kein separates Ordnungs-Datum.** Die Reihenfolge der Gates ist die Sequenz von `gates:` in `decisions/gates.yaml` (seine Kopfzeile ist „THE ONE LIST (D-10/O-4, bead coding-harness-bo0)"). Das Schema (`schema_version: 2`, validiert durch `validate_schema` in `scripts/ci_gates.py`) deklariert `id, title, command, action, job, enforcement, floor, placement, needs_tracker, needs_history, subsets, reason` — kein `order:`, Kosten- oder Dauerfeld. `gates()` in `scripts/ci_gates.py` gibt die Gates „in ihrer Reihenfolge" zurück, und `--commands --tsv` (der Reader-Schleife `main`) gibt sie genau in dieser Reihenfolge aus. Drei Reihenfolgen werden derzeit von dieser einen Sequenz abgeleitet: die lokale Runner-Reihenfolge, die Reihenfolge des CI-Befehlsschritts (mit Action-Gates im Voraus in `generate_ci`) und die Reihenfolge des `--job docs`-Subsets.

**Heutige lokale Reihenfolge: zuerst pytest.** Die Verifizierungs-Job-Gates in Dateireihenfolge: `pytest` (block, floor, both), `ruff-check`, `ruff-format`, `leerprobe`, `plans-registry`, `docs-links` (report), `frontmatter-current` (block), `bead-export`, `dangling-beads`, `decision-continuity`, `adr-answers`, `interview-minimums`, `question-context` (block), `criterion-ledger`, `research-handoff`, `guard-test-environment`, `gate-schema`, `ci-drift`, `ramp-valves`, `ruleset` (writer — lokal, nicht CI), `markdownlint` (action mit lokalem npx-Äquivalent, report), `lychee` (action, advisory, nur hosted — lokal übersprungen). Das `reason`-Feld des pytest-Gates besagt wörtlich „make verify führt es zuerst aus" (`decisions/gates.yaml`, Gate `pytest`).

**Gemessene Kosten pro Gate** (`docs/research/2026-11-04-verify-duration-baseline.md`, „Wo die Zeit hin geht", Median über fünf grüne Läufe vom 2026-11-05): pytest 991 s (81 % eines Median-Laufs von 1.223 s), leerprobe 196 s (16 %), markdownlint 10 s, ruleset 9 s, frontmatter-current 6 s, die anderen 15 Gates ≤ 2 s jeweils. Die teuren Gates laufen zuerst; die beiden Gates, die die 11 roten Läufe nach einem grünen pytest verursacht haben — `frontmatter-current` (8×) und `question-context` (3×) — kosten 6 s bzw. ≤ 2 s und laufen danach (`docs/research/2026-11-09-make-verify-long-term.md`, Aufzählungspunkt „Reihenfolge der Gates").

**Der lokale Runner hört nach einem Fehler nicht auf.** `scripts/verify_all.sh` ruft `ci_gates.py --commands --job "$JOB" --placement "$platzierung" --tsv` einmal auf und durchläuft die TSV-Zeilen (`id`, `enforcement`, `command`) in einer `while read`-Schleife, wobei jedes Gate über `sh -c` gestartet wird. Nur `enf = block` setzt `fehler=1`; ein `report`/`advisory`-Fehler gibt „rot, aber nur …" aus, ohne zu blockieren. Die Schleife enthält kein `break`: Nach einem roten Block-Gate läuft jedes verbleibende Gate, und die endgültige Ausgabe „VERIFY RED" wird ganz am Ende gedruckt. Für Gates, die ein Early-Stop übersprungen hätte, existiert heute keine Meldung.

**Das gehostete CI führt bereits nach einem Fehler jedes Gate aus.** Jeder abgeleitete Gate-Schritt trägt `if: ${{ !cancelled() }}` (`_schritt` in `scripts/ci_gates.py`, bead coding-harness-bl2), die Matrix-Job trägt `fail-fast: false`, und advisory/report-Schritte tragen `continue-on-error: true`. Festgelegt durch `test_every_step_after_a_failing_gate_still_runs` (`tests/test_ci.py:258`) und `test_every_gate_step_runs_even_after_a_failing_gate` (`tests/test_ci.py:433`).

**Der Vorgang zum vorzeitigen Stopp existiert bereits eine Ebene tiefer.** `run_targeted` (`scripts/stage2.py:6100`) führt die ausgewählten Gates „in Gate-Listen-Reihenfolge durch den gesperrten Interpreter aus, so wie `verify_all.sh` sie ausführt", und „das erste blockierende Rot, ein Startfehler oder Timeout beendet den Lauf"; ein report/advisory-Failure wird nur notiert. Die Gate-Auswahl stammt aus `targeted_selection` (`scripts/stage2.py:5941`), das `ci_gates.gates()` in Dateireihenfolge liest (docs-Subset immer, `leerprobe` bei Mitgliedschaft, Gates deren Befehls-Einstiegspunkte eine geänderte Datei schneiden) — es liest die Ausgabe eines roten Laufs nicht.

**Verbraucher der Laufausgabe und des Logs:**
- `red_sections` (`scripts/stage2.py:5243`), verwendet von `verify_evidence` (:5410), parst die Frames des Runners — `GATE_START` `── [gid] $ ` und `GATE_END` `── [gid] <verdict>` (:5214–5216) — und sammelt `RED (block)`-Abschnitte als Reparaturdiagnose. Es verarbeitet null bis mehrere rote Abschnitte; ein Lauf, der nach dem ersten roten Block endet, ergibt einen Abschnitt. Eine Meldung zu übersprungenen Gates, die nicht mit dem Frame-Format beginnen, ist für den Parser unsichtbar. Die Cross-Check `test_the_frames_red_sections_reads_are_the_ones_verify_all_prints` (`tests/test_stage2.py:2635`) liest die Runner-Quelle und verlangt, dass beide Frame-Schreibweisen dort stehen bleiben.
- `failed_test_ids` (`scripts/stage2.py:5634`) liest `FAILED <node id>`-Zeilen aus pytest-Zusammenfassungen im `make verify`-Output für die Retry-Auswahl der Reparatur; ein Lauf, der vor pytest endet, hat nichts davon zu bieten.
- Die Dauerhistorie (`scripts/verify_duration.py`): pro ausgeführtem Gate einen `gate`-Event (der seine `enforcement` enthält), einen `run_end` mit dem finalen Verdict. Ein früh gestoppter roter Lauf erhält immer noch seinen roten `run_end` vom Runner; ein getöteter Lauf ohne einen erhält „incomplete". Der Reader `cmd_report` zeigt `len(run['gates'])`-Gates pro Lauf.
- `scripts/run_report.py` listet Live-Prozesse, die `bash scripts/verify_all.sh` entsprechen (`tests/test_run_report.py:389`); es liest keine Gate-Ergebnisse.
- **Der Stop-Hook ist nicht in diesem Repository.** `docs/WORKFLOW.md:524` dokumentiert `.claude/hooks/session-stop/check-tests-green.sh`, aber der Pfad existiert nicht im Tree, und `docs/WORKFLOW.md:35–38` sagt genau das: der Hook gehört zu den Teilen, die „nicht in diesem Repository" sind. In diesem Repository liest er folglich keine Gate-Ergebnisse.

**Das `--job docs`-Subset** wählt verify-Gates mit `docs` in `subsets` (`in_job`, `scripts/ci_gates.py`), ausgeben in Dateireihenfolge: plans-registry, docs-links, frontmatter-current, dangling-beads, decision-continuity, adr-answers, interview-minimums, question-context, criterion-ledger, research-handoff, markdownlint. Kein pytest. Der Entwurfs-Post-Run-Check der Runners ist genau dieser Befehl, `DOCS_VERIFY = ["bash", "scripts/verify_all.sh", "--job", "docs"]` (`scripts/stage2.py:9063`).

**Pins, die das aktuelle Verhalten halten** (ein Änderungs-Touch-Bundle):
- `test_runner_worker_default_preserves_gate_verdicts` (`tests/test_ci.py:1701`): über eine synthetische Alpha/Beta/Gamma-Gate-Datei behauptet es „ein advisory und sogar ein blockierender Fehler stoppen nichts" und dass alle drei Gates in Listenreihenfolge laufen, sowohl bei advisory als auch bei blockierendem Versagen (:1739–1741).
- Teil (B) von `test_timing_preserves_job_selection_enforcement_and_nested_admission` (`tests/test_ci.py:2296–2315`): „der Lauf ist rot und das Gate danach läuft trotzdem" mit der Behauptung „ein Fehler stoppte die späteren Gates".
- `test_runner_holds_no_command_list_of_its_own` (`tests/test_ci.py:1255`): der Runner darf nur `ci_gates.py` und `verify_duration.py` aufrufen — eine Bestellregel kann nicht als Handliste in die Shell des Runners.
- `test_the_makefile_runs_what_the_one_list_runs` (`tests/test_ci.py:507`) hält die Makefile-Rezeptzeilen wörtlich an die Gate-Datei.
- CI-seitig müssen die beiden Pins „jeder Schritt läuft nach einem Fehler" (:258, :433) bestehen bleiben — die Absicht des Beads hält das CI-Verhalten fest.
- `tests/test_gate_catalog.py` hält `docs/governance/gate-catalog.md` (generiert durch `ci_gates.py --catalog`, „in Listenreihenfolge" gemäß `catalog_rows`) an das Rendering — eine Neuanordnung der Gate-Datei verschiebt Katalogzeilen.
- Das `ci-drift`-Gate hält `.github/workflows/ci.yml` an `--generate-ci` — eine Neuanordnung der Gate-Datei ordnet CI-Befehlsschritte neu an, sodass das generierte Workflow in derselben Änderung neu generiert werden muss.

## Was unklar ist

- Ob ein Stop-Hook außerhalb dieses Repositorys (Benutzerebene) die `make verify`-Ausgabe liest und einen vorzeitigen Stopp falsch interpretieren könnte, war von diesem Worktree aus nicht lesbar.
- Kein ADR regiert die Gate-Reihenfolge: eine Suche von `decisions/` nach `gate order / cheap / fail-fast / Reihenfolge` fand nichts. Ich habe nicht nach jeder möglichen Formulierung gesucht; eine anders betitelte ADR bleibt ein possibility, keine Feststellung.
- In `scripts/verify_duration.py` und den stage2-Verbrauchern, die ich vollständig gelesen habe, habe ich nichts gefunden, das die Gate-Anzahl eines Laufs mit der deklarierten Anzahl vergleicht (`gates_job` aus `ci_gates.py --report` wird pro Lauf nirgendwo gegen die gemessenen Gate-Events geprüft). Das ist eine „nicht gefunden"-Aussage über diese Leser, keine Garantie über jedes Skript.
- Verwandte archivierte Änderungen, die ich über Dateilisten, aber nicht Inhaltlich gefunden habe — `plans/changes/archive/2026-11-06-verify-duration/`, `2026-11-06-verify-machine-lock/`, `2026-10-08-runner-red-gate/`, `2026-11-06-draft-gates-only/` — sind wahrscheinlich Nachbarn (der Frame-Format-Bead `runner-red-gate` und die Dauererhöhung `1um6` sind in den Quellen benannt, die ich gelesen habe); nur `2026-11-06-fail-fast-attempts/` habe ich gelesen (`spec.md`: die Versuchsebene billige Checks — ruff über geänderte Dateien, ausgewähltes pytest — vor `make verify`, eine andere Ebene als die Gate-Schleife).

## Was eine Änderung berühren müsste

`decisions/gates.yaml` (Reihenfolge oder ein neues Ordnungs-/Kostenfeld, plus das „führt es zuerst aus" `reason` von pytest); `scripts/ci_gates.py` (`validate_schema` wenn ein Feld hinzugefügt wird, die `--commands`-Ausgabe, `--generate-ci` muss die heutigen CI-Semantiken halten); `.github/workflows/ci.yml` neu generiert (ci-drift ratchet); `docs/governance/gate-catalog.md` neu generiert (`--catalog`); `scripts/verify_all.sh` (der Early-Stop und das Benennen der nicht ausgeführten Gates, Frames Parser-kompatibel halten); die Pins in `tests/test_ci.py` (:1701, :2296 Teil B, Grenze :1255) und `tests/test_stage2.py` (:2635 Cross-Check, plus die Docs-Check-Evidenz-Tests, die einen `── [adr-answers] RED (block)`-Frame behaupten); und Tests, die das in der Bead-Absicht genannte Verhalten festlegen — ein gepflanztes rotes Frontmatter-Gate beendet einen lokalen Lauf vor pytest, ein grüner Lauf führt immer noch jedes Gate aus.

---

Notiz für die `neighbours:`-Kopfzeile: die drei archivierten Änderungen `2026-11-06-verify-duration`, `2026-10-08-runner-red-gate` und `2026-11-06-draft-gates-only` (sowie die bereits gelistete Research-Notiz) sind Kandidaten-Nachbarn, die ich nur über ihre Dateinamen und die Zitate anderer Artefakte kenne.
