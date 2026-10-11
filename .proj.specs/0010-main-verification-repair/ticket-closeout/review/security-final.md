# T-0012 security review

## Scope and method

Independent read-only candidate review follows the project security-review skill and upstream context/data-flow/false-positive methodology. Initial two-target frozen WIP: main base=HEAD=merge-base eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a (300 captured files), staging c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7 (115 files); committed/staged empty. See capture-main.json and capture-staging.json. Source hashes matched their manifests. Branches are canonical T12→main and T11 staging projection.

## Findings

HIGH=0, MEDIUM=0; no candidate at confidence>=0.8 required independent false-positive filtering. This is a diff-scoped conclusion, not whole-project security certification.

- scripts/main_publication_verification.py:139-147 limits the new exception to one fixed T1 path, exact 100644 successor identity and two exact receipt/approval byte identities. Other historical entries still use original identity. Different valid ancestor or unrelated approval cannot match pins. Existing wrapper additionally validates done receipt fields, commit existence and staging ancestry.
- New path inputs are constants; existing regular_path rejects absolute/traversal and intermediate/terminal links. Git calls use argv; no newly introduced attacker-controlled shell, unsafe deserialization or executable input.
- Original overlay, ancestry, scope and product inventory checks remain. Existing guard constants compare identically to the reviewed source.
- New closeout HTML and imported historical evidence were inspected statically for script, event handlers, iframe/form and external resource loading. No concrete new injection flow found. Historical T5 HTML's missing CSP is pre-existing hardening, not a new exploitable input.

Rejected concern: an actor already able to rewrite the verifier or concurrently mutate the trusted local checkout has the same trust level as the reviewed tool. No new permission boundary crossing was identified; hypothetical local races are not counted as vulnerabilities. Hash pins are not described as proof of human authorization; original/current authorization sources are separately audited.

## Supplemental delta

After a reproduced fixture bug, test_main_release.py:55 only gained branch -f. Independent supplemental security review confirms unchanged setUp operates in a newly created temporary clone and detaches HEAD first. Only that fixture's local staging ref is updated; no source repository or remote push. Runtime guard is byte-identical to the initial capture. Original conclusion HIGH0/MEDIUM0 stands. Red/green evidence retained; full final suites recorded separately.

## Limits

Read-only reasoning and static HTML analysis; no exploit execution, test rerun by reviewer or rendered HTML. Excluded dependency vulnerability scanning, DoS/rate limiting, low-severity hardening, remote account configuration, CI/deployment, and missing historical browser/print/Production evidence. Reports and delivery summaries appended after review do not expand executable scope.
