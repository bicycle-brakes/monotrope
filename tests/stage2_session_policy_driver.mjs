// Runs scripts/stage2_session_policy.mjs against made-up events, without Pi and
// without a model. Used by tests/test_stage2_session_policy.py: reads one JSON
// request on stdin, writes one JSON answer per case on stdout.
//
// A case is { mode: "handler", cwd, hasUI, answer, explode, event } (the
// extension as Pi runs it: its default export, its `tool_call` handler) or
// { mode: "decide", event, env } (the pure decision, for what the host fixes) or
// { mode: "platform", platform } (the file-system case rule of a host).
import { pathToFileURL } from "node:url";

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const request = JSON.parse(Buffer.concat(chunks).toString("utf8"));
const policy = await import(pathToFileURL(request.module).href);

const answers = [];
for (const item of request.cases) {
  if (item.mode === "platform") {
    answers.push({ caseInsensitive: policy.caseInsensitiveOn(item.platform) });
    continue;
  }
  if (item.mode === "decide") {
    try {
      answers.push({ decision: policy.decide(item.event, item.env) });
    } catch (error) {
      answers.push({ threw: String(error && error.message) });
    }
    continue;
  }
  const handlers = {};
  const flags = [];
  policy.default({
    on: (name, handler) => {
      handlers[name] = handler;
    },
    registerFlag: (name, options) => {
      flags.push({ name, ...options });
    },
  });
  const asked = [];
  const ctx = {
    cwd: item.cwd,
    hasUI: item.hasUI !== false,
    ui: {
      select: async (title) => {
        asked.push(title);
        if (item.answer === "throw") throw new Error("the UI broke");
        return item.answer;
      },
    },
  };
  let event = item.event;
  if (item.explode) {
    event = {
      toolName: item.event.toolName,
      get input() {
        throw new Error("the input exploded");
      },
    };
  }
  const result = await handlers.tool_call(event, ctx);
  answers.push({ result: result === undefined ? null : result, asked, flags, handlers: Object.keys(handlers) });
}
process.stdout.write(JSON.stringify(answers));
