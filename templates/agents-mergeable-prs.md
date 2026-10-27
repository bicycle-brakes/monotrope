<!--
Kit template: a section for the AGENTS.md of a repository that adopts this
workflow. Copy it into that file and fill the two placeholders. It is the
portable form of the rules in this repository's AGENTS.md, "Pull requests
stay mergeable" (maintainer, 2026-10-27).
-->

## Pull requests stay mergeable

A pull request that stays open while `main` moves ends in a conflict nobody
wants to resolve. These rules keep each one small enough to merge:

- **Synced daily, automatically.** Every working day each open pull request
  is test-merged against `main`
  (`git merge-tree --write-tree origin/main origin/<branch>`): one that
  merges cleanly gets `main` merged and pushed, one that conflicts is
  reported with its files and resolved while the conflict is small.
- **Asked about after `<working days, default 5>` working days.** An older
  pull request is put to the maintainer: finish, shrink or close.
- **Few at once on a hot file.** At most `<number, default 3>` open pull
  requests change the same hot file — here `<the files most changes
  touch>`. The oldest is finished before a new one opens.
- **Reviewed on a current base.** Phase 6 reviews the branch after it has
  merged `main`; a verdict holds only for the commit it saw.
- **Not stacked without a reason.** A pull request built on another names
  the reason in its body; the base merges before the next opens.
- **Generated files are regenerated.** A generated file is rebuilt by its
  generator on a conflict, never merged by hand.
- **Hot files are split.** A file that most changes touch is split by
  responsibility, and each change gets its own test file.
