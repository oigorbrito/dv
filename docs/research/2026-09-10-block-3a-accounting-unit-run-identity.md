# Block 3A — Unit of accounting and run identity

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE
Implementation approval: NONE

## Scope

This sub-block freezes the semantic unit of accounting for `dv` experiments and the minimum identity/lineage required to attribute every measured resource to the treatment that caused it.

It defines one experimental treatment run, one internal attempt, retry/replan/escalation lineage, repeated rollouts, terminal outcome, and what counts as one verified solved task for later economic denominators.

It does not yet freeze token fields, prices, latency fields, cache charging, infrastructure allocation, missing-telemetry policy, statistical estimators, sample size, or treatment ranking.

## Governing principle

The accounting boundary is the complete treatment invocation required to obtain a terminal verified outcome for one frozen task instance.

`ONE MODEL CALL != ONE RUN`

`ONE EXECUTOR INVOCATION != ONE RUN`

`ONE ATTEMPT != NECESSARILY ONE RUN`

`RETRY / ESCALATION COST BELONGS TO THE RUN THAT CAUSED IT`

A treatment cannot appear cheaper by counting only its successful final executor call while excluding planning, failed attempts, retries, escalation, verification, or other treatment-required work.

## Canonical entities

### Task instance

A `task_instance` is one frozen corpus item evaluated from its declared base state under its declared oracle.

Minimum identity:
- `corpus_version`;
- `task_id`;
- `task_family`;
- immutable base-state/revision identity;
- `oracle_version`.

### Treatment

A `treatment` is one predeclared experimental strategy applied to a task.

Minimum identity:
- `protocol_version`;
- `treatment_id`;
- immutable treatment configuration/version reference.

Any behaviorally material change requires a new treatment version. Silent mutation under the same identifier is forbidden.

### Treatment run

A `treatment_run` is the primary accounting unit.

One run begins when a frozen treatment is invoked on one frozen task instance for one specified rollout and ends only when that treatment reaches one terminal recorded verification outcome.

A run includes all treatment-caused work inside that boundary, including where applicable classification/routing, planning/task shaping, context construction/reconstruction, execution, treatment-attributable tools/runtime, verification, retries, replanning, handoffs, escalation, failed internal attempts, and terminal failure handling.

A run must never be split into multiple cheaper-looking observations merely because it used multiple executors, models, phases, or retries.

### Attempt

An `attempt` is a distinct treatment-controlled effort inside a treatment run that may produce a candidate state or evidence and may lead to retry, replan, escalation, verification, or termination.

Every attempt belongs to exactly one `treatment_run_id`. Attempts are subordinate accounting events, not independent task successes.

An attempt may end without a candidate patch/state. Its incurred resources remain attributable to the parent run.

## Retry, replan, and escalation

A `retry` repeats materially the same intended treatment step after an unsuccessful, invalid, interrupted, or otherwise nonterminal attempt. It receives a new `attempt_id`, stays inside the same `treatment_run_id`, references its triggering event, and does not reset accumulated resources.

A `replan` changes the treatment's intermediate plan or decomposition while remaining within the frozen treatment policy. It remains inside the same run and must be represented in lineage. If it exceeds the frozen treatment specification, it is a protocol change and requires a new version.

An `escalation` transfers work to a different capability/model/provider/tier because the frozen treatment policy permits that transition. It remains inside the same run and inherits the complete accumulated cost of earlier stages.

`CHEAP_ATTEMPT + ESCALATION_TO_STRONG = ONE TREATMENT RUN`

## Repeated rollouts

A `rollout` is one independent repetition of the same frozen task-treatment pairing under the confirmatory/pilot protocol.

Each rollout receives a distinct `rollout_id` and therefore a distinct `treatment_run_id`.

Repeated rollouts must not be merged into one run, nor may the most favorable rollout be selected post hoc as the representative result.

Rollout count and statistical use are deferred to later blocks.

## Terminal run outcome

Every treatment run terminates with exactly one frozen Block 2 outcome:

`VERIFIED_SOLVED_TASK = YES | NO | INCONCLUSIVE`

The outcome belongs to the whole run, not to the most favorable internal attempt.

A treatment-internal declaration of success cannot produce `YES` without the frozen verification path establishing `YES`.

## Verified solved task as denominator event

For later economic metrics, one verified solved task is one completed treatment run whose terminal global outcome is `YES`.

`verified_solved_count = count(treatment_run where outcome == YES)`

`NO` and `INCONCLUSIVE` contribute zero solved tasks, but their incurred resources remain part of treatment resource totals under Blocks 3B–3D.

This prevents survivorship accounting.

## Minimum run identity

Each run must be bindable to at least:
- `protocol_version`;
- `corpus_version`;
- `task_id`;
- `task_family`;
- immutable base-state identity;
- `oracle_version`;
- `treatment_id`;
- treatment configuration/version;
- `rollout_id`;
- globally unique `treatment_run_id`;
- ordered attempt/event lineage;
- candidate output/state identity where produced;
- verifier/harness/environment identity;
- terminal `YES | NO | INCONCLUSIVE`;
- raw evidence references;
- start/end timestamps sufficient for later latency accounting.

## Integrity rules

- No resource-bearing event may exist outside a parent `treatment_run_id` if the event was caused by that treatment invocation.
- No attempt can belong to two runs.
- No run can produce more than one terminal verified outcome.
- Restarting after terminal outcome creates a new rollout/run, not a continuation.
- Manual rescue or investigator intervention that changes treatment behavior must be explicitly recorded and cannot be silently treated as native treatment performance.
- Invalid/harness-failed runs remain real runs and cannot be deleted from accounting merely because their terminal outcome is `INCONCLUSIVE`.

## Completion criterion

Block 3A is complete when the project has a frozen treatment-run accounting boundary and immutable lineage semantics that make retries, escalation, repeated rollouts, failures, and terminal verified outcomes attributable without selective omission.

Status after this document:

`BLOCK_3A = COMPLETE`
`BLOCK_3B = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
