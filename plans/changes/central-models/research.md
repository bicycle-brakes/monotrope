---
title: "Research — central-models"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ylu
owner: Data Architect
provenance: human-written
tags: [research]
---

# central models — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 418 files, 1129 commits, 12 rules.

## Runner exploration — 2026-10-14

Phase 1 (Explore) for `central-models` is done. One constraint to flag first: **this sub-agent session has no write tool** — only Glob, Grep, Read. Per the house rule for text-returned results, the completed `research.md` follows below, ready for the orchestrator to commit **unchanged** to `plans/changes/central-models/research.md` (commit message should say the file came back as text from the explorer).

**Wichtigste Befunde in Kurzform:**

1. **Zwei Seiten von „Modell" existiert heute:** die *Deklaration* (`model-endpoints.yaml` — Endpunkte, Betreiber, Residenz, Abrechnung, Datenklassen, `modelle`, die Leiter) und die *Aufrufseite* (`scripts/stage2.py` — Konstanten `GLM_FLASH`/`GLM`/`HAIKU`/`SONNET`/`CODEX`/`OPUS` als `(endpoint, model, effort)`-Tupel). `stage2_runs.py` importiert die Konstanten („cannot drift"), `declaration_problem()` prüft jeden Aufruf zur Laufzeit gegen die Datei — ein Abdriften fällt aber erst beim Aufruf auf, nicht in der Suite.
2. **Weitere Kopien:** zwei Routing-Tabellen in `docs/WORKFLOW.md` (Anzeigenamen), `**Model:**`-Zeilen in **allen zwölf** `prompts/*.md`, Routing-Prosa in `AGENTS.md`, sieben Agent-Pins `model: claude-sonnet-5` (eine Generation hinter dem gerouteten Sonnet 5.5), Literale in drei Testdateien, und `scripts/kit/probe.py` bettet `claude-sonnet-5` in bekannte Test-IDs ein.
3. **Was keinen Gate liest:** `AGENTS.md`; die Efforts (`max`/`xhigh`/`medium`) stehen nur in Konstanten und Prosa; die Anzeige­namen-Zuordnung ist eine Heuristik im Test (`_kandidaten()`), keine deklarierte Tabelle.
4. **Offen fürs Interview:** die Bead-Beschreibung (coding-harness-ylu) liegt im Dolt-Tracker und wurde **nicht gelesen** — was genau „zentral" heißt und um welche Quelle, ist die Interviewfrage.

```markdown
---
title: "Research — central-models"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ylu
owner: data-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, models, routing]
---

# central models — Research

Read on 2026-10-14 in the worktree of branch `explore/central-models`, cut from
`main` at the merge of pull request #142; the branch carries only this change's
opening commit. This change answers bead coding-harness-ylu ("central models").
The bead's description lives in the tracker database under `.beads/` and was
not read this session — the exploring session ran without a tracker read — so
the change's exact intent stands as the first open question for the interview
(phase 1a). What this file records is the fact base the name points at: model
ids and the routing around them are declared in one file and re-stated, in
several forms, in several other places.

## What exists today

### The declaration — `model-endpoints.yaml`

- `model-endpoints.yaml` (repository root), key `endpunkte:` — six entries:
  `anthropic-api`, `claude-code-plan`, `bedrock-claude`, `glm-coding-plan`,
  `openai-codex`, `opencode-go`. Each carries `betreiber`, `residenz`,
  `abrechnung`, `darf_sehen` and `modelle`. The header comment states the rule
  "not listed is BLOCK", the same as in the two manifests under `scripts/`, and
  names `tests/test_model_endpoints.py` (RB-A6) as its checker.
- Key `datenklassen:` — `framework`, `kundencode`, `kundendaten`. The three
  endpoints in use that are not the Anthropic first-party ones
  (`glm-coding-plan`, `openai-codex`, `opencode-go`) clear only `framework`.
- The ordered `modelle` list of `opencode-go` (`deepseek-v4.1-flash`,
  `mimo-v2.6-flash`, `mimo-v2.6-pro`) is the review loop's ladder.
  `scripts/stage2.py`, function `ladder()`, reads exactly this entry; the test
  comment says the order is the maintainer's to change "in this file alone" —
  the tests pin only the set and the count of the three ids.
- Each entry also carries a dated prose remark (`bemerkung`) with vendor facts
  (prices, URLs, terms, residency basis);
  `tests/test_model_endpoints.py`, function `opencode_remark_problems`, holds
  dozens of those sentences as literal needles, so even remark edits are
  test-locked.
- Kit role: `scripts/kit/manifest.yaml`, rule `prefix: model-endpoints.yaml`,
  role `bestand` — the file does not travel with the kit; a target repository
  declares its own (RB-A6). The manifest's "Dublette" comment (comment block
  above the `rollen:` key) refers to the retired `.beads/issues.jsonl` export,
  not to this file.

### The call side — `scripts/stage2.py` and its siblings

- Route constants in `scripts/stage2.py`: `GLM_FLASH`, `GLM`, `HAIKU`,
  `SONNET`, `CODEX`, `OPUS` — each an `(endpoint, model, effort)` tuple:
  `("glm-coding-plan", "glm-5.3-flash", "max")`,
  `("glm-coding-plan", "glm-5.3", "max")`,
  `("claude-code-plan", "claude-haiku-4-5", None)`,
  `("claude-code-plan", "claude-sonnet-5-5", "medium")`,
  `("openai-codex", "gpt-6.1-sol", "max")`,
  `("claude-code-plan", "claude-opus-5-5", "xhigh")`. The constants' comment:
  "what the declaration must clear and the call pins"; the reviews have no
  fixed tuple (the ladder).
- Also in `scripts/stage2.py`: `GLM_BASE_URL`
  (`https://api.z.ai/api/anthropic`), `OPENCODE = "opencode-go"`,
  `PI_VERSION = "1.1.0"`, and `CODEX_ASK_RULE` — the `Bash(codex *)` ask rule
  that `.claude/settings.json` states as well; `tests/test_stage2.py` holds
  both sides equal (`test_…` around the `codex_rule_problems` checks).
- Runtime tie to the declaration: `scripts/stage2.py`, function
  `declaration_problem(root, endpoint, model)` re-reads
  `model-endpoints.yaml` before a call and refuses an endpoint the file does
  not declare, a model the endpoint does not list, an endpoint not cleared for
  `framework`, or one without a stated residency. A constant that drifts from
  the file therefore fails at call time — not in the test suite.
- `scripts/stage2_runs.py`: `GLM = stage2.GLM` and
  `FOREIGN_ROUTES = (stage2.CODEX, GLM, stage2.GLM_FLASH)` — imported, per its
  comment "read from stage2.py and cannot drift". The same script reads
  `model-endpoints.yaml` for the run-record check behind the sentence
  "routes cleared by model-endpoints.yaml".
- `scripts/stage2_session.py`: `TRANSPORTS = {"openai-codex": "codex",
  "opencode-go": "pi"}`; the `session` verb validates `--model` and
  `opencode-go/<model>` ids at runtime against the declared `modelle` lists.
- The route names of the run records (`flash`, `flash-repair`, `glm`,
  `glm-repair`, `codex`, `codex-repair`, `stage-1`) are literal strings at the
  call sites in `scripts/stage2.py` (`implement()` and the draft/repair
  routes).

### The prose copies

- `docs/WORKFLOW.md` carries two routing tables: the phase table of §2
  (Haiku 4.5, Opus 5.5, Sonnet 5.5, gpt-6.1-sol, with efforts) and the stage-2
  table of §4 (GLM 5.3 Flash, gpt-6.1-sol, Opus 5.5, "the ladder"). Display
  names, not ids.
- Every one of the twelve files in `prompts/` opens with a `**Model:**` line
  (measured by search, 2026-10-14): `01-explore.md` GLM 5.3 Flash with Haiku
  4.5 as the `--stage2-off` route; `01a-interview.md` and `02a-spec-review.md`
  and `06-review.md` Opus 5.5; `02-spec.md`, `02b-design.md`, `03-plan.md`
  gpt-6.1-sol; `04-implement.md` GLM 5.3 Flash (body: Sonnet 5.5 fallback,
  gpt-6.1-sol for repair); `07-commit.md` Haiku 4.5. Three name no model on
  purpose: `05-verify.md` ("none"), `04b-review-loop.md` ("none of its own —
  the ladder's rung"), `research-recheck.md` ("none fixed — the runner's
  configuration names a model declared in model-endpoints.yaml" — the one
  prompt that already points at the declaration as the source).
- `AGENTS.md` states the routing in prose (Codex drafts, Opus 5.5 reviews 2a,
  the loop on the `opencode-go` ladder, GLM 5.3 Flash explores and implements,
  Haiku 4.5 / Sonnet 5.5 as the `--stage2-off` routes). No gate reads
  `AGENTS.md` for model names: the resolution test reads only
  `.claude/agents/`, `prompts/` and `docs/WORKFLOW.md`.

### The pins — agents, tests, kit probe

- `.claude/agents/`: seven definitions (`code-generation-orchestrator`,
  `consistency-auditor`, `entity-builder`, `entity-deployer`,
  `migration-supervisor`, `preconditions-gate-runner`,
  `reconciliation-orchestrator`), every one pinning `model: claude-sonnet-5`.
- `tests/test_model_endpoints.py`: resolves every agent pin
  (`test_every_agent_model_resolves_to_a_declared_endpoint`), every prompt
  model line (`test_every_model_in_a_phase_prompt_resolves`) and every routing
  row of `docs/WORKFLOW.md` (`test_every_model_in_the_routing_table_resolves`)
  against the declaration's ids. The display-name-to-id mapping is the
  heuristic `_kandidaten()` (dots to dashes, with and without a `claude-`
  prefix); the "the ladder" row is skipped there and covered by the entry
  test, which pins the set and count of the three Go ids.
- `tests/test_stage2.py`: the routing behaviour is asserted with literal ids
  (`--model glm-5.3-flash`, `-m gpt-6.1-sol`, `claude-opus-5-5`,
  `claude-sonnet-5-5`, `claude-haiku-4-5`, `glm-5.3`); `TEST_LADDER` names the
  three Go ids.
- `tests/test_stage2_session.py`: `GO_BARE = "mimo-v2.6-flash"` plus literal
  ids in the transport and ladder cases.
- `scripts/kit/probe.py`: the known-test list embeds `claude-sonnet-5` inside
  parametrized test ids of the agent resolution test (entries marked
  "braucht-die-vollstaendige-suite"). A model change under `.claude/agents/`
  breaks those entries until the list is edited.
- `.codex/config.toml` pins no model (only `[features] hooks = true`).
  `tools/` contains no model-id literals (searched for the six id families).
  `templates/` carries only the `<model>` placeholder
  (`templates/findings.md`) and `name: claude-code`
  (`templates/handover.md`).

## What already holds the copies together

1. `model-endpoints.yaml` is the permission source: runtime-checked before
   every foreign call by `declaration_problem`, and the reference the agent,
   prompt and routing-table resolution tests resolve against.
2. `scripts/stage2.py`'s constants are the call source, imported by
   `scripts/stage2_runs.py`; a drift from the declaration surfaces only when a
   call runs.
3. The past routing decisions travel as ADRs and are cited in the
   declaration's remarks: ADR 0007 (stage-2 reviews Codex and GLM), ADR 0011
   (loop to `opencode-go`), ADR 0016 (2a to Opus 5.5; GLM 5.3 drafts after two
   failed Codex attempts), ADR 0017 (repair to Codex).

## What is unclear

- **What the change is to centralize, and around which source.** The bead
  description was not read (tracker under `.beads/`, no tracker read this
  session). The candidates the tree offers: the route constants, the display
  names, the efforts, the ladder — each copy listed above has its own guard
  today, except where noted below.
- Efforts (`max`, `xhigh`, `medium`, None) are pinned in the constants and the
  prose tables; no declaration states them.
- The display-name-to-id mapping lives as the heuristic `_kandidaten()` in the
  test, not as a declared table.
- The `opencode-go` rungs are not part of `FOREIGN_ROUTES` in
  `scripts/stage2_runs.py`; the comment there leaves "whether criterion 4 now
  also names the OpenCode Go rungs" to the maintainer.
- The seven agent pins are `claude-sonnet-5` while the routing tables route
  to Sonnet 5.5 — a generation gap the governance already called "a matter of
  its own" (`docs/governance/regelwerk.md`, the Agents/Hooks/Templates entry;
  its counts — sixteen agents, fourteen older — reflect an earlier state of
  the tree; today there are seven).
- `docs/adr/` and `docs/governance/` are `human-decided` in `provenance.yaml`;
  any edit there is a decision pull request (ADR 0008). `prompts/` and
  `AGENTS.md` are declared `human-written` only — declared, not yet enforced
  (`provenance.yaml` header comment).

## Which files a change would have to touch

By concern, with the provenance class of each (`provenance.yaml`):

| Concern | Files | Class |
|---|---|---|
| The declaration | `model-endpoints.yaml` | unmapped path (no entry in provenance.yaml) |
| The call side | `scripts/stage2.py` (constants and the prompts built from them), possibly `scripts/stage2_session.py` | — (code) |
| Doctrine | `docs/WORKFLOW.md` (two routing tables) | `human-written` or `ai-drafted-reviewed`, frontmatter required |
| Prompts | `prompts/` — the Model lines of the twelve files | `human-written` only |
| Harness prose | `AGENTS.md` | `human-written` only |
| Agent pins | `.claude/agents/*.md` (seven files) | `human-written` or `ai-drafted-reviewed` |
| Gates | `tests/test_model_endpoints.py`, `tests/test_stage2.py`, `tests/test_stage2_session.py` | `human-written` |
| Kit probe | `scripts/kit/probe.py` (known-test ids) | — (code) |
| Decisions | a new or amended ADR under `docs/adr/` | `human-decided` — decision PR |

## Not found / not there

- Search over `plans/specs/` and `plans/changes/` for `central[-_ ]models`:
  only this change's own files — no earlier artefact on the topic exists.
  `plans/specs/` holds only `implementation-verification/spec.md`.
- `docs/governance/` names no model id except the regelwerk's historical entry
  on `claude-opus-4` moved to `claude-opus-5` — and the file it names,
  `templates/run-log/run-log-schema.yaml`, carries no model id today.
- `ROADMAP.md`: no theme names models or endpoints directly (one passing
  "endpoint entry" mention in a slice note).

Stage-2 call, 2026-10-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 418 files, 1129 commits, 12 rules.
```

**Notizen für die Orchestrator-Sitzung:**

- `owner:` habe ich vom Skelett-Wert `Data Architect` auf den Rollen-Schlüssel `data-architect` aus `provenance.yaml` geändert (`RB-M8`: `owner` nennt eine Rolle von dort) — Begründung steht hier, damit es der Review nicht als stille Änderung durchgeht.
- Die Stage-2-Aufrufzeile wurde unverändert aus dem Skelett übernommen.
- Nächster Schritt: Datei committen (Commit-Meldung sagt, dass der Text vom Explorer zurückkam), dann `tools/bd show coding-harness-ylu` in der schreibenden Sitzung lesen und die Interviewfragen (Phase 1a) darauf aufbauen — die erste Frage steht im Abschnitt „What is unclear".

## Drafting addendum — 2026-10-14

Read inside this worktree at `e048fa4`, branch `explore/central-models`;
the earlier explorer's returned text above is preserved.

- The five maintainer-answered records in `decisions.md` settle the source,
  generated documentation, role contracts, four consumers and repository-local
  values. `findings.md` has a draft audit line and no phase-2a rows to resolve.
- The promised `scripts/validate_change_artefacts.py` is absent. The workflow
  still describes that validator as future work. `templates/` has spec, design
  and ADR templates but no plan template; `prompts/03-plan.md` supplies its form.
- `run_codex` ignores its caller's selection and unpacks global `CODEX`;
  `run_reviewer` pins thinking to `max`. Work attempts also dispatch by tuple
  equality. Removing declarations alone would not centralize the real call.
- `stage2_session.py::cli_argv` takes an explicit model and no effort;
  `stage2.py::main` requires `session --model`. A default can be proposed by a
  read-only query without changing that safety contract. Workflow section 3
  documents native sub-agent `effort` frontmatter and reading new definitions
  only at a new session; generated agent fields can use that existing surface.
- `stage2_runs.py::routes_cleared` reads declaration text through `Source`,
  including a revision, but combines it with imported current route constants.
  The shared parser must use the same revision for both selection and clearance.
- The mechanism manifest currently treats the three stage-2 Python modules
  as inventory under its `scripts/` fallback; the export manifest carries a
  narrow core and an empty endpoint skeleton. Transferring the runner needs
  explicit dependency rules: its direct project imports are `check_adr_answers`,
  `check_frontmatter_current`, `leakcheck`, `merge_guard`, and the session module.
- No research/review swarm implementation was found in the current runner.
  The latest relevant handover records them as separate pending work and says
  the free models' terms have not been read. Empty central swarm ladders avoid
  inventing either membership or data clearance.
- The highest existing ADR number is 0017. The central role amendment changes
  no D-/O-number's contract, so the existing continuity map can remain intact.
- Tracker and current remote PR state were not read: this draft is confined
  to the worktree and git directory. `BEAD_RENDER` is not preset, and the full
  registry check would ask the renderer for tracker state outside that scope;
  the runner performs that measurement after the draft. The latest handover's
  PR statement is historical, dated 2026-10-14 11:31, not a current query.
