# Block 1B.2b — F4 test-generation holdout candidates

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

This note advances only F4 (test generation / proactive defect discovery). It does not open F5, F6, or any later block.

## Source

Primary source: Microsoft TestExplora.

TestExplora is explicitly a repository-level benchmark for proactive bug discovery via generated tests. Its public dataset exposes `instance_id`, `repo`, `pull_number`, and `base_commit`; benchmark success is defined through generated tests that distinguish buggy from repaired behavior via Fail-to-Pass evaluation.

The source dataset currently exposes a single `dev` split. For `dv`, these three instances are assigned to a new sealed external holdout before any treatment is run. The original split label is recorded as a limitation rather than silently reinterpreted as a benchmark-native test split.

## Selection rule

The three instances below were selected only from source identity/repository diversity/base revision metadata. Solution patches were not used as selection criteria. TestExplora's benchmark definition itself establishes F4 membership, so no gold-patch structure is needed to classify them as test-generation tasks.

## Frozen F4 instances

### F4-01 — MichaelGrupp__evo-584

- repository: `MichaelGrupp/evo`
- source instance: `MichaelGrupp__evo-584`
- source PR: `584`
- base commit: `c8018e43c5792858e83bea3efd3a7d8c09873afd`
- source: TestExplora
- source split: `dev`
- dv split: `sealed_holdout`
- family: F4 test generation
- base revision existence: CONFIRMED on origin repository
- freeze status: FINAL_FROZEN

### F4-02 — davidaurelio__hashids-python-4

- repository: `davidaurelio/hashids-python`
- source instance: `davidaurelio__hashids-python-4`
- source PR: `4`
- base commit: `6ba61badeee2915d6e12a9488fedb68887890b5b`
- source: TestExplora
- source split: `dev`
- dv split: `sealed_holdout`
- family: F4 test generation
- base revision existence: CONFIRMED on origin repository
- freeze status: FINAL_FROZEN

### F4-03 — quantumlib__OpenFermion-1086

- repository: `quantumlib/OpenFermion`
- source instance: `quantumlib__OpenFermion-1086`
- source PR: `1086`
- base commit: `e4395e15d6330ea5dd2cab96451eae47a95113b1`
- source: TestExplora
- source split: `dev`
- dv split: `sealed_holdout`
- family: F4 test generation
- base revision existence: CONFIRMED on origin repository
- freeze status: FINAL_FROZEN

## Why these three

They provide three independent repositories with materially different domains while preserving one task construct: generate tests that expose a latent defect. The selection does not optimize for known model performance, known patch size, gold changed-file count, hidden tests, or source-task difficulty.

## Important limitation

TestExplora's public Hugging Face dataset exposes only a `dev` split at the time of selection. These instances are therefore not claimed to be a benchmark-native unseen test set. They become a `dv` sealed holdout because they are frozen before any `dv` treatment or policy is run against them.

This is weaker contamination protection than a newly private task set. It is acceptable for the initial falsification corpus only if the later protocol records public-benchmark contamination risk explicitly and does not claim generalization beyond the observed corpus.

## Leakage discipline

Fields such as `pr_patch`, `code_patch`, `test_patch`, detailed changed-function metadata, and any solution-derived information are evaluation-only and MUST NOT be supplied to the executor or routing policy.

Model-visible information for F4 must be reconstructed later from the benchmark's intended pre-solution task interface (repository state plus allowed documentation/context), not from the public dataset's solution columns.

## F4 status

- candidates selected: 3/3
- base commits pinned: 3/3
- base revisions confirmed on origin: 3/3
- final frozen instances: 3/3
- blockers: 0

F4 is complete for Block 1B.2b.

Do not proceed to F5 in this note.
