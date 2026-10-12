---
title: "Research — provenance-location"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-3ar.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, adr-answers, provenance, kit]
---

# Provenance location for instances — Research

Phase 1 for bead coding-harness-3ar.1, read against `origin/main` on
2026-10-12. Package 1 of `docs/research/2026-10-11-adr-answer-pin-plan.md`
(row 7, the Coding Harness half): the Coding Harness command reads a root
`provenance.yaml` with `roles:`; LakeSwitch keeps `decisions/provenance.yaml`
without `roles:`, so the command refuses there. Coding Harness lets an
instance name where its provenance file lives; the default stays unchanged.
The package touches only `scripts/check_adr_answers.py`, `scripts/harness.py`
and their tests.

## Questions for the exploration

1. Where and how do `scripts/check_adr_answers.py` and `scripts/harness.py`
   (verb `decide adr`) find and read `provenance.yaml` today: path
   resolution, the `roles:` lookup, what they do when the file or `roles:`
   is missing, and which tests pin that.
2. Which ways exist in this repository for an instance to name a location
   (a command-line option, an environment variable, a key in a config file
   such as `model-endpoints.yaml` or the kit manifest), and which one other
   scripts already use, so the change follows the existing idiom.
3. Which other readers of `provenance.yaml` exist (gates, kit scripts,
   `scripts/kit/manifest.yaml`), so a change knows what stays on the default.
4. What the kit carries of these two scripts to an instance, and what an
   instance run would need to pass the new location.

The interview (phase 1a) needs the maintainer; this file stops before it.

Stage-2 call, 2026-10-12: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 347 files, 861 commits, 12 rules.

## Runner exploration — 2026-10-12

*Note by the orchestrating session (2026-10-12): GLM's answer opened with a German preamble, a German summary and a code fence around the findings; all three were removed (house rule 1). The summary said: the map is read today at exactly one place (`harness.py`, `answering_role`, constant `PROVENANCE = "provenance.yaml"`, `root / PROVENANCE`); `check_adr_answers.py` never opens it; three other scripts read the same file at fixed root paths; the map's header comment names two readers that do not exist (in that form) today. German inside the findings below is quoted from existing files. The text below the heading is unchanged.*

## Findings

### The one read site of the map (question 1)

`scripts/check_adr_answers.py` never opens the map: a case-insensitive search
over `scripts/` for "provenance" returns no hit in that file. Its only constant
that couples it to the map is `ANSWERS_DIR = "decisions/answers"`; its docstring
calls the module "the one reader of the format" — of the answer format, not of
the map. The gate runs without arguments (`decisions/gates.yaml`, entry
`adr-answers`: `command: python3 scripts/check_adr_answers.py`, `job: verify`,
`enforcement: block`); `make verify` delegates to `scripts/verify_all.sh`, and
the Makefile header comment says the verify commands live in ONE place,
`decisions/gates.yaml`, with the runner asking `scripts/ci_gates.py`.

`scripts/harness.py` holds the map name once, as the module constant
`PROVENANCE = "provenance.yaml"` — a bare filename beside `MESSAGE_FILE`. The
only read site is `answering_role(root)`: it builds `path = root / PROVENANCE`
and reads it with `yaml.safe_load(path.read_text(encoding="utf-8"))`. The
refusal ladder, in order: unreadable file (`OSError` or `yaml.YAMLError`) →
`Refused`; document not a mapping → `Refused`; no `paths:` entry whose `prefix`
equals `ANSWERS_PREFIX` (`f"{gate.ANSWERS_DIR}/"`, i.e. `decisions/answers/`) →
`Refused`; the first matching entry without a non-blank `owner_role:` →
`Refused`; `roles:` missing, not a mapping, or without the named role →
`Refused` ("names no role under `roles:`"). Two entries with the same prefix
are not refused — the code takes `entries[0]`. Several refusal texts embed the
literal file name and a proposed entry text, so the name shows in the command's
output.

`main()` resolves `root` from the `--root` option (default `REPO_ROOT =
Path(__file__).resolve().parent.parent`) and calls `answering_role(root)` on
every run, before `message_path(root)` — in the interactive ask flow and in the
record flow alike.

The pinning tests are `tests/test_harness_decide_adr.py`, criterion 10 block:
`test_answered_by_is_the_role_the_map_names` (the `MAP` fixture with the role
renamed; asserts `harness.answering_role(repo)` and the `answered_by` written
into the answer files), the parametrized
`test_a_map_without_the_role_refuses_before_asking` (four cases — "no map"
(`map_text=None`), "no entry", "no owner_role", "role not declared" — each
expects exit 2 and nothing written), and
`test_this_repository_declares_the_answering_role`, which asserts
`answering_role(REPO_ROOT) == "framework-architect"` and opens
`REPO_ROOT / "provenance.yaml"` itself, asserting the `decisions/answers/`
entry holds `allowed: [human-decided]` and `frontmatter: none`. Every other
test builds its own tree through `_repo(tmp_path, ..., map_text=MAP)`; the
`MAP` text carries `roles:` with one role (`decider`, `handle: "@someone"`, no
`identities:`) and the `decisions/answers/` entry with `owner_role: decider` —
the command checks presence of the role key under `roles:`, not its shape.

### Ways this repository already names a location (question 2)

Three idioms exist; none of them names the map today.

- A command-line option naming the tree, not a file: `--root` on
  `harness.py decide adr` and on `check_adr_answers.py`, each defaulting to
  this repository.
- An environment variable carrying a path over a built-in default, read at
  call time ("Read at call time, never at import"): `LEAKCHECK_DENYLIST` in
  `scripts/leakcheck.py` `default_denylist()` (default
  `~/.config/cc-routing/denylist.txt`), `CC_SECRETS` in `scripts/stage2.py`
  `secrets_path()` (default `~/.config/cc-routing/secrets.env`), and the
  render-path variable of `scripts/bead_render.py` `render_pfad()`
  (`UMGEBUNGS_RENDER`; the `BEAD_RENDER` preset of the tracker render
  contract) — there, a preset path whose file is missing is a hard error, not
  a fall-back.
- A config file naming what to run, not where a file lives:
  `decisions/gates.yaml` carries `command:` keys (the `adr-answers` entry
  names `python3 scripts/check_adr_answers.py`).

A config-file key naming another file's location is not in the repository:
`model-endpoints.yaml` is read everywhere at the hardcoded
`root / "model-endpoints.yaml"` (`scripts/stage2.py` in the declaration check
and the `opencode-go` lookup, `scripts/stage2_session.py` in the endpoints
loader, `scripts/stage2_runs.py` in the declaration mutation). The two
manifests name prefixes with a role or a verdict and are not instance-side
overrides; `scripts/export/manifest.yaml` (its line for `provenance.yaml`:
`verdict: carry`) has no reader at all — its only mentions are comments in
`scripts/kit/manifest.yaml`, and the pin plan states the same
(docs/research/2026-10-11-adr-answer-pin-plan.md, "As-is" row).

### Every reader of the map (question 3)

Three scripts read it directly, each a different part; a fourth reads it
through the first.

- `scripts/check_frontmatter_current.py` `load_map(root)`:
  `root / "provenance.yaml"`, `yaml.safe_load`, returns `paths:` and
  `excluded:`; `is_held()` applies the longest matching `prefix` and holds
  `frontmatter: required`. A missing `paths:` list is `CannotMeasure`.
- `scripts/ramp_valves.py` `_roster_handles()`: `REPO_ROOT /
  "provenance.yaml"`; a missing file silently yields an empty set; it reads
  the `handle:` of each entry under `roles:` for the
  `provenance-review` valve.
- `scripts/harness.py` `answering_role()`: the `decisions/answers/` entry and
  `roles:` (question 1).
- `scripts/stage2.py` reads it indirectly: it imports
  `check_frontmatter_current` and, in its derived-file preparation, calls
  `check_frontmatter_current.load_map(root)` and `is_held(...)`, raising
  `check_frontmatter_current.CannotMeasure` when an entry is not a mapping
  with a string prefix.

Named but absent — the header comment of `provenance.yaml` says the file
"wird von `scripts/validate_provenance.py` gelesen und von
`tests/test_provenance.py` geprueft":

- `scripts/validate_provenance.py` is not there — no file matches
  `scripts/validate_provenance*`.
- `tests/test_provenance.py` is there, but never reads the map: it holds the
  RB-P5 journal-date-citation test, imports neither yaml nor the map name.
- The valve table of `scripts/ramp_valves.py` cites
  `tests/test_provenance.py::test_owner_is_a_role_not_a_person`,
  `::test_every_in_scope_file_declares_a_class` and
  `::test_every_docs_page_declares_a_doc_type`; none of the three names
  exists anywhere under `tests/` (case-sensitive search: no matches).

Test files that build their own map fixtures, and thereby pin the map's
location and shape for the readers above: `tests/test_harness_decide_adr.py`
(`_repo(..., map_text=MAP)` writes `provenance.yaml` at the tree's top),
`tests/test_frontmatter_current.py` (its
`test_a_root_below_the_top_of_the_repository_sees_its_own_edits` points the
check at a subdirectory and writes the map as `sub/provenance.yaml` — the map
is expected directly under whatever root a reader is given), and
`tests/test_stage2.py` (map fixtures for the derived-file preparation;
`test_malformed_provenance_returns_preparation_diagnostics` asserts the
diagnostics name "provenance").

Non-reading dependents that carry the file's name in text: the header comment
of `provenance.yaml` itself (its "Readers in this repository" list), the
house rule on decision pull requests in `AGENTS.md`, the matching paragraph
of `docs/WORKFLOW.md`, `prompts/07-commit.md`, the templates (`templates/
spec.md`, `adr.md`, `design.md`, `findings.md`, `arc42.md`, `handover.md`,
each citing the map's prefix rules for frontmatter), and
`scripts/new_change.py` (help text and generated comment). `.github/`
contains no occurrence of "provenance" (case-insensitive search: no matches)
— CI touches the map only through the gate commands. The real map carries
`owner_role: framework-architect` on the `decisions/answers/` entry and four
roles (`data-architect`, `framework-architect`, `data-product-owner`,
`operations-owner`) under `roles:`. This repository has the map only at the
root — no `decisions/provenance.yaml` exists (glob over the tree; the change
`harness-decide-adr` states the same in its `plan.md`).

### What the kit carries and what an instance run needs (question 4)

`scripts/kit/manifest.yaml` carries, all `rolle: mechanismus` ("traegt den
Ablauf und laeuft in einem fremden Repo unveraendert"):
`scripts/check_adr_answers.py` ("the check behind the gate adr-answers — the
gate file travels, so its script does"), `scripts/harness.py` ("the command
the gate's finding names"), `tests/test_check_adr_answers.py` and
`tests/test_harness_decide_adr.py` (each "builds its own trees; holds in the
probe copy"), `decisions/` ("die eine Gate-Liste ... reist mit — im Zielrepo
gilt dieselbe Datei"), `.github/workflows/ci.yml` (paired with
`decisions/gates.yaml`), and `provenance.yaml` itself ("die
Provenienzklassen. Das Vokabular reist, die Pfadzuordnung ist zu pruefen").
`geruest_ordner:` requires `plans/changes`, `plans/changes/archive` and
`plans/specs` to exist empty in the target. The probe
`scripts/kit/probe.py` never mentions `provenance.yaml` — the map is not
special-cased on the run. `tests/test_harness_decide_adr.py`'s docstring
states the coupling as intended: "The one file of this repository read is
`provenance.yaml`, which travels with the kit."

An instance run therefore needs, today: a readable `provenance.yaml` directly
under the tree the command is given, holding a `paths:` entry with
`prefix: "decisions/answers/"` and `owner_role:`, and a `roles:` mapping that
contains that role. The pin plan records LakeSwitch's as-is as
`decisions/provenance.yaml` without `roles:`, so the command refuses there
unchanged, and states the migration step as "Coding Harness lets an instance
name where its provenance file lives (default unchanged); LakeSwitch adds
`roles:`" (docs/research/2026-10-11-adr-answer-pin-plan.md, differences table
row 7). The same plan bounds package 1 to "touches only
`scripts/check_adr_answers.py`, `scripts/harness.py` and their tests" (work
packages, package 1); it says nothing about the other readers.

## What is unclear

- The header comment of `provenance.yaml` names two readers that do not hold
  today (`scripts/validate_provenance.py` is not there;
  `tests/test_provenance.py` exists but never reads the map). Which side is
  stale — comment or readers — is not decided here.
- The valve table of `scripts/ramp_valves.py` cites three test names that
  exist nowhere under `tests/`; whether those valves still measure anything
  is a runtime question this exploration did not run.
- Whether a relocated map should also be found by the other readers
  (`check_frontmatter_current.py`, `ramp_valves.py`, `stage2.py` through the
  first) is stated nowhere in the repository; the package names only the two
  scripts.

## Files a change would have to touch

Per the package statement (docs/research/2026-10-11-adr-answer-pin-plan.md,
package 1) and the read sites above:

- `scripts/harness.py` — the `PROVENANCE` constant, `answering_role()` (the
  only read site, its refusal texts, the `entries[0]` take), the `decide adr`
  parser (a `--root` option exists already).
- `scripts/check_adr_answers.py` — no map read site today; named by the
  package statement anyway.
- `tests/test_harness_decide_adr.py` — the `MAP` fixture,
  `_repo(map_text=...)`, the criterion-10 tests, and
  `test_this_repository_declares_the_answering_role`, which opens
  `REPO_ROOT / "provenance.yaml"` directly.
- `tests/test_check_adr_answers.py` — named by the package statement ("and
  their tests"); the only "provenance" in it is a fixture frontmatter value,
  so it pins nothing about the map.

Readers outside the package statement, listed because they open the same
file: `scripts/check_frontmatter_current.py` (`load_map`),
`scripts/ramp_valves.py` (`_roster_handles`), `scripts/stage2.py` (through
`check_frontmatter_current.load_map`), plus the three test files that build
map fixtures (`tests/test_frontmatter_current.py`,
`tests/test_stage2.py`, and the harness test above).

**Wo wir sind:** Phase 1 (Explore) für `provenance-location` ist inhaltlich abgeschlossen; der Befundstext oben ist unverändert in `research.md` zu übernehmen (mit `updated:` bleibt 2026-10-12). **Nächster Schritt:** Commit des Artefakts, dann Phase 1a (Interview) mit Ihnen — dort gehören die offenen Fragen hin (v. a. ob die Karten-Kopfzeilen-Leser stale sind und ob andere Leser einem umgezogenen Pfad folgen). **Von Ihnen benötige ich gerade:** nichts.
