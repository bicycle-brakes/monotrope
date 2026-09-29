---
title: "Findings — frontmatter-current"
category: findings
status: draft
implementation_status: none
date: 2026-09-29
last_reviewed: 2026-09-29
updated: 2026-09-29
supersedes: null
superseded_by: null
bead: coding-harness-qd7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings]
---

# Findings — frontmatter-current

Phase 6, round 1, on commit `e553bc8` (nine commits ahead of `origin/main`
at `1a6aff8`), reviewed in a fresh context against `spec.md`; `decisions.md`
and the "Implementation notes" of `plan.md` were read and not reopened. The
reviewer wrote nothing but this file.

Verdict: **no open BLOCKER, no `[AMBIGUITY]`, no `[DIVERGENT]`.** One MAJOR,
seven MINOR. Ready for a pull request; the MAJOR is a disagreement with a
`[DETAIL]` of the spec and is recorded for the maintainer, not resolved here.

Measured on 2026-09-29 in the worktree: `python3 -m pytest -q` 346 passed,
15 skipped; `python3 scripts/check_frontmatter_current.py` exit 0, 49 held
documents; `python3 scripts/ci_gates.py --check-ci` "ci.yml ist genau die
Ableitung der Gate-Datei"; `--check-schema` 16 gates ok;
`python3 scripts/check_docs.py` 22 "Frontmatter ohne" findings, none under
`docs/adr/` (baseline 22). The `verify` job's checkout carries
`fetch-depth: 0`, the `drift` job's does not.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | MAJOR | MAINT | base | `docs/adr/0001-early-parallelism.md`, frontmatter `status:` and `review:` (same pattern in ADRs 0002 and 0005) | The new header says `status: accepted` while the body's Status line says the ADR is superseded by ADR 0006 as a whole (0002 and 0005: superseded in part), and `review: {status: pending}` while the body records acceptance by the maintainer, for 0004 to 0006 in a Touch-ID-signed commit. A reader of the header alone believes ADR 0001 is in force and unreviewed. The values follow the spec's `[DETAIL]` "ADR header values restate the ADR" (Status line begins with "accepted"; `review: pending` because an agent may not write an approval name, rule RB-M2), so the code meets the spec; the disagreement is with that detail, and it is recorded, not resolved. `superseded` is a value this repository already uses for `status:` (`plans/_README.md`). Not `[DIVERGENT]`: the body's own Status line carries both words. | fixed in 0f4101f |
| F-2 | MINOR | SPEC | base | criterion 7, last sentence: hosted CI on the pull request | The gate has not run in hosted CI: no pull request exists yet, so "on the pull request that introduces the gate, hosted CI runs it green" is unverified. Locally the gate is green and the `verify` checkout has `fetch-depth: 0`; the hosted checkout of a pull request is GitHub's merge commit, which `--no-merges` skips (criterion 3). Closes itself when the pull request's `verify` job is green. [criterion 7] | open |
| F-3 | MINOR | MAINT | base | `scripts/check_frontmatter_current.py`, `run` | A map in which no `required` prefix matches any file passes green: "0 held documents, every `updated:` is current", exit 0. Reproduced in a temporary repository with `paths: [{prefix: "nothing/", frontmatter: required}]`. A gate over an empty set cannot bite; `check_docs.py` refuses the same situation ("die Pruefung misst nichts"). Today 49 files are held and the map travels with the kit, so the case needs a map edit that drops every `required` prefix. Criterion 4 says "exit 0 when nothing is reported", so this is spec-conformant. | fixed in 107600e |
| F-4 | MINOR | MAINT | base | `scripts/check_frontmatter_current.py`, `_BLOCK`, `read_updated`, `stamp` | A held file whose header uses CRLF line endings or starts with a UTF-8 byte-order mark is reported as `no-frontmatter` (the block pattern requires `---\n` at byte 0), so a file that plainly carries a header gets a message that says it has none, and the stamp leaves it alone. A held file with invalid UTF-8 in its body is read by the check with replacement characters but crashes the stamp with a `UnicodeDecodeError` traceback instead of a named finding. Reproduced in a temporary repository. `check_docs.py` has the same CRLF and BOM blind spot; no file in this tree hits either case (measured 2026-09-29). | fixed in 107600e |
| F-5 | MINOR | MAINT | base | `scripts/check_frontmatter_current.py`, `preflight` | The shallow test reads `git rev-parse --is-shallow-repository` and only compares stdout with `true`; the return code is not checked. On a git that lacks the flag (older than 2.15, 2017) the command fails, stdout is not `true`, and a shallow clone is measured as if it were full: every clean file gets the checked-out commit's date, and a stale header can pass. Fails open only on a git no supported runner ships; `ubuntu-latest` and this machine (2.55.0) have the flag. [criterion 4] | fixed in 107600e |
| F-6 | MINOR | MAINT | base | `scripts/check_frontmatter_current.py`, `reference_dates`; `tests/test_frontmatter_current.py` | The `--relative` flag on `git diff` (implementation note 4, added beyond the plan) has no test: with the flag removed in a scratch copy every test stays green, because no test points `--root` at a subdirectory of a repository. Of 23 faults planted in scratch copies, 21 went red; this one and "no-commit refusal removed" stayed green, the latter harmlessly (the run still exits 3 because `git diff HEAD` fails without a commit). | fixed in 751c105 |
| F-7 | MINOR | MAINT | base | `provenance.yaml`, the header comment added 2026-09-29 | The comment says "the one script that reads this map here is `scripts/check_frontmatter_current.py`". `scripts/ramp_valves.py` also reads `provenance.yaml` (its `roles:` roster). The sentence is true of `paths:` and `excluded:` and false of the file; a reader who edits `roles:` will not expect a second reader. | fixed in 4a3911a |
| F-8 | MINOR | MAINT | base | `scripts/check_frontmatter_current.py`, `_VALUE` | A value with a trailing YAML comment (`updated: 2026-09-10  # stamped`) is reported `unreadable`, although YAML reads it as the date. The stamp repairs it and the message names the fix, so nothing is lost; noted because criterion 2 says "a value that is not a `YYYY-MM-DD` date" and this one is. | fixed in 107600e |

## Checked without a finding

- **Criterion 1** (held files from the map): `held_files` and `is_held`
  against a temporary map with nested `required`/`optional`/`required`
  prefixes, an excluded prefix, a `none` prefix, an unmapped path, an ignored
  file, a deleted tracked file and a non-Markdown file. Planted: `optional`
  held, exclusion ignored, shorter prefix winning — all red. The real map:
  49 held; every unheld Markdown file with frontmatter is under
  `.claude/agents/`, `.agents/skills/` or `tools/claude-code/skills/`
  (harness configuration, decisions item 3).
- **Criterion 2**: no block, no line, two lines, `soon`, `2026-02-30`, an
  indented `updated:`, quoted and unquoted dates; the future bound at UTC
  today plus one day (tomorrow passes, the day after is reported). Planted:
  stale check off, bound at plus two, loose value regex — all red.
- **Criterion 3**: committer date, not author date (planted `%as` — red);
  `git mv` a day after the stamp is reported; a `--no-ff` merge days later
  dates nothing and a file changed on both sides takes the newer side
  (planted `--no-merges` dropped — red); a commit at 23:30 −05:00 is that
  local day; modified, staged and untracked files are held against today
  (planted each — red). A stamp of the 20th under a commit at 00:30 UTC on
  the 21st is reported, as the spec's timezone detail says. Git's default
  history simplification at GitHub's pull-request merge commit follows the
  side the file is identical to, so a file changed on the branch only is
  dated by the branch's commit.
- **Criterion 4**: exit 3 for a `--depth 1` clone with `fetch-depth: 0` and
  `needs_history` in the message, for a plain directory, a repository without
  a commit and an unparsable map; exit 1 with path, kind, both dates and the
  fix line verbatim through the real command line. Planted: fix line
  missing, exit 0 on findings — red. `NOT MEASURED` goes to stderr with a
  non-zero exit, which `verify_all.sh` treats as red.
- **Criterion 5**: byte comparison of a header with a comment, a flow mapping,
  a quoted value with trailing spaces, CRLF and umlauts in the body; insertion
  directly after `last_reviewed:`, else as the last line of the block; a
  second run rewrites nothing (planted "rewrite unchanged" — red); no header
  invented, a duplicate left alone, exit 1 with such a file (planted — red).
  The first stamp on this tree added exactly one line to each of 49 files
  (`git show --stat e553bc8`, 49 files, plus the notes in `plan.md`).
- **Criterion 6**: `decisions/gates.yaml` carries the gate with the exact
  command, job, enforcement, placement and `needs_history: true`; the
  generator gives `fetch-depth: 0` to the `verify` checkout only; `ci.yml` is
  byte-identical to the derivation (`--check-ci` green, so it was
  regenerated, not hand-edited); `needs_history: "yes"` is a schema error.
  Planted: full checkout everywhere, validation off, `gates()` dropping the
  field — all red.
- **Criterion 7**: the five prefix changes are in the map and
  `.claude/agents/` is `none`; the six ADR headers carry every key
  `check_docs.py` requires, with `title` equal to the heading, `created` and
  `last_reviewed` equal to the Date line's first and accepted dates,
  `produced_by.version` equal to `created`; `framework-architect` is the
  owner already used by 18 research and architecture documents. The three
  writers write `updated:` (scaffold asserted against today's date; the
  handover template and the skill block carry the line; `updated` is in the
  handover schema's optional set). Every held file is stamped `2026-09-29`
  and every held file's newest non-merge commit is dated 2026-09-29 or
  earlier.
- **Non-goals**: `check_docs.py` and `plans_registry.py` are untouched; no
  edit hook, no map validator, no body-only comparison, no branch rule.
- **A cost the spec does not name**, recorded for the maintainer, not a
  finding: two branches that change the same held document on different days
  both rewrite the `updated:` line, so their merge conflicts on that line
  every time. The conflict is one line and the stamp resolves it, but GitHub
  cannot build the pull-request merge commit until it is resolved.

## Not checked

Hosted CI (F-2). The kit probe (`scripts/kit/probe.py`) was not rerun; the
implementation notes report 267 cases and an unchanged red set of 31. The
installed user-level handover skill outside this repository (a non-goal).
Whether `git log` on a partial clone (`--filter=blob:none`) behaves like a
full one was not measured.
