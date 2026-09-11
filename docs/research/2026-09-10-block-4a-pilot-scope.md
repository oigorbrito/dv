# Block 4A — Pilot purpose, entry criteria, and development-set scope

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE
Implementation approval: MINIMUM PILOT INSTRUMENTATION ONLY

## Purpose

Block 4 is an exploratory pilot whose purpose is to test whether the frozen corpus, oracle, run identity, and accounting envelope can be exercised operationally before any confirmatory protocol is frozen.

The pilot is not evidence of external generalization and is not allowed to approve a dv architecture.

## Scope

Only the 18 development/pilot tasks in corpus v0 are admissible. The 18 external holdout tasks remain sealed and must not be executed, inspected for outcomes, or used for tuning.

Candidate treatments remain:
- E0 strongest-direct;
- E1 cheap/free-direct + verify;
- E2 cheap-first -> clean state-based escalation -> strong;
- E3 static policy by task family.

These are experimental arms, not approved policies.

## Entry requirements

A pilot run may enter comparative analysis only if it can be bound to the Block 3 canonical record and satisfy the reconciliation checks for identity, lineage, verification, resource accounting, latency, cache/setup provenance, and raw evidence.

No treatment may receive a weaker measurement boundary.

## Staged pilot principle

The pilot must fail cheaply before consuming the full development set.

Phase P0 is an instrumentation smoke pilot using one development task per family, all four treatments, one rollout each: 6 tasks x 4 treatments = 24 planned runs.

Only if P0 demonstrates defensible measurement integrity may Phase P1 expand to the remaining development tasks and repeated rollouts for variance estimation.

No fixed confirmatory sample size is implied by P0 or P1.

## Exit outcomes

Block 4 may end as:
- PILOT_READY: instrumentation and mechanics are adequate to inform Block 5;
- PILOT_INCONCLUSIVE: operational or measurement evidence is insufficient;
- PILOT_REDESIGN_REQUIRED: a documented defect requires remediation before further pilot execution.

A pilot outcome is not an architecture decision.

`BLOCK_4A = COMPLETE`
