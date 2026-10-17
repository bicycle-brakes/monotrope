#!/usr/bin/env python3
"""The research swarm: phase 1 of a `feature` or `architectural` change (ADR 0020 draft).

This is one phase-1 run the explore verb dispatches; it is not Stage 2 of the
model routing. The runner module (`scripts/stage2.py`) is passed in as
`runner` and is never imported here - stage2.py runs as `__main__`, so
importing it would execute the module a second time.

Six topics, three kinds of researcher, one judge, sixteen sequential calls:

1. a fresh Opus 5.5 call writes the one-sentence public topic from the private
   brief; a mechanical filter accepts it or the run stops before any free call
   (spec, criterion 23);
2. every declared free model researches public practice in an isolated Pi
   context - fresh scratch cwd, home and agent directory, only the
   runner-owned research-tools extension, no repository content beyond the
   topic sentence (Q-6); the rides-on model comes from the pinned Pi's own
   model inventory, never from an assumed provider;
3. eleven Flash calls compare the repository on the six topics - both declared
   models on topics 1-5, the pair's first on topic 6 beside the free
   contribution; peers share the frozen packet and the public reports, never
   each other's answers, and private report text stays in the runner's buffer
   until the Flash stage ends;
4. one fresh Opus 5.5 context reconciles all six pairs, evidence only.

The runner alone appends to `research.md`: audit lines as calls are gated,
reports as stages end, the receipts, the reconciliation and the status. A
failed participant marks its slot, the remaining scheduled roles still run,
and the run ends incomplete with exit 1; a declaration or leak refusal
records the blocked slot without a clean claim and stops with exit 2 before
any further call. Deadlines are monotonic and no role is retried (spec,
criteria 12, 18 and 19).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

import yaml

TOPICS = {
    1: "code today",
    2: "rules and decisions",
    3: "history",
    4: "tests and gates",
    5: "risks and edge cases",
    6: "outside world and neighbours",
}
# The pair's angles (design.md's table): (pair index, topic) -> the angle of that seat.
ANGLES = {
    (0, 1): "current code, its structure and what a change would reuse",
    (1, 1): "the boundaries and callers around that code",
    (0, 2): "the applicable rules, gates and ADR decisions",
    (1, 2): "the overall architecture and the nearby specifications",
    (0, 3): "the change history and its rationale",
    (1, 3): "reversals, supersessions and stale assumptions",
    (0, 4): "the existing tests and gates that hold today",
    (1, 4): "counterexamples the tests do not catch and the checks that are missing",
    (0, 5): "the failure paths and the behaviour at the code's edges",
    (1, 5): "boundary violations, recovery cases and the load that breaks it",
    (0, 6): "whether public practices fit this architecture and its adjacent specifications",
}
TOPIC_MINUTES = 5.0
RESEARCHER_MINUTES = 10.0
JUDGE_MINUTES = 15.0
RUN_MINUTES = 150.0
PACKET_FILES = ("research.md", "decisions.md", "spec.md", "design.md", "plan.md", "findings.md")
WORD = re.compile(r"^[A-Za-z][A-Za-z']*$")
URL = re.compile(r"""https?://[^\s)>"'\\]+""")
# The free researcher's whole tool surface, as Pi's `--tools` allow-list: the
# extension's two tools and no built-in one (the extension's own gate stays).
PUBLIC_TOOLS = "public_search,public_fetch"


def allowance(elapsed: float, role_minutes: float) -> float:
    """The seconds this launch may take: the smaller of its deadline and the run's rest."""
    return min(role_minutes * 60.0, max(RUN_MINUTES * 60.0 - elapsed, 0.0))


# ---------------------------------------------------------------------------
# The declaration
# ---------------------------------------------------------------------------


def swarm_problems(data: dict) -> list[str]:
    """What the `research_swarm` declaration requires, as the problems found.

    The mirror of `tests/test_model_endpoints.py:swarm_block_problems`: the
    two sides name the same faults, so a declaration the test clears is one
    the runner accepts, and vice versa (spec, criterion 11).
    """
    problems: list[str] = []
    block = data.get("research_swarm")
    if not isinstance(block, dict):
        return ["no research_swarm block"]

    def entry(name: object) -> dict:
        for candidate in data.get("endpunkte") or []:
            if isinstance(candidate, dict) and candidate.get("name") == name:
                return candidate
        return {}

    free = entry(block.get("free_endpoint"))
    if not free:
        problems.append("free endpoint not declared")
    else:
        if free.get("abrechnung") != "free":
            problems.append("free endpoint billing is not free")
        if list(free.get("darf_sehen") or []) != ["public-web"]:
            problems.append("free endpoint must be cleared for public-web only")
    if "public-web" not in set(data.get("datenklassen") or {}):
        problems.append("public-web data class not declared")
    roster = block.get("free_roster") or []
    if not roster or len(set(roster)) != len(roster):
        problems.append("free roster empty or duplicated")
    elif free:
        unknown = sorted(set(roster) - set(free.get("modelle") or []))
        if unknown:
            problems.append(f"roster ids not on the free endpoint: {unknown}")
    focuses = block.get("free_focuses") or {}
    if set(focuses) != set(roster):
        problems.append("free_focuses do not match the roster")
    for focus in focuses.values():
        seats = focus if isinstance(focus, list) else None
        if not seats or any(topic not in TOPICS for topic in seats):
            problems.append("a focus names a topic outside 1-6")
    with_six = [who for who, focus in focuses.items() if isinstance(focus, list) and 6 in focus]
    if len(with_six) != 1:
        problems.append("topic 6 needs exactly one free seat")
    flash = entry(block.get("flash_endpoint"))
    pair = block.get("flash_pair") or []
    if not flash:
        problems.append("flash endpoint not declared")
    elif len(pair) != 2 or len(set(pair)) != 2 or not set(pair) <= set(flash.get("modelle") or []):
        problems.append("flash pair must be two distinct ids on the flash endpoint")
    paid = entry(block.get("paid_endpoint"))
    if not paid:
        problems.append("paid endpoint not declared")
    for role in ("topic_author", "judge"):
        if block.get(role) not in set(paid.get("modelle") or []):
            problems.append(f"{role} not on the paid endpoint")
    if block.get("topic6_free") not in set(roster):
        problems.append("topic6_free is not a roster id")
    elif with_six != [block.get("topic6_free")]:
        problems.append("topic6_free does not match the topic-6 focus")
    return problems


def swarm_roles(runner, data: dict) -> dict:
    """The resolved roles of one run, or the refusal naming the declaration's fault."""
    problems = swarm_problems(data)
    if problems:
        raise runner.Refused("the research_swarm declaration is unusable: " + "; ".join(problems))
    block = data["research_swarm"]
    return {
        "free_endpoint": block["free_endpoint"],
        "roster": list(block["free_roster"]),
        "focuses": {str(who): list(seats) for who, seats in block["free_focuses"].items()},
        "topic6_free": block["topic6_free"],
        "flash_endpoint": block["flash_endpoint"],
        "pair": list(block["flash_pair"]),
        "paid_endpoint": block["paid_endpoint"],
        "topic_author": block["topic_author"],
        "judge": block["judge"],
    }


# ---------------------------------------------------------------------------
# The frozen input state
# ---------------------------------------------------------------------------


def _git(root: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    return done.stdout if done.returncode == 0 else ""


def tracked_paths(root: Path) -> set[str]:
    return {path for path in _git(root, "ls-files", "-z").split("\0") if path}


def adjacent_spec_headers(root: Path) -> str:
    """Title, class and bead of every change's spec - the nearby-specification pointers."""
    lines: list[str] = []
    folder = root / "plans" / "changes"
    if not folder.is_dir():
        return ""
    for path in sorted(folder.glob("*/spec.md")):
        match = re.match(r"---\n(.*?)\n---", path.read_text(encoding="utf-8", errors="replace"), re.S)
        if not match:
            continue
        try:
            header = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            continue
        if not isinstance(header, dict):
            continue
        lines.append(
            f"- {path.parent.name}: {header.get('title', '?')} "
            f"(class {header.get('class', 'unstated')}, bead {header.get('bead', '?')})"
        )
    return "\n".join(lines)


def build_packet(ctx) -> tuple[str, str, dict[Path, bytes], str]:
    """Freeze the private packet, its digest, the frozen bytes and HEAD.

    The packet carries what the design lists: the change's artefacts, the
    repository rules, the adjacent specs' headers, bounded git history and the
    tracked files - Pi's file tools alone are no git-history command, so the
    runner collects that evidence itself. The frozen map is keyed by path and
    covers every tracked file, so publication detects any change outside this
    run's own research append; `research.md` is the one file whose bytes this
    run may extend.
    """
    frozen: dict[Path, bytes] = {}
    parts: list[str] = [f"# Input packet for the change {ctx.change}"]
    for name in PACKET_FILES:
        path = ctx.folder / name
        try:
            data = path.read_bytes()
        except OSError:
            continue
        frozen[path] = data
        parts.append(f"## {name}\n\n{data.decode('utf-8', errors='replace')}")
    agents = ctx.root / "AGENTS.md"
    try:
        data = agents.read_bytes()
    except OSError:
        data = b""
    if data:
        frozen[agents] = data
        parts.append("## Repository rules (AGENTS.md)\n\n" + data.decode("utf-8", errors="replace"))
    adjacent = adjacent_spec_headers(ctx.root)
    if adjacent:
        parts.append("## Adjacent specifications\n\n" + adjacent)
    history = _git(ctx.root, "log", "--oneline", "-n", "300")
    if history:
        parts.append("## Git history (bounded to 300 subjects)\n\n" + history)
    tracked = sorted(tracked_paths(ctx.root))
    parts.append("## Tracked files\n\n" + "\n".join(tracked))
    for relative in tracked:
        path = ctx.root / relative
        try:
            frozen.setdefault(path, path.read_bytes())
        except OSError:
            continue
    head = _git(ctx.root, "rev-parse", "HEAD").strip()
    packet = "\n\n".join(parts)
    return packet, hashlib.sha256((packet + head).encode("utf-8")).hexdigest(), frozen, head


def without_updated(data: bytes) -> bytes:
    """The bytes with the header's `updated:` value blanked - the one line the runner's appends re-stamp."""
    match = re.match(rb"---\r?\n(.*?)\r?\n---", data, re.S)
    if not match:
        return data
    header = re.sub(rb"(?m)^updated:[^\r\n]*", b"updated:", match.group(1), count=1)
    return data[: match.start(1)] + header + data[match.end(1) :]


def input_state_holds(ctx, frozen: dict[Path, bytes], head: str) -> str | None:
    """None while every frozen input stands; the changed path's name otherwise.

    `research.md` is compared up to the point this run appended: the file must
    begin with the frozen bytes, so the run cannot publish over other writing,
    while its own appended block does not invalidate its digest (plan, step 6).
    Every append re-stamps the header's `updated:` line, so a run that crosses
    midnight changes that one value itself; it is left out of the comparison.
    """
    for path, data in frozen.items():
        try:
            now = path.read_bytes()
        except OSError:
            return path.relative_to(ctx.root).as_posix()
        if path.name == "research.md" and path.parent == ctx.folder:
            if not without_updated(now).startswith(without_updated(data)):
                return path.relative_to(ctx.root).as_posix()
        elif now != data:
            return path.relative_to(ctx.root).as_posix()
    if _git(ctx.root, "rev-parse", "HEAD").strip() != head:
        return "HEAD"
    return None


# ---------------------------------------------------------------------------
# The audit record and the per-call gate
# ---------------------------------------------------------------------------


class Audit:
    """The per-call lines of one run block, appended to research.md by the runner alone."""

    def __init__(self, runner, destination: Path, run_id: str) -> None:
        self.runner = runner
        self.destination = destination
        self.run_id = run_id

    def _what(self, role: str, topic: int | None) -> str:
        return f"swarm {role}" + (f" · topic {topic}" if topic is not None else "")

    def clean(self, role: str, topic: int | None, endpoint: str, model: str, result) -> None:
        self.runner.append(
            self.destination,
            f"Stage-2 call, {self.runner.today()}: {self._what(role, topic)} · run {self.run_id} · "
            f"endpoint {endpoint} · model {model} · leak check clean over "
            f"{result.files} files, {result.commits} commits, {result.rules} rules.",
        )

    def blocked(self, role: str, topic: int | None, endpoint: str, model: str, why: str) -> None:
        self.runner.append(
            self.destination,
            f"Stage-2 call, {self.runner.today()}: {self._what(role, topic)} · run {self.run_id} · "
            f"endpoint {endpoint} · model {model} · {why}.",
        )

    def outcome(self, role: str, topic: int | None, model: str, how: str, seconds: float) -> None:
        self.runner.append(
            self.destination,
            f"Swarm outcome, {self.runner.today()}: {self._what(role, topic)} · run {self.run_id} · "
            f"model {model} · {how} ({seconds:.0f}s).",
        )


def gate(runner, ctx, endpoint: str, model: str, prompt: str, public: bool, audit: Audit, role: str, topic: int | None):
    """Declaration, exact-prompt leak check and audit line for one call - immediately before it.

    `public` selects the scoped public-web check; every other role rides the
    framework check with its residency demand. A refusal records the blocked
    slot without a clean claim and stops the run with no further call (spec,
    criteria 12 and 13).
    """
    check = runner.public_declaration_problem if public else runner.declaration_problem
    problem = check(ctx.root, endpoint, model)
    if problem is None:
        result = runner.leakcheck.check(ctx.change, runner.leakcheck.default_denylist(), ctx.root, [("prompt", prompt)])
        print(result.verdict.render())
        if result.verdict.exit_code() == 0:
            audit.clean(role, topic, endpoint, model, result)
            return result
        problem = "the leak check is not clean; the call does not start"
    audit.blocked(role, topic, endpoint, model, f"refused - {problem}")
    raise runner.Refused(problem)


# ---------------------------------------------------------------------------
# The prompts
# ---------------------------------------------------------------------------


def _prompt(root: Path, name: str) -> str:
    return (root / "prompts" / "research-swarm" / name).read_text(encoding="utf-8")


def _brief(ctx, name: str) -> str:
    try:
        return (ctx.folder / name).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "(not written yet - exploration legitimately precedes this artefact)"


def topic_author_prompt(ctx) -> str:
    """The private brief and the criterion-23 instruction for the topic call.

    This prompt is exactly what must never reach a free researcher; the
    mechanical filter checks what comes back, not the model's promise. A
    missing spec or decisions file is the normal state of early exploration,
    not an error (spec, criterion 3).
    """
    parts = [
        "You write the one-sentence public topic for a research run about the change described below.",
        "Answer with the sentence and nothing else: one sentence of at most 20 words, in plain words,",
        "naming what the change is about - no file or path name, no identifier, no code, no change",
        "name, no tracker id, no hyphenated compound (write its parts as separate words).",
        'The shape to match: "container isolation for AI agent runs".',
        "---",
        "# The change's problem",
        _brief(ctx, "spec.md"),
        "# The maintainer's answers",
        _brief(ctx, "decisions.md"),
    ]
    return "\n\n".join(parts)


def public_prompt(root: Path, topic: str, focuses: list[int]) -> str:
    """Generic assigned questions plus the one topic sentence - no other change text."""
    focus = "\n".join(f"- Topic {number}: {TOPICS[number]}" for number in focuses)
    return _prompt(root, "public.md").replace("{{TOPIC}}", topic).replace("{{FOCUS}}", focus)


def repository_prompt(
    root: Path, read_request: str, topic_id: int, angle: str, packet: str, public_reports: str
) -> str:
    """One Flash seat's task: the topic, its angle, the frozen packet, the public reports."""
    body = (
        _prompt(root, "repository.md")
        .replace("{{TOPIC_ID}}", str(topic_id))
        .replace("{{TOPIC_NAME}}", TOPICS[topic_id])
        .replace("{{ANGLE}}", angle)
    )
    return "\n\n".join(
        [
            body,
            "---",
            "# The frozen input packet",
            packet,
            "---",
            "# The public research reports",
            public_reports or "(none arrived)",
            read_request,
        ]
    )


def judge_prompt(root: Path, read_request: str, packet: str, pairs: str, receipts_text: str, failed: list[str]) -> str:
    """The judge's materials: the pairs, the receipts, the failed slots - and nothing else."""
    return "\n\n".join(
        [
            _prompt(root, "judge.md"),
            "---",
            "# The frozen input packet",
            packet,
            "# The six pairs",
            pairs,
            "# Public source receipts",
            receipts_text or "(none)",
            "# Failed slots",
            "\n".join(f"- {slot}" for slot in failed) or "(none)",
            read_request,
        ]
    )


def topic_pairs(roles: dict, free_reports: dict[str, str], flash_reports: dict[tuple[int, int], str]) -> str:
    """Map independent seats and their public comparison evidence to each topic, including missing slots."""
    sections = []
    for topic_id, name in TOPICS.items():
        parts = [f"## Topic {topic_id}: {name}"]
        if topic_id == 6:
            member = roles["topic6_free"]
            parts += [f"Free seat: {member}", free_reports.get(member, "(missing contribution)")]
        for seat in (0, 1) if topic_id <= 5 else (0,):
            parts += [
                f"Flash seat: {roles['pair'][seat]}",
                flash_reports.get((topic_id, seat), "(missing contribution)"),
            ]
        if topic_id <= 5:
            parts.append("Public practice comparisons:")
            for member in roles["roster"]:
                if topic_id in roles["focuses"][member]:
                    parts += [f"Public focus: {member}", free_reports.get(member, "(missing contribution)")]
        sections.append("\n\n".join(parts))
    return "\n\n".join(sections)


# ---------------------------------------------------------------------------
# The calls
# ---------------------------------------------------------------------------


def public_env(own: dict[str, str]) -> dict[str, str]:
    """Only executable lookup is inherited; home/config/credential paths belong to this scratch run."""
    return {**({"PATH": os.environ["PATH"]} if "PATH" in os.environ else {}), **own}


def inventory_providers(listing: str) -> dict[str, set[str]]:
    """Every model id of a `pi --list-models` answer, with the providers that list it.

    Pi 1.1.0 prints a padded table (`dist/cli/list-models.js`): a header line
    `provider  model  context  max-out  thinking  images`, then one row per
    model whose provider has usable authentication, provider first and model
    id second. With no authenticated model it prints a guidance message
    instead, which yields no id here.
    """
    found: dict[str, set[str]] = {}
    for line in listing.splitlines():
        cells = line.split()
        if len(cells) < 6 or cells[:2] == ["provider", "model"]:
            continue
        found.setdefault(cells[1], set()).add(cells[0])
    return found


def free_transport(runner, roles: dict, key: str) -> dict[str, str]:
    """Map every free id to the Pi model id it actually rides on.

    The declaration's name is not an asserted provider id: the pinned
    runtime's own model inventory is what a call uses, and an id it does not
    map refuses the free stage here instead of assuming a provider (plan,
    step 1; the design's "declaration name" remark). The inventory runs with
    the free call's own credential and nothing else, so it lists exactly the
    providers that credential reaches. The Flash endpoint's provider is the
    paid subscription, never the free endpoint, so a free id listed only there
    is unmapped; an id that more than one remaining provider lists refuses as
    ambiguous instead of taking whichever comes last. Terms and residency of
    the free ids stay unknown; nothing here reads them.
    """
    runner.require_pi()
    with tempfile.TemporaryDirectory(prefix="stage2-swarm-") as tmp:
        env = public_env({"HOME": tmp, "PI_CODING_AGENT_DIR": tmp, "OPENCODE_API_KEY": key})
        done = runner.launch(
            [str(runner.PI_WRAPPER), "--list-models"],
            Path(tmp),
            env,
            key,
            timeout=60.0,
            limit="the model inventory's limit of 60 seconds",
        )
    if done.returncode != 0:
        raise runner.CallFailed(f"pi --list-models ended {done.returncode}; the free transport is unqualified.")
    listed = inventory_providers(done.stdout or "")
    paid = str(roles["flash_endpoint"])
    mapping: dict[str, str] = {}
    missing: list[str] = []
    ambiguous: list[str] = []
    for model in (str(member) for member in roles["roster"]):
        providers = sorted(listed.get(model, set()) - {paid})
        if not providers:
            missing.append(model)
        elif len(providers) > 1:
            ambiguous.append(f"{model} ({', '.join(providers)})")
        else:
            mapping[model] = f"{providers[0]}/{model}"
    if missing:
        raise runner.CallFailed(
            "the pinned Pi's model inventory does not map the free id(s) "
            + ", ".join(missing)
            + f" to a provider other than the paid {paid}; the free stage refuses rather than assume a provider."
        )
    if ambiguous:
        raise runner.CallFailed(
            "the pinned Pi's model inventory lists the free id(s) "
            + "; ".join(ambiguous)
            + " under more than one provider; the free stage refuses rather than pick one."
        )
    return mapping


def pi_public_call(runner, prompt_text: str, model_id: str, key: str, seconds: float, limit: str) -> tuple[str, str]:
    """One free researcher in its isolated context. Returns (answer, receipts text).

    Fresh scratch cwd, home and agent directory; the extension and the prompt
    are copied to generic scratch paths before loading, so no repository path
    can enter discovery metadata; only the OpenCode key and the receipts path
    join the allow-listed environment. The `--tools` allow-list declares only
    the extension's two tools to the model, and the extension's gate blocks
    any other call: no file or shell tool is offered or passes.
    """
    with tempfile.TemporaryDirectory(prefix="stage2-public-") as tmp:
        scratch = Path(tmp)
        agent = scratch / "agent"
        agent.mkdir()
        (agent / "settings.json").write_text(json.dumps({"retry": {"enabled": False}}), encoding="utf-8")
        home = scratch / "home"
        home.mkdir()
        research = scratch / "research"
        research.mkdir()
        extension = scratch / "research-tools.mjs"
        source = Path(__file__).resolve().parent / "stage2_research_tools.mjs"
        extension.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        prompt_file = research / "public-prompt.md"
        prompt_file.write_text(prompt_text, encoding="utf-8")
        receipts = research / "receipts.jsonl"
        command = [
            str(runner.PI_WRAPPER),
            "--print",
            "--no-session",
            "--no-approve",
            "--no-extensions",
            "-e",
            str(extension),
            "--no-mcp",
            "--no-skills",
            "--no-context-files",
            "--no-prompt-templates",
            "--no-themes",
            "--tools",
            PUBLIC_TOOLS,
            "--model",
            model_id,
            "--append-system-prompt",
            str(prompt_file),
            "Research the public topic as the appended instructions say.",
        ]
        env = public_env(
            {
                "HOME": str(home),
                "PI_CODING_AGENT_DIR": str(agent),
                "OPENCODE_API_KEY": key,
                "STAGE2_PUBLIC_RECEIPTS": str(receipts),
            }
        )
        return pi_result(runner, command, scratch, env, model_id, key, seconds, limit, receipts)


def pi_repository_call(runner, ctx, prompt: str, model: str, key: str, seconds: float, limit: str) -> str:
    """One Flash researcher: Pi on OpenCode Go, the read tools, discovery off, the worktree as cwd."""
    with tempfile.TemporaryDirectory(prefix="stage2-swarm-") as tmp:
        scratch = Path(tmp)
        agent = scratch / "agent"
        agent.mkdir()
        (agent / "settings.json").write_text(json.dumps({"retry": {"enabled": False}}), encoding="utf-8")
        home = scratch / "home"
        home.mkdir()
        prompt_file = scratch / "research-prompt.md"
        prompt_file.write_text(prompt, encoding="utf-8")
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
            "--tools",
            runner.PI_TOOLS,
            "--model",
            f"{runner.OPENCODE}/{model}",
            "--append-system-prompt",
            str(prompt_file),
            f"Research the change {ctx.change} as the appended instructions say.",
        ]
        env = runner.foreign_env({"HOME": str(home), "PI_CODING_AGENT_DIR": str(agent), "OPENCODE_API_KEY": key})
        answer, _ = pi_result(runner, command, ctx.root, env, model, key, seconds, limit)
        return answer


def pi_result(runner, command, cwd, env, model, key, seconds, limit, receipts: Path | None = None) -> tuple[str, str]:
    """Read evidence before the caller removes its scratch directory, on every exit path."""

    def receipt_text() -> str:
        return (
            runner.scrub(receipts.read_text(encoding="utf-8", errors="replace"), key)
            if receipts and receipts.exists()
            else ""
        )

    def output(value) -> str:
        # TimeoutExpired.output/stderr can be bytes even when subprocess.run uses text=True.
        return runner.scrub(value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or "", key)

    try:
        done = runner.launch(command, cwd, env, key, timeout=seconds, limit=limit)
    except runner.CallFailed as error:
        cause = error.__cause__
        partial = output(getattr(cause, "stdout", ""))
        stderr = output(getattr(cause, "stderr", ""))
        if stderr:
            print("\n".join(stderr.splitlines()[-40:]), file=sys.stderr)
        raise runner.CallFailed(str(error), partial_answer=partial, receipts_text=receipt_text()) from error
    answer = output(done.stdout)
    receipts_text = receipt_text()
    if done.returncode != 0 or not answer.strip():
        _relay_stderr(runner, done, key)
        reason = f"ended {done.returncode}" if done.returncode != 0 else "answered nothing"
        raise runner.CallFailed(f"pi ({model}) {reason}", partial_answer=answer, receipts_text=receipts_text)
    return answer, receipts_text


def _relay_stderr(runner, done, key: str) -> None:
    """The last lines of a failed call's standard error, scrubbed, on the runner's own (criterion 21)."""
    tail = "\n".join((done.stderr or "").splitlines()[-40:])
    if tail:
        print(runner.scrub(tail, key), file=sys.stderr)


# ---------------------------------------------------------------------------
# The validation
# ---------------------------------------------------------------------------


def topic_problems(answer: str, change: str, bead: str) -> list[str]:
    """The mechanical filter for the public topic (spec, criterion 23).

    One sentence, at most 20 words, no path, file name, identifier-shaped
    token, change name or bead id. A word is letters and apostrophes only: a
    hyphenated token is refused, because the repository's identifiers (bead
    ids, the repository name, endpoint and change names) are hyphenated words
    that no list of this change's own names can hold. A rejected topic stops
    the run before any free call.
    """
    text = answer.strip()
    text = re.sub(r"^[#>*\"'`\s]+", "", text)
    text = re.sub(r"[\"'`*\s]+$", "", text)
    if not text:
        return ["the topic call answered nothing"]
    if change.lower() in text.lower():
        return ["the topic names the change"]
    if bead.lower() in text.lower():
        return ["the topic names the bead"]
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if len(sentences) != 1:
        return ["the topic is not exactly one sentence"]
    words = sentences[0].split()
    if len(words) > 20:
        return ["the topic has more than 20 words"]
    for word in words:
        bare = word.strip(".,;:!?)({}\"'")
        if not WORD.match(bare) or re.search(r"[a-z][A-Z]", bare):
            return [f"the topic carries the identifier-shaped token '{word}'"]
    return []


def receipt_problems(report: str, receipts: list[dict]) -> list[str]:
    """The public URLs a report cites that no successful fetch receipt backs (spec, criterion 10)."""
    backed = {
        str(url)
        for receipt in receipts
        if receipt.get("kind") == "fetch" and receipt.get("status") == 200
        for url in (receipt.get("url"), receipt.get("final_url"))
        if url
    }
    return [url for url in (u.rstrip(".,;:") for u in URL.findall(report)) if url not in backed]


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


JUDGE_FIELDS = (
    "Practice comparison:",
    "Architecture comparison:",
    "Adjacent-spec comparison:",
    "Disagreement:",
    "Gaps:",
    "Human questions:",
)


# A path-shaped token: slash-separated segments ending in a file extension.
PATH_SHAPE = re.compile(r"[\w.-]+(?:/[\w.-]+)*\.[A-Za-z][A-Za-z0-9]*")
LINE_CITATION = re.compile(r"(?<![\w/.:-])([\w./-]+\.[A-Za-z][A-Za-z0-9]*):(\d+)(?:[-:]\d+)?(?![\w/.-])")
SYMBOL_CITATION = re.compile(r"(?<![\w/.:-])([\w./-]+)::([^\s`]+)")


def symbol_problem(path: str, symbol: str, sources: dict[str, bytes]) -> str | None:
    """None when the cited symbol stands in the frozen bytes of the cited path; the problem otherwise."""
    if path not in sources:
        return f"the citation '{path}::{symbol}' names no tracked path at the frozen state"
    text = sources[path].decode("utf-8", errors="replace")
    name = symbol.strip().rstrip("()").strip()
    parts = [part for part in name.split(".") if part]
    found = bool(parts) and (name in text or all(re.search(rf"(?<!\w){re.escape(part)}(?!\w)", text) for part in parts))
    return None if found else f"the citation '{path}::{symbol}' names no symbol of {path} at the frozen state"


def citation_problems(answer: str, sources: dict[str, bytes]) -> list[str]:
    """The judge's local citations that do not bind to the frozen state (spec, criterion 16).

    A `path::symbol` must name a tracked path and a symbol its frozen bytes
    contain; a citation by line numbers alone, or a bare path in backticks,
    is refused, because neither names what it claims stands there.
    """
    problems: list[str] = []

    def add(problem: str | None) -> None:
        if problem and problem not in problems:
            problems.append(problem)

    for path, symbol in SYMBOL_CITATION.findall(answer):
        add(symbol_problem(path, symbol, sources))
    for match in LINE_CITATION.finditer(answer):
        add(f"the citation '{match.group(0)}' gives line numbers only; cite `path::symbol`")
    for token in (raw.strip() for raw in re.findall(r"`([^`\n]+)`", answer)):
        if "::" in token or token.startswith(("http://", "https://")) or LINE_CITATION.fullmatch(token):
            continue
        if token in sources or ("/" in token and PATH_SHAPE.fullmatch(token)):
            add(f"the citation '{token}' is a bare path; cite `path::symbol`")
    return problems


def judge_problems(answer: str, sources: dict[str, bytes]) -> list[str]:
    """The judge's six sections, their labelled fields and their local citations.

    Sections must be `### Topic <n>` for 1-6, once each; every section names
    the six labelled fields; a repository citation must name a path and a
    symbol that existed at the frozen input state (spec, criteria 7, 14, 15
    and 16). `sources` maps each tracked path to its frozen bytes.
    """
    problems: list[str] = []
    sections: list[tuple[int, int]] = [
        (int(match.group(1)), match.start()) for match in re.finditer(r"^### Topic (\d+)\b", answer, re.M)
    ]
    if sorted(number for number, _ in sections) != [1, 2, 3, 4, 5, 6]:
        problems.append(f"the judge wrote topic sections {sorted(n for n, _ in sections)}, not 1-6 once each")
    for position, (number, start) in enumerate(sections):
        end = sections[position + 1][1] if position + 1 < len(sections) else len(answer)
        body = " ".join(answer[start:end].split())
        for field in JUDGE_FIELDS:
            if field not in body:
                problems.append(f"topic {number} lacks '{field}'")
    problems.extend(citation_problems(answer, sources))
    return problems


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------


def run(root: Path, change: str, runner, klass: str) -> None:
    """The whole phase-1 swarm; raises the runner's Refused (exit 2) or CallFailed (exit 1)."""
    started = time.monotonic()
    try:
        data = yaml.safe_load((root / "model-endpoints.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as error:
        raise runner.Refused("model-endpoints.yaml cannot be read") from error
    roles = swarm_roles(runner, data)
    # Role identities come from the declaration; the spec fixes the two efforts.
    topic_call = (roles["paid_endpoint"], roles["topic_author"], "high")
    judge_call = (roles["paid_endpoint"], roles["judge"], "xhigh")
    ctx = runner.preflight(root, change, topic_call, bead_file="research.md")
    # The runner's appends stamp `updated:`; stamping before the freeze keeps
    # the frozen prefix of `research.md` intact for the publication check.
    runner.stamp_updated(ctx.research)
    packet, digest, frozen, head = build_packet(ctx)
    tracked = tracked_paths(root)
    sources = {relative: frozen[ctx.root / relative] for relative in sorted(tracked) if (ctx.root / relative) in frozen}
    run_id = f"swarm-{uuid.uuid4().hex[:8]}"
    audit = Audit(runner, ctx.research, run_id)
    runner.append(
        ctx.research,
        f"## Research swarm — {runner.today()}\n\n"
        f"run {run_id} · class {klass} · baseline HEAD {head[:12]} · input digest {digest[:16]}\n",
    )
    failed: list[str] = []
    free_reports: dict[str, str] = {}
    flash_reports: dict[tuple[int, int], str] = {}
    receipts_all: list[dict] = []
    partials: dict[tuple[str, int | None, str], tuple[str, str]] = {}

    def remaining() -> float:
        return time.monotonic() - started

    def budget(role: str, topic: int | None, model: str, minutes: float) -> float | None:
        """The seconds a launch may take, or None - recorded - once the whole-run deadline is spent.

        A spent deadline refuses before the gate: no leak-check line, no
        process, and the slot is recorded unfinished (spec, criterion 19).
        """
        seconds = allowance(remaining(), minutes)
        if seconds > 0:
            return seconds
        slot = role + (f" (topic {topic})" if topic is not None else "")
        failed.append(f"{slot}: not started - the whole-run deadline of {RUN_MINUTES:g} minutes is spent")
        audit.outcome(role, topic, model, "not started - the whole-run deadline is spent", 0.0)
        return None

    def attempt(role: str, topic: int | None, call, model: str, how_ok: str) -> object | None:
        """Run one scheduled call; a failure marks its slot and the run carries on."""
        begin = time.monotonic()
        try:
            answer = call()
        except runner.CallFailed as error:
            partials[(role, topic, model)] = (error.partial_answer, error.receipts_text)
            failed.append(f"{role}" + (f" (topic {topic})" if topic is not None else "") + f": {error}")
            audit.outcome(role, topic, model, f"failed - {error}", time.monotonic() - begin)
            return None
        audit.outcome(role, topic, model, how_ok, time.monotonic() - begin)
        return answer

    # --- the public topic -----------------------------------------------------------------------
    prompt = topic_author_prompt(ctx)
    topic_seconds = allowance(remaining(), TOPIC_MINUTES)  # the run has just begun: never spent
    gate(runner, ctx, topic_call[0], topic_call[1], prompt, False, audit, "public topic", None)
    topic_answer = attempt(
        "public topic",
        None,
        lambda: runner.run_work_model(
            ctx,
            prompt,
            topic_call,
            writable=False,
            timeout=topic_seconds,
            limit=f"the topic call's deadline of {TOPIC_MINUTES:g} minutes",
        ),
        topic_call[1],
        "ok",
    )
    if topic_answer is None:
        raise runner.CallFailed("the public topic call failed; no free call starts.")
    filter_failure = topic_problems(str(topic_answer), change, ctx.bead)
    if filter_failure:
        runner.append(ctx.research, f"public topic rejected - {'; '.join(filter_failure)}. No free call starts.")
        raise runner.CallFailed(f"the public topic was rejected ({'; '.join(filter_failure)}); no free call starts.")
    topic = " ".join(str(topic_answer).strip().split())
    runner.append(ctx.research, f"public topic: {topic}")

    # --- the free stage -------------------------------------------------------------------------
    key = runner.reviewer_key()
    try:
        transport = free_transport(runner, roles, key)
    except runner.CallFailed as error:
        runner.append(ctx.research, f"free transport unqualified - {error}. No free call starts.")
        raise
    runner.append(ctx.research, "free transport: " + "; ".join(f"{a} rides {b}" for a, b in transport.items()))
    for member in roles["roster"]:
        member = str(member)
        model_id = transport[member]
        public_text = public_prompt(root, topic, roles["focuses"][member])
        seconds = budget("free researcher", None, model_id, RESEARCHER_MINUTES)
        if seconds is None:
            continue
        gate(runner, ctx, roles["free_endpoint"], member, public_text, True, audit, "free researcher", None)
        answer = attempt(
            "free researcher",
            None,
            lambda model_id=model_id, public_text=public_text, seconds=seconds: pi_public_call(
                runner,
                public_text,
                model_id,
                key,
                seconds,
                f"the researcher deadline of {RESEARCHER_MINUTES:g} minutes",
            ),
            model_id,
            "ok",
        )
        report, receipts_text = answer if answer is not None else partials[("free researcher", None, model_id)]
        receipts = parse_receipts(str(receipts_text))
        receipts_all.extend(receipts)
        unbacked = receipt_problems(str(report), receipts)
        retrieved = any(receipt.get("kind") == "fetch" and receipt.get("status") == 200 for receipt in receipts)
        note = " (failed — partial evidence)" if answer is None else ""
        note += f" (citations without receipts: {'; '.join(unbacked)})" if unbacked else ""
        if unbacked:
            failed.append(f"free researcher {member}: citations no receipt backs - {', '.join(unbacked)}")
        if answer is not None and not retrieved:
            # Public evidence is a retrieved page; a report from memory or from
            # failed tools is no contribution (spec, criteria 10 and 18).
            note += " (no retrieved page)"
            failed.append(f"free researcher {member}: retrieved no public page")
        if str(report).strip() or receipts_text:
            free_reports[member] = (
                f"### Free researcher {member}{note}\n\n{report or '(no answer; source receipts retained)'}"
            )
    runner.append(
        ctx.research,
        "### Public reports\n\n" + ("\n\n".join(free_reports.values()) if free_reports else "(none succeeded)"),
    )
    runner.append(
        ctx.research,
        "### Public source receipts\n\n```jsonl\n" + (jsonl(receipts_all) or "(none)") + "\n```",
    )

    # --- the Flash stage: private text buffered until the stage ends ----------------------------
    pair_text = "\n\n".join(free_reports.values()) if free_reports else "(no public reports arrived)"
    for topic_id in range(1, 7):
        seats = (0, 1) if topic_id <= 5 else (0,)
        for seat in seats:
            model = str(roles["pair"][seat])
            angle = ANGLES[(seat, topic_id)]
            flash_text = repository_prompt(root, runner.READ_REQUEST, topic_id, angle, packet, pair_text)
            seconds = budget("flash researcher", topic_id, model, RESEARCHER_MINUTES)
            if seconds is None:
                continue
            gate(
                runner,
                ctx,
                roles["flash_endpoint"],
                model,
                flash_text,
                False,
                audit,
                "flash researcher",
                topic_id,
            )
            answer = attempt(
                "flash researcher",
                topic_id,
                lambda model=model, flash_text=flash_text, seconds=seconds: pi_repository_call(
                    runner,
                    ctx,
                    flash_text,
                    model,
                    key,
                    seconds,
                    f"the researcher deadline of {RESEARCHER_MINUTES:g} minutes",
                ),
                model,
                "ok",
            )
            report = answer if answer is not None else partials[("flash researcher", topic_id, model)][0]
            if report and str(report).strip():
                note = " (failed — partial evidence)" if answer is None else ""
                flash_reports[(topic_id, seat)] = f"### Flash researcher {model} · topic {topic_id}{note}\n\n{report}"
    runner.append(
        ctx.research,
        "### Repository reports\n\n" + ("\n\n".join(flash_reports.values()) if flash_reports else "(none succeeded)"),
    )

    # --- the judge ------------------------------------------------------------------------------
    pairs = topic_pairs(roles, free_reports, flash_reports)
    judge_text = judge_prompt(root, runner.READ_REQUEST, packet, pairs, jsonl(receipts_all), failed)
    judge_seconds = budget("judge", None, judge_call[1], JUDGE_MINUTES)
    reconciliation = None
    if judge_seconds is not None:
        gate(runner, ctx, judge_call[0], judge_call[1], judge_text, False, audit, "judge", None)
        reconciliation = attempt(
            "judge",
            None,
            lambda: runner.run_work_model(
                ctx,
                judge_text,
                judge_call,
                writable=False,
                timeout=judge_seconds,
                limit=f"the judge deadline of {JUDGE_MINUTES:g} minutes",
            ),
            judge_call[1],
            "ok",
        )
    if judge_seconds is None:
        judge_faults = []  # the unfinished slot is already recorded
    elif reconciliation is None:
        judge_faults = ["the judge call failed"]
    else:
        judge_faults = judge_problems(str(reconciliation), sources)
    if reconciliation is not None:
        unbacked = receipt_problems(str(reconciliation), receipts_all)
        if unbacked:
            judge_faults.append("public citations no receipt backs - " + "; ".join(unbacked))
    if judge_faults:
        failed.append("judge: " + "; ".join(judge_faults))

    # --- publication ----------------------------------------------------------------------------
    changed = input_state_holds(ctx, frozen, head)
    if changed is not None:
        failed.append(f"the frozen input state changed: {changed}")
    if reconciliation:
        note = " (failed validation — partial evidence)" if judge_faults else ""
        runner.append(ctx.research, f"### Reconciliation{note}\n\n" + str(reconciliation).strip())
    status = "complete" if not failed else "incomplete - " + "; ".join(failed)
    runner.append(ctx.research, f"run {run_id} status: {status}.")
    if failed:
        raise runner.CallFailed(f"the research swarm run {run_id} is incomplete: {'; '.join(failed)}")
    print(f"swarm: six reconciled topics appended to {ctx.research.relative_to(root)} · run {run_id}")


def jsonl(receipts: list[dict]) -> str:
    """The receipts as JSON lines, one per receipt."""
    return "\n".join(json.dumps(receipt, sort_keys=True) for receipt in receipts)
