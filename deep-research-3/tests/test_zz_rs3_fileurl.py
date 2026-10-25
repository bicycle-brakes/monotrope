"""Scratch-only (deep-research-3): repository seat path lock vs file:// URLs on the real pinned Pi."""
import subprocess, types, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts")); sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage2, stage2_research_run
from test_pi_contract import StandIn, message_text
SECRET = "/tmp/claude-0/-home-user/ff6888fa-68cd-58d5-94f4-a97c8806208f/scratchpad/deep-research-3/h8/outside/secret.txt"

def test_fileurl(tmp_path):
    standin = StandIn([{"tool_calls": [
        {"name": "read", "arguments": {"path": SECRET}},
        {"name": "read", "arguments": {"path": "file://" + SECRET}},
        {"name": "ls", "arguments": {"path": "file://" + str(Path(SECRET).parent)}},
    ]}, {"content": "done"}])
    store = {"opencode-go": {"models": [{"id": "seat-model", "provider": "opencode-go", "api": "openai-completions",
             "baseUrl": standin.url, "input": ["text"], "contextWindow": 100000, "maxTokens": 1000}]}}
    root = tmp_path / "wt"; root.mkdir(); (root / "a.md").write_text("x")
    fake = types.SimpleNamespace(runner=stage2, selection={"catalog": {"models_store": store}}, key="sk-synthetic-rs3", change="demo", root=root)
    scratch = tmp_path / "scratch"; scratch.mkdir()
    command, cwd, env = stage2_research_run.Run.pi_command(fake, {"tools": "repository", "model": "seat-model"}, "PROMPT", scratch)
    done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=90, stdin=subprocess.DEVNULL)
    standin.close()
    print("\nRC", done.returncode, "REQUESTS", len(standin.requests))
    text = message_text(standin.requests[1])
    print("TOOL-RESULTS", text[text.rfind("</cwd>"):][-900:])
    print("SECRET-REACHED-MODEL", "SECRET-OUTSIDE-RS3" in text)
