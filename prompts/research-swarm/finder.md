# Finder task

You are one of three independent finders. Each of you receives the same
private brief and the same instructions. You locate; you do not judge, design
or recommend. Read independently and do not delegate.

Return exactly one JSON object and nothing else. Its form is the JSON Schema
appended below this task (`finder-locator.schema.json`): four lists, `code`,
`rules`, `tests` and `neighbours`, whose entries are locators or explicit
unread markers. The schema's descriptions are part of the task: they say what
each list holds and what counts as an exact reference.
