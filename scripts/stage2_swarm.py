#!/usr/bin/env python3
"""The research swarm's declaration, catalog and permission layer: phase 1 of a `feature` or `architectural` change.

The run itself is `scripts/stage2_research_run.py`; `run` below delegates to it. This module holds what
the preparation and the run share and what needs no model: the Go catalog selection, the six-seat
declaration check, the per-invocation role permissions, the slot graph and the public-call helpers.
The runner module (`scripts/stage2.py`) is passed in as `runner` and is never imported here - stage2.py
runs as `__main__`, so importing it would execute the module a second time.

Eleven topics (1-8 repository, 9-11 online), a finder trio, an Opus map merge, an Opus public sentence and
an Opus judge: `39 + 3N` calls for `N` selected free models. Every seat is named by the run's frozen
selection, never by a hardcoded roster (ADR 0020 draft, Q-12 to Q-14).
"""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Sequence
from pathlib import Path
from urllib.parse import urlsplit

# The free researcher's whole tool surface, as Pi's `--tools` allow-list: the
# extension's two tools and no built-in one (the extension's own gate stays).
PUBLIC_TOOLS = "public_search,public_fetch"


class ResearchCatalogError(ValueError):
    """A failed preflight (1) or invalid declaration (2), before model calls."""

    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code


def validate_research_free_policy(policy: dict) -> None:
    """Validate the entire selection policy before reading network sources."""
    keys = {"provider", "suffix", "include", "exclude"}
    if not isinstance(policy, dict) or set(policy) != keys:
        raise ResearchCatalogError("invalid free selection policy keys", 2)
    if policy["provider"] != "opencode-go" or policy["suffix"] != "-free":
        raise ResearchCatalogError("invalid free provider or suffix", 2)
    for key in ("include", "exclude"):
        values = policy[key]
        if (
            not isinstance(values, list)
            or any(not isinstance(item, str) or not item.endswith("-free") or item == "-free" for item in values)
            or len(set(values)) != len(values)
        ):
            raise ResearchCatalogError(f"invalid free selection {key}", 2)


class _CatalogObject(dict):
    def __init__(self, pairs):
        super().__init__(pairs)
        seen = set()
        self.duplicate_keys = set()
        for key, _ in pairs:
            if key in seen:
                self.duplicate_keys.add(key)
            seen.add(key)
        self.duplicates = bool(self.duplicate_keys)


def _catalog_json(body):
    def reject(value):
        raise ValueError(f"non-finite JSON value: {value}")

    return json.loads(body, object_pairs_hook=_CatalogObject, parse_constant=reject)


def _catalog_duplicates(value):
    if isinstance(value, dict):
        return getattr(value, "duplicates", False) or any(_catalog_duplicates(item) for item in value.values())
    return isinstance(value, list) and any(_catalog_duplicates(item) for item in value)


def select_research_catalog(bridge, policy, fixed_ids, *, expected_version, measured_wire_apis=("openai-completions",)):
    """Intersect a fresh pinned Pi response with capability evidence, never a cache union.

    The bridge transports raw source bodies. Python retains duplicate identity and
    malformed-field evidence that the runtime's permissive parser would discard.
    This selects a roster and classifies every seat candidate (`fixed_ids`, the
    preferred models) and every paid model of the fresh overlay; it does not
    authorize or dispatch any model. A candidate that is absent, baseline-only,
    non-chat, malformed or on an unmeasured wire API is skipped with its raw
    evidence, never a failure of the whole preflight (Q-12, Q-14).
    """
    validate_research_free_policy(policy)
    provider = policy["provider"]
    sources = bridge.get("sources", {})
    pi = sources.get("pi", {})
    runtime = bridge.get("pi_runtime", {})
    if (
        bridge.get("exit_code") != 0
        or bridge.get("pi_version") != expected_version
        or pi.get("status") != 200
        or runtime.get("aborted")
        or runtime.get("errors")
        or provider not in bridge.get("models_store", {})
    ):
        raise ResearchCatalogError(bridge.get("reason") or "pi-refresh-failed")
    try:
        raw = _catalog_json(pi["body"])
    except (KeyError, TypeError, ValueError) as error:
        raise ResearchCatalogError("pi-malformed") from error
    if _catalog_duplicates(raw):
        raise ResearchCatalogError("duplicate Pi identity or key")
    if isinstance(raw, dict):
        raw = raw["models"] if isinstance(raw.get("models"), list) else list(raw.values())
    if not isinstance(raw, list):
        raise ResearchCatalogError("pi-malformed")
    models = {}
    for item in raw:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            # The pinned parser ignores non-model entries. Only fixed/free
            # identities need candidate validation; other entries grant no seat.
            continue
        if item["id"] in models:
            raise ResearchCatalogError("duplicate Pi identity")
        models[item["id"]] = item

    def pi_reason(item):
        kind = item.get("type", "chat")
        inputs = item.get("input")
        if (
            kind not in ("chat", "image", "classifier")
            or not isinstance(inputs, list)
            or any(not isinstance(x, str) for x in inputs)
        ):
            return "pi-malformed"
        if kind != "chat" or "text" not in inputs:
            return "not-chat"
        if item.get("provider", provider) != provider:
            return "pi-malformed"
        try:
            target = urlsplit(item.get("baseUrl", "https://opencode.ai/zen/go/v1"))
            safe_origin = (
                target.scheme == "https"
                and target.hostname == "opencode.ai"
                and target.port in (None, 443)
                and target.username is None
                and target.password is None
                and target.path in ("/zen/go/v1", "/zen/go/v1/")
                and not target.query
                and not target.fragment
            )
        except (TypeError, ValueError, AttributeError):
            safe_origin = False
        if not safe_origin:
            return "pi-malformed"
        return None

    baseline = set(bridge.get("baseline", []))
    wire_apis = list(measured_wire_apis)

    def seat_reason(ident):
        item = models.get(ident)
        if item is None:
            return "baseline-only" if ident in baseline else "not-in-fresh-pi"
        reason = pi_reason(item)
        if reason:
            return reason
        return None if item.get("api") in wire_apis else "wire-api-not-measured"

    metadata = sources.get("models_dev", {})
    capability_reason = None
    capabilities = {}
    if metadata.get("status") != 200 or metadata.get("outcome") != "ok":
        capability_reason = metadata.get("outcome") or "unavailable"
    else:
        try:
            document = _catalog_json(metadata["body"])
            block = document.get(provider) if isinstance(document, dict) else None
            capabilities = block.get("models") if isinstance(block, dict) else None
            if not isinstance(capabilities, dict):
                capability_reason = "malformed"
                capabilities = {}
            elif (
                provider in getattr(document, "duplicate_keys", set())
                or "models" in getattr(block, "duplicate_keys", set())
                or _catalog_duplicates(capabilities)
            ):
                capability_reason = "duplicate-id"
            else:
                identities = [
                    entry.get("id")
                    for entry in capabilities.values()
                    if isinstance(entry, dict) and isinstance(entry.get("id"), str)
                ]
                if len(identities) != len(set(identities)):
                    capability_reason = "duplicate-id"
        except (KeyError, TypeError, ValueError):
            capability_reason = "malformed"
            capabilities = {}

    def evidence_of(ident, pi_keys=("type", "input", "provider", "baseUrl")):
        item = models.get(ident)
        entry = capabilities.get(ident)
        evidence = {
            key: {"present": True, "value": entry[key]}
            if isinstance(entry, dict) and key in entry
            else {"present": False}
            for key in ("id", "tool_call", "status")
        }
        evidence["entry"] = {"present": True, "value": entry} if ident in capabilities else {"present": False}
        evidence["pi"] = {
            key: {"present": True, "value": item[key]} if isinstance(item, dict) and key in item else {"present": False}
            for key in pi_keys
        }
        return evidence

    def metadata_reason(ident):
        """Why models.dev does not show tool support for the id, or None when it does."""
        entry = capabilities.get(ident)
        if capability_reason:
            return "capability-unavailable"
        if ident not in capabilities:
            return "metadata-missing"
        if (
            not isinstance(entry, dict)
            or getattr(entry, "duplicates", False)
            or entry.get("id") != ident
            or "tool_call" in entry
            and type(entry["tool_call"]) is not bool
            or "status" in entry
            and not isinstance(entry["status"], str)
        ):
            return "metadata-malformed"
        if not entry.get("tool_call", False):
            return "no-tool-support"
        if entry.get("status") == "deprecated":
            return "deprecated"
        return None

    candidates = []
    eligible = set()
    ids = sorted(
        {ident for ident in models if ident.endswith("-free")}
        | {ident for ident in bridge.get("baseline", []) if ident.endswith("-free")}
    )
    for ident in ids:
        item = models.get(ident)
        evidence = evidence_of(ident)
        reason = "not-in-fresh-pi" if item is None else pi_reason(item)
        if reason is None:
            reason = metadata_reason(ident)
        if reason is None:
            eligible.add(ident)
        candidates.append({"id": ident, "reason": reason, "evidence": evidence})
    seat_models = []
    for ident in sorted({*fixed_ids, *(name for name in models if not name.endswith("-free"))}):
        reason = seat_reason(ident)
        seat_models.append(
            {
                "id": ident,
                "reason": reason,
                "evidence": evidence_of(ident, ("type", "input", "provider", "baseUrl", "api")),
                "tool_support": metadata_reason(ident) if reason is None else "not-assessed",
            }
        )
    for ident in policy["include"]:
        if ident not in eligible:
            raise ResearchCatalogError(f"explicit free include is ineligible: {ident}")
    selected = eligible & set(policy["include"]) if policy["include"] else eligible
    selected -= set(policy["exclude"])
    for candidate in candidates:
        if candidate["reason"] is None and candidate["id"] not in selected:
            candidate["reason"] = "excluded" if candidate["id"] in policy["exclude"] else "not-included"
    return {
        "selected": sorted(selected),
        "N": len(selected),
        "policy": {**policy, "include": list(policy["include"]), "exclude": list(policy["exclude"])},
        "pi_version": bridge["pi_version"],
        "raw_pi_ids": sorted(models),
        "selection_outcome": "selected"
        if selected
        else ("capability-unavailable" if capability_reason else "measured-empty"),
        "fixed": list(fixed_ids),
        "models_store": bridge["models_store"],
        "sources": {
            name: {key: value for key, value in source.items() if key != "body"} for name, source in sources.items()
        },
        "candidates": candidates,
        "models": seat_models,
        "measured_wire_apis": wire_apis,
        "capability_status": "capability-unavailable" if capability_reason else "available",
        "capability_reason": capability_reason,
    }


# ---------------------------------------------------------------------------
# Role identities and per-invocation permissions (plan step 2; spec criteria 11, 37, 40)
# ---------------------------------------------------------------------------

GO_ENDPOINT = "opencode-go"
CLAUDE_ENDPOINT = "claude-code-plan"
PRIVATE_ROLES = ("finder", "repository", "finder_merge", "topic_author", "judge")
PUBLIC_ROLES = ("online", "online_free")
OPUS_ROLES = ("finder_merge", "topic_author", "judge")
ROLE_CLASS = {**dict.fromkeys(PRIVATE_ROLES, "framework"), **dict.fromkeys(PUBLIC_ROLES, "public-web")}
# The one program that serves an endpoint: pinned Pi for Go, the official read-only Claude Code for the plan.
LAUNCHERS = {GO_ENDPOINT: "pi", CLAUDE_ENDPOINT: "claude-code"}


def _declared_endpoint(data: dict, name: str) -> dict:
    for candidate in data.get("endpunkte") or []:
        if isinstance(candidate, dict) and candidate.get("name") == name:
            return candidate
    return {}


def invocation_problem(
    data: dict,
    role: str,
    endpoint: str,
    model: str,
    *,
    data_class: str | None = None,
    selected_free: Sequence[str] = (),
) -> str | None:
    """Why this role may not launch this model on this endpoint with this data class, or None.

    The decision is per invocation: the role fixes the data class and the launcher, so an endpoint's own
    permission (the Go endpoint may see framework content) never widens what an online seat carries, and a
    `-free` model, permitted dynamically for the public role alone, never fills a private role (criteria 11, 40).
    """
    if role not in ROLE_CLASS:
        return f"unknown research role {role}"
    wanted = ROLE_CLASS[role]
    if data_class is not None and data_class != wanted:
        return f"the {role} role carries {wanted} data only, not {data_class}"
    if endpoint not in LAUNCHERS:
        return f"no launcher serves the endpoint {endpoint}"
    free = isinstance(model, str) and model.endswith("-free")
    if role == "online_free":
        policy = (data.get("research_swarm") or {}).get("online_free")
        try:
            validate_research_free_policy(policy)  # type: ignore[arg-type]
        except ResearchCatalogError as error:
            return str(error)
        if endpoint != policy["provider"]:
            return f"free models run on {policy['provider']} only, not {endpoint}"
        if not model.endswith(policy["suffix"]) or model == policy["suffix"]:
            return f"{model} does not carry the {policy['suffix']} suffix"
        if model in policy["exclude"]:
            return f"{model} is excluded by the free selection policy"
        if policy["include"] and model not in policy["include"]:
            return f"{model} is not among the policy's explicit includes"
        if model not in set(selected_free):
            return f"{model} is not in this run's frozen free selection"
        return None
    if free:
        return f"a -free model never fills the {role} role"
    if role in OPUS_ROLES and (endpoint != CLAUDE_ENDPOINT or not model.startswith("claude-opus")):
        return f"the {role} role is Opus on {CLAUDE_ENDPOINT}"
    if role == "online" and endpoint != GO_ENDPOINT:
        return f"online seats run on {GO_ENDPOINT}"
    found = _declared_endpoint(data, endpoint)
    if not found:
        return f"model-endpoints.yaml declares no endpoint {endpoint}"
    terms = found.get("modelle_terms")
    if model not in (found.get("modelle") or []) and not (isinstance(terms, dict) and model in terms):
        return f"the endpoint {endpoint} does not declare the model {model}"
    if role in PRIVATE_ROLES:
        allowed = found.get("darf_sehen")
        if not isinstance(allowed, list) or "framework" not in allowed:
            return f"the endpoint {endpoint} may not see framework content"
        residency = found.get("residenz")
        if not isinstance(residency, str) or not residency.strip() or residency == "nicht-erklaert":
            return f"the endpoint {endpoint} states no data residency"
    return None


def role_launches(data: dict, roles: dict, selected_free: Sequence[str]) -> list[dict]:
    """Every launch identity of one run, or ResearchCatalogError (exit 2) naming the first unpermitted role.

    `roles` is the resolved set (`stage2_availability.research_roles`) built from the consumed seat selection
    and the declaration; `selected_free` is the run's frozen free selection. Nothing is returned for a set with
    a refused member, so no launch starts before the whole set is checked.
    """
    block = data.get("research_swarm")
    validate_research_free_policy(block.get("online_free") if isinstance(block, dict) else None)  # type: ignore[arg-type]
    plan = (
        [("finder", seat) for seat in roles["finder_agents"]]
        + [("finder_merge", roles["finder_merge"]), ("topic_author", roles["topic_author"])]
        + [("repository", seat) for seat in roles["repository_agents"]]
        + [("online", seat) for seat in roles["online_agents"]]
        + [("online_free", {"endpoint": GO_ENDPOINT, "model": ident}) for ident in selected_free]
        + [("judge", roles["judge"])]
    )
    launches = []
    for role, seat in plan:
        problem = invocation_problem(data, role, seat["endpoint"], seat["model"], selected_free=selected_free)
        if problem:
            raise ResearchCatalogError(f"{role} {seat['endpoint']}/{seat['model']}: {problem}", 2)
        launches.append(
            {
                "role": role,
                "endpoint": seat["endpoint"],
                "model": seat["model"],
                "program": LAUNCHERS[seat["endpoint"]],
                "data_class": ROLE_CLASS[role],
            }
        )
    return launches


def research_slot_plan(roles, selected_free):
    """Describe the amended graph; dispatch and runtime barriers are separate gates."""
    validate_research_free_policy(
        {"provider": "opencode-go", "suffix": "-free", "include": selected_free, "exclude": []}
    )
    if not isinstance(roles, dict):
        raise ResearchCatalogError("invalid research role declaration", 2)
    for name in ("finder_agents", "repository_agents", "online_agents"):
        seats = roles.get(name)
        if not isinstance(seats, list) or len(seats) != 3:
            raise ResearchCatalogError(f"{name} must declare three required seats", 2)
    all_roles = [seat for name in ("finder_agents", "repository_agents", "online_agents") for seat in roles[name]] + [
        roles.get(name) for name in ("finder_merge", "topic_author", "judge")
    ]
    for role in all_roles:
        if not isinstance(role, dict) or any(
            not isinstance(role.get(key), str) or not role[key] for key in ("endpoint", "model")
        ):
            raise ResearchCatalogError("invalid research role identity", 2)
        if role["model"].endswith("-free"):
            raise ResearchCatalogError("free seats belong only to the dynamic online roster", 2)
    graph = []

    def add(stage, role, topic=None, required=True):
        graph.append(
            {
                **role,
                "id": f"{stage}-{topic or 0}-{len(graph) + 1}",
                "stage": stage,
                "topic": topic,
                "required": required,
            }
        )

    for role in roles["finder_agents"]:
        add("finders", role)
    add("merge", roles["finder_merge"])
    add("sentence", roles["topic_author"])
    for topic in range(1, 12):
        for role in roles["repository_agents"] if topic <= 8 else roles["online_agents"]:
            add("topics", role, topic)
    for topic in range(9, 12):
        for ident in selected_free:
            add("topics", {"endpoint": "opencode-go", "model": ident}, topic, False)
    add("judge", roles["judge"])
    return graph


SEAT_KEYS = {"endpoint", "model"}


def seat_problems(data: dict) -> list[str]:
    """What the six research seats and the availability rule require, as the problems found (Q-12, Q-14).

    Each trio is exactly three seats with one preferred `{endpoint, model}` each and no fallback list.
    A model is declared by its endpoint's `modelle` or, for research only, by a `modelle_terms` record,
    so a record alone admits it and the review ladder never changes. A `-free` id never fills a seat,
    online seats run on `opencode-go`, and repository seats need an endpoint cleared for `framework`
    with a stated residency. One model fills at most one seat of a trio.
    """
    from stage2_availability import rule_problem

    block = data.get("research_swarm")
    if not isinstance(block, dict):
        return ["no research_swarm block"]
    problems: list[str] = []

    def endpoint(name: object) -> dict:
        for candidate in data.get("endpunkte") or []:
            if isinstance(candidate, dict) and candidate.get("name") == name:
                return candidate
        return {}

    for key, label in (("repository_seats", "repository"), ("online_seats", "online")):
        seats = block.get(key)
        if not isinstance(seats, list) or len(seats) != 3:
            problems.append(f"{key} must list exactly three seats")
            continue
        seen: set[tuple[str, str]] = set()
        for number, seat in enumerate(seats, 1):
            where = f"{label} seat {number}"
            if not isinstance(seat, dict) or set(seat) != SEAT_KEYS:
                problems.append(f"{where} needs exactly endpoint and model: one preferred model, no fallback list")
                continue
            name, model = seat["endpoint"], seat["model"]
            if not all(isinstance(value, str) and value for value in (name, model)):
                problems.append(f"{where} needs one endpoint name and one model id")
                continue
            entry = endpoint(name)
            terms = entry.get("modelle_terms")
            if not entry:
                problems.append(f"{where}: endpoint {name} is not declared")
            elif model not in (entry.get("modelle") or []) and not (isinstance(terms, dict) and model in terms):
                problems.append(f"{where}: {name}/{model} is not declared")
            if model.endswith("-free"):
                problems.append(f"{where}: a -free model never fills a seat")
            if label == "online" and name != "opencode-go":
                problems.append(f"{where}: online seats run on opencode-go")
            if label == "repository" and entry:
                allowed = entry.get("darf_sehen")
                residency = entry.get("residenz")
                if not isinstance(allowed, list) or "framework" not in allowed:
                    problems.append(f"{where}: endpoint {name} may not see framework content")
                if not isinstance(residency, str) or not residency.strip() or residency == "nicht-erklaert":
                    problems.append(f"{where}: endpoint {name} states no data residency")
            if (name, model) in seen:
                problems.append(f"{where}: {name}/{model} already fills another seat of the trio")
            seen.add((name, model))
    problems.extend(rule_problem(block.get("availability_preflight"), wire_apis=True))
    return problems


# ---------------------------------------------------------------------------


def _git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    return done.stdout if done.returncode == 0 else ""


def tracked_paths(root: Path) -> set[str]:
    return {path for path in _git(root, "ls-files", "-z").split("\0") if path}


# ---------------------------------------------------------------------------
# The public call and its receipts
# ---------------------------------------------------------------------------


def public_env(own: dict[str, str]) -> dict[str, str]:
    """Only executable lookup is inherited; home/config/credential paths belong to this scratch run."""
    return {**({"PATH": os.environ["PATH"]} if "PATH" in os.environ else {}), **own}


def parse_receipts(text: str) -> list[dict]:
    """The receipt JSON lines, skipping lines that do not parse."""
    parsed: list[dict] = []
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict):
            parsed.append(event)
    return parsed


def run(root: Path, change: str, runner, klass: str, selection: dict) -> None:
    """The whole phase-1 research run (`stage2_research_run`); raises the runner's Refused (2) or CallFailed (1)."""
    import stage2_research_run

    stage2_research_run.run(root, change, runner, klass, selection)
