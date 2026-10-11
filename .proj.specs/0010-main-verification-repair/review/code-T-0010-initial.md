# Initial implementation review

Frozen packet: base/HEAD/merge-base 88b9c53852f527ee636bcc4b4ca5e166f6ec10fd; 36 files, 2 tracked modifications, committed/staged diffs empty. Three independent read-only reviewers received the same hashes and contents. Snapshot drift: zero.

## Standards

P0=0/P1=0/P2=0; no actionable smell findings. Historical fixture uses fixed epoch input, bilingual sync matches, coverage report exists before stage 6 and the ticket remains review. No tests were independently rerun by this reviewer.

## Spec

P0=0/P1=1/P2=0. main_publication_verification.py:112–113 reused allowed_new when selecting existing protected files. Existing article-publication/materializer code and publication tests are allowed additions under the old policy, but are not CODE trust roots. Excluding them lets modification/deletion bypass the new live-source hash guard, violating M2's merged main plus only reviewed repair and management additions. Remedy: protect every existing released entry except the four explicit CODE sources, with a public CLI regression. All other reviewed fixed pins, complete scope, history separation and negative boundaries had no identified defect.

## Security

Initial candidate review: zero qualifying HIGH/MEDIUM findings at confidence >=0.8. Git uses argv, scope/pins are fixed and symlink handling is explicit. Reviewed verifier code remains a trust root; content hashes do not authenticate human authority. The functional Spec P1 remains a blocker until fixed and re-reviewed. No exploit execution or whole-project security claim. Dependency/DoS/low-hardening/deployment excluded.

Tests in the initial packet: 54 Vitest, 64 harness methods, 16 publication methods; eight command exits zero. These pass results did not waive the Spec finding. Final review must cover the corrected code and new regression.
