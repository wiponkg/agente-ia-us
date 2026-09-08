"""Módulo de geração de User Stories (dias 9-12).

Implementa os três blocos de prompt validados nos dias 4-6 (ver
docs/prompts-validados-dias-4-6.md): prompt base (fixo, define formato e
schema de saída), prompt de sistema (contexto do projeto + banco few-shot) e
prompt de usuário (a demanda específica). A saída é forçada a JSON
estruturado via response_schema do google-genai, no formato UserStory.
"""

from pathlib import Path

from google import genai
from google.genai import types

from app.core.config import settings
from app.domain.user_story import UserStory, UserStoryInput

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "prompts" / "templates"
FEW_SHOT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "few_shot_examples.md"

MODEL = "gemini-3.5-flash-lite"

_NAO_INFORMADO = "não informado"


def _load_template(name: str) -> str:
    return (TEMPLATES_DIR / name).read_text(encoding="utf-8")


def _build_system_instruction(data: UserStoryInput) -> str:
    base = _load_template("base.md")
    system_template = _load_template("system.md")
    few_shot = FEW_SHOT_PATH.read_text(encoding="utf-8")

    personas = ", ".join(data.personas_projeto) if data.personas_projeto else _NAO_INFORMADO

    system_context = system_template.format(
        descricao_produto=data.descricao_produto or _NAO_INFORMADO,
        stack_tecnica=data.stack_tecnica,
        regras_de_negocio=data.regras_de_negocio or _NAO_INFORMADO,
        personas=personas,
        sprint_goal=data.sprint_goal or _NAO_INFORMADO,
        exemplos_few_shot=few_shot,
    )
    return f"{base}\n\n{system_context}"


def _build_user_prompt(data: UserStoryInput) -> str:
    user_template = _load_template("user.md")
    return user_template.format(
        descricao_funcionalidade=data.descricao_funcionalidade,
        persona=data.persona,
        contexto_adicional=data.contexto_adicional or "nenhum",
    )


def generate_user_story(data: UserStoryInput) -> UserStory:
    client = genai.Client(api_key=settings.google_api_key)

    response = client.models.generate_content(
        model=MODEL,
        contents=_build_user_prompt(data),
        config=types.GenerateContentConfig(
            system_instruction=_build_system_instruction(data),
            response_mime_type="application/json",
            response_schema=UserStory,
        ),
    )

    if response.parsed is None:
        raise ValueError(
            f"Resposta do modelo não pôde ser parseada como UserStory: {response.text}"
        )

    return response.parsed
