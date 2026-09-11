# P1-W17 — Verifier-first acquisition with mandatory parent failure

## Closure decision

W17 added no task. The existing development inventory and the two W16 SMAG leads
were reviewed under the frozen parent-failure gate. No fresh lead survived all
pre-solution requirements, and no remaining independent executable work was
identified within the bounded scope. The wave therefore closes as acquisition
readiness evidence, not empirical treatment evidence.

`TASK_CORPUS = PARTIAL`, `COMPARATIVE_CORPUS_READY = NO`,
`P1_S1_RELEASE = NO`, and `HOLDOUT = SEALED` remain unchanged. No model, paid
API, treatment, candidate application, or holdout access occurred.

## Baseline and frozen rule

The repository began at `2a48c86f2638994f4184c694f540bb03667af0ec`, already
reconciled with `origin/main`, on a clean `main` worktree. The Harness self-test
ran again with exit code `0` and `6/6` tests passing. Bun `1.4.0`, Node
`v24.18.0`, and Python `3.13.14` were observed. GitHub TCP 443 remained
unavailable during the baseline probe, but this did not alter local work.

The mandatory rule was applied literally: a parent focal PASS is not a valid
failure and cannot authorize candidate execution or solution-based oracle
redefinition. Environment, missing verifier, network, harness, and flaky
outcomes are not converted into product failure.

## Existing inventory review

The complete 18-candidate development inventory remains in
`pilot-runs/block-5b/task-discovery-screening.json`. Its 17 rejected or
not-admitted entries retain their original reasons. The admitted carry-forward
tasks are `D-F2-05`, `D-F5-01`, and `D-F6-01`; their prior evidence was not
reinterpreted as new acquisition evidence. Their recorded focal outcomes are
respectively PASS for the bounded transactional verifier, PASS for the 10-test
UX focal suite, and PASS for the locked offline Cargo evidence.

The W16 SMAG leads were not reused. `SMAG-N1` is closed because its parent focal
was `7/7 PASS` and its broad preservation was externally blocked by six GitHub
API/network tests. `SMAG-N2` is closed because no independent pre-solution focal
verifier was identifiable. These decisions are preserved in
`pilot-runs/p1-w16-acquisition/`.

No new source was expanded: the W17 scope expressly prohibits broad repository
expansion without a verifier-first rationale, and the existing bounded lead set
was already closed. Consequently, no new parent workspace or candidate workspace
was materialized.

## State and blockers

There were zero new candidates frozen, zero solution diffs authorized, zero
candidates materialized, and zero candidates admitted. The corpus remains three
tasks across families F2, F5, and F6, with no comparative coverage claim.

Open blockers remain:

- `P1-W1-BLK-002`: insufficient independent executable corpus for comparative P1;
- `P1-W4-BLK-STRONG-CREDENTIAL`: strong executor qualification requires an
  authorized credential and an explicitly permitted qualification probe;
- `P1-W16-SMAG-PRESERVATION-NETWORK`: broad SMAG preservation depends on
  unavailable GitHub API/network access.

These blockers are not treatment failures. The nearest defensible next step is
either a new verifier-first lead with an independently failing parent focal and
reproducible preservation, or resolution of one of the registered environment
or credential blockers. No post-hoc oracle, candidate, or treatment execution is
permitted.

## Validation

The wave evidence records JSON parsing, parent-gate application, holdout and
solution-leakage checks, P0 immutability, secret scan, Harness self-test, and
`git diff --check`. All pass for the committed W17 artifacts. Candidate and
treatment execution remain `NOT_EXECUTED`.

