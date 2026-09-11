# Static Routing by Task Family — Falsification Note

Status: RESEARCH / NOT ARCHITECTURE APPROVAL
Date: 2026-09-10

## Question

Can most of the economic benefit of model/executor routing be captured by a simple empirically learned table keyed by task family and a small number of observable signals, without introducing an LLM-based or learned router into the `dv` core?

## Why this matters

The `dv` optimizes the whole system, not a component in isolation. A router that saves executor cost but adds classification, prompt, context, latency, maintenance, or misrouting cost can make the total system worse.

The primary metric therefore remains:

`total system tokens / verified solved task`

with monetary cost, latency, retries, escalations, verification cost and failure cost tracked alongside it.

## Evidence found

### 1. Task type may explain most recoverable routing gain

A 2026 study, *Most of the LLM routing gap is task type*, evaluated 14 models over 294 questions spanning seven task types and three languages, executing the full matrix twice. The authors report that a static lookup by task type recovered 21 of 29 reproducible routing opportunities under their main both-run criterion. Adding language recovered two more, leaving six of 294 items outside the static task-type-plus-language rule.

Important limitation: this comparison was fitted and evaluated on the same matrix with no holdout. It is evidence that coarse observable structure can matter substantially, not proof that the same table generalizes to `dv` workloads.

The same study also observed non-trivial run-to-run instability even with nominally deterministic settings, reinforcing that small routing gains can sit below the reproducibility floor and should not be treated as demonstrated improvement without replication.

### 2. Production-oriented routing work converges on category × difficulty cells

The 2026 T2MO methodology for enterprise coding assistants proposes classifying sessions by task category and difficulty tier, benchmarking candidate models in a production-like harness, and routing to the cheapest model that satisfies quality and latency constraints.

Crucially, its optimization target is not raw token price; it is expected cost per completed task, explicitly pricing failures and escalation. It also recommends staged evolution from static policies to more sophisticated classifiers only after evidence supports doing so.

This is closely aligned with the `dv` rule that the routing mechanism must earn its own overhead.

### 3. A small model can make front-door routing cheap, but accuracy is still a gate

A 2026 pre-registered experiment evaluating 1–4B models for front-door routing found that self-hosted classification can make the marginal monetary routing cost close to zero and sub-second in the tested setup. However, no tested model met the authors' standalone viability criterion of >=0.85 accuracy with <=2 s P95 latency.

Therefore, "cheap classifier" does not imply "safe routing policy". Misclassification cost must be included in the whole-task objective.

### 4. Confidence-only cascades are not a universal solution

Prior work on language-model cascades shows that uncertainty measures can improve cost-quality tradeoffs, but no single straightforward confidence rule works reliably across generative tasks. This weakens any proposal for a universal `if confidence < x -> escalate` rule.

## Engineering interpretation

The evidence supports a simpler progression than an intelligent router-first architecture:

```text
observed task family
      +
small stable signals
      |
      v
empirical lookup / thresholds
      |
      +--> cheapest validated executor for this cell
      |
      v
VERIFY
      |
      +--> success -> STOP
      |
      +--> insufficient -> controlled escalation
```

Possible observable signals, to be admitted only if empirically useful:

- task family/category;
- repository/language/runtime family;
- destructive or externally irreversible action;
- expected artifact type;
- presence of deterministic verifier;
- estimated scope from non-LLM metadata (files, diff size, dependency count, tool count);
- prior success rate of a provider for the same task cell;
- latency/cost budget;
- availability/readiness of provider;
- whether a safe verified plan/artifact is reusable.

Do not add a signal merely because it sounds predictive. Each signal adds classification, data, coupling and maintenance cost.

## Proposed policy hierarchy for empirical testing

These are baselines, not approved architecture:

- `B0`: strongest executor always.
- `B1`: cheapest/free executor always, then verify.
- `B2`: cheap-first cascade, escalate on failed verification.
- `B3`: static routing by task family.
- `B4`: static routing by task family × small observable difficulty/risk tier.
- `B5`: nearest-neighbor / embedding lookup over prior empirically labeled tasks.
- `B6`: learned or LLM router.

A more complex baseline may only replace a simpler one if it produces a reproducible improvement that exceeds its own routing and maintenance overhead.

## Acceptance rule

For candidate router/policy `R` versus simpler baseline `S`, do not approve `R` unless, on a representative held-out workload:

1. verified task success is non-inferior or superior under predeclared criteria;
2. total tokens per verified solved task improves materially;
3. total monetary cost per verified solved task improves materially, or a predeclared quality/latency gain justifies added cost;
4. routing decision overhead is included;
5. failure and escalation costs are included;
6. results reproduce across repeated runs where model stochasticity can affect the conclusion;
7. the gain is larger than the observed execution-noise/reproducibility floor;
8. the result survives holdout evaluation rather than only in-sample fitting.

Otherwise classify as `INCONCLUSIVE` or reject the added complexity.

## Current disposition

- Custom intelligent router in `dv`: **NOT JUSTIFIED**.
- LLM-based central decision-maker: **NOT JUSTIFIED**.
- Static empirically learned task-family table: **STRONG BASELINE CANDIDATE**.
- Task-family × small observable tier table: **STRONG BASELINE CANDIDATE**.
- Learned router: **ESCALATION-ONLY RESEARCH CANDIDATE**.
- Universal confidence threshold cascade: **NOT SUPPORTED AS GENERAL RULE**.

## Architectural consequence if the simple policy survives

If `B3/B4` perform competitively, the residual `dv` control surface may reduce to:

```text
configuration / empirical table
          +
provider capability metadata
          +
small adapters
          +
measurement envelope
          +
verification / escalation rules
```

That would further falsify the need for a Brain, super-orchestrator or central reasoning agent.

## Next falsification

Test whether task-family tables remain effective under:

1. held-out tasks;
2. provider/model updates;
3. multiple domains beyond coding;
4. free/local/weak executors versus strong paid executors;
5. realistic verification and escalation cost;
6. drift over time.

The next key question is therefore not "how do we build the router?" but:

> How stable are empirically learned task-family/provider cells over time, and how cheaply can we detect when a cell has drifted enough to require re-benchmarking?
