# P1-W12 bounded PostgreSQL runtime closure

## Outcome

W12 closes the PostgreSQL runtime blocker for D-F2-05. No treatment, model,
API, or holdout execution occurred. The exact frozen base was materialized in
a fresh detached workspace, restored from the W11 cache, and built without
dependency mutation.

## Runtime contract

The frozen repository workflow specifies `postgres:17-alpine`, database
`BomPraTi`, user `postgres`, and port 5432. The local image was already
available with digest
`sha256:18cfe3ef5e6815560c98237d6216d1e5119702fb0f3894c8785dd58b8bbe5d73`
and reported PostgreSQL 17.11. W12 used a dedicated host port, a fresh
database, and an ephemeral password held only in process memory. The container
was removed after evidence capture.

## Setup and verification

The six context migrations were applied successfully using the historical
setup semantics. The focal fixture exited `0` and reported PASS for overlap,
rollback recovery, ledger replay, independent progress, completed no-op, and
concurrent enqueue backstop. The production explicit-claim probe was executed
once in a separate fresh database and exited `0`, reporting PASS for lock
holding, lock release, and pending retry behavior.

An earlier attempt was rejected as evidence because a truncated ephemeral
password caused `28P01`; a second attempt was rejected because it reused a
non-pristine database and caused a deterministic duplicate key. Neither was
classified as product failure. The final fresh-database run is the admissible
evidence.

## D-F2-04 terminal search

The frozen searchleads CI contract installs an unpinned pytest. No repository-
controlled lock, dated package-index snapshot, or recoverable CI run resolved
that version. The existing local pytest 9.1.1 environment is not accepted as
historical reconstruction. D-F2-04 remains
`BLOCKED_NO_REPRODUCIBLE_HISTORICAL_RESOLUTION`, with no further local work
scheduled.

## Corpus impact

D-F2-05 is admitted. The development corpus advances from two to three tasks,
three families, and two repositories: F2, F5, and F6 across bpt2-abp and
metaO. This improves repository, runtime, and verifier diversity but does not
make the comparative corpus ready automatically. `COMPARATIVE_CORPUS_READY`
remains `NO`, `P1_S1_RELEASE` remains `NO`, and the holdout remains sealed.

The raw fixture and probe outputs, runtime provenance, and validation records
are preserved in `pilot-runs/p1-w12-postgres-runtime/`. No solution commit was
applied, no source checkout was changed, and no password was persisted.

## Next step

Close the remaining strong-executor credential blocker and decide whether the
three-task development corpus is sufficient for a smoke-only P1-S1 release.
Do not execute P1-S1 until the promotion gate is satisfied and the run specs
are materialized from the admitted corpus.
