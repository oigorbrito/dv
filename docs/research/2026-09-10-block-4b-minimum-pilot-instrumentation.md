# Block 4B — Minimum pilot instrumentation gate

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE
Implementation approval: MINIMUM PILOT INSTRUMENTATION ONLY

## Purpose

Define the minimum observable instrumentation required to execute the staged pilot without designing a generic dv runtime.

## Minimum required capabilities

The pilot harness must be able to:
1. materialize a development task at its frozen base revision without exposing solution material to the treatment;
2. assign protocol, corpus, task, treatment, rollout, and globally unique run identities;
3. preserve attempt/retry/replan/escalation lineage;
4. record treatment-caused model/tool/runtime events under the Block 3 categories;
5. preserve raw provider usage telemetry and missing/conflicting telemetry markers;
6. bind monetary reconstruction to explicit provider/model/price evidence;
7. timestamp run start/end and derive wall-clock latency;
8. invoke the frozen family oracle and retain raw V1/V2/V3 evidence;
9. emit exactly one terminal YES | NO | INCONCLUSIVE outcome per run;
10. reconcile raw events into non-duplicated run totals;
11. retain cache/setup/reuse provenance;
12. export enough raw evidence to recompute summaries independently.

## Non-goals

The pilot must not create a new generic workflow engine, registry, memory system, provider-neutral IR, durable runtime, or learned router.

A narrow script, structured record, adapter, or experiment wrapper is admissible only insofar as it is required to exercise the frozen measurement contract.

## Repository-state audit

At the start of Block 4, the `dv` repository root contains `AGENTS.md`, `README.md`, and `docs/`, with no executable pilot harness, source tree, workflow, measurement collector, provider adapter, task materializer, or run-record implementation visible in the repository.

Therefore the semantic measurement specification is complete, but the operational instrumentation entry gate is not satisfied.

This is an evidence-class distinction:

`DOCUMENTED MEASUREMENT CONTRACT != EXECUTABLE MEASUREMENT HARNESS`

## Gate decision

P0 comparative treatment runs must not be accepted until the above minimum instrumentation exists and passes at least one treatment-neutral dry-run reconciliation check.

Missing harness capability is a measurement/infrastructure blocker, not a treatment failure.

`BLOCK_4B = COMPLETE`
`P0_INSTRUMENTATION_GATE = FAIL`
