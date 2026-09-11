# Pesquisa Brain / MetaO / SMAG — snapshot de falsificação

Data: 2026-09-10

Status: **pesquisa; nenhuma arquitetura aprovada; não implementar ainda.**

## 1. Objetivo real

Não fundir MetaO + SMAG.

MetaO e SMAG são tratados como classes de capacidades. O objetivo é verificar se um componente mínimo e desacoplado teria alguma propriedade residual realmente necessária para acoplar implementações heterogêneas por contratos/adapters.

A hipótese deve ser eliminada sempre que uma composição mais simples de soluções existentes for suficiente.

## 2. Regras inegociáveis

### Engenharia de software

Exigir baixo acoplamento, contratos explícitos, substituibilidade, adapters pequenos, isolamento de falhas, estado externo, observabilidade, versionamento, manutenção viável, complexidade proporcional ao benefício e determinismo onde apropriado.

### Evidência empírica

Exigir baseline, tarefas representativas, ambiente controlado, repetições quando necessárias, resultados brutos, failures preservados, custo total, tokens totais, latência, verificação independente, comparação controlada e possibilidade de resultado `INCONCLUSIVE`.

**Propriedade sem evidência = não demonstrada.**

## 3. Objetivo econômico

O objetivo não é reduzir tokens de um agente isolado. É reduzir:

`total system tokens / verified solved task`

Contabilizar pelo menos:

- classification;
- planning/task shaping;
- routing;
- context;
- handoff/bootstrap;
- execution;
- replanning;
- verification.

Não aceitar economia local se planner/orchestrator/context reconstruction consumir o ganho.

## 4. Princípio contextual

Complexidade externa pode existir; complexidade cognitiva entregue ao modelo deve permanecer pequena.

Padrão desejado:

`durable/external state -> selection -> minimal working set -> model`

Capability universe não deve equivaler ao conjunto de capabilities simultaneamente visível ao modelo.

## 5. Componentes que já não justificam um Brain novo

A pesquisa encontrou prior art/implementações suficientes para não reimplementar, salvo evidência extraordinária:

- durable runtime / checkpoint / recovery;
- memória externa e compaction;
- retrieval e adaptive retrieval;
- token/context budgeting;
- tracing, experiment tracking, provenance e dataset versioning;
- registries e capability discovery;
- promotion/statistical gates;
- MCP para ferramentas/capabilities;
- A2A para agentes heterogêneos;
- providers/context providers substituíveis;
- generic workflow engines;
- plan/task reuse;
- planning adaptativo / when-to-plan.

## 6. Interoperabilidade e workflow IR

### A2A

A2A 1.0 é um standard para interoperabilidade entre agentes independentes construídos em diferentes frameworks, linguagens ou vendors. Ele cobre discovery de capabilities, modalidades de interação e collaborative tasks.

Fonte: https://github.com/a2aproject/A2A/blob/main/docs/specification.md

### Microsoft Agent Framework

O Agent Framework atual suporta agentes, workflows explícitos em grafo, MCP, múltiplos providers e context providers. Checkpoints persistem estado dos executores, mensagens pendentes, requests/responses e shared state, permitindo retomada.

Fontes:

- https://learn.microsoft.com/en-us/agent-framework/overview/
- https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints
- https://learn.microsoft.com/en-us/agent-framework/agents/providers/agent-to-agent

O `A2AAgent` encapsula endpoint A2A compatível como `AIAgent` independentemente da tecnologia usada remotamente. Isso enfraquece fortemente qualquer justificativa de criar interoperabilidade própria.

### Open Workflow

Open Workflow deve ser tratado como candidato de alta prioridade para uma representação declarativa/vendor-neutral antes de considerar IR própria. A hipótese atual é que workflow topology e task exchange não precisam ser representados por uma única abstração proprietária.

Separação conceitual preferível:

- workflow/graph standard -> topologia de execução;
- A2A Task -> unidade delegada de trabalho;
- A2A Artifact/Part ou referências externas -> resultados/dados;
- MCP -> ferramentas/capabilities.

**Carga da prova:** demonstrar experimentalmente insuficiência desses standards antes de criar schema/IR nova.

## 7. Task compilation não deve ser obrigatória

LLMCompiler/ReWOO fornecem prior art para separar planning de execution e, em algumas tarefas, reduzir custo/latência.

Por outro lado, estudos compute-controlled mostram que adicionar Planner -> Executor -> Verifier pode aumentar consumo sem ganho proporcional.

Resultado:

`useful task shaping != mandatory LLM planner`

Não usar `PLAN EVERYTHING` como default.

## 8. Baseline econômica mais promissora

A política conceitual que mais sobreviveu é:

1. reutilizar artifact/plano previamente verificado quando seguro;
2. caso contrário, tentar a menor execução plausível;
3. verificar;
4. expandir somente quando houver evidência de insuficiência;
5. recorrer a compile/multi-agent apenas quando tratamentos mais baratos forem insuficientes ou houver benefício empiricamente previsto.

Forma resumida:

`REUSE -> EXECUTE MINIMUM -> VERIFY -> EXPAND`

A ordem ainda deve ser testada. Não é arquitetura congelada.

## 9. Evidência forte para minimum-sufficient execution

O trabalho **Do AI Agents Know When a Task Is Simple? Toward Complexity-Aware Reasoning and Execution** propõe E3 (`Estimate, Execute, Expand`). No MSE-Bench, benchmark determinístico com 121 edições, E3 igualou a baseline mais forte em 100% de sucesso e reportou aproximadamente:

- 91% menos tokens;
- 85% menor custo;
- 92% menos arquivos inspecionados.

O estudo também inclui harness com modelo real e patches verificados por testes reais, embora em escopo menor.

Fonte: https://arxiv.org/abs/2607.13034

Consequência: um Brain/planner novo deve obrigatoriamente vencer uma baseline mínima desse tipo; caso contrário, não há justificativa econômica.

## 10. Evidência para plan reuse

**AgenticCache** reutiliza transições de plano e, em quatro benchmarks multi-agent embodied, reporta em média:

- 50% menos tokens;
- 65% menor latência;
- 22% maior task success nas 12 configurações avaliadas.

Fonte: https://arxiv.org/abs/2604.24039

Conclusão provisória:

`reuse before reasoning again`

Mas isso não justifica cache/planner proprietário dentro do Brain.

## 11. Multi-agent e coordination obesity

Acoplamento disponível não implica acoplamento obrigatório.

Uma arquitetura multi-agent pode aumentar fortemente tokens, latência, bootstrap/handoff e failure modes. Portanto single-executor/direct execution deve permanecer baseline para tarefas onde é suficiente.

Regra:

`avoid replacing context obesity with coordination obesity`

## 12. Handoff

Contextos isolados não implicam menor custo total. Cada executor/subagente pode reconstruir contexto e criar bootstrap tax.

Objetivo conceitual:

`min |handoff| subject to P(success | handoff) >= threshold`

Preferir handoff pequeno, suficiente, referencial e sem replicação do contexto global.

Ainda não foi demonstrado um mecanismo maduro universal que determine automaticamente o `minimum sufficient handoff` para executores heterogêneos e prove ótimo econômico ponta a ponta.

Essa é uma lacuna de pesquisa, **não uma autorização para implementar**.

## 13. Estado atualizado da falsificação

| Possível responsabilidade | Estado |
|---|---|
| registry | eliminada como novidade |
| capability discovery | eliminada como novidade |
| agent protocol/transport | eliminada como novidade |
| tool protocol | eliminada como novidade |
| durable runtime | eliminada como novidade |
| checkpoint/recovery | eliminada como novidade |
| memory/context store | eliminada como novidade |
| generic workflow engine | eliminada como novidade |
| heterogeneous executor boundary | fortemente coberta por A2A/adapters |
| heterogeneous tool boundary | fortemente coberta por MCP |
| provider-neutral workflow representation | fortemente coberta; testar Open Workflow antes de qualquer IR própria |
| plan persistence | eliminada como novidade |
| plan reuse | eliminada como novidade |
| when-to-plan | eliminada como novidade |
| minimum-first execution | prior art empírico forte |
| progressive expansion | prior art empírico forte |
| automatic minimum-sufficient handoff | parcialmente aberta |
| unified economic treatment policy | aberta como questão de pesquisa |
| proof de menor custo total ponta a ponta | aberta |

## 14. Hipótese residual

O Brain deixou de parecer um framework e pode desaparecer completamente.

Pergunta residual:

> Dada uma tarefa, qual é o tratamento suficiente mais barato agora — reuse, direct/minimal execution, reconstruction, compile, parallel/multi-agent — considerando também o custo de decidir essa estratégia?

Formalmente:

`strategy* = argmin E[C_total(strategy)]`

sujeito a uma probabilidade/critério mínimo de sucesso verificado.

Mas a decisão também possui custo:

`C_decision + C_selected < C_naive`

Uma política sofisticada não ganha automaticamente de uma regra quase mecânica `reuse -> minimum -> verify -> expand`.

## 15. Composição concorrente sem Brain

A principal hipótese concorrente agora é uma composição de componentes existentes:

```text
USER/TASK
   |
   v
verified reuse available? ---- yes ---> reuse
   |
   no
   v
minimum viable execution
   |
   v
VERIFICATION
   | success
   +----------------------------> STOP
   |
   | insufficient
   v
EXPAND / compile only now
   |
   v
workflow standard / graph
   |
   +---- A2A ---> heterogeneous agents/executors
   |
   +---- MCP ---> tools/capabilities
   |
   v
external artifacts/state + verifier
```

Runtime, persistence, discovery and transport permanecem substituíveis e externos à política.

## 16. Próxima falsificação

A última justificativa intelectualmente forte para um Brain é:

> Uma composição simples existe no papel, mas seu coordination/handoff/runtime overhead destrói a economia; portanto seria necessária uma microcamada própria.

Próximo protocolo deve comparar:

`C_composition = C_policy + C_workflow + C_A2A/MCP + C_handoff + C_runtime + C_executor + C_verification`

contra pelo menos:

- direct/monolithic baseline;
- reuse -> minimum -> verify -> expand baseline;
- eventual policy/control-plane candidata, somente se necessária.

Medir obrigatoriamente:

- verified task success;
- total tokens / verified solved task;
- total monetary cost / verified solved task;
- planning/policy tokens;
- orchestration/routing tokens;
- executor tokens;
- context tokens;
- verification tokens;
- handoff/bootstrap tokens;
- latency;
- retries;
- replan/expand count;
- tool calls;
- plan reuse rate;
- recovery sem repetir trabalho concluído.

Preservar resultados brutos e failures. Permitir `INCONCLUSIVE`.

## 17. Regra de decisão

**Eliminar antes de construir.**

Um novo componente só sobrevive se demonstrar uma propriedade não atendida por soluções existentes e se essa propriedade produzir mais trabalho correto por menor custo total, sem criar acoplamento ou complexidade desproporcionais.

`Não construir nada` permanece resultado plenamente válido.
