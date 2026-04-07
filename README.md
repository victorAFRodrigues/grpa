# GRPA — Goevo Robot Process Automation

O **GRPA** é um ecossistema de automação robótica de processos (RPA) desenvolvido em Python, integrado ao software **GOEVO**. Ele utiliza **Playwright** para automação de navegador e segue uma arquitetura modular focada em escalabilidade, reutilização de código e facilidade de manutenção.

Este repositório serve como um **boilerplate completo** para o desenvolvimento de novas automações.

---

## 📋 Índice

- [Configuração do Ambiente](#️-configuração-do-ambiente)
- [Execução em Desenvolvimento](#-execução-em-desenvolvimento)
- [Execução em Produção](#️-execução-em-produção)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Desenvolvendo uma Nova Automação](#-desenvolvendo-uma-nova-automação)
- [Recursos do Boilerplate](#️-recursos-do-boilerplate)
- [Padrões de Desenvolvimento](#-padrões-de-desenvolvimento)

---
 

## 🛠️ Requisitos

- Python 3.14+ instalado e disponível no PATH.

> ❗ Todas as dependências e configurações serão gerenciadas pelo wizard `setup.py`.

---

## ⚙️ Configuração do Ambiente

O **wizard de setup** (`setup.py`) é o único passo necessário para configurar o ambiente local. Ele irá:

1. Guiá-lo pelo preenchimento das variáveis de ambiente essenciais.  
2. Criar automaticamente o arquivo `.env`.  
3. Configurar o atalho `grpa` no terminal para execução da ferramenta.

**Para rodar o wizard:**

```bash
python setup.py
```
Após o setup, reinicie o terminal ou execute . $PROFILE (PowerShell) / source ~/.bashrc (Linux/Mac) para ativar o atalho grpa.

> Após o setup, reinicie o terminal ou execute `. $PROFILE` (PowerShell) / `source ~/.bashrc` (Linux/Mac) para ativar o atalho `grpa`.

### Opção B — Configuração manual

Copie o arquivo de exemplo e preencha as variáveis manualmente:

```bash
cp .envexample .env
```

Variáveis obrigatórias:

| Variável | Descrição |
|---|---|
| `API_URL` | URL base da API do GOEVO (ex: `https://empresa.goevo.net/API/v1/?Empresa/RPAManager`) |
| `GOEVO_APP_TPTOKEN` | Token de autenticação do app no GOEVO |
| `RPA_EXECUTOR` | Nome identificador deste executor (ex: `SRV_RPA_001`) |
| `GRPA_AUTOMATION_VERSION` | Versão atual dos módulos de automação (ex: `2.0.0.20260306`) |

Variável opcional:

| Variável | Descrição | Padrão |
|---|---|---|
| `ENV` | Modo de execução: `DOCKER` (headless) ou `LOCAL` (com janela) | `DOCKER` |

> ⚠️ **Docker:** O setup automático não se aplica a ambientes Docker. Use obrigatoriamente a **Opção B** e garanta que o `.env` esteja preenchido antes de subir os containers.

---

## 🚀 Execução em Desenvolvimento

### 1. Sem Docker (Local)

Ideal para debug e criação de novos scripts onde você precisa ver o navegador funcionando (`headless=False`).

**Pré-requisitos:**
- Python 3.14+
- [uv](https://github.com/astral-sh/uv) — gerenciador de pacotes

**Instalação:**

```bash
# Criar e ativar o ambiente virtual
uv venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate

# Instalar dependências
uv sync

# Instalar o navegador Playwright (Chromium)
uv run playwright install chromium

# Configurar o ambiente e o atalho grpa
uv run setup.py
```

**Executar:**

```bash
# Inicia o executor em modo contínuo (aguarda tarefas da fila)
grpa start

# Executa um ciclo único de teste
grpa test
```

### 2. Com Docker

Ideal para testar o comportamento em um ambiente isolado idêntico ao de produção.

> ⚠️ Certifique-se de que o `.env` está preenchido corretamente antes de continuar (ver [Configuração Manual](#opção-b--configuração-manual)).

```bash
docker-compose up --build
```

Este comando constrói a imagem localmente e sobe o serviço `rpa_executor01`, mapeando as pastas de logs, screenshots e automações para o seu host.

---

## 🏗️ Execução em Produção

Em produção, recomenda-se o uso de imagens pré-construídas para garantir a imutabilidade do ambiente.

### 1. Build da Imagem

```bash
docker build -t grpa_{nome_do_cliente}:latest .
```

### 2. Subindo com Docker Compose (Prod)

O arquivo `docker-compose.prod.yml` está configurado para escalar múltiplos executores usando a mesma imagem base, com volumes e identificadores separados por executor:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Estrutura de volumes em produção:**

```
./logs/GRPAE_001/
./screenshots/GRPAE_001/
./automations/GRPAE_001/    # Para injeção de automações externas, se necessário
```

---

## 📁 Estrutura do Projeto

```
grpa/
├── core/               # Núcleo do sistema (API, Worker, Logger, Browser Automation)
├── automations/        # Automações específicas, separadas por sistema
├── modules/            # Utilitários gerais (XML, DotEnv, Validações, Modelos)
├── logs/               # Logs de execução gerados automaticamente
├── screenshots/        # Capturas de tela automáticas em caso de erro
├── main.py             # Entry point da aplicação
├── setup.py            # Wizard de configuração do ambiente
└── .envexample         # Template de variáveis de ambiente
```

---

## 💡 Desenvolvendo uma Nova Automação

Siga este fluxo para garantir que sua automação seja compatível com o `worker` dinâmico do GRPA.

### 1. Estrutura de Pastas

Crie uma pasta dentro de `automations/` com o nome do sistema alvo:

```
automations/
└── meu_sistema/
    ├── common/       # Módulos reutilizáveis (login, preenchimento de formulários, etc.)
    ├── data/         # Arquivos JSON para simular dados da API localmente
    └── use_cases/    # Entry points da automação
```

### 2. Testes Locais Individuais

Para testar sua automação sem depender da fila da API:

1. Crie um arquivo JSON em `automations/meu_sistema/data/meu_caso.json` com os parâmetros do caso.
2. Execute o use case diretamente via módulo:

```bash
python -m automations.meu_sistema.use_cases.meu_caso
```

---

## 🛡️ Recursos do Boilerplate

- **PlaywrightElement** — Abstração para lidar com seletores e iframes automaticamente, reduzindo código repetitivo.
- **Captura de Evidências** — Screenshots automáticos em caso de falha, enviados para o GOEVO em Base64.
- **Logger Colorido** — Logs organizados por nível (`INFO`, `WARNING`, `ERROR`) e persistidos em arquivo por execução.
- **Auto-Update** — Mecanismo integrado para atualização de módulos via API (ver `core/updater.py`).

---

## 📝 Padrões de Desenvolvimento

- **Nomenclatura:** `snake_case` para arquivos, variáveis e funções.
- **Erros:** Deixe exceções críticas subirem naturalmente — o `Worker` é responsável por capturar, logar e enviar as evidências.
- **Modularização:** Utilize a pasta `common/` para encapsular formulários extensos e fluxos reutilizáveis entre use cases.