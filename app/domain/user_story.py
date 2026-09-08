from enum import Enum

from pydantic import BaseModel, Field, field_validator

FIBONACCI_STORY_POINTS = {1, 2, 3, 5, 8, 13}


class Priority(str, Enum):
    ALTA = "Alta"
    MEDIA = "Média"
    BAIXA = "Baixa"


class CriterioAceitacao(BaseModel):
    """Critério de aceitação no formato Given/When/Then (BDD)."""

    dado: str
    quando: str
    entao: str


class UserStoryInput(BaseModel):
    """Contexto estruturado fornecido ao agente para gerar uma User Story.

    Nomes de campo espelham os placeholders dos prompts validados nos dias
    4-6 (ver docs/prompts-validados-dias-4-6.md), para preencher os
    templates sem tradução.
    """

    descricao_funcionalidade: str
    persona: str
    stack_tecnica: str
    contexto_adicional: str | None = None
    descricao_produto: str | None = None
    regras_de_negocio: str | None = None
    personas_projeto: list[str] | None = None
    sprint_goal: str | None = None


class UserStory(BaseModel):
    """Schema de saída do prompt base (dias 4-6) — anatomia da User Story."""

    titulo: str
    descricao: str = Field(
        description='Formato "Como [persona], eu quero [ação] para que [benefício]"'
    )
    criterios_aceitacao: list[CriterioAceitacao]
    story_points: int = Field(
        description="Story Points sugeridos na escala Fibonacci (1, 2, 3, 5, 8, 13)"
    )
    story_points_justificativa: str
    priority: Priority
    tags: list[str] = Field(default_factory=list)

    # Preenchidos manualmente pelo PO na revisão, não fazem parte da saída do LLM.
    area_path: str | None = None
    iteration_path: str | None = None

    @field_validator("story_points")
    @classmethod
    def _validate_fibonacci(cls, v: int) -> int:
        # Não usamos um IntEnum aqui de propósito: o conversor de schema do
        # google-genai exige que "enum" seja lista de strings, e falha ao
        # receber um enum numérico (erro reproduzido ao testar geração real).
        if v not in FIBONACCI_STORY_POINTS:
            raise ValueError(
                f"story_points={v} não é um valor válido da escala Fibonacci "
                f"{sorted(FIBONACCI_STORY_POINTS)}"
            )
        return v
