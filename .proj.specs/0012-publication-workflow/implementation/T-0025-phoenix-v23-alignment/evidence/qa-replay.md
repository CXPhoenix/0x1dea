# Reconstruct the exact local QA context

The bundled commits are test inputs, not remote landing evidence. They preserve the exact code, tests, policy and metadata used by the complete runner. The bundle excludes the already public prerequisite histories 8baa132eec03336f6776ea45b0c8e4a6889c3c74 and bf6f872db9aa4a2d3e4a765ef4f171186349f432. `qa-bundle.json` records its SHA-256 and successful local verification.

Use a separate complete clone that contains both prerequisite commits. Never replace refs in the authoring checkout. Fetch the two bundled refs into temporary names, detach at qa-main, and set that disposable clone's named main/staging to the bundled commits before running the original command:

```sh
git fetch /absolute/path/to/qa-context.bundle refs/heads/main:refs/heads/qa-main refs/heads/staging:refs/heads/qa-staging
git checkout --detach qa-main
git update-ref refs/heads/main refs/heads/qa-main
git update-ref refs/heads/staging refs/heads/qa-staging
PYTHONDONTWRITEBYTECODE=1 PUBLICATION_TEST_DEPENDENCIES=/absolute/path/to/reviewed/node_modules python3 scripts/run-current-python-tests.py
```

Use the already reviewed Node 24.13.0 and pnpm 10.28.0. No package installation or automation activation is part of this replay. The original frozen contexts are selected by the unchanged runner. Full execution results and limits are in python-receipt.json, test-context.md and coverage.md.
