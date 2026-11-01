"""Every model named resolves to a declared endpoint (RB-A6).

**The gap this closes.** `docs/WORKFLOW.md` has always said which model runs
in which phase. Where it runs and what it may see was stated nowhere until
2026-09-08: `rg` over `docs/governance/` for `residen|endpunkt|datenabfluss`
found not one normative hit. An agent could name a model, and nobody held the
name against anything.

The requirement is not theoretical. Customer code carries the customer's
structure and identifiers: a model that sees it sees the data model, even
without a single row of payload data.
"""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ENDPUNKTE = REPO_ROOT / "model-endpoints.yaml"
AGENTEN = REPO_ROOT / ".claude" / "agents"
WORKFLOW = REPO_ROOT / "docs" / "WORKFLOW.md"
PROMPTS = REPO_ROOT / "prompts"

RESIDENZEN = ("anbieter-erklaert", "region-waehlbar", "nicht-erklaert")
# The free Zen plan is gone: free Go models are a dynamic online permission
# (`research_swarm.online_free`), not a billing kind of an endpoint.
ABRECHNUNGEN = ("token", "abonnement")


def _erklaerung() -> dict:
    """The declaration, loaded defensively.

    Defensively, because `@pytest.mark.parametrize` runs at **collection**: until
    2026-09-08 a broken or empty file made pytest abort with a `ValueError`
    while computing the test id, and then `test_the_declaration_is_not_empty`,
    which exists to warn of exactly that, never ran. A collection error is not
    a finding but a blind spot.
    """
    try:
        geladen = yaml.safe_load(ENDPUNKTE.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        geladen = {}
    if not isinstance(geladen, dict):
        geladen = {}
    # `setdefault` does NOT replace an existing `None`: when the file holds the
    # bare key `endpunkte:` without a value, yaml gives `{"endpunkte": None}`,
    # and `parametrize(argvalues=None)` dies at collection again. The key is
    # there, the value is missing: exactly the case the first version missed.
    geladen["endpunkte"] = geladen.get("endpunkte") or []
    geladen["datenklassen"] = geladen.get("datenklassen") or {}
    if not isinstance(geladen["endpunkte"], list):
        geladen["endpunkte"] = []
    if not isinstance(geladen["datenklassen"], dict):
        geladen["datenklassen"] = {}
    return geladen


def prompt_modelle() -> list[tuple[Path, str]]:
    """Every phase prompt with the model it names.

    RB-A6 says "every model named here". Until 2026-09-08 the enforcer read only
    `.claude/agents/` and the routing table: the seven prompts named six models
    nobody held against the declaration. And `prompts/` travels as
    `mechanismus`: the gap would have travelled with it.
    """
    gefunden: list[tuple[Path, str]] = []
    if not PROMPTS.is_dir():
        return gefunden
    for p in sorted(PROMPTS.glob("*.md")):
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # The dot must NOT be excluded: "Fable 5.1" and "Haiku 4.5" carry it
        # in the version. A pattern that forbade it missed four of the six
        # prompts, and would have reported that all it found resolved.
        #
        # Bilingual since the prompts became English (2026-09-10). The old
        # pattern knew only `**Modell:**`; after the translation it would have
        # found nothing, `parametrize` would have got an empty list, and a
        # parametrized test over an empty list is GREEN. The gate would have
        # failed in the same commit without anything turning red.
        # `test_prompts_are_found_at_all` stands against that as well.
        m = re.search(r"^\*\*(?:Modell|Model):\*\*\s*([^\n—]+?)\s*(?:—|\.\s*$|$)", text, re.M)
        if not m:
            continue
        wert = m.group(1).strip()
        # Phase 5 is deterministic and names "none" explicitly: a statement,
        # not a model name.
        if wert.lower().startswith(("keines", "keins", "kein ", "none")):
            continue
        gefunden.append((p, wert))
    return gefunden


def _endpunkt_ids(e: object) -> str:
    """An id even for a broken entry; otherwise collection dies."""
    return e.get("name", "(ohne-name)") if isinstance(e, dict) else "(kein-mapping)"


def zugelassene_modelle() -> set[str]:
    return {m for e in _erklaerung()["endpunkte"] if isinstance(e, dict) for m in (e.get("modelle") or [])}


def agent_modelle() -> list[tuple[Path, str]]:
    """Every agent definition with the model it pins."""
    gefunden: list[tuple[Path, str]] = []
    if not AGENTEN.is_dir():
        return gefunden
    for p in sorted(AGENTEN.glob("*.md")):
        # This function runs at import time too. A file that did not decode as
        # UTF-8 broke collection, and then `test_agents_are_found_at_all`, the
        # counter-check for exactly this case, did not run. One half was
        # hardened, this one was not.
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        m = re.search(r"^model:\s*(\S+)\s*$", text, re.M)
        if m:
            gefunden.append((p, m.group(1)))
    return gefunden


# ---------------------------------------------------------------------------
# The set is not empty
# ---------------------------------------------------------------------------


def test_the_declaration_is_not_empty() -> None:
    """An empty admission list lets everything through and checks nothing (RB-G7)."""
    e = _erklaerung()
    assert e["endpunkte"], "not a single endpoint declared"
    assert e["datenklassen"], "not a single data class declared"
    assert zugelassene_modelle(), "not a single model admitted"


def test_prompts_are_found_at_all() -> None:
    """Without prompts found, the test below checks nothing (RB-G7).

    The gap this closes: `prompt_modelle()` reads the model through a pattern.
    When the spelling in the prompts changes (the English translation of
    2026-09-10 changed it), the function returns an empty list.
    `@pytest.mark.parametrize` over an empty list is green. The gate would have
    failed silently, in exactly the commit that should have turned it red.

    The agent definitions always had this counter-check; the prompts lacked it.
    """
    gefunden = prompt_modelle()
    assert gefunden, (
        "not a single phase prompt names a model; does the pattern in "
        "`prompt_modelle()` still read the spelling used in prompts/?"
    )
    # Seven phases plus optional intermediate steps; phase 5 names none
    # explicitly. The lower bound records that the set matters, not a single
    # hit.
    assert len(gefunden) >= 5, f"only {len(gefunden)} prompt(s) with a model found"


def test_agents_are_found_at_all() -> None:
    """Without agent definitions, the test below checks nothing (RB-G7)."""
    assert agent_modelle(), "no agent definition with `model:` found; does the test read the right directory?"


# ---------------------------------------------------------------------------
# The declaration is complete
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("endpunkt", _erklaerung()["endpunkte"], ids=_endpunkt_ids)
def test_every_endpoint_states_operator_residency_and_billing(endpunkt: object) -> None:
    """An endpoint without an operator is a name, not a commitment."""
    assert isinstance(endpunkt, dict), f"entry is not a mapping: {endpunkt!r}"
    for feld in ("name", "betreiber", "residenz", "abrechnung", "darf_sehen", "modelle"):
        assert endpunkt.get(feld), f"{endpunkt.get('name')}: field '{feld}' is missing or empty"
    assert endpunkt["residenz"] in RESIDENZEN, (
        f"{endpunkt['name']}: residenz '{endpunkt['residenz']}' lies outside {RESIDENZEN}"
    )
    assert endpunkt["abrechnung"] in ABRECHNUNGEN, (
        f"{endpunkt['name']}: abrechnung '{endpunkt['abrechnung']}' lies outside {ABRECHNUNGEN}"
    )


@pytest.mark.parametrize("endpunkt", _erklaerung()["endpunkte"], ids=_endpunkt_ids)
def test_only_a_declared_data_class_may_be_seen(endpunkt: object) -> None:
    """`darf_sehen` names classes from the vocabulary, not invented ones."""
    assert isinstance(endpunkt, dict), f"entry is not a mapping: {endpunkt!r}"
    bekannt = set(_erklaerung()["datenklassen"])
    fremd = set(endpunkt["darf_sehen"]) - bekannt
    assert not fremd, f"{endpunkt['name']}: unknown data class(es) {sorted(fremd)}"


def test_customer_code_never_reaches_an_endpoint_without_stated_residency() -> None:
    """The actual requirement, and the reason this file exists.

    Customer code carries the customer's structure and identifiers. An endpoint
    without a stated residency cannot answer the question "where does it live",
    and that question is asked only once the answer is expensive.
    """
    verletzer = [
        e.get("name")
        for e in _erklaerung()["endpunkte"]
        if isinstance(e, dict) and "kundencode" in (e.get("darf_sehen") or []) and e.get("residenz") == "nicht-erklaert"
    ]
    assert not verletzer, f"endpoint(s) without a stated residency that may see customer code: {verletzer}"


def test_no_endpoint_is_cleared_for_customer_rows() -> None:
    """Rows do not leave the customer's environment: no exception, no provider."""
    verletzer = [
        e.get("name")
        for e in _erklaerung()["endpunkte"]
        if isinstance(e, dict) and "kundendaten" in (e.get("darf_sehen") or [])
    ]
    assert not verletzer, (
        f"endpoint(s) cleared for customer data: {verletzer}. "
        "The machine builds the pipeline; it does not read the data."
    )


# ---------------------------------------------------------------------------
# Every model named resolves
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("pfad,modell", agent_modelle(), ids=lambda v: getattr(v, "name", str(v)))
def test_every_agent_model_resolves_to_a_declared_endpoint(pfad: Path, modell: str) -> None:
    """Not listed is BLOCK: the same rule as in the two manifests."""
    assert modell in zugelassene_modelle(), (
        f"{pfad.name} pins '{modell}', which no endpoint in model-endpoints.yaml lists.\n"
        "Either declare the endpoint (with operator, residency and billing kind) "
        "or change the model."
    )


def _kandidaten(anzeige: str) -> set[str]:
    """A display name ("Sonnet 5") to its possible ids ("claude-sonnet-5").

    Two spellings of a version: dots turned into dashes (`claude-sonnet-5-5`,
    the id Anthropic gives) and dots kept (`glm-5.3`, `gpt-6.1-sol`, the ids
    other vendors give).
    """
    kern = anzeige.lower().replace(" ", "-").replace(".", "-")
    with_dots = anzeige.lower().replace(" ", "-")
    return {f"claude-{kern}", kern, with_dots, f"claude-{with_dots}"}


def _loest_auf(anzeige: str, ids: set[str]) -> bool:
    """Equality, not a substring.

    `any(kern in i for i in ids)` let "**Sonnet**" without a generation pass,
    because "sonnet" is inside "claude-sonnet-5": the table could have stopped
    naming a generation, and the check would have stayed green.
    """
    return bool(_kandidaten(anzeige) & ids)


def routing_models(text: str) -> list[str]:
    """The model names of the routing rows in `text`.

    A routing row starts with a phase number and an optional letter (`2a`,
    `4b`), then a phase name of one or more words, then the model in bold. The
    pattern used to read one digit and one word, and skipped the rows a stage 2
    adds.
    """
    return re.findall(r"^\| \d[a-z]? [A-Za-z][A-Za-z ]*? \| \*\*([^*]+)\*\* \|", text, re.M)


def test_every_model_in_the_routing_table_resolves() -> None:
    """The doctrine names models too, and they must resolve as well.

    Otherwise the rule holds for agent definitions and not for the table from
    which a person picks a model.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    tabelle = routing_models(text)
    assert tabelle, "no model found in the routing of docs/WORKFLOW.md (RB-G7)"
    # The table names display names ("Haiku 4.5"), the declaration ids.
    ids = zugelassene_modelle()
    for anzeige in tabelle:
        if anzeige in {"the ladder", "the swarms, then the ladder"}:
            continue  # no model id: the ids live in the `opencode-go` entry, checked by its own test
        if anzeige == "the research swarm":
            # No single model id: the swarm is a declared role roster. The row
            # resolves only while the declaration itself is complete and every
            # id it names sits on its declared endpoint.
            assert swarm_block_problems(_erklaerung()) == [], (
                "docs/WORKFLOW.md routes to 'the research swarm', but the declared swarm is incomplete"
            )
            continue
        assert _loest_auf(anzeige, ids), (
            f"docs/WORKFLOW.md routes to '{anzeige}', which no endpoint lists. "
            f"Looked for: {' or '.join(sorted(_kandidaten(anzeige)))}"
        )


@pytest.mark.parametrize("pfad,anzeige", prompt_modelle(), ids=lambda v: getattr(v, "name", str(v)))
def test_every_model_in_a_phase_prompt_resolves(pfad: Path, anzeige: str) -> None:
    """The seven prompts name models, and `prompts/` travels as mechanism."""
    ids = zugelassene_modelle()
    assert _loest_auf(anzeige, ids), (
        f"{pfad.name} names '{anzeige}', which no endpoint in model-endpoints.yaml lists. "
        f"Looked for: {' or '.join(sorted(_kandidaten(anzeige)))}"
    )


def test_a_dotted_id_resolves_and_a_prefix_does_not() -> None:
    """A display name with a dot resolves to the id that keeps it; a prefix does not."""
    assert _loest_auf("GLM 5.3", {"glm-5.3"})
    assert _loest_auf("gpt-6.1-sol", {"gpt-6.1-sol"})
    assert _loest_auf("Sonnet 5.5", {"claude-sonnet-5-5"})
    assert not _loest_auf("GLM 5", {"glm-5.3"}), "a prefix must not resolve by substring"


def test_the_routing_check_reads_lettered_and_multi_word_rows() -> None:
    """A row with a lettered phase or a phase name of several words is read."""
    text = "| 2a Spec review | **k3** | x |\n| 4b Review loop | **k3** | x |\n"
    assert routing_models(text) == ["k3", "k3"]
    assert routing_models("| 1 | Explore | x |\n") == []


# ---------------------------------------------------------------------------
# The opencode-go entry (stage2-mimo)
# ---------------------------------------------------------------------------


def _endpunkt(name: str) -> dict:
    """The one entry declared under `endpunkte:` with this name, or `{}`.

    Defensive like the declaration itself: a test over a missing entry must
    fail on its own assertion, not die on a `KeyError` the reader cannot place.
    """
    for e in _erklaerung()["endpunkte"]:
        if isinstance(e, dict) and e.get("name") == name:
            return e
    return {}


def test_the_opencode_go_entry_is_declared() -> None:
    """Criterion 1: the entry, its fields and the ladder order - refuted by any other value."""
    entry = _endpunkt("opencode-go")
    assert entry["betreiber"] == "OpenCode (Operator Anomaly Innovations, Inc.)"
    assert entry["residenz"] == "anbieter-erklaert"
    assert entry["abrechnung"] == "abonnement"
    assert entry["darf_sehen"] == ["framework"]
    # Membership is configuration: adding a model must require no test edit.
    models = entry["modelle"]
    assert isinstance(models, list) and models
    assert all(isinstance(model, str) and model for model in models)
    assert len(models) == len(set(models))
    # The paid Flash swarm (Q-10) and the free-stage rule (ADR 0021, decision 2).
    flash = entry["flash_swarm"]
    assert isinstance(flash, list)
    assert all(isinstance(model, str) and model for model in flash)
    assert len(flash) == len(set(flash))
    free = entry["free_stage"]
    assert free["provider"] == "opencode-go"
    assert free["id_suffix"] == "-free"
    assert free["include"] == []
    # Each exclusion is a dated decision; its record shape is validated below
    # through the runner's own `free_rule_problems`.
    assert [record["id"] for record in free["exclude"]] == ["step-5-preview-free"]
    assert free["input"] == "implementation-diff"


def _stage2():
    """The runner module, or None where the kit does not carry it.

    Lazy import, and never at collection time: `scripts/stage2.py` is not in
    the kit's `mechanismus`, and a module-level import would kill this whole
    file's collection in the throwaway repo - every declared red case in it
    would lose its explanation at once.
    """
    import sys

    root = Path(__file__).resolve().parent.parent
    if not (root / "scripts" / "stage2.py").is_file():
        return None
    sys.path.insert(0, str(root / "scripts"))
    try:
        import stage2
    except ImportError:
        return None
    return stage2


def test_free_selection_exceptions_require_dates_and_reasons() -> None:
    """Criterion 5: a free-rule exception without its date or reason does not pass validation.

    The validator is the runner's `free_rule_problems`, shared with every call
    that reads the rule; here it is held against planted mutants of the real
    entry, so a looser validator fails this file.
    """
    entry = dict(_endpunkt("opencode-go"))
    assert entry.get("free_stage", {}).get("provider") == "opencode-go"
    runner = _stage2()
    if runner is None:
        pytest.fail("the kit does not carry scripts/stage2.py; the rule validator cannot run here")
    assert runner.free_rule_problems(entry) == []
    rule = entry["free_stage"]
    dated = {"id": "extra-free", "date": "2026-10-16", "reason": "measured in the catalog"}
    # An exclude wins over matches - and so its record needs all three fields.
    for field in ("id", "date", "reason"):
        broken = {**entry, "free_stage": {**rule, "exclude": [{**dated, field: ""}]}}
        problems = runner.free_rule_problems(broken)
        assert problems and field in str(problems), f"an exclude without {field} passed validation"
    broken = {**entry, "free_stage": {**rule, "include": [{"id": "x-free", "date": "2026-13-45", "reason": "r"}]}}
    assert runner.free_rule_problems(broken), "an impossible date passed validation"
    broken = {**entry, "free_stage": {**rule, "exclude": ["ad-hoc-free"]}}
    assert runner.free_rule_problems(broken), "a bare string passed as an exception record"
    # The Zen provider never enters the rule, and the input stays the diff.
    broken = {**entry, "free_stage": {**rule, "provider": "opencode"}}
    assert any("Zen" in problem for problem in runner.free_rule_problems(broken))
    broken = {**entry, "free_stage": {**rule, "input": "full-repository"}}
    assert runner.free_rule_problems(broken), "a broader input than the implementation diff passed"
    broken = {**entry, "free_stage": {**rule, "id_suffix": "", "include": []}}
    assert runner.free_rule_problems(broken), "a rule that selects nothing passed"


def test_every_new_paid_model_carries_its_terms_reading() -> None:
    """Criterion 6: a paid model is admitted only with a dated terms reading or a dated skip.

    Every `modelle` id holds a `modelle_terms` record; an admitted one carries
    the date and the source of the retention/training reading, a skipped one
    its date and reason - so no paid model is silently omitted.
    """
    entry = _endpunkt("opencode-go")
    modelle = entry.get("modelle") or []
    assert modelle and len(modelle) == len(set(modelle))
    terms = entry.get("modelle_terms") or {}
    admitted, skipped = [], []
    for model in modelle:
        record = terms.get(model) or {}
        if record.get("uebersprungen"):
            assert record.get("grund"), f"{model} is skipped without its reason"
            assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(record["uebersprungen"]))
            skipped.append(model)
            continue
        assert record.get("gelesen"), f"{model} has no dated terms reading and no skip"
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(record["gelesen"]))
        assert record.get("quelle"), f"{model} names no source for its terms reading"
        assert record.get("training") == "Not used", f"{model} permits training or leaves it unread"
        assert record.get("aufbewahrung"), f"{model} leaves retention unread"
        admitted.append(model)
    assert set(admitted) | set(skipped) == set(modelle)

    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    import stage2

    # Q-13: every ladder model declares its dated cost value; the runner's ladder follows it, cheapest first.
    terms = entry["modelle_terms"]
    for model in admitted:
        record = terms[model]
        value = record.get("anfragen_5h")
        assert isinstance(value, int) and not isinstance(value, bool) and value > 0, f"{model}: no cost value"
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(record.get("anfragen_gelesen"))), f"{model}: no reading date"
        assert "opencode.ai/docs/go" in str(record.get("anfragen_quelle")), f"{model}: no source"
    order = stage2.ordered_models(entry, admitted)
    values = [terms[model]["anfragen_5h"] for model in order]
    assert values == sorted(values, reverse=True), "the ladder is not cheapest first"
    assert set(order) == set(admitted)
    # The hand-kept Flash swarm may drift as new cheaper models are declared.
    notice = stage2.cheapest_notice(entry, order, entry["flash_swarm"])
    assert bool(notice) == (set(entry["flash_swarm"]) != set(order[:3]))


def test_unread_terms_reach_the_free_stage_alone() -> None:
    """Criterion 7: the unread-terms acceptance is declared for the free class and bounded by it."""
    entry = _endpunkt("opencode-go")
    free = entry.get("free_stage") or {}
    # The diff-only purpose is a declared field, not prose alone ...
    assert free.get("input") == "implementation-diff"
    # ... and the acceptance names its own bounds: unread terms, no tools,
    # and no paid, Zen or interactive use of the exception.
    hinweis = free.get("hinweis", "")
    one = " ".join(hinweis.split())
    assert "NOT read" in one, "the acceptance does not state that the terms are unread"
    assert "no" in one and "tools" in one, "the acceptance does not state the tool-free confinement"
    for forbidden in ("paid model", "Zen", "interactive session"):
        assert forbidden in one, f"the acceptance does not name what it does not cover: {forbidden}"


# ---------------------------------------------------------------------------
# The one Go address record (go-access-point)
# ---------------------------------------------------------------------------


def _address_problems(entry: dict) -> list[str]:
    """What makes the entry's `adresse` unusable as the one Go address record.

    The synthetic cases below carry the faults; the real entry is checked with
    the same function, so the orchestrator's bootstrap cannot land a weaker
    shape than these tests hold (plan step 10: the runner never edits the held
    file). The strictness mirrors the runner's `load_address_policy`: exact
    keys, one host, per-wire-api bases on that host, dated sources.
    """
    problems: list[str] = []
    record = entry.get("adresse")
    if not isinstance(record, dict):
        return ["no adresse record"]
    if set(record) != {"host", "apis"}:
        problems.append(f"unknown or missing address keys: {sorted(record)}")
        return problems
    host = record["host"]
    if not isinstance(host, str) or not re.fullmatch(r"[a-z0-9.-]+", host or ""):
        problems.append(f"host is not a plain hostname: {host!r}")
        return problems
    apis = record["apis"]
    if not isinstance(apis, dict) or not apis:
        problems.append("no per-wire-api bases")
        return problems
    for api, part in apis.items():
        if not isinstance(api, str) or not api:
            problems.append("a wire api key is not a plain string")
            continue
        if not isinstance(part, dict) or set(part) != {"basis", "quelle", "gelesen"}:
            problems.append(f"{api}: not exactly basis, quelle and gelesen")
            continue
        if not isinstance(part["basis"], str) or not part["basis"].startswith(f"https://{host}/"):
            problems.append(f"{api}: basis is not an HTTPS URL on {host}")
        if not isinstance(part["quelle"], str) or not part["quelle"].strip():
            problems.append(f"{api}: quelle is missing or blank")
        read = part["gelesen"]
        if not isinstance(read, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", read):
            problems.append(f"{api}: gelesen is not a quoted ISO date")
        else:
            try:
                dt.date.fromisoformat(read)
            except ValueError:
                problems.append(f"{api}: gelesen is not a calendar date")
    return problems


def _address_fixture() -> dict:
    """The minimal valid record, as the orchestrator's bootstrap will declare it."""
    return {
        "name": "opencode-go",
        "adresse": {
            "host": "opencode.ai",
            "apis": {
                "openai-completions": {
                    "basis": "https://opencode.ai/zen/go/v1",
                    "quelle": "https://opencode.ai/docs/go",
                    "gelesen": "2026-10-31",
                }
            },
        },
    }


ADDRESS_FAULTS = {
    "no-record": lambda e: e.pop("adresse"),
    "unknown-key": lambda e: e["adresse"].update(gueltig_bis="x"),
    "no-apis": lambda e: e["adresse"].pop("apis"),
    "apis-not-a-map": lambda e: e["adresse"].update(apis=[]),
    "api-key-empty": lambda e: e["adresse"].update(apis={"": e["adresse"]["apis"]["openai-completions"]}),
    "host-with-scheme": lambda e: e["adresse"].update(host="https://opencode.ai"),
    "host-empty": lambda e: e["adresse"].update(host=""),
    "base-keys-broken": lambda e: e["adresse"]["apis"]["openai-completions"].pop("quelle"),
    "extra-base-key": lambda e: e["adresse"]["apis"]["openai-completions"].update(notiz="x"),
    "foreign-host-base": lambda e: e["adresse"]["apis"]["openai-completions"].update(
        basis="https://elsewhere.invalid/zen/go/v1"
    ),
    "plain-http-base": lambda e: e["adresse"]["apis"]["openai-completions"].update(
        basis="http://opencode.ai/zen/go/v1"
    ),
    "userinfo-base": lambda e: e["adresse"]["apis"]["openai-completions"].update(
        basis="https://user@opencode.ai/zen/go/v1"
    ),
    "blank-source": lambda e: e["adresse"]["apis"]["openai-completions"].update(quelle="   "),
    "native-date": lambda e: e["adresse"]["apis"]["openai-completions"].update(gelesen=dt.date(2026, 10, 31)),
    "impossible-date": lambda e: e["adresse"]["apis"]["openai-completions"].update(gelesen="2026-13-45"),
}


def test_the_address_record_shape_is_validated() -> None:
    """The record's faults are named: shape, dated sources, bases on the host (plan step 10)."""
    assert _address_problems(_address_fixture()) == []
    for name, fault in ADDRESS_FAULTS.items():
        entry = _address_fixture()
        fault(entry)
        assert _address_problems(entry), f"{name}: the fault passed the record shape check"


def test_the_opencode_go_entry_declares_its_address_record() -> None:
    """Criterion 1 (go-access-point): the real entry carries the record the runner loads.

    The orchestrator's bootstrap has landed (plan step 12): a missing or
    malformed record must fail, including deletion of the whole record.
    """
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    stage2_go = pytest.importorskip("stage2_go", reason="the runner is not part of this repository")

    entry = _endpunkt("opencode-go")
    assert _address_problems(entry) == []
    # The runner's own loader accepts exactly what the shape check accepts.
    try:
        policy = stage2_go.load_address_policy(REPO_ROOT)
    except stage2_go.RecordUnusable as error:
        raise AssertionError(f"the declared record does not load: {error}") from None
    assert policy.host == entry["adresse"]["host"]


def test_missing_address_record_fails_the_real_entry_proof(monkeypatch) -> None:
    """Deleting the bootstrapped address must fail the criterion's named proof, never skip it."""
    # The exported kit carries this test but not the runner. Only that missing
    # dependency may skip the proof; a missing production address may not.
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    pytest.importorskip("stage2_go", reason="the runner is not part of this repository")
    entry = dict(_endpunkt("opencode-go"))
    entry.pop("adresse", None)
    monkeypatch.setattr(__import__(__name__), "_endpunkt", lambda _name: entry)
    try:
        with pytest.raises(AssertionError, match="no adresse record"):
            test_the_opencode_go_entry_declares_its_address_record()
    except pytest.skip.Exception:
        pytest.fail("the missing production address record skipped its proof")


def opencode_remark_problems(remark: str) -> list[str]:
    """Criterion 2: every point of the remark, each one stated by its source."""
    one = " ".join(remark.split())
    found = []
    for needle in (
        "https://opencode.ai/zen/go/v1/chat/completions",
        "https://opencode.ai/zen/go/v1/messages` is not used",
        "refused on 2026-10-08",
        "Pi at the version the runner pins",
        "lists Pi among its validated clients",
        "`x-opencode-session` header",
        '"automatically or programmatically extracts data or Output"',
        '"while you are not logged into the Services"',
        "effective 2026-08-15",
        "accepted this residual risk on 2026-10-08",
        "USD 10 a month",
        "deepseek-v4.1-flash` USD 0.15",
        "0.30 / 1.20",
        "limit USD 60",
        "mimo-v2.6-pro` 0.435 / 0.87, limit USD 15",
        "0 days",
        '"Not used"',
        "valid through 2026-10-31",
        "On 2026-10-31 the Go page names only `/inference/go/` addresses",
        "the admitted host and the known base stand in `adresse` (ADR 0024)",
        "states no region",
        '"All our models are hosted in the US and EU."',
        "read 2026-10-07",
        "phase 2a",
        "phase 4b",
        "phase 6",
        "scripts/stage2.py",
    ):
        if needle not in one:
            found.append(needle)
    return found


def test_the_opencode_go_remark_names_every_source() -> None:
    """Criterion 2: the remark says what OpenCode states, with its source and date."""
    remark = _endpunkt("opencode-go")["bemerkung"]
    assert opencode_remark_problems(remark) == []
    planted = remark.replace('"All our models are hosted in the US and EU."', "a region it does not name")
    assert opencode_remark_problems(planted)
    planted = remark.replace("valid through 2026-10-31", "renewed without end")
    assert opencode_remark_problems(planted)
    planted = remark.replace("refused on 2026-10-08", "accepted")
    assert opencode_remark_problems(planted)
    planted = remark.replace("lists Pi among its validated clients", "lists Claude Code as a validated client")
    assert opencode_remark_problems(planted)
    planted = remark.replace("accepted this residual risk on 2026-10-08", "saw no risk")
    assert opencode_remark_problems(planted)
    assert "lists Claude Code" not in remark and "native session header" not in remark


def _remark_problems(codex: str, glm: str) -> list[str]:
    """What criterion 3 requires of the two old reviewer remarks, as the problems found."""
    problems = []
    if "Used for drafting spec, design and plan" not in codex:
        problems.append("codex: the draft")
    if "the review (phase 6)" not in codex:
        problems.append("codex: the review")
    if "the spec review (phase 2a) moved to Opus 5.5" not in codex:
        problems.append("codex: 2a's move")
    if "the review loop (phase 4b) moved to `opencode-go`" not in codex:
        problems.append("codex: the loop's move")
    if "No review phase routes to it" not in glm:
        problems.append("glm: no review phase")
    if "the review loop (phase 4b) moved to `opencode-go`" not in glm:
        problems.append("glm: the loop's move")
    if not ("stage2.py explore" in glm and "stage2.py implement" in glm and "stage2.py draft" in glm):
        problems.append("glm: the work verbs")
    return problems


def test_no_old_reviewer_remark_claims_a_review_phase() -> None:
    """Criterion 3: each old entry says which phases, if any, still route to it."""
    codex = " ".join(_endpunkt("openai-codex")["bemerkung"].split())
    glm = " ".join(_endpunkt("glm-coding-plan")["bemerkung"].split())
    assert _remark_problems(codex, glm) == []
    planted = codex.replace("the review loop (phase 4b) moved to `opencode-go`", "runs every review as before")
    assert _remark_problems(planted, glm) == ["codex: the loop's move"]
    planted = codex.replace("Used for drafting spec, design and plan", "Used for every phase")
    assert _remark_problems(planted, glm) == ["codex: the draft"]
    planted = codex.replace("the spec review (phase 2a) moved to Opus 5.5", "keeps the spec review")
    assert _remark_problems(planted, glm) == ["codex: 2a's move"]
    planted = codex.replace(
        "and for the review (phase 6) of `bounded`, `feature` and `architectural` changes,",
        "and for nothing else,",
    )
    assert _remark_problems(planted, glm) == ["codex: the review"]
    planted = glm.replace("stage2.py draft", "stage2.py sketch")
    assert _remark_problems(codex, planted) == ["glm: the work verbs"]


def test_no_remark_routes_the_spec_review_to_codex() -> None:
    """Criterion 36: the ladder's remark sends 2a to Opus 5.5 and 6 to Codex — 2a no longer to Codex."""
    remark = " ".join(_endpunkt("opencode-go")["bemerkung"].split())
    assert "the spec review (phase 2a) runs on Opus 5.5" in remark
    assert "the review (phase 6) on Codex" in remark
    assert "spec review (phase 2a) stays with Codex" not in remark
    planted = remark.replace("runs on Opus 5.5", "stays with Codex", 1)
    assert "spec review (phase 2a) stays with Codex" in planted, "the planted fault is the old routing"


# ---------------------------------------------------------------------------
# The research swarm declaration (research-swarm, ADR 0020 draft)
# ---------------------------------------------------------------------------


def swarm_block_problems(geladen: dict) -> list[str]:
    """What the swarm's Opus roles and public data class require, as the problems found.

    The seats and the availability rule have their own fixtures below (Q-12, Q-14). Here: the topic author,
    the finder merge and the judge ride the paid endpoint (Opus on Claude Code), and the `public-web` data
    class the online roles carry is declared. A present but broken block refuses; an absent block leaves the
    swarm undeployable. The fixture tests carry the synthetic cases, so the function travels without reading
    this repository's declaration.
    """
    problems: list[str] = []
    block = geladen.get("research_swarm")
    if not isinstance(block, dict):
        return ["no research_swarm block"]
    if "public-web" not in set(geladen.get("datenklassen") or {}):
        problems.append("public-web data class not declared")
    paid = next(
        (
            e
            for e in geladen.get("endpunkte") or []
            if isinstance(e, dict) and e.get("name") == block.get("paid_endpoint")
        ),
        {},
    )
    if not paid:
        problems.append("paid endpoint not declared")
    for rolle in ("topic_author", "judge"):
        if block.get(rolle) not in set(paid.get("modelle") or []):
            problems.append(f"{rolle} not on the paid endpoint")
    if "finder_merge" in block and block["finder_merge"] not in set(paid.get("modelle") or []):
        problems.append("finder_merge not on the paid endpoint")
    for legacy in ("free_endpoint", "free_roster", "free_focuses", "topic6_free", "flash_endpoint", "flash_pair"):
        if legacy in block:
            problems.append(f"obsolete key {legacy} (Zen roster and fixed pair were removed)")
    return problems


def _swarm_fixture() -> dict:
    """A minimal, complete declaration of the Opus roles - no repository file needed."""
    return {
        "datenklassen": {"framework": {}, "public-web": {}},
        "endpunkte": [{"name": "paid-e", "darf_sehen": ["framework"], "modelle": ["opus"]}],
        "research_swarm": {"paid_endpoint": "paid-e", "topic_author": "opus", "judge": "opus"},
    }


def test_the_swarm_declaration_clears_every_role() -> None:
    assert swarm_block_problems(_swarm_fixture()) == []


@pytest.mark.parametrize(
    ("how", "expected"),
    [
        ("drop-block", "no research_swarm block"),
        ("author-unlisted", "topic_author not on the paid endpoint"),
        ("judge-unlisted", "judge not on the paid endpoint"),
        ("merge-unlisted", "finder_merge not on the paid endpoint"),
        ("paid-endpoint-gone", "paid endpoint not declared"),
        ("public-web-class-gone", "public-web data class not declared"),
        ("zen-roster-returns", "obsolete key free_roster"),
        ("fixed-pair-returns", "obsolete key flash_pair"),
    ],
)
def test_a_broken_swarm_declaration_is_named(how: str, expected: str) -> None:
    """Each broken declaration names its fault - the counterpart that goes red."""
    data = _swarm_fixture()
    block = data["research_swarm"]
    if how == "drop-block":
        del data["research_swarm"]
    elif how == "author-unlisted":
        block["topic_author"] = "stranger"
    elif how == "judge-unlisted":
        block["judge"] = "stranger"
    elif how == "merge-unlisted":
        block["finder_merge"] = "stranger"
    elif how == "paid-endpoint-gone":
        block["paid_endpoint"] = "nowhere"
    elif how == "public-web-class-gone":
        del data["datenklassen"]["public-web"]
    elif how == "zen-roster-returns":
        block["free_roster"] = ["longcat"]
    elif how == "fixed-pair-returns":
        block["flash_pair"] = ["d-flash", "m-flash"]
    found = swarm_block_problems(data)
    assert any(expected in p for p in found), (how, found)


def test_the_declaration_carries_the_swarm_block() -> None:
    """The real declaration must clear the swarm; the kit's empty stub skips."""
    geladen = _erklaerung()
    if not geladen.get("research_swarm"):
        pytest.skip("no research_swarm block in this declaration (the kit's stub is empty)")
    assert swarm_block_problems(geladen) == []


# ---------------------------------------------------------------------------
# Research seats and the availability rule (research-swarm, Q-12 and Q-14)
# ---------------------------------------------------------------------------


def _seat_fixture() -> dict:
    """A complete seat declaration: three repository and three online seats, one preferred model each."""
    go = {"name": "opencode-go", "darf_sehen": ["framework"], "residenz": "anbieter-erklaert"}
    go["modelle"] = ["d-flash", "m-flash"]
    go["modelle_terms"] = {"q-flash": {"gelesen": "2026-10-17", "anfragen_5h": 5400}}
    claude = {"name": "claude-code-plan", "darf_sehen": ["framework"], "residenz": "anbieter-erklaert"}
    claude["modelle"] = ["haiku", "opus"]
    return {
        "datenklassen": {"framework": {}, "public-web": {}},
        "endpunkte": [go, claude],
        "research_swarm": {
            "repository_seats": [
                {"endpoint": "opencode-go", "model": "d-flash"},
                {"endpoint": "opencode-go", "model": "m-flash"},
                {"endpoint": "claude-code-plan", "model": "haiku"},
            ],
            "online_seats": [
                {"endpoint": "opencode-go", "model": "d-flash"},
                {"endpoint": "opencode-go", "model": "m-flash"},
                {"endpoint": "opencode-go", "model": "q-flash"},
            ],
            "availability_preflight": {
                "max_age_seconds": 900,
                "exclude_until": [],
                "measured_wire_apis": ["openai-completions"],
            },
        },
    }


SEAT_FAULTS = {
    "no-preferred-model": lambda d: d["research_swarm"]["repository_seats"].pop(),
    "second-model": lambda d: d["research_swarm"]["online_seats"][0].update(model=["d-flash", "m-flash"]),
    "fallback-list": lambda d: d["research_swarm"]["repository_seats"][0].update(fallback=["m-flash"]),
    "undeclared": lambda d: d["research_swarm"]["repository_seats"][0].update(model="ghost"),
    "free-preferred": lambda d: d["research_swarm"]["online_seats"][0].update(model="x-free"),
    "online-off-go": lambda d: d["research_swarm"]["online_seats"][0].update(
        endpoint="claude-code-plan", model="haiku"
    ),
    "repository-no-framework": lambda d: d["endpunkte"][0].update(darf_sehen=["public-web"]),
    "one-model-two-seats": lambda d: d["research_swarm"]["repository_seats"][1].update(model="d-flash"),
    "age-bool": lambda d: d["research_swarm"]["availability_preflight"].update(max_age_seconds=True),
    "age-string": lambda d: d["research_swarm"]["availability_preflight"].update(max_age_seconds="900"),
    "age-range": lambda d: d["research_swarm"]["availability_preflight"].update(max_age_seconds=3601),
    "wire-apis-empty": lambda d: d["research_swarm"]["availability_preflight"].update(measured_wire_apis=[]),
    "wire-apis-text": lambda d: d["research_swarm"]["availability_preflight"].update(
        measured_wire_apis="openai-completions"
    ),
    "exclusion-date": lambda d: d["research_swarm"]["availability_preflight"].update(
        exclude_until=[{"model_prefix": "x", "until": "soon", "reason": "r"}]
    ),
    "exclusion-no-zone": lambda d: d["research_swarm"]["availability_preflight"].update(
        exclude_until=[{"model_prefix": "x", "until": "2026-10-21T20:34:00", "reason": "r"}]
    ),
    "unknown-rule-key": lambda d: d["research_swarm"]["availability_preflight"].update(flash_size=3),
    "rule-missing": lambda d: d["research_swarm"].pop("availability_preflight"),
}


def test_seat_candidate_lists_and_availability_rule_are_validated() -> None:
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    stage2_swarm = pytest.importorskip("stage2_swarm", reason="the runner is not part of this repository")

    assert stage2_swarm.seat_problems(_seat_fixture()) == []
    for name, fault in SEAT_FAULTS.items():
        data = _seat_fixture()
        fault(data)
        assert stage2_swarm.seat_problems(data), f"{name}: the fault passed declaration validation"
    # A terms record alone declares a research model; the review ladder `modelle` is untouched.
    data = _seat_fixture()
    assert "q-flash" not in data["endpunkte"][0]["modelle"]
    assert not any("q-flash" in problem for problem in stage2_swarm.seat_problems(data))


def test_the_repository_declaration_carries_six_seats_and_the_rule() -> None:
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    stage2_swarm = pytest.importorskip("stage2_swarm", reason="the runner is not part of this repository")

    geladen = yaml.safe_load(ENDPUNKTE.read_text(encoding="utf-8"))
    if not geladen.get("research_swarm"):
        pytest.skip("no research_swarm block in this declaration (the kit's stub is empty)")
    block = geladen["research_swarm"]
    # Q-18: the Go seats are open and filled per run on the maintainer's choice; only the Haiku seat is pinned.
    assert block["repository_seats"] == [
        {"endpoint": "opencode-go"},
        {"endpoint": "opencode-go"},
        {"endpoint": "claude-code-plan", "model": "claude-haiku-5-5"},
    ]
    assert block["online_seats"] == [{"endpoint": "opencode-go"}] * 3
    rule = block["availability_preflight"]
    assert rule["max_age_seconds"] == 900 and rule["measured_wire_apis"] == ["openai-completions"]
    assert block["online_free"] == {"provider": "opencode-go", "suffix": "-free", "include": [], "exclude": []}
    # A model's data-terms record belongs to the review swarm's declaration (#157); until that merges,
    # only "not declared" may remain open here, never a shape or permission fault.
    open_problems = [p for p in stage2_swarm.seat_problems(geladen) if "is not declared" not in p]
    assert open_problems == []
