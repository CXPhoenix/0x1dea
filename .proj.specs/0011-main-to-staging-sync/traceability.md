# Traceability

| Type | Field | Boundary | Expected behavior | AC |
|---|---|---|---|---|
| Git | parents and pinned refs | isolated merge / remote readback | main ancestry imported; main and staging targets untouched | S1,S5 |
| Source | existing staging paths / candidates / assets / article / listing | Git identity inventory | exact staging identities except three integration sources | S1,S3 |
| Source | main helper / release tests / evidence | merge inventory | retain main additions and immutable helper/tests | S1,S3 |
| Guard | provenance / scope / fallback | current public CLI and disposable fixtures | select only existing contract; reject tampering without fallback | S2 |
| History | old hashes / modes / pins / manifests | both contract negative suites | immutable historical oracles preserved | S2,S3 |
| Tracker | blocked / unresolved dependencies / lint fixture | existing tracker suite | keep staging views and pinned main-safe lint read | S3 |
| Runtime | tests / build / browser / review | existing complete commands and browser | actual passes, counts, limits and independent findings | S4 |
| Delivery | branch / PR / status | GitHub PR and refs | push ticket branch, target staging, leave unmerged/review | S5 |
