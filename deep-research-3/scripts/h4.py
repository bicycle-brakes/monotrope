"""End to end: real catalog bridge -> select_research_catalog -> install_measured_models -> pinned Pi model resolution."""
import json, os, subprocess, sys, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
S = Path(sys.argv[1]); tree = S / "tree"; out = S / "h4"; out.mkdir(exist_ok=True)
sys.path.insert(0, str(tree / "scripts"))
import stage2, stage2_swarm, stage2_availability
GO = "opencode-go"
def model(i, **c):
    return {"id": i, "name": i, "provider": GO, "api": "openai-completions", "baseUrl": "https://opencode.ai/zen/go/v1",
            "reasoning": False, "input": ["text"], "contextWindow": 128000, "maxTokens": 4096, **c}
variant = sys.argv[2]
catalog = [model("alpha-free"), model("beta-free"), model("minimax-m3")]
if variant == "bad-free-input":      # Python's own "pi-malformed" local candidate fault
    catalog.append(model("gamma-free", input="text"))
elif variant == "bad-context":        # a field Python never inspects
    catalog.append(model("other-preview", contextWindow=0))
meta = {GO: {"models": {i: {"id": i, "tool_call": True} for i in ("alpha-free", "beta-free", "gamma-free")}}}
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        body = json.dumps(catalog if self.path.startswith("/api/models/providers/") else meta).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
srv = ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_port}"
js = "const { collectCatalog } = await import(process.argv[1]); console.log(JSON.stringify(await collectCatalog(JSON.parse(process.argv[2]))));"
done = subprocess.run(["node", "--input-type=module", "-e", js, (tree / "scripts/stage2_research_catalog.mjs").as_uri(),
                       json.dumps({"catalogBaseUrl": url, "metadataUrl": url + "/metadata"})],
                      capture_output=True, text=True, env={"PATH": os.environ["PATH"], "HOME": str(out)}, timeout=90)
bridge = json.loads(done.stdout)
policy = {"provider": GO, "suffix": "-free", "include": [], "exclude": []}
sel = stage2_swarm.select_research_catalog(bridge, policy, ["minimax-m3"], expected_version="1.2.0")
print("variant", variant, "| selected", sel["selected"], "| seat minimax-m3 reason",
      [m["reason"] for m in sel["seat_models"] if m["id"] == "minimax-m3"] if "seat_models" in sel else "?",
      "| candidates", [(c["id"], c["reason"]) for c in sel["candidates"]])
agent = out / variant; agent.mkdir(exist_ok=True)
stage2_availability.install_measured_models(stage2, agent, bridge["models_store"])
rt = tree / "tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/model-runtime.js"
script = """
const { ModelRuntime } = await import(process.argv[1]);
const r = await ModelRuntime.create({credentials: { async read() {}, async list() { return []; } }, modelsPath: process.argv[2], refreshOnCreate: false});
await r.refresh({ providers: ['opencode-go'], allowNetwork: false });
const pick = id => { const m = r.getModel('opencode-go', id); return m ? m.api + ' ' + m.baseUrl : 'NOT FOUND'; };
console.log('Pi error:', (r.getError() ?? 'none').split('\\n')[1] ?? 'none', '| alpha-free ->', pick('alpha-free'), '| minimax-m3 ->', pick('minimax-m3'));
"""
d = subprocess.run(["node", "--input-type=module", "-e", script, rt.as_uri(), str(agent / "models.json")],
                   capture_output=True, text=True, env={"PATH": os.environ["PATH"], "HOME": str(agent), "PI_OFFLINE": "1"})
print(d.stdout.strip(), d.stderr.strip()[:200])
srv.shutdown()
