import json, sys
sys.path.insert(0, sys.argv[1] + "/tree/scripts")
import stage2_swarm
GO = "opencode-go"
pi_models = [{"id": i, "api": "openai-completions", "input": ["text"]} for i in ("alpha-free", "minimax-m3")]
def bridge(md):
    return {"exit_code": 0, "pi_version": "1.2.0", "pi_runtime": {"errors": [], "aborted": False}, "baseline": [],
            "models_store": {GO: {"models": pi_models}},
            "sources": {"pi": {"status": 200, "body": json.dumps(pi_models)}, "models_dev": {"status": 200, "outcome": "ok", "body": md}}}
policy = {"provider": GO, "suffix": "-free", "include": [], "exclude": []}
clean = '{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"minimax-m3":{"id":"minimax-m3","tool_call":true,"cost":{"input":1}}}}}'
nested = '{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"minimax-m3":{"id":"minimax-m3","tool_call":true,"cost":{"input":1,"input":2}}}}}'
entry = '{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"beta-free":{"id":"beta-free","tool_call":true,"tool_call":false},"minimax-m3":{"id":"minimax-m3","tool_call":true}}}}'
for name, md in (("clean", clean), ("dup-key-nested-in-unrelated-paid-entry", nested), ("dup-key-inside-one-free-entry", entry)):
    r = stage2_swarm.select_research_catalog(bridge(md), policy, [], expected_version="1.2.0")
    print(name, "| selected", r["selected"], "| capability", r["capability_status"], r["capability_reason"], "| alpha", [c["reason"] for c in r["candidates"] if c["id"] == "alpha-free"])
