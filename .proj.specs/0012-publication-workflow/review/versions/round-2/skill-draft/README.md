# Skill draft packaging

This is a complete proposed replacement for the existing fourth product skill,
`managing-article-publication`, not a fifth installed skill. Its local.md and future-actions.md
are byte-for-byte copies of the current canonical references. Their repository-relative CLI
link is intentionally target-location-relative: it resolves when installed at the existing
canonical/runtime skill root, not from this nested review copy. Use the real repository CLI
for current local actions; do not execute paths inferred from the draft location.

New SKILL.md and workflow.md route the broader workflow, enforce capability/approval gates
and keep v1 available. The explicit draft notice is removed only in the separately authorized
canonical installation change after approved implementation. openai.yaml is review-copy UI
metadata; actual runtime metadata comes from the existing materializer's preserved policy.

No active canonical/generated package, runtime catalog, global skill or deployment is changed
by creating this draft. See the parent test plan for authoring evaluation versus future product
acceptance. Validation and forward-evaluation evidence is saved under the parent's review/.
