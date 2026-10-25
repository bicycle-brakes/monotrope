"""Scratch-only (deep-research-3): catalog samplingParams/headers reach the provider request on the real pinned Pi."""
import json, subprocess, types, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts")); sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage2, stage2_research_run, stage2_swarm
from test_pi_contract import StandIn

def test_sampling(tmp_path):
    # 1. Python's selection admits a seat row carrying samplingParams that rename the model.
    row = {"id": "minimax-m3", "api": "openai-completions", "baseUrl": "https://opencode.ai/zen/go/v1", "input": ["text"],
           "samplingParams": {"model": "kimi-k3"}, "headers": {"x-forged": "1"}}
    bridge = {"exit_code": 0, "pi_version": "1.2.0", "pi_runtime": {"errors": [], "aborted": False}, "baseline": [],
              "models_store": {"opencode-go": {"models": [row]}},
              "sources": {"pi": {"status": 200, "body": json.dumps([row])}, "models_dev": {"status": 503, "outcome": "http-error"}}}
    sel = stage2_swarm.select_research_catalog(bridge, {"provider": "opencode-go", "suffix": "-free", "include": [], "exclude": []},
                                               ["minimax-m3"], expected_version="1.2.0")
    print("\nSEAT-REASON", [m["reason"] for m in sel["models"] if m["id"] == "minimax-m3"])
    # 2. The same row (baseUrl pointed at the loopback stand-in) through the production repository-seat command.
    standin = StandIn([{"content": "done"}])
    store = {"opencode-go": {"models": [dict(row, baseUrl=standin.url, contextWindow=100000, maxTokens=1000)]}}
    root = tmp_path / "wt"; root.mkdir()
    fake = types.SimpleNamespace(runner=stage2, selection={"catalog": {"models_store": store}}, key="sk-synthetic-rs3", change="demo", root=root)
    scratch = tmp_path / "scratch"; scratch.mkdir()
    command, cwd, env = stage2_research_run.Run.pi_command(fake, {"tools": "repository", "model": "minimax-m3"}, "PRIVATE PROMPT", scratch)
    done = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=90, stdin=subprocess.DEVNULL)
    standin.close()
    req = standin.requests[0]
    print("RC", done.returncode, "| --model asked: opencode-go/minimax-m3 | body model sent:", req.body.get("model"), "| x-forged header:", req.headers.get("x-forged"))
