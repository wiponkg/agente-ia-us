"""Módulo de validação de qualidade (dias 9-12).

Checagens estruturais e heurísticas rodadas antes da revisão humana. Cobrem
os dois riscos identificados na revisão manual dos prompts (dias 4-6):
critérios de aceitação genéricos e Story Points sem base técnica — além do
formato geral e de duplicação contra o backlog (contexto histórico). Não
substitui a revisão do Product Owner.
"""

from dataclasses import dataclass, field
from difflib import SequenceMatcher

from app.domain.user_story import UserStory

GENERIC_PHRASES = [
    "deve ter acesso",
    "deve funcionar corretamente",
    "deve estar disponível",
    "deve funcionar como esperado",
]

DUPLICATE_SIMILARITY_THRESHOLD = 0.85
TITLE_MAX_WORDS = 10


@dataclass
class ValidationResult:
    is_valid: bool
    issues: list[str] = field(default_factory=list)


def _is_generic(texto: str) -> bool:
    lowered = texto.lower()
    return any(phrase in lowered for phrase in GENERIC_PHRASES)


def validate_user_story(
    story: UserStory, existing_titles: list[str] | None = None
) -> ValidationResult:
    issues: list[str] = []

    if not story.criterios_aceitacao:
        issues.append("Story sem nenhum critério de aceitação (viola Testable do INVEST).")

    for i, criterio in enumerate(story.criterios_aceitacao, start=1):
        if not (criterio.dado.strip() and criterio.quando.strip() and criterio.entao.strip()):
            issues.append(f"Critério {i} incompleto — faltam partes do Given/When/Then.")
        elif _is_generic(criterio.entao):
            issues.append(
                f"Critério {i} parece genérico — deve citar a permissão, ação ou "
                "regra de negócio específica (ver prompt base, dias 4-6)."
            )

    if not story.story_points_justificativa.strip():
        issues.append("Story Points sem justificativa baseada na stack técnica.")

    if len(story.titulo.split()) > TITLE_MAX_WORDS:
        issues.append(f"Título ultrapassa {TITLE_MAX_WORDS} palavras.")

    for existing in existing_titles or []:
        similarity = SequenceMatcher(None, story.titulo.lower(), existing.lower()).ratio()
        if similarity >= DUPLICATE_SIMILARITY_THRESHOLD:
            issues.append(
                f'Possível duplicata do backlog: "{existing}" (similaridade {similarity:.0%}).'
            )

    return ValidationResult(is_valid=not issues, issues=issues)
