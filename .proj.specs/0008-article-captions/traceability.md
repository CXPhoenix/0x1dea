# Traceability

| Type × field × boundary | Expected behavior | Criterion |
|---|---|---|
| Figure × id/title/alt/src × Markdown → SSR | Caption once, numbered semantic figure, alt/src retained | C1 |
| Meme/banner × alt/src × Markdown → SSR | Ordinary image unchanged, no number | C1, C6 |
| Table × id/caption/body × Markdown → SSR | Native caption; separate counter; ordinary table unchanged | C2 |
| Figure/table × references/order × document | Forward/backward links, reorder/insertion updates, document reset | C3 |
| Reference × text context × inline parser | Chinese adjacency; small note; exclude code/escapes/links/attributes/images | C3, C4 |
| Caption × markup/URL × rendering | Emphasis/source links, escaped HTML/Vue, safe schemes | C4 |
| Block/reference × invalid input × renderer | Duplicate/unknown/wrong-kind/invalid-id/body/caption/fence diagnostic | C5 |
| Article × authored bytes × migration | Three figures, eight original images, all references/citations, bounded delta | C6 |
| Figure/table/reference × layout/a11y × browser | Desktop/mobile/light/dark; focus, hash, navigation and SSR | C7 |
| Existing product × checks/authority × local delivery | Compatibility and truthful limits, no external action | C8 |
| Author guide × syntax/diagnostics × author → renderer | Copyable guide examples compile and explain all supported forms | C9 |
