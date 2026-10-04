# Open questions

No unresolved architectural choice blocks the approved local adoption. The owner
approved the complete site move and the two precise canonical alias-input mappings.

- Future landing/deployment: separate authorization is required. Target staging is
  configured for local workflow, while CF production remains main. Revisit when the
  owner authorizes actual landing and deployment verification. Current screenshot
  settings do not prove a successful build.
- CF root-dependency watch coverage: the owner selected `blog/*`; package.json,
  pnpm-lock.yaml and tsconfig.json watches are recommendations only. Revisit with
  the owner before changing external build settings.
- Existing empty-result controls, missing README screenshot, lower-case helper import
  portability and public CSS link discrepancy remain baseline issues. This adoption
  does not change their scope or represent their future fixes as completed tickets.
