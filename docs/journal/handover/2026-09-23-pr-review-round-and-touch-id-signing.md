---
title: "Session handover — pull requests reviewed and merged across three repositories, tracker export stage 3 finished, Touch-ID signing, 2026-09-23"
category: handover
created: 2026-09-23
direction: framework->framework
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-23"
tags: [handover, review, merge, tracker-export, gate-placement, signing, lakeswitch]
target_ref: "59ea1bf"
bead: coding-harness-1jg.3
status: pending
review:
  status: pending
  approved_by: null
  approved_at: null
---

# Resume here

One session, started 2026-09-22 and ended 2026-09-23. On the maintainer's
request it reviewed and merged the open pull requests in coding-harness,
portfolio-agentic-engineering and lakeswitch-ai. It finished the portfolio
tracker migration, set up a Touch-ID signing key for decisions, and took over
stage 3 of the tracker export from a stopped Cline session and merged it.
The portfolio part has its own handover
(`docs/journal/handover/2026-09-22-tracker-on-bd-130-behind-a-pin.md` there).
The lakeswitch part is in lakeswitch-ai's journal
(`journal/2026-09-23-pr36-interview-and-touch-id-confirmation.md`, untracked
like every file there).

## Where we are

As of 2026-09-23, `main` is at `59ea1bf` and no pull request is open apart
from this handover. **The tracker export is no longer committed.** The hosted
CI hydrates the tracker from `refs/dolt/data` in both jobs, renders once and
presets `BEAD_RENDER`. Local readers render fresh through
`scripts/bead_render.py`, and without `bd` they fail with instructions
(`coding-harness-1jg.3`, closed). Stages 1 to 3 are done; the parent bead
stays open for one successor, a CI job summary of changed beads
(`coding-harness-1jg.4`).

## Next step

Build the CI job summary that lists the beads a pull request changed
(`coding-harness-1jg.4`). It replaces the tracker diff the committed copy used
to show, and house rule 4 covers the gap until then (every pull request body
names the beads it opens, changes or closes).

## Needed from the maintainer

Nothing right now for this repository. In lakeswitch-ai, pull request #37
still waits for the two lines in `decisions/provenance.yaml` (unchanged since
2026-09-22).

## Decisions and preferences

- **D-52 successors (maintainer, 2026-09-23).** The committed copy gave two
  conveniences. For tracker changes in the diff, a pull request body names its
  beads (house rule 4), and a CI job summary follows (`coding-harness-1jg.4`).
  For agents without `bd`, the access point's error names
  `tools/beads/install.sh && tools/bd bootstrap --yes` and `BEAD_RENDER`.
- **Session merges are allowed** for the pull requests the maintainer names
  in the request. This time: review and merge of everything open, the
  portfolio migration (#163), gate placement (#32), lakeswitch #36, and the
  takeover of stage 3 (#34).
- **Decisions are confirmed with a Touch-ID key.** An agent prepares a change
  under a protected path. It is valid only through a commit the maintainer
  signs with a Secure Enclave key that signs on Touch ID only (Secretive, key
  `lakeswitch-decisions`, ECDSA
  `SHA256:LMqOFIm/waO3jemYoQjG8YWpM/iMQKEZW8D+S59QM7c`, a GitHub signing key
  since 2026-09-23). The maintainer runs that commit personally, and the
  Claude Code permission layer refuses it to a session, which fits. The older
  software key (`~/.ssh/id_ed25519`) stays for ordinary commits and is not
  proof of the maintainer. Decided for lakeswitch-ai in the #36 interview;
  whether coding-harness adopts it for its own `decisions/` is not decided.
- **Interview form that worked:** one question at a time, three options with
  one recommended, plain context first. Twice the maintainer asked for more
  explanation, and both times the plainer answer led straight to a decision.

## Open work and blockers

Task status lives in Beads; this list only points.

- CI job summary of changed beads (`coding-harness-1jg.4`, open, child of
  `coding-harness-1jg`).
- **Not reviewed by anyone:** `e02c915` (stage 3 step one, the access point
  `scripts/bead_render.py`) reached `main` through #32 after this session's
  review of that pull request. The takeover (#34) built on it and its tests
  pass in hosted CI, but its code was not read line by line.
- **The session scan misses sessions.** A Cline session worked in the primary
  checkout on 2026-09-23 and the scan never showed it. That is expected for a
  non-Claude harness, but it means the one-writer rule relies on the
  maintainer saying so.

## Working state and parallel-session boundary

- Primary checkout `~/coding-harness`: on `main` at `59ea1bf`, clean,
  measured 2026-09-23. `.beads/issues.jsonl` no longer exists on disk and is
  git-ignored; `python3 scripts/render_beads_export.py` writes a local render
  there when needed.
- This handover comes from the worktree `~/coding-harness-wt-handover-0923`
  (branch `docs/handover-2026-09-23-pr-round`); remove it after the merge.
- Merged by this session in this repository: #24 (`9364bc9`), #32
  (`f5c5968`), #34 (`59ea1bf`, content commits `2630922`, the header fix and
  the probe fix). The tracker was pushed before Git each time.
- Other repositories: portfolio #163 (`8675683`), #164 (`34bb722`), #165
  (`20a279c`); lakeswitch-ai #36 (`e1e7572`).
- Taken over from the stopped Cline session: its uncommitted stage-3 work
  (last edit 10:28), corrected and merged as #34. The Cline session has no
  credits left and is not running.

## Validation

- 2026-09-23, #34: `make verify` VERIFY GREEN (325 passed, 15 skipped) and
  `verify_all.sh --job drift` VERIFY GREEN locally. Hosted CI: `verify` green
  on the pull request, and `drift` green in a `workflow_dispatch` run on the
  branch (`35846445731`). Both hydrate with "Bootstrap plan: clone from
  remote".
- **Found on the way:** before #34 the hosted hydration never read
  `refs/dolt/data`. A duplicate Authorization header made `bd bootstrap`
  fall back to importing the committed JSONL, so `export-identity` compared
  the copy with itself. The D-52 condition "token read access in CI" had
  been recorded as shown on 2026-09-22 when it was not. It is shown now.
- 2026-09-23, #32 at `f4ac0fc`: `make verify` VERIFY GREEN, 329 passed, 15
  skipped. The generated `ci.yml` was unchanged against `main` at the time.
- Not read: `e02c915` (see "Open work").

## Addendum — 2026-09-23, after the handover was merged

- **`e02c915` is reviewed.** Read line by line after #35. It had four crash
  paths: no `bd` binary, readers without exit 3, and two `relative_to(REPO)`
  on a render outside the repository. All four are fixed with five tests in
  #36 (`5c28712`). The "not reviewed" item under "Open work" is done.
- **The D-52 record is corrected.** ADR 0004 and the D-4 row of the target
  architecture now say, in dated notes, that #26 did not show read access to
  `refs/dolt/data` and #34 did. The parent bead carries the same note.
- **ADR 0004 is accepted by the maintainer.** It is signed with the Touch-ID
  key in the pull request that carries this addendum.
- Next step unchanged: the CI job summary of changed beads
  (`coding-harness-1jg.4`).

## Addendum — 2026-09-23, session end: worktree writes verified, ADR 0005 accepted

### Where we are

As of 2026-09-23, `main` is at `de36d82`, no pull request is open, and no
bead is in progress. Two prerequisites of the Omnigent M0 pilot are settled
today.

- **Tracker writes from worktrees are safe and allowed.** All five D-5
  checks were green with bd 1.3.0 in a throwaway repository: same list,
  variables and sandbox, visibility, four concurrent writers with nothing
  lost, and the full prefix. `AGENTS.md` now allows tracker writes from an
  in-repository worktree; who may write is still house rule 4. The protocol
  is `docs/research/2026-09-23-worktree-tracker-writes.md`, merged as #38
  (bead `coding-harness-m34`, closed).
- **ADR 0005 is accepted.** Workers claim, create follow-up work and close
  their own bead. Three layers hold this: bd's claim rules (measured), a
  custom Omnigent session policy (documented, untested) and bd's events
  journal (measured). It supersedes ADR 0002's exclusive writer and
  read-only workers; ADR 0002's rules on stale results and the throwaway
  pilot store stay. The maintainer signed the acceptance with the Touch-ID
  key, merged as #39.
- `.claude/worktrees/` is git-ignored now; before #39 the main checkout
  listed in-repository worktrees as untracked.

### Next step

Start the Omnigent M0 pilot (`coding-harness-eev`). Its child bead
`coding-harness-36z` carries ADR 0005's three layers, each with a known-bad
case to prove in M0. The first question for the maintainer is where the
Omnigent server runs (the target names a dedicated machine, pinned, with
telemetry off).

### Needed from the maintainer

Decide the machine for the M0 Omnigent server. In lakeswitch-ai, pull
request #37 still waits for the two lines in `decisions/provenance.yaml`.
The session `lakeswitch-ai-b3` owns the open drafts #38 to #40 there.

### Decisions and preferences

- **Workers claim their own bead** (ADR 0005, maintainer, 2026-09-23). The
  maintainer asked for a feasibility check of that option before choosing it.
- **Bead `coding-harness-36z` was re-scoped twice today.** First the
  maintainer chose "no self-built lock, Omnigent sandbox configuration
  instead", then ADR 0005 replaced that scope. The notes on the bead record
  both scopes.
- **In-repository worktrees for session work.** This session used
  `.claude/worktrees/` for its last three changes, as D-5 asks.

### Working state

- **Primary checkout `~/coding-harness`:** on `main` at `de36d82`, clean.
  This addendum comes from `.claude/worktrees/handover-addendum`, which is
  removed after the merge.
- **The Touch-ID signing helper does not survive this session.** It
  consisted of a public-key file and a wrapper in the session's scratch
  directory. To sign the next confirmation:
  1. Read the public key with
     `SSH_AUTH_SOCK=~/Library/Containers/com.maxgoedjen.Secretive.SecretAgent/Data/socket.ssh ssh-add -L`.
     The key is `lakeswitch-decisions`, ECDSA
     `SHA256:LMqOFIm/waO3jemYoQjG8YWpM/iMQKEZW8D+S59QM7c`.
  2. Write a wrapper that sets that `SSH_AUTH_SOCK` and calls `ssh-keygen`.
  3. Commit with `git -c gpg.format=ssh -c user.signingkey=<pubkey file> -c gpg.ssh.program=<wrapper> commit -S`.

  The maintainer runs the commit personally, and the permission layer
  refuses it to a session. The recipe is also in lakeswitch-ai's journal
  entry of today.
- **Probe repositories** `~/m34-probe` and `~/m34-probe2` were removed.

### Validation

- 2026-09-23, #38: `make verify` VERIFY GREEN in the in-repository worktree.
  The probe measurements are in the protocol file.
- 2026-09-23, #39: `make verify` VERIFY GREEN before and after the
  acceptance edit. CI `verify` was green, and GitHub verified `8fc92e4`
  (`true`/`valid`).
- Not tested: the Omnigent session policy and environment passthrough. Both
  belong to M0.

## Addendum — 2026-09-23, after session end: two answers from the maintainer

- **The M0 Omnigent server runs on this machine**, the maintainer's
  MacBook, not on a dedicated machine as the target architecture's M0 row
  says (maintainer, 2026-09-23). Do not ask again. It is noted on the M0
  bead (`coding-harness-eev`) with its consequences: the sandbox is
  seatbelt, interactive sessions share the machine, the pilot stays in a
  throwaway repository, and telemetry must still be off. The next step
  stands: start M0 on this machine.
- **The Touch-ID signing helper can become permanent** as one global git
  alias, `git confirm`, which signs through Secretive with no helper files.
  The session proposed the exact `git config --global alias.confirm …`
  command and the maintainer runs it, since it changes the machine. **Not
  yet set up and not tested.** Until it is, the three-step recipe above
  holds.

## Addendum — 2026-09-23, later: `git confirm` works, lakeswitch #37's provenance lines merged

- **`git confirm` is set up and proven.** The maintainer set the global alias
  on 2026-09-23. A confirmation is now `git confirm -m "…"` or
  `git confirm -F <file>`. It signs through Secretive with Touch ID and needs
  no helper files; it was first used for lakeswitch-ai `a19126b` (GitHub:
  verified). This supersedes the three-step helper recipe above.
- **lakeswitch-ai: the two provenance lines are merged** (pull request #41,
  `492bb07`, class `ai-drafted` and location `plans/`, CI green including the
  signed-decision gate M-30). Pull request #37 still has to merge `main`; its
  branch belongs to the session `lakeswitch-ai-b3`.
