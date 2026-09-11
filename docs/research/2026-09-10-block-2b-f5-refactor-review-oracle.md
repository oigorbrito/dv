# Block 2B-F5 — Refactor/review-driven oracle

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

Defines only the executor-independent verification semantics for F5 refactor/review-driven tasks. It inherits Block 2A's ternary YES/NO/INCONCLUSIVE contract.

## Governing distinction

`FUNCTIONAL_PASS != REVIEW_CONSTRAINT_SATISFIED`

`REFACTOR_COMPILES != BEHAVIOR_PRESERVED`

F5 requires both the functional objective and every explicit mandatory review/acceptance constraint.

## Required evidence

### O1 — Functional objective
Executable evidence demonstrates the requested functional/performance/behavioral objective.

### O2 — Explicit review/constraint compliance
Every predeclared mandatory review constraint is independently checked. A candidate that solves O1 by violating O2 is a conclusive NO.

### O3 — Preservation
Relevant behavior outside the intended change remains valid. For refactoring this includes behavior preservation; for constrained corrections it includes adjacent behavior the constraint is intended to protect.

### O4 — Harness integrity
The exact candidate/base/environment are bound; required checks execute; skips/infrastructure failures are separated; evaluator artifacts cannot be altered to fabricate success.

## Decision

YES only if O1 + all mandatory O2 + O3 + O4 pass.
NO if valid evidence shows functional failure, any mandatory constraint violation, or required preservation failure.
INCONCLUSIVE if a mandatory check cannot be validly executed or interpreted.

## Frozen F5 mapping

- NLTK weighted-choice: performance improvement alone is insufficient; large valid populations must remain supported and no artificial cap may be introduced.
- datasets deprecated warning: duplicate warning suppression must obey the explicit initialization and per-callable semantics.
- MLflow dataset-source warning: suppression must obey immediate initialization and per-source cardinality semantics.

The issue and explicit review constraint are solver-visible requirements. Gold/mutant/solution-derived patches and validation matrices remain evaluation-only.

## Minimal verification

`functional objective + every mandatory review constraint + relevant preservation + harness integrity`

No full repository suite is automatically required; expansion policy is deferred.

## Completion

`BLOCK_2B_F5 = COMPLETE`
`BLOCK_2B_F6 = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
