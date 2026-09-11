# Block 4M — P0 operational materialization

Date: 2026-09-10
Status: COMPLETE / OPERATIONAL MATERIALIZATION INCONCLUSIVE
Architecture approval: NONE
Treatment approval: NONE
Holdout status: SEALED

## Purpose

Convert the Block 4R measurement harness and the frozen Block 4 P0 design into the smallest operational artifacts needed for one real reconciled run, without inventing provider choices, changing the corpus/oracles, or building a dv runtime.

## 4M-A — Treatment operational binding

Candidate arms remain:
- E0 strongest-direct;
- E1 cheap/free-direct + verify;
- E2 cheap-first -> clean state-based escalation -> strong;
- E3 static policy by task family.

Result: NOT operationally bindable from repository evidence alone.

The repository does not freeze a trustworthy provider/model/CLI configuration establishing which available executor is 'strongest' or 'cheap/free' under the current environment, nor the exact E2 escalation certificate or E3 family map. Selecting those now by intuition would create post-hoc treatment definitions.

Therefore treatment semantics remain frozen, but concrete provider/model/command bindings remain blocked.

`P4-BLK-004 = TREATMENT_PROVIDER_BINDING_REQUIRED`

## 4M-B — Six P0 oracle command contracts

Materialized:
`experiments/p0/p0-operational-manifest.json`

Evidence was taken from the original project PRs corresponding to the six P0 tasks rather than from external gold patches.

Materialized focal/preservation commands:
- D-F1-01 / RJ PR #21: `ProcessTextNormalizerTests` plus RJ.DomainTests preservation;
- D-F2-01 / metaO PR #413: `tests.unit.test_mission_run_input_preflight` plus unit preservation;
- D-F3-01 / SMAG PR #118: `packages/smag-governance/test/operator-session.test.mjs`;
- D-F4-01 / metaO PR #297: candidate-side Rust fixture test command identified, but the frozen F4 oracle also requires a controlled Fail-to-Pass observation against the base state;
- D-F5-01 / metaO PR #401: `tests.unit.test_operator_ux_doctor` plus unit preservation;
- D-F6-01 / metaO PR #451: discovery persistence, external-target shadow, and locked workspace preservation commands.

F4 is intentionally not declared executable from candidate-only state.

`P4-BLK-005 = F4_CONTROLLED_BASELINE_REPLAY_REQUIRED`

## 4M-C — Environment/workspace binding

The operational manifest freezes repository, base SHA, and required toolchain class per P0 task.

Real execution still requires isolated task workspaces checked out at the exact frozen base revisions, with toolchains/dependencies available and environment identity captured by Harness v1.

The current GitHub-connected research session can inspect and write repository content but does not itself provide a bound local/container workspace for RJ/metaO/SMAG at all six historical base SHAs.

No environment is therefore falsely claimed as executed.

`P4-BLK-006 = REAL_ISOLATED_WORKSPACE_BINDING_REQUIRED`

## 4M-D — Minimal verifier adapter

Materialized:
`tools/dv_oracle_adapter.py`

The adapter:
- accepts only predeclared command arrays;
- runs them in the bound task workspace;
- preserves stdout/stderr per check;
- hashes material verifier outputs;
- supports timeout;
- emits the existing `YES | NO | INCONCLUSIVE` contract;
- maps valid mandatory check failures to PRODUCT_FAILURE/NO;
- maps blocked/invalid oracle materialization and timeout to INCONCLUSIVE rather than inferred failure.

It does not perform routing, provider selection, task execution, repository checkout, state switching, or statistical analysis.

## 4M-E — First real dry-run attempt

Entry conditions checked:
1. Harness v1 exists and its synthetic/mechanical tests pass.
2. Run-spec template exists.
3. Five P0 task oracle command contracts can be made executable after workspace binding.
4. F4 requires an additional controlled base-state replay mechanism.
5. No E0-E3 concrete provider/model command binding is frozen.
6. No real isolated task workspace is available inside this session for an actual treatment run.

Decision: real dry run NOT EXECUTED.

This is not a treatment failure and not evidence about E0-E3 effectiveness.

`REAL_DRY_RUNS = 0`

## 4M-F — Release decision

P0 is not released.

Reason: executing a treatment before concrete treatment identity, workspace identity, and oracle state mechanics are frozen would violate the already-frozen experimental contract.

Outcome:

`BLOCK_4M = COMPLETE`

`BLOCK_4M_OUTCOME = OPERATIONAL_MATERIALIZATION_INCONCLUSIVE`

`P0_RELEASE = NO`

`BLOCK_5 = BLOCKED`

`ARCHITECTURE_APPROVAL = NONE`

## What Block 4M established

The remaining gap is now narrower than at the end of 4R.

The experiment no longer lacks a general measurement harness or a generic verifier command adapter. It lacks external execution bindings:
- real isolated workspaces at frozen revisions;
- concrete executor/provider/model identities for E0-E3;
- provider telemetry adapters for those concrete bindings;
- controlled dual-state replay for the F4 Fail-to-Pass requirement.

These are operational dependencies, not evidence for a new dv architecture.

## Next block

`BLOCK 4N — EXTERNAL EXECUTION BINDING AND REAL DRY RUN`

4N must remain narrow:
1. bind one real development workspace first;
2. freeze the exact strong and cheap/free executor identities from observable availability/cost evidence;
3. freeze E2 escalation certificate and E3 static family map before treatment outcomes;
4. bind provider-native usage/billing telemetry;
5. implement/reuse the minimum controlled base/candidate replay needed for F4;
6. execute one real run and require Harness v1 reconciliation PASS before releasing the 24-run P0.

Do not open the holdout and do not begin Block 5 until this gate passes.
