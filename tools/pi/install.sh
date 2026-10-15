#!/bin/sh
# Install the runner's own Pi (bead coding-harness-agx, ADR 0019): exactly the
# manifest dependency in the exact lock-file graph, with every dependency's
# lifecycle scripts disabled. The install may reach the npm registry once;
# running Pi afterwards never does. A failed install stops here with a
# non-zero exit and no partial fallback.
set -eu

dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
pkg="@earendil-works/pi-coding-agent"

say() {
    echo "tools/pi/install.sh: $*" >&2
    exit 1
}

for file in package.json package-lock.json .node-version; do
    [ -f "$dir/$file" ] || say "$file is missing from $dir; a fresh clone carries it (see tools/pi/README.md)."
done

command -v node >/dev/null 2>&1 ||
    say "node is not on PATH; install Node $(cat "$dir/.node-version") (see tools/pi/README.md)."
command -v npm >/dev/null 2>&1 ||
    say "npm is not on PATH; it ships with Node (see tools/pi/README.md)."

want_major=$(sed -n 's/^\([0-9][0-9]*\)\..*/\1/p' "$dir/.node-version")
[ -n "$want_major" ] || say ".node-version holds no <major>.<minor>.<patch> version."
have_major=$(node -p 'process.versions.node.split(".")[0]') || say "the Node on PATH could not be measured."
[ "$have_major" = "$want_major" ] ||
    say "Node $have_major is not the declared major $want_major (tools/pi/.node-version); the contracts measure the declared toolchain."

pin=$(sed -n 's/^[[:space:]]*"@earendil-works\/pi-coding-agent":[[:space:]]*"\([^"]*\)".*/\1/p' "$dir/package.json" | head -n 1)
[ -n "$pin" ] || say "package.json declares no $pkg dependency."
printf '%s\n' "$pin" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' ||
    say "\"$pin\" is not an exact <major>.<minor>.<patch> version; a floating pin is no pin."

# npm ci installs the lock file's exact graph and refuses a manifest/lock
# mismatch or a broken integrity value on its own; --ignore-scripts keeps
# every package's install scripts from running.
cd -- "$dir"
exec npm ci --ignore-scripts
