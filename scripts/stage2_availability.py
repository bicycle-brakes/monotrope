"""Prepare reachable models before a swarm run; stage2 owns every foreign-model call.

One module for both swarms (research-swarm spec, criterion 50). The
swarm-independent parts are shared functions: rule validation
(`rule_problem`), timed-exclusion matching (`excluded_reason`), the tool-free
probes (`probe_go`, `probe_claude`) and receipt sealing, verification and
writing (`seal`, `verify`, `write_receipt`). The data-terms and cost helpers
(`terms_problem`, `request_value`, `ordered_models`) belong to the runner,
`scripts/stage2.py`, which both swarms reach through the `runner` argument.

Two entry-point pairs sit beside the shared part. The review loop's
`prepare` and `consume` (pull request #157, ADR 0021) probe the free swarm,
the Flash swarm and the paid ladder. The research swarm's `prepare_research`
and `consume_research` select six seats; selection (the substitute pool, the
double-fill rule) is research-only, because the review ladder has no seats.

The separate preparation and consumption steps give the orchestrator a chance
to report the selection in the main conversation before any call is launched.
The receipt is external state, never an artifact a model can edit.
"""

from __future__ import annotations

import contextlib
import copy
import datetime as dt
import fcntl
import functools
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
from collections import OrderedDict
from pathlib import Path
from uuid import uuid4

import leakcheck
import stage2_go
import stage2_research_map
import stage2_swarm
import yaml

GO = "opencode-go"
PROBE_TEXT = "Availability probe only. Reply with OK. Do not review code or request tools."
PROBE_SECONDS = 60
CATALOG_SECONDS = 70
STATE_LABELS = {
    "selected": "selected",
    "skipped": "skipped",
    "excluded": "excluded",
    "unreachable": "unreachable",
    "not-probed": "not probed",
}

# A probe's first limit, and the one longer retry a timed-out probe gets (R-7 of the review-swarm review).
PROBE_SECONDS = 60
PROBE_RETRY_SECONDS = 180
# A free model's probe carries a real-size prompt (bead k9rw), so it gets twice the small probe's limits.
FREE_PROBE_SECONDS = 120
FREE_PROBE_RETRY_SECONDS = 360


def now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


# ---------------------------------------------------------------------------
# Intelligence: the Artificial Analysis Intelligence Index, read live at every research preparation (Q-18)
# ---------------------------------------------------------------------------

INTELLIGENCE_URL = "https://artificialanalysis.ai/api/v2/data/llms/models"
INTELLIGENCE_SOURCE = "Artificial Analysis Intelligence Index, https://artificialanalysis.ai/"
INTELLIGENCE_KEY_ENV = "ARTIFICIAL_ANALYSIS_API_KEY"
INTELLIGENCE_SECONDS = 20


def _fetch_intelligence(key: str) -> object:
    """One GET of the public model list; nothing from the repository is sent. Raises OSError or ValueError."""
    import urllib.request

    request = urllib.request.Request(INTELLIGENCE_URL, headers={"x-api-key": key, "accept": "application/json"})
    with urllib.request.urlopen(request, timeout=INTELLIGENCE_SECONDS) as response:  # noqa: S310 - fixed https URL
        return json.loads(response.read().decode("utf-8"))


INTELLIGENCE_FETCH = _fetch_intelligence  # tests replace it; the runner never reads a cached copy


def _normal(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.split("(")[0].lower())


def read_intelligence(models: list[str], slugs: dict[str, str]) -> dict:
    """The index per model id, or a reading marked not read with its reason; it never stops a preparation.

    A model matches an entry by its declared slug in `intelligence_slugs`, else by its id against the
    entry's slug or name with case, punctuation and a parenthesised effort label ignored. Several matching
    entries (one per reasoning effort) give the highest index.
    """
    reading: dict = {"source": INTELLIGENCE_SOURCE, "read_at": None, "status": "", "scores": dict.fromkeys(models)}
    key = os.environ.get(INTELLIGENCE_KEY_ENV, "").strip()
    if not key:
        reading["status"] = f"not read: {INTELLIGENCE_KEY_ENV} is not set"
        return reading
    try:
        document = INTELLIGENCE_FETCH(key)
        entries = document["data"] if isinstance(document, dict) else None
        if not isinstance(entries, list):
            raise ValueError("the response has no data list")
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("evaluations"), dict):
                raise ValueError("an intelligence entry has malformed evaluations")
        reading["read_at"] = now().isoformat(timespec="seconds")
        reasons = {}
        for model in models:
            wanted = slugs.get(model)
            best = None
            for entry in entries:
                score = entry["evaluations"].get("artificial_analysis_intelligence_index")
                if not isinstance(score, int | float) or isinstance(score, bool):
                    continue
                if wanted is not None:
                    hit = entry.get("slug") == wanted
                else:
                    hit = _normal(model) in {_normal(str(entry.get("slug", ""))), _normal(str(entry.get("name", "")))}
                if hit and (best is None or score > best):
                    best = score
            reading["scores"][model] = best
            if best is None:
                reasons[model] = "no matching index entry with a numeric score" + (
                    f" for configured slug {wanted}" if wanted is not None else ""
                )
        reading["reasons"] = reasons
        reading["status"] = (
            "read"
            if any(value is not None for value in reading["scores"].values())
            else ("not read: no matching index entry with a numeric score")
        )
    except Exception as error:  # Optional intelligence must never prevent a selection receipt.
        from stage2 import scrub

        reading["scores"] = dict.fromkeys(models)
        reading["status"] = "not read: " + scrub(str(error).replace(key, "[key]"), key)[:200]
    return reading


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Shared: the availability rule, timed exclusions, receipts
# ---------------------------------------------------------------------------


def _exclusion_problem(item: object) -> bool:
    try:
        until = dt.datetime.fromisoformat(item["until"])  # type: ignore[index]
        return not (
            isinstance(item["model_prefix"], str)  # type: ignore[index]
            and bool(item["model_prefix"].strip())  # type: ignore[index]
            and isinstance(item["reason"], str)  # type: ignore[index]
            and bool(item["reason"].strip())  # type: ignore[index]
            and until.tzinfo is not None
        )
    except (KeyError, TypeError, ValueError):
        return True


def rule_problem(value: object, *, flash_size: bool = False, wire_apis: bool = False) -> list[str]:
    """The problems of an `availability_preflight` rule; the review swarm's fields plus the research ones.

    `flash_size` (1..3) belongs to the review swarm, `measured_wire_apis` to the research swarm. An absent
    `exclude_until` is an empty list; anything else unknown is a fault.
    """
    if not isinstance(value, dict):
        return ["availability_preflight must be a mapping"]
    allowed = {"max_age_seconds", "exclude_until"}
    allowed |= {"flash_size"} if flash_size else set()
    allowed |= {"measured_wire_apis"} if wire_apis else set()
    problems = [f"availability_preflight has an unknown key {key!r}" for key in value if key not in allowed]
    age = value.get("max_age_seconds")
    if type(age) is not int or not 1 <= age <= 3600:
        problems.append("availability_preflight needs max_age_seconds as an integer from 1 to 3600")
    if flash_size:
        size = value.get("flash_size")
        if type(size) is not int or not 1 <= size <= 3:
            problems.append("availability_preflight needs flash_size as an integer from 1 to 3")
    exclusions = value.get("exclude_until", [])
    if not isinstance(exclusions, list) or any(_exclusion_problem(item) for item in exclusions):
        problems.append("availability_preflight has an invalid timed exclusion")
    if wire_apis:
        apis = value.get("measured_wire_apis")
        if (
            not isinstance(apis, list)
            or not apis
            or any(not isinstance(item, str) or not item.strip() for item in apis)
            or len(set(apis)) != len(apis)
        ):
            problems.append("availability_preflight needs measured_wire_apis as a unique, nonempty list of names")
    return problems


def excluded_reason(rule: dict, model: str) -> str | None:
    """The reason text while a dated exclusion covers the model, matched by prefix on the id or its last segment."""
    for item in rule.get("exclude_until", []):
        prefix = item["model_prefix"].lower()
        matches = model.lower().startswith(prefix) or model.rsplit("/", 1)[-1].lower().startswith(prefix)
        if matches and now() < dt.datetime.fromisoformat(item["until"]):
            return f"unavailable until {item['until']}: {item['reason']}"
    return None


def seal(receipt: dict) -> str:
    """The report id: SHA-256 over the receipt's canonical JSON, without the id itself."""
    content = {key: value for key, value in receipt.items() if key != "report_id"}
    return digest(json.dumps(content, sort_keys=True))


def verify(receipt: dict, token: str | None) -> bool:
    """Whether the receipt's id is the recomputed one and equals the id the caller passed."""
    return receipt.get("report_id") == seal(receipt) == token


@contextlib.contextmanager
def receipt_lock(path: Path):
    """Serialize receipt publication and the final identity check/removal across processes."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor = os.open(path.with_suffix(".lock"), os.O_RDWR | os.O_CREAT, 0o600)
    with os.fdopen(descriptor, "a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def write_receipt(path: Path, receipt: dict) -> None:
    """Atomic, owner-only: a crash leaves the whole receipt or none."""
    with receipt_lock(path):
        temporary = path.with_suffix(".tmp")
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(receipt, sort_keys=True))
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)


# ---------------------------------------------------------------------------
# Shared: the tool-free probes
# ---------------------------------------------------------------------------


def _model_listed(entry: dict, model: str) -> bool:
    terms = entry.get("modelle_terms")
    return model in (entry.get("modelle") or []) or (isinstance(terms, dict) and model in terms)


def research_declaration_problem(root: Path, endpoint: str, model: str, data_class: str = "framework") -> str | None:
    """Why the declaration does not clear this model for a research call, or None.

    A model is listed in `modelle` or - for research only - by a `modelle_terms` record, so a record alone
    admits it without touching the review ladder. Exclusions bind the requested data class; the endpoint
    must name a residency.
    """
    data = read_declaration(root)
    if isinstance(data, str):
        return data
    excluded = stage2_swarm.exclusion_problem(data, model, data_class)
    if excluded:
        return excluded  # No probe starts for a model excluded from the requested data class.
    found = _endpoint(data, endpoint)
    if found is None:
        return f"model-endpoints.yaml declares no endpoint {endpoint}"
    if not _model_listed(found, model):
        return f"the endpoint {endpoint} does not declare the model {model}"
    residency = found.get("residenz")
    if not isinstance(residency, str) or not residency.strip() or residency == "nicht-erklaert":
        return f"the endpoint {endpoint} states no data residency"
    return None


def research_terms_problem(runner, root: Path, endpoint: str, model: str) -> str | None:
    """Re-read paid Go terms at the call boundary, independently of saved research selection."""
    if endpoint != GO:
        return None
    data = read_declaration(root)
    if isinstance(data, str):
        return data
    found = _endpoint(data, endpoint)
    if found is None:
        return f"model-endpoints.yaml declares no endpoint {endpoint}"
    return runner.terms_problem(found, model)


def research_probe_problem(runner, root: Path, endpoint: str, model: str, data_class: str = "framework") -> str | None:
    """Keep research-only declarations and paid terms binding on each probe, including retries."""
    return research_declaration_problem(root, endpoint, model, data_class) or research_terms_problem(
        runner, root, endpoint, model
    )


def _checked_probe(
    runner,
    root: Path,
    change: str,
    endpoint: str,
    model: str,
    audit: list[str],
    admission=None,
    verb: str = "prepare-explore",
    text: str = PROBE_TEXT,
) -> None:
    """The declaration, the exact-prompt leak check and the audit line - for this one probe, immediately before it.

    `admission` (root, model -> problem or None) replaces the research declaration check for the review
    swarm's free class (ADR 0021, decision 3); the leak check stays mandatory either way.
    """
    problem = admission(root, model) if admission is not None else research_probe_problem(runner, root, endpoint, model)
    if problem:
        raise runner.Refused(problem)
    result = leakcheck.check(change, leakcheck.default_denylist(), root, [("prompt", text)])
    print(result.verdict.render())
    if result.verdict.exit_code() != 0:
        raise runner.Refused("the leak check is not clean; the probe does not start.")
    # Re-read admission after the scan, which can cross the terms' UTC cutoff.
    # Do not record a call or dispatch a probe on yesterday's admission.
    problem = admission(root, model) if admission is not None else research_probe_problem(runner, root, endpoint, model)
    if problem:
        raise runner.Refused(problem)
    audit.append(
        f"{verb} · endpoint {endpoint} · model {model} · leak check clean over "
        f"{result.files} files, {result.commits} commits, {result.rules} rules."
    )


def _failed(runner, program: str, done, reason: str, key: str | None) -> object:
    tail = " / ".join(line.strip() for line in (done.stderr or "").splitlines()[-3:] if line.strip())
    detail = f": {runner.scrub(tail, key)}" if tail else ""
    return runner.CallFailed(f"{program} call failed: {reason}{detail}")


# The fields of a measured catalog row that reach a research launch's models.json (deep review RS-3-3). Pi merges
# others into the provider request (`samplingParams` into the body, so a row could name another model than the
# one checked; `headers`, `compat`), and the selection checks none of them; they are dropped and named.
OVERLAY_FIELDS = ("id", "name", "api", "baseUrl", "reasoning", "input", "contextWindow", "maxTokens", "cost")
# A Go row's absent `baseUrl` is filled from the one address record's default for its wire api
# (`stage2_go`, go-access-point); an unmapped api has no default and the row is refused, so Pi never
# fills in a shipped definition's other path (deep review RS-3-7).
# Pi's stderr when it could not use its models.json, or fell back to an unconfigured model (deep review RS-3-1).
PI_CONFIG_ERRORS = (
    "Failed to load models.json",
    "Failed to parse models.json",
    "Invalid models.json schema",
    "not found for provider",
)


class OverlayError(ValueError):
    """A measured row Pi's models.json schema would reject: the launch fails closed, never with Pi's defaults."""


def _number(value: object, *, positive: bool = False) -> bool:
    return (
        type(value) in (int, float)
        and value == value  # not NaN
        and value not in (float("inf"), float("-inf"))
        and (not positive or value > 0)
    )


def pi_row_problem(row: dict) -> str | None:
    """The first field of ``row`` Pi 1.2.0's models.json schema (ModelDefinitionSchema) refuses, or None.

    Pi validates the whole file and drops every row when one fails, so a selected model would silently resolve
    to Pi's shipped definition or a custom id at Pi's default endpoint (deep review RS-3-1).
    """
    if not isinstance(row.get("id"), str) or not row["id"]:
        return "id"
    for name in ("name", "api", "baseUrl"):
        if name in row and (not isinstance(row[name], str) or not row[name]):
            return name
    if "reasoning" in row and type(row["reasoning"]) is not bool:
        return "reasoning"
    if "input" in row and (
        not isinstance(row["input"], list) or any(item not in ("text", "image") for item in row["input"])
    ):
        return "input"
    for name in ("contextWindow", "maxTokens"):
        if name in row and not _number(row[name], positive=True):
            return name
    if "cost" in row:
        cost = row["cost"]
        rates = ("input", "output", "cacheRead", "cacheWrite")
        if not isinstance(cost, dict) or any(not _number(cost.get(rate)) for rate in rates):
            return "cost"
        tiers = cost.get("tiers")
        if tiers is not None and (
            not isinstance(tiers, list)
            or any(
                not isinstance(tier, dict) or any(not _number(tier.get(k)) for k in ("inputTokensAbove", *rates))
                for tier in tiers
            )
        ):
            return "cost"
    return None


def go_policy(runner, root: Path):
    """The one address policy for this root, as a refusal when its record is unusable."""
    try:
        return stage2_go.load_address_policy(root)
    except stage2_go.RecordUnusable as error:
        raise runner.Refused(f"the Go address record is unusable: {error}") from None


def install_measured_models(
    runner, agent: Path, store: dict | None, *, model: str | None = None, address: stage2_go.AddressPolicy | None = None
) -> list[str]:
    """Give Pi's fresh agent directory the measured catalog: the retrieval evidence and its model definitions.

    ``models-store.json`` keeps the whole store as retrieval evidence. With ``model`` (every research launch and
    probe) ``models.json`` carries only that model's row (deep review RS-3-1: one malformed row elsewhere in the
    catalog made Pi reject the file), restricted to ``OVERLAY_FIELDS``, with the recorded default base filled in
    when it has none, and checked against Pi's schema first: a row Pi would refuse raises ``OverlayError``.
    Returns one note per row whose other fields were dropped or whose base was filled or moved, for the caller's
    audit. Without ``model`` the whole store goes through ``runner.activate_overlay`` under the address policy.
    Go rows are assessed before installation as well as at selection and dispatch; a refused row raises.
    """
    if not store:
        return []
    (agent / "models-store.json").write_text(json.dumps(store), encoding="utf-8")
    if model is None:
        if address is None:
            raise runner.Refused("activating the whole measured store needs the Go address record; none was passed.")
        runner.activate_overlay(agent, store, address)
        return []
    providers: dict[str, dict] = {}
    dropped: list[str] = []
    for provider, entry in store.items():
        definitions = entry.get("models", []) if isinstance(entry, dict) else []
        for definition in definitions if isinstance(definitions, list) else []:
            if not isinstance(definition, dict) or definition.get("id") != model:
                continue
            row = {name: definition[name] for name in OVERLAY_FIELDS if name in definition}
            if provider == GO and "baseUrl" not in row:
                filled = address.default_base(row.get("api")) if address is not None else None
                if filled is None:
                    raise OverlayError(
                        f"the measured row of {provider}/{model} has no base and its wire api "
                        "has no recorded default; Pi would fill one in"
                    )
                row["baseUrl"] = filled
                dropped.append(f"{provider}/{model}: base filled from the record's default for {row.get('api')}")
            if provider == GO:
                if address is None:
                    raise OverlayError(f"installing {provider}/{model} needs the Go address record")
                verdict = stage2_go.assess(address, model, row)
                if not verdict.admitted:
                    raise OverlayError(verdict.problem)
                if verdict.notice:
                    dropped.append(f"address notice · {verdict.notice}")
            # `provider` naming the same provider is redundant for Pi, and dropping it changes nothing.
            extra = sorted(
                str(name)
                for name in definition
                if name not in OVERLAY_FIELDS and not (name == "provider" and definition[name] == provider)
            )
            if extra:
                dropped.append(f"{provider}/{model}: dropped catalog field(s) {', '.join(extra)}")
            problem = pi_row_problem(row)
            if problem:
                raise OverlayError(f"the measured row of {provider}/{model} breaks Pi's models.json schema ({problem})")
            providers.setdefault(provider, {"models": []})["models"].append(row)
    (agent / "models.json").write_text(json.dumps({"providers": providers}), encoding="utf-8")
    return dropped


def pi_config_error(stderr: str | None) -> str | None:
    """Pi's own line saying it could not use its models.json or the configured model, or None."""
    for line in (stderr or "").splitlines():
        if any(marker in line for marker in PI_CONFIG_ERRORS):
            return line.strip()
    return None


def probe_go(
    runner,
    root: Path,
    change: str,
    model: str,
    key: str,
    audit: list[str],
    store: dict | None = None,
    *,
    admission=None,
    verb: str = "prepare-explore",
    timeout_seconds: int = PROBE_SECONDS,
    text: str = PROBE_TEXT,
) -> None:
    """One tool-free Go probe: pinned Pi wrapper, no tools, scratch directories, one text, one limit.

    `text` is the small static probe, or a free model's real-size one; the leak check sees the same text.

    The probe assesses its destination against the one address record before
    anything is installed or sent: a refused destination never probes, and a
    same-host path move is named in the audit. The destination comes only from
    the refreshed definition that is installed for this probe; callers cannot
    vouch for a separate definition. Dispatch re-checks it against current policy.
    The limit is a parameter, not a constant: a probe that only ran out of
    time is tried once more with a longer one (R-7 of the review-swarm
    review), and the longer try must use the same probe.
    """
    _checked_probe(runner, root, change, GO, model, audit, admission, verb, text)
    policy = go_policy(runner, root)
    row = stage2_go.definition_of(store or {}, GO, model)
    if row is None:
        raise runner.Refused(f"the probe's model {model} has no refreshed definition; no probe starts.")
    verdict = stage2_go.assess(policy, model, row)
    if not verdict.admitted:
        # One model's refused destination, not the operation's stop: the probe
        # loop and the research selection name it and carry on (criterion 5).
        raise stage2_go.DestinationRefused(verdict.problem)
    if verdict.notice:
        audit.append(f"address notice · {verdict.notice}")
        print(f"Address notice: {verdict.notice}")
    destination = verdict.definition
    with tempfile.TemporaryDirectory(prefix="stage2-probe-") as tmp:
        scratch = Path(tmp)
        agent = scratch / "agent"
        agent.mkdir()
        (agent / "settings.json").write_text(json.dumps({"retry": {"enabled": False}}), encoding="utf-8")
        # Research preparation probes what its launches will use: one checked row (deep review RS-3-1). The review
        # loop's probes keep the whole overlay until that loop's own repair changes `activate_overlay`.
        try:
            dropped = install_measured_models(
                runner,
                agent,
                store,
                model=model if verb == "prepare-explore" else None,
                address=policy,
            )
        except OverlayError as error:
            raise runner.CallFailed(f"pi call failed: {error}") from None
        audit.extend(dropped)
        home = scratch / "home"
        home.mkdir()
        prompt_file = scratch / "probe-prompt.md"
        prompt_file.write_text(text, encoding="utf-8")
        command = [
            str(runner.PI_WRAPPER),
            "--print",
            "--no-session",
            "--no-approve",
            "--no-extensions",
            "--no-mcp",
            "--no-skills",
            "--no-context-files",
            "--no-prompt-templates",
            "--no-themes",
            "--offline",
            "--no-tools",
            "--thinking",
            "max",
            "--model",
            f"{GO}/{model}",
            "--append-system-prompt",
            str(prompt_file),
            "Follow the appended availability instructions.",
        ]
        env = runner.foreign_env({"HOME": str(home), "PI_CODING_AGENT_DIR": str(agent), "OPENCODE_API_KEY": key})
        done = runner.dispatch_go(
            root,
            model,
            runner.launch,
            command,
            scratch,
            env,
            key,
            admission=admission,
            destination=destination,
            configuration=agent / "models.json",
            timeout=timeout_seconds,
            limit=f"the probe limit of {timeout_seconds} seconds",
        )
        if done.returncode != 0:
            raise _failed(runner, "pi", done, f"exit {done.returncode}", key)
        refused = pi_config_error(done.stderr)
        if refused:
            raise _failed(runner, "pi", done, f"Pi did not use the measured model ({refused})", key)
        if not runner.scrub(done.stdout or "", key).strip():
            raise _failed(runner, "pi", done, "the answer is empty", key)


def probe_claude(runner, root: Path, change: str, model: str, audit: list[str]) -> None:
    """One tool-free probe through the official Claude Code client: no tools, restricted, no session."""
    _checked_probe(runner, root, change, "claude-code-plan", model, audit)
    command = [
        "claude",
        "-p",
        PROBE_TEXT,
        "--model",
        model,
        "--tools",
        "",
        "--restricted",
        "--safe-mode",
        "--strict-mcp-config",
        "--permission-prompts",
        "none",
        "--no-session-persistence",
        "--output-format",
        "text",
    ]
    with tempfile.TemporaryDirectory(prefix="stage2-probe-") as tmp:
        done = runner.launch(
            command,
            Path(tmp),
            runner.foreign_env({}),
            None,
            timeout=PROBE_SECONDS,
            limit=f"the probe limit of {PROBE_SECONDS} seconds",
        )
    if done.returncode != 0:
        raise _failed(runner, "claude", done, f"exit {done.returncode}", None)
    if not (done.stdout or "").strip():
        raise _failed(runner, "claude", done, "the answer is empty", None)


# ---------------------------------------------------------------------------
# Research: the declaration, class and neighbours
# ---------------------------------------------------------------------------


# The shared declaration reader's parse cache: process-local and bounded, keyed
# by the decoded contents alone - never by path, size or modification time.
# Only a successful mapping parse enters it; a failed read, decode or parse is
# never cached, so the next call reads the file again (bead
# coding-harness-dca4). The parse is always PyYAML's pure `SafeLoader`, as
# before the cache: libyaml's C loader accepts and refuses other documents
# (a tab before a comment, an escaped surrogate pair), and it saved nothing
# measurable once the cache was in place (phase-6 rows F6-1 and F6-3).
_DECLARATION_CACHE_SIZE = 8
_DECLARATION_CACHE: OrderedDict[str, dict] = OrderedDict()
_DECLARATION_CACHE_LOCK = threading.Lock()


def read_declaration(root: Path) -> dict | str:
    """The parsed `model-endpoints.yaml`, or the problem text when it cannot be read.

    Every call reads the file's current bytes and decodes them, so an edit at an
    unchanged size and modification time is still seen. A successful mapping
    parse is reused for identical contents; every caller, including
    the first, receives its own deep copy, so one caller's edits never reach
    another read or thread.
    """
    try:
        text = (root / "model-endpoints.yaml").read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return "model-endpoints.yaml cannot be read"
    key = text
    with _DECLARATION_CACHE_LOCK:
        cached = _DECLARATION_CACHE.get(key)
        if cached is not None:
            _DECLARATION_CACHE.move_to_end(key)
    if cached is not None:
        return copy.deepcopy(cached)
    try:
        data = yaml.load(text, Loader=yaml.SafeLoader) or {}
    except yaml.YAMLError:
        return "model-endpoints.yaml cannot be read"
    if not isinstance(data, dict):
        return "model-endpoints.yaml cannot be read"
    with _DECLARATION_CACHE_LOCK:
        _DECLARATION_CACHE[key] = data
        while len(_DECLARATION_CACHE) > _DECLARATION_CACHE_SIZE:
            _DECLARATION_CACHE.popitem(last=False)
    return copy.deepcopy(data)


def _endpoint(data: dict, name: str) -> dict | None:
    return next((e for e in data.get("endpunkte") or [] if isinstance(e, dict) and e.get("name") == name), None)


def research_settings(root: Path, runner) -> tuple[dict, dict]:
    """The validated declaration and the research rule, or the refusal (exit 2) naming the fault."""
    data = read_declaration(root)
    if isinstance(data, str):
        raise runner.Refused(data)
    problems = stage2_swarm.seat_problems(data)
    malformed = stage2_swarm.exclusion_problem(data, "")
    if malformed:
        problems.append(malformed)
    block = data.get("research_swarm")
    policy = block.get("online_free") if isinstance(block, dict) else None
    try:
        stage2_swarm.validate_research_free_policy(policy)
    except stage2_swarm.ResearchCatalogError as error:
        problems.append(f"online_free: {error}")
    if problems:
        raise runner.Refused("the research seat declaration is unusable: " + "; ".join(problems))
    return data, block["availability_preflight"]


def given_neighbours(root: Path, change: str, runner) -> list[str]:
    """The `neighbours:` header of research.md, validated against the tracked files; exit 2 when invalid."""
    path = root / "plans" / "changes" / change / "research.md"
    try:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"---\n(.*?)\n---", text, re.S)
        header = yaml.safe_load(match.group(1)) if match else None
        node = yaml.compose(match.group(1), Loader=yaml.SafeLoader) if match else None
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        raise runner.Refused(f"plans/changes/{change}/research.md cannot be read as a header.") from error
    if isinstance(node, yaml.MappingNode):
        keys = [key for key, _ in node.value if key.tag == "tag:yaml.org,2002:str" and key.value == "neighbours"]
        if len(keys) > 1:  # a later key would silently discard the earlier dependency (F-56)
            raise runner.Refused(
                f"plans/changes/{change}/research.md states neighbours more than once; "
                "repair the header to contain exactly one `neighbours:` declaration."
            )
    frozen = dict.fromkeys(stage2_swarm.tracked_paths(root), b"")
    try:
        return stage2_research_map.validate_given_neighbours(header, frozen, f"plans/changes/{change}/spec.md")
    except stage2_research_map.ResearchMapError as error:
        raise runner.Refused(str(error)) from error


def research_binding(root: Path, change: str, klass: str, neighbours: list[str]) -> dict:
    return {
        "root": str(root.resolve()),
        "change": change,
        "configuration": digest((root / "model-endpoints.yaml").read_text(encoding="utf-8")),
        "class": klass,
        "neighbours": list(neighbours),
    }


def research_receipt_path(change: str, runner, root: Path) -> Path:
    return runner.record_dir(change, root) / "research-availability.json"


def catalog_bridge(runner, _root: Path) -> dict:
    """The fresh Go catalog through the pinned-Pi helper: no model call, no credential, one shared deadline."""
    node = shutil.which("node")
    if node is None:
        raise runner.CallFailed("node is not installed; the Go catalog cannot be refreshed and no call starts.")
    helper = Path(__file__).resolve().with_name("stage2_research_catalog.mjs")
    with tempfile.TemporaryDirectory(prefix="stage2-catalog-") as tmp:
        env = runner.foreign_env({"HOME": tmp, "PI_CODING_AGENT_DIR": tmp})
        try:
            done = subprocess.run(
                [node, str(helper)],
                cwd=tmp,
                env=env,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                check=False,
                timeout=CATALOG_SECONDS,
            )
            return json.loads(done.stdout)
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            raise runner.CallFailed(f"the Go catalog refresh failed: {error}") from error


# ---------------------------------------------------------------------------
# Research: selection
# ---------------------------------------------------------------------------


class _ProbeAudit(list[str]):
    """Persist each scrubbed launch audit independently of selection receipt publication."""

    def __init__(self, directory: Path, runner, key) -> None:
        super().__init__()
        self.directory, self.runner, self.key = directory, runner, key

    def append(self, line: str) -> None:
        line = self.runner.scrub(line, self.key())
        try:
            write_receipt(
                self.directory / f"research-probe-{uuid4().hex}.json",
                {"checked_at": now().isoformat(timespec="seconds"), "audit": line},
            )
        except OSError as error:
            raise self.runner.Refused("the probe audit cannot be persisted; no further probe starts.") from error
        super().append(line)


class _Selection:
    """One preparation: model outcomes, the substitute pool and the lazy, unique probes."""

    def __init__(self, root, change, runner, data, rule, catalog) -> None:
        self.root, self.change, self.runner, self.rule = root, change, runner, rule
        self.data = data
        self.go = _endpoint(data, GO) or {}
        self.catalog = {item["id"]: item for item in catalog["models"]}
        self.models_store = catalog.get("models_store")
        self.key: str | None = None
        self.audit: list[str] = _ProbeAudit(runner.record_dir(change, root), runner, lambda: self.key)
        self.probed: dict[str, str | None] = {}
        self.models: dict[str, dict] = {}
        self.go_framework = "framework" in (self.go.get("darf_sehen") or [])
        ids = {
            *self.catalog,
            *(self.go.get("modelle_terms") or {}),
            *(
                seat["model"]
                for name in ("repository_seats", "online_seats")
                for seat in data["research_swarm"][name]
                if seat["endpoint"] == GO and "model" in seat
            ),
        }
        for model in sorted(ids):
            if model.endswith("-free"):
                continue
            self.models[f"{GO}/{model}"] = self._go_outcome(model)
        for name in ("repository_seats", "online_seats"):
            for seat in data["research_swarm"][name]:
                if seat["endpoint"] != GO:
                    self.models.setdefault(f"{seat['endpoint']}/{seat['model']}", self._claude_outcome(seat))
        self.pool = [
            {"model": model, "anfragen_5h": self.runner.request_value(self.go, model)}
            for model in self.runner.ordered_models(self.go, self._admitted_pool())
        ]

    def _admitted_pool(self) -> list[str]:
        return [
            key.split("/", 1)[1]
            for key, item in self.models.items()
            if key.startswith(f"{GO}/") and item.get("admitted") and item.get("tool_support") is None
        ]

    def _go_outcome(self, model: str) -> dict:
        problems = [stage2_swarm.exclusion_problem(self.data, model, klass) for klass in ("framework", "public-web")]
        excluded = next((problem for problem in problems if problem), None) if all(problems) else None
        if excluded:
            return {"state": "excluded", "reason": excluded}  # Denied in both research classes: never probed or seated.
        problem = self.runner.terms_problem(self.go, model)
        if problem:
            return {"state": "skipped", "reason": problem}
        if self.runner.request_value(self.go, model) is None:
            return {"state": "skipped", "reason": "no admitted cost value (anfragen_5h missing or not positive)"}
        found = self.catalog.get(model)
        reason = found["reason"] if found else "not-in-fresh-pi"
        if reason:
            raw = json.dumps(found["evidence"]["pi"], sort_keys=True) if found else "{}"
            return {"state": "skipped", "reason": f"{reason}; raw {raw}"}
        outcome = {
            "state": "not-probed",
            "reason": "",
            "admitted": True,
            "tool_support": found["tool_support"],
        }
        excluded = excluded_reason(self.rule, model)
        if excluded:
            outcome.update(state="excluded", reason=excluded)
        elif found["tool_support"]:
            outcome["reason"] = f"{found['tool_support']}: not in the substitute pool"
        return outcome

    def _claude_outcome(self, seat: dict) -> dict:
        excluded = stage2_swarm.exclusion_problem(self.data, seat["model"])
        if excluded:
            return {"state": "excluded", "reason": excluded}
        outcome = {"state": "not-probed", "reason": "", "admitted": True, "tool_support": "not-pool"}
        excluded = excluded_reason(self.rule, seat["model"])
        if excluded:
            outcome.update(state="excluded", reason=excluded)
        return outcome

    def usable(self, endpoint: str, model: str, data_class: str) -> bool:
        item = self.models.get(f"{endpoint}/{model}")
        return (
            bool(item)
            and item.get("admitted") is True
            and item["state"] != "excluded"
            and stage2_swarm.exclusion_problem(self.data, model, data_class) is None
        )

    def reachable(self, endpoint: str, model: str, data_class: str) -> bool:
        """Probe at most once per preparation; the result is shared across seats and trios."""
        key = f"{endpoint}/{model}"
        item = self.models[key]
        if key not in self.probed:
            try:
                if endpoint == GO:
                    if self.key is None:
                        self.key = self.runner.reviewer_key()
                    probe_go(
                        self.runner,
                        self.root,
                        self.change,
                        model,
                        self.key,
                        self.audit,
                        self.models_store,
                        admission=lambda root, ident: research_probe_problem(self.runner, root, GO, ident, data_class),
                    )
                else:
                    probe_claude(self.runner, self.root, self.change, model, self.audit)
            except self.runner.CallFailed as error:
                self.probed[key] = self.runner.scrub(str(error), self.key)
                item.update(state="unreachable", reason=self.probed[key])
            except stage2_go.DestinationRefused as error:
                # A refused destination is a named skip for this preparation, never a
                # seat: the model cannot return through filtering or substitution.
                self.probed[key] = str(error)
                item.update(state="unreachable", reason=str(error))
            else:
                self.probed[key] = None
                item.update(state="selected", reason="reachable")
        return self.probed[key] is None

    def fill(self, label: str, seats: list[dict]) -> list[dict | None]:
        data_class = "framework" if label == "repository" else "public-web"
        chosen: list[dict | None] = [None] * len(seats)
        taken: set[str] = set()
        for number, seat in enumerate(seats):
            if "model" not in seat:
                continue
            endpoint, model = seat["endpoint"], seat["model"]
            if self.usable(endpoint, model, data_class) and self.reachable(endpoint, model, data_class):
                mark = "maintainer's choice" if seat.get("chosen") else "preferred"
                chosen[number] = {"seat": number + 1, "endpoint": endpoint, "model": model, "mark": mark}
                taken.add(f"{endpoint}/{model}")
        for number in range(len(seats)):
            if chosen[number] is not None or seats[number].get("chosen"):
                continue  # a model the maintainer chose is never silently replaced
            if label == "repository" and not self.go_framework:
                continue
            for entry in self.pool:
                model = entry["model"]
                key = f"{GO}/{model}"
                if key in taken or not self.usable(GO, model, data_class):
                    continue
                if key in self.probed and self.probed[key] is not None:
                    continue
                if self.reachable(GO, model, data_class):
                    chosen[number] = {
                        "seat": number + 1,
                        "endpoint": GO,
                        "model": model,
                        "mark": "cheapest" if "model" not in seats[number] else f"substitute for {number + 1}",
                    }
                    taken.add(key)
                    break
        return chosen


# A public topic is one sentence of at most 20 words, authored at run time; the probe stands one in.
PROBE_TOPIC_SENTENCE = "Availability probe only, not a real research topic"
FREE_RESEARCH_TOPIC = 9  # the first topic a free model researches; its request shape is the probe's


def free_research_probe_text(root: Path) -> str:
    """A free research member's probe: its real online_free request (first free topic), asking for OK only."""
    import stage2_research_run  # imported here: that module imports this one

    request = stage2_research_run.online_topic_prompt(root, FREE_RESEARCH_TOPIC, PROBE_TOPIC_SENTENCE)
    instruction = "Availability probe only. Reply with OK. Do not research and do not request tools."
    return "\n\n".join([instruction, request, instruction])


def probe_free_research(selection: _Selection, selected: list[str]) -> tuple[list[str], dict[str, str]]:
    """Probe each free member with the real-size request; return the reachable ones and each failure's reason."""
    runner, root = selection.runner, selection.root
    data = read_declaration(root)
    text = free_research_probe_text(root)
    if selection.key is None:
        selection.key = runner.reviewer_key()
    reachable: list[str] = []
    failed: dict[str, str] = {}
    for model in selected:
        for limit in (FREE_PROBE_SECONDS, FREE_PROBE_RETRY_SECONDS):
            try:
                probe_go(
                    runner,
                    root,
                    selection.change,
                    model,
                    selection.key,
                    selection.audit,
                    selection.models_store,
                    admission=lambda _root, ident: (
                        data
                        if isinstance(data, str)
                        else stage2_swarm.invocation_problem(data, "online_free", GO, ident, selected_free=selected)
                    ),
                    timeout_seconds=limit,
                    text=text,
                )
            except runner.CallFailed as error:
                failure = runner.scrub(str(error), selection.key)
                failed[model] = failure
                if "stopped by" in failure:
                    continue  # only a stopped call is worth the longer try
                break
            except stage2_go.DestinationRefused as error:
                failed[model] = str(error)
                break  # a refused destination is not retried at any limit
            else:
                failed.pop(model, None)
                reachable.append(model)
                break
    return reachable, failed


def _free_text(values: list[str]) -> str:
    return ", ".join(values) or "none"


def capture_preparation_warnings(prepare):
    """Scope dispatch warning evidence to this preparation, shared by its receipt."""

    @functools.wraps(prepare)
    def wrapped(root, change, runner, *args, **kwargs):
        with runner.capture_terms_warnings():
            return prepare(root, change, runner, *args, **kwargs)

    return wrapped


def preparation_terms(runner, entry: dict) -> dict:
    """Both preparation paths announce and retain the same current warning evidence."""
    warnings = runner.terms_warnings(entry)
    for warning in warnings:
        print(f"Terms warning: {warning}")
    return {"terms_warnings": runner.retain_terms_warnings(warnings)}


def research_report(state: dict) -> str:
    lines = [f"Availability checked: {state['checked_at']}"]
    lines.extend(f"Terms warning: {warning}" for warning in state.get("availability", {}).get("terms_warnings", []))
    lines.extend(f"Address notice: {notice}" for notice in (state.get("catalog") or {}).get("address_notices") or [])
    for label in ("repository", "online"):
        for item in state["seats"][label]:
            if item is None:
                continue
            lines.append(f"{label} seat {item['seat']}: {item['endpoint']}/{item['model']} ({item['mark']})")
    for label, items in state["unfilled"].items():
        lines.extend(f"seat-unavailable: {label} seat {number}" for number in items)
    pool = ", ".join(f"{item['model']} ({item['anfragen_5h']:g})" for item in state["pool"]) or "empty"
    lines.append(f"Pool, cheapest first: {pool}")
    lines.extend(intelligence_lines(state))
    lines.append(f"Free selection: {_free_text(state['free']['selected'])}")
    lines.extend(f"Unavailable (free): {model}: {reason}" for model, reason in state["free"]["unavailable"].items())
    lines.append("Models:")
    for key, item in state["models"].items():
        detail = f" - {item['reason']}" if item.get("reason") else ""
        lines.append(f"  {key}: {STATE_LABELS[item['state']]}{detail}")
    if state["unread"]:
        lines.append(f"Unread (no data-terms record, never used): {_free_text(state['unread'])}")
    lines.append("Reachability is a point-in-time result, not a billing or research-quality measurement.")
    return "\n".join(lines)


def _score_text(value: object) -> str:
    return "not read" if value is None else f"{value:g}"


def intelligence_lines(state: dict) -> list[str]:
    """Cost against intelligence for every reachable candidate, and the recommendation with its reason (Q-18)."""
    reading = state.get("intelligence")
    if not reading:
        return []
    scores = reading["scores"]
    lines = [
        f"Intelligence: {reading['source']} - {reading['status']}"
        + (f", {reading['read_at']}" if reading["read_at"] else "")
    ]
    reachable = [key for key, item in state["models"].items() if item["state"] == "selected"]
    lines.append("Candidates (reachable; requests per 5 hours, more is cheaper; intelligence index):")
    cost = {item["model"]: item["anfragen_5h"] for item in state["pool"]}
    cost.update(state.get("request_costs", {}))
    for key in reachable:
        model = key.split("/", 1)[1]
        price = f"{cost[model]:g}" if model in cost else "subscription"
        score_text = _score_text(scores.get(model))
        if scores.get(model) is None:
            reason = reading.get("reasons", {}).get(model) or reading["status"].removeprefix("not read: ")
            score_text = f"not read: {reason}"
        lines.append(f"  {key}: requests {price}, intelligence {score_text}")
    lines.append(
        "Recommendation: the seats above - per trio the cheapest reachable admitted models"
        + ("" if reading["status"] == "read" else "; intelligence was not read, so cost alone decides")
        + "."
    )
    missing = [key.split("/", 1)[1] for key in reachable if scores.get(key.split("/", 1)[1]) is None]
    if missing:
        lines.append(
            "Recommendation caveat: intelligence was not weighed for "
            + ", ".join(missing)
            + "; cost alone decides for these candidates."
        )
    stronger = sorted(
        (
            (scores[item["model"]], item["model"])
            for item in state["pool"]
            if f"{GO}/{item['model']}" in reachable and scores.get(item["model"]) is not None
        ),
        reverse=True,
    )
    if stronger:
        score, model = stronger[0]
        lines.append(
            f"Strongest reachable pool model: {model} (index {score:g}); worth its cost for an architectural or "
            "unclear change."
        )
    return lines


def chosen_seats(seats: dict[str, list[dict]], choice: dict[str, list[str]] | None, runner) -> dict[str, list[dict]]:
    """The declared seats with the maintainer's Go models in place of the open or pinned Go seats, in order."""
    if not choice:
        return seats
    result = {}
    for label, trio in seats.items():
        models = choice.get(label)
        if models is None:
            result[label] = trio
            continue
        go_seats = [number for number, seat in enumerate(trio) if seat["endpoint"] == GO]
        if len(models) != len(go_seats) or len(set(models)) != len(models):
            raise runner.Refused(
                f"--seats {label} names {len(models)} models; the trio has {len(go_seats)} distinct Go seats."
            )
        updated = [dict(seat) for seat in trio]
        for number, model in zip(go_seats, models, strict=True):
            updated[number] = {"endpoint": GO, "model": model, "chosen": True}
        result[label] = updated
    unknown = set(choice) - set(seats)
    if unknown:
        raise runner.Refused(f"--seats knows the trios repository and online, not {', '.join(sorted(unknown))}.")
    return result


@capture_preparation_warnings
def prepare_research(
    root: Path, change: str, runner, klass: str | None = None, choice: dict[str, list[str]] | None = None
) -> None:
    """Admit, probe and select the six seats, report them, and seal a receipt - or stop with exit 1 or 2.

    `choice` is the maintainer's answer to the recommendation (`--seats`): those Go models fill the trio's
    Go seats, and one that is not admitted or not reachable stops the preparation instead of being replaced.
    Writes nothing in the worktree: the receipt and its audit lines live in the runner's state directory.
    """
    path = research_receipt_path(change, runner, root)
    # A failed preparation must never leave an earlier receipt usable.
    with receipt_lock(path):
        path.unlink(missing_ok=True)
    runner.folder_of(root, change)
    klass = runner.declared_class(root, change, klass)
    if klass not in runner.SWARM_CLASSES:
        raise runner.Refused(f"prepare-explore belongs to feature or architectural changes, not {klass}.")
    data, rule = research_settings(root, runner)
    terms_evidence = preparation_terms(runner, _endpoint(data, GO) or {})
    neighbours = given_neighbours(root, change, runner)
    runner.require_pi()
    block = data["research_swarm"]
    seats = chosen_seats({"repository": block["repository_seats"], "online": block["online_seats"]}, choice, runner)
    go_entry = _endpoint(data, GO) or {}
    declared = go_entry.get("modelle_terms")
    # Every declared Go model is classified against the fresh overlay, so each skip carries its own reason.
    preferred = sorted(
        {seat["model"] for trio in seats.values() for seat in trio if seat["endpoint"] == GO and "model" in seat}
        | {model for model in (declared if isinstance(declared, dict) else {}) if not str(model).endswith("-free")}
    )
    try:
        catalog = stage2_swarm.select_research_catalog(
            catalog_bridge(runner, root),
            block["online_free"],
            preferred,
            expected_version=runner.PI_VERSION,
            measured_wire_apis=rule["measured_wire_apis"],
            address=go_policy(runner, root),
        )
    except stage2_swarm.ResearchCatalogError as error:
        if error.exit_code == 2:
            raise runner.Refused(str(error)) from error
        raise runner.CallFailed(f"the Go catalog is unmeasured: {error}; no probe or research call starts.") from error
    selection = _Selection(root, change, runner, data, rule, catalog)
    chosen = {label: selection.fill(label, trio) for label, trio in seats.items()}
    free_selected = [m for m in catalog["selected"] if not stage2_swarm.exclusion_problem(data, m, "public-web")]
    # A free member stays optional: a failed probe only removes it, it never stops the preparation.
    free_reachable, free_failed = probe_free_research(selection, free_selected)
    terms = selection.go.get("modelle_terms")
    terms = terms if isinstance(terms, dict) else {}
    state = {
        "checked_at": now().isoformat(timespec="seconds"),
        "availability": terms_evidence,
        "catalog": {
            key: catalog[key]
            for key in (
                "pi_version",
                "selection_outcome",
                "capability_status",
                "capability_reason",
                "measured_wire_apis",
                "address_notices",
                "sources",
                "candidates",
                "models",
                "models_store",
            )
        },
        "free": {
            "selected": free_reachable,
            "unavailable": free_failed,
            "excluded": [m for m in catalog["selected"] if stage2_swarm.exclusion_problem(data, m, "public-web")],
            "policy": catalog["policy"],
        },
        "seats": chosen,
        "unfilled": {
            label: [number + 1 for number, item in enumerate(items) if item is None] for label, items in chosen.items()
        },
        "pool": selection.pool,
        "request_costs": {
            model: runner.request_value(selection.go, model)
            for model in terms
            if runner.request_value(selection.go, model) is not None
        },
        "models": {
            key: {name: value for name, value in item.items() if name in {"state", "reason"}}
            for key, item in selection.models.items()
        },
        "unread": sorted(
            item["id"] for item in catalog["models"] if not item["id"].endswith("-free") and item["id"] not in terms
        ),
        "audit": selection.audit,
    }
    state["intelligence"] = read_intelligence(
        sorted({key.split("/", 1)[1] for key, item in selection.models.items() if item["state"] == "selected"}),
        block.get("intelligence_slugs") or {},
    )
    print(research_report(state))
    missing = [(label, number) for label, numbers in state["unfilled"].items() for number in numbers]
    if missing:
        names = ", ".join(f"{label} seat {number}" for label, number in missing)
        raise runner.CallFailed(
            f"seat-unavailable: {names} has no reachable admitted candidate; no receipt, no research call."
        )
    receipt = {
        "version": 1,
        "nonce": uuid4().hex,
        "binding": research_binding(root, change, klass, neighbours),
        "state": state,
    }
    receipt["report_id"] = seal(receipt)
    write_receipt(path, receipt)
    print(
        "Ask the maintainer in the main conversation which models to use, with this recommendation and its reason "
        "(intelligence against cost). To use a different choice, run "
        f"prepare-explore {change} --seats repository=<go models> --seats online=<go models>; "
        f"to use this one, run explore {change} --availability-reported {receipt['report_id']}"
    )


def consume_research(root: Path, change: str, token: str | None, runner, klass: str) -> dict:
    """Validate acknowledgment, freshness and input identity, then delete the receipt before any research call."""
    problem = "run prepare-explore and report its fresh selection in the main conversation; pass its id."
    _, rule = research_settings(root, runner)
    neighbours = given_neighbours(root, change, runner)
    path = research_receipt_path(change, runner, root)
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        state = receipt["state"]
        checked = dt.datetime.fromisoformat(state["checked_at"])
        age = (now() - checked).total_seconds()
        valid = (
            receipt["version"] == 1
            and verify(receipt, token)
            and receipt["binding"] == research_binding(root, change, klass, neighbours)
            and checked.tzinfo is not None
            and 0 <= age <= rule["max_age_seconds"]
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        valid = False
    if not valid:
        raise runner.Refused(problem)
    try:
        with receipt_lock(path):
            # A validated reader may be stale: never consume a newer preparation.
            with path.open(encoding="utf-8") as handle:
                current = json.load(handle)
            if current != receipt:
                raise runner.Refused(problem)
            path.unlink()
    except (OSError, ValueError) as error:
        raise runner.Refused(problem) from error
    return {**state, "report_id": token}


def research_roles(state: dict, data: dict) -> dict:
    """The graph's roles from the consumed selection: seats from the receipt, Opus roles from the declaration."""
    block = data["research_swarm"]
    paid = block["paid_endpoint"]

    def seat(item: dict) -> dict:
        return {"endpoint": item["endpoint"], "model": item["model"]}

    repository = [seat(item) for item in state["seats"]["repository"]]
    opus = {"endpoint": paid, "model": block["judge"], "effort": "xhigh"}
    return {
        "finder_agents": [dict(item) for item in repository],
        "repository_agents": repository,
        "online_agents": [seat(item) for item in state["seats"]["online"]],
        "finder_merge": {**opus, "model": block.get("finder_merge", block["judge"])},
        "topic_author": {**opus, "model": block["topic_author"], "effort": "high"},
        "judge": opus,
    }


# ---------------------------------------------------------------------------
# Review loop: preparation and consumption (ADR 0021, pull request #157)
# ---------------------------------------------------------------------------


def settings(root: Path, runner) -> dict | None:
    """An absent rule preserves legacy declarations; a present rule fails closed."""
    entry = runner.endpoint_entry(root)
    if "availability_preflight" not in entry:
        return None
    value = entry["availability_preflight"]
    problems = rule_problem(value, flash_size=True)  # the one validator both swarms use (criterion 50)
    if problems:
        raise runner.Refused("; ".join(problems) + ".")
    return value


def binding(root: Path, runner) -> dict:
    return {
        "root": str(root.resolve()),
        "configuration": digest((root / "model-endpoints.yaml").read_text(encoding="utf-8")),
        "diff": digest(runner.change_diff(root)),
    }


def receipt_path(root: Path, change: str, runner) -> Path:
    return runner.record_dir(change, root) / "availability.json"


def report(state: dict) -> str:
    available = state["availability"]
    lines = [
        f"Availability checked: {available['checked_at']}",
        f"Reachable: {', '.join(available['reachable']) or 'none'}",
        f"Free swarm: {', '.join(state['free']['selected']) or 'none'}",
        f"Flash swarm: {', '.join(state['paid']['flash']) or 'none'}",
        f"Paid ladder: {', '.join(state['paid']['rungs']) or 'none'}",
    ]
    lines.extend(f"Unavailable: {model}: {reason}" for model, reason in available["failed"].items())
    lines.extend(f"Skipped: {model}: {reason}" for model, reason in available["skipped"].items())
    # A receipt of an older runner holds no warning list; its absence is no
    # statement about current admission, which the round rechecks live.
    lines.extend(f"Terms warning: {warning}" for warning in available.get("terms_warnings", []))
    lines.extend(f"Address notice: {notice}" for notice in (state["free"] or {}).get("notices") or [])
    lines.append("Reachability is a point-in-time result, not a billing or review-quality measurement.")
    # Escape untrusted controls per line, preserving only the runner's own separators.
    return "\n".join(
        "".join(f"\\x{ord(char):02x}" if ord(char) < 32 or 127 <= ord(char) <= 159 else char for char in line)
        for line in lines
    )


@capture_preparation_warnings
def prepare(root: Path, change: str, runner) -> None:
    """Probe candidates without source input or tools, then publish a report receipt."""
    folder = runner.folder_of(root, change)
    rule = settings(root, runner)
    if rule is None:
        raise runner.Refused("this endpoint declares no availability_preflight rule.")
    path = receipt_path(root, change, runner)
    # A failed refresh/probe attempt must never leave an earlier receipt usable.
    path.unlink(missing_ok=True)
    findings = folder / "findings.md"
    text = findings.read_text(encoding="utf-8") if findings.exists() else ""
    record = runner.read_record(change, root)
    if record is None:
        refusal = runner.lost_record_refusal(change, root, text)
        if refusal:
            raise runner.Refused(refusal)
    # A maintainer's restart (ADR 0021, restart amendment) is the one way a run with history is prepared again.
    if not runner.restarted_fresh(record, text) and (
        runner.read_state(record, text) is not None or runner.rounds_run(record, text)
    ):
        raise runner.Refused("this review run already has history; preparation cannot reset its snapshot or stops.")
    problem = runner.entry_problem(root, runner.OPENCODE)
    if problem:
        raise runner.Refused(problem)
    entry = runner.endpoint_entry(root)
    terms_evidence = preparation_terms(runner, entry)
    runner.require_pi()
    free = runner.discover_free(root, allow_empty=True)
    paid = runner.ladder(root)
    skipped = {model: "not admitted; data terms have not been read" for model in runner.unread_catalog_ids(entry, free)}
    # A free id discovery dropped (excluded, or not a plain id) is named, never probed (DL-B-2, DL-B-7).
    skipped.update(free.get("dropped") or {})
    candidates = list(free["selected"])
    if not runner.free_diff(root)[0].strip():
        free["skipped"] = "free stage skipped: no implementation source diff"
        skipped.update({model: free["skipped"] for model in candidates})
        candidates = []
    for model in paid:
        if model not in free["overlay"]:
            skipped[model] = "absent from the fresh provider catalog"
        elif runner.request_value(entry, model) is None:
            skipped[model] = "no admitted cost value"
        else:
            candidates.append(model)
    reachable = []
    failed = {}
    slow: dict[str, int] = {}
    key = runner.reviewer_key()
    # A free model is probed with the free round's own prompt: the tiny probe passed a model whose real
    # requests all failed (bead k9rw). Without a free diff no free model is a candidate (above).
    free_text = runner.free_probe_prompt(root) if free["selected"] else None
    for model in dict.fromkeys(candidates):
        excluded = excluded_reason(rule, model)
        if excluded is not None:
            skipped[model] = excluded
        if model in skipped:
            continue
        is_free = model in free["selected"] and free_text is not None
        limits = (FREE_PROBE_SECONDS, FREE_PROBE_RETRY_SECONDS) if is_free else (PROBE_SECONDS, PROBE_RETRY_SECONDS)
        # A probe that only ran out of time is tried once more with a longer limit: a slow but
        # reachable model must not disappear from the run silently (R-7 of the review-swarm review).
        for attempt, limit in enumerate(limits, 1):
            # Every foreign call is checked and audited on its own, the second one too: an admission
            # withdrawn between the two probes must stop it, and the leak check runs before each call
            # (the review of PR #196).
            admission = runner._free_admission(model in free["selected"], {"free": free})
            endpoint = (runner.OPENCODE, model, "max")
            ctx = runner.preflight(root, change, endpoint, admission_problem=admission)
            audit: list[str] = []
            try:
                # All probes, including paid ones, have no repository input or tools: the shared probe.
                probe_go(
                    runner,
                    root,
                    change,
                    model,
                    key,
                    audit,
                    free.get("models_store"),
                    admission=admission
                    or (lambda root_, model_: runner.declaration_problem(root_, runner.OPENCODE, model_)),
                    verb="prepare-loop",
                    timeout_seconds=limit,
                    text=free_text if is_free else PROBE_TEXT,
                )
            except runner.CallFailed as error:
                failure = runner.scrub(str(error), key)
                failed[model] = failure
                # Only a stopped call is worth a longer try; a refused one stays refused.
                stopped = "stopped by" in failure
            except stage2_go.DestinationRefused as error:
                # The record refuses this model's destination: named in the
                # report's failed map, never retried, never substituted.
                failed[model] = str(error)
                stopped = False
            else:
                failure = None
                stopped = False
                reachable.append(model)
                failed.pop(model, None)
                if attempt > 1:
                    slow[model] = limit
            if audit:  # a probe that passed its checks leaves its call line, whatever its outcome
                if not findings.exists():
                    findings.write_text(runner.findings_header(ctx, runner.producer_for(endpoint)), encoding="utf-8")
                runner.append(findings, f"Stage-2 call, {runner.today()}: {audit[0]}")
            if failure is None or not stopped:
                break
    state = {"free": free, "paid": {}, "consumed": []}
    state["free"]["selected"] = [model for model in free["selected"] if model in reachable]
    admitted = [model for model in paid if model in reachable]
    flash = admitted[: rule["flash_size"]]
    state["paid"] = {"ladder": admitted, "flash": flash, "rungs": admitted[len(flash) :]}
    state["availability"] = {
        "checked_at": now().isoformat(timespec="seconds"),
        "reachable": reachable,
        "failed": failed,
        "slow": slow,
        "skipped": skipped,
        "terms_skipped": runner.skipped_models(root),
        # Advance notice inside the seven-day window, expired records excluded:
        # the warning travels in the receipt's digest and reaches the report
        # here (bead coding-harness-abra). A warning grants no admission.
        **terms_evidence,
    }
    print(report(state))
    for reason in state["availability"]["terms_skipped"]:
        print(f"Paid admission skipped: {reason}")
    if not runner.stages_of(state):
        raise runner.Refused("no reachable admitted reviewer remains; no review round or clean result was produced.")
    receipt = {"version": 1, "binding": binding(root, runner), "state": state}
    token = seal(receipt)
    receipt["report_id"] = token
    write_receipt(path, receipt)
    print(
        f"Report this selection in the main conversation, then run review-loop {change} --availability-reported {token}"
    )


def consume(root: Path, change: str, token: str | None, runner) -> dict:
    """Validate acknowledgment, freshness and input identity before any review call."""
    rule = settings(root, runner)
    path = receipt_path(root, change, runner)
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        state = receipt["state"]
        checked = dt.datetime.fromisoformat(state["availability"]["checked_at"])
        age = (now() - checked).total_seconds()
        valid = (
            rule is not None
            and receipt["version"] == 1
            and verify(receipt, token)
            and receipt["binding"] == binding(root, runner)
            and checked.tzinfo is not None
            and 0 <= age <= rule["max_age_seconds"]
            and state["consumed"] == []
            and bool(runner.stages_of(state))
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        valid = False
    if not valid:
        raise runner.Refused(
            "run prepare-loop and report its fresh selection in the main conversation; pass its --availability-reported id."
        )
    return state


def spend(root: Path, change: str, runner) -> None:
    """Spend the receipt once the first round is written, never earlier (ADR 0021, decision 6).

    A failed attempt consumes no stage and leaves no record, so it leaves the receipt too; the
    operator does not re-probe for a Pi that was missing (O190-3).
    """
    receipt_path(root, change, runner).unlink(missing_ok=True)
