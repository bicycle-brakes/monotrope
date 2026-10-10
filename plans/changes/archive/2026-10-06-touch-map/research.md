---
title: "Research — touch-map"
status: accepted
implementation_status: done
date: 2026-10-06
last_reviewed: 2026-10-06
updated: 2026-10-10
supersedes: null
superseded_by: null
bead: coding-harness-5p0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, pull-requests, review, diagrams, mermaid, templates]
---

# touch map — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). Read on
2026-10-06 in the worktree at `d5813ec` (branch `feat/touch-map`, fresh from
`origin/main`). Line numbers are given at that commit beside the symbol or
heading; they age, the symbol does not. What was not read says so.

The task (bead coding-harness-5p0): a generated section in every code pull
request that lists the touched code and draws it as a Mermaid map in the form
of ADR 0009, readable on the maintainer's phone. The maintainer's answers of
2026-10-06 stand in [`decisions.md`](decisions.md). Section 4 answers the
questions the orchestrating session asked, each tagged by the question
protocol (`docs/WORKFLOW.md`, "The question protocol", lines 131–157):
`[GAP]` resolved by reading, `[DETAIL]` decided here with its reason,
`[DECISION]` left to the maintainer.

## 0 · Existing artefacts on the topic

- `plans/specs/` is empty. `plans/changes/` holds `adhd-frame`,
  `harness-decide-adr`, `research-currency` and `archive/`; none matches
  `touch.?map|touch list|mermaid|module diagram` (case-insensitive search over
  `plans/`, `prompts/`, `templates/`, `.github/`, `docs/WORKFLOW.md`).
- No file under `scripts/`, `tests/`, `prompts/`, `.github/` or `decisions/`
  names `touch_map` or `touch-map`.
- The two sources live outside `main`:
  - the research note `docs/research/2026-10-06-diagrams-in-pull-requests.md`
    on branch `docs/research-pr-diagrams` at `20123f6` (pull request #83,
    open), read with `git show`; cited below as "the note";
  - LakeSwitch's practice: its handover text
    `handover-ch-module-diagram.md` (64 lines) and `modgraph.py` (245 lines)
    in the LakeSwitch session's scratch directory. `modgraph.py` there is
    byte-identical to the note's second appendix (compared with `diff`), so
    the note is the citable copy. Nothing of it is committed in LakeSwitch
    (its handover, "Origin").

Nothing to update instead of create.

## 1 · What exists today

### 1.1 The recommendation of the note (at `20123f6`)

- **The standard** (§6.1, lines 441–452): every pull request from the
  ordinary template that changes a code, runner or data file carries the
  generated list; prose-only pull requests get one line; the map only at
  three or more changed code files, collapsed at the end; never drawn by hand
  or by a model. Decision pull requests "stay as they are for now".
- **Thresholds** (§4, "Size thresholds", lines 324–335): no code → one line
  (37 of 80 pull requests, #1 to #82); one or two code files → list only (28
  of 80); three or more → list and map (15 of 80); more than about 15 boxes →
  no map, the list and a hint that the change may want splitting.
- **Template and prompt text** (§6.2, lines 454–478): a section "What it
  touches" between "What changes" and "Where it fits"; the map in
  `<details>` after the evidence block; a prompt line telling the agent to run
  `python3 scripts/touch_map.py origin/main HEAD` and paste unchanged.
- **First slice** (§6.3, lines 480–493): script, tests with planted faults,
  template section, prompt line; the gate is slice 2; a stop rule after five
  pull requests.
- **Phone test** (§6.4, lines 505–508): on 2026-10-06 the GitHub app showed
  pull request #83's map as a picture, and `<details>` stayed closed until
  tapped. App version and platform not read (§7).
- **Measured recall gaps** (§5.1, lines 397–404): on
  `origin/feat/hermes-runner-2` (`88c7660`) the prototype missed at least
  four links — a test reads `config.yaml`, `sudoers` and `env.example`
  through `p / "config.yaml"` and a tuple of bare names; and
  `tests/test_kit.py` checks `prompts/research-recheck.md`, which the
  prototype counts as prose.
- **What the prototype does not show** (§5.1, lines 405–407): what changed
  inside a file, and a "writes" link (`ci_gates.py` generates `ci.yml`).

### 1.2 The prototype (the note's first appendix, 199 lines, stdlib)

Rules (its docstring and `main`): the centre is changed `.py`/`.sh` outside
`tests/`; links are `runs` (Makefile, `decisions/gates.yaml`, a workflow or a
shell script names the path), `imports` (a module imports the centre's stem)
and `tests` (a test imports or names it); comments and docstrings are removed
first (`code_only`); prose (`docs/`, `plans/`, `*.md`) and registries (a file
naming ≥ 15 tracked paths) draw no links; unchanged tests fold into one
"+k unchanged tests" node. A name counts when the full path appears, or the
basename is unique and longer than eight characters (`mentions`). It reads
git objects only (`diff base...head`, `ls-tree head`, `show head:path`).

### 1.3 LakeSwitch's practice (`modgraph.py`, the note's §8 and appendix 2)

- Draws one package under `src/lakeswitch/` at the head: files as boxes,
  imports as arrows (`imports`, relative imports resolved), the CLI as a
  container box, outside packages dashed, a C4 level on every box
  (`container:`, `component:`, `code:`), status from `git diff
  --name-status` shown as text "(new)"/"(changed)" and as colour.
- Below the map the three lists **Added** (with imports added),
  **Changed**, **Removed** (with imports dropped), computed by diffing the
  edge sets at head and merge base (`main`, `new_edges`, `gone_edges`).
- Readability (`reduce`): no re-export edges from `__init__.py`, a transitive
  reduction of inside edges, a hub rule (in-degree ≥ max(4, half the other
  files) → drawn without arrows, named in the caption), and a caption naming
  head and merge base and saying "nothing drawn by hand".
- Checked by parsing every block with Mermaid 11 under jsdom before upload
  (handover, "Checked before upload"); measured there: 8 diagrams, 10 to 20
  boxes, 7 to 31 arrows (not re-measured here).
- Its proposal: `scripts/module_diagram.py`, a section "The module's code"
  right after "What changes", appetite about 1 h (estimate).

### 1.4 The prototype on this repository's merged pull requests

Run in this session (2026-10-06) from the scratch directory against the
merges on `origin/main`, the prototype copied unchanged from the note; each
run under one second.

| Pull request (merge) | Changed code files | Boxes | Links | Note |
| --- | --- | --- | --- | --- |
| #73 research-currency (`d5813ec`) | 1 | 4 | 3 | all 3 checked against `ci.yml`, `gates.yaml`, the test: right |
| #70 ADR 0009, a decision PR (`a847516`) | 1 | 4 | 3 | not checked one by one |
| #66 translate scripts (`00d7c31`) | 5 | 17 | 14 | not checked one by one |
| #54 harness decide adr (`ba940fb`) | 5 | 17 | 20 | 12 of 15 named boxes are changed or added files |
| #65 translate tests (`017ec56`) | 0 (5 tests) | 0 | 0 | all five tests under "No code link" |
| #71 roadmap trial (`87daf91`) | 0 | 0 | 0 | prints an empty `flowchart LR` block |

Three facts follow, measured:

1. **A tests-only pull request draws nothing.** The prototype links only
   *into* changed non-test code, so #65's five changed tests show no target.
2. **Medium pull requests cross the note's 15-box line.** Both five-file
   pull requests reach 17 boxes; in #54 they are mostly changed files, so
   folding unchanged neighbours would not bring it under 15.
3. **The prototype has no prose-only output yet**; #71 gets an empty map.

### 1.5 How tests name files here — the recall gap, measured

Tests build paths with `/` joins of string segments, e.g.
`REPO_ROOT / ".github" / "workflows" / "ci.yml"` (`tests/test_ci.py`,
`tests/test_gate_machinery.py`, `tests/test_regelwerk.py`); 11 test files
join under `"scripts"`, `"prompts"` or `".github"`. The prototype's
`mentions` sees neither the joined path nor short basenames: `ci.yml` (6
characters) and `Makefile` (8) fall under its "longer than eight" rule.

A trial resolver (scratch only: walk the AST, join the trailing string
segments of each `/` chain, match a tracked path that ends with them, or a
single unique basename) found, over every test at `d5813ec`, 29 links both
rules see, 43 only the prototype's rule sees (full path or unique long
basename in a string), and **6 only the join rule sees**: `test_ci.py`,
`test_gate_machinery.py` and `test_regelwerk.py` → `.github/workflows/ci.yml`;
`test_kit.py` → `scripts/export/manifest.yaml` (basename not unique);
`test_omnigent_deny_layers.py` → `tools/omnigent/install.sh`;
`test_recap_lock.py` → `tools/claude-code/hooks/recap.sh`. The two rules
complement each other; neither alone is enough.

Markdown is read by tests too: `prompts/` by `test_kit.py`,
`test_frontmatter_current.py`, `test_model_endpoints.py`; the pull request
templates by `test_pr_templates.py` and `test_check_adr_answers.py`;
`templates/` by three tests (grep over `tests/*.py`). 152 distinct `*.md`
names appear as string literals in tests.

### 1.6 Import edges are thin here

21 scripts directly under `scripts/` (`*.py`, `*.sh`), 23 test files. The
most-imported modules at `d5813ec`: `_verdict` and `bead_render` (5
importers each), `plans_registry` (4), `ci_gates` (3). Scripts import each
other by bare name after `sys.path.insert(0, ".../scripts")` (e.g.
`tests/test_ci.py`, line 31), so a module-stem match catches them. No module
reaches LakeSwitch's hub threshold of 4 *and* half of a module, because there
is no package; the note's §2.2 found 10 import edges among 19 modules on
another branch with pyreverse.

### 1.7 The pull request templates and their test

- `.github/pull_request_template.md` (24 lines): one line, "Your move",
  "What could break", `done:`, then `## What changes` (line 9), `## Where it
  fits` (line 13), `## After the merge` (line 16), and the evidence in
  `<details>` (lines 19–24).
- `.github/PULL_REQUEST_TEMPLATE/decision.md` (46 lines): the alert, "Your
  move", "What could break", `done:`, `## What your merge confirms` (line
  10), `## Options` (15), `## What changes for you` (20), `## Where it fits`
  (24), `## After the merge` (27), two `<details>` blocks, one HTML comment
  for agents.
- `tests/test_pr_templates.py`:
  - `test_one_alert_and_no_table_or_checkbox` (lines 62–68): in both
    templates no line that starts with `|` after stripping, no `- [ ]`
    checkbox, alerts only in the decision template (exactly one).
  - `test_the_ordinary_template_says_nothing_is_decided` (lines 71–74): the
    third line (index 2) of the ordinary template carries
    `**Your move:** nothing to decide.` — a new section cannot go above it.
  - `test_the_template_tells_an_agent_how_to_merge` (lines 77–82): the
    decision template holds exactly one HTML comment.
  - `DECISION_PARTS` (lines 21–29) lists the decision template's required
    markers; a new section does not touch them.
- Mermaid edge lines (`a -->|runs| b`) start with a node id, not `|`; the
  table rule would not catch a pasted map. The templates only carry
  placeholders anyway.
- `prompts/07-commit.md`, bullet "The pull request text explains itself"
  (lines 13–21), and the multi-decision form, whose closing sentence lists
  the sections that appear once: "What changes for you", "Where it fits",
  "After the merge", context and evidence (lines 57–60).
- **Decision pull requests can change code:** of the merges on `main` from a
  `decide/` branch, one (#70, `a847516`) exists, and it changed
  `scripts/check_decision_continuity.py`. Decision pull requests under other
  branch names were not searched.

### 1.8 Provenance: no decision pull request

- `provenance.yaml`: `prompts/` is `[human-written]` (lines 239–241),
  `.github/` is `[human-written]` (lines 262–264), `tests/` is
  `[human-written]` (lines 259–261); `scripts/` has no prefix of its own.
  `human-decided` holds `decisions/answers/` (lines 140–143), `docs/adr/`
  (146–148), the rule set and `.claude/rules/`.
- So a change to the templates, `prompts/07-commit.md` and a new script is
  not a decision pull request (`docs/WORKFLOW.md`, "Change classes, the ADR
  question and decision pull requests"; `AGENTS.md`, house rule 8). It
  becomes one only if it adds `decisions/answers/touch-map/adr.yaml` — the
  ADR answer a `feature` owes (section 4, [DECISION] 1).

### 1.9 ADR 0009 and Node.js

- `docs/adr/0009-architecture-delta-in-design-md.md`, "Decision" (lines
  115–121): the delta is a Mermaid flowchart "each box labelled with its C4
  level (person, system, container, component)" plus the lists added,
  changed, removed. The level **code** (a file) is not in that list; D-15
  pinned four kinds including `code` (ADR 0009, "Context", lines 37–40).
  LakeSwitch labels files `code:`.
- Lines 124–127: "no Node.js dependency" in the kit. Mermaid's own parser
  runs on Node.js (the note, §4 option (a)), so LakeSwitch's jsdom parse
  check cannot be a kit gate here.
- Lines 165–168: "Presence can be checked, truth cannot" — the same split
  the touch map inherits.
- `templates/design.md` does not exist on `main` (bead coding-harness-9qo
  brings it); the first filled "Architecture delta" lives on branch
  `feat/hermes-runner-2` (the note, §2.4).

### 1.10 The kit: what travels

`scripts/kit/manifest.yaml` (longest prefix wins):

- `prompts/` → `mechanismus` (lines 56–58); `.github/pull_request_template.md`
  and `.github/PULL_REQUEST_TEMPLATE/` → `mechanismus` (lines 200–205);
  `tests/test_pr_templates.py` → `mechanismus` (lines 147–149).
- `scripts/` and `tests/` catch-alls → `bestand` (lines 245–250); `.github/`
  catch-all → `bestand` (lines 263–265).
- So the template section and the prompt line travel with the kit; a new
  `scripts/touch_map.py` stays unless it gets a longer prefix. A travelling
  template would then name a script the kit does not carry.
- `scripts/export/manifest.yaml` (what goes to `lakeswitch-ai`) ends in a
  catch-all `drop` (line 29) and names `.github/` as staying (line 7).
- LakeSwitch has its own `.github/PULL_REQUEST_TEMPLATE.md` (seen in its
  checkout; its local `origin/main` ref dates from 2026-09-30, not fetched)
  and no `modgraph.py` committed. It does not take this repository's
  template today.

### 1.11 Ratchets a new script meets

- `tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason`
  (line 674): without a gate, the script needs an entry in
  `ci_gates.OHNE_AUFRUFER` (`scripts/ci_gates.py`, line 56) with a reason, as
  `harness.py` and `new_change.py` have ("Entry point, not a gate").
- `test_every_script_has_a_test_or_a_declared_reason` (line 835):
  `OHNE_TEST` is empty (`scripts/ci_gates.py`, line 109), so a test must
  import or run it.
- `test_every_gate_step_has_a_mutation_test` (line 1121) binds only once a
  gate exists (slice 2).

### 1.12 What CI can see (for slice 2)

- `.github/workflows/ci.yml` (lines 6–11) triggers on `push`,
  `pull_request` with GitHub's default activity types, `schedule` and
  `workflow_dispatch`; it is generated by `scripts/ci_gates.py`
  (`generate_ci`, the `"  pull_request:"` line 368). The default types do not
  include `edited`, so a changed pull request body does not start a run.
- The `verify` job checks out with `fetch-depth: 0` already, because a gate
  declares `needs_history` (`scripts/ci_gates.py`, lines 341–345).
- The event file (`$GITHUB_EVENT_PATH`) carries the body, `base.sha` and
  `head.sha` of the pull request; read without a token (the note, §4 (b);
  GitHub's event schema itself not re-read here).

## 2 · What is unclear

1. Whether the map belongs in every code pull request or from three code
   files on — the maintainer's words and the note's recommendation differ
   (section 4, [DECISION] 2).
2. The class, and with it the ADR question (section 4, [DECISION] 1).
3. The precision of the extended rules on more than the six merges of 1.4;
   the note checked 14 of 14 links on one branch, this session 3 of 3 on
   #73. To be measured in phase 4 on the same merges.
4. How github.com fits a map into a phone browser column (the note, §7) —
   not verified; the app view is.
5. GitHub's Mermaid version, and therefore which syntax the app accepts —
   not read.

## 3 · Files a change would touch

- `scripts/touch_map.py` — new: the section, from git objects only.
- `tests/test_touch_map.py` — new: planted faults on trees it builds itself.
- `scripts/ci_gates.py` — one entry in `OHNE_AUFRUFER` (no gate in slice 1).
- `scripts/kit/manifest.yaml` — the role of the two new files.
- `.github/pull_request_template.md` — the section.
- `.github/PULL_REQUEST_TEMPLATE/decision.md` — the same section.
- `prompts/07-commit.md` — one bullet, and the section's name in the
  multi-decision form's closing sentence.
- `tests/test_pr_templates.py` — a marker for the new section in both
  templates (optional; a test that the section is there).
- `plans/INDEX.md` — regenerated.
- Not touched: ADR 0009, `design.md`, `decisions/gates.yaml`,
  `.github/workflows/ci.yml` (slice 2).

## 4 · Answers for this change

### 4.1 What the script draws — [DETAIL]

Both sources combined, because neither alone fits this repository: imports
alone draw little (1.6), path links alone miss tests-only changes and joined
paths (1.4, 1.5).

- **Boxes:** every changed file that is code (`.py`, `.sh` outside
  `tests/`), every changed test, every changed runner (`Makefile`,
  `decisions/gates.yaml`, `.github/workflows/`), and every changed non-code
  file that a test, runner or code file reads. That last rule replaces a
  list of "code-like" folders: `prompts/07-commit.md` and the templates are
  drawn because tests read them (1.5); a note nothing reads stays prose.
  Unchanged neighbours one hop away are drawn (a runner, an importer); the
  unchanged tests of a file fold into "+k unchanged tests", as in the
  prototype.
- **Links, each with its kind:** `runs` (a runner or shell script names the
  path), `imports` (module stem, as scripts import by bare name after
  `sys.path.insert`), `tests` (a test imports it, names its path, or joins
  it with `/`). A changed test also links *outward* to what it tests, even
  when that is unchanged — the fix for #65. Comments, docstrings and
  registries draw nothing (the prototype's rules, measured in the note §5.1).
- **ADR 0009's form, from LakeSwitch:** a `flowchart LR`; each box labelled
  `code: <file name>` (C4's fourth level, which ADR 0009's list leaves out —
  noted, not amended here); status as text "(new)", "(changed)", "(removed)"
  *and* colour, never colour alone; below the map the three lists
  **Added**, **Changed**, **Removed**, with imports added and dropped
  (edge sets at head and merge base); a caption naming head and merge base
  and saying that nothing is drawn by hand.
- **Readability, from LakeSwitch:** a transitive reduction on `imports`
  edges only (a `runs` path through `verify_all.sh` does not imply that
  `Makefile` runs `ci_gates.py` itself); the hub rule, named in the caption.
- **Removed files** read their links at the merge base; a removed file still
  named at the head is listed as "still named by …".
- **Not taken from LakeSwitch:** the jsdom parse (Node.js, 1.9). In its
  place a stdlib structure check in the tests: ids match `[A-Za-z0-9_]+`,
  every label is quoted and holds no `"` or backtick (the failure modes of
  PR-Agent's #1943 and #2211, the note §2.1), every link's ends are
  declared. The maintainer's phone stays the final check of rendering.
- **Output stable for one merge base and head:** sorted, no timestamps, so
  slice 2 can compare a pasted section with a fresh run.

### 4.2 Recall — [DETAIL]

Three rules close the measured gaps:

1. Resolve `/` chains of string segments and match the tracked path that
   ends with them (1.5: +6 links at `d5813ec`); keep the prototype's full
   path and unique-basename rule beside it (43 links only it finds).
2. Draw tested non-code files (4.1) — closes "prompts/ counted as prose"
   without a folder list an instance must maintain.
3. Outward links of changed tests (1.4, #65).

Known misses that stay: a tuple of bare names joined in a loop (the hermes
test), dynamic imports, links through `subprocess` arguments assembled at
run time. The caption says "links found by reading the code; some may be
missing", so the list never claims completeness.

### 4.3 Thresholds — [DETAIL] above, [DECISION] 2 below

- **No changed code, test, runner or tested file:** one line, "Prose only:
  no code, runner or test changed." No map, no empty block (1.4, #71).
- **Upper bound: draw up to 30 boxes; above 15 add the line "Large change:
  consider splitting it" (Baum 2019, Di Biase 2019 in the note §3); above 30
  boxes no map, the list only.** Reason: the note's 15-box cut would remove
  the map from both measured five-file pull requests (17 boxes each, 1.4),
  where a map helps most (the note §3.1: mid-size changes); 30 is ADR 0009's
  own size line ("about thirty elements — more than one page holds",
  line 147). The map is collapsed, so its size costs the phone nothing until
  tapped.
- **Lower bound:** [DECISION] 2.

### 4.4 The template section and the prompt line — [DETAIL]

Placement: in one section right after "What changes", list first and the
collapsed map directly under it — not at the end of the body as the note
proposed. Reason: one contiguous section is one thing to replace when the
branch moves and one thing slice 2 compares; `<details>` stays closed on the
phone (the note §6.4), so the map costs one line there. Name: "What it
touches" (the note), because the section lists runners and tests, not only
"the module's code" (LakeSwitch); this repository has no packages (1.6).

In `.github/pull_request_template.md`, between `## What changes` and
`## Where it fits` (no table, no checkbox, below line 3):

```markdown
## What it touches
<the output of `python3 scripts/touch_map.py origin/main HEAD`, pasted unchanged after the last push>
<for a change with a design.md: "Architecture delta: `plans/changes/<name>/design.md`">
```

In `.github/PULL_REQUEST_TEMPLATE/decision.md`, the same three lines between
`## What changes for you` and `## Where it fits`. Reason: a decision pull
request can change code (#70, 1.7), and one rule for every pull request is
what slice 2 can check.

The script prints the whole section body itself: the list, then — when it
draws a map — `<details><summary>Map at <short sha></summary>`, the Mermaid
block, the three lists and the caption, then `</details>`. Nothing is left
for the agent to wrap or edit.

In `prompts/07-commit.md`, a bullet after "The pull request text explains
itself":

```markdown
- **What it touches is generated, never drawn.** After the last push, run
  `python3 scripts/touch_map.py origin/main HEAD` and paste its output under
  "What it touches" unchanged, in either template. Never edit it, and never
  draw a map by hand or have a model draw one. When the branch moves, run it
  again and replace the whole section.
```

and "What it touches" added to the list of sections that appear once in the
multi-decision form (lines 57–60).

### 4.5 Kit role — [DETAIL]

`scripts/touch_map.py` and `tests/test_touch_map.py` → `mechanismus`, each
with a longer prefix in `scripts/kit/manifest.yaml`. Reason: the template
section and the prompt line travel (1.10), and a travelling template that
names a script the kit does not carry sends every instance to a missing
file. The test must build its own git repositories (as
`tests/test_frontmatter_current.py` does) so it holds in the probe copy. The
rules that are this repository's own — which files are runners, the
registry threshold — sit as named constants at the top of the script, the
one place an instance changes. LakeSwitch is not changed by this: it keeps
its own template and `modgraph.py` until it decides otherwise.

### 4.6 A freshness gate later (slice 2, not now) — [GAP] resolved

How it could work, from 1.11, 1.12 and the note §4 (b):

- `touch-map-current` in `decisions/gates.yaml`, job `verify`, starting at
  `enforcement: report` with a valve, as `docs-links` does.
- `scripts/ci_gates.py` writes `pull_request:` with `types: [opened,
  synchronize, reopened, edited]`, so editing the body re-runs CI.
- The step reads body, `base.sha` and `head.sha` from `$GITHUB_EVENT_PATH`
  (no token), cuts the section from `## What it touches` to the next
  level-2 heading, normalises line endings, and compares it with a fresh
  run on the merge base and head. Cheapest first check: the caption's short sha equals
  `head.sha`. On `push` events there is no body; the step says so and stays
  out of the verdict.
- A mutation test (1.11): a body with one link removed goes red.
- What it cannot check: whether the reviewer looked. The note's stop rule
  (§6.3, item 5) covers that: after five pull requests with the section, the
  maintainer is asked once whether it changed what they looked at.

### 4.7 [DECISION] 1 — the class of this change

```text
Goal in one sentence:  Is this a feature (and you answer the ADR question
                       once), or a bounded change (no question)?
Options:
  1. feature.          A new script plus a new required section in every
                       pull request body: it changes how every change is
                       checked in review.
                       Consequence: the spec proposes "no ADR" with a
                       reason; `make verify` stays red until you answer.
                       Your choice of 2026-10-06 ("a pull request
                       convention, not an amendment of ADR 0009") is that
                       answer in substance — if you say it is, one sentence
                       suffices and the session records it with
                       `python3 scripts/harness.py decide adr --stated-in …`.
  2. bounded.          It extends the existing pull request template and
                       turns nothing red.
                       Consequence: no ADR question, no answer file; your
                       review of the pull request alone holds the class.
Recommendation:        Option 1 — the definition fits: "a self-contained
                       deliverable that changes … how it is checked"
                       (docs/WORKFLOW.md, lines 253–254), and every pull
                       request author gets a new duty. The precedent
                       research-currency was bounded because nobody had to
                       do anything; here everybody does.
If you say "ok":       class: feature, the ADR proposal "no"; the answer
                       file then makes the implementation pull request a
                       decision pull request (`decisions/answers/` is
                       human-decided), or the answer travels in a small
                       pull request of its own.
What is lost:          Option 2 would save you one sentence.
```

### 4.8 [DECISION] 2 — the lower bound for the map

```text
Goal in one sentence:  You asked for "a diagram in every pull request"; the
                       research recommends one only for bigger changes —
                       which do you want?
Options:
  1. Every code pull request gets the map (collapsed), whenever the script
     finds at least one link; prose-only pull requests get one line.
                       Consequence: about 43 of the first 80 pull requests
                       would have carried a map instead of 15 (counts from
                       the note §4); small maps of 2 to 4 boxes repeat what
                       the list says.
  2. The map from three changed code files on (the note's rule); below that
     the list only.
                       Consequence: 28 of those 80 pull requests would have
                       carried the list without a map.
Recommendation:        Option 1 — it is what you asked for, the closed
                       block costs one line on your phone (measured
                       2026-10-06), and the section looks the same in every
                       code pull request, so you always know where to tap.
                       Evidence for maps on small changes is weak either
                       way (the note §3: perceived help is for mid-size
                       changes; no study measured more defects found).
If you say "ok":       the lower bound is "at least one link"; the stop
                       rule after five pull requests still asks you whether
                       it helped.
What is lost:          Option 2 would keep small pull request bodies one
                       collapsed line shorter.
```

### 4.9 Class proposed

`feature` (4.7), pending the maintainer's answer. Appetite for slice 1 as
scoped here: about 2–3 h (the note's estimate, §4 (b); not measured).

## 5 · Addendum 2026-10-06 (phase 2): measured for the spec

Read and measured at `a887b82` by phase 2, with the prototype's own helpers
(`code_only`, `imports`) in a scratch script that is not committed. The
"sources" are the files whose text can make a link: code, tests and
runners — 56 of 200 tracked files.

1. **Registries among sources.** Only `.github/workflows/ci.yml` names 15
   or more tracked paths by full path (15), and the prototype exempts
   runners. No test and no script is a registry today.
2. **Module stems.** No two tracked `.py` files share a stem, so a stem
   match is unambiguous today.
3. **How far a changed test reaches.** Every tracked file a test names
   (full path, unique basename over eight characters, `/` join) or
   imports: 1 to 12 per test — `test_ci.py` 12, `test_gate_machinery.py`
   10, `test_frontmatter_current.py` 10, of which 9 are neither code nor a
   runner.
4. **Fixture paths read as links.** `test_frontmatter_current.py` names
   `AGENTS.md`, `README.md`, `provenance.yaml`, `plans/INDEX.md`,
   `templates/handover.md` and others as files it writes into a temporary
   tree, not the repository's own; `test_research_currency.py` names
   `docs/research/_INDEX.md` the same way (line 119). The name rules cannot
   tell such a path from the repository's file. Outward links from a
   changed test to every unchanged file it names would draw them as boxes.
5. **#71 is not prose-only under the extended rules.** It changes
   `provenance.yaml` (named by `tests/test_provenance.py`) and
   `scripts/kit/manifest.yaml` (named by `tests/test_kit.py`); the rule
   "a changed file a test reads is drawn" (4.1) draws both. Merges that
   stay prose-only: #68 (`6c5d51a`, one handover) and #72 (`3715528`, a
   research note and `docs/research/_INDEX.md`). At #72's head no test or
   runner holds that path, and `_INDEX.md` is not a unique basename
   (`docs/journal/_INDEX.md` exists too).
6. **Merges are read as `<merge>^1 <merge>^2`.** The six merges of 1.4
   are two-parent merges of `main`; their first parent is `main` before,
   the second the branch head.
7. **No `design.md` is owed today.** Neither `docs/WORKFLOW.md` nor any
   prompt names `design.md` on `main`; ADR 0009's section lives there only
   once bead coding-harness-9qo brings the template.
8. **Exit codes.** The checks here use 3 for "could not measure"
   (`scripts/check_adr_answers.py`, `scripts/check_research_currency.py`).
9. **The phase gate.** `scripts/validate_change_artefacts.py` named in
   `prompts/02-spec.md` and `prompts/03-plan.md` does not exist;
   `python3 scripts/plans_registry.py --check` stands in, as for the
   changes before this one.
10. **Baseline.** `make verify` green at `a887b82` (2026-10-06), with
    `markdownlint` red but report-only, as before.
