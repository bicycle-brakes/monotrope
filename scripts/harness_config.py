"""The one reader and renderer of the central harness configuration (ADR 0026).

`config/harness/` holds the harness's migrated settings, one small YAML file
per topic. This module is the shared contract every consumer goes through:

* `load(root)` validates every topic file against the one schema of this
  module and returns an immutable snapshot together with the bytes it read.
  No global cache, no environment overlay, no fallback default: an unusable
  file raises `HarnessConfigError` naming the file and the reason.
* `render(snapshot, text, source)` substitutes the reserved text placeholders
  `{{ harness.<dotted-key> }}` from one snapshot. It is a plain text
  substitution, never a template language: an unknown or malformed token is
  refused, and nothing inside a token is ever evaluated.
* `REQUIRED_BINDINGS` and `OWNED_NAMES` are the checker's inventory of where
  the owned settings must stay visible. They hold paths and key references,
  never setting values.

The schema gains a typed topic only when that topic's consumers migrate;
until then their settings keep their existing sources (design.md, migration
order).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

CONFIG_DIRNAME = Path("config") / "harness"


class HarnessConfigError(Exception):
    """A configuration file is missing, unreadable, ambiguous or invalid.

    `path` names the offending file when the refusal is about one; `reason`
    always carries what is wrong. The message is the full diagnostic a
    consumer shows.
    """

    def __init__(self, path: Path | None, reason: str) -> None:
        self.path = path
        self.reason = reason
        super().__init__(f"{path}: {reason}" if path is not None else reason)


class _StrictnessError(Exception):
    """A YAML mapping uses a construct the shared contract refuses."""


_MERGE_TAG = "tag:yaml.org,2002:merge"


class _StrictLoader(yaml.SafeLoader):
    """`SafeLoader` plus the ambiguity refusals of the shared contract."""


def _construct_mapping(loader: yaml.SafeLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    """Refuse merge keys and duplicate keys before any mapping is built.

    PyYAML would silently fold `<<:` merges and keep the last of duplicate
    keys, so a document could mean two things and readers could disagree; the
    contract wants one readable meaning or a refusal.
    """
    seen: list[object] = []
    for key_node, _ in node.value:
        if key_node.tag == _MERGE_TAG:
            raise _StrictnessError("merge keys (`<<:`) are not allowed")
        marker = key_node.value if isinstance(key_node, yaml.ScalarNode) else id(key_node)
        if marker in seen:
            raise _StrictnessError(f"duplicate key {key_node.value!r}")
        seen.append(marker)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


_StrictLoader.add_constructor("tag:yaml.org,2002:map", _construct_mapping)


class LaneSettings(BaseModel):
    """The lane topic; the writing-session count is its only owned setting so far."""

    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    writing_sessions_per_repository: int = Field(..., gt=0)


class HarnessConfig(BaseModel):
    """The one schema of `config/harness/`; a topic joins it when its consumers migrate."""

    model_config = ConfigDict(strict=True, frozen=True, extra="forbid")

    lanes: LaneSettings


@dataclass(frozen=True)
class HarnessSnapshot:
    """One captured configuration: the validated values and the bytes they were read from.

    The snapshot is immutable on purpose: an edit to the files after it was
    captured cannot change a composition that already holds it, and the next
    composition captures its own.
    """

    config: HarnessConfig
    sources: tuple[tuple[Path, bytes], ...]


# Each topic file, with the schema field it fills. The file-to-topic mapping
# is part of the shared contract.
TOPICS: dict[str, tuple[type[BaseModel], str]] = {"lanes.yaml": (LaneSettings, "lanes")}


def _parse_topic(path: Path, raw: bytes) -> object:
    """One topic file's bytes as parsed YAML, or the refusal naming file and reason."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HarnessConfigError(path, "is not valid UTF-8") from None
    try:
        return yaml.load(text, Loader=_StrictLoader)
    except _StrictnessError as error:
        raise HarnessConfigError(path, str(error)) from None
    except yaml.YAMLError as error:
        raise HarnessConfigError(path, f"malformed YAML ({error})") from None


def _validation_reason(error: ValidationError) -> str:
    """The first schema failure as `key: message`, for the diagnostic of one file."""
    first = error.errors()[0]
    key = ".".join(str(part) for part in first.get("loc", ()))
    return f"{key}: {first['msg']}" if key else first["msg"]


def load(root: Path) -> HarnessSnapshot:
    """Read, validate and freeze every topic file under `root/config/harness/`.

    An unknown entry in the directory is refused like a bad topic: the schema,
    not the directory listing, decides what configuration exists.
    """
    directory = root / CONFIG_DIRNAME
    if not directory.is_dir():
        raise HarnessConfigError(directory, "the central configuration directory is missing")
    values: dict[str, BaseModel] = {}
    sources: list[tuple[Path, bytes]] = []
    for path in sorted(directory.iterdir()):
        model_and_field = TOPICS.get(path.name) if path.is_file() else None
        if model_and_field is None:
            reason = (
                "unknown topic: not a regular file"
                if not path.is_file()
                else (f"unknown topic; known topics: {', '.join(sorted(TOPICS))}")
            )
            raise HarnessConfigError(path, reason)
        model, field = model_and_field
        try:
            raw = path.read_bytes()
        except OSError as error:
            raise HarnessConfigError(path, f"cannot be read ({error.strerror or error})") from None
        try:
            values[field] = model.model_validate(_parse_topic(path, raw))
        except ValidationError as error:
            raise HarnessConfigError(path, _validation_reason(error)) from None
        sources.append((path, raw))
    try:
        config = HarnessConfig(**values)
    except ValidationError as error:
        raise HarnessConfigError(directory, _validation_reason(error)) from None
    return HarnessSnapshot(config=config, sources=tuple(sources))


# --- Reserved placeholders -------------------------------------------------
#
# `{{ harness.<dotted-key> }}` is a reserved text substitution of the runner,
# not a template language. KEY is a well-formed dotted key, TOKEN the full
# well-formed spelling, CANDIDATE every `{{ harness... }}` a reader must
# judge, and RESERVED_PREFIX finds tokens a substitution left behind.

_KEY_SOURCE = r"[a-z0-9_]+(?:\.[a-z0-9_]+)+"
RESERVED_PREFIX = re.compile(r"\{\{\s*harness\b")
KEY = re.compile(_KEY_SOURCE)
TOKEN = re.compile(r"\{\{\s*harness\.(" + _KEY_SOURCE + r")\s*\}\}")
CANDIDATE = re.compile(r"\{\{\s*harness\.?([^{}]*?)\s*\}\}")


def lookup(config: HarnessConfig | HarnessSnapshot, dotted: str) -> object:
    """The one scalar value at `dotted`, or the refusal naming the unknown key.

    The walk goes through the declared schema fields only: a token can never
    reach an attribute the schema does not own, and nothing is evaluated.
    """
    node: object = config.config if isinstance(config, HarnessSnapshot) else config
    for part in dotted.split("."):
        if not isinstance(node, BaseModel):
            raise HarnessConfigError(None, f"{dotted}: {part} would read below a scalar value")
        if part not in type(node).model_fields:
            known = ", ".join(sorted(type(node).model_fields))
            raise HarnessConfigError(None, f"{dotted}: unknown setting; known keys: {known}")
        node = getattr(node, part)
    if isinstance(node, BaseModel) or not isinstance(node, int | str):
        raise HarnessConfigError(None, f"{dotted}: only a scalar value renders")
    return node


def render(snapshot: HarnessSnapshot, text: str, source: str = "") -> str:
    """Substitute the reserved tokens of one text from one captured snapshot.

    `source` names the text's file in the diagnostic; a malformed or unknown
    token refuses, nothing inside a token is evaluated, and no reserved token
    survives in the returned text.
    """
    where = f"{source}: " if source else ""

    def substitute(match: re.Match[str]) -> str:
        dotted = (match.group(1) or "").strip()
        if not KEY.fullmatch(dotted):
            form = "{{ harness.<dotted-key> }}"
            raise HarnessConfigError(None, f"{where}malformed reserved token {match.group(0)!r}; the form is {form}")
        try:
            return str(lookup(snapshot, dotted))
        except HarnessConfigError as error:
            raise HarnessConfigError(None, f"{where}{error.reason}") from None

    rendered = CANDIDATE.sub(substitute, text)
    leftover = RESERVED_PREFIX.search(rendered)
    if leftover:
        fragment = rendered[leftover.start() : leftover.start() + 40]
        raise HarnessConfigError(None, f"{where}a reserved token was not resolved: {fragment!r}")
    return rendered


# --- Marked literals in hand-written prose ---------------------------------
#
# A marker links one readable value to one owned setting so the drift check
# can compare them. It is a statement about prose, never a second authority.

MARKER_OPEN = re.compile(r"<!--\s*harness-config:")
MARKER = re.compile(r"<!--\s*harness-config:\s*(" + _KEY_SOURCE + r")\s*-->([^<>]*)<!--\s*/harness-config\s*-->")

# Where each owned setting must stay visible. Paths are relative to the
# repository root; the checker holds this inventory, so deleting the marker
# or the placeholder cannot waive it. OWNED_NAMES are the canonical and
# uppercase spellings a live numeric declaration may use.
REQUIRED_BINDINGS: tuple[tuple[str, str, str], ...] = (
    ("prompts/04-implement.md", "lanes.writing_sessions_per_repository", "placeholder"),
    ("AGENTS.md", "lanes.writing_sessions_per_repository", "marker"),
)
OWNED_NAMES: tuple[str, ...] = ("writing_sessions_per_repository", "WRITING_SESSIONS_PER_REPOSITORY")
