import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from utils import console, CONTEXT_DIR, gerar_nome_arquivo

def extrair_conteudo(url: str):
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
                return False

            markdown_puro = md(str(conteudo_principal), heading_style="ATX")
            nome_arquivo = gerar_nome_arquivo(url)
            caminho_arquivo = os.path.join(CONTEXT_DIR, nome_arquivo)

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(f"\n\n")
                f.write(markdown_puro)

            console.print(f"[bold green]✔ Extração concluída![/bold green] Arquivo salvo em: [bold cyan]{caminho_arquivo}[/bold cyan]")
            return True

        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]Erro de conexão:[/bold red] Não foi acessar a URL.\nDetalhes: {e}")
        except Exception as e:
            console.print(f"[bold red]Erro inesperado:[/bold red] {e}")
        return False