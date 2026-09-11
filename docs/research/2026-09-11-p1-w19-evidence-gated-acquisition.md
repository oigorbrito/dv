# P1-W19 — Evidence-gated verifier-first acquisition

## Closure

W19 produced no new P1 admission. The wave applied the frozen parent-failure
gate and the evidence-gated methodology policy. The result is not treatment
evidence, executor evidence, or a comparative result.

The carried state remains `TASK_CORPUS = PARTIAL`,
`COMPARATIVE_CORPUS_READY = NO`, `P1_S1_RELEASE = NO`, and
`HOLDOUT = SEALED`.

## Baseline and scope

The wave started at commit
`13cec2bbdf2bb2b68030b288c571fea877affa34`, with `origin/main` equal to
`HEAD`, a clean worktree, and the Harness self-test passing `6/6` with exit
code `0`. The scope was limited to at most one verifier-first acquisition
opportunity. No model, paid API, treatment, candidate, or holdout was used.

The prior closed inventory contains 18 screened candidates. The carried
admitted tasks remain `D-F2-05`, `D-F5-01`, and `D-F6-01`; no historical
candidate was reopened.

## Parent-side gate

The W18 lead `METAO-GATE-N1` was the only new lead carried into this closure.
Its exact parent was executed before solution inspection using the independent
issue-specific focal test. The command exited `0` with `12/12` tests passing.
Therefore the mandatory rule applies:

```text
PARENT_FOCAL = PASS
=> REJECT
=> SOLUTION_DIFF = NOT_INSPECTED
=> CANDIDATE_EXECUTION = NOT_TESTED
```

This result proves only that the parent did not exhibit the required valid
failure. It does not classify any treatment or candidate as successful or
unsuccessful.

Raw stdout, stderr, lead freeze, and parent result are preserved under
`pilot-runs/p1-w18-acquisition/`. W19's decision and validation records are
under `pilot-runs/p1-w19-acquisition/`.

## Evidence-gated methodology and documentation

The attached harness policy was applied as a change gate. No methodological or
documentary recommendation was emitted or committed merely for completeness,
architectural preference, or status narration. The only W19 records exist to
preserve an acquisition decision, its parent-failure attribution, the current
blockers, and the reproducibility-relevant commands and results.

The supported evidence classes for those records are:

- `ORACLE_VALIDITY`: the parent-side verifier result determines whether solution
  inspection is admissible;
- `FAILURE_ATTRIBUTION`: a parent focal pass must not be reclassified as a
  product failure;
- `REPRODUCIBILITY`: exact SHAs, commands, and raw logs preserve the decision;
- `TRACEABILITY`: the decision is bound to W18 evidence and the current HEAD.

No new harness abstraction, router, verifier, or protocol semantics was added.

## Outcome and blockers

W19 outcome: `NO_NEW_ADMISSION`. The nearest unresolved objective gap remains
one candidate with an independent parent-side verifier that demonstrates a
valid, reproducible parent product failure and has executable preservation
evidence. The strong executor credential blocker and the observed SMAG network
dependency remain unchanged.

The evidence-gated rule requires stopping when no supported improvement remains;
it does not authorize a speculative new workstream or a solution-derived
oracle.

## Validation

- Harness self-test: `6/6 PASS`, exit `0`.
- Parent-failure gate: `PASS` for the rejection decision.
- Solution leakage scan: `PASS`; no new solution diff was opened.
- Treatment/model/API execution: `NOT_EXECUTED`.
- Holdout: `SEALED`.
- Secret values: not recorded.
- Raw evidence from W18: preserved without overwrite.
