# dv — Coordination Tax / Orchestration Overhead

Status: PESQUISA / FALSIFICAÇÃO
Data: 2026-09-10

## Pergunta

Uma composição de standards, runtimes, adapters, agentes e ferramentas destrói a economia por causa de overhead de coordenação, contexto e handoff?

Objetivo: separar três custos que não devem ser confundidos:

1. overhead de protocolo/runtime/rede;
2. overhead cognitivo que entra no contexto do modelo;
3. overhead de coordenação produzido por chamadas extras, handoffs, planning e verification.

## Evidência atual

### MCP

ProMCP (Findings of ACL 2026) avaliou 20 servidores e 169 ferramentas em diferentes topologias. Em clientes customizados, planning + schema injection responderam por 56–72% dos tokens totais e 60–67% da latência. A execução efetiva das ferramentas foi uma fração pequena do custo.

Fonte: https://aclanthology.org/2026.findings-acl.1967/

Conclusão defensável: MCP em si não é automaticamente caro em tokens; o desenho da exposição de ferramentas/schemas pode ser o principal imposto cognitivo.

### Tool exposure

AgentWeave (2026), em um protocolo BFCL-derived estreito, reduziu em 70.18% as ferramentas expostas, 61.70% os input tokens e 50.95% a latência média do modelo local em relação à exposição de todas as ferramentas. O sucesso absoluto foi baixo e a evidência deve permanecer restrita ao escopo do experimento.

Fonte: https://arxiv.org/abs/2608.23078

How Many Tools Should an LLM Agent See? (2026) mostrou que uma política adaptativa podia manter cobertura próxima a mostrar 50 ferramentas no BFCL enquanto apresentava cerca de 7 em média. Em validação downstream, listas menores/adaptativas também melhoraram seleção da ferramenta correta.

Fonte: https://arxiv.org/abs/2605.24660

ToolScope (ACL 2026) mostrou ganhos de 8.38% a 38.6% em acurácia de seleção de ferramentas por filtragem contextual e fusão/redução de redundância.

Fonte: https://aclanthology.org/2026.acl-long.1573/

Conclusão: `capability universe != model-visible capability set` permanece fortemente suportado.

### A2A e fronteira distribuída

A documentação atual do Microsoft Agent Framework distingue composição in-process de A2A. `Agents as Tools` é descrito como o padrão multi-agent mais leve; cada delegação ainda é uma invocação completa de agente. A2A é recomendado quando existe uma fronteira real entre processos, serviços, linguagens ou equipes; cada chamada A2A adiciona HTTP/network overhead e concerns distribuídos.

Fontes:
- https://learn.microsoft.com/en-us/agent-framework/journey/agents-as-tools
- https://learn.microsoft.com/en-us/agent-framework/journey/agent-to-agent

Um benchmark do SDK a2a-rust mede overhead de transporte/protocolo na ordem de microssegundos/milisegundos em loopback e mostra um workflow de 7 passos em aproximadamente 1.45 ms de overhead do SDK. Isso é evidência de implementação, não benchmark universal de A2A nem de agentes reais.

Fonte: https://a2a-rust.com/reference/benchmarks.html

Conclusão defensável: protocolo/rede podem adicionar latência e complexidade operacional, mas o grande custo econômico de um sistema de agentes tende a aparecer quando a fronteira força mais chamadas de modelo, handoffs/context reconstruction ou schemas no prompt.

### Multi-agent

A Anthropic reportou que seu sistema multi-agent de pesquisa superou o single-agent em 90.2% em uma avaliação interna de pesquisa ampla e paralelizável. Porém, agentes usaram cerca de 4x mais tokens que chat e sistemas multi-agent cerca de 15x mais tokens que chat. A própria Anthropic destaca que tarefas com dependências fortes e contexto compartilhado — incluindo muitas tarefas de programação — são pior encaixe para multi-agent.

Fonte: https://www.anthropic.com/engineering/multi-agent-research-system

Conclusão: multi-agent pode justificar custo quando o ganho de qualidade/parallelism paga por ele; não deve ser default.

### Planner / Executor

Uma avaliação compute-controlled de planner-executor em TravelPlanner encontrou ganho em uma dimensão de satisfação de constraints, mas não ganho suficiente em validade global nem retorno por token em nenhuma condição testada.

Fonte: https://essay.utwente.nl/essays/111014

Conclusão: adicionar planner não pode ser considerado melhoria econômica por arquitetura; deve vencer uma baseline com orçamento comparável.

### Verification tax

Verificação também possui custo e deve entrar no denominador econômico. Trabalhos recentes tratam explicitamente verification cost como dimensão de avaliação, e pesquisas de alocação adaptativa mostram que verificar seletivamente pode reduzir chamadas de verifier.

Fontes:
- https://arxiv.org/abs/2608.08709
- https://arxiv.org/abs/2602.03975

Conclusão: `EXECUTE -> VERIFY -> EXPAND` não é economicamente gratuito. O protocolo do dv deverá separar verificadores determinísticos baratos (tests, schema, typecheck, hash, policy) de verificadores LLM/judge caros.

## Resultado atual da falsificação

| Hipótese | Estado | Razão |
|---|---|---|
| A2A/MCP por si só destroem economia de tokens | NÃO DEMONSTRADA | overhead de protocolo não equivale a tokens; schema/context exposure é o ponto crítico |
| Expor todas as capabilities ao modelo é aceitável | FALSIFICADA para tool-rich settings avaliados | múltiplos estudos mostram custo/queda de seleção |
| Multi-agent deve ser default | FALSIFICADA | custo em tokens é alto e benefício é task-dependent |
| Planner deve ser default | FALSIFICADA | evidência compute-controlled não mostra retorno por token universal |
| Local/in-process fast path é desejável | SOBREVIVE | menor boundary tax; compatível com MAF Agents-as-Tools |
| A2A deve ser usado só quando uma fronteira real justificar | SOBREVIVE | alinhado à documentação atual do MAF |
| Progressive disclosure/capability filtering é economicamente promissor | SOBREVIVE FORTE | evidência empírica convergente |
| Coordination tax justifica um Brain novo | NÃO DEMONSTRADA | ainda não há evidência de que uma microcamada própria vença composição simples |

## Implicação para o dv

A composição candidata deve preferir uma hierarquia de menor custo:

```text
same-process / direct capability
        |
        v
agent-as-tool / local adapter
        |
        v
MCP / external tool boundary when useful
        |
        v
A2A only for genuine remote/heterogeneous agent boundary
        |
        v
workflow / multi-agent only when task requires it
```

Isto não é arquitetura congelada. É uma hipótese de teste derivada de evidência atual.

A política deve minimizar não só network hops, mas principalmente:

- schemas/model-visible tools;
- model invocations;
- handoff/bootstrap tokens;
- context reconstruction;
- planning calls;
- verifier calls;
- retries/replans.

## Próxima falsificação

Executar/definir protocolo que compare, com a mesma classe de tarefa e oracle:

A. direct single executor;
B. direct + progressive capability filtering;
C. local agent-as-tool;
D. MCP tool composition;
E. A2A delegated executor;
F. workflow/multi-agent apenas onde aplicável.

Medir por braço:

- verified success;
- total input/output tokens;
- model invocation count;
- tool-schema tokens;
- handoff/context tokens;
- verifier tokens;
- retries/replans;
- wall-clock latency;
- monetary cost;
- `total tokens / verified solved task`.

Resultado permitido: PASS, FAIL ou INCONCLUSIVE.

## Regra

Não confundir interoperabilidade disponível com interoperabilidade obrigatória.

`system coordination overhead != model cognitive overhead`

A camada do dv só será justificável se reduzir custo total ou aumentar qualidade verificada de forma suficiente para compensar seu próprio overhead.