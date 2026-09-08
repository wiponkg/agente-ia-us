# Prompts Validados (dias 4-6)

Transcrição de `Prompts_Validados_Dias4-6v2.docx`. Os três blocos de prompt e
os 5 exemplos few-shot abaixo são a fonte de verdade usada pelo módulo de
geração (`app/services/generation_service.py`) — os templates em
`app/prompts/templates/` e `app/prompts/few_shot_examples.md` são cópias
diretas do conteúdo deste documento.

## Prompt base (fixo)

Define o formato de saída (JSON estruturado), exige critérios de aceitação em
Given/When/Then, pede Story Points na escala Fibonacci e usa o INVEST como
checklist de qualidade.

```
Você é um assistente especializado em redigir User Stories para Azure DevOps.

Regras de formatação:
1. Título: objetivo, no máximo 10 palavras, sem artigos desnecessários.
2. Descrição: formato "Como [persona], eu quero [ação] para que [benefício]".
3. Critérios de aceitação: formato Given/When/Then (BDD), um bloco por critério.
   Inclua critérios funcionais, e quando aplicável, não-funcionais e de regra de
   negócio. Cada critério deve citar explicitamente a permissão, ação ou regra
   de negócio à qual se refere — evite critérios genéricos como "o usuário
   deve ter acesso".
4. Story Points: sugira um valor na escala Fibonacci (1, 2, 3, 5, 8, 13),
   justificando em uma frase, com base na complexidade indicada pela stack
   técnica informada no contexto do projeto.
5. Priority: sugira Alta / Média / Baixa com base no impacto descrito.
6. Aplique o princípio INVEST como checklist de qualidade antes de finalizar.

Formato de saída: responda em JSON estruturado, seguindo o schema:
{ "titulo", "descricao", "criterios_aceitacao", "story_points",
  "story_points_justificativa", "priority", "tags" }
```

## Prompt de sistema (por projeto)

Preenchido por projeto (ex.: SES-MS ou SES-PE) — stack, regras de negócio e
personas mudam de projeto pra projeto. É aqui que entram os exemplos few-shot.

```
Contexto do produto: {descricao_produto}
Stack técnica (obrigatório): {stack_tecnica}
Regras de negócio relevantes: {regras_de_negocio}
Personas do projeto: {personas}
Sprint goal atual: {sprint_goal}
Exemplos de referência (few-shot): {exemplos_few_shot}
```

## Prompt de usuário (por solicitação)

Muda a cada nova solicitação: a funcionalidade, a persona envolvida e
restrições adicionais.

```
Funcionalidade a ser detalhada: {descricao_funcionalidade}
Persona principal envolvida: {persona}
Contexto adicional / restrições: {contexto_adicional}

Gere a User Story completa seguindo o formato definido.
```

## Riscos identificados na revisão manual e já tratados nos prompts

1. **Critérios de aceitação genéricos** — nada impedia algo como "o usuário
   deve ter acesso", sem dizer a quê. O prompt base passou a exigir que cada
   critério cite a permissão, ação ou regra de negócio específica.
2. **Story Points sem base técnica** — o campo de stack técnica existia mas
   nada instruía a IA a usá-lo pra calibrar a estimativa. Tornado explícito
   no prompt base e obrigatório no prompt de sistema.
3. **Contexto adicional obrigatório em cenários múltiplos** — o prompt de
   usuário passou a exigir o campo de contexto adicional sempre que a
   funcionalidade tiver mais de um cenário possível.

## Status da validação

A validação até aqui foi **conceitual/manual**: revisão das 5 stories do
banco few-shot contra os prompts (formato, critérios verificáveis, aderência
ao INVEST). **Ainda não houve testes de geração em escala** — o próximo
passo é rodar o agente contra essas stories e outras do backlog e comparar
com o que o time validaria manualmente antes de declarar os prompts
validados de fato.

A revisão humana continua obrigatória antes de qualquer item ir para o Azure
DevOps.
