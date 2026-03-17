import typer
import os
import json
import requests
from rich.panel import Panel
from rich.table import Table

from utils import console, CONTEXT_DIR, MANIFEST_FILE
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

@app.command()
def check():
    """ Verifica se as documentações salvas ainda estão atualizadas em relação à web. """
    verificar_contexto()
    
    if not os.path.exists(MANIFEST_FILE):
        console.print("[bold yellow]Aviso:[/bold yellow] Nenhum manifesto encontrado. Rode [bold cyan]python main.py scrape <url>[/bold cyan] primeiro.")
        return

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        try:
            dados = json.load(f)
        except json.JSONDecodeError:
            console.print("[bold red]Erro:[/bold red] Arquivo manifest.json corrompido.")
            return

    table = Table(title="🔍 Verificação de Sincronia de Contexto", style="magenta")
    table.add_column("URL", style="blue")
    table.add_column("Status", justify="center")
    table.add_column("Última Captura", style="green")

    with console.status("[bold yellow]Checando servidores remotos (via HEAD)...[/bold yellow]", spinner="dots"):
        for url, info in dados.items():
            try:
                res = requests.head(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
                novo_etag = res.headers.get('ETag')
                nova_data = res.headers.get('Last-Modified')
                
                desatualizado = False
                # Só acusa desatualizado se o servidor forneceu o dado antes E agora ele está diferente
                if info.get('etag') and novo_etag and novo_etag != info['etag']:
                    desatualizado = True
                elif info.get('last_modified') and nova_data and nova_data != info['last_modified']:
                    desatualizado = True
                
                if desatualizado:
                    status = "[bold red]🔄 DESATUALIZADO[/bold red]"
                else:
                    status = "[bold green]✅ EM DIA[/bold green]"
                
            except Exception:
                status = "[bold yellow]❓ OFFLINE/ERRO[/bold yellow]"
            
            table.add_row(url, status, info.get('ultima_captura', 'Desconhecido'))

    console.print(table)
    console.print("\n[italic]Dica: Se o status for [bold red]DESATUALIZADO[/bold red], rode o comando [bold cyan]scrape <url>[/bold cyan] novamente para atualizar seu contexto local.[/italic]")

if __name__ == "__main__":
    console.print("[bold magenta]⚡ BrainFeed CLI - Contexto para IAs[/bold magenta]")
    console.print("---")
    app()