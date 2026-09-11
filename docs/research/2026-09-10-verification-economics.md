# Verification Economics — Cheap Executors, Selective Verification, and Escalation

Status: RESEARCH / FALSIFICATION
Date: 2026-09-10

## Question

Can `dv` achieve lower `total system tokens / verified solved task` by combining weaker/free executors with cheap verification and selective escalation, instead of sending every task to a stronger model from the start?

This document does not approve an architecture. It records current evidence and the next empirical falsification.

## Current evidence

### 1. Cheap-first is not automatically cheap

Recent cascade research shows a structural problem with naive escalation: if every task is first sent to a cheap model and difficult tasks are then re-run by a stronger model, escalated tasks pay both costs.

`Is Escalation Worth It? A Decision-Theoretic Characterization of LLM Cascades` (arXiv:2605.06350) evaluates five benchmarks and eight models. Within the tested deterministic cascade class, a lightweight pre-generation router outperformed the best cascade on four of five datasets, primarily because it avoided paying the cheap-model generation cost for tasks sent directly to a stronger model.

Implication for `dv`:

> Do not freeze `cheap executor first` as a universal policy.

Cheap-first must compete against at least:

- direct weak executor;
- direct strong executor;
- pre-generation routing;
- partial-exploration routing;
- weak retry before escalation;
- selective verification.

### 2. Partial exploration can improve routing, but it creates a new cost term

`SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks` (arXiv:2607.00053) studies a weak model executing a few exploratory turns before deciding whether to continue or escalate. The paper reports substantially better cost efficiency while preserving most of the stronger model's performance.

This supports a possible strategy where difficulty is inferred from real execution evidence rather than task text alone.

But the exploratory trajectory is not free:

`C_total = C_explore + C_route + C_continue_or_escalate + C_verify`.

The exploration phase is justified only when its information value exceeds its cost.

### 3. Escalating a full weak-model trajectory can be counterproductive

`The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents` (arXiv:2608.24358) studies coding agents switching between low- and high-capability models. Across Claude and GPT model pairs, full-trajectory escalation recovered less than half of the low-to-high capability quality gap while incurring substantial additional cost.

The result also shows that the best handoff interface depends on direction: reducing low-capability trajectory information improved escalation quality, while removing strong-model trajectory information hurt downshift.

Implication for `dv`:

> Escalation should not imply replaying the full prior conversation/trajectory into the stronger model.

Candidate baseline for escalation:

```text
external durable state
+ current repository/workspace state
+ compact task contract
+ verified observations/failures
+ relevant artifact references
- weak model narrative/history unless empirically useful
```

This is a testable handoff policy, not an approved contract.

### 4. Verification itself must be cost-aware

`Adaptive Generate-Rank-Verify: Inference-Time Search with Costly Verification` (arXiv:2605.17609) formalizes settings where candidate generation/ranking is cheap but verification is expensive. Its adaptive policy progressively increases sampling and verification rather than applying the expensive verifier uniformly. Experiments in mathematical reasoning and competitive programming support adaptive verification over fixed policies in the studied settings.

Implication:

> A verifier is a scarce resource too. `VERIFY EVERYTHING WITH THE STRONGEST JUDGE` is not an economic baseline.

### 5. Verification has a hierarchy of certificate strength

For software tasks, many important claims have cheap executable certificates:

```text
compile
schema/type validation
static checks
unit/integration tests
property tests
reproduction scripts
hash/revision checks
policy gates
sandboxed execution
```

Execution-based evaluation is generally closer to functional correctness than stylistic or similarity-based judging for code where a suitable oracle exists.

However, tests are not automatically useful merely because an agent writes more of them. `Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents` (arXiv:2602.07900), analyzing six modern models on SWE-bench Verified plus controlled prompt experiments, reports that changing the amount of agent-written tests did not significantly alter final outcomes in its studied setting. Thus `more generated tests` is not itself evidence of stronger verification.

Rule:

> Prefer the cheapest verifier that constitutes a valid certificate for the claim being made; do not confuse verification activity with verification strength.

### 6. LLM judges should be selective, not universal truth authorities

`Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement` (arXiv:2407.18370) develops selective evaluation and cascaded judges: cheaper judges handle cases where their confidence is adequate and harder cases escalate.

This supports a verifier cascade conceptually, but it does not prove that a weak judge can verify every domain. A model judge is especially weak where correctness requires reasoning at or above the capability needed to produce the result and no independent certificate exists.

For code/workspace tasks, deterministic or executable evidence should therefore precede LLM judgment wherever possible.

## Updated economic hypothesis

The initial idea:

```text
weak/free executor
      -> verify
      -> strong executor if failure
```

is too coarse.

A more defensible hypothesis is:

```text
TASK
 |
 +-- cheap certificate / deterministic oracle available?
 |        |
 |        +-- yes --> cheapest sufficient executor --> certificate
 |        |                                      |
 |        |                              pass --> STOP
 |        |                              fail --> diagnose
 |        |
 |        +-- no --> uncertainty/risk policy
 |
 +-- evidence says task is likely beyond cheap tier?
 |        |
 |        +-- yes --> strong executor directly
 |        |
 |        +-- no --> cheap/minimal execution
 |
 v
VERIFY using cheapest sufficient verifier
 |
 +-- verified success --> STOP
 |
 +-- clear recoverable failure --> cheap recovery/retry if economically justified
 |
 +-- uncertainty / insufficient capability --> ESCALATE
                                            |
                                  compact state-based handoff
                                            |
                                      strong executor
                                            |
                                         VERIFY
```

The important change is that escalation and verification are decisions based on expected marginal value, not mandatory stages.

## Candidate verifier ladder

From cheapest/most deterministic toward more expensive/subjective:

1. syntax/schema/type/hash checks;
2. deterministic policy predicates;
3. compiler/build;
4. targeted existing tests;
5. broader existing test suite;
6. sandboxed behavioral/reproduction checks;
7. specialized static/dynamic analyzers;
8. cheap learned or LLM verifier;
9. strong LLM judge/verifier;
10. human review where required.

This is not a universal ordering of correctness strength. It is a candidate economic ladder. The correct verifier depends on the acceptance claim.

## New constraints for `dv`

### V1 — Verification cost is first-class

Measure separately:

- verifier input tokens;
- verifier output tokens;
- deterministic verifier runtime;
- model verifier cost;
- number of verification attempts;
- false accept / false reject where ground truth exists;
- human review time/cost where applicable.

### V2 — Escalation rate is first-class

A weak-first strategy can lose economically if too many tasks are escalated and paid twice.

Record:

`escalation_rate = escalated_tasks / tasks_started_on_cheap_tier`

and compare total cost against direct-strong baseline.

### V3 — Handoff payload must be experimentally varied

At minimum compare:

- full trajectory;
- compact summary;
- state + failed checks only;
- state + task contract + artifact refs;
- fresh strong-model restart from durable workspace state.

Primary metrics remain verified success and total system tokens/cost.

### V4 — Do not treat free executor tokens as zero system cost

Even if executor inference is free, its use can create:

- latency;
- retries;
- verifier calls;
- handoff/context reconstruction;
- strong-model escalation;
- infrastructure/runtime cost.

Therefore free/cheap executor is valuable only if total verified-task economics improve.

## Strongest current falsification

A new `dv` policy layer is unnecessary if a simple composition of existing mechanisms can achieve the same frontier:

```text
cheap deterministic certificates
+ simple pre-routing
+ minimal execution
+ selective verification
+ state-based escalation
+ existing runtime/adapters
```

A new economic controller should be considered only if this mechanical baseline is empirically insufficient and a learned/complex policy beats it after including its own decision cost.

## Required experiment matrix

For representative software tasks, compare at least:

| Treatment | Executor | Verification | Escalation |
|---|---|---|---|
| A | strong | deterministic + required domain checks | none |
| B | cheap/free | same checks | none |
| C | cheap/free | same checks | strong on failure |
| D | pre-router | same checks | route before generation |
| E | cheap exploration | same checks | route after bounded exploration |
| F | cheap/free | selective verifier ladder | compact state-based escalation |

For escalated treatments, compare full trajectory versus fresh/compact state transfer.

Primary outcome:

`total system tokens / verified solved task`

Additional:

- monetary cost / verified solved task;
- verified solve rate;
- false acceptance;
- latency;
- escalation rate;
- retry count;
- verifier cost;
- handoff size;
- context reconstruction cost.

## Current disposition

- `free/weak executor + verification`: PLAUSIBLE, NOT PROVEN.
- `cheap-first always`: REJECT AS UNIVERSAL RULE.
- `full-trajectory escalation`: NEGATIVE EVIDENCE; MUST NOT BE DEFAULT.
- `selective verification`: STRONG PRIOR ART; candidate baseline.
- `deterministic/executable certificates first`: DEFENSIBLE BASELINE when applicable.
- `strong LLM verifier for every task`: NOT JUSTIFIED.
- `new intelligent dv router/controller`: NOT JUSTIFIED YET.

## Sources

- Bouchard, D. `Is Escalation Worth It? A Decision-Theoretic Characterization of LLM Cascades`, arXiv:2605.06350, 2026.
- Son, S. et al. `SWE-Router: Routing in Multi-turn Agentic Software Engineering Tasks`, arXiv:2607.00053, 2026.
- Ganz, R. et al. `The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents`, arXiv:2608.24358, 2026.
- Dughmi, S. et al. `Adaptive Generate-Rank-Verify: Inference-Time Search with Costly Verification`, arXiv:2605.17609, 2026.
- Chen, Z. et al. `Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents`, arXiv:2602.07900, 2026.
- Jung, J. et al. `Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement`, arXiv:2407.18370, 2024.

## Decision rule

No component or policy described here is approved until it satisfies the repository-wide gate:

**software-engineering defensibility + empirical validation proportional to the claim.**
