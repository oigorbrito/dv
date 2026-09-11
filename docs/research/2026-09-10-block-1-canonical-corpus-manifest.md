# Block 1 — Canonical corpus manifest v0

Date: 2026-09-10
Status: BLOCK 1 FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Purpose

Freeze the first 36-task corpus before verifier policy, measurement accounting, executor selection, routing treatment, or acceptance thresholds are defined.

The corpus contains 18 development/pilot tasks and 18 sealed external holdout tasks, with three instances per family in each split.

`CORPUS_FROZEN != ARCHITECTURE_APPROVED`

## Split semantics

### Development/pilot

The development tasks are reconstructed from historical work in repositories already familiar to the project. They may be used for environment validation, instrumentation, policy construction, and pilot variance estimation. They MUST NOT be treated as evidence of external generalization.

Because these repositories and historical changes may be present in prior agent/model context, contamination/familiarity risk is HIGH. This is intentional for the development split and is one reason these tasks are excluded from the sealed holdout.

For each reconstructed task, the PR base SHA is the starting revision. The task must later be materialized from the pre-solution issue/PR requirement while withholding the solution diff/head from the executor.

### Sealed external holdout

The external tasks were frozen in the F1–F6 selection notes before any dv treatment is executed. Gold patches, hidden tests, solution-derived file counts, and treatment outcomes are not admissible routing/execution inputs.

Public-benchmark contamination remains a limitation; sealed means sealed with respect to this dv experiment, not private or guaranteed absent from model training.

## Development/pilot — 18 tasks

| ID | Family | Repository / source task | Base revision | Pre-solution task construct |
|---|---|---|---|---|
| D-F1-01 | F1 localized defect | `oigorbrito/RJ` PR #21 | `c627a1bcdc87ff9b0bbd5ccc0b7d108daa5e324d` | conservative deterministic process-text normalization defect/slice |
| D-F1-02 | F1 localized defect | `oigorbrito/metaO` PR #419 | `e5e50c848079664e176592c7b231a88269737572` | reject coercive numeric mission JSON values |
| D-F1-03 | F1 localized defect | `oigorbrito/metaO` PR #415 | `520204257dc8318b31bda9c34d7173b41bd71200` | validate certificate freshness flag pair before store side effects |
| D-F2-01 | F2 cross-component defect | `oigorbrito/metaO` PR #413 | `5c3bcdfb0c8aec778727a756f484a4b67a23601d` | mission parsing/validation must precede persistence and factory bootstrap |
| D-F2-02 | F2 cross-component defect | `oigorbrito/smag` PR #144 | `d538bf522c3dbc0717632fc901056b221de8fda4` | supervised session bootstrap/readiness/executor/acceptance lifecycle |
| D-F2-03 | F2 cross-component defect | `oigorbrito/smag` PR #121 | `9ec55ba71a35bd333b57f39acb5378c71f11380e` | Git staging, dirty state, ignored trees, rollback and Windows execution interaction |
| D-F3-01 | F3 feature/change | `oigorbrito/smag` PR #118 | `76ef9277062085e113c14bf1fdbb9c4bd218045b` | add foreground operator session/REPL while preserving governance path |
| D-F3-02 | F3 feature/change | `oigorbrito/metaO` PR #291 | `9d35699eb9f9e85e13a7c59b7acbf391dfb4c685` | add obligation-based ProjectCompletionGate |
| D-F3-03 | F3 feature/change | `oigorbrito/metaO` PR #339 | `471f1aaad5cef7562dca6f1b94ae434865ea210f` | add deterministic Project Discovery readiness coordinator |
| D-F4-01 | F4 test generation | `oigorbrito/metaO` PR #297 | `9d35699eb9f9e85e13a7c59b7acbf391dfb4c685` | create deterministic marketplace Discovery acceptance fixture/tests |
| D-F4-02 | F4 test generation | `oigorbrito/metaO` PR #301 | `9d35699eb9f9e85e13a7c59b7acbf391dfb4c685` | add property-based AcceptanceBudget harness |
| D-F4-03 | F4 test generation | `oigorbrito/metaO` PR #341 | `471f1aaad5cef7562dca6f1b94ae434865ea210f` | add boundary regression tests for non-finite/overflow AcceptanceBudget cases |
| D-F5-01 | F5 refactor/review | `oigorbrito/metaO` PR #401 | `9cc5d6d722d509175a669624c9235156dffb4f85` | canonicalize factory loading and preflight ordering without redesign |
| D-F5-02 | F5 refactor/review | `oigorbrito/metaO` PR #411 | `88525508b4da960057e4e59a78198b4c1a522601` | isolate runtime command store wiring while preserving semantics |
| D-F5-03 | F5 refactor/review | `oigorbrito/metaO` PR #247 | `18b5d90ac7bba05d8342b73b69b3b3226b32fd65` | retire Python product/runtime oracle after Rust migration while preserving reference evidence |
| D-F6-01 | F6 config/build/integration | `oigorbrito/metaO` PR #451 | `5d00cd284ce8fe810b0f5192c56d98608be516d4` | harden Rust test harness for parallel temp stores and external `CARGO_TARGET_DIR` |
| D-F6-02 | F6 config/build/integration | `oigorbrito/smag` PR #115 | `53e6fa2617d446717b81032d4b4d2cf1cc079d30` | deterministic npm/npx package bin aliases and distribution gates |
| D-F6-03 | F6 config/build/integration | `oigorbrito/smag` PR #132 | `e73186540fd4e740d413dc7090d816def0dec8cc` | preserve source Git origin through staged workspace cloning |

## Sealed external holdout — 18 tasks

| ID | Family | Instance | Repository | Base revision | Source |
|---|---|---|---|---|---|
| H-F1-01 | F1 | `sympy__sympy-23824` | `sympy/sympy` | `39de9a2698ad4bb90681c0fdb70b30a78233145f` | SWE-bench Verified |
| H-F1-02 | F1 | `pytest-dev__pytest-5631` | `pytest-dev/pytest` | `cb828ebe70b4fa35cd5f9a7ee024272237eab351` | SWE-bench Verified |
| H-F1-03 | F1 | `matplotlib__matplotlib-24177` | `matplotlib/matplotlib` | `493d608e39d32a67173c23a7bbc47d6bfedcef61` | SWE-bench Verified |
| H-F2-01 | F2 | `django__django-14053` | `django/django` | `179ee13eb37348cd87169a198aec18fedccc8668` | SWE-bench |
| H-F2-02 | F2 | `django__django-10939` | `django/django` | `1933e56eca1ad17de7dd133bfb7cbee9858a75a3` | SWE-bench |
| H-F2-03 | F2 | `scikit-learn__scikit-learn-25500` | `scikit-learn/scikit-learn` | `4db04923a754b6a2defa1b172f55d492b85d165e` | SWE-bench |
| H-F3-01 | F3 | `scikit-learn__scikit-learn-12908` | `scikit-learn/scikit-learn` | `314686a65d543bd3b36d2af4b34ed23711991a57` | SWE-bench |
| H-F3-02 | F3 | `sympy__sympy-16221` | `sympy/sympy` | `8fc3b3a96b9f982ed6dc8f626129abee36bcda95` | SWE-bench |
| H-F3-03 | F3 | `django__django-13797` | `django/django` | `3071660acfbdf4b5c59457c8e9dc345d5e8894c5` | SWE-bench |
| H-F4-01 | F4 | `MichaelGrupp__evo-584` | `MichaelGrupp/evo` | `c8018e43c5792858e83bea3efd3a7d8c09873afd` | TestExplora |
| H-F4-02 | F4 | `davidaurelio__hashids-python-4` | `davidaurelio/hashids-python` | `6ba61badeee2915d6e12a9488fedb68887890b5b` | TestExplora |
| H-F4-03 | F4 | `quantumlib__OpenFermion-1086` | `quantumlib/OpenFermion` | `e4395e15d6330ea5dd2cab96451eae47a95113b1` | TestExplora |
| H-F5-01 | F5 | `instance3::02506978e8943df4_nltk_weighted_choice_bins` | `nltk/nltk` | `bd49f9011d7dc8c6a36b3c4ae71f04060c9b3fb9` | SWE-Gate |
| H-F5-02 | F5 | `instance3::0a3098638e750c33_datasets_deprecated_once` | `huggingface/datasets` | `41adfd0f9ee9ba3a6b4f719d5b551c5b19ae45e2` | SWE-Gate |
| H-F5-03 | F5 | `instance3::0a3098638e750c33_mlflow_dataset_source_warning_once` | `mlflow/mlflow` | `a08c96792fdc4210fc443021eaf9fe0279d74162` | SWE-Gate |
| H-F6-01 | F6 | `django__django-12009` | `django/django` | `82a88d2f48e13ef5d472741d5ed1c183230cfe4c` | SWE-bench |
| H-F6-02 | F6 | `pytest-dev__pytest-9681` | `pytest-dev/pytest` | `fc72ffa39ed3b34b21fba83d6f80144ab0ae8a36` | SWE-bench |
| H-F6-03 | F6 | `pytest-dev__pytest-9780` | `pytest-dev/pytest` | `d52a6e6074844581f5f89653bd4071fb6ea847d3` | SWE-bench |

## Balance and overlap audit

- total tasks: 36
- development/pilot: 18
- sealed external holdout: 18
- each family: 6 total = 3 development + 3 holdout
- no exact repository overlaps between the development repositories (`oigorbrito/*`) and external holdout repositories
- external holdout contains repeated repositories, but no repository exceeds 4/36 of the total corpus
- language/runtime balance is imperfect: Python-heavy external benchmark sources and Rust/TypeScript-heavy project tasks are an explicit limitation
- F4 holdout uses public TestExplora `dev` instances re-sealed by dv; this is weaker than a benchmark-native private test split
- F5 holdout uses recent synthetic repairs around real review constraints; this measures explicit constraint compliance, not maintainer merge probability
- development tasks have high prior-context/familiarity risk and MUST NOT be used as generalization evidence

## Freeze rules after this commit

After this manifest is committed:

1. No task may be replaced because a treatment performs poorly on it.
2. No family may be relabeled using gold-patch structure or observed treatment behavior.
3. Any broken/unexecutable instance must remain in the audit trail with an explicit `CORPUS_DEFECT` disposition; replacement requires a versioned corpus revision and cannot silently modify v0.
4. Holdout outcomes cannot be used to tune the policy being evaluated on this holdout.
5. The executor/router must not receive gold patches, hidden tests, solution heads, prior conversation solution history, or solution-derived structural statistics.
6. Development historical PR heads/diffs are ground truth/evaluation material only; task reconstruction must expose the base revision plus requirement, not the completed solution.

## Block 1 completion decision

The six families are frozen, 36 instances are assigned before treatment execution, every instance has source/base/family/split identity, and known limitations are recorded.

`BLOCK_1 = COMPLETE`
`CORPUS_VERSION = v0`
`TREATMENT_OUTCOMES_OBSERVED = NO`
`ARCHITECTURE_APPROVAL = NONE`

Block 2 may begin only as a separate research block defining oracle/verification semantics. This manifest does not pre-approve any verifier, model, router, policy, adapter, runtime, or workflow.