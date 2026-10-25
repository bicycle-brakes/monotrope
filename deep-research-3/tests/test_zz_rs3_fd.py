"""Scratch-only (deep-research-3): a repository seat's find call on the real pinned Pi when fd is not installed."""
import subprocess, types, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts")); sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage2, stage2_research_run
from test_pi_contract import StandIn, message_text

def test_find(tmp_path):
    standin = StandIn([{"tool_calls": [{"name": "find", "arguments": {"pattern": "*.md"}}]}, {"content": "done"}])
    store = {"opencode-go": {"models": [{"id": "seat-model", "provider": "opencode-go", "api": "openai-completions",
             "baseUrl": standin.url, "input": ["text"], "contextWindow": 100000, "maxTokens": 1000}]}}
    root = tmp_path / "wt"; root.mkdir(); (root / "a.md").write_text("x")
    fake = types.SimpleNamespace(runner=stage2, selection={"catalog": {"models_store": store}}, key="sk-synthetic-rs3", change="demo", root=root)
    scratch = tmp_path / "scratch"; scratch.mkdir()
    command, cwd, env = stage2_research_run.Run.pi_command(fake, {"tools": "repository", "model": "seat-model"}, "PROMPT", scratch)
    print("\nOFFLINE-FLAG", "--offline" in command, "PI_OFFLINE" in env)
    try:
        done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=150)
        print("RC", done.returncode, "STDERR", done.stderr[-600:])
    except subprocess.TimeoutExpired as e:
        print("TIMEOUT", "STDERR", e.stderr, "STDOUT", e.stdout)
    standin.close()
    print("REQUESTS", len(standin.requests))
    if len(standin.requests) > 1:
        print("TOOL-RESULT", message_text(standin.requests[1])[-600:])
    print("AGENT-BIN", sorted(p.name for p in (scratch / "agent").rglob("*")))
