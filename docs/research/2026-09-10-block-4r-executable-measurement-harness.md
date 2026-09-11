# Block 4R — Executable measurement harness

Date: 2026-09-10
Status: MINIMAL HARNESS MATERIALIZED / RESEARCH ONLY
Architecture approval: NONE
Treatment approval: NONE

## Purpose

Materialize the smallest executable artifact required to unblock the Block 4 pilot measurement gate without creating a dv runtime, router, workflow engine, registry, memory system, provider-neutral IR, or treatment policy.

This artifact measures and reconciles one already-defined `treatment_run`. It does not decide what treatment to use.

## Empirical/reproducibility basis

The implementation is constrained by official/primary documentation rather than ad-hoc architecture preferences.

1. ACM/SIGSIM artifact-evaluation guidance requires research artifacts to be documented, consistent, complete to the extent possible, exercisable, and accompanied by verification/validation evidence. It also recommends automating computational results, testing from a blank environment, logging success and failure, and measuring resource use.
   - https://sigsim.acm.org/conf/pads/2026/blog/artifact-evaluation/

2. SWE-bench's official evaluation harness uses explicit run identifiers, isolated/reproducible execution environments, per-run logs, patch/test execution, grading, and result records. Its documented result-cache behavior also demonstrates why run identity must be explicit rather than inferred from task identity alone.
   - https://www.swebench.com/SWE-bench/guides/evaluation/
   - https://github.com/SWE-bench/SWE-bench/blob/main/docs/reference/harness.md

3. BenchExec documents a separation between benchmark orchestration and single-tool resource measurement (`runexec`), plus benchmarking guidance aimed at reliable measurements and containerized isolation. dv therefore keeps measurement plumbing separable from treatment logic instead of embedding a new orchestration architecture.
   - https://github.com/sosy-lab/benchexec/blob/main/doc/INDEX.md

4. OpenTelemetry's resource model treats telemetry as belonging to an explicitly identified observed entity and requires resource identity attributes to remain stable over the lifetime of the resource. dv uses the same semantic principle for run-bound telemetry without adopting OpenTelemetry as a mandatory dependency.
   - https://opentelemetry.io/docs/specs/otel/resource/
   - https://opentelemetry.io/docs/specs/otel/resource/data-model/

These sources support the engineering shape of the harness; they do not establish that dv's treatments are effective.

## Implemented artifact

`tools/dv_pilot_harness.py`

Properties:

- Python standard library only;
- one invocation executes one frozen treatment run plus one independent verifier command;
- globally unique `run_id` unless an explicit non-colliding ID is supplied;
- immutable input spec copied into the run directory;
- canonical SHA-256 digest of the run spec;
- UTC timestamps plus monotonic elapsed-time measurement;
- separate executor and verifier stdout/stderr logs;
- append-only harness event log (`events.jsonl`);
- child telemetry ingress through `DV_EVENT_LOG` and `DV_RUN_ID`;
- token categories constrained to the Block 3 partitions;
- monetary events require explicit currency;
- terminal verifier contract remains `YES | NO | INCONCLUSIVE`;
- a conclusive `YES` or `NO` requires `harness_valid=true`;
- a conclusive result requires non-empty evidence references during reconciliation;
- missing token or monetary telemetry remains `MISSING/UNRESOLVED`, never zero;
- duplicate event identifiers and malformed/misbound telemetry fail reconciliation;
- `reconcile` can recompute integrity checks from preserved raw artifacts.

## Deliberate non-features

The harness does not implement:

- routing;
- planning;
- task-family policy;
- E0/E1/E2/E3 semantics;
- provider/model selection;
- provider API clients;
- token estimation by guessed tokenizer;
- price tables;
- currency conversion;
- retries or escalation policy;
- Docker/container management;
- repository checkout/patch application;
- oracle-family logic;
- statistical aggregation;
- a database;
- OpenTelemetry export;
- BenchExec orchestration.

Those mechanisms belong in narrow adapters or existing external tools if/when required. Their absence is intentional to keep the 4R artifact measurement-only.

## Run-spec contract

One JSON object must contain at least:

```json
{
  "protocol_version": "4R-v1",
  "corpus_version": "v0",
  "task_id": "D-F1-01",
  "task_family": "F1",
  "base_revision": "<frozen-sha>",
  "oracle_version": "<frozen-oracle-id>",
  "treatment_id": "E0",
  "treatment_version": "<frozen-treatment-version>",
  "rollout_id": "r1",
  "environment_id": "<environment-identity>",
  "executor_command": ["<program>", "<arg>"],
  "verifier_command": ["<program>", "<arg>"]
}
```

Optional `working_directory` controls the working directory shared by executor and verifier.

The executor receives:

- `DV_RUN_ID`;
- `DV_EVENT_LOG`;
- `DV_RUN_DIR`;
- `DV_TASK_ID`;
- `DV_TREATMENT_ID`.

Provider/treatment adapters may append JSONL resource events to `DV_EVENT_LOG`. Each event must bind to the exact `run_id` and contain a unique `event_id`.

Example token/cost event:

```json
{"run_id":"...","event_id":"...","token_category":"execution","tokens":1234,"monetary_cost":0.01,"currency":"USD","source":"provider-usage"}
```

The verifier's final non-empty stdout line must be a JSON object, for example:

```json
{"outcome":"YES","harness_valid":true,"evidence_refs":["path/to/evidence"],"failure_attribution":null}
```

The executor process exit code is intentionally not equated with `VERIFIED_SOLVED_TASK`.

## Execution

From repository root:

```bash
python tools/dv_pilot_harness.py run --spec path/to/run-spec.json --out pilot-runs
```

Reconciliation can be repeated from preserved artifacts:

```bash
python tools/dv_pilot_harness.py reconcile pilot-runs/<run-id>
```

Tests:

```bash
python tools/test_dv_pilot_harness.py
```

## Validation performed before repository materialization

The exact harness logic was exercised with synthetic executor/verifier processes before commit.

Observed synthetic validation:

- unique run directory created;
- executor and verifier both executed;
- stdout/stderr preserved separately;
- one child resource event bound to the generated run ID;
- 123 synthetic tokens reconciled;
- USD 0.01 synthetic monetary cost reconciled;
- wall-clock duration measured;
- verifier `YES` with `harness_valid=true` and evidence reference accepted;
- reconciliation returned `PASS`.

The committed test suite additionally covers:

1. complete telemetry -> reconciliation PASS;
2. absent token/money telemetry -> values remain null/MISSING rather than zero;
3. conclusive outcome without evidence reference -> reconciliation FAIL.

Synthetic validation proves only harness mechanics. It is not a pilot treatment result.

## Remaining Block 4R gate

The former blocker `P4-BLK-001` is narrowed but not fully closed.

The repository now has an executable measurement envelope, but real P0 execution still requires narrow adapters/configuration that bind:

- the frozen six development tasks selected by Block 4C;
- the actual E0-E3 treatment commands;
- provider usage/billing telemetry where applicable;
- the already-frozen F1-F6 oracle commands/evidence;
- reproducible task environments.

These adapters must prefer existing execution/evaluation infrastructure (including benchmark-native harnesses where appropriate) and must not become a generic dv runtime.

## Decision

`BLOCK_4R_HARNESS = MATERIALIZED`

`HARNESS_MECHANICS = SYNTHETICALLY_EXECUTED`

`REAL_P0_RUNS = NOT_YET_EXECUTED`

`P4-BLK-001 = NARROWED_TO_REAL_ADAPTER/ENVIRONMENT_BINDING`

`ARCHITECTURE_APPROVAL = NONE`

The next defensible action is a real 4R dry run on one development task/treatment using its frozen oracle and real telemetry. Only if reconciliation passes should the 24-run P0 matrix begin.
