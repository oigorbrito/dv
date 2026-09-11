# Drift and selective rebenchmarking

Status: RESEARCH / FALSIFICATION
Date: 2026-09-10

## Question

Can a simple policy table by task family/provider remain economically useful over time without paying the cost of continuously rebenchmarking the full provider matrix?

## Current evidence

### Drift is heterogeneous

DriftBench (MLSys 2026) measured 236,985 prompt-response pairs across 105 serving configurations spanning 5 models, 4 GPU platforms, 3 frameworks, and 3 precisions. It reports that hardware/precision changes exhibited relatively systematic drift that could be predicted with useful held-out generalization, while framework/model changes were idiosyncratic and required re-measurement.

Implication for `dv`: not every change should invalidate every empirical cell. Invalidation scope should depend on the class of change.

### Routing under drift is prior art, not a blank-slate responsibility

Recent work on drift-aware LLM routing models nonstationary request mix and model-frontier changes and uses rolling audit windows plus a small shadow-audit stream. This is evidence that continuous full-matrix benchmarking is not the only available strategy.

However, this is research prior art, not evidence that `dv` should implement a learned drift-aware router.

### Sophisticated routers still need strong baselines

LLMRouterBench evaluates over 400K instances, 21 datasets, and 33 models and finds that multiple sophisticated routing methods fail to reliably beat simple baselines under unified evaluation. This reinforces the project rule that complexity must earn its cost empirically.

## Candidate invalidation policy — hypothesis only

Treat each empirical policy cell as revision-bound evidence:

`cell = task_family × provider × provider_revision × harness_revision × verifier_revision × environment_class`

Possible invalidation classes:

1. **Model/provider semantic change**
   - new model family;
   - major model revision;
   - provider behavior/policy change;
   - material framework change affecting execution semantics.
   - Default: invalidate affected provider cells and re-measure representative tasks.

2. **Harness/verifier change**
   - acceptance oracle changes;
   - new test harness;
   - task-family definition changes.
   - Default: invalidate cells whose verified-success meaning changed.

3. **Infrastructure-only change**
   - hardware;
   - precision;
   - serving configuration;
   - transport/runtime tuning.
   - Default: do not assume semantic invariance, but prefer targeted shadow checks before full rebenchmark if evidence suggests the change class is predictable.

4. **Price/latency change without semantic change**
   - token price;
   - quota;
   - observed latency;
   - local/free availability.
   - Default: recompute economic ranking from preserved measurements where possible; do not rerun quality benchmark unless behavior may also have changed.

5. **Observed production miss**
   - verified failure in a cell previously considered safe;
   - unexpected escalation rate;
   - cost regression;
   - verifier disagreement.
   - Default: quarantine or downgrade the cell and trigger targeted remeasurement.

## Cheap maintenance hypothesis

Prefer event-driven and sparse auditing over periodic full-matrix reruns:

```text
provider/config change
        |
        v
classify change type
        |
        +--> economic-only -> recompute ranking
        |
        +--> low semantic risk -> small shadow sample
        |
        +--> semantic/harness change -> targeted representative benchmark
        |
        +--> observed failure -> quarantine + targeted benchmark
```

Periodic broad rebenchmarking remains a safety net, not the primary mechanism.

## Shadow-audit concept

A small fraction of real or replayable tasks can be evaluated on alternate providers without changing the production decision. The purpose is not online learning by default; it is to detect whether stored evidence is becoming stale.

Required measurements:
- verified success;
- total tokens;
- monetary cost;
- latency;
- escalation rate;
- verifier disagreement;
- provider revision;
- harness/verifier revision.

The audit rate itself must be treated as a cost and included in system economics.

## Empirical falsification design

Compare at least:

- D0: fixed static table, no refresh;
- D1: periodic full rebenchmark;
- D2: event-driven targeted rebenchmark;
- D3: sparse shadow audit + targeted rebenchmark;
- D4: learned/adaptive drift-aware router.

Primary metric:

`total system tokens / verified solved task`

Also:
- monetary cost / verified solved task;
- verified task success;
- stale-cell failure rate;
- false invalidation rate;
- benchmark maintenance cost;
- detection delay after real drift;
- number of cells remeasured per change.

D4 is not admissible as preferred architecture unless its gain exceeds the cost and complexity of D2/D3.

## Current disposition

No new `dv` component is approved.

The strongest current hypothesis is that drift handling can remain mostly **revision-bound evidence + explicit invalidation + sparse targeted auditing**, rather than a continuously reasoning Brain.

This further reduces the residual `dv` core toward configuration, evidence metadata, adapters, and measurement.

## Decision rule

A policy cell is never timeless truth. It is evidence valid only for its declared revisions and scope.

Do not rebenchmark everything merely because something changed. Do not reuse old evidence merely because the provider name is unchanged.

Use the smallest remeasurement scope that is empirically defensible, and count maintenance/audit cost in the same economics as execution.