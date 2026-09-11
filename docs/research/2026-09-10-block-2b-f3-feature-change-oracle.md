# Block 2B-F3 — Feature/change oracle

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

This sub-block defines only the verification semantics for F3 (feature / behavior change). It does not define F4-F6, verifier ordering, routing, executor choice, retry/escalation policy, or verification cost thresholds.

It inherits the ternary success contract from Block 2A: `VERIFIED_SOLVED_TASK = YES | NO | INCONCLUSIVE`.

## Governing distinction

A feature task is not verified merely because one newly introduced example works.

`DEMO_WORKS != FEATURE_CONTRACT_SATISFIED`

and

`NEW_PATH_PASS != BACKWARD_COMPATIBILITY_PRESERVED`

For F3 the oracle must establish both the requested new behavior and preservation of relevant pre-existing behavior/API semantics.

## Required evidence dimensions

### O1 — Requested-capability evidence

There must be executable evidence that the requested feature/change is actually available at the intended public or task-visible surface.

The evidence must exercise the requested behavior, not an implementation detail that merely correlates with it.

Examples:
- an acceptance/regression test invoking the new option or mode;
- deterministic output/property checks for newly supported input;
- a command-level scenario exercising the new command behavior.

### O2 — Requirement-boundary evidence

Where the public task specifies multiple cases, modes, parameters, formats, or edge conditions, the predeclared oracle must cover the material requirement boundaries rather than accepting one happy-path example as the whole feature.

This does not require exhaustive state-space testing. It requires enough predeclared executable evidence to represent the explicit task contract.

If the task statement is underspecified and no defensible executable boundary can be constructed, the outcome is `INCONCLUSIVE` rather than silently narrowing the requirement after observing a candidate.

### O3 — Compatibility / preservation evidence

Relevant pre-existing behavior that should remain valid must continue to pass.

This can include:
- old/default API behavior;
- previous input modes or formats;
- compatibility expectations directly adjacent to the changed surface;
- existing focused tests selected before treatment results are observed.

For additive features, the old/default path is normally mandatory preservation evidence unless the task explicitly changes or deprecates it.

### O4 — Harness validity and integrity

Block 2A's V3 requirements apply unchanged:
- intended base/candidate state is evaluated;
- required commands/tests actually execute;
- expected tests are discovered rather than silently skipped;
- infrastructure/bootstrap failure is distinguished from candidate failure;
- logs/results bind to the exact candidate;
- candidate cannot alter the oracle/test harness in a way that fabricates success.

## Ternary decision rule for F3

### YES

`VERIFIED_SOLVED_TASK = YES` only when:
1. O1 conclusively demonstrates the requested capability;
2. O2 covers all predeclared material requirement boundaries and passes;
3. O3 required compatibility/preservation evidence passes;
4. O4 establishes a valid and intact harness;
5. no mandatory requirement reports a valid failure;
6. no unresolved contradiction remains.

### NO

`VERIFIED_SOLVED_TASK = NO` when valid executed evidence conclusively shows at least one mandatory feature requirement or preservation requirement is unsatisfied.

Examples:
- requested new mode is unavailable;
- one explicit required case fails;
- new feature works but breaks the default/legacy path;
- command accepts the option but produces behavior inconsistent with the task contract.

### INCONCLUSIVE

Use `INCONCLUSIVE` when evidence cannot defensibly distinguish success from evaluation insufficiency, including:
- required scenario never executed;
- task requirement is too ambiguous to construct a defensible oracle without post-hoc interpretation;
- unexpected skip or harness failure affects a mandatory check;
- environment drift invalidates the comparison;
- conflicting mandatory evidence lacks predeclared precedence.

## Mapping to the frozen F3 holdout

The three frozen F3 instances illustrate different oracle shapes without changing the common contract.

### F3-01 — scikit-learn OneHotEncoder reference/drop behavior

O1 must exercise the requested encoding capability at the public encoder surface. O2 must cover the material requested option semantics, not merely object construction. O3 must preserve relevant pre-existing/default OneHotEncoder behavior.

### F3-02 — SymPy Mathematica matrix/array printing

O1 must exercise matrix/array printing and verify the intended externally visible representation. O2 must cover the task-declared supported structure(s) represented by the frozen oracle. O3 must preserve relevant existing Mathematica-printer behavior for previously supported expressions.

### F3-03 — Django dumpdata compression

O1 must execute `dumpdata` through the requested compression path and verify the produced artifact/behavior. O2 must cover the predeclared supported compression semantics required by the task. O3 must preserve relevant uncompressed/default dumpdata behavior and any directly adjacent compatibility requirement selected before treatment observation.

These descriptions define semantic requirements only; exact commands/tests remain task-instance oracle material and must be frozen before confirmatory treatment results.

## Minimal-verification principle

F3 does not automatically require the entire repository test suite.

The minimum defensible F3 evidence package is:

`requested capability + material requirement boundaries + relevant compatibility + harness integrity`

Broader verification may later be economically justified by risk or uncertainty, but that policy is outside this sub-block.

## Anti-overfitting rule

The oracle must not be narrowed after seeing a candidate so that the candidate passes.

Likewise, new mandatory cases must not be added after seeing treatment results unless the task is formally marked as an oracle/corpus defect and versioned accordingly.

`POST_HOC_ORACLE_EDIT != VALID_CONFIRMATORY_EVIDENCE`

## Relationship to F1/F2

F1 primarily proves that a known defect disappears while preserving relevant local behavior.

F2 proves that a failing interaction/boundary is restored while preserving the participating components.

F3 proves that a requested new/changed capability exists across its material requirement boundary while preserving behavior that the change was not supposed to invalidate.

The shared V1/V2/V3 semantics remain; the family oracle specifies what those dimensions mean for feature/change tasks.

## Completion criterion

Block 2B-F3 is complete when F3 has an executor-independent, predeclarable ternary oracle requiring capability evidence, material requirement-boundary evidence, compatibility preservation, and harness validity.

Status:

`BLOCK_2B_F3 = COMPLETE`
`BLOCK_2B_F4 = NOT_STARTED`
`ARCHITECTURE_APPROVAL = NONE`
