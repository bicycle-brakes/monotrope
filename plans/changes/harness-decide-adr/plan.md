---
title: "Plan — harness-decide-adr"
status: draft
implementation_status: partial
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-10-11
supersedes: null
superseded_by: null
bead: coding-harness-3ar
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, adr, decisions, change-class, pull-request, permissions]
---

# Plan — harness-decide-adr

Implements `spec.md` (criteria 1–15). Stage 1: no model markings. Every new
file and text is English (house rule 1).

**Phase 2a was skipped** on 2026-09-30 by the coordinating session, because
the maintainer is travelling and the spec's open points were resolved with
the maintainer in conversation the same day; the phase 6 review covers it.
No 2a reviewer session exists, so phase 6 starts a fresh one, writes
"Reviewer session: none — phase 2a skipped (plan.md)" under its table in
`findings.md`, and also asks the three 2a questions of `spec.md` as rows of
dimension `SPEC`.

The decision-PR wording
comes from `docs/research/2026-09-30-decision-pull-requests.md` (the note),
whose proposals (a)–(f) the maintainer adopted as written (`decisions.md`,
second addendum); line numbers below are at commit `2616cbf`.

Two slices, each ending with `make verify` green and a pushed commit:
**slice 1** (about 2.5 h) marks decision pull requests and guards merges;
**slice 2** (about 4 h) builds the gate and the command and records the
three answers.

## Decided in phase 3

Sorted by the question protocol. No `[DECISION]` is open.

- `[GAP]`, closed — **the GitHub MCP merge tool is `merge_pull_request`**
  (github/github-mcp-server `README.md` at `85598ba`, read 2026-09-30; it
  takes `expectedHeadSha`). Claude Code names an MCP tool
  `mcp__<server>__<tool>`, and "deny and ask rules also accept glob patterns
  in the tool-name position; the pattern must match the full tool name"
  (code.claude.com/docs/en/permissions, read 2026-09-30). So
  `mcp__*__merge_pull_request` covers it under any server name, including
  this machine's `plugin_engineering_github`.
- `[GAP]`, closed — **RB-M2's file is `human-decided`.** This repository's
  map is `provenance.yaml` at the root (there is no `decisions/provenance.yaml`
  here); `docs/governance/regelwerk.md` has `allowed: [human-decided]`. The
  plan proposes a wording (last section) and edits nothing there.
- `[GAP]`, closed by the spec — **note open point 4, where acceptance is
  recorded:** in the merge, and nowhere else. The spec's answered decision
  says the evidence lives in the merge and nothing reads it (criterion 4,
  Non-goals); the answer format admits no further field (`schema_version:
  1`). No agent writes an `approved_by` for a merge that has not happened
  (RB-M1: accepted is derived, not set). A check comparing written acceptance
  with the merge commit goes on the not-now list.
- `[DETAIL]` — **note open point 3, a server-side ruleset for `main`:** not
  now. The spec's Non-goals already put "a push to `main`" and branch
  protection outside this change; the plan's availability for a private
  repository owned by a user account is not verified; and the
  `Bash(git push *main*)` ask rule is the local brake meanwhile.
- `[DETAIL]` — **the merge rules' one list is `scripts/merge_guard.py`**, a
  library without a command line, like `_verdict.py`. It stays `bestand`
  (the `scripts/` catch-all), as its test does: the test reads
  `.claude/settings.json`, and `.claude/` does not travel (kit D3). It gets a
  reason in `ci_gates.OHNE_AUFRUFER`. `scripts/kit/probe.py` needs no new
  entry: the one probe case a `bestand` name in that list turns red
  (`test_no_declared_reason_stands_for_a_script_that_has_a_caller`) is
  already in `REIST_NICHT`.
- `[DETAIL]` — **six ask rules, the note's (f) verbatim** (lines 567–572),
  two more than criterion 12's four ways to merge (`gh alias set`, a push to
  `main`), because the maintainer adopted (f) as written. After `--write` the
  order is the six merge rules, then Omnigent's one.
- `[DETAIL]` — **the several-decisions form (e) lives in
  `prompts/07-commit.md`**, not in a second template: criterion 13 keeps the
  block's text in one template file, and (e) is the rule for bundling.
- `[DETAIL]` — **the ordinary template travels with the decision template**
  (`mechanismus`): both share the top, and an instance with decision PRs but
  no default template would have no pull request that says "nothing to
  decide".
- `[DETAIL]` — **one reader.** `scripts/harness.py` imports
  `scripts/check_adr_answers.py`; the format exists once. Both take `--root`
  (default: the repository they live in), so tests run them on temporary
  trees.
- `[DETAIL]` — **YAML is read strictly**: a `yaml.SafeLoader` subclass that
  refuses a duplicate key in any mapping, for anchor headers and answers
  alike (the pilot refuses duplicates too). PyYAML's YAML 1.1 turns a bare
  `no` into `False`, which is what makes `proposed: no` fail criterion 2.
- `[DETAIL]` — **one finding per cause.** A feature whose header breaks
  criterion 2, and both features of a doubled `change`, are reported and not
  held to an answer; their answer is checked once the header reads.
- `[DETAIL]` — **the command writes last.** All prompts first; then each
  answer is rendered, re-read through the gate's reader, and only then
  written. One run records one change on the recording path, and each run
  rewrites the message file, so each recorded answer is its own commit.
- `[DETAIL]` — **the dialogue reads through an injected function**
  (`ask(prompt) -> str`), so tests script it; the terminal guard is tested
  through the real command line with stdin from `/dev/null`.
- `[DETAIL]` — **2a's skip is recorded in this plan** (above), and phase 6
  copies one line of it into `findings.md`, where it looks for the 2a
  session it would resume; `findings.md` itself is phase 6's file.
- `[DETAIL]` — **merge, not rebase**, when `origin/main` has moved: the
  branch is pushed, and a merge needs no force push.
- `[DETAIL]` — **the answers are asked while slice 1 is built** (the
  questions stand below), so slice 2 ends green. If they are not in hand
  when slice 2 reaches step 2.9, the slice stops there with the gate red on
  exactly the three missing answers — the one red the spec's `[DETAIL]`
  ("the pull request waits for the maintainer's answers") allows — and a
  short follow-up records them.
- `[DETAIL]` — **the label is created only on the maintainer's go** in the
  conversation, by the implementing session, before the pull request opens.
- `[DETAIL]` — **no reason in `OHNE_AUFRUFER` cites a bead id**:
  `test_no_declared_reason_cites_a_closed_or_unknown_bead` turns red once
  the bead closes.

**Not now:** the ruleset for `main`; a check of written acceptance against
the merge commit; the note's optional PreToolUse hook (f) and its
unmarked-decision check (g); draft pull requests as a merge block; a bot
identity for agents (spec, Non-goals). The phone rendering of alerts and
`<details>` (note §2.5) is tested by the maintainer reading this change's
own pull request, at no extra cost.

## S0 · Before slice 1

`git fetch origin`; if `origin/main` is not an ancestor of `HEAD`,
`git merge origin/main`. If either `plans/changes/frontmatter-current/` or
`plans/changes/omnigent-deny-layers/` has meanwhile moved to
`plans/changes/archive/<date>-<name>/`, every step below that names it edits
it there.

## Slice 1 — decision pull requests and the merge guard

### Files

Created:

- `scripts/merge_guard.py` — `MERGE_ASK_RULES: dict[str, tuple[str,
  str]]`, rule → (one-line reason, sample call), the six rules below;
  `EXTRA_SAMPLES` = `mcp__plugin_engineering_github__merge_pull_request`;
  `covers(rule, call) -> bool`, Claude Code's matching as documented: a rule
  without `(` is a tool-name glob (`fnmatch.fnmatchcase`), or a server name
  that matches `<rule>__…`, or bare `Bash`; `Bash(<p>)` turns a trailing
  `:*` into ` *`, `*` into `.*`, everything else literal, full match, and a
  trailing ` *` as the only wildcard also matches the bare command; other
  tools' rules match nothing. `problems(settings: dict) -> list[str]`: a
  rule missing from `permissions.ask`; a `deny` or `allow` rule that covers
  any sample.
- `tests/test_merge_guard.py` — criterion 12's tests (table below).
- `.github/PULL_REQUEST_TEMPLATE/decision.md` — the note's lines 418–459,
  byte for byte.
- `.github/pull_request_template.md` — the note's lines 481–500, byte for
  byte.
- `tests/test_pr_templates.py` — criterion 13's tests: `DECISION_PARTS`
  maps each part the criterion names to the text that carries it (decided:
  `**Merging this PR decides:**`; merge is the confirmation: `**Your move:**
  merge (or ask an agent to) = accept`; consequence: `## What your merge
  confirms`; options: `## Options`; next steps: `## After the merge`), plus
  `**Undo:**` and `## Where it fits`; `missing(text, parts)` returns the
  absent ones.

The six rules, with reason and sample:

| Rule | Reason | Sample |
|---|---|---|
| `Bash(gh pr merge *)` | every `gh pr merge`, any flag (`--auto`, `--admin`, `--squash`), and the bare command | `gh pr merge 54 --merge --match-head-commit abc1234` |
| `Bash(gh api *merge*)` | the REST merge endpoint and the GraphQL `mergePullRequest` mutation; a read containing "merge" also prompts | `gh api -X PUT repos/o/r/pulls/54/merge` |
| `Bash(gh api *Merge*)` | the GraphQL `enablePullRequestAutoMerge` mutation; whether matching ignores case is not documented | `gh api graphql -f query='mutation { enablePullRequestAutoMerge(input: {pullRequestId: "x"}) { clientMutationId } }'` |
| `Bash(gh alias set *)` | an alias would rename `pr merge` past the first rule | `gh alias set pm 'pr merge'` |
| `Bash(git push *main*)` | a push to the unprotected `main` lands a change with no pull request; any branch name containing "main" also prompts | `git push origin HEAD:main` |
| `mcp__*__merge_pull_request` | a GitHub MCP server's merge tool, under any server name | `mcp__github__merge_pull_request` |

Changed:

- `.claude/settings.json` — the six rules appended to `permissions.ask` by
  hand, then `python3 scripts/omnigent_policy.py --write` puts them in its
  order and format; hooks and `deny` unchanged, and
  `tools/omnigent/policy.yaml` shows no diff.
- `tests/test_omnigent_deny_layers.py` —
  `test_settings_ask_exactly_the_asked_tools` compares only
  `[r for r in ask if r.startswith(op.PREFIX)]` with the asked tools; its
  docstring says the merge rules beside them are held by
  `tests/test_merge_guard.py`. The deny/allow loop stays.
- `scripts/ci_gates.py` — `OHNE_AUFRUFER["merge_guard.py"]`: "Library — the
  one list of ask rules that stop an agent before it merges;
  tests/test_merge_guard.py compares .claude/settings.json against it, which
  is all a CI step could do".
- `scripts/kit/manifest.yaml` — `mechanismus` rules, English reasons:
  `.github/PULL_REQUEST_TEMPLATE/` ("the decision pull request's template —
  a decision takes effect by its merge"), `.github/pull_request_template.md`
  ("the ordinary template; its first lines say nothing is decided"),
  `tests/test_pr_templates.py` ("reads only the two templates, which
  travel").
- `prompts/07-commit.md` — three edits:
  1. "**Subject in English, body in German.**" → "**Subject and body in
     English** (`AGENTS.md`, house rule 1)."
  2. After the "pull request text explains itself" bullet, a bullet
     "**Say whether the pull request decides.**": a pull request that adds,
     changes or removes a file `provenance.yaml` reserves for
     `human-decided` (an ADR, an ADR answer under `decisions/answers/`, the
     rule set) is a decision PR — title `decide(<scope>): <the decision as a
     statement>`, label `decision`, body from
     `.github/PULL_REQUEST_TEMPLATE/decision.md` filled into a file and
     passed with `gh pr create --label decision --body-file <file>`; one
     decision per pull request, up to three only when none can be accepted
     without the others, in the form that follows (the note's lines
     514–531, then "What changes for you", "Where it fits", "After the
     merge", context and evidence once, as in the template); every other
     pull request takes `.github/pull_request_template.md`; commits inside
     keep their own types, only the title carries `decide`.
  3. The last line becomes a section `## The merge`: "**You do not sign off
     your own work.** The merge belongs to the maintainer: they merge, or
     explicitly ask an agent to, after the agent has restated the decision
     block." Then the note's six protocol steps (lines 544–558) as a
     numbered list, with `<n>` and `<sha>` for `54` and `abc1234`, and one
     sentence: `.claude/settings.json` asks before every merge command, so
     the permission prompt appears right below the restatement; where no
     prompt can be answered, the maintainer merges in the GitHub app.
- `docs/how-to/signed-decisions.md` — (a) after the introduction, a section
  `## Coding Harness (2026-09-30)`: the maintainer decided that Coding
  Harness introduces no commit signing, now or later, because signing needs
  the laptop and much of the work happens from a phone; a decision there
  takes effect when the maintainer merges the pull request that carries it,
  or asks an agent to (`prompts/07-commit.md`, "The merge"); this guide
  stays the description of LakeSwitch's practice. (b) Step 3: "Take over the
  code of `lakeswitch.signatures`; the coding-harness kit carries no
  signature check (maintainer, 2026-09-30)." (c) State table: heading date
  "2026-09-23; coding-harness row 2026-09-30", row "no signing; the
  maintainer's merge confirms a decision"; the paragraph below: ADR 0004 and
  0005 were Touch-ID-signed before that decision and stay as they are, and
  no gate or signers file is planned. (d) `## Open`: drop the two
  coding-harness bullets, keep D-55.
- `plans/changes/harness-decide-adr/spec.md`, `plan.md` —
  `implementation_status: partial`.
- `plans/INDEX.md` — regenerated.

### Steps

1. S0.
2. `scripts/merge_guard.py`, the settings edit, `--write`, then
   `python3 scripts/omnigent_policy.py --check` → exit 0 and `git diff
   tools/omnigent/policy.yaml` empty.
3. `tests/test_merge_guard.py` and the narrowed Omnigent test; the
   `OHNE_AUFRUFER` line.
4. The two templates, `tests/test_pr_templates.py`, the kit rules.
5. `prompts/07-commit.md`, `docs/how-to/signed-decisions.md`.
6. Plant each slice-1 fault of the mutation list, see its test red, restore.
7. `implementation_status: partial`; `python3
   scripts/check_frontmatter_current.py --stamp`; `python3
   scripts/plans_registry.py --index`; verification; commit; push.

## The three ADR questions (asked during slice 1)

The coordinating session asks the maintainer, one at a time, in the
conversation, and hands each answer with where it was stated (the session's
link or id and the date) to the implementing session. Proposals and reasons
are the anchors' (spec, `[DETAIL]` "The backfill").

1. **harness-decide-adr** — the change that adds the ADR question, its gate
   and command, and the rule that your merge confirms a decision. Should it
   be recorded as an architecture decision (ADR)? Proposal: **yes** — it
   chooses, among alternatives weighed on 2026-09-30, that your merge rather
   than a signature confirms a decision, and it fixes an answer format
   LakeSwitch will read unchanged. A "yes" means an ADR is drafted as work of
   its own after the merge. Answer yes or no, and one sentence why.
2. **frontmatter-current** — the check that every held document's
   `updated:` date is current. ADR? Proposal: **no** — one more check over
   existing document headers and one optional key in the gate list; nothing
   structural changes, and removing it is one revert.
3. **omnigent-deny-layers** — the deny lists for Omnigent's writing tools.
   ADR? Proposal: **no** — it applies ADR 0006's rule that nothing depends on
   an Omnigent policy alone; the list is configuration one file holds, and
   removing it is one revert plus uninstalling the policy.

The agent records a faithful English rendering of each reason; the decision
block of the pull request shows it, so the merge confirms the wording too.

## Slice 2 — the ADR question: gate, command, answers

### Files

Created:

- `scripts/check_adr_answers.py` — the gate and the one reader.
  - Constants: `CLASSES = ("spike", "bounded", "feature",
    "architectural")`; `NAME = ^[a-z0-9][a-z0-9-]*$`; `ROLE =
    ^[a-z][a-z0-9-]*$`; `ANSWER_KEYS` (the eight of criterion 3, in that
    order); `FIX = "python3 scripts/harness.py decide adr"`.
  - `strict_load(text)` — the strict loader above.
  - `reason_problem(text) -> str | None` — `None` when `text` is a string,
    not blank, and its first character is an upper-case letter or a
    backtick.
  - `anchors(root)` — `plans/changes/*/spec.md` except the folder
    `archive`, and `plans/changes/archive/*/spec.md`; each with its folder
    name, a leading `YYYY-MM-DD-` removed for archived ones.
  - `read_class(path)` — criterion 1: strict UTF-8; header = the text
    between a first line `---` and the next `---` line (a leading BOM and
    CRLF tolerated); top-level lines starting `class:`; exactly one; value
    bare, `"…"` or `'…'`, optionally followed by whitespace and `# …`; one
    of `CLASSES`. Otherwise a problem naming the cause.
  - `read_feature(anchor)` — criterion 2 on the strictly loaded header:
    `title` non-blank string; `change` a string matching `NAME` and equal to
    the folder name; `adr_question` a mapping with `proposed` in the strings
    `yes`/`no`, `reason` a non-blank string, optional `answered_by` null or
    string, no other key; `intent.outcome` kept when it is a string. Returns
    a `Feature` (anchor, change, title, proposed, proposal_reason, outcome)
    or problems.
  - `answer_problems(data) -> list[str]` — criterion 3 exactly:
    `type(v) is int and v == 1` for `schema_version`; `type(v) is date` for
    `answered_at` (a datetime or a string fails); `shown` with exactly
    `proposed` and `proposal_reason`; every other rule as the criterion
    says. `load_answer(path)` → (data, problems), a YAML error or a
    non-mapping being a problem.
  - `examine(root) -> Examination` — `anchors`, `features` (held),
    `anchor_findings` (criteria 1–2 and doubled `change`), `missing` (held
    features without `decisions/answers/<change>/adr.yaml`),
    `answer_findings` (a refused file, or one whose `change` differs).
  - Report, one line each, prefixed `adr-answers:`. A missing answer names
    the change, the anchor, the file and `fix: python3 scripts/harness.py
    decide adr`; a refused or foreign answer names the same and "fix: edit
    it in a decision pull request, or delete it and run python3
    scripts/harness.py decide adr"; a class or header finding says that
    whether the change owes an answer is unknown. Green: "read <N> change
    anchors; held <M> features to their answer files: <a, b, c>". No anchor
    or no feature: "examined nothing — read <N> change anchors, none of
    them a feature", exit 0. No line says "confirmed", "approved" or
    "signed".
  - `main(argv)` — `--root`; not a readable directory → "cannot measure",
    exit 3; findings → exit 1; else exit 0.
- `scripts/harness.py` — the command.
  - `argparse`: `decide` → `adr`, both required sub-commands; options
    `--change`, `--answer`, `--reason`, `--stated-in`, `--root`. An unknown
    verb or option is argparse's own exit 2, before anything runs.
  - `main` order: the four recording options all or none, none blank, else
    exit 2 → the role (criterion 10: the `paths:` entry with prefix
    `decisions/answers/`, its `owner_role`, that role under `roles:`; else
    exit 2 naming the entry to add) → the message path (`git -C <root>
    rev-parse --git-path ADR_ANSWER_MSG`, joined to root when relative; not
    a git work tree → exit 2) → one of the two paths.
  - `decide_adr(root, *, ask, out, today, role, message_path)` — the
    terminal path of criterion 7. `main` calls it only when
    `sys.stdin.isatty()`, else "run this yourself in a terminal", exit 2.
    Stops (exit 2) listing `anchor_findings` and `answer_findings` before any
    question; nothing open → "no open ADR question", exit 0. Per question:
    "ADR question <i> of <n> — change <change>", then Title, Anchor (path
    relative to root), Outcome (only when present), "Proposal: <yes|no> —
    <reason>"; "[y/n]" takes exactly `y` or `n` after stripping; the reason
    and the three explain-back lines take text that passes
    `reason_problem` after stripping, re-asking otherwise. `EOFError` or
    `KeyboardInterrupt` at any prompt → "Interrupted — nothing was
    written.", exit 1.
  - `record_adr(root, change, answer, reason, stated_in, *, out, today,
    role, message_path)` — criterion 9: `answer` in `yes`/`no`, the
    stripped reason passing `reason_problem`, the change a held feature
    (else exit 2 naming why: no anchor names it, it is `<class>`, or its
    header's problems), no answer file yet (else exit 2: "an existing answer
    changes only by an edit in a decision pull request"). Findings of other
    anchors do not block it.
  - Writing (both paths): `{schema_version: 1, change, question: "adr",
    answer, reason, shown: {proposed, proposal_reason}, answered_by: role,
    answered_at: today}` through `yaml.safe_dump(sort_keys=False,
    allow_unicode=True)` (it quotes `'no'`), re-read with `load_answer`, then
    written to `decisions/answers/<change>/adr.yaml`. Message: subject
    `docs(decisions): ADR answer for <change>` (or `ADR answers for <n>
    changes`); one line per change `- <change>: an ADR — <reason>` or `no
    ADR`; the terminal path adds "Explained back by the maintainer:" and the
    three lines, the recording path "Stated by the maintainer in: <source>".
    No LakeSwitch decision number. Printed steps: the files written, then
    `git add decisions/answers`, `git commit -F <message path>`, and "carry
    it in a decision pull request (label decision, body from
    .github/PULL_REQUEST_TEMPLATE/decision.md); it takes effect when the
    maintainer merges that pull request, or asks for the merge". It never
    runs `git add`, `commit`, `push`, `merge` or a signing command.
- `tests/test_check_adr_answers.py`, `tests/test_harness_decide_adr.py` —
  the tests below. Temporary repositories are built with
  `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1` and `-c user.name=t
  -c user.email=t@example.invalid -c commit.gpgsign=false`, as
  `tests/test_frontmatter_current.py` does. The gate's file names
  `check_adr_answers.py` in a string (the mutation ratchet looks for it
  there). **Neither file may contain the text `plans_registry.py`**: a file
  with a mutation-named test that names it makes
  `test_the_mutation_ratchet_only_turns_one_way` count the plans-registry
  gates as covered, and it goes red (found in the frontmatter-current build).
- `decisions/answers/{harness-decide-adr,frontmatter-current,omnigent-deny-layers}/adr.yaml`
  — written by the command's recording path in step 2.9, never by hand.

Changed:

- `decisions/gates.yaml` — after `decision-continuity`:

  ```yaml
  - id: adr-answers
    title: Every feature has the maintainer's answer to the ADR question
    command: python3 scripts/check_adr_answers.py
    job: verify
    enforcement: block
    floor: false
    placement: both
    reason: A feature merged with the ADR question unanswered is the failure the LakeSwitch pilot measured three times; the gate holds existence and format, the maintainer's merge confirms the answer.
  ```

- `.github/workflows/ci.yml` — `python3 scripts/ci_gates.py --generate-ci >
  .github/workflows/ci.yml`, never by hand.
- `scripts/ci_gates.py` — `OHNE_AUFRUFER["harness.py"]`: "Entry point, not a
  gate — a person, or an agent on the maintainer's word, records an ADR
  answer with it; tests/test_harness_decide_adr.py runs it".
- `scripts/kit/manifest.yaml` — `mechanismus`:
  `scripts/check_adr_answers.py` ("the check behind the gate adr-answers —
  the gate file travels, so its script does"), `scripts/harness.py` ("the
  command the gate's finding names"), the two test files ("build their own
  trees; hold in the probe copy"); `bestand`: `decisions/answers/` ("this
  repository's ADR answers; another repository's answers are its own").
- `provenance.yaml` — after the `docs/governance/fehler-katalog.md` entry,
  with a two-line English comment: `- prefix: "decisions/answers/"`,
  `allowed: [human-decided]`, `frontmatter: none`, `owner_role:
  framework-architect`. The header's reader list gains `scripts/harness.py`
  (reads `owner_role` of that entry and `roles:`).
- The three anchors, header lines appended before the closing `---`:
  - `plans/changes/archive/2026-09-21-reproducible-bead-export/spec.md`:
    `class: bounded`.
  - `plans/changes/frontmatter-current/spec.md`: `class: feature`,
    `change: frontmatter-current`, `adr_question: {proposed: "no", reason:
    "<the spec's reason for it>"}`.
  - `plans/changes/omnigent-deny-layers/spec.md`: the same with its name
    and reason.
- `docs/WORKFLOW.md` — (a) after "Artefact lifecycle", a subsection
  `### Change classes, the ADR question and decision pull requests`: the
  four classes, one line each, as the spec's `[DETAIL]` words them; only a
  `feature` owes an answer; the proposal lives in the spec header (`change`,
  `adr_question`), the answer in `decisions/answers/<change>/adr.yaml` in
  the pilot's format; the two ways to answer (typed in a terminal; stated in
  the conversation and recorded with `--change … --answer … --reason …
  --stated-in …`); the gate `adr-answers`; a decision takes effect when the
  maintainer merges its pull request or asks for the merge, no commit
  signing; what a decision PR carries (title form, label, the template's
  block) and the ordinary template; the limits of the spec's Non-goals in
  plain words (existence and format only; one GitHub account, so nobody can
  tell who merged; the ask rules are a brake, not a lock; nobody checks the
  class, a "yes" followed by an ADR, or the label and block; the upgrade is
  a bot identity and branch protection). (b) §3 table "What stands in the
  repository for it": one row `Decisions` — the gate, the command, the
  decision template.
- `prompts/02-spec.md` — the frontmatter paragraph gains `class:` (one of
  the four, pointing to the WORKFLOW subsection) and, for a `feature`,
  `change: <folder name>` and `adr_question: {proposed: "yes"|"no", reason:
  "<one sentence>"}`, with the warning that a bare `no` is a YAML boolean;
  the proposal only proposes, the maintainer answers.
- `AGENTS.md` — house rule 8, at most nine lines: a decision takes effect
  when the maintainer merges its pull request; a pull request touching a
  file `provenance.yaml` reserves for `human-decided` is a decision PR
  (title `decide(<scope>): …`, label `decision`, the decision template); an
  agent records an ADR answer only as the maintainer stated it (`python3
  scripts/harness.py decide adr … --stated-in …`), never one of its own; it
  merges only on the maintainer's request in the conversation, after
  restating the decision block (`prompts/07-commit.md`, "The merge");
  `.claude/settings.json` asks before every merge command. No word
  "README"; at most 200 lines.
- `plans/INDEX.md` — regenerated.

### Steps

1. `scripts/check_adr_answers.py` and its test file; that file's tests
   green.
2. `scripts/harness.py` and its test file; green.
3. `provenance.yaml`; the gate entry; regenerate `ci.yml`; the
   `OHNE_AUFRUFER` line; the kit rules.
4. The three anchors' header lines.
5. Plant each slice-2 fault of the mutation list, see its test red,
   restore.
6. `docs/WORKFLOW.md`, `prompts/02-spec.md`, `AGENTS.md`.
7. `python3 scripts/check_adr_answers.py` → exit 1 with exactly three
   lines, one missing answer per feature. Commit and push.
8. The answers are in hand (else: stop, report, and resume here).
9. For each: `python3 scripts/harness.py decide adr --change <name>
   --answer <yes|no> --reason "<English reason>" --stated-in "<source as
   handed over>"`, then `git add decisions/answers && git commit -F <the
   printed message path>` with the session's attribution trailers.
10. `python3 scripts/check_adr_answers.py` → exit 0, "held 3 features".
    `check_frontmatter_current.py --stamp`, `plans_registry.py --index`,
    verification, commit, push.

## Phase 7 — the pull request

1. Ask the maintainer in the conversation: "May I create the GitHub label
   `decision` now? It marks pull requests whose merge is your decision." On
   yes: `gh label create decision --color 8250df --description "Merging
   this PR accepts the decision stated at the top of its description."`
2. Title `decide(adr): 3 decisions on which changes need an ADR`; label
   `decision`; body in the several-decisions form (`prompts/07-commit.md`):
   one block per answer with its source, "Why these belong together: the
   gate this pull request adds is red without all three", "Where it fits:
   phase 7 of seven · stage 1 of three · touches: the gate, the command,
   `decisions/answers/`, the pull request templates,
   `.claude/settings.json`", "After the merge": the ADR draft if the first
   answer is yes (an agent, as a change of its own); the maintainer's
   choice on the RB-M2 wording (below); archiving this folder. Evidence:
   `make verify` at the head commit; bead coding-harness-3ar worked on and
   left open (it closes when LakeSwitch has switched).
3. It merges as criterion 11 says; where the permission prompt cannot be
   answered from the phone, the maintainer merges in the GitHub app.

## Verification command

Where `python3` lacks PyYAML, put
`/Users/mikypiky/.venvs/portfolio-agentic-engineering/bin` first on `PATH`;
where the signing key is locked, prefix the `GIT_CONFIG_*` variables shown.

```sh
python3 scripts/omnigent_policy.py --check
python3 -m pytest tests/test_merge_guard.py tests/test_pr_templates.py tests/test_omnigent_deny_layers.py tests/test_check_adr_answers.py tests/test_harness_decide_adr.py -q
python3 scripts/ci_gates.py --check-ci
python3 scripts/check_adr_answers.py
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
```

Expected after slice 2: the check prints "held 3 features", every test
passes, `VERIFY GREEN`. After slice 1: the same without the two ADR test
files and without `check_adr_answers.py`, which do not exist yet.

## Test per criterion

Gate tests in `tests/test_check_adr_answers.py`, command tests in
`tests/test_harness_decide_adr.py`, unless noted.

The list the gate criterion-ledger holds is the section "Criterion ledger" below; this table is the earlier record.

| Criterion | Test | Fault that turns it red |
|---|---|---|
| 1 | `test_an_anchor_whose_class_is_unknown_goes_red` — no header, no `class:`, `class: Feature`, two lines, invalid UTF-8 | any of them exits 0 |
| 1 | `test_the_class_line_takes_quotes_and_a_comment`; `test_a_non_feature_is_held_to_nothing_further` (bounded, spike, architectural without `change`) | quoting or a comment misread; a bounded anchor reported |
| 2 | `test_a_feature_header_that_breaks_the_shape_goes_red` — blank title, `change` ≠ folder, `proposed: no` bare, extra key under `adr_question`, missing `reason`, duplicate key | one of them accepted |
| 2 | `test_a_feature_in_the_pilots_full_shape_is_read` (every key the pilot requires, invented values); `test_an_archived_folder_loses_its_date`; `test_two_features_naming_one_change_go_red` | the pilot shape reported; an archived folder's date kept; a doubled change passes |
| 3 | `test_an_answer_in_the_pilots_shape_is_accepted` (quoted `'no'`, a reason folded over two lines, plain and `>-`) | refused |
| 3 | `test_every_single_deviation_of_an_answer_goes_red` — parametrised over each rule: `schema_version` `true`/`1.0`/`2`/missing, extra key, bad `change`, `question: ADR`, bare `no`, `maybe`, blank or lower-case reason, `shown` missing or extra key, bad `answered_by`, quoted or datetime `answered_at`, duplicate key, a list | one accepted |
| 4 | `test_an_active_feature_without_an_answer_goes_red`, `test_an_archived_feature_without_an_answer_goes_red`, `test_an_answer_naming_another_change_goes_red`, `test_a_malformed_answer_goes_red` — each line names change, file and the command | exit 0, or the line lacks one of the three |
| 4 | `test_a_feature_with_a_valid_answer_is_not_reported`; `test_no_report_line_calls_an_answer_confirmed` | a valid answer reported; "confirm", "approved" or "signed" in any output |
| 5 | `test_a_green_run_names_the_count_and_the_features`; `test_an_empty_tree_examined_nothing_and_is_not_a_pass`; `test_an_unreadable_root_is_exit_3` | a count missing; "OK" or "pass" on an empty tree; exit other than 3 |
| 6 | `test_the_gate_is_in_the_one_list` (real `decisions/gates.yaml`); `test_the_kit_carries_the_mechanism_and_not_the_answers` (`probe.rolle`); `tests/test_ci.py` as it stands; `leerprobe` | a field of the entry changed; an answer path `mechanismus`; a script without caller, test or mutation test |
| 7 | `test_without_a_terminal_the_dialogue_refuses_and_never_writes` (CLI, stdin `/dev/null`) | the guard removed |
| 7 | `test_each_question_shows_its_context` (two features, one with `intent.outcome`) | "1 of 2", change, title, path, outcome or proposal missing; outcome shown where there is none |
| 7 | `test_only_y_or_n_is_taken_as_an_answer`; `test_a_lower_case_or_blank_reason_is_refused` (reason and explain-back lines) | `yes`, `maybe` or a lower-case line taken |
| 7 | `test_an_interrupt_at_any_prompt_never_writes` — `EOFError` and `KeyboardInterrupt` at every prompt index | a file or the message written; exit other than 1 |
| 7 | `test_a_broken_anchor_or_a_refused_answer_is_listed_before_any_question`; `test_nothing_open_says_so` | `ask` called; exit other than 2 or 0 |
| 8 | `test_the_written_answer_is_what_the_gate_accepts` (then the gate CLI exits 0) | `shown`, role or date wrong; a file the gate refuses |
| 8 | `test_the_command_never_stages_or_commits` — HEAD, `git diff --cached` and index unchanged | a staged file or a commit |
| 8 | `test_the_message_lands_where_git_says`; `test_the_printed_steps_name_the_merge` | message elsewhere, not English, citing a `D-<n>`; steps without the merge |
| 8 | `test_an_unknown_verb_or_option_is_exit_2_and_never_writes` — `decide adrx`, `decid adr`, `--bogus` | anything asked or written |
| 9 | `test_a_stated_answer_is_recorded_without_a_terminal` — message names change, answer, reason, source; no explain-back | refused without a terminal; source missing |
| 9 | `test_a_stated_answer_that_breaks_a_rule_is_refused_and_never_writes` — each option missing or blank, `maybe`, lower-case reason, a bounded change, an unknown change, an answered change (byte-identical after) | anything written; exit other than 2 |
| 10 | `test_answered_by_is_the_role_the_map_names`; `test_a_map_without_the_role_refuses_before_asking` (no entry, no `owner_role`, role not in `roles:`; both paths); `test_this_repository_declares_the_answering_role` (real `provenance.yaml`) | a constant role; asking or writing without the role; the entry missing |
| 11 | review, and the texts of criterion 15 | — |
| 12 | `tests/test_merge_guard.py`: `test_settings_ask_before_every_merge`; `test_no_deny_or_allow_rule_covers_a_merge`; `test_each_rule_matches_its_own_sample`; `test_every_rule_has_a_reason_and_a_sample`; `test_a_missing_or_covered_merge_rule_is_caught` (a rule dropped; `Bash(gh *)` allowed, `Bash` denied, `mcp__github` allowed, `mcp__*` denied); `test_the_omnigent_render_keeps_the_merge_rules` (`op.write` on a copy keeps them in order, `op.check` silent) | a rule missing; a covering rule; `--write` dropping one |
| 12 | `tests/test_omnigent_deny_layers.py` as narrowed | an Omnigent ask rule missing or foreign |
| 13 | `tests/test_pr_templates.py`: `test_the_decision_template_has_every_part`; `test_a_template_missing_a_part_is_caught`; `test_the_decision_line_comes_first` (first three lines); `test_one_alert_and_no_table_or_checkbox`; `test_the_ordinary_template_says_nothing_is_decided`; `test_the_template_tells_an_agent_how_to_merge` (`decide(`, `"decision"`, `--match-head-commit` in the comment) | a part removed; the decision line moved down; a table or `- [ ]` added |
| 13 | the label (`gh label list`) and the pull request's body | phase 7 without them |
| 14 | the gate on the pull request's last commit; review of each answer against its source | red; an answer differing from what was stated |
| 15 | review; `tests/test_entry_points.py` | `AGENTS.md` over 200 lines |

**Mutation list** (planted, test red, restored; recorded in this file's
implementation notes). Slice 1: drop a merge rule from the settings; add
`Bash(gh *)` to `allow`; remove `## Options` from the decision template.
Slice 2: skip archived anchors; accept a bare `no`; drop the folder
comparison; accept `schema_version: true`; print "OK" on an empty tree;
exit 0 on a finding; remove the terminal guard; write before the last
prompt; accept `yes`; overwrite an existing answer; hard-code the role.

## Criterion ledger

- 1: tests/test_check_adr_answers.py::test_an_anchor_whose_class_is_unknown_goes_red — any of the five shapes exits 0
- 1: tests/test_check_adr_answers.py::test_the_class_line_takes_quotes_and_a_comment — quoting or a comment misread
- 1: tests/test_check_adr_answers.py::test_a_non_feature_is_held_to_nothing_further — a bounded anchor reported
- 1: tests/test_check_adr_answers.py::test_a_class_line_whose_value_runs_into_a_hash_is_not_misread — `class: feature#x` read as `feature`
- 2: tests/test_check_adr_answers.py::test_a_feature_header_that_breaks_the_shape_goes_red — one of the eight shapes accepted
- 2: tests/test_check_adr_answers.py::test_a_feature_in_the_pilots_full_shape_is_read — the pilot shape reported
- 2: tests/test_check_adr_answers.py::test_an_archived_folder_loses_its_date — an archived folder's date kept
- 2: tests/test_check_adr_answers.py::test_two_features_naming_one_change_go_red — a doubled change passes
- 3: tests/test_check_adr_answers.py::test_an_answer_in_the_pilots_shape_is_accepted — refused
- 3: tests/test_check_adr_answers.py::test_every_single_deviation_of_an_answer_goes_red — one deviation accepted
- 4: tests/test_check_adr_answers.py::test_an_active_feature_without_an_answer_goes_red — exit 0, or the line lacks change, file or command
- 4: tests/test_check_adr_answers.py::test_an_archived_feature_without_an_answer_goes_red — exit 0
- 4: tests/test_check_adr_answers.py::test_an_answer_naming_another_change_goes_red — exit 0
- 4: tests/test_check_adr_answers.py::test_a_malformed_answer_goes_red — exit 0
- 4: tests/test_check_adr_answers.py::test_a_feature_with_a_valid_answer_is_not_reported — a valid answer reported
- 4: tests/test_check_adr_answers.py::test_no_report_line_calls_an_answer_confirmed — "confirm", "approved" or "signed" in any output
- 5: tests/test_check_adr_answers.py::test_a_green_run_names_the_count_and_the_features — a count missing
- 5: tests/test_check_adr_answers.py::test_an_empty_tree_examined_nothing_and_is_not_a_pass — "OK" or "pass" on an empty tree
- 5: tests/test_check_adr_answers.py::test_an_unreadable_root_is_exit_3 — exit other than 3
- 5: tests/test_check_adr_answers.py::test_the_command_line_exits_1_on_a_finding_and_0_when_green — exit 0 on a finding
- 6: tests/test_check_adr_answers.py::test_the_gate_is_in_the_one_list — a field of the entry changed
- 6: tests/test_check_adr_answers.py::test_the_kit_carries_the_mechanism_and_not_the_answers — an answer path `mechanismus`
- 7: tests/test_harness_decide_adr.py::test_without_a_terminal_the_dialogue_refuses_and_never_writes — the guard removed
- 7: tests/test_harness_decide_adr.py::test_each_question_shows_its_context — context or proposal missing
- 7: tests/test_harness_decide_adr.py::test_only_y_or_n_is_taken_as_an_answer — `yes`, `maybe` taken
- 7: tests/test_harness_decide_adr.py::test_a_lower_case_or_blank_reason_is_refused — a lower-case line taken
- 7: tests/test_harness_decide_adr.py::test_an_interrupt_at_any_prompt_never_writes — a file or the message written
- 7: tests/test_harness_decide_adr.py::test_a_broken_anchor_or_a_refused_answer_is_listed_before_any_question — `ask` called
- 7: tests/test_harness_decide_adr.py::test_nothing_open_says_so — exit other than 0
- 8: tests/test_harness_decide_adr.py::test_the_written_answer_is_what_the_gate_accepts — the gate refuses the file
- 8: tests/test_harness_decide_adr.py::test_the_command_never_stages_or_commits — a staged file or a commit
- 8: tests/test_harness_decide_adr.py::test_the_message_lands_where_git_says — message elsewhere
- 8: tests/test_harness_decide_adr.py::test_the_printed_steps_name_the_merge — steps without the merge
- 8: tests/test_harness_decide_adr.py::test_an_unknown_verb_or_option_is_exit_2_and_never_writes — anything asked or written
- 9: tests/test_harness_decide_adr.py::test_a_stated_answer_is_recorded_without_a_terminal — refused without a terminal
- 9: tests/test_harness_decide_adr.py::test_a_stated_answer_that_breaks_a_rule_is_refused_and_never_writes — anything written
- 9: tests/test_harness_decide_adr.py::test_a_refusal_names_why_the_change_owes_no_answer — the three reasons unnamed
- 10: tests/test_harness_decide_adr.py::test_answered_by_is_the_role_the_map_names — a constant role
- 10: tests/test_harness_decide_adr.py::test_a_map_without_the_role_refuses_before_asking — asking without the role
- 10: tests/test_harness_decide_adr.py::test_this_repository_declares_the_answering_role — the entry missing
- 11: not a test — the maintainer's merge confirms a decision; the phase-6 review reads the texts
- 12: tests/test_merge_guard.py::test_settings_ask_before_every_merge — a rule missing
- 12: tests/test_merge_guard.py::test_no_deny_or_allow_rule_covers_a_merge — a covering rule
- 12: tests/test_merge_guard.py::test_each_rule_matches_its_own_sample — a sample unmatched
- 12: tests/test_merge_guard.py::test_every_rule_has_a_reason_and_a_sample — a rule without one
- 12: tests/test_merge_guard.py::test_a_missing_or_covered_merge_rule_is_caught — a rule dropped unseen
- 12: tests/test_merge_guard.py::test_the_omnigent_render_keeps_the_merge_rules — `--write` dropping one
- 12: tests/test_merge_guard.py::test_the_repository_flag_before_a_subcommand_still_asks — a flagged spelling passing
- 12: tests/test_merge_guard.py::test_a_rule_beside_the_merges_is_not_reported — a harmless rule reported
- 12: tests/test_merge_guard.py::test_the_matcher_follows_the_documented_forms — a documented form unmatched
- 12: tests/test_omnigent_deny_layers.py::test_settings_ask_exactly_the_asked_tools — a foreign Omnigent ask rule
- 13: tests/test_pr_templates.py::test_the_decision_template_has_every_part — a part removed
- 13: tests/test_pr_templates.py::test_a_template_missing_a_part_is_caught — caught nothing
- 13: tests/test_pr_templates.py::test_the_decision_line_comes_first — the decision line moved down
- 13: tests/test_pr_templates.py::test_one_alert_and_no_table_or_checkbox — a table or `- [ ]` added
- 13: tests/test_pr_templates.py::test_the_ordinary_template_says_nothing_is_decided — the template decides
- 13: tests/test_pr_templates.py::test_the_template_tells_an_agent_how_to_merge — the merge comment missing
- 13: not a test — the label on GitHub and the pull request's body, checked in phase 7 (`gh label list`)
- 14: not a test — the gate runs on the pull request's last commit; the phase-6 review reads each answer against its source
- 15: tests/test_entry_points.py::test_instruction_file_is_under_200_lines — `AGENTS.md` over 200 lines

## Not touched

- `scripts/export/manifest.yaml`, `scripts/new_change.py`,
  `plans/_README.md` (spec, `[DETAIL]`s).
- `docs/governance/regelwerk.md` — `human-decided`; see the proposal below.
- `docs/adr/` — the Touch-ID lines of ADRs 0004–0006 are history.
- `scripts/omnigent_policy.py` — its `--write` already keeps foreign ask
  rules; only its test narrows. `tools/omnigent/policy.yaml` — re-rendered
  identical.
- `scripts/kit/probe.py` (`REIST_NICHT`, `DECKEL`), `OHNE_TEST`,
  `OHNE_MUTATIONSTEST` — no entry needed; needing one means a test is
  missing.
- `prompts/01a-interview.md` and the other prompts; `research.md`,
  `decisions.md`, `spec.md` beyond `implementation_status`; the research
  note.
- GitHub settings (no ruleset, no branch protection); the label before the
  maintainer's go; the tracker; lakeswitch-ai.

## Proposed wording for RB-M2 (for the maintainer)

Today (German, `docs/governance/regelwerk.md`): a signature is an approval
in the pull request, transcribed by a tool that cannot judge; whoever
approves is neither the author nor the last pusher. Under one GitHub
account that cannot be met: the maintainer is author and last pusher of
every pull request, and GitHub lets no author approve their own.

Proposed text, level (2) and enforcer (`Ramp:signature-transcription`, due
2026-11-30) unchanged:

> A signature is an approval in the pull request, transcribed by a tool
> that cannot judge. Whoever approves is neither the author nor the last
> pusher. Where one person holds every role under one GitHub account, the
> approval is that person's merge — done by them, or by an agent on their
> explicit request after it restated what the pull request decides. That
> exception is a rule, not proof, and ends when agents act under an
> identity of their own.

Applying it is the maintainer's own decision PR, outside this change; the
rule set is German until its own translation, so the row is written in the
file's language when applied.

## Implementation notes

Written by the implementing session on 2026-09-30, after slice 1. The text
above is unchanged.

**S0.** `origin/main` at `1c708f7` was not an ancestor of the branch; merged
(merge commit `72f0015`, the handover of 2026-09-30 only). Neither sibling
folder had moved to `plans/changes/archive/`.

**Slice 1 mutations** — each planted in the working tree, its test seen red,
then restored with `git checkout`:

- `Bash(gh api *Merge*)` dropped from `.claude/settings.json` →
  `test_settings_ask_before_every_merge` red (and four more tests of
  `tests/test_merge_guard.py`).
- `Bash(gh *)` added to `allow` → `test_no_deny_or_allow_rule_covers_a_merge`
  red (and three more).
- `## Options` removed from the decision template →
  `test_the_decision_template_has_every_part` and
  `test_a_template_missing_a_part_is_caught` red.
- Beyond the list, for the criterion 12 rows: the Omnigent ask rule removed,
  and a foreign Omnigent ask rule added → the narrowed
  `test_settings_ask_exactly_the_asked_tools` red; `omnigent_policy.write`
  keeping no foreign ask rule → `test_the_omnigent_render_keeps_the_merge_rules`
  red.

**Where the work adds to the plan text.**

1. **How a sample call is written.** `covers(rule, call)` must know which
   tool a call is for, so a Bash sample is stored as `Bash(<command>)` — the
   table's command inside the tool's name — and an MCP sample as the bare
   tool name. The commands are the table's, unchanged.
2. **Two added tests** in `tests/test_merge_guard.py`:
   `test_a_rule_beside_the_merges_is_not_reported` (the counterpart — a
   matcher that took every rule for a merge rule would flag harmless
   settings) and `test_the_matcher_follows_the_documented_forms` (bare
   command, `:*`, word boundary, server name, other tools).
3. **One sentence of the note's (f) lead-in** (lines 542–543) opens the
   steps in `prompts/07-commit.md`, "The merge": the protocol holds for every
   pull request, and for an ordinary one the restatement is its one-line
   summary. Without it, step 3's "It decides" reads as if an ordinary pull
   request had no protocol.

### Slice 2

Written by the implementing session on 2026-09-30, after slice 2. The text
above is unchanged.

**Slice 2 mutations** — each planted in the working tree, its test seen red,
then restored with `git checkout` (run with the bytecode cache cleared and
`PYTHONDONTWRITEBYTECODE=1`; see item 6 below):

- archived anchors skipped → `test_an_archived_feature_without_an_answer_goes_red`;
- a bare `no` accepted → the `bare no` cases of
  `test_a_feature_header_that_breaks_the_shape_goes_red` and
  `test_every_single_deviation_of_an_answer_goes_red` (3 red);
- the folder comparison dropped → `test_a_feature_header_that_breaks_the_shape_goes_red`;
- `schema_version: true` accepted → `test_every_single_deviation_of_an_answer_goes_red`
  (`true` and `1.0`, 2 red);
- "OK" printed on an empty tree → `test_an_empty_tree_examined_nothing_and_is_not_a_pass`;
- exit 0 on a finding → `test_an_active_feature_without_an_answer_goes_red`,
  `test_the_command_line_exits_1_on_a_finding_and_0_when_green`;
- the terminal guard removed → `test_without_a_terminal_the_dialogue_refuses_and_never_writes`;
- writing before the explain-back prompts → `test_an_interrupt_at_any_prompt_never_writes`
  (6 of 10 cases red: every interrupt after the questions);
- `yes` accepted as an answer → `test_only_y_or_n_is_taken_as_an_answer`;
- an existing answer overwritten → the `an answered change` case of
  `test_a_stated_answer_that_breaks_a_rule_is_refused_and_never_writes`;
- the role hard-coded → `test_answered_by_is_the_role_the_map_names`.

**The answers** (step 9) were stated by the maintainer in Claude Code session
https://claude.ai/code/session_018qxAGMFNS3mM37eUEm5DuQ on 2026-09-30, relayed
by the coordinating session, and recorded with the command's `--stated-in`
path, one commit each: harness-decide-adr `yes`, frontmatter-current `no`,
omnigent-deny-layers `no`, each reason verbatim as relayed. Afterwards the gate
reads "read 4 change anchors; held 3 features to their answer files".

**Where the work departs from or adds to the plan text.**

1. **A kit exemption expired** (the plan says `scripts/kit/probe.py` is not
   touched).

   ```
   expected:   probe.py untouched — no REIST_NICHT entry needed
   found:      the leerprobe went red: test_the_two_manifests_really_disagree_somewhere
               passes in the throwaway repository now (it asks for more than 60
               files in both manifests; the four new mechanism files reached that)
   relevant:   the probe blocks a green case that still carries an exemption
   proposal:   strike the entry, as the probe's own message says, and lower
               DECKEL 32 -> 31 with a comment; no design choice is involved
   ```

   Done that way; the rest of the plan does not change.
2. **Names are matched with `fullmatch`**, not `^…$`: Python's `$` also
   matches before a trailing newline, so `"x\n"` would pass `^[a-z0-9][a-z0-9-]*$`.
3. **Abbreviated options are refused.** `harness.py` and the gate build their
   parsers with `allow_abbrev=False`, so `--chang` is an unknown option (exit
   2), not a guess at `--change`; `test_an_unknown_verb_or_option_is_exit_2_and_never_writes`
   holds it.
4. **The header-finding line says what is unknown.** A feature whose header
   breaks criterion 2 owes an answer; what cannot be told is whether it has
   one. Its line ends "whether it has the answer it owes is unknown until the
   header reads"; a class finding keeps "whether this change owes an ADR
   answer is unknown".
5. **Three tests beyond the table:**
   `test_a_class_line_whose_value_runs_into_a_hash_is_not_misread`
   (`class: feature#x` is one YAML scalar),
   `test_the_command_line_exits_1_on_a_finding_and_0_when_green` (the gate
   through its command line) and `test_a_refusal_names_why_the_change_owes_no_answer`
   (the three reasons of criterion 9, and another anchor's finding not
   blocking a recording).
6. **A stale bytecode cache can fake a result.** A mutation that keeps the
   file's size, restored within the same second, leaves the mutated `.pyc`
   valid, and the next run tests the mutant. The first mutation run left the
   suite red for exactly that reason; the mutations were run again with the
   cache cleared before and after each one and no bytecode written.
7. **The command reads `provenance.yaml` with `yaml.safe_load`**, like its
   other readers, not with the strict loader: a duplicate key elsewhere in the
   map is not this command's finding.
8. **Pushed once, at step 10**, not after step 7: the coordinating session
   asked for a push only when `make verify` is green.

### Repair round 1

Origin `fix-r1`, on the six findings of the phase-6 review (`findings.md`),
2026-09-30. Three fixed, two closed as named limits, one left for phase 7.
The rule table of slice 1 is the first cut: the list now holds eight rules,
and the reason of `Bash(gh alias set *)` and of both `gh api` rules changed.
The decisions below are the coordinating session's `[DETAIL]`s under the
maintainer's decision to ask before every merge command: closing another
spelling of that command is within it, and naming a spelling that passes is
too.

- **F-1, the repository flag before a subcommand** (`ba8bfb1`). Measured on
  2026-09-30 with `pr view`, never with a merge (gh 2.101.0): gh takes
  `-R o/r`, `-Ro/r`, `-R=o/r`, `--repo o/r` and `--repo=o/r` before `pr` and
  between `pr` and `merge` — the flag belongs to `gh pr`, and
  `gh pr merge --help` lists it as inherited. With the flag and no pull
  request argument, gh refuses to run ("argument required when using the
  --repo flag", measured with `view`; the same check is in gh's
  `pkg/cmd/pr/merge/merge.go`, read the same day). Two rules, the smallest
  set that covers the ten spellings:

  | Rule | Reason | Sample |
  |---|---|---|
  | `Bash(gh -* pr merge*)` | `gh pr merge` with a flag before `pr`: gh takes its repository flag there | `gh -R o/r pr merge 54` |
  | `Bash(gh pr -* merge *)` | `gh pr merge` with the repository flag between `pr` and `merge`; the flag needs an argument, so the rule wants one after `merge` | `gh pr -R o/r merge 54` |

  The second rule's trailing ` merge *` keeps `gh pr -R o/r view 53 --json
  mergeable` from prompting; a `merge*` there would not. The three rules the
  review proposed would have missed `--repo=`, `-Ro/r`, `-R=` and
  `pr --repo`. The eight spellings that are not a rule's sample are in
  `EXTRA_SAMPLES`, so no deny or allow rule may cover them either.
  `tests/test_merge_guard.py::test_the_repository_flag_before_a_subcommand_still_asks`
  types eleven merges and eight reads itself; dropping either rule, or
  widening to `Bash(gh *pr *merge*)`, turns it red (checked).
  `.claude/settings.json`: two lines added after `Bash(gh pr merge *)`, then
  `omnigent_policy.py --write`; `--check` says "the tree is what the list
  renders". Left out, and named in `docs/WORKFLOW.md`: a flag of the merge
  moved before `merge` together with its value. gh reads
  `gh pr --comments 53 view` as `gh pr view --comments 53` (measured), so
  `gh pr --squash 54 merge` is a merge no rule matches. One more rule would
  close it; it stays out because nobody writes it by accident, and the rules
  are a brake against accidents.
- **F-2 and F-3, named limits** (`a5c77d8`). No rule added. The two `gh api`
  reasons say a mutation is asked only when its name stands in the command;
  the `gh alias set` reason no longer claims the alias detour closed.
  `docs/WORKFLOW.md`, "What this does not do", names what passes:
  `sh -c '…'`, an absolute path, a script file, the moved merge flag, a
  GraphQL mutation read from a file (`--input <file>`, `-F query=@<file>`),
  `gh alias import` and an edit of gh's config file.
- **F-4, the short texts** (`551fa49`). `AGENTS.md` house rule 8 and
  `prompts/07-commit.md`, "The merge", say "every merge command it
  recognises" and "a brake, not a lock", and point to `docs/WORKFLOW.md`.
- **F-5, the `DECKEL` comment** (`e99eee9`). The trailing comment on
  `DECKEL = 31` is English. The German block comment above it is older than
  this change and stays (house rule 1: no translation in passing).
- **Left open.** F-6 closes in phase 7. The label `decision` exists on GitHub
  since 2026-09-30 (created by the coordinating session on the maintainer's
  yes; `gh label list --search decision`, 2026-09-30).

`make verify` on `551fa49` (2026-09-30, `commit.gpgsign` off): 514 passed,
15 skipped; `docs-links` and `markdownlint` red but report-only, none of
their lines in the passages this round touched. Last line:

```text
VERIFY GREEN — every local gate of the 'verify' job passed.
```
