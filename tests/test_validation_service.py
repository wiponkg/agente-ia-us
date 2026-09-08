from app.domain.user_story import CriterioAceitacao, Priority, UserStory
from app.services.validation_service import validate_user_story


def _story(entao: str, justificativa: str = "Baseado na complexidade da stack.") -> UserStory:
    return UserStory(
        titulo="Corrigir apontamento de arquivo no SharePoint",
        descricao="Como PO, eu quero corrigir apontamentos para que o time não dependa de acesso total",
        criterios_aceitacao=[
            CriterioAceitacao(
                dado="o PO acessa o módulo de Ordem de Serviço",
                quando="ele corrige o apontamento de um arquivo",
                entao=entao,
            )
        ],
        story_points=3,
        story_points_justificativa=justificativa,
        priority=Priority.ALTA,
    )


def test_valid_story_has_no_issues():
    story = _story(
        entao="o sistema deve permitir associar a permissão de escrita sobre Ordens de Serviço ao cargo de PO"
    )

    result = validate_user_story(story)

    assert result.is_valid
    assert result.issues == []


def test_generic_acceptance_criterion_is_flagged():
    """Risco identificado na revisão manual dos prompts (dias 4-6): critério genérico."""
    story = _story(entao="o usuário deve ter acesso")

    result = validate_user_story(story)

    assert not result.is_valid
    assert any("genérico" in issue for issue in result.issues)


def test_missing_story_points_justification_is_flagged():
    """Segundo risco identificado nos dias 4-6: Story Points sem base técnica."""
    story = _story(
        entao="o sistema deve permitir associar a permissão de escrita sobre Ordens de Serviço ao cargo de PO",
        justificativa="   ",
    )

    result = validate_user_story(story)

    assert not result.is_valid
    assert any("justificativa" in issue for issue in result.issues)


def test_duplicate_title_is_flagged():
    story = _story(
        entao="o sistema deve permitir associar a permissão de escrita sobre Ordens de Serviço ao cargo de PO"
    )

    result = validate_user_story(
        story, existing_titles=["Corrigir apontamento de arquivo no SharePoint"]
    )

    assert not result.is_valid
    assert any("duplicata" in issue for issue in result.issues)
