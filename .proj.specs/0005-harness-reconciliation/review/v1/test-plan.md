# Approved existing-seam test plan

| Seam | Intent | Scope | AC | Boundary conditions |
|---|---|---|---|---|
| Existing Python unittest + public verifier CLI | actual red→green source/path/provenance rejection | disposable real-Git clones, clean baseline and approved overlay | R1–R5 | altered bytes/type/missing, unknown untracked path, stale record, invalid pin, changed historic manifests; source untouched |
| Existing complete harness Python suite | retain original guard rejection semantics | original materializer/tracker/publication fixtures plus reconciliation | R1,R2,R4,R6 | old lint successor fixtures use pinned lint epoch rather than copying later mutable product bytes |
| Existing product Vitest/lint/build/materializer/structure | no product/config behavior regression | same installed tools, integrated candidate | R5,R6 | no installs; false/main build retains behavior; precise failures disclosed |
