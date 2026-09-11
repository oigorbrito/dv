# Block 4Z — First real run / P0 release decision

Date: 2026-09-10
Repository: `oigorbrito/dv`
Status: COMPLETE / INCONCLUSIVE / EXECUTION BLOCKED
Holdout: SEALED / NOT OPENED

## Frozen packet

The run was attempted exactly with the Block 4Y packet:

- task: `D-F1-01`
- family: `F1`
- repository: `oigorbrito/RJ`
- base revision: `c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d`
- treatment: `E0`
- model: `gpt-5.6-sol`
- reasoning effort: `high`
- escalation: `none`
- rollout: `r1`
- oracle: frozen F1 oracle through `tools/dv_oracle_adapter.py`
- harness: `tools/dv_pilot_harness.py` (Harness v1)

No corpus, treatment, harness, oracle, or holdout artifact was changed or opened.

## Workspace and toolchain preflight

The dv checkout identity at the start of the run was:

```text
checkout: C:\Projetos\dv
HEAD: 85af7db00f5753825311b744807bb12a858806b9
branch: main
worktree: clean
python: 3.13.14
dotnet: 10.0.401
```

The frozen historical workspace could not be materialized. The exact command was:

```text
python tools/dv_workspace_materializer.py --repository oigorbrito/RJ --revision c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d --destination C:\Projetos\dv\pilot-runs\block-4z-d-f1-01-r1\workspace --identity-out C:\Projetos\dv\pilot-runs\block-4z-d-f1-01-r1\evidence\D-F1-01-workspace.json
```

Result:

```text
exit code: 1 (Python exception; underlying git clone exit code: 128)
fatal: unable to access 'https://github.com/oigorbrito/RJ.git/': Failed to connect to github.com:443 after 41 ms: Could not connect to server
```

No historical workspace, clean-base identity, candidate state, or workspace identity evidence was produced.

## Execution and verification status

Because materialization failed, the protocol stopped at the required pre-execution boundary:

| Stage | Result | Reason |
|---|---|---|
| historical workspace at frozen SHA | NOT_EXECUTED | GitHub transport unavailable |
| E0 / `gpt-5.6-sol` / `high` / `r1` | NOT_EXECUTED | no authorized candidate workspace |
| provider-native telemetry | MISSING/UNRESOLVED | E0 did not start |
| frozen F1 oracle | NOT_EXECUTED | no candidate state |
| Harness v1 run | NOT_EXECUTED | no valid run spec/workspace |
| Harness v1 reconciliation | NOT_EXECUTED | no run to reconcile |

The raw failed materialization attempt is retained under:
`pilot-runs/block-4z-d-f1-01-r1/`.

## Decision

```text
BLOCK_4Z = COMPLETE
BLOCK_4Z_OUTCOME = INCONCLUSIVE / EXECUTION_BLOCKED
P4-BLK-007 = AUTHORIZED_REAL_EXECUTION_SURFACE_REQUIRED (OPEN)
REAL_DRY_RUNS = 0
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
BLOCK_5 = BLOCKED
HOLDOUT = SEALED
ARCHITECTURE_APPROVAL = NONE
TREATMENT_APPROVAL = NONE
```

This is not a treatment failure and does not support treatment ranking. The run did not reach E0, telemetry capture, oracle execution, or reconciliation. P0 may continue only after the same frozen packet is executed on a surface that can materialize the historical revision and provide the required authoritative provider telemetry and Harness v1 evidence.
