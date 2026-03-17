import re
import os
import json
from datetime import datetime
from rich.console import Console

CONTEXT_DIR = ".brainfeed"
MANIFEST_FILE = os.path.join(CONTEXT_DIR, "manifest.json")
console = Console()

def gerar_nome_arquivo(url: str) -> str:
    """Transforma a URL em um nome de arquivo válido para o sistema."""
    nome = re.sub(r'^https?://', '', url)
    nome = re.sub(r'[^a-zA-Z0-9]', '_', nome)
    return nome.strip('_')[:50] + ".md"

def salvar_no_manifesto(url: str, nome_arquivo: str, etag: str = None, last_modified: str = None):
    """Salva os metadados da captura para futura verificação de atualizações."""
    dados = {}
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = {}
    
    dados[url] = {
        "arquivo": nome_arquivo,
        "ultima_captura": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "etag": etag,
        "last_modified": last_modified
    }
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)