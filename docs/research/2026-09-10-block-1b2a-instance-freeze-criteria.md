# Block 1B.2a — Instance freeze criteria

Date: 2026-09-10
Status: RESEARCH / CORPUS CONSTRUCTION
Architecture approval: NONE

## Purpose

Define the operational gate that every external holdout instance must pass before it can be frozen into Block 1B.2.

This sub-block does not select executors, define an oracle, run models, inspect gold patches for classification, or approve any `dv` architecture.

## Governing rule

An instance is frozen from information available independently of the solution.

The selection decision must not depend on what the gold patch changed, how many files it changed, hidden tests, post-solution measurements, or model performance on the instance.

## Mandatory freeze record

Every selected instance must have all of the following recorded before the holdout is considered sealed:

1. stable external instance identifier;
2. source benchmark/dataset and source provenance;
3. repository owner/name;
4. immutable pre-solution revision/base commit or equivalent frozen upstream release;
5. task statement or task-visible specification sufficient to state the requested work;
6. primary Block-1 family classification justified from task-visible information;
7. language/runtime where available;
8. reproducible evaluation mechanism or a bounded reconstruction procedure supplied by the source benchmark;
9. contamination/leakage note;
10. explicit statement that gold implementation information was not used to classify/select the instance.

## Admission gate

An instance is admissible only if:

- its pre-solution state is reconstructible;
- its requested behavior/work is externally identifiable without reading the solution patch;
- it maps unambiguously enough to one primary family for stratified analysis;
- its source provides a credible executable/reconstructable evaluation path;
- it is independent of the user's own repositories;
- it does not require irreversible real-world effects;
- no prior treatment result was consulted to decide whether it enters the holdout.

If one of these conditions cannot be established, the instance is not frozen in the first corpus.

## No-leakage classification rule

Permitted during selection/classification:

- instance ID;
- repository;
- base revision/frozen release;
- issue/task statement;
- language/runtime;
- benchmark-provided environment identity;
- public metadata that existed before the solution;
- benchmark category when that category is intrinsic to the task source (for example, explicit feature or refactor benchmarks).

Forbidden during selection/classification:

- gold patch contents;
- gold changed-file count;
- gold line count/patch size;
- hidden test names/results when those reveal solution structure;
- retrospective success/failure of candidate executors;
- benchmark leaderboards for choosing instances that favor one treatment;
- post-solution implementation details unavailable at decision time.

Gold artifacts may later be used only by the evaluation harness/oracle or retrospective analysis after the corpus and protocol are frozen.

## Reproducibility interpretation

For Block 1B, `reproducible` means that a third party can reconstruct the same pre-solution task state and execute the benchmark's validation path from the recorded identifiers and source instructions, subject to explicitly recorded external/tooling blockers.

It does not require that `dv` reimplement the source benchmark harness.

Examples of acceptable mechanisms include:

- SWE-bench-style `base_commit` plus containerized harness/image;
- TestExplora `base_commit` plus its dual buggy/fixed execution workflow;
- a frozen upstream release plus task-specific reproducible grader, as in SWE Refactor Bench.

## Family assignment rule

The primary family must follow the requested work, not incidental contents of the reference solution.

Examples:

- an issue explicitly requesting a new supported operation is `F3 Feature/change`, even if the reference patch also fixes nearby code;
- a task explicitly asking the agent to generate a defect-revealing test is `F4 Test generation`;
- a behavior-preserving migration/refactoring task is `F5 Refactor/review` unless its primary requirement is specifically build/toolchain/repository integration, in which case it may be `F6`;
- a repair is `F1` or `F2` only when the task-visible specification supports that classification; do not infer local/cross-file scope from gold changed files.

For F1 versus F2, task-visible evidence must indicate the expected structural scope. If that cannot be justified before solution inspection, the candidate remains unclassified and is excluded from the first frozen holdout rather than guessed.

## Source-specific notes

### SWE-bench Multilingual

The source exposes a stable `instance_id`, repository, `base_commit`, problem statement, evaluation script/container identity, and test expectations. The evaluation harness can reconstruct and validate the pre-solution revision. Patch and test-patch fields exist in the dataset but are forbidden as selection/classification features for this experiment.

### FEA-Bench

The source provides instance ID, repository, pull number, base commit and environment-setup commit. Because the benchmark is intrinsically curated for feature implementation, membership may support F3 classification; individual task statements should still be reconstructed from the source PR/issue before freezing a concrete instance.

### TestExplora

The source provides instance ID, repository, pull number and base commit. Its construct is explicitly proactive repository-level test generation, with generated tests evaluated for a fail-to-pass distinction between buggy and repaired states. Code/test patches in the public dataset are evaluation provenance and must not be exposed to the future executor or used to cherry-pick the holdout.

### SWE-Refactor / SWE Refactor Bench

Intrinsic benchmark task definitions can support behavior-preserving refactor/migration classification. SWE Refactor Bench additionally provides frozen upstream releases and a reproducible multi-stage grader. Long-horizon whole-repository migrations should be used sparingly because they are not representative of ordinary small maintenance tasks.

## Freeze procedure for Block 1B.2b

For each family, in order:

1. identify more than three candidates from qualified sources;
2. inspect only permitted task-visible metadata;
3. reject ambiguous or non-reconstructible cases;
4. prefer repository diversity and avoid concentration;
5. freeze exactly three admissible instances;
6. record IDs/revisions/source/family before any treatment run;
7. do not replace a frozen task because a later model performs poorly or well on it, except for a demonstrated corpus defect/blocker under a predeclared replacement rule.

## Current disposition

Block 1B.2a: COMPLETE.

The next sub-block is Block 1B.2b: select and freeze the 18 concrete external holdout instances, three per family, under this gate.

No executor/model has been run. No oracle policy has been designed. No router or architecture is approved.
