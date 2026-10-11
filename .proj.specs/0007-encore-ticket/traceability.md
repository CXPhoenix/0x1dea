# Traceability

| Type | Field | Boundary | Expected behavior | Acceptance criterion | Evidence seam |
|---|---|---|---|---|---|
| Ticket | title, href, description | Trusted author → Vue | Exact independent text/destination; escaped plain text | E1 | Component mount |
| Ticket | description omitted | Trusted author → Vue | No empty description paragraph | E1 | Component mount |
| Author guide | Markdown examples | Author → registered component | Both description-present and description-omitted examples use the public props | E1 | Guide inspection + existing component mount |
| Article | registration, instance | Markdown → VitePress SSR | Real component, one ticket, intact following section | E2 | Actual build output |
| Ticket | stub, perforation, notches, action | CSS → browser | Approved D structure and existing theme tokens | E3 | Browser light/dark |
| Ticket | title, description, width | Browser → narrow layout | Wrapped, unclipped, no horizontal overflow | E3 | Browser 1280px/390px |
| Ticket | focus, link name, decoration | Keyboard/assistive tree → anchor | Visible native link focus; no decorative announcement | E4 | Browser keyboard/tree |
| Ticket | href | Anchor activation → target article | Original destination in same tab | E4 | Browser navigation |
| Source | existing article bytes | Task-entry working tree → final tree | Only recommendation paragraph replaced; caption WIP retained | E5 | Exact source comparison |
| Source | image/time/dependency/history | Existing source → final tree | Unchanged unrelated source and preservation rules | E5 | Bounded diff/hash inventory |
| Project | checks, publication | Local validation → delivery | Passing product checks; separate baseline and authorized-delta preservation rejections; strict independent source comparison; no external write | E6 | Existing commands/evidence |
