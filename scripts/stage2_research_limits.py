"""The checked-in time limits of the phase-1 research swarm (bead coding-harness-ht1b).

`research-swarm-limits.yaml` at a worktree root carries the whole-run allowance
(`run_minutes`) and the five role allowances (`role_minutes.finders`, `.merge`,
`.sentence`, `.topics`, `.judge`) in minutes. `load` reads that file for the
supplied repository root and validates it strictly: the exact schema, positive
finite numbers, every role at or below the run and the judge strictly below it.
An unusable document raises `LimitsError` naming the path and the fault — never
a default. The run reads the file once per invocation at `Run.open`; there is
no cache and no second source of values.
"""

from __future__ import annotations

import dataclasses
import math
from pathlib import Path

import yaml

FILE_NAME = "research-swarm-limits.yaml"
RUN_KEY = "run_minutes"
ROLE_KEY = "role_minutes"
ROLES = ("finders", "merge", "sentence", "topics", "judge")


class LimitsError(ValueError):
    """The limits document is unreadable or unusable; the message names the path and the fault."""


class _UniqueKeyLoader(yaml.SafeLoader):
    """A safe loader that refuses a repeated key instead of letting the last one silently win."""

    def construct_mapping(self, node, deep: bool = False):
        seen: set = set()
        for key_node, _value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise LimitsError(f"mapping key {key!r} is not a name")
            if key in seen:
                raise LimitsError(f"the key '{key}' appears more than once")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


@dataclasses.dataclass(frozen=True)
class Limits:
    """One invocation's captured allowances in minutes, with their seconds conversions."""

    run_minutes: float
    role_minutes: dict[str, float]

    @property
    def run_seconds(self) -> float:
        return self.run_minutes * 60.0

    def role_seconds(self, role: str) -> float:
        """The role's allowance in seconds; `role` is one of `ROLES`."""
        return self.role_minutes[role] * 60.0


def _number(path: Path, value: object, name: str) -> float:
    """One allowance in minutes: a positive finite number, never a bool, text, null or container."""
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise LimitsError(f"{path}: {name} must be a number of minutes, found {value!r}")
    try:
        number = float(value)
    except OverflowError as error:
        raise LimitsError(f"{path}: {name} is too large for a number of minutes ({error})") from error
    if not math.isfinite(number) or number <= 0.0:
        raise LimitsError(f"{path}: {name} must be a positive finite number of minutes, found {value!r}")
    if not math.isfinite(number * 60.0):
        raise LimitsError(f"{path}: {name} ({value!r}) converts to seconds beyond the representable range")
    return number


def load(root: Path) -> Limits:
    """Read, validate and return the limits of the repository at `root`; raise `LimitsError` otherwise."""
    path = Path(root) / FILE_NAME
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise LimitsError(f"{path}: the limits file cannot be read ({error})") from error
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise LimitsError(f"{path}: the limits file is not valid UTF-8 ({error})") from error
    try:
        document = yaml.load(text, Loader=_UniqueKeyLoader)
    except LimitsError as error:
        raise LimitsError(f"{path}: {error}") from error
    except yaml.YAMLError as error:
        raise LimitsError(f"{path}: the limits file is not valid YAML ({error})") from error
    if not isinstance(document, dict):
        raise LimitsError(f"{path}: the limits document must be a mapping, found {type(document).__name__}")
    missing = [key for key in (RUN_KEY, ROLE_KEY) if key not in document]
    unknown = sorted(str(key) for key in document if key not in (RUN_KEY, ROLE_KEY))
    if missing:
        raise LimitsError(f"{path}: the limits document is missing {', '.join(missing)}")
    if unknown:
        raise LimitsError(f"{path}: the limits document carries unknown key(s) {', '.join(unknown)}")
    run_minutes = _number(path, document[RUN_KEY], RUN_KEY)
    roles = document[ROLE_KEY]
    if not isinstance(roles, dict):
        raise LimitsError(f"{path}: {ROLE_KEY} must be a mapping of {', '.join(ROLES)}")
    missing = [role for role in ROLES if role not in roles]
    unknown = sorted(str(key) for key in roles if key not in ROLES)
    if missing:
        raise LimitsError(f"{path}: {ROLE_KEY} is missing {', '.join(missing)}")
    if unknown:
        raise LimitsError(f"{path}: {ROLE_KEY} carries unknown role(s) {', '.join(unknown)}")
    role_minutes = {role: _number(path, roles[role], f"{ROLE_KEY}.{role}") for role in ROLES}
    for role, minutes in role_minutes.items():
        if minutes > run_minutes:
            raise LimitsError(f"{path}: {ROLE_KEY}.{role} ({minutes:g}) must not exceed {RUN_KEY} ({run_minutes:g})")
    judge = role_minutes["judge"]
    if judge >= run_minutes:
        raise LimitsError(
            f"{path}: {ROLE_KEY}.judge ({judge:g}) must stay strictly below {RUN_KEY} ({run_minutes:g})",
        )
    return Limits(run_minutes=run_minutes, role_minutes=role_minutes)
