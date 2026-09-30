---
title: "Spec — harness-decide-adr"
status: draft
implementation_status: partial
date: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-3ar
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, adr, decisions, change-class]
class: feature
change: harness-decide-adr
adr_question: {proposed: "yes", answered_by: null, reason: "it decides, among weighed alternatives, that the maintainer's merge of a pull request confirms a decision in Coding Harness instead of a signed commit, and it fixes an answer format that other repositories will read unchanged"}
---

# Spec — harness-decide-adr

The ADR answer moves into Coding Harness (bead coding-harness-3ar). Research:
`research.md` — its section "Corrections after verification" holds where it
disagrees with the text above it. Decisions: `decisions.md` (interview of
2026-09-30), and two later decisions of the maintainer on 2026-09-30, relayed
to this phase by the coordinating session:

- **Coding Harness introduces no commit signing**, now or later. This
  replaces the sentences of `decisions.md` item 2 that make a signature check
  "the very next change" and plan a signed anchor after the trip, and it voids
  the follow-up bead that item names.
- **The maintainer's merge confirms a decision.** A decision takes effect
  only when the pull request that carries it is merged by the maintainer or on
  their explicit request; an agent may write the answer file, recording what
  the maintainer stated in the conversation (the open decision below, now
  answered).

The rest of `decisions.md` stands.

## Problem

A change can decide something that should be recorded as an architecture
decision, and nothing in Coding Harness asks. The principle "research →
interview → the maintainer's decision → an ADR or a feature" exists as a pilot
in lakeswitch-ai and is to have its home here (bead coding-harness-3ar).
Today (`research.md` sections 1–2 and the corrections; read on 2026-09-30,
Coding Harness at `34e23d5`, lakeswitch-ai at `09c9d62`):

- **No spec says what kind of change it is.** No spec in `plans/changes/`
  carries a class in its header; the four change classes exist only in prose
  (the reference architecture in `docs/research/`, and one archived spec's
  body, "Class: Bounded.").
- **No change carries the ADR question, and nobody answers it.** There is no
  proposal field, no answer file, no command that puts the question to the
  maintainer and no gate that notices a missing answer.
- **Nothing tells a decision from an ordinary change.** A pull request that
  decides something looks like any other, and nothing stops an agent from
  merging it.
- **The pilot waits for this repository.** LakeSwitch's gate M-31 fails from
  its pilot date, now 2026-12-15 (lakeswitch-ai pull request 68), unless
  LakeSwitch reads the Coding Harness version by then or signs a later date.
  LakeSwitch can switch without migrating anything only if the answer file and
  the anchor fields stay exactly as in the pilot (`schema_version: 1`).
- **The failure it prevents was measured.** In lakeswitch-ai three features
  merged with the question unanswered, because an agent's proposal and a
  person's answer looked the same (LakeSwitch specification G-17).

## Terms

- **Header** — the YAML frontmatter block at the top of a Markdown file,
  between its first two `---` lines.
- **Change anchor** — the `spec.md` of a change folder, active
  (`plans/changes/<name>/spec.md`) or archived
  (`plans/changes/archive/<YYYY-MM-DD>-<name>/spec.md`). Living specs under
  `plans/specs/` are not anchors.
- **Feature** — a change anchor whose header states `class: feature`.
- **Answer file** — `decisions/answers/<change>/adr.yaml`.
- **Decision artefact** — a file under a `provenance.yaml` prefix whose
  `allowed` classes are exactly `[human-decided]`: today `docs/adr/`,
  `docs/governance/quality-gates.md`, `docs/governance/regelwerk.md` and
  `.claude/rules/`, and with this change `decisions/answers/`.
- **Decision PR** — a pull request that adds, changes or removes a decision
  artefact.
- **The gate** — `python3 scripts/check_adr_answers.py`, gate `adr-answers`.
- **The command** — `python3 scripts/harness.py decide adr`.
- **The pilot** — lakeswitch-ai's `lakeswitch decide adr` and gate M-31 at
  `09c9d62`.

## Acceptance criteria

1. **Every anchor states one class from a closed set.** The header of each
   change anchor has exactly one top-level line `class: <value>` (the value
   optionally quoted, optionally followed by a comment), and the value is one
   of `spike`, `bounded`, `feature`, `architectural`. An anchor without a
   header, without such a line, with two of them, with another value, or that
   cannot be read as UTF-8 text is a finding saying that whether it owes an
   answer is unknown. An anchor of the other three classes is held to nothing
   further.
   *Refuted by,* each in a temporary repository: an anchor with no `class:`
   line, with `class: Feature`, with two `class:` lines, or with invalid
   UTF-8 that exits 0; a `bounded` anchor without `change` or `adr_question`
   that is reported.

2. **A feature's header carries its name and the proposal.** A feature's
   header parses as YAML and has `title` (non-blank text); `change` (text
   matching `^[a-z0-9][a-z0-9-]*$` that equals the change folder's name — for
   an archived folder, the name after its `YYYY-MM-DD-` prefix); and
   `adr_question`, a mapping with `proposed` (the text `yes` or `no`),
   `reason` (non-blank text), optionally `answered_by` (null or text), and no
   other key. Every other key of the header is left unexamined, so an anchor
   in the pilot's full shape (`artifact`, `created`, `review`,
   `class_history`, `appetite`, `intent` …) is read unchanged. Two features
   that name the same change are a finding.
   *Refuted by:* a fixture in the pilot's anchor shape — every key the
   pilot's anchor declaration requires, invented values — that is reported; a
   feature with a blank title, a `change` that differs from its folder,
   `proposed: no` unquoted (a YAML boolean), or an extra key under
   `adr_question` that is accepted; two features naming one change that
   exit 0.

3. **The answer file has the pilot's format.** An answer file is accepted
   exactly when it is a YAML mapping without duplicate keys that has these
   keys and no others: `schema_version` (the integer 1 — not `true`, not
   `1.0`); `change` (matching `^[a-z0-9][a-z0-9-]*$`); `question` (the text
   `adr`); `answer` (the text `yes` or `no`); `reason` (non-blank text whose
   first character is a capital letter or a backtick); `shown` (a mapping with
   exactly `proposed`, the text `yes` or `no`, and `proposal_reason`, non-blank
   text); `answered_by` (matching `^[a-z][a-z0-9-]*$`); `answered_at` (a YAML
   date, not a quoted string).
   *Refuted by:* a file in the shape of the five answers in lakeswitch-ai at
   `09c9d62` (quoted `'no'`, a reason folded over two lines) that is refused;
   any single deviation listed above that is accepted.

4. **The gate holds every feature to its answer — existence and format
   only.** For each feature, active or archived, the answer file of its
   `change` exists, is accepted (criterion 3) and names the same `change`. A
   missing file, a refused one, or one naming another change is a finding that
   names the change, the file and the fix — the command. The gate reads only
   the files of the tree, offline. It cannot see who wrote an answer or who
   merged it, and its report does not claim to; that is held by criterion 11.
   *Refuted by,* each in a temporary repository: an active feature without an
   answer, an archived feature without an answer, an answer naming another
   change, or a malformed answer that exits 0; a feature with a valid answer
   that is reported; a report line that calls an answer confirmed.

5. **The gate's report and exit codes.** Exit 0 when nothing is found; the
   report then names how many anchors it read and which features it held.
   When the tree has no anchor or no feature, the report says it examined
   nothing — never "OK" — and exits 0. Exit 1 when anything is found, one line
   per finding. Exit 3, measuring nothing, when the root it is given is not a
   readable directory.
   *Refuted by:* a finding with exit 0; a green run whose output lacks the
   number of anchors read; an empty tree whose output reads like a pass.

6. **The gate is in the one list and travels with the kit.**
   `decisions/gates.yaml` has the gate `adr-answers` with the command above,
   job `verify`, enforcement `block`, `floor: false`, placement `both`;
   `.github/workflows/ci.yml` is regenerated from it. The gate has a seeded
   test that turns it red under a name `tests/test_ci.py` counts as a mutation
   test. The gate's script, the command's script, the decision-PR template
   (criterion 13) and their tests are `mechanismus` in
   `scripts/kit/manifest.yaml`; `decisions/answers/` is `bestand` there, so no
   answer of this repository travels.
   *Refuted by:* `ci-drift`, `gate-schema`,
   `test_every_gate_step_has_a_mutation_test`,
   `test_every_script_has_a_caller_or_a_declared_reason`,
   `test_every_script_has_a_test_or_a_declared_reason` or `leerprobe` red;
   `python3 scripts/kit/probe.py --list` naming a file under
   `decisions/answers/`.

7. **In a terminal, the command puts each open question in the pilot's
   form.** Called without the recording options of criterion 9, it refuses
   without a terminal (exit 2, nothing written). It collects every feature
   without an answer file; if any anchor has a finding under criteria 1–2, or
   an existing answer file would be refused by the gate, it lists them and
   stops before asking (exit 2, nothing written). With nothing open it says so
   and exits 0. Otherwise, for each open question, it shows its number of the
   total, the change, the title, the anchor's path, `intent.outcome` when the
   header has one, and the proposal with its reason; it takes only `y` or `n`
   and asks again for anything else; it asks for a one-sentence reason and
   asks again when the reason is blank or starts with neither a capital letter
   nor a backtick. After the last question it asks for three explain-back
   lines under the same first-letter rule. End-of-input or an interrupt at any
   prompt prints that nothing was written, writes nothing and exits 1.
   *Refuted by:* tests with scripted input: a missing field of the shown
   context; `yes` or `maybe` taken as an answer; a lower-case reason or
   explain-back line taken; a file written after an interrupt; a question
   asked over an unreadable anchor or a refused answer file; a run without a
   terminal that asks anything.

8. **The command writes answers and a message, and nothing else.** When it
   completes (criterion 7 or 9) it writes one answer file per answered change
   that the gate accepts (criterion 3), with `shown` equal to the anchor's
   proposal, `answered_by` from criterion 10 and `answered_at` today; it writes
   the commit message to the file `git rev-parse --git-path ADR_ANSWER_MSG`
   names; it prints the remaining steps — stage the answers, commit with that
   message, and carry them in a decision PR, which takes effect when the
   maintainer merges it or asks for the merge (criterion 11); and it exits 0.
   The message is English, lists each change with "an ADR" or "no ADR" and its
   reason, and cites no LakeSwitch decision number. The command never stages,
   commits, pushes, merges or signs. An unknown verb or option is an error that
   runs nothing (exit 2).
   *Refuted by:* a written answer file the gate refuses; a changed index or a
   new commit after a run in a temporary repository; printed steps without the
   merge; `harness.py decide adrx` or an unknown option that asks or writes
   anything.

9. **An answer the maintainer stated in the conversation is recorded as
   stated.** `python3 scripts/harness.py decide adr --change <name> --answer
   yes|no --reason <text> --stated-in <where>` records one answer without a
   terminal. `--stated-in` names where the maintainer stated it — a session, a
   pull request comment — so a reader can go and look. It refuses, writing
   nothing (exit 2), when any of the four options is missing or blank, when
   `--answer` is neither `yes` nor `no`, when the reason breaks the
   first-letter rule, when the named change is not a feature with a readable
   anchor (criteria 1–2), when the change already has an answer file — an
   existing answer changes only by an edit in a decision PR — or when the role
   is not configured (criterion 10). Otherwise it writes as criterion 8 says;
   the message names the change, the answer, the reason and the `--stated-in`
   source, and has no explain-back lines, which belong to the maintainer's own
   typing in the terminal path. The answer file carries no source field:
   `schema_version: 1` admits none.
   *Refuted by:* a run with a missing or blank option, an answer `maybe`, a
   lower-case reason, a `bounded` change or an already answered change that
   writes anything; a message without the source; a second run that
   overwrites an answer.

10. **Who answered is configuration, not a constant.** `answered_by` is the
    `owner_role` of the `provenance.yaml` path entry for `decisions/answers/`,
    and that role must be declared under `roles:` in the same file. If the
    entry, the key or the role is missing, the command stops before asking or
    writing (exit 2) and names the line to add. This repository declares
    `decisions/answers/` with `allowed: [human-decided]`, `frontmatter: none`
    and `owner_role: framework-architect`.
    *Refuted by:* a temporary repository whose map names another role and
    whose written answer says anything else; a map without the entry, or with
    a role missing from `roles:`, under which the command asks or writes.

11. **The maintainer's merge confirms a decision.** An answer file, like
    every decision artefact, takes effect only when the decision PR that
    carries it is merged — by the maintainer, or on the maintainer's explicit
    request in the conversation. No signature, anchor or key is involved. An
    agent records only what the maintainer stated and never writes an answer
    of its own as the maintainer's. An agent never merges on its own
    initiative: it merges a pull request only when the maintainer asks for it
    in the conversation, and before the merge command it restates the pull
    request's decision block (criterion 13), so the permission prompt
    (criterion 12) is confirmed with the decision in view. **This is a rule,
    not proof.** Agents act under the maintainer's GitHub account, so neither
    GitHub nor the gate can tell who pressed merge.
    *Refuted by:* a sentence in `AGENTS.md`, `docs/WORKFLOW.md` or
    `docs/how-to/signed-decisions.md` that lets an agent merge without the
    maintainer's request, or names a signature, anchor or key as the
    confirmation in Coding Harness; the pull request of this change merged by
    an agent without the maintainer's request in the conversation (held by
    review of the session).

12. **Every merge an agent can start asks first.** `.claude/settings.json`
    `permissions.ask` has one rule for each way an agent here merges a pull
    request: `gh pr merge` with any arguments (auto-merge included), the REST
    merge endpoint through `gh api` (`…/pulls/<number>/merge`), the GraphQL
    mutations `mergePullRequest` and `enablePullRequestAutoMerge` through
    `gh api graphql`, and the merge tool of a GitHub MCP server, by a
    tool-name glob. The rules are named once, each with a one-line reason, in
    one list in a module under `scripts/`, which the test compares
    `.claude/settings.json` against — the pattern of
    `scripts/omnigent_policy.py`. No deny or allow rule in the project settings
    covers them. `scripts/omnigent_policy.py --check` stays silent, its
    `--write` keeps them, and the one test that pins `permissions.ask` to the
    Omnigent tools compares only Omnigent's own rules from now on. What an ask
    rule does, as Claude Code documents it (research, gaps closed, item 10):
    it prompts in every permission mode, `bypassPermissions` and auto mode
    included; where nobody can answer (`dontAsk`, a headless run without a
    prompt host) the call is refused; and an allow rule from any scope does
    not outrank it. It is a brake against accidents, not a lock: it matches
    the command's text, so another spelling — `curl` against the API, a push
    to `main`, a browser — passes it.
    *Refuted by:* the settings test red when one merge rule is removed from
    `.claude/settings.json` or a deny or allow rule covering one is added;
    `omnigent_policy.py --write` on a copy that drops a merge rule;
    `tests/test_omnigent_deny_layers.py` red.

13. **A decision PR says that it decides.** A decision PR carries the
    repository's decision label and begins its body with the decision block:
    what is decided, the options with their consequences, the consequence of
    the choice, the sentence that merging this pull request is the
    maintainer's confirmation, and the next steps. The block is English and
    written to be taken in at a glance. Its text lives in one template file in
    this repository, and a test holds that the template has each of those
    parts. The label's name and the template's wording come from the research
    note on decision pull requests being written on 2026-09-30; the plan takes
    them from there. An agent that opens or updates a decision PR sets the
    label and the block.
    *Refuted by:* the template test red when one part is removed; the label
    missing from the GitHub repository (`gh label list`); the pull request of
    this change — a decision PR, since it carries three answers — without the
    label or without the block at the top of its body.

14. **This repository is classified and green, with the maintainer's
    answers.** The three anchors that exist without a class get one: the
    archived `2026-09-21-reproducible-bead-export` → `bounded` (its body says
    "Class: Bounded."); `frontmatter-current` and `omnigent-deny-layers` →
    `feature`, each with `change` and `adr_question` as the `[DETAIL]` below
    gives them. This spec is a feature. On the pull request, the gate is green
    because the three answers are in it, each given by the maintainer — typed
    in the terminal (criterion 7) or stated in the conversation and recorded
    (criterion 9). The pull request is a decision PR (criterion 13) and merges
    as criterion 11 says.
    *Refuted by:* the gate red on the pull request's last commit when it
    merges; an anchor under `plans/changes/` without a class line; an answer
    whose answer or reason differs from what the maintainer stated at its
    `--stated-in` source (held by review).

15. **The texts say what is true.** `docs/WORKFLOW.md` states the four
    classes in one line each, that only a feature owes an answer, where the
    proposal and the answer live, both ways to give an answer, the gate, that
    the maintainer's merge confirms a decision and what a decision PR carries,
    and the limits named under Non-goals. `prompts/02-spec.md` asks the spec
    author for `class`, and for a feature `change` and `adr_question`.
    `AGENTS.md` states the agent's part in a few lines: record an answer only
    as the maintainer stated it, mark a decision PR, never merge on its own
    initiative, restate the decision block before a requested merge.
    `docs/how-to/signed-decisions.md` states for Coding Harness the
    maintainer's decisions of 2026-09-30 — no commit signing, the merge
    confirms — and no longer points a further repository to a signature check
    in the Coding Harness kit.
    *Refuted by:* a sentence in these files that names a signature check or
    signed anchor as planned for Coding Harness, a class outside the four, or
    a command, option, label or gate name that does not exist; `AGENTS.md`
    over 200 lines (`tests/test_entry_points.py`). Held by review, not by a
    test of prose.

## Non-goals

- **Commit signing in Coding Harness, in any form** — no port of LakeSwitch's
  gate M-30, no fix of its key list here (bead coding-harness-in1 stays with
  LakeSwitch's gate), no key-loss recovery, no signers file, no anchor.
  Maintainer's decision, 2026-09-30.
- **Proof of who merged.** The upgrade, if an agent is ever found deciding on
  the maintainer's behalf: agents act under a bot identity of their own, and
  branch protection requires approval by someone other than the pusher (rule
  RB-M2 of `docs/governance/regelwerk.md`). Not now.
- **A hosted check that a decision PR carries the label and the block.** The
  rule, the template and the maintainer's reading before the merge hold it.
  Not now.
- **Closing every other way to merge** — the API by `curl`, the web page, a
  push to `main`. Branch protection belongs to the upgrade above.
- **Anything in lakeswitch-ai** — the switch, deleting the pilot, the adapter
  from an exit code to LakeSwitch's gate result, and the pin mechanism it
  needs (`harness.lock.yaml`, LakeSwitch decision D-21). LakeSwitch's own
  change, in its own session. LakeSwitch keeps its signed decisions; the
  merge rule here is Coding Harness's.
- **The pilot's date file and its check** (`decisions/answers/pilot.yaml`) —
  LakeSwitch's reminder to move; dated transitions here are
  `scripts/ramp_valves.py`'s job.
- **The pilot's commit-message language check** (LakeSwitch gate M-6).
  Coding Harness has no such gate (research, gaps closed); whether LakeSwitch
  needs it as a hook of its own when it switches is decided there.
- **Class duties beyond the answer** — the one-way ratchet, phases per class,
  `appetite`, `class_history`, `intent` (`decisions.md` item 3).
- **A check that the class is right.** The spec author states the class and
  the maintainer's review of the pull request holds it. A feature stated as
  `bounded` skips the question; that is the accepted limit of item 3.
- **What follows a "yes".** No gate checks that an ADR follows an answer of
  "yes" (a non-goal of the pilot too); the ADR is drafted as work of its own.
  That includes this change, whose proposal is "yes".
- **An answer file whose change has no anchor** is not reported, as in the
  pilot.
- **A packaged `harness` command** (entry point, `pyproject.toml`), further
  question kinds, the remaining parts of bead coding-harness-xv3 (digest,
  guided flow, reminder), findings as checked data (bead coding-harness-4me),
  and a declared-document foundation in the shape of LakeSwitch's.
- **`scripts/export/manifest.yaml`, `scripts/new_change.py` and
  `plans/_README.md`** stay as they are (see the `[DETAIL]` items).

## Open decisions

None open.

### [DECISION] — How an answer is confirmed as the maintainer's

**Answered on 2026-09-30 by the maintainer** (relayed by the coordinating
session; its addendum to `decisions.md` follows): **the maintainer's merge
confirms.** The question as it stood in this spec until then:

```text
Goal in one sentence:  Coding Harness must be able to tell an answer the
                       maintainer gave from one an agent wrote, without
                       commit signing.
What the answer had to settle, and what it settled:
  1. What the maintainer does that no agent may do on their behalf: merge
     the decision PR, or ask for the merge in the conversation and confirm
     the permission prompt (criteria 11–12). By rule, not by proof.
  2. Where the evidence lives: in the merge. The gate cannot read who merged
     and does not try (criterion 4); no other check reads it (Non-goals).
  3. What the command prints: stage, commit, carry it in a decision PR,
     which takes effect when merged by the maintainer or on their request
     (criterion 8).
  4. Answers given before the mechanism: none exist in this repository.
What is lost against a signature: proof. An agent under the maintainer's
                       account could merge; the rule, the ask prompt and the
                       decision block make that a visible breach, not an
                       impossible one.
```

### `[DETAIL]` — decided here, with the reason

Each of these is reversible and binds nothing beyond this change.

- **The phase gate is `plans_registry.py --check`.** The validator the phase
  prompts name, `scripts/validate_change_artefacts.py`, does not exist in this
  tree; the sibling change `frontmatter-current` found the same (its research,
  item 14).
- **The command's shape: `python3 scripts/harness.py decide adr`.** The
  verbs are the pilot's; a later packaged `harness` command replaces only the
  program name. A script called `harness.py` that knows one verb is the
  smallest form of that; an unknown verb is refused, not guessed.
- **The recording options: `--change`, `--answer`, `--reason`,
  `--stated-in`, all four or none.** One change per run keeps each recorded
  answer tied to its own source. The source goes into the commit message and
  the decision block, not into the answer file, because `schema_version: 1`
  admits no further key and LakeSwitch reads the file unchanged.
- **A stated reason is recorded in English.** The maintainer speaks German
  in the conversation; the repository is English (`AGENTS.md`, house rule 1).
  The agent records a faithful English rendering, and the decision block
  shows it before the merge, so the merge confirms the wording too.
- **Decision artefacts are the paths `provenance.yaml` reserves for
  `human-decided`.** The map already says which files only a person decides;
  a second list would drift from it.
- **The merge rules get their own one list**, beside the Omnigent one rather
  than inside it: `scripts/omnigent_policy.py` owns Omnigent's tools, and its
  `--write` already keeps every rule it does not own. The plan names the
  module.
- **The gate's script is `scripts/check_adr_answers.py`**, beside the other
  `check_*` scripts, with exit 1 for findings and exit 3 for "cannot measure"
  as `check_frontmatter_current.py` and `check_decision_continuity.py` use
  them.
- **Enforcement `block`, `floor: false`.** `block`, because an unanswered
  feature must not merge — the failure the pilot was built against.
  `floor: false`, as the pilot's M-31, and because joining the
  non-negotiable set is a governance act, not a spec's.
- **The pull request waits for the maintainer's answers; no ramp.** The
  pilot did the same: its own pull request carried the maintainer's answers
  for itself and four earlier features before it merged (lakeswitch-ai commit
  `9d34f91` in pull request 62). Consequence: the implementing session ends
  with the gate red on exactly three missing answers and asks the maintainer
  for them in the conversation; it records each with criterion 9, and the
  pull request goes green. A ramp would let this change merge unanswered —
  the failure it exists against.
- **The backfill restates, and classes upward where the text is silent.** The
  archived spec says "Class: Bounded." in its body, and archived headers have
  been stamped before (commit `e553bc8`), so its line restates a fact.
  `frontmatter-current` adds a check and `omnigent-deny-layers` adds a
  control; each is a self-contained deliverable, the reference architecture's
  recognition rule for a feature
  (`docs/research/arc42_Referenzarchitektur_Agentischer_Delivery-Workflow.md`,
  §8.2). Classing them upward costs two questions; classing them down would
  settle their answer without the maintainer. Their proposals:
  - `frontmatter-current`: `proposed: "no"`, reason "one more check over
    existing document headers and one optional key in the gate list; no
    subsystem, dependency, interface or trust boundary changes, and removing
    it is one revert";
  - `omnigent-deny-layers`: `proposed: "no"`, reason "it applies ADR 0006's
    rule that nothing depends on an Omnigent policy alone; the deny list is
    configuration one file holds, and removing it is one revert plus
    uninstalling the policy".
  Each edited file gets its `updated:` stamp, as the gate
  `frontmatter-current` requires. Both packages' beads are closed and their
  folders await archiving (`plans_registry.py --check`, DRIFT, 2026-09-30);
  if they move first, the edit follows them, and criterion 2's folder rule
  already reads archived names.
- **This change proposes "yes".** It chooses, among alternatives weighed in
  the interview and in the decision above, that a merge rather than a
  signature confirms a decision, and it fixes a format another repository
  will read unchanged — a trust-boundary and a contract choice. The
  maintainer answers; the proposal only proposes.
- **The four classes, one line each**, from Coding Harness's own reference
  architecture (§8.2 as above), which LakeSwitch's decision D-24 names as the
  source: `spike` — answers a question; its output is a recommendation;
  `bounded` — changes an existing, readable flow without deciding anything
  new; `feature` — a self-contained deliverable that changes what the system
  must do or how it is checked; `architectural` — a new subsystem or a break
  of an interface, which carries its ADR already, so it is not asked.
- **`change` must equal the folder name.** The pilot never compares them;
  here the comparison closes a copied anchor that would be "answered" by
  another change's file. All five features in lakeswitch-ai at `09c9d62`
  satisfy it, so LakeSwitch migrates nothing.
- **An empty tree exits 0 and says "examined nothing".** In the pilot, a
  result that examined nothing is red (LakeSwitch specification G-2). Here a
  fresh kit instance has no feature, and a gate red from its first day is
  switched off; `plans_registry.py` sets the rule this repository follows —
  an empty set is named, never silent.
- **The outcome is shown only when the header has `intent.outcome`.** A
  Coding Harness spec states its intent in its body; copying it into the
  header would make two versions. The command shows the anchor's path
  instead, and a LakeSwitch anchor still shows its outcome.
- **`answered_by` comes from `provenance.yaml`**, as the pilot's role comes
  from LakeSwitch's provenance map (`owner_role` of `decisions/`). The map
  already carries the roster (`roles:`) and travels with the kit, so an
  instance sets its role where it sets its roster. `framework-architect`,
  because the question is about the framework's architecture and the ADRs
  here are owned by that role. No reader of `provenance.yaml` validates the
  keys of a path entry, so the new key breaks nothing.
- **The terminal guard stays on the terminal path only.** It keeps a
  pipeline from answering by accident; it was never the confirmation, since a
  program can open a pseudo-terminal. The recording path needs no terminal,
  because the maintainer often answers from a phone.
- **The reader uses the standard library and PyYAML only.** The CI installs
  `pytest`, `PyYAML` and `ruff`; the pilot's strictness — unknown keys,
  duplicate keys, a boolean or float where an integer or text is due, a quoted
  date — is reproduced without pydantic.
- **The language check of the reason is not ported.** Coding Harness has no
  commit-message language gate; the reason's first-letter rule is kept, and
  English stays house rule 1, held by review.
- **The message.** English, the pilot's structure for the terminal path,
  no LakeSwitch decision numbers.
- **Kit and export.** The two scripts, the template and their tests are
  `mechanismus`: the gate file travels, so every gate's script does (the
  precedent of `check_frontmatter_current.py`). `decisions/answers/` is
  `bestand`: this repository's answers are not another's. The export manifest
  records the maintainer's travel decision of 2026-09-20, the
  `frontmatter-current` gate did not enter it, and LakeSwitch takes this
  mechanism through the pin (D-21) — it stays unchanged.
- **`scripts/harness.py` gets a reason in `ci_gates.OHNE_AUFRUFER`**: a
  person or an agent on the maintainer's word runs it, no CI step can, as for
  `new_change.py`.
- **`scripts/new_change.py` is untouched.** It writes `research.md` only; the
  class belongs to the spec, which phase 2 writes after `prompts/02-spec.md`.
- **`plans/_README.md` is untouched.** It documents the fields
  `plans_registry.py` holds; the class fields are held by the new gate and
  documented where the gate and the prompt are.
