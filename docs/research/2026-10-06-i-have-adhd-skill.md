---
title: "The i-have-adhd skill against Coding Harness — what is covered, what to fold in, whether to install"
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
tags: [research, adhd, accessibility, communication, output-shape, claude-code, plugins, hooks, evals]
---

# The i-have-adhd skill against Coding Harness

## Result first

**Do not install the plugin. Fold five of its rules into `AGENTS.md` and the
maintainer's global `CLAUDE.md` instead.**

- **Most of it is already here.** Of 17 items (10 rules, 6 break rules, the
  pre-send check), 10 are covered, 6 partly, and 1 differs by design (time
  estimates; here the appetite is a stop and the clock is read, never
  estimated).
- **Five gaps are worth closing**, by benefit:
  1. Stop a debug spiral after three failed attempts.
  2. A pre-send check: first line, last line, no filler.
  3. Error reports that may say "cause not yet known".
  4. Lists: three for choices, five for everything else, the rest counted.
  5. "Step n of m" in multi-step work, for every harness.
- **The plugin as-is is the wrong carrier.** Its always-on hook puts about
  1,200 words of upstream text into every Claude Code session start, resume,
  clear and compaction, and an update changes that text without a review here.
  It also reaches only one harness, and four of its parts clash with how this
  repository works (§4).
- **Measuring output shape:** this repository already tests the shape of its
  templates. The plugin's model-judged A/B design is sound and reusable, but it
  costs model calls. First count real breaches, report-only (§6).

**Next step for the maintainer:** paste the German block in §7.2 into
`~/.claude/CLAUDE.md` (about two minutes). An agent may open the
`AGENTS.md` pull request (§7.1); the merge stays yours.

## 1 · Question and scope

On 2026-10-06 the maintainer asked to take the `i-have-adhd` skill into
account and to compare it with what Coding Harness already does to shape
agent output for a reader with ADHD.

Read on 2026-10-06, all as data, none as instructions:

- **The skill** ([ayghri/i-have-adhd][repo], MIT, © 2026 Ayoub Ghriss) at
  commit `839872f` (2026-09-19), plugin version 0.3.0, 53,914 stars when
  read: `skills/i-have-adhd/SKILL.md`, `README.md`, `INSTALL.md` (Claude Code
  part), `AGENTS.md`, `.claude-plugin/plugin.json`, `hooks/hooks.json`,
  `hooks/always-on.sh`, `hooks/always-on.mjs`, `evals/README.md`,
  `evals/rubric.md`, `evals/RESULTS.md`, `evals/cases.jsonl`, the one
  multi-turn scenario, `evals/runners.example.json`, and the blinding part of
  `scripts/judge.py`.
- **This repository** at `d5813ec` (`origin/main`, 2026-10-05):
  [`AGENTS.md`](../../AGENTS.md) ("Communication and session continuity"),
  [`docs/WORKFLOW.md`](../WORKFLOW.md) (question protocol, findings process,
  the five rules), [`prompts/03-plan.md`](../../prompts/03-plan.md) (plan
  card), [`prompts/04-implement.md`](../../prompts/04-implement.md) (appetite
  stop, `done:` and `Resume:` lines), both pull request templates,
  [`tools/claude-code/`](../../tools/claude-code/README.md) (README, the
  output text of `hooks/handover.sh` and `hooks/recap.sh`, the handover
  skill), the
  [ADHD frame note](2026-09-30-adhd-frame.md), the
  [decision pull request note](2026-09-30-decision-pull-requests.md#24-cognitive-accessibility-and-adhd)
  §2.4, `tests/test_pr_templates.py`, `tests/test_entry_points.py`,
  `tests/test_handover_entry.py` (docstring).
- **The maintainer's global rules** `~/.claude/CLAUDE.md`, section
  "Antworten ADHS-gerecht formulieren", read only.

Not read, not run: the skill's translations and its adapters for other
runtimes (Codex, Cursor, OpenCode, Pi, Gemini); its tests, including
`tests/test_always_on_hooks.py`; the internals of `run_evals.py` beyond its
README; the book it credits (*The Adult ADHD Tool Kit*, Ramsay and Rostain);
the video its README links; the current text of Claude Code's own system
prompt. Nothing was installed and no evaluation was run.

## 2 · What the skill is

**Ten rules.** Lead with the next action; number multi-step tasks; end with
one concrete next action; suppress tangents; restate state every turn; give
specific time estimates; make completed work visible; matter-of-fact tone for
errors; cap lists to five; no preamble, recap or closing pleasantries.

**Six break rules.** "Explain" requests may run long; a destructive action is
confirmed first; after three "still broken" turns, stop changing code and ask
one diagnostic question; real ambiguity gets one question; when a rule would
delete the answer, the task wins; inside an agent harness, the system prompt
outranks the skill.

**A pre-send check.** Delete an announcing first sentence, an "anything
else?" or recap last sentence, "by the way" sidebars, hedges that add no
information (keeping real uncertainty), and idioms. Then: do the first and
last lines tell what to do next and what just happened?

**Five premises** open the skill: small working memory, knowing is not doing,
starting is hardest, time feels uniform, visible progress matters. It gives no
source per premise; the credited book was not read here.

**How "always on" works in Claude Code.** The skill is not invoked by the
model (`disable-model-invocation: true`); the user types `/i-have-adhd`, and
"stop adhd mode" or "normal mode" turns it off. Always-on is opt-in: the user
creates the flag file `~/.claude/.i-have-adhd-always`. The plugin's
`SessionStart` hook (matcher `startup|resume|clear|compact`) runs
`node -e`, which loads `hooks/always-on.mjs`; that script checks the flag,
strips the frontmatter from `SKILL.md`, and prints a line beginning
"ADHD MODE ACTIVE (always-on)" followed by the full skill body as session
context. Every failure exits 0, so a missing Node silently turns it off.
`always-on.sh` and a PowerShell twin exist as fallbacks; `hooks.json` wires
only the Node command.

## 3 · The comparison

Status: **covered**, **partly**, or **different** (by design). "Here" names
where Coding Harness or the maintainer's rules carry it today.

| Skill item | Here today | Status |
|---|---|---|
| 1 Next action first | result first (`CLAUDE.md`); main point and next action (`AGENTS.md`); PR "In one line", "Your move" | covered |
| 2 Number steps | `CLAUDE.md`; PR "After the merge" | covered |
| 3 End with one next action | `CLAUDE.md`; `Resume:` line (04); handover "Next step" | covered |
| 4 Suppress tangents | "Nur das Nötige" (`CLAUDE.md`); `[GAP]` → explore; plan card "Not now" | covered |
| 5 Restate state | session-entry orientation; status line recap after every answer | partly |
| 6 Time estimates | appetite is a stop; time read from `date` (04) | different |
| 7 Show wins | changed behaviour; proposed, implemented, tested; `done:` line | covered |
| 8 Plain errors | four-line stop (04); "claim nothing unread" (`CLAUDE.md`) | partly |
| 9 Lists ≤ 5 | at most three priorities (`AGENTS.md`); three options per decision PR | partly |
| 10 No filler | implied by "result first"; no explicit list | partly |
| B1 Explain | headings in long answers (`CLAUDE.md`) | covered |
| B2 Destructive | merge ask in `.claude/settings.json`; `tools/bd` refusals; maintainer merges | covered |
| B3 Debug spiral | two `fix-r` review rounds escalate; appetite stop | partly |
| B4 Ambiguity | `[DECISION]` for two readings; one question at a time | covered |
| B5 Options are the answer | question form (02); decision PR options, recommended first | covered |
| B6 Harness wins | "the repository rules" (`CLAUDE.md`); house rules | covered |
| Pre-send check | result first and next step last, as rules, not as a check | partly |

Persistence, the skill's "rules do not lapse when the topic changes", is
structural here: the rules sit in files the harness loads as instructions.
Whether they are re-read after a compaction was not measured.

### What the partial rows lack, and what adopting would change

- **5 Restate state.** The recap line (`↻ Recap: Erledigt · Nächstes`) and
  `▶ Jetzt` restate state after every answer, but only on the maintainer's
  Claude Code display. A Codex or Omnigent session shows nothing. Inside an
  answer, nothing asks for "step n of m". Adopting: one line in `AGENTS.md`,
  and the harness's task list for multi-step work.
- **8 Plain errors.** The four-line stop covers a broken plan, not an error
  reported in conversation. The skill's own evaluation found its weak spot:
  the one consistent regression (`partial-success`, −0.63 over three trials)
  came with a grader note that the answer asserted a cause "without any
  evidence", and the evaluation names rule 8's "cause, then fix" as the
  plausible mechanism. Adopting: the shape *where · observed · cause · next
  step*, with "cause not yet known" allowed and a guessed cause forbidden.
  That joins the rule to "claim nothing unread".
- **9 Lists.** Three is the cap for priorities, options and decisions;
  nothing caps other lists (findings, files, beads in a message). Adopting:
  five per visible group for those, and the rest counted, never silently
  dropped (an unshown item must not read as "none").
- **10 No filler.** The rules imply it; nothing names the formulas, in either
  language. Adopting: an explicit list, German for the conversation, English
  for pull request texts and agent reports.
- **B3 Debug spiral.** Inside a change, time is bounded by the appetite and
  repair by the two-round escalation (`docs/WORKFLOW.md`, findings process).
  Outside a change, in plain conversation, nothing stops a loop of fixes.
  Adopting: after three failed attempts at the same symptom, no fourth fix;
  name the assumption that may be wrong, then one diagnostic step, or one
  question if the answer lies with the maintainer.
- **Pre-send check.** The rules say what the first and last line carry; no
  rule asks the agent to check before sending. Adopting: the check itself,
  short.

### Covered items with a small remainder, not proposed

- **3** sizes the next action ("under two minutes"); the `Resume:` line asks
  for one verb-first action naming its file or command, which serves the same
  end.
- **7** adds "try it": how the maintainer can see the result himself.
  Useful when there is something to look at; the evidence rule already names
  the command.
- **6** could be kept for the maintainer's own steps only ("reading this
  pull request: about five minutes"). No evidence was found that an agent
  estimates a human's time well; not proposed.

## 4 · Conflicts

1. **German conversation, English repository.** The skill's formula lists are
   English. In a German chat the model must transfer them, so a German list
   belongs in `CLAUDE.md` and an English one in `AGENTS.md`, for pull request
   texts and reports between agents.
2. **House rule 7, texts carry their own meaning.** Terseness can strip
   meaning: "Step 3 of 5 done" without naming the step fails house rule 7.
   "No recap" must not delete the closing message's proposed, implemented and
   tested line, or the handover and pull request links: that is evidence, not
   filler. Any adopted line keeps both.
3. **Three priorities against five list items.** Not a contradiction once
   split: three for what competes for a choice (the decision pull request note
   picked three over COGA's ceiling of five, for a phone), five for any other
   visible list.
4. **The first line.** The skill wants an action the reader can do. Here the
   agent acts and the maintainer mostly decides or does nothing, so the first
   line is the result and "Your move" or "Needed from you" follows. At session
   start the orientation (Where we are / Next step / Needed from you) comes
   first. An always-on skill would give the same line two instructions. The
   skill's own break rule 6 ("do the work instead of asking 'want me to'")
   points the same way as this repository.
5. **Time estimates against the appetite.** Here an estimate is replaced by a
   stop and by reading `date`, because time perception is measurably off and
   perceived speed misleads ([ADHD frame note](2026-09-30-adhd-frame.md),
   §2.1–2.2). Rule 6 is not adopted for agent work.
6. **An always-on hook beside Claude Code's system prompt.** The hook adds a
   third instruction source at `SessionStart`, beside the system prompt and
   the instruction files, and next to this repository's own entry hook. The
   skill yields to the system prompt (break rule 6) but says nothing about
   `AGENTS.md` or `CLAUDE.md`. How two `SessionStart` contexts are ordered was
   not measured.
7. **Installing into `~/.claude`.** Agents here never install there; the
   maintainer's display is installed from this repository, after
   `install.sh --check`. The skill's README install path is a prompt that
   tells an agent to install it, which is exactly the kind of instruction an
   agent here does not follow.
8. **Hidden mode state.** "stop adhd mode" turns the rules off for a session,
   and nothing on the display shows that. Small, but it is state the
   maintainer would have to remember.

No conflict: rule 7, "make completed work visible", asks for concrete
results, not streaks or counters, which the ADHD frame note lists as things
to avoid.

## 5 · Install the plugin, or fold the rules in?

**Fold the rules in. Do not install the plugin, neither on demand nor
always-on.**

1. **Little to gain.** Ten of 17 items are covered; the five gaps fit in
   about a dozen lines (§7).
2. **Unreviewed text in every session.** Always-on injects about 1,200 words
   from a third-party repository at every start, resume, clear and
   compaction, and `claude plugin marketplace update` changes them without a
   review here. This repository's own entry hook refuses the same pattern for
   cloned repositories: whoever controls the clone would control the session
   context (`tests/test_handover_entry.py`, docstring). Whether a Claude Code
   marketplace can be pinned to a commit was not verified.
3. **One harness.** A plugin reaches Claude Code; `AGENTS.md` reaches every
   harness that works here.
4. **Four conflicts** (§4, items 1, 4, 5 and 6) would need overrides anyway.
5. **Its own gate failed.** The skill's evaluation (2026-08-02, Claude Opus
   4.8, 14 cases, 3 trials) raised the weighted score from 4.045 to 4.473 and
   cut blockers from 7 to 3, but its release gate requires zero blockers and
   failed. Its one consistent regression is the guessed cause (§3, row 8).

If the maintainer wants to feel the difference first, he installs it himself,
on demand only (no flag file), for a few days, and compares. No agent here
installs it.

## 6 · Could Coding Harness measure its own output shape?

**How the skill measures.** Each case is a prompt with criteria; one
condition runs bare, the other with the skill injected. A model judge grades
every condition of a case in one call, blind: conditions are relabelled A, B,
C in an order derived from a hash of the case key, so a resumed run repeats
it. The rubric weighs correctness 35 %, autonomy 25 %, actionability 20 %,
safety and concision 10 % each. Two design points carry over directly:

- **Isolation.** Runs pass `--setting-sources ""`, because user-level hooks,
  plugins and memory would otherwise leak into the baseline. Here the
  maintainer's entry and recap hooks would leak the same way.
- **A pinned model** recorded with every published number.

**What this repository measures today.** The shape of its templates, not of
its messages: `tests/test_pr_templates.py` checks that the decision line comes
first, that there is one alert, and no table or checkbox. The plan and
handover validators check presence. No test sees what an agent actually wrote
into a pull request body or a chat.

**What it could do, in order of cost:**

1. **Report-only counts over written artefacts.** Merged pull request bodies
   and handovers are in git and GitHub: a script can check that line one is
   the "In one line" or decision line, that `done:` names a command, a result
   and a short commit, that `Resume:` is one verb-first action. No model call.
   This repository turns a rule into a check only after it has been broken
   twice, so it starts as a count, not a gate.
2. **A model-judged A/B for conversation shape,** only if a chat rule is
   broken twice and the counts cannot see it. German cases from real
   situations: session entry, appetite stop, red `make verify`, a debug
   spiral, a decision question, a partial success. It costs model calls and
   a budget. Its gate should be comparative: the skill's absolute "no
   blockers" rule, as its own results note, can never pass while one blocker
   survives anywhere.

## 7 · Proposed text

Proposed, not implemented, not tested.

### 7.1 For `AGENTS.md` (English)

Five bullets for "Communication and session continuity", after the bullet
that begins "Ask one decision at a time". `AGENTS.md` has 181 lines at
`d5813ec` against a budget of 200 (`tests/test_entry_points.py`); this block
adds 13.

```markdown
- Check a message to the maintainer before sending: the first line says what
  happened or was found, the last what happens next. Cut announcing openers,
  offers of more help, recaps, "by the way" asides, idioms and empty hedges;
  keep a hedge that carries real uncertainty.
- Cap lists: three priorities, options or decisions; five items in any other
  visible list, the rest counted ("4 more") and given on request.
- Report an error as where, what was observed, the cause and the next step.
  A cause no evidence shows yet is "cause not yet known", never a guess.
- After three failed attempts at the same symptom, make no fourth fix: name
  the assumption that may be wrong, take one diagnostic step, and ask only if
  the answer lies with the maintainer.
- In multi-step work, name the step ("step 2 of 4: schema migrated") in each
  progress report, and keep the steps in the harness's task list if it has one.
```

### 7.2 For `~/.claude/CLAUDE.md` (German, for the maintainer to paste)

Five bullets for the end of the section "Antworten ADHS-gerecht formulieren".
No agent writes that file.

```markdown
- **Vor dem Senden prüfen:** Die erste Zeile sagt, was passiert ist oder
  herauskam, die letzte, was als Nächstes passiert. Streichen: Ankündigungen
  („Gute Frage“, „Lass mich …“, „Ich schaue mir … an“), Schlussfloskeln
  („Ich hoffe, das hilft“, „Sag Bescheid, wenn …“), Wiederholungen,
  „übrigens“-Einschübe, Redewendungen und leere Abschwächungen. Echte
  Unsicherheit bleibt stehen.
- **Listen:** höchstens drei Prioritäten oder Optionen, sonst höchstens fünf
  Punkte. Den Rest zählen („4 weitere“), nicht stillschweigend weglassen.
- **Fehler sachlich:** wo, was beobachtet, Ursache und nächster Schritt. Ist
  die Ursache nicht belegt, heißt es „Ursache noch unbekannt“, nie geraten.
- **Keine Fehlersuche im Kreis:** Nach drei erfolglosen Versuchen am selben
  Symptom kein vierter Fix. Die Annahme nennen, die falsch sein könnte, einen
  Diagnoseschritt machen und nur fragen, wenn die Antwort bei mir liegt.
- **Bei mehreren Schritten:** in jeder Zwischenmeldung „Schritt n von m“ mit
  Namen des Schritts.
```

The two blocks say the same in two languages; `AGENTS.md` is the reference
when they drift.

## Sources

Read 2026-10-06 at commit `839872f` unless marked.

- **repo**: <https://github.com/ayghri/i-have-adhd> — MIT, © 2026 Ayoub
  Ghriss; 53,914 stars on 2026-10-06
- **skill**: <https://github.com/ayghri/i-have-adhd/blob/839872f/skills/i-have-adhd/SKILL.md>
- **hooks**: <https://github.com/ayghri/i-have-adhd/blob/839872f/hooks/hooks.json>,
  <https://github.com/ayghri/i-have-adhd/blob/839872f/hooks/always-on.mjs>,
  <https://github.com/ayghri/i-have-adhd/blob/839872f/hooks/always-on.sh>
- **evals**: <https://github.com/ayghri/i-have-adhd/blob/839872f/evals/README.md>,
  <https://github.com/ayghri/i-have-adhd/blob/839872f/evals/RESULTS.md>
  (run of 2026-08-02, Claude Code 2.1.220, `claude-opus-4-8`),
  <https://github.com/ayghri/i-have-adhd/blob/839872f/evals/rubric.md>
- This repository's notes: [ADHD frame](2026-09-30-adhd-frame.md),
  [decision pull requests](2026-09-30-decision-pull-requests.md)

[repo]: https://github.com/ayghri/i-have-adhd
