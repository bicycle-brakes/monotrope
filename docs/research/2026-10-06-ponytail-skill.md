---
title: "Ponytail, the least-code skill — what the seven phases should take from it"
category: research
status: proposed
created: 2026-10-06
last_reviewed: 2026-10-06
updated: 2026-10-06
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-06"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research, ponytail, skills, plugins, over-engineering, yagni, review, planted-faults, mutation, supply-chain, prompts]
---

# Ponytail, the least-code skill

## Result first

**Take the ladder, not the plugin.** Recommendation (b), kept narrow:

1. **Fold the ladder into prompts 03 and 04, and add one finding kind,
   "built and not promised", to prompt 06** — in this repository's words,
   with a credit line. The exact text is in §7. It is a change of its own,
   after the template-bundle change merges, because that change edits
   prompts 03 and 06 too.
2. **Do not install the plugin (a).** It runs three Node hooks on every
   session start, every prompt and every sub-agent, in every repository on
   the machine, the customer instance included. Its code comes from a
   project that shipped six releases in four days. Its rule for tests ("one
   runnable check … YAGNI applies to tests too") is the opposite of prompt
   04's rule that every test has a counterpart. And no other harness here
   would read it.
3. **No periodic audit job (c) for now.** One audit by hand later, if (b)
   proves its worth over three changes.

**What the hand-run ladder found** over five changes (about 4,300 changed
lines outside `plans/`, measured 2026-10-06):

- **Few candidates: about 220 lines, about 5 %.** The implementers built
  almost nothing extra (about 11 lines). The two big candidates grew in the
  review loop. One is a Mermaid parser in a test file that grew through two
  repair rounds. The other is defence against pathological YAML headers,
  asked for by MINOR `MAINT` findings, and one more such row is still open.
- **A rule the repository already has goes unchecked.** Prompt 03 says a
  plan longer than its diff is a finding. The `plan.md` of hermes-runner has
  643 lines for a diff of 139 lines outside `plans/` (4.6 times as long).
  No review row and no gate noticed.
- **Two candidates are the maintainer's decisions**: the pinned but unused
  Jinja2 and Pydantic (D-47), and the arc42 skeleton. The ladder flags them,
  but they are not an agent's to cut. The question protocol already routes
  them right.

**The clash, measured:** on `main` at `d5813ec`, deleting 29 of the 30
tests of `tests/test_research_currency.py` (499 lines) leaves
`make verify` green: 517 cases pass instead of 600, and every blocking
gate still passes. The mutation ratchet looks for one named mutation test
per gate. The test ratchet looks for one test file that runs each script.
A test per acceptance criterion, with its planted fault, is held only by
the prompts and the phase-6 reviewer. Pressure for less code that reaches the
tests would pass every machine check. So the proposed text names the tests
and their planted faults as never thinner.

## 1 · Question and scope

On 2026-10-06 the maintainer asked to take
`github.com/DietrichGebert/ponytail` into account. It is a skill and plugin
that makes an agent write the least code that works. The questions:

- Where would its ladder and its review help phase 3 (plan), phase 4
  (implement, on Sonnet) and phase 6 (review, on Opus)?
- Where would it clash with the planted-fault rule, the mutation ratchet,
  the gates, the kit, the house rules and "not read is not none"?
- Measured, not guessed: run the ladder by hand over three to five recent
  changes, as a reviewer would, and list the candidates by file and line.
- Options (a) install, (b) fold into the prompts, (c) a periodic audit,
  (d) nothing — with a recommendation and, for (b), the exact text.

Nothing was installed, no external model was called, and nothing under
`~/.claude` was touched. Ponytail's content was read through the GitHub API
as data, at commit `552acd5` (2026-10-05).

## 2 · Ponytail today

### 2.1 · The project

Measured through the GitHub API on 2026-10-06:

- MIT licence. 155,949 stars and 8,374 forks. Created 2026-06-12. Last
  push 2026-10-05 (`552acd5`).
- Release v4.13.0 of 2026-10-05: 32 merged changes, 25 of them from
  first-time contributors.
- Six releases between 2026-10-02 and 2026-10-05 (v4.10.1 to v4.13.0).
  98 commits in the 30 days before 2026-10-06.
- It ships adapters for about 20 agent hosts. "Ponytail is one prompt"
  (`README.md`); everything else loads that prompt into a host.
- The README warns: install only from `DietrichGebert/ponytail` or the npm
  package `@dietrichgebert/ponytail`; "a copy that does [ship `.exe` or
  `.dll` files] is not mine". npm releases are published from CI with
  provenance (release v4.8.2).

### 2.2 · The ladder and its rules

The core is `skills/ponytail/SKILL.md` (120 lines). Before writing code,
the agent stops at the first rung that holds:

1. Does this need to exist at all? If not, skip it and say so.
2. Is it already in this codebase? Reuse it.
3. Does the standard library do it?
4. Does a native platform feature cover it?
5. Does an installed dependency solve it?
6. Can it be one line?
7. Only then: the minimum code that works.

Rules around the ladder that matter here:

- The ladder runs **after** reading: "lazy about the solution, never about
  reading".
- A bug fix goes to the root cause, in the shared function every caller
  uses.
- Never cut: validation at trust boundaries, error handling that prevents
  data loss, security, accessibility, anything explicitly requested.
- A shortcut with a known ceiling gets a `ponytail:` comment naming the
  ceiling and the upgrade path.
- Output: code first, then at most three short lines. Explanations the
  user asked for are exempt.
- **Tests:** "Non-trivial logic … leaves ONE runnable check behind … No
  frameworks, no fixtures, no per-function suites unless asked … YAGNI
  applies to tests too."
- "Complex request? Ship the lazy version and question it in the same
  response … Never stall on an answer you can default."

### 2.3 · The commands

- `/ponytail-review`: reviews a diff for over-engineering only. One numbered
  line per finding with a tag (`delete`, `stdlib`, `native`, `reuse`,
  `yagni`, `shrink`) and its replacement, then `net: -N lines possible`.
  Correctness and security are out of scope. It never flags "a single smoke
  test or `assert`-based self-check" — it says nothing about a second test.
- `/ponytail-audit`: the same, over the whole repository, ranked. It greps
  for a symbol before proposing to delete it.
- `/ponytail-debt`: collects the `ponytail:` comments into a ledger and
  flags those without an upgrade trigger.

### 2.4 · What installing it runs

The Claude Code plugin declares three hooks
(`hooks/claude-codex-hooks.json`), each a `node -e` command:

- **SessionStart** (`ponytail-activate.js`): writes a mode flag under
  `~/.claude`, injects the rules as hidden context, copies a status-line
  script into `~/.claude`, and, once, tells the agent to "proactively offer"
  to add a ponytail status line to `~/.claude/settings.json`.
- **SubagentStart** (`ponytail-subagent.js`): injects the same rules into
  **every** sub-agent unless `PONYTAIL_SUBAGENT_MATCHER` narrows it.
- **UserPromptSubmit** (`ponytail-mode-tracker.js`): reads every prompt for
  `/ponytail` commands.

Read at `552acd5`: none of the hooks makes a network call or starts a child
process. All three fail silently. The risk is the update path: code from a
fast-moving repository runs at every session start, prompt and sub-agent,
with the user's rights.

### 2.5 · The benchmark, and what it does not show

The headline is −54 % lines, −20 % cost and 100 % safe. Read from
`benchmarks/results/2026-06-18-agentic.md` and `benchmarks/agentic/README.md`:

- **Set-up:** real headless Claude Code sessions on a public FastAPI and
  React template, 12 feature tickets, **Haiku 4.5 only**, n = 4. Lines are
  the `git diff`, tests excluded.
- **Where the gain is:** user-interface tickets where a native input
  replaces a component (date picker 404 → 23 lines, colour picker
  287 → 23). Most backend endpoints: near zero (search 44 → 44,
  duplicate 24 → 23); archive 175 → 116. The −54 % is the mean over all
  twelve.
- **Safety tier:** 5 security tasks × 4 runs = 20 runs per arm, checked
  deterministically. Ponytail 20/20; a bare "YAGNI and one-liners" prompt
  19/20. The authors call this "a floor, not a dramatic result".
- **Threats the authors name:** one model; n = 4; safety checks are a
  floor; the over-engineering and completeness judges are an LLM
  (Sonnet 4.6) with a rubric. An earlier run was contaminated: the plugin's
  SessionStart hook fired in every arm, the baseline included.
- **Others' runs** (listed in `benchmarks/README.md`, not opened here): one
  on Opus 4.8 found about 44 % less code and "trims everyday bad-input
  handling on 5/24 tasks". One on Cursor found higher process cost on large
  tasks. The README itself says a reasoning model can spend more tokens
  deliberating the rungs.
- **Not measured at all:** Sonnet 5 or Opus 5.5, this repository's models.
  Test strength: the benchmark counts whether a run wrote tests at all
  (1–4 % of runs, in a run of 2026-06-17 the authors later superseded),
  never whether a test can go red.

For this repository: no user interface, Python scripts, tests and Markdown.
The benchmark's own data puts that near the "irreducible" end, where the
gain is small. §3 agrees.

## 3 · The ladder run by hand over five changes

### 3.1 · Method

Five changes, at their heads on 2026-10-06:

| Change | Ref | Changed lines outside `plans/` |
| --- | --- | --- |
| research-currency (merged) | `d5813ec` | 1,165 |
| template-bundle | `9c930e0` | 1,522 |
| project-lock | `a33e341` | 859 (lock file left out) |
| rb-m6-one-account | `b5f8631` | 640 |
| hermes-runner | `7beed6b` | 139 |

Together 4,325 changed lines of code, tests and docs. The 397-line lock
file of project-lock is generated and left out. For each change the diff
was read as a reviewer would read it, the ladder was climbed for every new
function, helper and dependency, and the repository was searched for an
existing equivalent (`git grep`).
hermes-runner changes almost no code (a prompt, 120 lines), so it was only
measured for the plan-length rule. Every candidate is in ponytail-review's
form: tag, place, what to cut, what replaces it.

### 3.2 · Candidates an agent could cut

1. **`yagni:` a Mermaid parser in a test file** (template-bundle,
   `tests/test_templates.py:68-77`, `204-231` and the tests at `670-735`).
   `c4_problems` with the patterns `NODE` and `MERMAID_KEYWORDS`, about 105
   lines with its own counter-probes. It checks one example diagram of two
   boxes (`templates/design.md:86-89`). It grew in the review loop: row 6-12
   (planted faults passed) led to the parser, row 6-16 (fix-r2) to the
   keyword rule, row 6-17 (fix-r3) to `end;`. Two fix-r rows in a row are,
   by `docs/WORKFLOW.md`, an escalation. Replacement: assert the two labels
   (`'["Person: '`, `'["Container: '`); a planted fault (drop the `Person:`
   prefix) still turns it red. About −100 lines.
2. **`yagni:` defence against headers nobody writes** (research-currency,
   `scripts/check_research_currency.py:63-66`, `69-70`, `72`, `103-106`,
   `134-137`, `149-153`; tests `tests/test_research_currency.py:276-292`,
   `369-435`).
   Recursion, memory and alias-bomb guards and two special reasons, from
   MINOR `MAINT` rows F-4 and F-5. F-8, still open, asks for one more guard.
   About 20 lines in the script and 85 in the tests. The input arrives only
   through a reviewed pull request into `docs/research/`, and the job only
   reports. Replacement: nothing. Ceiling: a hostile header breaks one
   nightly report until it is fixed. **Contestable**: it depends on whether
   `docs/research/` counts as a trust boundary. This note says it does
   not.
3. **`reuse:` a fourth header reader** (research-currency,
   `scripts/check_research_currency.py:58`). It copies the pattern of
   `scripts/check_frontmatter_current.py:54`. Two more readers exist:
   `scripts/plans_registry.py:57` and `scripts/handover_schema.py:119`.
   Replacement: one reader in a shared module, as `scripts/_verdict.py`
   already is. About −2 lines here, more across the repository. The readers
   differ in strictness on purpose (findings of research-currency, lines
   82-91), so this is an audit item, not a quick cut.
4. **`shrink:` the gate file read four times** (project-lock,
   `scripts/ci_gates.py:283-294`). `interpreters()` repeats the validate-
   and-read of `gates()` (`251-256`). `generate_ci()` calls both
   (`453-454`). Replacement: read once, pass the document. About −6 lines.
5. **`yagni:` a check for a doubled interpreter** (project-lock,
   `scripts/ci_gates.py:172-174`). A doubled `"3.12"` would only run one leg
   twice. About −3 lines and one test case.
6. **`shrink:` three ways to cut a Markdown section** (template-bundle,
   `tests/test_templates.py:116-120`, `144-149`, `158-164`). `section` and
   `raw_section` differ only in whether fences are stripped. Replacement:
   one function with a flag. About −6 lines.
7. **Plan longer than the change** (hermes-runner,
   `plans/changes/hermes-runner/plan.md`). 643 lines for 139 changed lines
   outside `plans/`. Slice 1's own part (lines 84-441) is 358 lines; about
   220 of them record repair rounds. The rule is in
   `prompts/03-plan.md:45-47`. No review row and no gate checked it. (The
   other four plans are shorter than their diffs.)

Sum of 1–6: about 220 lines, 5 % of 4,325. Implementer-made over-building
(3, 4, 5): about 11 lines.

### 3.3 · Candidates that are decisions, not cuts

- **Jinja2, Pydantic and pydantic-core** are pinned in
  `pyproject.toml:19-23` (project-lock) and installed in every CI leg.
  `git grep` at `a33e341` finds no import. Rung 1 says "not needed". But
  the maintainer decided the pins (D-46, D-47, 2026-09-21) for the
  foundation LakeSwitch builds on (`plans/changes/project-lock/decisions.md`).
- **`templates/arc42.md`** (template-bundle, 114 lines). This repository's
  own research said "not now"; the maintainer chose the skeleton
  (`plans/changes/template-bundle/decisions.md`, 2026-10-05 addendum,
  item 8).

The ladder may raise such a case as a question; cutting it is never an
agent's call. Ponytail's own rule ("anything explicitly requested") agrees.

### 3.4 · Where the ladder holds

- **rb-m6-one-account:** no candidate. `tests/test_repo_settings.py` is
  about 140 lines of measurement and the rest counterparts (8 of its 16
  tests carry a mutation name). Its `gh_api` is the only one in the
  repository. "Not measured is red" is a house invariant, not flexibility.
- **project-lock, `scripts/verify_all.sh:44-55`:** the `PATH` prepend serves
  both bare `ruff` callers (`scripts/ramp_valves.py:71`,
  `tests/test_ci.py:855`). Ponytail's own root-cause rule prefers one place
  over two callers.
- **project-lock, `tests/test_lock.py`:** already uses `packaging`,
  `tomllib` and `importlib.metadata` (rungs 3 and 5).
- **research-currency `--format json`:** it has a consumer, the re-check
  prompt on the hermes-runner branch (`prompts/research-recheck.md:18`).
- **research-currency `CannotMeasure` and exit 3:** an over-engineering
  lens might tag it `delete:`. It is the rule "an empty set is not a
  result" (RB-G7) and must stay.

### 3.5 · What this says

The implementers did not over-build. The extra code came from the review
loop: MINOR `MAINT` rows asking for more defence, and planted-fault rows
answered with a more complex test helper, which then drew its own fix-r
rows. Phase 6 is where a least-code check pays. Phase 4 needs the ladder
mostly as a guard against copying what the repository already has.

## 4 · Fit and clash

### 4.1 · Phase 3, plan

- **Fits.** Prompt 03 already says "No longer than the change" — the
  ladder's twin for the plan. Rung 2 (already in this repository) belongs
  here: the plan names every new file, so it can name what it reuses.
  Candidate 3 would have surfaced there.
- **Clash.** None. The ladder works on the solution, and the plan's
  required list (every file, the verification command, the test and fault
  per criterion) stays.

### 4.2 · Phase 4, implement

- **Fits.** Read first, then climb; reuse before rewriting; root cause in
  the shared function. All of this matches "the plan is the contract".
- **Clash 1 — silent shrinking.** "Ship the lazy version … never stall"
  contradicts prompt 04: a deviation from the plan is a four-line stop, and
  an ambiguous contract is a `[DECISION]`. A lazier way than the plan's
  must be a stop, not a swap.
- **Clash 2 — tests.** "One runnable check … YAGNI applies to tests too"
  contradicts "for every test its counterpart, which plants the fault and
  goes red". Ponytail's "unless asked" exempts tests the plan asks for —
  but an always-on plugin cannot know what the plan asks.
- **Clash 3 — the debt ledger.** `ponytail:` comments and `/ponytail-debt`
  are a second tracker. Here a deliberate simplification is a `[DETAIL]`
  with its reason in `plan.md`, and deferred work is a bead (house rule 2).

### 4.3 · Phase 6, review

- **Fits.** Phase 6 checks code against the spec: "what was promised and
  not built". The ladder adds the mirror: what was built and not promised.
  The reviewer already "reads the code a change calls", which is what
  rung 2 needs.
- **Clash.** Prompt 06 allows exactly three kinds of finding and "no
  suggestions the spec does not ask for". A deletion row is a fourth kind.
  It is compatible only if it is tied to the spec (no criterion, no `MAINT`
  concern and no decision needs the code), always `MINOR`, and never a
  repair round of its own. Otherwise it adds rounds instead of removing
  lines.
- **Sharpen `MAINT`.** Candidate 2 came from rows that asked for more
  defence without saying where the input crosses a trust boundary. Asking
  for that one sentence is the cheapest brake. Candidate 1 came from rows
  that asked a test helper to catch more; the "helper more complex than
  its input" clause of §7.3 is aimed at that.

### 4.4 · Tests, planted faults and the ratchet

Measured on `main` at `d5813ec`, in a worktree, on 2026-10-06:

- Baseline `make verify`: green, 600 cases pass.
- 29 of the 30 tests were removed from `tests/test_research_currency.py`;
  `test_the_list_notices_a_note_past_the_threshold` stayed. Then
  `ruff check --fix` and `ruff format` tidied the leftovers (the same
  measurement in a scratch copy showed both gates red until that step).
  Result: `make verify` **green**, 517 cases pass. Every blocking gate
  passed; the two report-only gates (`docs-links`, `markdownlint`) were
  red before and after, over other files. The file was restored afterwards.
- Why: the mutation ratchet (`tests/test_ci.py:1059-1063`, `1121`) accepts
  one test per gate whose name says it goes red. The test ratchet
  (`tests/test_ci.py:835`) accepts one test file that imports or runs the
  script. Neither counts tests per acceptance criterion.
- Seen by the ratchet's name pattern (counted 2026-10-06): 1 of 30 tests in
  `test_research_currency.py`, 2 of 68 in `test_templates.py`
  (template-bundle), 3 of 12 in `test_lock.py` (project-lock), 8 of 16 in
  `test_repo_settings.py` (rb-m6-one-account).

So a push for less code that reaches the tests passes every machine check.
Only prompt 03 (the test and fault per criterion), prompt 04 (the
counterpart) and the phase-6 reviewer ("a test without its counterpart")
hold the line. Any adoption must name tests and planted faults as never
thinner, in the prompt the implementer reads.

The other way round, the ladder helps the planted-fault rule. A simpler
helper needs fewer counter-probes: candidate 1's parser needed its own
tests and drew two fix-r rows; a literal check needs one planted fault.

### 4.5 · Gates, kit and house rules

- **Gates.** None changes. (b) is prompt text; nothing machine-checks it.
  A gate for plan length could come later; the plan gate prompt 03 names
  (`scripts/validate_change_artefacts.py`) does not exist in this
  repository — already known (`plans/changes/adhd-frame/research.md:116`).
- **Kit.** `prompts/` is a mechanism entry (`scripts/kit/manifest.yaml:55-57`)
  and travels to every instance. The proposed text names no domain and no
  file that stays home. A plugin under `~/.claude` would travel nowhere —
  and still act in every repository on the machine.
- **House rule 1 (English) and rule 7 (texts carry their meaning):** the
  text in §7 is written for that.
- **Customer instance (house rule 6).** A user-level plugin also injects its
  rules into sessions in `oracle-source-inventory`. That is no leak, but it
  changes how agents work there without any decision in that repository.
- **The maintainer's display.** The plugin nudges the agent to edit
  `~/.claude/settings.json` for its own status line. The display belongs to
  `tools/claude-code/` (`AGENTS.md`, "Sessions across checkouts").
- **"Not read is not none."** An over-engineering lens reads code that says
  "not measured" as dead flexibility. Ponytail's audit greps before a
  `delete:`, which finds the callers but not the reason. The never-thinner
  list must name it.

## 5 · Options and consequences

**(a) Install the plugin as-is.** The maintainer's decision alone; agents
never install into `~/.claude`.

- Works at once in Claude Code, with the review and audit commands.
- Three Node hooks run at every session start, prompt and sub-agent, in
  every repository, from a project with six releases in four days.
- Its rules reach every sub-agent, the spec planner and the reviewers too.
  Its test rule contradicts prompt 04, and §4.4 shows no machine would
  notice.
- Not portable: Codex, Omnigent and the kit's instances would not see it.
  A standing rule belongs in `AGENTS.md` or the prompts.
- Reversal: uninstall. Ponytail ships `scripts/uninstall.js` for the
  files its hooks write under `~/.claude` (not read here).

**(b) Fold the ladder into prompts 03 and 04, and one finding kind into
06.**

- About 30 lines of prompt text, versioned, reviewed, carried by the kit.
- Aims where §3 found the waste: the review loop and copies of what exists.
- Tests and planted faults are named as never thinner.
- Cost: one more thing for the reviewer to look at; a risk of MINOR rows
  that nobody takes. Mitigation: always `MINOR`, never a round of its own.
- It is a workflow change: its own change package; the class and the ADR
  question are the maintainer's. Reversal: revert the prompt lines.

**(c) A periodic over-engineering audit,** like the research re-check.

- Would find repository-wide duplication (candidate 3's four readers).
- The research re-check itself runs by hand first
  (`docs/research/2026-10-05-hermes-agent-runner.md`), and a report that
  lists deletions has no owner and no gate.
- A one-off audit by hand gives the same first finding at a fraction of
  the cost.

**(d) Nothing.**

- Prompt 03's "no longer than the change" stays unchecked (candidate 7).
- MINOR hardening rows keep turning into repair rounds (candidates 1, 2;
  F-8 is open now).

## 6 · Recommendation

**(b), narrow.** Then:

1. Write the text of §7 as its own change, after template-bundle merges.
2. Measure it over the next three changes: rows of the new kind, how many
   were taken, lines removed, repair rounds, and whether any criterion lost
   its test or planted fault.
3. Drop it if, after three changes, no row was taken or a row caused a
   repair round of its own.
4. If it holds, one audit of the repository by hand (option c, once), with
   candidate 3 as its first question.

(a) stays the maintainer's call. If he wants the commands anyway, set
`PONYTAIL_SUBAGENT_MATCHER` so the rules do not reach the spec planner and
the reviewers, and decline the status-line offer.

## 7 · Proposed text for (b)

Proposed, not applied. Against `main` at `d5813ec`; the template-bundle
change also edits prompts 03 and 06, so place it after that merge.

### 7.1 · `prompts/03-plan.md` — one more item under "Required"

After "Every file by name":

```markdown
- **The least that meets the spec.** Before you name a new file, function,
  test helper or dependency, climb and stop at the first rung that holds:
  not needed (say so under what you do not touch) → already in this
  repository (name the path you reuse) → the standard library or the
  platform (git, GitHub, the shell) → an installed dependency → only then
  new code. The ladder shortens the solution, never the reading, and never
  what the spec asks: every criterion keeps its test and its planted fault.
  (The ladder is adapted from ponytail, github.com/DietrichGebert/ponytail,
  MIT.)
```

### 7.2 · `prompts/04-implement.md` — a paragraph before the last one

```markdown
**The least code that meets the plan.** Read the code the change touches,
end to end, first. Where the plan leaves the how to you, climb the ladder
of `prompts/03-plan.md` and stop at the first rung that holds. A lazier way
than the plan's is a deviation: the four-line stop, never a silent swap.
Never thinner: a test the plan names and its planted fault, a result that
says "not measured" instead of an empty list, validation where outside
input enters, handling that prevents data loss, and anything
`decisions.md` settled. A simplification with a known ceiling is a
`[DETAIL]` in `plan.md` (the ceiling, and what would lift it), not a code
comment; work it defers is a bead.
```

### 7.3 · `prompts/06-review.md` — a fourth kind, and one sentence on `MAINT`

Replace "You report exactly three kinds of thing:" with "You report exactly
four kinds of thing:", and add after the third:

```markdown
- **Built and not promised** — code that no acceptance criterion, no
  `MAINT` concern and no decision needs: a re-implementation of what the
  repository already has (name the path), a helper more complex than the
  input it checks, a defence against an input that only a reviewed commit
  can bring, a `plan.md` longer than the diff outside `plans/` (give both
  counts). One row each: where, what to cut, what replaces it. Always
  `MINOR`, dimension `SPEC`, never a repair round of its own. A test the
  plan names and its planted fault are never this kind.
```

Append to the `MAINT` bullet: "A row that asks for more defence says where
the input crosses a trust boundary."

**On the licence:** the text above restates an idea in this repository's
words and copies no text, so MIT's notice duty should not apply. The
credit line is courtesy. This is an assessment, not legal advice.

## 8 · Not read or not verified

**Ponytail, not read:** `tests/`, `pi-extension/`, the adapters for other
hosts (`.opencode/`, `.cursor/`, `.kiro/` and the rest),
`docs/agent-portability.md`, `docs/cursor-hooks.md`, `examples/`, `i18n/`.
`hooks/ponytail-instructions.js` was not read; `ponytail-config.js` and
`ponytail-runtime.js` only searched for file writes, network calls and
child processes. Of the benchmark code, `run.py` was only searched for its
test metric; `tasks.py`, `judge.py` and `complete.py` were not read.

**Ponytail, not verified:** the benchmark numbers are as the authors report
them; their raw runs are not in the repository and nothing was re-run. The
independent benchmarks and issues #121 and #126 were not opened. The npm
package was not compared with the GitHub tree. How Claude Code updates a
marketplace plugin was not checked. The plugin was never installed, and no
hook was run.

**This repository:** the ladder ran over the code outside `plans/` of four
changes; for hermes-runner only the plan length was measured. Test files
were read by structure and by the ranges named in §3, not test by test.
The Markdown templates of template-bundle were not read for
over-engineering. The proposed prompt text was not tried on a real change.
CI was not run; `make verify` was run locally.

## Sources

Ponytail (`github.com/DietrichGebert/ponytail`, read through the GitHub
API at `552acd5`, 2026-10-05): `skills/ponytail/SKILL.md`, `AGENTS.md`,
`README.md`, `skills/ponytail-review/SKILL.md`,
`skills/ponytail-audit/SKILL.md`, `skills/ponytail-debt/SKILL.md`,
`commands/ponytail-review.toml`, `.claude-plugin/plugin.json`,
`.claude-plugin/marketplace.json`, `hooks/claude-codex-hooks.json`,
`hooks/ponytail-activate.js`, `hooks/ponytail-subagent.js`,
`hooks/ponytail-mode-tracker.js`, `package.json`, `INSTALL.md` (searched),
`benchmarks/README.md`, `benchmarks/agentic/README.md`,
`benchmarks/results/2026-06-18-agentic.md`,
`benchmarks/results/2026-06-16-robustness-audit.md`,
`benchmarks/results/2026-06-17-agentic-safety.md` (its table), the release
notes up to v4.13.0, and the repository metadata (stars, forks, commits,
contributors).

This repository, `main` at `d5813ec`: `prompts/03-plan.md`,
`prompts/04-implement.md`, `prompts/05-verify.md`, `prompts/06-review.md`,
`docs/WORKFLOW.md` (§2, model routing), `docs/governance/regelwerk.md`
(RB-G4), `tests/test_ci.py` (the ratchets), `provenance.yaml`,
`scripts/kit/manifest.yaml`, `scripts/check_research_currency.py`,
`tests/test_research_currency.py`, `scripts/plans_registry.py`,
`plans/changes/research-currency/` (spec, plan, findings).

Branches, at their heads on 2026-10-06: template-bundle `9c930e0`
(`tests/test_templates.py`, `templates/design.md`, `templates/findings.md`,
`plans/changes/template-bundle/decisions.md` and `findings.md`);
project-lock `a33e341` (`scripts/ci_gates.py`, `scripts/verify_all.sh`,
`pyproject.toml`, `tests/test_lock.py`, the added tests of
`tests/test_ci.py`, `plans/changes/project-lock/decisions.md`);
rb-m6-one-account `b5f8631` (`tests/test_repo_settings.py`,
`scripts/ramp_valves.py`, `decisions/gates.yaml`); hermes-runner `7beed6b`
(`plans/changes/hermes-runner/plan.md`, `prompts/research-recheck.md`).
