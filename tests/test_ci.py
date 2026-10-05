"""Tests about the CI itself — the gates that guard the gates.

Two failure shapes are meant to snag here, both measured:

1. **A gate whose trigger is narrower than its input is green because it never
   ran.** Until 2026-08-31, `.claude/**` and `.github/**` triggered not a single
   gate in this repo — a pull request that changed only a hook was merged
   unchecked.

2. **A copied gate list is the drift it was written against.**
   `verify_all.sh` must hold no commands of its own; it asks `ci_gates.py`,
   and that reads `ci.yml`.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CI_FILE = REPO_ROOT / ".github" / "workflows" / "ci.yml"
RUNNER = REPO_ROOT / "scripts" / "verify_all.sh"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from ci_gates import gates, misst_in  # noqa: E402


def _einschraenkungen() -> dict[str, list[str]]:
    """Which path restrictions the triggers carry — per trigger, empty if none.

    Until 2026-09-08 there was an allowlist here (`paths:`), and this file
    checked whether it covers everything the gates read. It did not: nine
    tracked files triggered no run, among them `model-endpoints.yaml`, which
    RB-A6 rests on. The derivation could not see that, because it drew
    directories from string literals in the gate scripts — a root file does not
    appear in them.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    # `on` is parsed by PyYAML as the boolean True (YAML 1.1) — allow both forms.
    trigger = doc.get("on") or doc.get(True)
    gefunden: dict[str, list[str]] = {}
    for name in ("push", "pull_request"):
        block = trigger.get(name) or {}
        if not isinstance(block, dict):
            continue
        for schluessel in ("paths", "paths-ignore"):
            werte = block.get(schluessel) or []
            if werte:
                gefunden[f"{name}.{schluessel}"] = list(werte)
    return gefunden


# --------------------------------------------------------------------------
# 1 · The trigger covers what the gates read
# --------------------------------------------------------------------------


def test_ci_exists_and_has_gates() -> None:
    assert CI_FILE.is_file(), "There is no CI definition."
    assert len(gates()) >= 10, "The verification list is suspiciously short."


def test_the_trigger_does_not_restrict_paths() -> None:
    """Every change to a tracked file runs the gates.

    An allowlist ages with every new file — `model-endpoints.yaml` was added in
    a later PR, and nobody updated the filter. An exception list would be empty:
    `scripts/kit/probe.py` classifies EVERY tracked file via `git ls-files`, and
    `.gitignore` even changes which files it sees. There is no file whose change
    can touch no gate.
    """
    gefunden = _einschraenkungen()
    assert not gefunden, (
        "The CI trigger restricts paths: "
        + "; ".join(f"{k} = {v}" for k, v in sorted(gefunden.items()))
        + ". A file that triggers no run is merged unchecked — and the next "
        "uninvolved PR goes red for it."
    )


def _oberste_verzeichnisse() -> set[str]:
    """The tracked top-level directories.

    From `git ls-files`, not from `iterdir()`: a local `.venv/` or `htmlcov/`
    would otherwise have changed the set and made the test differ between CI
    and a developer machine.
    """
    ergebnis = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    return {p.split("/", 1)[0] for p in ergebnis.stdout.splitlines() if "/" in p}


def _verzeichnisse_aus_quelltext(quelltext: str, oberste: set[str]) -> set[str]:
    """Which directories does this source text name as a path?

    Two spellings, and the second is the reason this function exists at all:

    1. as a literal with a slash — `"docs/journal/"`
    2. **segment by segment** — `REPO_ROOT / ".beads" / "issues.jsonl"`

    The first version of this check knew only (1). But the real read path of the
    `dangling-beads` gate is in form (2), and `.beads` came out only because it
    also happens to be in `SKIP_PREFIXES` — the list of directories the gate
    explicitly does **not** read. The check was green, and it was green on the
    token with the opposite meaning.

    Over-detection is harmless here and intended: a hit that is not a path makes
    the set larger and the test therefore stricter. Under-detection is the
    failure this is written against.
    """
    gefunden: set[str] = set()
    for zitat in re.findall(r"""["']([^"'\n]{1,200})["']""", quelltext):
        kopf = zitat.split("/", 1)[0]
        if kopf in oberste and (kopf == zitat or zitat.startswith(kopf + "/")):
            gefunden.add(kopf)
    return gefunden


def _verzeichnisse_die_die_gates_lesen() -> dict[str, set[str]]:
    """Derives from the gate commands which directories are read.

    The parametrisation above is a hand list: it checks that a known directory
    is in the filter, but not that the list is complete. A hand list is only as
    good as its last maintainer — and `.beads/` was missing from it, although
    `check_dangling_bead_ids.py` reads from it. Since bead 1jg.3 no reader opens
    `.beads/` itself any more — the ONE access point does. So the derivation
    follows the import: a gate script that loads `bead_render` reads what the
    access point reads.
    """
    oberste = _oberste_verzeichnisse()
    zugriffspunkt = REPO_ROOT / "scripts" / "bead_render.py"
    gelesen: dict[str, set[str]] = {}
    for gate in gates():
        for treffer in re.finditer(r"([A-Za-z0-9_./-]+\.py)\b", gate.get("command") or ""):
            rel = treffer.group(1)
            quelle = REPO_ROOT / rel
            if not quelle.is_file():
                continue
            quellen = [quelle.read_text(encoding="utf-8")]
            if "bead_render" in quellen[0] and zugriffspunkt.is_file():
                quellen.append(zugriffspunkt.read_text(encoding="utf-8"))
            for text in quellen:
                for verzeichnis in _verzeichnisse_aus_quelltext(text, oberste):
                    gelesen.setdefault(verzeichnis, set()).add(rel)
    return gelesen


def _deckt(muster: list[str], verzeichnis: str) -> bool:
    """Segment by segment, not as a string prefix.

    `scripts/**` does not cover `script/`, even though `startswith` claims it does.
    """
    return any(p == verzeichnis or p.startswith(verzeichnis + "/") for p in muster)


def test_no_directory_a_gate_reads_is_excluded() -> None:
    """No gate reads from a directory that an exception excludes.

    As long as `_einschraenkungen()` is empty, this is trivially true — the test
    stays anyway: it is the ratchet for the day someone adds an exception. The
    derivation below deliberately over-detects.
    """
    ausnahmen = [p for werte in _einschraenkungen().values() for p in werte]
    if not ausnahmen:
        gelesen = _verzeichnisse_die_die_gates_lesen()
        assert gelesen, "the derivation finds not a single directory that is read (RB-G7)"
        return
    getroffen = {
        verzeichnis: sorted(skripte)
        for verzeichnis, skripte in _verzeichnisse_die_die_gates_lesen().items()
        if _deckt(ausnahmen, verzeichnis)
    }
    assert not getroffen, "Exceptions exclude directories that gates read: " + "; ".join(
        f"{d}/ (read by {', '.join(s)})" for d, s in sorted(getroffen.items())
    )


def test_die_ableitung_sieht_die_segmentweise_schreibweise() -> None:
    """Control test on the form the first version failed on.

    `REPO_ROOT / ".beads" / "issues.jsonl"` — no slash in the literal. That is
    exactly how the read path stands in `check_dangling_bead_ids.py`.
    """
    quelle = 'EXPORT = REPO_ROOT / ".beads" / "issues.jsonl"'
    assert _verzeichnisse_aus_quelltext(quelle, {".beads", "docs"}) == {".beads"}


def test_die_ableitung_sieht_die_literale_schreibweise() -> None:
    """And the other form, so that the extension does not lose the first."""
    quelle = 'SKIP = ("docs/lessons/_rohbefunde/",)\nP = "scripts/x.py"'
    assert _verzeichnisse_aus_quelltext(quelle, {"docs", "scripts"}) == {"docs", "scripts"}


def test_die_ableitung_erfindet_nichts() -> None:
    """A source text without paths yields the empty set.

    Without this check, the detection could report everything quoted, and the
    test built on it would be mere noise.
    """
    assert _verzeichnisse_aus_quelltext('x = "hallo"\ny = "ein Satz mit Leerzeichen"', {"docs"}) == set()


def test_der_echte_lesepfad_des_bead_gates_wird_erkannt() -> None:
    """Not via SKIP_PREFIXES, but via the line that actually reads.

    The old test was green because `.beads/` happened to be in the list of
    excluded prefixes as well. Since bead 1jg.3 (step two), no gate opens the
    copy any more: the state travels as a render — BEAD_RENDER in CI, a temp
    render locally. What remains is exactly one place with the path literal, the
    synthetic-repo seam of the plans-registry gate (monkeypatch contract); the
    ratchet says: there must never be more than this one.
    """
    gelesen = _verzeichnisse_die_die_gates_lesen()
    assert gelesen.get(".beads") == {"scripts/plans_registry.py"}, (
        "more than the known test seam depends on the copy — a second path "
        "opens .beads/ beside the synthetic-repo shim of the plans-registry gate: "
        f"{gelesen.get('.beads')}"
    )


def test_die_ableitung_findet_ueberhaupt_etwas() -> None:
    """If it found nothing, the test above would be empty and therefore always green.

    Since bead 1jg.3 (step two), `.beads` is deliberately NOT part of it any
    more — the test above sets the ratchet against that.
    """
    gelesen = _verzeichnisse_die_die_gates_lesen()
    assert len(gelesen) >= 5, f"Only {len(gelesen)} directories derived: {sorted(gelesen)}"
    assert "docs" in gelesen


def test_every_gate_has_a_name_and_an_id() -> None:
    """The name is for humans, the id is the key of the local runner."""
    ohne_id = [g["name"] for g in gates() if not g["id"]]
    assert not ohne_id, f"Gates without an id: {ohne_id}"


def test_every_step_after_a_failing_gate_still_runs() -> None:
    """A step behind a valve needs `if:`, otherwise it drops out silently.

    `ramp_valves.py` deliberately returns `exit 1` as soon as a transition valve
    is due — that is its function, not a fault. GitHub Actions then skips every
    following step of the same job that carries no `if:`. A timer job whose
    checks fall silent from some date on keeps reporting green: not over a clean
    tree, but over a set from which the checks have disappeared.

    That is exactly what W-11 was: `provenance-history` stood without `if:`
    behind `ramp-valves` and would never have run again from 2026-10-31. The
    finding was visible a year ahead and still no test noticed it — because
    there was none that reads the order.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    verletzt: list[str] = []
    ventile = 0
    for job_name, job in (doc.get("jobs") or {}).items():
        gesehen = False
        for schritt in job.get("steps") or []:
            if gesehen and "if" not in schritt:
                verletzt.append(f"{job_name}.{schritt.get('id') or schritt.get('name')}")
            # `ramp_valves.py` is the one step that turns red on schedule.
            # Recognised by its command, not by its id: an id is renamed before
            # anyone reads this test.
            if "ramp_valves.py" in str(schritt.get("run", "")):
                gesehen = True
                ventile += 1
    # Without this line the test is silently green as soon as `ramp_valves.py`
    # occurs in no job any more — renamed, moved, pulled into another script. It
    # would then run over the empty set and report a pass, which is exactly the
    # class of failure it is written against.
    assert ventile, (
        "No step runs ramp_valves.py — this test ran over the empty set. Either "
        "the script was renamed, then the test follows it; or the valve is gone, "
        "then this test belongs deleted."
    )
    assert not verletzt, (
        f"Steps behind the valve without `if:` — they drop out as soon as a transition valve falls due: {verletzt}"
    )


def test_a_gate_that_needs_the_tracker_gets_a_hydration_step() -> None:
    """4t8, 1jg.3: tracker-reading gates measure in CI against ONE render.

    The hydration step (pinned bd, checksum-verified, refs/dolt/data) sits
    before the first gate that needs it, renders once and sets BEAD_RENDER — all
    readers of the run take the same state (D-52, condition 2). And only in jobs
    that have such a gate — since 1jg.3 the drift job too, because
    plans-registry-strict reads the tracker. A job without a tracker reader does
    not get the step: there it would be decoration.
    """
    import ci_gates

    ci = ci_gates.generate_ci()
    assert "tools/beads/install.sh" in ci, "the checksum-verified bd installation is missing"
    assert "refs/dolt/data" in ci, "the tracker transport is missing in the derivation"
    assert "git config --local --unset-all http.https://github.com/.extraheader" in ci, (
        "the checkout header sits locally and globally — git sends it twice, and "
        "bd bootstrap silently falls back instead of reading refs/dolt/data"
    )
    assert 'echo "BEAD_RENDER=$PWD/.beads/issues.jsonl" >> "$GITHUB_ENV"' in ci, (
        "the hydration does not render once up front — a render of its own per "
        "reader would be exactly the double measurement that D-52 stands against"
    )
    assert ci.index("id: setup-tracker") < ci.index("id: bead-export"), (
        "the hydration must come BEFORE the first tracker-reading gate"
    )

    drift_teil = ci[ci.index("\n  drift:") :]
    assert "setup-tracker" in drift_teil, (
        "plans-registry-strict reads the tracker — without a committed copy (bead 1jg.3) "
        "the drift job measures only with a hydration of its own"
    )
    assert drift_teil.index("id: setup-tracker") < drift_teil.index("id: plans-registry-strict")


def test_a_gate_that_needs_history_gets_a_full_checkout_only_in_its_job(monkeypatch: pytest.MonkeyPatch) -> None:
    """qd7: a hosted checkout holds one commit, so a gate that asks when a file last changed needs all of them.

    `frontmatter-current` declares `needs_history`: the derived `verify` job checks out with
    `fetch-depth: 0`, and the `drift` job, which has no such gate, does not. Without the flag
    no job may carry it, or the full clone would be a default and not a declaration.
    """
    import ci_gates

    ci = ci_gates.generate_ci()
    verify_teil, drift_teil = ci.split("\n  drift:", 1)
    assert "fetch-depth: 0" in verify_teil, "the verify job runs frontmatter-current on one commit of history"
    assert "fetch-depth: 0" not in drift_teil, "a job without such a gate must not pay for the full history"
    assert "        with:\n          fetch-depth: 0" in verify_teil.split("id: setup-deps")[0], (
        "the flag belongs to the checkout step"
    )

    alle = ci_gates.gates()
    monkeypatch.setattr(ci_gates, "gates", lambda: [{**g, "needs_history": False} for g in alle])
    assert "fetch-depth" not in ci_gates.generate_ci(), "with no gate asking, no job gets the full history"

    monkeypatch.setattr(ci_gates, "gates", lambda: [{**g, "needs_history": g["job"] == "drift"} for g in alle])
    verify_teil, drift_teil = ci_gates.generate_ci().split("\n  drift:", 1)
    assert "fetch-depth: 0" in drift_teil and "fetch-depth" not in verify_teil, "the flag follows its gate's job"


def test_the_schema_rejects_a_non_boolean_needs_history() -> None:
    """qd7: `needs_history: "yes"` is a schema error, and a boolean is not."""
    import ci_gates

    doc = yaml.safe_load(ci_gates.GATE_FILE.read_text(encoding="utf-8"))
    assert ci_gates.validate_schema(doc) == []
    ziel = next(g for g in doc["gates"] if g["id"] == "frontmatter-current")
    assert ziel["needs_history"] is True

    ziel["needs_history"] = "yes"
    fehler = ci_gates.validate_schema(doc)
    assert any("frontmatter-current" in f and "needs_history" in f for f in fehler), fehler


def test_every_gate_step_runs_even_after_a_failing_gate() -> None:
    """bl2: a red gate does not silently switch off the later gates.

    The test above guards the one valve that is red on schedule
    (`ramp_valves.py`). The same dropout shape holds for EVERY gate stage:
    without `if: ${{ !cancelled() }}`, GitHub Actions skips all following steps
    as soon as a blocking gate is red — CI still fails, but over a set from
    which the later gates have disappeared, and it contradicts the local run.
    Two latent bugs (the lychee report against the strict kit probe;
    export-identity with a wrapper without a binary) had stayed hidden in
    exactly this way until the suite turned greener.

    checkout and setup-deps deliberately do not carry the `if`: without them no
    gate has a subject.

    A gate with `placement: writer` is left out of the workflow by declaration
    (`misst_in`), so it is not counted here; the count is of the gates the
    hosted run measures (rb-m6-one-account: the gate `ruleset`).
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    gate_ids = {g["id"] for g in gates() if misst_in(g, "ci")}
    fehlen: list[str] = []
    geprueft = 0
    for job_name, job in (doc.get("jobs") or {}).items():
        im_job = [s for s in job.get("steps") or [] if s.get("id") in gate_ids]
        assert im_job, f"{job_name}: no gate step — this test ran over the empty set."
        for schritt in im_job:
            geprueft += 1
            if schritt.get("if") != "${{ !cancelled() }}":
                fehlen.append(f"{job_name}.{schritt.get('id')}")
    assert geprueft == len(gate_ids), (
        f"{geprueft} of {len(gate_ids)} gates appear as steps — the test would have skipped some silently."
    )
    assert not fehlen, (
        "Gate steps without `if: ${{ !cancelled() }}` — as soon as an earlier "
        f"gate is red, they drop out silently and CI says less than the local run: {fehlen}"
    )


def test_every_step_with_an_id_also_carries_a_name() -> None:
    """W-7: the name half that `test_every_gate_has_a_name_and_an_id` cannot check.

    That test reads `gates()`, and `ci_gates.py:152` discards every step without
    `name` there before the list comes back — deliberately, since nameless steps
    are infrastructure. Exactly for that reason it *cannot* see the half it
    carries in its name: a gate step that someone creates without a name
    disappears silently from `ci_gates.py --list`, from the local runner and from
    every count, and no test goes red.

    So this test reads `ci.yml` directly. The criterion is the `id`: one assigns
    it in order to reference a step — whoever does that means a gate and not
    infrastructure.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    ohne_name = []
    mit_id = 0
    for job_name, job in (doc.get("jobs") or {}).items():
        for schritt in job.get("steps") or []:
            if not schritt.get("id"):
                continue
            mit_id += 1
            if not schritt.get("name"):
                ohne_name.append(f"{job_name}.{schritt['id']}")
    assert mit_id, "No step carries an id — this test ran over the empty set."
    assert not ohne_name, (
        f"Steps with an id but without a name — they drop out of ci_gates.py --list and the local runner: {ohne_name}"
    )


def test_the_makefile_runs_what_the_one_list_runs() -> None:
    """W-6: nothing pinned the Makefile, although it duplicates gate commands verbatim.

    `make test` and `make staleness` repeat what stands in `ci.yml` as a gate.
    If the step there changes its flags, the two drift apart silently — and
    being green locally while CI is red is exactly the state `verify_all.sh`
    argues against by holding no list of its own.

    What is compared is the **whole recipe line**, not a substring. The first
    version of this test asked `command in makefile` and stayed green when the
    control test appended `--tb=short` — an appended flag leaves the substring
    standing and is exactly the drift that is meant to be noticed here.
    """
    zeilen = {
        z.strip() for z in (REPO_ROOT / "Makefile").read_text(encoding="utf-8").splitlines() if z.startswith("\t")
    }
    aus_ci = {g["command"] for g in gates() if g.get("command")}
    verdoppelt = {
        "python3 -m pytest tests/ -q": "make test",
        "python3 scripts/plans_registry.py --check": "make staleness",
    }
    fehlt = []
    for befehl, target in verdoppelt.items():
        if befehl not in zeilen:
            fehlt.append(f"{target}: no recipe line reads exactly '{befehl}'")
        elif befehl not in aus_ci:
            fehlt.append(f"{target}: '{befehl}' is no longer in the one list (ci.yml)")
    assert not fehlt, "Makefile and the one list have drifted apart:\n  " + "\n  ".join(fehlt)


def test_concurrency_group_carries_the_event() -> None:
    """Otherwise a late run kills the one that executes the suite.

    What remains is a run reported green with the suite never run.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    gruppe = doc["concurrency"]["group"]
    assert "event_name" in gruppe, f"Concurrency group without an event: {gruppe}"


# --------------------------------------------------------------------------
# 2 · The local runner holds no list of its own
# --------------------------------------------------------------------------


def test_runner_holds_no_command_list_of_its_own() -> None:
    """`verify_all.sh` must not know the check commands itself.

    This is pinned negatively: the script must contain no call of the checked
    scripts — with exactly one exception, the call of `ci_gates.py`, through
    which it obtains the list.
    """
    text = RUNNER.read_text(encoding="utf-8")
    aufrufe = set(re.findall(r"scripts/([a-z_]+\.py)", text))
    assert aufrufe <= {"ci_gates.py"}, (
        f"verify_all.sh calls scripts directly: {sorted(aufrufe - {'ci_gates.py'})}. "
        "That way it holds a second list — exactly the drift it is written against."
    )


def test_runner_reports_what_it_cannot_run() -> None:
    """Omitting would be invisible; declaring is the difference.

    A list that conceals what it does not cover reads like completeness.
    """
    nicht_lokal = [g for g in gates() if not g["local_runnable"]]
    assert nicht_lokal, "Expected: at least one marketplace action in CI."

    ergebnis = subprocess.run(["bash", str(RUNNER), "--list"], cwd=REPO_ROOT, capture_output=True, text=True)
    assert ergebnis.returncode == 0, ergebnis.stderr
    for g in nicht_lokal:
        assert g["id"] in ergebnis.stdout, f"The runner conceals the gate '{g['id']}', which it cannot run."


def test_no_second_verification_workflow() -> None:
    """There is exactly one verification list.

    A second workflow with check steps would be a competing list. A pure deploy
    path is not one — it checks nothing.
    """
    workflows = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))
    mit_pruefschritten = []
    for wf in workflows:
        if wf.name == "ci.yml":
            continue
        doc = yaml.safe_load(wf.read_text(encoding="utf-8")) or {}
        for job in (doc.get("jobs") or {}).values():
            for step in job.get("steps", []):
                cmd = step.get("run", "")
                if "scripts/" in cmd or "pytest" in cmd:
                    mit_pruefschritten.append(f"{wf.name}: {cmd.strip()[:60]}")
    assert not mit_pruefschritten, "Check steps found outside ci.yml — a second list:\n  " + "\n  ".join(
        mit_pruefschritten
    )


# --------------------------------------------------------------------------
# 3 · The exclusion of the vendoring surface also holds on a direct call
# --------------------------------------------------------------------------


@pytest.mark.skip(
    reason="2ee-triage 2026-09-19: instance test — it requires "
    "docs/patterns/contract_models.py (vendored file of the migration "
    "mechanism), which this checkout does not carry. Valve: decision in "
    "coding-harness-2ee, at the latest before M1."
)
def test_formatter_exclusion_survives_an_explicit_path() -> None:
    """`exclude` alone filters only the file search, not the argument.

    Whoever types `ruff format docs/patterns/contract_models.py` formats the
    vendored file despite the exclusion — that is how it was reformatted here
    once already. The exclusion was there, it just did not apply on the path a
    human takes.

    So what is checked is behaviour, not the configuration string: the
    formatter is given the excluded file explicitly and must still not touch it.
    """
    ziel = REPO_ROOT / "docs" / "patterns" / "contract_models.py"
    assert ziel.is_file(), "Precondition: the vendored file exists."

    ergebnis = subprocess.run(
        ["ruff", "format", "--check", str(ziel)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert ergebnis.returncode == 0 and "Would reformat" not in ergebnis.stdout, (
        "The formatter sees the excluded file because it was named explicitly. "
        "`force-exclude = true` is missing in ruff.toml."
    )


def test_a_local_equivalent_derives_its_arguments_from_the_action() -> None:
    """The substitute command must not repeat the action's arguments.

    Otherwise there would be two lists of globs — the same drift this whole
    module is built against, only one level deeper. So what is checked is that
    every glob from the action configuration is also in the derived command: if
    someone changes the globs in `ci.yml`, the local run moves with them.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    schritte = {s.get("id"): s for s in doc["jobs"]["verify"]["steps"] if s.get("id")}
    ersatz = [g for g in gates() if g.get("via_local_equivalent")]
    assert ersatz, "No gate with a local equivalent — then this test checks nothing."

    for g in ersatz:
        konfig = schritte[g["id"]].get("with") or {}
        globs = [x.strip() for x in str(konfig.get("globs", "")).split("\n") if x.strip()]
        assert globs, f"Gate '{g['id']}' has no 'globs' in the action — the derivation would run into nothing."
        for glob in globs:
            assert glob in g["command"], (
                f"Glob '{glob}' is in the action, but not in the local command of '{g['id']}'. "
                "The substitute command must be derived from the action, not maintained beside it."
            )


def test_the_runner_still_admits_what_it_cannot_do_at_all() -> None:
    """A substitute tool is not the same as the real step.

    And a step that queries foreign servers has no local equivalent at all: a
    run here says something about the network connection, not about the pull
    request. The runner must keep declaring that — a list that conceals what it
    does not cover reads like completeness.
    """
    gar_nicht = [g for g in gates() if not g["local_runnable"]]
    assert gar_nicht, "Expected: at least one step without a local equivalent."
    ergebnis = subprocess.run(["bash", str(RUNNER), "--list"], cwd=REPO_ROOT, capture_output=True, text=True)
    assert ergebnis.returncode == 0, ergebnis.stderr
    for g in gar_nicht:
        assert g["id"] in ergebnis.stdout, f"The runner conceals '{g['id']}'."


def _list_entries(capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """`ci_gates.py --list`, in process: the line that follows each gate's `[id]` line."""
    import ci_gates

    monkeypatch.setattr(sys, "argv", ["ci_gates.py", "--list"])
    assert ci_gates.main() == 0
    zeilen = capsys.readouterr().out.splitlines()
    return {
        zeile.split("[", 1)[1].split("]", 1)[0]: zeilen[i + 1]
        for i, zeile in enumerate(zeilen)
        if "[" in zeile and "]" in zeile and not zeile.startswith("      ")
    }


def test_the_list_marks_a_writer_gate_as_local_only(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The list says where a gate does not run — as it does for a hosted-only one (RB-M6, F-1).

    `make verify` is annotated "the CI runs the same"; a `placement: writer` gate
    runs there only, and a list that shows it like any other gate reads like
    the CI running it too. Gates that run in both places carry no such mark.
    """
    import ci_gates

    alle = gates()
    writer = [g for g in alle if g["placement"] == "writer"]
    assert writer, "Precondition: the gate list has a writer gate (`ruleset`)."
    eintraege = _list_entries(capsys, monkeypatch)
    for g in alle:
        marked = "nicht in der CI" in eintraege[g["id"]]
        assert marked == (g["placement"] == "writer"), (
            f"`ci_gates.py --list` and the placement of '{g['id']}' ({g['placement']}) disagree about local-only."
        )

    # Not a one-gate accident: a gate that moves to `writer` gets the mark, one that leaves loses it.
    tauschen = {g["id"]: ("both" if g["placement"] == "writer" else g["placement"]) for g in alle}
    erstes_both = next(g["id"] for g in alle if g["placement"] == "both" and g["local_runnable"])
    tauschen[erstes_both] = "writer"
    monkeypatch.setattr(ci_gates, "gates", lambda: [{**g, "placement": tauschen[g["id"]]} for g in alle])
    danach = _list_entries(capsys, monkeypatch)
    assert "nicht in der CI" in danach[erstes_both]
    assert all("nicht in der CI" not in danach[g["id"]] for g in writer)


def test_no_workflow_copies_a_whole_directory_into_a_publish_target() -> None:
    """A `cp -r` into a publish directory is a publication without selection.

    The deleted Pages workflow did exactly that: `cp -r docs/presentations` into
    the directory that GitHub Pages serves. Of the three decks there, two carried
    the customer's real name. The workflow was on `workflow_dispatch` — so not
    dead, but one click away.

    The test does not forbid publishing. It forbids the *copy without
    selection*: what goes out is named, not collected.
    """
    workflows = sorted((REPO_ROOT / ".github" / "workflows").glob("*.yml"))
    assert workflows, "Precondition: there are workflows at all."

    treffer: list[str] = []
    for wf in workflows:
        for nr, zeile in enumerate(wf.read_text(encoding="utf-8").splitlines(), 1):
            entkommentiert = zeile.split("#", 1)[0]
            if re.search(r"\bcp\s+-[a-zA-Z]*r", entkommentiert) and re.search(
                r"_site|public|gh-pages|dist", entkommentiert
            ):
                treffer.append(f"{wf.name}:{nr}  {zeile.strip()}")
    assert not treffer, (
        "Recursive copy into a publish target:\n  "
        + "\n  ".join(treffer)
        + "\n\nUse an allowlist of named files instead — and a gate that runs the "
        "denylist over the publish directory before anything goes up."
    )


@pytest.mark.skip(
    reason="2ee-triage 2026-09-19: instance test — landing-page artefacts "
    "(docs/archive/pages-landing/) live in the origin repo, not in this "
    "checkout. Valve: decision in coding-harness-2ee, at the latest before M1."
)
def test_the_archived_landing_page_is_not_wired_to_anything() -> None:
    """Archived means: no workflow, no active document points at it any more."""
    assert not (REPO_ROOT / ".github" / "workflows" / "publish-html.yml").exists()
    assert (REPO_ROOT / "docs" / "archive" / "pages-landing" / "index.html").is_file(), (
        "The landing page is gone instead of archived — then the evidence of how it looked is missing."
    )
    assert not (REPO_ROOT / "docs" / "index.html").exists()

    aktiv = [REPO_ROOT / "README.md", REPO_ROOT / "AGENTS.md"]
    for datei in aktiv:
        text = datei.read_text(encoding="utf-8")
        assert "publish-html" not in text, f"{datei.name} names the deleted workflow"
        assert "publiziert automatisch" not in text, f"{datei.name} still claims an automatic publication"


# --------------------------------------------------------------------------
# The drift job: the other side moves without a commit in this repo
# --------------------------------------------------------------------------


def _scripts() -> list[Path]:
    ordner = REPO_ROOT / "scripts"
    kandidaten = list(ordner.glob("*.py")) + list(ordner.glob("*.sh"))
    return sorted(p for p in kandidaten if not p.name.startswith("test_"))


def _heimatlose_namen(namen: list[str], ci: str, runner: str, ohne_aufrufer: dict[str, str]) -> list[str]:
    """The pure decision, separated from the file search — so that a control test

    can push real names through, instead of searching for a string in the source
    text of this test file (finding 11, round 2: the glob did not see eight shell
    scripts, and a test that only reads the source text would not have shown that).
    """
    return [
        name
        for name in namen
        if f"scripts/{name}" not in ci and f"scripts/{name}" not in runner and name not in ohne_aufrufer
    ]


def test_every_script_has_a_caller_or_a_declared_reason() -> None:
    """A tool without a caller cannot be told apart from a forgotten one.

    On 2026-08-14, nine of twenty-one scripts had none — and nowhere did it say
    which of them were intentional. Since then the rule is: every script —
    `*.py` as well as `*.sh` — stands either in a `run:` step (`ci.yml`, both
    jobs) or in `ci_gates.OHNE_AUFRUFER` with a reason (RB-G3).

    `ci_gates.py` itself is the caller of the local runner; it counts as wired
    as soon as `verify_all.sh` starts it.
    """
    from ci_gates import OHNE_AUFRUFER

    ci = CI_FILE.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")

    heimatlos = _heimatlose_namen([p.name for p in _scripts()], ci, runner, OHNE_AUFRUFER)
    assert not heimatlos, (
        "Without a caller and without a reason:\n  "
        + "\n  ".join(heimatlos)
        + "\n\nEither a step in ci.yml or a line in ci_gates.OHNE_AUFRUFER."
    )


def test_an_orphan_shell_script_gets_flagged() -> None:
    """The control test to finding 11 (round 2).

    If this test fails, the ratchet does not catch a `.sh` script without a
    caller — exactly the gap that triggered the finding. The name is invented
    (as in `test_a_mere_mention_does_not_count_as_a_test` below): a real script
    name would stand verbatim in `ci.yml` or `verify_all.sh` and would turn the
    check into one that proves nothing.

    Deliberately no second check against the real `scripts/` inventory beside
    it: `_scripts()` depends on the set of scripts in this repo, which does not
    travel with the kit probe (*Leerprobe*, `scripts/kit/probe.py`;
    `manifest.yaml`: only the explicitly named scripts are `mechanismus`, the
    rest is `bestand`) — a reality check would have gone red there through no
    fault of its own.
    """
    heimatlos = _heimatlose_namen(
        ["verwaistes_werkzeug.sh"],
        ci="",
        runner="",
        ohne_aufrufer={},
    )
    assert heimatlos == ["verwaistes_werkzeug.sh"], (
        "A .sh script without a caller and without a reason must fall through the "
        "same check as a .py script — if it does not, the extension to "
        "*.sh is merely claimed, not effective."
    )


def test_the_glob_itself_finds_a_real_orphan_shell_script() -> None:
    """The second half of the control test: not only the derivation, also the glob.

    The previous test sends an invented name directly through
    `_heimatlose_namen()` — that proves the decision does not distinguish
    extensions, but not that `_scripts()` SEES a `.sh` at all. Before finding 11
    (round 2), `_scripts()` globbed only `*.py`; a `.sh` would never have
    reached the candidate list, however the decision would have turned out.

    Hence a real `.sh` without a caller under `scripts/` here — created and
    deleted again within this test, so that none of it is committed and the kit
    probe (`scripts/kit/probe.py`) never gets a look at it: the probe copies
    according to `git ls-files`, and an untracked file does not exist for it.
    """
    ziel = REPO_ROOT / "scripts" / "verwaistes_werkzeug__test_ci_nie_committen.sh"
    ziel.write_text("#!/bin/sh\necho nie aufgerufen\n", encoding="utf-8")
    try:
        from ci_gates import OHNE_AUFRUFER

        ci = CI_FILE.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        heimatlos = _heimatlose_namen([p.name for p in _scripts()], ci, runner, OHNE_AUFRUFER)
        assert ziel.name in heimatlos, (
            f"{ziel.name} lies under scripts/, has no caller and no "
            "declared reason — yet the check does not report it. The "
            "glob in _scripts() sees no *.sh files."
        )
    finally:
        ziel.unlink(missing_ok=True)


def test_no_declared_reason_stands_for_a_script_that_has_a_caller() -> None:
    """The reasons age along. A reason beside a wired script lies."""
    from ci_gates import OHNE_AUFRUFER

    ci = CI_FILE.read_text(encoding="utf-8")
    ueberholt = [n for n in OHNE_AUFRUFER if f"scripts/{n}" in ci]
    assert not ueberholt, f"has long been running in CI, yet carries a reason: {ueberholt}"

    fehlend = [n for n in OHNE_AUFRUFER if not (REPO_ROOT / "scripts" / n).is_file()]
    assert not fehlend, f"Reason for a script that does not exist: {fehlend}"

    ohne_text = [n for n, grund in OHNE_AUFRUFER.items() if len(grund.strip()) < 10]
    assert not ohne_text, f"Reason without content: {ohne_text}"


# ---------------------------------------------------------------------------
# The third ratchet: a script without a test
#
# `OHNE_AUFRUFER` asks whether a script runs. `OHNE_MUTATIONSTEST` asks whether
# a gate can go red. Neither asks whether a script occurs in a test at all — and
# exactly that did not hold for six scripts on 2026-09-08, among them two
# running gates.
# ---------------------------------------------------------------------------

# An import of the module or a start as a subprocess. Both mean: the code is
# executed. An occurrence of the name in prose does not.
#
# Measured via the syntax tree, not via text search — and the reason is a control
# test that refuted the first draft: it checked "the path occurs AND somewhere in
# the file `subprocess` stands". As soon as
# `test_a_mere_mention_does_not_count_as_a_test` further below planted the path
# as example text, `build_sales_deck.py` counted as evidenced — by exactly the
# test that was meant to prove that a mention does not count.
_IMPORT = "^[ \t]*(?:import {mod}\\b|from {mod} import)"


def _zeichenketten(baum: ast.Module) -> set[str]:
    """Every string of the syntax tree — comments are not in there.

    That is exactly the trick: the false evidence was **comments** — on
    2026-09-08 `tests/test_dependencies.py` and `tests/test_human_gates.py` each
    named a script only in prose, and the naive yardstick counted that as
    evidence. A syntax tree does not know comments.

    Why not narrower, only strings *inside a call*: that was the second draft,
    and it lost `export_schemas.py`. Its test builds the path segment by segment
    — `REPO_ROOT / "scripts" / "export_schemas.py"` —, which is a `BinOp`, not a
    `Call`. The same spelling has already undermined a path detection once in
    this repo (see `_verzeichnisse_aus_quelltext`).
    """
    return {
        knoten.value for knoten in ast.walk(baum) if isinstance(knoten, ast.Constant) and isinstance(knoten.value, str)
    }


def _belegt(script: Path) -> list[str]:
    """Which test files execute this script?

    The yardstick is execution, not mention. The naive yardstick
    (`script.name in text`) yielded two untested scripts instead of six on
    2026-09-08: `build_sales_deck.py` stands in a comment in
    `tests/test_dependencies.py`, `export_mermaid_assets.py` in one in
    `tests/test_human_gates.py`. No run touches them.
    """
    treffer: list[str] = []
    muster = re.compile(_IMPORT.format(mod=re.escape(script.stem)), re.M)
    erwartet = {script.name, f"scripts/{script.name}"}
    for datei in _testdateien():
        text = datei.read_text(encoding="utf-8")
        if muster.search(text):
            treffer.append(datei.name)
            continue
        if erwartet & _zeichenketten(ast.parse(text)):
            treffer.append(datei.name)
    return treffer


def test_every_script_has_a_test_or_a_declared_reason() -> None:
    """A tool without a test is invisibly broken.

    Without a caller, a script is conspicuous: it does nothing. Without a test it
    is not conspicuous — it may be doing the wrong thing, and nobody runs it to
    notice. Hence the same rule as for the callers: either a test executes it, or
    it stands with a reason in `ci_gates.OHNE_TEST`.
    """
    from ci_gates import OHNE_TEST

    ungehalten = [p.name for p in _scripts() if p.name not in OHNE_TEST and not _belegt(p)]
    assert not ungehalten, (
        "Without a test and without a reason:\n  "
        + "\n  ".join(ungehalten)
        + "\n\nEither a test file that imports the module or starts it as a "
        "subprocess, or a line in ci_gates.OHNE_TEST."
    )


def test_a_mere_mention_does_not_count_as_a_test() -> None:
    """The control test for the yardstick (AK-2).

    A file that names the script only in a comment evidences nothing. If this
    test fails, the yardstick has fallen back to substring occurrence — and then
    the ratchet above reports completeness over a set that does not contain the
    untested scripts at all.

    **The name is invented.** A real one would be wrong here: the expected
    strings would then stand verbatim in this file, `_belegt` would find them in
    the syntax tree of `test_ci.py` — and the script would count as evidenced by
    the test that is meant to prove that a mention does not count. That is
    exactly what happened with the second draft.
    """
    name = "erfundenes_werkzeug.py"
    nur_erwaehnt = f"# scripts/{name} wird hier nur erwaehnt\nimport subprocess\nX = 1\n"
    ausgefuehrt = f"import subprocess\nsubprocess.run(['python3', 'scripts/{name}'])\n"
    segmentweise = f'from pathlib import Path\nSCRIPT = Path("scripts") / "{name}"\n'

    erwartet = {name, f"scripts/{name}"}
    assert not (erwartet & _zeichenketten(ast.parse(nur_erwaehnt))), (
        "The name stands only in a comment, and `subprocess` stands in the file — "
        "still nothing touches the script. That must not count as evidence."
    )
    assert erwartet & _zeichenketten(ast.parse(ausgefuehrt)), (
        "A real subprocess call must count as evidence, otherwise the yardstick is worthless."
    )
    assert erwartet & _zeichenketten(ast.parse(segmentweise)), (
        "The segment-by-segment spelling must count as evidence — the second draft failed on it (`export_schemas.py`)."
    )


def test_the_test_exemption_list_only_shrinks() -> None:
    """Three is the state as of 2026-09-08. The number may fall and never rise.

    Whoever creates a script writes its test; whoever resolves one of the reasons
    here strikes the line. Without a cap the ratchet would be a filing tray:
    every new untested script would get an entry, and everything would stay
    green.
    """
    from ci_gates import OHNE_TEST

    assert len(OHNE_TEST) <= 3, (
        f"The exemption list has grown to {len(OHNE_TEST)}. A new script needs a test, not an entry here."
    )


def test_no_declared_reason_stands_for_a_script_that_has_a_test() -> None:
    """These reasons age too. A reason beside a tested script lies."""
    from ci_gates import OHNE_TEST

    ueberholt = {n: _belegt(REPO_ROOT / "scripts" / n) for n in OHNE_TEST}
    ueberholt = {n: t for n, t in ueberholt.items() if t}
    assert not ueberholt, f"has long had a test, yet carries a reason: {ueberholt}"

    fehlend = [n for n in OHNE_TEST if not (REPO_ROOT / "scripts" / n).is_file()]
    assert not fehlend, f"Reason for a script that does not exist: {fehlend}"

    ohne_text = [n for n, grund in OHNE_TEST.items() if len(grund.strip()) < 10]
    assert not ohne_text, f"Reason without content: {ohne_text}"


# ---------------------------------------------------------------------------
# Reasons that cite a tracker item
# ---------------------------------------------------------------------------

# `wp-p3.7.1` or `portfolio-agentic-engineering-wp-p3.7.1` — both forms occur in
# the reasons. The catalogue number `V-10` is NOT an item id; it is resolved via
# the title prefix.
_VORGANG = re.compile(r"`(?:portfolio-agentic-engineering-)?([a-z0-9]+[a-z0-9.\-]*)`")
_KATALOG = re.compile(r"\bV-(\d{2})\b")


def _bead_status() -> dict[str, str]:
    """`id -> status` from the tracker state, fetched via the ONE
    access point (bead 1jg.3): in CI the preset render, for the writer a fresh
    render, transitionally the committed copy. Parsing stays file reading — the
    access point decides WHICH file that is.
    """
    from bead_render import render_pfad  # noqa: E402 — the ONE access point

    zeilen = render_pfad().read_text(encoding="utf-8").splitlines()
    status: dict[str, str] = {}
    titel: dict[str, str] = {}
    for zeile in zeilen:
        zeile = zeile.strip()
        if not zeile:
            continue
        try:
            satz = json.loads(zeile)
        except json.JSONDecodeError:
            continue
        if isinstance(satz, dict) and isinstance(satz.get("id"), str):
            status[satz["id"]] = str(satz.get("status", ""))
            if isinstance(satz.get("title"), str):
                titel[satz["id"]] = satz["title"]
    # The catalogue numbers as a second key: "V-10: ..." -> the same state.
    for bid, t in titel.items():
        m = re.match(r"^V-(\d{2})\b", t)
        if m:
            status[f"V-{m.group(1)}"] = status[bid]
    return status


def test_no_declared_reason_cites_a_closed_or_unknown_bead() -> None:
    """A reason that points to a closed item keeps an exception open
    for someone who is no longer there.

    Measured on 2026-09-08: `build_sales_deck.py` carried *"V-31 deletes it with
    the deck path"*. V-31 had been closed since 2026-08-14 — and had never had
    this subject, but `publish-html.yml` and the landing page. So the exception
    stood on a promise nobody had made.
    """
    from ci_gates import OHNE_AUFRUFER, OHNE_TEST

    status = _bead_status()
    assert status, "The bead export is empty — the check measures nothing (RB-G7)."

    schlecht: list[str] = []
    for quelle, dct in (("OHNE_AUFRUFER", OHNE_AUFRUFER), ("OHNE_TEST", OHNE_TEST)):
        for name, grund in dct.items():
            zitiert = set(_VORGANG.findall(grund)) | {f"V-{n}" for n in _KATALOG.findall(grund)}
            for vid in zitiert:
                if vid not in status:
                    continue  # not an item but a file name or the like — not checked here
                if status[vid] == "closed":
                    schlecht.append(f"{quelle}[{name}] cites {vid}, closed")
    assert not schlecht, (
        "Reason points to a closed item:\n  "
        + "\n  ".join(schlecht)
        + "\n\nEither correct the reason or reopen the item."
    )


def test_drift_job_runs_on_schedule_and_dispatch_only() -> None:
    """The timer is the enforcement.

    A DRIFT check without `schedule:` is a report: the other side moves without
    a commit in this repo, so no pull request can trigger it (ADR-028 R2,
    RB-G3). And conversely the job must not hang on every PR — it reads an
    outside world that the PR did not change.
    """
    doc = yaml.safe_load(CI_FILE.read_text(encoding="utf-8"))
    trigger = doc.get("on") or doc.get(True)
    assert "schedule" in trigger, "no timer — the drift job can never run"
    assert trigger["schedule"], "empty schedule block"
    assert "workflow_dispatch" in trigger, "no manual start for the drift job"

    drift = doc["jobs"]["drift"]
    bedingung = drift["if"]
    assert "schedule" in bedingung and "workflow_dispatch" in bedingung, bedingung
    assert "push" not in bedingung and "pull_request" not in bedingung, (
        "The drift job hangs on the pull request — then every PR pays for a "
        "measurement of an outside world that it did not change."
    )

    verify = doc["jobs"]["verify"]
    assert "push" in verify["if"] and "pull_request" in verify["if"], (
        "The verification job would otherwise have to run on the timer too, and there it would say nothing."
    )


def test_the_drift_job_runs_the_plans_registry_strictly() -> None:
    """The two lifecycle rules have their timer.

    `plans_registry.py` reports "built and not archived" and a one-sided
    supersession as DRIFT. Without a call with `--strict`, under ADR-028 R2 that
    stays a report instead of a gate — this test pins that exactly this call
    stands in the `drift` job.
    """
    treffer = [g for g in gates() if g["job"] == "drift" and "plans_registry.py" in (g["command"] or "")]
    assert treffer, "no step in the drift job calls plans_registry.py"
    assert any("--strict" in g["command"] for g in treffer), (
        "plans_registry.py runs in the drift job, but without --strict — so "
        "the two lifecycle rules stay out of reach for an exit other than 0."
    )


def test_the_drift_job_holds_only_steps_that_can_run() -> None:
    """A step that fails without an instance checkout makes the job chronically red.

    A job that is red every morning is not read — that is the same failure as no
    job at all, only with noise. So `drift` holds today only what runs here;
    everything else carries a reason in `OHNE_AUFRUFER`.
    """
    drift_gates = [g for g in gates() if g["job"] == "drift" and not g["id"].startswith("drift-setup")]
    assert drift_gates, "the drift job has not a single check step"
    for g in drift_gates:
        assert "oracle-source-inventory" not in g["command"], (
            f"{g['id']} needs the project instance, which is not checked out here"
        )
        assert "--project-path" not in g["command"], f"{g['id']} needs an instance path"


# --------------------------------------------------------------------------
# Mutation coverage (RB-G4)
# --------------------------------------------------------------------------

# A test that only asserts that it is green today checks the world and not the
# gate. Only the mutation test says something about the gate: **does it go red
# if you break what it is meant to protect against?**
#
# These name forms count as mutation evidence. The list is deliberately bound to
# names and not to comments: a name is carried along when something is renamed,
# a comment is not.
MUTATIONS_NAMEN = re.compile(
    r"^def (test_\w*(?:goes_red|red_on|detects_tampering|refuses|is_caught|catches|"
    r"not_a_write|is_an_error|is_exit_2|never_writes|is_not_a_pass|notices)\w*)\(",
    re.M,
)

# Gates without mutation evidence — with the reason and the intent.
#
# This list is a **ratchet**: it may shrink, never grow. Whoever adds a gate
# writes its mutation test; whoever resolves one of the reasons here strikes the
# line. The valve `gate-mutation-coverage` carries the deadline (RB-G4).
OHNE_MUTATIONSTEST: dict[str, str] = {
    "pytest": "runs the mutation tests itself; a mutant for it would be circular",
    "ruff-check": "third-party tool; the choice of rule groups is held instead by ramp_valves.py",
    "ruff-format": "third-party tool with its own test suite; we do not mutate its formatter",
    "markdownlint": "third-party tool via a marketplace action; we do not mutate its rule set",
    "lychee": "third-party tool, advisory — a red run says something about the network, not the candidate",
    "plans-registry": "the hygiene rules run green in test_gate_machinery.py; the seeded red run is still outstanding in the 2ee-triage",
    "plans-registry-strict": "same machine as plans-registry, only on the timer — the evidence falls with it",
}


def test_the_mutation_exemption_list_only_shrinks() -> None:
    """W-8: the ratchet that the comment promises and no test held.

    `OHNE_MUTATIONSTEST` lists gates for which there is no mutation counterpart.
    The associated test asserts three things — no exception for a vanished gate,
    none for one already covered, no duplicate — but **not that the list must not
    grow**. Whoever creates a new gate without a control test enters it, and
    everything stays green.

    Twelve is the state as of 2026-09-07. The number may fall and never rise.
    """
    assert len(OHNE_MUTATIONSTEST) <= 12, (
        f"The exemption list has grown to {len(OHNE_MUTATIONSTEST)}. A new gate "
        "needs a seeded control test, not an entry here."
    )


def _testdateien() -> list[Path]:
    return sorted((REPO_ROOT / "tests").glob("test_*.py"))


def _pruefling(gate: dict) -> str:
    """The subject of this gate — the script it runs."""
    befehl = gate.get("command") or ""
    # The subfolder has to be included: until 2026-09-08 the pattern ended before
    # the second `/`, and a script under `scripts/kit/` was invisible to the
    # ratchet — it reported "no script recognisable" and demanded an exception
    # for a gate that had long had its mutation evidence.
    m = re.search(r"(?:scripts|docs/patterns)/(?:[A-Za-z_]+/)*([A-Za-z_]+\.py)", befehl)
    if m:
        return m.group(1)
    # A gate can also run a test file itself — `ruleset-drift` checks a statement
    # about the repo configuration for which there is no script and there should
    # be none: a tool that can change rulesets would be a greater risk than the
    # finding it makes. Its mutation evidence then lies in exactly that file, and
    # that is where the ratchet looks for it too.
    m = re.search(r"(tests/[A-Za-z_]+\.py)", befehl)
    return m.group(1) if m else ""


def test_every_gate_step_has_a_mutation_test() -> None:
    """Every gate has a run that turns it red — or a reason in the ratchet.

    Measured on 2026-08-14: nine of twenty-one steps had none. Four of them
    because their tool had no tests at all.
    """
    quellen = {p: p.read_text(encoding="utf-8") for p in _testdateien()}

    ohne: list[str] = []
    for g in gates():
        gid = g["id"]
        if gid.endswith("setup-deps"):
            continue
        ziel = _pruefling(g)
        if not ziel:
            if gid not in OHNE_MUTATIONSTEST:
                ohne.append(f"{gid} (no script recognisable)")
            continue
        if ziel.startswith("tests/"):
            # If the gate runs a test file, its evidence lies IN that file. The
            # search below would instead accept every file that merely MENTIONS
            # the path — on 2026-09-08 that made `test_workflow_entry.py` the
            # evidence for `ruleset-drift`, because it names the name in a list
            # and has some mutation evidence of its own. A coverage that assumes
            # from a mention covers nothing.
            datei = REPO_ROOT / ziel
            belegt = datei.is_file() and bool(MUTATIONS_NAMEN.search(datei.read_text(encoding="utf-8")))
        else:
            belegt = any(MUTATIONS_NAMEN.search(text) for p, text in quellen.items() if ziel in text)
        if not belegt and gid not in OHNE_MUTATIONSTEST:
            ohne.append(f"{gid} → {ziel}")

    assert not ohne, (
        "Gate without mutation evidence and without an entry in the ratchet:\n  "
        + "\n  ".join(ohne)
        + "\n\nEither write a `*_goes_red_when_*` test or enter the reason "
        "in OHNE_MUTATIONSTEST — both are a decision, silence is not."
    )


def test_the_mutation_ratchet_only_turns_one_way() -> None:
    """An entry in the ratchet whose gate has long been covered lies.

    And an entry for a gate that no longer exists keeps an exception open for
    something nobody runs any more.
    """
    quellen = {p: p.read_text(encoding="utf-8") for p in _testdateien()}
    bekannt = {g["id"]: g for g in gates()}

    verwaist = sorted(set(OHNE_MUTATIONSTEST) - set(bekannt))
    assert not verwaist, f"Exception for a gate that does not exist: {verwaist}"

    ueberholt = []
    for gid in OHNE_MUTATIONSTEST:
        ziel = _pruefling(bekannt[gid])
        if ziel and any(MUTATIONS_NAMEN.search(t) for p, t in quellen.items() if ziel in t):
            ueberholt.append(gid)
    assert not ueberholt, f"long since covered, but still in the ratchet: {ueberholt}"

    ohne_grund = [g for g, grund in OHNE_MUTATIONSTEST.items() if len(grund.strip()) < 10]
    assert not ohne_grund, f"Exception without a reason: {ohne_grund}"
