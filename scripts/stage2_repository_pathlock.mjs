// The path lock of the swarm's repository seats (decisions.md Q-16, finding F-24).
//
// A repository seat reads the worktree with Pi's four read-only file tools
// (read, grep, find, ls). Those tools accept absolute paths, `..` and symbolic
// links, so a seat could read the model's home directory or the research state
// store (spec criterion 52). This extension is the ONLY one a repository seat
// loads, copied to a generic scratch path before loading. Its `tool_call` gate
// resolves every path argument — with `..` collapsed and symbolic links followed
// (realpath) — and blocks the call unless the result lies inside the worktree
// the seat was started in (its working directory). It is plain JavaScript, so
// the lock holds on every platform Pi runs on; no operating-system sandbox.
//
// The path is judged where Pi itself would open it (review findings RS-3-2 and
// RS-3-6): the lock mirrors Pi 1.2.0's `normalizePath` (unicode spaces to a
// space, a leading "@" stripped, `~` refused, a `file://` URL turned into its
// path with fileURLToPath) and, for read, every fallback name Pi's
// `resolveReadPath` tries when the literal path is missing (the macOS AM/PM,
// NFD and curly-quote variants): each one that exists must stay inside.
//
// Limits, stated: the lock checks the path a tool is called with, not what the
// tool then walks. A symbolic link INSIDE the worktree that points out is
// refused when named directly, but a directory walk (grep, find) does not
// follow links by default in Pi's backends (ripgrep, fd). A glob or search
// pattern is refused when it is absolute, begins with `~` or has a `..` segment.
//
// The pure helpers are exported so tests can drive them without Pi.
import { existsSync, realpathSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const LOCKED_TOOLS = ["read", "grep", "find", "ls"];
const PATH_FIELDS = ["path"];
// The glob of grep's file filter and the glob pattern of find. A grep `pattern` is a regular expression, not a path.
const GLOB_FIELDS = { grep: ["glob"], find: ["pattern"], read: [], ls: [] };

// Resolves the longest existing prefix of `target` (following links) and
// re-appends the rest, so a path that does not exist yet is judged by where it
// would be created.
export function realTarget(target) {
  let existing = target;
  const rest = [];
  for (;;) {
    try {
      return path.join(realpathSync(existing), ...rest.reverse());
    } catch (error) {
      const parent = path.dirname(existing);
      if (parent === existing) throw error;
      rest.push(path.basename(existing));
      existing = parent;
    }
  }
}

// Pi's set of unicode spaces (utils/paths.js UNICODE_SPACES), each read as a plain space.
const UNICODE_SPACES = /[\u00A0\u2000-\u200A\u202F\u205F\u3000]/g;

function normalize(text) {
  // Pi strips a leading "@" and maps unicode spaces to a plain space.
  return String(text).replace(UNICODE_SPACES, " ").replace(/^@/, "");
}

// The absolute path Pi's resolveToCwd gives for an already normalized text; a `file://` URL is
// converted the way Pi converts it (throws when it names no local path).
function piResolve(text, root) {
  const local = /^file:\/\//.test(text) ? fileURLToPath(text) : text;
  return path.isAbsolute(local) ? path.resolve(local) : path.resolve(root, local);
}

// The fallback names Pi's resolveReadPath tries, in its order, when the resolved path is missing.
function readFallbacks(resolved) {
  const amPm = resolved.replace(/ (AM|PM)\./gi, "\u202F$1.");
  const nfd = resolved.normalize("NFD");
  const curly = resolved.replace(/'/g, "\u2019");
  const nfdCurly = nfd.replace(/'/g, "\u2019");
  return [amPm, nfd, curly, nfdCurly].filter((name) => name !== resolved);
}

function escapes(realRoot, target) {
  const relative = path.relative(realRoot, realTarget(target));
  return relative === ".." || relative.startsWith(".." + path.sep) || path.isAbsolute(relative);
}

export function confinementError(rawPath, root, { read = false } = {}) {
  if (typeof rawPath !== "string") return "the path must be a string";
  const text = normalize(rawPath);
  if (text.startsWith("~")) return `the path '${rawPath}' begins with ~, which names a home directory outside the worktree`;
  const realRoot = realTarget(root);
  const outside = `the path '${rawPath}' resolves outside the worktree: repository seats read only inside it`;
  try {
    const resolved = piResolve(text, root);
    if (escapes(realRoot, resolved)) return outside;
    if (read) {
      for (const name of readFallbacks(resolved)) {
        if (existsSync(name) && escapes(realRoot, name)) return outside;
      }
    }
  } catch {
    return `the path '${rawPath}' cannot be resolved inside the worktree`;
  }
  return null;
}

export function patternError(pattern) {
  if (typeof pattern !== "string") return null;
  const text = normalize(pattern);
  if (text.startsWith("~") || path.isAbsolute(text) || /^[a-zA-Z]:[\\/]/.test(text)) {
    return `the pattern '${pattern}' is absolute or begins with ~: repository seats search only inside the worktree`;
  }
  if (text.split(/[\\/]/).includes("..")) {
    return `the pattern '${pattern}' contains a '..' segment: repository seats search only inside the worktree`;
  }
  return null;
}

// The verdict for one tool call: null when allowed, else the reason.
export function gate(toolName, input, root) {
  if (!LOCKED_TOOLS.includes(toolName)) {
    return `the tool '${toolName}' does not exist in a repository seat: only read, grep, find and ls are available`;
  }
  const args = input && typeof input === "object" ? input : {};
  for (const field of PATH_FIELDS) {
    if (args[field] !== undefined && args[field] !== null) {
      const error = confinementError(args[field], root, { read: toolName === "read" });
      if (error) return error;
    }
  }
  for (const field of GLOB_FIELDS[toolName]) {
    const error = patternError(args[field]);
    if (error) return error;
  }
  if (toolName === "read" && typeof args.path !== "string") return "read needs a path inside the worktree";
  return null;
}

export function registerPathLock(pi, root = process.cwd()) {
  if (!pi || typeof pi.on !== "function") {
    throw new Error("this extension needs a Pi host with on(); it refuses to load anywhere else");
  }
  pi.on("tool_call", async (event) => {
    const reason = gate(event && event.toolName, event && event.input, root);
    return reason === null ? undefined : { block: true, reason };
  });
}

export default function (pi) {
  registerPathLock(pi);
}
