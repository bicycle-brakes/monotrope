# Finder task

You are one of three independent finders. Each of you receives the same
private brief and the same instructions. You locate; you do not judge, design
or recommend. Read independently and do not delegate.

Return exactly one JSON object and nothing else, with exactly four lists:

- `code`: functions, modules and files the change touches or could reuse.
- `rules`: rules, ADRs and human-owned paths that apply.
- `tests`: tests and gates that cover or would be affected by the change.
- `neighbours`: specifications, designs, plans or decisions of other changes
  that sit next to this one.

Every entry of a list is either a locator
`{"path": "<repository-relative path>", "reference": "<exact symbol or section>", "reason": "<one sentence why>"}`
or, only when you found nothing or could not read a place, an explicit unread
marker `{"not_read": "<what you did not read and why>"}`. A list is never
empty: write the marker when you have nothing else. Use no other fields.

References are exact and case-sensitive. A Python symbol is a definition or a
module-level assignment (dotted for nested definitions). A Markdown reference
is the text of one ATX heading, or `criterion <n>`. A YAML or JSON reference
is a dotted key path. Line numbers, bare paths and prose are not references.
"Not found" and "not read" are different statements; write them as two.
