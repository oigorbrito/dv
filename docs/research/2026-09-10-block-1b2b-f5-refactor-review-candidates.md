# Block 1B.2b — F5 refactor/review holdout candidates

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

This note advances only F5 (refactor / review-driven correction). It does not open F6 or any later block.

The selection rule remains pre-solution: the review or behavior-preserving constraint must be visible in task metadata supplied independently of the gold implementation. Gold-patch structure is not an admissible classification signal.

## Source

SWE-Gate is used as the preferred reservoir for F5 because it explicitly separates the functional issue from a review-derived acceptance constraint and provides separate functional and constraint test commands plus reproducible Docker contexts.

SWE-Gate is very recent and its instances are synthetic repairs around real review constraints. That limitation is retained as a corpus caveat; the benefit is construct alignment with F5.

## Frozen F5 instances

### F5-01 — instance3::02506978e8943df4_nltk_weighted_choice_bins

- repository: `nltk/nltk`
- base commit: `bd49f9011d7dc8c6a36b3c4ae71f04060c9b3fb9`
- source: SWE-Gate
- issue: weighted-choice lookup is too slow for large candidate vocabularies.
- review constraint: a performance repair must preserve support for large valid populations and must not introduce an artificial cap.
- pre-solution rationale: functional success alone is insufficient; an implementation that accelerates the path by rejecting large populations violates the supplied acceptance constraint. This is therefore review/constraint-driven correction by task construction, independent of the gold patch.
- environment: exported reproducible Docker recipe in SWE-Gate.
- freeze status: FINAL_FROZEN

### F5-02 — instance3::0a3098638e750c33_datasets_deprecated_once

- repository: `huggingface/datasets`
- base commit: `41adfd0f9ee9ba3a6b4f719d5b551c5b19ae45e2`
- source: SWE-Gate
- issue: repeated calls to one deprecated API can emit duplicate `FutureWarning` messages.
- review constraint: warning-dedup tracking must exist before the first invocation; repeated calls to the same deprecated callable must be suppressed while distinct deprecated callables can each emit their own first warning.
- pre-solution rationale: the acceptance constraint places a stricter state-initialization and per-callable semantics requirement over the basic functional goal. Passing only the functional test is not sufficient.
- environment: exported reproducible Docker recipe in SWE-Gate.
- freeze status: FINAL_FROZEN

### F5-03 — instance3::0a3098638e750c33_mlflow_dataset_source_warning_once

- repository: `mlflow/mlflow`
- base commit: `a08c96792fdc4210fc443021eaf9fe0279d74162`
- source: SWE-Gate
- issue: retrying unsupported dataset-source resolution can repeat the same warning.
- review constraint: warning tracking must be ready immediately; the same raw source may warn at most once while different raw sources may each warn once.
- pre-solution rationale: this separates generic deduplication from the review-level semantics of immediate initialization and per-source cardinality. The family classification is therefore visible before the solution.
- environment: exported reproducible Docker recipe in SWE-Gate.
- freeze status: FINAL_FROZEN

## Leakage controls

The following SWE-Gate artifacts are evaluation-only and MUST NOT be supplied to routing/execution policy construction:

- `gold.patch`;
- `mutant.patch` beyond the benchmark-provided starting repository state as reconstructed by the harness;
- `diff_not_follow_constraint.patch`;
- mirror functional/constraint patches;
- validation matrices containing solution-derived outcomes.

The executor may receive the issue plus the explicit review constraint because the constraint is the task requirement being evaluated in F5.

## Important qualifications

1. SWE-Gate is a September 2026 benchmark and is less mature than older SWE-style corpora.
2. The benchmark uses synthetic repository-level repair instances constructed around real review constraints; this is not identical to evaluating an untouched historical PR thread.
3. The recorded `repo_commit` values are those exported by SWE-Gate's reproducible base contexts. For these selected instances the source field is `local_target_repo_head_fallback`; the commits were independently confirmed to exist in their upstream repositories before freezing.
4. This block does not claim that SWE-Gate's review constraints predict maintainer merge decisions. It only uses them as explicit acceptance constraints.

## F5 status

- candidates selected: 3/3
- distinct repositories: 3/3
- base commits pinned: 3/3
- upstream commit existence confirmed: 3/3
- final frozen instances: 3/3
- blockers: none

## Corpus progress

F1: 3/3 frozen
F2: 3/3 frozen
F3: 3/3 frozen
F4: 3/3 frozen
F5: 3/3 frozen
F6: not started

External sealed holdout progress: 15/18.

Do not proceed to Block 2. The next research block is only F6 (configuration/build/integration).
