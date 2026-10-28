<!--
Kit template: the repository settings the workflow's rules rely on. Apply
them by hand on the hosting service when the repository adopts the kit, and
check them again after any change of settings (maintainer, 2026-10-27).
Written for GitHub; another host needs the equivalent.
-->

# Repository settings the workflow relies on

## The default branch ruleset

Create one active ruleset that targets the default branch with these rules:

- **Require a pull request** before merging; required approvals may stay at
  zero for a single-maintainer repository.
- **Require status checks to pass**, naming the CI job that runs the gates
  (here `verify`), with **"require branches to be up to date"** switched on.
- **Block force pushes** and **restrict deletions**.

Check it with `gh api repos/<owner>/<repo>/rulesets` and the ruleset's id.

## Auto-merge — only together with the ruleset

Switch on "Allow auto-merge" (`gh api -X PATCH repos/<owner>/<repo> -F
allow_auto_merge=true`) **only after** the ruleset above is active. Without a
required check, auto-merge merges at once, before CI has run. The agent arms
it per pull request with `--match-head-commit <full sha>` and never with
`--admin`; a decision pull request is merged by the maintainer.

## Night-run permissions — a manual step

A night run pushes to its working branches and starts the foreign-model
runner without a person at the keyboard. In Claude Code the maintainer adds
the allow rules for exactly those commands by hand to the local, untracked
settings file (`.claude/settings.local.json`), for example the branch
prefixes `<fix/*>` for `git push` and the runner command. Whether the kit
installs such rules itself is an open decision of the maintainer; until it
is taken, nothing in the kit widens what runs without asking. Merge
commands stay behind a prompt.
