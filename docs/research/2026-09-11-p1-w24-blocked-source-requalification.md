# P1-W24 — Blocked-source requalification

## Closure decision

`W24 = BLOCKED_SOURCES_RETAINED`. The two sources required by the wave,
`bpt2-abp` and `smag`, were requalified before any new source expansion. Both
remain `BLOCKED_SOURCE`. No new lead reached the parent-failure gate, and no
definitive rejection was reopened.

The result is not treatment evidence. No model, treatment, paid API, solution
diff, candidate execution, or holdout access occurred.

## Baseline and remote state

The baseline was branch `main`, `HEAD=
741e186b07a13315b3825d081d3e220a0ac7da0d`, clean worktree, and
`origin/main=13d2742c7b3ea2de0f5accb02089dd4edf2a2b35`. The remote was an
ancestor with `LOCAL_ONLY=2` and `REMOTE_ONLY=0`. The supported Harness
self-test passed `9/9`; `git diff --check` passed. Remote publication was not
retried because authorization remained unavailable.

## bpt2-abp

The source has a local .NET SDK (`10.0.401`), `global.json`, and a populated
NuGet cache with 17 top-level package directories. The bounded inventory did not
identify `packages.lock.json`. The registered `postgresql-x64-18` service was
`Stopped`, and GitHub TCP/443 was unavailable.

The prior bpt2 lead remains excluded. A new lead would still require a
reproducible locked restore, a bounded versioned PostgreSQL runtime, and a
pre-existing independent parent verifier. Those conditions were not satisfied.
The source remains `BLOCKED_SOURCE`, not `REJECT_SOURCE`, because the evidence
does not disprove that a future clean lead could satisfy the contract.

## smag

The source has `package.json`, root `bun.lock`, and package-scoped lockfiles.
However, no genuinely new undecided lead was identified. `SMAG-N1` and
`SMAG-N2` remain definitive closed decisions and were not reopened. TCP/443 was
unavailable, so the previously observed external preservation dependency could
not be removed. A future lead could still become eligible with a parent-side
verifier and sufficient task-scoped local preservation; therefore the source
remains `BLOCKED_SOURCE`, not `REJECT_SOURCE`.

## Expansion gate and parent-failure gate

Because neither blocked source resolved to `SCREEN`, the new-source expansion
gate was not reached. No new repository was screened. This preserves the
protocol rule that repository expansion requires an evidence-backed rationale
after current blocked sources are resolved.

There were zero metadata-only opportunities, lead freezes, parent
materializations, parent focal executions, repeatability checks, or immutable
pre-solution freezes. Consequently, there were zero parent-failure-qualified
leads. No solution inspection was authorized.

## Corpus state

The admitted corpus remains `D-F2-05`, `D-F5-01`, and `D-F6-01`, across
families `F2`, `F5`, and `F6`, in two repositories. Counts remain `3` tasks and
`2` repositories before and after W24. `TASK_CORPUS = PARTIAL`,
`COMPARATIVE_CORPUS_READY = NO`, and `P1_S1_RELEASE = NO` remain unchanged.

## Validation and side effects

The W24 JSON artifacts parsed successfully. Source exclusion, source-disposition
consistency, parent-failure gate, failure attribution, solution-leakage scan,
holdout scan, P0 immutability, secret scan, Harness self-test, and
`git diff --check` passed. No source checkout was modified; both source
checkouts were already dirty and were not used as experimental workspaces.

The full evidence is in
`pilot-runs/p1-w24-blocked-source-requalification/`:

- `baseline.json`;
- `source-requalification.json`;
- `acquisition-closure.json`;
- `validation.json`;
- `command-evidence.txt`.

## Final state and next gap

- `bpt2-abp = BLOCKED_SOURCE`;
- `smag = BLOCKED_SOURCE`;
- new-source expansion: `NO`;
- new admissions: `0`;
- parent-failure-qualified leads: `0`;
- `TASK_CORPUS = PARTIAL`;
- `COMPARATIVE_CORPUS_READY = NO`;
- `P1_S1_RELEASE = NO`;
- `REAL_P0_RUNS = 0/24`;
- `HOLDOUT = SEALED`.

The nearest objective gap is an independently verified parent failure from a
new or genuinely undecided lead, with local/offline preservation. For bpt2, the
additional concrete gap is reproducible package and PostgreSQL supply. For
smag, it is a new lead with task-scoped local preservation or a reproducible
network-enabled environment.
