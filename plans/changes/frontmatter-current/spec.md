---
title: "Spec — frontmatter-current"
status: draft
implementation_status: none
date: 2026-09-29
last_reviewed: 2026-09-29
updated: 2026-09-29
supersedes: null
superseded_by: null
bead: coding-harness-qd7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec]
---

# Spec — frontmatter-current

## Problem

A document's header can say the document is older than its content, and
nothing notices. The maintainer asked for a basic mechanism that keeps headers
current and stops a stale one from being merged (`decisions.md`, items 1–2).
Today (`research.md`, corrections and addendum, measured on `9f14283`):

- No header records when its content last changed. `updated:` stands in 0 of
  30 `docs/` files with frontmatter; `last_reviewed` records a review, not a
  change.
- `provenance.yaml` declares per prefix whether a file must carry frontmatter,
  but nothing reads that field. The documents the maintainer named are not all
  declared: `docs/adr/`, `docs/how-to/` and `docs/governance/` are `optional`,
  `docs/architecture/` and `docs/research/` have no entry, and
  `.claude/agents/` — excluded by the maintainer — is `required`.
- The six ADRs carry no frontmatter at all.
- The hosted checkout has one commit of history. In CI, `git log -1 -- <file>`
  returns the checked-out commit for every file — on a pull request, GitHub's
  merge commit, dated the day of the run. The generated checkout step has no
  `with:`, so no gate can ask for more history.

## Terms

- **Held file** — a file this check holds (criterion 1).
- **Reference date** — the date a held file's `updated:` must not be older
  than (criterion 3).
- **The stamp** — `python3 scripts/check_frontmatter_current.py --stamp`.

## Acceptance criteria

1. **Held files come from the map.** A file is held exactly when it is a
   Markdown file (`*.md`), tracked or untracked-but-not-ignored, present on
   disk, not under an `excluded:` prefix of `provenance.yaml`, and the longest
   `paths:` prefix that matches it declares `frontmatter: required`. A file
   under `optional`, `none` or no entry is never held, whether or not it
   carries frontmatter.
   *Refuted by:* a temporary repository in which a stale file under an
   `optional`, `none`, unmapped or excluded prefix is reported, a stale file
   under `required` is not, or a shorter prefix wins over a longer one.

2. **What is reported.** A held file is reported when it has no frontmatter
   block; when the block has no top-level `updated:` line, more than one, or a
   value that is not a `YYYY-MM-DD` date (quoted or not); when `updated:` is
   earlier than the file's reference date; or when `updated:` is later than the
   UTC date at run time plus one day. Nothing else is reported.
   *Refuted by:* any of these cases exiting 0 in a temporary repository, or a
   held file whose `updated:` equals its reference date being reported.

3. **The reference date.** For a held file whose content equals `HEAD`, it is
   the committer date — as a calendar date in the offset recorded in that
   commit — of the newest non-merge commit that changed the file at its
   current path, under git's default history simplification
   (`git log -1 --no-merges --format=%cs -- <path>`). A rename or move to the
   current path counts as a change. A merge commit never counts, including the
   merge commit GitHub builds for a pull request. For a held file that is
   untracked or differs from `HEAD` in the index or the worktree, the reference
   date is today on the running machine's clock and timezone.
   *Refuted by,* each in a temporary repository: a body change committed a day
   after the stamp that exits 0; a `git mv` committed a day after the stamp
   that exits 0; a file changed only on a branch, stamped on the day of the
   branch commit and merged with `--no-ff` days later, that is reported; a
   commit made at 23:30 −05:00 whose stamp names that local day being
   reported; an uncommitted edit under yesterday's stamp that exits 0.

4. **Exit codes and the message.** Exit 0 when nothing is reported. Exit 1
   when something is: one line per file with the path, the finding and — for a
   stale file — both dates, then the fix
   `python3 scripts/check_frontmatter_current.py --stamp` verbatim. Exit 3,
   measuring nothing, when the repository is shallow (the message names
   `fetch-depth: 0`), when the path is not a git work tree or has no commit,
   or when `provenance.yaml` cannot be read.
   *Refuted by:* a `--depth 1` clone that exits 0 or 1; a failing run whose
   output lacks the fix command.

5. **The stamp.** `--stamp` sets `updated:` to today's local date in every held
   file reported for a missing, unreadable, stale or future `updated:`. It
   replaces that one line or, when the line is missing, inserts it directly
   after the top-level `last_reviewed:` line, or else as the last line of the
   block. It changes no other byte. A file reported for a missing frontmatter
   block or for more than one `updated:` line is named and left unchanged, and
   the stamp then exits 1. A second run directly after the first changes no
   file, and the check then reports none of the stamped files.
   *Refuted by:* a byte difference outside the `updated:` line; a second run
   that rewrites a file; a stamped file still reported; a header invented for
   a file that had none.

6. **The gate.** `decisions/gates.yaml` carries `frontmatter-current` with the
   command `python3 scripts/check_frontmatter_current.py`, job `verify`,
   enforcement `block`, placement `both`, and a new optional boolean key
   `needs_history: true`. `scripts/ci_gates.py` refuses a non-boolean
   `needs_history` and gives the checkout of each generated job that runs such
   a gate `fetch-depth: 0`, and no other job. `.github/workflows/ci.yml` is
   regenerated.
   *Refuted by:* `ci-drift` red; the `verify` job's checkout without
   `fetch-depth: 0`; the `drift` job's checkout with it; `--check-schema`
   accepting `needs_history: "yes"`.

7. **This repository is green and stays so.** `provenance.yaml` declares
   `docs/adr/`, `docs/how-to/` and `docs/governance/` `required`, adds
   `docs/architecture/` and `docs/research/` as `required`, and sets
   `.claude/agents/` to `none`. Every held file carries a current `updated:`;
   the six ADRs get a full header with every key `scripts/check_docs.py`
   requires. `scripts/new_change.py`, Variante A of `templates/handover.md` and
   the frontmatter block of the handover skill write `updated:`, and the
   handover field list allows it. On the pull request that introduces the
   gate, hosted CI runs it green.
   *Refuted by:* the gate red on that pull request; a `.claude/agents/` file
   held; a fresh `new_change.py` scaffold reported by the check;
   `check_docs.py` reporting a missing header key under `docs/adr/`;
   `tests/test_feedback_channel.py` failing on `updated`.

## Non-goals

In this change, not now:

- **Generalising** — other date fields, other checks on header content, or a
  shared frontmatter schema for all validators.
- **An edit hook** that stamps on every save in Claude Code.
- **A validator for the whole provenance map** — `allowed:` classes per
  prefix, unmapped paths, and the origin repository's prefixes that name
  directories that do not exist here (`docs/vertrieb/`, `docs/lessons/` …).
- **The lakeswitch-ai port**, and a kit instance's first run (files copied from
  here arrive with this repository's `updated:` and need one stamp there).
- **Comparing only the body**, so that a header-only commit (a review status,
  `last_reviewed`) would not need a new stamp.
- **Making `verify` a required status check.** Whether GitHub refuses a merge
  on a red `verify` was not read (research addendum 12). If it is not
  required, `block` makes the check red but does not by itself stop a merge;
  asserting the branch rules from the repository is rule RB-M6's work.
- `scripts/check_docs.py`'s key list and `scripts/plans_registry.py`'s
  `REQUIRED` — both stay as they are (see the `[DETAIL]` on one owner).
- The user-level handover skill outside this repository.

## Open decisions

### [DECISION] 1 — Who confirms the headers on the six accepted ADRs

**Answered 2026-09-29 by the maintainer: option 2** — "I want the headers, but
without a signature" (`decisions.md`, item 5). The implementing session
commits the six headers as an ordinary commit.

```
Goal in one sentence:  The six accepted ADRs have no header yet; to be held,
                       each gets one — does that edit need your Touch-ID
                       signature, like every change to an accepted ADR since
                       2026-09-23?
Options:
  1. You confirm it.   The implementing session prepares the six headers and
                       leaves them uncommitted; you commit them with
                       `git confirm`. Consequence: one Touch-ID step before
                       the pull request can merge; accepted ADRs keep changing
                       only through your signed commit, and the open question
                       whether this repository adopts the signed-decision rule
                       stays open.
  2. Ordinary commit.  The session commits the headers like any other file;
                       your review of the pull request is the confirmation.
                       Consequence: no extra step, but the first change to
                       accepted ADRs since 2026-09-23 that reaches main
                       without your signature — a precedent that header-only
                       edits need none, set in passing.
Recommendation:        Option 1 — because it costs one touch and does not
                       settle an open governance question by precedent.
If you say "ok":       The session writes the six headers (values in
                       plan.md), commits everything else, and stops. You run
                       `python3 scripts/check_frontmatter_current.py --stamp`,
                       then `git add docs/adr && git confirm -m "docs(adr):
                       add the frontmatter header to ADRs 0001–0006"`, and
                       push. CI is red on the pull request until that commit
                       is there.
What is lost:          Option 2 would let the implementation run to a green
                       pull request without you.
```

The header adds no decision: every value restates a line the ADR already
carries (`[DETAIL]` on ADR header values below). Background:
`research.md`, addendum 11.

### `[DETAIL]` — decided here, with the reason

Each of these is reversible and binds nothing beyond this change.

- **Committer date, not author date.** A rebase or amend makes the commit
  again, and the stamp has to follow; the fix is the same stamp. Consequence:
  a squash or rebase merge on GitHub would rewrite committer dates on `main`
  to the merge day. This repository merges with merge commits (research
  addendum 12), which keep the branch's commits and their dates; if that
  changes, this rule is revisited.
- **Timezone.** The reference date is the calendar date in the offset
  recorded in the commit (`%cs`); the stamp writes the local date of the
  machine that runs it. On the machine that commits, the two agree. A stamp
  at 23:59 and a commit at 00:01 turn red, and the stamp fixes it. The future
  bound uses the UTC date plus one day, so no timezone makes a fresh stamp
  look like the future.
- **Merge commits never count.** A pull request's merge commit and GitHub's
  merge commit on `main` are made by a machine on the day of merging.
  Counting them would turn every file both sides changed red on a date no
  stamp in the pull request can know. Default history simplification follows
  the side a merge is identical to, so a file changed on one side is dated by
  that side's commit. Cost: text first written in a conflict resolution is
  dated by the newer side's commit, not by the merge.
- **Renames count.** A path-limited log shows a move as a change at the new
  path; seeing through it (`--follow` plus a similarity test) costs more than
  one stamp per move, and a moved document has new links a reader may care
  about. Archiving a change folder therefore needs a stamp in the same commit,
  and the check says so.
- **Every byte counts, the header included.** One `git log` per file, no diff
  parsing; a header-only commit needs a stamp too. Body-only comparison is in
  the non-goals.
- **Uncommitted and untracked files are held against today,** so `make
  verify` and the stop hook catch a missing stamp before the commit, not after
  the push.
- **A shallow clone is refused, not deepened.** A check that fetches changes
  the repository it measures and needs the network. The gate declares its
  need, the generator provides the full checkout, and the refusal makes a
  removed `fetch-depth: 0` loud.
- **`needs_history` is a key of the gate, not a full checkout for every
  job.** The one gate list stays the only source of a CI property, and
  retiring the gate retires its full clone — the same pattern as
  `needs_tracker`.
- **`optional` files are not held, even with frontmatter.** The map defines
  `optional` as "not yet classified"; holding those files would claim work
  nobody did. Once the five prefixes change, no `optional` file carries
  frontmatter (research addendum 5), so the rule costs nothing today. Making a
  document held is one line in the map.
- **`.claude/agents/` becomes `none`, not a fourth value.** Decisions item 3
  excludes it, and `.claude/commands/` — the same kind of file — is already
  `none`. The map's comment is reworded so that `none` means "no document
  header": a frontmatter a tool reads as configuration may stand there, and no
  document check reads it. Nothing else reads the field.
- **Enforcement `block`, `floor: false`.** `block`, because the maintainer
  asked that a stale header cannot be merged. No `report` phase is needed:
  the backfill makes the gate green in the same pull request, and a ramp is
  for checks that turn the tree red on their first day. `floor: false`,
  because joining the non-negotiable set is a governance act, not a spec's.
- **Markdown only.** Decisions item 2 speaks of Markdown documents;
  frontmatter is a Markdown convention.
- **One owner for `updated:`.** `check_docs.py` and `plans_registry.py` do not
  learn the field. The handover field list gets `updated` as optional: it has
  to allow what the new check requires, and requiring it there too would be a
  second enforcement of one rule.
- **Exit 1 for findings,** as `check_docs.py` and
  `check_decision_continuity.py` use it, **exit 3 for "cannot measure"**
  (bead coding-harness-4t8).
- **ADR header values restate the ADR.** Title from the heading, `status:
  accepted` (every Status line begins so), `created` from the first date of
  the Date line, `last_reviewed` from its acceptance date, `owner:
  framework-architect`, `provenance: human-decided` (the map's only class for
  `docs/adr/`), `produced_by` a Claude Code session, and `review: pending` as
  in `docs/governance/regelwerk.md` — an approval name written by an agent
  would be the signature rule RB-M2 exists against; the body's Review line
  stays the record of acceptance.
- **The three writers write `updated:`,** so a new held file is not born
  reported: the entry script, the handover template and the handover skill.
  The skill takes effect after `tools/claude-code/install.sh`.
- **The script is `scripts/check_frontmatter_current.py`** beside the other
  `check_*` scripts, with `--stamp`, and `--root` so tests can point it at a
  temporary repository.
- **The script and its test travel with the kit (`mechanismus`).** The gate
  file travels, and every gate's script travels with it. The tests build their
  own repositories and never read this repository's dates: in the kit probe's
  fresh one-commit copy, a test over real dates would be red on every day
  after the stamp.
