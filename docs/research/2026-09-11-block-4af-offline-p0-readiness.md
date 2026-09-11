# BLOCK 4AF — Offline P0 readiness / 24-run materialization

Date: 2026-09-11
Repository: `oigorbrito/dv`
Entry state: `BLOCK_4AE = COMPLETE / INCONCLUSIVE / API_QUOTA_OR_BILLING_BLOCKED`
Holdout: `SEALED / NOT OPENED`

## Scope and constraints

This block prepared local P0 artifacts without any paid model call. No OpenAI API was called, no token estimate was made, no candidate was produced, and no treatment was executed. Corpus, treatment bindings, pricing snapshot, oracle semantics, and Harness v1 were not changed.

The frozen P0 order was used exactly:

```text
F1: E0, E1, E2, E3
F2: E1, E2, E3, E0
F3: E2, E3, E0, E1
F4: E3, E0, E1, E2
F5: E0, E1, E2, E3
F6: E1, E2, E3, E0
```

## Local Git sources and SHA availability

Discovery was restricted to `C:\Projetos` and did not modify any source checkout. `metaO` was found at
`C:\Projetos\metao-gate`, whose origin identifies `oigorbrito/metaO`.

| Repository | Path | .git | Origin | HEAD | Branch | Worktree |
|---|---|---|---|---|---|---|
| RJ | `C:\Projetos\RJ` | present | compatible | `4282cd5c836f81c6da95d17cf317c05525b417d7` | `preserve/rjudi-local-2026-09-08-192438` | dirty, 42 lines |
| metaO | `C:\Projetos\metao-gate` | present | compatible | `2f730773d073a5c4c5bd05b7ae4c0a4f2481a533` | `qualification/issue-396-ado-terminal-provenance` | dirty, 9 lines |
| smag | `C:\Projetos\smag` | present | compatible | `cca06e6bbf6c5d0c4b654a5807b5ddd2be16fb7b` | `fix/supervisor-session-bootstrap` | dirty, 5 lines |

For each task, `cat-file -e <SHA>^{commit}` and `show -s --format=fuller <SHA>` were executed. All six objects were available; no fetch or SHA substitution occurred.

| Task | Repository | Frozen base | Historical object |
|---|---|---|---|
| D-F1-01 | `oigorbrito/RJ` | `c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d` | AVAILABLE |
| D-F2-01 | `oigorbrito/metaO` | `5c3bcdfb0c8aec778727a756f484a4b67a23601d` | AVAILABLE |
| D-F3-01 | `oigorbrito/smag` | `76ef9277062085e113c14bf1fdbb9c4bd218045b` | AVAILABLE |
| D-F4-01 | `oigorbrito/metaO` | `9d35699eb9f9e85e13a7c59b7acbf391dfb4c685` | AVAILABLE |
| D-F5-01 | `oigorbrito/metaO` | `9cc5d6d722d509175a669624c9235156dffb4f85` | AVAILABLE |
| D-F6-01 | `oigorbrito/metaO` | `5d00cd284ce8fe810b0f5192c56d98608be516d4` | AVAILABLE |

Result: `6/6 HISTORICAL_OBJECT = AVAILABLE`. Raw evidence: `pilot-runs/block-4af-offline-readiness/evidence/source-discovery.json`.

## Isolated base workspaces

Six local no-hardlink clones were materialized under `pilot-runs/block-4af-offline-readiness/workspaces/<TASK-ID>` and checked out detached at the exact base SHA. All six proved exact HEAD, detached HEAD and clean worktree. Source dirty states remained unchanged.

| Task | HEAD | Detached | Clean | Provenance |
|---|---|---:|---:|---|
| D-F1-01 | `c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d` | YES | YES | `C:\Projetos\RJ` |
| D-F2-01 | `5c3bcdfb0c8aec778727a756f484a4b67a23601d` | YES | YES | `C:\Projetos\metao-gate` |
| D-F3-01 | `76ef9277062085e113c14bf1fdbb9c4bd218045b` | YES | YES | `C:\Projetos\smag` |
| D-F4-01 | `9d35699eb9f9e85e13a7c59b7acbf391dfb4c685` | YES | YES | `C:\Projetos\metao-gate` |
| D-F5-01 | `9cc5d6d722d509175a669624c9235156dffb4f85` | YES | YES | `C:\Projetos\metao-gate` |
| D-F6-01 | `5d00cd284ce8fe810b0f5192c56d98608be516d4` | YES | YES | `C:\Projetos\metao-gate` |

Result: `6/6 isolated workspace status = PASS`. Raw identities: `evidence/workspace-identities.json` and `evidence/workspace-verification.txt`.

## Toolchain readiness

```text
git    2.55.0.windows.5
python 3.13.14
dotnet 10.0.401
node   v24.18.0
npm    11.16.0
cargo  1.98.0 (797e8a9bc 2026-08-05)
rustc  1.98.0 (88d9e12ae 2026-08-18)
```

All required tools were available. This is not dependency/readiness proof for the frozen repository contents. Raw evidence: `evidence/toolchains.json`.

## Oracle command readiness

The frozen commands were executed against clean base workspaces only. Stdout, stderr and exit codes are preserved under `evidence/oracle/` and summarized in `oracle-command-readiness.json`. These are base-readiness results, not treatment outcomes.

| Task | Result | Exit codes | Observed limitation |
|---|---|---|---|
| D-F1-01 | FAIL | focal 1; preservation 1 | compilation failure |
| D-F2-01 | FAIL | focal 1; preservation 1 | test modules/import `metao` unavailable |
| D-F3-01 | FAIL | focal 1 | declared Node test path absent |
| D-F4-01 | ENVIRONMENT_BLOCKED | candidate-focal 101 | Cargo test target absent; controlled Fail-to-Pass replay remains required |
| D-F5-01 | FAIL | focal 1; preservation 1 | import `metao` unavailable |
| D-F6-01 | FAIL | all 101 | `Cargo.toml` absent in frozen base |

F4 was not redefined: the frozen manifest still requires controlled Fail-to-Pass replay in addition to the candidate focal command.

## 24 identities and concrete run specs

The 24 deterministic identities are `<TASK-ID>--<E[0-3]>--r1`, in the frozen task-specific order above. The output contains 24 treatment specs plus 6 task oracle binding specs under `pilot-runs/block-4af-offline-readiness/run-specs/`.

```text
concrete treatment specs: 24/24
unique treatment run IDs: 24
executor command: BLOCKED_OFFLINE_NO_EXECUTOR
executor surface: BLOCKED
holdout_allowed: false
```

E3 specs preserve the frozen family model map. Their reasoning effort is `null` because the frozen binding does not specify one for E3; no value was invented. E2 preserves initial Luna/medium plus deterministic escalation semantics.

## Treatment binding audit

The audit compared only the frozen binding, operational manifest and generated specs:

```text
E0: gpt-5.6-sol / high / strongest-direct
E1: gpt-5.6-luna / medium / direct plus verify
E2: gpt-5.6-luna / medium -> deterministic certificate -> gpt-5.6-sol / high
E3: F1 Luna, F2 Sol, F3 Sol, F4 Sol, F5 Luna, F6 Luna
```

Result: `TREATMENT_BINDING_AUDIT = PASS` (`evidence/treatment-binding-audit.json`).

## Harness v1 static validation and readiness matrix

Every concrete spec passed the existing `tools/dv_pilot_harness.py::validate_spec` function. The Harness self-test also passed.

```text
RUN_SPEC_READINESS_PASS = 24/24
unique run IDs = 24
holdout references = 0
solution/gold-patch references = 0
missing telemetry treated as zero = false
Harness self-test = PASS (6 tests, exit code 0)
```

The full 24-row matrix (task, family, treatment, base object, workspace, toolchain, oracle command, run-spec, Harness status, executor surface and readiness) is preserved in `evidence/readiness-matrix.json`. All 24 rows have `EXECUTOR_SURFACE = BLOCKED`; local oracle failures make `offline_ready_count = 0`.

## Classification, blockers and limitations

```text
BLOCK_4AF = COMPLETE
BLOCK_4AF_OUTCOME = OFFLINE_P0_READINESS_PARTIAL
HISTORICAL_SHA_AVAILABILITY = 6/6
ISOLATED_WORKSPACES = 6/6 PASS
OFFLINE_READY_RUNS = 0/24
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
HOLDOUT = SEALED
```

Remaining blockers are separate:

1. Authorized paid executor/provider surface and quota/billing remain unavailable; no treatment can run here.
2. Frozen-base oracle commands are not locally executable in this environment: F1 compilation fails, F2/F5 lack importable `metao` test dependencies, F3 lacks the declared test path, and F4/F6 lack required Cargo targets/files.
3. F4 additionally requires the already-frozen controlled Fail-to-Pass replay; this block did not redefine or execute it.

This block proves artifact generation, object availability, isolated workspace identity and static Harness schema readiness. It does not prove treatment behavior, provider telemetry, cost, verified task success, P0 measurement readiness or release. Base command failures are not treatment failures.

## Next defensible step

Resolve the local base/oracle execution prerequisites without changing the frozen protocol, then rerun only the declared readiness commands. Separately restore an authorized executor with provider-native telemetry. Until both conditions are met, `REAL_P0_RUNS` remains `0/24` and `P0_RELEASE` remains `NO`.
