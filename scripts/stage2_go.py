"""The one address policy for every runner-controlled OpenCode Go launch.

Every Go launch — review loop, research swarm, availability probe and the
interactive session — assesses its effective destination against the single
`adresse` record on the `opencode-go` entry of `model-endpoints.yaml`
(bead coding-harness-4tr4, decisions Q-1/Q-2/Q-5). A different path on the
admitted host runs on with a notice; any other destination is refused before
a model request.

The record is data, never a code default: a missing, unreadable or ambiguous
record fails closed, and no literal base, host or cached policy exists in
this module. The record holds no credentials and no model permissions — it
admits an address alone, and every other restriction keeps applying.

Record shape (field names follow `model-endpoints.yaml`'s German keys beside
English technical terms, dated sources per value, as `modelle_terms` does):
    adresse:
      host: opencode.ai
      apis:
        openai-completions:
          basis: "https://opencode.ai/inference/go/openai/v1"
          quelle: "https://opencode.ai/docs/go (the Go page)"
          gelesen: "2026-10-31"
"""

from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

import yaml

PROVIDER = "opencode-go"

# The record's known keys. An unknown key refuses the record: a typo would
# otherwise silently deactivate part of the policy (fail closed, criterion 8).
ADDRESS_KEYS = ("host", "apis")
BASE_KEYS = ("basis", "quelle", "gelesen")

_API = re.compile(r"[a-z0-9][a-z0-9-]*")
_DATE_ONLY = re.compile(r"\d{4}-\d{2}-\d{2}")
# A DNS hostname: dot-separated labels of letters, digits and inner hyphens,
# no whitespace, no scheme, no port, no path, no trailing dot.
_HOST = re.compile(r"[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)*")


class RecordUnusable(Exception):
    """The address record is missing, unreadable or malformed; Go admission fails closed."""


class DestinationRefused(Exception):
    """One model's destination is refused by the policy; the model is named and no request starts.

    This is one row's outcome, not the operation's: a probe or a selection
    marks the model refused and carries on, while an unusable record
    (`RecordUnusable`) stops the whole operation.
    """


@dataclass(frozen=True)
class BaseRecord:
    """One wire API's known base, with the source it was read from and when."""

    api: str
    base: str
    source: str
    read: str


@dataclass(frozen=True)
class AddressPolicy:
    """The admitted host and its per-wire-API known bases, as the record states them."""

    host: str
    apis: dict[str, BaseRecord]

    def default_base(self, api: str | None) -> str | None:
        """The recorded base for a wire API, or None when unmapped — never a guessed default."""
        if not isinstance(api, str) or api not in self.apis:
            return None
        return self.apis[api].base

    def recorded_path(self, api: str | None) -> str | None:
        """The known base's path for a wire API, or None when unmapped."""
        if not isinstance(api, str) or api not in self.apis:
            return None
        return urlsplit(self.apis[api].base).path


@dataclass(frozen=True)
class Assessment:
    """The outcome of one destination assessment.

    `definition` is the effective definition with an explicit base; `notice`
    names a same-host path move; `problem` is the sanitised refusal reason.
    Exactly one of `notice` and `problem` reasons a departure from the record;
    an admitted definition on the recorded path carries neither.
    """

    definition: dict
    notice: str | None = None
    problem: str | None = None

    @property
    def admitted(self) -> bool:
        return self.problem is None


class _NoDuplicateLoader(yaml.SafeLoader):
    """A safe loader that refuses duplicate mapping keys instead of silently keeping the last."""


def _construct_mapping(loader: yaml.SafeLoader, node: yaml.Node, deep: bool = False) -> dict:
    loader.flatten_mapping(node)
    mapping: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            hash(key)
        except TypeError as error:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark, "found an unhashable key", key_node.start_mark
            ) from error
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark, f"found duplicate key {key!r}", key_node.start_mark
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_NoDuplicateLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def _read_date(value: object, field: str) -> str:
    """The field's quoted ISO calendar date, or a RecordUnusable naming the field.

    The declared-dates rule of the terms machinery applies unchanged: a YAML-
    native date, a timestamp or a malformed date is refused, never repaired.
    """
    if not isinstance(value, str) or not _DATE_ONLY.fullmatch(value):
        raise RecordUnusable(f"the address record's {field} is not a quoted ISO date YYYY-MM-DD")
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        raise RecordUnusable(f"the address record's {field} is not a valid calendar date") from None
    return value


def _record_problem(text: str) -> AddressPolicy:
    """Validate the raw `adresse` mapping and return the policy it declares."""
    if not isinstance(text, dict):
        raise RecordUnusable("the address record (adresse) is missing or not a mapping")
    unknown = sorted(str(key) for key in text if key not in ADDRESS_KEYS)
    if unknown:
        raise RecordUnusable(f"the address record carries unknown keys: {', '.join(unknown)}")
    host = text.get("host")
    if not isinstance(host, str) or not _HOST.fullmatch(host.lower()) or len(host) > 253:
        raise RecordUnusable("the address record's host is not a plain DNS hostname")
    apis = text.get("apis")
    if not isinstance(apis, dict) or not apis:
        raise RecordUnusable("the address record's apis is missing, empty or not a mapping")
    records: dict[str, BaseRecord] = {}
    for api, record in apis.items():
        if not isinstance(api, str) or not _API.fullmatch(api):
            raise RecordUnusable(f"the address record's api name {api!r} is not a plain wire-api name")
        if not isinstance(record, dict):
            raise RecordUnusable(f"the address record for {api} is not a mapping")
        unknown = sorted(str(key) for key in record if key not in BASE_KEYS)
        if unknown:
            raise RecordUnusable(f"the address record for {api} carries unknown keys: {', '.join(unknown)}")
        base = record.get("basis")
        if not isinstance(base, str):
            raise RecordUnusable(f"the address record for {api} has no explicit base (basis)")
        problem = url_problem(base, host)
        if problem:
            raise RecordUnusable(f"the address record for {api} has an unusable base: {problem}")
        path = urlsplit(base).path
        if path in ("", "/"):
            raise RecordUnusable(f"the address record for {api} has no known path in its base")
        source = record.get("quelle")
        if not isinstance(source, str) or not source.strip():
            raise RecordUnusable(f"the address record for {api} has no documentation source (quelle)")
        read = _read_date(record.get("gelesen"), f"gelesen for {api}")
        records[api] = BaseRecord(api=api, base=base, source=source.strip(), read=read)
    return AddressPolicy(host=host.lower(), apis=records)


def load_address_policy(root: Path) -> AddressPolicy:
    """The one address policy, read fresh from the held `model-endpoints.yaml` at call time.

    The document is parsed with the duplicate-rejecting loader: a duplicate
    key never reaches validation with one of its values silently lost. Any
    unusable state — an unreadable file, duplicate keys, no or several
    `opencode-go` entries, a malformed record — raises `RecordUnusable`;
    no literal default or cached policy stands in for it.
    """
    path = root / "model-endpoints.yaml"
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        raise RecordUnusable(f"{path.name} cannot be read; the Go address record is unavailable") from None
    try:
        data = yaml.load(text, Loader=_NoDuplicateLoader) or {}
    except yaml.YAMLError as error:
        raise RecordUnusable(f"{path.name} is not readable YAML: {error}") from None
    entries = data.get("endpunkte") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise RecordUnusable(f"{path.name} declares no endpoints list; the Go address record is unavailable")
    named = [entry for entry in entries if isinstance(entry, dict) and entry.get("name") == PROVIDER]
    if len(named) != 1:
        raise RecordUnusable(
            f"{path.name} declares {len(named)} entries named {PROVIDER}; the address record must be unique"
        )
    return _record_problem(named[0].get("adresse"))


def definition_of(store: object, provider: str, model: str) -> dict | None:
    """The one definition of `model` in the store's provider entry, or None.

    None covers a missing entry, a missing row and an ambiguous one alike:
    a duplicated id never names which row a launch assessed, so it is
    unusable rather than a choice (fail closed).
    """
    entry = store.get(provider) if isinstance(store, dict) else None
    models = entry.get("models") if isinstance(entry, dict) else None
    if not isinstance(models, list):
        return None
    found = [item for item in models if isinstance(item, dict) and item.get("id") == model]
    return found[0] if len(found) == 1 else None


def _has_control_or_backslash(value: str) -> bool:
    return any(ord(char) < 0x20 or ord(char) == 0x7F or char == "\\" for char in value)


def url_problem(value: object, host: str) -> str | None:
    """Why the value is not an unambiguous HTTPS URL on the admitted host, or None.

    Strict forms only: HTTPS, the admitted host (case-insensitive), the
    default port — explicit 443 tolerated — no userinfo, query, fragment,
    control character or backslash, and a parseable authority. The path is
    free: a same-host path move is admissible with a notice, not a refusal.
    The reason names the structural fault alone and never echoes the value,
    so a credential-bearing URL cannot enter a diagnostic.
    """
    if not isinstance(value, str) or not value:
        return "the base is missing or not a string"
    if _has_control_or_backslash(value):
        return "the base carries a control character or backslash"
    try:
        parts = urlsplit(value)
    except ValueError:
        return "the base does not parse as a URL"
    if parts.scheme != "https":
        return "the base is not HTTPS"
    hostname = parts.hostname
    if not hostname or hostname.lower() != host.lower():
        return "the base's host is not the admitted host"
    try:
        port = parts.port
    except ValueError:
        return "the base's authority does not parse"
    if port is not None and port != 443:
        return "the base names a non-default port"
    if parts.username is not None or parts.password is not None:
        return "the base carries userinfo"
    if parts.query:
        return "the base carries a query"
    if parts.fragment:
        return "the base carries a fragment"
    return None


def _same_path(left: str | None, right: str | None) -> bool:
    """Whether two base paths are the same, tolerating one trailing slash."""
    if left is None or right is None:
        return False
    trim = lambda path: path[:-1] if len(path) > 1 and path.endswith("/") else path  # noqa: E731
    return trim(left) == trim(right)


def assess(policy: AddressPolicy, model: str, definition: object) -> Assessment:
    """Assess one Go model definition against the policy; the one check every launch shares.

    The effective definition keeps an explicit base: an absent base is filled
    from the record for the definition's resolved wire API, and an unmapped
    API has no default — the definition is refused rather than guessed at.
    A base on the admitted host under another path is admitted with a move
    notice naming model, recorded path and observed path; every other
    destination is refused with a sanitised reason before any model request.
    A mapping in the record grants no model admission: terms, wire-API and
    every other restriction stay with their own checks.
    """
    if not isinstance(definition, dict):
        return Assessment({}, problem=f"the model {model} has no usable definition")
    api = definition.get("api")
    if api is not None and not isinstance(api, str):
        return Assessment({}, problem=f"the model {model} has an unreadable wire api")
    base = definition.get("baseUrl")
    if "baseUrl" in definition and not isinstance(base, str):
        return Assessment({}, problem=f"the model {model} has an unreadable base")
    if base is None:
        filled = policy.default_base(api)
        if filled is None:
            return Assessment(
                {},
                problem=(
                    f"the model {model} declares no base and its wire api has no recorded base"
                    if api is not None
                    else f"the model {model} declares neither a base nor a wire api"
                ),
            )
        base = filled
    problem = url_problem(base, policy.host)
    if problem:
        return Assessment({}, problem=f"the model {model} is refused: {problem}")
    recorded = policy.recorded_path(api)
    observed = urlsplit(base).path
    # Without a mapped api there is no recorded path to have moved from; the
    # explicit on-host base is then admitted as it stands, no notice invented.
    if recorded is None or _same_path(recorded, observed):
        return Assessment({**definition, "baseUrl": base})
    return Assessment(
        {**definition, "baseUrl": base},
        notice=(
            f"{PROVIDER}/{model}: the recorded base path is {recorded}, the definition names {observed}; "
            "running on with this same-host move"
        ),
    )
