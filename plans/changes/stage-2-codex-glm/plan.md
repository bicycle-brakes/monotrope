---
title: "Plan — stage-2-codex-glm"
category: plan
status: draft
implementation_status: partial
date: 2026-09-30
created: 2026-09-30
last_reviewed: 2026-09-30
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-bc9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, codex, glm, leak-check, model-routing, adr]
---

# Plan — stage-2-codex-glm

Implements `spec.md` (criteria 1–72, as changed on 2026-09-30 by the
maintainer's answers 10–12). Stage 1: no model markings. Every new file
and sentence is English; existing German stays as it is (house rule 1).
Phase 4 runs on Sonnet 5.5 at effort `medium`; phase 6 of this change runs on
Opus 5.5 in a fresh session (answer 12; spec, "Order of work"), and says so
in `findings.md`, since the 2a reviewer's session cannot be resumed.

**No real call before the merge** (criterion 1): no step below starts `codex`
or `claude` against a model endpoint. Every test uses stand-ins; every
reading of a real program is `--help` or `--version`.

Written against `origin/main` at `ba940fb` (pull request #54). On
2026-09-30 `origin/main` held #54 and none of #55 (RB-M2 row), #56 (ADR 0008
and its pointers) or #57 (archive of two change folders); `ba940fb` is merged
into this branch (merge commit `7fd4e0f`).

Three slices, each one session that ends with `make verify` green, a commit
and a push:

| Slice | What | Estimate |
|---|---|---|
| 1 | the declaration, the resolver, the leak check | about 3 h |
| 2 | the runner, the loop prompt, the ask rule | about 4.5 h |
| 3 | doctrine, prompts, `AGENTS.md`, ADR 0007, the continuity chain | about 2.5 h |
| | **total** | **about 10 h** (9–11 h) |

The appetite is the maintainer's 9–11 h (answer 10), reached by dropping the
local proofs, not by cutting a slice. Nothing else is cut without the
maintainer. If slice 2 passes 5 h, the session stops after the verb it is
on, commits green, and reports; the remaining verbs open the next session.

## Decided in phase 3

No `[DECISION]` is open. Answers 10 and 11 removed the one that could have
arisen (a reviewer whose reads cannot be confined).

- `[GAP]`, closed by reading — **Codex CLI 0.159.2** (`--help`, 2026-09-30):
  `codex exec resume` has no `-s`, so the sandbox goes by
  `-c sandbox_mode="read-only"` on the first call and on every resume alike;
  `-m`, `-c`, `--disable`, `--json` and `-o` exist on both. The installed
  binary carries the names `sandbox_mode`, `model_reasoning_effort`,
  `hooks`, `memories` and `thread.started` (`strings`, 2026-09-30). Whether
  they take effect is not measured (answer 10).
- `[GAP]`, closed by reading — **Claude Code 2.1.285** (`--help`,
  2026-09-30): `--restricted` ignores user, project and local settings files
  (so the project's session-start hook does not load) and names Bash and
  WebFetch only if `--tools` does; `--tools Read,Grep,Glob` limits the
  built-in tools; `--append-system-prompt-file`, `--permission-mode dontAsk`,
  `--no-session-persistence` and `--strict-mcp-config` exist. `--bare` is not
  used: it takes only `ANTHROPIC_API_KEY` or an `apiKeyHelper`, and the
  configuration known to answer at Z.ai sets `ANTHROPIC_AUTH_TOKEN`
  (portfolio's GLM profile, research §8). `--restricted` also confines the
  file tools to the working directory by its help text; not measured, and
  not claimed (answer 11).
- `[GAP]`, closed by measuring — **the history scan costs little.** `git log
  --branches --remotes --cc -p --text` over this repository: 244 commits,
  about 58,000 lines, well under a second (2026-09-30).
- `[GAP]`, closed by reading — **two traps in the kit.**
  `tests/test_kit.py::test_the_kit_does_not_describe_the_phases` goes red when
  a file under `scripts/kit/` names five of the seven phase words.
  `manifest.yaml` names four already (spec, plan, verify, commit), so no new
  reason there may contain `review`, `implement` or `explore`; `probe.py`
  names four (spec, plan, review, commit), so no new comment there may
  contain `implement`, `explore` or `verify`. And
  `tests/test_ci.py::test_the_mutation_ratchet_only_turns_one_way` goes red
  when a test file with a mutation-named test (`refuses`, `is_caught`,
  `goes_red`, …) contains the text `plans_registry.py`: `test_stage2.py`
  imports the module as `plans_registry` and never writes that file name.
- `[DETAIL]` — **hooks and memories off stay as configuration.** Answer 10
  drops the proof, not the flags: they cost nothing, and memories could
  carry another session's reasoning into a reviewer meant to be fresh. The
  maintainer's veto is one word.
- `[DETAIL]` — **the model line of `02a-spec-review.md` and `06-review.md`
  keeps Fable 5.1 first**, with the Codex path after the dash. The kit's
  exception list keeps those two ids, and `gpt-6.1-sol` is resolved through
  the §4 routing rows (criterion 42).
- `[DETAIL]` — **every reviewer answers six cells**, `| ID | Severity |
  Dimension | Origin | Where | Finding |`; the runner adds `Reviewer`,
  `Status` and `Broke a test` (and `Phase 6` for loop rows). A reviewer
  cannot then mislabel itself, and one parser serves both programs.
- `[DETAIL]` — **the runner appends, never edits above.** Each call's rows
  go into a new block at the end of `findings.md`: a heading, a table, and
  the session or verdict line under it. The one exception is the `Phase 6`
  cells of the loop block, which `review` fills in the block it wrote.
- `[DETAIL]` — **loop rows get the runner's ids**, `L<round>-<n>`: the id
  carries the round (criterion 37), and Codex's marks map to unique ids.
- `[DETAIL]` — **a round is counted by its block.** A successful answer
  writes its round block to the loop record even with no row (the block
  says so); a failed call writes nothing. After a release, the line
  `Rounds run: <n>` under the released block keeps the count.
- `[DETAIL]` — **an undecided loop row holds the next round and the
  release.** A row's `Status` must begin `taken` or `rejected`, and a taken
  row's `Broke a test` must be `yes` or `no` (the Terms' "before the next
  round starts or the rows are released", which the measurement of the first
  three runs relies on).
- `[DETAIL]` — **the foreign environment is an allow-list**: `PATH`, `HOME`,
  `USER`, `LOGNAME`, `SHELL`, `TMPDIR`, `LANG`, `LC_ALL`, `LC_CTYPE`, `TERM`,
  `TZ`, and `CODEX_HOME` when set; then the call's own variables. For GLM:
  `ANTHROPIC_BASE_URL`, the key in `ANTHROPIC_AUTH_TOKEN` and
  `ANTHROPIC_API_KEY` (as the profile the proposal measured does),
  `glm-5.3` in `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`,
  `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`,
  `ANTHROPIC_SMALL_FAST_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL` (one model,
  one declaration check), a fresh empty `CLAUDE_CONFIG_DIR`, and
  `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` (with nobody signed in,
  Claude Code's own update and telemetry traffic has no business starting).
- `[DETAIL]` — **GLM's prompt travels as a file** outside the worktree,
  passed with `--append-system-prompt-file`; the diff can exceed what an
  argument list holds, and standard input must stay empty. The short user
  prompt names the change. Untracked files join the diff as
  `git diff --no-index /dev/null <file>`: a new test file is an uncommitted
  change too.
- `[DETAIL]` — **the leak check reads every file, whatever its suffix,**
  as UTF-8 with replacement characters, and a symbolic link as its target's
  text; merges are scanned with `--cc`, which shows what a merge adds beyond
  its parents. It never prints a match or a rule's pattern, and it reads
  its default paths at call time, so a test's `HOME` holds.
- `[DETAIL]` — **no timeout on a call.** A review at effort `max` takes as
  long as it takes; an interrupt ends it without a session line.
- `[DETAIL]` — **exit codes**: the runner 0 done, 1 a call failed, 2
  refused before any call; the leak check 0 clean, 2 a match or cannot
  measure (the port's vocabulary, `_verdict.py`).
- `[DETAIL]` — **§7 of `docs/WORKFLOW.md`**: the three stage-2 cells of the
  `.claude/` rows become "✅ unchanged". The decided stage 2 keeps Claude
  Code for every phase it ran; "rebuild" there would contradict §4 in the
  same file.

**Not now:** web search off for Codex (not asked for); a re-measurement
when a program's version changes (no measurement exists to repeat); the
criteria merge map of the 2a review (numbering kept).

## S0 · Before each slice

`git fetch origin`; if `origin/main` is not an ancestor of `HEAD`, `git
merge origin/main` (no rebase, no force push) and regenerate
`plans/INDEX.md`. If #56 has landed, slice 3's edits to `AGENTS.md` and
`docs/WORKFLOW.md` go in beside ADR 0008's pointers; ADR 0007 keeps its
number. Where a step names a file #57 moved to `plans/changes/archive/`, it
edits it there. If #58 (reviews on Opus 5.5 until stage 2 is live) has
landed, its interim rows in `docs/WORKFLOW.md` §3 and its model lines in
`prompts/02a-spec-review.md` and `prompts/06-review.md` are what slice 3
replaces: a conflict resolves toward this change's routing (answer 12), and
the kit keys of those two prompts go back to `Fable 5.1`.

## Slice 1 — the declaration, the resolver, the leak check

### Files

Changed:

- `model-endpoints.yaml` —
  - `claude-sonnet-5-5` added to the `modelle` of `anthropic-api` and
    `claude-code-plan`.
  - After `glm-coding-plan`, the endpoint `openai-codex`: `betreiber:
    OpenAI`, `residenz: anbieter-erklaert`, `abrechnung: abonnement`,
    `darf_sehen: [framework]`, `modelle: [gpt-6.1-sol]`, and an English
    `bemerkung`: Codex through the official Codex CLI only, signed in with
    the maintainer's ChatGPT subscription — any other way in is not covered;
    used for the spec review (phase 2a) and the review (phase 6) of `feature`
    and `architectural` changes, through `python3 scripts/stage2.py`; OpenAI
    states that it processes and stores personal-plan data in the United
    States and wherever its affiliates and service providers are, and
    personal plans get no region choice (search summaries of OpenAI's pages,
    2026-09-30).
  - `glm-coding-plan`'s `bemerkung` rewritten in English: Anthropic-compatible
    endpoint `https://api.z.ai/api/anthropic`, operated in China; used for
    the review loop before phase 6 (phase 4b) through `python3
    scripts/stage2.py review-loop`; only through Claude Code, which the
    vendor lists as a supported tool. No word of implementation or markings.
  - `kimi-code` removed from `endpunkte`; under `ausgeschlossen` a new entry:
    `was: "Kimi (Moonshot AI; models k3 and kimi-for-coding)"`, `klasse:
    framework`, `grund:` dropped by the maintainer on 2026-09-30 — stage 2
    reviews with Codex and GLM (ADR 0007).
  - The heading comment of the stage-2 block becomes English, because its
    meaning changes: "Stage 2 — other vendors review (docs/WORKFLOW.md §4,
    ADR 0007)". The German paragraph below it stays.
  - Under the German "Stand 2026-09-10" paragraph, an English paragraph:
    **2026-09-30, the ChatGPT subscription behind `openai-codex`**, declared
    personal use by the owner on the same terms — to be obtained again when
    the project is run commercially, `lakeswitch-ai` goes public, or a
    client pays for work that runs through this endpoint; the account's
    setting "Improve the model for everyone" as the maintainer read it, and
    the date read. The implementing session asks for that setting at the
    start of the slice (through the coordinating session). Until the answer
    is in hand, the sentence says "not read yet" — no value is guessed — and
    the pull request is not opened.
- `tests/test_model_endpoints.py` — English docstrings on new code only.
  - `_kandidaten(anzeige)` also returns the dot-keeping forms:
    `with_dots = anzeige.lower().replace(" ", "-")`, adding `with_dots`
    and `f"claude-{with_dots}"`. `_loest_auf` stays set equality.
  - A new `routing_models(text) -> list[str]` holds the table pattern
    `^\| \d[a-z]? [A-Za-z][A-Za-z ]*? \| \*\*([^*]+)\*\* \|` (re.M);
    `test_every_model_in_the_routing_table_resolves` calls it.
  - New tests, pure (no file read): `test_a_dotted_id_resolves_and_a_prefix_does_not`
    (`GLM 5.3`→`glm-5.3`, `gpt-6.1-sol`, `Sonnet 5.5`→`claude-sonnet-5-5`
    resolve; `GLM 5` against `{glm-5.3}` does not);
    `test_the_routing_check_reads_lettered_and_multi_word_rows` (a text with
    `| 2a Spec review | **k3** | x |` and `| 4b Review loop | **k3** | x |`
    yields `k3` twice; `| 1 | Explore | x |` yields nothing).
- `Makefile` — the stub becomes `python3 scripts/leakcheck.py --name
  "$(NAME)"`; its comment says it runs before a foreign call and never in CI.
- `scripts/ci_gates.py` — `OHNE_AUFRUFER["leakcheck.py"]`: "Run before every
  foreign call by scripts/stage2.py and by hand as make leakcheck; it needs
  the denylist each machine keeps outside the repository, which no CI step
  holds".
- `scripts/kit/manifest.yaml` — two `mechanismus` rules after
  `scripts/harness.py`: `scripts/leakcheck.py` ("the barrier before a
  foreign endpoint: scans the change, the tree and the history against a
  denylist each machine keeps outside the repository") and
  `tests/test_leakcheck.py` ("builds its own repositories and denylists;
  holds in the probe copy"). No `review`, `implement` or `explore`.
- `plans/changes/stage-2-codex-glm/spec.md`, `plan.md` —
  `implementation_status: partial`. `plans/INDEX.md` — regenerated.

Created:

- `scripts/leakcheck.py` — the port of portfolio's `scripts/leakcheck.py`
  (read at `5f99f0b`), in English, `from _verdict import Verdict`.
  - `default_denylist() -> Path`: `LEAKCHECK_DENYLIST`, else
    `Path.home() / ".config/cc-routing/denylist.txt"`, read at call time.
  - `read_denylist(path) -> tuple[list[Rule], str | None]`: `name = regex`
    per line, `#` comments, a bare line named `line-<n>`; missing,
    unreadable, no rule, or an invalid pattern (named by line number, never
    by its text) is a reason.
  - `check(name, denylist, root, prompt_texts=()) -> Result` with `Result
    (verdict, files, commits, rules)`. Refusals, each one BLOCK naming why:
    no name, or a name with `/` or equal to `.` or `..`; the denylist's
    reason; `plans/changes/<name>/` missing or without a file; `git -C root
    ls-files -z --cached --others --exclude-standard` failing ("the tree
    cannot be listed"); an unreadable file; `git log` failing ("the history
    cannot be read"). The scanned set, in this order:
    (a) every file under `plans/changes/<name>/`;
    (b) every listed path that exists on disk — a symbolic link as its
    target's text, a file as bytes decoded `utf-8` with `errors="replace"`
    — one count for (a) and (b) together, by relative path;
    (c) `git -C root log --branches --remotes --cc -p --text --no-color
    --no-ext-diff --no-textconv --format=commit%x00%H%n%B`, split at lines
    starting `commit\x00`, line numbers counted within each commit;
    (d) each `(label, text)` of `prompt_texts`.
  - A match: `verdict.block(f"{place} — rule '{rule}' matches (length
    {n})", "The matched text is not shown. Open the place, remove or replace
    the value, run the check again.")`, where the place is `<path>:<line>`,
    `commit <sha12>:<line>` or `prompt text <label>:<line>`. Clean:
    `verdict.info(f"leak check clean: {files} files, {commits} commits,
    {rules} rules")`, plus `, {n} prompt texts` when there were any.
  - `main(argv)`: `--name` (default `""`), `--denylist` (default
    `default_denylist()`), `--prompt-file PATH` (repeatable, labelled by its
    file name, unreadable → refusal), `--root` (hidden; default the
    repository); prints `verdict.render()`, returns `verdict.exit_code()`.
- `tests/test_leakcheck.py` — the tests in the table below. Temporary
  repositories with `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`
  and `-c user.name=t -c user.email=t@example.invalid -c
  commit.gpgsign=false`; an autouse fixture sets `HOME` and
  `LEAKCHECK_DENYLIST` under `tmp_path`. Mode-000 cases skip when
  `os.geteuid() == 0`.

### Steps

1. S0. Ask for the ChatGPT setting.
2. `model-endpoints.yaml`; the resolver and its two tests; the endpoint tests
   green.
3. `scripts/leakcheck.py` and `tests/test_leakcheck.py`; green.
4. `Makefile`, `OHNE_AUFRUFER`, the kit rules; `python3 scripts/kit/probe.py
   --list | grep leakcheck` names both files.
5. Plant each slice-1 fault of the mutation list, see its test red, restore
   (bytecode cache cleared, `PYTHONDONTWRITEBYTECODE=1`).
6. `make leakcheck NAME=stage-2-codex-glm` once, against the real denylist:
   record the three counts in the implementation notes. A match there is
   not a stop — it names a place, never the text, and it would refuse the
   first stage-2 run; report it.
7. `implementation_status: partial`; `python3
   scripts/check_frontmatter_current.py --stamp`; `python3
   scripts/plans_registry.py --index`; verification; commit; push.

## Slice 2 — the runner, the loop prompt, the ask rule

### Files

Created:

- `scripts/stage2.py` — `python3 scripts/stage2.py <verb> <change>
  [--root DIR]` (argparse, `allow_abbrev=False`; `--root` hidden, default the
  repository). Verbs `spec-review`, `review-loop`, `release-loop`,
  `review`. Constants: `CODEX = ("openai-codex", "gpt-6.1-sol", "max")`,
  `GLM = ("glm-coding-plan", "glm-5.3", "max")`, `GLM_BASE_URL =
  "https://api.z.ai/api/anthropic"`, `CODEX_ASK_RULE = ("Bash(codex *)",
  "codex typed directly skips the leak check and the declaration; the runner
  is the way in")`, `READ_REQUEST` ("Read nothing outside this worktree and
  the repository's git directory."), `ANSWER_FORMAT` (the six cells; one
  sentence when there is no finding), `MARK_FORMAT` (`<ID>: agree` or `<ID>:
  disagree — <reason>`, one line per loop row). Every prompt the runner
  builds ends with `READ_REQUEST`.
  - **Shared, in this order, before every call:** the change named and
    `plans/changes/<change>/` a directory (15); `spec.md` with a `bead` in
    its header (else refused: `findings.md` could not get its header); the
    endpoint in `model-endpoints.yaml` exists, lists the model, has
    `framework` in `darf_sehen` and `residenz` other than `nicht-erklaert`
    (17); the prompt built — the phase prompt file in full, the change's
    name, `ANSWER_FORMAT`, `READ_REQUEST`; `leakcheck.check(change,
    leakcheck.default_denylist(), root, [("prompt", prompt)])` in-process,
    immediately before this call (16) — not clean: its report printed, exit
    2; then `findings.md` created if missing and its call line appended (21);
    then the call, `stdin=subprocess.DEVNULL` (19), `cwd=root`, the
    allow-list environment (18). Any refusal exits 2 and starts nothing.
  - **`findings.md` created by the runner** (21): header `title: "Findings
    — <change>"`, `category: findings`, `status: draft`,
    `implementation_status: none`, `date`, `created`, `last_reviewed` and
    `updated` today, `supersedes: null`, `superseded_by: null`, `bead` from
    `spec.md`, `owner: Data Architect`, `provenance: ai-drafted-reviewed`,
    `produced_by: {kind: llm-session, name: <codex or claude-code>, version:
    "<today>"}`, `review: {status: pending, approved_by: null, approved_at:
    null}`, `tags: [findings, stage-2]`; body `# Findings — <change>`.
  - **The call line** (21): `Stage-2 call, <date>: <verb> · endpoint
    <endpoint> · model <model> · leak check clean over <f> files, <c>
    commits, <r> rules.`
  - **Codex** — `codex exec --json -m gpt-6.1-sol -c
    model_reasoning_effort="max" -c sandbox_mode="read-only" --disable hooks
    --disable memories -o <tmp>/answer.md <prompt>`; a resume is `codex exec
    resume <id>` with the same options before the prompt; never
    `--ephemeral` (23, 24). `<tmp>` is a temporary directory outside the
    worktree. The thread id is the `thread_id` of the first JSON line with
    `"type": "thread.started"`; none, or a non-zero exit, fails the call:
    exit 1, the program's standard error printed (last 40 lines), no rows
    and no session line (27).
  - **Rows** — `parse_rows(answer) -> (rows, rest)`: a line whose stripped
    form starts and ends with `|` and splits into exactly six cells, other
    than the header (`ID`) and the separator, is a row. When the answer is
    not only rows and blank lines, the whole answer is appended after the
    table under "The answer below was not only rows; it is kept as it came."
    An answer with no row keeps its text the same way.
  - **`spec-review`** (23, 25, 26): a fresh Codex call with
    `prompts/02a-spec-review.md`; appends `## Phase 2a — Codex, <date>`, the
    table `| ID | Severity | Dimension | Origin | Where | Finding | Reviewer
    | Status | Broke a test |` with `Codex`, `open`, `—` in the last three
    cells, then `Reviewer session: codex <thread id>`.
  - **`review`** (25, 28–31): refused while a loop row is undecided. The
    session is the last `Reviewer session: codex <id>` line of
    `findings.md`: present, the call resumes it; absent, a fresh call. Prompt:
    `prompts/06-review.md` in full, then "Write only your verdict now." —
    no loop row. Appends `## Phase 6 — Codex, <date>`, the table, and
    `Phase 6 verdict: codex <thread id>, <date>`; when no session was
    recorded, or the resumed thread id differs from the recorded one, also
    `Reviewer session: codex <thread id> — a fresh session reviewed: <no
    phase-2a session was recorded | the resume of <old> started a new
    thread>`. Then the release (below). With loop rows released, a second
    call resumes the verdict's thread, prompt = `MARK_FORMAT`, "Your verdict
    stands and is not changed.", and the released rows; its own leak check
    and call line first. Each `<ID>: agree|disagree …` line fills that row's
    `Phase 6` cell (`agree`, or `disagree — <reason>`); a row without a line
    gets `no answer`. The verdict block is not touched. A failed second call
    exits 1 and leaves the `Phase 6` cells `—`.
  - **`review-loop`** (32–37): refused when two rounds have run — the round
    blocks in the loop record plus every `Rounds run: <n>` in `findings.md`
    — or while a row of the record is undecided; refused without `GLM_KEY`
    in the secrets file (`CC_SECRETS`, else
    `~/.config/cc-routing/secrets.env`; lines `KEY=value` or `export
    KEY=value`, quotes stripped, nothing evaluated). The diff:
    `git merge-base HEAD origin/main` (missing → refused), `git diff <base>`,
    then each untracked, not ignored file as `git diff --no-index --
    /dev/null <path>`. The prompt file (`<tmp>/glm-prompt.md`):
    `prompts/04b-review-loop.md` in full, `ANSWER_FORMAT`, `READ_REQUEST`,
    the diff. Call: `claude -p "Review the change <change> as the appended
    instructions say." --append-system-prompt-file <tmp>/glm-prompt.md
    --model glm-5.3 --effort max --tools Read,Grep,Glob --restricted
    --strict-mcp-config --permission-mode dontAsk --no-session-persistence
    --output-format text`. Exit 0: the answer, credential scrubbed, goes to
    the loop record as `## Round <n> — GLM, <date>` with the table `| ID |
    Severity | Dimension | Origin | Where | Finding | Reviewer | Status |
    Broke a test |`, ids `L<n>-<k>`, `GLM`, empty, empty; no row → the block
    says "GLM reported no finding." Non-zero: exit 1, nothing written to the
    record.
  - **The loop record**: `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/<change>/loop.md`,
    opening with two lines for the implementer: write `Status` (`taken —
    <test or criterion>` or `rejected — <reason>`) and, for a taken row,
    `Broke a test` (`yes` or `no`) before the next round or the release.
  - **`release-loop`** (38, 39): refused, changing nothing, without a line
    matching `^Phase 6 verdict: \S+ \S+, \d{4}-\d{2}-\d{2}$` in `findings.md`
    or while a row is undecided; no record → appends "Loop rows: none — the
    GLM loop did not run for this change." once. Otherwise appends `## Phase
    4b — GLM loop rows, released <date>`, one table with the column `Phase
    6` added (`—`), every row as the record holds it, `Rounds run: <n>`, and
    any kept prose; then removes the record directory. `review` calls the
    same function.
  - `scrub(text, secret)` replaces the key in everything the runner prints
    or writes (20). `codex_rule_problems(settings) -> list[str]`: the rule
    missing from `permissions.ask`, or a `deny` or `allow` rule that covers
    `Bash(codex exec x)` (`merge_guard.covers`) (61).
- `tests/test_stage2.py` — the tests in the table. Fixtures: `repo` (a
  temporary git repository with `plans/changes/demo/spec.md` carrying
  `bead: demo-1`, copies of the real `prompts/*.md` and
  `model-endpoints.yaml`, one commit, `refs/remotes/origin/main` set by
  `git update-ref`); `stand_ins` (a `bin/` holding `codex` and `claude`
  written from one template with `#!<sys.executable>`, importing only
  `json`, `os`, `sys`, `pathlib`: each appends a record — argv, environment,
  cwd, whether fd 0 is `/dev/null`, the listing of `CLAUDE_CONFIG_DIR`, the
  text of an `--append-system-prompt-file`, the worktree paths that contain
  a scenario's marker — to `calls.jsonl`, may plant a file, prints the
  scenario's canned JSON lines or text, writes `-o`, and exits with the
  scenario's code; a `gitbin/` holding only a link to `git`); `env`
  (monkeypatched `PATH=<bin>:<gitbin>`, `HOME`, `XDG_STATE_HOME`,
  `CC_SECRETS` with `GLM_KEY=<test key>`, `LEAKCHECK_DENYLIST` with one
  rule, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`; and the
  caller's `GH_TOKEN`, `OPENAI_API_KEY`, `X_SECRET`,
  `ANTHROPIC_MODEL=caller-model`, `ANTHROPIC_BASE_URL=http://caller.invalid`).
  The runner runs in-process through `stage2.main([... , "--root",
  str(repo)])`. `import plans_registry` for criterion 21; the file name
  `plans_registry.py` never appears in the file.
- `prompts/04b-review-loop.md` — `# Phase 4b · Review loop`; `**Model:**
  GLM 5.3 — at effort `max`, through Claude Code against Z.ai; started only
  by `python3 scripts/stage2.py review-loop <change>`.` `**Input:**` the
  change's diff against its merge base with `origin/main`, uncommitted
  changes included, and this text — the runner puts both in the prompt.
  `**Result:**` rows for the loop record, outside the repository until the
  phase-6 verdict. `**Gate:**` at most two rounds, `make verify` green after
  each repair. For the reviewer: the house rules it needs because it may not
  read `AGENTS.md` (every row in English; no customer name, schema, entity or
  figure; a finding reads without the spec beside it; read nothing outside
  the worktree); what to report (phase 6's three kinds, dimensions `SPEC`
  and `MAINT`, severities `BLOCKER`, `MAJOR`, `MINOR`); the six-cell answer,
  or one sentence when nothing is found. For the implementer: the evidence
  rule in the words of criterion 47; `Status` and `Broke a test` written in
  the loop record before the next round or the release; loop rows never
  copied into the worktree; round 2 only after the repair and `make verify`
  green. About 45 lines.

Changed:

- `.claude/settings.json` — `"Bash(codex *)"` appended by hand after
  `mcp__*__merge_pull_request`; then `python3 scripts/omnigent_policy.py
  --write` (it keeps the rule, Omnigent's ask rule last) and `--check`
  silent; `tools/omnigent/policy.yaml` without a diff.
- `scripts/ci_gates.py` — `OHNE_AUFRUFER["stage2.py"]`: "Entry point, not a
  gate — starts the stage-2 reviewers on the maintainer's machine, with a
  subscription and a credential no CI step holds; tests/test_stage2.py runs
  it against stand-ins".
- `scripts/kit/probe.py` — `REIST_NICHT` gains
  `"tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[04b-review-loop.md-GLM 5.3]": "bestand-dieses-repos"`;
  `DECKEL = 32`, its trailing comment "raised again on <date> (31 -> 32)",
  and a comment line: the loop prompt `prompts/04b-review-loop.md` came along
  (plans/changes/stage-2-codex-glm); a prompt with a model line is one case
  more, red in the throwaway repo for the reason the other prompt cases are:
  `model-endpoints.yaml` stays home. No `implement`, `explore` or `verify`.
- `plans/INDEX.md` — regenerated.

### Steps

1. S0.
2. `stage2.py` preconditions, environment, leak gate, `findings.md` and the
   call line, with their tests (15–21, 2, 3).
3. `spec-review`, then `review` without loop rows (22–29).
4. `prompts/04b-review-loop.md`, the kit entry; `review-loop`,
   `release-loop`, then `review` with loop rows (30–39).
5. The ask rule, `--write`, `--check`, its tests (61); `OHNE_AUFRUFER`.
6. Plant each slice-2 fault of the mutation list, see red, restore.
7. Stamp, index, verification, commit, push.

## Slice 3 — doctrine, prompts, ADR 0007, continuity

### Files

Created:

- `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` — in the form of ADR
  0008 (`provenance: human-decided`, `status: accepted`, `review: {status:
  pending, approved_by: null, approved_at: null}`; "Status: accepted by the
  merge of the pull request that carries this file"; "amends D-13 of the
  2026-09-16 interview"; date 2026-09-30). Sections: **Context** (D-13's four
  criteria and their state on 2026-09-30, research §4; the maintainer's
  routing of 2026-09-30); **Decision** — (1) D-13 amended as answer 1 says:
  criteria 3 and 4 stay and the runner enforces them on every call,
  criterion 2 governs lakeswitch-ai's content, criterion 1 is replaced by
  measuring the first three stage-2 runs with the stop rule, the accepted
  loss is the measured stage-1 baseline (62); (2) framework content — this
  repository's tree, as the class `framework` of `model-endpoints.yaml`
  defines it — may flow to `openai-codex` through the official Codex CLI and
  to `glm-coding-plan` through Claude Code, nothing else and nowhere else;
  lakeswitch-ai's own trees are not sent and their disclosure decision stays
  theirs (63); (3) Kimi is dropped (64); (4) the reviewers' reads are not
  confined — they can read the whole disk, the customer checkout included;
  the prompts ask them not to, a request and not a lock; accepted by the
  maintainer as a residual risk on 2026-09-30 (22); **Options considered**
  (research's three: amend, build now and switch on later, run without
  touching D-13); **Consequences**, ending with: it does not enter M2, the
  Omnigent milestone for cross-vendor operation, whose further entry
  conditions nobody was asked about (65). About 90 lines; it names `D-13`.
- `tests/test_stage2.py` — the doctrine tests of the table, added to the
  file of slice 2.

Changed:

- `docs/WORKFLOW.md` —
  - Header: "**Standing:** stage 1 is binding; stage 2 is active for
    framework content, by change class, since ADR 0007 (§4); stage 3 is
    not." (52) The list "Not all of it is here yet" loses
    `templates/plan-marking.md`, `scripts/run_change.sh`, the
    `scripts/cc-*.sh` profiles and `tests/test_model_profiles.py`; its
    "Checked on" gets the date and commit of this slice. Each remaining
    entry is checked absent from the tree and named elsewhere in the file
    (53).
  - §2 phase table: after row 4, `| 4b | Review loop *(stage 2)* | the loop
    rows — outside the repository until the phase-6 verdict, then in
    findings.md (release-loop) | at most two rounds; make verify green after
    each repair | [04b-review-loop.md](../prompts/04b-review-loop.md) |`, the
    cells formatted as the neighbours are (46).
  - §2 "The findings process": the evidence rule and its consequence, in the
    words of criterion 47.
  - §3 routing table: `| 4 Implement | **Sonnet 5.5** | effort medium; a
    solid worker given a clear plan |` (43); the rows `2a Spec review` and
    `6 Review` on **Fable 5.1** (replacing #58's interim Opus 5.5 rows if
    they stand). The paragraph "Spec review and review on Fable 5.1" (or
    #58's interim paragraph, replaced) says: Fable 5.1, except the `feature`
    and `architectural` changes §4 routes to Codex (44); one sentence:
    implement on Sonnet 5.5 at effort `medium`, for every change
    (maintainer, 2026-09-30). "One reviewer for both" gains: for Codex, the
    runner resumes with `codex exec resume`.
  - §4 rewritten, title "## 4 · Stage 2 — Codex and GLM review (active for
    framework content)": the class table with its caveat (40, 41); the
    routing rows in §3's form, `| 2a Spec review | **gpt-6.1-sol** | effort
    max, through the Codex CLI and the runner |`, `| 4b Review loop | **GLM
    5.3** | effort max, through Claude Code against Z.ai and the runner |`,
    `| 6 Review | **gpt-6.1-sol** | effort max; the same Codex session as
    2a, resumed |` (42); why across vendors (the present paragraph, Kimi
    replaced by the decided pair); the runner as the only way — its four
    verbs, a green leak check and a clearing declaration before every call,
    what every call carries, the ask rule on `codex` as a brake (45); reads:
    the prompts' request and the plain sentence that it is a request, not a
    lock, and that the reviewers can read the rest of the disk, the
    customer checkout included (22); the loop — rounds, the loop record
    outside the repository, the implementer's `Status` and `Broke a test`
    there, the release after the verdict, the `Phase 6` marks; the columns
    `Reviewer` and `Broke a test` and their meaning (49); measuring the
    first three stage-2 runs and the stop rule (50); the two caveats, the
    last sentence now "the leak check runs before every call". Gone: the six
    profiles, `run_change.sh`, the plan markings, "Seeing agents that wait"
    (51). Every verb, option and variable named exists (51).
  - §6: the two-to-three-weeks signal stated as the original one, and "ADR
    0007 opened stage 2 for framework content with the first three stage-2
    runs measured in its place (§4)" (54).
  - §7: the stage-2 cells of `.claude/agents/`, `.claude/commands/` and
    "Claude Code hooks" read "✅ unchanged".
- `prompts/02a-spec-review.md` — model line: `Fable 5.1 — for a spike or
  bounded change, …; for a feature or architectural change gpt-6.1-sol at
  effort max, started by python3 scripts/stage2.py spec-review <change>`;
  the `Session` line gives both paths (the runner writes `Reviewer session:
  codex <thread id>`); one sentence: through the runner, answer in the six
  cells, the runner adds the rest (55).
- `prompts/06-review.md` — the same two paths (`python3 scripts/stage2.py
  review <change>` resumes); a paragraph "**Verdict first.**": write the
  verdict, ending with `Phase 6 verdict: <reviewer> <session>, <date>` under
  the table, before reading any loop row; then, on the Fable path, `python3
  scripts/stage2.py release-loop <change>` and each loop row's `Phase 6`
  cell marked `agree` or `disagree — <reason>`; on the Codex path the runner
  does both (56). A change that ran stage 2 has the columns `Reviewer` and
  `Broke a test` (§4).
- `prompts/04-implement.md` — model line `Sonnet 5.5 — at effort medium
  (claude --model claude-sonnet-5-5 --effort medium); a solid worker given a
  clear plan.` (57); a paragraph with the evidence rule and a pointer to
  `04b-review-loop.md` (48).
- `prompts/03-plan.md` — the section "Model markings (stage 2 only)" goes
  (58).
- `prompts/02-spec.md` — "**Acceptance criteria.** Checkable sentences, one
  condition each; where a trigger, a state or a failure applies, the
  sentence begins with When, While or If. Each one comes with what would
  *refute* it. A criterion that cannot go red is not one." (59)
- `AGENTS.md` — the one-screen table gains `| 4b | Review loop *(stage 2)*
  | loop rows, into findings.md after the phase-6 verdict | at most two
  rounds, make verify green after each repair |`; under the table: "**Stage
  2** (framework content, by change class, ADR 0007): a foreign reviewer —
  Codex or GLM — is started only through `python3 scripts/stage2.py`, which
  runs the leak check before every call." At most 200 lines (60).
- `scripts/check_decision_continuity.py` — `AMENDMENT_ADRS["D-13"] =
  ("0007-stage-2-reviews-by-codex-and-glm.md",)` (66).
- `docs/architecture/2026-09-17-omnigent-first-target.md` — the D-13 row:
  "Amend", the old text kept, then "Amended by ADR 0007 (2026-09-30): for
  framework content, the leak check and the declared endpoint hold on every
  call; criterion 2 governs lakeswitch-ai's content; three measured stage-2
  runs replace the three qualification runs; M2 is not entered." (67); a
  note "> **Changed, 2026-09-30.** [ADR 0007](…) amends D-13 …" after the
  note of 2026-09-27 (68).
- `docs/architecture/2026-09-17-implementation-plan.md` — the same dated
  note before "Read this first" (68).
- `scripts/kit/probe.py` — the key `[04-implement.md-Sonnet 5]` becomes
  `[04-implement.md-Sonnet 5.5]`.
- `plans/INDEX.md` — regenerated.

### Steps

1. S0.
2. The prompts and the probe key; `tests/test_model_endpoints.py` green.
3. `docs/WORKFLOW.md`, `AGENTS.md`.
4. ADR 0007, the map, the two architecture documents;
   `python3 scripts/check_decision_continuity.py` exits 0.
5. The doctrine tests; the slice-3 faults of the mutation list.
6. Read §4, the header list, §6 and §7 once against the tree (51, 53).
7. Stamp, index, verification, commit, push.

## Phase 7 — the pull request

1. Criterion 1: `grep -rl "worktrees/stage-2-codex-glm" ~/.codex/sessions`
   prints nothing, and
   `${XDG_STATE_HOME:-$HOME/.local/state}/coding-harness/stage2/stage-2-codex-glm`
   does not exist. Both results go into the pull request body.
2. The ChatGPT setting is filled (criterion 8); otherwise the pull request
   waits.
3. A decision pull request (69): title `decide(stage-2): Codex and GLM
   review framework changes before the merge, D-13 amended (ADR 0007)`,
   label `decision`, body beginning with the block of
   `.github/PULL_REQUEST_TEMPLATE/decision.md`. It names bead
   coding-harness-bc9 (worked on) and coding-harness-kw0 (its re-scoping is
   the tracker writer's). No tracker write here.

## Verification command

Where `python3` lacks PyYAML, put
`/Users/mikypiky/.venvs/portfolio-agentic-engineering/bin` first on `PATH`;
where the signing key is locked, prefix the `GIT_CONFIG_*` variables shown.

```sh
python3 -m ruff format --check scripts/ tests/ && python3 -m ruff check scripts/ tests/
python3 -m pytest tests/test_model_endpoints.py tests/test_leakcheck.py tests/test_stage2.py tests/test_merge_guard.py tests/test_omnigent_deny_layers.py tests/test_kit.py tests/test_ci.py -q
python3 scripts/omnigent_policy.py --check
python3 scripts/check_decision_continuity.py
python3 scripts/kit/probe.py --list | grep -c leakcheck
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
```

Expected after slice 3: every test passes, `2` from the probe listing,
`VERIFY GREEN`. After slice 1: without `tests/test_stage2.py`. After slice
2: the continuity check as on `main`.

## Test per criterion

`L` = `tests/test_leakcheck.py`, `S` = `tests/test_stage2.py`, `M` =
`tests/test_model_endpoints.py`. "Review" means the phase-6 reviewer holds
it against the named text.

| # | Test | Fault that turns it red |
|---|---|---|
| 1 | Phase 7, step 1 | a Codex session file with this worktree's path, or a loop record, before the merge |
| 2 | S `test_the_runner_finds_only_stand_ins` (each `PATH` entry: a `codex` or `claude` there carries the stand-in marker); S `test_a_stand_in_contacts_nothing` (its imports) | a directory with the real program on the path; a network import |
| 3 | L and S `test_the_suite_never_reaches_the_real_denylist_or_secrets` (defaults resolve under `tmp_path`) | a default read at import time, or a hard-coded home |
| 4 | M `test_every_endpoint_states_…` as it stands; S `test_openai_codex_is_declared_as_decided` | a value missing or different; `kundencode` seen |
| 5 | S `test_kimi_is_excluded_not_declared` | an endpoint naming Moonshot, `k3` or `kimi-for-coding`; no dated entry |
| 6 | M `test_every_model_in_a_phase_prompt_resolves[04-implement.md-Sonnet 5.5]` | `claude-sonnet-5-5` missing from either endpoint |
| 7 | S `test_the_glm_remark_names_the_review_loop` (no `implement`, `Umsetzung`, marking) | the old remark |
| 8 | review against the maintainer's statement | the setting missing or unsupported |
| 9 | M `test_a_dotted_id_resolves_and_a_prefix_does_not`; M `[04b-review-loop.md-GLM 5.3]` | dots dashed only; substring match |
| 10 | M `test_the_routing_check_reads_lettered_and_multi_word_rows` | the single-digit, one-word pattern |
| 11 | L `test_a_match_anywhere_in_the_scanned_set_goes_red` — change file, uncommitted edit, untracked file, commit message, an earlier commit's patch, a commit only on `refs/remotes/origin/side`, prompt text | any place skipped |
| 12 | L `test_a_check_that_cannot_measure_refuses` — denylist missing, empty, mode 000, invalid pattern; no name; folder missing, empty; mode-000 file; not a repository — exit 2 and the reason | exit 0 or a silent refusal |
| 13 | L `test_the_report_never_carries_the_match` (32 seeded letters, CLI; no 8-gram in stdout or stderr; place, rule, length present; the pattern text absent) | the match or its pattern printed |
| 14 | L `test_a_clean_tree_passes_and_names_its_counts` (exact numbers) | a count missing or wrong |
| 15 | S `test_no_change_or_a_missing_folder_refuses_every_verb` | a recorded start |
| 16 | S `test_a_leak_refuses_the_call`; S `test_each_call_runs_its_own_leak_check` (the verdict call's stand-in plants a match; the mark call does not start) | a start after a match; one check for two calls |
| 17 | S `test_an_endpoint_the_declaration_does_not_clear_refuses` — missing, model absent, no `framework`, `nicht-erklaert`; both vendors | a recorded start |
| 18 | S `test_the_foreign_environment_is_the_runners` | a caller's `*_KEY`, `*_TOKEN`, `*_SECRET`, `ANTHROPIC_MODEL` or `ANTHROPIC_BASE_URL` seen |
| 19 | S `test_every_call_gets_an_empty_standard_input` | stdin inherited |
| 20 | S `test_the_glm_credential_never_leaves_the_runner` (stand-in echoes the key to stdout and stderr, exit 0 and 1) | 8 characters of it in output, `findings.md` or the record |
| 21 | S `test_every_call_leaves_its_line_in_findings`; S `test_a_findings_file_the_runner_creates_has_a_registry_header` (`plans_registry._frontmatter`, `REQUIRED`, `STATUS`, `IMPLEMENTATION`); S `test_a_spec_without_a_bead_refuses` | no line; a header field missing; a call without a bead |
| 22 | S `test_every_prompt_asks_to_read_nothing_outside` (each call); review of §4 and ADR 0007 | the request missing; a "confined" claim |
| 23 | S `test_codex_is_pinned_on_first_and_resumed_calls` | `-m`, effort or sandbox missing; `--ephemeral` |
| 24 | S `test_codex_runs_with_hooks_and_memories_off` | a `--disable` missing |
| 25 | S `test_the_codex_prompt_carries_its_phase_prompt_in_full` | the prompt file or the change's name absent |
| 26 | S `test_the_spec_review_answer_lands_as_codex_rows_with_its_session`; S `test_an_answer_that_is_not_rows_is_kept` | fewer than three `Codex` rows; another id; text dropped |
| 27 | S `test_a_failed_codex_call_writes_no_session_line` (no `thread.started`; exit 1) | a session line; exit 0 |
| 28 | S `test_review_resumes_the_recorded_session` | `exec` without `resume <id>` |
| 29 | S `test_a_fresh_phase_6_session_says_so` (none recorded; a different resumed id) | silence |
| 30 | S `test_no_loop_row_reaches_the_verdict_call` (prompt and worktree scan of the stand-in) | the marker found |
| 31 | S `test_codex_marks_each_loop_row_after_its_verdict` (verdict block byte-equal before and after the mark call) | a row without a mark; a changed verdict row |
| 32 | S `test_the_glm_call_goes_to_zai_with_glm_5_3_at_max` | another base, model or effort |
| 33 | S `test_the_glm_call_carries_no_user_or_project_configuration` (empty fresh `CLAUDE_CONFIG_DIR`, `--restricted`) | unset, the user's, non-empty; the flag missing |
| 34 | S `test_the_glm_call_can_only_read_and_search` (`--tools` ⊆ Read, Grep, Glob; no `--allowedTools`, `acceptEdits`, `bypassPermissions`) | a wider tool set |
| 35 | S `test_the_glm_prompt_carries_the_loop_prompt_and_the_uncommitted_diff` (an edit and an untracked file) | either missing |
| 36 | S `test_a_third_round_is_refused` (also after a release) | a third start |
| 37 | S `test_a_round_lands_in_the_loop_record_not_the_worktree` | a row in the worktree; an id without `L<n>-` |
| 38 | S `test_release_without_a_verdict_line_refuses_and_changes_nothing` (byte-identical) | a released row |
| 39 | S `test_release_carries_every_row_with_its_marks`; S `test_an_undecided_loop_row_holds_the_next_round_and_the_release` | a row lost or altered; an undecided release |
| 40, 41 | review of §4 | a class routed otherwise; the caveat missing |
| 42, 43 | S `test_the_routing_rows_name_the_decided_models` (§4: 2a, 4b, 6 with `max`; §3: 4 with Sonnet 5.5 and `medium`) | another model or effort |
| 44, 45 | review of §3 and §4 | the exception or the runner sentence missing |
| 46 | S `test_the_phase_table_has_the_review_loop` | the `4b` row or its prompt link missing |
| 47, 48 | S `test_the_evidence_rule_stands_where_findings_are_taken` (`docs/WORKFLOW.md`, `04-implement.md`, `04b-review-loop.md`); review for the "anywhere" half | the sentence missing |
| 49, 50 | review of §4 | a column or the stop rule missing or altered |
| 51, 53 | review, slice 3 step 6 | a name the tree lacks |
| 52, 54 | S `test_the_standing_note_says_stage_2_is_active` (the old sentence absent); review of §6 | "prepared, not active" |
| 55, 56 | S `test_the_review_prompts_give_both_paths` (`gpt-6.1-sol`, `Fable 5.1`, `scripts/stage2.py`; `Phase 6 verdict:` and `release-loop` in 06) | a path or the verdict line missing |
| 57, 58 | S `test_the_implement_prompt_names_sonnet_5_5_at_medium`; S `test_the_plan_prompt_asks_for_no_markings` | Sonnet 5; a marking |
| 59 | S `test_the_spec_prompt_asks_one_condition_and_a_refutation` | either sentence missing |
| 60 | S `test_agents_md_names_the_loop_and_the_runner`; `tests/test_entry_points.py` | the row or sentence missing; over 200 lines |
| 61 | S `test_settings_ask_before_codex`; S `test_a_missing_or_covered_codex_rule_is_caught` | the rule removed; `Bash(codex *)` allowed |
| 62–65 | review of ADR 0007 | a part missing or stated otherwise; M2 declared entered |
| 66, 67 | S `test_d13_is_amended_by_adr_0007` (the map, the ADR naming D-13, the row "Amend" with ADR 0007); the gate `decision-continuity` | the map entry or the row |
| 68 | review of both documents | a note missing |
| 69 | the pull request | no `decide(`, label or block |
| 70 | `make verify` on the last commit | any gate red |
| 71 | `python3 scripts/kit/probe.py --list` | the leak check absent |
| 72 | review | a new German sentence; German rewritten in passing |

**Mutation list** (planted, test red, restored; recorded in the
implementation notes). Slice 1: resolver without the dot form; the routing
pattern back to one digit and one word; skip untracked files; drop
`--remotes`; print the match; exit 0 on a missing denylist. Slice 2: drop
the leak check before the second call; copy the caller's environment; pass
stdin through; drop `-c sandbox_mode`; write the session line on a failed
call; release without a verdict line; count rounds only in the record;
put loop rows in the worktree; remove the ask rule. Slice 3: the `D-13`
map entry removed; the 4b row removed; Sonnet 5 back in `04-implement.md`.

## Not touched

- `scripts/export/manifest.yaml`, `templates/`, `.github/workflows/ci.yml`,
  `decisions/gates.yaml` — the leak check and the runner are no gates.
- `.codex/config.toml`, `.codex/hooks.json` — the runner switches them off
  per call, not in the tree.
- `.claude/agents/` (they pin `claude-sonnet-5`, spec non-goal),
  `bedrock-claude`, `glm-5.3-flash`, the German text of
  `model-endpoints.yaml` and `tests/test_model_endpoints.py` beyond the lines
  named.
- `docs/architecture/2026-09-17-gap-analysis.md`,
  `docs/architecture/target-architecture.md` — measurements and history.
- `research.md`, `decisions.md`, `findings.md`, `spec.md` beyond
  `implementation_status`; the tracker; lakeswitch-ai.

## Repair round 1

Origin `fix-r1`, 2026-09-30, on the nine findings F-1 to F-9 of the phase-6
review (`findings.md`, "Phase 6 — review, round 1", reviewed at `317763b`;
this round starts at `41abf42`). All nine are fixed, in `6b6e6f6` (the runner
and its prompts, F-1 to F-4 and F-7) and `7a89f3c` (the leak check and
`docs/WORKFLOW.md`, F-5, F-6, F-8, F-9). The decisions below are the
coordinating session's `[DETAIL]`s. Two items of "Not touched" were touched
on purpose: `spec.md`, in criterion 36 and one `[DETAIL]` (F-1), and
`findings.md`, in the Status column and one paragraph. The evidence rule of
this change held: each row was taken because a test demonstrates it or the
spec supports it, and every new test was run red before the fix.

**Evidence, tests red before and green after.** The 36 new tests were
written first: 27 in `tests/test_stage2.py` (26 of the runner and its
prompts, one doctrine test for §4) and 9 in `tests/test_leakcheck.py`; the two
files held 100 tests before the round and hold 136 after. Run against the
unrepaired tree (`git archive 41abf42` with the new test files copied in), 29
of the 136 were red, 22 in `tests/test_stage2.py` and 7 in
`tests/test_leakcheck.py`; after the fixes all 136 pass. The seven new tests
that were green on the unrepaired tree are guards for behaviour that must
stay: a no-finding answer is a round, a non-zero exit is no round, the verdict
line as the runner writes it, an escaped pipe in a `Status` reason, a
header-less loop record, a tracked file that is gone from the disk, and the
advice for a file match, which names no reflog. `make verify` on `7a89f3c`
(2026-09-30, `commit.gpgsign` off): 654 passed, 15 skipped, last line `VERIFY
GREEN — every local gate of the 'verify' job passed.` (`markdownlint` reports
and does not block).

### F-1, what a round is (`[DIVERGENT]`, BLOCKER)

The spec said a call without rows "is a failed call, not a round"; the plan,
the code and `test_a_round_without_a_finding_still_counts` said a successful
"no finding" answer counts. The code side stays, and the spec follows it:

- A call that exits 0 and answers — with rows or with "no finding" — is a
  round. The reviewer's clean result is a result; not counting it would let
  the loop call GLM again on a tree that has not changed.
- A call that fails is no round: a non-zero exit, and now also an empty
  answer, which the code counted as a round before (the test
  `test_a_call_without_an_answer_is_not_a_round[empty-answer]` was red). The
  maintainer's two rounds are not used up by a crash.
- `spec.md` criterion 36 and its `[DETAIL]` carry the new wording, marked as
  changed in repair round 1, the old wording struck, nothing renumbered; the
  refutation gained the two cases above. Two tests cover both sides:
  `test_a_no_finding_answer_is_a_round_and_a_failed_call_is_not` (round 1
  "no finding", round 2 two rows, a third call refused with "2 rounds have
  run") and `test_a_call_without_an_answer_is_not_a_round`.

### F-2, the release must not lose content

Measured against the stand-ins before the fix, with one correction to the
finding: the escaped form of a pipe (`a\|b`) in a `Status` reason already
parsed into nine cells, so (b) reproduces only for an unescaped pipe.

- **The parser knows six cells.** A table line of more than six cells whose
  second cell is a severity holds a pipe inside its last cell (a shell pipe, a
  regular expression); the last cell takes the rest, each pipe escaped. A
  line that does not start like a row stays text. The reviewers are also asked
  to write a pipe inside a cell as `\|` (the runner's closing paragraph and
  the three prompts), which the parser always honoured.
- **The record knows nine cells.** A pipe the implementer types into `Status`
  makes a tenth; the cells between the reviewer and the last one are the
  reason, each pipe escaped. The undecided-row guard therefore sees the row,
  and a decided row keeps its reason.
- **Carry, not refuse.** `release-loop` (and `review`, which calls it) appends
  every line of the record that is not its intro, a heading, the table's own
  header and separator, or a loop row — prose and unreadable table lines alike
  — as it stands, under "Kept from the loop record", before it deletes the
  record. Criterion 39 asks that every loop row arrive and the `[DETAIL]` says
  an answer that is not rows is "never dropped"; a refusal on such a line
  would make the implementer repair the record by hand, which is itself a
  silent rewrite. To keep that from copying every raw row twice, the record
  and `findings.md` now hold only the text of an answer that is not a row when
  rows were parsed (the whole answer when there are none), and the note says
  so ("what is not [a six-cell row] is kept below as it came").
- **One refusal remains**, for a line whose first cell is a loop id and that
  has fewer cells than a row: it cannot be read as a row, so the decision
  guard cannot hold it, and it would otherwise be deleted with the record. The
  refusal names the id, changes nothing, and `review-loop` and `review` meet
  it too.

### F-3, Codex's answer and the phase-6 prompt

The prompt and the runner now ask for the same six cells. `prompts/06-review.md`
no longer sends Codex to `templates/findings.md` (a file this repository does
not have) with "columns exactly as they stand there"; it names the six cells
for the runner path and the `findings.md` columns for the Fable path. An
answer that is nevertheless a table the parser cannot read as rows is never
headed "reported no finding": the head says it answered in table lines that
are not six-cell rows, and the lines follow as they came. Codex and GLM share
the one function (`answer_parts`), so the GLM record says the same.

### F-4, the verdict line

The pattern accepts the forms the prompts can produce: a reviewer of several
words (`Fable 5.1 <uuid>`), no session (`fable, 2026-10-01`), trailing spaces
and a full stop. It still wants the comma and the `YYYY-MM-DD` date last. A
line that starts like a verdict (case-insensitively) and has not the form is
named in the refusal, with the form. `prompts/06-review.md` states the form.

### F-5 and F-6, the leak check

- A listed path that exists and is neither a regular file nor a link to one
  is a BLOCK that names it: the link to a directory and the submodule entry
  of the finding, and, by the same rule, a repository nested in the tree and
  a special file. Refusing, not scanning, because a directory behind a link
  can lie anywhere on the disk. A link with nothing behind it is scanned as
  its own text; a tracked file gone from the disk is no refusal, since there
  is nothing to read and the index scan shows its deletion.
- The staged changes are scanned with `git diff --cached` (additions and
  deletions against `HEAD`, binary as text, no external diff or text
  conversion). That reads what `git show :<path>` can show beyond the disk; a
  staged file equal to `HEAD` is in the history scan already. A failure to read
  the index refuses, like a failure to read the history. The three counts of
  the report do not change.
- The reflog is not scanned. The limit is written into the docstring and into
  `docs/WORKFLOW.md` §4 together with the stash, refs outside `refs/heads` and
  `refs/remotes` (tags, `refs/dolt/`) and unreachable objects, and the advice
  for a match in a commit says that rewriting the commit does not remove the
  value. Measured in a temporary repository on 2026-09-30: after an amend,
  `git log --branches --remotes -p` no longer shows the value and `git log -g
  -p` does; a staged-and-stashed value is shown by `git stash show -p` and not
  by the branch scan; after `git reflog expire --expire=now --all` and `git gc
  --prune=now` `git log -g -p` shows neither.

### F-7, the `updated:` stamp

Every write the runner makes to a file with a header — the call line, the
blocks, the release, the marks — ends with `check_frontmatter_current.stamp`,
the stamp the gate `frontmatter-current` itself offers as its repair. The
loop record has no header and gets none.

### F-8 and F-9, the doctrine text

§4 now says the read-only sandbox, the session, the hooks and memories and the
skipped project settings are configured on every call and not measured (the
maintainer's decision of 2026-09-30, ADR 0007), and what an ineffective hooks
switch would let through. F-9 was trivial (two names on the "not here yet" list
and one exact sentence about `.claude/settings.json`, the list re-dated to
`41abf42`), so it is fixed here; it has no test, because criterion 53 is held
by review.

### Left open

- No reviewer has read this round. A re-review of the nine rows (and of the new
  code around them: the folding rule, the carrying release, the index scan)
  comes before phase 7. Findings this round produces carry origin `fix-r1`;
  two consecutive rounds of `fix-r` origin are an escalation, not a third
  round (`docs/WORKFLOW.md` §2).
- The named limits stay limits: the reflog, the stash, tags and unreachable
  objects are not scanned, and the runner's settings are not measured.
- Phase 7 is untouched: no pull request, no tracker write, no `decide(`
  label.

## Repair round 2

Origin `fix-r2`, 2026-09-30, on the two rows the re-review of round 1 opened,
F-10 and F-11 (`findings.md`, "Phase 6 — review, round 1"; this round starts at
`8622437`). Both are fixed in `022930e`, together with the three notes the
re-review left in the Status cells of F-4, F-6 and F-7. Pull request #60 stays
unmerged and is not touched. The evidence rule of this change held again: each
row was taken because a test demonstrates it, and each new test that can be red
was run red before the fix.

**Evidence, tests red before and green after.** Thirteen test cases were
written first: 11 in `tests/test_stage2.py` (seven new tests, and two new cases
of the existing test of the refused verdict line) and 2 in
`tests/test_leakcheck.py` (one new test, two cases); the two files held 136
tests before the round and hold 149 after. Run against the unrepaired tree
(`git archive 8622437` with the new test files copied in), 8 of the 149 were red:
F-10 three, F-11 three (one test, one case per verb), F-4 two (two new cases).
After the fix all 149 pass, and
`make verify` on `022930e` (2026-09-30, `commit.gpgsign` off) gives 667 passed, 15
skipped, last line `VERIFY GREEN — every local gate of the 'verify' job
passed.` (`markdownlint` reports and does not block). The other five cases are
guards for behaviour that must stay and were green before: the stamp in
`fill_marks`, `git diff --cached` against plain `git diff` (two cases), a
damaged row of the record's own tables beside GLM's text, and round 2's rows
after round 1's words. Each guard was checked by planting its fault in a copy of
the tree, and the planted fault turned it red: no stamp in `fill_marks`; plain
`git diff` in the leak check; the refusal of a damaged row switched off; the
round heading no longer ending GLM's words. The three fixes were planted back the
same way: GLM's `#` lines skipped again (two F-10 tests red), GLM's lines read as
rows (the three F-11 cases red), `pending` accepted (the two F-4 cases red).

### F-10 and F-11, who wrote a line of the record

Both findings come from one fact the record did not keep apart: a line of it is
either the record's own (heading, intro, round table, the runner's statement and
note, the implementer's decisions) or GLM's words, kept "as they came" below the
note. The repair keeps them apart by position, which is exactly how the runner
writes a round: the lines after the note `NOT_ROWS_NOTE`, up to the next round
heading, are GLM's (`_record_lines`).

- **F-10, carried as they came.** `kept_lines` leaves out only the record's own
  furniture: its heading (the first line), the two intro sentences, the round
  headings, the tables' header and separator, and the blank lines between the
  runner's own lines. A line of GLM's is carried whatever it starts with — a
  heading (`## Why this matters`), a code comment (`# run: grep foo \| wc -l`), a
  table line that is no row, a blank line inside the text — and stands apart from
  the runner's lines by one blank line. A sentence of the intro that GLM quoted
  is carried too: the old code removed the intro with `str.replace` over the whole
  record, which took GLM's copy with it. The module docstring now lists what is
  left out, and the Status of F-2, which said "every line … as it stands", says
  the same.
- **F-11, rows are the record's own.** `record_rows` reads only the record's own
  lines. The undecided-row guard and the refusal of a damaged row therefore meet
  the nine-cell rows of the round tables the runner wrote and the implementer
  decided, and a table line GLM wrote, `| L1-1 | still open |` included, is text to
  carry. Criterion 39 is intact: a damaged row of the round tables (a cell deleted
  by hand) still refuses by its id in `release-loop`, `review-loop` and `review`,
  and a test has that row stand beside GLM's text.
- **Decided, not asked (`[DETAIL]`):** position over content. The alternative,
  telling GLM's line from a row by its shape, fails for the same reason F-11 did:
  GLM's table line has a loop id too. Position is what the runner controls.
- **Limit, stated not fixed.** A line of GLM's in the form of the record's own
  round heading (`## Round <n> — GLM, `) cannot be told from one; it ends GLM's
  words and is left out, and `rounds_run` counts it as a round, as it did before.
  The answer format asks for table rows only, and the runner cannot write a
  marker GLM could not also write. The limit is in the docstring of
  `_record_lines`.

### The three notes of the re-review

- **F-4, `pending` is no reviewer.** The verdict pattern refuses a reviewer whose
  first word is `pending`, in any case, with or without a session; such a line
  reaches the existing refusal that names the line, which now also says `pending`
  is no reviewer, and `prompts/06-review.md` says so. No other placeholder word is
  refused: the re-review named this one, and a list of placeholders is a guess.
- **F-6, `--cached` against plain `git diff`.** Measured in a temporary
  repository: after a staged value, the file put back and the entry marked
  `skip-worktree` or `assume-unchanged`, `git diff` is empty and `git diff
  --cached` shows the value. The test builds exactly that, for both flags.
- **F-7, the stamp in `fill_marks`.** The test calls `fill_marks` on a file whose
  header says 2026-09-29, so the stamp is checked on its own and not through the
  `append` before it.

### Left open

- No reviewer has read this round. Findings it produces carry origin `fix-r2`; it
  is the second round in a row with `fix-r` findings (`fix-r1`, `fix-r2`), so a
  review finding here is an escalation to the maintainer under `docs/WORKFLOW.md`
  §2, not a third repair round.
- The named limits of round 1 stay (reflog, stash, tags and unreachable objects
  are not scanned; the runner's settings are not measured), and the one above.
- Phase 7 is untouched: no pull request opened or changed, no tracker write, no
  `decide(` label.

## Amendment 1 — the routing decisions of 2026-10-06 (bead coding-harness-bib)

The maintainer decided on 2026-10-06, in the Claude Code session, four things
(bead coding-harness-bib, "Model routing: no Fable; explore and implement on
GLM 5.3 Flash once stage 2 is live"):

1. No Fable. Opus 5.5 takes its places: the interview (1a), the escalation and
   the fallback when stage 2 fails. A `bounded` change's stage-2 reviews — 2a
   where one is held, and 6 — go to Codex. Main carries the part outside stage 2
   since pull request #87 (merge `ed180ae`).
2. Phase 4 Implement runs on `glm-5.3-flash` (the Z.ai endpoint declared in
   `model-endpoints.yaml`) once stage 2 is live.
3. Phase 1 Explore runs on `glm-5.3-flash` once stage 2 is live (instead of
   Haiku 4.5).
4. The leak check stays: asked and kept.

Until this pull request is merged and live, Claude models keep doing what
main's routing says. The amendment is made in three steps, one commit each:
A the merge of `origin/main`, B the routing in doctrine, prompts and tests, C
ADR 0007 and its continuity, and then D the pull request body (not a commit).

### Step A — merging `origin/main` (65 commits since the merge base `1e4cccf`)

Written against `origin/main` at `d5813ec`. Six files conflicted; each choice:

| File | Choice |
|---|---|
| `docs/WORKFLOW.md` (§4 opening) | The branch's text. Main's still read "adding GLM and Kimi (prepared, not active)" — the placeholder this change replaces. |
| `docs/architecture/2026-09-17-implementation-plan.md`, `...-omnigent-first-target.md` | Both "Changed" notes stay, the older (ADR 0007, 2026-09-30) first and ADR 0009 (2026-10-05) after it; `updated:` takes the later date. |
| `plans/INDEX.md` | Both sides' rows, then regenerated with `python3 scripts/plans_registry.py --index`. |
| `prompts/02a-spec-review.md`, `prompts/06-review.md` (Session lines) | Main's Claude path with `claude-opus-5-5` replaces the Fable command; the branch's Codex path stays beside it. |

Two places git merged without a conflict and still contradicted main, because
the branch had written them for the time after stage 2 and main had not
touched those lines: the Model lines and the "Fable path" sentences of the two
prompts, and the routing rows and the paragraph "Spec review and review on
Fable 5.1" of `docs/WORKFLOW.md` §3. `claude-fable-5-1` is no longer a
declared model (main took it out of `model-endpoints.yaml`), so
`tests/test_model_endpoints.py` was red on both. Choice: where main removed
Fable, it stays removed; the branch's post-stage-2 routing for `spike` and
`bounded` becomes Opus 5.5 for now (step B moves `bounded` on to Codex). The
same swap in the probe keys of `scripts/kit/probe.py`, the verdict-line
examples and the routing assertions of `tests/test_stage2.py`, and the
fallback sentence of ADR 0007 (Fable 5.1 to Opus 5.5).

Time log: started 2026-10-07 00:52 (CEST); step A resolved at 00:59.

### Step B — decisions 1 to 3 in the doctrine, the prompts and the tests

What changed (proposed and implemented; tested by `make verify`, no real call):

- `docs/WORKFLOW.md` §3: the rows of 2a and 6 name Opus 5.5 and send a
  `bounded`, `feature` or `architectural` change to Codex; the rows of 1 and 4
  stay Haiku 4.5 and Sonnet 5.5 and say that GLM 5.3 Flash replaces them where
  the runner starts the phase; the "No Fable" paragraph says which rows leave
  the table; escalation and cost lines follow.
- `docs/WORKFLOW.md` §4: the title and opening paragraph (Flash explores and
  implements; no Fable, no Kimi); the class table (`bounded` goes to Codex for
  2a where held and for 6, GLM keeps the loop); two new routing rows (1 Explore
  and 4 Implement on GLM 5.3 Flash, for every change); the paragraph "The two
  Flash rows are decided and not built"; "A foreign model" in place of "A
  foreign reviewer" in the runner section; a paragraph on what explore and
  implement send and what the leak check covers; the fallback reads Opus 5.5
  for the reviews and §3's rows for phases 1 and 4.
- Prompts: `01-explore.md` and `04-implement.md` lead with GLM 5.3 Flash and
  name the Claude model that runs until the runner starts the phase;
  `02a-spec-review.md` and `06-review.md` send a bounded change to Codex.
  `AGENTS.md`, the probe keys in `scripts/kit/probe.py` and the remark of the
  `glm-coding-plan` endpoint in `model-endpoints.yaml` follow.
- Tests (`tests/test_stage2.py`): the routing rows hold five section-4 rows and
  two section-3 rows; the implement and explore prompts; the class table; no
  Fable in a routing row or a prompt; the Flash rows say "decided and not
  built". Each has its mutation, which must go red.

Choices I made as `[DETAIL]` (the maintainer can narrow any of them):

1. **Explore and implement on Flash are not routed by class.** The class is
   stated in the spec, after phase 1, so explore cannot wait for it; and the
   decision names the two phases, not a class. They run on Flash for every
   change, a `spike` included. The class table routes the reviews only.
2. **§3 keeps Haiku 4.5 and Sonnet 5.5 as what runs where the runner does not
   start the phase.** That is true of every phase until the runner has verbs for
   these two, and it is what the fallback returns to.
3. **The fallback of the stop rule is Opus 5.5 for the reviews**, and phases 1
   and 4 return to §3's rows. The decision names the fallback of the review
   stage; what builds when stage 2 falls back is the corollary.
4. **A `bounded` change's phase 6 starts a fresh Codex session where no
   phase-2a session was held.** `review` in `scripts/stage2.py` already does
   that and writes the line "a fresh session reviewed: no phase-2a session was
   recorded"; no code change was needed.
5. **No effort is set for GLM 5.3 Flash.** The decision gives none, and a
   guess in a routing row would read as a decision.

### Open items from Amendment 1

- **O-1 — the runner's verbs `explore` and `implement` are not built.** How the
  older design did it, as far as this tree and its history show: plan steps
  carried a marking (`[FLASH]`, `[GLM5.3]`, `[SONNET]`, rules in
  `templates/plan-marking.md`), `scripts/run_change.sh` grouped equal markings
  into segments and ran each as a session with a verify gate after it, and six
  `scripts/cc-*.sh` profiles started one Claude Code session each against its
  endpoint with every `ANTHROPIC_*` variable set. **None of those files is in
  this repository** (`git ls-tree` of `origin/main` at `d5813ec` finds no such
  file; main's opening note of `docs/WORKFLOW.md` lists them as missing at
  `9f14283`, and its section 4 still describes them as the mechanics), and this
  change retired the marking text from section 4 and from `prompts/03-plan.md`. So nothing exists to reuse, and a verb is a slice of its
  own: a runner call with write tools for implement (the reviewers' calls are
  limited to `Read`, `Grep`, `Glob`), a decision on how a plan assigns steps to
  Flash or keeps one on Claude, the effort for Flash, tests with stand-ins like
  the existing verbs, and the leak check around each call (the existing one
  already scans the tree and the prompt). It is more than a small step, so it
  is written here and not built. It needs a bead of its own; none was created
  (no tracker write in this amendment).
- **O-2 — until O-1 is built, §3 runs the two phases**: Haiku 4.5 explores and
  Sonnet 5.5 implements, and `docs/WORKFLOW.md` §4 says so in one paragraph, held
  by a test.
- **O-3 — the roadmap line "Stage 2 live"** (`ROADMAP.md`) still speaks of
  reviews only; it was not changed here.
- **O-4 — the real leak check does not reproduce its earlier "clean".** Run on
  2026-10-07 at `c951e96` with the maintainer's real denylist
  (`make leakcheck NAME=stage-2-codex-glm`; no model call): **BLOCK, four
  places** — `tests/test_stage2.py` line 45 (the planted fake key `KEY` of the
  runner's tests, rule `openai-style-key`, length 34), and the patches of three
  commits: `6a1532c` (the commit that added that key), `79d2f5c` (the merge of
  step A, whose combined diff shows the same line) and `fba000d` (a test of
  `main` with a URL fixture that carries a user and a password, rule
  `connection-string-with-credentials`, length 19). All four read as planted test
  fixtures, not as real values (not opened beyond the line numbers, the check
  does not print a match). The check scans every file the tree tracks and the
  patch of every commit reachable from a branch, so a planted fixture is a
  permanent BLOCK until the fixture is built at run time and the commits that
  carry it are rewritten, or the denylist's rule is narrowed — the first two are
  history rewrites, the third is the maintainer's own file. Nothing was changed
  here; the old line "Real leak check against the real denylist: clean
  (2026-09-30)" of the pull request body is replaced by this measurement. It
  decides whether the first real call of stage 2 can run at all, so it is the
  maintainer's to settle.

Time log: step B committed at 01:09 (CEST), started 00:52.

### Step C — ADR 0007

`docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` (unmerged, so amended in
place; the file name stays, because the continuity map and the D-13 row name
it):

- Title and header: "Codex and GLM work on framework content"; the review
  line names the decisions of 2026-10-06 (bead coding-harness-bib); the date
  line says "widened on 2026-10-06 before the merge".
- Context: a paragraph "Widened on 2026-10-06" with the four decisions, and the
  sentence that this ADR no longer keeps phases 1 and 4 with Anthropic.
- Decision 1: the criteria hold on a call of explore or implement as on a call
  of a review; the fallback reads Opus 5.5 for the reviews and Haiku 4.5 and
  Sonnet 5.5 for phases 1 and 4. Decision 2: the scope names exploration and
  implementation, says that far more of the repository goes to Z.ai, and that
  LakeSwitch and customer content never go. Decision 3: Kimi is dropped, and so
  is Fable. Decision 4: the reads of the foreign models are not confined; the
  earlier acceptance named the reviewers, and the maintainer confirms the wider
  reach by merging. New decision 5: explore and implement on GLM 5.3 Flash,
  decided, not built.
- Options: "Reviews only, as this ADR first stood" is listed as set aside by the
  maintainer. Consequences: the interim routing on `main`, the class remark
  (`spike` and `bounded`), "More leaves than reviews", and the other changes
  that follow from answers. Validation names the tests that hold the routing.
- The two "Changed, 2026-09-30" notes of the architecture documents carry one
  added sentence about the widening.
- `check_decision_continuity.py` is green with D-13 mapped to this file; the
  test `test_d13_is_amended_by_adr_0007` holds eight needles of the ADR,
  four of them new, and that neither "phases 1 and 4 stay with Anthropic" nor
  a Fable fallback stands in it.

Time log: step C committed at 01:12 (CEST), started 00:52.

### Step D — the body of pull request #60

Not a commit: the body is rewritten from `gh pr view 60 --json body` in the
decision template's form and applied with `gh pr edit 60 --body-file`. What it
states: decision 2's line and "Confirms" carry the new routing (GLM 5.3 Flash
explores and implements, Codex reviews `feature`, `architectural` and `bounded`
changes, the GLM loop stays in 4b, Opus 5.5 is the fallback, no Fable, no Kimi),
"What changes for you" says that more of the repository goes to Z.ai behind the
leak check, the head shas are the head of this branch, and bead
coding-harness-bib is in the evidence. It also says that explore and implement
are decided and not built (O-1), and states the leak-check measurement (O-4)
instead of the earlier "clean". The pull request's title was not changed; it
still reads "Codex and GLM review Coding Harness changes".

Time log: step D written at 01:17 (CEST); started 00:52. No Codex, GLM or MiMo
call, no tracker write, nothing installed, no merge and no new pull request.
