# Block 2A — Verifiable success contract

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

This sub-block defines only the contract for classifying a software-engineering task outcome as `VERIFIED_SOLVED_TASK = YES | NO | INCONCLUSIVE`.

It does not yet choose per-family oracle implementations, verifier order, executor, router, model, retry policy, escalation policy, or cost thresholds.

## Governing principle

Executor completion, patch production, exit code 0, a green focused test, or model self-report are not sufficient to establish a verified solved task.

The verification decision must be independent of the executor and must distinguish three logically different questions:

1. Did the candidate change satisfy the task-specific required behavior?
2. Did it preserve required pre-existing behavior / avoid material regressions?
3. Was the evaluation harness itself valid and sufficiently executed to support the conclusion?

Therefore:

`EXECUTOR_SUCCESS != VERIFIED_TASK_SUCCESS`

and

`FOCUSED_TEST_PASS != VERIFIED_TASK_SUCCESS`

## Evidence dimensions

### V1 — Task satisfaction evidence

Evidence that the requested behavior/change is achieved.

Examples, depending on task family:
- fail-to-pass regression tests;
- explicit acceptance tests;
- executable scenario reproductions;
- deterministic output/property checks;
- review/constraint tests;
- packaging/install/CI behavior probes.

V1 must be bound to the exact task instance and evaluated candidate state.

### V2 — Regression-preservation evidence

Evidence that relevant behavior which should remain valid has not been materially broken.

Possible evidence:
- pass-to-pass tests;
- broader existing test suite;
- build/type/static checks;
- compatibility/invariant checks;
- explicitly selected regression set justified before treatment results are observed.

A narrow success probe cannot silently stand in for V2.

### V3 — Harness-validity evidence

Evidence that the evaluation mechanism itself reached the intended executable boundary and produced interpretable results.

Examples:
- patch/state applied to the intended base revision;
- environment built successfully;
- required commands actually executed;
- expected tests were discovered/executed rather than silently skipped;
- timeout/infrastructure/bootstrap failures distinguished from product failures;
- logs/results bound to the exact candidate revision/state.

A harness failure must not be converted into product failure, and missing harness evidence must not be converted into success.

## Ternary decision contract

### VERIFIED_SOLVED_TASK = YES

Allowed only when all required dimensions are satisfied:

- V1: required task behavior conclusively passes;
- V2: required regression-preservation evidence passes;
- V3: harness validity is established;
- no mandatory oracle/constraint reports failure;
- no unresolved evidence contradiction exists.

For tasks where a dimension is genuinely not applicable, `N/A` must be justified by the task's predeclared oracle specification; it cannot be inferred after seeing results.

### VERIFIED_SOLVED_TASK = NO

Used only when valid executed evidence conclusively shows that a mandatory requirement is not satisfied.

Examples:
- task-specific acceptance test fails under a valid harness;
- required regression test fails because of the candidate change;
- explicit review constraint is violated;
- required build/package/install behavior fails under a valid reproducible environment.

`NO` requires a valid observation of failure, not absence of evidence.

### VERIFIED_SOLVED_TASK = INCONCLUSIVE

Used when the available evidence cannot defensibly establish either YES or NO.

Examples:
- harness/bootstrap/infrastructure failure before the relevant test executes;
- required verifier/test unavailable;
- unexpected skips or incomplete discovery make the regression result ambiguous;
- contradictory verifier outputs with no predeclared precedence rule;
- timeout without enough evidence to attribute failure to the candidate;
- environment drift invalidates the intended comparison;
- task oracle itself is discovered to be defective or insufficient.

`INCONCLUSIVE` is a first-class research outcome and must never be coerced to PASS or FAIL merely to simplify statistics.

## Decision skeleton

```text
candidate state
    |
    v
HARNESS VALID? (V3)
    |
    +-- no / unknown --> INCONCLUSIVE
    |
    +-- yes
          |
          v
TASK REQUIREMENTS PASS? (V1)
          |
          +-- conclusive fail --> NO
          |
          +-- pass
                |
                v
REQUIRED REGRESSION/CONSTRAINT EVIDENCE PASS? (V2)
                |
                +-- conclusive fail --> NO
                |
                +-- missing/ambiguous --> INCONCLUSIVE
                |
                +-- pass --> YES
```

## Independence rule

The verification authority must be logically distinct from executor self-declaration.

An executor may generate tests, diagnostics, or proposed evidence, but those artifacts become verification evidence only when evaluated by a separately defined oracle/verifier path.

`AGENT_SAYS_DONE != VERIFIED_SOLVED_TASK`

## Evidence binding

Each verification record must eventually be bindable to at least:

- corpus version;
- task instance ID;
- frozen base revision;
- candidate/treatment ID;
- candidate output/revision identity;
- verifier/oracle version;
- environment/harness version;
- command/test identity;
- result status;
- raw log/evidence reference;
- execution timestamp or run identity where relevant.

Exact storage/schema design is deferred; this block defines required semantics only.

## Benchmark evidence motivating this contract

SWE-bench's current grading logic treats an instance as fully resolved when all `FAIL_TO_PASS` and all `PASS_TO_PASS` checks pass. This is a useful baseline but not sufficient as a universal `dv` oracle.

Public SWE-bench issue reports document cases where candidate patches passed the selected F2P/P2P evaluation yet failed unchanged developer tests, demonstrating that a narrow selected regression set can overestimate correctness.

Other reported cases show false negatives when PASS_TO_PASS tests are skipped because of evaluation-environment CPU constraints, demonstrating that harness validity and test execution status must be distinguished from product behavior.

SWE-bench's own dataset guidance also explicitly treats the gold patch/test patch as evaluation data that should not be exposed to the solver.

Therefore `dv` adopts three separated evidence dimensions rather than equating one benchmark-specific resolved flag with universal verified task success.

## Non-goals of Block 2A

This block does not yet define:
- the exact oracle for F1-F6;
- full-suite vs targeted-test policy;
- deterministic vs learned verifier precedence;
- LLM judges;
- verifier escalation;
- retry behavior after verifier failure;
- statistical aggregation across repeated runs;
- cost accounting for verification;
- corpus-defect replacement procedure beyond the existing corpus-version rule.

## Completion criterion

Block 2A is complete when the project has a frozen executor-independent ternary success contract distinguishing task satisfaction, regression preservation, and harness validity.

Status after this document:

`BLOCK_2A = COMPLETE`
`BLOCK_2B = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
