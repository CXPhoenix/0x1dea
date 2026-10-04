# Cloudflare Pages owner handoff

The owner independently changed Cloudflare. The parent inspected the actual pixels of Library `libfile_d33cc20e295c81918b60e1d41867b001`; this worker uses that attributed attestation rather than claiming its own live CF inspection. The older screenshot described docs; the newer screenshot states:

| Field | Latest supplied screenshot |
| --- | --- |
| Repository | CXPhoenix/0x1dea |
| Build command | npx vitepress build blog |
| Output directory | blog/.vitepress/dist |
| Root directory | blank |
| Included watch path | blog/* |
| Production branch | main |
| Automatic deployments | Enabled |
| Build system | Version 3 (not Node version) |
| Comments / cache | Enabled / Disabled |

Node/pnpm versions, excluded watch paths, preview settings and any successful deployment remain unverified. No CF login/API/write, push or deploy was performed. Local actual pnpm docs:build uses blog and emits an output byte-identical to the baseline.

Cloudflare documents watch globs as crossing directory separators, so blog/* includes .vitepress changes. Excluded paths take precedence; remaining changed paths matching any include can trigger a build. A blog/*-only include does not cover root package.json, pnpm-lock.yaml or tsconfig.json. Add those root dependency/config paths if the owner wants such changes to trigger automatic builds. This is a recommendation, not evidence that the dashboard was changed or permission to change it.

The screenshot's production main and the authorized future Harness landing target staging are distinct. This local candidate has not landed on either. Until main contains the whole blog tree, a future automatic build with the new command can fail; no unauthorized push is a remedy. Preserve current CF/account/security settings and use a later separately authorized landing/deployment decision.

Primary references: [Cloudflare build watch paths](https://developers.cloudflare.com/pages/configuration/build-watch-paths/), [build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/). The cited behavior was checked during the parent/worker's earlier handoff analysis; the screenshot attribution above is the source for actual displayed settings.
