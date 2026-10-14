---
title: "Research — handover-currency"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ni8
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# handover currency — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md).
The runner preserved the explorer's returned text below; the draft-stage
repository gaps are appended separately. The outer provenance describes the
GLM exploration, and the addendum names its own drafting model.

Stage-2 call, 2026-10-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 418 files, 1129 commits, 12 rules.

## Runner exploration — 2026-10-14

Phase 1 für `handover-currency` ist gelaufen.** Wo wir stehen: Das Repository kennt vier Bedeutungen von „Currency" für Handovers (Kalenderalter, die nie aus `pending` bewegten Status-Felder, überholte Aussagen gegenüber Addenda, die ROADMAP-Pflicht „jede Übergabe prüft Now"), aber kein Gate misst irgendein davon — erzwungen wird nur `updated:` relativ zur letzten Änderung der Datei. Die Bead-Beschreibung (`coding-harness-ni8`) steckt im Tracker und war in dieser Phase nicht lesbar; das steht als offene Frage in der Datei. Ich habe keine Dateien verändert — der Text unten ist zum Einfügen in `plans/changes/handover-currency/research.md` (Orchestrator committet ihn unverändert).

**Vorschlag für die Datei (vollständiger Inhalt):**

```markdown
---
title: "Research — handover-currency"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ni8
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# handover currency — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md), run on
2026-10-14 in the worktree `.claude/worktrees/handover-currency` (branch
`explore/handover-currency`, tip `abe8a41`, the commit that opened this change;
`main` at `659fb35`, the merge of pull request #142, at session start). This
file collects facts about the handover subsystem; it decides nothing.

Stage-2 call, 2026-10-14: explore · attempt 1 · route flash · endpoint
glm-coding-plan · model glm-5.3-flash · leak check clean over 418 files, 1129
commits, 12 rules.

## What exists today

### The handover and its doctrine

- `docs/WORKFLOW.md`, section "The eighth movement: the session handover":
  a session ends with a file `docs/journal/handover/<date>-<name>.md` after
  [`templates/handover.md`](../../../templates/handover.md); the gate named
  there is the frontmatter check against `scripts/handover_schema.py`
  (direction, provenance and the goal's standing are required). Two doctrine
  rules: "the handover is the file, not the chat", and "every number carries
  its cut-off" — "a handover ages by design; it is appended to, never
  overwritten".
- `AGENTS.md`, house rule 5 and "Communication and session continuity": the
  same two rules, plus the duty to maintain a dated handover file before a
  session ends and to link it in the closing message.
- `ROADMAP.md`, the trial paragraph (maintainer, 2026-10-05, citing the
  research note `docs/research/2026-10-05-likec4-roadmap-arc42.md`, part B):
  "Every handover checks whether Now is still true"; the roadmap becomes a kit
  template only after it stays true through two handovers, and is removed when
  a handover finds it stale twice. This is a content-currency duty written in
  prose; no mechanism in the repository is named as carrying it.
- `tools/claude-code/skills/handover/SKILL.md` (the `/handover` skill, German):
  the writer's procedure — detect the repository's convention
  (`handover.sh where`), measure state instead of remembering it, write a file
  whose fixed section order includes `## Next step` (the section the start
  hook parses, see below), append a dated addendum when a handover on the same
  topic exists, always open a pull request, and validate with
  `python3 -m pytest tests/test_feedback_channel.py -q` before it.
- `docs/WORKFLOW.md`, section "Recurring jobs": a job prompt runs outside the
  seven phases, for no change; the first one is `prompts/research-recheck.md`.

### The corpus and its measured state

- `docs/journal/handover/` holds **34 files**, `2026-09-16-coding-harness-bootstrap.md`
  through `2026-10-14-night-run-third.md` (glob over the directory).
- All 34 files carry a top-level `status: pending` (search of `^status: ` over
  the directory: 34 matches, every value `pending`; no file carries `closed`
  or `acknowledged`). The vocabulary in `scripts/handover_schema.py`
  (`STATUS`) is pending/acknowledged/closed, and the template's direction
  table says why nothing moves: a `framework->framework` handover has a
  recipient who does nothing — "nobody waits for an acknowledgement"
  (`templates/handover.md`). The files read also carry a `review:` block with
  `status: pending`; `review` is in the schema's `OPTIONAL` set, so the tests
  do not require it, and the count of files without one was not measured.
- All 34 files carry `updated:` (search of `^updated: `: 34 matches, none
  truncated). Nine September files say `updated: 2026-09-29`; the archived
  change `plans/changes/archive/2026-09-29-frontmatter-current/` worked on
  exactly this requirement, and the `OPTIONAL` comment in
  `scripts/handover_schema.py` names it as bead coding-harness-qd7.
- Every file the (truncated) direction listing showed says
  `direction: framework->framework`; the closed set and the per-file duty are
  enforced by `tests/test_feedback_channel.py`
  (`test_every_handover_declares_a_direction`,
  `test_direction_comes_from_the_closed_set`).
- `docs/journal/_INDEX.md` (German) does **not** list the session handovers —
  it says so itself: framework handovers live in `docs/journal/handover/` and
  are checked by `tests/test_feedback_channel.py`; the index table is reserved
  for `framework->project` handovers, of which none exists yet (the test
  `test_journal_index_lists_every_open_project_handover` guards that table).

### What enforces currency today — and of which kind

- `provenance.yaml`, `paths:` list, holds the prefix `docs/journal/handover/`
  with `frontmatter: required` and allowed provenance
  `[ai-generated, ai-drafted-reviewed]`.
- The gate `frontmatter-current` (`decisions/gates.yaml`: command
  `python3 scripts/check_frontmatter_current.py`, job `verify`, enforcement
  `block`, `needs_history: true`, reason naming bead coding-harness-qd7) runs
  `scripts/check_frontmatter_current.py`. Its `findings()` reports a file
  `STALE` when its `updated:` date is **older than the file's own last
  non-merge commit** (`reference_dates()`), and `FUTURE` when later than
  tomorrow; `--stamp` repairs missing/unreadable/stale/future values. The
  enforced kind of currency is therefore *header not older than the file's
  last change* — relative, never calendar age. A handover nobody touches for
  months stays green under it.
- `scripts/stage2.py` imports `check_frontmatter_current` and stamps
  `updated:` on held files it writes, so stage-2 runs keep their own writes
  green.
- `tests/test_feedback_channel.py` validates every file in the corpus against
  the schema (common fields present, no unknown field, channel-contract fields
  only on project handovers, records immutable); `tests/test_frontmatter_current.py`
  backs the stamp gate. Neither reads a handover date against the calendar.
- **No gate names handovers or the journal**: a case-insensitive search of
  `decisions/gates.yaml` for "handover" and "journal" finds only the
  plans-hygiene title ("no one-sided handover" — that is a change's own
  `handover.md`, the stage-2 session-takeover concept, a different thing) and
  the `markdownlint` gate's exclusion `!docs/journal/**` (that gate is
  `report` anyway). The age-based shape that exists is `research-currency`
  (below), scoped to `docs/research/`. This is "not there" for anything
  *named* for handovers; a gate touching handover files under an unrelated
  name was not searched for beyond this.
- The display measures age but only shows it:
  `tools/claude-code/hooks/handover.sh` orders handovers by the date in the
  file name, then mtime (`list_handovers`), prefers the commit time for "last
  changed" (`doc_time`), shows the age in the session entry, and runs the
  safety net — a Haiku session note with a `turns_after_handover` counter for
  a session that kept working after the newest handover; notes expire after 90
  days (`find -mtime +90 -delete`). `tools/claude-code/hooks/recap.sh` updates
  the note at Stop; its own header says the note is "a safety net, never the
  handover". The entry line is consumed by the status line (comment in
  `recap.sh`; `tools/claude-code/statusline.sh` itself was not read).

### The named precedent: research-currency

- `scripts/check_research_currency.py` (docstring): lists the notes under
  `docs/research/` whose top-level `last_reviewed:` is more than
  `STALE_AFTER_DAYS = 90` days before the day of the run. "It is a report: it
  decides nothing and turns nothing red." Deterministic order, `--format json`
  for a re-check agent, a `not measured` exit when the corpus is missing.
- Its gate row (`decisions/gates.yaml`, id `research-currency`): job `drift`,
  enforcement `report`, reason: "report is the level the maintainer chose on
  2026-10-05, not a step towards block". CI runs it in the drift job
  (`.github/workflows/ci.yml`, step id `research-currency`).
- The paired job prompt `prompts/research-recheck.md` re-checks one note and
  appends a dated addendum.
- The kit carries script and test (`scripts/kit/manifest.yaml`, prefixes
  `scripts/check_research_currency.py` and `tests/test_research_currency.py`,
  reason "the gate file travels").
- The change behind it is fully documented in
  `plans/changes/research-currency/` (spec, design, plan, findings — see
  `plans/INDEX.md`); `ROADMAP.md` parks the recurring-jobs theme with research
  currency named under it (bead coding-harness-pu9).

### Open prior art inside the repository

- `docs/research/2026-09-23-obsidian-as-reader.md`, section "A machine-readable
  head for handovers": proposes `summary`, `next_step`, `needs_maintainer`,
  `blockers` frontmatter keys so a reader shows current state instead of stale
  prose — its example is a *Needed from the maintainer* entry that an addendum
  had already closed. Status there: open at `4e7ea5c`;
  `scripts/handover_schema.py` has none of these keys.
- The third night run's handover (`docs/journal/handover/2026-10-14-night-run-third.md`)
  records the adjacent exploration coding-harness-l9s (write the handover
  automatically when the usage limit reaches 95 %; a Stop hook that blocks once
  named as the only documented way). Same subsystem, its own change; the two
  have not been coordinated anywhere read.

## Where it lives

- Doctrine: `docs/WORKFLOW.md` ("The eighth movement", "Recurring jobs"),
  `AGENTS.md` (house rule 5), `ROADMAP.md` (the trial paragraph),
  `templates/handover.md`.
- Corpus: `docs/journal/handover/` (34 files), `docs/journal/_INDEX.md`.
- Schema and checks: `scripts/handover_schema.py` (the one field list —
  `GEMEINSAM`, `KANAL_EXKLUSIV`, `OPTIONAL`, `STATUS`, record markers),
  `tests/test_feedback_channel.py`, `scripts/check_frontmatter_current.py`,
  `tests/test_frontmatter_current.py`, `provenance.yaml`.
- Gates: `decisions/gates.yaml`, `scripts/ci_gates.py` (mentions
  `handover_schema.py`; the exact relation was not read),
  `.github/workflows/ci.yml`.
- Display and writer: `tools/claude-code/hooks/handover.sh`,
  `tools/claude-code/hooks/recap.sh`, `tools/claude-code/skills/handover/SKILL.md`,
  `tools/claude-code/statusline.sh` (not read), `tools/claude-code/install.sh`
  (not read — `AGENTS.md` says the display installs from there).
- Precedent: `scripts/check_research_currency.py`,
  `tests/test_research_currency.py`, `prompts/research-recheck.md`,
  `plans/changes/research-currency/`, `scripts/kit/manifest.yaml`.
- A second, different "handover" concept shares the word: the change's own
  `handover.md` that the stage-2 session takeover reads
  (`docs/WORKFLOW.md` on `stage2.py --handover`; `scripts/stage2.py`,
  `scripts/stage2_session.py`). A change about journal currency must not
  conflate the two.

## What is unclear about it

1. **The bead's own scope.** The description of coding-harness-ni8 lives in
   the tracker (`.beads/`, Dolt) and was not readable in this phase — no
   `tools/bd` here. The `plans/INDEX.md` row and the change name are the only
   in-repo statements of scope. Open until `tools/bd show coding-harness-ni8`.
2. **Which meaning of "currency" is meant.** The repository contains four
   notions and no artifact that picks one: (a) calendar age of the newest
   handover (the `last_reviewed`/90-days shape of `check_research_currency.py`),
   (b) the never-moving `status: pending` / `review: pending` lifecycle (all
   34 files), (c) body state overtaken by addenda (the Obsidian proposal's
   example), (d) the ROADMAP trial duty "every handover checks whether Now is
   still true". A `[DECISION]` for the maintainer, phase 1a.
3. **Whether session handovers' status fields are meant to leave `pending` at
   all.** The template says nobody waits for an acknowledgement on
   `framework->framework`; the schema keeps the vocabulary anyway. Measured
   fact, no rule found that ever sets another value.
4. **Level and place of any check.** The maintainer pinned research-currency
   to `report` "not a step towards block" (`decisions/gates.yaml`); no
   statement about handovers exists, and the verify/drift job choice is open.
5. **Interaction with coding-harness-l9s** (handover at 95 %): if handovers
   start being written automatically, any currency rule measures a different
   corpus. Not decided anywhere read.

## Which files a change would have to touch

A subset of these, depending on the rule chosen — listed as the subsystem's
surface, not as a design:

- `decisions/gates.yaml` (gate rows: command, job, enforcement, reason).
- A checking script under `scripts/` with its test under `tests/` — the two
  existing shapes are `scripts/check_research_currency.py` +
  `tests/test_research_currency.py` (calendar age, report) and
  `scripts/check_frontmatter_current.py` + `tests/test_frontmatter_current.py`
  (change-relative, block).
- `.github/workflows/ci.yml` and `scripts/ci_gates.py` (gate wiring).
- `scripts/handover_schema.py`, `templates/handover.md` and
  `tests/test_feedback_channel.py` together — the schema docstring states why
  the field list lives once; the test checks the template against the schema,
  and every corpus file against the schema, so a field-list change reaches all
  34 handovers.
- `provenance.yaml` (the `docs/journal/handover/` prefix is already
  `frontmatter: required`).
- `tools/claude-code/hooks/handover.sh` and
  `tools/claude-code/skills/handover/SKILL.md` (display and writer; the skill
  is the installed copy — `AGENTS.md`: change in `tools/claude-code/`, install
  with `tools/claude-code/install.sh`).
- `docs/WORKFLOW.md` ("The eighth movement", "Recurring jobs"), `ROADMAP.md`
  (the trial paragraph), `AGENTS.md` (house rule 5) — the doctrine statements
  any rule would have to agree with.
- `scripts/kit/manifest.yaml` (only if a new script travels in the kit).
- The corpus `docs/journal/handover/` itself, if a field became required
  retroactively.
```

**Nichts weiter von dir gerade** — die zwei offenen Punkte für die Folgephasen: Bead-Beschreibung lesen (`tools/bd show coding-harness-ni8`, Orchestrator), dann Interview (1a) zur Bedeutung von „Currency" mit je einer Empfehlung pro Frage.

Resume: `plans/changes/handover-currency/research.md` mit dem obigen Inhalt überschreiben (Provenance-Block ist schon gesetzt), committen auf `explore/handover-currency`, dann `tools/bd show coding-harness-ni8` für die Bead-Beschreibung vor dem Interview.

## Draft-stage repository gaps — 2026-10-14

Written by gpt-6.1-sol; read in this worktree at
`d9cbe209d3201e3ebeea35b23743ab4aae01d2dd`;
`origin/main` is locally recorded at `659fb354129589b364f2d38ded8a496d344a8a45`.
These findings extend the exploration after decisions Q-1 through Q-4 settled
the requested meaning of currency; they do not replace those answers.

- The class definitions distinguish a feature (changes the required behavior
  or its check) from an architectural change (new subsystem/interface break).
  The existing schema already owns both directions and the existing gate
  runner has block/unmeasured/history semantics (`docs/WORKFLOW.md`, "Change
  classes"; `scripts/handover_schema.py`; `decisions/gates.yaml`). No living
  capability spec matching handover currency was found under `plans/specs/`.
- There is no `templates/plan.md` or
  `scripts/validate_change_artefacts.py` in this checkout. The plan form is
  the phase-3 prompt; available artifact checks are the interview gate,
  criterion ledger and plans registry. The runner regenerates derived files
  and runs `make verify` itself (`scripts/stage2.py`, `verify_draft`).
- Adoption already belongs to the instance: the existing adoption file stays
  home while its reader travels (`scripts/adoption.py`;
  `scripts/kit/manifest.yaml`). That file records days for older changes,
  not historical handover bodies. A backdated header alone cannot distinguish
  a newly created handover from the legacy corpus.
- The current authoring skill appends dated addenda, and its first three
  sections carry the next session's entry; the latest handover also uses the
  older `## Addendum <date>` form (`tools/claude-code/skills/handover/SKILL.md`;
  `docs/journal/handover/2026-10-14-night-run-third.md`). New session evidence
  must cover addenda without retroactively completing earlier bodies.
- The kit roles and export verdicts are different maps: schema and feedback
  tests are mechanism, but the export's default drops the schema. A new
  exported checker importing it needs an explicit export dependency entry
  (`scripts/kit/manifest.yaml`; `scripts/export/manifest.yaml`).
- The latest relevant handover's addendum says no PR was open at its
  2026-10-14 11:31 cut-off. Current remote PR state, tracker status, parallel
  sessions outside this worktree and private vault contents were not read:
  this runner draft is restricted to the worktree and repository git directory.
  The vault registration and known project-note locator are interviewer
  evidence in decisions Q-1; resolving the live registration is an authoring
  lookup for the orchestrator, not a new interview or a guessed implementation.
