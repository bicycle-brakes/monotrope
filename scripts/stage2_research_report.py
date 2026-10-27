"""Pure structured topic reports and bounded runner-resolved claim evidence.

This helper never reads a file, starts a model, resolves DNS or reads a
tracker. The runner supplies frozen sources and each seat's own receipts.
"""

from __future__ import annotations

import copy
import ipaddress
import json
import re
from datetime import datetime
from urllib.parse import quote, urlsplit

from stage2_research_refs import resolve_research_reference


class ResearchReportError(ValueError):
    """A failed topic contribution; retain raw output and stop required completion."""

    exit_code = 1


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ResearchReportError("duplicate report JSON key")
        result[key] = value
    return result


def _constant(_value):
    raise ResearchReportError("non-finite report JSON value")


def _load(value):
    try:
        raw = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, allow_nan=False)
        raw.encode("utf-8")
        parsed = json.loads(raw, object_pairs_hook=_object, parse_constant=_constant)
        json.dumps(parsed, ensure_ascii=False, allow_nan=False).encode("utf-8")
        return parsed
    except (TypeError, ValueError, UnicodeError, RecursionError) as error:
        raise ResearchReportError("invalid report JSON") from error


def _keys(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= set(value) or set(value) - set(required) - set(optional):
        raise ResearchReportError("report fields do not match the template")


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _strings(value):
    return isinstance(value, list) and all(_text(item) for item in value)


def _links(value, local_ids):
    if not _strings(value) or not value or len(set(value)) != len(value) or not set(value) <= local_ids:
        raise ResearchReportError("report links need unique existing local claim ids")


def research_seat_id(endpoint, model):
    """Encode trusted endpoint/model components without namespace collisions."""
    if not _text(endpoint) or not _text(model):
        raise ResearchReportError("invalid endpoint/model identity")
    try:
        return quote(endpoint, safe="") + ":" + quote(model, safe="")
    except UnicodeError as error:
        raise ResearchReportError("invalid endpoint/model identity") from error


def _public_url(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
        host = parsed.hostname
        if (
            parsed.scheme != "https"
            or not host
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port not in (None, 443)
        ):
            return False
        if host == "localhost" or host.endswith((".localhost", ".local")):
            return False
        try:
            return ipaddress.ip_address(host).is_global
        except ValueError:
            return True
    except ValueError:
        return False


def _page_reference(citation, receipts):
    if not _public_url(citation):
        return None
    for receipt in receipts:
        if (
            not isinstance(receipt, dict)
            or receipt.get("kind") != "fetch"
            or type(receipt.get("status")) is not int
            or receipt["status"] != 200
        ):
            continue
        if citation not in (receipt.get("url"), receipt.get("final_url")):
            continue
        if not _public_url(receipt.get("url")) or not _public_url(receipt.get("final_url")):
            continue
        if not isinstance(receipt.get("excerpt"), str) or not isinstance(receipt.get("title"), str):
            continue
        try:
            retrieved = datetime.fromisoformat(receipt["retrieved"])
            if retrieved.tzinfo is None:
                continue
            evidence = {key: receipt[key] for key in ("url", "final_url", "status", "title", "retrieved", "excerpt")}
            excerpt = json.dumps(evidence, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
            excerpt.encode("utf-8")
        except (KeyError, TypeError, ValueError, UnicodeError):
            continue
        return {"citation": citation, "kind": "page", "supported": True, "excerpt": excerpt}
    return None


def _reference(citation, topic, sources, history, receipts):
    missing = {"citation": citation, "supported": False, "reason": "no runner evidence"}
    if topic >= 9:
        return _page_reference(citation, receipts) or missing
    if "::" in citation:
        path, reference = citation.split("::", 1)
        return {"citation": citation, "kind": "local", **resolve_research_reference(sources, path, reference)}
    if topic == 6 and re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", citation):
        commits = history.get("commits", {}) if isinstance(history, dict) else {}
        record = commits.get(citation) if isinstance(commits, dict) else None
        if isinstance(record, dict) and record.get("hash") == citation:
            try:
                excerpt = json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
                excerpt.encode("utf-8")
            except (ValueError, TypeError, UnicodeError):
                return missing
            return {"citation": citation, "kind": "commit", "supported": True, "excerpt": excerpt}
    return missing


def _evidence(citations, topic, sources, history, receipts):
    references = [_reference(item, topic, sources, history, receipts) for item in citations]
    valid = bool(references) and all(item["supported"] for item in references)
    if not valid:
        return "unsupported", [{key: value for key, value in item.items() if key != "excerpt"} for item in references]
    remaining = 4000
    for item in references:
        excerpt = item["excerpt"]
        item["excerpt"] = excerpt[:remaining]
        item["truncated"] = len(excerpt) > remaining
        remaining -= len(item["excerpt"])
    return "valid", references


def validate_research_report(raw, *, run_id, topic, seat, sources, history=None, receipts=(), neighbours=()):
    """Validate one raw report without consulting peer reports or a judge.

    The caller supplies trusted run/topic/endpoint-qualified seat identities.
    Questions keep links to unsupported claims: later judgement never erases
    raw human decisions. Only empty-neighbour topic 5 waives the claim floor.
    """
    identity = r"[A-Za-z0-9][A-Za-z0-9._:%+-]*"
    component = r"(?:[A-Za-z0-9._~-]|%[0-9A-F]{2})+"
    if (
        type(topic) is not int
        or topic not in range(1, 12)
        or not isinstance(run_id, str)
        or not re.fullmatch(identity, run_id)
        or not isinstance(seat, str)
        or not re.fullmatch(component + ":" + component, seat)
    ):
        raise ResearchReportError("invalid trusted report identity")
    if (
        not isinstance(neighbours, list | tuple)
        or any(not _text(path) for path in neighbours)
        or len(set(neighbours)) != len(neighbours)
    ):
        raise ResearchReportError("invalid trusted neighbour packet")
    if topic >= 9 and neighbours:
        raise ResearchReportError("online report receives no neighbour identities")
    value = _load(raw)
    required = {"claims", "counter_evidence", "not_read", "neighbour_relation", "questions"}
    if topic == 3:
        required.add("class_assessment")
    if topic == 5:
        required.add("neighbour_relations")
    _keys(value, required)
    if (
        not _strings(value["counter_evidence"])
        or not _strings(value["not_read"])
        or not _text(value["neighbour_relation"])
    ):
        raise ResearchReportError("report needs counter-evidence, unread and neighbour fields")
    if topic >= 9 and value["neighbour_relation"] != "not-assessable":
        raise ResearchReportError("online neighbour relation must be not-assessable")
    claims, questions = value["claims"], value["questions"]
    if not isinstance(claims, list) or len(claims) > 7 or not isinstance(questions, list):
        raise ResearchReportError("invalid claims/questions template")
    claim_ids = set()
    for claim in claims:
        fields = {"id", "statement", "kind", "evidence", "confidence", "basis"}
        if topic == 6:
            fields.add("volatile")
        _keys(claim, fields, {"governance"} if topic == 6 else ())
        local = claim["id"]
        if not isinstance(local, str) or not re.fullmatch(r"C[1-7]", local) or local in claim_ids:
            raise ResearchReportError("invalid or duplicate local claim id")
        claim_ids.add(local)
        if (
            not all(_text(claim[key]) for key in ("statement", "confidence", "basis"))
            or claim["kind"] not in ("fact", "assumption", "judgement")
            or not _strings(claim["evidence"])
        ):
            raise ResearchReportError("invalid claim template")
        if topic == 6 and (
            type(claim["volatile"]) is not bool
            or (claim["volatile"] and claim.get("governance") not in ("central", "runtime", "dated"))
            or ("governance" in claim and claim["governance"] not in ("central", "runtime", "dated"))
        ):
            raise ResearchReportError("volatile claim requires a governance proposal")
    question_ids = set()
    for question in questions:
        _keys(question, {"id", "question", "classification", "claims"})
        local = question["id"]
        if (
            not isinstance(local, str)
            or not re.fullmatch(r"Q[1-9][0-9]*", local)
            or local in question_ids
            or not _text(question["question"])
            or question["classification"] not in ("[DECISION]", "[GAP]", "[DETAIL]")
        ):
            raise ResearchReportError("invalid or duplicate report question")
        question_ids.add(local)
        _links(question["claims"], claim_ids)
    if topic == 3:
        assessment = value["class_assessment"]
        _keys(assessment, {"class", "claims"})
        if assessment["class"] not in ("bounded", "spike", "feature", "architectural"):
            raise ResearchReportError("invalid class assessment")
        _links(assessment["claims"], claim_ids)
    if topic == 5:
        relations = value["neighbour_relations"]
        if not isinstance(relations, list):
            raise ResearchReportError("invalid neighbour relations")
        seen = set()
        for relation in relations:
            _keys(relation, {"path", "relation", "claims"})
            path = relation["path"]
            if (
                not _text(path)
                or path not in neighbours
                or path in seen
                or relation["relation"] not in ("related", "unrelated", "contradicts")
            ):
                raise ResearchReportError("invalid or duplicate neighbour relation")
            seen.add(path)
            _links(relation["claims"], claim_ids)
        if seen != set(neighbours):
            raise ResearchReportError("neighbour relations differ from the packet")
        if not neighbours and "no packet neighbour" not in value["not_read"]:
            raise ResearchReportError("empty neighbour packet needs its exact not-read marker")
    prefix = f"{run_id}/{topic}/{seat}/"
    result = {"raw": copy.deepcopy(value), "run_id": run_id, "topic": topic, "seat": seat, **copy.deepcopy(value)}
    result["claims"] = []
    for claim in claims:
        status, resolved = _evidence(claim["evidence"], topic, sources, history, receipts)
        result["claims"].append(
            {
                **copy.deepcopy(claim),
                "local_id": claim["id"],
                "id": prefix + claim["id"],
                "evidence_status": status,
                "resolved": resolved,
            }
        )
    if not any(claim["evidence_status"] == "valid" for claim in result["claims"]) and not (
        topic == 5 and not neighbours
    ):
        raise ResearchReportError("report has no runner-backed evidence claim")
    result["questions"] = [
        {
            **copy.deepcopy(item),
            "local_id": item["id"],
            "id": prefix + item["id"],
            "claims": [prefix + local for local in item["claims"]],
        }
        for item in questions
    ]
    for key in ("class_assessment", "neighbour_relations"):
        if key not in result:
            continue
        items = result[key] if isinstance(result[key], list) else [result[key]]
        for item in items:
            item["claims"] = [prefix + local for local in item["claims"]]
    return result
