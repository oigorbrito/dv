# Block 3E — Measurement envelope reconciliation and freeze

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE
Implementation approval: NONE

## Purpose

This document reconciles Blocks 3A–3D into one canonical measurement specification suitable for Block 4 pilot instrumentation.

It does not approve an architecture, select a winning treatment, claim statistical sufficiency, or authorize confirmatory conclusions.

## Block 3 canonical objective

Measure the complete treatment cost of obtaining a terminal verified task outcome, preserving separate token, monetary, and latency dimensions and preventing favorable omission of treatment-caused work.

The primary experimental economic question is not:

`Which executor is cheapest?`

It is:

`Which treatment achieves verified solved tasks at the lowest complete system resource cost under the frozen verification contract?`

## Canonical accounting unit

Primary unit:

`TREATMENT_RUN`

One treatment run is one frozen treatment applied to one frozen task instance for one rollout until exactly one terminal Block 2 outcome is produced:

`YES | NO | INCONCLUSIVE`

All treatment-caused work remains inside that run, including routing, planning, context work, execution, verification, retries, replanning, handoffs, escalation, and failed internal attempts.

Internal attempts are subordinate events. They are not separately selectable successes.

Repeated rollouts are distinct treatment runs and must remain distinct observations.

## Canonical success denominator

`verified_solved_count = count(treatment_run where terminal outcome == YES)`

`NO` and `INCONCLUSIVE` contribute zero verified solved tasks while retaining all incurred resource usage in treatment totals.

This is required to avoid survivorship accounting.

## Primary token metric

For each treatment:

`TOTAL_SYSTEM_TOKENS = sum(all attributable token usage across every assigned run)`

Primary token effectiveness metric:

`TOKEN_COST_PER_VERIFIED_SOLVED_TASK = TOTAL_SYSTEM_TOKENS / verified_solved_count`

Mandatory minimum token partitions:
- routing/classification;
- planning/task shaping;
- context construction/reconstruction;
- execution;
- handoff/escalation;
- verification/judging;
- retry/replanning.

Provider-exposed input/output/cached/reasoning or other billable token classes must be retained where available.

Executor-only token accounting is insufficient.

## Primary monetary metric

For each treatment:

`TOTAL_MONETARY_COST = sum(all non-duplicated attributable monetary events across every assigned run)`

Primary monetary effectiveness metric:

`MONETARY_COST_PER_VERIFIED_SOLVED_TASK = TOTAL_MONETARY_COST / verified_solved_count`

At minimum, monetary accounting must be capable of representing model/API charges, paid external services, material runtime compute, verification cost as a tagged subset where separable, and material coordination/infrastructure cost.

Observed zero price does not imply zero token use, zero latency, or zero resource consumption.

## Primary latency measure

Canonical per-run latency:

`WALL_CLOCK_LATENCY = terminal_run_time - treatment_run_start_time`

Component diagnostics should distinguish model-call, tool/runtime, verification, and coordination overhead where measurable.

Component durations may overlap and are not required to sum to wall clock.

Parallelism may reduce wall-clock latency while increasing token/monetary consumption; both dimensions must remain visible.

## Metric dimensionality

The experiment preserves at least three independent dimensions:

1. tokens;
2. monetary cost;
3. wall-clock latency.

No primary dimension is silently converted into another.

Therefore:

`TOKEN EFFICIENCY != MONETARY EFFICIENCY != LATENCY EFFICIENCY`

A later protocol may define multi-objective decision rules or non-inferiority margins, but Block 3 does not invent weights or collapse these measures into an arbitrary composite score.

## Zero-success rule

If a treatment produces `verified_solved_count = 0`, its token-cost-per-verified-solved-task and monetary-cost-per-verified-solved-task cannot be reported as zero or omitted.

They are treated as undefined/infinite for comparative effectiveness purposes, with raw totals still reported.

Exact statistical representation belongs to the later frozen analysis protocol.

## Accounting-integrity rules

The following are mandatory for pilot measurement:

- failed and inconclusive runs retain incurred resources;
- retries/replans/escalations accumulate rather than replace earlier consumption;
- timeouts retain incurred cost and elapsed time;
- parallel calls accumulate resource use while wall-clock remains elapsed time;
- missing telemetry is never defaulted to zero;
- telemetry conflicts are preserved and reconciled by treatment-independent rules;
- cache/reuse provenance must be visible;
- treatment-specific setup cannot be disguised as experiment-global setup;
- dynamic run-specific work belongs to the run even if potentially reusable;
- warm/cold state differences must be controlled or explicitly measured;
- free tiers, credits, subscriptions, and quota effects must be tagged rather than erased;
- provider/model/price drift must remain observable;
- manual intervention must be logged and cannot silently create native treatment success;
- resource categories cannot be double-counted;
- raw evidence must support recomputation of normalized aggregates.

## Setup and reuse classification

Resource-bearing work must be assigned to one of these scopes:

1. `experiment_global_setup`
   - treatment-neutral, frozen before results, identically available to all treatments;

2. `treatment_specific_setup`
   - required because of one treatment and reusable across its runs;

3. `run_specific_work`
   - caused by a particular task/run;

4. `cross_run_reuse_event`
   - later use of a prior artifact with provenance preserved.

Block 4 may measure both marginal and amortized views where useful, but the chosen comparison basis must be predeclared before treatment results are interpreted.

## Missing-data rule for pilot readiness

Primary accounting requires sufficient telemetry to reconstruct the metric boundary defensibly.

Evidence precedence for resource telemetry:

1. trustworthy provider billing/usage evidence;
2. trustworthy runtime/client telemetry covering the same event;
3. predeclared deterministic reconstruction validated before comparison;
4. otherwise `MISSING/UNRESOLVED`.

If unresolved missingness prevents a primary metric from being computed defensibly, that comparison is not repaired with a favorable estimate. It remains measurement-incomplete and may be `INCONCLUSIVE` for the affected metric.

## Minimum canonical pilot record

Exact storage technology/schema remains unapproved, but every pilot run must be representable with at least the following semantic fields:

### Identity
- protocol version;
- corpus version;
- task ID;
- task family;
- immutable base revision/state;
- oracle version;
- treatment ID;
- treatment configuration/version;
- rollout ID;
- globally unique treatment run ID;
- environment/harness identity.

### Lineage
- ordered event/attempt IDs;
- parent/trigger relation for retry, replan, handoff, or escalation;
- provider/model/service identity per resource event where applicable;
- candidate output/state identity;
- manual intervention markers.

### Verification
- terminal `YES | NO | INCONCLUSIVE`;
- verifier/oracle evidence references;
- harness-validity evidence;
- protocol-deviation markers.

### Tokens
- functional token category;
- provider-reported token classes where available;
- normalized total token usage;
- raw telemetry reference.

### Monetary
- original usage/charge data;
- provider/service;
- price schedule/version or billing evidence;
- original currency;
- normalized reporting currency where conversion is required;
- non-duplicated total run cost.

### Latency
- run start;
- run end;
- wall-clock duration;
- model/tool/verification/coordination component timing where measurable;
- timeout/cancellation markers.

### Reuse/setup
- cache type/status;
- artifact provenance;
- setup-scope classification;
- reuse event identity.

### Integrity
- missing telemetry markers;
- conflicting telemetry markers;
- accounting reconciliation status;
- raw evidence/log locations.

## Required pre-pilot reconciliation checks

Before a pilot run is accepted into comparative summaries, measurement instrumentation must be able to check:

1. one run -> one task, treatment, rollout, terminal outcome;
2. no orphan resource-bearing events;
3. every retry/escalation linked to its parent run;
4. no reset of accumulated cost after retry/escalation;
5. no duplicate charging of the same event;
6. failed/inconclusive resources preserved;
7. token partition reconstructs total token usage to the extent telemetry permits;
8. monetary computation binds usage to an explicit price/billing source;
9. wall-clock timestamps are coherent;
10. cache/setup/reuse provenance is explicit where material;
11. missing/conflicting telemetry is visible rather than silently imputed;
12. raw evidence is sufficient to reproduce normalized aggregates.

Failure of reconciliation does not imply zero cost or task failure. It means the measurement is not yet defensible for the affected primary comparison.

## What Block 3 intentionally does not decide

Block 3 does not freeze:
- number of pilot rollouts;
- confirmatory sample size;
- randomization/order/counterbalancing;
- task-treatment assignment policy;
- statistical estimator or confidence interval method;
- significance threshold;
- equivalence/non-inferiority margin;
- acceptable latency tradeoff;
- composite utility weights;
- winner/approval threshold;
- architecture choice;
- learned router;
- custom runtime/registry/workflow engine;
- custom provider-neutral IR.

Those decisions must occur only in their proper later blocks and, where result-sensitive, before sealed holdout results are observed.

## Pilot entry gate

Block 4 may begin only if the pilot instrumentation can produce the canonical measurement record and pass the reconciliation checks above on representative dry runs or instrumentation checks.

This gate tests measurement viability, not treatment superiority.

A valid Block 4 result remains that the instrumentation or comparison is insufficient and requires a documented protocol revision before confirmatory work.

## Block 3 conclusion

The measurement envelope is now frozen around complete treatment-run economics rather than executor-local cost.

The central empirical objective remains:

`minimize complete system resources per VERIFIED_SOLVED_TASK`

subject to preserving independent correctness, monetary, token, and latency evidence rather than optimizing one proxy in isolation.

No architecture or component has been approved by completing this block.

## Status

`BLOCK_1 = COMPLETE`
`BLOCK_2 = COMPLETE`
`BLOCK_3A = COMPLETE`
`BLOCK_3B = COMPLETE`
`BLOCK_3C = COMPLETE`
`BLOCK_3D = COMPLETE`
`BLOCK_3E = COMPLETE`
`BLOCK_3 = COMPLETE`
`BLOCK_4 = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
`IMPLEMENTATION_APPROVAL = NONE`

Next:

`BLOCK_4 — PILOT`

The pilot must evaluate measurement/instrumentation behavior and empirical variance before the confirmatory protocol is frozen. It must not consume the sealed holdout as an exploratory tuning set.
