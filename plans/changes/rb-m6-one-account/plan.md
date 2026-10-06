---
title: "Plan — rb-m6-one-account"
status: draft
implementation_status: partial
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-bma
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, governance, ruleset, ramp-valves, decision-pr]
---

# Plan — rb-m6-one-account

```text
For you:     RB-M6 asks for exactly the ruleset you set today; make verify on your machine checks it at GitHub and goes red if it weakens or GitHub cannot be reached
Done when:   criteria 1–12 hold and make verify is green with the new ruleset gate, after you answer the ADR question (proposed: no)
Appetite:    2 h of phase 4, one repair round included
Not now:     the second approval and a bot identity; a ruleset check in hosted CI; the merge-freshness valve due the same day
Pre-mortem:  suppose it failed: most likely because make verify went red offline once too often and the gate got switched off
Starts unless you say stop.
```

Implements `spec.md`, criteria 1–12; class `feature`, ADR question proposed
"no". Stage 1: no model markings. Facts read at `d5813ec`. The phase-2/3
validator the prompts name is not in this repository; the headers are held by
`python3 scripts/plans_registry.py --check`.

## Decided in phase 3

No `[DECISION]` is open.

- `[DETAIL]` **Appetite 2 h:** about 1 h 30 min of steps, the rest one repair
  round.
- `[DETAIL]` **Names:** `gh_api`, `measure`, `ruleset_findings`,
  `LIVE_ENV = "RULESET_ASSERT"`, `REQUIRED_CHECK = "verify"`.
- `[DETAIL]` **Stubs** copy from the live answers of 2026-10-05 (research
  1.4) only the keys the code reads: `type`, `parameters`, `ruleset_id`,
  `id`, `bypass_actors`, `default_branch`.
- `[DETAIL]` **`-rs` in the gate command:** a skip would print its reason in
  the gate's output instead of passing quietly.
- `[DETAIL]` **"gh missing" runs the real `gh_api` with `PATH` set to an
  empty temporary directory;** the other unreachable cases stub the API.
- `[DETAIL]` **`<DAY>`** below is the day phase 4 writes the text
  (`date +%F`); the decision date stays 2026-10-05.

## Steps

0. **The ADR answer** (before step 1; nothing else waits on it). The
   orchestrating session asks the maintainer: "Does this change need an ADR?
   Proposed: no — it applies ADR 0008 to RB-M6, and the rule set's history
   entry records it, as for RB-M2 in #55." Only once answered:
   `python3 scripts/harness.py decide adr --change rb-m6-one-account --answer no --reason "<the maintainer's sentence, English>" --stated-in "<session, date>"`
   writes `decisions/answers/rb-m6-one-account/adr.yaml`. A "yes" stops
   phase 4: the ADR comes first.

1. **`tests/test_repo_settings.py`** (new, 50 min). English module docstring:
   what RB-M6 asks (the five requirements), why only the writer machine
   measures (research 1.6), that not measured is red, and the return trigger
   (a second identity). Then:
   - `gh_api(path) -> tuple[int, str]`: `subprocess.run(["gh", "api", path],
     cwd=REPO_ROOT, capture_output=True, text=True)`; stdout on 0, else
     stderr; `FileNotFoundError` → `(127, "gh is not installed")`.
   - `RULE_TYPES`: `pull_request` → "pull request required",
     `required_status_checks` → "required check verify",
     `non_fast_forward` → "no force push", `deletion` → "no deletion".
   - `ruleset_findings(rules, rulesets) -> list[str]`: empty `rules` → "no
     active rule on the default branch — nothing binds a merge". Per type, the
     matching rules (for `required_status_checks` only those listing
     `context == REQUIRED_CHECK`); none → "<what> is not asked for". The
     `ruleset_id`s of all matches are the suppliers; per supplier: no detail
     → `not measured: ruleset <id> could not be read`; no `bypass_actors` key
     or not a list → `not measured: ruleset <id> shows no bypass list — GitHub
     shows it only to whoever may edit the ruleset`; a non-empty list →
     "ruleset <id> lets <actors> bypass it".
   - `measure(api=gh_api) -> list[str]`: `repos/{owner}/{repo}` →
     `default_branch` (non-empty string); `repos/{owner}/{repo}/rules/branches/`
     + `urllib.parse.quote(branch, safe="")` → a list of mappings; for each
     supplier id `repos/{owner}/{repo}/rulesets/<id>` → a mapping. Any
     non-zero exit, non-JSON or wrong shape returns at once
     `["not measured: <path>: <reason>"]`. Then `ruleset_findings`.
   - Tests (names carry the mutation pattern of `tests/test_ci.py`):
     `test_todays_ruleset_holds`, `test_a_stricter_ruleset_still_holds`,
     `test_the_ruleset_check_goes_red_when_a_bypass_is_added`,
     `test_the_ruleset_check_goes_red_when_a_rule_is_removed` (parametrized
     over `RULE_TYPES`), `test_the_ruleset_check_goes_red_when_verify_is_not_required`,
     `test_the_ruleset_check_goes_red_on_an_empty_rule_list`,
     `test_a_hidden_bypass_list_is_not_a_pass`,
     `test_the_measurement_holds_on_todays_answers` (a stub API answering by
     path), `test_an_unreachable_api_is_not_a_pass` (parametrized: no `gh`
     on `PATH`, exit 1, non-JSON, `[]` for the repository),
     `test_master_has_a_ruleset_with_required_checks`
     (skipped unless `os.environ.get(LIVE_ENV) == "1"`, with the reason
     "reads GitHub; runs in the gate ruleset on a writer machine
     (decisions/gates.yaml)"; body `findings = measure()`, then
     `assert not findings, "\n".join(findings)`),
     `test_the_ruleset_gate_turns_the_live_check_on` (reads
     `decisions/gates.yaml`: gate `ruleset` has the command prefix
     `f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py"`, job
     `verify`, enforcement `block`, placement `writer`, `floor` false).
   - Defines neither `test_recent_commits_carry_a_real_identity_and_trailers`
     nor `test_codeowners_covers_every_human_decided_path`.

2. **`decisions/gates.yaml`** (5 min), directly after `ramp-valves`:

   ```yaml
     - id: ruleset
       title: The branch ruleset asks for what rule RB-M6 asks
       command: RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs
       job: verify
       enforcement: block
       floor: false
       placement: writer
       reason: The ruleset lives at GitHub and changes without a commit; GitHub shows its bypass list only to whoever may edit it, so the maintainer's own gh login measures it on the writer machine, and an unreachable API is red (RB-M6).
   ```

3. **`scripts/ramp_valves.py`** (5 min): delete the `"ruleset-assert"` entry
   of `REGEL_VENTILE`; in its place:

   ```python
       # "ruleset-assert" (RB-M6) closed on <DAY>: the gate `ruleset` asserts the
       # branch ruleset (tests/test_repo_settings.py); rule set 4.0.0 records it.
   ```

4. **`scripts/kit/manifest.yaml`** (2 min), after `tests/test_model_endpoints.py`:

   ```yaml
     - prefix: tests/test_repo_settings.py
       rolle: mechanismus
       reason: "RB-M6: asserts the ruleset of whichever repository it runs in; the live part runs only in the gate `ruleset`, the rest checks invented API answers, so it holds in the probe copy (bead coding-harness-bma)"
   ```

5. **`docs/governance/regelwerk.md`** (15 min). Header: `version: 4.0.0`,
   `updated: <DAY>`; nothing else in the header. The RB-M6 row becomes:

   ```markdown
   | **RB-M6** | Die Branch-Regeln werden aus dem Repository heraus behauptet und fordern, was ein Konto halten kann: Pull Request erforderlich, geforderte Prüfung `verify` (der Job, der die Gate-Liste fährt), kein Force-Push, kein Löschen, kein Bypass. Die zweite Zustimmung — Code-Owner-Review und Zustimmung nicht vom letzten Pusher — kehrt zurück, sobald eine zweite Identität existiert, etwa eine GitHub App. Eine unerreichbare Verwaltungs-Schnittstelle ist BLOCK, nicht grün | 4 | `tests/test_repo_settings.py`::test_master_has_a_ruleset_with_required_checks · ::test_an_unreachable_api_is_not_a_pass | P L I |
   ```

   In §7, above `### 3.0.0 — 2026-09-30`:

   ```markdown
   ### 4.0.0 — <DAY>

   **RB-M6** fordert, was ein Konto halten kann. Maintainer, Agenten und jedes
   Token handeln hier unter demselben GitHub-Konto, und GitHub lässt niemanden
   den eigenen Pull Request freigeben — Code-Owner-Review und „Zustimmung nicht
   vom letzten Pusher" waren so nie erfüllbar. Seit dem 2026-10-05 trägt `main`
   ein Ruleset mit genau dem, was ein Konto halten kann; die Regel fordert jetzt
   genau das und behauptet es gegen das echte Ruleset. Die zweite Zustimmung
   kehrt zurück, sobald eine zweite Identität existiert — der Upgrade-Pfad aus
   ADR 0008. Entschieden vom Maintainer am 2026-10-05 (Änderung
   `rb-m6-one-account`, Bead `coding-harness-bma`).

   MAJOR, weil §4 es so vorschreibt: die Regel fordert anderes als vorher.

   - **Geändert:** RB-M6 — Wortlaut neu, Stufe 2 → 4, Erzwinger um `::test_an_unreachable_api_is_not_a_pass` ergänzt, `Ramp:ruleset-assert` entfällt; Geltung unverändert. Keine ID geändert, keine entfernt
   - **Tests:** neu `tests/test_repo_settings.py`. Das echte Ruleset liest das Gate `ruleset` (`decisions/gates.yaml`, `placement: writer`): GitHub zeigt die Bypass-Liste nur dem, der das Ruleset ändern darf, also misst `make verify` auf der Maschine des Maintainers, nicht die gehostete CI. Das Ventil `ruleset-assert` ist geschlossen, nicht still gestrichen: die Behauptung, auf die es wartete, läuft jetzt
   - **Agents/Hooks/Templates:** nichts. `docs/WORKFLOW.md` sagt, dass `tests/test_repo_settings.py` jetzt existiert, sein Container-Zaun noch nicht
   - **lakeswitch-ai:** nichts — das Ruleset dort („lakeswitch floor", gelesen am 2026-10-05) fordert bereits Pull Request, `verify`, kein Force-Push, kein Löschen und keinen Bypass
   ```

6. **`docs/WORKFLOW.md`** (3 min): `updated: <DAY>`; after the sentence
   ending "it describes the target, not this tree." in the note "Not all of
   it is here yet", append inside the same quote paragraph:
   "Since <DAY>, `tests/test_repo_settings.py` exists: it asserts the branch
   ruleset (rule RB-M6); the container fence §3 describes is not in it yet."

7. **Artefacts** (2 min): `implementation_status: partial` in this folder's
   five files, then `python3 scripts/plans_registry.py --index`.

## Verification

```bash
python3 -m pytest tests/test_repo_settings.py tests/test_regelwerk.py tests/test_ramp_valves.py tests/test_ci.py tests/test_kit.py tests/test_gate_machinery.py -q
RULESET_ASSERT=1 python3 -m pytest tests/test_repo_settings.py -q -rs
python3 scripts/ramp_valves.py --format=json | grep ruleset-assert   # expect no output
python3 scripts/ci_gates.py --check-ci && git diff --exit-code .github/workflows/ci.yml
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
```

| Criterion | Held by | Goes red when |
|---|---|---|
| 1 | phase 6 reading of the row | a present requirement for code-owner or last-pusher approval stays, or a part is missing |
| 2 | `test_regelwerk.py::test_rules_at_level_three_or_higher_name_an_existing_enforcer[RB-M6]`, `::test_every_named_ramp_exists_and_no_valve_is_orphaned` | an enforcer name is wrong, or a `Ramp:` stays without its valve |
| 3 | `test_regelwerk.py::test_version_is_semver_and_history_is_monotone`, `::test_sync_impact_entry_exists_for_the_current_version`; gate `frontmatter-current`; `git diff` in phase 6 | version and entry disagree, a line is missing, `updated:` is old, another row moved |
| 4 | `test_todays_ruleset_holds`, `test_a_stricter_ruleset_still_holds` | the check misreads today's answer, or demands an exact match |
| 5 | the four `goes_red` tests | a requirement is not checked |
| 6 | `test_a_hidden_bypass_list_is_not_a_pass`, `test_an_unreachable_api_is_not_a_pass` | a missing key or a failed call reads as "holds" |
| 7 | `test_master_has_a_ruleset_with_required_checks` in the gate; `test_the_measurement_holds_on_todays_answers` | a wrong API path, or the live ruleset weakened |
| 8 | `test_the_ruleset_gate_turns_the_live_check_on`; gate `ci-drift`; `git diff --exit-code` | the variable or placement drifts, or `ci.yml` changes |
| 9 | the `grep` above; `test_regelwerk.py` (orphan check) | the valve stays, or stays only on one side |
| 10 | `test_ci.py::test_every_gate_step_has_a_mutation_test`, `::test_the_mutation_exemption_list_only_shrinks`; gates `leerprobe`, `ramp-valves` | no mutation evidence, the kit role missing, another valve made due |
| 11 | gate `frontmatter-current`; phase 6 reading | the note still implies absence, or the dated list is edited |
| 12 | `make verify` | any block gate red |

## Not touched

- **GitHub:** the ruleset, settings, labels, secrets — read only.
- **`.github/workflows/ci.yml`** and **`scripts/ci_gates.py`:** a `writer`
  gate needs no generator change, and the file must stay byte-identical.
- **The rule set beyond RB-M6:** RB-M2, the other rows, every older history
  entry, `last_reviewed:`, `review:`.
- **The valve `merge-freshness`** and every other valve; `OHNE_*`,
  `REIST_NICHT` and its cap.
- **`docs/governance/quality-gates.md`, `docs/architecture/target-architecture.md`,
  `docs/adr/`.**

## Phase 7

A decision pull request from `decide/rb-m6-one-account`, two decisions that
stand together (the gate `adr-answers` needs the answer for this feature):
title `decide(governance): RB-M6 asks for what one account can hold`, label
`decision`, body in the multi-decision form of `prompts/07-commit.md` — (1)
RB-M6 amended, rule set 4.0.0; (2) no ADR for this change. "What could
break": `make verify` red offline or without a `gh` login. "After the merge":
nothing to run; the valve `merge-freshness` still falls due on 2026-10-31.

## Phase 4 record

Written by the phase-4 session, 2026-10-05. Branch `decide/rb-m6-one-account`,
started at `979c8bd`. Commits: `ba7d17f` (guard test), `5a94114` (live test,
gate, kit role), `e3e5f4c` (rule set 4.0.0, valve, workflow note), `8570917`
and `a880547` (holes the planted faults found). Not recorded and not done on
purpose: step 0, the ADR answer — it is the maintainer's to state (house
rule 8), so `make verify` stays red on the gate `adr-answers` only.

### Time used

2026-10-05 23:27:56–23:44:02, 16 min 6 s (appetite 2 h); no break, no appetite stop reached.

### Verify

`make verify` at `22657eb` (2026-10-05, network and the maintainer's `gh`
login present): `pytest` 638 passed, 16 skipped (600 and 15 at `979c8bd`);
gate `ruleset` green; every other block gate green except `adr-answers`, which
is red on exactly the missing ADR answer for `rb-m6-one-account` (the same
single red as at `979c8bd`). `markdownlint` and `docs-links` are report-only
and red as before. The plan's other commands: `ramp_valves.py --format=json |
grep ruleset-assert` prints nothing, 26 valves open and none due (27 before);
`ci_gates.py --check-ci` green and `.github/workflows/ci.yml` identical to
`979c8bd`. The rule set differs from `979c8bd` only in the RB-M6 row, the two
header keys and the 4.0.0 entry. The only edit after that run is this section
and the time line.

### Deviations

Each in the four labels of `prompts/04-implement.md`; D1 is the one that
changes a file the plan did not name, and it stands in its own commit
(`ba7d17f`) so it can be reverted alone.

- **D1 — the step-count guard did not know a `writer` gate.**
  - expected: "a `writer` gate needs no generator change" (Not touched), and
    `tests/test_ci.py` green after step 2.
  - found: `tests/test_ci.py::test_every_gate_step_runs_even_after_a_failing_gate`
    counts every gate of `decisions/gates.yaml` against the steps of `ci.yml`
    (18 of 19) — no gate had used `writer` before, so the test never met one.
  - relevant: the floor gate `pytest` goes red in CI and locally the moment the
    gate `ruleset` exists; without a fix the change cannot be green.
  - proposal (applied): count only `ci_gates.misst_in(g, "ci")` gates, the one
    place that rule lives; a hosted gate dropping out of `ci.yml` is still red
    (planted fault F28). `[DETAIL]`, mechanical, one line plus a docstring note.
- **D2 — `gh_api` has a 60 s limit.** The plan's `gh_api` has none; a `gh` that
  hangs on a dropped network would hang `make verify`. A timeout is
  `(124, "gh did not answer within 60 s")`, red as `not measured`.
- **D3 — tests beyond the plan's list**, each added because a planted fault
  stayed green without it (F03, F06, F11, F12, F13 below):
  `test_the_measurement_asks_for_the_branch_the_repository_names`,
  `test_a_missing_gh_says_so`,
  `test_the_live_check_goes_red_without_gh_when_the_gate_turns_it_on`,
  `test_the_live_check_calls_nothing_without_the_variable`,
  `test_the_ruleset_gate_check_goes_red_when_the_gate_drifts` (with the helper
  `_gate_findings`), and more cases in `test_an_unreachable_api_is_not_a_pass`
  (no answer, a failed call that still prints a valid answer, and the cause
  each case plants).
- **D4 — `..._when_a_rule_is_removed` is parametrized over a literal list of
  the four types,** not over `RULE_TYPES`: a requirement that fell out of the
  table fell out of the test with it (F03 was green).
- **D5 — step 7 says "five files"; the folder has four** (`decisions.md`,
  `research.md`, `spec.md`, `plan.md`). All four carry
  `implementation_status: partial`.
- **D6 — the live test's failure message says what to do.** When any finding
  begins `not measured:`, the assertion message adds: "The gate `ruleset` needs
  network and a `gh` login on this machine; not measured is red, never green
  (RB-M6)." An agent that runs `make verify` offline reads the cause and the
  way out in the failure itself. The plan's `assert not findings, "\n".join(findings)`
  is otherwise kept.
- **The plan's behaviour does not block this verify** (network and a `gh` login
  are here); offline it is red on the one gate `ruleset`, see "Gate offline".

### Gate offline

Measured with a `gh` shim that exits 1 with a DNS error (`make verify`,
2026-10-05, before D6): the gate `ruleset` red (block), every other gate as
without the shim (`adr-answers` red, `markdownlint` and `docs-links` report
only, the rest green). The failure line reads `not measured:
repos/{owner}/{repo}: exit 1: error connecting to api.github.com: dial tcp:
lookup api.github.com: no such host`; after D6 the hint line follows it.
Nothing is skipped quietly offline; the cost is the plan's own: `make verify`
needs network and a `gh` login on the writer machine.

### Planted faults

Each fault was planted in the committed tree, the named test selection run,
the file restored with `git checkout`. All red unless marked. File level
(runner script in the session's scratchpad, not committed):

| # | Fault planted | Result |
|---|---|---|
| F01 | a missing `bypass_actors` key read as "no bypass" | red: `test_a_hidden_bypass_list_is_not_a_pass` |
| F02 | a non-empty bypass list ignored | red: `..._goes_red_when_a_bypass_is_added` |
| F03 | `RULE_TYPES` loses `deletion` | **green first** (hole), red after D4: `KeyError` |
| F04 | any check counts as `verify` | red: `..._goes_red_when_verify_is_not_required` |
| F05 | missing `gh` swallowed as success | red: `test_an_unreachable_api_is_not_a_pass[no-gh]` |
| F06 | a timeout swallowed as success | **green first** (hole), red after D3 (`[no-answer]` asserts the cause) |
| F07 | shape check of the rules answer removed | red: `[rules-not-a-list]` |
| F08 | supplying rulesets never read | red: `test_the_measurement_holds_on_todays_answers` |
| F09 | branch name not URL-escaped | red: `test_the_measurement_asks_for_the_branch_the_repository_names` |
| F10 | empty rule list not special-cased | red: `..._goes_red_on_an_empty_rule_list` |
| F11 | exit code of a failed call ignored | **green first** (hole), red after D3 (`[rules-exit-1-with-a-valid-answer]`) |
| F12 | live test skipped even with the variable | **green first** (hole), red after D3: `..._goes_red_without_gh_when_the_gate_turns_it_on` |
| F13 | live test not skipped without the variable | **green first** (hole), red after D3: `..._calls_nothing_without_the_variable` |
| F14 | gate sets `RULESET_CHECK=1` | red: `test_the_ruleset_gate_turns_the_live_check_on` |
| F15 | gate without the variable | red: same |
| F16 | gate `placement: both` | red: same, and `test_ci.py` |
| F17 | gate `enforcement: report` | red: same |
| F18 | gate `floor: true` | red: same |
| F19 | gate `ruleset` absent | red: same |
| F20 | valve `ruleset-assert` back in `ramp_valves.py` | red: `test_regelwerk.py` (valve without a rule) |
| F21 | `Ramp:ruleset-assert` left in the RB-M6 row | red: `test_regelwerk.py` (named, not present) |
| F22 | wrong enforcer name in the RB-M6 row | red: `test_regelwerk.py` (enforcer does not exist) |
| F23 | `version: 3.0.0` over the 4.0.0 entry | red: `test_regelwerk.py` (head vs top entry) |
| F24 | 4.0.0 history entry missing | red: `test_regelwerk.py` |
| F25 | rule set `updated:` stale | red: gate `frontmatter-current` |
| F26 | kit role of the new test changed to `bestand` | red: gate `leerprobe` (kit probe, BLOCK) |
| F27 | every mutation-test name renamed away | red: `test_ci.py::test_every_gate_step_has_a_mutation_test` (renaming only `goes_red` stays green by design: the pattern has other names) |
| F28 | D1 reverted (guard counts the writer gate) | red: `test_ci.py::test_every_gate_step_runs_even_after_a_failing_gate` |

End to end, a `gh` shim in the session's scratchpad proxied the real,
read-only API and distorted the answer; nothing at GitHub was written and the
live ruleset was not touched. The live test went red, with the finding named,
for each of: a bypass actor added (E01); the bypass key hidden (E02); the pull
request, force-push, deletion or required-check rule removed (E03–E06); `verify`
replaced by another check (E07); an empty rule list (E08); the rules answer not
a list (E09); `gh` exit 1 (E10); an answer that is not JSON (E11); `gh` not on
`PATH` (E12); a `gh` that never answers, limit set to 1 s (E13). With the
shim passing everything through, the live test passed. Without
`RULESET_ASSERT`, the live test was skipped (reason names the gate `ruleset`)
and `gh` was called zero times; with it, three times (repository, branch
rules, ruleset).

Totals: 28 file-level + 13 end-to-end = 41 faults planted; 41 red. Five of the
file-level ones were green first (F03, F06, F11, F12, F13) and closed by D3 and
D4; one more (F27, single rename) is an equivalent mutant by design.

## Repair round 1

Only row F-1 of `findings.md` (BLOCKER, `[DIVERGENT]`), at the dispatching
session's word of 2026-10-06; F-2 is the maintainer's decision, F-3 to F-7 are
the maintainer's choice, and no ADR answer is recorded. The fix is one commit,
`8524800`, on `decide/rb-m6-one-account`. Not reviewed.

| Row | Commit | What changed |
| --- | --- | --- |
| F-1 | `8524800` | `docs/WORKFLOW.md` and `prompts/05-verify.md` annotate `make verify` as what the CI runs, minus a `placement: writer` gate, which runs there only, and `make gates` as marking such a gate. `scripts/ci_gates.py --list` appends " — laeuft nur lokal (make verify), nicht in der CI" to the command line of a `writer` gate, as it says "laeuft nur in der CI" for a hosted-only one. `tests/test_ci.py::test_the_list_marks_a_writer_gate_as_local_only` holds the marker both ways, on the real list and on a list where a `both` gate moves to `writer` and the real one leaves it. |

Planted faults for the new test, each in the committed tree, the test run,
the file restored with `git checkout`; all red:

| # | Fault planted | Result |
|---|---|---|
| R1-1 | the marker is never printed (`if False:`) | red: `test_the_list_marks_a_writer_gate_as_local_only` |
| R1-2 | the marker is printed on every locally runnable gate (`if True:`) | red: same |
| R1-3 | the marker keyed on `placement == "hosted"` instead of `"writer"` | red: same |
| R1-4 | the marker hard-wired to the gate id `ruleset` | red: same (the synthetic `writer` gate has no mark) |
| R1-5 | the marker text loses its "nicht in der CI" wording | red: same |

## Repair round 2

Rows F-3 to F-7 of `findings.md` (all MINOR), under the maintainer's standing
rule of 2026-10-06: a MINOR row on tests, security or a false statement is
repaired without asking. F-2 is untouched (decided and fixed in `a9f55a8`,
awaiting review). Every row is set to "fixed in <commit>, not reviewed"; the
rule-set text, the live ruleset, `ci.yml` and `gates.yaml` are unchanged, and
nothing was written to GitHub (only `gh api` GETs, through the real `gh` or
the read-only shim of the session's scratchpad).

| Row | Commit | What changed |
| --- | --- | --- |
| F-3 | `8f9b11e` | `tests/test_repo_settings.py`: a `verify` entry counts only when its `integration_id` is 15368 (GitHub Actions). An unpinned or other-app entry is the finding "required check verify is not pinned to GitHub Actions"; one pinned entry still holds beside an unpinned one in another ruleset. |
| F-4 | `fba000d` | `measure` compares `full_name` of the repository answer with the checkout's `origin` (`local_repository`, case-insensitive); a mismatch, a missing name or an unreadable origin is `not measured:` and stops before the rules of another repository are read. |
| F-5 | `8078d0e`, `21251a2` | The tie parses the gate command (leading `NAME=value`, then `python3 -m pytest …`, no chain, redirect or substitution) and starts a pytest with its arguments and variables that reports which tests it would run: the live test must be among them and the run must not be only a collection. `21251a2` names the chain case itself. |
| F-6 | `f010de1`, `bd1904d` | `tests/test_ci.py`: `MAY_BE_WRITER_ONLY` names the gates that may be writer-only (today `ruleset`) with a reason; a floor gate never may be, an unnamed one may not, and an entry whose gate is gone, no longer writer-only or a floor gate must go. |
| F-7 | `d2f27f8` | The hint test reads the `E` lines of the failure (`_assertion_message`), not the whole output. |

### Deviations

- **D7 — the check is stricter than spec term (b).**
  - expected: spec term (b) asks for an entry with `context: verify` only.
  - found: the maintainer's words were "exactly today's ruleset", the amended row promises "der Job, der die Gate-Liste fährt", and an unpinned entry lets a commit status posted with any token satisfy the rule without the job (F-3).
  - relevant: code and spec now differ by the pin; the rule-set row is true as written.
  - proposal (applied for the code; `spec.md` left as it is): the next review decides whether term (b) is amended to name `integration_id`. `[DETAIL]`.
- **D8 — the F-6 tests avoid the names `*_goes_red_*`.** `test_the_mutation_ratchet_only_turns_one_way` counts a mutation-test name in a file that merely mentions a script as evidence for that script; one such name in `tests/test_ci.py` made `plans-registry` look covered and turned that ratchet red (measured, then renamed to `…_flags_…`).
- **D9 — F-4 reads `origin` only.** A repository renamed at GitHub (the API answers with the new name) or a checkout whose `origin` is not the repository `gh` defaults to is red with the cause named; the way out is `git remote set-url origin …`. A fork whose `gh` default is its upstream is red on purpose.
- **D10 — F-5 costs about two seconds of suite time:** one pytest start per distinct gate command in the tests (cached within a run).

### Planted faults

Each fault was planted in the committed tree, the named test selection run
(first failing test shown), the file restored with `git checkout`.

| # | Fault planted | Result |
|---|---|---|
| R2-1 | the pin ignored (`and True`) | red: `…verify_is_not_pinned_to_github_actions[no-integration-id]` |
| R2-2 | any non-null `integration_id` counts | red: `…[another-app]` |
| R2-3 | the app id is 15369 | red: `test_todays_ruleset_holds` |
| R2-4 | the unpinned finding never built (`if False and any(`) | red: `…[no-integration-id]` |
| R2-5 | an unpinned `verify` reports nothing | red: `…goes_red_when_a_rule_is_removed[required_status_checks]` |
| R2-6 | the repository comparison switched off | red: `…goes_red_when_it_measured_another_repository` |
| R2-7 | the comparison is case-sensitive | red: `…does_not_mind_the_case_of_the_repository_name` |
| R2-8 | an unknown local repository passes | red: `…cannot_name_its_repository_is_not_measured` |
| R2-9 | owner read from the wrong URL segment | red: `…names_its_repository_by_its_origin[https-git]` |
| R2-10 | `.git` kept in the name | red: same |
| R2-11 | `RULESET_ASSERT=1` no longer required | red: `…gate_check_goes_red_when_the_gate_drifts[variable]` |
| R2-12 | "does the live test run" not asked | red: `…[k-suffix]` |
| R2-13 | a collect-only run counts as running | red: `…[collect-only]` |
| R2-14 | chain, redirect and substitution allowed | **green first** (the probe pytest read `\|\|` as a file and failed for the wrong reason), red after `21251a2`: `…goes_red_when_it_chains_or_redirects[\|\| true]` |
| R2-15 | the command's own variables not handed to the probe | red: `…[addopts-in-front]` |
| R2-16 | the tie hard-wired to "starts like the gate" again | red: `…[k-suffix]` |
| R2-17 | `python3 -m pytest` not required | red: `…[another-interpreter]` |
| R2-18 | floor gate `pytest` set to `placement: writer` in `decisions/gates.yaml`, `ci.yml` regenerated | red: `test_only_the_named_gates_are_writer_only` alone; `test_ci.py`, `test_gate_machinery.py`, `--check-schema` and `--check-ci` green |
| R2-19 | non-floor `ruff-format` set to `writer` the same way | red: same single test |
| R2-20 | an unnamed writer-only gate allowed | **green first** (the case used the floor gate `ruff-check`), red after `bd1904d` (case now `ruff-format`) |
| R2-21 | the floor check removed | **green first** (a floor gate was still flagged as "unnamed"), red after `bd1904d` (the case asserts the message) |
| R2-22 | an entry for a gate that left `writer` not flagged | red: `…flags_a_gate_that_moves[named-gate-comes-back]` |
| R2-23 | the named gate misspelt in the list | red: `test_only_the_named_gates_are_writer_only` |
| R2-24 | the hint never appended (the reviewer's plant, `if False and any(`) | red: `…goes_red_without_gh_when_the_gate_turns_it_on` |
| R2-25 | the hint text changed | red: same |
| R2-26 | the test reads the whole output again | green — the old test with the hint present; equivalent by design (R2-24 is the fault it must catch) |

End to end, read-only: `GH_REPO=MPAdesso/lakeswitch-ai` with
`RULESET_ASSERT=1` makes the live test red ("it answers for
'MPAdesso/lakeswitch-ai', but this checkout is of 'MPAdesso/coding-harness'")
where it was green before (E2-1); a `gh` shim that passes `gh api <path>` to
the real `gh` and removes `integration_id` from the rules answer makes it red
("not pinned to GitHub Actions"), and passes without the distortion (E2-2);
the gate command with a ` -k "not master"` suffix makes
`test_the_ruleset_gate_turns_the_live_check_on` red and nothing else (E2-3).
Totals: 26 file-level faults, 3 end to end; 28 red, one equivalent (R2-26), and
three that were green first (R2-14, R2-20, R2-21) and are closed.

## Time used

Phase 4 and its repair rounds before this one: see "Time used" in the Phase 4
record above.

Repair round 1 (F-1 only; appetite 20 min, set by the dispatching session;
read from `date`):

- 2026-10-06 01:08–01:11, no break, appetite not reached; two `make verify` runs, the first red on `adr-answers` and `frontmatter-current` (`docs/WORKFLOW.md` stamped after it)

Repair round 2 (F-3 to F-7; appetite 45 min, set by the dispatching session;
read from `date` at the start, between steps and before each commit):

- 2026-10-06 14:57:55–15:15:26, no break, appetite not reached; seven `make verify` runs, all green (one per step, two on the records); the gate `ruleset` read the real ruleset (green) in each
