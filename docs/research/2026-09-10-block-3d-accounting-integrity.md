# Block 3D — Treatment-independent accounting integrity

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE
Implementation approval: NONE

## Scope

This sub-block freezes integrity rules that prevent one treatment from receiving favorable accounting because of retries, failures, caching, shared artifacts, missing telemetry, parallelism, free tiers, or infrastructure differences.

It governs measurement treatment, not architecture.

## Governing principle

Equivalent resource events must be accounted for under equivalent rules independent of treatment identity or observed outcome.

`SAME RESOURCE EVENT -> SAME ACCOUNTING RULE`

`FAILED WORK != FREE WORK`

`MISSING TELEMETRY != ZERO USAGE`

`CACHE HIT != ZERO SYSTEM WORK BY DEFAULT`

`PARALLEL != FREE`

Accounting rules must be frozen before pilot results are interpreted and may not be changed post hoc to favor a treatment.

## 1. Failed and inconclusive runs

Every run assigned to a treatment remains part of treatment accounting, including terminal `NO` and `INCONCLUSIVE`.

All resources consumed before termination remain attributable to the run.

A run may be excluded from a specific inferential analysis only under a later predeclared protocol rule, but exclusion from analysis does not erase its raw accounting record.

Harness failures and environment failures remain `INCONCLUSIVE` under Block 2 semantics; they are not rewritten as product failures merely to simplify accounting.

## 2. Retries, replans, and escalations

All retries, replans, and escalations remain inside the parent treatment run defined in Block 3A.

Resource totals accumulate monotonically across the run.

No later successful attempt may replace or erase earlier resource consumption.

If a retry is caused by experiment infrastructure rather than the treatment, the event must be explicitly attributed as infrastructure-caused. Whether it is included in a primary comparative estimator is deferred to the frozen pilot/confirmatory protocol, but the raw event must remain visible.

## 3. Timeouts and cancellation

Timeout/cancellation events must preserve:
- elapsed wall-clock time to termination;
- all tokens/costs already incurred;
- reason/actor initiating termination;
- whether work continued remotely after local cancellation, when observable;
- terminal verification outcome under Block 2.

A timeout does not imply zero cost and does not automatically imply `NO`.

## 4. Parallel calls

All token and monetary resource use from parallel calls is accumulated.

Wall-clock latency is measured by actual elapsed treatment-run time, not by summing parallel durations.

Parallelism is therefore permitted to trade higher resource consumption for lower elapsed latency, but neither dimension may be hidden by the other.

## 5. Cache hits

Cache behavior must be observable and treatment-independent.

At minimum distinguish:
- provider-side input/prompt caching reported by telemetry;
- local deterministic artifact cache;
- reusable plan/context artifact;
- repository/index/preprocessing cache;
- verification-result cache, if ever allowed by later protocol.

Provider-reported cached token classes are recorded as reported and priced according to the applicable schedule.

A cache hit does not erase the existence or provenance of the cached artifact.

## 6. Precomputation and reusable artifacts

Precomputation is classified by causal scope:

### Experiment-global fixed setup

Work performed once, before treatment assignment/results, and identically available to all treatments may be recorded as experiment setup rather than charged repeatedly to each run.

Examples may include downloading the frozen corpus or constructing a treatment-neutral immutable test environment.

### Treatment-specific fixed setup

Work required only because a treatment needs it must be recorded as treatment-specific setup.

It cannot be reclassified as experiment-global merely because it is reusable across that treatment's runs.

### Run-specific dynamic work

Work generated or refreshed because of a particular task/run belongs to that run, even if its result could theoretically be reused later.

### Cross-run reuse

If a later run consumes a previously produced artifact, the event must record the reuse and the artifact provenance. The pilot/confirmatory protocol must predeclare whether primary accounting uses:
- marginal observed cost;
- amortized treatment-specific setup cost;
- both as separate analyses.

The basis cannot be selected after observing treatment rankings.

## 7. Warm vs cold state

Any state capable of materially changing tokens, cost, or latency must be classified before comparison where feasible.

Examples:
- warm provider cache;
- warmed dependency/build cache;
- preloaded repository index;
- retained conversation/context state;
- persistent executor process;
- previously generated plan or summary.

Treatments must receive equivalent warm/cold-state rules unless state retention is itself an explicit frozen part of the treatment.

If state asymmetry is intrinsic to a treatment, it must be measured rather than normalized away.

## 8. Missing provider usage telemetry

Missing usage telemetry is never interpreted as zero.

For a resource-bearing event with incomplete telemetry, use this precedence:

1. trustworthy provider-reported usage/billing record;
2. trustworthy runtime/client telemetry covering the same event;
3. a predeclared deterministic reconstruction method validated before treatment comparison;
4. otherwise mark the relevant accounting field `MISSING/UNRESOLVED`.

No favorable point estimate may be invented from missing telemetry.

If missingness prevents defensible computation of a primary metric, the affected comparison is `INCONCLUSIVE` for that metric unless a later frozen protocol has an already-declared missing-data rule.

## 9. Telemetry conflicts

When two trustworthy sources disagree:
- preserve both raw values;
- record source identity and boundary;
- apply a predeclared precedence rule only if the sources measure equivalent quantities;
- otherwise mark the discrepancy unresolved.

Do not silently choose the lower value.

## 10. Provider/model identity and drift

Every model/service event should preserve the most specific provider model/version/deployment identity available.

If a provider silently changes a model behind a stable alias and the change is detectable or documented, the affected runs must be marked for drift analysis.

Provider drift is not automatically treatment failure, but it can invalidate comparability and therefore may produce an `INCONCLUSIVE` experimental comparison.

## 11. Price drift

Raw usage must be retained separately from computed currency cost.

Each reconstructed charge must bind to the price schedule applicable to the event time unless the protocol explicitly defines a normalized price analysis.

Primary observed-cost accounting may not mix historical price schedules inconsistently across treatments.

If a normalized constant-price sensitivity analysis is later used, it must be labeled separately from observed contemporaneous cost.

## 12. Currency conversion

When multiple currencies occur:
- preserve original amount/currency;
- use one predeclared conversion source and convention for canonical reporting;
- bind the conversion to a specified date/time rule;
- preserve the exchange-rate evidence/reference.

No treatment-specific conversion basis is allowed.

## 13. Free tiers, subscriptions, credits, quotas

Observed out-of-pocket cost and underlying resource usage must remain distinguishable.

A zero-price/free-tier event may have monetary cost zero but still has tokens, latency, quota consumption, and failure risk.

Credits/subscriptions/prepaid access must be tagged. If the later protocol compares normalized list-price cost, that analysis must be frozen before inspecting comparative results.

Quota exhaustion/rate limiting is part of empirical treatment behavior if it arises under the declared operating conditions; it must not be silently retried outside the accounting boundary.

## 14. External/runtime overhead

Material treatment-dependent overhead must be recorded when measurable, including paid sandbox/runtime, network/service calls, storage, queues, and coordination services.

Negligible or unavailable-to-measure overhead may be documented as such, but cannot be represented as precisely zero without evidence.

No fictional token equivalent is assigned to non-token deterministic work.

## 15. Manual investigator intervention

Any manual action after run start must be logged with actor, reason, timestamp, and effect.

If the intervention changes treatment behavior, supplies missing solution information, repairs a treatment-caused failure, or otherwise creates an advantage unavailable under the frozen treatment, the run cannot be counted as native treatment success.

Its verification outcome may remain recordable, but treatment-performance interpretation becomes `INCONCLUSIVE` or protocol-deviant according to the later frozen analysis rule.

## 16. Accounting invariants

The following invariants are frozen:

- every resource-bearing treatment event maps to one run or a declared setup scope;
- every run has one treatment, one task, one rollout, and one terminal outcome;
- retries/escalations never reset totals;
- `NO`/`INCONCLUSIVE` never erase resources;
- missing telemetry never becomes zero by default;
- shared setup cannot be treatment-specific in substance and experiment-global in accounting;
- resource categories cannot be double-counted;
- raw evidence is retained sufficiently to recompute normalized aggregates;
- treatment identity cannot determine which accounting rule is applied;
- accounting policy changes require a new protocol/specification version and cannot rewrite prior frozen results silently.

## Audit/reconciliation requirement

Before any pilot treatment comparison is accepted, each run must pass an accounting reconciliation check confirming at least:
- identity completeness;
- lineage completeness;
- terminal outcome presence;
- no orphan resource events;
- no duplicate event charging;
- token/cost field consistency where telemetry permits;
- explicit status for missing/conflicting telemetry;
- explicit cache/setup provenance where relevant.

A reconciliation failure does not become zero cost; it prevents a defensible primary metric until resolved or classified by the frozen protocol.

## Completion criterion

Block 3D is complete when treatment-independent accounting rules prevent selective omission or favorable reinterpretation of failures, retries, escalations, parallel calls, caching/reuse, free tiers, missing telemetry, drift, and material external overhead.

Status after this document:

`BLOCK_3A = COMPLETE`
`BLOCK_3B = COMPLETE`
`BLOCK_3C = COMPLETE`
`BLOCK_3D = COMPLETE`
`BLOCK_3E = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
