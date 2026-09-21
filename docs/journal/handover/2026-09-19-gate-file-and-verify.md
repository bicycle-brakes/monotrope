---
title: "Session handover — gate file, one verify command and the CI derivation (bo0), 2026-09-19"
category: handover
created: 2026-09-19
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-19"
tags: [handover, gates, bo0, 2ee, omnigent]
target_ref: a547826
bead: coding-harness-bo0
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Handover: gate file and one verify command (bo0)

The maintainer approved five gap solutions on 2026-09-19 (recorded in the
session that also revised the three Omnigent-first artefacts for readability,
commit `a547826`). This session implemented the first one: the gate file, the
one verify command and the CI derivation — bead `coding-harness-bo0`, still
open because the export renderer of D-4 is deliberately not delivered yet.

## What was built and what proves it

- `decisions/gates.yaml` — the one gate list (12 gates: pytest, ruff-check,
  ruff-format, leerprobe, plans-registry, docs-links, bead-export,
  gate-schema, ci-drift, dangling-beads, markdownlint, lychee,
  plans-registry-strict; enforcement as advisory/report/block, floor flags,
  one reason each).
- `scripts/ci_gates.py` rewritten: reads the gate file, validates its schema,
  derives `.github/workflows/ci.yml` (`--generate-ci`) and holds the committed
  workflow to the derivation (`--check-ci`, the `ci-drift` gate). The old
  direction — ci.yml as the source — is reversed per the bo0 re-scope.
- `scripts/verify_all.sh` — the local runner: no commands of its own, resolves
  the pinned interpreter (G-12), respects the enforcement vocabulary (only
  `block` turns the run red), prints a report with candidate/base SHAs and the
  gate-file hash.
- `Makefile` — `make verify` delegates to the runner; `make test` and
  `make staleness` carry the exact gate commands, pinned against the list by
  `test_the_makefile_runs_what_the_one_list_runs` (W-6).
- `scripts/check_docs.py`, `scripts/check_bead_export.py`,
  `scripts/check_dangling_bead_ids.py` — three new honest gates (docs
  frontmatter/links/anchors; export line check; cited bead ids resolve).
- `tests/test_gate_machinery.py` — mutation proofs (`*_goes_red_when_*`) for
  the self-built gates plus execution coverage the ratchets demand.
- Evidence: `pytest tests/test_ci.py tests/test_gate_machinery.py` →
  46 passed, 2 skipped; `make verify` runs end to end; the Leerprobe
  (`scripts/kit/probe.py --strict`) exits 0.

## The maintainer's five decisions (2026-09-19)

1. `bo0`: manifest + verifier + generated CI (this session's work).
2. `2ee`: triage the red tests into three buckets — rebuild enforcer /
   instance-only with dated valve / fix the rule text.
3. `9qo`/`jc3`: templates, then validator, then a Bounded probe — before M1.
4. Kit proof: a throwaway-repo test (deliberately extra effort for clean
   isolation; may share M0's disposable-repo setup).
5. Decision protection: a validator rule (every D/O id mapped) plus the three
   ADRs — early parallelism, coordinator permission, public-scan naming —
   before any runtime activation. None of the three ADRs exists yet.

## 2ee triage started inside this session

Two `test_ci.py` tests are classified as instance-only with a dated valve
(skip markers, reason names `coding-harness-2ee`, valve before M1):
`test_formatter_exclusion_survives_an_explicit_path` and
`test_the_archived_landing_page_is_not_wired_to_anything`. `REIST_NICHT` in
`scripts/kit/probe.py` was rewritten for the new gate world (72 declared,
measured via `--messen`; DECKEL visibly raised 62 → 75 with reason). The kit
manifest classifies the new files as mechanism (`decisions/`, the derived
`ci.yml`, the three new checks, the runner).

## Remaining red — owned, named, not hidden

- `pytest` gate: 37 in-repo failures, all pre-existing migration debt —
  `test_regelwerk` 21 (enforcers live in portfolio), `test_feedback_channel`
  11, `test_kit` 3, `test_model_endpoints` 1 (+ parametrised). Owned by
  `coding-harness-2ee` (bucket 1: rebuild the enforcers here; bucket 2:
  classify with dated valves).
- `docs-links` gate: 35 corpus findings (dead links in governance/WORKFLOW
  docs, frontmatter gaps). Owned by `coding-harness-bt8`; the gate runs as
  `report` until bt8 lands, then flips to `block` (the dated valve is the
  flip).
- `bo0` stays open: the export identity gate of D-4 needs the one-writer
  renderer first; that deliverable pairs with the export script (see the
  implementation plan, "Export renderer and identity gate together").

## Session-state notes

The checkout stands on `docs/omnigent-first-target` (PR #8 head at session
start: `160f234`); the readability revision `a547826` and this session's
follow-up commit are pushed to it. A backup stash `stash@{0}` from the
checkout switch can be dropped. `plans/INDEX.md` was regenerated
(`plans_registry.py --index`) after the earlier stash had taken it.
Interpreter note: the system `python3` lacks pytest/PyYAML — the suite runs
under `/Users/mikypiky/.venvs/portfolio-agentic-engineering/bin/python3`, and
the runner resolves an interpreter with PyYAML on its own.

## Next session

One concrete action: claim `coding-harness-2ee` and run the three-bucket
triage over the 37 named failures — the pytest gate turns green as the
buckets close, and that is the last M0 prerequisite after the three ADRs.

## Addendum: continuity gate, export identity and PR split (2026-09-19, same session)

- **PR split.** The gate machinery moved out of #8 onto its own branch —
  **PR #11** (`feat/gate-file-and-verify`, based on main, cherry-picked).
  #8 is docs-only again (head `a547826`).
- **PR #12** — the three ADRs (early parallelism D-3/D-7, exclusive
  coordinator writer, public-scan naming D-17), stacked on #8, bead
  `coding-harness-nkr`.
- **Continuity gate** (`decision-continuity`) + validator
  `scripts/check_decision_continuity.py`: every D/O id must stay mapped,
  every amendment ADR must exist. SKIPs visibly while the target document
  lives in #8; sharpens after the merge. Goes-red proof in
  `tests/test_gate_machinery.py`.
- **D-4 delivered:** `scripts/render_beads_export.py` (one-writer renderer —
  renders via `tools/bd` into a temp file, line-validates, then moves) plus
  the `export-identity` gate (committed export must equal the fresh render;
  SKIPs where the tracker does not live). AGENTS.md house rule 4 updated.
  With this, `bo0`'s scope is complete — it closes when #11 reaches main.
- **Leerprobe re-set:** `REIST_NICHT` re-measured (52 entries, DECKEL 53),
  the two intentionally-empty-geruest cases carry their proper vocabulary;
  probe exits 0.
- **Parallel sessions observed:** a Codex session (read-only on this repo,
  usage-limited) and a Cline session were active while this session ran;
  tracker writes were coordinated around them. The shared terminal swallowed
  two long commands — keep commands short when a TUI shares the pane.

Remaining red is unchanged in ownership: the `pytest` gate (37 = `2ee`) and
the `docs-links`/`markdownlint` reports (`bt8`).


## Anhang 3 — 2026-09-20: `2ee` geschlossen, VERIFY GREEN

Die Welle 3 ist mit der Präfix-Entscheidung des Maintainers („enger Kern
reist") umgesetzt und PR #15 ist bereit. Cluster D ist gefallen: die 7
Agent-Definitionen aus AGENTS.md §3 sind **committed** (`.claude/agents/`,
je `model: claude-sonnet-5` und die RB-A1-Klausel byte-gleich aus dem
Regelwerk §6 — extrahiert mit der Logik des Tests selbst). Eine parallele
Codex-Session kann sie nicht mehr still löschen; ein Löschen wäre jetzt
ein sichtbarer Git-Delete.

Stand: **264 passed, 0 failed, 15 skipped.** `make verify`: **VERIFY
GREEN** — alle 11 Gates (pytest, ruff-check, ruff-format, leerprobe,
plans-registry, bead-export, dangling-beads, decision-continuity,
export-identity, gate-schema, ci-drift). Die Sperrklinke trägt 30
Einträge (DECKEL 31): die 7 neuen Fälle sind die Agent-Modelle gegen den
geruest-Rumpf `model-endpoints.yaml` im Leerprobekopf.

Bead `coding-harness-2ee` ist geschlossen. Was bleibt, ist menschliche
Abnahme: Reviews der Kette #8 → #12 → #11 → #13 → #14 → #15 und die
ADR-Annahme in #12. Damit ist M0 mechanisch vollständig.

