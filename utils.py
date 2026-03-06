import re
from rich.console import Console

CONTEXT_DIR = ".brainfeed"
console = Console()

def gerar_nome_arquivo(url: str) -> str:
    """Transforma a URL em um nome de arquivo válido para o sistema."""
    nome = re.sub(r'^https?://', '', url)
    nome = re.sub(r'[^a-zA-Z0-9]', '_', nome)
    return nome.strip('_')[:50] + ".md"