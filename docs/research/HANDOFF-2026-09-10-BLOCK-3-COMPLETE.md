# HANDOFF — dv research after Block 3 completion

Date: 2026-09-10
Repository: `oigorbrito/dv`
Current research state: Block 1 COMPLETE; Block 2 COMPLETE; Block 3 COMPLETE; Block 4 NOT STARTED
Architecture approval: NONE
Implementation approval: NONE

## Continuation rule

Do not reopen Blocks 1–3 unless a concrete documented defect is discovered.

The next research block is:

`BLOCK 4 — PILOT`

The pilot exists to validate instrumentation, operational feasibility, variance, protocol mechanics, and obvious treatment pathologies before any confirmatory protocol is frozen.

Do not use the sealed external holdout as an exploratory tuning set.

## Canonical project objective remains unchanged

`dv` is research into whether a minimal capability-composition/economic-policy layer is justified between existing providers, standards, runtimes, verifiers, and heterogeneous capabilities.

The unit of composition is capability/function, not repository/framework/codebase.

MetaO, SMAG, MAF, and other systems remain capability/prior-art/chassis/falsifier sources, not mandatory code dependencies.

A valid final result remains:

`NO BUILD`

or, if evidence warrants only a very small intervention:

`MICRO-POLICY JUSTIFIED`

or:

`INCONCLUSIVE`

No architecture is approved merely because research documentation is complete.

## Frozen governing rules

- software-engineering defensibility and empirical validation are required before architecture/component approval;
- `DOCUMENTED != EXECUTED != MEASURED != ACCEPTED`;
- `EXECUTOR_SUCCESS != VERIFIED_TASK_SUCCESS`;
- `LOWER EXECUTOR TOKENS != LOWER SYSTEM COST`;
- `POPULAR != PROVEN`;
- `INFERRED != EMPIRICALLY_DEMONSTRATED`;
- `INCONCLUSIVE` is a first-class outcome;
- economic objective is complete system resource cost per verified solved task;
- work in closed blocks;
- no post-hoc policy/oracle/corpus/accounting edits to favor a treatment.

## Block 1 — COMPLETE

Canonical corpus: 36 tasks.

- 18 development/pilot tasks;
- 18 sealed external holdout tasks;
- six task families;
- 3 development + 3 holdout tasks per family.

The sealed holdout remains unavailable for exploratory tuning.

## Block 2 — COMPLETE

Global verification outcome:

`VERIFIED_SOLVED_TASK = YES | NO | INCONCLUSIVE`

Required dimensions:
- V1 task satisfaction;
- V2 regression/preservation;
- V3 harness validity.

Failure attribution and evidence precedence remain frozen.

## Block 3 — Measurement Envelope — COMPLETE

### 3A — accounting unit and run identity

File:
`docs/research/2026-09-10-block-3a-accounting-unit-run-identity.md`

Commit:
`7592483c853df147dbf358924ed632cdd005b705`

Frozen semantics:
- primary accounting unit is one complete `treatment_run`;
- one run = one frozen task + treatment + rollout through one terminal verified outcome;
- attempts are subordinate events;
- retries, replans, handoffs, and escalations remain inside the parent run;
- repeated rollouts are distinct runs;
- `NO` and `INCONCLUSIVE` do not erase resource consumption;
- only terminal `YES` contributes one verified solved task to the economic denominator.

### 3B — token accounting

File:
`docs/research/2026-09-10-block-3b-token-accounting.md`

Commit:
`8837c461a4ce4cac82326f155d7a6236fda891f8`

Primary token metric:

`TOTAL_SYSTEM_TOKENS / VERIFIED_SOLVED_TASK`

Mandatory token partitions:
- routing/classification;
- planning/task shaping;
- context construction/reconstruction;
- execution;
- handoff/escalation;
- verification/judging;
- retry/replanning.

Executor-only accounting is explicitly insufficient.

All token usage from `NO` and `INCONCLUSIVE` runs remains in treatment totals.

### 3C — monetary and latency accounting

File:
`docs/research/2026-09-10-block-3c-monetary-latency-accounting.md`

Commit:
`0bb2bfbe8c30d6437f89a8a208eb2d33b6267c48`

Primary monetary metric:

`TOTAL_MONETARY_COST / VERIFIED_SOLVED_TASK`

Canonical latency measure:

`WALL_CLOCK_LATENCY`

Tokens, money, and latency remain separate dimensions.

`TOKEN EFFICIENCY != MONETARY EFFICIENCY != LATENCY EFFICIENCY`

Free/zero-price execution still retains token, latency, quota, and reliability effects.

### 3D — accounting integrity

File:
`docs/research/2026-09-10-block-3d-accounting-integrity.md`

Commit:
`ecfa799776c723b8b70df6e05a0b5de8cc662207`

Frozen integrity rules include:
- failures/inconclusives retain resources;
- retries/escalations accumulate;
- timeouts retain incurred resource use;
- parallelism does not make calls free;
- missing telemetry is never zero by default;
- telemetry conflicts cannot be resolved by choosing the favorable number;
- cache/reuse provenance must be explicit;
- treatment-specific setup cannot masquerade as global setup;
- dynamic run work belongs to the run;
- warm/cold state asymmetry must be controlled or measured;
- free tiers/credits/subscriptions must be tagged;
- provider/model/price drift must remain observable;
- material manual intervention must be recorded;
- raw evidence must permit reconciliation/recomputation.

### 3E — canonical reconciliation/freeze

File:
`docs/research/2026-09-10-block-3e-measurement-envelope-freeze.md`

Commit:
`d4ffdecf10439d6572c6dd8e8738a218805e5f0f`

Block 3 is reconciled into one canonical pilot-ready measurement envelope.

The primary research accounting question is now:

`Which treatment achieves verified solved tasks at the lowest complete system resource cost under the frozen verification contract?`

No arbitrary composite score was introduced.

The following remain separate:
- verified correctness;
- total system tokens;
- monetary cost;
- wall-clock latency.

## Canonical pilot record requirements

Every pilot run must be representable with:
- protocol/corpus/task/treatment/rollout/run identity;
- immutable base-state and oracle identity;
- attempt/retry/replan/escalation lineage;
- candidate-state identity;
- terminal verification outcome;
- token partition and raw telemetry;
- monetary evidence and price binding;
- wall-clock and component timing where measurable;
- cache/setup/reuse provenance;
- missing/conflicting telemetry markers;
- accounting reconciliation status;
- raw evidence/log references.

Exact storage technology/schema is not architecture-approved. Block 4 should implement only the minimum instrumentation needed to exercise this frozen measurement contract; it must not opportunistically create a new generic runtime, workflow engine, registry, memory system, or provider-neutral IR.

## Block 4 entry gate

Before comparative pilot summaries are trusted, representative pilot/dry runs must demonstrate that instrumentation can:

1. preserve one run -> one task/treatment/rollout/outcome;
2. attach all resource-bearing events to a run or declared setup scope;
3. retain failed/inconclusive costs;
4. preserve retry/escalation lineage;
5. avoid duplicate charging;
6. reconstruct token totals from available telemetry;
7. bind monetary cost to explicit billing/price evidence;
8. produce coherent wall-clock timing;
9. expose cache/setup/reuse provenance;
10. expose missing/conflicting telemetry rather than silently imputing it;
11. retain enough raw evidence to reproduce aggregates.

If instrumentation cannot satisfy these requirements, the defensible result of the pilot may be `INCONCLUSIVE` / measurement redesign rather than forced treatment ranking.

## What remains intentionally unfrozen

Block 4/5 must still determine, in proper sequence:
- actual pilot execution design;
- number of pilot rollouts;
- treatment ordering/randomization/counterbalancing where applicable;
- variance and failure modes;
- instrumentation reliability;
- confirmatory sample size;
- statistical estimator/interval method;
- decision/non-inferiority/equivalence margins if justified;
- treatment approval/rejection rule;
- confirmatory protocol;
- sealed-holdout execution.

These must not be invented retroactively after seeing confirmatory outcomes.

## Candidate treatment arms remain unapproved

Initial candidates remain:
- E0 strongest-direct;
- E1 cheap/free-direct + verify;
- E2 cheap-first -> clean state-based escalation -> strong;
- E3 static task-family policy.

Learned/LLM routing remains excluded from the first round unless a later explicit protocol revision is justified before confirmatory evidence is observed.

## Exact continuation point

`BLOCK_1 = COMPLETE`
`BLOCK_2 = COMPLETE`
`BLOCK_3 = COMPLETE`
`BLOCK_4 = NOT_STARTED`

NEXT:

`BLOCK 4 — PILOT`

Recommended internal sequence for the next chat:

- 4A — pilot purpose, entry criteria, and development-set scope;
- 4B — minimum measurement harness/instrumentation plan;
- 4C — pilot execution design and treatment ordering;
- 4D — run pilot on development tasks only;
- 4E — analyze instrumentation defects, variance, failure modes, and treatment pathologies;
- 4F — pilot reconciliation/freeze and explicit go/no-go into Block 5.

Do not touch the sealed external holdout during exploratory pilot work.
