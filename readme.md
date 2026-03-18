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
   git clone [https://github.com/dpaty/brainfeed.git](https://github.com/dpaty/brainfeed.git)
   cd brainfeed
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Como Usar

O BrainFeed possui uma interface de terminal (CLI) rica e intuitiva. 

### 1. Inicializar o projeto
Cria a pasta `.brainfeed` na raiz do seu projeto.
```bash
python main.py init
```

### 2. Escanear a Stack Tecnológica
Analisa o projeto e gera o arquivo `stack_context.md` blindando as versões para a IA.
```bash
python main.py scan
```

### 3. Extrair Documentação da Web
Baixa e converte qualquer página web para Markdown.
```bash
python main.py scrape [https://docs.exemplo.com/api](https://docs.exemplo.com/api)
```

### 4. Monitorar a Saúde do Contexto
Verifica rapidamente se alguma das documentações que você baixou foi atualizada na web.
```bash
python main.py check
```

### 5. Adicionar Regras do Projeto (Integração SKILL.md)
Adiciona diretrizes rápidas na sua "Bíblia do Projeto" e gera automaticamente o arquivo `SKILL.md` para os Agentes de IA lerem na raiz do repositório.
```bash
python main.py rule "Sempre use tipagem estática nas funções em Python."
```

## 🏗️ Arquitetura do Projeto

O projeto foi construído de forma modular para facilitar a manutenção e escalabilidade:

```text
brainfeed/
├── .brainfeed/    # O "cérebro" gerado com seus arquivos .md e manifest.json
├── main.py        # Ponto de entrada da CLI (Typer)
├── scanner.py     # Lógica de detecção de stack (Python, Node.js, Go)
├── scraper.py     # Lógica de extração e conversão Web -> Markdown
├── utils.py       # Configurações globais e funções utilitárias
└── SKILL.md       # Arquivo exportado com as regras para Agentes Autônomos
```

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Quer adicionar suporte a novas linguagens no scanner ou melhorar o scraper? 

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/NovaFuncionalidade`)
3. Faça o Commit de suas mudanças (`git commit -m 'feat: Adiciona NovaFuncionalidade'`)
4. Faça o Push para a Branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---
<div align="center">
  Desenvolvido com ☕ e 🧠 por <a href="https://github.com/dpaty">Dior Intelligence</a>.
</div>