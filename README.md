# dv

Repositório de pesquisa para avaliar, por falsificação, se existe necessidade de um novo componente de controle entre sistemas do tipo MetaO, SMAG e executores heterogêneos.

## Estado atual

**Pesquisa apenas. Não implementar arquitetura ainda.**

A hipótese de um novo `brain`/kernel está sendo ativamente reduzida. O objetivo é provar que ele é desnecessário antes de propor qualquer software novo.

Critério principal:

> engenharia de software defensável + evidência empírica + economia de tokens totais por trabalho verificadamente resolvido.

Métrica norteadora:

`total system tokens / verified solved task`

O custo total deve incluir classificação, planejamento, routing, contexto, handoff, execução, replanning e verificação.

## Hipótese residual

Grande parte da infraestrutura inicialmente atribuída ao possível Brain já possui prior art ou implementações maduras: durable execution, checkpoints, memória externa, retrieval, context providers, capability discovery, A2A, MCP, workflow engines, plan reuse e planning adaptativo.

A pergunta residual é menor:

> Uma composição de standards/runtimes existentes já consegue escolher e executar o tratamento suficiente mais barato para cada tarefa, sem introduzir coordination/context overhead que destrua a economia?

A baseline conceitual atualmente mais forte é:

`REUSE -> minimum execution -> VERIFY -> EXPAND only if necessary`

Não congelar isso como arquitetura antes de testes.

## Documentação

- [`docs/research/2026-09-10-brain-falsification.md`](docs/research/2026-09-10-brain-falsification.md) — snapshot da pesquisa, evidências, hipóteses eliminadas e próxima falsificação.
- [`docs/research/2026-09-10-capability-coverage-matrix.md`](docs/research/2026-09-10-capability-coverage-matrix.md) — matriz do que já existe, o que falta provar/adicionar e quais funções podem ser supridas por MetaO, SMAG e standards externos.

## Regra de decisão

Não construir novo registry, protocol, runtime, memory system, generic router, workflow engine ou IR própria sem evidência de uma lacuna que não possa ser atendida por composição simples de soluções existentes.

Resultado válido da pesquisa: **não construir nada**.
