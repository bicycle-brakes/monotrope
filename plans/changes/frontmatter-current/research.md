---
title: "Research — frontmatter-current"
status: draft
implementation_status: none
date: 2026-09-29
last_reviewed: 2026-09-29
supersedes: null
superseded_by: null
bead: coding-harness-qd7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# frontmatter-current — Research

## Question

Implement a mechanism to track when a document's content last changed, distinct from when it was last reviewed. Add an `updated:` field to frontmatter, fail CI when it is older than the file's last commit, and provide a command to stamp dates automatically.

Which existing checks validate frontmatter, how is CI structured, and what infrastructure exists today to support this?

## What was measured

**Frontmatter validators**

- `scripts/check_docs.py` (lines 27–39): Defines PFlicht (required keys when frontmatter exists):
  - title, category, status, created, last_reviewed, owner, provenance, produced_by, review, tags
  - No `updated` field today
  - Runs via `python3 scripts/check_docs.py --base docs`

- `scripts/plans_registry.py` (lines 40–43, 305–322): 
  - REQUIRED fields for plans/: status, implementation_status, date, last_reviewed, bead
  - STALE_AFTER_DAYS = 90 (line 43)
  - Staleness check: `_age_days()` parses date strings, drifts if age > 90 days and not archived (lines 305–313)
  - Runs via `python3 scripts/plans_registry.py --check`

- `scripts/handover_schema.py` (lines 32–98): Defines handover frontmatter structure (GEMEINSAM, KANAL_EXKLUSIV, OPTIONAL)
  - Not relevant to docs frontmatter, but shows schema pattern used in this codebase

**CI and verify setup**

- `.github/workflows/ci.yml` (generated from decisions/gates.yaml per line 3):
  - Runs `scripts/plans_registry.py --check` (line 75)
  - Runs `scripts/check_docs.py` (line 79)
  - Shallow checkout: `actions/checkout@v4` with default fetch-depth (appears to be full history based on later git operations)

- `Makefile`: `make verify` → `bash scripts/verify_all.sh`

- `scripts/verify_all.sh` (lines 49–72): Reads decisions/gates.yaml via `ci_gates.py --commands`, runs TSV-formatted commands, only `block` enforcement fails the run

**Frontmatter count (measured at branch feat/frontmatter-current)**

Command used: Python scan of rglob('*.md') looking for `---\n...\n---\n` pattern

| Directory | With frontmatter | Without | Total | Notes |
|-----------|------------------|---------|-------|-------|
| docs/     | 30               | 7       | 37    | Includes prompts/, which exempt from requirement |
| plans/    | 10               | 1       | 11    | INDEX.md generated, excluded |
| prompts/  | 0                | 9       | 9     | Instruction files, exempt per task description |

Frontmatter fields (docs/ with FM=30):
- `last_reviewed`: 21/30 
- `created`: 30/30
- `updated`: 0/30

**Last content-changing commit dates**

Command: `git log -1 --format=%cs -- <file>`

Measured on three files:
- `docs/WORKFLOW.md`: 2026-09-22
- `docs/WORKFLOW.md`, `docs/AGENTS.md`, `docs/README.md` in same commit (2026-09-22 05fb0d3)
- Files untracked in this worktree return empty (e.g., plans/changes/frontmatter-current/research.md)

Edge cases observed:
- Untracked files: `git log` returns empty output (edge case for automation)
- Files changed in working tree but not committed: `git log` shows last committed date, not working-tree change
- Shallow clones: not present in this repo (full history observed)

**Make targets and hooks**

- `Makefile`: verify, test, staleness, gates, leakcheck
- `.claude/settings.json`: One SessionStart hook (bd prime). No PostToolUse hook for auto-stamping.

**Provenance map: coding-harness vs. lakeswitch-ai**

Coding Harness: No decisions/provenance.yaml file exists.

Lakeswitch-ai `decisions/provenance.yaml` (lines 46–110):
- `frontmatter: required` for: decisions/, spec/, prompts/, plans/, docs/, docs/adr/, docs/research/
- `frontmatter: none` for: rendered/, examples/, journal/, src/, tests/, plugin/, .github/
- Only validation: `provenance` field must match allowed classes per prefix
- No schema for additional fields (e.g., `created`, `last_reviewed`, `updated`)

## What exists

1. **Two independent frontmatter checks** (check_docs.py for docs/, plans_registry.py for plans/), each enforcing different required keys—they must be unified or aligned

2. **Staleness detection** already works in plans_registry.py via date parsing and age threshold (line 43)—pattern can be reused

3. **CI structure** delegates to decisions/gates.yaml; adding a new check requires editing that file (per Makefile comment, lines 1–9)

4. **No schema file** defines frontmatter fields across the repository; checks hardcode lists (PFlicht, REQUIRED)

5. **No auto-stamp mechanism** in hooks; PostToolUse hook does not exist (could be added to .claude/settings.json)

6. **Git date retrieval** is straightforward (`git log -1 --format=%cs`), but untracked files and working-tree changes need handling

## Risks and edge cases

1. **Merges and renames**: `git log` sees the commit that moved or renamed a file, not necessarily the one that changed content. Renames on the same file can make the "last change" hard to interpret.

2. **Untracked files** in CI (e.g., during a fresh branch): `git log` returns empty, so automation must handle that case or the check fails opaquely.

3. **Shallow clones**: This repo appears to use full history, but shallow clones (fetch-depth < history) can make `git log` incomplete. CI workflow should verify depth.

4. **File changed in working tree but not committed**: `updated:` would stale if stamped only on commit. An auto-stamp hook on edit would help, but hooks depend on editor integration (PostToolUse covers Claude, not other editors).

5. **Multiple frontmatter validators** (check_docs.py, plans_registry.py, lakeswitch-ai's provenance.py) each re-parse YAML and define required keys separately—adding `updated:` to one but not all creates inconsistency.

## Corrections after verification (orchestrating session, 2026-09-29)

The phase-1 run was checked against the tree at `9f14283`. Three findings above
are wrong and one is incomplete; where they disagree, this section holds.

1. **The provenance map exists and already declares frontmatter per prefix.**
   It is the root file `provenance.yaml`, not `decisions/provenance.yaml`. Each
   `paths:` entry carries `frontmatter: required | optional | none`, longest
   prefix wins, and its comment defines the three values (`required`: a file
   without frontmatter is a BLOCK; `optional`: classification not yet done;
   `none`: none belongs here). `docs/WORKFLOW.md`, `plans/` and
   `docs/journal/handover/` are `required`; `docs/adr/`, `docs/how-to/` and
   `docs/governance/` are `optional`; `prompts/`, `templates/`, `AGENTS.md`,
   `README.md`, `.github/` are `none`.
2. **Nothing reads that field today.** The comment names
   `scripts/validate_provenance.py`; the script is not in the tree
   (`ls scripts`). The files that mention `provenance.yaml` are
   `scripts/ramp_valves.py`, `scripts/new_change.py`, the two manifests and
   `tests/test_feedback_channel.py`; none enforces `frontmatter:`. The map is
   declared, not enforced. Many of its prefixes (`docs/vertrieb/`,
   `docs/konzept/`, `docs/lessons/` …) come from the origin repository and
   name directories that do not exist here.
3. **The CI checkout is shallow.** Both `actions/checkout@v4` steps in
   `.github/workflows/ci.yml` set no `fetch-depth`, and the action's default is
   1. With one commit of history, `git log -1 -- <file>` returns the checked-out
   commit for every file — on a pull request, GitHub's merge commit, dated
   today. A check against git dates needs `fetch-depth: 0` (or a deepen step) in
   the job that runs it. The earlier line "full history observed" was measured
   in a local clone, not in CI.
4. **The one gate list is `decisions/gates.yaml`** (D-10); `ci.yml` is
   generated from it by `scripts/ci_gates.py --generate-ci`, and a hand edit
   fails the `ci-drift` gate. A new check is a new entry there, then
   regeneration. (`docs/WORKFLOW.md` §3 still calls `ci.yml` the one list; that
   sentence is out of date — noted for pull request 49, not this change.)
5. **`check_docs.py` runs as `report`, not `block`** (gate `docs-links`), until
   bead coding-harness-bt8 clears 35 measured corpus findings.

## Open points

- [DECISION] Should `updated:` be required in all frontmatter or only in specific prefixes? Task says "docs/, docs/adr/, plans/changes/" explicitly, but check_docs.py runs on "docs/ recursively"—does that include subdirs like docs/adr/?

- [GAP] No unified frontmatter schema file exists (like lakeswitch-ai will need). Where should the schema live: decisions/gates.yaml, a new checks config, or inline in each validator?

- [DETAIL] Should `updated:` track content-only changes or also metadata (frontmatter) changes? How does "last content change" differ from "last edit"?

- [DETAIL] Auto-stamp implementation: Should this be a PostToolUse hook (Claude Code only), a Git pre-commit hook (all editors), or a CI stamp-on-merge step?

- [DETAIL] How to handle untracked files in CI without breaking the build? Should CI skip the age check if the file is untracked, or treat it as always-current?

## Addendum — measured in phase 2 (spec session, 2026-09-29)

The gaps the spec needed, measured on `9f14283` plus this change folder. The
open points above are settled in `spec.md` ("Open decisions").

1. **Held set under the proposed map: 47 Markdown files** (45 tracked, plus
   `research.md` and `decisions.md` of this folder): `docs/WORKFLOW.md` 1,
   `docs/adr/` 6, `docs/architecture/` 4, `docs/governance/` 2, `docs/how-to/`
   1, `docs/journal/handover/` 9, `docs/research/` 13, `plans/_README.md` 1,
   `plans/changes/` 10. Throwaway count script over
   `git ls-files --cached --others --exclude-standard`, longest prefix,
   `excluded:` honoured.
2. **The six ADRs carry no frontmatter.** Their metadata is a bullet list in
   the body (`Status`, `Review`, `Date`).
3. **`docs/architecture/` and `docs/research/` have no entry in
   `provenance.yaml`.** All 17 files there carry frontmatter, every one with
   `provenance: ai-drafted-reviewed`.
4. **`.claude/agents/` is `required` in the map** (7 files, frontmatter read
   by Claude Code), which contradicts decisions item 3. `.claude/commands/` is
   already `none`.
5. **After the five prefix changes no `optional` file carries frontmatter**
   (`docs/journal/_INDEX.md`, the one remaining optional file, has none).
6. **No gate can ask for history today.** `scripts/ci_gates.py::generate_ci`
   writes `- uses: actions/checkout@v4` without `with:` in both jobs.
7. **The handover field set is closed.** `scripts/handover_schema.py::ERLAUBT`
   has no `updated`; `tests/test_feedback_channel.py` fails on any handover
   that carries an unknown field, and on a template block that names one.
8. **Three writers create held headers:** `scripts/new_change.py`
   (`_frontmatter_template`), `templates/handover.md` (Variante A) and
   `tools/claude-code/skills/uebergabe/SKILL.md` (§3a).
9. **Kit.** Every gate's script is `mechanismus` in `scripts/kit/manifest.yaml`.
   The kit probe copies the `mechanismus` files into a fresh repository with
   one commit and runs `pytest` there; `REIST_NICHT` holds 31 entries at
   `DECKEL = 31`, so a new test that is red in that copy has no room.
10. **Ratchets in `tests/test_ci.py` a new gate meets:** a mutation test (a
    test name from `MUTATIONS_NAMEN` in a file that contains the script's file
    name), a test and a caller for every script.
11. **Accepted ADRs and signatures.** Since 2026-09-23 every change to an
    accepted ADR file reached `main` together with the maintainer's
    Touch-ID-signed acceptance commit of a new ADR (`0ddb9aa` → `8fc92e4`,
    `3d7eb02`); no change to an accepted ADR stood on its own. Whether
    coding-harness adopts the signed-decision rule is open
    (`docs/how-to/signed-decisions.md`, "Open").
12. **Merges.** The last six merges on `main` are merge commits
    ("Merge pull request #43" … "#48"). GitHub's allowed merge methods and
    whether `verify` is a required status check were **not read**: the
    `gh api` call needs an approval this session does not have.
13. **`check_docs.py` baseline:** 45 findings, 22 of them "Frontmatter ohne",
    none under `docs/adr/` (2026-09-29, `9f14283` plus worktree).
14. **The phase gate `scripts/validate_change_artefacts.py`** named in
    `prompts/02-spec.md` and `prompts/03-plan.md` does not exist in this tree;
    `python3 scripts/plans_registry.py --check` is the validator that runs.
15. **git behaviour the spec relies on** — default history simplification
    follows the parent a merge is identical to, `--no-merges` drops merge
    commits, a path-limited log shows a rename as a change at the new path,
    `%cs` prints the date in the commit's own offset — is git's documented
    behaviour. A throwaway measurement could not run in this session (the
    command needed an approval); the plan's tests measure each case.
