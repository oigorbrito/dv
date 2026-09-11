# BLOCK 5B — P1 verifier-first task discovery and executor S0 qualification

Date: 2026-09-11
Repository: `C:\Projetos\dv`
Entry HEAD: `f26acaaa2a1287d05d11dbc544ba4adce4d98ab9`
Holdout: `SEALED`

## Decision summary

This block performed no treatment execution, model invocation, paid API call, candidate generation, or holdout access.
The frozen admissibility contract was restated before screening. The result is intentionally partial:

```text
TASK_DISCOVERY_STATUS = P1_TASK_CORPUS_PARTIAL
EXECUTOR_S0_STATUS = S0_QUALIFICATION_PARTIAL
P1_S1_RELEASE = NO
P1_DEVELOPMENT_CORPUS = 1 admitted task / 18 development candidates screened
PROPOSED_S1_PILOT = 1 task, pilot-only, no comparative claim
```

Only `D-F6-01` is admitted. The other 17 development candidates remain recorded with explicit exclusion or non-admission
reasons. No family was filled with a similar test and no task was selected using expected treatment performance.

## 1. Frozen admissibility gate

Before discovery, `experiments/p1/task-admissibility-contract-v1.json` was re-hashed as:
`41a8e3fa589cca43053ee8f627c69d624f50c5910e2075385f2440561c961d60`.

Admission required exact pre-solution base, frozen task statement, independent focal verifier and provenance, independence
from treatment output, reproducible base/candidate execution, preservation evidence, reproducible environment, no gold
solution exposure, hashable/versioned verifier artifacts, separable failure attribution, and unambiguous family assignment.
The gate was not relaxed after inspection.

## 2. Development task discovery

The source universe was limited to the 18 development tasks in the canonical manifest. Legacy holdout identifiers were not
opened or copied into the new corpus. The complete machine-readable screening record is
`pilot-runs/block-5b/task-discovery-screening.json`.

The three families with unresolved independent-oracle defects remain `NOT_OPERATIONALIZABLE_YET` for this pilot. F1 and F5
remain `PARTIAL` because environment/setup reproducibility is not established. F6 is `OPERATIONALIZABLE` based on the
already versioned D-F6-01 verifier and controlled baseline evidence.

`D-F6-01` uses base `5d00cd284ce8fe810b0f5192c56d98608be516d4`, a detached clean workspace, the v2 neutral working-directory
contract, locked offline Cargo execution, and the prior evidence file
`pilot-runs/block-4ah-offline-oracle-closure/evidence/f6-offline-recovery-results.json`. The evidence records exit code 0
for discovery persistence, phase6 shadow, and the locked workspace preservation suite. The base was not modified and no
historical solution was applied.

The admitted corpus is `experiments/p1/p1-development-corpus-v1.json`. It is not a six-family corpus and makes no claim of
comparability or generalization. The proposed S1 pilot has one task and is suitable only for pipeline/harness interaction
checks; it cannot support family comparison, executor ranking, statistical superiority, or external generalization.

## 3. Executor S0 qualification

`experiments/p1/executor-s0-qualification-v1.json` contains 10 candidate records. This is surface and admissibility
qualification, not performance benchmarking. Six remote records are credential-blocked because 5B did not authorize paid
generation calls. Ollama is `S0_DOWNLOAD_REQUIRED`; vLLM is environment-blocked because no runtime/model was installed or
pinned. OpenManus and Microsoft Agent Framework are frameworks requiring an underlying provider/model, so they are not
standalone comparable executors in this block.

The exact Google economic model name was rechecked. `gemini-3.8-flash` is documented as an exact model ID in the current
source register. The previous generic `gemma-4` record was corrected prospectively to `gemma-4-31b-it` (with the documented
26B alternative); this does not mutate 5A or bind a treatment.

Documentation sources and retrieval date are preserved in `pilot-runs/block-5b/executor-documentation-register.json`.
Current provider documentation is evidence of a callable surface, not evidence that credentials, quota, telemetry fields,
terms, or benchmark suitability are qualified. For example, [OpenAI model documentation](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4),
[Google Gemini model documentation](https://ai.google.dev/gemini-api/docs/models?authuser=77&hl=en),
[Google hosted Gemma documentation](https://ai.google.dev/gemma/docs/core/gemma_on_gemini_api), and
[Ollama compatibility documentation](https://docs.ollama.com/api/openai-compatibility) were used only for this screening.

## 4. Local environment

The inventory is preserved in `pilot-runs/block-5b/local-environment-inventory.json`:

- Windows `10.0.26200.0`; process environment reports 8 processors.
- WMI CPU, RAM, and GPU queries were denied by the execution environment, so hardware identity and VRAM are `UNKNOWN`.
- Ollama and vLLM executables were not found.
- Docker and WSL command surfaces were found, but neither was used to install or download a model.
- No large model download was performed.

These are environment observations, not claims that local inference is impossible on the host outside this sandbox.

## 5. Harness compatibility

Harness v1 was not modified. Existing self-tests were not used to claim provider performance. The evidence supports
`HARNESS_V1_SUFFICIENT` for the already defined artifact/evidence envelope and deterministic reconciliation shape, while
remote non-OpenAI and framework-specific runtime adapters remain unqualified. No generic provider-neutral runtime was built.

## 6. Deterministic shaping

`experiments/p1/task-shaping-schema-v1.json` defines S1 fields for objective, constraints, allowed scope, relevant paths,
verifier reference, environment constraints, and required artifact. It is metadata-derived, contains no LLM planning, and
was not executed as an S0/S1 comparison.

## 7. Validation

The following checks were run and preserved:

- all 7 new JSON/evidence artifacts parsed successfully;
- discovery record contains 18 unique development candidates and one admitted task;
- admitted base/verifier hashes match the recorded prior evidence;
- no legacy holdout identifier was included;
- no API secret was recorded;
- no model/treatment call occurred;
- Harness v1 self-test: `python -B tools/test_dv_pilot_harness.py`, exit code 0, 6 tests passed;
- `git diff --check` passed for the block commit.

## 8. Remaining blockers and next defensible step

F1/F5 need reproducible local package environments. F2/F3/F4 need independently versioned verifier artifacts or a new
prospective task acquisition process that creates the verifier before any solution is exposed. Remote executors need
credentialed S0 qualification with native usage, timeout, artifact capture, cost source, and terms evidence. Local executors
need runtime/model pinning and hardware evidence. None of these blockers can be solved by treatment output.

The next defensible step is to acquire new prospective development tasks under the frozen verifier-first procedure and then
qualify at least one strong and one economic/local/free executor through non-comparative S0 checks. The legacy holdout stays
sealed.

```text
BLOCK_5B = COMPLETE
BLOCK_5B_OUTCOME = P1_TASK_CORPUS_PARTIAL / S0_QUALIFICATION_PARTIAL
REAL_P0_RUNS = 0/24
P0_RELEASE = NO
HOLDOUT = SEALED
TREATMENT_EXECUTION = false
```
