# Phase 7 · Commit

**Model:** Haiku 5.5 — cheap and sufficient.
**Result:** pull request.
**Gate:** CI green.

- **Conventional Commits with a work-item reference:** `feat(<bead>): …`
- **Subject and body in English** (`AGENTS.md`, house rule 1). The body says
  *why* — the *what* is in the diff.
- **Provenance is declared:** `Co-Authored-By:` or `Assisted-by:` where an
  assistant took part. Concealing that share does not make the result more
  dependable; it makes the question unanswerable.
- **The pull request text explains itself.** It is read by someone who does not
  have the artefacts open beside it: what this is about, what was broken, what
  holds now and why, how it was checked — with numbers measured at the state of
  this pull request. Spec, plan and verification evidence are named as
  references at the end; shorthand from the artefacts (D1, A-5, G-3, work-item
  ids) carries no sentence. The same goes for the commit body.
  The acceptance card — what changes for you, how it was checked, what could
  break, and the `done:` line — is carried by both templates, and every pull
  request body keeps it, the multi-decision form included.
- **What it touches is generated, never drawn.** After the last push, run
  `python3 scripts/touch_map.py origin/main HEAD` and paste its output under
  "What it touches" unchanged, in either template. Never edit it, and never
  draw a map by hand or have a model draw one. When the branch moves, run it
  again and replace the whole section. A change with a `design.md` adds one
  line below it: `Architecture delta: plans/changes/<name>/design.md`.
- **Say whether the pull request decides.** A pull request that adds, changes
  or removes a file `provenance.yaml` reserves for `human-decided` (an ADR, an
  ADR answer under `decisions/answers/`, the rule set) is a decision PR. Its
  title is `decide(<scope>): <the decision as a statement>`, its label
  `decision`, and its body comes from
  `.github/PULL_REQUEST_TEMPLATE/decision.md`, filled into a file and passed
  with `gh pr create --label decision --body-file <file>`. One decision per
  pull request; up to three only when none can be accepted without the
  others, in this form:

  ```markdown
  > [!IMPORTANT]
  > **Merging this PR makes 3 decisions:**
  > 1. <decision 1, one sentence>
  > 2. <decision 2, one sentence>
  > 3. <decision 3, one sentence>

  **Your move:** merge = accept all three · comment "change 2: …" · close = reject all.

  **What could break:** <what could fail after the merge, and where it would show>

  done: <verification command>: <result> at <short sha> · <time used> of <appetite>

  ## 1 · <short name of decision 1>
  - **Confirms:** <what becomes binding>
  - **Options:** **<A> (recommended):** <consequence> · <B>: <consequence>
  - **Undo:** <how, or why not>

  ## 2 · <short name of decision 2>
  …

  ## Why these belong together
  <one sentence: what breaks if only some are accepted>
  ```

  "What changes for you", "What it touches", "Where it fits", "After the
  merge", context and evidence then appear once, as in the template. Every
  other pull request takes `.github/pull_request_template.md`. Commits inside
  keep their own types; only the title carries `decide`.
- **If this commit finishes the work item, say so:** a `Closes-Bead: <id>`
  trailer, like GitHub's `Closes #123`. The scope names only *what was worked
  on* — a work item usually has several commits, and the last is rarely the
  finish. Without the trailer the item stays open; that is the right default,
  because a merged pull request often leaves work behind.

Then the end of the artefact lifecycle: the delta into the living capability
spec, lasting decisions as an ADR under `docs/adr/`, the rest into
`plans/changes/archive/YYYY-MM-DD-<name>/`.

The trailer is the only way to declare a closure on merge; a bead is never
closed by hand for a merged pull request. Two places carry it out, both locally,
because the tracker writes to a database this repository does not carry:

- **In the merge step:** once `gh pr view <n> --json state,mergeCommit` shows
  `MERGED` (never merely after queue admission), the tracker's writer runs
  `make close-merged ARGS=--write`. It closes what a `Closes-Bead` trailer on
  the integration branch declares and what is still open — both are checked,
  not claimed. Without `--write` the command only reports.
- **Archive after closure:** once `make close-merged ARGS=--write` has run,
  the session responsible for cleanup runs `make archive` in its own
  up-to-date cleanup worktree, inspects the manifest it prints, and runs
  `make archive ARGS=--write`. It moves only folders whose bead is closed and
  regenerates `plans/INDEX.md`; the result goes through `make verify` and an
  ordinary reviewed pull request, never a direct push and never the
  maintainer's merge.
- **At session start:** the repository's SessionStart hook
  (`tools/claude-code/hooks/beads-start.sh`) runs the same reconciliation
  before `tools/bd prime`, so a closure the merge step missed is caught by the
  next session. It writes only when this session is the only writing session
  in the checkout's repository; a second session skips it and says why. A
  failed reconciliation is shown, never silent; `make close-merged
  ARGS=--write` repeats it by hand.

Only the tracker's one writer reconciles (`AGENTS.md`, house rule 4). The
command is idempotent: a bead that is already closed is left alone.

## The merge

**One path into the merge queue: `scripts/enqueue_pr.py <n>`** (bead
coding-harness-va1l; maintainer grant 2026-11-25, PR #459). The script checks
before it admits: its own copy equals `origin/main`'s, phase 6 is clean and
names the reviewed commit, only records or a clean merge of `main` follow it,
every required check of `main`'s rules is green on the head, and the head's
`Closes-Bead` trailer names the change's open bead. It admits through the
GitHub enqueue call pinned to that head, which can only queue, never merge
directly. Queued is not merged: report "queued" until `gh pr view <n> --json
state` shows `MERGED`, then reconcile the declared closures (above).

1. **Ordinary pull request:** the orchestrator runs `scripts/enqueue_pr.py
   <n>` itself once phase 6 is clean; no request from the maintainer is
   needed. A refusal names every failed condition; fix them, never work
   around them.
2. **Decision PR, handover, unfinished work, archive move, spike, or any
   request the default refuses:** only when the maintainer asks, in their
   own message, e.g. `merge #<n>`. The agent reads the PR (`gh pr view <n>
   --json headRefOid,labels,statusCheckRollup,body`), restates in chat and
   as a PR comment (`Queuing #<n> at <sha> on your request. It decides: …
   It confirms: … CI: green.`), then runs `scripts/enqueue_pr.py <n>
   --maintainer`. The maintainer mode skips the phase-6, change-folder and
   trailer conditions and keeps the checks, the pinned head and
   enqueue-only. It asks every time and is denied in an unattended run.
3. A direct `gh pr merge`, `--admin` or a merge through the API is never the
   path; the ask rules stop it.
4. A group that fails in the queue leaves the pull request open; say so and
   start again at step 1 or 2.

`.claude/settings.json` asks before every merge command it recognises, so the
permission prompt appears right below the restatement; where no prompt can be
answered, the maintainer merges in the GitHub app. It is a brake, not a lock:
another spelling passes it (`docs/WORKFLOW.md`, "What this does not do").
