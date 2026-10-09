// The policy of an interactive Pi session started by `scripts/stage2.py session`.
//
// Pi asks for no approval and has no sandbox (docs/security.md of the pinned
// Pi 1.1.0), so the runner supplies the policy itself: this file, copied into
// the session's private directory and loaded explicitly with
// `pi --no-extensions -e <copy>`. It is plain ESM with no imports beyond node's
// own, so a copy runs anywhere, and `tests/test_stage2_session_policy.py` runs
// it without Pi and without a model.
//
// What it enforces (plans/changes/stage2-session/spec.md, criterion 11):
//   (a) read, grep, find, ls, edit and write may touch only a path inside the
//       worktree, as Pi resolves it (a leading `@`, `~`, `file://`, symlinks);
//       a find pattern or grep glob that reaches outside is blocked too;
//   (b) edit and write may not touch this file, `.stage2-sessions/` or `.pi/`
//       of the worktree (`.git/` is not protected: maintainer's answer Q-3);
//   (c) a `bash` call that matches a dangerous pattern asks first, and is
//       blocked when no UI can ask (Q-2); any other `bash` call runs unasked;
//   (d) any failure of the handler blocks the call.
// It confines the file tools, not the shell: an approved or unlisted `bash`
// command can read and write whatever the maintainer's user can.

import { realpathSync } from "node:fs";
import { homedir } from "node:os";
import { basename, dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

export const FLAG = "stage2-session-policy";
export const PATH_TOOLS = ["read", "grep", "find", "ls", "edit", "write"];
export const WRITE_TOOLS = ["edit", "write"];
// Relative to the worktree. The runner's own launch files live under the first.
export const PROTECTED_DIRS = [".stage2-sessions", ".pi"];

// `git`, then any global options (`-C <dir>`, `-c k=v`, `--no-pager`), then a space: the verb follows.
const GIT = String.raw`\bgit(?:\s+-\S+(?:\s+[^-\s]\S*)?)*\s+`;

// Dangerous `bash` patterns. The first three are the ones of Pi's shipped
// example `permission-gate.ts`; the rest are the runner's addition for what the
// previous OpenCode policy kept shut: a network client, a push, a hard reset.
// The list is one array: extend it here and in its test.
export const DANGEROUS = [
  { id: "rm-recursive", pattern: /\brm\b[^\n;|&]*\s(-[a-zA-Z]*[rR][a-zA-Z]*|--recursive)\b/ },
  { id: "sudo", pattern: /\bsudo\b/ },
  { id: "chmod-777", pattern: /\b(chmod|chown)\b.*777/ },
  { id: "network-client", pattern: /\b(curl|wget|scp|rsync|ssh|sftp|nc|ncat)\b/ },
  { id: "git-push", pattern: new RegExp(`${GIT}push\\b`) },
  { id: "git-reset-hard", pattern: new RegExp(`${GIT}reset\\b[^\\n;|&]*--hard\\b`) },
  { id: "git-clean", pattern: new RegExp(`${GIT}clean\\b`) },
];

const UNICODE_SPACES = /[  -   　]/g;
const THIS_FILE = fileURLToPath(import.meta.url);

// A path the way Pi's `resolvePath` reads it (dist/utils/paths.js, Pi 1.1.0).
export function resolveToolPath(input, cwd, home) {
  if (typeof input !== "string" || input.includes("\0")) {
    throw new Error("the path is not a string, or holds a NUL byte");
  }
  let path = input.replace(UNICODE_SPACES, " ");
  if (path.startsWith("@")) path = path.slice(1);
  if (path === "~") path = home;
  else if (path.startsWith("~/")) path = join(home, path.slice(2));
  if (/^file:\/\//.test(path)) path = fileURLToPath(path);
  return isAbsolute(path) ? resolve(path) : resolve(cwd, path);
}

// The real path of the deepest part that exists, with the rest appended, so a
// symlink inside the worktree cannot lead a new file out of it. Any other
// failure (a loop, no permission) throws, and a throw blocks the call.
export function canonical(path) {
  const tail = [];
  let head = path;
  for (;;) {
    try {
      const real = realpathSync.native(head);
      return tail.length ? join(real, ...tail.reverse()) : real;
    } catch (error) {
      if (error.code !== "ENOENT" && error.code !== "ENOTDIR") throw error;
      const parent = dirname(head);
      if (parent === head) throw error;
      tail.push(basename(head));
      head = parent;
    }
  }
}

function fold(path, caseInsensitive) {
  return caseInsensitive ? path.toLowerCase() : path;
}

export function isInside(root, target, caseInsensitive) {
  const rel = relative(fold(root, caseInsensitive), fold(target, caseInsensitive));
  return rel === "" || (rel !== ".." && !rel.startsWith(`..${sep}`) && !isAbsolute(rel));
}

// A find pattern or grep glob that is anchored elsewhere or climbs out.
function reachesOut(glob) {
  if (typeof glob !== "string") return false;
  const text = glob.replace(UNICODE_SPACES, " ");
  return /^[/~@]/.test(text) || /^file:/.test(text) || text.split(/[\\/]/).includes("..");
}

function block(reason) {
  return { action: "block", reason: `stage2 session policy: ${reason}` };
}

// The decision for one tool call. Pure apart from reading the file system:
// `env` is { cwd, home, ownFile, caseInsensitive }. Returns
// { action: "allow" } | { action: "block", reason } | { action: "ask", title }.
export function decide(event, env) {
  const tool = event.toolName;
  const input = event.input;
  if (tool === "bash") {
    const command = input && input.command;
    if (typeof command !== "string") return block("a bash call without a command");
    const hit = DANGEROUS.find((entry) => entry.pattern.test(command));
    return hit
      ? { action: "ask", title: `Dangerous command (${hit.id}):\n\n  ${command}\n\nAllow?` }
      : { action: "allow" };
  }
  if (!PATH_TOOLS.includes(tool)) return { action: "allow" };

  const root = canonical(resolve(env.cwd));
  const given = input.path;
  const required = tool === "read" || tool === "edit" || tool === "write";
  if (given === undefined && !required) {
    // grep, find and ls search the working directory when no path is given.
  } else {
    const target = canonical(resolveToolPath(given, env.cwd, env.home));
    if (!isInside(root, target, env.caseInsensitive)) {
      return block(`${tool} on a path outside the worktree`);
    }
    if (WRITE_TOOLS.includes(tool)) {
      const own = canonical(env.ownFile);
      const guarded = PROTECTED_DIRS.map((name) => canonical(join(root, name)));
      if (fold(target, env.caseInsensitive) === fold(own, env.caseInsensitive)) {
        return block(`${tool} on the policy's own file`);
      }
      if (guarded.some((dir) => isInside(dir, target, env.caseInsensitive))) {
        return block(`${tool} on a protected directory`);
      }
    }
  }
  if (tool === "find" && reachesOut(input.pattern)) return block("a find pattern that reaches outside the worktree");
  if (tool === "grep" && reachesOut(input.glob)) return block("a grep glob that reaches outside the worktree");
  return { action: "allow" };
}

export default function (pi) {
  // Listed by `pi --help` when this file is loaded: how the runner confirms the load.
  pi.registerFlag(FLAG, {
    description: "stage2 session policy: file tools bounded to the worktree, dangerous shell commands ask",
    type: "boolean",
    default: true,
  });
  pi.on("tool_call", async (event, ctx) => {
    try {
      const verdict = decide(event, {
        cwd: ctx.cwd,
        home: homedir(),
        ownFile: THIS_FILE,
        caseInsensitive: process.platform === "darwin" || process.platform === "win32",
      });
      if (verdict.action === "block") return { block: true, reason: verdict.reason };
      if (verdict.action === "ask") {
        if (!ctx.hasUI) return { block: true, reason: "stage2 session policy: a dangerous command and no UI to ask" };
        const choice = await ctx.ui.select(verdict.title, ["Yes", "No"]);
        return choice === "Yes" ? undefined : { block: true, reason: "stage2 session policy: refused by the user" };
      }
      return undefined;
    } catch (error) {
      return { block: true, reason: `stage2 session policy: the handler failed (${error && error.message})` };
    }
  });
}
