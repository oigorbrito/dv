# Block 4R — Executable measurement harness and pilot re-entry gate

Date: 2026-09-10
Status: COMPLETE / HARNESS READY / REAL P0 BLOCKED BEFORE EXECUTION
Architecture approval: NONE
Treatment approval: NONE

## Purpose

Materialize and validate the smallest executable measurement artifact required by Blocks 3 and 4 without creating a dv runtime, router, workflow engine, registry, memory system, provider-neutral IR, provider selector, or retry engine.

The harness measures one already-defined `treatment_run`; it does not define the treatment or the task oracle.

## Empirical/reproducibility basis

The implementation remains constrained by primary/official guidance already recorded in this block:

- ACM/SIGSIM artifact-evaluation guidance: exercisable artifacts, automation, logs, validation evidence and reproducibility;
- SWE-bench evaluation harness: explicit run identity, isolated/reproducible environments, per-run logs and independent grading;
- BenchExec: separation between experimental orchestration and resource measurement;
- OpenTelemetry resource semantics: stable identity for the entity to which telemetry belongs.

These sources justify the measurement shape only. They do not establish treatment effectiveness.

## Implemented artifact

`tools/dv_pilot_harness.py`

The harness remains Python-stdlib-only and executes exactly one treatment command and one verifier command per invocation.

### Core properties

- globally unique `run_id` unless a non-colliding explicit ID is supplied;
- immutable input spec copied into the run directory;
- canonical SHA-256 of the input spec;
- required explicit `working_directory`;
- UTC timestamps and monotonic elapsed time;
- separate executor/verifier stdout and stderr;
- append-only harness event log;
- child resource events bound to `DV_RUN_ID`;
- terminal verifier contract `YES | NO | INCONCLUSIVE`;
- conclusive YES/NO requires `harness_valid=true` and evidence references;
- missing telemetry remains missing, never zero;
- duplicate/misbound/malformed telemetry fails reconciliation;
- reconciliation is recomputable from raw artifacts.

## 4R hardening completed

The transversal gaps found after the first harness materialization are now closed.

### H1 — environment snapshot

The harness records:

- declared environment ID;
- Python/runtime identity;
- platform/machine;
- Git worktree root when available;
- Git HEAD when available;
- dirty-state signal and digest;
- optional toolchain versions supplied by the run spec;
- optional container image digest supplied by the run spec.

A full 40-character declared `base_revision` that disagrees with the observed Git HEAD causes reconciliation failure.

`working_directory` is mandatory. This was strengthened after validation showed that an inherited caller directory makes environment attribution ambiguous and can make repository inspection unexpectedly expensive.

### H2 — timeout/cancellation evidence

Executor and verifier support separately declared positive timeout values.

A timeout preserves:

- elapsed duration;
- termination reason;
- process result;
- already-written stdout/stderr;
- already-emitted resource telemetry.

Verifier timeout produces `INCONCLUSIVE / HARNESS_FAILURE` rather than an inferred product failure.

Executor timeout is recorded but does not itself force `PRODUCT_FAILURE`; the independent verifier remains responsible for task outcome semantics.

### H3 — material artifact integrity

The run summary records SHA-256 plus byte length for the material non-recursive artifacts:

- `spec.json`;
- `events.jsonl`;
- `child-events.jsonl`;
- executor stdout/stderr;
- verifier stdout/stderr.

`run.json` is intentionally not hashed inside its own manifest to avoid recursive self-hashing.

### H4 — resource provenance

Resource telemetry now requires explicit provenance.

Token events require at minimum:

- `run_id`;
- unique `event_id`;
- valid token category;
- non-negative integer tokens;
- `source`;
- `provider`;
- `model_or_service`.

Monetary events additionally require:

- non-negative monetary cost;
- currency;
- `billing_ref` or `price_schedule_ref`.

Optional cache state is restricted to:

`hit | miss | partial | not_applicable | unknown`

Multiple currencies cannot be silently summed without predeclared normalization.

## Test evidence

`tools/test_dv_pilot_harness.py`

The hardened harness was executed against six synthetic/integrity tests and all passed:

1. complete resource telemetry reconciles and material artifacts are hashed;
2. missing token/money telemetry remains null/MISSING rather than zero;
3. conclusive verifier outcome without evidence fails reconciliation;
4. resource telemetry without provenance fails reconciliation;
5. verifier timeout becomes `INCONCLUSIVE / HARNESS_FAILURE`;
6. executor timeout is retained without automatically becoming product failure.

Observed validation result:

`6/6 PASS`

This is evidence of harness mechanics and integrity behavior only.

`HARNESS_PASS != TREATMENT_PASS`

## Deliberate non-features remain unchanged

The harness still does not implement:

- routing or planning;
- E0/E1/E2/E3 semantics;
- model/provider selection;
- provider API clients;
- guessed token estimation;
- price tables or currency conversion;
- retry/escalation policy;
- Docker/container management;
- checkout/patch application;
- family-oracle implementation;
- statistical aggregation;
- database/storage service;
- OpenTelemetry export;
- BenchExec orchestration.

These remain outside the measurement kernel unless empirical execution demonstrates a need.

## Real P0 re-entry attempt

Block 4C froze P0 as 24 runs:

- one first development task from each family F1–F6;
- all E0–E3 candidate treatments;
- one rollout each;
- deterministic rotated treatment ordering.

A real dry-run was evaluated for admissibility before execution.

It is not yet admissible for two independent reasons.

### P4-BLK-002 — treatment operationalization missing

E0–E3 are frozen only as conceptual arms:

- E0 strongest-direct;
- E1 cheap/free-direct + verify;
- E2 cheap-first -> state-based escalation -> strong;
- E3 static task-family policy.

No concrete provider/model/executor command, configuration version, context policy, escalation boundary, or provider telemetry adapter is yet frozen for these arms.

Selecting those values during execution would create the treatment after the pilot design and make the run non-reproducible as an observation of a frozen treatment.

### P4-BLK-003 — per-instance oracle materialization missing

Block 2 froze family-level oracle semantics but not executable per-instance commands.

For example, the canonical F1 oracle explicitly records:

`exact per-instance commands/tests: DEFERRED to later oracle materialization`

and:

`verifier implementation: NONE`

Therefore the harness cannot yet bind a real candidate state to an already-materialized independent verifier without inventing evaluation commands after the fact.

## Decision

The measurement harness itself has reached the defensible first-version boundary.

`BLOCK_4R = COMPLETE`

`HARNESS_V1 = READY`

`HARNESS_TESTS = 6/6 PASS`

`REAL_P0_RUNS = 0/24`

`P4-BLK-001 = CLOSED (measurement harness materialized)`

`P4-BLK-002 = OPEN (treatment operationalization)`

`P4-BLK-003 = OPEN (per-instance oracle materialization)`

`P0_REENTRY = BLOCKED BEFORE EXECUTION`

`ARCHITECTURE_APPROVAL = NONE`

No P0 treatment outcome has been observed, so no treatment ranking or policy conclusion exists.

## Next defensible block

Before P0 can execute, a separate pre-outcome materialization block must freeze only the missing operational bindings:

1. concrete E0–E3 treatment configurations and narrow telemetry adapters;
2. executable verifier/oracle commands for the six P0 development instances;
3. reproducible workspace/environment recipes bound to the already-frozen base revisions;
4. one real dry-run admission check through Harness v1.

This next block must prefer existing provider/benchmark/project-native mechanisms and must not expand into a generic dv runtime.
