# 🧠 BrainFeed CLI

<div align="center">
  <p><strong>O alimentador de contexto definitivo e automatizado para o seu Agente de IA.</strong></p>
  
  [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Typer](https://img.shields.io/badge/CLI-Typer-black?style=for-the-badge)](https://typer.tiangolo.com/)
  [![Rich](https://img.shields.io/badge/UI-Rich-magenta?style=for-the-badge)](https://rich.readthedocs.io/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
</div>

---

## 💡 O Problema que Resolvemos

Construído para desenvolvedores que utilizam IAs e Agentes Autônomos (como Claude Code, Cursor, Aider, etc.) no seu fluxo de trabalho. O BrainFeed resolve o maior problema da geração de código: as **alucinações por falta de contexto atualizado e padrões arquiteturais**.

Enquanto outras ferramentas funcionam como bibliotecas estáticas, o BrainFeed age como um assistente proativo, extraindo documentações da web em tempo real e mapeando a stack do seu projeto automaticamente.

## ✨ Superpoderes (Features)

- 🕷️ **Scraper Sob Demanda (`scrape`):** Precisa usar uma biblioteca nova? Passe a URL da documentação e o BrainFeed extrai o texto, limpa o "lixo visual" (menus, rodapés, scripts) e gera um arquivo Markdown limpo e perfeito para a sua IA consumir.
- 🔍 **Auto-Scan Automático (`scan`):** A ferramenta lê o seu `package.json` (Node.JS/TS), `requirements.txt`/`pyproject.toml` (Python) ou `go.mod` (Go), identifica todas as suas dependências e versões, e gera um manual rigoroso para a IA não errar as versões do seu projeto.
- 📜 **Bíblia do Projeto Local (`rule`):** Crie uma memória local com as regras de negócio e arquitetura do seu time. O BrainFeed exporta automaticamente um arquivo `SKILL.md` na raiz do projeto, garantindo integração nativa com Agentes Autônomos.
- 🔄 **Monitoramento Vivo (`check`):** Compara as assinaturas HTTP (ETag/Last-Modified) das documentações salvas com os servidores originais e avisa se a sua IA está prestes a usar uma API desatualizada.

## 🚀 Como Instalar

Certifique-se de ter o Python 3 instalado na sua máquina.

1. Clone este repositório:
   ```bash
   git clone https://github.com/dpaty/brainfeed.git
   cd brainfeed