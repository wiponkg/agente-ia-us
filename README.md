# Agente de User Story

Agente de IA que auxilia o Product Owner a gerar User Stories para o Azure
DevOps a partir de contexto estruturado (produto, técnico, negócio, sprint e
persona). Ver o plano completo em `docs/ARCHITECTURE.md`.

> Status: esqueleto de arquitetura (dias 7-8 do cronograma). O módulo de
> geração e o módulo de validação ainda não estão implementados — ver `TODO`s
> em `app/services/`.

## Stack

- Python 3.13
- FastAPI (interface futura) + Typer (CLI, fase 1)
- Gemini via `google-genai`
- Gerenciador de dependências: [`uv`](https://docs.astral.sh/uv/)

## Setup

```bash
cp .env.example .env
# preencher GOOGLE_API_KEY em .env
uv sync
```

## Uso (CLI)

```bash
uv run agente-user-story generate --feature "..." --persona "analista de segurança"
```

## Testes

```bash
uv run pytest
```
