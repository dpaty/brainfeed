import typer
import os
from rich.panel import Panel

from utils import console, CONTEXT_DIR
from scraper import extrair_conteudo
from scanner import escanear_projeto

app = typer.Typer(help="BrainFeed - O alimentador de contexto definitivo para o seu Agente de IA.")

def verificar_contexto():
    """Garante que a pasta existe antes de rodar os comandos."""
    if not os.path.exists(CONTEXT_DIR):
        console.print("[bold red]Erro:[/bold red] Pasta de contexto não encontrada. Rode [bold cyan]python main.py init[/bold cyan] primeiro.")
        raise typer.Exit()

@app.command()
def init():
    """ Inicializa o BrainFeed no projeto atual (Cria a pasta de contexto). """
    if not os.path.exists(CONTEXT_DIR):
        os.makedirs(CONTEXT_DIR)
        console.print(f"[bold green]✔ Sucesso![/bold green] Pasta [bold cyan]{CONTEXT_DIR}[/bold cyan] criada.")
    else:
        console.print(f"[bold yellow]Aviso:[/bold yellow] A pasta [bold cyan]{CONTEXT_DIR}[/bold cyan] já existe.")

@app.command()
def scrape(url: str):
    """ Extrai a documentação de uma URL, limpa o lixo visual e converte para Markdown. """
    verificar_contexto()
    console.print(Panel(f"🔍 Buscando documentação em:\n[bold blue]{url}[/bold blue]", title="BrainFeed Scraper"))
    extrair_conteudo(url)

@app.command()
def scan():
    """ Escaneia o projeto local e gera o contexto da Stack para a IA. """
    verificar_contexto()
    escanear_projeto()

@app.command()
def rule(texto: str):
    """ Adiciona uma 'regra de ouro' do projeto para o agente de IA seguir. """
    verificar_contexto()
    rules_file = os.path.join(CONTEXT_DIR, "project_rules.md")

    if not os.path.exists(rules_file):
        with open(rules_file, "w", encoding="utf-8") as f:
            f.write("# 📜 Regras de Ouro do Projeto\n\n")
            f.write("> **Instrução para a IA:** Leia e aplique rigorosamente as regras abaixo ao gerar ou modificar código neste repositório.\n\n")

    with open(rules_file, "a", encoding="utf-8") as f:
        f.write(f"- {texto}\n")

    console.print(f"[bold green]✔ Regra anotada com sucesso![/bold green] A IA agora sabe que: [italic]'{texto}'[/italic]")

if __name__ == "__main__":
    console.print("[bold magenta]⚡ BrainFeed CLI - Contexto para IAs[/bold magenta]")
    console.print("---")
    app()