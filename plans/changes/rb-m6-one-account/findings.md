---
title: "Findings — rb-m6-one-account"
category: findings
created: 2026-10-06
updated: 2026-10-06
status: draft
implementation_status: partial
date: 2026-10-06
last_reviewed: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-bma
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, governance, ruleset, ramp-valves, decision-pr]
---

# Findings — rb-m6-one-account

Phase 6, round 1, on commit `b5f8631` (branch `decide/rb-m6-one-account`,
eight commits over `origin/main` at `d5813ec`), 2026-10-06. The reviewer ran
on Opus 5.5 in a fresh context, wrote nothing but this file and the
regenerated `plans/INDEX.md`, opened no pull request, wrote nothing to the
tracker, recorded no ADR answer and changed nothing at GitHub: every call to
GitHub was a `gh api` GET, through the real `gh` or through a shim in the
session's scratchpad that refuses anything but `gh api <path>`. Measured
against `spec.md` (criteria 1–12, the non-goals and the `[DETAIL]`s) and
`decisions.md` (the maintainer's answer of 2026-10-05); `plan.md` was read
for its deviations, its planted faults and its evidence, not as the
yardstick. `templates/findings.md` does not exist on `origin/main`; the
columns are those of `plans/changes/research-currency/findings.md`.

**Verdict: two BLOCKER, both `[DIVERGENT]`; five MINOR; no `[AMBIGUITY]`.**
The code does what the spec asks, and every criterion that a test can hold
is held. Both blockers are places that now say the opposite of what the
change makes true — that hosted CI runs what `make verify` runs (F-1), and
that RB-M6 at level 4 blocks the merge in CI (F-2). F-1 is two comment lines
and one list marker; F-2 is the maintainer's call, since the rule set is
`human-decided`. The five MINOR are a weakening of the ruleset the check
does not see (F-3), a check that can measure another repository (F-4), a
gate tie that holds only the prefix of the command (F-5), the detection
deviation D1 gave up (F-6), and a test that cannot fail for the hint it
asserts (F-7). The ADR answer is still missing, so `make verify` is red on
`adr-answers`, as `decisions.md` expects; it is no row here.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | `docs/WORKFLOW.md` lines 338–339; `prompts/05-verify.md` lines 9–10; `scripts/ci_gates.py --list` (`make gates`) | `[DIVERGENT]` Three places say that hosted CI runs what `make verify` runs, and this change makes that false for the first time. `docs/WORKFLOW.md` and `prompts/05-verify.md` both annotate `make verify` as "every locally runnable gate — the same the CI runs" and `make gates` as "what the CI runs"; `make gates` (measured on `b5f8631`) lists `[ruleset]` as an ordinary gate, while it marks the hosted-only `lychee` with "laeuft nur in der CI". Against that, `decisions/gates.yaml` gives `ruleset` `placement: writer`, `ci.yml` has no such step (byte-identical to `origin/main`, measured), and the 4.0.0 entry of the rule set says "misst `make verify` auf der Maschine des Maintainers, nicht die gehostete CI". The case it breaks: a reader who sees `ruleset` red in a local run — offline, say — is told CI runs the same and expects the pull request's check to go red too, or trusts hosted CI to notice a weakened ruleset when the maintainer works from another machine; neither happens. Before this change no gate was `writer`, so the local set was a subset of the hosted one and the sentences held loosely. What should hold: the two annotations and the list say that a `writer` gate runs in `make verify` only. The plan's "Not touched: `scripts/ci_gates.py` … a `writer` gate needs no generator change" missed the list, as it missed `tests/test_ci.py` (D1). [criterion 11, "the workflow text stays true"] | fixed in `8524800` — reviewed at `b9ee999`, closed: both annotations now say the CI runs what `make verify` runs "minus a `writer` gate (here only)" and that `make gates` marks such a gate; `make gates` on `b9ee999` prints "— laeuft nur lokal (make verify), nicht in der CI" on `[ruleset]` and on no other gate, in agreement with the gate's `reason` and the 4.0.0 entry. `tests/test_ci.py::test_the_list_marks_a_writer_gate_as_local_only` holds the mark; replayed, R1-1 to R1-5 each turn it red. See "Phase 6, round 2" |
| F-2 | BLOCKER | SPEC | base | `docs/governance/regelwerk.md`, §3 "Die Leiter" row 4, the RB-M6 row (Stufe 4) and the 4.0.0 entry, line `Tests:` | `[DIVERGENT]` The rule set answers "does a broken RB-M6 fail the CI run?" both ways. §3 defines level 4 as "CI blockierend — der Lauf schlägt fehl (BLOCK); ohne Fix kein Merge", and RB-M6 now stands at 4; the same document's 4.0.0 entry says the ruleset is measured by `make verify` on the maintainer's machine, "nicht die gehostete CI". The case: the maintainer removes the `deletion` rule in the web interface on a Monday; on Tuesday an agent's pull request passes the hosted `verify` check (the `ruleset` gate is not in it) and is merged on GitHub without a local `make verify` in between — nothing blocks, although level 4 promises "ohne Fix kein Merge". The spec chose level 4 as a `[DETAIL]` ("the gate blocks the run that phase 4 requires to be green"), reading "der Lauf" as the local run; §3's heading says CI, and no rung of the ladder describes a gate that blocks only on a writer machine. Before this change no level-4 rule rested on a writer-only gate. The rule set is `human-decided`, so which answer stands — level 4 with §3 amended to cover a blocking writer-machine gate, another level, or the divergence rejected with a reason — is the maintainer's, in this decision pull request. [criteria 2 and 3] | decided 2026-10-06 (level 4, ladder amended) — fixed in `a9f55a8`, not reviewed |
| F-3 | MINOR | MAINT | base | `tests/test_repo_settings.py`, `_lists_required_check`; the RB-M6 row, "(der Job, der die Gate-Liste fährt)" | The check accepts a `verify` check from any source, so a ruleset that unpins it stays green. Today's ruleset (read 2026-10-06, `gh api repos/MPAdesso/coding-harness/rulesets/24528176`) requires `{"context": "verify", "integration_id": 15368}` — the check must come from GitHub Actions, the job that runs the gate list, as the amended row says in its parenthesis. Replayed end to end through the shim on `b5f8631`: the same answer with `integration_id` removed — the live test passes. Under one account that is the weakening that matters: unpinned, a commit status `verify: success` posted with the maintainer's token — which every agent holds — satisfies the rule without the job ever running (GitHub's documented meaning of `integration_id`; not measured, it would write). The spec's definition (b) asks for the context only, so the code meets the spec; the maintainer's words were "exactly today's ruleset", and the row promises the job. What should hold: an unpinned `verify` entry is a finding, or the row drops the parenthesis. [criterion 5, spec term (b)] | fixed in `8f9b11e`, not reviewed |
| F-4 | MINOR | MAINT | base | `tests/test_repo_settings.py`, `measure` and `gh_api` (`repos/{owner}/{repo}`) | The check never asserts which repository it measured. `gh` fills `{owner}/{repo}` from `GH_REPO` when that variable is set, else from the repository's default (`gh repo set-default`), else from the remote. Measured on 2026-10-06 on `b5f8631`: `GH_REPO=MPAdesso/lakeswitch-ai` with the variable `RULESET_ASSERT=1` makes the live test pass against lakeswitch-ai's ruleset 22305982, which happens to hold the five; `gh api 'repos/{owner}/{repo}' --jq .full_name` answers `MPAdesso/lakeswitch-ai` there and `MPAdesso/coding-harness` without it. The case: a shell or an agent harness that exports `GH_REPO` for other work, or an instance cloned as a fork whose default points to its upstream (reasoned, not measured), gets a green gate for a repository other than the one it guards. What should hold: the measured `full_name` is compared with the repository the gate runs in, and a mismatch is `not measured`. [criterion 7, "reads the default branch, its active rules and each supplying ruleset"] | fixed in `fba000d`, not reviewed |
| F-5 | MINOR | SPEC | base | `tests/test_repo_settings.py`, `_gate_findings` (`startswith(prefix)`) | The test that ties the gate to the live check holds only the start of the command, so a suffix can switch the live check off with every test green. Planted on `b5f8631`: the gate command becomes `RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs -k "not master"` — `tests/test_repo_settings.py`, `tests/test_ci.py` and `tests/test_gate_machinery.py` pass, `--check-schema` and `--check-ci` pass, and the gate itself runs green with "38 passed, 1 deselected": nothing reads GitHub. A deselection is not a skip, so `-rs` prints nothing about it. Deleting the gate or dropping the variable is caught (planted faults F14, F15, F19); this is the pre-mortem's "the gate got switched off" by a quieter route. What should hold: the tie fails for any command that does not run `test_master_has_a_ruleset_with_required_checks`. [criterion 8, "a test holds the command to the variable the test file reads"] | fixed in `8078d0e`, not reviewed |
| F-6 | MINOR | MAINT | base | `tests/test_ci.py`, `test_every_gate_step_runs_even_after_a_failing_gate` (deviation D1, commit `ba7d17f`) | D1 gives up one detection the old count had by accident: a gate that moves to `writer` now leaves hosted CI with no test red, floor gates included. Planted on `b5f8631`: the floor gate `pytest` set to `placement: writer` and `ci.yml` regenerated — `tests/test_ci.py`, `tests/test_gate_machinery.py`, `--check-schema` and `--check-ci` all pass, and the hosted run would no longer run the test suite. On `origin/main` the same edit turns this test red (17 steps for 18 gates). The verdict on D1 itself: not a weakening of what the test guards — every hosted gate step still needs `if: ${{ !cancelled() }}`, the count still proves the test saw every hosted gate, and D1 reverted is red (planted fault F28, replayed); the old count contradicted the schema, which has allowed `writer` since bead 1jg.2, and would have made any `writer` gate impossible. MINOR, not MAJOR: the move takes two deliberate edits that both show in the diff (`decisions/gates.yaml` and the regenerated `ci.yml`), and no gate but `ruleset` is `writer` today. What should hold: which gates may be `writer` — at least never a `floor: true` gate — is held by a test of its own. [criterion 10, "no ratchet grows"; plan, D1] | fixed in `f010de1`, not reviewed |
| F-7 | MINOR | MAINT | base | `tests/test_repo_settings.py`, `test_the_live_check_goes_red_without_gh_when_the_gate_turns_it_on` (deviation D6) | The test asserts the hint "needs network and a `gh` login" in the output, but pytest prints the hint's source line in every traceback, so the assertion holds without the hint. Planted on `b5f8631`: the condition that appends the hint becomes `if False and any(...)` — the three live-check tests pass, and the failure message no longer carries the hint (measured: the `E` lines show only `not measured: … exit 127: gh is not installed`; the hint text appears once, as source, line 19 of the output). The hint itself works today (measured with the shim's exit 1: the `E` lines read the finding and then "The gate `ruleset` needs network and a `gh` login on this machine; not measured is red, never green (RB-M6)."). What should hold: the test reads the assertion message — an `E` line, or `--tb=line` — not the whole output. [plan, D6] | fixed in `d2f27f8`, not reviewed |
| 2a-1 | — | SPEC | base | `decisions.md` (the maintainer's words); `spec.md`, `[DETAIL]` "The five are a floor" | *Where does the spec admit two plausible readings?* The maintainer said "pull request required, required check verify, no force push, no deletion, no bypass — exactly today's ruleset". The spec reads the five as a floor (a stricter ruleset holds) and says why: turning red on a stricter one would punish the upgrade the decision expects. The other reading — today's ruleset exactly, the `integration_id` pin included — is plausible; its one consequence that matters is F-3. Not an `[AMBIGUITY]`: the spec decides it in the open, reversibly, and the decision pull request lets the maintainer confirm it — provided its decision block says "a floor, not an exact match" in so many words. | answered |
| 2a-2 | — | SPEC | base | `plan.md`, "Not touched" and "Deviations" | *What is missing that would have to be decided while building?* The plan held that a `writer` gate needs no change outside the new files; the build met two places that assumed no `writer` gate exists — `tests/test_ci.py` (D1, recorded) and `ci_gates.py --list` with the two annotations (F-1, not recorded). Everything else the build met is written down in D2–D6. | answered |
| 2a-3 | — | SPEC | base | `spec.md`, criteria 1, 11 and 12 | *Which acceptance criterion cannot go red?* Criteria 1 and 11 are prose, read here (F-1, F-3). Criterion 12 is one measurement and waits on the ADR answer. Criterion 7's "at the commit of this change, it passes" is one measurement, re-measured here green. Every other criterion has a test that a planted fault turns red, except the holes F-5 and F-7. | answered |

Reviewer session: none — no phase 2a ran for this change (`spec.md` names
none, and `decisions.md` records phase 1a as skipped); this review ran in a
fresh session.

## Checked without a finding

- **The amended RB-M6 row (criterion 1).** It names the five requirements,
  the return trigger ("sobald eine zweite Identität existiert, etwa eine
  GitHub App") and keeps "Eine unerreichbare Verwaltungs-Schnittstelle ist
  BLOCK, nicht grün"; code-owner review and the last-pusher approval appear
  only as what returns. Nothing in it goes beyond the maintainer's words but
  the parenthesis on `verify`, which is F-3. No other row of the rule set
  changed (`git diff origin/main...HEAD -- docs/governance/regelwerk.md`:
  the row, `version:`, `updated:` and the new entry only).
- **The precedent of pull request #55 (criterion 3).** Merge `e490772`
  changed `version:` 2.0.0 → 3.0.0, `updated:`, one row and added the entry
  above the previous one, leaving `last_reviewed:` and `review:` alone; this
  change does the same with 3.0.0 → 4.0.0. MAJOR follows §4's semver ("ihre
  Bedeutung geändert"). The entry has the prose, the MAJOR sentence and the
  four mandatory lines; it names the decision of 2026-10-05, the closed
  valve, the writer-machine measurement and LakeSwitch. Its LakeSwitch line
  was re-read on 2026-10-06: ruleset 22305982 "lakeswitch floor" on
  `MPAdesso/lakeswitch-ai` supplies `pull_request`, `required_status_checks`
  (`verify`, `floor`), `non_fast_forward` and `deletion` with an empty
  bypass list.
- **The live check against the real ruleset (criteria 4, 7).** Read on
  2026-10-06: ruleset 24528176, `enforcement: active`, target
  `~DEFAULT_BRANCH`, the four rule types, `bypass_actors: []`,
  `current_user_can_bypass: never`; the branch-rules answer carries the same
  four with `ruleset_id` 24528176. The stubs copy exactly the keys the code
  reads. Through the shim passing everything through, the live test passes
  with three calls (repository, branch rules, ruleset); without
  `RULESET_ASSERT` it is skipped, names the gate `ruleset`, and calls `gh`
  zero times.
- **"Unreachable is BLOCK, not green" (criterion 6).** Measured end to end:
  `gh` exit 1, `gh` not on `PATH`, an empty answer with exit 0, and a
  supplying ruleset that answers 404 each fail the live test with one
  `not measured:` finding naming the step; the gate is `enforcement: block`.
- **Agents and hosted CI.** `.github/workflows/ci.yml` is byte-identical to
  `origin/main` and `--check-ci` is green, so the pull request's `verify`
  check and the floor gate `pytest` there are unaffected: the live test is
  skipped without the variable, and the two tests that run it in a
  subprocess put an empty or fake `gh` on `PATH`. An agent's `make verify`
  without network or login is red on the one gate `ruleset`, and the
  failure reads the cause and the way out (F-7 is only about the test of
  that line). `prompts/05-verify.md` already tells an agent that "a red run
  is reported, not worked around". That only the maintainer's machine
  measures is stated in the gate's `reason`, the module docstring and the
  4.0.0 entry; F-1 is where it is contradicted.
- **The valves (criteria 9, 10).** `ruleset-assert` is gone from
  `REGEL_VENTILE`, a comment stands in its place, and no valve names RB-M6;
  `ramp_valves.py --format=json` lists 26 valves, none due. With the date
  forced: on 2026-10-30 none is due, on 2026-10-31 exactly
  `merge-freshness` (RB-G7, bead coding-harness-34z), which this change does
  not touch (its entry is unchanged in the diff). `commit-identity` and
  `codeowners-here` stay closed because they wait for functions, not for
  the file, and the file defines neither.
- **Kit and ratchets (criterion 10).** `tests/test_repo_settings.py` has the
  role `mechanismus`; `OHNE_MUTATIONSTEST`, `OHNE_AUFRUFER`, `OHNE_TEST`
  and `REIST_NICHT` are not in the diff. The gate's mutation evidence is in
  the file it runs (`*_goes_red_when_*`).
- **The workflow note (criterion 11).** The sentence is appended inside the
  quote paragraph, the dated list is unchanged, and `updated:` moved.
- **The suite (criterion 12, as far as it can be measured now).**
  `make verify` on `b5f8631`, 2026-10-06, commit signing off: `pytest` 638
  passed and 16 skipped; `ruleset` green ("39 passed"); every other block
  gate green except `adr-answers` ("rb-m6-one-account: no answer");
  `docs-links` and `markdownlint` red but report-only. The plan's records
  match. A first run of this review wrote its log under a name another
  session in the same scratchpad also used, and showed `d5813ec` numbers;
  the run quoted here wrote to a name of its own and reports candidate
  `b5f8631`, 19 gates.
- **Planted faults.** Thirteen of the plan's 41 replayed on `b5f8631`, each
  alone, the file restored with `git checkout` (the tree clean after each):
  F01 → 2 of the 4 hidden-bypass cases red; F04 →
  `…_goes_red_when_verify_is_not_required` red; F11 →
  `[rules-exit-1-with-a-valid-answer]` red; F12 →
  `…_goes_red_without_gh_when_the_gate_turns_it_on` red; F14 →
  `test_the_ruleset_gate_turns_the_live_check_on` red; F20 →
  `test_every_named_ramp_exists_and_no_valve_is_orphaned` red; F26 →
  `leerprobe` BLOCK (the RB-M6 enforcer among the red cases); F28 →
  `test_every_gate_step_runs_even_after_a_failing_gate` red; and end to end
  through the shim E01 (bypass actor), E03 (pull-request rule removed), E07
  (`verify` replaced by `lint`), E10 (`gh` exit 1) and E12 (`gh` not on
  `PATH`) → the live test red with the finding named. Every result as
  `plan.md` records it. Own variants: a bypass actor with
  `bypass_mode: pull_request` (red); an empty answer with exit 0 (red); a
  supplying ruleset that cannot be read (red); the `integration_id` removed
  (green — F-3); `GH_REPO` pointing at another repository (green — F-4); a
  `-k "not master"` suffix on the gate command (green — F-5); the floor
  gate `pytest` moved to `writer` (green — F-6); the D6 hint switched off
  (green — F-7).

## Not checked

No hosted run: there is no pull request yet, so the `verify` check on this
branch was not seen. What GitHub returns to a token without write access to
the ruleset (no `bypass_actors` key, research 1.6) was not measured — no
such token was used; the stub case holds the code's answer. Organisation
rulesets, a fork with `gh repo set-default` (F-4 reasons it) and a Claude
Code sandbox that blocks `api.github.com` were not tried. A commit status
posted by hand (F-3) was not tried, since it writes. The plan's other 28
planted faults were not re-run. `research.md` was read only where the spec
cites it.

## For phase 7

`plans/INDEX.md` was regenerated with `python3 scripts/plans_registry.py
--index` for this file. Phase 7 waits on three things:

1. **F-1** — a repair round: the two annotations and `make gates` say that
   a `writer` gate runs locally only.
2. **F-2** — the maintainer's decision on level 4 and §3, in this decision
   pull request; the rule set is `human-decided`, so no agent closes it.
3. **The ADR answer** — recorded with `scripts/harness.py decide adr` as
   the maintainer states it; until then `adr-answers` keeps `make verify`
   red.

F-3 to F-7 can be fixed in the same round or closed as named limits, the
maintainer's choice. The pull request is a decision pull request
(`decide(governance): …`, label `decision`), names bead coding-harness-bma
in its body (house rule 4), says in its decision block that the five are a
floor (2a-1), and says under "after the merge" that the valve
`merge-freshness` still falls due on 2026-10-31.

## Phase 6, round 2 (2026-10-06)

Repair round 1 read, on commit `b9ee999`, 2026-10-06, by a reviewer on
Opus 5.5 in a fresh context that wrote nothing but this file, opened no pull
request, wrote nothing to the tracker, called no external model and changed
nothing at GitHub. It read the repair diff `48f69e9..b9ee999` — the two
annotations, the list mark in `scripts/ci_gates.py`, the new test, the
`updated:` stamps and "Repair round 1" of `plan.md`, where the repair and its
planted faults are recorded — against row F-1 only. F-2 stays the
maintainer's decision; F-3 to F-7 were not re-read. Above this section only
the Status column of F-1 changed.

**Verdict: F-1 is closed; no new row, so nothing of origin `fix-r1`.** What
still stops phase 7 is F-2 and the missing ADR answer.

- **The three places are true now.** `make verify` runs the verify job's
  gates with `--placement lokal`, everything but `hosted`
  (`scripts/verify_all.sh`); the derived `ci.yml` holds everything but
  `writer` (`misst_in`, `generate_ci`). "The CI runs the same, minus a
  `writer` gate (here only)" names exactly that difference, and `make gates`
  now marks `[ruleset]`, the one `writer` gate, and no other line. The words
  agree with the gate's `reason` ("measures it on the writer machine") and
  the 4.0.0 entry ("misst `make verify` auf der Maschine des Maintainers,
  nicht die gehostete CI"). Searched on `b9ee999`: no other sentence in the
  tree says the CI and `make verify` run the same set. The nearest, the
  `verify_all.sh` entry of `OHNE_AUFRUFER` ("Die CI faehrt jedes Gate als
  eigenen Schritt"), says how the CI runs gates — one step each, not through
  the runner — not which.
- **Minimal.** Two comment lines in each of `docs/WORKFLOW.md` and
  `prompts/05-verify.md`, two lines in the `--list` branch of `main`, one test
  with its helper, the `updated:` stamps and the plan record. No generator,
  schema or runner change; `ci.yml` is untouched and `--check-ci` green.
- **Replays.** All five planted faults, R1-1 to R1-5, each alone on a clean
  export of `b9ee999` (`git archive`), `tests/test_ci.py` run, the file
  restored: each turns `test_the_list_marks_a_writer_gate_as_local_only`
  red, R1-4 at the synthetic `writer` gate as `plan.md` says. The export has
  no `.git` and no tracker, so four other tests of the file are red there
  with and without a fault (measured); they are not counted. Own variants:
  the mark keyed on `misst_in(g, "lokal")` (red); the mark moved from the
  command line to the gate's title line (red); `not misst_in(g, "ci")`
  (green, an equivalent rewrite, as it should be); `placement != "both"` and
  `placement == "writer" and not via_local_equivalent` (green — see below).
- **The suite.** `make verify` on `b9ee999`, 2026-10-06, commit signing
  off: `pytest` 639 passed and 16 skipped (one more than round 1, the new
  test); `ruleset` green ("39 passed"); every block gate green except
  `adr-answers` ("rb-m6-one-account: no answer"); `docs-links` and
  `markdownlint` red but report-only, as in round 1.

Seen, and no row:

- The two green variants differ from the code only on gates the file does
  not hold: a `hosted` gate with a command, and a `writer` gate run through
  an action's local equivalent. For the first, the list prints no mark at
  all — measured on `b9ee999` by moving `ruff-check` to `hosted` in a
  scratch copy; at `48f69e9` the list had no placement branch (read) —
  although `make verify` skips such a gate. That is F-1's shape for a gate
  that does not exist, older than this round.
- The longer annotations add three `MD013` line-length hits
  (`docs/WORKFLOW.md` lines 338 and 339, `prompts/05-verify.md` line 9: 103,
  93 and 102 characters, up from 68, 66 and 72). `markdownlint` is
  report-only by its reason.
- The new mark is German, like its neighbour "laeuft nur in der CI" and the
  rest of the `--list` output; house rule 1 translates that output in a pull
  request of its own (bead coding-harness-yim), not in passing.
- `prompts/05-verify.md` still says `make gates` reads "from ci.yml"; it
  reads `decisions/gates.yaml`, as `docs/WORKFLOW.md` says. The words were
  the same at `48f69e9`; the repair kept them.

Not checked: a hosted run (still no pull request); a planted revert of the
two annotations, since no test holds prose — criterion 11 is read.

For phase 7: F-1 no longer stops the pull request. Two things still do —
F-2, the maintainer's decision on level 4 and §3, and the ADR answer,
recorded as the maintainer states it.
