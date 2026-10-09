---
title: "Session handover — starting coding-harness-0al on the maintainer's Mac, as of 2026-10-09"
category: handover
created: 2026-10-09
updated: 2026-10-09
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-10-09"
tags: [handover, stage-2, opencode, session-verb, remote-to-local]
target_ref: cff84a1
bead: coding-harness-0al
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

## Where we are

As of 2026-10-09, `main` is at `cff84a1`. The bug in bead coding-harness-0al
(`stage2.py session` refuses under OpenCode 2.x) is **read but not measured**:
it occurs only on the maintainer's Mac, where two OpenCode installs exist, and
the remote session that wrote this file has neither (`opencode` is not on its
PATH). Nothing was changed in `scripts/` or `tests/`, and the tracker was not
written. This file is the preparation: the code facts, the measurement to run
first, and the two fix options with a recommendation.

## Next step

**Superseded by the addendum at the end of this file:** the maintainer wants
no more OpenCode CLI, which changes what the local session does first. The
original step follows for the record.

On the Mac, in a worktree of its own from a freshly fetched `origin/main`
(`git worktree add .claude/worktrees/stage2-session-opencode2 -b
fix/stage2-session-opencode2 origin/main`, then `make venv`), run the
measurement below **before touching any code**, and write the output into the
change's `research.md` with the date and both versions. The bead says the same:
measure, then fix.

## Needed from the maintainer

1. **Start the local session.** One writer per tracker (house rule 4): the
   session that starts first writes the tracker; a second one only claims the
   bead and leaves its handover comment on it.
2. **Choose the fix after the measurement**, not before (see "The two fix
   options"). A decision pull request is not needed for either option: neither
   changes what may leave the repository.

## What the code does today (read at `cff84a1`)

All of it is in `scripts/stage2_session.py`; the symbols, not line numbers:

- `executables(transport, runner)` resolves the CLI with
  `shutil.which("opencode")` — the **first** `opencode` on PATH. On the Mac
  that is `~/.opencode/bin/opencode` (v2.0.24, `~/.zshrc:37`), not
  `/opt/homebrew/bin/opencode` (v1.18.35). It checks no version.
- `verify_policy(...)` writes the runner's policy (`policy_config(model)`) to
  `opencode.policy.json` in the session's private directory and hands it to
  OpenCode as `OPENCODE_CONFIG`.
- `effective_policy(...)` then runs `opencode --pure debug agent harness-session`
  and parses its JSON (`Agent.Info`: `name`, `mode`, `model` as
  `{providerID, modelID}`, `permission` as one ordered rule list). Anything
  it cannot confirm refuses (`runner.Refused`).
- `policy_problems(...)` holds the rule list against `GUARDED`
  (`external_directory`, `task`, `webfetch`, `bash`): the last catch-all of
  each must carry an allowed action, and nothing after it may relax it.

What the bead measured on 2026-10-08, to be **re-measured, not trusted**:
under v2.0.24 `debug agent` prints help and exits 1 (the subcommand is now
`debug agents`), and `OPENCODE_CONFIG` did not appear among the debug config
sources, so the runner's policy would not be loaded. Today this ends in a
refusal ("opencode debug agent exited 1; the effective policy is unknown") —
**safe, but the verb is unusable on that PATH**. The danger the bead names is
the future one: if someone loosened the check, a session would run without the
runner's policy.

Why the tests stay green: `tests/test_stage2_session.py` puts stand-in
`opencode`/`osascript` executables first on PATH and feeds a canned answer in
1.18.35's shape (`effective(...)`). No test runs a real OpenCode.

## The measurement (run first, read-only)

```bash
# 1. which binaries, in PATH order
type -a opencode
for bin in ~/.opencode/bin/opencode /opt/homebrew/bin/opencode; do
  echo "== $bin"; "$bin" --version
done

# 2. the runner's own policy file, written the way verify_policy writes it
POL="$(mktemp -d)/opencode.policy.json"
python3 - "$POL" <<'PY'
import json, sys
sys.path.insert(0, "scripts")
import stage2_session as s
model = "opencode-go/deepseek-v4.1-flash"   # any declared id; the policy only pins it
open(sys.argv[1], "w").write(json.dumps(s.policy_config(model), indent=2) + "\n")
PY

# 3. what each binary says to the exact call the runner makes
for bin in ~/.opencode/bin/opencode /opt/homebrew/bin/opencode; do
  echo "== $bin: debug agent"
  OPENCODE_CONFIG="$POL" "$bin" --pure debug agent harness-session \
    >/tmp/0al-agent.out 2>/tmp/0al-agent.err; echo "exit=$?"
  head -c 600 /tmp/0al-agent.out; echo; head -c 600 /tmp/0al-agent.err
done

# 4. v2 only: the renamed subcommand and where the config comes from
OPENCODE_CONFIG="$POL" ~/.opencode/bin/opencode --pure debug --help
OPENCODE_CONFIG="$POL" ~/.opencode/bin/opencode --pure debug agents harness-session | head -c 1500
OPENCODE_CONFIG="$POL" ~/.opencode/bin/opencode --pure debug config | head -c 1500
```

Record, per binary: the version, the exit code, whether stdout is JSON in the
`Agent.Info` shape, and whether the `harness-session` agent with the pinned
model and the runner's permission rules shows up. **A binary that prints
nothing usable is "not read", not "no rules"** (AGENTS.md, "What could not be
read"). Keep the model id as the declared one; do not call a model (steps 1 to
4 start no session and send no content anywhere).

## The two fix options

**A. Pin the version the runner was built against (recommended first).**
`executables()` looks for an `opencode` whose `--version` is the pinned
1.18.35 — scanning every `opencode` on PATH, not only the first, so the
Homebrew install is found behind the v2 one — and otherwise refuses naming
the version it found. This mirrors how the runner pins Pi (it refuses any
other version; raising the pin means measuring again). Smallest change; the
refusal becomes a clear message instead of "exited 1". Cost: a Homebrew
upgrade past 1.18.35 makes the verb refuse until the pin is re-measured.

- Tests to add: v2 first and v1 later on PATH picks v1; only v2 on PATH refuses
  and names the version; an unreadable `--version` refuses as "could not be
  read", not as a mismatch.

**B. Port to v2.** `effective_policy()` calls the renamed subcommand and the
config loading is made to work (if the measurement in step 4 shows
`OPENCODE_CONFIG` is still honoured under another name or path). Larger, and
it needs a second canned answer in v2's shape in the tests. Do this only if
step 4 shows the policy *can* be loaded and read back under v2 — otherwise the
policy cannot be confirmed and B is not available.

Recommendation: measure, then take A unless the measurement shows B is as
small. Either way the refusal stays the default: a binary whose effective
policy cannot be read starts no session.

## Decisions and preferences

- One change, one bead, one branch, one worktree, one session; few agents,
  visible queue; nothing is merged by an agent without the maintainer asking
  for it in their own message.
- Phase order applies: explore (`research.md` with the measurement), spec,
  plan, implement, verify (`make verify`), review (Codex in phase 6), commit.
  Create the change folder with the repository's own command and search
  `plans/changes/` first (house rule: never create twice).
- Texts in this repository are English; the conversation with the maintainer
  is German.

## Open work and blockers

- coding-harness-0al — this bug (P2, open, not claimed).
- coding-harness-rwa (P3) needs a decision pull request first (ADR 0007 binds
  GLM to Claude Code); coding-harness-36z (P1, D-60 write guard) waits for
  ADR 0005 to be accepted. Neither is started here.
- The interactive `session` verb reaches a declared OpenCode endpoint under its
  own amendment (bead coding-harness-amp); this bug does not change that.

## Working state and parallel-session boundary

- Branch `chore/0al-prep` (this file only), pushed, **no pull request**
  opened: the maintainer asked for the preparation, not for another pull
  request. Merge it, or copy the file, as preferred.
- Three pull requests were in flight when this was written (#105, #106, #107)
  and #108 was merged; each merge makes the next branch stale, so a worktree
  for 0al starts from whatever `origin/main` is then.
- This remote session wrote nothing in the tracker and touched no other
  checkout.

## Validation

- Read at `cff84a1`: `scripts/stage2_session.py` (symbols named above) and the
  fixture shape in `tests/test_stage2_session.py`.
- Not run: any OpenCode binary (none on the remote session's PATH), the
  measurement above, either fix, `scripts/stage2.py session`.
- The measurement commands are written from the code and the bead and were not
  executed; the `type -a`, `--version` and `debug` lines are the ones to
  correct if a flag differs.

## Addendum 2026-10-09 (later): the port of the session verb to Pi

The maintainer, in German, in the directing conversation: "Ja, prüfe die
Umstellung auf pi, ich will keine opencode mehr benutzen." Read as: the
`opencode` CLI goes; the OpenCode Go service stays, because the review loop
already reaches it through Pi (ADR 0011). If that reading is wrong, the first
question of the next session is which one is meant.

### What it does to coding-harness-0al

Both fixes in the section above are moot if the session verb stops calling
`opencode`: no `opencode --pure debug agent` call remains, so there is
nothing to pin or to port. The bead would close as superseded (the tracker
writer's act). The local measurement against the two OpenCode binaries is no
longer needed.

### What Pi 1.1.0 offers (read, not run)

Source: the npm tarball of `@earendil-works/pi-coding-agent@1.1.0`, unpacked and
read in a scratch directory; no Pi code was executed. Files named below are
inside that package.

- **Interactive use exists.** Pi opens its terminal UI when stdin and stdout
  are terminals and neither `--print` nor `--mode` selects another interface
  (`docs/cli.md`). The loop's flags (`--model opencode-go/<id>`, `--tools`,
  `--thinking`, `--offline`) apply to it too. The key is `OPENCODE_API_KEY`
  (`docs/providers.md`), the same as the loop's.
- **No approval prompts and no sandbox** (`docs/security.md`): Pi "does not ask
  for approval before every tool call", and "lack of a built-in sandbox" is
  stated as outside its security boundary. OpenCode's `bash: ask` and
  `external_directory: deny` therefore have no built-in counterpart.
- **An extension can gate tool calls.** A `tool_call` handler can block a call,
  and a handler that fails blocks it (fail-safe) (`docs/extensions.md`).
  `--no-extensions` still loads an explicit `-e <path>` (`docs/cli.md`), so the
  runner can disable discovery and load exactly one policy extension.
  Shipped examples: `examples/extensions/permission-gate.ts` (asks for
  dangerous `bash` commands, blocks when there is no UI) and
  `protected-paths.ts` (blocks `write`/`edit` on listed paths).
- **No sub-agents** ("skips features like sub-agents", `README.md`) and **no
  web-fetch tool**: the built-ins are `read`, `bash`, `edit`, `write`, `grep`,
  `find`, `ls` (and `powershell` on Windows) (`docs/cli.md`).

### The runner's OpenCode policy, rule by rule

| Today (OpenCode, `policy_config`) | With Pi |
|---|---|
| `bash: ask` | policy extension: every `bash` call asks through the UI and is blocked when there is none |
| `external_directory: deny` | policy extension: block `read`, `grep`, `find`, `ls`, `edit`, `write` with a path outside the worktree. `bash` cannot be confined; the doctrine already says an approved shell command can read what the user can read |
| `task: deny` | nothing to deny: Pi has no sub-agent tool |
| `webfetch: deny` | nothing to deny: no such tool; `--offline` stops Pi's own network use; `bash` is gated as above |
| the model pinned for the agent | `--model opencode-go/<id>` |

### What does not carry over

The **read-back**. Today the runner asks OpenCode for its effective agent and
refuses what it cannot confirm. Pi has no such command in the docs read. It
lists the flags registered by loaded extensions in `pi --help`
(`docs/cli.md`) and has RPC `get_state`/`get_commands`
(`docs/rpc-commands.md`), so the runner could confirm that the policy
extension *loaded*, not that its handlers *behave*. The behaviour would be
held by tests of the handlers in this repository, run without Pi and without a
model. That is a weaker guarantee than the read-back, and the maintainer
should choose it knowingly.

### Size and shape of the change

In `scripts/stage2_session.py` the OpenCode-specific parts are
`policy_config`, `effective_policy`, `wildcard`, `catch_all`,
`policy_problems`, `insert_denials` and `verify_policy`, plus the OpenCode
branches of `TRANSPORTS`, `executables`, `prepare` and `cli_argv`. In
`tests/test_stage2_session.py` 25 uses of the canned `effective(...)` answer
(the file has 43 tests) go or change. `require_pi` in `scripts/stage2.py`
already pins Pi to 1.1.0 and can be reused. Terminal dispatch through
`osascript` stays.

### Is it a decision pull request?

Recommended: yes. The endpoint (`opencode-go`) does not change and ADR 0011
already declares it. What changes is the launcher of an *interactive* session
that can write files and run approved shell commands, and the way its limits
are enforced (an extension instead of OpenCode's read-back). The session
verb's ADR 0007 amendment still travels as a draft in its change folder, which
is where this belongs. The maintainer decides whether it is a decision pull
request.

### Next step

Not a measurement against OpenCode. A one-page plan first (house rule: plan,
then build), in a worktree of its own from a freshly fetched `origin/main`:

1. State what the verb can do afterwards that it cannot today: start an
   interactive OpenCode Go session without the OpenCode CLI.
2. Measure Pi on the Mac without a model call: `pi --version` prints `1.1.0`;
   `pi -ne -e <policy extension> --help` lists the extension's flag;
   the extension's handlers pass tests with fake events (path outside the
   worktree is blocked, `bash` without UI is blocked, a handler error blocks).
3. Take the decision on the read-back (above) before writing code.

Not run: Pi itself, any launch, any extension, any model call. The table is
read from the docs of the pinned version; the first real launch may show a
difference.
