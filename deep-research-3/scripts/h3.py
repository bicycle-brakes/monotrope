import json, subprocess, sys
from pathlib import Path
S = Path(sys.argv[1]); tree = S / "tree"; out = S / "h3"
sys.path.insert(0, str(tree / "scripts"))
import stage2
cases = {
  "no-api-no-baseurl-new": [{"id": "fresh-new", "input": ["text"], "type": "chat"}],
  "no-api-no-baseurl-shipped": [{"id": "minimax-m3", "input": ["text"], "type": "chat"}],
  "pi-malformed-input-string": [{"id": "fresh-new", "api": "openai-completions", "baseUrl": "https://opencode.ai/zen/go/v1", "input": ["text"]},
                                 {"id": "x", "input": "text"}],
  "headers-number": [{"id": "fresh-new", "api": "openai-completions", "input": ["text"], "headers": {"x-a": 1}}],
}
runtime = tree / "tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/model-runtime.js"
script = """
const { ModelRuntime } = await import(process.argv[1]);
globalThis.fetch = async () => { throw new Error('network forbidden'); };
const runtime = await ModelRuntime.create({credentials: { async read() {}, async list() { return []; } }, modelsPath: process.argv[2], refreshOnCreate: false});
await runtime.refresh({ providers: ['opencode-go'], allowNetwork: false });
const m = runtime.getModel('opencode-go', process.argv[3]);
console.log(JSON.stringify({error: runtime.getError()?.split('\\n').slice(0,3).join(' | ') ?? null, model: m ? {api: m.api, baseUrl: m.baseUrl} : null}));
"""
for name, models in cases.items():
    agent = out / name; agent.mkdir(parents=True, exist_ok=True)
    try:
        stage2.activate_overlay(agent, {"opencode-go": {"models": models}})
    except Exception as e:
        print(name, "activate_overlay raised", type(e).__name__, e); continue
    done = subprocess.run(["node", "--input-type=module", "-e", script, runtime.as_uri(), str(agent / "models.json"), models[0]["id"]],
                          capture_output=True, text=True, env={"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(agent), "PI_OFFLINE": "1"})
    print(name, done.stdout.strip(), done.stderr.strip()[:300])
