// Runs scripts/stage2_repository_pathlock.mjs against scripted tool calls, without Pi and
// without network. Used by tests/test_stage2_repository_pathlock.py: reads one JSON
// request on stdin ({ module, root, cases }), writes one JSON answer per case on stdout.
//
// A case is { tool, input } — the tool_call gate of the loaded extension, as Pi calls it —
// or { load: true } — what the extension registers on a host — or { load: "no-host" }.
import { pathToFileURL } from "node:url";

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const request = JSON.parse(Buffer.concat(chunks).toString("utf8"));
const extension = await import(pathToFileURL(request.module).href);

const answers = [];
for (const item of request.cases) {
  try {
    if (item.load) {
      const events = [];
      const host = item.load === "no-host" ? {} : { on: (name) => events.push(name), registerTool: () => events.push("registerTool") };
      extension.default(host);
      answers.push({ events });
    } else {
      const handlers = {};
      extension.registerPathLock({ on: (name, fn) => { handlers[name] = fn; } }, request.root);
      const result = await handlers.tool_call({ toolName: item.tool, input: item.input }, {});
      answers.push({ result: result === undefined ? null : result });
    }
  } catch (error) {
    answers.push({ threw: String((error && error.message) || error) });
  }
}
process.stdout.write(JSON.stringify(answers));
