# Block 4Y — Execution-surface handoff / first real run

Date: 2026-09-10
Status: COMPLETE / EXECUTABLE HANDOFF FROZEN / REAL RUN NOT EXECUTED
Architecture approval: NONE
Treatment approval: NONE
Holdout: SEALED

## Purpose

Convert the already-frozen Block 4X execution gate into an exact, transferable first-run packet without adding another generic dv runtime, provider abstraction, workflow engine, or measurement subsystem.

Block 4Y is complete when an execution-capable environment can pick up one immutable packet and either produce the first real reconciled run or preserve a concrete pre-execution blocker. Block 4Y itself does not claim a real treatment result unless that execution actually occurs.

## Frozen first run

The first admissible P0 run remains:

- task: `D-F1-01`
- family: `F1`
- repository: `oigorbrito/RJ`
- frozen base: `c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d`
- treatment: `E0`
- E0 model: `gpt-5.6-sol`
- E0 reasoning effort: `high`
- escalation: none
- verifier authority: frozen F1 oracle plus Block 4M executable oracle adapter
- rollout: `r1`

Do not substitute a different model, task, base revision, treatment, or oracle under the same run identity.

## Authoritative artifacts

Execution must use the existing artifacts as authorities rather than recreating their logic:

- `experiments/p0/p0-operational-manifest.json`
- `experiments/p0/treatment-binding-v1.json`
- `experiments/p0/run-spec.template.json`
- `tools/dv_workspace_materializer.py`
- `tools/dv_pilot_harness.py`
- `tools/dv_oracle_adapter.py`
- `tools/dv_f4_replay.py` (not used by the first F1 run, retained for later F4 P0 execution)

## Required execution-surface capabilities

One environment must simultaneously provide:

1. Git/network access sufficient to materialize the historical repository revision.
2. `python` and the task toolchain (`dotnet` for D-F1-01).
3. An authorized invocation path for the frozen E0 model.
4. Provider-native or otherwise prevalidated authoritative usage telemetry for input, cached-input where reported, output tokens, and model identity.
5. Monetary accounting using the frozen price snapshot unless an authoritative provider charge is captured directly; any pricing drift must be preserved as provenance rather than silently replacing the frozen snapshot.
6. Ability to let the executor modify only the isolated candidate workspace.
7. Ability to invoke the frozen verifier after candidate execution.
8. Ability to retain the Harness v1 run directory without post-run mutation of raw evidence.

## Required preflight

Before invoking E0, record and validate:

```text
repository == oigorbrito/RJ
HEAD == c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d
worktree == clean
dotnet == available
python == available
treatment == E0
model == gpt-5.6-sol
reasoning_effort == high
provider telemetry == available
holdout access == absent/not used
```

Any mismatch is a pre-execution blocker and must not be converted into a treatment failure.

## Canonical workspace materialization

From the dv repository root in an execution-capable environment:

```text
python tools/dv_workspace_materializer.py \
  --repository oigorbrito/RJ \
  --revision c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d \
  --destination <isolated-workspace>/D-F1-01 \
  --identity-out <evidence>/D-F1-01-workspace.json
```

The materializer must reject revision drift or an unexpectedly dirty fresh checkout.

## Executor boundary

The E0 executor must receive only the development-task information admissible under the frozen corpus/protocol. It must not receive:

- PR solution diff/head as a solution aid;
- holdout instances or outcomes;
- gold patch;
- verifier-owned hidden evidence beyond what the task contract permits;
- results from E1/E2/E3 on the same task.

The executor adapter must append resource events to `DV_EVENT_LOG` bound to the exact `DV_RUN_ID`.

At minimum, each provider-backed usage event must preserve:

- `run_id`;
- unique `event_id`;
- Block 3 token category;
- provider identity;
- model identity;
- input tokens;
- cached input tokens when reported;
- output tokens;
- authoritative usage source/reference;
- monetary cost and currency when directly supplied, or enough raw usage to recompute under the frozen pricing snapshot;
- cache/reuse provenance.

Missing provider usage is `MISSING/UNRESOLVED`, never zero.

## F1 verifier binding

After E0 terminates, invoke the Block 4M oracle adapter against the candidate workspace with the D-F1-01 mandatory checks from the P0 manifest:

1. focused defect-target/preservation evidence:

```text
dotnet test RJ.DomainTests/RJ.DomainTests.csproj --filter FullyQualifiedName~ProcessTextNormalizerTests
```

2. local preservation suite:

```text
dotnet test RJ.DomainTests/RJ.DomainTests.csproj
```

The oracle adapter must preserve raw stdout/stderr and hashes and emit only `YES`, `NO`, or `INCONCLUSIVE` under the frozen Block 2 semantics.

Executor exit code alone is not the outcome.

## Harness invocation contract

Create a concrete run spec from `experiments/p0/run-spec.template.json` with:

- the exact frozen identities above;
- `working_directory` set to the isolated D-F1-01 workspace;
- executor command set to the authorized E0 adapter/CLI invocation;
- verifier command set to the frozen F1 oracle-adapter invocation;
- timeout values fixed before execution;
- environment identity captured before candidate modification.

Then execute:

```text
python tools/dv_pilot_harness.py run --spec <first-real-run-spec.json> --out <pilot-runs>
```

Recompute independently from preserved artifacts:

```text
python tools/dv_pilot_harness.py reconcile <pilot-runs>/<run-id>
```

## Acceptance gate for the first real run

The run is admissible as a real dry run only when all are true:

- historical workspace identity is proven;
- E0 actually executed;
- provider/model identity is proven;
- token telemetry is complete enough for the Block 3 primary token metric;
- monetary accounting is complete enough for the Block 3 monetary metric;
- verifier executed against the produced candidate state;
- terminal outcome is valid under Block 2;
- raw evidence hashes/references are present;
- reconciliation status is `PASS`;
- no solution leakage or holdout exposure occurred.

A verifier outcome of `YES` is not sufficient if accounting/reconciliation fails.

## P0 release rule

Only after one real D-F1-01/E0 run passes the measurement/integrity gate may P0 continue in the already-frozen order.

This first run is a measurement-readiness gate, not evidence that E0 is superior.

If the first run is `NO` but the harness/accounting is valid, that can still demonstrate measurement readiness. If it is `INCONCLUSIVE` because of harness/environment/telemetry failure, P0 remains blocked until the cause is prospectively corrected.

## Current-session execution result

The current session cannot satisfy the execution-surface requirements established in Block 4X:

- its shell cannot reach GitHub to clone the historical workspace;
- it has no authorized external E0 invocation surface exposing provider-native usage/billing telemetry.

Therefore:

`REAL_RUN_EXECUTED_IN_BLOCK_4Y = NO`

This is not a treatment result.

## Block decision

`BLOCK_4Y = COMPLETE`

`BLOCK_4Y_OUTCOME = EXECUTABLE_HANDOFF_FROZEN_REAL_RUN_PENDING_EXTERNAL_SURFACE`

`P4-BLK-007 = OPEN`

`REAL_DRY_RUNS = 0`

`REAL_P0_RUNS = 0/24`

`P0_RELEASE = NO`

`BLOCK_5 = BLOCKED`

`HOLDOUT = SEALED`

`ARCHITECTURE_APPROVAL = NONE`

## Falsification boundary

No additional generic dv component is justified by Block 4Y. The next increase in evidence must come from executing this frozen packet on a capable surface, not from writing more orchestration code.
