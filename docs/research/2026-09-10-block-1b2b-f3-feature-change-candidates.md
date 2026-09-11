# Block 1B.2b — F3 feature/change holdout candidates

Date: 2026-09-10
Status: FINAL_FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

This note advances only F3 (feature / behavior change). It does not open F4 or any later block.

The classification rule remains pre-solution: each instance must be evidently a feature/change from the task-visible problem statement. Gold-patch structure, changed-file count, patch size, hidden tests, or post-solution signals are not admissible selection features.

## Source

SWE-bench task metadata is used as the reproducible source because each selected instance provides a stable `instance_id`, immutable `base_commit`, repository, test-oriented evaluation metadata, and a model-visible problem statement.

## Final frozen F3 instances

### F3-01 — scikit-learn__scikit-learn-12908

- repository: `scikit-learn/scikit-learn`
- base commit: `314686a65d543bd3b36d2af4b34ed23711991a57`
- source: SWE-bench
- split: test
- classification: F3 feature/change
- pre-solution rationale: the problem statement explicitly asks for an option in `OneHotEncoder` to support 1-of-(k-1) encoding / a reference category, and later describes `drop_first` support. The requested behavior is an additive capability rather than repair of an existing documented behavior.
- freeze status: FINAL_FROZEN

### F3-02 — sympy__sympy-16221

- repository: `sympy/sympy`
- base commit: `8fc3b3a96b9f982ed6dc8f626129abee36bcda95`
- source: SWE-bench
- split: test
- classification: F3 feature/change
- pre-solution rationale: the task explicitly states that the Wolfram Mathematica printer does not support matrices and arrays and asks to add that support. This is a bounded capability addition visible directly in the issue text.
- freeze status: FINAL_FROZEN

### F3-03 — django__django-13797

- repository: `django/django`
- base commit: `3071660acfbdf4b5c59457c8e9dc345d5e8894c5`
- source: SWE-bench
- split: test
- classification: F3 feature/change
- pre-solution rationale: the task explicitly proposes adding fixture-compression support to `dumpdata` because `loaddata` already supports compressed fixtures. The requested change is a new command capability, not a defect classification inferred from implementation details.
- freeze status: FINAL_FROZEN

## Diversity note

The three instances come from three distinct repositories and cover three different functional surfaces:

- preprocessing API behavior (`OneHotEncoder`);
- symbolic-code printer capability (Mathematica matrices/arrays);
- framework management-command behavior (`dumpdata` fixture compression).

This reduces repository-specific dominance within F3 while preserving a common task-family construct: explicit feature addition.

## Leakage discipline

No gold patch, changed-file count, patch-size statistic, hidden-test information, or post-solution metadata was used to classify these tasks as F3.

The `base_commit` values were copied from task metadata, not reconstructed from solution commits.

## F3 status

- candidates selected: 3/3
- base commits pinned: 3/3
- final frozen instances: 3/3
- blockers: 0

F3 is complete. Do not proceed to F4 in this note.
