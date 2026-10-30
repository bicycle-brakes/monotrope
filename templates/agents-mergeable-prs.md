<!--
Kit template: a section for the AGENTS.md of a repository that adopts this
workflow. Copy it into that file and fill the two placeholders. It is the
portable form of the rules in this repository's AGENTS.md, "Pull requests
stay mergeable" (maintainer, 2026-10-27).
-->

## Pull requests stay mergeable

A pull request that stays open while `main` moves ends in a conflict nobody
wants to resolve. These rules keep each one small enough to merge:

- **Synced on request, by the helper.** Every working day the day session or
  the night orchestrator calls the sync helper explicitly (in this kit
  `python3 scripts/pr_sync.py sync --root .`): an open pull request that
  test-merges cleanly against `main` gets `main` merged and pushed with its
  generated index rebuilt, one that conflicts is reported with its files
  and resolved while the conflict is small. A hand merge uses the same
  engine (`python3 scripts/pr_sync.py merge-main --root .`). GitHub's
  server-side Update branch and merge buttons cannot run the local helper;
  the unchanged generated-file gate stays their backstop.
- **Small enough to review.** A pull request that would change more than
  about `<lines, default 800>` lines (generated files not counted) is cut
  into slices, one pull request per slice, each with its own review.
- **Merged when green, without waiting.** A pull request the agent may merge
  itself is armed with `gh pr merge <n> --auto --merge --match-head-commit
  <full sha>`, never `--admin`; a decision pull request never is. This is
  safe only while the default branch's ruleset requires the CI check and an
  up-to-date branch (`templates/repo-settings.md`). After a branch update the
  head changes: re-arm with the new head.
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
  generator on a conflict, never merged by hand — `plans/INDEX.md` by
  `make index` or the helper above, which renders it from the complete
  merged tree.
- **Hot files are split.** A file that most changes touch is split by
  responsibility, and each change gets its own test file.
