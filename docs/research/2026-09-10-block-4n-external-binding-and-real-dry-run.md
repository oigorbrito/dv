# Block 4N — External execution binding and real dry-run gate

Date: 2026-09-10
Status: COMPLETE / REAL_DRY_RUN_BLOCKED_BY_EXECUTION_SURFACE

## Purpose

Close the remaining pre-P0 operational bindings without widening `dv` into a runtime or workflow engine.

## 4N-A — real workspace binding

Materialized `tools/dv_workspace_materializer.py`.

It clones one declared repository, checks out the frozen SHA detached, rejects revision mismatch or a dirty fresh worktree, and emits workspace identity. It deliberately does not install dependencies or execute treatments.

Result: MATERIALIZED, NOT EXECUTED IN THIS GitHub-only session.

## 4N-B/C — concrete E0-E3 treatment freeze

Frozen in `experiments/p0/treatment-binding-v1.json` before any P0 outcome.

For the first P0 protocol version:
- E0 = GPT-5.6 Sol direct, high reasoning, then frozen verifier;
- E1 = GPT-5.6 Luna direct, medium reasoning, then frozen verifier;
- E2 = Luna first, with only predeclared objective escalation triggers to Sol; escalation receives frozen task state plus compact factual failure certificate, not hidden reasoning/transcript;
- E3 = static family policy fixed before outcomes: F1 Luna, F2 Sol, F3 Sol, F4 Sol, F5 Luna, F6 Luna.

These are experimental arms, not architecture or treatment approval.

Provider choice is intentionally single-family for this first pilot so model-tier cost/capability is varied while provider/API/tooling differences are held down. Cross-provider generalization is not claimed.

## 4N-D — telemetry binding

The treatment manifest requires provider/model identity, input/cached/output tokens, raw provider usage evidence, price snapshot, timestamps, and retention of retries/escalations under the parent run.

Pricing is a frozen snapshot and must not be silently recomputed using later prices. Subscription inclusion is not treated as zero economic cost.

No provider-native response was generated in this session; therefore no token or monetary measurement is claimed.

## 4N-E — F4 controlled replay

Materialized `tools/dv_f4_replay.py`.

The adapter executes the identical focal command against already-materialized base and candidate workspaces. A demonstrated base nonzero -> candidate zero transition yields the replay certificate. Base PASS does not prove proactive discovery and is INCONCLUSIVE. Timeout/launch ambiguity is INCONCLUSIVE.

Result: P4-BLK-005 is materially remediated at adapter level but not empirically executed.

## 4N-F — first real dry run

Attempt gate: BLOCKED.

This session can read/write GitHub repositories but does not expose an arbitrary shell/Codex/API execution surface with the user's provider credentials and native billing/usage record. A GitHub commit is not a treatment execution. Therefore claiming a real dry run would violate:

`DOCUMENTED != EXECUTED != MEASURED != ACCEPTED`

No synthetic substitute is accepted as a real P0 run.

## Blocker disposition

- P4-BLK-004 `TREATMENT_PROVIDER_BINDING_REQUIRED`: RESOLVED AT PROTOCOL LEVEL. Concrete model tiers/policy/escalation are frozen. Runtime credential/execution availability remains external.
- P4-BLK-005 `F4_CONTROLLED_BASELINE_REPLAY_REQUIRED`: RESOLVED AT ADAPTER LEVEL; execution evidence still absent.
- P4-BLK-006 `REAL_ISOLATED_WORKSPACE_BINDING_REQUIRED`: RESOLVED AT MATERIALIZER LEVEL; real checkout evidence still absent.
- P4-BLK-007 `AUTHORIZED_REAL_EXECUTION_SURFACE_REQUIRED`: OPEN / BLOCKING.

## Decision

`BLOCK_4N = COMPLETE`
`BLOCK_4N_OUTCOME = EXTERNAL_EXECUTION_BINDING_READY_BUT_UNEXECUTED`
`REAL_DRY_RUNS = 0`
`REAL_P0_RUNS = 0/24`
`P0_RELEASE = NO`
`BLOCK_5 = BLOCKED`
`HOLDOUT = SEALED`
`ARCHITECTURE_APPROVAL = NONE`

## Next block

`BLOCK 4X — REAL EXECUTION GATE`

This block must occur on an authorized execution surface that can:
1. run Git and the task toolchain;
2. invoke the frozen treatment model with real credentials/entitlement;
3. preserve provider-native usage telemetry;
4. persist the harness evidence bundle.

Sequence:
- materialize D-F1-01 at its frozen base;
- run one treatment-neutral/environment preflight;
- execute the first frozen P0 treatment according to the existing family order;
- reconcile raw evidence under Block 3;
- only on PASS release the remaining 23 P0 runs;
- execute all 24 without changing tasks/order/treatments;
- analyze actual variance/pathologies;
- then decide whether Block 5 can begin.

Do not add more generic harness functionality before a concrete execution defect demonstrates need.
