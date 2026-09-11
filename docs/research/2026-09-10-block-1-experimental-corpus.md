# Block 1 — Experimental corpus

Status: RESEARCH / NOT AN ARCHITECTURE APPROVAL
Date: 2026-09-10

## Purpose

Define the smallest heterogeneous software-engineering corpus capable of falsifying the hypothesis that a new `dv` routing/composition layer is needed.

This block defines only the corpus. It does **not** define verifier policy, measurement accounting, executor choice, routing policy, or acceptance thresholds.

## Governing principle

The corpus must make simple policies fail when task heterogeneity genuinely matters, while avoiding artificial difficulty, benchmark leakage, or a distribution dominated by one kind of work.

A valid corpus must therefore contain multiple task families, multiple repositories, different structural scopes, and a sealed holdout that is not used to derive the routing table.

## Candidate corpus v0

Minimum candidate size: **36 tasks**.

- 18 development/pilot tasks
- 18 sealed holdout tasks
- 6 task families
- 6 tasks per family total
- at least 3 repositories per family where feasible
- no repository may dominate the corpus

The number 36 is a corpus-design starting point, not a claim of statistical sufficiency. Sample-size adequacy is deferred to the confirmatory protocol after pilot variance is observed.

## Task families

### F1 — Localized defect repair

Examples:
- incorrect branch condition;
- wrong boundary value;
- localized parsing/serialization error;
- small API behavior regression.

Desired property: a competent executor should often solve the task with a small working set.

### F2 — Cross-file / integration defect repair

Examples:
- interface/implementation mismatch;
- behavior spanning service + domain + persistence boundary;
- multi-module regression;
- dependency interaction failure.

Desired property: requires aggregation across more than one local context and tests whether cheap/minimal execution knows when expansion is necessary.

### F3 — Feature / behavior change

Examples:
- add a bounded API behavior;
- extend an existing domain rule;
- add a new supported input variant;
- introduce a small capability without redesigning the subsystem.

Desired property: tests implementation from specification rather than pure repair.

### F4 — Test generation / test completion

Examples:
- add missing regression coverage;
- encode an existing behavioral contract in tests;
- strengthen an insufficient test fixture;
- add property/edge-case coverage where appropriate.

Desired property: distinct work class whose best executor/provider may differ from ordinary bug repair.

### F5 — Refactor / code-quality / review-driven correction

Examples:
- remove duplication without semantic change;
- fix a concrete code-review finding;
- improve structure while preserving behavior;
- resolve deterministic style/static-analysis failures that require code changes.

Desired property: separates behavior-preserving engineering from feature/repair work.

### F6 — Configuration / build / dependency / repository integration

Examples:
- repair build configuration;
- correct dependency/version integration;
- fix project wiring or CI-local configuration;
- reconcile executable repository setup with documented expectations.

Desired property: tests non-algorithmic repository work where environment and tooling matter strongly.

## Why these families

Recent software-engineering benchmarks show that bug fixing alone is too narrow. OmniCode explicitly broadens evaluation to bug fixing, test generation, code-review fixing, and style fixing. Repository-level benchmark work also shows that codebase understanding, integration width, reproducible environments, and task quality materially affect agent performance.

The corpus therefore intentionally includes both code-change and repository/integration work instead of treating all software tasks as homogeneous patch generation.

## Source strata

The corpus should be assembled from two strata.

### S1 — External, reproducible benchmark tasks

Use recent repository-level tasks with executable environments and defensible task statements. Prefer long-tail or recently curated repositories when possible to reduce contamination/memorization risk.

Candidate sources include verified or reproducible subsets from current SWE-style benchmark ecosystems. Individual tasks must still pass the inclusion criteria below; benchmark membership alone is not sufficient.

### S2 — Project-representative tasks

Use real or faithfully reconstructed tasks representative of the user's own software-engineering workload, but freeze them as independent instances before execution.

These tasks exist to test ecological validity: a policy that wins on a public benchmark but fails on the actual class of projects `dv` is intended to serve is not sufficient evidence.

Project-representative instances must not expose prior ChatGPT conversation history, previous solution patches, or hidden implementation knowledge to the executor.

## Split discipline

### Development/pilot split

May be used to:
- validate environment setup;
- identify broken/ambiguous instances;
- derive a simple static task-family policy;
- estimate variance for later power/sample-size decisions.

### Sealed holdout split

Must not be used to:
- choose provider per family;
- tune routing thresholds;
- select prompts based on observed outcomes;
- repair the policy after seeing results;
- decide which tasks are retained because they favor a treatment.

The holdout is opened only after the candidate treatments and evaluation protocol are frozen.

## Repository separation

Where corpus size permits, prefer repository-level separation between development and holdout rather than merely splitting issues from the same repositories. This reduces leakage from repository-specific familiarity and cached structural knowledge.

If the same repository must appear in both splits, record that explicitly and treat it as a weaker holdout condition.

## Structural difficulty descriptors

Each instance may be tagged with pre-execution, non-solution descriptors such as:
- language/runtime;
- repository size bucket;
- task family;
- presence of an executable test command;
- presence of build/type/static checks;
- expected external-system dependency;
- whether the task is safely sandboxable;
- whether the issue statement names specific files/components.

Do **not** expose gold-patch statistics such as exact files changed, exact lines changed, or hidden test information to a routing policy. Those may be retained only for retrospective analysis.

## Inclusion criteria

An instance is admissible only if all of the following hold:

1. The task statement is concrete enough to distinguish success from unrelated change.
2. The starting repository revision is frozen.
3. The task can be executed in a reproducible local/containerized environment, or the environmental limitation is explicitly bounded.
4. No gold patch, hidden test, or prior solution is exposed to the executor.
5. The task belongs unambiguously to one primary family for stratified analysis.
6. The task is not trivialized by already containing the completed solution in visible history/artifacts.
7. The task does not require irreversible real-world effects for completion.
8. The task is legal and safe to execute in the research environment.

## Exclusion criteria

Exclude instances that are:
- underspecified to the point that multiple incompatible outcomes are equally valid;
- dependent on unavailable proprietary infrastructure without a reproducible substitute;
- known to leak the gold solution through tests, patches, metadata, or repository history exposed to the agent;
- primarily subjective design/aesthetic work with no defensible acceptance target;
- dominated by external outages or credentials rather than software-engineering capability;
- duplicates or near-duplicates across development and holdout;
- already solved in context supplied to the executor.

## Balance constraints

The initial corpus must avoid these failure modes:

- >25% of tasks from one repository;
- >25% of tasks from one language/runtime if avoidable;
- >1/3 of tasks from a single task family;
- all hard tasks concentrated in one family;
- all project-representative tasks placed only in development or only in holdout.

Exact balancing may be relaxed only when documented as a corpus limitation.

## Contamination controls

For every task, preserve:
- source repository;
- frozen starting revision;
- task source/date;
- whether the repository is widely benchmarked/popular;
- whether the task is newly curated/long-tail;
- evidence that gold patch/tests are not model-visible through the harness.

Recent work on SWE-QA-Pro and SWE-Bench Pro Verified shows that memorization/leakage and flawed task/test construction can materially inflate apparent capability. Corpus integrity is therefore part of experimental validity, not housekeeping.

## Candidate allocation

Initial target allocation:

| Family | Development/Pilot | Sealed Holdout | Total |
|---|---:|---:|---:|
| F1 Localized defect | 3 | 3 | 6 |
| F2 Cross-file defect | 3 | 3 | 6 |
| F3 Feature/change | 3 | 3 | 6 |
| F4 Test generation | 3 | 3 | 6 |
| F5 Refactor/review | 3 | 3 | 6 |
| F6 Config/build/integration | 3 | 3 | 6 |
| **Total** | **18** | **18** | **36** |

This allocation is deliberately symmetric so that early routing conclusions cannot be produced merely by family prevalence.

## What this block does NOT approve

This corpus design does not approve:
- a `dv` router;
- a static table;
- cheap-first execution;
- strong-first execution;
- any model/provider;
- an LLM judge;
- any verifier ladder;
- any workflow engine;
- any adapter implementation.

It only establishes a candidate population on which those hypotheses can later be tested.

## Block 1 completion criterion

Block 1 is complete when:

1. the six families are accepted as the initial scope;
2. 36 admissible instances are selected and frozen;
3. development/pilot and sealed holdout are assigned before treatment outcomes are observed;
4. each instance has source/revision/family/split metadata;
5. corpus limitations and any repository overlap are recorded.

Until then, status remains `CORPUS_DESIGN_ONLY`.
