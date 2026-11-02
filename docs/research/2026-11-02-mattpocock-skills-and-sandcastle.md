---
title: "Evaluation — Matt Pocock's skills and Sandcastle, against the harness"
category: research
created: 2026-11-02
updated: 2026-11-02
last_reviewed: 2026-11-02
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-g4iq
tags: [evaluation, skills, review, sandbox, outside-practice]
---

# Matt Pocock's skills and Sandcastle, against the harness

The maintainer shared on 2026-11-02 the first email of a seven-part course
("AI Skills 1/7", AI Hero) that asks the reader to install a skill set and
then walks through `/grill-with-docs`, `/prototype` and `/handoff`,
`/to-spec` and `/to-tickets`, Sandcastle, `/code-review` and "the full loop",
and asked for a critical, technical reading of the mechanics behind it and of
how it could help here. Nothing was installed: the email's "go run it now" is
the course's instruction, not the maintainer's, and the machine's disk was
full that day. A first reading by the orchestrating session, not the research
swarm (see the sibling evaluation of the same day,
`2026-11-02-model-wiki-and-egm.md`).

## Sources and what was read

- **mattpocock/skills** (<https://github.com/mattpocock/skills>, MIT,
  created 2026-02-03, last push 2026-11-01, 309,735 stars on 2026-11-02),
  read through the GitHub API on 2026-11-02: the skills `grill-with-docs`,
  `grilling`, `domain-modeling`, `handoff`, `prototype`, `to-spec`,
  `to-tickets`, `code-review`, `implement`, and the scope notes
  `.out-of-scope/question-limits.md` and `native-question-tool.md`. Not read:
  the other skills (among them `tdd`, `triage`, `wayfinder`, the
  `in-progress` ones such as `software-factory`), the `docs/` pages, the ADRs.
- **mattpocock/sandcastle** (<https://github.com/mattpocock/sandcastle>,
  MIT, created 2026-03-17, last push 2026-11-02, 8,777 stars): the README and
  the guide pages on branch strategies, sandbox providers and iterations. Not
  read: the source code, its ADRs, the other guide pages.
- The course emails after the first were not read.

## What the skill set is, technically

- **Prompt text only.** Every skill is a `SKILL.md` of a few dozen to a few
  hundred lines; `grill-with-docs` is one line ("Call the Skill tool twice,
  for 'grilling' and 'domain-modeling'"). There is no validator, no gate, no
  runner, no recorded state between skills beyond what the agent writes to an
  issue tracker or `.scratch/`. Whether a step happened depends entirely on
  the model following text.
- **No behavioural tests.** The repository tree (2026-11-02) has no test
  directory; nothing checks what a skill makes a model do. EGM, by contrast,
  ships scenario tests per skill (sibling evaluation, row 8).
- **Popularity is not evidence.** 309,735 stars in nine months and a course
  with a certificate say how widely it is seen. The repository contains no
  measurement of effect.
- **Auto-invocation.** Of the nine skills read, `grilling`,
  `domain-modeling`, `prototype` and `code-review` carry no
  `disable-model-invocation: true` and may be triggered by the model on its
  own. Installed beside this harness, `code-review` takes the name of the
  Claude Code skill the maintainer already uses, and `handoff` writes its
  document to `$TMPDIR` — the opposite of house rule 5 (the handover is a file
  in the repository, delivered as a pull request).

## Skill by skill

| Skill | Mechanism | Against the harness on 2026-11-02 | Verdict |
|---|---|---|---|
| `grilling` (inside `/grill-with-docs`) | Decisions form a design tree; each round asks the whole **frontier** — every question whose prerequisites are settled — numbered, each with a recommended answer, "worded so 'yes' accepts" it. Facts are the agent's job, found by a fresh sub-agent without blocking the other questions. No cap on questions ("Codex just asked me 200 questions" was declined as a cap request). Ends when the frontier is empty | The interview (phase 1a) asks one question at a time with context (ADR 0018), for the maintainer's ADHD; `[GAP]` is explored, not asked — the same rule as "facts are the agent's job" | **Take two parts, reject one.** The frontier is a sound rule for *which* question comes next; "worded so yes accepts the recommendation" lowers the answer cost. Asking the whole frontier at once contradicts one question at a time and is rejected |
| `domain-modeling` | A `GLOSSARY.md` updated the moment a term is settled, free of implementation detail; an ADR only when a decision is (1) hard to reverse, (2) surprising without context and (3) the result of a real trade-off | No glossary file exists (searched by file name, 2026-11-02), although the maintainer's rules forbid internal terms without context and house rule 7 demands self-contained text. ADRs have no admission test; 23 are on `main` (0001-0023, 2026-11-02) | **Take both.** A glossary is the reference the paraphrase step (bead coding-harness-m1ba) and every answer to the maintainer can lean on. The three ADR criteria would sort decisions that need an ADR and a decision PR from those a bead note carries — fewer decision PRs, less attention |
| `prototype` | Throwaway code that answers one question; runs with one command; no persistence; state shown after each action; when done the prototype goes to a throwaway branch out of `main`, the verdict into the issue | A spike produces a research note; no rule says where spike code lives | **Take the capture rule** for spikes with code: code on a side ref or branch, verdict in the bead — the same pattern the night of 2026-11-01/02 arrived at for stopped attempts |
| `handoff` | Compacts the conversation into a file in `$TMPDIR`; names the skills the next session should load; references other artefacts instead of copying them | Handover is a repository file and a pull request; it carries more (decisions, parallel-session boundary, validation) | **Ours is stronger.** One point to check in our own practice: "do not duplicate content already captured in other artefacts" — the 2026-11-02 handover repeats lane status the tracker holds |
| `to-spec` | "Do NOT interview the user; just synthesize"; problem, solution, an "extremely extensive" list of user stories, implementation and testing decisions, out of scope; no file paths | Phase 2 demands acceptance criteria that can go red (the spec review's third question) and a settled interview | **Reject.** Volume of user stories is not precision, and a spec without refutable criteria fails exactly where the harness's spec review looks |
| `to-tickets` | Tracer-bullet vertical slices, each verifiable alone and sized to one fresh context window, with blocking edges; a wide refactor goes **expand–contract** (add the new form, migrate callers in batches, delete the old form) | Beads carry dependencies; pull requests are sliced at about 800 lines; `scripts/stage2.py` is a hot file that lanes B and C both change (night plan 2026-11-01, rule 3) | **Take expand–contract** for splitting the hot file: it keeps every batch green and lets two lanes land without merge order fights (bead coding-harness-32xf) |
| `code-review` | Two axes in parallel fresh sub-agents — **standards** (documented rules plus a fixed list of Fowler smells, always marked as judgement) and **spec** (missing, unasked-for, wrongly implemented; quote the spec line per finding) — reported side by side, never merged or re-ranked; the fixed point is validated before any sub-agent starts | The review loop gives other model families the diff without tools; phase 6 checks against the spec (`[DIVERGENT]` counts as a blocker); rows carry a dimension | **Mostly have it.** Two details worth taking: a spec finding quotes the spec line it rests on, and an unasked-for behaviour is its own finding type. The smell list is generic; the harness's own rules matter more |
| `implement` | TDD at agreed seams; type checks and single test files often, **the full suite once at the end**; then `code-review` | The repair prompt tells the model "You may run tests and `make verify`", and the runner runs `make verify` after each attempt. The round-4 repair of 2026-11-02 (two attempts) passed the verify lock **nine** times; on a machine whose disk and swap were full that day | **Take it — the most concrete gain.** The repairing model runs the named tests only; the runner alone runs the full suite, once per attempt. Fewer full runs, less memory and disk, and one fewer way for two lanes to compete |

## Sandcastle

`sandcastle.run()` starts one agent in a sandbox with a branch strategy and
merges its commits back. Mechanics worth knowing:

- **Native sandbox on macOS (Seatbelt).** The agent can write only the
  repository or worktree, the git directories Sandcastle mounts, a private
  temporary directory and a private home, both removed on close; the real
  home with `~/.claude`, `~/.codex` and `~/.config/gh` is hidden; only the env
  vars Sandcastle passes are visible; every process the agent started is
  killed when the sandbox closes (except one that leaves its process group).
- **Git hardening.** `.git/config`, hooks and `info` are mounted read-only,
  so `git config` without `--global` fails inside; host-side git commands
  ignore repository config that names a program.
- **Branch strategies.** `head` (write the working directory), `merge-to-head`
  (temporary branch, merged back, kept if a failed run left commits), and a
  named `branch` in a reused worktree.
- **Loop end by string.** An iteration loop stops when the agent prints
  `<promise>COMPLETE</promise>`.

Critique, measured against what the harness needs:

- **It does not solve the red-first interference** (bead
  coding-harness-wkxm): the sandbox shares the repository's `.git`, so a ref
  that another lane moves is still seen; only the private clone isolates refs.
- **It does not solve the path leak** (bead coding-harness-xul8): the
  repository appears "at its real host path", and the network is open.
- **The completion signal is a string the agent chooses to print.** The
  harness ends an attempt on post-run checks (`make verify`, red-first), which
  a model cannot fake by printing a word.
- **Seatbelt "doesn't promise to keep the agent away from your macOS
  Keychain"** — its own words.
- **What it would help with:** a stage-2 attempt that cannot write outside its
  worktree (the class of bead coding-harness-10w, a restore that wrote outside
  the worktree), a private temporary directory removed on close (on
  2026-11-02, 1.1 GB of pytest temporary directories had piled up under the
  user's `$TMPDIR`), and no stray processes after a stopped attempt (the
  orchestrator killed process groups by hand that day).

**Verdict:** no adoption of the library (TypeScript, and a second runner
beside `scripts/stage2.py`). A spike is worth it on the **mechanism**:
whether the runner's foreign-model calls and repair attempts can run under a
macOS Seatbelt profile (`sandbox-exec`) that allows writes only to the
worktree and a private temporary directory, and what that breaks.

## Recommendation

1. **Do not install the skill set** beside the harness: four auto-invoked
   skills, one name collision with an installed skill, a handoff that
   contradicts house rule 5, and a grilling mode that contradicts one
   question at a time.
2. **The repairing model runs the named tests only; the runner runs
   `make verify` once per attempt** — the concrete gain, measured.
3. **Question protocol:** the next question is one whose prerequisites are
   settled (the frontier), worded so that "yes" accepts the recommendation —
   a proposal for the maintainer, since it touches ADR 0018's protocol.
4. **A glossary** of the harness's own terms, and **three criteria for when a
   decision needs an ADR** — proposals.
5. **Expand–contract** as the way to split `scripts/stage2.py` (bead
   coding-harness-32xf).
6. **A spike on a Seatbelt profile** for stage-2 attempts.
7. **Not adopted:** `to-spec`'s no-interview synthesis, a handoff outside the
   repository, a completion signal as the end of an attempt, the library
   itself.

## Not done in this reading

Nothing was installed or run. No skill was tried on this repository; the
recommendations rest on the text of the skills and guides, and on the
harness's own logs of 2026-11-02.

## Beads (2026-11-02)

Existing beads checked first; three already held a point:

- The repairing model runs the named tests only — **already bead
  coding-harness-gxwg** (in progress since 2026-10-31, plan card waiting for
  the maintainer); the measurement and the repair prompt's own `make verify`
  permission were added as a note.
- Question frontier and yes-wording — new bead coding-harness-e4zd, linked to
  coding-harness-04xk (the same protocol; one decision PR for both).
- Glossary and three ADR criteria — new bead coding-harness-il3o, linked to
  the epic coding-harness-3ar and to the paraphrase step coding-harness-m1ba.
- Seatbelt spike — new bead coding-harness-nevd, linked to
  coding-harness-s9r (isolate each writing attempt).
- Expand–contract — notes on coding-harness-vg9 (split `stage2.py`) and
  coding-harness-32xf (hot files and merge order).
- Prototype as an interview option (course lesson 3, `prototype` capture rule) — new bead coding-harness-7izx.
