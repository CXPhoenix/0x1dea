# Batch implementation and combined PR authority

Owner message on 2026-10-24 (Asia/Taipei):

> B ~ D 做完後全部一起 PR
> 授權給你，把 B ~ D 一次做完

This extends the earlier allocation/TDD authority to implementing B–D with their unchanged approved tables, committing the reviewed ticket changes and pushing a new branch to open one combined A–D engineering PR against main. Existing main-first design and separate merge/staging/publication authority remain. Do not merge the PR or alter deployment/account/trust/credential/global-skill settings.

The batch may stack reviewed local predecessor implementations before their common PR lands. Preserve permanent dependency edges and review status; an unlanded predecessor is not falsely marked done. Separate ticket branches/commits identify A–D. Revalidate the complete combination; no earlier pass proves a later slice.
