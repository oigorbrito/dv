# dv — Objetivo Canônico do Projeto

Status: CANÔNICO PARA A PESQUISA
Data: 2026-09-10

## 1. Objetivo

O objetivo do `dv` é construir, somente se empiricamente justificado, uma camada mínima de integração/composição capaz de acoplar projetos e ferramentas independentes por suas **capacidades**, sem depender de suas implementações internas.

MetaO e SMAG são referências iniciais porque materializam funções úteis, mas **não são dependências obrigatórias nem limites do sistema**. Se um terceiro, quarto, quinto ou décimo projeto acrescentar uma capacidade melhor, mais barata, mais madura, mais interoperável ou mais eficiente, ele deve poder ser incorporado sem reconstruir o núcleo.

A unidade de composição é a **função/capacidade**, não o código, linguagem, framework ou repositório de origem.

## 2. Origem da reavaliação

A decisão de reavaliar a direção anterior de MetaO e SMAG foi provocada pela análise de projetos externos, em especial o OpenManus (`FoundationAgents/OpenManus`).

Ao observar uma abordagem modular capaz de combinar agentes, ferramentas e fluxos de execução, surgiu a hipótese de que manter e evoluir isoladamente dois sistemas próprios poderia ser menos eficiente do que compor capacidades maduras de vários projetos por uma camada de integração estreita.

Esse episódio é o **gatilho histórico da reavaliação**, não evidência suficiente para copiar a arquitetura do OpenManus nem para adotá-lo como dependência obrigatória.

Regra decorrente:

> Quando um projeto externo demonstrar uma ideia, capacidade ou composição potencialmente superior, o `dv` deve reavaliar sua direção em vez de preservar decisões anteriores por inércia.

A comparação deve continuar submetida a engenharia de software defensável e validação empírica. Uma arquitetura aparentemente madura, elegante ou popular é somente candidata até ser testada no contexto e nas métricas relevantes do `dv`.

## 3. Motivação

O ecossistema de agentes, executores, runtimes, protocolos e ferramentas evolui rápido demais para que um único desenvolvedor acompanhe, reimplemente e mantenha internamente todas as melhores soluções.

Por isso, o projeto deve favorecer composição e substituição em vez de reprodução de funcionalidades existentes.

A camada proposta deve absorver diferenças de implementação por standards, contratos ou adapters pequenos, mantendo o restante do sistema desacoplado.

## 4. Resultado funcional desejado

O sistema composto deve buscar, quando demonstrável:

- melhor qualidade final de resposta/entrega;
- menor custo monetário total;
- menor consumo total de tokens por tarefa verificadamente resolvida;
- uso eficiente de executores gratuitos ou de menor capacidade quando suficientes;
- capacidade de escalar para executores mais fortes somente quando necessário;
- supervisão, verificação e correção independentes da confiança no executor;
- substituição de componentes sem reconstrução global;
- combinação de múltiplos projetos quando a composição produzir ganho real;
- evitar multi-agent, planning ou orchestration quando um caminho simples já for suficiente.

Lentidão de um executor gratuito não é, por si só, defeito eliminatório. Se a composição conseguir entregar resultado verificadamente correto com custo significativamente menor e latência ainda aceitável para o caso de uso, esse trade-off deve ser medido e pode ser vantajoso.

## 5. MetaO e SMAG: conceitos, não código

Do MetaO interessa principalmente a classe de funções como:

- seleção/estratégia;
- governança;
- policy/budget/approval;
- supervisão;
- admission/health/certification;
- recovery/failover/replan;
- evidência;
- independent acceptance.

Do SMAG interessa principalmente a classe de funções como:

- governança de execução;
- seleção/substituição de executor;
- supervisão do processo executor;
- staging/isolamento;
- auditoria independente;
- acceptance;
- promoção ou bloqueio;
- rollback;
- evidência e proveniência da execução.

Essas listas não significam que o código do MetaO ou do SMAG será incorporado. Cada função pode ser suprida por:

- MetaO;
- SMAG;
- outro projeto;
- um standard;
- um serviço externo;
- uma composição de vários componentes;
- ou nenhuma camada adicional, se a função não for necessária para determinada tarefa.

## 6. Princípio de extensibilidade

Forma conceitual:

```text
TASK / GOAL
    |
    v
minimal composition / integration layer
    |
    +--> capability provider A
    +--> capability provider B
    +--> capability provider C
    +--> future provider N
    |
    v
executor(s) / tools / verifier(s)
    |
    v
verified result
```

O componente de integração não deve conhecer detalhes internos desnecessários dos providers. Preferir standards existentes (por exemplo A2A, MCP e workflow standards) e adapters estreitos antes de criar protocolos próprios.

## 7. Objetivo econômico

Métrica principal:

`total system tokens / verified solved task`

A avaliação deve contabilizar o sistema inteiro, incluindo quando aplicável:

- classificação;
- seleção;
- planning/task shaping;
- retrieval/context;
- routing;
- handoff/bootstrap;
- execução;
- retries;
- replanning/expansion;
- supervisão;
- auditoria/verificação;
- coordenação entre componentes.

Economia de tokens em um executor não conta como ganho se o restante do sistema consumir a economia.

Também medir:

- monetary cost / verified solved task;
- verified task success;
- latency;
- retries/replans;
- number of model calls;
- handoff/context size;
- executor tier/model usado;
- capacidade de usar opção gratuita/barata sem perda inaceitável de qualidade.

## 8. Estratégia operacional provisória

A pesquisa atual favorece como baseline, ainda não como arquitetura congelada:

```text
REUSE verified artifact/plan when safe
        |
otherwise
        v
minimum plausible execution
        |
        v
VERIFY
  | success
  +-------> STOP
  |
  | insufficient
  v
EXPAND / stronger executor / more context / planning / composition
```

A ideia é não pagar antecipadamente por inteligência, contexto ou orquestração que talvez não sejam necessários.

## 9. Regra de evolução

O `dv` deve permanecer proativo em relação ao ecossistema:

1. descobrir projetos/standards relevantes;
2. identificar a capacidade que fornecem;
3. comparar maturidade, custo, interoperabilidade e evidência;
4. testar se podem substituir ou complementar providers existentes;
5. preferir composição simples à implementação própria;
6. preservar providers como substituíveis;
7. remover ou trocar componentes quando surgir solução empiricamente superior.

Portanto, a arquitetura futura deve permitir evolução do ecossistema sem exigir que o mantenedor acompanhe internamente cada implementação.

## 10. Regra fixa de admissibilidade

Nenhuma capacidade, componente, arquitetura ou decisão do `dv` é considerada aprovada apenas por plausibilidade, popularidade, elegância ou porque funciona isoladamente.

Toda decisão relevante deve ser sustentada por dois eixos:

1. **Engenharia de software defensável** — baixo acoplamento, contratos claros, substituibilidade, isolamento de falhas, manutenção viável, segurança, observabilidade e complexidade proporcional ao benefício.
2. **Evidência empírica adequada à alegação** — baseline, tarefas representativas, métricas predefinidas, execução real quando necessária, resultados brutos e falhas preservados, comparação controlada e possibilidade explícita de resultado `INCONCLUSIVE`.

Regras:

- `boa ideia != aprovada`;
- `código funcionando != arquitetura aprovada`;
- `documentado != executado`;
- `benchmark isolado != superioridade geral`;
- `popularidade != evidência`;
- `evidência insuficiente -> INCONCLUSIVE`.

## 11. Regra de decisão

Não se apegar ao código de MetaO, SMAG ou qualquer outro projeto.

Não preservar uma implementação por identidade, autoria ou histórico.

Preservar somente capacidades cujo benefício seja demonstrado.

Um provider novo deve ser aceito quando satisfizer o contrato necessário e demonstrar melhor relação entre qualidade, custo, tokens, latência, confiabilidade e manutenção para o escopo avaliado.

Um provider existente deve poder ser removido quando deixar de ser competitivo ou necessário.

## 12. Condição de sucesso do projeto

O projeto terá sucesso se conseguir demonstrar uma composição substituível que faça ferramentas e executores heterogêneos trabalharem juntos com resultado verificável e custo total competitivo — inclusive aproveitando executores gratuitos ou mais fracos quando suficientes — sem criar um novo monólito difícil de manter.

O sucesso não exige usar MetaO ou SMAG.

O sucesso não exige criar um Brain.

O sucesso pode inclusive ser demonstrar que standards + adapters + providers existentes já são suficientes e que quase nenhum código novo é necessário.
