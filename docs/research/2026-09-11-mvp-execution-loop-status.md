# MVP execution loop status

This record closes the locally executable part of the current DV execution
loop on September 11, 2026. It does not report treatment evidence.

## Evidence boundary

- DV `HEAD` is `08dcd2c1340b3b6c30d7733fa48e6e1f441d24b9`.
- The worktree is clean. `origin/main` is an ancestor, but the local branch is
  thirteen commits ahead; remote publication remains unauthorized.
- The Harness self-test passes `9/9`. All 28 current P1 JSON files parse, the
  P0 immutability check passes, and `git diff --check` passes.
- No treatment, model benchmark, paid API call, candidate generation, or
  holdout access occurred.

## Local gating

The environment contains `GEMINI_API_KEY` by boolean presence only. A Gemini
qualification probe was not executed because free-tier eligibility was not
verified and a credentialed generation request could incur external charges.
OpenAI and Anthropic credentials are absent. Ollama, vLLM, and llama.cpp are
not installed. Docker is installed but its daemon is inaccessible. The GPU is
reported as a GeForce GTX 1650 with 4096 MiB.

A non-generative Gemini model-catalog request succeeded and exposed
`models/gemini-3.7-flash` and `models/gemini-3.8-flash`, among others. This
proves metadata-surface access only. It does not qualify generation,
provider-native usage telemetry, pricing, or free-tier eligibility, so the
qualification probe remains pending.

The current admitted corpus remains `D-F2-05`, `D-F5-01`, and `D-F6-01`.
`COMPARATIVE_CORPUS_READY=NO`, `P1_S1_RELEASE=NO`, and `REAL_P0_RUNS=0/24`.
The registered external blockers are marked `PENDING_EXTERNAL_ACTION` for
queue management. This is an operational status, not a resolution or a
promotion of any scientific gate.

## New-source screening

The local NAIA lead at commit `756ebf1d` changes only
`src/product/calendar.mjs`. Its parent already contains
`test/product/calendar.test.mjs`, but the parent test does not assert the
changed list-range behavior. The lead therefore does not establish the
required failing-parent/verifier pair and is rejected for this screening pass.
An isolated archive of the parent was replayed with
`node --test test/product/product-slice.test.mjs`: all 18 tests passed with
exit code 0. This confirms `NO_PARENT_FAILURE`, rather than a product failure.
No solution diff was inspected and no source was modified.

A second local lead in `Rag-git` was screened at commit `5e366b36`, whose
parent contains preexisting governance and evidence tests. The isolated
parent replay was blocked before test execution because the environment lacks
`pytest` and `fitz`. The lead is therefore recorded as
`BLOCKED / ENVIRONMENT_NOT_REPRODUCIBLE`; it is not admitted and is not
classified as a product failure.

A third local lead in `searchleads` was screened at commit `eb78122`. It changes
only `.gemini/rules/empirical_guidelines.yaml` and `GEMINI.md`, with no product
change and no independently failing parent/verifier pair. It is rejected as
`NO_PRODUCT_VERIFIER_PAIR`; no solution diff was inspected and no source was
modified.

A fourth `searchleads` lead was screened at `9df9f6f`. Replaying its isolated
parent with `python -B scripts/run_live_network_certification.py` produced the
expected import failure (`ModuleNotFoundError: No module named 'searchleads'`,
exit code 1). The workflow invoking this exact command predates the task, and
the parent has library-level preservation tests using injected transports, but
those tests do not verify the script entrypoint. The candidate replay then
passed the import boundary but was blocked at `brasilapi.com.br:443` by
`WinError 10013` (exit code 1). The lead is therefore recorded as
`BLOCKED_ENVIRONMENT_NETWORK_REPLAY`; candidate-side success remains
unverified under a reproducible network contract. No solution diff was
inspected and no source was modified.

A fifth local lead in `smag` was screened around issue #94. The verifier
`packages/opencode/test/tool/external-directory-symlink.test.ts` was introduced
before the later source fix `6959888ca`, establishing temporal independence.
The isolated parent replay from `packages/opencode` reached Bun but was blocked
by the local dependency surface (`preload not found "@opentui/solid/preload"`,
exit code 1). The package `@opentui/solid@0.4.5` is present in the local Bun
cache, but no checkout has a materialized installation. An offline installation
was attempted in a temporary clone with `bun install --offline
--frozen-lockfile`: 20 packages resolved from cache, but Bun reported that the
lockfile had changes and exited 1. No lockfile or source checkout was modified.
It remains `BLOCKED_ENVIRONMENT_NOT_REPRODUCIBLE`; this is not a product
failure, and no solution diff was inspected.

Using the non-frozen offline install only in the temporary clone allowed the
parent test command to start, but it failed before assertions because the
transitive module `@ai-sdk/gateway` was absent (`0 pass`, `2 fail`, `1 error`,
exit code 1). Raw output is retained at
`pilot-runs/mvp-execution-loop/smag-parent695-offline-test.txt`; the temporary
workspace was removed. This remains an environment blocker, not product
evidence.

The same offline frozen-install probe was then run against the exact verifier
parent `f5bc2686d`. Bun resolved 19 packages from the local cache but again
reported `lockfile had changes, but lockfile is frozen` and exited 1. The
source checkout and lockfile remained unchanged; the SMAG lead stays pending
under `ENVIRONMENT_BLOCKED_LOCKFILE_REPRODUCIBILITY`.

A sixth SMAG lead was screened using the pre-existing
`packages/smag-governance/test/origin-resolution.test.mjs` verifier and the
isolated parent `5397b29a7f3f3beb3479e8332ce91d2afc8d81e0` of task commit
`0d54f44cf`. The exact Node command from `packages/smag-governance` failed
before assertions because `packages/smag-governance/src/smag.mjs` does not
export `resolveGitHubOrigin` (`SyntaxError`, exit code 1). This is recorded as
`BLOCKED_VERIFIER_OR_PRODUCT_SURFACE_UNRESOLVED`: attribution to the
historical product change, verifier surface, or missing export contract remains
unresolved without solution-side semantic inspection. The candidate diff was
not inspected, no source checkout was changed, and no treatment was executed.

A seventh SMAG lead, commit `a7363a803bb6d3f1c040fd14da8efd08288f54a9`, was
screened against parent `43573893b32363ac6ea608f5862feb2358f973f7` using the
pre-existing `packages/smag-governance/test/supervise.test.mjs` verifier. The
isolated replay from `packages/smag-governance` completed with exit code 0 and
7/7 tests passing. It therefore establishes `REJECTED_NO_PARENT_FAILURE`, not
product evidence. The candidate diff was not inspected, no source checkout was
changed, and no treatment was executed.

An eighth SMAG lead, commit `e1f939f9a023e4da87cc2754d78e5132a5978c3b`, was
screened against parent `6ddf8c7461bdb13d407e7f78239dbecd53375573` using the
pre-existing `packages/smag-governance/test/git-staging.test.mjs` verifier.
The isolated parent replay reached the assertion but failed on Windows newline
representation: actual `DIRTY\r\n` versus expected `DIRTY\n` (exit code 1).
This is recorded as `BLOCKED_ENVIRONMENT_LINE_ENDING`, because the observed
failure does not yet isolate the historical product behavior from platform
normalization. The candidate diff was not inspected, no source checkout was
changed, and no treatment was executed.

The same verifier was then replayed against the isolated historical candidate
snapshot `e1f939f9a023e4da87cc2754d78e5132a5978c3b`. It passed 1/1 test with
exit code 0 and the temporary workspace was removed. This establishes a
promising historical Fail-to-Pass pair, but not task admission: task-statement
freezing, full preservation evidence, and the reproducible environment contract
remain to be closed. It remains a pending acquisition lead, not treatment
evidence; no generated candidate or solution diff was inspected.

An attempted broad candidate preservation probe (`node --test test/*.test.mjs`)
was not promoted to a result: 55 test files were scheduled and 21 passing lines
were observed, but the wrapper did not expose a terminal exit code or complete
summary before its child processes released the temporary workspace. The probe
is therefore `INCONCLUSIVE`, not preservation PASS. The temporary workspace was
eventually removed without force-killing unidentified processes. No source
checkout was changed and no treatment was executed.

A second preservation probe with `--test-concurrency=1` likewise produced no
terminal summary or exit code and left a Node process live. That specifically
identified probe process was terminated and its exact temporary workspace was
removed. The result remains `INCONCLUSIVE`; no preservation PASS is inferred.

The SMAG staging lead was subsequently closed as an admissible development task
`D-F2-06`. Its task statement is anchored to the independent document
`docs/evidence/SMAG-WAVE1-STAGING-WINDOWS-LINKS-V1.md` at commit
`d07422f79b01738f260f2446eb9689ca031392e7` (blob
`194343d4e01ec1b15a83e45096156a6db4614f64`), which predates the candidate fix.
The focal verifier and related regression files were present in parent
`6ddf8c7461bdb13d407e7f78239dbecd53375573`; the candidate snapshot passed the
focal verifier, while the parent failed on the byte-preservation assertion.
The targeted preservation set (`git.test.mjs`, `git-origin-staging.test.mjs`,
and `staging-links.test.mjs`) passed 5 tests with 1 explicit Windows symlink
privilege skip in both parent and candidate. This supports admission with the
platform limitation recorded; it is not treatment evidence. The broad suite
probes remain inconclusive and are not used as a silent substitute.

## Remaining decision

The next defensible action is to qualify the first authorized strong executor
with exactly one synthetic probe, or to acquire a new verifier-first task with
an independently failing historical parent. Until one of those gates is
closed, the MVP status remains `INCONCLUSIVE` and the architecture decision
remains `INCONCLUSIVE`.

Raw evidence is in
`pilot-runs/mvp-execution-loop/2026-09-11-local-gate-evidence.json`.
