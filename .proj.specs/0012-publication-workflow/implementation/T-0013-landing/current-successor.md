# Current/historical verification successor

The four shared source files are byte-identical to the independently reviewed final
T15 packet and final integrated T14/T15 passing code. They are carried by the T13
closeout parent so that neither child ticket requires a separate copy of the shared fix.

A closed T13 must be compared against the exact engineering policy at its actual main
landing, not the rolling future map. Original test_current_baseline.py is unchanged;
its original review/M0 counterfactual runs with fixed #22 code/tracker/assertions.
All new/live cases remain current, and a byte preflight rejects editing the old test.
The new current Git boundary rejects partial/promisor history and implicit transport.

Original v1/publication/main-publication helpers, old runner, old assertions, M0 manifests,
writing packages and all article bytes remain unchanged. This is shared verification
infrastructure, not a legacy candidate migration or a deployment change.
