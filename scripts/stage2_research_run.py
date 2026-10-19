"""The phase-1 research run (ADR 0020 draft): finders, map, public sentence, eleven topics, judge.

The runner module (`scripts/stage2.py`) is passed in as `runner` and is never imported here
(stage2.py runs as `__main__`). `stage2_swarm.run` delegates to `run` below.

Stages, in order: receipt consumption (done by the caller) -> lock, frozen inputs and resume lookup ->
finder trio -> Opus map merge -> Opus public sentence -> local history -> topics 1-11 (`33 + 3N`
required and free slots) -> Opus judge. Every stage is one `dispatch` call: provider queues of four,
serialised declaration and leak check at dispatch, one terminal outcome per slot, and a durable
record in the runner-owned state store written as each slot ends (Q-13). A finished valid slot of the
latest stored run is reused only on an exact match of binding, stage, topic, seat, endpoint, model and
prompt hash; reused slots are not dispatched. No worker writes `research.md`: audit lines, reports and
the status are buffered and appended once, by the runner, at the end (or abort) of the run.

Seat identities come from the run's frozen selection (`stage2_availability.research_roles`) and the
declaration, never from a hardcoded tuple. Opus roles run with an empty tool list and see only their
own packet. The run never probes, refreshes the catalog, retries or swaps a seat.
"""

from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import json
import re
import subprocess
import tempfile
import threading
import time
import unicodedata
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

import research_handoff
import stage2_availability
import stage2_research_map
import stage2_swarm
from stage2_research_dispatch import GateVerdict, Slot, dispatch
from stage2_research_history import ResearchHistoryError, build_research_history
from stage2_research_judge import ResearchJudgeError, build_research_judge_packet, research_claim_scores
from stage2_research_report import ResearchReportError, _keys, _load, research_seat_id, validate_research_report
from stage2_research_snapshot import ResearchSnapshotError, _without_updated, freeze_research_state, stored_binding
from stage2_research_store import Store, StoreLocked, StoreWriteError, plan_reuse, research_dir

CLOCK = time.monotonic  # injectable; the dispatcher and all deadlines of the run read it

GO, CLAUDE = stage2_swarm.GO_ENDPOINT, stage2_swarm.CLAUDE_ENDPOINT
MINUTES = {"finders": 10.0, "merge": 10.0, "sentence": 5.0, "topics": 10.0, "judge": 15.0}
RUN_MINUTES = 150.0
PREPARATION_SECONDS = 60.0  # freezing and history each get this much

TOPIC_NAMES = {
    1: "Code and reuse",
    2: "Callers and interfaces",
    3: "Rules and ADRs",
    4: "Architecture fit",
    5: "Neighbouring specs",
    6: "History and stale assumptions",
    7: "Tests and gates",
    8: "Risks and edge cases",
    9: "Best practice online",
    10: "Tools and standards online",
    11: "Failures online",
}
TOPIC_SCOPES = {
    1: "Existing functions and modules, analogous patterns, changes needed to reuse them and objections. "
    "Scope: mapped code plus direct imports; no new-code proposals.",
    2: "Callers across code, tests, commands, CI, hooks and prompts; signatures, options, formats and "
    "configuration; readers versus changing callers; kit and instance consumers. Scope: connections to the "
    "map, with caller and callee cited.",
    3: "Exact obligations, human-owned paths, required ADR changes and the next number, conflicting rules, "
    "and whether the declared class fits. Scope: repository rules only, no new rules; a class disagreement "
    "is a human decision.",
    4: "The documented layer, the prescribed runner, tracker and gate routes, framework, kit and instance "
    "responsibility, and architecture statements the change would invalidate. Scope: mapped code and "
    "documented architecture only, no target design.",
    5: "Constraints, contradictions, overlap and order, shared resources and the relevance of suggested "
    "neighbours. Scope: the packet neighbours' spec, design, plan and decisions only; contradictions become "
    "human decisions.",
    6: "The last change and its reason, reversals and supersession, stale facts, recorded rationale and "
    "governance of repeatedly changing facts. Scope: the runner-collected mapped history only, cited by full "
    "packet commit hash or frozen `path::section`; proposals await the maintainer.",
    7: "Existing checks, uncovered behaviour, stand-in-only evidence, checks the change breaks, red-first "
    "possibilities and limits. Scope: mapped tests and gates only; write no test and run no verification.",
    8: "Failure paths, unusual input, security boundaries, recovery and concurrent sessions. Scope: mapped "
    "places only; name risks without designing repairs.",
    9: "Approaches, reasons and conditions, disagreements and warnings. Scope: retrieved primary documentation, "
    "papers and projects before secondary pages; tools belong to topic 10, incidents to topic 11.",
    10: "Existing tools, services and libraries, their maturity, version, release and licence, standards and "
    "formats, cost and local or remote execution. Scope: retrieved project sources with dates; no adoption "
    "recommendation.",
    11: "Incidents and causes, vulnerabilities and advisories, traps and mitigations. Scope: retrieved issue "
    "trackers, vendor advisories, CVE records and postmortems with dates; no assertion about our code.",
}
JUDGE_KEYS = {
    "claim_judgements",
    "supported_facts",
    "assumptions",
    "applicability",
    "gaps",
    "human_questions",
    "practice_comparison",
    "architecture_comparison",
    "neighbour_comparison",
    "disagreements",
}
BLOCK = re.compile(r"\n<!-- research-swarm/v2 run [0-9a-f]+ -->.*?<!-- /research-swarm/v2 -->\n", re.S)


class Stop(Exception):
    """The run cannot go on: `code` 1 is an incomplete run, 2 a security refusal."""

    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------


def payload_text(stdout: str) -> str:
    """The model's JSON object: the answer itself, or the single fenced block that holds it."""
    text = (stdout or "").strip()
    found = re.fullmatch(r"```(?:json)?[ \t]*\n(.*)\n```", text, re.S)
    return found.group(1).strip() if found else text


def fence(info: str, body: str) -> str:
    longest = max((len(run) for run in re.findall(r"`+", body)), default=0)
    ticks = "`" * max(3, longest + 1)
    return f"{ticks}{info}\n{body}\n{ticks}"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


SEPARATORS = set(',;()"“”„«»')
DASHES = set("–—")
APOSTROPHES = set("'’")


def public_sentence_problems(answer: str, change: str, bead: str, tracked: set[str]) -> list[str]:
    """The mechanical allow-list for the public sentence (spec «Public topic», S-4 and S-26); empty means accepted."""
    text = unicodedata.normalize("NFC", (answer or "").strip())
    if not text:
        return ["the topic call answered nothing"]
    if text[-1] in ".?":
        text = text[:-1].rstrip()
    if not text:
        return ["the topic is empty"]
    kept: list[str] = []
    for index, char in enumerate(text):
        before = text[index - 1] if index else ""
        after = text[index + 1] if index + 1 < len(text) else ""
        if unicodedata.category(char).startswith("L"):
            kept.append(char)
        elif char.isspace() or char in SEPARATORS:
            kept.append(" ")
        elif char in APOSTROPHES or char == "-":
            joined = unicodedata.category(before or " ").startswith("L") and unicodedata.category(
                after or " "
            ).startswith("L")
            if joined:
                kept.append(char)
            elif char == "-":
                return ["the topic carries a hyphen outside a word"]
            else:
                kept.append(" ")  # at a word edge an apostrophe counts as a quotation mark
        elif char in DASHES:
            if not (before.isspace() and after.isspace()):
                return ["the topic carries a dash outside spaces"]
            kept.append(" ")
        else:
            return [f"the topic carries the character {char!r}, which the allow-list refuses"]
    words = "".join(kept).split()
    if not words:
        return ["the topic holds no word"]
    if len(words) > 20:
        return ["the topic has more than 20 words"]
    for word in words:
        for segment in re.split(r"[-'’]", word):
            if any(a.islower() and b.isupper() for a, b in zip(segment, segment[1:], strict=False)):
                return [f"the topic carries the identifier-shaped token '{word}'"]
    names = {change.lower(), str(bead).lower()}
    for path in tracked:
        parts = PurePosixPath(path).parts
        for part in (*parts, *(PurePosixPath(item).stem for item in parts)):
            if re.search(r"[-_.0-9]", part):
                names.add(part.lower())
    clash = sorted({word for word in words if word.lower() in names})
    if clash:
        return ["the topic names the change, the bead or a repository identifier: " + ", ".join(clash)]
    return []


# ---------------------------------------------------------------------------
# One run
# ---------------------------------------------------------------------------


class Run:
    def __init__(self, root: Path, change: str, runner, klass: str, selection: dict) -> None:
        self.root, self.change, self.runner, self.klass, self.selection = root, change, runner, klass, selection
        self.folder_rel = f"plans/changes/{change}"
        self.research_rel = f"{self.folder_rel}/research.md"
        self.own_spec = f"{self.folder_rel}/spec.md"
        self.lines: list[str] = []  # audit lines, appended once at the end
        self.records: dict[str, dict] = {}
        self.entries: dict[str, dict] = {}
        self.stage_order: list[str] = []
        self.scratch: dict[str, tempfile.TemporaryDirectory] = {}
        self.started_at: dict[str, str] = {}
        self.key: str | None = None
        self.state = None
        self.store: Store | None = None
        self.locked = False
        self.run_id: str | None = None
        self.source = None
        self.not_reused: list[tuple[str, str]] = []
        self.map: dict | None = None
        self.history: dict | None = None
        self.sentence: str | None = None
        self.reports: list[dict] = []
        self.outcomes: list[dict] = []
        self.judge: dict | None = None
        self.judge_text: str | None = None
        self.scores: list | None = None
        self.security: str | None = None
        self.stop = threading.Event()
        self.began = CLOCK()
        self.lock = threading.Lock()

    # -- small helpers ---------------------------------------------------------------------------

    def scrub(self, text: str) -> str:
        return self.runner.scrub(text, self.key) if self.key else text

    @property
    def deadline(self) -> float:
        return self.began + RUN_MINUTES * 60.0

    def read_data(self) -> dict:
        data = stage2_availability.read_declaration(self.root)
        if isinstance(data, str):
            raise self.runner.Refused(data)
        return data

    def seat_id(self, entry: dict) -> str:
        return research_seat_id(entry["endpoint"], entry["model"])

    # -- opening ---------------------------------------------------------------------------------

    def open(self) -> None:
        runner = self.runner
        self.data = self.read_data()
        try:
            self.roles = stage2_availability.research_roles(self.selection, self.data)
            free = (self.selection.get("free") or {}).get("selected")
            self.free = list(free) if isinstance(free, list) else []
            if not isinstance(free, list):
                raise stage2_swarm.ResearchCatalogError("the consumed selection holds no free selection", 2)
            stage2_swarm.role_launches(self.data, self.roles, self.free)
            self.plan_size = len(stage2_swarm.research_slot_plan(self.roles, self.free))
        except (KeyError, TypeError) as error:
            raise runner.Refused("the consumed selection does not hold the six seats") from error
        except stage2_swarm.ResearchCatalogError as error:
            raise runner.Refused(str(error)) from error
        self.given = stage2_availability.given_neighbours(self.root, self.change, runner)
        author = self.roles["topic_author"]
        self.ctx = runner.preflight(
            self.root, self.change, (author["endpoint"], author["model"], "high"), "research.md"
        )
        if any(seat["endpoint"] == GO for seat in self.all_seats()):
            runner.require_pi()
            self.key = runner.reviewer_key()
        self.store = Store(research_dir(self.change), scrub=self.scrub)
        git_dir = stage2_swarm._git(self.root, "rev-parse", "--absolute-git-dir").strip()
        try:
            self.store.assert_outside(self.root, *([git_dir] if git_dir else []))
            self.store.acquire_lock()
        except StoreLocked as error:
            raise runner.Refused(str(error)) from error
        except StoreWriteError as error:
            raise runner.CallFailed(f"the research state store is unusable ({error})") from error
        self.locked = True
        # The runner's appends stamp `updated:`; stamping before the freeze keeps the frozen prefix intact.
        runner.stamp_updated(self.ctx.research)
        try:
            self.state = freeze_research_state(
                self.root, self.folder_rel, deadline=time.monotonic() + PREPARATION_SECONDS
            )
        except ResearchSnapshotError as error:
            raise runner.CallFailed(f"the inputs could not be frozen ({error}); no model call starts.") from error
        self.sources = self.state.sources()
        self.manifest = self.state.manifest()
        self.research_bytes = self.sources[self.research_rel]
        self.binding = stored_binding(self.manifest, self.research_rel, self.research_bytes)
        try:
            self.source = self.store.resume_source(self.manifest, self.research_rel, self.research_bytes)
            self.run_id = self.store.start_run(self.change, self.selection.get("report_id"), self.binding)
        except StoreWriteError as error:
            raise runner.CallFailed(f"the research state store is unusable ({error})") from error
        self.brief = self.build_brief()
        self.agents = self.sources.get("AGENTS.md", b"").decode("utf-8", errors="replace")

    def all_seats(self) -> list[dict]:
        return [
            *self.roles["finder_agents"],
            *self.roles["repository_agents"],
            *self.roles["online_agents"],
            *({"endpoint": GO, "model": ident} for ident in self.free),
        ]

    def text_of(self, relative: str) -> str | None:
        data = self.sources.get(f"{self.folder_rel}/{relative}")
        return data.decode("utf-8", errors="replace") if data is not None else None

    def build_brief(self) -> str:
        """The private brief: frozen research (without earlier runner blocks), decisions and spec, bead id only."""
        research = self.research_bytes.decode("utf-8", errors="replace")
        research = _without_updated(BLOCK.sub("", research).encode()).decode().rstrip()
        parts = [f"# Private brief for the change {self.change}", f"Bead: {self.ctx.bead}", "## research.md", research]
        for name in ("decisions.md", "spec.md"):
            text = self.text_of(name)
            if text is not None:
                parts += [f"## {name}", text.rstrip()]
        return "\n\n".join(parts)

    # -- prompts ---------------------------------------------------------------------------------

    def prompt_file(self, name: str) -> str:
        return (self.root / "prompts" / "research-swarm" / name).read_text(encoding="utf-8")

    def private_brief(self) -> str:
        return "\n\n".join([self.brief, "# Repository rules (AGENTS.md)", self.agents.rstrip()])

    def finder_prompt(self) -> str:
        return "\n\n".join([self.prompt_file("finder.md"), "---", self.private_brief(), self.runner.READ_REQUEST])

    def merge_prompt(self, reports: dict[str, str]) -> str:
        parts = [self.prompt_file("finder-merge.md"), "---"]
        for finder, text in reports.items():
            parts += [f"## Finder {finder}", text]
        return "\n\n".join(parts)

    def sentence_prompt(self) -> str:
        return "\n\n".join([self.prompt_file("public-topic.md"), "---", self.brief])

    def topic_head(self, topic: int, template: str) -> str:
        return (
            self.prompt_file(template)
            .replace("{{TOPIC_ID}}", str(topic))
            .replace("{{TOPIC_NAME}}", TOPIC_NAMES[topic])
            .replace("{{TOPIC_SCOPE}}", TOPIC_SCOPES[topic])
        )

    def repository_prompt(self, topic: int) -> str:
        assert self.map is not None and self.history is not None
        parts = [self.topic_head(topic, "repository.md"), self.prompt_file("report.md"), "---", self.private_brief()]
        packet = {key: self.map[key] for key in ("entries", "scope", "gaps", "not_read")}
        parts += ["# Finder map (data)", json.dumps(packet, ensure_ascii=False, sort_keys=True, indent=2)]
        if topic == 5:
            neighbours = self.map["neighbours"]
            body = (
                json.dumps(neighbours, ensure_ascii=False, sort_keys=True, indent=2)
                if neighbours
                else "no packet neighbour: the packet holds no given or suggested neighbour."
            )
            parts += ["# Packet neighbours (data)", body]
        if topic == 6:
            parts += ["# Mapped history (data)", json.dumps(self.history, ensure_ascii=False, sort_keys=True, indent=2)]
        parts.append(self.runner.READ_REQUEST)
        return "\n\n".join(parts)

    def online_prompt(self, topic: int) -> str:
        assert self.sentence is not None
        head = self.topic_head(topic, "public.md").replace("{{TOPIC}}", self.sentence)
        return "\n\n".join([head, self.prompt_file("report.md")])

    # -- the dispatcher glue ---------------------------------------------------------------------

    def line(self, text: str) -> None:
        with self.lock:
            self.lines.append(text)

    def what(self, entry: dict) -> str:
        return f"swarm {entry['role']}" + (f" · topic {entry['topic']}" if entry["topic"] else "")

    def gate(self, slot: Slot) -> GateVerdict:
        entry = self.entries[slot.slot_id]
        data = stage2_availability.read_declaration(self.root)
        problem = (
            data
            if isinstance(data, str)
            else stage2_swarm.invocation_problem(
                data, entry["role"], entry["endpoint"], entry["model"], selected_free=self.free
            )
        )
        if problem is None:
            result = self.runner.leakcheck.check(
                self.change, self.runner.leakcheck.default_denylist(), self.root, [("prompt", slot.prompt)]
            )
            print(result.verdict.render())
            if result.verdict.exit_code() == 0:
                return GateVerdict(
                    False, {"clean": True, "files": result.files, "commits": result.commits, "rules": result.rules}
                )
            problem = "the leak check is not clean; the call does not start"
        return GateVerdict(True, {"clean": False, "refused": problem})

    def audit(self, slot: Slot, verdict: GateVerdict) -> None:
        entry = self.entries[slot.slot_id]
        record = verdict.record
        self.line(
            f"Stage-2 call, {self.runner.today()}: {self.what(entry)} · run {self.run_id} · "
            f"endpoint {entry['endpoint']} · model {entry['model']} · leak check clean over "
            f"{record['files']} files, {record['commits']} commits, {record['rules']} rules."
        )
        assert self.store is not None and self.run_id is not None
        started = utc()
        self.started_at[slot.slot_id] = started
        self.store.write_launch(self.run_id, slot.slot_id, {**self.key_fields(entry), "launched_at": started})

    def key_fields(self, entry: dict) -> dict:
        return {
            "slot_id": entry["slot_id"],
            "stage": entry["stage"],
            "topic": entry["topic"],
            "seat": entry["seat"],
            "endpoint": entry["endpoint"],
            "model": entry["model"],
            "prompt_sha256": entry["prompt_sha256"],
            "required": entry["required"],
        }

    def on_terminal(self, slot: Slot, result, *, persist: bool = True) -> None:
        entry = self.entries[slot.slot_id]
        receipts = ""
        tmp = self.scratch.pop(slot.slot_id, None)
        if tmp is not None:
            path = Path(tmp.name) / "research" / "receipts.jsonl"
            if path.exists():
                receipts = self.scrub(path.read_text(encoding="utf-8", errors="replace"))
            tmp.cleanup()
        gate = result.gate_record if isinstance(result.gate_record, dict) else {}
        record = {
            **self.key_fields(entry),
            "outcome": result.outcome,
            "started": result.started,
            "returncode": result.returncode,
            "started_at": self.started_at.get(slot.slot_id),
            "ended_at": utc(),
            "stdout": self.scrub(result.stdout or ""),
            "stderr": self.scrub("\n".join((result.stderr or "").splitlines()[-40:])),
            "receipts": receipts,
            "leak_check": gate,
        }
        if result.outcome == "refused":
            record["refused"] = gate.get("refused") or gate.get("audit_error") or gate.get("error") or "refused"
            self.line(
                f"Stage-2 call, {self.runner.today()}: {self.what(entry)} · run {self.run_id} · "
                f"endpoint {entry['endpoint']} · model {entry['model']} · refused - {record['refused']}."
            )
        elif result.started or result.outcome != "cancelled":
            self.line(
                f"Swarm outcome, {self.runner.today()}: {self.what(entry)} · run {self.run_id} · "
                f"model {entry['model']} · {result.outcome}."
            )
        self.records[slot.slot_id] = record
        if not persist:
            return
        assert self.store is not None and self.run_id is not None
        self.store.write_result(self.run_id, slot.slot_id, record)

    # -- launching -------------------------------------------------------------------------------

    def launch(self, slot: Slot, allowance: float):  # noqa: ARG002 - the dispatcher enforces the time
        entry = self.entries[slot.slot_id]
        tmp = tempfile.TemporaryDirectory(prefix="stage2-research-")
        self.scratch[slot.slot_id] = tmp
        scratch = Path(tmp.name)
        try:
            if entry["program"] == "claude-code":
                command, cwd, env = self.claude_command(entry, slot.prompt, scratch)
            else:
                command, cwd, env = self.pi_command(entry, slot.prompt, scratch)
            return subprocess.Popen(  # noqa: S603 - fixed argv, no shell
                command,
                cwd=cwd,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
                start_new_session=True,
            )
        except BaseException:
            self.scratch.pop(slot.slot_id, None)
            tmp.cleanup()
            raise

    def claude_command(self, entry: dict, prompt: str, scratch: Path) -> tuple[list[str], Path, dict]:
        prompt_file = scratch / "work-prompt.md"
        prompt_file.write_text(prompt, encoding="utf-8")
        tools = "" if entry["tools"] == "none" else self.runner.WORK_READ_TOOLS
        command = [
            "claude",
            "-p",
            f"Run the research task for {self.change} exactly as the appended instructions say.",
            "--append-system-prompt-file",
            str(prompt_file),
            "--model",
            entry["model"],
        ]
        if entry.get("effort"):
            command += ["--effort", entry["effort"]]
        command += [
            "--tools",
            tools,
            "--restricted",
            "--safe-mode",
            "--strict-mcp-config",
            "--permission-mode",
            "dontAsk",
            "--permission-prompts",
            "none",
            "--no-session-persistence",
            "--output-format",
            "text",
        ]
        cwd = self.root if entry["tools"] == "repository" else scratch
        return command, cwd, self.runner.foreign_env({})

    def pi_command(self, entry: dict, prompt: str, scratch: Path) -> tuple[list[str], Path, dict]:
        agent = scratch / "agent"
        agent.mkdir()
        (agent / "settings.json").write_text(json.dumps({"retry": {"enabled": False}}), encoding="utf-8")
        stage2_availability.install_measured_models(
            self.runner, agent, (self.selection.get("catalog") or {}).get("models_store")
        )
        home = scratch / "home"
        home.mkdir()
        common = [
            str(self.runner.PI_WRAPPER),
            "--print",
            "--no-session",
            "--no-approve",
            "--no-extensions",
            "--no-mcp",
            "--no-skills",
            "--no-context-files",
            "--no-prompt-templates",
            "--no-themes",
        ]
        model = f"{GO}/{entry['model']}"
        if entry["tools"] == "public":
            research = scratch / "research"
            research.mkdir()
            extension = scratch / "research-tools.mjs"
            source = Path(__file__).resolve().parent / "stage2_research_tools.mjs"
            extension.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            prompt_file = research / "public-prompt.md"
            prompt_file.write_text(prompt, encoding="utf-8")
            command = [
                *common[:5],
                "-e",
                str(extension),
                *common[5:],
                "--tools",
                stage2_swarm.PUBLIC_TOOLS,
                "--model",
                model,
                "--append-system-prompt",
                str(prompt_file),
                "Research the public topic as the appended instructions say.",
            ]
            env = stage2_swarm.public_env(
                {
                    "HOME": str(home),
                    "PI_CODING_AGENT_DIR": str(agent),
                    "OPENCODE_API_KEY": self.key or "",
                    "STAGE2_PUBLIC_RECEIPTS": str(research / "receipts.jsonl"),
                }
            )
            return command, scratch, env
        prompt_file = scratch / "research-prompt.md"
        prompt_file.write_text(prompt, encoding="utf-8")
        command = [
            *common,
            "--tools",
            self.runner.PI_TOOLS,
            "--model",
            model,
            "--append-system-prompt",
            str(prompt_file),
            f"Research the change {self.change} as the appended instructions say.",
        ]
        env = self.runner.foreign_env(
            {"HOME": str(home), "PI_CODING_AGENT_DIR": str(agent), "OPENCODE_API_KEY": self.key or ""}
        )
        return command, self.root, env

    # -- one stage -------------------------------------------------------------------------------

    def entry(self, stage, role, seat, spec, prompt, *, topic=None, required=True, order=None, tools="repository"):
        """One planned slot: identity and exact prompt, frozen before anything starts."""
        free = role == "online_free"
        slot_id = stage if topic is None and seat is None else f"{stage}-{topic if topic else 0}-{seat}"
        if free:
            slot_id = f"{stage}-{topic}-free-{spec['model']}"
        entry = {
            "slot_id": slot_id,
            "stage": stage,
            "role": role,
            "topic": topic,
            "seat": seat,
            "endpoint": spec["endpoint"],
            "model": spec["model"],
            "effort": spec.get("effort"),
            "program": stage2_swarm.LAUNCHERS[spec["endpoint"]],
            "tools": tools,
            "prompt": prompt,
            "prompt_sha256": digest(prompt),
            "required": required,
            "order": order if order is not None else (topic or 0, seat if isinstance(seat, int) else 0, spec["model"]),
        }
        self.entries[slot_id] = entry
        return entry

    def run_stage(self, stage: str, entries: list[dict], validate, *, reserve: float) -> list[dict]:
        """Reuse what the stored run offers, dispatch the rest, and return every slot's record in plan order."""
        assert self.store is not None and self.run_id is not None and self.source is not None
        self.stage_order.append(stage)
        planned = [
            {k: e[k] for k in ("slot_id", "stage", "topic", "seat", "endpoint", "model", "prompt_sha256")}
            for e in entries
        ]
        prefix = stage + "-"
        scoped = dataclasses.replace(
            self.source,
            results={k: v for k, v in self.source.results.items() if k == stage or k.startswith(prefix)},
            interrupted=[k for k in self.source.interrupted if k == stage or k.startswith(prefix)],
        )
        reuse = plan_reuse(scoped, planned, lambda record: validate(self.entries[record["slot_id"]], record))
        self.not_reused.extend(reuse.not_reused)
        for slot_id, record in reuse.reused.items():
            self.store.adopt(self.run_id, self.source, record)
            self.records[slot_id] = {**record, "reused_from": self.source.run_id}
        launch_ids = {item["slot_id"] for item in reuse.to_launch}
        slots = [
            Slot(
                slot_id=e["slot_id"],
                provider="go" if e["endpoint"] == GO else "claude",
                required=e["required"],
                order=e["order"],
                role_allowance=MINUTES[stage] * 60.0,
                identity={k: e[k] for k in ("stage", "topic", "seat", "endpoint", "model", "role")},
                prompt=e["prompt"],
            )
            for e in entries
            if e["slot_id"] in launch_ids
        ]
        if slots:
            result = dispatch(
                slots,
                gate=self.gate,
                launcher=self.launch,
                audit=self.audit,
                on_terminal=self.on_terminal,
                stop=self.stop,
                deadline=self.deadline,
                reserve=reserve,
                clock=lambda: CLOCK(),
            )
            by_id = {slot.slot_id: slot for slot in slots}
            for item in result.results:
                if item.slot_id not in self.records:  # the failed store stopped the callbacks: keep the outcome
                    self.on_terminal(by_id[item.slot_id], item, persist=False)
            for item in result.results:
                if item.outcome == "refused":
                    self.security = self.security or f"{item.slot_id}: {self.records[item.slot_id].get('refused')}"
            if result.exit_code == 2:
                raise Stop("a declaration or leak check refused a call; every queued call was cancelled", 2)
            if result.reason:
                raise Stop(f"the state store stopped the stage ({result.reason}: {result.detail})", 1)
        return [self.records[e["slot_id"]] for e in entries]

    def invalidate(self, record: dict, why: str) -> None:
        """A process success whose payload fails validation is an invalid report, kept as partial evidence."""
        assert self.store is not None and self.run_id is not None
        record["outcome"] = "invalid-report"
        record["error"] = why
        self.store.write_result(self.run_id, record["slot_id"], record)

    # -- stages ----------------------------------------------------------------------------------

    def stages(self) -> None:
        self.stage_finders()
        self.stage_merge()
        self.stage_sentence()
        self.stage_history()
        self.stage_topics()
        self.stage_judge()

    def require_ok(self, records: list[dict], what: str) -> None:
        bad = [r for r in records if r["outcome"] != "ok"]
        if bad:
            names = ", ".join(f"{r['slot_id']} ({r['outcome']})" for r in bad)
            raise Stop(f"{what} failed: {names}; no later stage starts.", 1)

    def stage_finders(self) -> None:
        prompt = self.finder_prompt()
        entries = []
        for number, seat in enumerate(self.roles["finder_agents"], 1):
            entries.append(self.entry("finders", "finder", number, seat, prompt))

        def valid(_entry, record) -> bool:
            try:
                stage2_research_map.validate_locator_report(payload_text(record["stdout"]))
            except stage2_research_map.ResearchMapError:
                return False
            return True

        records = self.run_stage("finders", entries, valid, reserve=MINUTES["judge"] * 60.0)
        for record in records:
            if record["outcome"] == "ok" and not valid(None, record):
                self.invalidate(record, "the finder answer is not the four-list locator object")
        self.require_ok(records, "a finder")
        self.finder_reports = {self.seat_id(self.entries[r["slot_id"]]): payload_text(r["stdout"]) for r in records}

    def map_merge(self, record: dict) -> dict:
        try:
            return stage2_research_map.merge_research_map(
                self.finder_reports, payload_text(record["stdout"]), self.sources, self.given, self.own_spec
            )
        except stage2_research_map.ResearchMapError as error:
            if error.exit_code == 2:
                raise Stop(str(error), 2) from error
            raise

    def stage_merge(self) -> None:
        spec = self.roles["finder_merge"]
        entry = self.entry("merge", "finder_merge", None, spec, self.merge_prompt(self.finder_reports), tools="none")

        def valid(_entry, record) -> bool:
            try:
                self.map_merge(record)
            except (stage2_research_map.ResearchMapError, Stop):
                return False
            return True

        (record,) = self.run_stage("merge", [entry], valid, reserve=MINUTES["judge"] * 60.0)
        self.require_ok([record], "the map merge")
        try:
            self.map = self.map_merge(record)
        except stage2_research_map.ResearchMapError as error:
            self.invalidate(record, str(error))
            raise Stop(f"the map merge is not the exact finder union ({error}); no topic starts.", 1) from error

    def stage_sentence(self) -> None:
        spec = self.roles["topic_author"]
        entry = self.entry("sentence", "topic_author", None, spec, self.sentence_prompt(), tools="none")
        tracked = set(self.sources)

        def problems(record) -> list[str]:
            return public_sentence_problems(record["stdout"], self.change, self.ctx.bead, tracked)

        (record,) = self.run_stage("sentence", [entry], lambda _e, r: not problems(r), reserve=MINUTES["judge"] * 60.0)
        self.require_ok([record], "the public sentence call")
        found = problems(record)
        if found:
            self.invalidate(record, "; ".join(found))
            raise Stop(f"the public topic was rejected ({'; '.join(found)}); no topic starts.", 1)
        self.sentence = " ".join(record["stdout"].strip().split())

    def stage_history(self) -> None:
        assert self.map is not None
        paths = sorted({entry["path"] for entry in self.map["entries"] if entry["status"] == "resolved"})
        try:
            self.history = build_research_history(
                self.root, self.manifest["head"], paths, deadline=time.monotonic() + PREPARATION_SECONDS
            )
        except ResearchHistoryError as error:
            raise Stop(f"the local history could not be collected ({error}); no topic starts.", 1) from error

    def topic_entries(self) -> list[dict]:
        entries = []
        for topic in range(1, 12):
            if topic <= 8:
                prompt = self.repository_prompt(topic)
                for number, seat in enumerate(self.roles["repository_agents"], 1):
                    entries.append(self.entry("topics", "repository", number, seat, prompt, topic=topic))
            else:
                prompt = self.online_prompt(topic)
                for number, seat in enumerate(self.roles["online_agents"], 1):
                    entries.append(self.entry("topics", "online", number, seat, prompt, topic=topic, tools="public"))
        for topic in range(9, 12):
            prompt = self.online_prompt(topic)
            for ident in sorted(self.free):
                spec = {"endpoint": GO, "model": ident}
                entries.append(
                    self.entry(
                        "topics",
                        "online_free",
                        "free",
                        spec,
                        prompt,
                        topic=topic,
                        required=False,
                        tools="public",
                        order=(topic, 0, ident),
                    )
                )
        return entries

    def validate_topic(self, entry: dict, record: dict) -> dict:
        assert self.map is not None
        topic = entry["topic"]
        return validate_research_report(
            payload_text(record["stdout"]),
            run_id=self.run_id,
            topic=topic,
            seat=self.seat_id(entry),
            sources=self.sources,
            history=self.history if topic == 6 else None,
            receipts=stage2_swarm.parse_receipts(record.get("receipts", "")) if topic >= 9 else (),
            neighbours=[item["path"] for item in self.map["neighbours"]] if topic == 5 else (),
        )

    def stage_topics(self) -> None:
        entries = self.topic_entries()

        def valid(entry, record) -> bool:
            try:
                self.validate_topic(entry, record)
            except ResearchReportError:
                return False
            return True

        records = self.run_stage("topics", entries, valid, reserve=MINUTES["judge"] * 60.0)
        for entry, record in zip(entries, records, strict=True):
            report = None
            if record["outcome"] == "ok":
                try:
                    report = self.validate_topic(entry, record)
                except ResearchReportError as error:
                    self.invalidate(record, str(error))
            if report is not None:
                self.reports.append(report)
            self.outcomes.append(
                {
                    "topic": entry["topic"],
                    "seat": self.seat_id(entry),
                    "required": entry["required"],
                    "outcome": record["outcome"],
                }
            )
        failed = [o for o in self.outcomes if o["required"] and o["outcome"] != "ok"]
        if failed:
            names = ", ".join(f"topic {o['topic']} {o['seat']} ({o['outcome']})" for o in failed)
            raise Stop(f"required topic slots did not finish with a valid report: {names}; no judge starts.", 1)

    def validate_judge(self, record: dict) -> dict:
        text = payload_text(record["stdout"])
        value = _load(text)
        _keys(value, JUDGE_KEYS)
        for name in ("supported_facts", "assumptions", "applicability", "gaps", "human_questions"):
            if not isinstance(value[name], list) or any(not isinstance(item, str) for item in value[name]):
                raise ResearchReportError(f"judge field {name} must be a list of strings")
        for name in ("practice_comparison", "architecture_comparison", "neighbour_comparison"):
            if not isinstance(value[name], str) or not value[name].strip():
                raise ResearchReportError(f"judge field {name} must be nonempty text")
        known = {claim["id"] for report in self.reports for claim in report["claims"]}
        if not isinstance(value["disagreements"], list):
            raise ResearchReportError("judge disagreements must be a list")
        for item in value["disagreements"]:
            _keys(item, {"claims", "summary"})
            if (
                not isinstance(item["claims"], list)
                or len(set(item["claims"])) < 2
                or not set(item["claims"]) <= known
                or not isinstance(item["summary"], str)
                or not item["summary"].strip()
            ):
                raise ResearchReportError("a disagreement names at least two known global claim ids and a summary")
        scores = research_claim_scores(
            run_id=self.run_id, reports=self.reports, outcomes=self.outcomes, verdicts=value["claim_judgements"]
        )
        return {"reconciliation": value, "scores": scores}

    def stage_judge(self) -> None:
        assert self.map is not None
        try:
            packet = build_research_judge_packet(
                self.prompt_file("judge.md"),
                run_id=self.run_id,
                map_record=self.map,
                reports=self.reports,
                outcomes=self.outcomes,
            )
        except ResearchJudgeError as error:
            raise Stop(f"the judge packet cannot be built ({error}).", 1) from error
        self.packet_size = packet["size_characters"]
        if not packet["allowed"]:
            raise Stop(
                f"{packet['reason']}: the packet holds {packet['size_characters']} characters.", packet["exit_code"]
            )
        spec = self.roles["judge"]
        entry = self.entry("judge", "judge", None, spec, packet["packet"], tools="none")

        def valid(_entry, record) -> bool:
            try:
                self.validate_judge(record)
            except (ResearchReportError, ResearchJudgeError):
                return False
            return True

        (record,) = self.run_stage("judge", [entry], valid, reserve=0.0)
        self.require_ok([record], "the judge")
        try:
            self.judge = self.validate_judge(record)
        except (ResearchReportError, ResearchJudgeError) as error:
            self.invalidate(record, str(error))
            raise Stop(f"the judge answer failed validation ({error}).", 1) from error
        self.judge_text = record["stdout"]

    # -- publication -----------------------------------------------------------------------------

    def expected_slots(self) -> list[dict]:
        """Every slot identity the run plans (39 + 3N), fixed by the consumed selection before any call."""

        def plain(stage, seat, spec, topic=None, required=True):
            slot_id = stage if topic is None and seat is None else f"{stage}-{topic if topic else 0}-{seat}"
            return {
                "slot_id": slot_id,
                "stage": stage,
                "topic": topic,
                "seat": seat,
                "endpoint": spec["endpoint"],
                "model": spec["model"],
                "required": required,
            }

        plan = [plain("finders", n, seat) for n, seat in enumerate(self.roles["finder_agents"], 1)]
        plan.append(plain("merge", None, self.roles["finder_merge"]))
        plan.append(plain("sentence", None, self.roles["topic_author"]))
        for topic in range(1, 12):
            seats = self.roles["repository_agents"] if topic <= 8 else self.roles["online_agents"]
            plan += [plain("topics", n, seat, topic) for n, seat in enumerate(seats, 1)]
        for topic in range(9, 12):
            for ident in sorted(self.free):
                spec = {"endpoint": GO, "model": ident}
                free_id = f"topics-{topic}-free-{ident}"
                plan.append({**plain("topics", "free", spec, topic, False), "slot_id": free_id})
        plan.append(plain("judge", None, self.roles["judge"]))
        return plan

    def manifest_record(self, status: str) -> dict:
        slots = []
        for _slot_id, record in sorted(self.records.items()):
            slots.append(
                {
                    **{
                        k: record.get(k) for k in ("slot_id", "stage", "topic", "seat", "endpoint", "model", "required")
                    },
                    "prompt_sha256": record.get("prompt_sha256"),
                    "outcome": record["outcome"],
                    "launched": bool(record.get("started")) and "reused_from" not in record,
                    "reused_from": record.get("reused_from"),
                    "started_at": record.get("started_at"),
                    "ended_at": record.get("ended_at"),
                    "leak_check": record.get("leak_check"),
                    "error": record.get("error"),
                }
            )
        for planned in self.expected_slots():  # an aborted run still names every slot it never started
            if planned["slot_id"] not in self.records:
                slots.append(
                    {
                        **planned,
                        "prompt_sha256": None,
                        "outcome": "not-started",
                        "launched": False,
                        "reused_from": None,
                        "started_at": None,
                        "ended_at": None,
                        "leak_check": None,
                        "error": f"never started: {status}",
                    }
                )
        slots.sort(key=lambda slot: slot["slot_id"])
        return {
            "schema": "research-swarm/v2",
            "run_id": self.run_id,
            "change": self.change,
            "class": self.klass,
            "status": status,
            "receipt_id": self.selection.get("report_id"),
            "head": self.manifest["head"],
            "digest": self.manifest["digest"],
            "untracked": self.manifest["untracked"],
            "free_selected": self.free,
            "free_count": len(self.free),
            "budget": 39 + 3 * len(self.free),
            "selection": self.selection.get("seats"),
            "catalog": {k: v for k, v in (self.selection.get("catalog") or {}).items() if k != "models_store"},
            "preparation": {
                key: self.selection.get(key) for key in ("checked_at", "pool", "models", "unread", "audit", "unfilled")
            },
            "resume": {
                "source_run": self.source.run_id if self.source else None,
                "usable": bool(self.source and self.source.usable),
                "reasons": self.source.reasons if self.source else [],
                "interrupted": self.source.interrupted if self.source else [],
                "not_reused": [list(item) for item in self.not_reused],
            },
            "given_neighbours": self.given,
            "slots": slots,
        }

    def inventory(self) -> dict:
        """The runner-derived obligation inventory: raw reports and the judge's structured disagreements only."""
        assert self.map is not None
        disagreements = self.judge["reconciliation"]["disagreements"] if self.judge is not None else []
        return research_handoff.derive_inventory(
            run_id=self.run_id,
            declared_class=self.klass,
            packet=self.map["neighbours"],
            reports=self.reports,
            disagreements=disagreements,
        )

    def publish(self, status: str) -> str:
        """Append the buffered record once, with the status, and return the status line."""
        assert self.store is not None and self.run_id is not None
        parts = [
            f"<!-- research-swarm/v2 run {self.run_id} -->",
            f"## Research swarm — {self.runner.today()}",
            f"run {self.run_id} · class {self.klass} · baseline HEAD {self.manifest['head'][:12]} · "
            f"input digest {self.manifest['digest'][:16]}",
            fence(
                "research-swarm/v2 manifest",
                json.dumps(self.manifest_record(status), ensure_ascii=False, sort_keys=True, indent=2),
            ),
        ]
        if self.map is not None:
            parts.append(
                fence("research-swarm/v2 map", json.dumps(self.map, ensure_ascii=False, sort_keys=True, indent=2))
            )
        if self.sentence:
            parts.append(f"public topic: {self.sentence}")
        if self.history is not None:
            parts.append(
                fence(
                    "research-swarm/v2 history", json.dumps(self.history, ensure_ascii=False, sort_keys=True, indent=2)
                )
            )
        for report in self.reports:
            parts.append(
                fence(
                    "research-swarm/v2 report",
                    json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2, default=str),
                )
            )
        for slot_id in sorted(self.records):
            record = self.records[slot_id]
            if record["outcome"] != "ok" and (record.get("stdout") or record.get("stderr")):
                partial = {k: record.get(k) for k in ("slot_id", "outcome", "error", "stdout", "stderr", "receipts")}
                parts.append(
                    fence("research-swarm/v2 partial", json.dumps(partial, ensure_ascii=False, sort_keys=True))
                )
        if self.judge is not None:
            parts.append(
                fence(
                    "research-swarm/v2 reconciliation",
                    json.dumps(self.judge, ensure_ascii=False, sort_keys=True, indent=2),
                )
            )
        if self.map is not None and self.reports:
            parts.append(
                fence(
                    "research-swarm/v2 inventory",
                    json.dumps(self.inventory(), ensure_ascii=False, sort_keys=True, indent=2),
                )
            )
        if self.judge is None and self.judge_text:
            parts.append("### Judge answer (failed validation — partial evidence)\n\n" + self.judge_text.strip())
        if self.lines:
            parts.append("### Audit\n\n" + "\n".join(f"- {line}" for line in self.lines))
        status_line = f"run {self.run_id} status: {status}."
        parts += [status_line, "<!-- /research-swarm/v2 -->"]
        text = "\n\n".join(parts)
        existing = self.ctx.research.read_bytes()
        tail = (b"\n" if existing and not existing.endswith(b"\n") else b"") + b"\n" + text.rstrip().encode() + b"\n"
        with contextlib.suppress(ResearchSnapshotError, StoreWriteError):  # the record still lands
            self.store.set_append(
                self.run_id, stored_binding(self.manifest, self.research_rel, self.research_bytes, append=tail)
            )
        self.runner.append(self.ctx.research, text)
        return status_line

    def close(self) -> None:
        for tmp in self.scratch.values():
            tmp.cleanup()
        self.scratch.clear()
        if self.state is not None:
            self.state.close()
        if self.store is not None and self.locked:
            self.store.release_lock()


def run(root: Path, change: str, runner, klass: str, selection: dict) -> None:
    """The whole phase-1 run; raises the runner's Refused (exit 2) or CallFailed (exit 1)."""
    current = Run(root, change, runner, klass, selection)
    try:
        current.open()
        stop: Stop | None = None
        try:
            current.stages()
        except Stop as error:
            stop = error
        except (StoreWriteError, ResearchSnapshotError) as error:
            stop = Stop(f"the research state store failed ({error}).", 1)
        status = "complete"
        if stop is not None:
            status = f"incomplete - {stop}"
        else:
            try:
                drift = current.state.changed_paths(deadline=time.monotonic() + PREPARATION_SECONDS)
            except ResearchSnapshotError as error:
                drift = [f"(drift check failed: {error})"]
            if drift:
                status = "incomplete - the frozen input state changed: " + ", ".join(drift)
        failed_free = [
            f"{r['slot_id']} ({r['outcome']})"
            for r in current.records.values()
            if not r.get("required") and r["outcome"] != "ok"
        ]
        if status == "complete" and failed_free:
            status = "complete - best-effort free seats did not finish: " + ", ".join(sorted(failed_free))
        line = current.publish(status)
        complete = status.startswith("complete")
        refusal = {"slot": current.security.split(":")[0], "reason": current.security} if current.security else None
        try:
            current.store.finish_run(current.run_id, "complete" if complete else "incomplete", refusal=refusal)
            if complete:
                current.store.clear()
        except StoreWriteError as error:
            raise runner.CallFailed(f"the research state store could not be finished ({error})") from error
        if stop is not None and stop.code == 2:
            raise runner.Refused(line)
        if not complete:
            raise runner.CallFailed(f"the research run {current.run_id} is incomplete: {status}")
        print(
            f"swarm: eleven reconciled topics appended to {current.ctx.research.relative_to(root)} · run {current.run_id}"
        )
    finally:
        current.close()
