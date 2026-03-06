import os
import json
import re
from rich.table import Table
from utils import console, CONTEXT_DIR

def escanear_projeto():
    stack_info = []
    project_type = "Desconhecido"

    with console.status("[bold yellow]Analisando a stack do projeto...[/bold yellow]", spinner="dots"):
        # 1. Node.js
        if os.path.exists("package.json"):
            project_type = "Node.js / JavaScript / TypeScript"
            with open("package.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for dep, ver in data.get("dependencies", {}).items():
                    stack_info.append((dep, ver, "Produção"))
                for dep, ver in data.get("devDependencies", {}).items():
                    stack_info.append((dep, ver, "Desenvolvimento"))

        # 2. Python Clássico (requirements.txt)
        elif os.path.exists("requirements.txt"):
            project_type = "Python (pip)"
            with open("requirements.txt", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = re.split(r'[=<>~]+', line)
                        name = parts[0]
                        ver = parts[1] if len(parts) > 1 else "latest"
                        stack_info.append((name, ver, "Produção"))

        # 3. Python Moderno (pyproject.toml - Poetry, etc)
        elif os.path.exists("pyproject.toml"):
            project_type = "Python (Poetry/PEP 621)"
            with open("pyproject.toml", "r", encoding="utf-8") as f:
                content = f.read()
                # Extração leve usando Regex para não precisar instalar bibliotecas TOML externas
                deps = re.findall(r'^([a-zA-Z0-9_-]+)\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
                for dep, ver in deps:
                    stack_info.append((dep, ver, "Produção"))

        # 4. GoLang (go.mod)
        elif os.path.exists("go.mod"):
            project_type = "Go"
            with open("go.mod", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line.startswith("require "):
                        parts = line.replace("require ", "").strip().split()
                        if len(parts) >= 2: stack_info.append((parts[0].strip('()'), parts[1], "Produção"))
                    elif line and not line.startswith("module") and not line.startswith("go") and not line.startswith(")"):
                        parts = line.split()
                        if len(parts) >= 2 and "." in parts[0]:
                            stack_info.append((parts[0], parts[1], "Produção"))

        if not stack_info:
            console.print("[bold yellow]Nenhum arquivo de dependências suportado encontrado (package.json, requirements.txt, pyproject.toml, go.mod).[/bold yellow]")
            return

    # Montagem visual da tabela
    table = Table(title=f"Stack Detectada: {project_type}", style="cyan")
    table.add_column("Biblioteca", style="magenta", justify="left")
    table.add_column("Versão", style="green", justify="center")
    table.add_column("Tipo", style="blue", justify="center")

    for dep, ver, tipo in stack_info: table.add_row(dep, ver, tipo)
    console.print(table)

    # Geração do Contexto
    stack_file = os.path.join(CONTEXT_DIR, "stack_context.md")
    with open(stack_file, "w", encoding="utf-8") as f:
        f.write(f"# Contexto do Projeto: {project_type}\n\n")
        f.write("> **Instrução para a IA:** Abaixo estão as bibliotecas e versões estritas utilizadas neste projeto. Ao gerar código, respeite e utilize exclusivamente estas dependências.\n\n")
        for dep, ver, tipo in stack_info:
            f.write(f"- **{dep}** (Versão: `{ver}`) - {tipo}\n")

    console.print(f"[bold green]✔ Mapa do projeto gerado para a IA em:[/bold green] [bold cyan]{stack_file}[/bold cyan] 🧠")