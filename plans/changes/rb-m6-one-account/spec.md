---
title: "Spec — rb-m6-one-account"
status: draft
implementation_status: partial
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-bma
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, governance, ruleset, ramp-valves, decision-pr]
class: feature
change: rb-m6-one-account
adr_question: {proposed: "no", reason: "it applies ADR 0008 (agents act under the maintainer's account, a second identity is the upgrade path) to rule RB-M6; the rule set's own history entry records the amendment, as it did for RB-M2 in pull request #55, and a later rule-set version reverses it"}
---

# Spec — rb-m6-one-account

Rule RB-M6 asks for what one GitHub account can hold, and the repository checks
that against the live ruleset. Inputs: [`research.md`](research.md) (read at
`d5813ec`) and [`decisions.md`](decisions.md) (the maintainer's decision of
2026-10-05, answered). Bead coding-harness-bma.

## Problem

- **The rule cannot be met.** RB-M6 asks for code-owner review and an
  approval not by the last pusher. The maintainer, the agents and every token
  act as one GitHub account, and GitHub lets no author approve their own pull
  request (ADR 0008; research 1.8). No one can give that approval.
- **Its date turns everything red.** The valve `ruleset-assert` falls due on
  2026-10-31; the gate `ramp-valves` is blocking in every local and hosted
  `verify` run, and a due valve has no green state (research 1.3). Since the
  ruleset on `main` requires `verify` and allows no bypass, nothing merges
  until it is fixed.
- **Nothing checks the ruleset.** The enforcer RB-M6 names,
  `tests/test_repo_settings.py`, does not exist in this repository
  (research 1.2). A ruleset weakened in the web interface goes unnoticed.
- **What can be held already stands.** Since 2026-10-05 `main` carries a
  ruleset with exactly what one account can hold (research 1.4).

## Terms

- **Default branch** — the repository's `default_branch` as the API reports
  it (`main` here).
- **Active rules** — what `GET repos/{owner}/{repo}/rules/branches/<default
  branch>` returns; GitHub resolves targeting and leaves out rules of
  rulesets in `evaluate` or `disabled` (research 1.6).
- **Supplying ruleset** — the ruleset an active rule comes from (its
  `ruleset_id`).
- **The five requirements** — (a) *pull request required*: an active rule of
  type `pull_request`; (b) *required check `verify`*: an active rule of type
  `required_status_checks` whose list holds an entry with `context: verify`;
  (c) *no force push*: type `non_fast_forward`; (d) *no deletion*: type
  `deletion`; (e) *no bypass*: every ruleset supplying (a)–(d) shows a
  `bypass_actors` key whose value is an empty list.
- **Writer machine** — where a gate with `placement: writer` runs: the local
  runner (`make verify`), with the maintainer's own `gh` login.

## Acceptance criteria

Each criterion names what refutes it. "A stub" is an API answer the test
invents; no test changes anything at GitHub.

1. **The rule says what one account can hold.** The RB-M6 row, in German and
   in place, says: the branch rules are asserted from within the repository
   and ask for the five requirements; the second approval (code-owner review,
   approval not by the last pusher) returns as soon as a second identity
   exists, for example a GitHub App; an unreachable management API is BLOCK,
   not green.
   *Refuted by:* a row that still asks for code-owner review or last-pusher
   approval as a present requirement, lacks one of the five, the return
   trigger or the BLOCK sentence.

2. **Level and enforcer.** RB-M6 stands at level 4 and names
   `tests/test_repo_settings.py::test_master_has_a_ruleset_with_required_checks`
   and `::test_an_unreachable_api_is_not_a_pass`, and no `Ramp:`; it applies
   in P L I, as before.
   *Refuted by:* `tests/test_regelwerk.py` red, a `Ramp:` left in the row, or
   another level or scope.

3. **Version and history.** The rule set's `version:` is `4.0.0` (MAJOR: the
   rule asks for something else) and `updated:` is the day of the edit. A §7
   entry `### 4.0.0 — <that day>` stands above `3.0.0` with the four
   mandatory lines; it names the decision of 2026-10-05, why MAJOR, the
   closed valve, that the ruleset is measured on the writer machine and not
   in hosted CI, and LakeSwitch's state. No other row and no older entry
   changes.
   *Refuted by:* `tests/test_regelwerk.py` or the gate `frontmatter-current`
   red, a missing item, or a diff of the rule set outside the RB-M6 row, the
   two header keys and the new entry.

4. **Today's ruleset holds, and so does a stricter one.** A pure function
   takes the active rules and the supplying rulesets' details and returns
   findings, empty when the five requirements hold. On a stub equal to the
   live answers of 2026-10-05 (research 1.4) it returns none; on a ruleset
   that asks for more — approvals, code-owner review, approval of the last
   push, further checks or rules — it returns none.
   *Refuted by:* a finding on either stub.

5. **Each requirement that goes is a finding.** The function returns at
   least one finding, naming what is missing, when: a bypass actor is added
   to a supplying ruleset; any one of the four rule types is removed;
   `verify` is not among the required checks; there is no active rule at all.
   *Refuted by:* any of these stubs returning no finding.

6. **Not measured is not "no".** Each of these returns at least one finding
   that begins `not measured:` and names the step, never an empty list: `gh`
   is not installed; an API call exits non-zero (network, login, permission);
   an answer is not JSON or lacks its expected shape; a supplying ruleset's
   detail has no `bypass_actors` key (what GitHub returns to a token without
   write access to the ruleset). The measuring function the live test calls
   is the one these stubs drive.
   *Refuted by:* a stub of any case returning no finding, or a finding for it
   that reads as a rule violation instead of `not measured:`.

7. **The live check.** With the environment variable `RULESET_ASSERT=1`,
   `test_master_has_a_ruleset_with_required_checks` reads the default branch,
   its active rules and each supplying ruleset through `gh api` and fails
   listing every finding. Without the variable it is skipped, with a reason
   that names the gate `ruleset`, and calls nothing. In that gate on the
   maintainer's machine, at the commit of this change, it passes.
   *Refuted by:* a red gate run on today's ruleset, a skip or a pass with the
   variable set while `gh` fails, or a call to `gh` without the variable.

8. **The gate.** `decisions/gates.yaml` carries `ruleset` with the command
   `RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs`,
   `job: verify`, `enforcement: block`, `floor: false`,
   `placement: writer`, neither `needs_tracker` nor `needs_history`, and a
   reason saying why only the writer machine measures. A test holds the
   command to the variable the test file reads. `.github/workflows/ci.yml` is
   byte-identical before and after.
   *Refuted by:* `ci-drift` red, a diff of `ci.yml`, or the tying test green
   while the gate's variable differs from the file's.

9. **The valve is closed, not dropped.** `ruleset-assert` is gone from
   `scripts/ramp_valves.py` and from the RB-M6 row; a comment where the entry
   stood says it closed, that the gate `ruleset` asserts the ruleset, and
   rule-set version 4.0.0; the §7 entry's `Tests:` line says the same. No
   valve names RB-M6 any more.
   *Refuted by:* `python3 scripts/ramp_valves.py --format=json` listing
   `ruleset-assert`, `tests/test_regelwerk.py` red, or the comment or the
   history line missing.

10. **No ratchet grows, the kit carries it, no other valve falls due.**
    `tests/test_repo_settings.py` has the role `mechanismus` in
    `scripts/kit/manifest.yaml`; `OHNE_MUTATIONSTEST`, `OHNE_AUFRUFER`,
    `OHNE_TEST`, `REIST_NICHT` and its cap are unchanged. The file defines
    neither `test_recent_commits_carry_a_real_identity_and_trailers` nor
    `test_codeowners_covers_every_human_decided_path` (research 1.3).
    *Refuted by:* `tests/test_ci.py` or the gate `leerprobe` red, one of
    the lists longer, or `ramp_valves.py` reporting a due valve on a day
    before 2026-10-31.

11. **The workflow text stays true.** `docs/WORKFLOW.md`'s note "Not all of
    it is here yet" gains one sentence after its list: since the day of this
    change `tests/test_repo_settings.py` exists and asserts the branch
    ruleset (rule RB-M6), while the container fence §3 describes is not in
    it yet. The dated list itself is not edited; `updated:` moves.
    *Refuted by:* the note still implying the file is absent, an edit to the
    dated list, or `frontmatter-current` red.

12. **On this repository.** Once the maintainer's ADR answer is recorded and
    `plans/INDEX.md` is regenerated, `make verify` on the maintainer's
    machine is green, the gate `ruleset` included.
    *Refuted by:* any red block gate.

## Non-goals

- **The second approval and a second identity.** Code-owner review,
  last-pusher approval and a bot identity return by a later rule-set version
  when the identity exists. No machine trigger is built: no file here
  declares agent identities, and RB-M2's exception names its end the same
  way, in words.
- **A ruleset check in hosted CI.** The workflow token cannot see the bypass
  list (research 1.6), and a token that can would also be able to change the
  ruleset it checks.
- **Any change to GitHub** — the ruleset, settings, labels or secrets.
- **The valve `merge-freshness`** (RB-G7). It falls due on the same day; the
  gate `ramp-valves` still turns red on 2026-10-31 through it unless it is
  handled on its own. No bead tracks it (research 1.3).
- **Other texts with RB-M6's old content:** `docs/governance/quality-gates.md`
  row MG-3 (human-decided) and `docs/architecture/target-architecture.md`
  rows T0/T1 (research 1.10).
- **The rest of the origin file:** the container fence, and the CODEOWNERS
  (RB-M7) and commit-identity (RB-P4) checks valves expect there.
- **RB-M2, every other row, the rule set's translation** (bead
  coding-harness-yim), **a new ADR**, and **a rename of the enforcer
  function** (it keeps the name RB-M6 has carried since 1.0.0, "master"
  included).

## Open decisions

No `[DECISION]` is open: the maintainer's answer of 2026-10-05 settles what
the rule asks for (`decisions.md`). The ADR question is proposed "no" in the
header and waits for the maintainer's one-sentence answer, recorded with
`scripts/harness.py decide adr` exactly as stated; until then the gate
`adr-answers` is red. Decided here, each revisable:

- `[DETAIL]` **Class `feature`.** The change alters how a rule is checked (a
  new assertion and gate) and carries a decision; `bounded` excludes
  "deciding anything new". The sibling `frontmatter-current` — one check, one
  gate entry — was a `feature` too. Classed per `docs/WORKFLOW.md`, "Change
  classes"; "D-13" defines no classes in either repository (research 1.9).
- `[DETAIL]` **No ADR proposed.** ADR 0008 already decided the account fact
  and the upgrade path; PR #55 amended RB-M2 on the same ground without one.
- `[DETAIL]` **The five are a floor.** "Exactly today's ruleset" says the
  rule asks for what is set today; a stricter ruleset still meets it.
  Turning red on a stricter one would punish the upgrade the decision
  expects.
- `[DETAIL]` **Where it is measured: the writer machine, every
  `make verify`.** Only the maintainer's login sees the bypass list, the one
  property an admin weakening would change; the hosted drift timer that RB-G2
  prefers for outside counterparts cannot see it, and a writer gate on the
  drift job would never run. The hosted `verify` check stays unaffected, so
  no pull request is blocked by GitHub for a ruleset change. Consequence:
  `make verify` needs network and a `gh` login, or is red — as RB-M6's last
  sentence asks.
- `[DETAIL]` **Level 4.** The gate blocks the run that phase 4 requires to be
  green. The history entry says that hosted CI does not measure it.
- `[DETAIL]` **No bypass on any supplying ruleset.** If a second ruleset with
  a bypass duplicated a required rule, the check goes red although a
  bypass-free one holds it: a rare false alarm, failing closed, for a much
  simpler check.
- `[DETAIL]` **Targeting is GitHub's.** The branch-rules endpoint resolves
  `~DEFAULT_BRANCH`, `~ALL` and patterns; the default branch is read from the
  API, so the test holds in any instance.
- `[DETAIL]` **The opt-in is an environment variable,** `RULESET_ASSERT`: the
  floor gate `pytest` runs the whole suite in hosted CI and must not call
  GitHub, and its command is a governance act to change.
- `[DETAIL]` **The workflow note gets an added sentence,** not an edited
  list: the list is a dated measurement.
- `[DETAIL]` **The German wording** of the row and the history entry is the
  plan's (`plan.md`); its meaning is criterion 1's.
