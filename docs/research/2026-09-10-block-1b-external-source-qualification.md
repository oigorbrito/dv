# Block 1B.1 — External holdout source qualification

Date: 2026-09-10
Status: RESEARCH / SOURCE QUALIFICATION
Architecture approval: NONE

## Purpose

Qualify external task reservoirs for the sealed holdout before selecting concrete instance IDs.

The goal is not to maximize benchmark prestige. The goal is to obtain reproducible, repository-level software-engineering tasks that collectively cover the six task families frozen in Block 1A without leaking gold-patch information into future routing decisions.

## Fixed corpus structure

- 18 development/pilot tasks: may come from known/user repositories.
- 18 sealed holdout tasks: external repositories only.
- Six families, target three holdout instances per family:
  1. localized defect;
  2. cross-file defect;
  3. feature/change;
  4. test generation;
  5. refactor/review;
  6. configuration/build/integration.

## Admission rules for a source

A source is admissible only if it can provide, directly or reproducibly:

- a repository and immutable historical revision/base commit;
- a task/problem statement available independently of the gold implementation;
- an executable or reconstructable environment/harness;
- enough metadata to classify the task family without inspecting the gold patch;
- a reproducible way to restore the pre-solution state;
- external provenance independent of the user's own repositories.

The following are forbidden selection/routing features:

- gold patch contents;
- exact changed-file count from the gold patch;
- exact patch size/line count;
- hidden test names or results;
- any post-solution signal unavailable to an executor at decision time.

## Qualified sources

### SWE-bench Multilingual / SWE-style issue-resolution corpora

Disposition: QUALIFIED RESERVOIR, NOT SUFFICIENT ALONE.

Strengths:

- real repository-level issue-resolution tasks;
- immutable base revisions and historical pre-solution state;
- execution-oriented harness/containerization;
- broad repository/language diversity in the multilingual variant.

Best fit:

- localized defect;
- cross-file defect;
- feature/change;
- some configuration/build/integration instances when the problem statement itself establishes that category.

Limitation:

Issue-resolution corpora are structurally biased toward repair/change tasks and should not be stretched to represent explicit test-generation or pure refactoring simply because the gold patch happens to contain tests/refactors.

### SWE-PolyBench

Disposition: QUALIFIED.

Published characteristics:

- 2,110 repository-level instances from 21 repositories;
- Java, JavaScript, TypeScript and Python;
- bug fixes, feature additions and code refactoring;
- automated evaluation harness;
- repository/task-stratified subset available.

Best fit:

- localized/cross-file defects;
- feature/change;
- refactor.

Selection caveat:

Concrete instances must still be classified from task-visible metadata, not from solution patch statistics.

### SWE-Refactor

Disposition: QUALIFIED, PREFERRED FOR PURE REFACTOR FAMILY.

Published characteristics:

- 1,099 developer-written behavior-preserving refactorings;
- 18 Java projects;
- 922 atomic and 177 compound instances;
- instances validated with compilation, test execution and automated refactoring detection.

Best fit:

- refactor/review family, especially where a behavior-preserving transformation is explicitly the task.

Reason for preference:

This source avoids relabeling incidental edits in generic issue benchmarks as refactoring.

### SWE Refactor Bench

Disposition: QUALIFIED SPECIALIZED RESERVOIR; USE SPARINGLY.

Published characteristics:

- 20 whole-repository migrations;
- four technical-debt categories;
- evaluation separates migration completeness from behavioral correctness.

Best fit:

- high-complexity refactor/migration;
- configuration/build/integration when the task statement explicitly concerns build/toolchain migration.

Limitation:

Tasks are intentionally long-horizon and may be outliers for a small first holdout. They should not dominate the corpus.

### TestExplora

Disposition: QUALIFIED, PREFERRED FOR TEST-GENERATION FAMILY.

Published characteristics:

- repository-level benchmark for proactive bug discovery through generated tests;
- 2,389 test-generation tasks;
- sourced from 1,552 real GitHub pull requests across 482 repositories;
- tasks require generated tests to trigger a fail-to-pass distinction between buggy and repaired revisions;
- Docker-oriented evaluation support.

Best fit:

- explicit test generation.

Reason for preference:

It provides a task whose requested work is actually test creation, rather than using test changes embedded in a bug-fix gold patch as a proxy.

### SWEE-Bench / SetUpAgent-derived corpora

Disposition: QUALIFIED SECONDARY RESERVOIR.

Published characteristics:

- historically accurate dependency setup, test execution and result parsing;
- hundreds of repositories;
- distribution differs materially from classic SWE-bench, including lower issue-description quality and higher fix complexity.

Best fit:

- defect and feature diversity;
- robustness against relying on a small set of highly popular repositories.

### FEA-Bench

Disposition: QUALIFIED, PREFERRED SECONDARY SOURCE FOR FEATURE/CHANGE.

Published characteristics:

- repository-level feature implementation;
- pull requests from 83 GitHub repositories;
- code changes paired with relevant unit-test files.

Best fit:

- feature/change.

### SWE-Gate

Disposition: CANDIDATE / NOT YET REQUIRED FOR FIRST HOLDOUT.

Published characteristics:

- repository-level repair instances built around review constraints;
- separates functional tests from review-constraint tests;
- 303 instances over 75 Python repositories.

Potential fit:

- review-constrained repair.

Caution:

It is very recent (September 2026) and synthesizes repair instances around real review constraints. It is useful prior art for distinguishing functional correctness from acceptance constraints, but is not necessary to populate the first 18 holdout tasks while more established specialized sources are available.

## Family-to-source mapping for Block 1B.2

| Holdout family | Preferred source | Secondary source | Target |
| --- | --- | --- | ---: |
| Localized defect | SWE-bench Multilingual / SWE-PolyBench | SWEE-Bench | 3 |
| Cross-file defect | SWE-bench Multilingual / SWE-PolyBench | SWEE-Bench | 3 |
| Feature/change | FEA-Bench / SWE-PolyBench | SWE-style corpora | 3 |
| Test generation | TestExplora | externally reproducible test-only PR task | 3 |
| Refactor/review | SWE-Refactor | SWE-PolyBench / SWE Refactor Bench | 3 |
| Configuration/build/integration | explicit task-visible cases from SWE-style/PolyBench or SWE Refactor Bench | reproducible external PR | 3 |

## Key methodological conclusion

No single external benchmark should populate all six families.

Forcing one benchmark to cover the entire corpus would trade convenience for construct validity. A mixed-source holdout is preferable provided every selected instance is normalized later to the same task contract and evaluated under a family-appropriate reproducible oracle.

That normalization and oracle definition belong to later blocks and are not performed here.

## Block status

Block 1B.1: COMPLETE.

Block 1B.2 remains open: select and freeze 18 concrete external instance IDs, three per family, while preserving the no-gold-leakage rule.

No model/executor has been run. No oracle has been designed. No architecture is approved.
