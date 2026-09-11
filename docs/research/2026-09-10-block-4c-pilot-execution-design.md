# Block 4C — Pilot execution design and treatment ordering

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE
Implementation approval: MINIMUM PILOT INSTRUMENTATION ONLY

## Purpose

Freeze the pilot mechanics before observing treatment outcomes.

## P0 smoke pilot

Use exactly one development task from each family, selected deterministically as the first canonical development instance in corpus v0:
- D-F1-01
- D-F2-01
- D-F3-01
- D-F4-01
- D-F5-01
- D-F6-01

All four candidate treatments are assigned to each selected task, one rollout each, for 24 planned treatment runs.

P0 exists to falsify measurement readiness, not to rank treatments.

## Ordering

To avoid giving one treatment a systematic warm-state advantage, treatment order must rotate by family using a deterministic Latin-style cyclic ordering:
- F1: E0, E1, E2, E3
- F2: E1, E2, E3, E0
- F3: E2, E3, E0, E1
- F4: E3, E0, E1, E2
- F5: E0, E1, E2, E3
- F6: E1, E2, E3, E0

This is a pilot balancing mechanism only; Block 5 must freeze any confirmatory randomization/counterbalancing independently.

## State policy

Each run must begin from the frozen task base revision and a declared environment state. Any cache retained across runs must be treatment-neutral or explicitly recorded. Solution heads/diffs remain evaluator-only.

## Stop conditions

P0 stops immediately for comparative purposes if any systemic condition prevents defensible accounting, including:
- run identity cannot be preserved;
- resource events cannot be attributed;
- required token/cost telemetry is materially missing without a validated reconstruction path;
- oracle execution cannot be bound to the candidate state;
- retries/escalations cannot be retained;
- duplicate accounting cannot be ruled out;
- solution leakage is detected.

The stop condition is `PILOT_INCONCLUSIVE` or `PILOT_REDESIGN_REQUIRED`, never an inferred treatment ranking.

## P1 expansion rule

Only after P0 measurement reconciliation passes may the pilot expand across the 18 development tasks. Repeated rollout count is intentionally not frozen until P0 exposes operational variance and cost; choosing it now would be unsupported.

## Analysis boundaries

Pilot summaries, if P0 passes, must report correctness, token cost, money, and latency separately and preserve all NO/INCONCLUSIVE incurred resources. No composite score is allowed.

`BLOCK_4C = COMPLETE`
