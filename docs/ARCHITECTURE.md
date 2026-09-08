# Arquitetura do Agente de User Story

Entregável da etapa "Arquitetura e Fluxo" (dias 7-8) do cronograma. Documenta
as decisões de stack e o fluxo conversacional do agente, conforme definido em
"Agente de User Story — Atividades". Os módulos core (dias 9-12) já têm uma
primeira versão funcional, construída e testada ao vivo com os prompts
validados nos dias 4-6 (`docs/prompts-validados-dias-4-6.md`).

## Decisões de stack

| Decisão | Escolha | Justificativa |
|---|---|---|
| Modelo de linguagem | Gemini, modelo `gemini-3.5-flash-lite` (`google-genai`) | Já em uso em outros projetos da organização (radar-inteligente-backend, budai-central), evitando setup de credencial/conta novo. Testado ao vivo: `gemini-2.5-flash`/`gemini-2.5-flash-lite` estão descontinuados para novos usuários da conta atual (404) e `gemini-3.6-flash` retornou 503 (alta demanda) no momento do teste — `gemini-3.5-flash-lite` respondeu de forma estável. Reavaliar custo/qualidade vs. GPT-4/Claude/modelo Gemini mais robusto se necessário; o nome do modelo é uma constante isolada em `generation_service.py`, fácil de trocar. |
| Backend | Python 3.13 + FastAPI + uv | Serviço leve, fácil de rodar como CLI local e, futuramente, expor como API (para a extensão do Azure DevOps ou bot do Teams) sem reescrever a lógica core. |
| Interface (fase 1) | CLI (Typer) | Fase 1 não integra com a API do Azure DevOps — a story gerada é revisada e copiada manualmente para o backlog. Chat no Teams e extensão do Azure DevOps ficam previstos para fases futuras. |
| Saída estruturada | `response_schema` do `google-genai` direto no `UserStory` (Pydantic) | Evita parsing manual de JSON. Achado ao testar: o conversor de schema do SDK exige que campos `enum` sejam listas de string — por isso `story_points` é `int` livre com validação Fibonacci via `field_validator`, em vez de um `IntEnum`. |

## Módulos (fase 1)

```
app/
├── cli.py                        # Interface de linha de comando (Typer)
├── core/
│   └── config.py                 # Configuração tipada (pydantic-settings)
├── domain/
│   └── user_story.py             # Schemas: UserStoryInput, UserStory, AcceptanceCriterion
├── services/
│   ├── generation_service.py     # Módulo de geração de User Stories
│   └── validation_service.py     # Módulo de validação de qualidade
└── prompts/
    └── templates/                # Prompt base, de sistema e de usuário (etapa 4-6)
```

- **Módulo de geração** (`generation_service.py`): recebe um `UserStoryInput`
  (funcionalidade, contexto, persona), monta o prompt a partir dos templates
  e chama o Gemini para produzir título, descrição, critérios de aceitação
  (Given/When/Then), Story Points sugeridos (Fibonacci) e prioridade, em
  formato JSON estruturado (`UserStory`).
- **Módulo de validação** (`validation_service.py`): verifica se a story
  segue o formato correto, se os critérios de aceitação são testáveis
  (princípio INVEST) e se não há duplicação com stories já existentes no
  backlog.
- A integração automática com a API do Azure DevOps **não** faz parte desta
  fase — fica prevista para uma etapa futura.

## Fluxo conversacional (fase 1 — CLI)

```
Usuário (PO) → CLI (`agente-user-story generate --feature ... --persona ...`)
   → generation_service.generate_user_story(input)
       → monta prompt (base + sistema + usuário)
       → chama Gemini
       → parseia resposta em UserStory
   → validation_service.validate_user_story(story)
   → CLI imprime a User Story para revisão humana
   → PO ajusta manualmente (Story Points, critérios) e cria o item no Azure DevOps
```

## Pontos de intervenção humana (obrigatórios)

1. Revisão da User Story gerada antes da criação manual do item no Azure DevOps.
2. Ajuste dos Story Points sugeridos pelo time.
3. Validação dos critérios de aceitação antes da criação do item.

O agente é um assistente do Product Owner, não seu substituto.

## Fora de escopo nesta fase

- Integração com a API REST do Azure DevOps (criação automática de itens).
- Interface de chat no Teams.
- Extensão nativa do Azure DevOps.

## Fluxo de trabalho de referência

Este projeto reaproveita, como referência de padrão de código, a
estrutura de serviços de IA do `budai-central` (services organizados por
domínio, chamando `google-genai`) — sem depender do stack Next.js/Firebase
daquele projeto. É um repositório próprio e independente do
`radar-inteligente-backend`.
