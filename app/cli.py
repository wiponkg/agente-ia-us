"""Interface de linha de comando do Agente de User Story (fase 1).

Nesta primeira fase o agente não integra com a API do Azure DevOps: a
User Story gerada é exibida no terminal para revisão humana e cópia manual
para o backlog.
"""

import typer
from rich.console import Console
from rich.panel import Panel

from app.domain.user_story import UserStoryInput
from app.services.generation_service import generate_user_story
from app.services.validation_service import validate_user_story

app = typer.Typer(help="Agente de User Story — assistente do Product Owner")
console = Console()


@app.callback()
def main() -> None:
    """Agente de User Story — assistente do Product Owner.

    Um callback vazio é necessário para o Typer manter "generate" como
    subcomando explícito — sem ele, um Typer app com um único comando
    colapsa e passa a tratar esse comando como a raiz do CLI.
    """


@app.command()
def generate(
    feature: str = typer.Option(..., "--feature", help="Descrição da funcionalidade/demanda"),
    persona: str = typer.Option(..., "--persona", help='Persona alvo, ex: "analista de segurança"'),
    stack: str = typer.Option(
        ..., "--stack", help="Stack técnica envolvida (usada para calibrar Story Points)"
    ),
    product: str = typer.Option(None, "--product", help="Contexto do produto / documento de visão"),
    business_rules: str = typer.Option(None, "--business-rules", help="Regras de negócio relevantes"),
    sprint_goal: str = typer.Option(None, "--sprint-goal", help="Sprint goal atual"),
    context: str = typer.Option(None, "--context", help="Contexto adicional / restrições"),
) -> None:
    """Gera uma User Story a partir de uma funcionalidade, persona e stack técnica."""
    data = UserStoryInput(
        descricao_funcionalidade=feature,
        persona=persona,
        stack_tecnica=stack,
        descricao_produto=product,
        regras_de_negocio=business_rules,
        sprint_goal=sprint_goal,
        contexto_adicional=context,
    )

    story = generate_user_story(data)
    result = validate_user_story(story)

    console.print(Panel(f"[bold]{story.titulo}[/bold]\n\n{story.descricao}", title="User Story gerada"))

    for i, criterio in enumerate(story.criterios_aceitacao, start=1):
        console.print(
            f"[bold]Critério {i}[/bold]\n"
            f"  Dado {criterio.dado}\n"
            f"  Quando {criterio.quando}\n"
            f"  Então {criterio.entao}\n"
        )

    console.print(f"Story Points: {story.story_points} — {story.story_points_justificativa}")
    console.print(f"Priority: {story.priority.value}")
    if story.tags:
        console.print(f"Tags: {', '.join(story.tags)}")

    if result.is_valid:
        console.print("\n[green]Validação: nenhum problema encontrado.[/green]")
    else:
        console.print("\n[yellow]Pontos para revisão antes de levar ao Azure DevOps:[/yellow]")
        for issue in result.issues:
            console.print(f"  - {issue}")

    console.print(
        "\n[dim]Revisão humana obrigatória: ajuste o que for preciso antes de criar "
        "manualmente o item no Azure DevOps.[/dim]"
    )


if __name__ == "__main__":
    app()
