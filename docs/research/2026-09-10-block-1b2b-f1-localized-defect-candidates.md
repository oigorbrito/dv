# Block 1B.2b — F1 localized-defect holdout candidates

Date: 2026-09-10
Status: FINAL FROZEN / RESEARCH ONLY
Architecture approval: NONE

## Scope

This note advances only F1 (localized defect repair). It does not open F2 or any later block.

The selection rule remains pre-solution: classification must be defensible from the public problem statement and stable task metadata. Gold-patch structure is not an admissible classification signal.

## Source

SWE-bench Verified is used as the reservoir because it provides human-validated issue-resolution tasks with a frozen base commit and reproducible test-based evaluation. The model-visible task consists of the problem statement plus repository state; gold solution/test information remains evaluation-only.

## Frozen F1 instances

### F1-01 — sympy__sympy-23824

- repository: `sympy/sympy`
- base commit: `39de9a2698ad4bb90681c0fdb70b30a78233145f`
- source: SWE-bench Verified
- classification: F1 localized defect
- pre-solution rationale: the issue explicitly identifies `physics.hep.kahane_simplify()` and explains a concrete ordering defect in the function's handling of leading uncontracted gamma matrices. It further states that the source of the defect is simple and lies in the insertion loop. This is sufficient to classify the task as localized without inspecting the gold patch.
- freeze status: FINAL_FROZEN

### F1-02 — pytest-dev__pytest-5631

- repository: `pytest-dev/pytest`
- base commit: `cb828ebe70b4fa35cd5f9a7ee024272237eab351`
- source: SWE-bench Verified
- classification: F1 localized defect
- pre-solution rationale: the issue supplies the failing stack trace and identifies the problematic predicate in `num_mock_patch_args`: membership testing `p.new in sentinels` when `p.new` is a NumPy array. The defect is therefore localized by information present in the issue itself, not by solution inspection.
- base-commit provenance: confirmed from `SWE-bench/swe-bench-tasks` task metadata and independently mirrored SWE-bench task metadata. The commit value was obtained from task metadata, not inferred from the gold patch.
- freeze status: FINAL_FROZEN

### F1-03 — matplotlib__matplotlib-24177

- repository: `matplotlib/matplotlib`
- base commit: `493d608e39d32a67173c23a7bbc47d6bfedcef61`
- source: SWE-bench Verified
- classification: F1 localized behavioral defect
- pre-solution rationale: the public issue provides a minimal reproduction around `Axes.hist(..., density=True, histtype="step")` and contrasts it with the working `histtype="bar"` behavior. This bounds the behavioral surface to histogram autoscaling rather than a repository-wide integration failure. The classification does not depend on the gold patch.
- freeze status: FINAL_FROZEN

## Leakage control

No solution patch, changed-file count, patch size, hidden-test result, or post-solution structural signal was used to justify F1 membership.

The `pytest-dev__pytest-5631` base commit was resolved from task metadata only. This distinction matters because immutable starting revision is admissible corpus metadata, while gold solution structure is not an admissible classification feature.

## F1 status

- candidates selected: 3/3
- candidates with pinned base commit: 3/3
- final frozen instances: 3/3
- unresolved blockers: 0

**Block 1B.2b-F1: COMPLETE.**

This closes only the F1 family. F2 remains unopened in this document and must be handled as a separate block.
