# dv

Repositório de pesquisa para avaliar, por falsificação, se existe necessidade de uma camada mínima de integração/composição entre sistemas de governança, executores, runtimes, verificadores e outras capacidades heterogêneas.

## Objetivo canônico

O objetivo não é fundir MetaO + SMAG nem se apegar ao código de qualquer projeto específico.

MetaO e SMAG são referências iniciais de **funções/capacidades**. O `dv` deve poder acoplar um terceiro, quarto ou N-ésimo projeto quando ele tornar o sistema mais completo, barato, performático, verificável ou econômico em tokens.

A unidade de composição é a capacidade, não o repositório.

O sistema deve buscar aproveitar executores gratuitos ou de menor capacidade quando forem suficientes, usando supervisão, verificação, contexto e escalonamento de forma econômica para manter boa qualidade final. Executores mais fortes devem ser usados quando o ganho justificar o custo.

Documento canônico: [`docs/PROJECT-OBJECTIVE.md`](docs/PROJECT-OBJECTIVE.md).

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

> Uma composição de standards/runtimes/providers existentes já consegue escolher e executar o tratamento suficiente mais barato para cada tarefa, sem introduzir coordination/context overhead que destrua a economia?

A baseline conceitual atualmente mais forte é:

`REUSE -> minimum execution -> VERIFY -> EXPAND only if necessary`

Não congelar isso como arquitetura antes de testes.

## Documentação

- [`docs/PROJECT-OBJECTIVE.md`](docs/PROJECT-OBJECTIVE.md) — objetivo canônico, motivação, princípios de composição e condição de sucesso.
- [`docs/research/2026-09-10-brain-falsification.md`](docs/research/2026-09-10-brain-falsification.md) — snapshot da pesquisa, evidências, hipóteses eliminadas e próxima falsificação.
- [`docs/research/2026-09-10-capability-coverage-matrix.md`](docs/research/2026-09-10-capability-coverage-matrix.md) — matriz do que já existe, o que falta provar/adicionar e quais funções podem ser supridas por MetaO, SMAG, standards e outros providers.

## Regra de decisão

Não construir novo registry, protocol, runtime, memory system, generic router, workflow engine ou IR própria sem evidência de uma lacuna que não possa ser atendida por composição simples de soluções existentes.

Não preservar MetaO, SMAG ou qualquer provider por identidade. Preservar apenas capacidades empiricamente úteis e substituíveis.

Resultado válido da pesquisa: **não construir nada**.
