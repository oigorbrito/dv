# P1-W1F — Readiness closure

Date: 2026-09-11
Repository: `C:\Projetos\dv`
Initial HEAD: `771bfda344f0be08eb36fd6df32d25880d6a658e`
Current phase: `P1-S0_EXECUTOR_AND_HARNESS_QUALIFICATION`

## Result

```text
P1_PROTOCOL = INTERNALLY_CONSISTENT
TASK_CORPUS = PARTIAL
EXECUTOR_S0 = PARTIAL
HARNESS_P1_READINESS = PARTIAL
P1_S1_RELEASE = NO
HOLDOUT = SEALED
ARCHITECTURE_APPROVAL = NONE
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
```

No treatment comparison, model generation, paid API call, model download, solution application, or holdout access occurred.

## Baseline and remote state

The local branch is `main`, HEAD is the expected master-plan commit, and `origin/main` remains at
`85af7db00f5753825311b744807bb12a858806b9`. The divergence is `REMOTE_ONLY=0`, `LOCAL_ONLY=14`. The remote blocker is
recorded as `P1-W1-BLK-001`; all local readiness work continued. Historical untracked workspaces remain preserved and
outside this commit:

```text
pilot-runs/block-4aa-d-f1-01-e0-r1/workspace/
pilot-runs/block-4ab-d-f1-01-e0-r1/workspace/
pilot-runs/block-4af-offline-readiness/workspaces/
pilot-runs/block-4ai-protocol-repair/workspaces/
```

They are referenced by prior evidence/docs, so no deletion, `git clean`, stash, overwrite, or broad ignore rule was used.
Their observed aggregate sizes were retained in the session evidence; they are historical materializations, not new P1
normative artifacts.

## Corpus revisita

The six F1/F5 candidate bases were materialized as fresh archive trees from their exact historical SHAs without modifying
source checkouts. D-F1-01 produced exit code 1 because the frozen .NET configuration requires Microsoft.Testing.Platform
while the project uses VSTest; no source/toolchain mutation was made. D-F5-01 focal execution passed 10/10 tests, while
the 469-test preservation suite had one installed console-script failure. This is environment/setup drift, not treatment
failure. F1-02/F1-03/F5-02/F5-03 were not run with substitute tests because no independent focal verifier was bound.

D-F6-01 passed the consistency check: exact base/verifier IDs and hashes, workspace paths, preservation suite and master
plan references remain valid. Its status remains `ADMISSIBLE_FOR_P1`, not treatment execution.

The normative matrix is [corpus-readiness-matrix-v1.json](../../pilot-runs/p1-w1-readiness/corpus-readiness-matrix-v1.json).
It records `TASK_CORPUS=PARTIAL`; the one admitted task remains `SMOKE_TEST_ONLY`.

## Local executor discovery

Observed surfaces were Python 3.13.14, Node 24.18.0, Docker 29.7.2, NVIDIA utility with GeForce GTX 1650 / 4096 MiB,
and WSL availability from the previous inventory. Ollama, vLLM, `llama-server`, and `llama-cli` were not found. No
`ollama list` or model download was attempted because Ollama was absent. Docker was recorded as an environment capability,
not as an executor.

Remote credential presence was checked only as booleans; values were not printed or persisted. Presence does not qualify a
remote executor. The updated qualification matrix records six credential-blocked remote candidates, one download-required
local candidate, one local environment-blocked candidate, and two framework-only candidates.

## Harness audit and contracts

Harness v1 already represents run identity, task/executor identity, invocation logs, candidate artifacts, verifier and
preservation evidence, environment provenance, telemetry missingness, hashing, timeout handling and failure attribution.
The only observed limitation is surface-specific retry/escalation semantics and lack of a dedicated normalized GPU/energy
schema. Neither blocks the current admitted D-F6-01 path; no Harness change was required. No provider-neutral runtime or
adapter was built.

The ten contract validation cases confirm that credential-blocked, download-required, environment-blocked, absent
telemetry, missing energy, verifier/oracle/Harness failures, and a complete smoke-compatible result have distinct
representations. Missing measurements remain missing and never become zero.

## Promotion recalculation

Accounting representation, one admissible task, and holdout isolation pass. The required strong path and economic/local/free
path do not: no executor is `S0_READY` or `S0_READY_TELEMETRY_LIMITED`. Consequently `P1_S1_RELEASE=NO` and no smoke run
was started.

The next actions, in order, are: resolve the nearest corpus verifier/environment gap; qualify a strong executor; qualify
an economic/local/free executor; close native telemetry/accounting; address any demonstrated surface-specific Harness gap;
materialize S1 specs; then execute smoke only after release gates pass.

## Evidence and limitations

Evidence is under `pilot-runs/p1-w1-readiness/`, including the snapshot, baseline replay, corpus matrix, executor matrix,
Harness audit, contract cases, promotion recalculation and validation. Previous block evidence was not overwritten.

This wave establishes readiness status only. It does not establish executor quality, treatment ranking, token savings,
cost savings, or architectural merit. The remote remains behind local history and requires a later clean-worktree
fast-forward reconciliation. The historical workspace directories still prevent a clean push gate, but they were not
classified as external blockers and were preserved.
