---
title: "coding-harness bootstrap — repository, tracker, separation plan — as of 2026-09-16"
category: handover
created: 2026-09-16
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: Cline
  version: "2026-09-16"
tags: [handover, bootstrap, migration, beads, separation]
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Handover — coding-harness bootstrap

Written in English because that is the decided direction for content
artefacts. This file is the first document of this repository and doubles as
the migration's anchor: every open item that conceptually belongs here but is
still tracked in `portfolio-agentic-engineering` is referenced from here by
full id. **No tracker items were imported** — one item, one tracker; the new
tracker starts empty except the beads created by this session.

## What this repository is

The source of truth for the coding workflow: seven phases, three stages, the
session handover, the kit that carries the process into new repositories, and
the research corpus. It splits one role out of
`portfolio-agentic-engineering`, which was carrying four at once (framework
governance, coding workflow, OSI→lakeswitch transfer logistics, domain
content) — a mixing its own architecture register documents (categories D and
E, measured 2026-09-15).

The three-repo topology after the separation:

| Repo | Role |
|---|---|
| `coding-harness` (here) | doctrine, prompts, templates, kit, model routing, research — later the template repository |
| `portfolio-agentic-engineering` | framework governance, transfer logistics, domain content |
| `lakeswitch-ai` | product repo, clean-room workflow instance — untouched by this migration |

## What this session did (2026-09-16)

- Created the private repository and cloned it to `~/coding-harness`.
- Bootstrapped the tracker with an **explicit prefix**:
  `bd init --prefix coding-harness --non-interactive`. Verified output:
  *Issues will be named: coding-harness-\<hash\>*. The prefix is not
  correctable afterwards (the failure mode behind
  `portfolio-agentic-engineering-wp-p0.1`).
- Set `git config beads.role maintainer` (silences the role warning,
  GH#2950) and `bd config set export.auto true` — the rendered export
  (`.beads/issues.jsonl`) now updates after writes without a separate render
  script.
- Confirmed the Dolt remote `origin` was registered automatically
  (`git+https://github.com/MPAdesso/coding-harness.git`); transport follows
  the `refs/dolt/data` model.
- Added `tools/bd` (version pin `1.1.2` in `tools/beads/VERSION`, refuses
  `init`/`migrate`/`upgrade`, escape hatch `BD_PIN_BYPASS=1`) — the
  guardrails exist from day one here, which portfolio never had.
- Laid the skeleton: `plans/changes/`, `plans/changes/archive/`,
  `plans/specs/` (empty, per the kit manifest's `geruest_ordner`),
  `docs/journal/handover/`, `docs/research/`, house `AGENTS.md` (English),
  `README.md`.
- Deliberately **no** `ci.yml` yet: an empty gate list would be a claim
  without content. It arrives with the first mechanism files (Phase 3.2),
  then holds exactly the gates those files need — one list, per repo.

## The separation plan (agreed with the maintainer)

Phases, each measured (Leerprobe `scripts/kit/probe.py` from portfolio +
`make verify` in both repositories), each moving ownership completely —
never copying:

1. **Phase 2 — research corpus intake** into `docs/research/` (lowest
   coupling, highest volume; this is what burst portfolio's frame).
2. **Phase 3 — mechanism migrates**, in order: templates → validators
   (`validate_change_artefacts.py`, `plans_registry.py`) → kit → cc-routing
   (`cc-*.sh`, `model-endpoints.yaml`) → prompts → `docs/WORKFLOW.md` last.
3. **Phase 4 — portfolio becomes a consumer**: mechanism files removed there,
   references rewritten, `zfyv` closed with a pointer here.
4. **Template switch** only after the Leerprobe sits at roughly ≥95 % and one
   full seven-phase run has happened in this repository.

## Open items — referenced, not imported

These live in the portfolio tracker and stay there until closed:

| Bead | State 2026-09-16 | Bearing on this repo |
|---|---|---|
| `portfolio-agentic-engineering-zfyv` | in progress | the workflow establishment this repo inherits; closes with a pointer here at Phase 4 |
| `portfolio-agentic-engineering-uqvm` | open | first full seven-phase run with metrics — its successor should run HERE, on real work |
| `portfolio-agentic-engineering-kmwa` | open | stage-2 keys and endpoints (`~/.config/cc-routing/secrets.env`); blocks nothing here |
| `portfolio-agentic-engineering-69il` | being fixed 2026-09-16 | the WORKFLOW §2 gate-sentence defect must be fixed BEFORE step 3.6 moves the file |
| `portfolio-agentic-engineering-wp-p3.7.2` / `-wp-p3.7.4` | open | skills-drift and tracker-drift gates — patterns to do better here, not to copy blindly |

## Standing constraints

- **English** for content artefacts, commit messages and PR bodies.
- **One writer per tracker.** A parallel session was working in portfolio
  during this bootstrap (the 69il fix and the #159 merge); portfolio was only
  read, never written.
- **The customer instance stays out of bounds** — requirements travel, never
  expressions.
- `docs/WORKFLOW.md` numbers carry their cut-off: everything measured there
  says *measured 2026-09-15, af09f8e*; after the move, re-measure instead of
  carrying stale counts.

## What to do first, next session

1. Check whether PR #159 (readability pass) and the 69il fix landed on
   portfolio master — both gate migration step 3.6.
2. Start Phase 2: intake the research corpus into `docs/research/`.
3. Keep this handover's table honest: when a portfolio bead closes, strike
   the row here with its closing date.

---

## Migration state — appended 2026-09-16, evening session

- **Phase 2 done** (commit `b15592a`): the three research documents carry
  frontmatter; `docs/research/_INDEX.md` added; provenance classes are
  `ai-drafted-reviewed` with review pending — the maintainer corrects a
  class where the hand differed. `coding-harness-anw` closed.
- **Phase 3 done** (commit `5efe809`): the 24 mechanism entries of
  portfolio's kit manifest adopted from portfolio master `4ce8240` — which
  already carried the 69il fix (PR #160) and the readability pages
  (PR #159). Deliberate deviations: no `ci.yml` yet (`coding-harness-bo0`),
  `.beads/issues.jsonl` stays this repository's own export.
- **Measured baseline** (portfolio venv, 2026-09-16): **167 passed,
  60 failed, 4 skipped.** Classes: 27 `test_ci` (bo0), 21 `test_regelwerk`,
  11 `test_feedback_channel`, 1 `test_model_endpoints` (`.claude/agents`,
  seam 1). Classified in the tracker; `test_kit`'s 19 collected, not yet
  run here — the Leerprobe is the acceptance run for this migration.
- **Phase 4a opened in portfolio:** PR #162 (branch
  `docs/sever-pointers-coding-harness`) carries ADR-032, the AGENTS.md
  banner and the rendered adr index. Not merged; **Phase 4b** (removing the
  mechanism copies there) follows the maintainer's per-gate decision.
- **Live reproduction of portfolio's wp-p0.1:** `bd create` produced
  short-prefix ids (`portfolio-vevj`, `portfolio-prrw`, `portfolio-lcb8`)
  in a worktree and in the main checkout, with `issue-prefix` correctly set
  and with `BD_ISSUE_PREFIX` — documented in PR #162's description. None of
  them reached a pushed state.
