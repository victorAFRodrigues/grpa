# GRPA - Goevo Robot Process Automation

O **GRPA** é um ecossistema de automação robótica de processos (RPA) desenvolvido em Python, integrado ao software **GOEVO**. Ele utiliza **Playwright** para automação de navegador e segue uma arquitetura modular focada em escalabilidade, reutilização de código e facilidade de manutenção.

Este repositório serve como um **boilerplate completo** para o desenvolvimento de novas automações.

---

## 🛠️ Configuração do Ambiente

Antes de rodar o projeto em qualquer ambiente, crie um arquivo `.env` na raiz do projeto baseado no `.envexample`:

```bash
cp .envexample .env
```

Preencha as variáveis obrigatórias:
- `API_URL`: URL base da API do GOEVO.
- `GOEVO_APP_TPTOKEN`: Token de autenticação.
- `RPA_EXECUTOR`: Nome identificador deste executor (ex: `GRPAE_001`).
- `GRPA_AUTOMATION_VERSION`: Versão atual das automações.

---

## 🚀 Execução em Desenvolvimento

### 1. Sem Docker (Local)
Ideal para debug e criação de novos scripts onde você precisa ver o navegador funcionando (modo `headless=False`).

**Pré-requisitos:**
- Python 3.14+
- [uv](https://github.com/astral-sh/uv) (Gerenciador de pacotes rápido)

**Setup:**
```bash
# Criar e ativar o ambiente virtual
uv venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate

# Instalar dependências
uv sync

# Instalar o navegador Playwright (Chromium)
uv run playwright install chromium
```

**Rodar a aplicação:**
```bash
uv run main.py
```

### 2. Com Docker
Ideal para testar o comportamento em um ambiente isolado idêntico ao de produção.

**Rodar com Docker Compose:**
```bash
docker-compose up --build
```
*Este comando irá construir a imagem localmente e subir o serviço `rpa_executor01` mapeando as pastas de logs, screenshots e automações para o seu host.*

---

## 🏗️ Execução em Produção

Em produção, recomenda-se o uso de imagens pré-construídas para garantir a imutabilidade do ambiente.

### 1. Build da Imagem
Construa a imagem Docker com uma tag específica:
```bash
docker build -t grpa_lelac:latest .
```

### 2. Subindo com Docker Compose (Prod)
O arquivo `docker-compose.prod.yml` está configurado para escalar múltiplos executores usando a mesma imagem base, mas com volumes e identificadores separados.

```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Estrutura de Volumes em Produção:**
Os logs e screenshots serão organizados por executor na raiz do projeto:
- `./logs/GRPAE_001/`
- `./screenshots/GRPAE_001/`
- `./automations/GRPAE_001/` (Se necessário injetar automações externamente)

---

## 📁 Estrutura do Projeto

- `core/`: Núcleo do sistema (API, Worker, Logger, Browser Automation).
- `automations/`: Onde residem as automações específicas (separadas por sistema).
- `modules/`: Utilitários gerais (XML, DotEnv, Validações, Modelos).
- `logs/`: Logs de execução gerados automaticamente.
- `screenshots/`: Capturas de tela automáticas em caso de erro.

---

## 💡 Desenvolvendo uma Nova Automação

Siga este fluxo para garantir que sua automação seja compatível com o `worker` dinâmico do GRPA.

### 1. Estrutura de Pastas
Crie uma pasta dentro de `automations/` com o nome do sistema alvo (ex: `meu_sistema`):

```filesystem
automations/
   meu_sistema/
        common/          # Módulos reutilizáveis (login, preenchimento de capas, etc)
        data/            # Arquivos JSON para simular dados da API localmente
        use_cases/       # Entry points da automação
```

### 2. Testes Locais Individuais
Para testar sua automação sem depender da fila da API:
1. Crie um arquivo JSON em `automations/meu_sistema/data/meu_caso.json`.
2. Execute o arquivo do use case diretamente via módulo:
   ```bash
   python -m automations.meu_sistema.use_cases.meu_caso
   ```

---

## 🛡️ Recursos do Boilerplate

- **PlaywrightElement**: Abstração para lidar com seletores e **iframes** automaticamente.
- **Captura de Evidências**: Screenshots automáticos em caso de falha, enviados para o GOEVO em Base64.
- **Logger Colorido**: Logs organizados por nível e persistidos em arquivo.
- **Auto-Update**: Mecanismo integrado para atualização de módulos (ver `core/updater.py`).

---

## 📝 Padrões de Desenvolvimento
- **Nomenclatura:** `snake_case` para tudo.
- **Erros:** Deixe exceções críticas subirem; o `Worker` cuida do log e evidência.
- **Performance:** Utilize `common/` para modularizar formulários extensos.
