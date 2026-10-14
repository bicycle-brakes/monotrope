---
title: "Migrationsplan: Referenzarchitektur mit Omnigent instanziieren"
category: research
status: current
created: 2026-09-16
last_reviewed: 2026-09-16
updated: 2026-10-14
owner: Data Architect
provenance: ai-drafted-reviewed
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, migration, omnigent, referenzarchitektur]
---

# Migrationsplan: Referenzarchitektur mit Omnigent instanziieren

**Ziel:** Die arc42-Referenzarchitektur (Version 1.2) schrittweise in eine produktive Omnigent-Zieltopologie überführen — ohne Big Bang, ohne Unterbrechung laufender Arbeit, mit definierten Abbruchkriterien pro Stufe. Der Plan folgt dem Prozessgewichtungs-Prinzip der Architektur selbst (§8.2): Die Migration skaliert mit dem Risiko, nicht mit der Begeisterung.

**Grundprinzipien des Plans:**

1. **Fallback bleibt geübt.** Die tmux/Beads-Fallback-Topologie (§8.10) bleibt bis zum Abschluss von Stufe 4 voll funktionsfähig; jede Stufe kann ohne Arbeitsverlust zurückgerollt werden, weil die Modellwahrheit in Repo und Arbeitsgraph liegt, nicht im Omnigent-Server (Deployment-Invariante, §7).
2. **Jede Stufe hat Exit-Kriterien, keine Zeiträume.** Die Dauer hängt von Teamgröße und Nutzungsfrequenz ab; die Kriterien sind messbar und an die Qualitätsszenarien des arc42 (Q1–Q10) angelehnt.
3. **Nichts wird parallel doppelt geführt.** Pro Stufe gibt es genau eine aktive Topologie pro Workflow-Klasse — doppelte Task-Verfolgung oder doppelte Gate-Kanäle sind verboten (AG-1-Geist).

---

## Stufe 0: Voraussetzungen und POC (1–2 Wochen)

**Ziel:** Technische Machbarkeit beweisen, Reife-Risiken (§11: Alpha-Reife, CVE-Historie) an einem nicht-kritischen Pfad vermessen.

**Schritte:**

1. **Infrastruktur:** Omnigent-Server auf einer dedizierten Linux-Maschine (nicht dem Produktiv-Laptop) installieren; `bwrap` verifizieren (fehlt es, dürfen keine Terminals starten — das ist gewollt, IS-6); Omnigent-Version **pinnen** (exakte Versionsnummer dokumentieren, ADW-D17-Konsequenz); **Telemetrie-Opt-out als allererster Konfigurationsschritt** (C11-Pflicht).
2. **Policy-Basisset:** Die Approval Boundaries aus §8.4 als Server-Policies kodieren (unsandboxed Shell, Netzwerk-Egress, secret-haltende Pfade, Schreiben außerhalb des Repos, Workflow-Dispatch → block/approve). Policy-Dateien ins Repo legen und dem menschlich reviewten PR-Pfad unterstellen — von Anfang an, nicht nachträglich.
3. **Non-Vacuity-Test der Policies (§8.7):** Für jede Policy ein bekannt-böser Testfall: Agent anweisen, genau die blockierte Aktion zu versuchen (z. B. `cat ~/.ssh/id_rsa`, Schreiben nach `/tmp` außerhalb des Repos, `curl` zu externem Host). Erwartung: block oder approve-Prompt, plus Eintrag im Aktionslog. **Eine Policy, die im Test nicht feuert, ist nicht deployed** — das ist die Laufzeit-Non-Vacuity, die ECC fehlte.
4. **Beads-Integration prüfen:** Test-Repo mit `bd` initialisieren; verifizieren, dass Agenten-Sessions in Omnigent-Terminals `bd ready`/`bd update`/`bd close` korrekt ausführen und der Graph über Git synchronisiert; „Landing the Plane" (AG-5) einmal manuell durchspielen.
5. **Beobachtbarkeit prüfen:** Eine Session absichtlich in einen Blocker laufen lassen (Approval-Prompt offen lassen) und verifizieren, dass der Zustand in der Web-UI/auf dem Mobilgerät sichtbar wird (IS-3).

**Exit-Kriterien:**
- Alle Policies des Basissets feuern nachweislich (Non-Vacuity-Testprotokoll im Repo).
- Eine vollständige Beads-Task-Schleife (claim → implementieren → commit → close) in einer sandboxed Omnigent-Session ohne manuelle Eingriffe außerhalb der Approvals.
- Telemetrie-Opt-out nachgewiesen (Egress-Beobachtung der Server-Instanz).
- Rollback geübt: Dieselbe Task-Schleife einmal in der tmux-Fallback-Topologie wiederholt.

**Abbruchkriterien (zurück zu reinem Fallback):** Sandbox auf dem Zielsystem nicht funktionsfähig; Beads-CLI in Omnigent-Terminals nicht zuverlässig betreibbar; Alpha-Instabilität, die den POC-Arbeitsfluss mehr als einmal pro Tag unterbricht.

---

## Stufe 1: Bounded-Klasse produktiv (2–4 Wochen)

**Ziel:** Erster echter Arbeitsfluss — die risikoärmste Aufgabenklasse (Bounded: G1 kurz + G5, §8.2) läuft vollständig in der Omnigent-Topologie.

**Schritte:**

1. **Scope scharf ziehen:** Nur Bounded-Tasks (Änderung an existierendem, lesbarem Flow) in genau einem Repo. Feature- und Architectural-Klassen bleiben explizit im Fallback.
2. **G1/G5 über den Omnigent-Kanal:** Die kurze G1-Freigabe und das G5-Review laufen über die Omnigent-Session (Mensch-Gate-Kanal, §5.3); mindestens eine Freigabe bewusst vom Mobilgerät erteilen, um den Kanal zu üben.
3. **Worker-Instanziierung:** Bounded-Tasks als Beads claimen; Implementierung durch eine frische Session pro Task (I3) in eigener Pane (IS-1). Optional: **Aider als Worker** in der Omnigent-Pane (`aider --message "<Task-Beschreibung + FR-Referenz>"`), mit `git-commit-verify: true` in `.aider.conf.yml` (Pflicht wegen ADW-D11 — Aider umgeht Commit-Hooks sonst per Default) und Commit-Prompt-Konvention für Bead-/FR-Referenz (AG-7).
4. **Spend-Cap setzen:** Erstes hartes Kosten-Deckel pro Session (konservativ, z. B. doppelte erwartete Task-Kosten); Verhalten bei Erreichen beobachten.
5. **Kontextbudget-Telemetrie einschalten (KB-10):** Gate-Reports um die Kontextbelegung ergänzen; Baseline-Werte für Q8 sammeln.

**Exit-Kriterien:**
- ≥ 10 Bounded-Tasks vollständig in der Zieltopologie abgeschlossen, davon ≥ 1 mit Mobile-Approval.
- Q5 eingehalten: Prozess-Overhead ≤ 10 Minuten menschlicher Zeit pro Bounded-Task — *inklusive* der Policy-Approvals. Wenn Approvals den Bounded-Pfad über 10 Minuten drücken, sind die Policies zu feinmaschig (Review-Finding, Policies nachschärfen — nicht abschalten).
- Kein einziger Sandbox-Ausbruch oder Policy-Ausnahme-Approval ohne dokumentierten Grund im Aktionslog.
- Q8-Baseline vorliegend: Fixkosten-Belegung ≤ 15 % vor Arbeitsbeginn.

**Abbruchkriterien:** Q5 wiederholt verletzt trotz Policy-Nachschärfung; mehr als ein unerklärter Policy-Aussetzer (Policy feuert nicht, obwohl sie sollte — Non-Vacuity-Verletzung in Produktion).

---

## Stufe 2: Feature-Pfad mit Cross-Vendor-Review (4–8 Wochen)

**Ziel:** Der volle Gate-Pfad (G1–G5) läuft für die Feature-Klasse in der Zieltopologie — inklusive der anspruchsvollsten Neuerung: G4 als Cross-Vendor-Review.

**Schritte:**

1. **Vollständiger Artefakt-Pfad:** P0–P6 mit allen Artefakten (Spec, Design/ADRs, Plan, tasks.md → Beads-Transkription nach G3, AG-2). Die Gate-Anfragen G1–G3 laufen über den Omnigent-Kanal; die Artefakte bleiben Repo-Dateien (I1 — Omnigent transportiert, besitzt aber nichts).
2. **G4 als Cross-Vendor-Review einführen:** Implementierer-Session und Reviewer-Session aus **verschiedenen Harness-/Modellfamilien** (z. B. Implementierung via Claude Code, Review via Codex/OpenCode — je nach lizenzierten Harnesses). Reviewer-Input bleibt kuratiert: Diff per SHA-Range + Spec-Ausschnitt + Anforderungstext (§8.3), Befundklassifikation Critical/Important/Minor mit blockierender Wirkung.
3. **Verifikations-Report normieren:** P5-Abschluss als maschinell gatebarer `verification-report.md` (Build/Types/Lint/Tests/Security/Diff × PASS/FAIL × READY/NOT READY, §6.1); der Report ist das Evidenz-Verdict, nicht der Chat (KB-2).
4. **Nachtmodus-Probe (kontrolliert):** Ein einzelner, zeitlich begrenzter unbeaufsichtigter Lauf auf einem Feature-Task mit freigegebenem Plan: Stop-Bedingungen aktiv (P6-5), Spend-Cap hart, Heartbeat-Überwachung, am Morgen Aktionslog-Inspektion + G5. Q10 als Checkliste abarbeiten.
5. **Drift-Audit einplanen (SM-25):** Erstes periodisches Audit der Traceability-Kette (FR → Szenario → Test → Bead → Commit → PR → Change → Archiv, AG-7) nach zwei Wochen Feature-Betrieb.

**Exit-Kriterien:**
- ≥ 3 Features vollständig durch G1–G5 in der Zieltopologie; Q1 erfüllt (100 % FRs mit grünem Test).
- G4-Cross-Vendor-Review hat mindestens einen echten Befund gefunden, den die Selbstprüfung des Implementierers nicht gefunden hatte (Wirksamkeitsnachweis von I4 — sonst Konfiguration prüfen: gleicher Vendor? gleicher Kontext?).
- Q10-Checkliste für den Nachtmodus-Probelauf vollständig grün, inklusive Spend-Cap-Wirksamkeit.
- Drift-Audit ohne blockierende Befunde (oder Realign-Changes abgeschlossen ≤ 5 Arbeitstage, Q4).
- Q2-Stichprobe: Ein Außenstehender rekonstruiert ein Feature der Stufe allein aus dem Repo in < 10 Minuten.

**Abbruchkriterien:** Cross-Vendor-Review erweist sich als nicht betreibbar (Lizenz-/Setup-Hürden) — dann G4 auf interne Reviewer-Session mit verschärfter Kontext-Trennung zurückstufen und als technische Schuld in §11 eintragen; wiederholte Eskalations-Stürme am G4 (Review-Flut statt Review-Qualität → Befundschwellen und Input-Kurierung nachschärfen).

---

## Stufe 3: Nachtmodus und Parallelität als Standard (laufend)

**Ziel:** Unbeaufsichtigte Läufe und parallele Multi-Task-Ausführung werden Routine — die Stufe, in der die Zieltopologie ihren eigentlichen Produktivitätsgewinn entfaltet.

**Schritte:**

1. **Nachtmodus standardisieren:** Freigegebene Pläne (G1–G3 am Tag) laufen über Nacht ab; Standard-Profil: Cloud-Sandbox statt lokaler Maschine (kein Sleep-Problem, kein lokaler Blast Radius, IS-6), Spend-Cap pro Lauf, Mobile-Approval für Policy-Anfragen, morgendliches Ritual: Aktionslog-Inspektion → G4-Ergebnisse → G5.
2. **Parallelität über Worktrees:** Mehrere Beads gleichzeitig claimbar → parallele Sessions in eigenen Worktrees (P6-2: sequenzielles Mergen); Beads-Speichermodus bei Multi-Writer-Bedarf von Embedded auf Server-Modus umstellen (AG-6).
3. **Optional: Polly-Orchestrierung pilotieren** — *nur* wenn echte Parallelisierbarkeit vorliegt und die Token-Kosten der Orchestrierung gegen den Parallelisierungsgewinn gerechnet sind (§4 verwirft Orchestrierung als Default weiterhin; die Pilotierung selbst ist ein Bounded-Experiment mit eigenem Abbruchkriterium: Kosten × Nutzen < 1 → zurück zum manuellen Dispatch).
4. **Heartbeat-Prozessgruppen-Kill prüfen:** Supervisor-Modell (§8.4) einmal im Ernstfall testen (Heartbeat absichtlich aussetzen → Terminierung + Quarantäne muss greifen).

**Exit-Kriterien (Dauerbetrieb):**
- Nachtläufe liefern ≥ 1 mergbaren PR pro Woche bei null unerklärten Policy-Ausnahmen.
- Parallele Ausführung ohne Integrationskonflikte (sequenzielles Mergen eingehalten).
- Morgendliches G5-Ritual ≤ 15 Minuten pro Lauf (sonst lohnt der Nachtmodus nicht — ehrliche Rechnung).

---

## Stufe 4: Härtung, Vollausbau und Fallback-Abbau (nach Bedarf)

**Ziel:** Die optionale Evidenzebene aus dem Lösungsdokument nachrüsten und den Fallback von „geübt" auf „dokumentiert" herunterfahren.

**Schritte (priorisiert nach Aufwand/Nutzen):**

1. **Mutation-Score-Gate im CI (Lücke 1):** Diff-basierte Mutationsanalyse (PIT/Stryker/mutmut je nach Stack) als Quality Gate mit Mindest-Score; Known-Bad-Verifikation der Gates selbst in den Scheduled-CI-Job (§8.7).
2. **Evidenzgebundene Status (Lücke 3):** Attestierungs-Dateien unter `.workflow/attestations/` (hash-verkettet, mit dem Change committed); G5 prüft Attestierungs-Vollständigkeit. Vollausbau Witness/Archivista nur bei Compliance-Druck.
3. **Evidenzgebundener Confidence-Lifecycle (Lücke 2, ADW-D13-Schärfung):** Gelernte Regeln mit Evidenz-Metadaten (verweis auf verifizierte Commits/PRs); M_core-Schutz für verifizierte Invarianten; Promotion weiterhin menschlich.
4. **Traceability-Matrix als CI-Artefakt (Lücke 5):** FR × Test × Pfad-Matrix automatisiert berechnen; Lücken (FR ohne Test, Test ohne FR, Code ohne FR-Bezug) als blockierende Befunde (§8.5).
5. **Fallback-Härtung statt Abbau:** Die tmux-Fallback-Topologie wird nicht gelöscht, sondern als **Disaster-Recovery-Pfad** in der Betriebsdoku fixiert (inkl. halbjährlicher Übung — ein untrainierter Fallback ist kein Fallback).

---

## Übersicht: Stufen, Gates, Messlatten

| Stufe | Scope | Zentrale neue Fähigkeit | Messlatte (arc42-Referenz) | Rollback |
|---|---|---|---|---|
| 0 — POC | Test-Repo, keine Produktivarbeit | Policies feuern nachweislich (Non-Vacuity), Beads-Schleife, Telemetrie aus | Testprotokolle vollständig | tmux-Übung |
| 1 — Bounded | 1 Repo, Bounded-Klasse | Erster echter Fluss, Mobile-Approval, Spend-Cap, KB-10-Baseline | Q5 (≤ 10 min), Q8 (≤ 15 %) | Stufe-0-Zustand |
| 2 — Feature | Feature-Klasse, voller Gate-Pfad | Cross-Vendor-G4, normierter Verifikations-Report, Nachtmodus-Probe | Q1, Q2, Q4, Q10; G4-Wirksamkeitsnachweis | G4-Intern-Variante |
| 3 — Nachtmodus/Parallel | Dauerbetrieb | Cloud-Sandbox-Nachtläufe, Multi-Worktree-Parallelität, optional Polly | ≥ 1 PR/Woche aus Nachtläufen, G5-Ritual ≤ 15 min | Tagesbetrieb Stufe 2 |
| 4 — Härtung | Alle Klassen | Mutation-Gate, Attestierungen, Traceability-Matrix im CI | Lücken-Dokument Kap. 6 | Fallback als DR-Pfad |

**Querschnittsregeln für alle Stufen:**

- **Versions-Pinning mit Upgrade-Prozess (ADW-D17):** Omnigent-Upgrades nur nach Changelog-Lektüre und Test-Deployment; kein Auto-Update auf dem Produktiv-Server. Dasselbe gilt für `bd` (AG-6) und Aider.
- **Policy-Änderungen sind Regelwerk-Änderungen:** Sie durchlaufen den menschlich reviewten PR-Pfad (§8.4) — nie direkt auf dem Server editiert.
- **Keine zwei aktiven Topologien pro Workflow-Klasse:** Eine Klasse ist entweder migriert oder nicht; Mischzustände innerhalb einer Klasse erzeugen doppelte Wahrheiten.
- **Jede Stufe endet mit einer Retrospektive im Repo:** Befunde, Policy-Nachschärfungen und Reife-Beobachtungen (Alpha-Risiko!) werden als Change-Dokument abgelegt — die Migration selbst unterliegt denselben Artefakt-Regeln wie jede andere Arbeit am System (I1 gilt auch für den Migrationsprozess).

---

*Hinweis: Dieser Plan ist eine konzeptionelle Migrationsanleitung; konkrete Dauern, Spend-Cap-Höhen und Policy-Schärfe sind im jeweiligen Deployment zu kalibrieren. Er ersetzt keine Sicherheitsbewertung des Omnigent-Einsatzes im eigenen Bedrohungsmodell — insbesondere die Alpha-Reife (CVE-Historie) verlangt einen bewussten Upgrade-Prozess und die gepflegte Fallback-Topologie.*
