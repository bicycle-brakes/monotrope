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
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from uuid import uuid4

import leakcheck
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


def now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


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


def research_declaration_problem(root: Path, endpoint: str, model: str) -> str | None:
    """Why the declaration does not clear this model for a research call, or None.

    A model is listed in `modelle` or - for research only - by a `modelle_terms` record, so a record alone
    admits it without touching the review ladder. The endpoint must name a residency.
    """
    data = read_declaration(root)
    if isinstance(data, str):
        return data
    found = _endpoint(data, endpoint)
    if found is None:
        return f"model-endpoints.yaml declares no endpoint {endpoint}"
    if not _model_listed(found, model):
        return f"the endpoint {endpoint} does not declare the model {model}"
    residency = found.get("residenz")
    if not isinstance(residency, str) or not residency.strip() or residency == "nicht-erklaert":
        return f"the endpoint {endpoint} states no data residency"
    return None


def _checked_probe(
    runner,
    root: Path,
    change: str,
    endpoint: str,
    model: str,
    audit: list[str],
    admission=None,
    verb: str = "prepare-explore",
) -> None:
    """The declaration, the exact-prompt leak check and the audit line - for this one probe, immediately before it.

    `admission` (root, model -> problem or None) replaces the research declaration check for the review
    swarm's free class (ADR 0021, decision 3); the leak check stays mandatory either way.
    """
    problem = admission(root, model) if admission is not None else research_declaration_problem(root, endpoint, model)
    if problem:
        raise runner.Refused(problem)
    result = leakcheck.check(change, leakcheck.default_denylist(), root, [("prompt", PROBE_TEXT)])
    print(result.verdict.render())
    if result.verdict.exit_code() != 0:
        raise runner.Refused("the leak check is not clean; the probe does not start.")
    audit.append(
        f"{verb} · endpoint {endpoint} · model {model} · leak check clean over "
        f"{result.files} files, {result.commits} commits, {result.rules} rules."
    )


def _failed(runner, program: str, done, reason: str, key: str | None) -> object:
    tail = " / ".join(line.strip() for line in (done.stderr or "").splitlines()[-3:] if line.strip())
    detail = f": {runner.scrub(tail, key)}" if tail else ""
    return runner.CallFailed(f"{program} call failed: {reason}{detail}")


def install_measured_models(runner, agent: Path, store: dict | None) -> None:
    """Give Pi's fresh agent directory the measured catalog: the retrieval evidence and its model definitions."""
    if store:
        (agent / "models-store.json").write_text(json.dumps(store), encoding="utf-8")
        runner.activate_overlay(agent, store)


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
) -> None:
    """One tool-free Go probe: pinned Pi wrapper, no tools, scratch directories, fixed text, one limit.

    The limit is a parameter, not a constant: a probe that only ran out of time is tried once more
    with a longer one (R-7 of the review-swarm review), and the longer try must use the same probe.
    """
    _checked_probe(runner, root, change, GO, model, audit, admission, verb)
    with tempfile.TemporaryDirectory(prefix="stage2-probe-") as tmp:
        scratch = Path(tmp)
        agent = scratch / "agent"
        agent.mkdir()
        (agent / "settings.json").write_text(json.dumps({"retry": {"enabled": False}}), encoding="utf-8")
        install_measured_models(runner, agent, store)
        home = scratch / "home"
        home.mkdir()
        prompt_file = scratch / "probe-prompt.md"
        prompt_file.write_text(PROBE_TEXT, encoding="utf-8")
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
        done = runner.launch(
            command,
            scratch,
            env,
            key,
            timeout=timeout_seconds,
            limit=f"the probe limit of {timeout_seconds} seconds",
        )
        if done.returncode != 0:
            raise _failed(runner, "pi", done, f"exit {done.returncode}", key)
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


def read_declaration(root: Path) -> dict | str:
    """The parsed `model-endpoints.yaml`, or the problem text when it cannot be read."""
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return "model-endpoints.yaml cannot be read"
    return data if isinstance(data, dict) else "model-endpoints.yaml cannot be read"


def _endpoint(data: dict, name: str) -> dict | None:
    return next((e for e in data.get("endpunkte") or [] if isinstance(e, dict) and e.get("name") == name), None)


def research_settings(root: Path, runner) -> tuple[dict, dict]:
    """The validated declaration and the research rule, or the refusal (exit 2) naming the fault."""
    data = read_declaration(root)
    if isinstance(data, str):
        raise runner.Refused(data)
    problems = stage2_swarm.seat_problems(data)
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


def research_receipt_path(change: str, runner) -> Path:
    return runner.record_dir(change) / "research-availability.json"


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


class _Selection:
    """One preparation: model outcomes, the substitute pool and the lazy, unique probes."""

    def __init__(self, root, change, runner, data, rule, catalog) -> None:
        self.root, self.change, self.runner, self.rule = root, change, runner, rule
        self.go = _endpoint(data, GO) or {}
        self.catalog = {item["id"]: item for item in catalog["models"]}
        self.models_store = catalog.get("models_store")
        self.audit: list[str] = []
        self.probed: dict[str, str | None] = {}
        self.key: str | None = None
        self.models: dict[str, dict] = {}
        self.go_framework = "framework" in (self.go.get("darf_sehen") or [])
        ids = {
            *self.catalog,
            *(self.go.get("modelle_terms") or {}),
            *(
                seat["model"]
                for name in ("repository_seats", "online_seats")
                for seat in data["research_swarm"][name]
                if seat["endpoint"] == GO
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
        outcome = {"state": "not-probed", "reason": "", "admitted": True, "tool_support": "not-pool"}
        excluded = excluded_reason(self.rule, seat["model"])
        if excluded:
            outcome.update(state="excluded", reason=excluded)
        return outcome

    def usable(self, endpoint: str, model: str) -> bool:
        item = self.models.get(f"{endpoint}/{model}")
        return bool(item) and item.get("admitted") is True and item["state"] != "excluded"

    def reachable(self, endpoint: str, model: str) -> bool:
        """Probe at most once per preparation; the result is shared across seats and trios."""
        key = f"{endpoint}/{model}"
        item = self.models[key]
        if key not in self.probed:
            try:
                if endpoint == GO:
                    if self.key is None:
                        self.key = self.runner.reviewer_key()
                    probe_go(self.runner, self.root, self.change, model, self.key, self.audit, self.models_store)
                else:
                    probe_claude(self.runner, self.root, self.change, model, self.audit)
            except self.runner.CallFailed as error:
                self.probed[key] = self.runner.scrub(str(error), self.key)
                item.update(state="unreachable", reason=self.probed[key])
            else:
                self.probed[key] = None
                item.update(state="selected", reason="reachable")
        return self.probed[key] is None

    def fill(self, label: str, seats: list[dict]) -> list[dict | None]:
        chosen: list[dict | None] = [None] * len(seats)
        taken: set[str] = set()
        for number, seat in enumerate(seats):
            endpoint, model = seat["endpoint"], seat["model"]
            if self.usable(endpoint, model) and self.reachable(endpoint, model):
                chosen[number] = {"seat": number + 1, "endpoint": endpoint, "model": model, "mark": "preferred"}
                taken.add(f"{endpoint}/{model}")
        for number in range(len(seats)):
            if chosen[number] is not None:
                continue
            if label == "repository" and not self.go_framework:
                continue
            for entry in self.pool:
                model = entry["model"]
                key = f"{GO}/{model}"
                if key in taken or not self.usable(GO, model):
                    continue
                if key in self.probed and self.probed[key] is not None:
                    continue
                if self.reachable(GO, model):
                    chosen[number] = {
                        "seat": number + 1,
                        "endpoint": GO,
                        "model": model,
                        "mark": f"substitute for {number + 1}",
                    }
                    taken.add(key)
                    break
        return chosen


def _free_text(values: list[str]) -> str:
    return ", ".join(values) or "none"


def research_report(state: dict) -> str:
    lines = [f"Availability checked: {state['checked_at']}"]
    for label in ("repository", "online"):
        for item in state["seats"][label]:
            if item is None:
                continue
            lines.append(f"{label} seat {item['seat']}: {item['endpoint']}/{item['model']} ({item['mark']})")
    for label, items in state["unfilled"].items():
        lines.extend(f"seat-unavailable: {label} seat {number}" for number in items)
    pool = ", ".join(f"{item['model']} ({item['anfragen_5h']:g})" for item in state["pool"]) or "empty"
    lines.append(f"Pool, cheapest first: {pool}")
    lines.append(f"Free selection: {_free_text(state['free']['selected'])}")
    lines.append("Models:")
    for key, item in state["models"].items():
        detail = f" - {item['reason']}" if item.get("reason") else ""
        lines.append(f"  {key}: {STATE_LABELS[item['state']]}{detail}")
    if state["unread"]:
        lines.append(f"Unread (no data-terms record, never used): {_free_text(state['unread'])}")
    lines.append("Reachability is a point-in-time result, not a billing or research-quality measurement.")
    return "\n".join(lines)


def prepare_research(root: Path, change: str, runner, klass: str | None = None) -> None:
    """Admit, probe and select the six seats, report them, and seal a receipt - or stop with exit 1 or 2.

    Writes nothing in the worktree: the receipt and its audit lines live in the runner's state directory.
    """
    path = research_receipt_path(change, runner)
    # A failed preparation must never leave an earlier receipt usable.
    with receipt_lock(path):
        path.unlink(missing_ok=True)
    runner.folder_of(root, change)
    klass = runner.declared_class(root, change, klass)
    if klass not in runner.SWARM_CLASSES:
        raise runner.Refused(f"prepare-explore belongs to feature or architectural changes, not {klass}.")
    data, rule = research_settings(root, runner)
    neighbours = given_neighbours(root, change, runner)
    runner.require_pi()
    block = data["research_swarm"]
    seats = {"repository": block["repository_seats"], "online": block["online_seats"]}
    go_entry = _endpoint(data, GO) or {}
    declared = go_entry.get("modelle_terms")
    # Every declared Go model is classified against the fresh overlay, so each skip carries its own reason.
    preferred = sorted(
        {seat["model"] for trio in seats.values() for seat in trio if seat["endpoint"] == GO}
        | {model for model in (declared if isinstance(declared, dict) else {}) if not str(model).endswith("-free")}
    )
    try:
        catalog = stage2_swarm.select_research_catalog(
            catalog_bridge(runner, root),
            block["online_free"],
            preferred,
            expected_version=runner.PI_VERSION,
            measured_wire_apis=rule["measured_wire_apis"],
        )
    except stage2_swarm.ResearchCatalogError as error:
        if error.exit_code == 2:
            raise runner.Refused(str(error)) from error
        raise runner.CallFailed(f"the Go catalog is unmeasured: {error}; no probe or research call starts.") from error
    selection = _Selection(root, change, runner, data, rule, catalog)
    chosen = {label: selection.fill(label, trio) for label, trio in seats.items()}
    terms = selection.go.get("modelle_terms")
    terms = terms if isinstance(terms, dict) else {}
    state = {
        "checked_at": now().isoformat(timespec="seconds"),
        "catalog": {
            key: catalog[key]
            for key in (
                "pi_version",
                "selection_outcome",
                "capability_status",
                "capability_reason",
                "measured_wire_apis",
                "sources",
                "candidates",
                "models",
                "models_store",
            )
        },
        "free": {"selected": list(catalog["selected"]), "policy": catalog["policy"]},
        "seats": chosen,
        "unfilled": {
            label: [number + 1 for number, item in enumerate(items) if item is None] for label, items in chosen.items()
        },
        "pool": selection.pool,
        "models": {
            key: {name: value for name, value in item.items() if name in {"state", "reason"}}
            for key, item in selection.models.items()
        },
        "unread": sorted(
            item["id"] for item in catalog["models"] if not item["id"].endswith("-free") and item["id"] not in terms
        ),
        "audit": selection.audit,
    }
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
        "Report this selection in the main conversation, then run "
        f"explore {change} --availability-reported {receipt['report_id']}"
    )


def consume_research(root: Path, change: str, token: str | None, runner, klass: str) -> dict:
    """Validate acknowledgment, freshness and input identity, then delete the receipt before any research call."""
    problem = "run prepare-explore and report its fresh selection in the main conversation; pass its id."
    _, rule = research_settings(root, runner)
    neighbours = given_neighbours(root, change, runner)
    path = research_receipt_path(change, runner)
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
    lines.append("Reachability is a point-in-time result, not a billing or review-quality measurement.")
    return "\n".join(lines)


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
    if runner.read_state(record, text) is not None or runner.rounds_run(record, text):
        raise runner.Refused("this review run already has history; preparation cannot reset its snapshot or stops.")
    problem = runner.entry_problem(root, runner.OPENCODE)
    if problem:
        raise runner.Refused(problem)
    runner.require_pi()
    free = runner.discover_free(root, allow_empty=True)
    entry = runner.endpoint_entry(root)
    paid = runner.ladder(root)
    skipped = {model: "not admitted; data terms have not been read" for model in runner.unread_catalog_ids(entry, free)}
    candidates = list(free["selected"])
    if not runner.free_diff(root).strip():
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
    for model in dict.fromkeys(candidates):
        excluded = excluded_reason(rule, model)
        if excluded is not None:
            skipped[model] = excluded
        if model in skipped:
            continue
        # A probe that only ran out of time is tried once more with a longer limit: a slow but
        # reachable model must not disappear from the run silently (R-7 of the review-swarm review).
        for attempt, limit in enumerate((PROBE_SECONDS, PROBE_RETRY_SECONDS), 1):
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
                )
            except runner.CallFailed as error:
                failure = runner.scrub(str(error), key)
                failed[model] = failure
                # Only a stopped call is worth a longer try; a refused one stays refused.
                stopped = "stopped by" in failure
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
