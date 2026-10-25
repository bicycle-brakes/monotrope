"""Scratch-only capture (deep-research-3): the production public-researcher command on the real pinned Pi."""
import json, subprocess, types, sys
from pathlib import Path
import sys; sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts")); sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage2, stage2_research_run
from test_pi_contract import StandIn, tool_names, message_text

def test_capture(tmp_path):
    standin = StandIn([
        {"tool_calls": [
            {"name": "read", "arguments": {"path": "/etc/hostname"}},
            {"name": "bash", "arguments": {"command": "id > /tmp/pwned-rs3"}},
            {"name": "public_fetch", "arguments": {"url": "https://127.0.0.1/"}},
        ]},
        {"content": "done"},
    ])
    store = {"opencode-go": {"models": [{"id": "capture-free", "provider": "opencode-go", "api": "openai-completions",
             "baseUrl": standin.url, "input": ["text"], "contextWindow": 100000, "maxTokens": 1000}]}}
    fake = types.SimpleNamespace(runner=stage2, selection={"catalog": {"models_store": store}}, key="sk-synthetic-rs3")
    scratch = tmp_path / "scratch"; scratch.mkdir()
    entry = {"tools": "public", "model": "capture-free"}
    command, cwd, env = stage2_research_run.Run.pi_command(fake, entry, "PUBLIC PROMPT MARKER", scratch)
    done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=120)
    standin.close()
    first = standin.requests[0]
    print("RC", done.returncode, "STDERR", done.stderr[-500:])
    print("TOOLS", sorted(tool_names(first)))
    print("SYSTEM-HAS-PROMPT", "PUBLIC PROMPT MARKER" in message_text(first)); print("FIRST-REQUEST", message_text(first)[:3000])
    if len(standin.requests) > 1:
        print("RESULTS", message_text(standin.requests[1])[-1500:])
    print("PWNED", Path("/tmp/pwned-rs3").exists())
