# HANDOFF — dv after Block 4M completion

Date: 2026-09-10
Repository: `oigorbrito/dv`

## Current state

`BLOCK_1 = COMPLETE`
`BLOCK_2 = COMPLETE`
`BLOCK_3 = COMPLETE`
`BLOCK_4 = COMPLETE / PILOT_INCONCLUSIVE`
`BLOCK_4R = COMPLETE`
`BLOCK_4M = COMPLETE / OPERATIONAL_MATERIALIZATION_INCONCLUSIVE`
`BLOCK_5 = BLOCKED`

`ARCHITECTURE_APPROVAL = NONE`
`TREATMENT_APPROVAL = NONE`
`HOLDOUT = SEALED`

## Block 4M artifacts

### Narrow executable oracle adapter
`tools/dv_oracle_adapter.py`

Commit introducing it:
`abc54da1eb1f871a9582d7cd7c0c48dc3ec871bc`

### Canonical P0 operational manifest
`experiments/p0/p0-operational-manifest.json`

Commit:
`26a304ecd43f1c000ba6951d41b33bbff01a599b`

Contains the six P0 development task identities, frozen base revisions, toolchain classes, and the focal/preservation commands recoverable from the original project PR evidence.

### Canonical run-spec template
`experiments/p0/run-spec.template.json`

Commit:
`e628fde502aada00a69da1e558649b45d7ad34ef`

### Block closeout
`docs/research/2026-09-10-block-4m-p0-operational-materialization.md`

Commit:
`30081aef48cecf40849b50fe0bbf353f3b076ad4`

## What is now materially available

- Harness v1 for one treatment run;
- independent verifier-command adapter;
- explicit P0 run-spec shape;
- P0 task repository/base/toolchain identities;
- executable focal/preservation command contracts for D-F1-01, D-F2-01, D-F3-01, D-F5-01, and D-F6-01 after real workspace binding;
- candidate-side focal command for D-F4-01, with its required controlled base-state Fail-to-Pass replay explicitly still unresolved.

## Remaining blockers

`P4-BLK-004 = TREATMENT_PROVIDER_BINDING_REQUIRED`

E0-E3 have conceptual semantics but no frozen concrete provider/model/CLI/configuration binding that establishes current strongest vs cheap/free execution from observable evidence.

`P4-BLK-005 = F4_CONTROLLED_BASELINE_REPLAY_REQUIRED`

The frozen F4 oracle requires controlled Fail-to-Pass evidence against the base state. Candidate-only test execution is insufficient.

`P4-BLK-006 = REAL_ISOLATED_WORKSPACE_BINDING_REQUIRED`

A real dry run requires an isolated checkout at the frozen historical base revision with its runtime/dependencies available and environment identity captured.

Provider-native usage/billing telemetry must be bound when the concrete treatment provider is selected.

## Real execution status

`REAL_DRY_RUNS = 0`
`REAL_P0_RUNS = 0/24`
`P0_RELEASE = NO`

No treatment result is inferred from this absence of execution.

## Exact continuation point

NEXT:

`BLOCK 4N — EXTERNAL EXECUTION BINDING AND REAL DRY RUN`

Recommended sequence:
- 4N-A: bind one real development workspace at its frozen SHA;
- 4N-B: establish and freeze concrete current E0/E1 executor identities from observable capability/cost evidence;
- 4N-C: freeze E2 escalation certificate and E3 static family policy before outcomes;
- 4N-D: bind provider-native token/cost telemetry;
- 4N-E: reuse or minimally implement controlled F4 base/candidate replay;
- 4N-F: execute one real dry run, reconcile it, and release P0 only on PASS.

Do not reopen Blocks 1-4M unless a concrete defect is discovered. Do not open the holdout. Do not begin Block 5 before a real reconciled P0 measurement gate passes.
