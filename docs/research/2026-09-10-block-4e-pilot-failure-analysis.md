# Block 4E — Pilot instrumentation defects, variance, failure modes, and pathologies

Date: 2026-09-10
Status: COMPLETE / RESEARCH ONLY
Architecture approval: NONE

## Purpose

Analyze what the attempted Block 4 entry actually demonstrated without upgrading missing execution into treatment evidence.

## Primary blocker

`P4-BLK-001 — executable measurement harness absent`

Severity: BLOCKING
Scope: all candidate treatments
Attribution: research infrastructure, not product/treatment behavior

The repository contains a defensible semantic protocol but not the minimum executable instrumentation needed to instantiate a treatment run under Blocks 2–3.

## Consequences

Because P0 produced zero accepted treatment runs:
- treatment success variance is unmeasured;
- token variance is unmeasured;
- monetary variance is unmeasured;
- latency variance is unmeasured;
- retry/escalation frequency is unmeasured;
- family-specific treatment pathologies are unmeasured;
- treatment ranking is unavailable.

These quantities are `UNMEASURED`, not zero.

## Pathology discovered at pilot level

The pilot exposed a research-process pathology rather than a treatment pathology: specification maturity exceeded operational measurement maturity.

This is useful falsification evidence because advancing directly to confirmatory design would create false precision around sample size, margins, or estimators before the system can produce one reconciled observation.

## Minimum remediation boundary

The next admissible implementation is narrowly scoped to a pilot measurement harness satisfying Block 4B. Its purpose is evidence production, not product architecture.

It may contain only what is necessary to:
- materialize frozen development tasks solution-blind;
- invoke treatments through explicit wrappers;
- collect run/event identity and resource telemetry;
- invoke frozen oracles;
- retain raw evidence;
- reconcile accounting.

Existing tools/standards should be composed before custom infrastructure is added. No generic runtime/router/registry/IR is justified by this blocker.

## Re-entry evidence required

P0 may be retried only after a treatment-neutral dry run demonstrates all Block 3 reconciliation checks and a raw record can be independently recomputed.

A successful dry run proves only measurement readiness; it does not prove treatment quality.

## Statistical implication

No defensible variance estimate exists yet, so Block 5 must not freeze confirmatory sample size, superiority/non-inferiority margin, or precision target from fabricated assumptions.

`BLOCK_4E = COMPLETE`
`TREATMENT_PATHOLOGIES = UNMEASURED`
`PILOT_BLOCKER = P4-BLK-001`
