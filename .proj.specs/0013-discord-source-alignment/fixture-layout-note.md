# Current fixture policy serialization

Within owner-approved main/staging fixture alignment, real Git merge-tree exposed a temporary policy JSON conflict: current additions (including the inert workflow) and actual staging's33 dedicated entries both append at the closing common-map hunk. The only conflicting path is engineering-v1.json. Preserve the actual policy files and product merge refusal.

Fixture setup now places all new current fixture common entries before the original-main baseline entries; the baseline relative order and all current values remain identical. This happens deterministically before tree capture and grant hashing, never after a failure or as a retry. No schema/key/identity changes are made by reordering. The source policy bytes are not reordered. The original real merge-tree, exact registry checks, grant digest and assertions run unchanged.

External experiments: moving only current repair additions still conflicted because inert WORKFLOW remained last; moving every new fixture entry including WORKFLOW returned merge-tree exit0. Independent contract review confirmed this remains fixture input preparation, with no product/trust/merge-strategy change. Full-v5 runs were stopped after the focused failure was known and are preserved as interrupted, not passing. Final focused/full evidence is separate.
