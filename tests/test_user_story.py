from app.domain.user_story import CriterioAceitacao, Priority, UserStory


def _sample_story(**overrides) -> UserStory:
    defaults = dict(
        titulo="Visualizar indicadores de carga do sistema",
        descricao=(
            "Como analista de segurança, eu quero visualizar os indicadores de "
            "carga do sistema para que eu possa identificar anomalias rapidamente"
        ),
        criterios_aceitacao=[
            CriterioAceitacao(
                dado="o usuário está logado no sistema",
                quando="ele acessa a tela de dashboard",
                entao="deve visualizar os indicadores de carga do sistema, atualizados a cada 5 minutos",
            )
        ],
        story_points=3,
        story_points_justificativa="Complexidade baixa: consulta simples a um endpoint já existente.",
        priority=Priority.ALTA,
    )
    defaults.update(overrides)
    return UserStory(**defaults)


def test_user_story_valid_schema():
    story = _sample_story()

    assert story.story_points == 3
    assert story.priority == Priority.ALTA
    assert len(story.criterios_aceitacao) == 1
