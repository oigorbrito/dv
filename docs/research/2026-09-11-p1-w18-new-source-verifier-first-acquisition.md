# P1-W18 — New-source verifier-first acquisition

## Closure

W18 ended with one justified new source and one frozen lead. The parent focal
verifier executed successfully, so the mandatory rule rejected the lead as
`NO_PARENT_FAILURE`. No candidate solution diff was opened, no candidate was
materialized, and no candidate or treatment was executed. This is not treatment
evidence.

The resulting state remains `TASK_CORPUS = PARTIAL`,
`COMPARATIVE_CORPUS_READY = NO`, `P1_S1_RELEASE = NO`, and `HOLDOUT = SEALED`.

## Baseline and source rationale

The wave started at `2a48c86f2638994f4184c694f540bb03667af0ec`, on clean `main`,
with `origin/main` equal to HEAD. The Harness self-test passed `6/6`. Bun
`1.4.0`, Node `v24.18.0`, and Python `3.13.14` were available. GitHub TCP 443
remained unavailable, but the selected source was already local and did not
require a remote fetch.

The selected source was `C:\Projetos\metao-gate`, a local checkout of
`oigorbrito/metaO` not exhausted by the closed P1 candidate inventory. It was
chosen because its parent-side Rust workspace contains versioned issue-specific
tests, a lockfile, and no required model/API credentials. The source checkout
was inspected read-only and its pre-existing dirty state was not modified.

## Lead freeze and parent gate

`METAO-GATE-N1` was frozen before solution inspection:

- candidate: `2f730773d073a5c4c5bd05b7ae4c0a4f2481a533`;
- parent: `2572ddcc1ca4c0aa78abc095fdc35bccc6e15a05`;
- family: proposed `F6`;
- verifier: `experiments/rust-chassis-a/metao-testkit/tests/issue_396_ado_qualification.rs`;
- verifier SHA-256: `8D9F894F453BE40DED191F96B7B69601EFCB91BF21D3153A2294094DC04CBBF7`;
- lockfile SHA-256: `277084EAE55CAC991A0ED8FF58A7797E2C0822DC61927AAEA3E9EDE6A3E3BCF6`.

The exact parent was materialized detached and clean. The focal command was:

```text
cargo test --manifest-path experiments/rust-chassis-a/Cargo.toml --locked --offline --test issue_396_ado_qualification
```

It exited `0` with `12 passed, 0 failed`. The parent therefore did not exhibit
a valid task-relevant product failure or pre-frozen objective deficiency. Under
W18, `PARENT_FOCAL = PASS` means `status = PASS`, disposition `REJECTED`, and
classification `NO_PARENT_FAILURE`. Preservation was not run because the hard
gate prohibits progression after a parent focal PASS.

The first execution exceeded the short tool wait while compiling, with no
output; the process was safely terminated as our own process. A subsequent
bounded execution completed successfully and its stdout/stderr are preserved.

## Solution and candidate boundary

Solution inspection was not authorized by B7. Accordingly:

- `SOLUTION_DIFF_AUTHORIZED = NO`;
- `SOLUTION_LEAKAGE = NOT_APPLICABLE`;
- candidate materialization = `NOT_TESTED`;
- candidate focal = `NOT_TESTED`;
- candidate preservation = `NOT_TESTED`.

No oracle was redefined, no test was copied backward, and no gold solution was
used. The closed inventory of 18 prior candidates and W15/W16/W17 leads remains
closed and is referenced rather than reopened.

## Final blockers and validation

Open blockers are the insufficient comparative corpus (`P1-W1-BLK-002`), strong
executor credential qualification (`P1-W4-BLK-STRONG-CREDENTIAL`), and the W16
SMAG preservation network dependency (`P1-W16-SMAG-PRESERVATION-NETWORK`). The
nearest objective gap is a new verifier-first lead whose parent focal genuinely
fails under a reproducible, independent verifier; alternatively, an existing
blocked lead may be revisited only when its exact unblock condition is observed.

Evidence includes `lead-freeze.json`, `parent-result.json`,
`closed-inventory.json`, raw focal logs, and `validation.json` under
`pilot-runs/p1-w18-acquisition/`. JSON parsing, SHA/verifier validation,
parent-gate validation, holdout and secret scans, P0 immutability, Harness
self-test, and `git diff --check` passed. Treatment/model/API execution remains
`NOT_EXECUTED`.

