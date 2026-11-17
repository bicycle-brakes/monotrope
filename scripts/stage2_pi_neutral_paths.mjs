// Keeps machine-local location identifiers out of every request a Pi launch of
// the runner sends to a model (plans/changes/pi-neutral-paths/spec.md).
//
// It is plain ESM with no imports beyond node's own, copied into each launch's
// private directory and loaded explicitly with `pi --no-extensions -e <copy>`
// beside the launch's other extension. What it does, on pinned Pi 1.5.0:
//   1. `before_agent_start`: the prompt's working-directory section reads `.`
//      (the process working directory and the tools' root do not move), the
//      `<docs>` section with Pi's installation paths is dropped, and context
//      files whose resolved location lies outside the working directory are
//      removed - a parent, global or symlink-escaped instruction file reaches
//      no request, one inside the repository stays.
//   2. `before_provider_request`: known local prefixes (working directory,
//      home, agent directory, this launch's private directory, the Pi install)
//      are replaced in every string of the outgoing payload - system prompt,
//      messages, tool results and errors - while the local transcript and the
//      tools' arguments stay as they are. A home or worktree path that survives
//      the replacement (another spelling of it) stops the process before the
//      request is sent: Pi swallows an error a handler throws and sends the
//      request anyway, so the stop is a process exit, not a throw.
// The pure helpers are exported; the real-Pi contracts that hold this file
// against the pinned install live in `tests/test_pi_contract.py`.

import { realpathSync, writeSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { dirname, isAbsolute, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

export const STOP_CODE = 78;
export const NEUTRAL_CWD = ".";

const THIS_FILE = fileURLToPath(import.meta.url);

function real(path) {
  try {
    return realpathSync.native(path);
  } catch {
    return undefined;
  }
}

function escape(text) {
  return text.replace(/[.*+?^${}()|[\]\\\/]/g, "\\$&");
}

function usable(path) {
  return typeof path === "string" && path.length > 1 && path !== sep && isAbsolute(path);
}

function unique(paths) {
  return [...new Set(paths.filter(usable))];
}

// The root of the pinned install this process runs from: the part of the entry
// script's path that precedes `node_modules`.
export function installPrefix(entry) {
  if (typeof entry !== "string" || !entry) return undefined;
  for (const candidate of [entry, real(entry)]) {
    if (!candidate) continue;
    const at = candidate.indexOf(`${sep}node_modules${sep}`);
    if (at > 0) return candidate.slice(0, at);
  }
  return undefined;
}

// The prefixes to replace and the prefixes that must not survive, for one launch.
// `env` is { cwd, home, agent, own, tmp, entry }.
export function localPrefixes(env) {
  const make = (paths, token) => unique(paths.flatMap((path) => [path, real(path)])).map((path) => ({ path, token }));
  const entries = [
    ...make([env.cwd], NEUTRAL_CWD),
    ...make([env.home], "~"),
    ...make([env.agent], "<agent>"),
    ...make([env.own], "<launch>"),
    ...make([env.tmp], "<tmp>"),
    ...make([installPrefix(env.entry)], "<pi>"),
  ];
  // Longest first, so a private directory inside the worktree is named before the worktree.
  const seen = new Set();
  return entries
    .sort((a, b) => b.path.length - a.path.length)
    .filter((entry) => (seen.has(entry.path) ? false : seen.add(entry.path)));
}

function replacerOf(prefixes) {
  return prefixes.map(({ path, token }) => ({
    pattern: new RegExp(`(?<![\\w.~-])${escape(path)}(?![\\w.-])`, "g"),
    token,
  }));
}

export function neutralText(text, prefixes) {
  let out = text;
  for (const { pattern, token } of replacerOf(prefixes)) out = out.replace(pattern, token);
  return out;
}

// A copy of a JSON-shaped value with every string neutralized; other values stay.
export function neutralValue(value, prefixes) {
  const compiled = replacerOf(prefixes);
  const walk = (item) => {
    if (typeof item === "string") return compiled.reduce((text, { pattern, token }) => text.replace(pattern, token), item);
    if (Array.isArray(item)) return item.map(walk);
    if (item && typeof item === "object") {
      const proto = Object.getPrototypeOf(item);
      if (proto !== Object.prototype && proto !== null) return item;
      return Object.fromEntries(Object.entries(item).map(([key, inner]) => [key, walk(inner)]));
    }
    return item;
  };
  return walk(value);
}

// Home and worktree locations still readable in `text`, in any letter case.
export function survivors(text, env) {
  const guarded = unique([env.cwd, real(env.cwd), env.home, real(env.home)]);
  return guarded.filter((path) => new RegExp(`(?<![\\w.~-])${escape(path)}(?![\\w.-])`, "i").test(text));
}

export function isInside(root, target) {
  const rel = relative(root, target);
  return rel === "" || (rel !== ".." && !rel.startsWith(`..${sep}`) && !isAbsolute(rel));
}

// Context files whose resolved target lies inside `cwd`. A file whose location
// cannot be resolved is not kept; an unresolvable `cwd` throws, and the caller stops.
export function repositoryContext(files, cwd) {
  const root = realpathSync.native(resolve(cwd));
  return files.filter((file) => {
    try {
      return isInside(root, realpathSync.native(resolve(root, file.path)));
    } catch {
      return false;
    }
  });
}

const DOCS_SECTION = /<docs>\n[\s\S]*?\n<\/docs>\n*/;

export function withoutDocs(prompt) {
  return prompt.replace(DOCS_SECTION, "");
}

export function stop(reason) {
  try {
    writeSync(2, `stage2 neutral paths: ${reason}; the request was not sent.\n`);
  } catch {
    // nothing left to say it to
  }
  process.exit(STOP_CODE);
}

function launchEnv(cwd) {
  return {
    cwd: cwd || process.cwd(),
    home: process.env.HOME || homedir(),
    agent: process.env.PI_CODING_AGENT_DIR,
    own: dirname(THIS_FILE),
    tmp: tmpdir(),
    entry: process.argv[1],
  };
}

export default function (pi) {
  pi.on("before_agent_start", async (event, ctx) => {
    try {
      const cwd = (ctx && ctx.cwd) || process.cwd();
      const options = event.systemPromptOptions;
      options.contextFiles = repositoryContext(options.contextFiles || [], cwd);
      options.cwd = NEUTRAL_CWD;
      return { systemPrompt: withoutDocs(event.systemPrompt) };
    } catch (error) {
      stop(`the prompt could not be neutralized (${error && error.message})`);
    }
  });
  pi.on("before_provider_request", async (event, ctx) => {
    try {
      const env = launchEnv(ctx && ctx.cwd);
      const payload = neutralValue(event.payload, localPrefixes(env));
      const left = survivors(JSON.stringify(payload), env);
      if (left.length) stop("a home or worktree path survived the neutralization");
      return payload;
    } catch (error) {
      stop(`the request could not be neutralized (${error && error.message})`);
    }
  });
}
