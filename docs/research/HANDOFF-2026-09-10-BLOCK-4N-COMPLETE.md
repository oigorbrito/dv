# HANDOFF — dv after Block 4N completion

Date: 2026-09-10
Repository: `oigorbrito/dv`

## Canonical state

`BLOCK_1 = COMPLETE`
`BLOCK_2 = COMPLETE`
`BLOCK_3 = COMPLETE`
`BLOCK_4 = COMPLETE / PILOT_INCONCLUSIVE`
`BLOCK_4R = COMPLETE`
`BLOCK_4M = COMPLETE / OPERATIONAL_MATERIALIZATION_INCONCLUSIVE`
`BLOCK_4N = COMPLETE / EXTERNAL_EXECUTION_BINDING_READY_BUT_UNEXECUTED`
`BLOCK_5 = BLOCKED`

`REAL_DRY_RUNS = 0`
`REAL_P0_RUNS = 0/24`
`P0_RELEASE = NO`
`HOLDOUT = SEALED`
`ARCHITECTURE_APPROVAL = NONE`
`TREATMENT_APPROVAL = NONE`

## New Block 4N artifacts

- `experiments/p0/treatment-binding-v1.json` — freezes concrete E0-E3 model tiers, E2 escalation certificate, E3 family policy, pricing snapshot, and telemetry requirements before outcomes.
- `tools/dv_workspace_materializer.py` — narrow isolated frozen-SHA Git workspace materializer.
- `tools/dv_f4_replay.py` — controlled base/candidate Fail-to-Pass replay adapter.
- `docs/research/2026-09-10-block-4n-external-binding-and-real-dry-run.md` — block closeout.

## Blocker status

P4-BLK-004: resolved at protocol level; runtime execution/credential availability remains external.
P4-BLK-005: resolved at adapter level; no real replay evidence yet.
P4-BLK-006: resolved at materializer level; no real checkout evidence yet.
P4-BLK-007: OPEN — authorized real execution surface with provider-native telemetry required.

## Exact continuation

NEXT = `BLOCK 4X — REAL EXECUTION GATE`

Do not design more generic harness infrastructure. Use an execution-capable environment to materialize D-F1-01, run environment preflight, execute the first frozen treatment in the existing P0 order, preserve native telemetry, reconcile under Block 3, and only then release the rest of the 24-run P0.

If the execution surface cannot provide real provider usage/cost evidence, classify the run INCONCLUSIVE rather than zero-cost or PASS.

Block 5 starts only after real P0 execution and reconciliation produce enough operational evidence to freeze a defensible confirmatory protocol.
