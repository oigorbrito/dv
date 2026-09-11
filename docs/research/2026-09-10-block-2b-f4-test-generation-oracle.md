# Block 2B-F4 — Test-generation / proactive defect-discovery oracle

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

This sub-block defines only the verification semantics for F4 (test generation / proactive defect discovery). It does not define F5-F6, verifier ordering, executor choice, routing, retry/escalation, or verification cost policy.

It inherits the ternary success contract from Block 2A: `VERIFIED_SOLVED_TASK = YES | NO | INCONCLUSIVE`.

## Governing distinction

In F4 the executor's product is primarily a test artifact, not a repair patch. Therefore ordinary test success is not sufficient.

`GENERATED_TEST_RUNS != DEFECT_DISCOVERED`

`TEST_FAILS_ON_BASE != VALID_DEFECT_SIGNAL`

`FAIL_TO_PASS != UNIVERSAL_TEST_QUALITY`

The oracle must establish that the generated test is executable, semantically relevant to the intended behavior, distinguishes the defective state from the repaired/reference state, and is sufficiently stable to support the conclusion.

## Required evidence dimensions

### O1 — Test artifact validity

The generated artifact must be syntactically/structurally admissible for the target repository and must be discovered/executed by the intended test runner.

A file that is never collected, exits before assertions, or fails because of import/setup corruption does not count as defect discovery.

### O2 — Differential defect signal

The central F4 evidence is a controlled differential execution:

- on the frozen defective/base state, the generated test must fail for the intended behavioral reason;
- on the repaired/reference state, the same test must pass under the same relevant harness conditions.

This is the TestExplora-style Fail-to-Pass criterion and is the minimum evidence that the generated test distinguishes buggy from repaired behavior rather than merely failing arbitrarily.

### O3 — Semantic relevance / oracle fidelity

F2P alone does not prove that the test encodes the intended behavior rather than exploiting an incidental difference between two revisions.

The test must be traceable to the task-visible/documentation-derived behavior contract and must not depend on solution-only details unavailable to the executor.

Where the benchmark/source provides documentation-derived intent, that intent is the semantic authority for relevance. Gold patch structure is evaluation-only and cannot be used to retroactively justify the generated assertion.

### O4 — Stability / non-flakiness

The differential result must be sufficiently reproducible to distinguish a real defect signal from nondeterministic behavior.

The exact repetition count is not fixed by this sub-block; it will be determined in the later experimental protocol. However, a candidate that alternates pass/fail under materially identical conditions cannot receive `YES` without a predeclared stability rule being satisfied.

Flaky or timing/environment-sensitive behavior that prevents attribution yields `INCONCLUSIVE` rather than automatic `NO`.

### O5 — Harness validity and integrity

Block 2A V3 applies unchanged and is especially important for generated-test tasks:

- exact defective and repaired/reference revisions are evaluated;
- the same generated test artifact is used on both states except for unavoidable harness normalization declared in advance;
- required commands actually execute;
- test collection/execution is observed;
- environment/bootstrap failures are distinguished from assertion failures;
- raw logs bind to the exact test artifact and repository state;
- executor-visible information excludes gold solution/test material;
- candidate cannot modify benchmark/evaluator machinery to fabricate F2P.

## Ternary decision rule for F4

### YES

`VERIFIED_SOLVED_TASK = YES` only when all required conditions hold:

1. O1: generated test is valid and actually executes;
2. O2: it fails on the defective/base state and passes on the repaired/reference state under a valid controlled comparison;
3. O3: the assertion is semantically tied to the intended/documented behavior rather than an incidental revision difference;
4. O4: required stability/repetition criterion is met;
5. O5: harness validity/integrity is established;
6. no mandatory contradiction remains.

### NO

`VERIFIED_SOLVED_TASK = NO` is appropriate only when valid executed evidence conclusively shows that the generated test does not meet the mandatory F4 contract.

Examples:
- no admissible test artifact is produced;
- the test is not collected or cannot execute because of candidate-authored test errors;
- it passes on the defective state, so it does not expose the latent defect;
- it fails on both defective and repaired/reference states for a candidate-authored semantic/assertion error;
- it passes on both states and therefore does not discriminate the defect;
- the assertion is demonstrably unrelated to the documented/task behavior under the frozen semantic oracle.

### INCONCLUSIVE

Use `INCONCLUSIVE` when the evidence cannot defensibly attribute the observed result to the generated test's defect-discovery capability, including:

- environment/bootstrap failure on one side of the differential run;
- repaired/reference state cannot be reconstructed or executed;
- unexpected nondeterminism/flakiness defeats the stability rule;
- test execution is skipped or collection status is ambiguous;
- the semantic intent itself is insufficient or contradictory;
- differential outcome depends on uncontrolled external state;
- evaluator contamination or oracle leakage is discovered.

## Mapping to the frozen F4 holdout

The frozen F4 instances come from TestExplora and therefore use the benchmark construct itself as the primary task definition: generate tests that reveal a defect through a Fail-to-Pass transition between the buggy/base and repaired versions.

For each frozen F4 instance, the model/router-visible surface must remain restricted to the benchmark's intended pre-solution information: repository state plus allowed documentation/context. Public solution-derived dataset columns such as `pr_patch`, `code_patch`, `test_patch`, changed-function metadata, or equivalent gold information remain evaluation-only.

The generated test is evaluated after generation against both sides of the frozen differential comparison.

## Minimal-verification principle

The minimum defensible F4 evidence package is:

`test executes + controlled F2P + semantic relevance + stability + harness integrity`

This is intentionally stronger than simply checking whether a generated test fails on the base revision.

It also does not automatically require broad repository regression testing, because F4 measures defect-discovery ability rather than acceptance of a repair patch. Broader checks may be added later only when justified by the confirmatory protocol or by protection against evaluator manipulation.

## Evidence basis

TestExplora defines each task so that a generated test should trigger a Fail-to-Pass transition between buggy and repaired versions and uses documentation-derived intent as the oracle while hiding defect-related signals from the model.

This provides strong evidence for O2 and O3 as the core F4 construct.

However, recent work on bug-reproduction tests shows that F2P alone is insufficient as a universal measure of test utility/quality for downstream repair. Therefore `dv` treats F2P as necessary but not sufficient and adds semantic relevance, stability, and harness-integrity requirements.

Research on automatically generated tests also reports that flakiness can be at least as prevalent as in developer-written tests, supporting explicit stability treatment rather than assuming one observed transition is deterministic.

## Anti-leakage and anti-gaming rules

`SOLUTION_DERIVED_ASSERTION != VALID_PROACTIVE_DISCOVERY`

`EVALUATOR_TAMPERING != DEFECT_DISCOVERY`

`ONE_LUCKY_FLAKY_F2P != VERIFIED_TEST`

The executor cannot receive the repaired implementation, gold patch, hidden/reference tests, or solution-derived changed-function metadata unless that information is explicitly part of the benchmark's legitimate pre-solution interface. Any such exposure invalidates the proactive-discovery claim for that run.

## Relationship to prior families

F1-F3 evaluate a candidate code change against an external oracle.

F4 evaluates a candidate *test* by using two controlled program states as part of the oracle. This makes differential execution and test-artifact integrity first-class verification requirements.

## Completion criterion

Block 2B-F4 is complete when F4 has an executor-independent ternary oracle requiring valid test execution, controlled buggy-to-repaired discrimination, semantic relevance, stability, and harness integrity.

Status:

`BLOCK_2B_F4 = COMPLETE`
`BLOCK_2B_F5 = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
