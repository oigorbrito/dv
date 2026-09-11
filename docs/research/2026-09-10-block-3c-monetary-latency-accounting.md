# Block 3C — Monetary and latency accounting

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE
Implementation approval: NONE

## Scope

This sub-block freezes monetary-cost and latency dimensions for each treatment run. It defines what categories must be observed and the primary economic metric.

It does not yet freeze detailed cache/reuse allocation, missing-telemetry handling, shared-infrastructure allocation, statistical inference, sample size, or treatment acceptance margins.

## Governing principles

A token-efficient treatment can still be economically inferior because providers price token classes differently, verification has cost, infrastructure is nonzero, retries add work, or latency is materially worse.

Therefore:

`TOKEN SAVINGS != MONETARY SAVINGS`

`MONETARY SAVINGS != LATENCY IMPROVEMENT`

`CHEAP MODEL PRICE != CHEAP VERIFIED SOLUTION`

The primary monetary effectiveness metric is:

`TOTAL_MONETARY_COST / VERIFIED_SOLVED_TASK`

All treatment-caused monetary cost from all runs belongs in the numerator; only terminal `YES` runs count as verified solved tasks.

## Monetary accounting categories

At minimum, a run must be capable of separating:

1. `model_api_cost`
   - provider/model charges for input, output, cached input, reasoning, or other billed classes;
   - all calls for routing, planning, context, execution, handoff/escalation, verification, retry/replanning.

2. `external_tool_service_cost`
   - paid APIs/services invoked specifically by the treatment;
   - metered external search, sandbox, database, storage, or specialist services where material.

3. `runtime_compute_cost`
   - metered CPU/GPU/VM/container/runtime cost when treatment-dependent and material;
   - local/free compute is not assigned an invented commercial price in primary observed accounting unless a later protocol explicitly defines an opportunity-cost model.

4. `verification_cost`
   - separable monetary cost of verification/judging where possible;
   - if verification calls are already included in `model_api_cost`, this is a tagged subset, not double-counted.

5. `coordination_infrastructure_cost`
   - treatment-dependent orchestration, networking, storage, queueing, or persistent runtime costs when directly measurable and material.

No category may be double-counted.

## Provider price binding

Each billable event must be bound, where possible, to:
- provider;
- model/service identifier;
- pricing unit/class;
- applicable price schedule/version or observation date;
- usage quantity;
- computed event cost;
- currency.

Price changes must not silently alter historical run costs. Raw usage and price binding must be sufficient to recompute cost under the contemporaneous price schedule and, if desired later, under a normalized sensitivity schedule.

Observed billed cost takes precedence over reconstructed cost when both are trustworthy and cover the same boundary; discrepancies must be retained for reconciliation rather than silently choosing the more favorable value.

## Total monetary cost

For one run:

`total_monetary_cost_run = sum(all non-duplicated attributable monetary events)`

For one treatment:

`total_monetary_cost_treatment = sum(total_monetary_cost_run for every assigned run)`

Primary effectiveness metric:

`monetary_cost_per_verified_solved_task = total_monetary_cost_treatment / verified_solved_count`

If `verified_solved_count = 0`, the ratio cannot be represented as zero. Later analysis must report it as undefined/infinite for comparative effectiveness purposes.

## Free tiers and zero-price resources

A provider call that is genuinely priced at zero under the applicable experimental conditions may have observed monetary cost `0`, but:
- its token usage is still recorded under Block 3B;
- its latency is still recorded;
- quota/rate-limit failures remain part of run outcomes and resource history;
- zero marginal price must not be generalized into a claim of zero resource consumption.

Promotional credits, subscriptions, prepaid bundles, or research grants must be represented transparently. A later confirmatory protocol may define both observed out-of-pocket and normalized list-price analyses, but must not choose the favorable basis post hoc.

## Latency accounting

Latency is a separate dimension, not converted into money unless a later frozen protocol explicitly defines such a valuation.

At minimum record per run:

1. `wall_clock_latency`
   - elapsed time from treatment-run start to terminal run outcome;
   - primary user-visible/time-to-verified-result measure.

2. `model_call_latency`
   - elapsed time attributable to model/provider calls where measurable.

3. `tool_runtime_latency`
   - execution time for tools, tests, builds, sandboxes, or deterministic computation.

4. `verification_latency`
   - time spent establishing the frozen oracle outcome; may overlap tagged model/tool latency and therefore must not be naively summed if overlapping.

5. `coordination_overhead_latency`
   - orchestration, queueing, network, handoff, scheduling, or state-transfer delays where measurable.

The canonical run latency is wall-clock elapsed time. Component latencies are diagnostic decompositions and may overlap; they are not required to arithmetically sum to wall clock.

## Parallelism

Parallel work does not reduce resource usage merely because wall-clock time is lower.

For parallel calls:
- all attributable tokens and monetary costs are accumulated;
- wall-clock latency measures actual elapsed run time;
- individual call durations remain separately observable;
- summed call durations must not be substituted for wall-clock latency.

Thus resource efficiency and latency efficiency remain distinct.

## Timeouts and failed/inconclusive runs

A timeout is not assigned zero latency or zero cost.

All incurred costs and elapsed time up to termination remain attributable to the run. Product-vs-harness interpretation follows frozen Block 2 evidence semantics; accounting does not rewrite the outcome.

`NO` and `INCONCLUSIVE` runs remain in monetary and latency descriptive distributions and in treatment monetary totals.

## Raw evidence requirement

Each monetary/latency event must eventually be bindable to:
- `treatment_run_id`;
- event/attempt identity;
- resource category;
- provider/model/service identity where relevant;
- raw usage/charge telemetry;
- price schedule reference where reconstructed;
- normalized monetary amount and currency;
- start/end/duration data where available;
- raw evidence/log reference.

## Currency

A canonical reporting currency must be frozen before pilot analysis if treatments incur charges in multiple currencies. Raw original-currency amounts and conversion basis/date must be retained. Currency conversion policy belongs to Block 3D/3E reconciliation and cannot be selected after observing which treatment benefits.

## Secondary metrics

Later analysis may report:
- monetary cost per run;
- model/API cost share;
- verification cost share;
- wall-clock latency per run;
- latency conditional on outcome;
- cost and latency by task family;
- cost/latency distributions and tail behavior.

These remain secondary/descriptive unless a later frozen protocol explicitly promotes them.

## Completion criterion

Block 3C is complete when monetary cost and latency have independent, treatment-complete accounting boundaries and the primary monetary metric is frozen as `total monetary cost / verified solved task`, without conflating zero price, token efficiency, monetary efficiency, or latency efficiency.

Status after this document:

`BLOCK_3A = COMPLETE`
`BLOCK_3B = COMPLETE`
`BLOCK_3C = COMPLETE`
`BLOCK_3D = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
