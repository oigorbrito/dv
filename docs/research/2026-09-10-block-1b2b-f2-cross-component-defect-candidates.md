# Block 1B.2b — F2 cross-component / integration-defect holdout candidates

Date: 2026-09-10
Status: FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

This note advances only F2 (cross-component / integration defect repair). It does not open F3 or any later block.

The classification rule remains pre-solution. A task qualifies for F2 only when its public problem statement itself establishes that the failure arises from interaction among distinct components, subsystems, configuration modes, or integration surfaces. Gold-patch file count, patch size, changed paths, and hidden tests are not admissible classification signals.

F2 does not mean "the gold patch happened to touch multiple files". It means the task presented to the executor is intrinsically cross-component/integration-shaped from information available before the solution.

## Frozen F2 instances

### F2-01 — django__django-14053

- repository: `django/django`
- base commit: `179ee13eb37348cd87169a198aec18fedccc8668`
- source: SWE-bench task corpus; split `test`; also listed in SWE-bench Verified
- classification: F2 cross-component/integration defect
- pre-solution rationale: the issue explicitly describes interaction between `HashedFilesMixin.post_process()`, `collectstatic.collect()`, storage subclasses such as `ManifestStaticFilesStorage`, and downstream integrations such as WhiteNoise/S3 backends. The defect is expressed as duplicate lower-level yields leaking across these component boundaries and causing incorrect statistics and duplicate downstream work. This classification is justified by the issue text alone.
- freeze status: FINAL_FROZEN

### F2-02 — django__django-10939

- repository: `django/django`
- base commit: `1933e56eca1ad17de7dd133bfb7cbee9858a75a3`
- source: SWE-bench task corpus; split `test`
- classification: F2 cross-component/integration defect
- pre-solution rationale: the issue states that the failure appears only when a `ModelAdmin` combines a custom-widget inline, media JavaScript, and `filter_horizontal`, producing `MediaOrderConflictWarning` and loading `inlines.js` before jQuery. The failing behavior is therefore explicitly an interaction among admin media/widget/inline surfaces, not an isolated function defect.
- freeze status: FINAL_FROZEN

### F2-03 — scikit-learn__scikit-learn-25500

- repository: `scikit-learn/scikit-learn`
- base commit: `4db04923a754b6a2defa1b172f55d492b85d165e`
- source: SWE-bench task corpus; split `test`; SWE-bench Lite member
- classification: F2 cross-component/configuration integration defect
- pre-solution rationale: the public issue explicitly requires the interaction of global `set_config(transform_output="pandas")`, `CalibratedClassifierCV`, isotonic regression, dataframe output, and `_CalibratedClassifier.predict_proba()`. The crash occurs at the boundary where a dataframe-shaped result is assigned into a NumPy probability vector. The integration character is therefore visible before solution inspection.
- freeze status: FINAL_FROZEN

## Rejected candidate during selection

`pydicom__pydicom-997` was considered because its issue spans encapsulated pixel-data generation and decoder behavior. It was not selected for this holdout family because the canonical task metadata marks it as split `dev`, while the selected F2 instances are held-out `test` tasks. This rejection was made from task metadata, not solution information.

## Leakage controls

The selection did not inspect or use:

- gold patch structure;
- number of changed files;
- solution patch size;
- hidden-test content;
- treatment/model results.

The public problem statements and `task.yaml` metadata were sufficient to justify classification and pin immutable base revisions.

## F2 status

- candidates selected: 3/3
- candidates with pinned base commit: 3/3
- final frozen instances: 3/3
- blockers: 0

F2 is complete. Do not reinterpret these tasks using post-solution information later; any classification revision must be justified from admissible pre-solution evidence and recorded explicitly.
