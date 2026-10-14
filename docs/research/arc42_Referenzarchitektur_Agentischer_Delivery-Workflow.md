---
title: "Referenzarchitektur „Agentischer Delivery-Workflow“ (ADW) — arc42"
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
tags: [research, arc42, adw, referenzarchitektur, omnigent]
---

# Architektur-Dokumentation nach arc42

## Referenzarchitektur „Agentischer Delivery-Workflow“ (ADW)

**Version 1.2 · Stand: 16. September 2026 (übernommen), Fassung 1.2 · Status: Referenzarchitektur (konzeptionell, werkzeugneutral in den Konventionen; Ziel-Instanziierung der Laufzeitschicht: Omnigent)**

> Dieses Dokument beschreibt die in den Vorarbeiten entwickelte Best-Practice-Architektur für agentengestützte Softwareentwicklung nach dem arc42-Template. „System“ ist hierbei das *socio-technische Gesamtsystem* aus Coding-Agenten, Menschen, Artefakten und Infrastruktur, das ein Softwareprodukt vom Zielbild bis zum Merge führt. Normative Anforderungen verwenden MUSS/SOLL/KANN; Phasen (P0–P6), Gates (G0–G5), Invarianten (I1–I6) und Spec-Management-Regeln (SM-1 bis SM-31) verweisen auf die Vorarbeiten und werden hier konsolidiert.

---

## 1. Einführung und Ziele

### 1.1 Aufgabenstellung

Die Architektur definiert, **wie Software mit agentischen Coding-Systemen so entwickelt wird, dass Qualität, Nachvollziehbarkeit und menschliche Kontrolle erhalten bleiben**, während der Durchsatz der Agenten genutzt wird. Konkret strukturiert das System den Weg von einer Produktidee über Spezifikation, Architektur, Planung und Implementierung bis zur Integration — einschließlich der Verwaltung der dabei entstehenden Spezifikationen (Übersicht, Versionierung, Änderungspropagation). Das System ist bewusst **harness-neutral**: Es instanziiert sich mit OpenCode, Claude Code, OpenHands, Cline, Goose oder Eigenbauten und setzt nur Protokoll- und Artefakt-Konventionen voraus, keine bestimmte Implementierung.

Die zu lösende Kernspannung: Coding-Agenten erzeugen hochwertigen Code nur unter Bedingungen, die ihrer Natur widersprechen — sie brauchen präzise Absicht (statt vager Prompts), frischen Kontext (statt wachsender Historie), unabhängige Prüfung (statt Selbstbewertung) und harte Grenzen ihrer Entscheidungsmacht (statt impliziter Autonomie). Die Architektur erzeugt diese Bedingungen strukturell, nicht durch Appell.

### 1.2 Qualitätsziele

| Priorität | Qualitätsziel | Szenario (Messlatte) |
|---|---|---|
| 1 | **Korrektheit gegenüber Absicht** | Gelieferter Code erfüllt die freigegebene Spec; jede Anforderung ist durch mindestens einen automatisierten Test belegt (SM-26); Konvergenz-Check vor Merge meldet „Converged“. |
| 2 | **Nachvollziehbarkeit (Auditierbarkeit)** | Jede Verhaltensänderung ist von Spec über Change, Commits und PR bis zur Living Spec lückenlos rückverfolgbar; ein Außenstehender rekonstruiert den Stand allein aus dem Repository, ohne Chat-Historie (I1, I2). |
| 3 | **Menschliche Kontrolle an teuren Punkten** | Zielbild, Architektur, Schnittstellen, Merge und Regelwerk werden ausschließlich von Menschen entschieden (Gates G0–G3, G5); Agenten handeln autonom nur im billig umkehrbaren Raum. |
| 4 | **Drift-Freiheit von Spec und Code** | Living Specs beschreiben jederzeit das Ist-Verhalten; Drift wird spätestens am Merge-Gate (G5, SM-22) bzw. durch periodische Audits (SM-25) erkannt und per Realign-Change behoben (SM-24). |
| 5 | **Effizienz / Proportionalität** | Prozessaufwand skaliert mit der Aufgabenklasse (Spike → Architectural, §8.2); triviale Änderungen durchlaufen keinen Framework-Overhead, aber niemals umgehen sie die Freigabe (I6). |
| 6 | **Kontexteffizienz** | Die Durchsetzungsschicht kostet den Agenten kaum Fenster: Fixkosten-Belegung ≤ 15 % vor Arbeitsbeginn, volle Durchsetzung ≤ 20 % (Q8); Evidenz zirkuliert als Verdict, nicht als Rohdaten (KB-1/KB-2). |

### 1.3 Stakeholder

| Rolle | Erwartung an die Architektur |
|---|---|
| **Product Owner** | Zielbild und Prioritäten bleiben menschliche Hoheit (G0, G1); Specs sind für Nicht-Entwickler lesbar; Negativraum ist explizit. |
| **Engineering Lead / Architekt** | Architekturentscheidungen fallen vor der Task-Zerlegung (G2) mit dokumentierten Alternativen (ADRs); Constitution wird technisch durchgesetzt, nicht nur deklariert. |
| **Entwickler:in (Gate-Bediener)** | Gates sind leicht bedienbar: genau ein Artefakt pro Gate, kurze Artefakte, klare Eingangskriterien; kein Review-Marathon (G4 automatisiert mit Eskalation). |
| **Coding-Agent (als Systemnutzer)** | Jederzeit eindeutige, vollständige Arbeitsanweisungen aus Dateien; kein implizites Kontextwissen nötig; klare Eskalationspfade statt Raten. |
| **Reviewer / QA** | Unabhängige Prüfung ist institutionalisiert (I4); Befundklassifikation (Critical/Important/Minor) mit blockierender Wirkung. |
| **Security / Compliance** | Vollständiger Audit-Trail (datiertes Archiv, Checkpoint-Commits); Stop-Bedingungen bei unbeaufsichtigten Läufen; keine Agenten-Merges ohne PR. |
| **Plattform-/Partner-Teams** | Geteilte Requirements als read-only Referenzen; gepinnte Spec-Versionen an Integrationsgrenzen (SM-15). |

---

## 2. Randbedingungen (Constraints)

### 2.1 Technische Randbedingungen

| # | Randbedingung | Begründung / Konsequenz |
|---|---|---|
| C1 | **Datei- und Git-Basierung**: Alle Steuerungsartefakte sind Klartext-Dateien (Markdown) im selben Repository wie der Code. Ausnahme: der Arbeitsgraph (Beads, §8.11) speichert in einer Git-synchronisierten Dolt-Datenbank unter `.beads/`; der JSONL-Export dient als diffbare Klartext- und Audit-Sicht. | Macht Zustand agentenlesbar, diffbar und versionierbar (I1, I2); keine externe Planungsplattform als Pflichtkomponente. Die `.beads/`-Ausnahme ist analog zu `.git/` selbst begründet: strukturierter Zustand mit Git-Versionierung und Klartext-Export. |
| C2 | **Harness-Neutralität**: Konventionen dürfen nur Fähigkeiten voraussetzen, die alle gängigen Harnesses bieten (Dateizugriff, Shell, Subagenten oder äquivalente Kontexttrennung). | Instanziierbar mit Spec Kit, OpenSpec, Superpowers, BMAD oder Eigenbau; verhindert Vendor-Lock-in. |
| C3 | **LLM-Kontextfenster als knappe Ressource**: Modellqualität degradiert mit Kontextfüllung („Context Rot“). | Erzwingt I3 (frischer Kontext pro Phase/Task), Delegation von Exploration an Subagenten, destillierte statt roher Übergaben. |
| C4 | **Agenten sind nicht-deterministisch**: Gleiche Eingabe kann zu unterschiedlichen Ergebnissen führen. | Erzwingt I4 (keine Selbstgenehmigung), automatisierte Verifikation, reproduzierbare Gates statt Vertrauen in Einzelantworten. |
| C5 | **Kein Agenten-Merge in Hauptzweig**: Agents haben technisch keine Merge-Berechtigung auf den Hauptzweig. | Durchsetzung von G5 über Branch-Protection-Regeln der Plattform, nicht über Prompt-Anweisungen. |
| C6 | **Protokollkonformität**: Werkzeuganbindung über MCP, Client-Anbindung über ACP, Projektkontext über AGENTS.md. | Interoperabilität und Austauschbarkeit der Komponenten (siehe §3.2). |
| C10 | **Kontextbudget der Durchsetzungsschicht**: Die Durchsetzungsschicht darf den nutzbaren Kontext des Agenten nicht nennenswert reduzieren; Fixkosten (Regeln, Spec-Kontext, Evidenz-Transport) bleiben ≤ 15 % des Fensters, Evidenz wird nur als Verdict transportiert, nie als Rohdaten. | Erzwingt Auslagerung aller Prüfungen in CI/Server/Middleware (KB-1/KB-2); verhindert, dass Guardrails durch Kontextfülle unsichtbar werden (Context Rot, Lost-in-the-Middle). Details: §8.9. |
| C11 | **Omnigent als Ziel-Laufzeitschicht**: Die Referenz-Instanziierung der Laufzeit- und Governance-Ebene (Session-Substrat, Action-Policies, Sandboxing, Gate-Kanal) ist Omnigent (Databricks, Apache 2.0). Die *Konventionen* der Architektur bleiben harness-neutral (C2 gilt unverändert); C11 betrifft nur die Ziel-Deployment-Topologie. | ADR-17: Omnigent liefert als einziges System mehrere Bausteine des Modells produktfertig (tmux-basierte Terminals mit OS-Sandboxing, dreistufiges Policy-System, Multi-Device-Sessions, Cross-Vendor-Review). Konsequenzen: Versions-Pinning (Alpha-Reife), Telemetrie-Opt-out-Pflicht, eine zusätzliche Server-Komponente in §7, serverseitige CI-Gates bleiben trotzdem die Sicherheitsgrenze (Lücke-4-Logik). |

### 2.2 Organisatorische Randbedingungen

| # | Randbedingung | Konsequenz |
|---|---|---|
| C7 | **Menschliche Gate-Kapazität ist begrenzt** (Minuten pro Tag, nicht Stunden). | Artefakte sind kurz (Spec 1–3 Seiten); G4 ist automatisiert mit Eskalationsschwelle; Gates bündeln Entscheidungen statt sie zu zerstreuen. |
| C8 | **Rollen müssen besetzbar sein**: Product Owner und Engineering Lead als benannte Personen pro Projekt. | Entscheidungsrechte-Matrix (§9) verlangt benannte Entscheider für G0–G3, G5. |
| C9 | **Bestehende CI/CD- und Git-Plattform wird wiederverwendet** (GitHub/GitLab/Azure DevOps o. ä.). | Quality Gates, Branch Protection und PR-Workflow sind Plattformfunktionen; die Architektur definiert nur ihre Nutzung. |

### 2.3 Konventionen

- **Dokumentationskonvention**: Specs folgen den Template-Strukturen (User Stories mit Priorität und Independent Test, nummerierte FRs, Akzeptanzszenarien in Given/When/Then oder EARS); ADRs im MADR-Format; Delta-Specs mit ADDED/MODIFIED/REMOVED/RENAMED-Sektionen.
- **Namenskonventionen**: kebab-case Change-Namen, Domänen-Slugs für Living Specs, FR-IDs in Testnamen, Change-Referenzen in Commit-Messages (Conventional Commits).
- **Verzeichniskonvention**: `CONSTITUTION.md`, `AGENTS.md`, `docs/vision.md`, `docs/decisions/`, `openspec/` bzw. `specs/` mit `specs/` (Living) und `changes/` (aktiv + `archive/`).

---

## 3. Kontextabgrenzung

### 3.1 Fachlicher Kontext

Das System erhält als fachliche Eingaben Produktideen, Change Requests und Fehlermeldungen und liefert als fachliche Ausgaben überprüfte, in den Hauptzweig integrierte Softwareänderungen samt aktualisierter Living Documentation. Drei Einstiegspunkte sind vorgesehen (nach Spec Kit): **Neuentwicklung** (voller Pfad P0–P6), **Bugfixing** (abgespeckter Pfad: Diagnose → Fix → Verifikation, ohne vollständige SDD-Zeremonie) und **Ideenbewertung** (endet am G0 mit Go/Clarify/Stop, ohne Code). Fachlich ausgegrenzt sind: Produktstrategie oberhalb des Zielbilds, Betrieb/Monitoring der produzierten Software, und alles, was nach dem Merge beginnt (Release-Management kann anschließen, ist aber nicht Teil dieses Systems).

### 3.2 Technischer Kontext

| Externe Schnittstelle | Richtung | Protokoll/Konvention | Zweck |
|---|---|---|---|
| **LLM-Provider** (Anthropic, OpenAI, Google, lokale Server via Ollama/vLLM) | ausgehend | Provider-APIs, modellagnostisch abstrahiert (z. B. LiteLLM) | Modellleistung für alle Agentenrollen; austauschbar, da Harness-Effekte > Modellwahl für Prozessqualität |
| **Git-Plattform** (GitHub/GitLab/…) | bidirektional | Git, PR-APIs, Branch Protection | Versionierung (Specs + Code), G5-Durchsetzung, Audit-Trail |
| **CI/CD-Pipeline** | bidirektional | Plattform-Runner, Log-Export | Automatisierte Verifikation; Fehlerlogs fließen als Feedback an den Agenten zurück |
| **MCP-Server** (Werkzeuge, Datenquellen) | eingehend (in den Agenten) | Model Context Protocol | Standardisierte Werkzeuganbindung; einmal gebaute Server laufen in jedem Harness |
| **Editor/IDE-Clients** (Zed, VS Code, Neovim, JetBrains) | ausgehend/eingehend | Agent Client Protocol (ACP) | Mensch-Agent-Interaktion und Einbettung fremder Agenten |
| **Issue-Tracker** (optional) | eingehend | REST/CLI | Change Requests als Eingabe für G0/P1 |
| **Omnigent-Server** (Ziel-Laufzeitschicht, C11) | bidirektional | Omnigent-API/Socket, Web-UI, Mobile-Follow | Meta-Harness: verwaltet Sessions/Terminals, wertet Action-Policies aus (allow/block/approve), provisioniert Sandboxes, stellt Gate- und Beobachtungskanal über Geräte hinweg |
| **Cloud-Sandbox-Provider** (optional: Modal, E2B, Daytona, Kubernetes u. a.) | ausgehend | Omnigent-Sandbox-Adapter | Disposable Remote-Ausführung von Agenten-Sessions außerhalb der Entwickler-Maschine (§7) |

![Bausteinsicht Ebene 1: Systemkontext und Hauptbausteine](assets/arc42_bausteinsicht.png)

---

## 4. Lösungsstrategie

Die Architektur beruht auf fünf strategischen Grundentscheidungen, aus denen alle Detailentscheidungen (§9) ableitbar sind.

| # | Strategie | Kernidee | Erreichte Qualitätsziele |
|---|---|---|---|
| S1 | **Artefakt-zentrierte Steuerung statt Dialog-Steuerung** | Jede Phase erzeugt ein versioniertes Klartext-Artefakt (Spec, Design, Plan, Tasks, Review-Log); der nächste Schritt liest nur Artefakte, nie Gesprächshistorie. Agenten werden zu „Arbeitskräften über Akten“. | Nachvollziehbarkeit (2), Korrektheit (1) |
| S2 | **Gate-Architektur mit asymmetrischer Entscheidungsverteilung** | Menschen entscheiden an genau sechs definierten Punkten (G0–G5) über das, was teuer umzukehren ist; Agenten entscheiden alles Billige autonom. Ein Gate (G4) ist bewusst automatisiert, um menschliche Kapazität (C7) zu schonen. | Kontrolle (3), Effizienz (5) |
| S3 | **Kontext-Hygiene als Systemeigenschaft** | Frischer Kontext pro Phase und Task (I3); Exploration wird an Subagenten delegiert, die Destillate zurückgeben; Reviewer erben niemals Session-Historie. | Korrektheit (1) |
| S4 | **Unabhängige Verifikation als Invariante** | Wer erstellt, genehmigt nicht (I4): Test-First (ausführbare Spec vor Code), Validator-Gates vor Commits, Reviewer-Subagenten mit kuratiertem Input, CI als finale Hürde. | Korrektheit (1), Drift-Freiheit (4) |
| S5 | **Zwei-Ebenen-Spec-Modell mit Git als Versionierungsschicht** | Living Specs (domänen-organisierter Ist-Zustand) + Change-Deltas (ADDED/MODIFIED/REMOVED) + datiertes Archiv; keine parallelen Versionsnummern; Spec-Merge läuft im selben PR wie Code. | Drift-Freiheit (4), Nachvollziehbarkeit (2) |

**Verworfene Alternativen:** (a) *Vollautomatik ohne menschliche Gates* — verworfen wegen Qualitätsziel 3 und dokumentierter Fehlmodi (stille Fehlinterpretationen, Scope Creep); (b) *Feature-Snapshot-Specs ohne Living Spec* (Spec-Kit-Grundmodell) — verworfen für Brownfield, weil „wie verhält sich das System heute?“ unbeantwortet bleibt und Drift strukturell entsteht; (c) *Multi-Agent-Orchestrierung als Default* — verworfen, weil kontrollierte Experimente und Anthropic-Praxis zeigen, dass gekoppelte Coding-Arbeit unter Orchestrierung leidet (Kosten ×2–15, Identity Drift); Orchestrierung bleibt eine situative Option in P4 bei echter Parallelisierbarkeit; (d) *Externes Planungs-/ALM-Tool als Source of Truth* — verworfen wegen C1/C2 und weil eine Spec, die der Agent nicht im Repository lesen kann, für ihn nicht existiert (SM-11).

---

## 5. Bausteinsicht

### 5.1 Ebene 1: Whitebox Gesamtsystem

Das Gesamtsystem besteht aus vier Hauptbausteinen (blau im Diagramm §3.2), zwei Infrastrukturbausteinen (mittelblau) und den externen Partnern Mensch und LLM-Provider.

| Baustein | Verantwortung | Zentrale Regeln |
|---|---|---|
| **Coding-Agent (Harness)** | Orchestriert den Workflow: erkundet, erstellt alle Artefakte, dispatcht Ausführung, stellt Gate-Anfragen. Enthält die Prozesslogik (Skills/Prompts). | Darf keine Gates selbst passieren (I4); read-only in Explorationsphasen; Ratsche I5. |
| **Spezifikationskern** | Verwaltet das Zwei-Ebenen-Modell: Living Specs, Change-Ordner, Delta-Semantik, Sync/Archiv-Mechanik, Index/Register. | SM-1 bis SM-6 (Modell), SM-12 bis SM-16 (Versionierung), SM-29/30 (Sync). |
| **Gate-Engine** | Erzwingt Gates: prüft Eingangskriterien, blockiert Phasenübergänge, dispatcht Reviewer-Subagenten (G4), eskaliert an Menschen. | I4, I6; G4 automatisiert mit Eskalationsschwelle. |
| **Ausführungsebene** | Führt Tasks aus: frische Subagenten, TDD-Zyklen, Worktree-Isolation, atomare Commits. | P4-1 bis P4-6; „iron law“ Test-First. |
| **Laufzeit- und Governance-Schicht (Omnigent)** | Ziel-Instanziierung der Laufzeitebene (C11, ADR-17): Meta-Harness oberhalb der Coding-Harnesses — verwaltet Sessions/Terminals (tmux-basiert) mit OS-Sandboxing (`bwrap`/`seatbelt`), wertet dreistufige Action-Policies aus (Server/Agent/Session → allow/block/approve), Spend-Caps, synchronisiert Sessions über Terminal/Browser/Mobile, dispatcht optional Sub-Agenten verschiedener Harnesses mit Cross-Vendor-Review (Polly). | IS-1 bis IS-6 (§8.10); Policy-Instanziierung der Approval Boundaries (§8.4); ersetzt keine Bausteinlogik des Modells — Spezifikationskern, Arbeitsgraph und serverseitige Gates bleiben eigenständig. |
| **Session-Substrat (tmux/Herdr — Fallback)** | Harness-neutrale Minimal-Instanziierung der Prozess- und Session-Isolation, falls Omnigent nicht verfügbar (Air-Gapped ohne Server, Migration, POC): persistente, einzeln adressierbare Sessions/Panes pro Subagent, Zustandsbeobachtung, Detach/Reattach. | IS-1 bis IS-5 (§8.10); Substrat ≠ Orchestrierer, Substrat ≠ Sicherheits-Sandbox. |
| **Arbeitsgraph (Beads)** | Operative Task-Registry der Ausführung: abhängigkeitsbewusster, abfragbarer Arbeitsgraph (Ready-Erkennung, Claim/Release, discovered-from-Kanten), Git-synchronisiert unter `.beads/`. | AG-1 bis AG-7 (§8.11); leitet sich aus dem G3-freigegebenen Plan ab, ersetzt ihn nicht. Omnigent hat keinen Abhängigkeitsgraphen — Beads bleibt auch in der Omnigent-Topologie die Task-Wahrheit. |
| **Git-Repository** | Alleinige persistente Zustands- und Versionierungsschicht für Code, Specs, Archiv und Regelwerk. | C1, SM-12 bis SM-14; Branch Protection für C5. |
| **CI/CD-Pipeline** | Führt die vollständige Verifikation aus und liefert Fehlerlogs als strukturiertes Feedback zurück. | P5-4; Quality Gates mit Coverage-Schwellen. |

### 5.2 Ebene 2: Spezifikationskern (Whitebox)

Der Spezifikationskern ist der Baustein mit der größten eigenen Logik und wird daher verfeinert.

| Unterbaustein | Verantwortung | Artefakte |
|---|---|---|
| **Living-Spec-Register** | Domänen-organisierte Ist-Spezifikationen; generiert `INDEX.md` (Domäne, Owner, letzter Change, offene Changes). | `specs/<domäne>/spec.md`, `INDEX.md` |
| **Change-Manager** | Führt aktive Changes als Ordner mit dem vollständigen Artefakt-Bundle; erzwingt Artefakt-Reihenfolge (proposal → specs → design → tasks) und Kohärenz bei Updates (SM-21). | `changes/<name>/{proposal.md, specs/, design.md, tasks.md, review-log.md}` |
| **Delta-Engine** | Interpretiert ADDED/MODIFIED/REMOVED/RENAMED; garantiert, dass MODIFIED-Blöcke vollständige Fassungen enthalten (SM-3); validiert Delta-Dateien. | Delta-`spec.md` je Domäne im Change |
| **Sync- & Archiv-Dienst** | Merged verifizierte Deltas semantisch und idempotent in Living Specs (SM-29); archiviert datiert und unveränderlich (SM-13); fragt bei ausstehendem Sync aktiv nach. | `changes/archive/YYYY-MM-DD-<name>/` |
| **Drift-Monitor** | Erkennt Rückwärts-Drift: Verifikation vor Archiv (SM-23), PR-Change-Bezug (SM-22), periodische Audits inkl. Traceability-Lücken (SM-25, SM-28). | Befundlisten, Realign-Changes |

### 5.3 Ebene 2: Gate-Engine (Whitebox)

| Unterbaustein | Verantwortung |
|---|---|
| **Eingangskriterien-Prüfer** | Validiert pro Gate die formalen Bedingungen (z. B. G1: keine `[NEEDS CLARIFICATION]`-Marker mehr; G2: Constitution Check bestanden und re-checked). |
| **Mensch-Gate-Kanal** | Stellt G0–G3 und G5 als gebündelte, kurze Entscheidungsanfragen (Artefakt-Link, Entscheidungsoptionen, Begründungspflicht bei Ablehnung). In der Omnigent-Topologie (C11) läuft der Kanal über die geräteübergreifende Session-Synchronisation: Gate-Anfragen und Action-Approvals sind vom Terminal, Browser und Telefon beantwortbar — wichtig für C7 und den Nachtmodus (§6.4). |
| **Validator (G4)** | Automatisiertes Gate: Test-Suite, Reviewer-Subagent mit SHA-Range-Input, Befundklassifikation; blockiert bei Critical/Important, eskaliert bei Zurückweisung oder Wiederholungs-FAIL. Ziel-Instanziierung unter Omnigent: Reviewer-Dispatch als Cross-Vendor-Review (Implementierer und Reviewer aus unterschiedlichen Harness-/Modellfamilien) — die schärfste bisher verfügbare Umsetzung von I4, weil der Reviewer weder Kontext noch Modell-Blind-Spots mit dem Implementierer teilt. |
| **Eskalations-Router** | Leitet Abweichungen an das richtige Gate zurück: Planlücke → G3, Architekturbruch → G2, Spec-Widerspruch → G1 (siehe §6.3). |

---

## 6. Laufzeitsicht

### 6.1 Szenario 1: Feature-Delivery (Hauptpfad)

1. **Mensch → Agent:** Change Request (Text). Agent klassifiziert laut die Aufgabenklasse (Spike/Bounded/Feature/Architectural) und benennt den Pfad.
2. **P0/P1:** Agent erstellt/aktualisiert Spec-Artefakte (Stories, FRs, Akzeptanzszenarien, Negativraum); Clarify-Schleife mit nummerierten Rückfragen.
3. **G1 (Mensch):** Intent-Gate — Freigabe oder Rückverweis mit Änderungspunkten. *Hartes Gate: keine Implementierungsaktion vorher (I6).*
4. **P2:** Agent führt Constitution Check durch, erstellt Design mit Alternativen (ADRs), Contracts, Datenmodell; Re-Check. Neue Abhängigkeiten entstammen einer dokumentierten **Adopt/Extend/Build-Entscheidung** mit mindestens zwei bewerteten Kandidaten (Search-First-Pflicht: Paket-Registry, Skills/MCP, GitHub/Web; übersprungene Suchkanäle werden deklariert, nicht still weggelassen).
5. **G2 (Mensch, architekturverantwortlich):** Architektur-Gate — Freigabe ggf. mit Auflagen.
6. **P3:** Agent zerlegt in 2–5-Minuten-Tasks mit Dateipfaden, Code-Skizzen, Verifikationsschritten; bei Risiko: frische Gegenlesung durch zweites Modell.
7. **G3 (Mensch):** Go-Signal. *Danach* wird der freigegebene Plan in den Arbeitsgraph transkribiert (Beads-Epic mit Task-Beads und Abhängigkeiten, AG-2) — nie vorher: Das Gate genehmigt das Artefakt, der Graph operationalisiert es.
8. **P4 (Schleife pro Task):** Frischer Subagent in eigener Session/Pane (IS-1) claimt den nächsten claimbaren Task aus dem Arbeitsgraph (`bd ready` → `bd update --claim`) → failing Test → Minimalimplementierung → grün → atomarer Commit (mit Change-/Task-/Bead-Referenz, AG-7) → Bead erst nach G4-Verdict schließen (AG-4).
9. **G4 (automatisiert):** Reviewer-Subagent prüft Diff per SHA-Range gegen Spec-Ausschnitt; PASS → Bead `close`, nächster Task wird automatisch claimbar; FAIL → Befunde zurück an P4; Eskalation bei Critical/wiederholtem FAIL.
10. **P5:** Konvergenz-Check gegen Gesamt-Spec; Verifikation der Artefakt-Implementierungs-Kohärenz (SM-23); Abschluss als normierter `verification-report.md` im Change-Ordner (Kategorien Build/Types/Lint/Tests/Security/Diff × PASS/FAIL × Gesamturteil READY/NOT READY — maschinell gatebar statt Prosa).
11. **P6:** Sync der Deltas in Living Specs + Validierung (SM-29); Agent öffnet PR (nie Merge, C5).
12. **G5 (Mensch):** Merge-Gate; danach datierte Archivierung des Changes (SM-13) und Regel-Promotion ins Regelwerk (SM-28/P6-4). Jede Session endet mit **Landing the Plane** (AG-5): Arbeitsgraph synchronisieren, abgeschlossene Beads schließen, offene Beads mit Fortschrittsnotiz versehen, committen/pushen — der nächste Agent (oder die nächste Session) startet aus dem Graph, nicht aus Erinnerung.

### 6.2 Szenario 2: Änderung an implementierter Spec (Fall A, Vorwärtspropagation)

Living Spec sagt X, X soll zu X′ werden. Ablauf: Neuer Change mit MODIFIED-Delta (vollständige neue Fassung, SM-3) → G1 → **Impact-Analyse über Traceability-IDs** (SM-18: `grep FR-xxx` über Tests, Commits, Contracts; Benennung betroffener Module und Konsumenten) → Implementierung inklusive Anpassung aller Tests der alten Fassung (SM-19: kein grüner Test auf Altverhalten) → Verifikation → Sync/Archiv wie 6.1 Schritte 11–12. Bei Contract-Brüchen (SM-15): zusätzlich G2 und Kommunikation an Konsumenten vor Merge.

### 6.3 Szenario 3: Abweichung und Eskalation (Korrekturpfade)

| Auslöser zur Laufzeit | Ablauf |
|---|---|
| **Spec-Lücke in P4 entdeckt** (Fall B) | Agent stoppt Implementierung → aktualisiert Artefakte in Reihenfolge Spec → Design → Tasks (SM-20/21, `/opsx:update`-Muster) → je nach Berührung G3-/G2-/G1-Re-Entry → Fortsetzung. Neu entdeckte, nicht zum Task-Scope gehörende Arbeit wird als Bead mit `discovered-from`-Kante im Arbeitsgraph erfasst (AG-3) — niemals als Scope Creep im laufenden Task abgearbeitet. |
| **Task scheitert wiederholt** (2–3 Versuche) | Fortschritt in Datei sichern → Kontext verwerfen → mit geschärftem Prompt und Befundliste neu starten; bei erneutem FAIL Eskalation an Mensch (G4-Eskalation). Verboten: Korrigieren im gleichen Kontext („im Kreis“). |
| **Verhaltens-PR ohne Change-Bezug** | G5 weist zurück (SM-22); Behebung: Realign-Change (Spec auf Ist ziehen) oder regulärer Fix-Change (Code auf Soll ziehen), je nachdem, welche Seite das Fehlverhalten ist (SM-24). |
| **Drift-Audit findet Lücke** (periodisch, SM-25) | Befundliste (Anforderung ohne Test, Test ohne Anforderung, Szenario ohne Verhaltensnachweis) → Realign-Change durchläuft normalen Pfad. |

### 6.4 Szenario 4: Unbeaufsichtigter Lauf (Nachtmodus)

Zulässig nur mit aktivierten Stop-Bedingungen (P6-5): maximale Iterationszahl, Zeitlimit, Idle-Erkennung (kein neuer Commit in n Iterationen → Abbruch), Checkpoint-Commits als Audit-Trail. G1–G3 werden vorab menschlich passiert (der Lauf arbeitet einen freigegebenen Plan ab); G4 läuft automatisiert; G5 bleibt menschlich und findet morgens statt. Diese Konstellation (Ralph-Philosophie) validiert Ideen über Nacht, shippt aber nichts ohne PR-Review. Der Nachtmodus profitiert doppelt vom Session-Substrat und Arbeitsgraph: Persistente Sessions überstehen Verbindungsabbrüche und Laptop-Sleep, die Zustandsbeobachtung (blocked/done/idle) verwandelt stille Stalls in Benachrichtigungen statt in unbemerkt verstrichene Stunden (IS-3), und der Arbeitsgraph trägt den Fortschritt über Session-Neustarts und Kompaktifizierungen hinweg — die Session ist „Vieh“, die Arbeit liegt im Graph (GUPP-Prinzip: Ist Arbeit auf dem Hook, wird sie ausgeführt, von welcher Session auch immer). In der Omnigent-Zieltopologie (C11) kommen drei Verstärker hinzu: Sessions laufen sandboxed (IS-6) und können vom Telefon aus beobachtet und bei Approval-Anfragen beantwortet werden (Mensch-Gate-Kanal, §5.3); **Spend-Caps** auf Server-Ebene deckeln die Token-/Kosten-Spirale eines entgleisten Nachtlaufs hart; und Cloud-Sandboxes entkoppeln den Lauf vollständig von der Entwickler-Maschine (kein Sleep-Problem, kein lokaler Blast Radius).

---

## 7. Verteilungssicht

Die Architektur ist bewusst verteilungsarm; es existiert genau ein verbindlicher technischer Zustandsort.

| Knoten | Inhalt | Bemerkung |
|---|---|---|
| **Entwickler-Maschine / Agent-Runner** | Harness-Prozess(e), Subagenten, Worktrees, **Beads-CLI** mit `.beads/`-Datenverzeichnis; **Omnigent-Terminals** (tmux-basiert, `bwrap`-/`seatbelt`-sandboxed) bzw. Fallback **Session-Substrat** (tmux ≥ 3.0 oder Herdr) | Stateless im Sinne des Modells: jeder Zustand, der einen Neustart überleben muss, liegt im Repository bzw. im Git-synchronisierten Arbeitsgraph (I2). Skaliert horizontal über parallele Worktrees; sequenzielles Mergen verhindert Integrationskonflikte (P6-2). Beads-Speichermodus: Embedded (Default, Single-Writer per Dateilock) für Einzel-Workflows; Server-Modus (`dolt sql-server`) erst bei parallelen Multi-Writer-Fleets; maschinenübergreifende Synchronisation über Git-Remote-Refs. |
| **Omnigent-Server (Zieltopologie, C11)** | Meta-Harness-Prozess: Session-/Terminal-Verwaltung, Policy-Auswertung (Server/Agent/Session-Stufen), Sandbox-Provisionierung, Web-UI + Mobile-Follow, Aktionslog | Eine bewusst in Kauf genommene Server-Komponente (ADR-17): Sie enthält **keine** Modellwahrheit — Artefakte, Gates und Arbeitsgraph bleiben im Repo; fällt der Server aus, ist die Arbeit aus Repo + Graph fortsetzbar (Q7/Q9). Telemetrie wird per Konfiguration deaktiviert (Opt-out-Pflicht). |
| **Cloud-Sandbox-Provider (optional)** | Disposable Remote-Sessions (Modal, E2B, Daytona, Kubernetes u. a., über Omnigent-Adapter) | Entkoppelt unbeaufsichtigte Läufe von der Entwickler-Maschine; server-provisioniert, ephemer; Alternative zur lokalen `bwrap`-Sandbox für risikoreiche oder parallele Läufe (IS-6). |
| **Git-Plattform** | Repository mit Code, Specs, Archiv, Regelwerk; Branch Protection; PR-Workflow | Einzige Source of Truth (C1); durchsetzungsseitiger Anker von C5 und G5 — auch in der Omnigent-Topologie bleibt dies die Sicherheitsgrenze (IS-5). |
| **CI/CD-Runner** | Test-Suites, Linting, Quality Gates, Validierungsläufe (`openspec validate --specs` o. ä.) | Muss vom Agenten Log-Zugriff ermöglichen (Feedback-Schleife P5-4). |
| **LLM-Endpunkte** | Modellinferenz | Externer Dienst oder self-hosted (Air-Gapped-Variante: lokale Modelle via Ollama/vLLM, Architektur unverändert; Omnigent routet harness-seitig, LiteLLM-kompatibel). |
| **Optional: Spec-Store (Multi-Repo)** | Eigenes Repository für geteilte Requirements | Nur bei Cross-Repo-Features; Konsumenten mounten read-only (SM-6, SM-11). |

**Deployment-Invariante:** Der *Kern* des Referenzmodells (Gate-Engine, Spezifikationskern, Arbeitsgraph) bleibt serverlos — als Konventionen, Templates, CLI-Werkzeuge und Agent-Skills realisiert. Die Zieltopologie fügt mit dem Omnigent-Server genau **eine** Laufzeitkomponente hinzu (C11), die Durchsetzungs- und Beobachtungsfunktionen übernimmt, die serverlos nur als Eigenbau erreichbar wären (Action-Policies, Sandboxing, Multi-Device-Kanal). In der Fallback-Topologie (tmux/Herdr ohne Omnigent) gilt weiterhin: null zusätzliche Infrastruktur, C2 unverändert erfüllt.

---

## 8. Querschnittliche Konzepte

### 8.1 Domänenmodell der Steuerungsartefakte

```
Constitution (1) ──prüft gegen──> Design (P2)
Vision/Zielbild (1) ──rahmt──> Spec (1..n pro Feature)
Spec 1──n Requirement (FR-xxx) 1──n Akzeptanzszenario
Spec 1──1 Design ──n ADR ──n Contract
Design 1──1 Plan ──n Task (2–5 min, eigener Testzyklus)
Task 1──n Commit ──referenziert──> Change
Change 1──n DeltaSpec (ADDED/MODIFIED/REMOVED/RENAMED je Domäne)
Change 1──1 ReviewLog (Befunde: Critical/Important/Minor)
LivingSpec (pro Domäne) <──merged── DeltaSpec (bei Archive)
Traceability: FR-xxx ↔ Test(name) ↔ Modul ↔ Change ↔ PR
```

Lebenszyklus-Regeln: Artefakte werden **nur vorwärts vervollständigt, aber jederzeit kohärent aktualisiert** (SM-21); abgeschlossene Changes sind **unveränderlich** (SM-13); Living Specs haben **keinen Lebenszyklus-Status**, sondern Änderungshistorie über `git log`.

### 8.2 Prozessgewichtung (Skalierungskonzept)

| Klasse | Erkennungsregel | Pfad | Gates |
|---|---|---|---|
| Spike | Machbarkeitsfrage; Output = Empfehlung | Exploration, zeitboxt | G0-light |
| Bounded | Änderung an existierendem, lesbarem Flow | P1-kurz → P4 → P5 → P6 | G1 (kurz, in Chat) + G5 |
| Feature | in sich geschlossenes Deliverable | voll | G1, G2, G3, G4, G5 |
| Architectural | neues Subsystem / Schnittstellenbruch | voll + Sub-Specs + ADRs | alle, G2 verschärft |

Regeln: Klassifikation wird laut ausgesprochen und ist menschlich überstimmbar; **Einbahn-Ratsche** (I5): nur Hochstufung mid-task, bei Stopp und Begründung; **Bounded-Test**: ohne existierenden Bestandsflow ist eine Aufgabe per Definition nicht bounded; das Freigabe-Gate skaliert nie mit der Aufgabe, nur die Artefakt-Tiefe (I6).

### 8.3 Kontext- und Sitzungsmanagement

Phasen und Tasks laufen in getrennten Kontexten/Sessions (I3); Übergaben sind ausschließlich Artefakte plus explizit kuratierte Ausschnitte (bei Reviews: Diff per SHA-Range + Spec-Ausschnitt + Anforderungstext). Exploration wird an Subagenten delegiert, die strukturierte, token-begrenzte Destillate liefern; endlose Exploration wird durch Scope- und Fragebegrenzung verhindert. AGENTS.md/CLAUDE.md werden als knappe, verifizierte Regelwerke gepflegt (P0-4); Aufblähung verwässert wirksame Regeln und ist ein dokumentiertes Anti-Pattern. Die normativen Budget-Regeln für diese Mechanismen (Injektionsbudgets, Delta-Loading, Kompaktifizierungs-Schutzliste, Telemetrie) sind in §8.9 (KB-1 bis KB-10) konsolidiert.

### 8.4 Sicherheits- und Compliance-Konzept

Branch Protection + fehlende Merge-Berechtigung des Agenten (C5); Secrets-Masking in Agenten-Logs; Sandbox-Ausführung für ungeprüften Code (wo der Harness es bietet); vollständiger Audit-Trail durch datiertes Archiv, Checkpoint-Commits und PR-Protokoll; Stop-Bedingungen als Pflicht bei unbeaufsichtigten Läufen; Regelwerk-Änderungen (Constitution, AGENTS.md) nur per menschlich reviewtem PR (§9, Matrix).

**Approval Boundaries (Least Agency):** Das Modell ist niemals finale Autorität für unsandboxed Shell-Ausführung, Netzwerk-Egress, Lesen secret-haltender Pfade, Schreiben außerhalb des Repos und Workflow-Dispatch/Deployment; jede dieser Aktionen MUSS eine Freigabestelle zwischen Modell und Aktion passieren. Für unbeaufsichtigte Läufe gilt zusätzlich das **Heartbeat-Modell**: Ein Supervisor überwacht den Task, der Task schreibt periodisch (z. B. 30 s) ein Lebenszeichen; bei Ausbleiben wird die gesamte **Prozessgruppe** terminiert (nicht nur der Elternprozess) und der Task zur Log-Inspektion quarantäniert. Grundlage aller Detektion ist ein **strukturiertes Aktionslog** (Tool, Input-Zusammenfassung, berührte Dateien, Approval-Entscheidungen, Netzwerkversuche, Session-ID) als Pflichtevidenz — wer nicht sehen kann, was der Agent tat, kann ihn nicht absichern. *(Übernommen aus ECC Security Guide, E-7.)*

**Ziel-Instanziierung unter Omnigent (C11):** Das dreistufige Policy-System (Server/Agent/Session) wertet **jede** Aktion gegen Regeln vom Typ allow/block/approve aus — Durchsetzung auf Meta-Harness-Ebene statt im Prompt, exakt die Forderung aus ADR-11 (Anweisungen sind unwirksam, technische Blockade schließt den Weg). Die obigen Approval Boundaries werden als Server-Policies kodiert (nicht als Agenten-Konvention, damit sie auch bei Fehlverhalten einzelner Sessions greifen); **Spend-Caps** ergänzen die Boundary-Liste um eine Kosten-Dimension (hartes Deckel für Nachtläufe, §6.4); das Omnigent-Aktionslog liefert die strukturierte Pflichtevidenz. Zwei Grenzen bleiben explizit: Erstens sind Omnigent-Policies *harness-seitig* — sie ersetzen nicht die serverseitigen CI-/Branch-Protection-Gates als Sicherheitsgrenze (IS-5, Lücke-4-Logik). Zweitens gilt die Non-Vacuity-Pflicht (§8.7) auch für Policies: Jede Policy MUSS mit einem bekannt-bösen Testfall verifiziert werden (blockt sie wirklich?), und die Policy-Dateien selbst unterliegen dem menschlich reviewten PR-Pfad wie das Regelwerk.

### 8.5 Nachvollziehbarkeitskonzept (Traceability)

Durchgehende ID-Kette `FR-xxx → Szenario → Test(name) → Commit(Change/Task) → PR → Change-Ordner → Archive`. Die Traceability-Matrix ist ein **generiertes** Artefakt (SM-28) und Teil des Drift-Audits; Lücken (Anforderung ohne Test, Test ohne Anforderung) sind blockierende Befunde, keine Hinweise.

### 8.6 Fehlerbehandlungs- und Lernkonzept

Fehler werden dreistufig behandelt: (1) lokal im TDD-Zyklus (red → green), (2) strukturell via Eskalations-Router (§6.3: richtige Gate-Ebene statt Improvisation), (3) organisational via **Regel-Promotion** mit dreistufigem **Confidence-Lifecycle** (ADR-13): Review-Erkenntnisse werden als atomare Regel-Kandidaten (ein Trigger, eine Aktion, Evidenzliste, Confidence-Score) erfasst, zunächst **projektbezogen** aktiviert (keine Cross-Project-Kontamination) und erst nach Beobachtung in mindestens zwei Projekten zur globalen Regel promoviert; die Injektion in Agentenkontexte unterliegt einem **Budget** (wenige, konfidenz- und relevanzgerankte Regeln statt Vollabzug), damit Regelwerke nicht aufblähen (P0-4). Die Promotion passiert ein menschliches Review-Gate, weil Confidence aus Wiederholung — nicht aus Wahrheitsprüfung — entsteht (§11). *(Lifecycle übernommen aus ECC Instincts v2.1, E-6.)*

### 8.7 Durchsetzungsschicht als geschützter Baustein

Die Erzwingungsmechanismen (Hooks, Gates, Prüfskripte) werden selbst als architektonischer Baustein behandelt — mit drei Pflichten. Erstens **Registry**: Alle Hooks/Gates stehen in einer schema-validierten Registry mit stabiler ID, Zweckbeschreibung und Fingerprint; Änderungen an dieser Registry durchlaufen denselben menschlich reviewten PR-Pfad wie Code. Zweitens **Schutz vor dem Agenten**: Änderungen an Prüfkonfigurationen (Linter-/Formatter-/Coverage-/CI-Gate-Configs) und Umgehungsmechanismen (`git --no-verify`, `core.hooksPath`-Überschreibungen, Deaktivierungs-Flags) werden auf Tool-Ebene blockiert — der Agent MUSS den Code an den Check anpassen, nie den Check an den Code (ADR-11). Drittens **Eigenverifikation**: Jeder Durchsetzungsmechanismus MUSS mit einer Test-Suite ausgeliefert werden, die mindestens einen bekannt-schlechten Fall als BLOCK assertiert, und SOLL zur Laufzeit prüfen, dass seine Subjektmenge nicht leer ist — ein Gate über einer leeren Menge ist von einem bestandenen Gate ununterscheidbar (Non-Vacuity-Prinzip). *(Übernommen aus ECC Hook-Registry, Config-Protection, Block-no-verify und Hook-Testpraxis, E-1/E-2/E-3/E-5; Laufzeit-Non-Vacuity aus dem Forschungspapier „Doktrin vs. Durchsetzung".)*

### 8.8 Konsistenz statt Einzelnachweis (pass^k)

Verifikation nicht-deterministischer Prüfobjekte (LLM-generierter Code, flaky Tests) folgt der Unterscheidung **pass@k** (mindestens ein Erfolg aus k Versuchen — ausreichend für Exploration und Vorschläge) vs. **pass^k** (alle k Versuche erfolgreich — gefordert, wenn Konsistenz zählt). Konsequenz: Ein einmalig grüner Gate-Lauf ist bei nicht-deterministischen Prüfobjekten keine ausreichende Evidenz; kritische Verifikationen MÜSSEN bei Flakiness-Verdacht mehrfach konsistent bestehen, und pass@k-Ergebnisse DÜRFEN NICHT als Zuverlässigkeitsnachweis für Gates verwendet werden. Ergänzend gilt **rollenbasiertes Modell-Routing** (ADR-14): Subagent-Rollen erhalten Modellklassen nach Aufgabenart (Exploration/einfache Edits → effiziente Klasse; Standard-Implementierung → Mittelklasse; Architektur, Sicherheitsanalyse, komplexes Debugging → Spitzenklasse), mit Eskalation bei Erstversuch-Fehlschlag, >5-Dateien-Scope oder Sicherheitskritikalität. *(Übernommen aus ECC Longform Guide, E-10.)*

### 8.9 Kontextbudget-Verwaltung

Die Durchsetzungsschicht (Gates, Hooks, Verifikation, Regelwerke, Evidenz) muss selbst kontextsparend gebaut sein, sonst erzeugt sie genau den Zustand, gegen den C3 und I3 die Architektur schützen: Ein voller Kontext degradiert die Modellqualität weit vor dem Fensterlimit (Context Rot), und Regeln in der Fenstermitte verlieren messbar an Wirksamkeit (Lost-in-the-Middle) — eine Guardrail-Regel, die das Modell nicht mehr „sieht", wird nicht durchgesetzt. Das Grundprinzip lautet daher: **Prüfungen laufen außerhalb des Kontexts; ins Fenster gelangen nur Verdicts.** Die schwere Maschinerie (Tests, Mutationsanalyse, Policy-Evaluierung, Drift-Matrix, Attestierungs-Verifikation) gehört in CI, auf den Server oder in eine Governance-Middleware; der Agent erhält Ergebnis plus Verweis (Pfad/Hash), nie Rohdaten. Die Budget-Modellrechnung (siehe „Kontextbudget-Prüfung und -Begrenzung") zeigt: Diszipliniert umgesetzt kostet die gesamte Durchsetzungsschicht ~5–10k Token (~7 % eines 200k-Fensters); die naive Variante (volle Specs, Logs und Attestierungs-JSONs im Prompt) reißt die Kompaktifizierungsschwelle bereits vor Arbeitsbeginn.

![Kontextbudget-Allokation: disziplinierte vs. naive Umsetzung](assets/kontextbudget_allokation.png)

| ID | Anforderung | Stufe |
|---|---|---|
| KB-1 | **Durchsetzung läuft außerhalb des Kontexts.** Jede Prüfung (Tests, Mutation, Policy, Drift-Matrix, Attestierung) MUSS in CI/Server/Middleware ausgeführt werden; der Agent erhält ausschließlich das Verdict plus Verweis auf das Evidenzartefakt. | MUSS |
| KB-2 | **Verdict-not-Log.** Evidenzartefakte (Test-Logs, Attestierungs-JSONs, Mutanten-Reports) leben als Dateien im Repo; ins Fenster gelangt höchstens eine kompakte Zusammenfassung (≤ 1k Token). | MUSS |
| KB-3 | **Injektionsbudget für gelernte Regeln.** Maximal 6 Regeln, Confidence ≥ 0,7, ≤ 250 Token pro Regel inkl. Herkunftszeile (ECC-Standard, ADR-13); Überschuss verdrängt nach Confidence × Recency. | MUSS |
| KB-4 | **Delta-Loading für Specs.** Geladen werden nur die über FR-IDs referenzierten Abschnitte des Change-Deltas plus der betroffene Living-Spec-Slice — niemals vollständige Living Specs oder fremde Changes. | MUSS |
| KB-5 | **Progressive Disclosure für Skills und Prozesswissen.** Ruhezustand: Name + Ein-Zeilen-Beschreibung (~80 Token); Volltext erst bei tatsächlicher Aktivierung; Referenzmaterial erst während der Ausführung. | MUSS |
| KB-6 | **Exploration und Review in Sub-Agenten.** Codebase-Exploration, Log-Analyse und unabhängiger Code-Review laufen in isolierten Kontexten (I3) und geben 1–2k-Destillate zurück; der Hauptkontext wächst proportional zu abgeschlossenen Aufgaben, nicht zu Explorations-Tiefe. | MUSS |
| KB-7 | **Kompaktifizierungs-Disziplin.** Gemischte Strategie (Trimming + Zusammenfassung), Auslösung spätestens bei ~75 % Belegung; der Kompaktifizierungs-Schritt MUSS eine Schutzliste erhalten (Invarianten, aktuelle FR-IDs, Gate-Status werden nie wegkompaktifiziert). | SOLL |
| KB-8 | **Positionsdisziplin.** Invarianten, nicht-verhandelbare Verbote und die aktuelle Aufgaben-ID stehen am Anfang oder Ende des Kontexts, niemals in der Mitte. | SOLL |
| KB-9 | **Retrieval-Hygiene.** Tool-Outputs (Suche, Fetch, Logs) werden vor Aufnahme in den Kontext gefiltert/getrimmt; Extraktion statt Roh-Dumps. | SOLL |
| KB-10 | **Budget-Telemetrie als Gate-Metrik.** Jeder Gate-Report enthält die aktuelle Kontextbelegung; überschreitet der Fixkosten-Anteil (System + Regeln + Spec + Evidenz) 15 % des Fensters, ist das ein Review-Finding — analog zu einem ausufernden Diff. | MUSS |

### 8.10 Session-Substrat und Prozess-Isolation (Ziel: Omnigent, Fallback: tmux/Herdr)

Das Session-Substrat ist die Laufzeitschicht unter den Agenten: Es startet, isoliert und überwacht die Prozesse, in denen Agenten-Sessions laufen. Seine Rolle in dieser Architektur ist präzise begrenzt — es liefert **Prozess-, Session- und Kontext-Isolation sowie Beobachtbarkeit**, nicht mehr und nicht weniger. Die **Ziel-Instanziierung ist Omnigent** (C11, ADR-17): Seine nativen Terminals sind tmux-basiert (erfüllen also die gesamte bewährte Substrat-Semantik: Persistenz, Detach/Reattach, einzelne Adressierbarkeit), ergänzen sie aber um **OS-Level-Sandboxing** — auf Linux `bwrap` (bei Omnigent *mandatorisch*: fehlt das Binary, startet das Terminal nicht), auf macOS `seatbelt`, auf Windows Job Objects — sowie um die geräteübergreifende Session-Synchronisation (Terminal ↔ Browser ↔ Mobile). Als harness-neutrale **Fallback-Instanziierung** bleiben **tmux** (Referenz: 18 Jahre gereift, überall verfügbar, produktiv erprobtes Substrat großer Multi-Agenten-Installationen wie Gas Town) und **Herdr** („tmux für Agenten": Socket-API, eingebaute Zustandserkennung; pre-1.0) definiert. Die Architektur definiert die Anforderungen weiterhin werkzeugneutral — die Wahl der Instanziierung ändert keine davon:

| ID | Anforderung | Stufe |
|---|---|---|
| IS-1 | **Ein Agent = eine Session.** Jeder Subagent/Task läuft in einer eigenen, einzeln adressierbaren Session oder Pane (eigener Prozess, eigenes Terminal, eigener Kontext). Bei paralleler Ausführung gilt das ohne Ausnahme. | MUSS (parallel), SOLL (seriell) |
| IS-2 | **Session-Isolation ergänzt, ersetzt nicht.** Worktree-Isolation (P4) und Kontext-Hygiene (I3, §8.3) bleiben unverändert; das Substrat bietet keinen Ersatz für inhaltliche Isolation. | MUSS |
| IS-3 | **Zustandsbeobachtbarkeit.** Der Supervisor (Mensch oder Heartbeat-Prozess, §8.4) MUSS den Zustand jeder Session sehen können (läuft / blockiert / fertig / idle). Stille Stalls — ein Agent wartet unbemerkt stundenlang auf eine Eingabe — gelten als Prozessbefund. Omnigent liefert Beobachtbarkeit als Produktfunktion (Session-Follow über Geräte, Approval-Wartezustände sichtbar); Herdr liefert State-Sidebar und Blocker-Benachrichtigungen; bei nacktem tmux übernimmt es ein Wächter-Skript (Pane-Scraping, Idle-Erkennung). | MUSS (im unbeaufsichtigten Betrieb), SOLL (interaktiv) |
| IS-4 | **Zwei-Schichten-Trennung: Substrat ≠ Orchestrierer.** Das Substrat stellt Isolation, Persistenz und Signalisierung bereit; die Entscheidung, *welche* Agenten *was* in *welcher Reihenfolge* tun, liegt ausschließlich beim Orchestrierer (Mensch, Lead-Agent oder Workflow-Logik — in der Omnigent-Topologie optional Polly, §4 verwirft Voll-Orchestrierung als Default weiterhin). Die Socket-/API-Orchestrierungsfähigkeit (Agenten spawnen Agenten) darf nur die Orchestrierer-Rolle nutzen. | MUSS |
| IS-5 | **Substrat ist keine Sicherheitsgrenze.** Auch mit OS-Sandboxing gilt: Die Sicherheitsgrenze der Architektur liegt bei den serverseitigen CI-/Branch-Protection-Gates (Lücke-4-Logik). Omnigents `bwrap`/`seatbelt`-Sandbox und das Policy-System reduzieren den lokalen Blast Radius erheblich — sie sind die *stärkste lokale* Schicht, aber lokal bleibt lokal: umgehbar durch den Benutzer, konfigurationsabhängig, plattformasymmetrisch (Windows: Job Objects statt `bwrap`). tmux/Herdr ohne Sandbox bieten nur Prozess-, keine Rechte-Isolation. | MUSS (als Architekturverständnis) |
| IS-6 | **Sandbox-Ausführung für Agenten-Sessions.** In der Omnigent-Topologie laufen Agenten-Sessions grundsätzlich innerhalb der OS-Sandbox (lokal via `bwrap`/`seatbelt` oder remote in einer Cloud-Sandbox, §7); unsandboxed Ausführung ist nur interaktiv und mit expliziter Policy-Ausnahme zulässig — und jede Ausnahme erzeugt einen Approval-Eintrag im Aktionslog (§8.4). | MUSS (Omnigent-Topologie), SOLL (Fallback-Topologie) |

**Empfehlung (Zielbild):** Omnigent-Server als Laufzeit- und Governance-Schicht (C11); lokale Terminals in `bwrap`-Sandbox, unbeaufsichtigte und risikoreiche Läufe zusätzlich oder stattdessen in Cloud-Sandboxes. **Migration/Fallback:** nacktes tmux bleibt die Minimal-Instanziierung (Reife, Verfügbarkeit, SSH-Tauglichkeit), Herdr die KANN-Zwischenstufe. Die Wahl ist reversibel: Das Substrat besitzt keine Artefakte und keinen Zustand des Modells — die Wahrheit liegt in Repo (I1/I2) und Arbeitsgraph (§8.11).

### 8.11 Arbeitsgraph mit Beads

Der Arbeitsgraph ist die **operative Task-Registry** der Ausführungsebene: ein abhängigkeitsbewusster, abfragbarer Graph aus Arbeitseinheiten („Beads"), der im Repository unter `.beads/` liegt und über Git synchronisiert wird (Dolt-Datenbank mit JSONL-Export als Klartext-/Audit-Sicht). Er löst das bekannte Versagen von Markdown-TODO-Listen: kein Abhängigkeitsgraph, keine Claim-Semantik, keine Abfragbarkeit („was ist jetzt dran?"), kein Überleben von Kontext-Resets. Beads (`bd`) ist hierfür der etablierte Standard (bd 1.0, Embedded-Dolt als Default; Steve Yegges Gas Town als großangelegte Referenznutzung desselben Stacks: tmux-Substrat + Beads-Arbeitsgraph). Die Architektur nutzt Beads verbindlich — mit scharfer Abgrenzung gegen die Gate-Artefakte:

| ID | Anforderung | Stufe |
|---|---|---|
| AG-1 | **Beads ist die einzige operative Task-Verfolgung.** Tasks in P4–P6 werden als Beads angelegt, geclaimt, kommentiert und geschlossen; Markdown-TODO-Listen als parallele Aufgabenverfolgung sind verboten (AGENTS.md-Konvention: „Do not use markdown TODO lists for task tracking"). | MUSS |
| AG-2 | **Plan-Artefakt vor Arbeitsgraph.** Das G3-Gate genehmigt ausschließlich das Plan-Artefakt (tasks.md im Change-Ordner); der Arbeitsgraph wird erst nach Freigabe aus dem Plan transkribiert (Epic + Task-Beads + Abhängigkeiten). Kein Gate liest seinen Eingangszustand aus Beads — Gates lesen Artefakte (I1 bleibt unangetastet); Beads ist Ausführungszustand, nicht Genehmigungsgrundlage. | MUSS |
| AG-3 | **Discovered-Work-Kanten.** Während der Ausführung entdeckte Arbeit außerhalb des Task-Scopes wird als neuer Bead mit `discovered-from`-Kante erfasst statt im laufenden Task mitbearbeitet zu werden; die Eskalationslogik von §6.3 entscheidet über deren Priorisierung. | MUSS |
| AG-4 | **Evidenzgebundenes Schließen.** Ein Bead wird erst geschlossen, nachdem das zugehörige Verifikations-Verdict (G4/G5) vorliegt; der Bead-Status ist Arbeitsbehauptung, das Gate-Verdict ist Wahrheit. Statusübergänge ohne Verdict sind ungültig (Anschluss an das Konzept evidenzgebundener Status). | MUSS |
| AG-5 | **Landing the Plane.** Jede Session endet mit einer Hygiene-Sequenz: Graph synchronisieren, fertige Arbeit schließen, offene Beads mit Fortschrittsnotiz versehen, Änderungen committen/pushen. Bei unbeaufsichtigten Läufen gehört diese Sequenz in den Abschluss-Workflow des Laufs selbst. | MUSS |
| AG-6 | **Speichermodus nach Topologie.** Embedded-Modus (Single-Writer per Dateilock) als Default; Server-Modus nur bei parallelen Multi-Writer-Fleets; der JSONL-Export wird mitversioniert und dient als diffbare Audit-Sicht (C1-Ausnahme, §2.1). Versions-Pinning von `bd`; AGENTS.md-Instruktionen werden bei Tool-Upgrades mitgepflegt (veraltete Kommandos in persistenten Agenten-Gedächtnissen sind ein dokumentierter Realfall). | MUSS |
| AG-7 | **Traceability-Anbindung.** Commits referenzieren neben Change und FR-ID die Bead-ID; die Traceability-Kette wird damit zu `FR → Szenario → Test → Bead → Commit → PR → Change → Archiv`. | MUSS |

**Abgrenzung:** Die Architektur übernimmt bewusst **Substrat + Arbeitsgraph**, aber keinen Voll-Orchestrierer im Sinne von Gas Town (Rollen-Zoo, Mail-Systeme, Merge-Queues, Formulas/Molecules): Der Orchestrierungs-Mehrwert ist für Einzel- und Kleinst-Team-Workflows gering gegenüber Kosten (Token-Verbrauch, Betriebskomplexität, pre-1.0-Reife), und §4 hat Multi-Agent-Orchestrierung als Default bereits verworfen. Die Molecule-/Formula-Idee (Workflow als instanziierbarer Bead-Graph, der Abstürze und Kompaktifizierungen überlebt) ist dagegen als KANN-Option für wiederkehrende Standard-Workflows (Releases, Realign-Changes, Drift-Audits) vorgemerkt.

---

## 9. Architekturentscheidungen

| ID | Entscheidung | Begründung | Alternativen (verworfen) | Betroffene Q-Ziele |
|---|---|---|---|---|
| ADR-01 | **Zwei-Ebenen-Spec-Modell** (Living Specs + Change-Deltas) statt Feature-Snapshots | Beantwortet „Ist-Zustand heute?“ und „Historie?“ gleichermaßen; Merge-Semantik (ADDED/MODIFIED/REMOVED) macht Propagation mechanisch | Feature-Snapshots à la Spec Kit (Drift), einzelne Monolithen-Spec (keine Änderungsverfolgung) | 2, 4 |
| ADR-02 | **Git als einzige Versionierungsschicht**, keine Versionsnummern auf Specs | Duplikate driften garantiert; Commit-Kopplung von Spec-Merge und Code erzeugt konsistente Stände | SemVer pro Spec-Datei; externes ALM-Tool | 2, 4 |
| ADR-03 | **Sechs-Gates-Modell mit G4-Automatisierung** | Menschliche Kapazität (C7) auf teure Entscheidungen konzentrieren; Qualität ohne Daueraufsicht | Alle Gates manuell (Skalierung), nur End-Gate (Kontrollverlust) | 3, 5 |
| ADR-04 | **Keine Selbstgenehmigung (I4) als Invariante** | Selbstprüfung prüft gegen Erinnerung statt Grundwahrheit („game of telephone“) | Implementierer reviewed selbst; rein statische Analyse | 1 |
| ADR-05 | **Test-First als „iron law“** | Failing Test = ausführbare Spec; verhindert Tests, die nur Code bestätigen | Test-After; Coverage-Mindestwerte allein | 1 |
| ADR-06 | **Einbahn-Ratsche + Bounded-Test** | Verhindert Prozess-Umgehung durch Fehlklassifikation („too simple to need approval“) | Freie Pfadwahl je Task; immer voller Prozess | 3, 5 |
| ADR-07 | **Harness-Neutralität über MCP/ACP/AGENTS.md** | Austauschbarkeit von Agenten und Clients; Investitionsschutz | Festlegung auf einen Harness | 5 (Kosten), C2 |
| ADR-08 | **Subagent-Delegation mit Destillat-Übergabe** | Kontextfenster ist Engpass (C3); rohe Explorationsergebnisse vergiften Hauptkontext | Monolithische Einzel-Session; Volltext-Übergaben | 1 |
| ADR-09 | **PR als zwingendes letztes Gate (kein Agenten-Merge)** | Fängt „Buchstabe erfüllt, Geist verfehlt“; technisch via Branch Protection durchgesetzt | Auto-Merge bei grüner CI; Review nach Merge | 1, 3 |
| ADR-10 | **Regel-Promotion (Closed Loop) statt wiederholter Reviews** | Wiederholungsfehler werden organisatorisch unmöglich; Review-Aufwand sinkt strukturell | Review-Kommentare ohne Kodifizierung | 1, 5 |
| ADR-11 | **Schutz der Durchsetzungsschicht vor dem Agenten** (Hook-Registry, Config-Protection, Bypass-Blockade) | Agenten schwächen erfahrungsgemäß Checks, statt Code zu reparieren; nur technische Blockade schließt den Umgehungsweg, Anweisungen nicht (Compliance-Gap-Evidenz) | Prompt-Verbote (unwirksam); nachträgliches Review (zu spät) | 1, 3 |
| ADR-12 | **Fact-Forcing vor Erstberührung und destruktiven Kommandos** | Untersuchung als Eintrittskarte erzeugt Bewusstsein, das Selbstbestätigung („sind Sie sicher?") nie erzeugt; verhindert blindes Editieren fremder Dateien | Ja/Nein-Bestätigungen (immer „ja"); Freigabe-Dialogs ohne Inhalt | 1 |
| ADR-13 | **Confidence-Lifecycle für gelernte Regeln** (atomar, projekt-scoped, Promotion nach 2+ Projekten, Injection-Budget) | Verhindert Cross-Project-Kontamination und Regelwerk-Aufblähung; trennt beobachtete Häufigkeit von bewiesener Richtigkeit (Promotion nur per menschlichem Gate) | Binäre Übernahme in AGENTS.md; sofort globaler Scope | 1, 5 |
| ADR-14 | **Rollenbasiertes Modell-Routing** (Modellklasse nach Subagent-Rolle, Eskalationsregeln) | Token-Ökonomie: Exploration braucht keine Spitzenmodelle; Sicherheitsanalyse darf nicht am billigsten Modell hängen | Einheitliches Modell für alle Rollen; manuelle Auswahl pro Session | 5 (Kosten), 1 |
| ADR-15 | **Session-Substrat für Prozess-Isolation** (Ziel: Omnigent-Terminals, Fallback: tmux, KANN: Herdr; IS-1 bis IS-6) | Persistente, einzeln adressierbare Sessions isolieren Agenten-Prozesse und -Kontexte, überstehen Disconnects und machen Zustände (blocked/done) beobachtbar — stille Stalls werden sichtbar; bewährtes Muster (Gas Town läuft produktiv auf tmux); Omnigent nutzt dasselbe tmux-Fundament und ergänzt OS-Sandboxing + Multi-Device-Follow | GUI-Wrapper (plattformgebunden, keine SSH-Tauglichkeit); IDE-Sessions (kein Detach); Substrat als Sicherheitsgrenze missverstehen (IS-5) | 1, 3, 5 |
| ADR-16 | **Beads als Arbeitsgraph der Ausführung** (AG-1 bis AG-7; Plan-Artefakt bleibt Gate-Grundlage) | Abhängigkeitsbewusster, abfragbarer, Git-synchronisierter Arbeitszustand: `bd ready` beantwortet „was ist dran?" nach jedem Kontext-Reset; Claim/Release-Semantik für parallele Agenten; discovered-from-Kanten strukturieren Work-Discovery; überlebt Sessions, Kompaktifizierung und Abstürze (I2/I3-Verstärker) | Markdown-TODO-Listen (kein Graph, keine Claims); GitHub Issues o. ä. (nicht repo-lokal, nicht agenten-nah); Voll-Orchestrator Gas Town (Kosten, Komplexität, pre-1.0-Reife — Substrat und Arbeitsgraph werden übernommen, der Rollen-Orchestrator nicht) | 1, 2, 5 |
| ADR-17 | **Omnigent als Ziel-Laufzeit- und Governance-Schicht** (C11; Policy-System, Sandboxing, Multi-Device-Sessions, optionales Cross-Vendor-Review via Polly) | Einzige verfügbare Instanz, die mehrere Bausteine des Modells produktfertig liefert statt als Eigenbau: Action-Policies auf Meta-Harness-Ebene (ADR-11-Forderung „Durchsetzung außerhalb des Prompts"), mandatorisches OS-Sandboxing (schließt die bei tmux/Herdr offene IS-5-Lücke lokal so weit wie möglich), geräteübergreifender Gate-Kanal (C7, Nachtmodus), Cross-Vendor-Review als schärfste I4-Umsetzung; Apache 2.0, Databricks-Herkunft | Reiner tmux/Beads/Aider-Eigenbau-Stack (mehr Kontrolle, aber Policy-/Sandbox-/Mobile-Ebene komplett selbst zu bauen und zu warten); Gas Town als Voll-Orchestrator (zu schwer, pre-1.0, anderer Scope); ausschließliche Harness-Neutralität ohne Ziel-Instanziierung (verliert die produktfertigen Durchsetzungsfunktionen) | 1, 3, 5 |

**Entscheidungsrechte-Matrix (verbindlich):**

| Entscheidungstyp | Entscheider | Agent darf |
|---|---|---|
| Zielbild, Prioritäten, Negativraum | Mensch (G0/G1) | vorschlagen, klären |
| Architektur, Schnittstellen, neue Abhängigkeiten | Mensch (G2) | Alternativenpapier erstellen |
| Task-Zerlegung, Dateistruktur, Reihenfolge | Agent erstellt, Mensch genehmigt (G3) | vollständig ausarbeiten |
| Implementierungsdetails im Task-Scope | Agent autonom | entscheiden (unter G4-Kontrolle) |
| Qualitätsurteil pro Task | unabhängige Instanz (G4) | nie selbst beurteilen (I4) |
| Merge, Release, Regelwerk | Mensch (G5 / Regel-PR) | PR vorbereiten, Regeln vorschlagen |

---

## 10. Qualitätsanforderungen

### 10.1 Qualitätsbaum

```
Qualität
├── 1 Korrektheit gegenüber Absicht
│    ├── 1.1 Jede FR durch ≥1 automatisierten Test belegt
│    ├── 1.2 Akzeptanzszenarien ausführbar verifiziert
│    └── 1.3 Konvergenz-Check „Converged“ vor Merge
├── 2 Nachvollziehbarkeit
│    ├── 2.1 Vollständige Kette FR→Test→Commit→PR→Change→Archiv
│    ├── 2.2 Rekonstruierbarkeit ohne Chat-Historie
│    └── 2.3 Unveränderliches, datiertes Archiv
├── 3 Kontrolle
│    ├── 3.1 Gates G0–G3, G5 ausschließlich menschlich passierbar
│    ├── 3.2 Kein Agenten-Merge (technisch erzwungen)
│    └── 3.3 Kein Prozesspfad ohne Freigabe (I6)
├── 4 Drift-Freiheit
│    ├── 4.1 Living Spec = Ist-Verhalten (Audit-verifiziert)
│    ├── 4.2 Kein Verhaltens-PR ohne Change-Bezug
│    └── 4.3 Sync vor Archiv, validiert und idempotent
├── 5 Effizienz
│    ├── 5.1 Prozessaufwand proportional zur Aufgabenklasse
│    ├── 5.2 Gate-Interaktion ≤ Minuten pro Entscheidung
│    └── 5.3 Kein Orchestrierungs-Overhead ohne Parallelisierungsnutzen
└── 6 Kontexteffizienz
     ├── 6.1 Fixkosten der Durchsetzung ≤ 15 % des Kontextfensters
     ├── 6.2 Evidenztransport nur als Verdict, nie als Rohdaten
     └── 6.3 Kompaktifizierung erhält Invarianten und Gate-Status (Schutzliste)
```

### 10.2 Bewertungsszenarien

| # | Szenario | Maß/Zielwert |
|---|---|---|
| Q1 | Neue Anforderung wird implementiert | 100 % der FRs der betroffenen Spec haben nach P5 mindestens einen grünen Test mit FR-ID; Konvergenz-Status „Converged“. |
| Q2 | Externe Prüfung eines 3 Monate alten Features | Prüfer findet vollständige Kette (Spec-Stand, Change, PR, Review-Log) in < 10 Minuten allein aus dem Repository. |
| Q3 | Agent versucht Merge ohne PR / Gate ohne Freigabe | Technisch unmöglich (Branch Protection) bzw. Prozessverletzung im Audit sichtbar; 0 Vorfälle. |
| Q4 | Verhaltensändernder Hotfix ohne Change | Wird an G5 blockiert oder im nächsten Drift-Audit (≤ 7 Tage) als Befund gemeldet; Realign-Change abgeschlossen ≤ 5 Arbeitstage. |
| Q5 | Triviale Änderung (Bounded) | Gesamter Prozess-Overhead ≤ 10 Minuten menschlicher Zeit; trotzdem dokumentierte Freigabe vor Implementierung. |
| Q6 | Wiederholter Review-Befund derselben Klasse | Nach Regel-Promotion: Wiederholungsrate der kodierten Fehlerklasse = 0 (gemessen über Befundklassen im Review-Log). |
| Q7 | Kontextübergreifende Wiederaufnahme | Neuer Agent mit leerem Kontext setzt Arbeit allein aus Artefakten fort, ohne Rückfragen zu getroffenen Entscheidungen. |
| Q8 | Feature-Session mit vollständiger Durchsetzung (alle Gates, alle Evidenzen) | Fixkosten-Belegung vor Arbeitsbeginn ≤ 20 % des Fensters (davon Durchsetzungs-Fixkosten ≤ 15 %); die Kompaktifizierungsschwelle wird frühestens durch Arbeitskontext erreicht, niemals durch Durchsetzungsartefakte; gemessen per KB-10-Telemetrie in jedem Gate-Report. |
| Q9 | Abbruch mitten in P4 (Session-Crash, Kompaktifizierung, Laptop-Sleep) | Eine neue Session in einer neuen Substrat-Session findet über den Arbeitsgraph exakt den nächsten claimbaren Task inklusive Abhängigkeiten und Fortschrittsnotizen (`bd ready`/`bd show`); kein Work-Item und kein Abhängigkeitszusammenhang geht verloren; Wiederaufnahme ohne Rückfragen an den Menschen. |
| Q10 | Unbeaufsichtigter Nachtlauf in der Omnigent-Zieltopologie | Alle Sessions laufen sandboxed (IS-6); jede Aktion außerhalb der Approval Boundaries wird von Server-Policies geblockt oder als Approval-Anfrage gestellt, die vom Mobilgerät beantwortbar ist; Spend-Cap begrenzt die Kosten des Laufs hart; das Aktionslog rekonstruiert am Morgen jede Aktion; Ausfall des Omnigent-Servers selbst verliert keine Arbeit (Repo + Arbeitsgraph, Q7/Q9). |

---

## 11. Risiken und technische Schulden

| Risiko | Eintrittswahrscheinlichkeit / Auswirkung | Mitigation in der Architektur | Restrisiko |
|---|---|---|---|
| **Gate-Erosion**: Unter Zeitdruck werden Freigaben zur Formsache („rubber stamping“) | mittel / hoch | Kurze Artefakte (C7), Begründungspflicht bei Ablehnung, Q5-Zielwert, Ratsche I5 | mittel — Kulturfrage, nicht vollständig technisch lösbar |
| **Spec-Drift trotz Mechanik** (v. a. Rückwärts-Drift aus Fremdbeiträgen) | hoch / mittel | SM-22 (G5-Filter), SM-25 (Audits), SM-24 (Realign-Pflicht) | niedrig–mittel |
| **Artefakt-Inflation**: Teams produzieren Dokumente statt Software | mittel / mittel | Prozessgewichtung (8.2), Seitenlimits (P1-8), „Artifact scales, approval doesn't“ (I6) | niedrig |
| **Kontext-Verschmutzung bei großen Monorepos** | mittel / hoch | I3, Subagent-Destillate (ADR-08), Scoped Exploration | mittel — abhängig von Harness-Reife |
| **Modell-/Harness-Regressionen** nach Updates | mittel / mittel | Harness-Neutralität (ADR-07), Gates als modellunabhängige Kontrollschicht | niedrig |
| **Framework-Lock-in auf Tool-Ebene** (Spec Kit vs. OpenSpec vs. Eigenbau) | mittel / niedrig | Architektur definiert Konventionen, nicht Tools (C2); Delta-Semantik ist portabel | niedrig |
| **Vertrauens-Automation Bias**: Menschen übernehmen G4-Ergebnisse ungeprüft auch in Eskalationsfällen | mittel / hoch | Eskalations-Router mit expliziter Mensch-Pflicht bei Critical/Zurückweisung; Q6-Messung | mittel |
| **Unbeaufsichtigte Läufe erzeugen PR-Flut** | mittel / mittel | Stop-Bedingungen (P6-5), Iterationslimits, Heartbeat + Prozessgruppen-Kill (§8.4), G5 als Menschenfilter | niedrig |
| **Agent schwächt die Verifikation selbst** (Linter-Config, Coverage-Schwelle, `--no-verify`) | hoch / hoch | ADR-11: Config-Protection + Bypass-Blockade auf Tool-Ebene; Registry-Diffs im PR sichtbar | niedrig |
| **Gelernte Regeln kodieren schlechte Muster** (Confidence aus Wiederholung, nicht Wahrheit) | mittel / mittel | ADR-13: Projekt-Scope, Promotion erst nach 2+ Projekten, menschliches Review-Gate bei Promotion, Injection-Budget | mittel — Beobachtung bleibt kein Wahrheitsbeweis |
| **Deaktivierbarkeit der Durchsetzung** (Env-Flags, Strictness-Profile öffnen Umgehungskanäle) | mittel / hoch | §8.7: Deaktivierungs-Flags selbst blockieren bzw. in Hochrisiko-Umgebungen sperren; Registry als diffbares Artefakt | mittel — Komfort/Sicherheits-Trade-off bleibt konfigurationsabhängig |
| **Kontextblähung durch Durchsetzungsartefakte**: Naive Evidenz-Injektion (volle Specs, Logs, Attestierungs-JSONs im Prompt) füllt das Fenster vor Arbeitsbeginn und macht Guardrails durch Context Rot / Lost-in-the-Middle faktisch unsichtbar | mittel / hoch | C10, §8.9 (KB-1 bis KB-5): Prüfungen außerhalb des Kontexts, Verdict-not-Log, Injektionsbudget, Delta-Loading, Progressive Disclosure; Q8-Messlatte | niedrig — bei Einhaltung von KB-1/KB-2 |
| **Kompaktifizierung kürzt Invarianten weg**: Die Auto-Kompaktifizierung entfernt ausgerechnet Regeln, Verbote oder Gate-Status; der Agent arbeitet danach prozesskonform aussehend, aber ohne die Regeln im Fenster | mittel / hoch | KB-7: Schutzliste im Kompaktifizierungs-Schritt (Invarianten, FR-IDs, Gate-Status); KB-8: Positionsdisziplin; KB-10: Telemetrie macht Belegungssprünge sichtbar | mittel — abhängig von der Harness-Kontrolle über den Kompaktifizierungs-Prompt |
| **Paralleler Blast Radius**: Mehrere Agenten in parallelen Sessions mit weiten Rechten erzeugen gleichzeitig schlechte Edits; der Schaden skaliert mit der Parallelität | mittel / hoch | IS-1/IS-2: Worktree-Isolation pro Agent, kleine Tasks, Least Agency (§8.4), sequenzielles Mergen (P6-2); G4/G5 bleiben pro Change wirksam; Merge-Queue-Muster als KANN bei hoher Parallelität | mittel — Disziplin- und Rechtefrage, kein Substrat-Feature |
| **Substrat-Sandbox-Fehlinterpretation**: Teams halten tmux-/Herdr-Isolation fälschlich für Sicherheitsisolation und lockern Approval Boundaries | mittel / hoch | IS-5 als explizite Architektur-Regel; §8.4 unverändert; Sicherheitsgrenze liegt serverseitig | niedrig — bei Schulung/Kommunikation |
| **Arbeitsgraph-Reife und Sync-Fehler**: Beads ist jung (1.0 erst 2026); Sync-/Migrations-Bugs und veraltete Kommandos in persistenten Agenten-Gedächtnissen sind dokumentierte Realfälle | mittel / mittel | AG-5 (Landing the Plane als Pflicht), AG-6 (Versions-Pinning, JSONL-Audit-Export, Pflege der AGENTS.md-Instruktionen bei Upgrades); Git bleibt letzte Wahrheit — Graph ist rekonstruierbar | niedrig–mittel — Git-Backing begrenzt den Schaden |
| **Voll-Orchestrator-Versuchung**: Der sichtbare Erfolg von Gas Town verleitet zum Sprung auf Multi-Agenten-Orchestrierung, bevor Aufgabenklasse und Parallelisierbarkeit das rechtfertigen (Token-Kosten, Betriebskomplexität) | mittel / mittel | ADR-16 trifft die bewusste Teilübernahme (Substrat + Arbeitsgraph, kein Rollen-Orchestrator); §4 verwirft Orchestrierung als Default; Eskalationspfad bleibt über Prozessgewichtung (§8.2) | niedrig |
| **Omnigent-Reife (Alpha)**: Schnelle Breaking Changes; bereits eine kritische Lücke in der Historie (CVE-2026-62674, CVSS 9.0, Command-Injection über geteilte Agenten, gefixt in 0.3.0) — Meta-Harness-Ebene ist selbst Angriffsfläche | hoch / mittel | Versions-Pinning mit bewusstem Upgrade-Prozess (Changelog-Pflichtlektüre, Test-Deployment vor Produktiv-Upgrade); geteilte/fremde Agenten-Definitionen nur aus eigenem Repo laden; Omnigent-Policy-Dateien unter demselben menschlich reviewten PR-Pfad wie das Regelwerk (§8.4); Fallback-Topologie (tmux) bleibt dokumentiert und geübt | mittel — Abhängigkeit von der Weiterentwicklung durch Databricks |
| **Telemetrie-Default**: Omnigent sendet in der Grundkonfiguration Nutzungs-Telemetrie (Opt-out) | mittel / mittel | Opt-out als verpflichtender Installationsschritt (C11); Netzwerk-Egress der Server-Instanz in der eigenen Firewall-Policy sichtbar machen | niedrig |
| **Sandbox-Plattformasymmetrie**: `bwrap` (Linux) ist die starke Variante; Windows nutzt Job Objects mit schwächerer Isolation; macOS `seatbelt` dazwischen | mittel / mittel | Unbeaufsichtigte und risikoreiche Läufe auf Linux-Runner oder in Cloud-Sandboxes verlegen (IS-6); Windows nur interaktiv mit verschärften Approval-Policies | niedrig–mittel |

---

## 12. Glossar

| Begriff | Definition |
|---|---|
| **Living Spec** | Domänen-organisierte Spezifikation des aktuellen Systemverhaltens; wird bei jedem archivierten Change aktualisiert; Ebene 1 des Spec-Modells. |
| **Change(-Ordner)** | Versionierte Arbeitseinheit mit Artefakt-Bundle (proposal, Delta-Specs, design, tasks, review-log); Ebene 2 des Spec-Modells. |
| **Delta-Spec** | Änderungsbeschreibung relativ zur Living Spec mit den Sektionen ADDED / MODIFIED / REMOVED / RENAMED; MODIFIED enthält die vollständige neue Fassung. |
| **Sync** | Semantischer, idempotenter, validierter Merge der Delta-Specs in die Living Specs (SM-29), Voraussetzung für Archivierung. |
| **Archiv** | Datiert abgelegte, unveränderliche abgeschlossene Changes (`changes/archive/YYYY-MM-DD-…`); Audit-Trail. |
| **Spec-Drift** | Divergenz zwischen Spec und Code; vorwärts (Änderung nicht implementiert) oder rückwärts (Code ohne Spec-Änderung). |
| **Realign-Change** | Kleiner Change, der eine Living Spec auf den Ist-Zustand des Codes zieht (Behebung von Rückwärts-Drift). |
| **Gate (G0–G5)** | Blockierender Kontrollpunkt mit definierten Eingangskriterien und Entscheidungsoptionen; G0–G3, G5 menschlich, G4 automatisiert mit Eskalation. |
| **Constitution** | Projektweites, unverhandelbares Regelwerk (Qualität, Tests, Verbote); wird in P2 geprüft (Constitution Check, vor und nach Design). |
| **Harness** | Laufzeitumgebung eines Coding-Agenten (Tool-Zugriff, Kontextverwaltung, Ausführung); Beispiele: OpenCode, Claude Code, OpenHands. |
| **Invarianten (I1–I6)** | Phasenübergreifende, nicht verhandelbare Architekturregeln (Artefakt vor Aktion; Zustand in Dateien/Git; frischer Kontext; keine Selbstgenehmigung; Einbahn-Ratsche; Gate skaliert nie). |
| **Traceability-Kette** | Durchgehende Referenz `FR-ID → Szenario → Test → Commit → PR → Change → Archiv`; Grundlage von Impact-Analyse und Drift-Audit. |
| **Einbahn-Ratsche** | Regel I5: Aufgabenklassifikation darf während der Ausführung nur hochgestuft werden (mehr Prozess), niemals herunter. |
| **Bounded-Test** | Kriterium für die Klasse „Bounded“: es muss ein existierender, lesbarer Flow im Bestand geben, der geändert wird. |
| **Regel-Promotion** | Überführung akzeptierter Review-Erkenntnisse in persistente Regeln; Closed-Loop-Lernmechanismus mit Confidence-Lifecycle (Kandidat → Projekt-Scope → global nach 2+ Projekten, Injection-Budget). |
| **Fact-Forcing** | Gate-Muster: Vor riskanten Aktionen muss der Agent konkrete Fakten liefern (Importer, API, Schema, Rollback-Plan) statt Selbstbestätigung — Untersuchung als Eintrittskarte (ADR-12). |
| **Hook-Registry** | Schema-validiertes Inventar aller Durchsetzungsmechanismen mit stabiler ID, Zweck und Fingerprint; macht die Durchsetzung selbst auditierbar (§8.7). |
| **Non-Vacuity** | Anforderung an jedes Gate: Es muss nachweisbar rot werden *können* (bekannt-schlechter Testfall) und zur Laufzeit eine nicht-leere Subjektmenge prüfen — ein Gate über einer leeren Menge ist von einem bestandenen ununterscheidbar. |
| **pass@k / pass^k** | Konsistenzmetriken: pass@k = mindestens ein Erfolg aus k Versuchen (genügt für Exploration); pass^k = alle k Versuche erfolgreich (gefordert bei Verifikation nicht-deterministischer Objekte). |
| **Least Agency** | Sicherheitsprinzip: Der Agent erhält nur den minimalen Handlungsspielraum, den die Aufgabe erfordert; die Sicherheitsgrenze ist die Policy zwischen Modell und Aktion, nicht der System-Prompt. |
| **Confidence-Lifecycle** | Lebenszyklus gelernter Regeln (aus ECC Instincts): atomare Regel mit Evidenz und Konfidenz 0,3–0,9, Projekt-Scope als Default, Promotion zu global nach projektübergreifender Evidenz, budgetierte Injektion. |
| **Heartbeat-Modell** | Überwachung unbeaufsichtigter Läufe: Task schreibt periodisches Lebenszeichen; Supervisor terminiert bei Ausbleiben die gesamte Prozessgruppe und quarantäniert den Task zur Log-Inspektion. |
| **ADR** | Architecture Decision Record: dokumentierte Entscheidung mit Kontext, Optionen, Entscheidung, Konsequenzen. |
| **MCP / ACP / AGENTS.md** | Offene Interoperabilitätsstandards: Werkzeuganbindung (Model Context Protocol), Client-Agent-Anbindung (Agent Client Protocol), projektweite Agenten-Instruktionen. |
| **EARS** | Easy Approach to Requirements Syntax; Notation für mehrdeutigkeitsfreie, testbare Anforderungen („WHEN … THE SYSTEM SHALL …“). |
| **Context Rot** | Qualitätsdegradation von Modellausgaben mit wachsender Kontextfüllung; setzt weit vor dem Fensterlimit ein; treibt I3, ADR-08 und §8.9. |
| **Lost-in-the-Middle** | Positionaler Degradationseffekt: Informationen in der Fenstermitte werden vom Modell deutlich schlechter verarbeitet als am Anfang/Ende; begründet KB-8 (Positionsdisziplin). |
| **Kontextbudget (KB-1 bis KB-10)** | Normative Anforderungen zur Kontextökonomie der Durchsetzungsschicht (§8.9): Prüfungen außerhalb des Kontexts, Verdict-not-Log, Injektionsbudgets, Delta-Loading, Progressive Disclosure, Sub-Agent-Isolation, Kompaktifizierungs- und Positionsdisziplin, Retrieval-Hygiene, Budget-Telemetrie. |
| **Verdict-not-Log** | Prinzip KB-2: Evidenz zirkuliert im Agentenkontext nur als kompaktes Ergebnis (READY/NOT READY, Score, Warnliste) plus Verweis (Pfad/Hash) auf das Repo-residente Evidenzartefakt — niemals als Rohdaten. |
| **Progressive Disclosure** | Lademuster KB-5: Fähigkeiten/Prozesswissen liegen im Ruhezustand nur als kurze Metabeschreibung (~80 Token) im Kontext; der Volltext wird erst bei tatsächlicher Aktivierung geladen. |
| **Session-Substrat** | Laufzeitschicht unter den Agenten (tmux oder Herdr): startet, isoliert und überwacht Agenten-Sessions als eigene Prozesse/Panes; liefert Prozess-/Kontext-Isolation, Persistenz über Disconnects und Zustandsbeobachtbarkeit — ausdrücklich keine Sicherheits-Sandbox (IS-5). |
| **Herdr** | Junges, agentenbewusstes Terminal-Multiplexing („tmux für Agenten", pre-1.0): eingebaute Zustandserkennung (working/blocked/done/idle), Blocker-Benachrichtigungen und Socket-API, über die Agenten Panes erzeugen und auf Zustände warten können; KANN-Alternative zu tmux (ADR-15). |
| **Arbeitsgraph (Beads, `bd`)** | Git-synchronisierter, abhängigkeitsbewusster Issue-Graph für Agenten (Dolt-Datenbank unter `.beads/`, JSONL-Export als Klartext-Sicht): Ready-Erkennung (`bd ready`), Claim/Release-Semantik, `discovered-from`-Kanten; operative Task-Registry der Ausführungsebene (ADR-16, AG-1 bis AG-7). |
| **Landing the Plane** | Pflicht-Hygienesequenz am Session-Ende (AG-5): Arbeitsgraph synchronisieren, fertige Beads schließen, offene mit Fortschrittsnotiz versehen, committen/pushen — die nächste Session startet aus dem Graph, nicht aus Erinnerung. |
| **GUPP** | „Gastown Universal Propulsion Principle": Sessions sind flüchtig („Vieh"), die Arbeit liegt persistent im Arbeitsgraph — liegt Arbeit auf dem Hook, wird sie von der nächsten verfügbaren Session ausgeführt; Begründungsmuster für Session-Unabhängigkeit (Q9). |
| **Omnigent** | Meta-Harness (Databricks, Apache 2.0, Alpha) oberhalb der Coding-Harnesses: tmux-basierte Terminals mit OS-Sandboxing (`bwrap`/`seatbelt`/Job Objects), dreistufiges Action-Policy-System (Server/Agent/Session → allow/block/approve), Spend-Caps, Cloud-Sandbox-Adapter, geräteübergreifende Session-Synchronisation; Ziel-Laufzeitschicht dieser Architektur (C11, ADR-17). |
| **Meta-Harness** | Steuerungsebene oberhalb einzelner Coding-Harnesses (Analogie: Kubernetes für Agenten) — ersetzt keine Coding-Engine, fügt Orchestrierung, Policy und Observability harnessübergreifend hinzu. |
| **Polly** | Omnigents Orchestrierungs-Agent: plant, delegiert an Sub-Agenten verschiedener Harnesses in separaten Worktrees und erzwingt Cross-Vendor-Review (Implementierer und Reviewer aus unterschiedlichen Modellfamilien); optionale Instanziierung von IS-4/G4 — Voll-Orchestrierung bleibt kein Default (§4). |
| **Action-Policy (Omnigent)** | Stateful ausgewertete Regel pro Agenten-Aktion (allow/block/approve) auf Server-, Agent- oder Session-Stufe; Instanziierung der Approval Boundaries (§8.4) — Durchsetzung außerhalb des Prompts. |

---

*Anhang — Verhältnis zu den Vorarbeiten: Dieses Dokument konsolidiert die drei Vorarbeiten in arc42-Form: (1) „Referenzmodell Agentischer Delivery-Workflow“ (Phasen P0–P6, Gates G0–G5, Invarianten I1–I6, Entscheidungsrechte) → Kapitel 4, 5, 6, 8, 9; (2) „Spec-Management: Versionierung und Änderungspropagation“ (SM-1 bis SM-31) → Kapitel 5.2, 6.2, 6.3, 8.1, 8.5, 10; (3) „Workflow-Steuerung im Harness“ (Evidenzbasis, Framework-Vergleich, Anti-Patterns) → Kapitel 4 (verworfene Alternativen), 11. Ergänzend flossen die Konzepte E-1 bis E-10 aus der ECC-Repo-Analyse (affaan-m/ECC, 16.09.2026) ein: Schutz der Durchsetzungsschicht (§8.7, ADR-11), Fact-Forcing (ADR-12), Confidence-Lifecycle (§8.6, ADR-13), Modell-Routing und pass^k (§8.8, ADR-14), Heartbeat/Least Agency (§8.4), Verifikations-Report (§6.1), Search-First (§6.1) — dokumentiert in „ECC-Analyse: Übernahme in die Referenzarchitektur“. Aus der Kontextbudget-Prüfung (17.09.2026) flossen die Kontexteffizienz-Anforderungen ein: Randbedingung C10, Qualitätsziel 6 und Szenario Q8, Querschnittskonzept §8.9 mit KB-1 bis KB-10, zwei neue Risiken in §11 sowie Glossar-Ergänzungen — dokumentiert in „Kontextbudget-Prüfung und -Begrenzung“. Aus der Substrat-/Arbeitsgraph-Prüfung (17.09.2026) flossen ein: Session-Substrat tmux/Herdr (§8.10, IS-1 bis IS-5, ADR-15) und Beads als Arbeitsgraph (§8.11, AG-1 bis AG-7, ADR-16) mit Anpassungen an C1 (`.beads/`-Ausnahme), §5.1 (zwei neue Bausteine), §6.1/§6.3/§6.4 (Claim-Loop, discovered-from, Nachtmodus-Persistenz, Landing the Plane), §7 (Speichermodi), Q9 sowie fünf neue Risiken in §11. Aus der Omnigent-Festlegung (17.09.2026, Version 1.2) flossen ein: C11 und ADR-17 (Omnigent als Ziel-Laufzeit- und Governance-Schicht bei unverändert harness-neutralen Konventionen), neuer Baustein „Laufzeit- und Governance-Schicht" in §5.1, Omnigent-Zeilen in §3.2 und §7 (Server-Knoten, Cloud-Sandboxes), IS-6 und Umstellung von §8.10 auf die Ziel-/Fallback-Topologie, Policy-Instanziierung der Approval Boundaries in §8.4, Cross-Vendor-Review als G4-Instanziierung in §5.3, Nachtmodus-Verstärker in §6.4, Szenario Q10 sowie drei neue Risiken (Alpha-Reife, Telemetrie-Default, Sandbox-Asymmetrie) in §11. Der operative Weg zur Zieltopologie ist im „Migrationsplan: Referenzarchitektur mit Omnigent instanziieren" festgelegt (Stufen 0–4: POC → Bounded-Klasse → Feature-Pfad mit Cross-Vendor-Review → Nachtmodus/Parallelität → Härtung; mit Exit-/Abbruchkriterien je Stufe, Fallback-Disziplin und Messlatten an Q1–Q10). Die arc42-Struktur folgt dem offiziellen Template (arc42.de/arc42.org).*
