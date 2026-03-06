import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
import json

app = typer.Typer(help="BrainFeed - O alimentador de contexto definitivo para o seu Agente de IA.")
console = Console()

CONTEXT_DIR = ".brainfeed"

def gerar_nome_arquivo(url: str) -> str:
    """Transforma a URL em um nome de arquivo válido para o sistema."""
    nome = re.sub(r'^https?://', '', url)
    nome = re.sub(r'[^a-zA-Z0-9]', '_', nome)
    return nome.strip('_')[:50] + ".md"

@app.command()
def init():
    """
    Inicializa o BrainFeed no projeto atual (Cria a pasta de contexto).
    """
    if not os.path.exists(CONTEXT_DIR):
        os.makedirs(CONTEXT_DIR)
        console.print(f"[bold green]✔ Sucesso![/bold green] Pasta [bold cyan]{CONTEXT_DIR}[/bold cyan] criada.")
    else:
        console.print(f"[bold yellow]Aviso:[/bold yellow] A pasta [bold cyan]{CONTEXT_DIR}[/bold cyan] já existe.")

@app.command()
def scrape(url: str):
    """
    Extrai a documentação de uma URL, limpa o lixo visual e converte para Markdown.
    """
    if not os.path.exists(CONTEXT_DIR):
        console.print("[bold red]Erro:[/bold red] Pasta de contexto não encontrada. Rode [bold cyan]python main.py init[/bold cyan] primeiro.")
        raise typer.Exit()

    console.print(Panel(f"🔍 Buscando documentação em:\n[bold blue]{url}[/bold blue]", title="BrainFeed Scraper"))

    with console.status("[bold yellow]Baixando e processando a página...[/bold yellow]", spinner="dots"):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["nav", "footer", "script", "style", "header", "aside"]):
                tag.decompose()

            conteudo_principal = soup.find("main") or soup.find("article") or soup.body

            if not conteudo_principal:
                console.print("[bold red]Erro:[/bold red] Não foi possível encontrar conteúdo útil na página.")
                raise typer.Exit()

            markdown_puro = md(str(conteudo_principal), heading_style="ATX")
            nome_arquivo = gerar_nome_arquivo(url)
            caminho_arquivo = os.path.join(CONTEXT_DIR, nome_arquivo)

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(f"\n\n")
                f.write(markdown_puro)

            console.print(f"[bold green]✔ Extração concluída![/bold green] Arquivo salvo em: [bold cyan]{caminho_arquivo}[/bold cyan]")

        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Erro de conexão:[/bold red] Não foi possível acessar a URL.\nDetalhes: {e}")
        except Exception as e:
            console.print(f"[bold red]Erro inesperado:[/bold red] {e}")

@app.command()
def scan():
    """
    Escaneia o projeto local e gera o contexto da Stack para a IA.
    """
    if not os.path.exists(CONTEXT_DIR):
        console.print("[bold red]Erro:[/bold red] Rode [bold cyan]python main.py init[/bold cyan] primeiro.")
        raise typer.Exit()

    stack_info = []
    project_type = "Desconhecido"

    with console.status("[bold yellow]Analisando a stack do projeto...[/bold yellow]", spinner="dots"):
        if os.path.exists("package.json"):
            project_type = "Node.js / JavaScript / TypeScript"
            with open("package.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                deps = data.get("dependencies", {})
                dev_deps = data.get("devDependencies", {})
                
                for dep, ver in deps.items():
                    stack_info.append((dep, ver, "Produção"))
                for dep, ver in dev_deps.items():
                    stack_info.append((dep, ver, "Desenvolvimento"))

        elif os.path.exists("requirements.txt"):
            project_type = "Python"
            with open("requirements.txt", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = re.split(r'[=<>~]+', line)
                        name = parts[0]
                        ver = parts[1] if len(parts) > 1 else "latest"
                        stack_info.append((name, ver, "Produção"))

    if not stack_info:
        console.print("[bold yellow]Nenhum arquivo de dependências (package.json ou requirements.txt) encontrado nesta pasta.[/bold yellow]")
        raise typer.Exit()

    table = Table(title=f"Stack Detectada: {project_type}", style="cyan")
    table.add_column("Biblioteca", style="magenta", justify="left")
    table.add_column("Versão", style="green", justify="center")
    table.add_column("Tipo", style="blue", justify="center")

    for dep, ver, tipo in stack_info:
        table.add_row(dep, ver, tipo)

    console.print(table)

    stack_file = os.path.join(CONTEXT_DIR, "stack_context.md")
    with open(stack_file, "w", encoding="utf-8") as f:
        f.write(f"# Contexto do Projeto: {project_type}\n\n")
        f.write("> **Instrução para a IA:** Abaixo estão as bibliotecas e versões estritas utilizadas neste projeto. Ao gerar código, respeite e utilize exclusivamente estas dependências.\n\n")
        for dep, ver, tipo in stack_info:
            f.write(f"- **{dep}** (Versão: `{ver}`) - {tipo}\n")

    console.print(f"[bold green]✔ Mapa do projeto gerado para a IA em:[/bold green] [bold cyan]{stack_file}[/bold cyan] 🧠")

@app.command()
def rule(texto: str):
    """
    Adiciona uma 'regra de ouro' do projeto para o agente de IA seguir.
    """
    if not os.path.exists(CONTEXT_DIR):
        console.print("[bold red]Erro:[/bold red] Rode [bold cyan]python main.py init[/bold cyan] primeiro.")
        raise typer.Exit()

    rules_file = os.path.join(CONTEXT_DIR, "project_rules.md")
    
    # Se o arquivo não existir, criamos com um cabeçalho bonitinho
    if not os.path.exists(rules_file):
        with open(rules_file, "w", encoding="utf-8") as f:
            f.write("# 📜 Regras de Ouro do Projeto\n\n")
            f.write("> **Instrução para a IA:** Leia e aplique rigorosamente as regras abaixo ao gerar ou modificar código neste repositório.\n\n")

    # Adiciona a nova regra ao arquivo (o "a" é de append)
    with open(rules_file, "a", encoding="utf-8") as f:
        f.write(f"- {texto}\n")

    console.print(f"[bold green]✔ Regra anotada com sucesso![/bold green] A IA agora sabe que: [italic]'{texto}'[/italic]")

if __name__ == "__main__":
    console.print("[bold magenta]⚡ BrainFeed CLI - Contexto para IAs[/bold magenta]")
    console.print("---")
    app()