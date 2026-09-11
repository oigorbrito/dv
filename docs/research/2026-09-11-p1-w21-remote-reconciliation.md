# P1-W21 — Remote reconciliation and verifier-first acquisition

## Closure

W21 reconciled the unpublished local history and performed no new treatment or
model execution. The verifier-first acquisition gate was maintained; no new
candidate was admitted.

## Remote reconciliation

The starting state was clean `main` with three local commits ahead of
`origin/main`:

```text
LOCAL HEAD  = 1b9e96821a949e2a0e586a5f327b7e1fc53c24ed
ORIGIN MAIN = 13cec2bbdf2bb2b68030b288c571fea877affa34
REMOTE_ONLY = 0
LOCAL_ONLY  = 3
```

The ancestor check passed. A normal non-force `git push origin main` completed
with exit code `0`, followed by `git fetch origin --prune`. The final state is:

```text
HEAD        = 1b9e96821a949e2a0e586a5f327b7e1fc53c24ed
origin/main = 1b9e96821a949e2a0e586a5f327b7e1fc53c24ed
REMOTE_ONLY = 0
LOCAL_ONLY  = 0
WORKTREE    = CLEAN
```

The remote result is operational provenance only. It does not change any
scientific result or treatment status.

## Verifier-first acquisition

The closed inventory remains 18 candidates and the admitted tasks remain
`D-F2-05`, `D-F5-01`, and `D-F6-01`. No previously rejected lead was reopened.
No new lead had enough independent parent-side evidence to justify solution
inspection. Consequently:

- new admissions: `0`;
- solution diffs opened: `0`;
- candidate executions: `0`;
- treatment/model/API executions: `0`;
- holdout access: `NONE`.

The parent-failure rule and evidence-gated methodology policy remain unchanged.
In particular, `PARENT_FOCAL = PASS` still rejects a lead before solution
inspection, and unsupported methodological or documentary suggestions remain
suppressed.

## Validation and current state

- Harness self-test: `9/9 PASS`, exit `0`.
- Remote reconciliation: `PASS`, fast-forward only, no force operation.
- Secret scan: `PASS`.
- P0 immutability: `PASS`.
- Holdout: `SEALED`.
- `TASK_CORPUS = PARTIAL`.
- `COMPARATIVE_CORPUS_READY = NO`.
- `P1_S1_RELEASE = NO`.
- `REAL_P0_RUNS = 0/24`.

Raw remote, acquisition, and validation evidence is preserved under
`pilot-runs/p1-w21-remote-reconciliation/`. The nearest unresolved experimental
gap remains a new candidate with an independent, reproducible parent-side
verifier, a valid parent product failure, and executable preservation evidence.
