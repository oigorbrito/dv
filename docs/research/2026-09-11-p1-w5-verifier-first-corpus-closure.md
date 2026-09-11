# P1-W5 verifier-first corpus closure

## Result

W5 completed the local work that could increase the development corpus without
weakening the frozen admissibility contract. No model, treatment, benchmark,
candidate solution, or holdout was executed or accessed.

```text
TASK_CORPUS = PARTIAL
ADMITTED_TASKS = 2
ADMITTED_FAMILIES = 2
EXECUTOR_S0 = UNCHANGED_FROM_W4
P1_S1_RELEASE = NO
HOLDOUT = SEALED
```

The Harness self-test passed six tests with exit code `0` at the start of the
wave. The initial and remote heads were both
`2b8b3b9ab8ad2148f40d116613c90a7d16311699`.

## D-F5-01 resolution

D-F5-01 was materialized at
`9cc5d6d722d509175a669624c9235156dffb4f85` in a detached, clean workspace.
The focal verifier file hash is
`8216e56aa683724f2a61368ebc04264174e4207c3694c9793894a98bd886563b`.

The focal command passed 10 tests. The preservation suite passed all 469 tests
after a legitimate repository-defined editable installation in an isolated
venv. The environment used Python 3.13.14, pip 26.2.1, and setuptools 84.0.0
already available on the machine. The setup used no index, no dependency
upgrade, and no source modification.

The previous single failure was causal: the `metao` console script was absent
from the active environment. The historical README and CI use `pip install -e
.`; reproducing that setup restored the script and the preservation suite.
D-F5-01 is therefore `ADMITTED`.

## D-F1-01 resolution

D-F1-01 was checked at
`c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d` in a detached, clean workspace.
The base declares the Microsoft.Testing.Platform runner, while the solution
contains VSTest-targeted test projects. The local SDKs are 10.0.400 and
10.0.401; the base requests 10.0.100 with feature roll-forward.

Both the focal project command and the README-prescribed solution command exit
1 before test execution. Microsoft.Testing.Platform reports that VSTest-targeted
projects are unsupported under the configured runner, including four solution
test projects. No source edit, test-framework migration, or SDK substitution
was made. D-F1-01 remains `BLOCKED_HISTORICAL_TOOLCHAIN_MISMATCH` and is not
admitted.

## Remaining candidates

The existing 18-candidate inventory was consumed. The remaining F1/F5/F2/F3/F4
and F6 candidates retain their previous provenance or verifier failures; no
new candidate was discovered and no retrospective verifier was invented. A
provenance screen was sufficient for candidates whose independent verifier was
not established, so their environments were not reconstructed unnecessarily.

## Corpus and promotion

The admitted corpus now contains D-F5-01 and D-F6-01, spanning F5 and F6. This
supports a two-task pipeline/smoke pilot only; it does not support treatment
ranking, executor ranking, family superiority, generalization, or statistical
claims. `TASK_CORPUS` remains `PARTIAL`.

The strong executor and economic/local/free executor gates remain unresolved
from W4. Consequently `P1_S1_RELEASE=NO` and no smoke spec was created.

## Evidence and cleanup

Raw and normalized evidence is under
`pilot-runs/p1-w5-verifier-first-corpus-closure/`. Earlier evidence was not
overwritten. Temporary clone and venv paths used during diagnosis were
discarded after evidence capture; the preserved historical workspaces remain
outside the repository and are not committed.

The updated corpus is
`experiments/p1/p1-development-corpus-v2.json`. The previous corpus version
remains unchanged. The blocker register records the new D-F1 environment
blocker and leaves executor, Harness-surface, corpus, and strong-credential
blockers open.

## Next objective

First resolve an approved strong executor and complete its provider-native
qualification. In parallel, acquire additional tasks only through the same
verifier-first gate. Do not start P1-S1 until both executor paths, accounting,
Harness evidence, and the smoke corpus gate pass.
