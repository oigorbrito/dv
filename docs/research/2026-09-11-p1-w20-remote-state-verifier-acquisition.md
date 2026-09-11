# P1-W20 — Remote-state discipline and verifier-first acquisition

## Closure

W20 produced no new P1 admission. The wave applied the parent-side failure gate
and reviewed only justified, locally available acquisition opportunities. The
result is not treatment evidence, executor evidence, or a comparative result.

The carried scientific state remains `TASK_CORPUS = PARTIAL`,
`COMPARATIVE_CORPUS_READY = NO`, `P1_S1_RELEASE = NO`, and
`HOLDOUT = SEALED`.

## Remote state

The W20 baseline named `1e2fe31...`, but the actual local HEAD includes the W19
acquisition commit and the subsequent harness policy commit:

```text
HEAD       = 412d1d5a0ceb76815e1231467300ceb244ed517b
origin/main = 13cec2bbdf2bb2b68030b288c571fea877affa34
REMOTE_ONLY = 0
LOCAL_ONLY  = 2
WORKTREE    = CLEAN
```

This mismatch was recorded rather than repaired destructively. W20 did not
perform remote reconciliation because acquisition and remote publication are
separate operations. The objective unblock condition is a later explicit,
non-force fast-forward publication with a clean worktree.

## Acquisition boundary

The closed development inventory contains 18 candidates. W14, W16, and W17
closed their respective leads without a new admissible task. W18 supplied one
new source lead, `METAO-GATE-N1`, but its parent focal verifier passed `12/12`.
The frozen rule therefore applies:

```text
PARENT_FOCAL = PASS
=> REJECT
=> SOLUTION_DIFF = NOT_INSPECTED
=> CANDIDATE_EXECUTION = NOT_TESTED
```

Local sources that were enumerated but lacked an unclosed, verifier-first lead
were not promoted by inference. No solution diff was opened, no candidate was
materialized, and no historical lead was reopened.

## Evidence-gated policy

The evidence-gated harness policy was applied to W20 changes. The committed
records exist only to preserve the remote-state fact, the parent-gate decision,
the acquisition inventory, and validation evidence. No suggestion was emitted
merely because an additional document, dashboard, architecture description, or
refactor might be desirable.

The supporting chain is explicit:

```text
observed parent pass / remote divergence
-> oracle validity, failure attribution, reproducibility, traceability
-> smallest sufficient evidence records
-> Harness and static validation
```

The policy guard itself remains available through
`python -B tools/dv_pilot_harness.py policy-check --suggestion <file>`.

## Validation and blockers

- Harness self-test: `9/9 PASS`, exit `0`.
- New candidates: `0`.
- Parent-failure gate: `PASS` for the W18 rejection.
- Solution leakage: `PASS`; no new solution diff opened.
- Treatment/model/API execution: `NOT_EXECUTED`.
- Holdout: `SEALED`.
- Secret values: not recorded.
- P0 artifacts: unchanged.

Open blockers remain:

- `P1-W1-BLK-002`: comparative corpus insufficient;
- `P1-W4-BLK-STRONG-CREDENTIAL`: authorized C1 credential unavailable;
- `P1-W16-SMAG-PRESERVATION-NETWORK`: broad preservation depends on external
  GitHub/network behavior;
- local remote-state divergence: two local commits are not yet on `origin/main`.

The nearest experimental gap is a new candidate with an independent,
reproducible parent-side verifier that demonstrates a valid product failure and
has executable preservation evidence. No further work is justified from the
currently closed local inventory without new evidence or an explicit remote
reconciliation event.
