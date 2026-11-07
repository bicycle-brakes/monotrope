"""The one free-model selection rule of the review loop and the research swarm.

Both swarms select free OpenCode Go models from a fresh catalog. The rule that decides which catalog ids
may become free members lives here and nowhere else: provider, fresh-catalog membership, a plain model id,
the policy's suffix, include and exclude lists, the hard vetoes (a global exclusion of the declaration and
paid admission) and the destination of the fresh definition. A caller translates its own policy format
into `Policy` and its own eligibility evidence into `Candidate.problem`; it keeps its catalog order,
reporting and capability checks.

An id the endpoint also admits as paid (`modelle`) is never a free member, whatever its name ends in: the
free class is admitted by class, the paid class by a dated reading of its terms, and the two never meet
(bead coding-harness-wb40, after coding-harness-vku6).

This module performs no I/O, network call, catalog refresh, probe or credential lookup. It imports only
`stage2_go`, never `stage2` or either caller.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from typing import NamedTuple

import stage2_go

# A catalog id the runner may select: third-party catalog text never carries a `|` or other markup into
# the record's cells (DL-B-7 of the loop's deep review).
MODEL_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/-]*")

PAID_REASON = "a paid model; the free class does not admit it"

# Why an id that passed the provider and fresh-catalog gates is not a selected member.
SKIP_NOT_FRESH = "not-fresh"
SKIP_EXCLUDED = "excluded"
SKIP_NOT_INCLUDED = "not-included"


class Veto(NamedTuple):
    """A hard refusal no include can override: its kind (`plain`, `excluded`, `paid`) and the reason text."""

    kind: str
    reason: str


def model_veto(
    model: str,
    *,
    paid: Iterable[str] = (),
    exclusion: Callable[[str], str | None] | None = None,
    plain: bool = True,
) -> Veto | None:
    """The hard veto of one id, or None: the per-id check both the selector and the call boundaries share.

    The order is the id's shape, paid admission, then the declaration's exclusion. `paid` is the current
    `modelle` of the endpoint, supplied at the call, never trusted from a saved selection.
    """
    if plain and not MODEL_ID.fullmatch(model):
        return Veto("plain", "not a plain model id")
    if model in set(paid):
        return Veto("paid", PAID_REASON)
    if exclusion is not None:
        problem = exclusion(model)
        if problem:
            return Veto("excluded", problem)
    return None


@dataclass(frozen=True)
class Policy:
    """One caller's free policy, normalized.

    `include_adds` is the meaning of the include list: True selects those ids beyond the suffix (the
    review loop), False restricts the suffix's ids to them when the list is not empty (the research swarm).
    """

    provider: str
    suffix: str = ""
    include: tuple[str, ...] = ()
    exclude: tuple[str, ...] = ()
    include_adds: bool = True


@dataclass(frozen=True)
class Candidate:
    """One catalog row: its provider and id, the fresh definition to assess, the caller's eligibility refusal."""

    provider: str
    model: str
    definition: object = None
    problem: str | None = None


@dataclass
class Result:
    """What the selection decided, in candidate order.

    `selected` are the free members; `eligible` passed every gate before the policy's own exclude and
    include lists; `dropped` names each refused id (not one the policy excludes) with its reason; `vetoed`
    holds the hard vetoes of every considered id; `refused_destination` the destination refusals;
    `skipped` the ids the policy leaves out; `notices` the same-host path moves of eligible ids.
    """

    selected: list[str] = field(default_factory=list)
    eligible: list[str] = field(default_factory=list)
    dropped: dict[str, str] = field(default_factory=dict)
    vetoed: dict[str, Veto] = field(default_factory=dict)
    refused_destination: dict[str, str] = field(default_factory=dict)
    skipped: dict[str, str] = field(default_factory=dict)
    notices: list[str] = field(default_factory=list)


def select(
    candidates: Iterable[Candidate],
    policy: Policy,
    *,
    fresh: set[str],
    paid: Iterable[str],
    exclusion: Callable[[str], str | None] | None,
    address: stage2_go.AddressPolicy | None = None,
) -> Result:
    """The free members among the candidates, by the one rule.

    A candidate of another provider or one the fresh catalog does not hold is never considered; an id
    the suffix (or, additively, an include) does not name is not a candidate of the free class. Every
    named id then passes the hard vetoes, the caller's eligibility and the destination assessment
    (`stage2_go.assess`, when a definition and the address record are given); the policy's exclude list
    and, restrictively, its include list decide last. A hard veto wins over every include.
    """
    paid_ids = {str(item) for item in paid}
    includes = set(policy.include)
    excludes = set(policy.exclude)
    result = Result()
    seen: set[str] = set()
    for candidate in candidates:
        model = candidate.model
        if candidate.provider != policy.provider or model in seen:
            continue
        seen.add(model)
        if model not in fresh:
            result.skipped[model] = SKIP_NOT_FRESH
            continue
        named = bool(policy.suffix) and model.endswith(policy.suffix)
        if policy.include_adds and model in includes:
            named = True
        if not named:
            continue
        excluded = model in excludes
        veto = model_veto(model, paid=paid_ids, exclusion=exclusion)
        problem = veto.reason if veto else candidate.problem
        notice = None
        if veto:
            result.vetoed[model] = veto
        elif problem is None and candidate.definition is not None and address is not None:
            verdict = stage2_go.assess(address, model, candidate.definition)
            if not verdict.admitted:
                problem = verdict.problem
                result.refused_destination[model] = verdict.problem
            else:
                notice = verdict.notice
        if problem is not None:
            if excluded:
                result.skipped[model] = SKIP_EXCLUDED
            else:
                result.dropped[model] = problem
            continue
        result.eligible.append(model)
        if notice:
            result.notices.append(notice)
        if excluded:
            result.skipped[model] = SKIP_EXCLUDED
        elif not policy.include_adds and includes and model not in includes:
            result.skipped[model] = SKIP_NOT_INCLUDED
        else:
            result.selected.append(model)
    return result
