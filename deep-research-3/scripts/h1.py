import json, subprocess, sys
from pathlib import Path
S = Path(sys.argv[1]); tree = S / "tree"; out = S / "h1"
sys.path.insert(0, str(tree / "scripts"))
import stage2
good = {"id": "minimax-m3", "provider": "opencode-go", "api": "openai-completions",
        "baseUrl": "https://opencode.ai/zen/go/v1", "input": ["text"], "contextWindow": 1000, "maxTokens": 100}
bad = dict(good, id="other-model", contextWindow=0)   # violates Pi's exclusiveMinimum 0
for name, models in (("good-only", [good]), ("good-plus-bad", [good, bad])):
    agent = out / name; agent.mkdir(parents=True, exist_ok=True)
    stage2.activate_overlay(agent, {"opencode-go": {"models": models, "lastModified": 0, "checkedAt": 1}})
    runtime = tree / "tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/model-runtime.js"
    script = """
const { ModelRuntime } = await import(process.argv[1]);
globalThis.fetch = async () => { throw new Error('network forbidden'); };
const runtime = await ModelRuntime.create({credentials: { async read() {}, async list() { return []; } }, modelsPath: process.argv[2], refreshOnCreate: false});
const result = await runtime.refresh({ providers: ['opencode-go'], allowNetwork: false });
console.log(JSON.stringify({error: runtime.getError()?.slice(0,200) ?? null, model: runtime.getModel('opencode-go', 'minimax-m3') ? {api: runtime.getModel("opencode-go","minimax-m3").api, baseUrl: runtime.getModel("opencode-go","minimax-m3").baseUrl} : null}));
"""
    done = subprocess.run(["node", "--input-type=module", "-e", script, runtime.as_uri(), str(agent / "models.json")],
                          capture_output=True, text=True, env={"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(agent), "PI_OFFLINE": "1"})
    print(name, done.stdout.strip(), done.stderr.strip()[:300])
