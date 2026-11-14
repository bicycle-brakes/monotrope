---
title: "Research — bd-1-3-4"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-tr84
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-14", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# bd 1 3 4 — Research

Stage-2 call, 2026-11-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1072 files, 4219 commits, 12 rules.

## Runner exploration — 2026-11-14

Die Recherche ist vollständig. Hier ist die Prosa, die an `plans/changes/bd-1-3-4/research.md` angehängt werden soll — dies ist das Ergebnis des Phase-1-Explorers für den GLM-Flash-Flash-Lauf (Bead `coding-harness-tr84`, Stage-2-Aufruf vom 2026-11-14, oben im Skelett vermerkt).

---

## research.md Ergänzung

### Header-Vorschlag für die `neighbours:`-Zeile

`plans/changes/archive/2026-11-06-pi-pin/spec.md` (die pin-Bump-Präzedenzfalle), `plans/changes/archive/2026-09-21-reproducible-bead-export/research.md` (render identity & machine-local fields), `plans/changes/ci-bead-summary/research.md` (tracker reads through `tools/bd`).

### Was es heute gibt

Das Repository pinnt das Beads-CLI (`bd`) auf eine genaue Version und leitet jeden Aufruf über einen Wrapper. Der Pin selbst ist die Datei `tools/beads/VERSION` und enthält aktuell `1.3.0`. Der Änderungsname `bd-1-3-4` lautet Version 1.3.4: Das ist die Interpretation, die die Repository-Beweise tragen — der Pin ist ein drei-teiliges Version-String desselben Schemas, der letzte Pin-Schritt (1.1.2 → 1.3.0) als "tracker pin to bd 1.3.0" dokumentiert ist (`docs/journal/handover/2026-09-17-tracker-pin-and-session-end-interview.md`, Titel und Abschnitt "What changed in this repository"), und kein anderes nummeriertes Schema (1.3.4 kommt in keinem verfolgten Dokument vor — `plans/INDEX.md` listet nur den Änderungsordner). Die eigene Überschrift des Beads und seine Beschreibung konnten für diese Forschung nicht gelesen werden: Der Tracker ist die Dolt-Datenbank auf `refs/dolt/data` on origin (`AGENTS.md`, Hausregel 2), und keine verfolgte Datei oder das lokale `.beads/`-Verzeichnis (`metadata.json`, `config.yaml`, `interactions.jsonl`) enthält `tr84`. Das ist ein "konnte nicht lesen", kein "nicht vorhanden".

Der Wrapper `tools/bd` liest den Pin (`PINNED` in Zeile 23), löst zuerst das versionierte Binärfile `~/.local/bin/bd-<pinned version>` auf (`BD_BIN`, Zeile 33), greift auf das `bd` in PATH zurück, weigert sich bei einer Nichtübereinstimmung (`INSTALLED != PINNED`, Zeile 49–54), weigert die drei verbbasierten Operationen `init`, `migrate`, `upgrade`, sofern nicht `BD_PIN_BYPASS=1` (Zeile 56–62) gesetzt ist, und beendet mit Code 127, wenn kein Binary gefunden wird — ein Exit-Code, den `scripts/render_beads_export.py` (`BD_FEHLT`, Zeile 35) explizit als "the tracker does not live on this machine" konsumiert. Der Header-Kommentar des Wrappers erklärt die Versions-Side-by-Side-Logik: "a newer bd migrates a store's schema on open — a one-way step" (`tools/bd`, Zeilen 27–28) und benennt die Escape-Hatch-Begründung: "a future schema upgrade has to run `bd migrate` once, on one machine" (Zeilen 16–19).

Der Installer `tools/beads/install.sh` leitet die Version vom selben Pin ab (`VERSION` aus `tools/beads/VERSION`, Zeile 18), baut den Tarball-Namen `beads_<version>_<os>_<arch>.tar.gz` (Zeile 31), benötigt die Checksum-Datei `tools/beads/checksums/<tarball>.sha256` und lehnt die Installation geschlossen ab, wenn sie fehlt (Zeilen 32–36; die Nichtübereinstimmungs-Nachricht ist auf Deutsch, Zeilen 57–60), lädt von `https://github.com/steveyegge/beads/releases/download/v<version>/…` (Zeile 44) herunter, installiert nach `~/.local/bin/bd-<version>` (Zeile 69) und überspringt den Download, wenn dieses Ziel bereits vorhanden ist und die Version meldet (Zeilen 38–42). Checksums existieren heute für genau zwei Plattformen: `tools/beads/checksums/beads_1.3.0_darwin_arm64.tar.gz.sha256` und `beads_1.3.0_linux_amd64.tar.gz.sha256`; die linux-Datei enthält `2f92b904…cdcf3b` — denselben Hash, der in `tools/cloud-env/setup.sh` (`BD_SHA256`, Zeile 10) dupliziert wurde.

Eine zweite, unabhängige Installationsstelle existiert: `tools/cloud-env/setup.sh`硬codiert `BD_VERSION=1.3.0` und den linux-Hash (Zeilen 9–10) — es liest `tools/beads/VERSION` nicht, weil es "outside any checkout" läuft (Kopfzeilenkommentar, Zeilen 2–5). Die eigene "Known limits" der README benennt die Kopplungslücke ausdrücklich: "A bd version bump has to change both; no check holds them together yet" (`tools/cloud-env/README.md`, Zeilen 38–41). Das README erwähnt die installierte Version auch in Prosa ("**bd 1.3.0** to `~/.local/bin/bd-1.3.0`", Zeilen 20–21).

CI installiert `bd` durch den Installer ohne jedes Version-Literal: Der Schritt "Hydrate the tracker (pinned bd, checksum-verified)" (id `setup-tracker`) führt `bash tools/beads/install.sh`, dann `bash tools/bd bootstrap --yes` in beiden Jobs aus (`.github/workflows/ci.yml`, Zeilen 48–61 und 186–199). `tests/test_ci.py` (`test_…`, Assertion bei Zeile 313) prüft nur, dass die Installer-Zeile vorhanden ist. Fünf Git-Hooks führen das nackte `bd` über den PATH-Shim `tools/beads/bin/bd` aus, der durch den Wrapper (`exec "$here/../../bd"`) weiterleitet — versionsunabhängig. Jede der fünf Hook-Dateien trägt noch einen verwalteten Abschnitt, der von einem älteren bd installiert wurde: `--- BEGIN BEADS INTEGRATION v1.1.2 ---` in allen fünf unter `.beads/hooks/` (pre-commit, pre-push, post-merge, post-checkout, prepare-commit-msg). Der Pin-Schritt von 2026-09-17 hat sie NICHT aktualisiert — die Marker sagen immer noch v1.1.2, während der Pin 1.3.0 ist. Das ist die Repository-Präzedenz für, was der letzte Schritt am Hooks nicht tat.

Das Verhalten des Renderers ist version-sensibel an einer Stelle: `scripts/render_beads_export.py` dokumentiert, dass "bd 1.3.0 writes `heartbeat_at` and `lease_expires_at` into the writer's export" und listet diese beiden Maschinen-lokalen Felder einmal in `MASCHINENLOKAL` auf (Zeilen 38–45); wenn die Notation des Trackers ändert, weigert sich das Skript, still umzuschreiben (`NichtReproduzierbar`, Zeilen 52; der Byte-für-Byte-Wiedergabe-Wächter, `_ohne_maschinenlokales`, Zeilen 63+). Die Forschungsnotiz der Archived-Änderung `2026-09-21-reproducible-bead-export` fügte hinzu, dass "not found is not 'not there'" — ob bd weitere Maschinen-lokale Felder in anderen Situationen behält, war offen, als die Notiz geschrieben wurde (deren "What is unclear", Zeilen 59–64). Der Tracker-Zugriff für Gates läuft durch `scripts/bead_render.py` (neues Rendering über `tools/bd` oder das Voreingestellte `BEAD_RENDER`, `render_pfad`, Zeilen 81–106; exit 3 "nicht gemessen", `nicht_gemessen`, Zeilen 109–117) — jedes Gate, das den Tracker liest, läuft indirekt auf der Version, die der Wrapper bereitstellt.

Pin-Historie und Schema-Lehre: Der Wrapper kam am Tag 1 mit Pin 1.1.2 herauf (`docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`, Zeilen 62–64). Der Schritt auf 1.3.0 war reaktiv und trägt die Kernlehre der Änderung: "The tracker store had been migrated to schema v66 overnight, and bd 1.1.2 refuses that store" und "bd 1.3.0 migrates a store when it opens it — a one-way write" (Handover 2026-09-17, Zeilen 37–38 und 83). Derselbe Handover dokumentiert auch die machines-seitige Konsequenz, die außerhalb dieses Repos bleibt: der globale `bd`-Guard des Maintainers bei `~/.local/bin/bd` (exit 64), der die Customer-Instanz-Store auf dem 1.1.2-Schema vor jedem neueren bd schützt (Zeilen 80–88).

Nichts testiert die Wrapper-Logik selbst: `BD_PIN_BYPASS` kommt nur im Wrapper und zwei historischen Dokumenten vor; die Tests, die `tools/bd` referenzieren (`tests/test_beads_start.py`, `tests/test_close_merged_beads.py`, `tests/test_gate_machinery.py`, `tests/test_omnigent_deny_layers.py`, `tests/test_archive_closed_changes.py`), ersetzen alle durch Stand-in-Fälschungen für den Tracker und üben die Versionsprüfung, den Bypass oder die 127-Semantik des Wrappers nicht aus — "nicht gefunden" durch gezielte Suche nach `BD_PIN_BYPASS`, `beads/VERSION` und `checksum` unter `tests/`. Kein Test hält `tools/cloud-env/setup.sh`'s `BD_VERSION` an den Pin oder die Checksums-Verzeichnis — "nicht gefunden", derselbe Suchlauf; die README bestätigt es in Prosa (siehe oben).

### Wo es lebt

- Pin: `tools/beads/VERSION` (eine Zeile, `1.3.0`).
- Wrapper: `tools/bd` (Versionsprüfung, versionierte Binärsuche, Verweigerung der Verben, Escape-Hatch, exit 127).
- Installer: `tools/beads/install.sh` (Versionsabgeleitet, Plattformerkennung, fail-closed Checksumme, versioniertes Ziel); Hook-Shim: `tools/beads/bin/bd`.
- Checksums: `tools/beads/checksums/beads_1.3.0_{darwin_arm64,linux_amd64}.tar.gz.sha256` — nur diese beiden.
- Zweite Installationsstelle: `tools/cloud-env/setup.sh` (`BD_VERSION`, `BD_SHA256`, linux amd64 only) + Prosa-Version-Nennungen in `tools/cloud-env/README.md`.
- CI: `.github/workflows/ci.yml`, "Hydrate the tracker" (`setup-tracker`) in beiden Jobs — kein Literal, Assertion in `tests/test_ci.py` (Installer-Zeile).
- Hooks: `.beads/hooks/*` — Shims versionsunabhängig, verwaltete Abschnitte noch als `v1.1.2` beschriftet.
- Versions-sensitive Verhalten: `scripts/render_beads_export.py` (`MASCHINENLOKAL`, Wiedergabe-Wächter); Tracker-Rendering für Gates: `scripts/bead_render.py`.
- Geschichtlicher Präzedenzfall: `docs/journal/handover/2026-09-16-coding-harness-bootstrap.md`, `docs/journal/handover/2026-09-17-tracker-pin-and-session-end-interview.md`; Änderungs-Präzedenzfall für Pin-Arbeit: `plans/changes/archive/2026-11-06-pi-pin/` (spec, design, plan, research, decisions, findings — Klasse `feature` mit ADR 0019); Render-Vertragskontext: `docs/adr/0004-tracker-render-is-the-contract.md`, `docs/adr/0002-exclusive-coordinator-writer.md` (Renderer-Halter), `docs/adr/0005-workers-claim-their-own-bead.md` (Claim-Messung auf bd 1.3.0, Zeile 43).

### Was unklar daran ist

- Die Überschrift des Beads `coding-harness-tr84` und seine Beschreibung waren für diese Phase nicht lesbar (Dolt-Tracker unter `refs/dolt/data`; nichts Verfolgtes oder lokales unter `.beads/` nennt es). Die Lesung "bump the bd pin 1.3.0 → 1.3.4" folgt aus dem Änderungsnamen und den Repository-Beweisen; die eigene Wortwahl des Beads ist ein offene Frage.
- Ob Upstream Releases 1.3.1 bis 1.3.4 existieren, welchen Hashes ihre Tarballs tragen und ob irgendein zwischen 1.3.0 und 1.3.4 den Store-Schema oder die Export-JSON-Notation ändert, ist im Repository nicht entscheidbar — die Release-Seite von `steveyegge/beads` ist außerhalb. Ob `bd migrate` einmal benötigt wird (die Escape-Hatch-Situation, für die `tools/bd` Zeilen 16–19 existieren) hängt genau davon ab. Vorherige Messungen hier (Claim-Test, ADR 0005 Zeile 43; Worktree-Fünf-Check, `docs/research/2026-09-23-worktree-tracker-writes.md` Zeilen 23, 36) sind auf 1.3.0 gebunden und veralten still, wenn der Pin sich ohne Neumessung bewegt.
- Ob 1.3.4 die verwalteten Hook-Abschnitte neu schreiben möchte, wenn `bd hooks install` von der neuen Version ausgeführt wird, und ob die Abschnitte überhaupt aktualisiert werden sollen, ist im Repository nicht entscheidbar — sie sagen immer noch `v1.1.2` nach dem 1.3.0 Schritt, so dass die Präzedenz "leave them" ist, aber der Handover dokumentiert die Entscheidung nicht explizit.
- Ob bd 1.3.4 weitere Maschinen-lokale Export-Felder jenseits von `heartbeat_at`/`lease_expires_at` einführt (`MASCHINENLOKAL` in `scripts/render_beads_export.py`) ist unbekannt; die 2026-09-21 Forschungsnotiz benannte dieselbe Unklarheit für 1.3.0 und löste sie nicht.
- Ob `tools/bd bootstrap --yes` (CI und `tools/cloud-env/setup.sh` Zeilen 55, 56; AGENTS.md Hausregel 2) sich zwischen den Versionen verhält, ist hier nicht dokumentiert; der Bootstrap der Hydrations-Hydrations-Seiteneffekte (Schreiben von `.beads/.gitignore` und `.beads/config.yaml`, durch ADR 0004 "Decision", Zeilen 85–87 und die cloud-env Wiederherstellung in `setup.sh` Zeile 56) sind die bekannte Oberfläche.

### Welche Dateien eine Änderung berühren müsste

- `tools/beads/VERSION` — der Pin selbst.
- `tools/beads/checksums/` — Checksum-Dateien für die neue Version, minimal in den zwei Plattformen, die der Installer und die Cloud-Umgebung heute abdecken (`darwin_arm64`, `linux_amd64`).
- `tools/cloud-env/setup.sh` — `BD_VERSION` und `BD_SHA256` (Zeilen 9–10); `tools/cloud-env/README.md` — die Version-Nennungen (Zeilen 20–21) und die Checksum-Kopie-Bemerkung (Zeilen 38–41). README's eigene Worte: eine Bump-Änderung muss beide Stellen treffen, kein Check hält sie zusammen.
- `.github/workflows/ci.yml` — nur wenn der Hydrationsschritt selbst etwas zu sagen bekommt; heute trägt er kein Version-Literal (Änderung fließt durch VERSION + Checksums).
- `scripts/render_beads_export.py` — nur wenn die Exportnotation oder die Maschinen-lokalen Felder unter der neuen Version sich ändern (`MASCHINENLOKAL`, Wiedergabe-Wächter entscheidet dann selbst).
- `.beads/hooks/*` — nur wenn die verwalteten Abschnitte aktualisiert werden sollen (Präzedenz: beim 1.3.0 Schritt nicht berührt).
- Evidenz-Aktualisierung: die auf 1.3.0 gebundenen Messungs-Sätze in `docs/WORKFLOW.md` (Zeile 776), `docs/adr/0005-workers-claim-their-own-bead.md` (Zeile 43), `docs/research/2026-09-23-worktree-tracker-writes.md` — historische Sätze; ob sie neu gemessen oder nur datiert werden, ist eine Spezifikationsphase-Frage.
- Die deutschen Installer-Nachrichten in `tools/beads/install.sh` (Zeilen 34, 57–60) sind im Baum, aber `AGENTS.md` Hausregel 1 weist In-Baum-Übersetzungen ihren eigenen Pull-Requests zu (Bead `coding-harness-yim`) — hier als benachbarte Grenze notiert, nicht als Teil dieses Änderungspfads.

### Offene Fragen für den Menschen

Keine, die den Explore blockieren. Die eine Frage, die beim Spec ankommt, ist die oben unbeantwortbare: ob 1.3.1–1.3.4 das Store-Schema ändern (und so die einmalige `bd migrate` mit `BD_PIN_BYPASS=1` auslösen, deren Existenz `tools/bd` Zeilen 16–19 vorhergesehen) — das wird durch die Upstream-Release-Notizen plus eine Messung auf Kratzkopien beantwortet, bevor der gemeinsame Store geöffnet wird, nicht durch diese Phase.

---

Notiz für den Runner: das Skelett Frontmatter sagt `provenance: human-written`; pro seiner eigenen eingebetteten Anweisung und `provenance.yaml` (Klasse `ai-drafted-reviewed`, `review_required: true`) verschiebt das Füllen durch diese Phase die Frontmatter nach `ai-drafted-reviewed` mit `produced_by:` und `review:`. Die Stage-2-Zeile (2026-11-14) bleibt stehen.
