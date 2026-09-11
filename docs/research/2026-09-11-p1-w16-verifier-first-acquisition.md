# P1-W16 — Verifier-first candidate acquisition

## Decision

W16 produced no new admissible P1 task. The bounded lead set was closed with two
objective rejections; `TASK_CORPUS` remains `PARTIAL`, `COMPARATIVE_CORPUS_READY`
remains `NO`, and `P1_S1_RELEASE` remains `NO`. This wave is acquisition evidence,
not treatment evidence.

No model, paid API, treatment, candidate application, or holdout access occurred.
The legacy holdout remains sealed.

## Frozen scope and source

The admissibility rule and lead identities were frozen before solution-diff
inspection. The selected source was the local `oigorbrito/smag` checkout, used
read-only; its pre-existing dirty state was not changed. `medvi` and contaminated
W15 workspaces were not re-screened. The bounded lead set was `SMAG-N1` and
`SMAG-N2`.

## Evidence and decisions

`SMAG-N1` uses parent `abafbde08af387f14c4e65abe9e26a09aee7f2bd` and the focal
verifier `packages/smag-governance/test/supervisor-session.test.mjs`, present in
the parent tree with blob SHA-1
`a19f9e09d43459fa9d463dfe848d2e53f603b393`. The neutral recovered command was
`node --test test/supervisor-session.test.mjs` from
`packages/smag-governance`, because the repository root test configuration points
to an absent root. It exited `0` with `7/7` tests passing. The parent therefore
did not demonstrate a focal product failure. The broad preservation command
`node --test test/*.test.mjs` exited `1`: `548` passed and `6` failed out of
`555`; the failures were GitHub API/network or GitHub App credential-exchange
tests. This is an external environment blocker, not a treatment result.

`SMAG-N1` was rejected because the parent focal already passes and preservation
was not executable under the observed environment. The historical solution diff
was inspected only after the freeze, for confirmation; it was not used to define
the verifier.

`SMAG-N2` uses parent
`b0a3dbb9eb61aaae996be6e14f1b40fa2ee2368c`. No exact, independent pre-solution
focal verifier was identifiable in the parent tree, so it was rejected before
any verifier could be admitted. The later solution-diff inspection only confirmed
test/source interleaving and did not create or repair an oracle.

## Corpus state

Before and after W16: 3 admitted tasks, 3 admitted families (`F2`, `F5`, `F6`),
and 2 repositories. No task was added. The existing admitted tasks remain
unchanged. W16 did not claim comparative readiness or a smoke release.

## Preserved evidence

- `pilot-runs/p1-w16-acquisition/leads-frozen.json`
- `pilot-runs/p1-w16-acquisition/pre-solution-verifier.json`
- `pilot-runs/p1-w16-acquisition/solution-confirmation.json`
- `pilot-runs/p1-w16-acquisition/environment-evidence.json`
- `pilot-runs/p1-w16-acquisition/smag-n1-focal.stdout.log`
- `pilot-runs/p1-w16-acquisition/smag-n1-focal.stderr.log`
- `pilot-runs/p1-w16-acquisition/smag-n1-preservation.stdout.log`
- `pilot-runs/p1-w16-acquisition/smag-n1-preservation.stderr.log`

The temporary parent clone was materialization evidence only and is not a
normative workspace or committed corpus artifact.

## Validation and blockers

JSON parsing, SHA/verifier resolution, ID uniqueness, solution-leakage scan,
holdout scan, P0 immutability, secret scan, DV harness self-test (`6/6`), and
`git diff --check` passed for the wave. Treatment execution is `NOT_EXECUTED`.

The nearest unresolved objective gap remains acquisition of one candidate with
an independent verifier, executable preservation suite, and reproducible
pre-solution environment. The carried remote blocker remains
`P1-W14-BLK-GITHUB-PUSH`; local work remains continuable. Strong-executor
qualification remains separately blocked by the authorized credential gate.

