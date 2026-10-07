**In one line:** <what this PR changes, and why, in plain words>.

**Your move:** nothing to decide. Merge (or ask an agent to) when CI is green.

**What could break:** <what could fail after the merge, and where it would show>

done: <verification command>: <result> at <short sha> · <time used> of <appetite>

## What changes
- <behaviour that changed, and why it matters>
- <second change, if any>

## What it touches
<the output of `python3 scripts/touch_map.py origin/main HEAD`, pasted unchanged after the last push>
<for a change with a design.md: "Architecture delta: `plans/changes/<name>/design.md`">

## Where it fits
Phase <n, name> of seven · stage <1> of three · touches: <component, path>

## After the merge
1. <next step> (<who>), or "nothing"

<details><summary>Evidence at <short sha></summary>

- `make verify`: <result> (<date>)
- Beads: <title> (<id>), opened / changed / closed
- Spec, plan: `<paths>`
</details>
