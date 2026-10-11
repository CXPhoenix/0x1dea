# Round 1 — frozen spec

Base/HEAD/merge-base: 88b9c53852f527ee636bcc4b4ca5e166f6ec10fd. Parent supplied a frozen manifest, five untracked file contents and three empty diffs. Four independent read-only reviewers used the unchanged prompt. Completeness, Verifiability and Contract conflict: P0=0/P1=0/P2=0. Red team: P0=0/P1=1/P2=0.

## P1: Git history overlays

Git replace refs or legacy grafts can change the meaning of pinned objects and ancestry. Resolve inside T-0010: reject replacement refs and graft files before the current release guard; use Git's --no-replace-objects for its oracle/ancestry reads. Add a public CLI negative case beginning with accepted main. No round 2 is needed: zero P0, and this finding is an implementation constraint under the original immutable-object requirement.

All results are spec-only, not evidence of passing implementation tests. Existing historical rules remain intact.

Implementation resolution: the public CLI replace/graft regression passed; original Git objects are read with --no-replace-objects and overlays are explicitly rejected. The full final 65-method harness also passes.
