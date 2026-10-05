---
title: "Plan — rb-m6-one-account"
status: draft
implementation_status: none
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
