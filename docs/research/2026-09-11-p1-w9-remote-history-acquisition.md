# P1-W9 remote-history verifier-first acquisition

## Outcome

W9 screened 19 solution leads from the newly authorized remote-history source
universe. It produced no additional admission. Two high-value candidates were
materialized at their exact pre-solution parents, but both were blocked before
baseline execution by reproducibility constraints.

```text
NEW_ADMISSIONS = 0
TASK_CORPUS = PARTIAL
COMPARATIVE_CORPUS_READY = NO
ADMITTED_TASKS = 2
ADMITTED_FAMILIES = 2
REPOSITORIES = 1
P1_S1_RELEASE = NO
HOLDOUT = SEALED
```

No treatment, model, smoke run, candidate solution, or holdout content was
executed or accessed.

## Baseline and provenance boundary

The wave started at
`4baf3b5cbcdf579ef51f4afbbf854f2c1b9bc573` on `main`, with equal local and
remote references and a clean worktree. The Harness self-test passed 6/6 with
exit code 0.

For all 19 leads, the first parent was recorded before solution diffs were
consulted. The parent SHA is the only prospective base. The merge lead
`3786591cf847c2301caa3675fd4c3e1752ec4f89` uses its feature parent
`b12049d6d78eb0793ee6a41fda8befc9e945237f`, not the merge mechanics.

The complete lead and parent register is
`pilot-runs/p1-w9-remote-history-acquisition/acquisition-leads.json`.

## Materialized candidates

### D-F2-05 — bpt2 Saved Search claim/recovery

The parent `f3d2cd2d4c0840077451222868ca0d1c0323cdd2` contains a bounded
PostgreSQL claim/recovery fixture, a workflow, and a repository audit describing
the baseline contract. The candidate statement was frozen as an executor-
neutral transaction, rollback, cancellation, and idempotency requirement.

The fresh detached workspace was clean at the exact parent. The frozen build
command exited `1` before compilation because NuGet repository-signature access
to `api.nuget.org` was blocked by socket policy (`NU1301`). The preservation
execution could not proceed because the same restore is a prerequisite. No
solution file was applied.

Classification: `BLOCKED`, `BASE_NOT_REPRODUCIBLE_LOCALLY`.

### D-F2-04 — searchleads evidence-envelope integrity

The parent `2c886f863cf6d5f9473d15e60f2f55f938162876` contains
`tests/test_evidence_envelope_integrity_v3.py`. The task statement and verifier
reference were frozen before any solution-diff inspection. A fresh detached
workspace was clean at the parent.

The focal command and the repository preservation command both exited `1`:
Python 3.13.14 reported `No module named pytest`. An existing `pytest.exe`
launcher was present in a separate Python 3.12 path, but its interpreter was
not available; no arbitrary installation was attempted.

Classification: `BLOCKED`, `BASE_NOT_REPRODUCIBLE_LOCALLY`.

## Cheap-screen rejections

The remaining 17 leads were not materialized. Parent-tree evidence showed that
the required independent verifier was absent, not directly bound to the
historical behavior, coupled to solution/test changes, or dependent on an
unbounded external service. They remain recorded with narrow reasons in
`candidate-freezes.json`; no similar test was substituted and no rejected ID
was reused.

This closes the high-priority remote-history screen under the W9 rule. Further
progress requires either an approved reproducible Python/pytest environment,
an approved NuGet/package-cache environment, or a new remote lead with
independent verifier provenance.

## Corpus and diversity

The corpus remains D-F5-01 and D-F6-01: two tasks, two families, one
repository, Python and Rust, and two verifier types. The cross-repository
leads did not reach admissibility. The corpus therefore remains suitable only
for pipeline/smoke mechanics and not for treatment ranking, executor ranking,
family generalization, or comparative statistical claims.

## Blockers

```text
P1-W1-BLK-002 = OPEN_FOR_S2
P1-W4-BLK-STRONG-CREDENTIAL = OPEN
P1-W1-BLK-003 = OPEN_FOR_S1
P1-W9-D-F2-04 = OPEN
P1-W9-D-F2-05 = OPEN
P1-W1-BLK-004 = CLOSED
P1-W5-D-F1-01 = CLOSED
```

The W9 blocker register preserves the exact before/after state. Holdout access
is `NONE`; P0 artifacts are unchanged.

## Validation

JSON parsing, parent SHA validation, candidate-freeze ordering, ID uniqueness,
evidence-path checks, secret scan, holdout scan, P0 immutability, Harness
self-test, and `git diff --check` are recorded in the W9 evidence directory.
The two materialized candidates produced only environment-blocked evidence;
they are not admitted tasks and do not count as treatment runs.
