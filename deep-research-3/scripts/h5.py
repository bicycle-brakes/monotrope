import json, subprocess, sys
from pathlib import Path
S = Path(sys.argv[1]); tree = S / "tree"; out = S / "h5"
sys.path.insert(0, str(tree / "scripts"))
import stage2
cases = {
  "api-no-baseurl-shipped": [{"id": "minimax-m3", "api": "openai-completions", "input": ["text"]}],
  "id-number-row": [{"id": "minimax-m3", "api": "openai-completions", "baseUrl": "https://opencode.ai/zen/go/v1", "input": ["text"]}, {"id": 7, "input": ["text"]}],
}
runtime = tree / "tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/model-runtime.js"
script = """
const { ModelRuntime } = await import(process.argv[1]);
globalThis.fetch = async () => { throw new Error('network forbidden'); };
const runtime = await ModelRuntime.create({credentials: { async read() {}, async list() { return []; } }, modelsPath: process.argv[2], refreshOnCreate: false});
await runtime.refresh({ providers: ['opencode-go'], allowNetwork: false });
const m = runtime.getModel('opencode-go', process.argv[3]);
console.log(JSON.stringify({error: runtime.getError()?.split('\\n').slice(0,2).join(' | ') ?? null, model: m ? {api: m.api, baseUrl: m.baseUrl} : null}));
"""
for name, models in cases.items():
    agent = out / name; agent.mkdir(parents=True, exist_ok=True)
    stage2.activate_overlay(agent, {"opencode-go": {"models": models}})
    done = subprocess.run(["node", "--input-type=module", "-e", script, runtime.as_uri(), str(agent / "models.json"), "minimax-m3"],
                          capture_output=True, text=True, env={"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(agent), "PI_OFFLINE": "1"})
    print(name, done.stdout.strip(), done.stderr.strip()[:300])
