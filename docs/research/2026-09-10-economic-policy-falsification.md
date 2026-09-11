# dv — Falsificação da hipótese de política econômica mínima

Status: PESQUISA / NÃO APROVADO PARA IMPLEMENTAÇÃO
Data: 2026-09-10

## Pergunta

O `dv` precisa de um componente próprio de decisão econômica para escolher entre executor barato/forte, retry, escalada, verificação, workflow e multi-agent, ou regras mecânicas simples + providers existentes já são suficientes?

A hipótese deve ser falsificada antes de qualquer implementação.

## Evidência atual

### 1. Routing e cascades podem reduzir custo, mas não há vencedor universal

`LLMRouterBench` (2026) avalia mais de 400 mil instâncias, 21 datasets e 33 modelos, com múltiplos baselines de routing. O trabalho confirma complementaridade entre modelos, mas encontra que vários métodos sofisticados, inclusive alguns recentes/comerciais, não superam de forma confiável baselines simples sob avaliação unificada. Também observa retornos decrescentes com ensembles maiores.

Implicação para o `dv`: não justificar um router próprio por sofisticação. Primeiro comparar políticas mínimas e transparentes.

### 2. Cascata cheap-first paga re-run/escalation tax

Uma cascata que executa primeiro um modelo barato paga esse custo mesmo quando a tarefa terminará no modelo forte. Portanto `cheap-first sempre` não é economicamente dominante.

Trabalhos de 2026 sobre routing/cascades mostram que pré-routing pode evitar esse custo em tarefas suficientemente previsíveis, enquanto cascades podem ser vantajosas quando feedback real da execução é informativo.

### 3. Em software, trajetória parcial pode ser útil para decidir — mas não necessariamente para transferir

`SWE-Router` usa alguns passos exploratórios de um modelo barato para melhorar a decisão de continuar ou escalar em tarefas de software. Isso indica que a dificuldade pode emergir durante a execução e que prompt-only routing possui limite informacional.

Contudo, `The Handoff Tax` mostra que continuar uma trajetória produzida pelo modelo fraco com um modelo forte pode degradar a relação custo/qualidade. No estudo, full-trajectory escalation recupera menos da metade do gap de qualidade entre os tiers e adiciona prêmio de custo. Reduzir ou remover a trajetória fraca, preservando o estado do repositório, melhora a escalada.

Implicação: separar:

1. **trajectory as signal for routing**;
2. **trajectory as context for receiver**.

O primeiro pode ser útil; o segundo pode ser prejudicial.

### 4. Downshift e escalation são assimétricos

A evidência do Handoff Tax sugere:

- weak -> strong: preferir estado/artifacts + problema limpo, evitando transcript fraco quando possível;
- strong -> weak: preservar mais do contexto/blueprint produzido pelo forte pode ajudar o fraco.

Essa regra ainda precisa ser reproduzida nos providers escolhidos pelo `dv` antes de virar política operacional.

### 5. Verificação também deve ser alocada seletivamente

Pesquisa sobre adaptive/selective verification mostra que verificar todos os estados ou todas as hipóteses uniformemente pode desperdiçar custo. Há evidência de ganhos ao usar gates determinísticos/ranking barato e reservar verificação cara para estados onde ela tem maior valor informacional.

Implica que o custo do verificador faz parte da política econômica; não pode ser tratado como custo fixo ou gratuito.

## Consequência arquitetural provisória

Até aqui, não há evidência suficiente para um novo `Brain` ou router inteligente próprio.

O candidato mais defensável é uma política mecânica mínima, configurável e observável:

```text
TASK
  |
  +-- verified reusable artifact/plan? --> REUSE --> VERIFY
  |
  +-- task family has validated cheap policy? --> CHEAP/DIRECT --> VERIFY
  |
  +-- task family has validated strong-only policy? --> STRONG/DIRECT --> VERIFY
  |
  v
minimum diagnostic/exploration
  |
  v
cheap deterministic signals / execution feedback
  |
  +-- sufficient --> continue cheapest validated path
  |
  +-- insufficient --> escalate
                         |
                         +-- pass state/artifact refs + clean task spec
                         +-- avoid weak transcript by default on escalation
  |
  v
VERIFY with cheapest adequate verifier
  |
  +-- success --> STOP
  +-- inconclusive/fail --> expand only as justified
```

## Regra contra router prematuro

Não implementar um router aprendido, LLM-router ou metareasoner enquanto uma policy mecânica não tiver sido medida como baseline.

Um selector inteligente só pode ser considerado se demonstrar, em tarefas representativas:

`C_selector + C_selected_path < C_mechanical_policy`

mantendo ou aumentando:

`verified task success`

e sem elevar serious-failure rate além do limite predefinido.

## Baselines mínimos a comparar

B0 — strong executor direto.

B1 — cheap/free executor direto + verificação.

B2 — cheap-first + escalation após falha.

B3 — task-family static routing.

B4 — minimum-exploration + deterministic escalation rule.

B5 — learned/LLM routing, apenas depois de B0–B4.

Todas as variantes devem contabilizar:

- input/output/reasoning tokens quando disponíveis;
- tool/schema/context tokens;
- retries;
- handoff/bootstrap;
- verification;
- latency;
- monetary cost;
- verified success;
- serious failures;
- executor tier;
- provider/version;
- task family;
- artifacts reutilizados.

Métrica econômica principal:

`total system tokens / verified solved task`

Métrica monetária correspondente:

`total monetary cost / verified solved task`

## Decisão provisória

**OPEN / NOT APPROVED.**

Existe evidência forte de que tratamento econômico adaptativo pode ser útil, mas não de que o `dv` deva implementar um componente novo para isso.

A direção defensável agora é:

1. usar política mecânica mínima;
2. medir por família de tarefa;
3. permitir providers substituíveis;
4. tratar trajectory/handoff de forma direcional;
5. escalar verificação e executor somente quando sinais observáveis justificarem;
6. promover um selector mais complexo apenas se superar os baselines simples de forma reproduzível.

## Próxima falsificação

A pergunta agora é se uma policy por **task family + evidence signals** consegue ser suficientemente simples e estável para evitar um modelo/router adicional.

Se sim, o possível Brain encolhe para configuração/policy + observabilidade, sem nova inteligência central.

Se não, medir exatamente qual propriedade residual exige uma decisão aprendida e qual é o ganho líquido após incluir o custo do próprio selector.

## Referências principais

- Li et al. — LLMRouterBench: A Massive Benchmark and Unified Framework for LLM Routing, Findings of ACL 2026.
- Moslem et al. — Cluster, Route, Escalate: Cascaded Framework for Cost-Aware LLM Serving, 2026.
- Kotte — UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing, 2026.
- Ganz et al. — The Handoff Tax: Continuing Non-Native Trajectories in LLM Agents, 2026.
- SWE-Router / trajectory-based routing work on SWE-bench Verified, 2026.
- Adaptive Test-Time Compute Allocation via Learned Heuristics over Categorical Structure, 2026.
