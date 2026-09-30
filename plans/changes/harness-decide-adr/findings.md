---
title: "Findings — harness-decide-adr"
category: findings
created: 2026-09-30
updated: 2026-09-30
status: draft
implementation_status: partial
date: 2026-09-30
last_reviewed: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-3ar
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, adr, decisions, change-class, merge-guard, pull-request]
---

# Findings — harness-decide-adr

Phase 6, round 1, on commit `f41b0f1` (branch `feat/harness-decide-adr`,
eighteen commits over `origin/main` at `1c708f7`), 2026-09-30. The reviewer
ran in a fresh context, wrote nothing but this file and the regenerated
`plans/INDEX.md`, opened no pull request, created no label and wrote nothing
to the tracker. Measured against `spec.md` (criteria 1–15, non-goals) and the
maintainer's decisions in `decisions.md` with its two addenda; the plan's
"Implementation notes" were read for the departures, not as the yardstick.
Phase 2a was skipped, so the plan's three 2a questions are answered here as
rows of dimension `SPEC`.

**Verdict: no BLOCKER, no `[AMBIGUITY]`, no `[DIVERGENT]`.** One MAJOR, five
MINOR, all open; none stops the pull request. The MAJOR is a measured hole in
the merge guard that the research note foresaw and could not verify; it is
recorded for the maintainer, not resolved here.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | MAJOR | MAINT | base | `scripts/merge_guard.py`, `MERGE_ASK_RULES`; `.claude/settings.json`, `permissions.ask` | A valid form of the one command the guard names is not asked. `gh` accepts its repository flag before the subcommand — measured on 2026-09-30 with read-only calls: `gh -R MPAdesso/coding-harness pr view 53`, `gh --repo … pr view 53` and `gh pr -R … view 53` each answered — so `gh -R <owner/repo> pr merge 54`, `gh --repo … pr merge 54` and `gh pr -R … merge 54` are merges. None of the six rules matches them: Claude Code matches "everything before the first `*` as written" (code.claude.com/docs/en/permissions, read 2026-09-30), and `covers()` agrees (all three: no rule). The research note listed exactly this form as "not verified" (§6); the plan adopted the note's rules verbatim without closing it. The Claude Code docs put this in the "different form" class (`Bash(git push *)` does not stop `git -C . push origin main`), and the spec calls that class a spelling the brake may miss, so the code meets the spec; the disagreement recorded is with the rule set: the brake is meant to catch an accidental `gh pr merge`, and this is one. Two ways out, the maintainer's choice: three more ask rules (`Bash(gh -R * pr merge *)`, `Bash(gh --repo * pr merge *)`, `Bash(gh pr -R * merge *)`), or the limit named in the WORKFLOW.md list beside `curl`. [criterion 12] | open — for the maintainer |
| F-2 | MINOR | MAINT | base | `scripts/merge_guard.py`, the rules `Bash(gh api *merge*)` and `Bash(gh api *Merge*)` | The GraphQL mutations are asked about only when their name stands in the command text. `gh api graphql --input <file>` and `gh api graphql -F query=@<file>` carry `mergePullRequest` or `enablePullRequestAutoMerge` inside the file, and the command text has no "merge" — measured with `covers()`: `Bash(gh api graphql --input q.json)` matches no rule (it matched only when the file happened to be called `merge.json`). Same class as F-1; the criterion names the mutations as covered "through `gh api graphql`", and this is the one `gh api graphql` form that is not. [criterion 12] | open |
| F-3 | MINOR | MAINT | base | `scripts/merge_guard.py`, the rule `Bash(gh alias set *)` and its reason | The reason says an alias would rename `pr merge` past the first rule, and the rule stops one of the ways to set one. `gh alias import <yaml>` (gh 2.101.0, `gh alias --help`, 2026-09-30) sets aliases from a file and matches no rule; an edit of gh's own config file sets them too and passes every Bash rule. The rule is the note's (f) verbatim and beyond criterion 12's four ways; recorded because its reason claims the alias detour closed, and it is not. | open |
| F-4 | MINOR | MAINT | base | `AGENTS.md`, house rule 8, last sentence; `prompts/07-commit.md`, "The merge", last paragraph | Both say `.claude/settings.json` "asks before every merge command". `docs/WORKFLOW.md` says the same rules are "a brake against an accidental merge, not a lock" that another spelling passes, and F-1 to F-3 are merge commands that pass. A reader of `AGENTS.md` alone — the one file every harness reads — believes every merge is asked. Not `[DIVERGENT]`: WORKFLOW.md's limit names other programs and routes, and rule 8 points to "The merge", where the merge command is `gh pr merge`; the two texts read together are one rule with its limit, and only the short one lacks the limit. [criterion 15] | open |
| F-5 | MINOR | SPEC | base | `scripts/kit/probe.py`, line 161, the trailing comment on `DECKEL = 31` | The trailing comment was extended in German ("gesenkt am 2026-09-30 (32 -> 31)") while the block comment above it, written by the same change, is English. House rule 1: new text in a repository artefact is English; the existing German half of the line is not translated in passing. Departure 1 of the slice 2 notes is otherwise as described: the probe refuses a green exemption (`abgelaufen` in `probe.py`), so striking the entry was forced, and the cap fell by exactly that one entry. | open |
| F-6 | MINOR | SPEC | base | criterion 13 (label, pull request body), criterion 14 (hosted gate on the pull request), criterion 11 (the merge itself) | Held by phase 7, which has not happened: the GitHub repository has no label `decision` (`gh label list`, 2026-09-30: eleven labels, none of them `decision`; the plan creates it on the maintainer's go before the pull request opens), there is no pull request whose body could carry the decision block, and hosted CI has not run the gate. Closes itself when the pull request exists with the label and the block, CI is green on its last commit, and the maintainer merges it or asks for the merge. | open — closes in phase 7 |
| 2a-1 | — | SPEC | base | `spec.md`, the one place weighed | *Where does the spec admit two plausible readings?* One candidate, and it is read one way: criterion 12's "`gh pr merge` with any arguments (auto-merge included)" against its own caveat "another spelling passes it". Read as "arguments after the subcommand" — the reading the criterion's own reference settles, since it points to the Claude Code docs, whose table puts a flag before the subcommand in the "different form" class — the flag-first forms of F-1 are a spelling, and nothing in the spec is broken. The other reading, "any valid `gh pr merge` invocation", would make F-1 a gap against the spec. Recorded in F-1 as a finding for the maintainer, not marked `[AMBIGUITY]`, because the spec's reference decides it. No other place: the criteria name their inputs, results and refutations. | answered |
| 2a-2 | — | SPEC | base | `plan.md`, "Decided in phase 3" and "Implementation notes" | *What is missing that would have to be decided while building?* Every hole the build met is written down: the plan's `[DETAIL]`s (the sample-call form, `fullmatch` for names, the one reader, the strict loader, the injected `ask`, the six rules from the note) and the implementation notes (`allow_abbrev=False`, the header-finding wording, the struck kit exemption, the bytecode cache). Nothing was filled silently: no constant, path, option or wording in the code lacks its sentence in `spec.md` or `plan.md`. | answered |
| 2a-3 | — | SPEC | base | `spec.md`, criteria 11, 12 (runtime part), 13 (label and body), 14 (the answers' wording), 15 | *Which acceptance criterion cannot go red?* Those the spec itself marks "held by review": 11 (an agent merging without the maintainer's request can only be seen after the fact), 12's runtime sentences (that an ask rule prompts in every mode rests on the docs read on 2026-09-30; no test here drives Claude Code's prompt), 13's label and body and 14's hosted run (F-6), 14's "as the maintainer stated it" (the reviewer did not read the session; the maintainer reads the decision block before the merge), and 15 (prose). Each is a statement of intent with a named reader, not a criterion a test refutes; the spec says so in each case, and the refutation it names is a person's reading. Every other criterion has a test that a planted fault turns red (see "Checked without a finding"). | answered |

Reviewer session: none — phase 2a skipped (plan.md).

## Checked without a finding

- **Criterion 1, the class.** `read_class` refuses no header, no `class:`
  line, two lines, `Feature`, a value outside the four, `class: feature#x`,
  invalid UTF-8; takes bare, double- and single-quoted values with a
  trailing comment, a byte-order mark and CRLF. The other three classes are
  held to nothing further ("examined nothing" with the count).
- **Criterion 2, the feature header.** The strict loader refuses a doubled
  key; `title`, `change` (name rule and folder equality, dated archive
  folders stripped) and `adr_question` (exactly `proposed`, `reason`,
  optional `answered_by`; a bare `no` named as a YAML boolean) are checked
  and nothing else is: the fixture in the pilot's full shape reads, with its
  folded `intent.outcome`. Two features naming one change are both
  reported and held to no answer.
- **Criterion 3, the answer format.** `answer_problems` reproduces the
  pilot's strictness without pydantic: `type(v) is int and v == 1`,
  `type(v) is date`, exact key sets for the file and for `shown`, the
  first-letter rule, the name and role patterns. The three pilot-shaped
  fixtures (quoted `'no'`, a plain fold, a `>-` block, a backtick reason)
  are accepted; each of 24 single deviations is refused and turns the gate
  red.
- **Criterion 4, existence and format.** A missing, refused or foreign
  answer names the change, the anchor, the file and the command; a valid
  answer is not reported; an answer without an anchor is ignored (the
  pilot's rule, a stated non-goal). No output line of a green, red, empty
  or unmeasurable run contains "confirm", "approved" or "signed".
- **Criterion 5, report and exits.** Exit 0 with the anchor count and the
  held features; "examined nothing — read 0 change anchors, none of them a
  feature" for a tree without anchors and for a bare directory, never "OK";
  exit 1 with one line per finding; exit 3 for a missing root and for a
  file, through the command line too. The empty-set exit 0 is the spec's
  own `[DETAIL]` (a fresh kit instance has no feature), so it is not a gate
  over an empty set that hides a failure; it says so.
- **Planted faults, in a scratch copy of `scripts/`, `tests/`,
  `decisions/`, `provenance.yaml`, `.claude/` and `.github/` (removed
  after; no bytecode written):** the foreign-`change` branch dropped →
  `test_an_answer_naming_another_change_goes_red` red; the four-or-none
  check of the recording options dropped →
  `test_a_stated_answer_that_breaks_a_rule_is_refused_and_never_writes`
  red; the bare-command clause of `covers()` dropped →
  `test_the_matcher_follows_the_documented_forms` red; the three
  explain-back prompts skipped →
  `test_a_lower_case_or_blank_reason_is_refused` red. The implementation
  notes' own fourteen mutations were not re-run.
- **Criterion 6, the one list and the kit.** `decisions/gates.yaml` carries
  `adr-answers` with the exact command, `verify`, `block`, `floor: false`,
  `both`; `ci.yml` is byte-identical to the derivation (`--check-ci`);
  `test_check_adr_answers.py` names the gate's script and carries
  `_goes_red` tests, so `tests/test_ci.py` counts it as the mutation test;
  `harness.py` and `merge_guard.py` have their `OHNE_AUFRUFER` reasons in
  English and without a bead id. Kit roles measured through `probe.rolle`:
  the two scripts, the two ADR test files, both templates and
  `tests/test_pr_templates.py` are `mechanismus`; `decisions/answers/` is
  `bestand`; `scripts/merge_guard.py`, `tests/test_merge_guard.py` and
  `tests/test_omnigent_deny_layers.py` are `bestand` (they read
  `.claude/settings.json`, which does not travel). `probe.py --list` names
  no file under `decisions/answers/`. The struck exemption: the throwaway
  copy now holds 61 files that are in both manifests against the kit
  test's floor of "more than 60" — a margin of one, so the next mechanism
  file that leaves the export manifest brings the entry back with the cap
  raised; not a fault of this change, recorded so nobody is surprised.
- **Criteria 7–8, the terminal path.** Without a terminal the command line
  refuses (`stdin` from `/dev/null`, exit 2, nothing written); a broken
  anchor or a refused answer file is listed before any question; each
  question shows its number of the total, change, title, anchor path, the
  outcome only where the header has one, and the proposal; only `y` or `n`
  is taken (`yes`, `maybe`, `Y`, blank asked again); a blank or lower-case
  reason or explain-back line is asked again; an `EOFError` or
  `KeyboardInterrupt` at each of the five prompts writes nothing and exits
  1. The written files pass the gate, `shown` equals the proposal, the role
  and date are the injected ones; HEAD, the index and the staged set are
  unchanged after both paths; the message lands where
  `git rev-parse --git-path ADR_ANSWER_MSG` says, absolute in a linked
  worktree; the printed steps name the merge and the maintainer's request;
  `adrx`, `decid`, `--bogus` and the abbreviation `--chang` are argparse's
  exit 2 before anything runs.
- **Criteria 9–10, the recording path.** All four options or none, none
  blank; `maybe` and `Yes` refused; a lower-case reason refused; a bounded,
  unknown or already answered change refused with the reason named and the
  existing file byte-identical after; a finding of another anchor does not
  block a recording; the message names change, answer, reason and source
  and has no explain-back lines. `answered_by` is the map's `owner_role`
  (`someone-else` in a temporary map), and a map without the entry, the
  key or the role refuses before asking on both paths; this repository's
  map names `framework-architect` under `roles:`.
- **Criterion 11 and the texts.** Grepped every added line of `AGENTS.md`,
  `docs/WORKFLOW.md`, `docs/how-to/signed-decisions.md`, `prompts/`,
  `.github/` and the three scripts for "sign", "confirm", "approv",
  "proof", "who merged": no sentence names a signature, anchor or key as the
  confirmation in Coding Harness, lets an agent merge without the
  maintainer's request, or claims the gate or GitHub can tell who merged.
  The how-to's new section, its step 3, its state row and its `## Open`
  list say no signing, now or later; ADRs 0004 and 0005 stay history. The
  one remaining "signature" in `prompts/07-commit.md` is the quotation of
  rule RB-M1's idea, applied to the merge.
- **Criterion 12, what the rules rest on.** The Claude Code permissions
  page, read on 2026-09-30: rules are evaluated deny, then ask, then allow,
  first match wins, and "a matching ask rule prompts even when a more
  specific allow rule also matches"; `bypassPermissions` skips prompts
  "except for the actions no mode auto-approves"; `dontAsk` denies every
  call that would prompt; a `*` in a Bash rule "matches any text, including
  spaces"; a trailing ` *` also matches the bare command, only when it is
  the rule's only wildcard; `:*` is the equivalent trailing form; deny and
  ask rules "accept glob patterns in the tool-name position" that must
  match the full name; ask rules apply to any subcommand of a compound
  command and "past any leading assignment", and known wrappers (`timeout`,
  `command`, …) are stripped. `covers()` follows every documented form it
  needs (the assignment stripping is not modelled and no sample needs it).
  The six rules are in `.claude/settings.json` in the list's order, then
  Omnigent's one; `omnigent_policy.py --check` reports "the tree is what
  the list renders"; `--write` on a copy keeps them in order; no deny or
  allow rule in the project settings covers a sample, and the planted
  `allow Bash(gh *)`, `deny Bash`, `allow mcp__github`, `deny mcp__*` are
  each caught while `Bash(gh pr view *)`, `Bash(git push origin feat/*)`,
  `mcp__github__get_pull_request`, `mcp__gitlab` and an `Edit` rule are
  not. The GitHub MCP tool is `merge_pull_request`, and the glob covers it
  under this machine's server name. `GH_TOKEN=x gh pr merge 54` is asked by
  Claude Code (docs: deny and ask match past a leading assignment). The
  narrowed Omnigent test compares only the `mcp__omnigent__` rules.
- **Criterion 13, the templates.** `.github/PULL_REQUEST_TEMPLATE/decision.md`
  equals the note's lines 418–459 and `.github/pull_request_template.md`
  its lines 481–500, byte for byte (`diff`, empty). The decision line is
  in the first three lines, one alert, no table, no checkbox; the ordinary
  template says "nothing to decide" on line 3; the agent's comment names
  `decide(`, `"decision"` and `--match-head-commit`; removing any of the
  seven parts turns the test red. `prompts/07-commit.md` carries the
  several-decisions form (e) and the six protocol steps with `<n>` and
  `<sha>`; `prompts/02-spec.md` asks for `class`, `change` and
  `adr_question` and warns about the bare `no`. The report-only
  `markdownlint` gate now lists both templates (MD041, MD022, MD032): the
  texts are GitHub-rendered pull request bodies copied as the plan
  required, and the gate reports, it does not block.
- **Criterion 14, this repository.** The archived spec states
  `class: bounded`; `frontmatter-current` and `omnigent-deny-layers` state
  `class: feature` with `change` and the `[DETAIL]`'s proposals; this spec
  proposes "yes"; every edited anchor is stamped `updated: 2026-09-30`.
  `python3 scripts/check_adr_answers.py` on `f41b0f1`: "read 4 change
  anchors; held 3 features to their answer files: frontmatter-current,
  harness-decide-adr, omnigent-deny-layers", exit 0. The three answer files
  say `yes`, `no`, `no` — as the coordinating session states the maintainer
  answered; each was written by the recording path in a commit of its own
  (`5e2e896`, `3afd4ee`, `5d63474`) whose message names the source. Each
  recorded `reason` is the anchor's proposal reason with a capital initial;
  whether the maintainer's own words were these is what the maintainer
  reads in the decision block before the merge (the criterion's "held by
  review"); the reviewer did not read the session.
- **Criterion 15.** `docs/WORKFLOW.md` states the four classes in one line
  each, the feature's duty, both homes, both ways to answer, the gate, the
  merge rule, what a decision pull request carries and the non-goals' limits
  in plain words, plus the `Decisions` row in the §3 table; `AGENTS.md`
  has 177 lines and no word "README" (`tests/test_entry_points.py` green
  in `make verify`); every command, option, label and gate name in the
  texts exists in the tree.
- **Non-goals.** No commit signing anywhere; no proof of who merged claimed;
  no hosted label or body check; no branch protection; nothing in
  lakeswitch-ai; no pilot date file; no language check; no class duties
  beyond the answer; `scripts/export/manifest.yaml`, `scripts/new_change.py`
  and `plans/_README.md` untouched; `docs/governance/regelwerk.md` untouched
  (the RB-M2 wording stands in the plan as a proposal for the maintainer).
- **Suite.** `python3 -m pytest` over the change's five test files plus
  `tests/test_ci.py`, `tests/test_kit.py`, `tests/test_entry_points.py`:
  220 passed, 2 skipped. `make verify` on `f41b0f1` (with `commit.gpgsign`
  off): VERIFY GREEN; `docs-links` and `markdownlint` red but report-only,
  the latter now including the two templates (above).

## Not checked

Hosted CI on the pull request, the label and the pull request body (F-6).
Claude Code's permission prompt was not driven live; criterion 12's runtime
sentences rest on the documentation read on 2026-09-30. GitHub Mobile's
rendering of the alert and `<details>` (the note's own open point). The
session in which the maintainer stated the three answers. The
implementation notes' mutation list was not re-run. `gh alias import` was
read from `gh alias --help`, not run.

## For phase 7

`plans/INDEX.md` was regenerated with `python3 scripts/plans_registry.py
--index` for this file. F-1 wants one sentence from the maintainer — three
more ask rules, or the limit named beside `curl` in WORKFLOW.md — and can be
carried in this pull request or after it; F-2 to F-5 are small and can be
fixed in a repair round or recorded; F-6 closes itself in phase 7. The
pull request is a decision PR: it carries three answers under
`decisions/answers/`, so it takes the label `decision`, the title form
`decide(<scope>): …` and the several-decisions block, and it merges only
as criterion 11 says.
